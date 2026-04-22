from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess
import sys

from .bundle import _bundle_root

DEFAULT_VERIFY_TESTS = [
    "tests/gateway/test_stream_consumer.py",
    "tests/gateway/test_feishu.py",
    "tests/gateway/test_feishu_session_notices.py",
]


@dataclass(frozen=True)
class VerifyResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str

    @property
    def passed(self) -> bool:
        return self.returncode == 0


@dataclass(frozen=True)
class ApplyResult:
    target: Path
    files_copied: int
    copied_paths: list[str]
    verify: VerifyResult | None = None


def verify_target_repo(
    target_repo: str | Path,
    *,
    python_bin: str | Path | None = None,
    tests: list[str] | None = None,
) -> VerifyResult:
    target = Path(target_repo)
    if not target.exists() or not target.is_dir():
        raise FileNotFoundError(f"Target repo directory does not exist: {target}")

    selected_tests = tests or DEFAULT_VERIFY_TESTS
    command = [str(python_bin or sys.executable), "-m", "pytest", *selected_tests, "-q"]
    result = subprocess.run(
        command,
        cwd=target,
        text=True,
        capture_output=True,
        check=False,
    )
    return VerifyResult(
        command=command,
        returncode=result.returncode,
        stdout=result.stdout,
        stderr=result.stderr,
    )


def apply_bundle(
    target_repo: str | Path,
    dry_run: bool = False,
    *,
    verify: bool = False,
    python_bin: str | Path | None = None,
    tests: list[str] | None = None,
) -> ApplyResult:
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

    verify_result = None
    if verify and not dry_run:
        verify_result = verify_target_repo(target, python_bin=python_bin, tests=tests)

    return ApplyResult(target=target, files_copied=len(copied), copied_paths=copied, verify=verify_result)
