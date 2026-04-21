from pathlib import Path

from hermes_feishu_streaming_plugin.installer import apply_bundle


def test_apply_bundle_copies_files_into_repo(tmp_path: Path):
    target = tmp_path / "repo"
    target.mkdir()

    result = apply_bundle(target)

    assert result.files_copied > 5
    assert (target / "gateway" / "platforms" / "feishu.py").exists()
    assert (target / "tests" / "gateway" / "test_stream_consumer.py").exists()
    assert any(path.endswith("gateway/platforms/feishu.py") for path in result.copied_paths)


def test_apply_bundle_supports_dry_run(tmp_path: Path):
    target = tmp_path / "repo"
    target.mkdir()

    result = apply_bundle(target, dry_run=True)

    assert result.files_copied > 5
    assert not (target / "gateway" / "platforms" / "feishu.py").exists()
