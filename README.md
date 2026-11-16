<p align="center"><img src="plugins/firmory/assets/logo-blue.png" alt="Firmory" width="88" height="88"></p>

# Firmory

**Build on shared digital assets**

Connect Codex or Claude Code to your Firmory workspace. Find a project, pick a file, and trace the versions recorded as its sources.

English · [繁體中文](README.zh-TW.md)

[Website](https://firmory.ai/) · [Installation guide](docs/installation.md) · [Changelog](CHANGELOG.md) · [Report a problem](https://github.com/DepsilonAI/firmory-plugins/issues/new/choose)

**Version 1.1.0** · [MCP endpoint](https://firmory.ai/mcp). This package is distributed from Firmory’s own marketplace.

## ZIP downloads

[Codex ZIP](https://github.com/DepsilonAI/firmory-plugins/releases/download/v1.1.0/firmory-1.1.0-codex.zip) · [Claude Code ZIP](https://github.com/DepsilonAI/firmory-plugins/releases/download/v1.1.0/firmory-1.1.0-claude-code.zip) · [Illustrated installation guide](https://firmory.ai/download#plugins)

Drag the Codex ZIP into **Customize → Plugins** without extracting it, or use the GitHub install commands below for Codex CLI. Extract the Claude Code ZIP and follow its README.

## Codex

```sh
codex plugin marketplace add DepsilonAI/firmory-plugins
codex plugin add firmory@firmory-plugins
codex -c 'mcp_servers.firmory_cloud.url="https://firmory.ai/mcp"' mcp login firmory_cloud --scopes openid --oauth-client-registration cimd
```

Authorize your Firmory account in the browser. Open a new chat and run Firmory setup to select and confirm the team. The account can access its permitted teams without signing in again for each switch. To install from the app, see the [installation guide](docs/installation.md).

## Claude Code

```sh
claude plugin marketplace add DepsilonAI/firmory-plugins
claude plugin install firmory@firmory-plugins
```

Start a new session. Use `/mcp` to authenticate the Firmory cloud connection, then run `/firmory:setup`. Access requires a Firmory account with team access. No local Firmory CLI is needed.

## Start a conversation

- Show me the projects and files available in my workspace
- Find the project brief and summarize its goals and key decisions
- Open "Welcome.pdf" and summarize its key points

Ask "Which team am I using?", "List my teams", or "Switch to the Design team". The AI uses `get_current_team`, `list_teams`, and `switch_team`; subsequent file operations use the selected team. Firmory checks current membership and permissions on every operation. Team selection is shared by calls using the same OAuth credential and is independent of the team selected in the browser.

Firmory returns records visible in the selected team. You can follow up about a file or version in the same Codex or Claude Code conversation.

Version 1.1.0 requires the account-aware MCP backend described in [the rollout guide](docs/account-teams.md). Older published downloads use organization-bound authorization; reconnect once with the account scope after rollout.

## Data and access

The host sends the arguments needed for each tool call to Firmory, such as a search term or file and version identifiers. Firmory controls which tools and records the account can access. The lookup workflow does not submit changes to answer questions. Never paste credentials into a chat or issue. See the [plugin description](plugins/firmory/README.md), [privacy policy](https://firmory.ai/privacy), and [terms](https://firmory.ai/terms).

## Repository layout

```text
.agents/plugins/marketplace.json       Codex catalog
.claude-plugin/marketplace.json        Claude Code catalog
plugins/firmory/
  plugin.json                         Portable manifest + OpenAI presentation
  mcp.json                            Portable remote MCP configuration
  .claude-plugin/plugin.json           Claude manifest
  .claude-plugin/icon.png              Claude directory icon
  .mcp.json                           Claude remote MCP configuration
  skills/                             Shared setup and Firmory workflows
  assets/                             Shared brand assets
```

Both catalogs point to the same plugin folder. The backend and customer workspace data are not part of this repository.

## Support and maintenance

Use [GitHub issues](https://github.com/DepsilonAI/firmory-plugins/issues/new/choose) for package or documentation problems. See [SECURITY.md](SECURITY.md) for private vulnerability reports, [CONTRIBUTING.md](CONTRIBUTING.md) for changes, and the [maintainer guide](docs/maintaining.md) for validation and release requirements.

## License

The plugin code and documentation are licensed under the [MIT License](LICENSE). This license does not grant trademark rights in the Firmory name or logos, or access to Firmory’s hosted services.
