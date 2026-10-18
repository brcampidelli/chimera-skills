# Review: stripe-best-practices

- **Reviewer:** Claude Opus 5.5 (agent, for Bruno Campidelli) — pending human sign-off
- **Date:** 2026-10-17
- **Mode:** adapt
- **License:** MIT
- **Upstream:** https://github.com/stripe/ai/tree/c1f5b0826f3f33d7e1cc7eff5e5e6cd42749808b/providers/claude/plugin/skills/stripe-best-practices
- **Upstream sha:** `c1f5b0826f3f33d7e1cc7eff5e5e6cd42749808b`
- **License file read:** `LICENSE` at that sha
- **Content sha256:** `2893821ade949ed9caf714460b8e0899fb64a9a2a90e529787afa3653b76caf1`

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

ADAPTED: the upstream line installing the Stripe CLI with an unpinned global npm command was replaced by a pointer to the official install docs. Version numbers in the skill (API/SDK versions) are upstream's as of the pinned sha.
