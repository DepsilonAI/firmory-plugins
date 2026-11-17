---
name: setup
description: Recover a missing Firmory connection or explicitly request team reauthorization, then continue the user's original task.
---

# Connect Firmory

Use this skill only for missing authorization, an explicit connection request, or changing the authorized team. Connected starter questions use the Firmory skill directly; do not route them through a separate setup conversation. Preserve the user's original task and continue it after authorization. Do not produce a generic welcome, repeat the plugin name, or ask the user to retype a task that can already run.

If the user explicitly requests reauthorization or a team change, use Change the authorized team below even when the current connection still works. A successful workspace read is not completion of that request.

1. Discover the tools exposed by this plugin's `firmory_cloud` connection. The host may prefix tool names. If `workspace` is available, call it with `{}` now; a protected call lets the host request OAuth when needed. Do not require the user to confirm that they have signed in before making this read-only call.
2. If the host reports missing or expired authorization, use its Firmory Connect or Sign in action to start the browser OAuth flow. Let the user sign in, select the intended team, and approve access there. Keep passwords, verification codes, tokens, and callbacks out of chat. Do not construct an authorization URL, visit the website's generic sign-in page as a substitute, or request credentials in chat.
3. If tools are not loaded, inspect the installed Firmory connection with the host's available plugin/connection discovery controls first. Start its connection flow when an authentication action is available. A missing tool alone does not prove the session is expired. Use the Codex terminal fallback below only for a directly configured CLI MCP server. CLI login does not reconnect a hosted Firmory App plugin. For other hosts without a supported action, give one concise instruction to open Firmory's connection settings and sign in. Do not invent a tool, claim a browser was opened, or repeatedly invoke setup.
4. Once the host reports authorization complete, rediscover tools if necessary and call `workspace({})` again. Check `isError` before reading `structuredContent.team.name`, `space.rootNodeId`, or `space.teamLibraryNodeId`. Only confirm connection after a successful workspace response. Resume the original read-only question automatically when the host allows continuation; do not require a special reply such as "Connected". If the host requires another turn, tell the user to retry their original question once authorization finishes.
5. On declined authorization, stop. On a service outage or permission error, report that error instead of starting an endless sign-in loop. When the user asks to switch teams, follow the flow below.

If an explicit setup request has no pending task, finish by showing the authorized team and its current accessible projects via `browse_folder` on the returned root, using pagination or clearly marking a partial listing. Do not end with "Connected, try asking...". For a verification-only request, report the verified connection without unrelated browsing. Otherwise continue the original task using the Firmory skill. Answer in the user's language; the supplied starter questions remain in English.

## Verify a connection requested by the Firmory website

When the user supplies a connection challenge from Firmory, complete the normal authorization and workspace check above, then discover and call this connection's `verify_connection` tool with `{ "challenge": "<the supplied challenge>" }`. Do not generate or alter a challenge, send it to another connection, or include it in the final reply. If the tool reports an error or is unavailable, report that the website connection has not been verified. An expired challenge requires a new check from the website; a permission or team mismatch requires the intended team, not repeated sign-in attempts.

Check `isError` before reading the result. Only a successful response with `connectionCheck.status` equal to `verified` confirms the website check. Report the returned team and, when present, project so the user can confirm the intended workspace. Workspace access alone does not complete this website check. Continue the user's original task after verification. A challenge is optional for ordinary plugin setup; do not require one unless the user is completing this website flow.

## Codex terminal fallback

Use this only for a directly configured Codex CLI MCP server when terminal execution is supported. It does not reconnect the hosted Firmory App plugin; use that plugin's own connection controls instead. Prefer `codex` on PATH. On macOS, if it is absent, check the app-bundled executable at `/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex` and use it only if present.

```sh
codex -c 'mcp_servers.firmory_cloud.url="https://firmory.ai/mcp"' mcp login firmory_cloud --scopes user:org:read --oauth-client-registration cimd
```

The temporary URL override lets the CLI find this plugin's server without adding a second persistent connection. Let Codex generate and open the authorization flow and store its own credentials. Do not read credential files, copy tokens, construct callback URLs, or substitute another provider's CLI. Keep the login process alive while the user completes the browser flow; do not start overlapping attempts. If it times out, report that the attempt expired before offering a fresh attempt. Do not retry a declined authorization.

A zero exit status confirms authorization, not workspace access. Reload the host's MCP connection if that control is available, rediscover tools, and verify `workspace` before resuming the original question. If tools still fail to load, report the actual loading error; do not send the user through sign-in again. If this chat cannot refresh tools, ask the user to open a new chat with Firmory and retry their original question.


## Change the authorized team

Only start this flow when the user asks to change teams or explicitly requests reconnect/reauthorization. A project change inside the current team never needs reauthorization.

1. Call `workspace` to identify the current team. If it already matches the requested team unambiguously and the user did not explicitly request reauthorization, continue without another authorization. If authentication is missing, start the host's connection flow instead.
2. Discover this Firmory connection's `request_team_authorization` tool using the host's tool search/refresh capability when available; do not conclude it is unavailable just because it is absent from the initially loaded tools. Do not call obsolete `list_teams`, `get_current_team`, or `switch_team`, even if stale host metadata advertises them. Team selection happens on the OAuth consent page, not through a cross-team data query.
3. Once discovered, call `request_team_authorization` once with `currentTeamId` from the workspace response. Do not skip this call because workspace access is still valid. Its authorization challenge requests the host's OAuth UI; it does not itself switch teams. The user chooses Change on the consent page, selects the intended team, and allows access. Do not require a target team name before opening the picker. Keep the pending task while authorization completes.
4. If discovery still lacks the tool, or a genuine tool-not-found response occurs, refresh/reload the existing connection's tools once through an available supported host control and rediscover. Do not treat missing tool metadata as an expired token or repeatedly retry a missing name. If the host still lacks the tool or does not surface the returned OAuth challenge, use its actual reconnect/sign-in control. For Claude Code use the existing Firmory connection in `/mcp`. For a hosted Firmory App use its own connection settings; CLI credentials do not replace it. Only when no supported action is available, give one concise settings instruction, state that in-chat reauthorization did not start, and stop retrying. Do not construct OAuth URLs, revoke tokens, or uninstall the plugin.
5. After authorization, call `workspace` again. Verify the requested team name when one was provided, otherwise show the actual authorized team. Discard old node IDs and cursors after a team change. If a different team was requested but the same or wrong team was authorized, explain the mismatch without an automatic authorization loop. For reauthorization without a team-change request, successfully verifying the same team is valid. On cancellation, continue using the previous team only if it is still valid and the user wants to continue there.
6. Resume the original task in the verified team. Never report a successful switch or completed authorization based only on an opened page or CLI success. If the user only requested a team change, report the verified team briefly without starting another setup flow.
