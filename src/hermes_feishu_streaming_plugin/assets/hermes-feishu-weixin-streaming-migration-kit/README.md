# Hermes Feishu / Weixin Streaming Migration Kit

This is a transferable bundle for another Hermes repo or another Hermes operator.

Contents:
- `SKILL.md` — installable/readable skill instructions
- `references/` — migration steps, Feishu format calls, modified file list, verification, patch
- `files/` — current modified files copied with relative paths preserved

Quick use in another Hermes repo:
1. Read `SKILL.md`
2. Apply `references/migration.patch` or copy `files/` into the repo root preserving paths
3. Run commands from `references/verification.md`
