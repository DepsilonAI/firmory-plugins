<p align="center"><img src="plugins/firmory/assets/logo-blue.png" alt="Firmory" width="88" height="88"></p>

# Firmory

**Build on shared digital assets**

Connect Codex or Claude Code to your Firmory workspace. Find a project, pick a file, and trace the versions recorded as its sources.

English · [繁體中文](README.zh-TW.md)

[Website](https://firmory.ai/) · [Installation guide](docs/installation.md) · [Changelog](CHANGELOG.md) · [Report a problem](https://github.com/DepsilonAI/firmory-plugins/issues/new/choose)

**Version 1.0.1** · [MCP endpoint](https://firmory.ai/mcp). This package is distributed from Firmory’s own marketplace.

## ZIP downloads

[Codex ZIP](https://github.com/DepsilonAI/firmory-plugins/releases/download/v1.0.1/firmory-1.0.1-codex.zip) · [Claude Code ZIP](https://github.com/DepsilonAI/firmory-plugins/releases/download/v1.0.1/firmory-1.0.1-claude-code.zip) · [Illustrated installation guide](https://firmory.ai/download#plugins)

Drag the Codex ZIP into **Customize → Plugins** without extracting it, or use the GitHub install commands below for Codex CLI. Extract the Claude Code ZIP and follow its README.

## Codex

```sh
codex plugin marketplace add DepsilonAI/firmory-plugins
codex plugin add firmory@firmory-plugins
codex mcp login firmory_cloud --scopes user:org:read
```

Complete sign-in in the browser. Open a new chat and run Firmory setup to confirm the connected team. To install from the app, see the [installation guide](docs/installation.md).

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

Firmory returns records visible to your team. You can follow up about a file or version in the same Codex or Claude Code conversation.

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

A distribution license has not yet been selected. Public visibility is not an open-source license; licensing must be resolved before directory submission.
