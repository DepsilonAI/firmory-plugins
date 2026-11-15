---
name: setup
description: Sign in to Firmory, verify the connected team, and resume the user's workspace question after authorization.
---

# Connect Firmory

Preserve the user's original question. Setup establishes the connection; it is not a replacement task.

1. Discover the tools exposed by this plugin's `firmory_cloud` connection. The host may prefix tool names. If `workspace` is available, call it with `{}` now; a protected call lets the host request OAuth when needed. Do not require the user to confirm that they have signed in before making this read-only call.
2. If the host reports missing or expired authorization, use its Firmory Connect or Sign in action to start the browser OAuth flow. Let the user sign in, select the intended team, and approve access there. Keep passwords, verification codes, tokens, and callbacks out of chat. Do not construct an authorization URL, visit the website's generic sign-in page as a substitute, or request credentials in chat.
3. If tools are not loaded, inspect the installed Firmory connection with the host's available plugin/connection discovery controls first. Start its connection flow when an authentication action is available. A missing tool alone does not prove the session is expired. If the host has no connection action but is running Codex with terminal access, use the Codex terminal fallback below. For other hosts without a supported action, give one concise instruction to open Firmory's connection settings and sign in. Do not invent a tool, claim a browser was opened, or repeatedly invoke setup.
4. Once the host reports authorization complete, rediscover tools if necessary and call `workspace({})` again. Check `isError` before reading `structuredContent.team.name`, `space.rootNodeId`, or `space.teamLibraryNodeId`. Only confirm connection after a successful workspace response. Resume the original read-only question automatically when the host allows continuation; do not require a special reply such as "Connected". If the host requires another turn, tell the user to retry their original question once authorization finishes.
5. On declined authorization, stop. On a service outage or permission error, report that error instead of starting an endless sign-in loop. When switching teams, reconnect for the intended team, discard previous IDs and cursors, and verify the new workspace before continuing.

If setup was the only request, confirm the team and offer: "Show me the projects and files available in my workspace". Otherwise continue the requested task using the Firmory skill. Answer in the user's language; the supplied starter questions remain in English.

## Verify a connection requested by the Firmory website

When the user supplies a connection challenge from Firmory, complete the normal authorization and workspace check above, then discover and call this connection's `verify_connection` tool with `{ "challenge": "<the supplied challenge>" }`. Do not generate or alter a challenge, send it to another connection, or include it in the final reply. If the tool reports an error or is unavailable, report that the website connection has not been verified. An expired challenge requires a new check from the website; a permission or team mismatch requires the intended team, not repeated sign-in attempts.

Check `isError` before reading the result. Only a successful response with `connectionCheck.status` equal to `verified` confirms the website check. Report the returned team and, when present, project so the user can confirm the intended workspace. Workspace access alone does not complete this website check. Continue the user's original task after verification. A challenge is optional for ordinary plugin setup; do not require one unless the user is completing this website flow.

## Codex terminal fallback

Use this only in Codex when its Firmory connection action is unavailable and terminal execution is supported. Run the installed Codex CLI yourself; do not stop at telling the user to find a sign-in button. Prefer `codex` on PATH. On macOS, if it is absent, check the app-bundled executable at `/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex` and use it only if present.

```sh
codex -c 'mcp_servers.firmory_cloud.url="https://firmory.ai/mcp"' mcp login firmory_cloud --scopes user:org:read --oauth-client-registration cimd
```

The temporary URL override lets the CLI find this plugin's server without adding a second persistent connection. Let Codex generate and open the authorization flow and store its own credentials. Do not read credential files, copy tokens, construct callback URLs, or substitute another provider's CLI. Keep the login process alive while the user completes the browser flow; do not start overlapping attempts. If it times out, report that the attempt expired before offering a fresh attempt. Do not retry a declined authorization.

A zero exit status confirms authorization, not workspace access. Reload the host's MCP connection if that control is available, rediscover tools, and verify `workspace` before resuming the original question. If tools still fail to load, report the actual loading error; do not send the user through sign-in again. If this chat cannot refresh tools, ask the user to open a new chat with Firmory and retry their original question.
