import json
import subprocess
import sys
from pathlib import Path


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "hermes_feishu_streaming_plugin", *args],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
        check=False,
    )


def test_cli_manifest_outputs_json():
    result = run_cli("manifest")
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["bundle_name"] == "hermes-feishu-weixin-streaming-migration-kit"
    assert "references/verification.md" in payload["files"]


def test_cli_export_writes_bundle(tmp_path: Path):
    result = run_cli("export", "--output-dir", str(tmp_path))
    assert result.returncode == 0, result.stderr
    exported = tmp_path / "hermes-feishu-weixin-streaming-migration-kit"
    assert exported.exists()
    assert (exported / "README.md").exists()


def test_cli_locators_outputs_json():
    result = run_cli("locators")
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert any(item["path"] == "gateway/platforms/feishu.py" for item in payload)


def test_cli_locate_reports_target(tmp_path: Path):
    result = run_cli("locate", "--target", str(tmp_path))
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["repo_root"] == str(tmp_path)
    assert payload["missing_files"] >= 1
