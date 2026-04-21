# Upgrade locator workflow

This bundle does not only ship a patch — it also ships a **re-location strategy** for future Hermes upgrades.

## Why this exists

Patch application is the easy part.

The real maintenance problem starts later, when:

- Hermes upstream moves line numbers,
- helper functions get renamed,
- logic gets split across new files,
- or only part of the old patch still applies cleanly.

This document tells you how to recover.

---

## 1. Print the locator manifest

```bash
python -m hermes_feishu_streaming_plugin locators
```

That command prints a machine-readable list of:

- target file path,
- why the file matters,
- stable anchor strings to search for.

The same data is also stored in:

- `references/modification-map.json`

---

## 2. Scan the target Hermes repository

```bash
python -m hermes_feishu_streaming_plugin locate --target /path/to/hermes-agent
```

Read the result like this:

- `matched_files` — file exists and all expected anchor patterns were found
- `partial_files` — file exists but only some anchor patterns were found
- `missing_files` — file path no longer exists

### Interpretation

#### Case A — full match
The target repo is structurally close to the source migration. You can usually apply or manually merge with low friction.

#### Case B — partial match
The file still exists, but upstream has drifted. This is the common “manual merge required” case.

Action:
1. open the file,
2. jump to the matched anchor lines,
3. compare against this bundle’s `files/` version,
4. port semantics, not line numbers.

#### Case C — missing file
The path moved or the subsystem was refactored.

Action:
1. search the target repo for the anchor strings from `modification-map.json`,
2. identify the new owning module,
3. move the migration logic there.

---

## 3. File-by-file anchor strategy

### `gateway/platforms/feishu.py`
Search for:

- `class FeishuAdapter(BasePlatformAdapter):`
- `def _build_event_handler(self) -> Any:`
- `async def send(`
- `async def edit_message(`
- `def _build_outbound_payload(`

If one of these moved, keep the same semantics:

- metadata-aware outbound payload routing,
- interactive-card fallback,
- remembered message type,
- metadata-only edit support,
- text-first caption then file.

### `gateway/run.py`
Search for:

- `from gateway.stream_consumer import GatewayStreamConsumer, StreamConsumerConfig`
- `"tool_status": {"text": status_text}`
- `progress_transport`
- `GatewayStreamConsumer(`

Preserve the outcome:

- Feishu => embedded tool progress
- Weixin => duplicate path suppressed
- notice cards => metadata injected

### `gateway/stream_consumer.py`
Search for:

- `_STATUS_ONLY_PLACEHOLDER = "\u200b"`
- `class GatewayStreamConsumer:`
- `def on_status(`
- `status_changed = status_update is not None`

Preserve the outcome:

- status-only flush works,
- metadata-only edits still force an update,
- placeholder does not get a cursor appended.

---

## 4. Recommended recovery order after upstream drift

When the patch does not apply cleanly, recover in this order:

1. `gateway/stream_consumer.py`
2. `gateway/run.py`
3. `gateway/platforms/feishu.py`
4. `gateway/config.py`
5. `gateway/display_config.py`
6. tests
7. docs

Reason: once stream-consumer + run are aligned, the runtime behavior becomes understandable again; Feishu adapter formatting then becomes much easier to port correctly.

---

## 5. What not to preserve by accident

Do **not** cargo-cult line numbers or variable names.

Preserve these behaviors instead:

- one active Feishu stream/card path,
- embedded tool status on Feishu,
- no standalone duplicate tool progress on Weixin,
- metadata-only edits must still flush,
- session/context notices use the same low-noise card path,
- caption then file for generic attachments.

---

## 6. Final verification

After manual recovery, run the commands in `verification.md`.

If those pass, your re-located migration is functionally aligned even if the target repo structure has evolved.
