import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest


LAUNCHER = Path(__file__).resolve().parents[1] / "plugins/firmory/skills/firmory/scripts/codex_oauth.py"
SPEC = importlib.util.spec_from_file_location("codex_oauth", LAUNCHER)
oauth = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(oauth)


class CodexOauthTests(unittest.TestCase):
    def test_authorize_requests_account_scope_and_keeps_the_oauth_url_out_of_output(self):
        with tempfile.TemporaryDirectory() as directory:
            client = Path(directory) / "client.py"
            client.write_text(
                "import sys\n"
                "assert sys.argv[1:] == ['login', 'firmory_cloud', '--scopes', 'openid', "
                "'--oauth-client-registration', 'cimd']\n"
                "print('Authorize `firmory_cloud` by opening this URL in your browser:')\n"
                "print('https://example.test/authorize?state=private-oauth-state')\n",
                encoding="utf-8",
            )
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertTrue(oauth.authorize([sys.executable, str(client)]))
        self.assertEqual(json.loads(output.getvalue()), {
            "status": "browser_authorization_pending",
            "resourceUrl": "https://firmory.ai/mcp",
        })

    def test_status_ignores_a_same_name_server_at_a_different_endpoint(self):
        with tempfile.TemporaryDirectory() as directory:
            client = Path(directory) / "client.py"
            client.write_text(
                "import json\n"
                "print(json.dumps([{'name': 'firmory_cloud', 'auth_status': 'o_auth', "
                "'transport': {'url': 'https://example.test/mcp'}}]))\n",
                encoding="utf-8",
            )
            self.assertEqual(oauth.connection_status([sys.executable, str(client)]), "connection_unavailable")


if __name__ == "__main__":
    unittest.main()
