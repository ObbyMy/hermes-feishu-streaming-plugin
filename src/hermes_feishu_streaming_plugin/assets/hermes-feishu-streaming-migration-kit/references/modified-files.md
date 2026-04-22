# Modified files (Feishu-only bundle)

This bundle currently ships these Hermes files:

- `gateway/platforms/feishu.py`
- `gateway/run.py`
- `gateway/stream_consumer.py`
- `gateway/display_config.py`
- `tests/gateway/test_stream_consumer.py`
- `tests/gateway/test_feishu.py`
- `tests/gateway/test_feishu_session_notices.py`
- `tests/agent/test_display.py`
- `tests/run_agent/test_context_pressure.py`
- `website/docs/user-guide/messaging/feishu.md`

Why they matter:

- `gateway/platforms/feishu.py`: Feishu adapter send/edit/card/fallback behavior
- `gateway/run.py`: stream consumer wiring and embedded tool-progress path for Feishu
- `gateway/stream_consumer.py`: status-only placeholder and metadata-only flush behavior
- `gateway/display_config.py`: Feishu display defaults
- tests: guard against regressions in the restored Feishu behavior
