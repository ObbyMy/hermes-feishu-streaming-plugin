# Verification

From the target Hermes repo root:

```bash
source venv/bin/activate
python -m pytest tests/gateway/test_stream_consumer.py tests/gateway/test_feishu.py tests/gateway/test_feishu_session_notices.py -q
```

Latest rehearsal on this machine:

- target clone: `/home/jiangshuo/.hermes/projects/hermes-agent-upstream-check`
- applied clone: `/home/jiangshuo/.hermes/projects/hermes-agent-upstream-applied`
- result: passed
