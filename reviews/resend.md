# Review: resend

- **Reviewer:** Claude Opus 5.5 (agent, for Bruno Campidelli) — pending human sign-off
- **Date:** 2026-10-17
- **Mode:** include
- **License:** MIT
- **Upstream:** https://github.com/resend/resend-skills/tree/b2ae7b1798b70134faf679f35fc05b4331462988/skills/resend
- **Upstream sha:** `b2ae7b1798b70134faf679f35fc05b4331462988`
- **License file read:** `LICENSE` at that sha
- **Content sha256:** `2e890f68a2124f4513e62289072c4ac7c01fe97bd80ae4d1c1f04f940b112978`

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

references/fetch-all-templates.mjs omitted (executable); templates.md still mentions it. references/webhooks.md shows a local tunnel command with elevated privileges for the developer: kept verbatim under a reviewed exception; the agent should not run it.
