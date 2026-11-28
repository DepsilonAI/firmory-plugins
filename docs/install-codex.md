# Firmory for Codex

[Illustrated installation guide](https://firmory.ai/download#codex) · [Releases](https://github.com/DepsilonAI/firmory-plugins/releases)

1. Install Codex with plugin support and sign in to your account.
2. Open **Customize → Plugins** in Codex. Drag the Firmory Codex ZIP into that page and follow the installation prompts. Keep the ZIP compressed; no extraction is needed.
3. In a new Codex chat, select **Firmory** and ask "Show me the projects and files available in my workspace". When sign-in is needed, the plugin starts Codex's browser authorization from the task.
4. In the browser, sign in to your Firmory account and allow access. Return to Codex to select a team. You can say "Switch to the Design team" or "Switch my Firmory account" to use another authorized team or account.
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

This ZIP connects to https://firmory.ai/mcp using browser sign-in. It can read the files your team permits and save changes when you ask. [Privacy](https://firmory.ai/privacy) · [Terms](https://firmory.ai/terms).

## Capture work as a Skill

Ask `@Firmory` to do a task and capture it in Firmory, then work through the task in the same chat. Reusable materials go to the project's production library as they become ready. At the end, Codex saves a Skill with the method and links to its materials. Ask for a link others can reuse to enable public sharing. They can paste that link into a new chat along with their own task.

## Sync reminders

Local installers include a file-edit hook. Enable and trust the hook when your client asks; Python 3 must be available. At task completion, Firmory offers Sync now, Remind me next time, or Sync settings using available host choices. "Edit locally first" skips the sync question and upload. Settings support asking after changes, explicitly authorized automatic sync of linked files, or manual sync only, scoped to the current user/team/project/local workspace. Local clients can remember the mode when requested; web clients without persistent preferences keep it in the current conversation. Automatic mode handles future observed edits, not background syncing, and never silently overwrites conflicts. Hooks cannot watch arbitrary shell commands or external editors; web plugins cannot watch local files.
