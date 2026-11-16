# Account authorization and MCP teams

Version 1.1.0 requires changes in the existing Firmory MCP/API backend and web consent page. The plugin repository contains client configuration and skills; it does not host the remote tools. Keep the existing MCP endpoint and plugin identity.

## OAuth contract

New connections request `openid` without `user:org:read`. The MCP resource advertises `openid` in protected-resource metadata and scope challenges; the private OpenAI review package declares the same base scope. Public installers continue to use standard discovery. Clerk OAuth/CIMD configuration must allow the account scope, resource audience, and existing redirect URIs. The consent page explains that the account may access and switch between its permitted teams, with current read/write permissions.

Validate each opaque OAuth token's revocation, expiry, audience, scope and subject. Tokens carrying `user:org:read` remain bound to their original organization, even when they also carry `openid`. They must return `REAUTHORIZATION_REQUIRED` for account team discovery/switching until the user reconnects once with the new scope.

## Tools

| Tool | Arguments | Result |
| --- | --- | --- |
| `list_teams` | Optional `limit` (1–100, default 20), `offset` (default 0) | `teams: [{id, name, role, current}]`, `nextOffset` or null |
| `get_current_team` | `{}` | Current `actor`, `team`, `space`; `team` and `space` are null before selection |
| `switch_team` | `teamId`, a returned Firmory team UUID | Verified `actor`, `team`, `space`, also used by subsequent calls |
| `workspace` | `{}` | Current verified workspace; `TEAM_NOT_SELECTED` before selection |

`list_teams` includes only ready teams with live view permission. Pagination advances over membership records, so a filtered page may be empty while `nextOffset` is non-null. No tool creates membership or grants permissions.

Persist the selection under a SHA-256 digest scoped to resource URL, authenticated user and OAuth access token. Store no bearer tokens. Selections expire after 30 days; a refreshed/replaced credential starts without a selection. Different credentials and environments are isolated. Calls sharing one credential also share selection, so switches must be serialized with workspace operations. Browser organization changes do not affect this state. Revalidate live user status, membership, team lifecycle and action permissions on every operation. A rejected switch must retain the previous selection; after an uncertain service or transport failure, verify `get_current_team` before continuing; never fall back to another team after access is revoked. Discard old IDs/cursors after a successful switch and resolve resources in the new team.

## Rollout

1. Apply backend migration `0033_mcp_account_connections` to create the connection selection/provenance table. Do not change or remove existing organization-bound provenance records.
2. Deploy the API Worker with the private account-aware `McpBusiness` methods, then the MCP Worker advertising account authorization and the three team tools.
3. Deploy the web consent changes and account-scope login/setup instructions. Verify the existing Clerk OAuth/CIMD settings accept `openid` without requiring organization consent. Keep MFA and password-reset tasks enforced.
4. Test fresh authorization without an active browser organization. List at least two permitted teams, select one, read its workspace, switch to the other through MCP, and confirm subsequent calls use it. Check browser independence, separate credentials, removed membership, unavailable teams, rejected switches and revoked tokens.
5. Build and distribute the 1.1.0 plugin only after the service supports the new contract. Existing organization-only users reconnect once. This source change and a successful local package build do not establish production deployment or complete live OAuth verification.

Build local installers with `python3 scripts/build_distribution.py --env production --release-version 1.1.0 --public-only`. Run package tests and strict client validation before distribution.

## Local verification

The source change was checked with 140 targeted tests: 105 MCP/auth/business tests, 3 real PostgreSQL selection-store tests (including the complete migration chain), 18 existing PostgreSQL MCP mutation regressions, 11 web authorization/setup tests, and 3 distribution tests. Backend and frontend typechecks, changed frontend file lint, and strict Claude marketplace/plugin validation passed. The PostgreSQL tests used an isolated temporary local server and fixture databases. Live Clerk browser OAuth and production deployment were not run; those remain rollout checks.
