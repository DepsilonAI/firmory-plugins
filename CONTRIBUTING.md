# Contributing

This repository contains the Firmory plugin package and its two marketplace catalogs. Start with the [README](README.md) and [maintainer guide](docs/maintaining.md).

## Report a problem

Search existing issues, then describe the client and plugin versions, reproduction steps, expected behavior, and actual behavior. Cloud connection failures are expected while this package remains a design preview. Report suspected vulnerabilities privately using [SECURITY.md](SECURITY.md).

## Propose a change

Keep changes focused on installation, documentation, compatibility, or the existing Firmory workflows. Explain the problem and how you verified the change. Keep English and Traditional Chinese README status and installation instructions aligned.

Both platform manifests must describe the same version and functionality. Keep everything required at runtime inside `plugins/ask-firmory/`; installed clients may not receive root-level documentation. Do not add real workspace data, credentials, private service URLs, or developer machine paths.

The distribution license is pending. Discuss substantive code or asset contributions with the maintainers before submitting them. Do not add third-party content without establishing its rights and attribution.

For package changes, include the checks actually run and any untested cloud behavior. A successful JSON or CLI validation does not prove OAuth or end-to-end functionality. Use the pull request template and the release checks in the maintainer guide.
