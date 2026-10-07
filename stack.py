#!/usr/bin/env python3
"""LAN-only static docs, isolated per stand. No repository/runtime-root mounts."""
import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

REPO = Path(__file__).resolve().parent


def address(host):
    value = ipaddress.IPv4Address(host)
    private = any(value in ipaddress.IPv4Network(net) for net in
        ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "127.0.0.0/8"))
    if not private:
        raise ValueError("docs require a literal private LAN or loopback IPv4")
    return str(value)


def settings(root, host=None, port=None, site_url=None):
    path = root / "docs-site/settings.json"
    saved = json.loads(path.read_text()) if path.exists() else {}
    if host is None:
        envfile = root / "monitoring/monitoring.env"
        monitoring = dict(line.split("=", 1) for line in envfile.read_text().splitlines() if "=" in line) if envfile.exists() else {}
        host = saved.get("host", monitoring.get("MONITORING_HOST", "127.0.0.1"))
    port = port if port is not None else saved.get("port", 8008)
    if type(port) is not int or not 1024 <= port <= 65535:
        raise ValueError("docs port must be 1024..65535")
    result = {"host": address(host), "port": port}
    url = site_url or saved.get("site_url")
    if url:
        from urllib.parse import urlsplit
        parsed = urlsplit(url)
        if parsed.scheme != "https" or not parsed.hostname or parsed.netloc != parsed.hostname or parsed.path != "/" or parsed.query or parsed.fragment:
            raise ValueError("site-url must be a plain HTTPS origin with trailing slash")
        result["site_url"] = url
    return result


def project(root):
    return "cpc-docs-" + hashlib.sha256(str(root.resolve()).encode()).hexdigest()[:10]


def nginx(config):
    return f'''worker_processes 1;
pid /tmp/nginx.pid;
error_log /dev/stderr warn;
events {{ worker_connections 128; }}
http {{
  include /etc/nginx/mime.types;
  default_type application/octet-stream;
  access_log /dev/stdout;
  server_tokens off;
  client_body_temp_path /tmp/client-body;
  proxy_temp_path /tmp/proxy;
  fastcgi_temp_path /tmp/fastcgi;
  uwsgi_temp_path /tmp/uwsgi;
  scgi_temp_path /tmp/scgi;
  keepalive_timeout 10;
  client_header_timeout 5s;
  client_body_timeout 5s;
  send_timeout 10s;
  client_max_body_size 1k;
  server {{
    listen {config["host"]}:{config["port"]};
    server_name _;
    root /usr/share/nginx/html;
    index index.html;
    autoindex off;
    disable_symlinks on;
    absolute_redirect off;
    add_header X-Content-Type-Options nosniff always;
    add_header X-Frame-Options DENY always;
    add_header Referrer-Policy same-origin always;
    add_header Cache-Control "no-cache" always;
    error_page 404 /404.html;
    location = /healthz {{ default_type text/plain; return 200 "ok\\n"; }}
    location ~ (^|/)\\. {{ return 404; }}
    location / {{
      limit_except GET {{ deny all; }}
      try_files $uri $uri/ =404;
    }}
  }}
}}
'''


def build(destination, config):
    # Invoked only in the dedicated docs venv; no blockchain imports or keys.
    from mkdocs.config import load_config
    from mkdocs.commands.build import build as mkdocs_build
    loaded = load_config(config_file=str(REPO / "mkdocs.yml"), strict=True,
        site_dir=str(destination), site_url=config.get("site_url",f'http://{config["host"]}:{config["port"]}/'))
    mkdocs_build(loaded)
    # mktemp is 0700; Nginx's non-root worker needs to traverse this mount only.
    destination.chmod(0o755)
    if any(p.is_symlink() for p in destination.rglob("*")):
        raise ValueError("symlinks are forbidden in published docs")


def compose(root, config, *args):
    directory = root / "docs-site"
    current = json.loads((directory / "settings.json").read_text())
    site = Path(current["site"]).resolve()
    if site.parent != (directory / "releases").resolve() or not (site / "index.html").is_file():
        raise ValueError("invalid docs release path")
    env = {**os.environ, "DOCS_SITE": str(site), "DOCS_CONFIG": str(directory / "nginx.conf"),
        "DOCS_HOST": config["host"], "DOCS_PORT": str(config["port"])}
    subprocess.run(["docker", "compose", "--project-name", project(root), "--file",
        str(REPO / "docker-compose.yml"), *args], env=env, check=True)


@contextmanager
def lock(directory):
    fd = os.open(directory / ".operator.lock", os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "a+b") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield


def save(path, value):
    with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as stream:
        json.dump(value, stream, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
        name = stream.name
    os.replace(name, path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["up", "down", "status", "logs", "build"])
    parser.add_argument("--dir", type=Path, default=REPO.parent / ".runtime/comet-staking-devnet")
    parser.add_argument("--host")
    parser.add_argument("--port", type=int)
    parser.add_argument("--site-url", help="canonical public HTTPS origin; saved across stand restarts")
    parser.add_argument("--destination", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    root = args.dir.resolve()
    config = settings(root, args.host, args.port, args.site_url)
    if args.command == "build":
        if args.destination is None:
            parser.error("internal build requires --destination")
        build(args.destination.resolve(), config)
        return
    directory = root / "docs-site"
    if args.command != "up" and not (directory / "settings.json").exists():
        print("Docs not configured; no containers changed.")
        return
    if not root.is_dir():
        parser.error("stand directory does not exist; start the stand first")
    directory.mkdir(mode=0o700, exist_ok=True)
    with lock(directory):
        if args.command == "up":
            python = REPO.parent / ".tools/docs-venv/bin/python"
            if not python.is_file():
                raise RuntimeError("docs venv missing; see docs README for installation")
            releases = directory / "releases"
            releases.mkdir(exist_ok=True)
            destination = Path(tempfile.mkdtemp(prefix="site-", dir=releases))
            subprocess.run([str(python), str(Path(__file__).resolve()), "build", "--dir", str(root),
                "--host", config["host"], "--port", str(config["port"]), "--destination", str(destination),
                *(["--site-url",config["site_url"]] if "site_url" in config else [])], check=True)
            # Previous releases survive failed builds and stop; only HTML/config mount.
            (directory / "nginx.conf").write_text(nginx(config))
            save(directory / "settings.json", {**config, "site": str(destination)})
            compose(root, config, "up", "-d", "--wait", "--wait-timeout", "60")
            print(f'Docs EN: http://{config["host"]}:{config["port"]}/', flush=True)
            print(f'Docs RU: http://{config["host"]}:{config["port"]}/ru/', flush=True)
        else:
            compose(root, config, *{"down": ["down"], "status": ["ps"], "logs": ["logs", "--tail", "80"]}[args.command])


if __name__ == "__main__":
    main()
