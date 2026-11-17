---
name: sync
description: Remind the user to sync locally created or edited deliverables to Firmory, and save the selected changes only when the user asks to sync.
---

# Sync changes to Firmory

After successfully creating or changing local deliverables during a Firmory-connected task, include one short reminder at task completion in the user's language. Group the changed filenames and offer "Sync to Firmory" or "Later" using the host's choice control if available, otherwise a short question. Do not fabricate clickable buttons. Do not interrupt every edit or repeat the same pending reminder on unrelated turns. A subsequent edit to a deliverable can prompt a new reminder. Also apply this rule when you know a shell command changed deliverables; hooks do not detect arbitrary shell or external-editor changes.

Skip reads, failed/no-op edits, temporary files, build outputs, dependency files, and content already accepted by Firmory. Do not inspect unrelated folders to look for changes. If the user chooses Later, acknowledge briefly and continue. Do not schedule notifications or upload in the background.

When the user requests Sync:

1. Call `workspace` and confirm the currently authorized team. Reuse the explicit project/destination from the task; otherwise resolve the named project with current `search` or `browse_folder` results and ask for the destination if ambiguous. Do not switch teams silently. Follow setup if a different team requires authorization.
2. Show the selected filenames and destination when they have not already been agreed. Do not include unrelated files or credentials. Local deletions are not remote-delete instructions.
3. Use existing Firmory tools. For supported text use `write_text`; for other files follow `prepare_upload` and the returned upload instructions. Use the actual advertised schema. If the client cannot transfer bytes, say so and provide the existing Firmory upload entry; do not claim a sync happened.
4. Update an existing document only when the task or user identifies the corresponding Firmory file. Read its current version and use the version precondition. If it changed since the local source was read, explain the conflict and ask before overwriting. For new files, check name collisions rather than silently replacing another file. Declare the exact source versions actually used.
5. Report Saved only after an accepted change. Report Pending review for a submitted change awaiting approval; do not call it synced. On failure retain the pending filenames and explain the error. On uncertain outcomes, inspect the existing change instead of issuing a duplicate write. Do not retry automatically after declined authorization.

No filesystem watcher, file inventory, background sync, or extra server-side project selection is required. Keep pending work in the current conversation and recheck live state before any write.
