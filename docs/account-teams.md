# Team-scoped authorization

Each MCP connection is authorized for one team. OAuth requests `user:org:read`; the server verifies the token and its organization, then checks current membership and permissions on every call. Changing teams requires a new authorization for the intended team. Browser team changes do not alter an existing connection.

Within the authorized team, resolve a project by name using `search` or `browse_folder`, then use its returned ID. Project selection does not require authentication or a server-side selection record. Query again to see newly created projects and current files.

The account-wide team-switching implementation introduced in 1.1.0 is withdrawn. Applied migration `0033_mcp_account_connections` and its schema history are retained; runtime code no longer reads or writes that table. Do not delete applied migrations or production records.

Deploy the restored team-scoped API and MCP workers and web consent page, then distribute the matching plugin. Configure the published OpenAI App to request `user:org:read`. Existing valid team-scoped connections remain usable; account-only connections must authorize a team. Source changes and a built ZIP do not change an already published App's OAuth settings.
