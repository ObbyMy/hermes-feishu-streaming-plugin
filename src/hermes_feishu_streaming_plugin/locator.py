from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json
from typing import Iterable


@dataclass(frozen=True)
class LocatorSpec:
    path: str
    purpose: str
    patterns: list[str]


@dataclass(frozen=True)
class LocatorMatch:
    pattern: str
    matched: bool
    line_numbers: list[int]


@dataclass(frozen=True)
class FileLocatorResult:
    path: str
    purpose: str
    exists: bool
    all_patterns_matched: bool
    matches: list[LocatorMatch]


@dataclass(frozen=True)
class LocateReport:
    repo_root: str
    matched_files: int
    missing_files: int
    partial_files: int
    files: list[FileLocatorResult]

    def to_json(self) -> str:
        return json.dumps(
            {
                "repo_root": self.repo_root,
                "matched_files": self.matched_files,
                "missing_files": self.missing_files,
                "partial_files": self.partial_files,
                "files": [asdict(item) for item in self.files],
            },
            ensure_ascii=False,
            indent=2,
        )


LOCATOR_SPECS: list[LocatorSpec] = [
    LocatorSpec(
        path="gateway/platforms/feishu.py",
        purpose="Feishu 适配器：单卡片流式消息、消息编辑、interactive card/fallback、caption+file 发送顺序",
        patterns=[
            "class FeishuAdapter(BasePlatformAdapter):",
            "def _build_event_handler(self) -> Any:",
            "async def send(",
            "async def edit_message(",
            "def _build_outbound_payload(",
        ],
    ),
    LocatorSpec(
        path="gateway/run.py",
        purpose="网关主流程：stream consumer 接线、tool progress 传输模式、Feishu session/context metadata 注入",
        patterns=[
            "from gateway.stream_consumer import GatewayStreamConsumer, StreamConsumerConfig",
            '"tool_status": {"text": status_text}',
            "progress_transport",
            "GatewayStreamConsumer(",
        ],
    ),
    LocatorSpec(
        path="gateway/stream_consumer.py",
        purpose="流式消费器：status-only flush、metadata-only edit、段落边界、inline commentary、placeholder 逻辑",
        patterns=[
            "_STATUS_ONLY_PLACEHOLDER = \"\\u200b\"",
            "class GatewayStreamConsumer:",
            "def on_status(",
            "status_changed = status_update is not None",
        ],
    ),
    LocatorSpec(
        path="gateway/config.py",
        purpose="gateway 配置桥接：session_reset 的 default/platform/type 覆盖注入",
        patterns=[
            'sr = yaml_cfg.get("session_reset")',
            'gw_data["default_reset_policy"]',
            'gw_data["reset_by_platform"]',
            'gw_data["reset_by_type"]',
        ],
    ),
    LocatorSpec(
        path="gateway/display_config.py",
        purpose="平台显示默认值：Feishu 默认开启 streaming 并调整 tool_progress / preview 长度",
        patterns=[
            "_PLATFORM_DEFAULTS: dict[str, dict[str, Any]] = {",
            '"feishu":          _FEISHU_DEFAULTS',
        ],
    ),
    LocatorSpec(
        path="hermes_cli/gateway.py",
        purpose="CLI / gateway 入口补充：与该迁移配套的小型配置/入口调整",
        patterns=[
            "def run_gateway(",
            "gateway.run",
        ],
    ),
    LocatorSpec(
        path="tests/gateway/test_stream_consumer.py",
        purpose="验证 stream_consumer 的 status-only / metadata-only / paragraph-inline 逻辑",
        patterns=[
            "GatewayStreamConsumer",
            "status_only_placeholder",
        ],
    ),
    LocatorSpec(
        path="tests/gateway/test_run_progress_topics.py",
        purpose="验证 gateway/run 中 Feishu embedded tool progress 与 Weixin 去重路径",
        patterns=[
            "embedded",
            "standalone_tool_progress",
        ],
    ),
    LocatorSpec(
        path="tests/gateway/test_feishu.py",
        purpose="验证 Feishu adapter 的发送/编辑/fallback/card 路径",
        patterns=[
            "FeishuAdapter",
            "interactive",
        ],
    ),
]


def locator_manifest() -> list[dict]:
    return [asdict(spec) for spec in LOCATOR_SPECS]


def locator_manifest_json() -> str:
    return json.dumps(locator_manifest(), ensure_ascii=False, indent=2)


def _find_line_numbers(lines: Iterable[str], pattern: str) -> list[int]:
    matched_lines: list[int] = []
    for idx, line in enumerate(lines, start=1):
        if pattern in line:
            matched_lines.append(idx)
    return matched_lines


def locate_bundle_targets(target_repo: str | Path) -> LocateReport:
    root = Path(target_repo)
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError(f"Target repo directory does not exist: {root}")

    results: list[FileLocatorResult] = []
    matched_files = 0
    missing_files = 0
    partial_files = 0

    for spec in LOCATOR_SPECS:
        file_path = root / spec.path
        if not file_path.exists() or not file_path.is_file():
            missing_files += 1
            results.append(
                FileLocatorResult(
                    path=spec.path,
                    purpose=spec.purpose,
                    exists=False,
                    all_patterns_matched=False,
                    matches=[LocatorMatch(pattern=pattern, matched=False, line_numbers=[]) for pattern in spec.patterns],
                )
            )
            continue

        text = file_path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        matches = [
            LocatorMatch(
                pattern=pattern,
                matched=bool(line_numbers := _find_line_numbers(lines, pattern)),
                line_numbers=line_numbers,
            )
            for pattern in spec.patterns
        ]
        all_patterns_matched = all(item.matched for item in matches)
        if all_patterns_matched:
            matched_files += 1
        else:
            partial_files += 1
        results.append(
            FileLocatorResult(
                path=spec.path,
                purpose=spec.purpose,
                exists=True,
                all_patterns_matched=all_patterns_matched,
                matches=matches,
            )
        )

    return LocateReport(
        repo_root=str(root),
        matched_files=matched_files,
        missing_files=missing_files,
        partial_files=partial_files,
        files=results,
    )
