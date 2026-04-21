---
name: hermes-feishu-weixin-streaming-migration-kit
description: Transfer Hermes Feishu/Weixin streaming-card and tool-progress fixes to another Hermes repo using a ready-made bundle of modified files, migration patch, Feishu payload conventions, and verification commands.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, feishu, weixin, gateway, streaming, migration, transfer, patch]
    related_skills: [hermes-agent, hermes-feishu-gateway-setup, hermes-gateway-streaming-debugging, systematic-debugging]
---

# Hermes Feishu / Weixin Streaming Migration Kit

Use this when you want to hand another Hermes instance a **drop-in migration pack** for the gateway changes that fixed:

- Feishu single-card streaming and embedded tool progress
- Feishu interactive-card formatting and fallback behavior
- Weixin duplicate preview/tool-progress suppression
- session-reset / session-notice Feishu card rendering
- context-pressure Feishu card rendering
- document+caption send behavior on Feishu

## What this skill gives you

Load this skill, then use its bundled reference files:

- `references/modified-files.md` — exact changed files and why they changed
- `references/feishu-format-calls.md` — Feishu `_hermes_stream` metadata contract and rendering rules
- `references/migration-steps.md` — copy/apply workflow for another Hermes repo
- `references/migration.patch` — ready-to-apply git patch
- `references/verification.md` — focused pytest commands
- `references/transfer-bundle-path.txt` — local export bundle path

## Fastest transfer options

### Option A: send the whole bundle
Send the exported directory or tarball to the other Hermes/user. The bundle includes:

- modified source files
- modified tests
- docs
- migration patch
- skill instructions

### Option B: apply the patch in another Hermes repo
From the target Hermes repo root:

```bash
git apply migration.patch
source venv/bin/activate
python -m pytest tests/gateway/test_stream_consumer.py tests/gateway/test_run_progress_topics.py tests/gateway/test_weixin.py tests/gateway/test_feishu.py -q
```

### Option C: copy files directly
If patching is inconvenient, copy files from the bundle's `files/` subtree into the target repo root, preserving paths.

## Core migration behavior to preserve

### Feishu

1. Adapter capabilities:
   - `SUPPORTS_MESSAGE_EDITING = True`
   - `SUPPORTS_METADATA_ONLY_STREAM_UPDATES = True`
   - `STREAMING_CARD_METADATA_KEY = "_hermes_stream"`
   - `STREAM_TOOL_BOUNDARY_MODE = "paragraph"`
   - `STREAM_INTERIM_MESSAGE_MODE = "inline"`

2. Streaming state is carried in metadata:

```json
{
  "_hermes_stream": {
    "phase": "streaming",
    "elapsed_seconds": 1.2,
    "tool_status": {"text": "💻 terminal: \"pwd\""}
  }
}
```

3. Status-only flushes must work even without visible text:
   - use `"\u200b"` as placeholder body
   - do not append stream cursor to that placeholder

4. Tool progress should be embedded into the active stream card, not sent as a standalone progress message.

5. Session-reset / session-switch / context-pressure notices should render as low-noise Feishu cards via `_hermes_stream` metadata.

6. Generic file attachments with caption should use:
   - first send caption as plain text
   - then send native file message

### Weixin

1. Do not try to preserve gateway-side streaming UX on a non-editable transport.
2. For the turn where streaming/tool progress would duplicate bubbles, disable gateway-side preview/progress and rely on final reply.

## Recommended target files to inspect first

- `gateway/platforms/feishu.py`
- `gateway/run.py`
- `gateway/stream_consumer.py`
- `gateway/config.py`
- `gateway/display_config.py`
- `tests/gateway/test_stream_consumer.py`
- `tests/gateway/test_run_progress_topics.py`
- `tests/gateway/test_feishu.py`

## Acceptance checklist

- Feishu tool execution shows one live card, not tiny preview + second card
- Feishu tool completion clears `tool_status`
- final answer edits back into the same stream/card path
- context-pressure and session notices use Feishu card styling
- Weixin no longer emits preview/tool/final duplicate bubbles
- focused pytest suite passes

## Pitfalls

- Do not route all Feishu streaming messages to cards just because `_hermes_stream` exists; only use streaming cards when tool-status or notice-card logic requires it.
- Do not deduplicate edits by text alone; metadata-only changes must still trigger edit.
- Do not append `▉` to `"\u200b"` placeholder messages.
- Do not keep standalone tool-progress enabled on Weixin if the adapter cannot truly edit messages.
- Do not use `post + media` for generic file attachments with caption on Feishu.

## Handoff message template

Use this with another Hermes instance:

```text
Load the skill `hermes-feishu-weixin-streaming-migration-kit` and read all linked reference files. Then apply the migration bundle from the path recorded in `references/transfer-bundle-path.txt` to the target Hermes repo. Preserve relative file paths. Run the verification commands from `references/verification.md`. Finally report: root cause summary, files changed, exact pytest results, and remaining risks.
```
