"""Add a non-blocking reminder after local edits; never read or upload files."""
import json
import sys


def reminder(event):
    if not isinstance(event, dict) or event.get("hook_event_name") != "PostToolUse":
        return None
    if event.get("tool_name") not in {"apply_patch", "Edit", "Write", "MultiEdit", "NotebookEdit"}:
        return None
    response = event.get("tool_response")
    if isinstance(response, dict) and (response.get("isError") or response.get("error")
                                     or response.get("success") is False
                                     or response.get("exit_code", 0) not in (0, None)):
        return None
    return {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": (
        "Firmory: if this tool actually changed user deliverable files locally, include one concise "
        "sync reminder in your next task-completion response, in the user's language. Group all "
        "changes in this task; do not interrupt each edit. Name the changed deliverables and offer "
        "Sync to Firmory or Later. Follow the Firmory sync skill if the user chooses Sync. Do not "
        "upload automatically or repeat a reminder for unchanged or already-synced versions. "
        "Skip failed/no-op edits, temporary/build files, and changes already saved through Firmory."
    )}}


if __name__ == "__main__":
    try:
        event = json.loads(sys.stdin.read(2 * 1024 * 1024))
    except (ValueError, UnicodeError):
        print("Firmory sync reminder could not read the hook event.", file=sys.stderr)
        sys.exit(1)
    output = reminder(event)
    if output:
        print(json.dumps(output))
