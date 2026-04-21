from pathlib import Path

from gateway.config import Platform, load_gateway_config


def test_load_gateway_config_bridges_session_reset_platform_overrides(monkeypatch, tmp_path):
    hermes_home = tmp_path / ".hermes"
    hermes_home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))

    (hermes_home / "config.yaml").write_text(
        """
session_reset:
  default:
    mode: idle
    idle_minutes: 60
  platforms:
    feishu:
      mode: none
  types:
    group:
      mode: daily
      at_hour: 5
""".strip()
        + "\n",
        encoding="utf-8",
    )

    config = load_gateway_config()

    assert config.default_reset_policy.mode == "idle"
    assert config.default_reset_policy.idle_minutes == 60
    assert config.reset_by_platform[Platform.FEISHU].mode == "none"
    assert config.reset_by_type["group"].mode == "daily"
    assert config.reset_by_type["group"].at_hour == 5
