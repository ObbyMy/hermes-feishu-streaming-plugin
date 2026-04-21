---
name: hermes-feishu-weixin-streaming-migration-kit
description: Transfer the OpenClaw-style Feishu streaming-card and Weixin duplicate-suppression workflow to another Hermes repo, with modified files, upgrade locators, patch references, and verification commands.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, feishu, weixin, gateway, streaming, migration, transfer, patch, skill]
    related_skills: [hermes-agent, hermes-feishu-gateway-setup, hermes-gateway-streaming-debugging, systematic-debugging]
---

# Hermes Feishu / Weixin Streaming Migration Kit

Use this skill when you want another Hermes instance to reproduce the **OpenClaw-style optimized Feishu streaming card workflow** that was already implemented and verified here.

## What this skill transfers

This bundle preserves the full migration package, not just a loose patch:

- modified source files
- regression tests
- migration patch
- rationale docs
- future-upgrade locator map

## Read these files first

- `references/modified-files.md` — exact changed files, why they changed, and which anchors to search later
- `references/upgrade-locator.md` — how to find the same touchpoints after Hermes upstream changes
- `references/modification-map.json` — machine-readable locator manifest
- `references/feishu-format-calls.md` — `_hermes_stream` metadata contract and card rendering rules
- `references/migration-steps.md` — copy/apply workflow
- `references/verification.md` — focused pytest commands

## Core behavior that must survive the migration

### Feishu

1. One active stream/card path instead of preview bubble + standalone tool bubble + final bubble.
2. Tool progress embedded into the active stream card.
3. Metadata-only updates must still trigger an edit.
4. Session-reset / session-switch / context-pressure notices use the same low-noise card path.
5. Generic file attachments with caption send **caption first, file second**.

### Weixin

1. Do not preserve fake streaming UX on a transport that cannot truly edit.
2. Suppress the duplicate preview/tool-progress path and rely on the final reply.

## Fastest transfer modes

### Option A — export and send the whole bundle

Use the standalone repo CLI:

```bash
python -m hermes_feishu_streaming_plugin export --output-dir ./dist
```

Then share the exported directory or archive.

### Option B — scan the target repo before merging

```bash
python -m hermes_feishu_streaming_plugin locate --target /path/to/hermes-agent
```

Use this before manual merge whenever the target Hermes version may have drifted.

### Option C — patch the target repo

From the target Hermes repo root:

```bash
git apply migration.patch
source venv/bin/activate
python -m pytest tests/gateway/test_stream_consumer.py tests/gateway/test_run_progress_topics.py tests/gateway/test_weixin.py tests/gateway/test_feishu.py -q
```

### Option D — copy files directly

Copy everything under `files/` into the target repo root, preserving relative paths.

## Minimum acceptance checklist

- Feishu tool execution shows one live card, not fragmented bubbles
- tool completion clears `tool_status`
- final answer edits back into the same stream/card path
- context/session notices use card styling
- Weixin no longer emits preview/tool/final duplicates
- focused pytest suite passes

## Pitfalls

- Do not deduplicate edits by text alone; metadata changes must still flush.
- Do not append the stream cursor to `"\u200b"` placeholder bodies.
- Do not keep standalone tool-progress enabled on Weixin if the transport cannot edit.
- Do not blindly preserve line numbers from the old patch; preserve behavior instead.
- Do not use `post + media` for generic file attachments with caption on Feishu.

## Handoff template

```text
Load the bundle or standalone repository for `hermes-feishu-weixin-streaming-migration-kit`. Read `references/modified-files.md`, `references/upgrade-locator.md`, and `references/verification.md`. Run the locator against the target Hermes repo first. Then apply the patch or copy the bundled files while preserving relative paths. Finally report: files changed, which anchors moved, exact pytest results, and any remaining merge risks.
```
