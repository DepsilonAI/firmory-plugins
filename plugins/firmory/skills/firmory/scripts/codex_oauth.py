"""Start Firmory OAuth using the local Codex client's browser and credential store."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess


SERVER = "firmory_cloud"
RESOURCE = "https://firmory.ai/mcp"
BUNDLED_CODEX = Path("/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex")
SCRIPT_DIR = Path(__file__).resolve().parent


def report(status):
    print(json.dumps({"status": status, "resourceUrl": RESOURCE}), flush=True)


def codex_command():
    binary = str(BUNDLED_CODEX) if os.access(BUNDLED_CODEX, os.X_OK) else shutil.which("codex")
    if not binary:
        raise OSError("Codex executable unavailable")
    return [binary, "-c", f"mcp_servers.{SERVER}.url={json.dumps(RESOURCE)}", "mcp"]


def connection_status(command):
    result = subprocess.run(
        [*command, "list", "--json"], cwd=SCRIPT_DIR, capture_output=True, text=True,
        encoding="utf-8", timeout=15, check=True,
    )
    for server in json.loads(result.stdout):
        if server.get("name") != SERVER or server.get("transport", {}).get("url") != RESOURCE:
            continue
        return {
            "o_auth": "authorized",
            "not_logged_in": "authorization_required",
        }.get(server.get("auth_status"), "connection_unavailable")
    return "connection_unavailable"


def authorize(command):
    with subprocess.Popen(
        [*command, "login", SERVER, "--scopes", "openid", "--oauth-client-registration", "cimd"],
        cwd=SCRIPT_DIR, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        encoding="utf-8", errors="replace",
    ) as client:
        try:
            for line in client.stdout:
                if line.strip() == f"Authorize `{SERVER}` by opening this URL in your browser:":
                    report("browser_authorization_pending")
        except KeyboardInterrupt:
            client.terminate()
            return False
        return client.wait() == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("status", "authorize"))
    action = parser.parse_args().action
    try:
        command = codex_command()
        if action == "status":
            report(connection_status(command))
            return 0
        if authorize(command):
            report("authorized")
            return 0
    except (OSError, ValueError, subprocess.SubprocessError):
        pass
    report("authorization_incomplete" if action == "authorize" else "connection_unavailable")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
