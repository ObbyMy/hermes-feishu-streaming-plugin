# Modified files and migration intent

This reference answers three questions for every touchpoint:

1. **What changed?**
2. **Why was it changed?**
3. **Where should you look again after Hermes upstream moves?**

---

## 1. `gateway/platforms/feishu.py`

### What changed

This is the most important file in the migration.

Key behavior added or adjusted:

- enables true message editing for Feishu;
- introduces the `_hermes_stream` metadata contract;
- allows streaming to render as one editable card instead of fragmented bubbles;
- tracks outbound message types so edits can preserve the correct Feishu transport;
- adds interactive-card fallback behavior;
- ensures file attachments with caption go through **text first, file second**.

### Why it changed

Without these changes, Feishu tends to degrade into:

- a tiny provisional text bubble,
- a separate tool-progress message,
- and a later final answer.

That is exactly the UX this migration removes.

### Where to look in newer Hermes versions

Search for these anchors first:

- `class FeishuAdapter(BasePlatformAdapter):`
- `def _build_event_handler(self) -> Any:`
- `async def send(`
- `async def edit_message(`
- `def _build_outbound_payload(`

### Merge note

If upstream changed Feishu payload formatting, preserve these semantics even if the exact implementation differs:

- metadata-aware outbound payload selection,
- interactive-card fallback,
- metadata-only edit support,
- remembered outbound message type,
- text-first file caption behavior.

---

## 2. `gateway/run.py`

### What changed

This file wires the streaming UX into the gateway runtime.

Key behavior added or adjusted:

- introduces transport modes for tool progress: `embedded`, `standalone`, `off`;
- embeds tool status into the active Feishu stream card;
- suppresses duplicate standalone progress on Weixin;
- injects metadata for session notices and context-pressure notices;
- aligns commentary / stream-consumer orchestration with the card workflow.

### Why it changed

This file is where the assistant runtime decides whether tool progress becomes:

- part of the current editable stream,
- a separate progress bubble,
- or completely disabled.

The OpenClaw-style Feishu behavior depends on making the right choice here.

### Where to look in newer Hermes versions

Search for these anchors first:

- `from gateway.stream_consumer import GatewayStreamConsumer, StreamConsumerConfig`
- `"tool_status": {"text": status_text}`
- `progress_transport`
- `GatewayStreamConsumer(`

### Merge note

If upstream refactors callback plumbing, preserve the outcome rather than the exact variable names:

- Feishu => embedded tool progress
- Weixin => no duplicate streaming/progress preview path
- session/context notices => card-ready metadata path

---

## 3. `gateway/stream_consumer.py`

### What changed

This file implements the runtime behavior of a single streaming response.

Key behavior added or adjusted:

- adds `on_status()` for transient tool-state refreshes;
- supports status-only flushes using `\u200b`;
- supports metadata-only edits even when visible text is unchanged;
- supports paragraph boundary handling for tool segments;
- supports inline commentary mode;
- avoids appending the stream cursor to the placeholder body.

### Why it changed

A large part of the Feishu UX problem was not just adapter formatting — it was the streaming consumer refusing to flush when only metadata changed.

Without this file-level change, Feishu can know about tool status internally but never visibly render the live card state at the right moment.

### Where to look in newer Hermes versions

Search for these anchors first:

- `_STATUS_ONLY_PLACEHOLDER = "\u200b"`
- `class GatewayStreamConsumer:`
- `def on_status(`
- `status_changed = status_update is not None`

### Merge note

If upstream changed edit deduplication, preserve this rule:

> metadata changes must be allowed to force an edit even when visible text is unchanged.

---

## 4. `gateway/config.py`

### What changed

Adds bridging for nested `session_reset` configuration into runtime gateway config:

- default policy
- platform-specific policy
- type-specific policy

### Why it changed

The Feishu session notice behavior depends on the effective runtime policy being available in the same shape the gateway expects.

### Where to look in newer Hermes versions

Search for:

- `sr = yaml_cfg.get("session_reset")`
- `gw_data["default_reset_policy"]`
- `gw_data["reset_by_platform"]`
- `gw_data["reset_by_type"]`

---

## 5. `gateway/display_config.py`

### What changed

Adds a Feishu-specific display tier with defaults tailored to the streaming-card UX:

- `tool_progress = all`
- `show_reasoning = False`
- `tool_preview_length = 60`
- `streaming = True`

### Why it changed

The generic medium-tier defaults were not aligned with the intended Feishu experience.

### Where to look in newer Hermes versions

Search for:

- `_PLATFORM_DEFAULTS: dict[str, dict[str, Any]] = {`
- `"feishu":          _FEISHU_DEFAULTS`

---

## 6. `hermes_cli/gateway.py`

### What changed

Contains a small supporting adjustment tied to this migration bundle.

### Why it changed

The migration was not strictly adapter-only; a small CLI / gateway bootstrap alignment was also needed so the behavior remains coherent end-to-end.

### Where to look in newer Hermes versions

Search for:

- `def run_gateway(`
- `gateway.run`

---

## 7. Tests

Regression coverage was added or updated in:

- `tests/gateway/test_stream_consumer.py`
- `tests/gateway/test_run_progress_topics.py`
- `tests/gateway/test_feishu.py`
- `tests/gateway/test_feishu_session_notices.py`
- `tests/gateway/test_gateway_config_session_reset.py`
- `tests/gateway/test_display_config.py`
- `tests/run_agent/test_context_pressure.py`
- `tests/agent/test_display.py`

### Why the tests matter

The migration is easy to partially re-implement in a way that *looks* right but silently regresses one of these cases:

- tool-start card never appears,
- metadata clears but edit is skipped,
- Weixin duplicates reappear,
- session/context notices fall back to noisy plain text.

---

## Practical upgrade order

When Hermes upstream changes and the patch stops applying cleanly, use this order:

1. `gateway/stream_consumer.py`
2. `gateway/run.py`
3. `gateway/platforms/feishu.py`
4. `gateway/config.py`
5. `gateway/display_config.py`
6. tests
7. docs

Then run the commands in `verification.md`.
