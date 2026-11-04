# Install, update, and remove Firmory

[Back to README](../README.md) · [Illustrated installation guide](https://firmory.ai/plugins)

## ZIP installation

Download a client-specific ZIP from [GitHub Releases](https://github.com/DepsilonAI/firmory-plugins/releases), extract the whole directory including hidden catalogs, and follow its README. See [Codex ZIP instructions](install-codex.md) or [Claude Code ZIP instructions](install-claude-code.md).

## Prerequisites

Use a Firmory account with access to the intended team. Package inspection requires no account. Sign in using your client’s OAuth browser flow; never paste a token into a client configuration or chat.

Use a client with plugin marketplace support and working GitHub access. Package loading was checked with Codex CLI `0.166.0-alpha.5.1` and Claude Code `2.1.284`; these are tested versions, not claimed minimum versions. Other versions have not been verified.

## Codex app

1. Open Plugins and choose **Add plugin marketplace**.
2. Enter `DepsilonAI/firmory-plugins` as the repository source, using `main` as the Git ref if requested. Leave sparse paths blank.
3. Open the Firmory marketplace and install **Firmory**.
4. Choose the plugin’s connection action to authorize the production service in your browser. Start a new chat and run Firmory setup to confirm the team. If the app does not offer sign-in, use the Codex login command in the README.

UI labels can vary by client version. If the marketplace action is unavailable, use the terminal commands in the [README](../README.md#codex). Adding the marketplace and installing its plugin are separate steps. Installation is not confirmation that the cloud service is connected.

## Claude Code

Use the terminal commands in the [README](../README.md#claude-code), then open a new session. You can inspect the installed package with:

```sh
claude plugin list
claude plugin details firmory
```

Expect the package `firmory@firmory-plugins` and the `firmory` and `setup` skills. In a new session, use `/mcp` to select the plugin’s Firmory cloud server and authenticate, then run `/firmory:setup`. Choose the plugin connection if a local Firmory server is also installed. From the terminal, `claude mcp list` shows this connection as `plugin:firmory:firmory_cloud`; `claude mcp login plugin:firmory:firmory_cloud` starts its OAuth flow.

## Verify the installation

In Codex, use `codex plugin list` or the Plugins panel to find Firmory. In either client, inspect the package’s two skills and the remote MCP server configuration. A configured server URL does not prove that the server is reachable or authenticated.

The remote service is `https://firmory.ai/mcp`. In Codex, `codex mcp list` should show `firmory_cloud`. A 401 before sign-in is expected. After authorization, run setup and verify the **team name from a successful cloud read**. A successful install or a browser redirect alone is not a workspace verification.

## Update

Run in your terminal for Codex:

```sh
codex plugin marketplace upgrade firmory-plugins
codex plugin add firmory@firmory-plugins
```

For Claude Code:

```sh
claude plugin marketplace update firmory-plugins
claude plugin update firmory@firmory-plugins
```

Start a new chat or session afterward. Review the [changelog](../CHANGELOG.md) before updating. Updating the catalog alone is not the same as updating the installed plugin.

## Remove

For Codex:

```sh
codex plugin remove firmory@firmory-plugins
codex plugin marketplace remove firmory-plugins
```

For Claude Code:

```sh
claude plugin uninstall firmory@firmory-plugins
claude plugin marketplace remove firmory-plugins
```

Start a new chat or session afterward. Removing the client plugin is separate from deleting data already held by Firmory. Manage account data and connection permissions separately in the relevant account settings.

## Troubleshooting

| Symptom | Next step |
| --- | --- |
| `plugin` command is not recognized | Check your client version and its plugin support. |
| Marketplace added, but Firmory is absent | Install `firmory@firmory-plugins`; adding a catalog does not install its contents. |
| Skills are missing after installation | Start a new session and verify the plugin is enabled in the client. |
| 401 or sign-in required | Authenticate the plugin connection with the intended account, then run setup. |
| Client cannot register with the authorization server | Use a client with OAuth client ID metadata document (CIMD) support. The issuer advertises CIMD, not dynamic client registration. |
| The URL is the old `api.firmory.ai` address or returns 404 | Update the marketplace and installed plugin, then check that `firmory_cloud` uses the production URL above. |
| How do I follow up about a file? | Continue in the same Codex or Claude Code chat and refer to the file and version. |
| A newer package does not appear | Refresh the marketplace, update the plugin, then start a new session. |
| A connection shows the wrong team | Switch accounts or teams in connection settings and run setup again; wait for the service to confirm the team. |

For another package problem, [open an issue](https://github.com/DepsilonAI/firmory-plugins/issues/new/choose) with your client version, plugin version, installation command, and a redacted error. Do not include private workspace content or credentials.

References: [OpenAI packaging](https://developers.openai.com/plugins/build/plugins) · [Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces).
