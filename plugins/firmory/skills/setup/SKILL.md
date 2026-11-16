---
name: setup
description: Authorize a Firmory account, select or switch the team through MCP, and resume the user's workspace task.
---

# Connect Firmory

Preserve the user's original question. Setup establishes the connection; it is not a replacement task.

1. Discover the tools exposed by this plugin's `firmory_cloud` connection. The host may prefix tool names. If `get_current_team` is available, call it with `{}` now; a protected call lets the host request OAuth when needed. Do not require the user to confirm that they have signed in before making this read-only call. An older service may expose only `workspace`; call that to check the existing connection, but do not invent team tools or claim switching is supported.
2. If authorization is missing or expired, use the host's Firmory Connect or Sign in action to start browser OAuth. Let the user sign in and authorize their account. New connections use `openid` without `user:org:read`, so team selection happens through MCP after authorization. Keep credentials and callbacks out of chat. Do not construct authorization URLs or visit generic sign-in as a substitute.
3. If tools are not loaded, inspect the installed Firmory connection with the host's plugin/connection discovery controls first. Start its connection flow when available. A missing tool alone does not prove expiration. If no connection action is available in Codex with terminal access, use the fallback below. In other hosts, give one concise instruction to open Firmory connection settings and sign in. Do not invent tools or repeatedly invoke setup.
4. After authorization, rediscover tools if necessary and call `get_current_team({})`. Check `isError` before reading results. If no team is selected or the task names a different team, call `list_teams`; follow `nextOffset` with the same limit as needed. Match the task's intended team to a returned ID. If several match or the intended team is unclear, ask which team; if only one team is available, select it. Call `switch_team` with that `teamId`, then verify using the returned workspace or `workspace({})`. Report the selected team only after success. Discard all previous team IDs and cursors after a successful switch. Resume the original task automatically when the host permits continuation.
5. On declined authorization, stop. On `REAUTHORIZATION_REQUIRED`, the old organization-only grant needs one new account authorization with `openid`; never treat it as account-wide access. On `TEAM_NOT_SELECTED`, select a team through MCP instead of signing in again. Report outages and permission errors without an endless login loop. Switching teams on an account grant uses `switch_team`, independently of the browser; serialize switching with other calls on the same credential.

If setup was the only request, confirm the team and offer: "Show me the projects and files available in my workspace". Otherwise continue the requested task using the Firmory skill. Answer in the user's language; the supplied starter questions remain in English.

## Verify a connection requested by the Firmory website

When the user supplies a connection challenge from Firmory, complete the normal authorization and workspace check above, then discover and call this connection's `verify_connection` tool with `{ "challenge": "<the supplied challenge>" }`. Do not generate or alter a challenge, send it to another connection, or include it in the final reply. If the tool reports an error or is unavailable, report that the website connection has not been verified. An expired challenge requires a new check from the website; a permission or team mismatch requires the intended team, not repeated sign-in attempts.

Check `isError` before reading the result. Only a successful response with `connectionCheck.status` equal to `verified` confirms the website check. Report the returned team and, when present, project so the user can confirm the intended workspace. Workspace access alone does not complete this website check. Continue the user's original task after verification. A challenge is optional for ordinary plugin setup; do not require one unless the user is completing this website flow.

## Codex terminal fallback

Use this only in Codex when its Firmory connection action is unavailable and terminal execution is supported. Run the installed Codex CLI yourself; do not stop at telling the user to find a sign-in button. Prefer `codex` on PATH. On macOS, if it is absent, check the app-bundled executable at `/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex` and use it only if present.

```sh
codex -c 'mcp_servers.firmory_cloud.url="https://firmory.ai/mcp"' mcp login firmory_cloud --scopes openid --oauth-client-registration cimd
```

The temporary URL override lets the CLI find this plugin's server without adding a second persistent connection. Let Codex generate and open the authorization flow and store its own credentials. Do not read credential files, copy tokens, construct callback URLs, or substitute another provider's CLI. Keep the login process alive while the user completes the browser flow; do not start overlapping attempts. If it times out, report that the attempt expired before offering a fresh attempt. Do not retry a declined authorization.

A zero exit status confirms account authorization, not team selection or workspace access. Reload the host's MCP connection if that control is available, rediscover tools, and use `get_current_team`, `list_teams`, and `switch_team` as needed to verify the workspace before resuming the original question. If tools still fail to load, report the actual loading error; do not send the user through sign-in again. If this chat cannot refresh tools, ask the user to open a new chat with Firmory and retry their original question.
