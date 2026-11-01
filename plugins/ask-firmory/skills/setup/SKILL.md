---
name: setup
description: Connect the user's Firmory workspace when they choose setup or ask to connect Firmory.
---

# Connect Firmory

Use the host's Firmory connection flow. Ask the user to sign in and select the intended team in Firmory when authentication is required. Never request tokens, cookies, or passwords in chat.

Use the plugin's firmory_workspace tool to confirm the authorized team. Report a connection only after this call succeeds. If the account or team is wrong, ask the user to switch through the connection settings and check again. On a connection error, keep the current question and offer to retry after reconnection.

On success, show the team name and, when returned, the Ask Firmory workspace link. Offer “Which files did my team update this week?” as a first question. Do not start a private conversation just to verify the connection. Only surface HTTPS web links from the tool's designated handoff fields and the Firmory service's verified web origin.
