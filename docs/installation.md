# Install, update, and remove Firmory

[Back to README](../README.md)

## Preview prerequisites

The package is a design preview. You can inspect and install its skills and configuration, but the cloud service, sign-in, and web handoff are not ready. You do not need to supply credentials to inspect the package.

Use a client with plugin marketplace support and working GitHub access. Package loading was checked with Codex CLI `0.166.0-alpha.5.1` and Claude Code `2.1.284`; these are tested versions, not claimed minimum versions. Other versions have not been verified.

## Codex app

1. Open Plugins and choose **Add plugin marketplace**.
2. Enter `DepsilonAI/firmory-plugins` as the repository source, using `main` as the Git ref if requested. Leave sparse paths blank.
3. Open the Firmory marketplace and install **Firmory**.
4. Start a new chat to load the installed package.

UI labels can vary by client version. If the marketplace action is unavailable, use the terminal commands in the [README](../README.md#codex). Adding the marketplace and installing its plugin are separate steps. Installation is not confirmation that the cloud service is connected.

## Claude Code

Use the terminal commands in the [README](../README.md#claude-code), then open a new session. You can inspect the installed package with:

```sh
claude plugin list
claude plugin details ask-firmory
```

Expect the package `ask-firmory@firmory-plugins` and the `firmory` and `setup` skills. Once cloud connectivity is released, `/ask-firmory:setup` will start the connection workflow. At present a missing or unreachable cloud tool is a preview limitation.

## Verify the installation

In Codex, use `codex plugin list` or the Plugins panel to find Firmory. In either client, inspect the package’s two skills and the remote MCP server configuration. A configured server URL does not prove that the server is reachable or authenticated.

The intended remote service is `https://api.firmory.ai/mcp`. Do not replace it with a third-party endpoint to work around a connection failure.

## Update

Run in your terminal for Codex:

```sh
codex plugin marketplace upgrade firmory-plugins
codex plugin add ask-firmory@firmory-plugins
```

For Claude Code:

```sh
claude plugin marketplace update firmory-plugins
claude plugin update ask-firmory@firmory-plugins
```

Start a new chat or session afterward. Review the [changelog](../CHANGELOG.md) before updating. Updating the catalog alone is not the same as updating the installed plugin.

## Remove

For Codex:

```sh
codex plugin remove ask-firmory@firmory-plugins
codex plugin marketplace remove firmory-plugins
```

For Claude Code:

```sh
claude plugin uninstall ask-firmory@firmory-plugins
claude plugin marketplace remove firmory-plugins
```

Start a new chat or session afterward. Removing the client plugin is separate from deleting data already held by Firmory. When cloud access is available, manage account data and connection permissions through the relevant Firmory and client account settings.

## Troubleshooting

| Symptom | Next step |
| --- | --- |
| `plugin` command is not recognized | Check your client version and its plugin support. |
| Marketplace added, but Firmory is absent | Install `ask-firmory@firmory-plugins`; adding a catalog does not install its contents. |
| Skills are missing after installation | Start a new session and verify the plugin is enabled in the client. |
| Connection fails, the endpoint returns 404, or cloud tools are missing | This preview’s cloud integration is pending. Reinstalling does not enable the service. |
| A newer package does not appear | Refresh the marketplace, update the plugin, then start a new session. |
| A future connection shows the wrong team | Switch accounts or teams in connection settings and run setup again; wait for the service to confirm the team. |

For another package problem, [open an issue](https://github.com/DepsilonAI/firmory-plugins/issues/new/choose) with your client version, plugin version, installation command, and a redacted error. Do not include private workspace content or credentials.

References: [OpenAI packaging](https://developers.openai.com/plugins/build/plugins) · [Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces).
