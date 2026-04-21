from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil

from .bundle import _bundle_root


@dataclass(frozen=True)
class ApplyResult:
    target: Path
    files_copied: int
    copied_paths: list[str]


def apply_bundle(target_repo: str | Path, dry_run: bool = False) -> ApplyResult:
    target = Path(target_repo)
    if not target.exists() or not target.is_dir():
        raise FileNotFoundError(f"Target repo directory does not exist: {target}")

    bundle_files = _bundle_root() / 'files'
    copied: list[str] = []
    for source in sorted(bundle_files.rglob('*')):
        if not source.is_file():
            continue
        rel = source.relative_to(bundle_files)
        copied.append(str(rel).replace('\\', '/'))
        if dry_run:
            continue
        dest = target / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)

    return ApplyResult(target=target, files_copied=len(copied), copied_paths=copied)
