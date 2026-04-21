# Hermes Feishu / Weixin Streaming Migration Kit

This bundle is the portable payload inside the standalone skill repository.

It preserves four things together:

1. **the modified Hermes files** (`files/`)
2. **the migration instructions** (`SKILL.md`)
3. **the reasoning and verification docs** (`references/`)
4. **the future upgrade locator map** (`references/upgrade-locator.md`, `references/modification-map.json`)

## Contents

- `SKILL.md` — installable/readable skill instructions
- `references/modified-files.md` — what changed, why, and where to look again later
- `references/upgrade-locator.md` — how to relocate touchpoints after Hermes upstream updates
- `references/modification-map.json` — machine-readable anchor map for the locator CLI
- `references/migration.patch` — patch form of the migration
- `references/verification.md` — focused regression commands
- `files/` — copied source/test/docs files with original relative paths preserved

## Quick use

1. Read `SKILL.md`
2. Use the standalone repo CLI to inspect or export the bundle
3. Run `locate --target /path/to/hermes-agent` before merging into a newer Hermes tree
4. Apply `references/migration.patch` or copy `files/` into the repo root preserving paths
5. Run commands from `references/verification.md`
