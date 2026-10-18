# Review: systematic-debugging

- **Reviewer:** Claude Opus 5.5 (agent, for Bruno Campidelli) — pending human sign-off
- **Date:** 2026-10-17
- **Mode:** include
- **License:** MIT
- **Upstream:** https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/systematic-debugging
- **Upstream sha:** `bb92a77741419a4ab5f06e711a283343f1ada0c3`
- **License file read:** `LICENSE` at that sha
- **Content sha256:** `ed6079d1b22d62f42feb1dd0e3f6b2bed58b6c9f0fe4924900b82439af4bca8c`

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

find-polluter.sh and condition-based-waiting-example.ts omitted (executable); root-cause-tracing.md and condition-based-waiting.md still mention them. test-pressure-*.md are upstream skill-testing scenarios, kept verbatim.
