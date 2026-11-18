# Team authorization and sync interactions

## Change team

User asks to change team → read the current workspace → request_team_authorization(currentTeamId) → the host's native reauthorization action → user selects the intended team using the same account and approves consent → verify workspace on the original connection → resume the original task. The MCP tool returns the documented tool-level OAuth challenge, without UI metadata, a settings URL, or a duplicate-account flow. The deprecated optional authorize argument remains accepted and is not another user step. Project changes never use this flow.

The MCP tool does not revoke credentials or change membership, grants, or a selected-team row. It does not return a transport 401 that triggers refresh of the old grant. A retry using a different authorized team returns its workspace without another challenge. Only the host creates the OAuth request bound to the existing connection. Do not invent a callback URL, link identifier, or native host metadata. Direct Claude Code and Codex CLI MCP connections use their own OAuth controls.

Client policy is a prerequisite: in the verified Codex runtime 0.166.0-alpha.5.1, `AskForApproval::Never` returns before creating the native auth elicitation, even when `AuthElicitation` is enabled. The desktop Full access preset selects this policy. If runtime evidence confirms it, have the user choose Default permissions; do not modify security controls automatically or diagnose this from UI absence alone. The upstream Calendar auth test uses OnRequest and preserves the existing link ID. See [the runtime guard](https://github.com/openai/codex/blob/rust-v0.166.0-alpha.5.1/codex-rs/core/src/mcp_tool_call.rs#L822).

Client verification is still required. An auth-required response does not prove that the host displayed its reauthorization action. If no action appears, report that authorization has not started, keep the task pending, and do not loop. Check that the published tool has no stale UI template binding. Only a successful workspace response for the intended team completes acceptance.

## Local edits

The sync skill owns the interaction. Hooks only supply context; they do not upload or authorize anything. Native host choices are preferred, with plain-text fallback. Links navigate to actual files; they never stand in for sync actions.

User: "Add 111 to test.md, edit locally first."

Expected: "test.md updated locally: added 111. Not synced." Include a local file link when supported. No sync question and no upload, even with automatic mode previously enabled. Local-only content stays excluded from later automatic uploads until the user explicitly includes it.

Whenever a relevant new local file change is discovered, including a manual edit found during inspection, show filenames, a short summary, and the resolved destination (team / project / path) in one native choice. Do not duplicate it in the completion text.

| Action | Result |
| --- | --- |
| Sync now | Save this batch to the agreed destination. Resolve unknown destinations before writing. |
| Enable automatic sync | Show the verified team/project/local workspace scope before selection; enable future linked-file sync on explicit selection. Current changes stay local unless explicitly included. |
| Not this time, remind me next time | No upload now. Remind once on the next task that edits or explicitly inspects these pending files, even if unchanged. Do not remind on unrelated questions. No timed notification. |

No answer, dismissal, or a preselected option authorizes nothing. Do not fabricate buttons or action links if the host lacks native choice UI.

### Preferences

Default is Ask after changes. Automatic mode requires explicit consent for the verified user, team, project, and local workspace root; it covers future observed edits to known linked files at task completion. New files, deletion, moves, conflicts, unknown base versions, and local-only content require a separate decision. Enabling automatic mode does not save the pending batch unless explicitly included. Only when I ask stops unsolicited prompts without blocking direct sync requests.

Preferences are conversation-scoped by default. On explicit request, local clients may persist a mode in one user-owned JSON file following the sync skill's validation contract. Store scope IDs, local root, and mode only; no credentials, contents, pending uploads, or file mappings. Missing or invalid persisted state never grants automatic permission. Web clients without a persistent store must state conversation-only scope. Do not claim cross-client or team-wide preferences.

### Saving and recovery

Verify the actual workspace before saving, then the agreed destination and recorded remote base version. Use existing tools and version preconditions. Report Synced only for accepted changes, Pending review for review requests, and per-file outcomes for partial batches. Conflicts, cancellation, and unknown outcomes pause the batch; inspect before retrying and never silently create duplicates. Required host approvals remain in effect. No background upload, filesystem watcher, or synchronization database is introduced.

The shared PostToolUse hook runs on supported local editing tools in trusted local Codex/Claude Code installations. It adds model context without transmitting files. It cannot observe external editor changes, arbitrary shell writes, or local files from a web-only session. Skills cover changes the agent can observe in those contexts.

## Host acceptance checks

These cases require testing an installed candidate in each intended host. Hook/archive tests do not prove model behavior or native choice rendering.

| Scenario | Required outcome |
| --- | --- |
| Local-first edit in ask or auto mode | Local result only; no upload or immediate sync question. |
| Give a local path, user edits externally, then asks to inspect | Compare against the downloaded baseline; in ask mode, summarize the observed change and offer a sync choice in the same response. No background watcher is needed. |
| Read an unchanged local file or repeat inspection of the same pending snapshot | No new reminder unless the user chose to defer it to this next relevant task; inspection does not mark the file synced. |
| Inspect a changed file in explicit manual mode | Describe the change without an unsolicited sync prompt. |
| Inspect a local file with no known baseline | Do not invent changes or assume it is synced; resolve the base before any automatic write. |
| One-time sync approved, then user requests further edits | Approval does not expand to future contents; use a new consent decision unless an explicit auto preference covers them. |
| Three local edits in one task | One grouped decision with filenames and destination. |
| Choice dismissed or unanswered | No upload or preference change. |
| Sync now with known destination | No redundant confirmation beyond required host approvals. |
| Remind next time, then an unrelated question | No reminder on unrelated work. |
| Remind next time, then inspect the pending file | One reminder even if unchanged; include still-pending changes, without uploading. |
| New changes discovered by edit, read, or comparison tools | Same direct three choices; apply explicit local-only/manual instructions or authorized automatic mode. |
| Manual mode, edit again, then request sync | No unsolicited prompt; direct sync still works. |
| Enable automatic mode | Show scope; current batch stays local; future linked-file edits may save. |
| Automatic mode with new file, unknown base, or local-only contents | Ask before writing; no guessed mapping or silent overwrite. |
| Change team/account/project/local root | No inherited automatic permission from another scope. |
| Reopen local conversation with persisted mode | Exact validated scope only; reconstruct mappings/base versions before auto writes. |
| Corrupt preference or failed persistence | No implicit automatic permission or false claim of remembering. |
| Web without persistent preferences | State conversation-only scope. |
| Conflict, cancellation, partial failure, unknown outcome | Preserve local edits; accurate status; no retry loop or duplicate save. |
| Successful automatic save | Brief accepted result/version, no new sync question. |
