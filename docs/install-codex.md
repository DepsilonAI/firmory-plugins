# Firmory for Codex

[Illustrated installation guide](https://firmory.ai/download#codex) · [Releases](https://github.com/DepsilonAI/firmory-plugins/releases)

1. Install Codex with plugin support and sign in to your account.
2. Open **Customize → Plugins** in Codex. Drag the downloaded Codex ZIP into that page and follow the installation prompts. Keep the ZIP compressed; no extraction is needed.
3. Connect Firmory in your client's MCP settings. If needed, run this in the terminal.

```sh
codex -c 'mcp_servers.firmory_cloud.url="https://firmory.ai/mcp"' mcp login firmory_cloud --scopes user:org:read --oauth-client-registration cimd
```

4. In the browser, sign in to Firmory, select your team and allow access. Ask "Show me the projects and files available in my workspace". Firmory verifies the team while answering; no separate setup question is needed.
5. Ask a first question.

- Show me the projects and files available in my workspace
- Summarize the latest saved context for this project
- Find files that still reference an earlier version of a file

## Install the production plugin from GitHub instead

For Codex CLI installation, run these commands in any folder. These install the production plugin from GitHub. To keep this ZIP's environment, use the ZIP instructions above.

```sh
codex plugin marketplace add DepsilonAI/firmory-plugins
codex plugin add firmory@firmory-plugins
```

This ZIP connects to https://firmory.ai/mcp using browser sign-in. It can read the files your team permits and save changes when you ask. [Privacy](https://firmory.ai/privacy) · [Terms](https://firmory.ai/terms).

## Sync reminders

Firmory checks relevant linked files while you work. When it discovers an edit, choose **Sync now**, **Enable automatic sync**, or **Remind next time**. If the remote version also changed, review the differences before saving.
