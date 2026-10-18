"""Validate the chimera-skills catalogue. Reads files only; never executes anything it inspects.

    python scripts/check.py                    # all checks; Chimera's parser if it is importable
    python scripts/check.py --require-chimera  # CI: fail when the parser cannot be imported
    python scripts/check.py --print-tree-hash skills/<id>   # the hash a review must record

Every rule here exists because "public on GitHub" is not "safe to hand to an agent". The catalogue
is curation, not approval: Chimera still imports each skill pending and tainted. This script is
what keeps the curation honest — licence read, source pinned, every vendored byte accounted for,
and a review that names exactly the content it reviewed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
CATALOG = ROOT / "catalog"
REVIEWS = ROOT / "reviews"

ALLOWED_SPDX = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "MPL-2.0", "CC0-1.0"}
OWN_LICENSE = "Apache-2.0"
MODES = {"own", "include", "adapt"}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MAX_SKILL_LINES = 500
MAX_DESCRIPTION = 1024

SCRIPT_EXT = {".sh", ".bash", ".zsh", ".ps1", ".bat", ".cmd", ".py", ".js", ".mjs", ".cjs", ".ts", ".rb", ".pl"}

# (rule, regex, flags). Matched line by line over every file inside a skill directory.
TEXT_RULES: list[tuple[str, str, int]] = [
    ("pipe-to-shell", r"\b(curl|wget|iwr|invoke-webrequest)\b[^\n|]*\|\s*(sudo\s+)?(ba|z|da)?sh\b", re.I),
    ("pipe-to-shell", r"\|\s*iex\b", re.I),
    ("privilege-escalation", r"(^|[\s`$(])sudo\s", 0),
    ("reader-directed", r"\b(ignore|disregard|forget)\s+(all\s+|any\s+)?(the\s+)?(previous|prior|above|earlier)\s+(instructions|prompts?|rules)", re.I),
    ("reader-directed", r"\bdo\s+not\s+(tell|inform)\s+the\s+user\b|\bwithout\s+(telling|informing)\s+the\s+user\b", re.I),
    ("reader-directed", r"\b(reviewer|maintainer|approver)s?\b[^\n]{0,40}\b(approve|merge|skip (the )?review)\b", re.I),
    ("dominating-trigger", r"\bbefore\s+(any|every|each)\s+(response|reply|answer|message|turn)\b", re.I),
    ("dominating-trigger", r"\b(on|in|at)\s+(every|each)\s+(turn|response|reply|message)\b", re.I),
    ("dominating-trigger", r"\b(always|must)\s+(use|invoke|load|run|consult|check)\s+this\s+skill\b", re.I),
    ("dominating-trigger", r"\bYOU\s+(ABSOLUTELY\s+)?MUST\b|\bMANDATORY\b|\bNEVER\s+CALL\b", 0),
]
GLOBAL_INSTALL = re.compile(r"\b(npm|pnpm|yarn|bun)\s+(install|i|add|global\s+add)\b(?P<args>[^\n`]*)", re.I)
SCRIPT_RULES: list[tuple[str, str]] = [
    ("script-network", r"requests\.|urllib|http\.client|\bfetch\(|axios|\bcurl\b|\bwget\b|socket\.|Invoke-WebRequest"),
    ("script-shell", r"subprocess|os\.system|child_process|\bexec\(|\bspawn\(|\beval\("),
]


@dataclass
class Finding:
    path: str
    line: int
    rule: str
    text: str


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tree_hash(skill_dir: Path) -> str:
    """One hash over every file in the skill (relative path + content). A review records it."""
    h = hashlib.sha256()
    for f in sorted(p for p in skill_dir.rglob("*") if p.is_file()):
        rel = f.relative_to(skill_dir).as_posix()
        h.update(rel.encode() + b"\0" + sha256_bytes(f.read_bytes()).encode() + b"\n")
    return h.hexdigest()


def split_frontmatter(text: str) -> tuple[dict | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    try:
        loaded = yaml.safe_load(text[4:end])
    except yaml.YAMLError:
        return None, text
    return (loaded if isinstance(loaded, dict) else None), text[end + 4 :]


def _all_keys(obj: object) -> list[str]:
    if isinstance(obj, dict):
        return [str(k) for k in obj] + [k for v in obj.values() for k in _all_keys(v)]
    if isinstance(obj, list):
        return [k for v in obj for k in _all_keys(v)]
    return []


def csv_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v.strip()]
    return []


class Checker:
    def __init__(self, require_chimera: bool) -> None:
        self.errors: list[str] = []
        self.require_chimera = require_chimera
        self.categories = {c["id"] for c in yaml.safe_load((ROOT / "categories.yaml").read_text("utf-8"))["categories"]}
        if len(self.categories) != 26:
            self.err("categories.yaml", f"expected the 26 canonical categories, found {len(self.categories)}")
        self.lock: dict[str, dict] = json.loads((ROOT / "upstream.lock").read_text("utf-8"))
        self.notice = (ROOT / "NOTICE").read_text("utf-8")
        self.exceptions = json.loads((ROOT / "security-exceptions.json").read_text("utf-8"))["exceptions"]
        self.used_exceptions: set[int] = set()
        self.parser = self._load_parser()

    def err(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def _load_parser(self):  # noqa: ANN202 - optional dependency
        try:
            from chimera.skills import skill_md  # type: ignore[import-not-found]
        except Exception:  # noqa: BLE001 - any import failure means "not available"
            if self.require_chimera:
                self.err("chimera", "chimera.skills.skill_md is not importable and --require-chimera was given")
            return None
        return skill_md

    # ---------------------------------------------------------------- repo level
    def check_repo(self) -> None:
        lic = (ROOT / "LICENSE").read_text("utf-8") if (ROOT / "LICENSE").exists() else ""
        if "Apache License" not in lic or "Version 2.0" not in lic:
            self.err("LICENSE", "repository LICENSE must be Apache-2.0")
        ids = {p.name for p in SKILLS.iterdir() if p.is_dir()}
        for lock_id in self.lock:
            if lock_id not in ids:
                self.err("upstream.lock", f"entry '{lock_id}' has no skills/{lock_id}/")
        for folder, suffix in ((CATALOG, ".json"), (REVIEWS, ".md")):
            for f in folder.glob(f"*{suffix}"):
                if f.stem not in ids:
                    self.err(f"{folder.name}/{f.name}", "orphan: no matching skill")

    # ---------------------------------------------------------------- per skill
    def check_skill(self, d: Path) -> None:
        sid = d.name
        where = f"skills/{sid}"
        skill_md = d / "SKILL.md"
        if not skill_md.exists():
            self.err(where, "missing SKILL.md")
            return
        text = skill_md.read_text("utf-8")
        if "\r\n" in text:
            self.err(where, "SKILL.md must use LF line endings")
        if text.count("\n") > MAX_SKILL_LINES:
            self.err(where, f"SKILL.md over {MAX_SKILL_LINES} lines; move detail to references/")
        front, body = split_frontmatter(text)
        if front is None:
            self.err(where, "frontmatter missing or not valid YAML mapping")
            return
        meta = front.get("metadata") if isinstance(front.get("metadata"), dict) else {}
        mode = str(meta.get("mode", ""))
        self._check_frontmatter(where, sid, front, meta, mode)
        if mode == "own":
            self._check_own(where, sid, d, meta)
        elif mode in {"include", "adapt"}:
            self._check_upstream(where, sid, d, front, meta, mode)
        self._check_catalog(sid, front, meta, mode)
        self._check_review(sid, d, mode)
        self._scan_security(d)
        self._check_with_chimera(where, sid, text, front)
        if not body.strip():
            self.err(where, "SKILL.md has no instructions body")

    def _check_frontmatter(self, where: str, sid: str, front: dict, meta: dict, mode: str) -> None:
        name = front.get("name")
        if name != sid or not isinstance(name, str) or not NAME_RE.match(name) or len(name) > 64:
            self.err(where, f"name must equal the folder name, kebab-case, <=64 chars (got {name!r})")
        desc = front.get("description")
        if not isinstance(desc, str) or not desc.strip():
            self.err(where, "description is required")
        elif len(desc) > MAX_DESCRIPTION:
            self.err(where, f"description over {MAX_DESCRIPTION} chars")
        if front.get("license") not in ALLOWED_SPDX:
            self.err(where, f"license {front.get('license')!r} not in allowlist {sorted(ALLOWED_SPDX)}")
        if not meta:
            self.err(where, "metadata block missing")
            return
        if mode not in MODES:
            self.err(where, f"metadata.mode must be one of {sorted(MODES)}")
        cat = meta.get("category")
        if cat not in self.categories:
            self.err(where, f"metadata.category {cat!r} is not one of the 26 categories")
        sec = csv_list(meta.get("categories_secondary"))
        if len(sec) > 3:
            self.err(where, "at most 3 secondary categories")
        for s in sec:
            if s not in self.categories or s == cat:
                self.err(where, f"secondary category {s!r} unknown or equal to the primary")
        if not csv_list(meta.get("tags")):
            self.err(where, "metadata.tags must list at least one tag")

    def _check_own(self, where: str, sid: str, d: Path, meta: dict) -> None:
        if sid in self.lock:
            self.err(where, "mode own but listed in upstream.lock")
        if any(k.startswith("upstream_") for k in meta):
            self.err(where, "mode own must not carry upstream_* metadata")
        lic_files = [p for p in d.iterdir() if p.name.startswith("LICENSE")]
        if lic_files:
            self.err(where, "own skills are covered by the repository LICENSE; remove the per-skill LICENSE")

    def _check_upstream(self, where: str, sid: str, d: Path, front: dict, meta: dict, mode: str) -> None:
        entry = self.lock.get(sid)
        if entry is None:
            self.err(where, f"mode {mode} requires an upstream.lock entry")
            return
        if not SHA_RE.match(str(entry.get("sha", ""))):
            self.err("upstream.lock", f"{sid}: sha must be a full 40-hex commit")
        if entry.get("spdx") not in ALLOWED_SPDX:
            self.err("upstream.lock", f"{sid}: spdx {entry.get('spdx')!r} not allowed")
        if entry.get("mode") != mode:
            self.err(where, f"metadata.mode {mode} != upstream.lock mode {entry.get('mode')}")
        for key, lkey in (("upstream_repo", "repo"), ("upstream_path", "path"), ("upstream_sha", "sha"),
                          ("upstream_license", "spdx")):
            if str(meta.get(key)) != str(entry.get(lkey)):
                self.err(where, f"metadata.{key} does not match upstream.lock {lkey}")
        if front.get("license") != entry.get("spdx"):
            self.err(where, "frontmatter license must equal the upstream SPDX id")
        if not meta.get("changes"):
            self.err(where, "metadata.changes must state what was modified (Apache-2.0 s.4(b))")
        files = entry.get("files", {})
        if not any(Path(k).name.startswith("LICENSE") for k in files):
            self.err(where, "upstream LICENSE file must be vendored next to the skill")
        present = {p.relative_to(d).as_posix(): p for p in d.rglob("*") if p.is_file()}
        for rel, digest in files.items():
            if rel not in present:
                self.err(where, f"lock lists {rel} but it is missing")
            elif sha256_bytes(present[rel].read_bytes()) != digest:
                self.err(where, f"{rel} differs from the reviewed copy (update upstream.lock and the review)")
        for rel in present:
            if rel not in files:
                self.err(where, f"{rel} is not accounted for in upstream.lock")
        if sid not in self.notice or str(entry.get("repo")) not in self.notice:
            self.err("NOTICE", f"missing attribution for {sid} ({entry.get('repo')})")

    def _check_catalog(self, sid: str, front: dict, meta: dict, mode: str) -> None:
        where = f"catalog/{sid}.json"
        path = CATALOG / f"{sid}.json"
        if not path.exists():
            self.err(where, "missing")
            return
        cat = json.loads(path.read_text("utf-8"))
        expected = {
            "id": sid,
            "category": meta.get("category"),
            "categories_secondary": csv_list(meta.get("categories_secondary")),
            "tags": csv_list(meta.get("tags")),
            "license": front.get("license"),
            "mode": mode,
        }
        for key, value in expected.items():
            if cat.get(key) != value:
                self.err(where, f"{key} {cat.get(key)!r} != SKILL.md {value!r}")
        if not isinstance(cat.get("featured"), bool):
            self.err(where, "featured must be true or false")
        for key in ("title", "summary", "executes"):
            if not isinstance(cat.get(key), dict) or not cat[key].get("pt-BR") or not cat[key].get("en"):
                self.err(where, f"{key} needs pt-BR and en text")
        if any(re.search(r"install(s|_?count|ations)|downloads|instala", k, re.I) for k in _all_keys(cat)):
            self.err(where, "no install counts: Chimera has no telemetry and nobody publishes per-skill counts")
        source = cat.get("source")
        if mode == "own":
            if source is not None:
                self.err(where, "own skills have source null")
            return
        entry = self.lock.get(sid, {})
        if not isinstance(source, dict):
            self.err(where, "source object required for upstream skills")
            return
        if source.get("repo") != entry.get("repo") or source.get("sha") != entry.get("sha"):
            self.err(where, "source repo/sha must match upstream.lock")
        if not isinstance(source.get("stars"), int) or not DATE_RE.match(str(source.get("stars_read_at", ""))):
            self.err(where, "stars must be an integer with stars_read_at as YYYY-MM-DD")

    def _check_review(self, sid: str, d: Path, mode: str) -> None:
        where = f"reviews/{sid}.md"
        path = REVIEWS / f"{sid}.md"
        if not path.exists():
            self.err(where, "missing")
            return
        text = path.read_text("utf-8")
        fields = dict(re.findall(r"^- \*\*(.+?):\*\* `?([^`\n]+?)`?\s*$", text, re.M))
        if not DATE_RE.match(fields.get("Date", "")):
            self.err(where, "Date: YYYY-MM-DD required")
        if not fields.get("Reviewer"):
            self.err(where, "Reviewer required")
        if fields.get("Content sha256") != tree_hash(d):
            self.err(where, "Content sha256 does not match the skill as it is now: re-review required")
        if mode != "own" and fields.get("Upstream sha") != self.lock.get(sid, {}).get("sha"):
            self.err(where, "Upstream sha must equal the pinned sha in upstream.lock")
        if "- [ ]" in text:
            self.err(where, "unchecked checklist item")
        if text.count("- [x]") < 8:
            self.err(where, "security checklist incomplete (expected at least 8 checked items)")

    # ---------------------------------------------------------------- security
    def _excepted(self, rel: str, rule: str, line: str) -> bool:
        for i, ex in enumerate(self.exceptions):
            if ex["file"] == rel and ex["rule"] == rule and ex["contains"] in line:
                self.used_exceptions.add(i)
                return True
        return False

    def _scan_security(self, d: Path) -> None:
        findings: list[Finding] = []
        for f in sorted(p for p in d.rglob("*") if p.is_file()):
            rel = f.relative_to(ROOT).as_posix()
            raw = f.read_bytes()
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                findings.append(Finding(rel, 0, "binary-file", "skills ship text only"))
                continue
            is_script = f.suffix.lower() in SCRIPT_EXT or text.startswith("#!")
            if is_script:
                findings.append(Finding(rel, 1, "script-present", "skills here ship no executable files"))
            for n, line in enumerate(text.splitlines(), 1):
                for rule, pattern, flags in TEXT_RULES:
                    if re.search(pattern, line, flags):
                        findings.append(Finding(rel, n, rule, line.strip()[:160]))
                m = GLOBAL_INSTALL.search(line)
                if m and re.search(r"(^|\s)(-g|--global)(\s|$)", m.group("args")):
                    pkgs = [t for t in m.group("args").split() if not t.startswith("-")]
                    if not pkgs or any(not re.search(r"@\d", t) for t in pkgs):
                        findings.append(Finding(rel, n, "unpinned-global-install", line.strip()[:160]))
                if is_script:
                    for rule, pattern in SCRIPT_RULES:
                        if re.search(pattern, line):
                            findings.append(Finding(rel, n, rule, line.strip()[:160]))
        for fd in findings:
            if not self._excepted(fd.path, fd.rule, fd.text):
                self.err(f"{fd.path}:{fd.line}", f"[{fd.rule}] {fd.text}")

    def _check_with_chimera(self, where: str, sid: str, text: str, front: dict) -> None:
        if self.parser is None:
            return
        parsed = self.parser.untrusted(self.parser.parse_skill_md(text))
        m = parsed.manifest
        if m.name != sid:
            self.err(where, f"Chimera parser read name {m.name!r}")
        if not m.description.strip():
            self.err(where, "Chimera parser read an empty description")
        if m.license != front.get("license"):
            self.err(where, f"Chimera parser read license {m.license!r}")
        if front.get("stage") and m.stage != front.get("stage"):
            self.err(where, f"stage {front.get('stage')!r} is not in Chimera's vocabulary")
        if front.get("topic") and m.topic != front.get("topic"):
            self.err(where, f"topic {front.get('topic')!r} is not in Chimera's vocabulary")
        if m.status != "pending" or m.provenance != "tainted":
            self.err(where, "untrusted() must hold the skill pending and tainted")
        if not parsed.instructions.strip():
            self.err(where, "Chimera parser read no instructions")

    def finish(self) -> int:
        for i, ex in enumerate(self.exceptions):
            if i not in self.used_exceptions:
                self.err("security-exceptions.json", f"stale exception (nothing matches): {ex}")
        return 0 if not self.errors else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--require-chimera", action="store_true")
    ap.add_argument("--print-tree-hash", metavar="SKILL_DIR")
    args = ap.parse_args()
    if args.print_tree_hash:
        print(tree_hash(ROOT / args.print_tree_hash))
        return 0
    c = Checker(args.require_chimera)
    c.check_repo()
    dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    for d in dirs:
        c.check_skill(d)
    code = c.finish()
    parser_note = "Chimera parser: used" if c.parser else "Chimera parser: not available (skipped)"
    if code:
        print("\n".join(c.errors))
        print(f"\nFAIL: {len(c.errors)} problem(s) across {len(dirs)} skills. {parser_note}.")
    else:
        print(f"OK: {len(dirs)} skills, {len(c.lock)} pinned upstream, "
              f"{len(c.used_exceptions)} reviewed exception(s). {parser_note}.")
    return code


if __name__ == "__main__":
    sys.exit(main())
