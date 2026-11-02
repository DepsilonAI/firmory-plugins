# Maintaining and releasing Firmory

## Package contract

The store name is Firmory, the stable plugin ID is `firmory`, and the marketplace ID is `firmory-plugins`. Both catalogs reference `plugins/firmory`. Keep the portable manifest and Claude manifest version, identity, description, and repository metadata aligned.

The portable `mcp.json` and Claude `.mcp.json` describe the same `firmory_cloud` HTTPS service using their respective transport formats. Shared skills and brand assets live inside the plugin folder. The current package has no lifecycle hooks, local executable, or install-time dependency installation.

The root README is for repository visitors. The plugin README is part of the installed package and must remain useful on its own.

## Validate a change

From the repository root, with Claude Code installed:

```sh
claude plugin validate --strict .
claude plugin validate --strict ./plugins/firmory
```

Inspect the JSON files for matching identity and versions, local catalog paths, existing asset paths, and the intended HTTPS endpoint. Confirm the square directory icon is present and the two skills have valid frontmatter.

Then test installation from a disposable client profile: register the local repository as a marketplace, install `firmory@firmory-plugins`, and inspect the installed components. Confirm both clients load the two skills and the `firmory_cloud` configuration. Exercise update and removal when changing package versions or catalog behavior.

Record the client versions and exact commands in the pull request. There is currently no automated CI workflow in this repository; do not treat a missing check as a pass. The Claude CLI checks package structure, not all directory requirements or cloud behavior.

## Build and promote

`main` installs the production plugin at `https://firmory.ai/mcp`. Build preview archives with Python 3 from the repository root.

```sh
python3 scripts/build_distribution.py --env preview
```

At submission time, choose a new stable version and run the production build. For example, to package version 1.0.0, run the following command.

```sh
python3 scripts/build_distribution.py --env production --release-version 1.0.0 --review-cases /path/to/verified-review-cases.json --demo-recording-url PUBLIC_VIDEO_URL
```

`dist/` contains two archives identified by version and environment. The OpenAI ZIP carries the portable manifest and OAuth declaration. The marketplace ZIP contains both catalogs, both client manifests, shared skills, and the plugin README. Production builds set every MCP configuration to `https://firmory.ai/mcp`. The builder checks packaged text for preview hosts.

Test the **extracted production marketplace** in clean Codex and Claude Code profiles. Confirm that the challenge advertises production OAuth metadata and that each authorized client can call `workspace({})`. Use the returned root to list visible projects. With review fixtures, check a report’s declared source version and a specification’s downstream graph. Verify the correct team and file versions against the fixture records.

After those checks pass, publish the extracted marketplace tree to a dedicated release branch or tag in this repository and point Anthropic at its `plugins/firmory` folder on that ref. Upload the matching production OpenAI ZIP. Record the source commit, published ref and artifact checksums. Confirm the package license, reviewer account, and publisher identity before submitting.

## References

- [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins)
- [OpenAI submission](https://developers.openai.com/plugins/deploy/submission)
- [Claude marketplace creation](https://code.claude.com/docs/en/plugin-marketplaces)
- [Claude directory pre-submission checks](https://claude.com/docs/plugins/pre-submission-checklist)
