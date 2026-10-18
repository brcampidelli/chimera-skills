# Review: improve-codebase-architecture

- **Reviewer:** Claude Opus 5.5 (agent, for Bruno Campidelli) — pending human sign-off
- **Date:** 2026-10-17
- **Mode:** include
- **License:** MIT
- **Upstream:** https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/improve-codebase-architecture
- **Upstream sha:** `49dd158d1076134a641b33efb035946536778336`
- **License file read:** `LICENSE` at that sha
- **Content sha256:** `75f51aa3e52a45fed9c53dae85ca423ed9c7a0d651a0c22ad449a9607ffea905`

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

disable-model-invocation: true kept. Writes an HTML report file when used.
