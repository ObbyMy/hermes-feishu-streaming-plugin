from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
from pathlib import Path
import json
import shutil
from typing import Iterable

PACKAGE = "hermes_feishu_streaming_plugin"
BUNDLE_NAME = "hermes-feishu-weixin-streaming-migration-kit"


@dataclass(frozen=True)
class BundleManifest:
    bundle_name: str
    files: list[str]

    def to_json(self) -> str:
        return json.dumps({"bundle_name": self.bundle_name, "files": self.files}, ensure_ascii=False, indent=2)


def _bundle_root() -> Path:
    return Path(resources.files(PACKAGE).joinpath("assets", BUNDLE_NAME))


def _iter_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if path.is_file():
            yield path


def bundle_manifest() -> BundleManifest:
    root = _bundle_root()
    files = [str(path.relative_to(root)).replace('\\', '/') for path in _iter_files(root)]
    return BundleManifest(bundle_name=BUNDLE_NAME, files=files)


def reference_text(relative_path: str) -> str:
    root = _bundle_root()
    target = root / relative_path
    if not target.exists() or not target.is_file():
        raise FileNotFoundError(relative_path)
    return target.read_text(encoding='utf-8')


def export_bundle(output_dir: str | Path) -> Path:
    root = _bundle_root()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / BUNDLE_NAME
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(root, destination)
    return destination
