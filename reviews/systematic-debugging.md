# Review: systematic-debugging

- **Reviewer:** Claude Opus 5.5 (AI agent). Human sign-off by the owner: pending
- **Human sign-off:** pending (first wave reviewed by an AI agent; the owner has not signed yet)
- **Date:** 2026-10-17
- **Mode:** adapt
- **License:** MIT
- **Upstream:** https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/systematic-debugging
- **Upstream sha:** `bb92a77741419a4ab5f06e711a283343f1ada0c3`
- **License file read:** `LICENSE` at that sha
- **Content sha256:** `d7caeeb2233b646580235c58f2d9a677c03e54d8d099eac0f13c6cc77f3f39a7`

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

ADAPTED: find-polluter.sh and condition-based-waiting-example.ts omitted (executable); root-cause-tracing.md now describes manual bisection and condition-based-waiting.md points to upstream at the pinned commit, so nothing references a missing file. test-pressure-*.md are upstream skill-testing scenarios, kept verbatim.
