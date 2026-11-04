# Firmory for Codex

[Illustrated installation guide](https://firmory.ai/download#codex) · [Releases](https://github.com/DepsilonAI/firmory-plugins/releases)

1. Install Codex with plugin support and sign in to your account.
2. Open **Customize → Plugins** in Codex. Drag `firmory-1.0.1-codex.zip` into that page and follow the installation prompts. Keep the ZIP compressed; no extraction is needed.
3. Connect Firmory in your client's MCP settings. If needed, run this in the terminal.

```sh
codex mcp login firmory_cloud --scopes user:org:read
```

4. In the browser, sign in to Firmory, select your team and allow access. Start a new chat and run Firmory setup to confirm the team.
5. Ask a first question.

- Show me the projects and files available in my workspace
- Find the project brief and summarize its goals and key decisions
- Open "Welcome.pdf" and summarize its key points

## Install from GitHub instead

For Codex CLI installation, run these commands in any folder. The CLI installs from GitHub rather than from this ZIP.

```sh
codex plugin marketplace add DepsilonAI/firmory-plugins
codex plugin add firmory@firmory-plugins
```

The plugin connects to https://firmory.ai/mcp using browser sign-in. It can read the files your team permits and save changes when you ask. [Privacy](https://firmory.ai/privacy) · [Terms](https://firmory.ai/terms).
