# Feishu format calls and metadata contract

This migration relies on Feishu using a `_hermes_stream` metadata envelope.

## 1. Normal embedded tool-progress stream

```json
{
  "_hermes_stream": {
    "phase": "streaming",
    "elapsed_seconds": 1.4,
    "tool_status": {
      "text": "💻 terminal: \"pwd\""
    }
  }
}
```

Behavior:
- The visible body may be ordinary text, or `"\u200b"` for metadata-only updates.
- When body is exactly `"\u200b"`, do **not** append cursor glyphs like `▉`.
- Feishu adapter should render an interactive streaming card only when tool-status or notice-card conditions require it.

## 2. Tool completion edit

```json
{
  "_hermes_stream": {
    "phase": "completed",
    "elapsed_seconds": 2.0
  }
}
```

Behavior:
- `tool_status` must be removed.
- Final answer should edit the same message/card path if possible.

## 3. Context-pressure notice card

```json
{
  "_hermes_stream": {
    "phase": "completed",
    "notice_kind": "context_pressure",
    "notice_text": "⚠ 距离压缩阈值 85%（阈值 50%，即将触发压缩）"
  }
}
```

Behavior:
- Feishu should render a low-priority interactive card, not a noisy plain warning bubble.
- Keep this visually lighter than the main tool-progress card.

## 4. Session notice card

Example tool-status line for session boundary events:

```json
{
  "_hermes_stream": {
    "phase": "completed",
    "tool_status": {
      "text": "会话已切换"
    }
  }
}
```

Usages:
- `/new`
- `/resume`
- idle auto-reset
- manual reset notices

## 5. Feishu attachment rule for generic files with caption

Do **not** send a generic file/document caption using `post + media` for ordinary files.

Use this sequence instead:
1. send caption as normal `text`
2. send native attachment as `file` (or `media` / `audio` if appropriate)

## 6. Adapter capability flags to preserve

```python
SUPPORTS_MESSAGE_EDITING = True
SUPPORTS_METADATA_ONLY_STREAM_UPDATES = True
STREAMING_CARD_METADATA_KEY = "_hermes_stream"
STREAM_TOOL_BOUNDARY_MODE = "paragraph"
STREAM_INTERIM_MESSAGE_MODE = "inline"
```
