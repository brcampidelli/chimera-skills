# Review: mcp-builder

- **Reviewer:** Claude Opus 5.5 (agent, for Bruno Campidelli) — pending human sign-off
- **Date:** 2026-10-17
- **Mode:** include
- **License:** Apache-2.0
- **Upstream:** https://github.com/anthropics/skills/tree/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/mcp-builder
- **Upstream sha:** `dbd4588f9e1033efb41dad4bef2f7947c8993d44`
- **License file read:** `skills/mcp-builder/LICENSE.txt` at that sha
- **Content sha256:** `7ddeaefa4bd39e7bf834c75b11196cfe170243ea9d93c38c4c73d9ed72e4a419`

## Checklist

- [x] Licence read in the file itself (not the README or a badge) and is on the allowlist
- [x] Source pinned to a full commit sha (or own content under the repository Apache-2.0)
- [x] No executable files shipped in the skill directory
- [x] No pipe-to-shell installs, unpinned global installs or privilege escalation (or a reviewed exception)
- [x] No sentences directed at the agent or reviewer to skip review, hide things or drop prior instructions (or a reviewed exception)
- [x] Trigger describes when the skill applies; it does not claim every turn
- [x] Network use, if any, is the user's own service under Chimera governance; nothing sends code or data to a third party
- [x] Actions with money, production or access stay with a human
- [x] Imports into Chimera pending and tainted

## Notes

scripts/ (connections.py, evaluation.py, example XML, requirements.txt) omitted: the evaluation harness calls a vendor API. reference/evaluation.md still describes running it; use Chimera's own eval tooling instead.
