# Upgrade locator guide

If Hermes upstream changes line numbers, search these stable anchors first:

- `class FeishuAdapter(BasePlatformAdapter):`
- `async def edit_message(`
- `GatewayStreamConsumer(`
- `_STATUS_ONLY_PLACEHOLDER = "\u200b"`
- `"tool_status": {"text": status_text}`
- `"feishu":          _FEISHU_DEFAULTS`

If the locator reports partial matches, inspect the surrounding block and preserve behavior rather than old line numbers.
