"""Docs publisher safety and stand isolation; no host containers or keys used."""
import json
from pathlib import Path
import sys
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from docs import stack


@pytest.mark.parametrize("host", ["0.0.0.0", "8.8.8.8", "192.0.2.1", "localhost", "::", "169.254.1.1"])
def test_no_public_or_wildcard_docs_bind(host):
    with pytest.raises(ValueError):
        stack.address(host)


def test_settings_use_monitoring_lan_then_saved_override(tmp_path):
    directory = tmp_path / "monitoring"
    directory.mkdir()
    (directory / "monitoring.env").write_text("MONITORING_HOST=192.168.0.100\nGRAFANA_ADMIN_PASSWORD=not-for-docs\n")
    assert stack.settings(tmp_path) == {"host": "192.168.0.100", "port": 8008}
    directory = tmp_path / "docs-site"
    directory.mkdir()
    (directory / "settings.json").write_text(json.dumps({"host": "127.0.0.1", "port": 18008}))
    assert stack.settings(tmp_path) == {"host": "127.0.0.1", "port": 18008}
    assert stack.settings(tmp_path, "192.168.1.5", 8009) == {"host": "192.168.1.5", "port": 8009}
    assert "not-for-docs" not in stack.nginx(stack.settings(tmp_path))


@pytest.mark.parametrize("port", [80, -1, 65536, True])
def test_port_bounds(tmp_path, port):
    with pytest.raises(ValueError):
        stack.settings(tmp_path, "127.0.0.1", port)


def test_project_is_per_stand_and_nginx_is_static_only(tmp_path):
    assert stack.project(tmp_path / "a") != stack.project(tmp_path / "b")
    config = stack.nginx({"host": "192.168.0.100", "port": 8008})
    assert "listen 192.168.0.100:8008;" in config
    assert "autoindex off;" in config and "disable_symlinks on;" in config
    assert "limit_except GET" in config and "proxy_pass" not in config
    for name in ("client_body", "proxy", "fastcgi", "uwsgi", "scgi"):
        assert name+"_temp_path /tmp/" in config  # read-only container filesystem


def test_release_must_be_inside_the_docs_directory(tmp_path, monkeypatch):
    directory = tmp_path / "docs-site"
    directory.mkdir()
    stack.save(directory / "settings.json", {"site": str(tmp_path)})
    calls = []
    monkeypatch.setattr(stack.subprocess, "run", lambda *args, **kwargs: calls.append(args))
    with pytest.raises(ValueError, match="release"):
        stack.compose(tmp_path, {"host": "127.0.0.1", "port": 8008}, "up")
    assert calls == []


def test_public_canonical_url_is_saved_without_public_binding(tmp_path):
    config = stack.settings(tmp_path, "192.168.0.100", 8008, "https://docs.computechain.space/")
    directory = tmp_path / "docs-site"
    directory.mkdir()
    stack.save(directory / "settings.json",config)
    assert stack.settings(tmp_path) == config
    assert config["host"] == "192.168.0.100"


@pytest.mark.parametrize("url",["http://docs.computechain.space/","https://user:pass@example.com/","https://example.com/path/","https://example.com/?a=1","https://example.com/#x"])
def test_reject_ambiguous_canonical_url(tmp_path,url):
    with pytest.raises(ValueError):
        stack.settings(tmp_path,"127.0.0.1",8008,url)
