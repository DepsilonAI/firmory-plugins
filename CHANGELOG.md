# Changelog

## 1.0.1 — public distribution

- Use the new Firmory icon in brand blue #3352E4.
- Start with workspace discovery, project briefing, or a summary of Welcome.pdf when that file is available.
- Provide separate Codex and Claude Code ZIP downloads with illustrated installation instructions at https://firmory.ai/plugins.

## 1.0.0 — first production package

- Install as `firmory@firmory-plugins` in Codex and Claude Code. The package connects to the production Firmory workspace.
- Update the English and Chinese store listings and declare interactive, read, and write capabilities.

## 0.2.0-alpha.3 — preview

- Verify the connected team with `workspace` and use the cloud tool schemas for project discovery and file lineage.
- Build separate preview and production distributions from the same plugin sources.

## 0.2.0-alpha.2 — cloud preview

- Connect both clients to `https://preview.firmory.ai/mcp` through native OAuth.
- Discover the signed-in service’s tools; remove the dependency on a proposed chat tool and guessed handoff format.
- Update setup, prompts, and connection troubleshooting.

### Documentation

- Add a branded English entry point and a Traditional Chinese README.
- Explain the intended first-use flow, preview limitations, and data handling.
- Add installation verification, update, removal, and troubleshooting guidance.
- Add contribution and private security-reporting instructions, issue templates, and a pull request template.
- Document package validation and the remaining release requirements.

## 0.2.0-alpha.1 — design preview

- Publish the shared Firmory plugin folder with Codex and Claude Code marketplace catalogs.
- Include portable and Claude manifests, remote MCP configuration, and two shared skills: `firmory` and `setup`.
- Include the Firmory blue icon and English listing metadata with Traditional Chinese presentation copy.
- Keep the installed package identifier `ask-firmory` and display name Firmory.

Cloud MCP, OAuth connection, and continuing a conversation in Ask Firmory are pending implementation and end-to-end testing. This version is not an approved directory release.
