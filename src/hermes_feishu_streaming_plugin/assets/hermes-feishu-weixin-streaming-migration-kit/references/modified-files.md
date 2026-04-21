# Modified files manifest

## Source files

- `gateway/platforms/feishu.py`
  - Adds Feishu streaming-card rendering, message-type tracking, metadata-aware send/edit flow, interactive-card fallback, context-pressure card rendering, session-notice card support, and safer file+caption behavior.
- `gateway/run.py`
  - Routes tool progress with transport modes (`embedded` for Feishu, `off` for Weixin in the problematic path), emits Feishu session/context metadata, and aligns commentary/stream orchestration.
- `gateway/stream_consumer.py`
  - Adds status-aware streaming (`on_status`), metadata-only placeholder flushes, force-edit when metadata changes, no-edit capability guards, and paragraph/inline streaming behavior.
- `gateway/config.py`
  - Bridges nested `session_reset` config into runtime gateway config.
- `gateway/display_config.py`
  - Aligns gateway display defaults/handling for this streaming UX.
- `hermes_cli/gateway.py`
  - Small gateway CLI/config touch-up tied to the migration.

## Tests

- `tests/gateway/test_stream_consumer.py`
- `tests/gateway/test_run_progress_topics.py`
- `tests/gateway/test_feishu.py`
- `tests/gateway/test_feishu_session_notices.py`
- `tests/gateway/test_gateway_config_session_reset.py`
- `tests/gateway/test_display_config.py`
- `tests/run_agent/test_context_pressure.py`
- `tests/agent/test_display.py`

## Docs

- `website/docs/user-guide/messaging/feishu.md`

## Bundle-only files

- `references/migration.patch` — unified patch covering the migration files
- `references/feishu-format-calls.md` — exact Feishu metadata / card-call contract
- `references/migration-steps.md` — apply/copy workflow
- `references/verification.md` — pytest commands and expected scope
