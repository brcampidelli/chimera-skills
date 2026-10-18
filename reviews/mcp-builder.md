# Review: mcp-builder

- **Reviewer:** Claude Opus 5.5 (AI agent). Human sign-off by the owner: pending
- **Human sign-off:** pending (first wave reviewed by an AI agent; the owner has not signed yet)
- **Date:** 2026-10-17
- **Mode:** adapt
- **License:** Apache-2.0
- **Upstream:** https://github.com/anthropics/skills/tree/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/mcp-builder
- **Upstream sha:** `dbd4588f9e1033efb41dad4bef2f7947c8993d44`
- **License file read:** `skills/mcp-builder/LICENSE.txt` at that sha
- **Content sha256:** `a4f591d0953769e87b1fd7868734707104bc3441a2c10129eb4e58cd46313394`

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

ADAPTED: scripts/ (connections.py, evaluation.py, example XML, requirements.txt) omitted because the harness calls a vendor API; the 'Running Evaluations' part of reference/evaluation.md was replaced by a short note pointing to your own eval tooling, and SKILL.md no longer mentions the provided scripts.
