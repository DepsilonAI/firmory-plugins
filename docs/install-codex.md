# Firmory for Codex

[Illustrated installation guide](https://firmory.ai/download#codex) · [Releases](https://github.com/DepsilonAI/firmory-plugins/releases)

1. Install Codex with plugin support and sign in to your account.
2. Open **Customize → Plugins** in Codex. Drag `firmory-1.1.0-codex.zip` into that page and follow the installation prompts. Keep the ZIP compressed; no extraction is needed.
3. Connect Firmory in your client's MCP settings. If needed, run this in the terminal.

```sh
codex -c 'mcp_servers.firmory_cloud.url="https://firmory.ai/mcp"' mcp login firmory_cloud --scopes openid --oauth-client-registration cimd
```

4. In the browser, sign in to Firmory and authorize your account. Start a new chat and run Firmory setup to select and confirm the team. You can then ask the AI to view or switch teams through MCP without signing in again.
5. Ask a first question.

- Show me the projects and files available in my workspace
- Find the project brief and summarize its goals and key decisions
- Open "Welcome.pdf" and summarize its key points

## Install the production plugin from GitHub instead

For Codex CLI installation, run these commands in any folder. These install the production plugin from GitHub. To keep this ZIP's environment, use the ZIP instructions above.

```sh
codex plugin marketplace add DepsilonAI/firmory-plugins
codex plugin add firmory@firmory-plugins
```

This version requires the account-aware MCP backend. Existing organization-only connections need one new account authorization after rollout.

This ZIP connects to https://firmory.ai/mcp using browser sign-in. It can read the files your team permits and save changes when you ask. [Privacy](https://firmory.ai/privacy) · [Terms](https://firmory.ai/terms).
