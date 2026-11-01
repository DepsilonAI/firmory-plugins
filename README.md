<p align="center"><img src="plugins/ask-firmory/assets/logo-blue.png" alt="Firmory" width="88" height="88"></p>

# Firmory

**Build on your team’s AI work.**

Ask about the files, versions, and sources behind your team’s work, from Codex or Claude Code. Firmory is designed to answer through your connected workspace and let you continue the conversation in Ask Firmory on the web.

English · [繁體中文](README.zh-TW.md)

[Website](https://firmory.ai/) · [Installation guide](docs/installation.md) · [Changelog](CHANGELOG.md) · [Report a problem](https://github.com/DepsilonAI/firmory-plugins/issues/new/choose)

> **Design preview — 0.2.0-alpha.1.** The plugin package can be installed for inspection. Cloud MCP, OAuth sign-in, and web conversation handoff are not ready for use. Installing this preview does not yet enable workspace questions. This repository is a Firmory-managed marketplace; it is not an approved OpenAI or Anthropic directory listing.

## What you will be able to ask

These are intended use cases, not results from a working cloud integration:

- Which files did my team update this week?
- Help me check which version of the brief a report was based on.
- I’m revising a spec. Which documents were built from its current version?

## Install the preview

Use a client version that supports plugin marketplaces. No local MCP server, Node.js, or Python runtime is required by this package. A Firmory account with access to a team will be required when cloud connectivity is available.

### Codex

Run in your terminal:

```sh
codex plugin marketplace add DepsilonAI/firmory-plugins
codex plugin add ask-firmory@firmory-plugins
```

Start a new chat after installation. The display name is **Firmory**; its stable package identifier is `ask-firmory`.

### Claude Code

Run in your terminal:

```sh
claude plugin marketplace add DepsilonAI/firmory-plugins
claude plugin install ask-firmory@firmory-plugins
```

Start a new session after installation. Once cloud connectivity is released, run `/ask-firmory:setup` in Claude Code to connect your workspace.

See the [installation guide](docs/installation.md) for the Codex app flow, verification, updates, removal, and troubleshooting.

## First-use flow

The planned experience is:

1. Install Firmory in your preferred client.
2. Run Firmory setup and sign in through the client’s connection flow.
3. Confirm the connected team.
4. Ask a question and receive an answer with the available file-version references.
5. Open the returned Ask Firmory link to continue the same private conversation on the web.

Steps 2–5 require the pending cloud implementation. Setup must confirm the team through a successful service call before reporting that it is connected.

## Data and access

The intended integration sends your question and relevant file, timezone, or conversation context to Firmory. Firmory’s agent reads accessible workspace history and stores the exchange in a private conversation. Asking a question can therefore create conversation data even though it does not edit workspace files.

The package contains two skills, brand assets, and remote MCP configuration. It includes no local server executable, install script, or lifecycle hook. Sign-in credentials belong in the client’s connection flow, never in a chat or GitHub issue. See the [plugin description](plugins/ask-firmory/README.md), [privacy policy](https://firmory.ai/privacy), and [terms](https://firmory.ai/terms).

## Repository layout

```text
.agents/plugins/marketplace.json       Codex catalog
.claude-plugin/marketplace.json        Claude Code catalog
plugins/ask-firmory/
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
