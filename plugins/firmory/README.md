# Firmory

Search, capture, download, and share reusable AI Skills.

Use Firmory in Codex or Claude Code to search Skills across your workspace and the public Firmory catalog, view a Skill's steps and package files, download complete Skills locally, turn how you work into a reusable Skill with live save receipts and undo, and share Skills safely with an interactive confirmation card.

The plugin connects to its configured `firmory_cloud` service over HTTPS. Ask your question directly: if sign-in is needed, authorize your account in the browser and continue the task. Use `list_teams` and `switch_team` to change workspaces without signing in again.

[Product](https://firmory.ai/) · [Support](https://firmory.ai/#faq) · [Privacy](https://firmory.ai/privacy) · [Terms](https://firmory.ai/terms)

## Start a conversation

- Search Firmory for a skill I can use, view its contents, or download it
- Turn how I do this task into a reusable Firmory skill
- Show me the skills, projects, and files available in my workspace

[Illustrated installation guide](https://firmory.ai/download).

## Key workflows

- **Find, view, and download Skills:** Mention `@Firmory` and describe the Skill you want. Firmory searches both your workspace and the public Discover catalog (`search_skills`), displays interactive Skill cards to view instructions and package files (`public_read`, `library_get`), and downloads complete Skill directories (`download_skill`).
- **Capture as you work:** Walk Firmory through your method or ask it to capture a completed task. Steps, supporting files, lessons learned, and context are saved with inline receipts (`undo_save` to undo, `set_saving` to pause).
- **Share with confirmation:** Say “share it” to open a confirmation card (`prepare_skill_share`) where you review what becomes public, switch memory items on or off, redact personal or company names, and get a canonical `@handle/slug` link plus ready-to-post copy (`skill_share_status`).

See [Firmory Skills, Sharing, and Production Library](skills/firmory/references/production-library.md).

## License

The plugin code and documentation are licensed under the [MIT License](LICENSE). This license does not grant trademark rights in the Firmory name or logos, or access to Firmory’s hosted services.
