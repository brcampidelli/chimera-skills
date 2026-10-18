# Review: pdf

- **Reviewer:** Claude Opus 5.5 (AI agent). Human sign-off by the owner: pending
- **Human sign-off:** pending (first wave reviewed by an AI agent; the owner has not signed yet)
- **Date:** 2026-10-17
- **Mode:** adapt
- **License:** Apache-2.0
- **Upstream:** https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/pdf
- **Upstream sha:** `49f948faa9258a0c61caceaf225e179651397431`
- **License file read:** `skills/.curated/pdf/LICENSE.txt` at that sha
- **Content sha256:** `5f954b9f4d7871197149e015791b668ca65e701edd12c93d14651a65e0a3b7de`

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

ADAPTED: the privileged apt-get line was replaced by asking the user to install poppler-utils. pip/uv installs pinned to reportlab==5.0.1, pdfplumber==0.11.10, pypdf==6.21.1 (current on 2026-10-17). Legal substitute for Anthropic's proprietary pdf skill (not read).
