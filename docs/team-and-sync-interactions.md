# Team authorization and sync interactions

## Change team

User asks to change team → read current workspace → request_team_authorization(currentTeamId) → host OAuth UI → choose Change on Firmory consent and authorize the target team → verify workspace → resume the original task. If authorization is cancelled or the team is wrong, report that outcome without repeating the login flow. If the host does not surface the auth challenge, use its existing connection settings. Project changes never use this flow.

The MCP tool changes no membership, grant, or selected-team row. A retry with a newly authorized team returns its workspace, preventing another challenge after success. Actual OAuth UI behavior must be tested in each host; a valid protocol response alone is not proof that a browser opened.

## Local edits

Successful deliverable edits → one grouped reminder at task completion → Sync to Firmory / Later. Sync verifies team, project, destination, and current remote version before using the existing write/upload tools. Later leaves the files local. Pending review, conflicts, failures, and uncertain writes are reported separately from Saved. No background upload, filesystem watcher, or new synchronization database is introduced.

The shared PostToolUse hook runs on supported local editing tools in trusted local Codex/Claude Code installations. It adds model context without transmitting files. It cannot observe external editor changes, arbitrary shell writes, or local files from a web-only session. Skills cover changes the agent can observe in those contexts.
