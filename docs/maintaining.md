# Maintaining and releasing Firmory

## Package contract

The store name is Firmory, the stable plugin ID is `ask-firmory`, and the marketplace ID is `firmory-plugins`. Both catalogs reference `plugins/ask-firmory`. Keep the portable manifest and Claude manifest version, identity, description, and repository metadata aligned.

The portable `mcp.json` and Claude `.mcp.json` describe the same `firmory_cloud` HTTPS service using their respective transport formats. Shared skills and brand assets live inside the plugin folder. The current package has no lifecycle hooks, local executable, or install-time dependency installation.

The root README is for repository visitors. The plugin README is part of the installed package and must remain useful on its own.

## Validate a change

From the repository root, with Claude Code installed:

```sh
claude plugin validate --strict .
claude plugin validate --strict ./plugins/ask-firmory
```

Inspect the JSON files for matching identity and versions, local catalog paths, existing asset paths, and the intended HTTPS endpoint. Confirm the square directory icon is present and the two skills have valid frontmatter.

Then test installation from a disposable client profile: register the local repository as a marketplace, install `ask-firmory@firmory-plugins`, and inspect the installed components. Confirm both clients load the two skills and the `firmory_cloud` configuration. Exercise update and removal when changing package versions or catalog behavior.

Record the client versions and exact commands in the pull request. There is currently no automated CI workflow in this repository; do not treat a missing check as a pass. The Claude CLI checks package structure, not all directory requirements or cloud behavior.

## Release requirements

Before describing the integration as usable:

- From each installed client, verify browser authorization, authenticated MCP initialization, tool discovery, and a successful workspace query against `https://preview.firmory.ai/mcp`. A 401 challenge or metadata response alone is not an end-to-end pass.
- Verify workspace discovery, team switching, expired authorization, and access revocation.
- Verify file/version answers against known data and preserve the question across connection recovery.
- Verify that retries do not create duplicate conversations and that web handoff continues the correct private conversation.
- Verify that another user or team cannot access that conversation through its URL.
- Confirm data-handling and listing statements match deployed behavior.

Before directory submission:

- Select the distribution license and include the required license metadata or file inside the plugin package. Review brand asset rights separately.
- Prepare a populated review account and reproducible cases without exposing customer data.
- Validate the package in each developer portal; resolve blocking findings.
- Complete publisher identity requirements and submit separately to OpenAI and Anthropic.

## Versions and artifacts

For installed-package changes, update both manifests to the same new version and add a changelog entry. Root documentation-only edits do not require a plugin version bump.

After validation, tag the reviewed commit and publish release notes that distinguish working functionality from pending features. Build submission artifacts from that exact commit and record their checksums. Review the extracted archive, including hidden manifests, to ensure that every runtime path resolves and no credentials, system files, or development caches are included.

The marketplace package and the OpenAI portal upload have different MCP metadata requirements in the current tested clients. Preserve the portable runtime configuration used here; the tested Codex loader rejected portal-specific `extensions` on remote server entries. Verify any portal-only OAuth metadata against the current submission specification and keep it out of the marketplace runtime copy unless compatibility has been retested.

The upload builder is not yet distributed in this repository. Moving it here with package consistency checks and CI is a remaining maintenance improvement; a GitHub release must not imply reproducible portal artifacts until that work is complete.

## References

- [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins)
- [OpenAI submission](https://developers.openai.com/plugins/deploy/submission)
- [Claude marketplace creation](https://code.claude.com/docs/en/plugin-marketplaces)
- [Claude directory pre-submission checks](https://claude.com/docs/plugins/pre-submission-checklist)
