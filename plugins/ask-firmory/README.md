# Firmory

Connect Codex or Claude Code to your team’s Firmory preview workspace. Use Firmory setup, sign in through the client’s browser authorization flow, and check the connected team before asking about a project, file version, or source relationship. Claude Code users can run `/ask-firmory:setup` in a new session.

The plugin connects directly to `https://preview.firmory.ai/mcp` over Streamable HTTP. It does not require a local Firmory CLI. The client sends tool arguments, such as a search term or selected file version, to Firmory and receives results available to the signed-in account. The service supplies the tools and enforces access. The lookup skill does not change files to answer questions.

A chat in the client does not by itself create a web conversation. Continue in Ask Firmory only when the service returns a link for the same conversation.

[Product](https://firmory.ai/) · [Support](https://firmory.ai/#faq) · [Privacy](https://firmory.ai/privacy) · [Terms](https://firmory.ai/terms)
