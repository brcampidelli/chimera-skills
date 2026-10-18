# Review: resend

- **Reviewer:** Claude Opus 5.5 (AI agent). Human sign-off by the owner: pending
- **Human sign-off:** pending (first wave reviewed by an AI agent; the owner has not signed yet)
- **Date:** 2026-10-17
- **Mode:** adapt
- **License:** MIT
- **Upstream:** https://github.com/resend/resend-skills/tree/b2ae7b1798b70134faf679f35fc05b4331462988/skills/resend
- **Upstream sha:** `b2ae7b1798b70134faf679f35fc05b4331462988`
- **License file read:** `LICENSE` at that sha
- **Content sha256:** `31a9d702b685f0e9c745c026c9df1bf4d9c49b8954e0d409995679843d1be95d`

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

ADAPTED: references/fetch-all-templates.mjs omitted (executable) and the templates.md pointer to it replaced by a pagination description; the webhooks.md tunnel commands (one used sudo) replaced by a pointer to the tools' official docs, which removed the former security exception; the Python install in installation.md pinned to resend==2.50.0.
