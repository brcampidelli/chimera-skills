# Review: pdf

- **Reviewer:** Claude Opus 5.5 (agent, for Bruno Campidelli) — pending human sign-off
- **Date:** 2026-10-17
- **Mode:** adapt
- **License:** Apache-2.0
- **Upstream:** https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/pdf
- **Upstream sha:** `49f948faa9258a0c61caceaf225e179651397431`
- **License file read:** `skills/.curated/pdf/LICENSE.txt` at that sha
- **Content sha256:** `15c38b657067e58850a2f420579828bc6eaf3c9540b5e3db959f7b5f5b8236c3`

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

ADAPTED: the privileged apt-get line was replaced by asking the user to install poppler-utils. pip/uv installs in the skill are unpinned package names: pin them in the project when used. Legal substitute for Anthropic's proprietary pdf skill (not read).
