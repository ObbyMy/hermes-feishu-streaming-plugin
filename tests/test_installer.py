from pathlib import Path

from hermes_feishu_streaming_plugin.installer import apply_bundle, verify_target_repo


def test_apply_bundle_copies_files_into_repo(tmp_path: Path):
    target = tmp_path / "repo"
    target.mkdir()

    result = apply_bundle(target)

    assert result.files_copied > 5
    assert (target / "gateway" / "platforms" / "feishu.py").exists()
    assert (target / "tests" / "gateway" / "test_stream_consumer.py").exists()
    assert any(path.endswith("gateway/platforms/feishu.py") for path in result.copied_paths)
    assert result.verify is None


def test_apply_bundle_supports_dry_run(tmp_path: Path):
    target = tmp_path / "repo"
    target.mkdir()

    result = apply_bundle(target, dry_run=True)

    assert result.files_copied > 5
    assert not (target / "gateway" / "platforms" / "feishu.py").exists()
    assert result.verify is None


def test_verify_target_repo_runs_pytest(monkeypatch, tmp_path: Path):
    target = tmp_path / "repo"
    target.mkdir()

    calls = {}

    class Completed:
        returncode = 0
        stdout = "3 passed"
        stderr = ""

    def fake_run(command, cwd, text, capture_output, check):
        calls["command"] = command
        calls["cwd"] = cwd
        calls["text"] = text
        calls["capture_output"] = capture_output
        calls["check"] = check
        return Completed()

    monkeypatch.setattr("hermes_feishu_streaming_plugin.installer.subprocess.run", fake_run)

    result = verify_target_repo(target, python_bin="/tmp/python", tests=["tests/test_one.py"])

    assert result.passed is True
    assert result.returncode == 0
    assert result.stdout == "3 passed"
    assert calls["command"] == ["/tmp/python", "-m", "pytest", "tests/test_one.py", "-q"]
    assert calls["cwd"] == target


def test_apply_bundle_can_verify(monkeypatch, tmp_path: Path):
    target = tmp_path / "repo"
    target.mkdir()

    class FakeVerifyResult:
        command = ["python", "-m", "pytest", "-q"]
        returncode = 0
        stdout = "ok"
        stderr = ""

        @property
        def passed(self):
            return True

    def fake_verify_target_repo(target_repo, *, python_bin=None, tests=None):
        assert Path(target_repo) == target
        assert python_bin == "/tmp/python"
        assert tests == ["tests/test_one.py"]
        return FakeVerifyResult()

    monkeypatch.setattr("hermes_feishu_streaming_plugin.installer.verify_target_repo", fake_verify_target_repo)

    result = apply_bundle(target, verify=True, python_bin="/tmp/python", tests=["tests/test_one.py"])

    assert result.verify is not None
    assert result.verify.passed is True
