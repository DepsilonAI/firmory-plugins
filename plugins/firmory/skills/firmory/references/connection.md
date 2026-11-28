# Connect Firmory

Use this reference when a requested Firmory feature needs sign-in, or when the user asks to connect, switch accounts, or switch Teams. Keep the original task and resume it when the account and destination Team are verified. An @mention by itself does not start sign-in.

1. Discover the tools on the installed plugin's `firmory_cloud` connection. If `workspace({})` is available, call it before working with Team data. When it returns `team: null` or `TEAM_NOT_SELECTED`, the account is authorized and a Team still needs to be selected.
2. If authorization is missing, start browser authorization. For local Codex use the launcher below. For a hosted Firmory App, start its available connection action. Keep passwords, verification codes, tokens, and callbacks out of chat.
3. After authorization, refresh tool discovery as needed. Verify `workspace` or select the Team if none is active. Report a service or tool loading failure rather than assuming every failed call needs login. On cancellation, keep the unfinished work local.

## Verify a connection requested by the Firmory website

When the user supplies a connection challenge from Firmory, complete the normal authorization and workspace check above, then discover and call this connection's `verify_connection` tool with `{ "challenge": "<the supplied challenge>" }`. Do not generate or alter a challenge, send it to another connection, or include it in the final reply. If the tool reports an error or is unavailable, report that the website connection has not been verified. An expired challenge requires a new check from the website; a permission or team mismatch requires the intended team, not repeated sign-in attempts.

Check `isError` before reading the result. Only a successful response with `connectionCheck.status` equal to `verified` confirms the website check. Report the returned team and, when present, project so the user can confirm the intended workspace. Workspace access alone does not complete this website check. Continue the user's original task after verification. A challenge is optional for ordinary plugin setup; do not require one unless the user is completing this website flow.

## Start browser authorization in local Codex

In local Codex desktop or CLI with shell tools, run `scripts/codex_oauth.py` yourself using Python 3 and the absolute path under this installed Skill. The launcher delegates browser authorization and credential storage for `https://firmory.ai/mcp` to the installed Codex client. The user only interacts with the browser. A hosted Firmory App uses its own connection flow.

1. If the tools are missing, run the launcher with `status`. When it reports `authorization_required`, immediately run it with `authorize`. A known authentication-required error or an explicit sign-in, reconnect, or account-switch request can start `authorize` directly. If status is already `authorized`, first refresh tool discovery.
2. Start only one ongoing command. When it reports `browser_authorization_pending`, ask the user to complete authorization in the Firmory browser page. Keep the process alive while the client can wait. Tell the user to select **Switch account** on the authorization page for an account change, then click **Allow**. The OAuth grant is for the account.
3. After the launcher reports `authorized`, refresh discovery and verify the workspace or select a Team. If the host retains the previous connection and cannot refresh it, continue from a new local chat with the same plugin. Stop on cancellation, failure, or lack of a supported connection action.

Do not construct authorization URLs, ask the user to run a command, read stored credentials, or preemptively sign out the active connection.

## Select or switch Teams after account authorization

1. Call `workspace({})` to verify the selected Team and record `team.id`. If no Team is selected or the user asks to list or switch Teams, call `list_teams`. Follow `nextOffset` with the same `limit` when looking for a named Team or when a complete list is requested.
2. Match an explicitly named Team. If none is selected and the account has exactly one accessible Team, use it. When a choice is needed, show the accessible Team names and ask once. Use only the Team ID returned by `list_teams`.
3. Call `switch_team({teamId})` and use its verified workspace result. Switching Teams on an account grant does not start OAuth. In a mutation, pass the verified `team.id` as `expectedTeamId` when advertised. If the tool reports a Team mismatch, verify the destination again and keep the write paused until the intended Team is established. Discard project IDs, node IDs, and cursors from the earlier Team after a switch.
4. If the tool reports `REAUTHORIZATION_REQUIRED`, the current grant is an older Team-only authorization. Start account authorization once through the appropriate flow, then continue with `list_teams`. A project change inside the same Team requires no authentication.

## Change the authorized account

An explicit account change starts a new OAuth authorization even when the connection already works. Record the current `workspace.actor.userId` when available. In local Codex use the browser launcher. On a hosted App use its account connection action or `request_account_authorization({currentUserId})` when advertised. The user chooses **Switch account** and authorizes the intended account in Firmory.

After authorization, verify that the returned account changed. If no Team is selected yet, use `list_teams` to choose one and check `workspace.actor.userId` on the new workspace. If the original account is still connected, report the result and stop the switch attempt. Use only newly verified Teams and IDs when resuming the user's task.
