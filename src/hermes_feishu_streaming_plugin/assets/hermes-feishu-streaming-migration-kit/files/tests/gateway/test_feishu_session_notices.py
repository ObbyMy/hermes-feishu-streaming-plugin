from datetime import datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from gateway.config import Platform
from gateway.platforms.base import MessageEvent
from gateway.run import GatewayRunner
from gateway.session import SessionEntry, SessionSource


@pytest.mark.asyncio
async def test_handle_resume_command_sends_feishu_session_card_metadata():
    runner = object.__new__(GatewayRunner)
    adapter = SimpleNamespace(
        STREAMING_CARD_METADATA_KEY="_hermes_stream",
        send=AsyncMock(),
    )
    runner.adapters = {Platform.FEISHU: adapter}
    runner._running_agents = {}
    runner._session_db = MagicMock()
    runner._session_db.resolve_session_by_title.return_value = "target-session"
    runner._session_db.get_session_title.return_value = "旧会话"

    current_entry = SessionEntry(
        session_key="feishu:dm:u1",
        session_id="current-session",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    switched_entry = SessionEntry(
        session_key="feishu:dm:u1",
        session_id="target-session",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    runner.session_store = MagicMock()
    runner.session_store.get_or_create_session.return_value = current_entry
    runner.session_store.switch_session.return_value = switched_entry
    runner.session_store.load_transcript.return_value = [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好"},
    ]
    runner._async_flush_memories = AsyncMock()
    runner._background_tasks = set()
    runner._session_key_for_source = GatewayRunner._session_key_for_source.__get__(runner, GatewayRunner)

    source = SessionSource(platform=Platform.FEISHU, chat_id="oc_123", user_id="u1")
    event = MessageEvent(text="/resume 旧会话", source=source)

    result = await GatewayRunner._handle_resume_command(runner, event)

    assert result is None
    adapter.send.assert_awaited_once()
    _, sent_text = adapter.send.await_args.args
    sent_metadata = adapter.send.await_args.kwargs["metadata"]
    assert "Conversation restored" in sent_text
    assert sent_metadata["_hermes_stream"]["phase"] == "completed"
    assert sent_metadata["_hermes_stream"]["tool_status"]["text"] == "会话已切换"


def test_session_notice_metadata_adds_completed_stream_for_feishu():
    runner = object.__new__(GatewayRunner)
    runner.adapters = {
        Platform.FEISHU: SimpleNamespace(STREAMING_CARD_METADATA_KEY="_hermes_stream")
    }
    source = SessionSource(platform=Platform.FEISHU, chat_id="oc_123", user_id="u1")
    event = MessageEvent(text="hello", source=source)
    event.metadata = {"thread_id": "omt_1"}

    metadata = GatewayRunner._session_notice_metadata(runner, event, "会话已自动重置")

    assert metadata["thread_id"] == "omt_1"
    assert metadata["_hermes_stream"]["phase"] == "completed"
    assert metadata["_hermes_stream"]["tool_status"]["text"] == "会话已自动重置"


def test_format_long_running_notice_localizes_activity():
    notice = GatewayRunner._format_long_running_notice(
        10,
        {
            "api_call_count": 35,
            "max_iterations": 90,
            "last_activity_desc": "starting API call #35",
        },
    )

    assert notice == "⏳ 仍在处理中（已耗时 10 分钟——轮次 35/90，开始第 35 次 API 调用）"


def test_format_long_running_notice_prefers_current_tool():
    notice = GatewayRunner._format_long_running_notice(
        10,
        {
            "api_call_count": 35,
            "max_iterations": 90,
            "current_tool": "terminal",
            "last_activity_desc": "API call #35 completed",
        },
    )

    assert notice == "⏳ 仍在处理中（已耗时 10 分钟——轮次 35/90，当前工具：terminal）"


def test_should_suppress_feishu_status_notice_for_retry_waits():
    assert GatewayRunner._should_suppress_feishu_status_notice(
        Platform.FEISHU,
        "lifecycle",
        "⏳ Retrying in 2.3s (attempt 1/3)...",
    )
    assert GatewayRunner._should_suppress_feishu_status_notice(
        Platform.FEISHU,
        "lifecycle",
        "⏱️ Rate limit reached. Waiting 12s before retry (attempt 2/3)...",
    )


def test_should_suppress_feishu_status_notice_for_long_running_noise():
    assert GatewayRunner._should_suppress_feishu_status_notice(
        Platform.FEISHU,
        "lifecycle",
        "⏳ 仍在处理中（已耗时 9 分钟——轮次 25/90，工具已完成：terminal（0.3s））",
    )
    assert GatewayRunner._should_suppress_feishu_status_notice(
        Platform.FEISHU,
        "lifecycle",
        "⚠️ 已有 15 分钟无新进展。如果代理仍未响应，约 15 分钟后会超时结束。你可以继续等待，或使用 /reset。",
    )


def test_should_not_suppress_context_pressure_notice_for_feishu():
    assert not GatewayRunner._should_suppress_feishu_status_notice(
        Platform.FEISHU,
        "context_pressure",
        "⚠️ 上下文：▰▰▰▰▰ 距离压缩阈值 80%",
    )


def test_build_status_notice_payload_turns_context_pressure_into_card():
    runner = object.__new__(GatewayRunner)
    runner.adapters = {
        Platform.FEISHU: SimpleNamespace(STREAMING_CARD_METADATA_KEY="_hermes_stream")
    }

    suppressed, content, metadata = GatewayRunner._build_status_notice_payload(
        runner,
        Platform.FEISHU,
        "context_pressure",
        "⚠️ 上下文：▰▰▰▰▰ 距离压缩阈值 80%\n上下文即将触发压缩（阈值：窗口容量的 50%）。",
        {"thread_id": "omt_1"},
    )

    assert suppressed is False
    assert content == "本轮上下文较长，系统可能会自动整理历史内容。"
    assert metadata["thread_id"] == "omt_1"
    assert metadata["_hermes_stream"]["notice_kind"] == "context_pressure"


def test_should_reset_embedded_status_text_only_before_any_stream_output():
    assert GatewayRunner._should_reset_embedded_status_text(SimpleNamespace(already_sent=False)) is True
    assert GatewayRunner._should_reset_embedded_status_text(SimpleNamespace(already_sent=True)) is False
