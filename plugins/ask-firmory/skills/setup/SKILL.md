---
name: setup
description: Connect Firmory and confirm which team the current OAuth session can access.
---

# Connect Firmory

Select this plugin’s `firmory_cloud` server. Use the client’s sign-in action and let the user choose their team on the Firmory consent screen. Keep passwords, verification codes, tokens and OAuth callbacks in that flow.

Call `workspace` with `{}` on the authorized connection. Check `isError` before reading `structuredContent.team.name`. Only report that team as connected after a successful response. The call also returns `space.rootNodeId` and `space.teamLibraryNodeId` for browsing. Offer a first question in the user’s language. For example: “Which projects can I access in my Firmory workspace?”, “我可以访问哪些团队项目？” or “我可以存取哪些團隊專案？”

If `workspace` is unavailable, report that the workspace could not be verified. On a declined authorization, stop. On an expired authorization, reconnect through the host. To switch teams, authorize the intended team, discard previous IDs and cursors, and call `workspace` again.
