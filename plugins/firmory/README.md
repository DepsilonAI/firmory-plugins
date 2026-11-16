# Firmory

Build on shared digital assets

Use Firmory in Codex or Claude Code to find the projects you can access, check which version of a brief informed a report, or follow a specification to documents that cite it. Run Firmory setup, authorize your account through the browser, then select and confirm the team name. Ask the AI to list your teams, show the current team, or switch teams without authorizing each team separately. Claude Code users can run `/firmory:setup`.

The plugin connects to its configured `firmory_cloud` service over HTTPS. The host sends tool arguments such as search terms, file identifiers, and versions to Firmory. The service returns records available to the selected team. The lookup workflow uses read operations. Follow-up questions stay in the current client conversation.

[Product](https://firmory.ai/) · [Support](https://firmory.ai/#faq) · [Privacy](https://firmory.ai/privacy) · [Terms](https://firmory.ai/terms)

## Start a conversation

- Show me the projects and files available in my workspace
- Find the project brief and summarize its goals and key decisions
- Open "Welcome.pdf" and summarize its key points

[Illustrated installation guide](https://firmory.ai/download).

Team tools: `list_teams` lists currently accessible teams, `get_current_team` reports the current selection, and `switch_team` selects a returned team ID for subsequent calls. Selection belongs to the OAuth connection, independently of the browser. Account authorization remains subject to live team membership and read/write permissions. Older organization-only grants need one new account authorization.
