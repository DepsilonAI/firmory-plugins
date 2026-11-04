# Firmory for Claude Code

[Illustrated installation guide](https://firmory.ai/download#claude-code) · [Releases](https://github.com/DepsilonAI/firmory-plugins/releases)

1. Install Claude Code with plugin support and sign in to your account.
2. Extract this ZIP. Keep the entire firmory-claude-code folder, including its hidden catalog files.
3. Open a terminal in the extracted firmory-claude-code folder. Run these commands one at a time.

```sh
claude plugin marketplace add .
claude plugin install firmory@firmory-plugins
```

4. Connect Firmory in your client's MCP settings. If needed, run this in the terminal.

```sh
claude mcp login plugin:firmory:firmory_cloud
```

5. In the browser, sign in to Firmory, select your team and allow access. Start a new chat and run Firmory setup to confirm the team. In Claude Code, run /firmory:setup.
6. Ask a first question.

- Show me the projects and files available in my workspace
- Find the project brief and summarize its goals and key decisions
- Open "Welcome.pdf" and summarize its key points

## Install from GitHub instead

```sh
claude plugin marketplace add DepsilonAI/firmory-plugins
claude plugin install firmory@firmory-plugins
```

The plugin connects to https://firmory.ai/mcp using browser sign-in. It can read the files your team permits and save changes when you ask. [Privacy](https://firmory.ai/privacy) · [Terms](https://firmory.ai/terms).
