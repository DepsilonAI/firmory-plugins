---
name: setup
description: Connect or reconnect the Firmory preview workspace and confirm the authorized team.
---

# Connect Firmory

Use the host’s OAuth connection for this plugin’s `firmory_cloud` server at `https://preview.firmory.ai/mcp`. Let the user sign in and authorize in the browser. Never request a token, cookie, password, or callback URL in chat. Do not use a similarly named local or production server.

After authorization, inspect the tools advertised by that connection. Use its read-only workspace discovery tool (such as `firmory_workspace` if listed), following the actual input schema. Report the team name only from a successful result. If there is no suitable tool, distinguish an authenticated transport from an unverified workspace. Never create an asset or conversation just to test a connection.

If authorization is declined, stop. If the service rejects the session, reconnect through the host; if the wrong team is active, switch in Firmory and verify again. Keep the original question but discard IDs from the previous account or team.

When the team is confirmed, offer: “Which projects can I access in my Firmory workspace?”
