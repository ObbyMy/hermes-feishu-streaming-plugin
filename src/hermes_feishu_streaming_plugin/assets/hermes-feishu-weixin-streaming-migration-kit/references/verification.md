# Verification

## Focused gateway regression set

```bash
source venv/bin/activate && python -m pytest tests/gateway/test_stream_consumer.py tests/gateway/test_run_progress_topics.py tests/gateway/test_weixin.py tests/gateway/test_feishu.py tests/gateway/test_feishu_session_notices.py tests/gateway/test_gateway_config_session_reset.py tests/run_agent/test_context_pressure.py -q
```

## Additional Feishu/display regression set

```bash
source venv/bin/activate && python -m pytest tests/agent/test_display.py tests/gateway/test_display_config.py tests/gateway/test_feishu.py tests/gateway/test_feishu_session_notices.py tests/gateway/test_gateway_config_session_reset.py tests/run_agent/test_context_pressure.py -q
```

## Expected results from the source bundle

- Focused gateway regression set: `241 passed`
- Additional Feishu/display regression set: `208 passed`

Warnings from `lark_oapi` / `websockets.legacy` deprecations may still appear and are not part of this migration's failure signal.
