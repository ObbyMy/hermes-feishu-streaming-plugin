from pathlib import Path

import pytest

from hermes_feishu_streaming_plugin.bundle import (
    BUNDLE_NAME,
    bundle_manifest,
    export_bundle,
    reference_text,
)


def test_bundle_manifest_contains_expected_feishu_reference():
    manifest = bundle_manifest()
    assert manifest.bundle_name == BUNDLE_NAME
    assert "references/feishu-format-calls.md" in manifest.files
    assert "files/gateway/platforms/feishu.py" in manifest.files


def test_reference_text_reads_metadata_contract():
    content = reference_text("references/feishu-format-calls.md")
    assert "_hermes_stream" in content
    assert "SUPPORTS_MESSAGE_EDITING = True" in content


def test_export_bundle_copies_expected_files(tmp_path: Path):
    exported = export_bundle(tmp_path)
    assert exported.name == BUNDLE_NAME
    assert (exported / "SKILL.md").exists()
    assert (exported / "references" / "migration.patch").exists()
    assert (exported / "files" / "gateway" / "platforms" / "feishu.py").exists()


def test_reference_text_rejects_unknown_path():
    with pytest.raises(FileNotFoundError):
        reference_text("references/not-real.md")
