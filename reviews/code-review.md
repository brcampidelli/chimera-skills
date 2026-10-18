# Review: code-review

- **Reviewer:** Claude Opus 5.5 (AI agent). Human sign-off by the owner: pending
- **Human sign-off:** pending (first wave reviewed by an AI agent; the owner has not signed yet)
- **Date:** 2026-10-17
- **Mode:** include
- **License:** MIT
- **Upstream:** https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/engineering/code-review
- **Upstream sha:** `49dd158d1076134a641b33efb035946536778336`
- **License file read:** `LICENSE` at that sha
- **Content sha256:** `ce8291f7b5b0221cb36a295ed090ecabfc5c62eab005776943d3323eeeb67d35`

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

agents/openai.yaml omitted. Uses sub-agents if the host supports them.
