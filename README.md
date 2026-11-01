# Firmory plugins

Firmory connects a team's AI work through files, versions, and recorded source relationships. This repository contains the plugin package and catalogs for Codex and Claude Code.

## Preview status

Version 0.2.0-alpha.1 is a design preview. Both clients can install the package from this catalog. The proposed remote MCP endpoint, OAuth connection, and web conversation handoff still require backend implementation and end-to-end testing before release.

## Install the preview

For Codex, add the marketplace and install the plugin.

```sh
codex plugin marketplace add DepsilonAI/firmory-plugins
codex plugin add ask-firmory@firmory-plugins
```

For Claude Code, add the same marketplace and install the plugin.

```sh
claude plugin marketplace add DepsilonAI/firmory-plugins
claude plugin install ask-firmory@firmory-plugins
```

The store display name is Firmory. The stable package identifier is ask-firmory.

## Package contents

The catalogs in .agents/plugins and .claude-plugin point to the same plugin folder. The skills and brand assets are shared. Each client has its own MCP configuration format.

See [the plugin README](plugins/ask-firmory/README.md) for its intended behavior and data flow.

## Release preparation

Before publishing, complete remote MCP and OAuth testing, confirm the plugin's distribution license, and prepare a dedicated review account. Directory approval is handled separately by OpenAI and Anthropic.

[Firmory](https://firmory.ai/) · [Privacy](https://firmory.ai/privacy) · [Terms](https://firmory.ai/terms)
