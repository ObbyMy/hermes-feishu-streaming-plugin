# AGENTS.md

This repository is designed so another Hermes agent can succeed with **only this repo URL**.

## Goal

Apply the bundled Feishu-only gateway migration to a target Hermes Agent checkout, then verify it.

## If you are a Hermes agent opening this repo

Follow this workflow in order:

1. Read:
   - `README.md`
   - `docs/feishu-restore-runbook.md`
2. Install the repo locally:
   ```bash
   pip install -e .[dev]
   ```
3. Inspect the target Hermes repo:
   ```bash
   python -m hermes_feishu_streaming_plugin locate --target /path/to/hermes-agent
   ```
4. Apply the migration and run the focused regression suite:
   ```bash
   python -m hermes_feishu_streaming_plugin apply \
     --target /path/to/hermes-agent \
     --verify \
     --python /path/to/hermes-agent/venv/bin/python
   ```
5. Report back:
   - locate summary (`matched_files`, `missing_files`, `partial_files`)
   - files copied
   - exact verify command
   - exact pytest result
   - remaining risks

## Important boundaries

- This repo is **Feishu-only**.
- Do **not** add non-Feishu platform-specific code or docs here.
- Private machine credentials/config are intentionally not stored in git.
- If the user asks to restore a live machine's existing Feishu bot tokens, `session_reset`, or systemd service state, request that machine's private restore bundle separately.

## Default verification tests

Use these tests unless the user asks for more:

- `tests/gateway/test_stream_consumer.py`
- `tests/gateway/test_feishu.py`
- `tests/gateway/test_feishu_session_notices.py`

## Canonical CLI commands

```bash
python -m hermes_feishu_streaming_plugin manifest
python -m hermes_feishu_streaming_plugin locators
python -m hermes_feishu_streaming_plugin locate --target /path/to/hermes-agent
python -m hermes_feishu_streaming_plugin verify --target /path/to/hermes-agent --python /path/to/hermes-agent/venv/bin/python
python -m hermes_feishu_streaming_plugin apply --target /path/to/hermes-agent --verify --python /path/to/hermes-agent/venv/bin/python
python -m hermes_feishu_streaming_plugin agent-handoff
```
