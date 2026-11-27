# Firmory

Build on shared digital assets

Use Firmory in Codex or Claude Code to find the projects you can access, check which version of a brief informed a report, or follow a specification to documents that cite it. Ask your question directly. If sign-in is needed, authorize your team in the browser and continue the task. A separate setup question is not required. Ask to change teams when you need a different team's authorization; project changes within the authorized team do not require sign-in.

The plugin connects to its configured `firmory_cloud` service over HTTPS. The host sends tool arguments such as search terms, file identifiers, and versions to Firmory. The service returns records available to the signed-in team. The lookup workflow uses read operations. Follow-up questions stay in the current client conversation.

[Product](https://firmory.ai/) · [Support](https://firmory.ai/#faq) · [Privacy](https://firmory.ai/privacy) · [Terms](https://firmory.ai/terms)

## Start a conversation

- Show me the projects and files available in my workspace
- Find the project brief and summarize its goals and key decisions
- Open "Welcome.pdf" and summarize its key points

[Illustrated installation guide](https://firmory.ai/download).

## Skills and production files

In Codex, mention `@Firmory` and ask it to do the work and capture it in Firmory. As you work, the agent saves reusable assets in the project’s production library. At completion, it submits a Skill that links to those assets and returns the Skill link with your deliverable. Ask for a link others can reuse to share the Skill. Give Firmory that link and describe the next task to reuse it. [Skills and the production library](skills/firmory/references/production-library.md)

## License

The plugin code and documentation are licensed under the [MIT License](LICENSE). This license does not grant trademark rights in the Firmory name or logos, or access to Firmory’s hosted services.
