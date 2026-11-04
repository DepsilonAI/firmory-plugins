---
name: setup
description: Sign in to Firmory, verify the connected team, and resume the user's workspace question after authorization.
---

# Connect Firmory

Preserve the user's original question. Setup establishes the connection; it is not a replacement task.

1. Discover the tools exposed by this plugin's `firmory_cloud` connection. The host may prefix tool names. If `workspace` is available, call it with `{}` now; a protected call lets the host request OAuth when needed. Do not require the user to confirm that they have signed in before making this read-only call.
2. If the host reports missing or expired authorization, use its Firmory Connect or Sign in action to start the browser OAuth flow. Let the user sign in, select the intended team, and approve access there. Keep passwords, verification codes, tokens, and callbacks out of chat. Do not construct an authorization URL, visit the website's generic sign-in page as a substitute, or request credentials in chat.
3. If tools are not loaded, inspect the installed Firmory connection with the host's available plugin/connection discovery controls first. Start its connection flow when an authentication action is available. A missing tool alone does not prove the session is expired. If this host exposes neither the tools nor a connection action, give one concise instruction to open Firmory's connection settings and sign in. Do not invent a tool, claim a browser was opened, or repeatedly invoke setup.
4. Once the host reports authorization complete, rediscover tools if necessary and call `workspace({})` again. Check `isError` before reading `structuredContent.team.name`, `space.rootNodeId`, or `space.teamLibraryNodeId`. Only confirm connection after a successful workspace response. Resume the original read-only question automatically when the host allows continuation; do not require a special reply such as "Connected". If the host requires another turn, tell the user to retry their original question once authorization finishes.
5. On declined authorization, stop. On a service outage or permission error, report that error instead of starting an endless sign-in loop. When switching teams, reconnect for the intended team, discard previous IDs and cursors, and verify the new workspace before continuing.

If setup was the only request, confirm the team and offer: "Show me the projects and files available in my workspace". Otherwise continue the requested task using the Firmory skill. Answer in the user's language; the supplied starter questions remain in English.
