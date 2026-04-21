# Migration steps

## Option A — copy full bundle

1. Copy the exported bundle directory to the target machine/repo.
2. From the target Hermes repo root, copy everything under `files/` into the repo root, preserving paths.
3. Run the verification commands from `verification.md`.

## Option B — apply the patch

From the target Hermes repo root:

```bash
git apply migration.patch
source venv/bin/activate
python -m pytest tests/gateway/test_stream_consumer.py tests/gateway/test_run_progress_topics.py tests/gateway/test_weixin.py tests/gateway/test_feishu.py -q
```

If the repo has drift and the patch does not apply cleanly:
- manually merge the files listed in `modified-files.md`
- use the copied files under the bundle `files/` tree as the source of truth
- then rerun tests

## Recommended order to merge manually

1. `gateway/stream_consumer.py`
2. `gateway/run.py`
3. `gateway/platforms/feishu.py`
4. `gateway/config.py`
5. `gateway/display_config.py`
6. tests
7. docs

## Critical manual checks after merging

- Feishu tool-start can replace a tiny provisional preview with a metadata-only placeholder card.
- Clearing tool status still edits the message even if visible body text did not change.
- Weixin no longer emits preview + tool-progress + final duplicates.
- Feishu generic file+caption send path is text-first then file.
