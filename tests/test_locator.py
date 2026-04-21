import json
from pathlib import Path

from hermes_feishu_streaming_plugin.locator import locate_bundle_targets, locator_manifest


def test_locator_manifest_contains_expected_touchpoints():
    manifest = locator_manifest()
    paths = {item["path"] for item in manifest}
    assert "gateway/platforms/feishu.py" in paths
    assert "gateway/run.py" in paths
    assert "gateway/stream_consumer.py" in paths


def test_locate_bundle_targets_matches_embedded_files(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()

    # minimal embedded-like structure
    (repo / "gateway" / "platforms").mkdir(parents=True)
    (repo / "gateway").mkdir(exist_ok=True)
    (repo / "hermes_cli").mkdir(exist_ok=True)
    (repo / "tests" / "gateway").mkdir(parents=True)

    (repo / "gateway" / "platforms" / "feishu.py").write_text(
        "\n".join(
            [
                "class FeishuAdapter(BasePlatformAdapter):",
                "def _build_event_handler(self) -> Any:",
                "async def send(",
                "async def edit_message(",
                "def _build_outbound_payload(",
            ]
        ),
        encoding="utf-8",
    )
    (repo / "gateway" / "run.py").write_text(
        "\n".join(
            [
                "from gateway.stream_consumer import GatewayStreamConsumer, StreamConsumerConfig",
                '"tool_status": {"text": status_text}',
                "progress_transport",
                "GatewayStreamConsumer(",
            ]
        ),
        encoding="utf-8",
    )
    (repo / "gateway" / "stream_consumer.py").write_text(
        "\n".join(
            [
                '_STATUS_ONLY_PLACEHOLDER = "\\u200b"',
                "class GatewayStreamConsumer:",
                "def on_status(",
                "status_changed = status_update is not None",
            ]
        ),
        encoding="utf-8",
    )
    (repo / "gateway" / "config.py").write_text(
        "\n".join(
            [
                'sr = yaml_cfg.get("session_reset")',
                'gw_data["default_reset_policy"]',
                'gw_data["reset_by_platform"]',
                'gw_data["reset_by_type"]',
            ]
        ),
        encoding="utf-8",
    )
    (repo / "gateway" / "display_config.py").write_text(
        "\n".join(
            [
                "_PLATFORM_DEFAULTS: dict[str, dict[str, Any]] = {",
                '"feishu":          _FEISHU_DEFAULTS',
            ]
        ),
        encoding="utf-8",
    )
    (repo / "hermes_cli" / "gateway.py").write_text(
        "\n".join(["def run_gateway(", "gateway.run"]),
        encoding="utf-8",
    )
    (repo / "tests" / "gateway" / "test_stream_consumer.py").write_text(
        "\n".join(["GatewayStreamConsumer", "status_only_placeholder"]),
        encoding="utf-8",
    )
    (repo / "tests" / "gateway" / "test_run_progress_topics.py").write_text(
        "\n".join(["embedded", "standalone_tool_progress"]),
        encoding="utf-8",
    )
    (repo / "tests" / "gateway" / "test_feishu.py").write_text(
        "\n".join(["FeishuAdapter", "interactive"]),
        encoding="utf-8",
    )

    report = locate_bundle_targets(repo)
    payload = json.loads(report.to_json())
    assert payload["matched_files"] == 9
    assert payload["missing_files"] == 0
    assert payload["partial_files"] == 0


def test_locate_bundle_targets_marks_missing_files(tmp_path: Path):
    report = locate_bundle_targets(tmp_path)
    payload = json.loads(report.to_json())
    assert payload["matched_files"] == 0
    assert payload["missing_files"] == 9
