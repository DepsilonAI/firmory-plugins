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
        "Firmory: after actual local deliverable changes, follow the Firmory sync skill at task "
        "completion. Respect the user's latest local-only instruction and scoped sync preference. "
        "Local-only means no upload or immediate sync question; manual mode means no unsolicited "
        "sync prompt. Otherwise use the skill's grouped human-choice flow or explicitly authorized "
        "automatic mode. Do not upload automatically without explicit consent for the verified "
        "scope and linked files. Never treat this hook as consent. Do not interrupt each edit, "
        "fabricate buttons/links, or repeat unchanged reminders. Skip failed/no-op edits, "
        "temporary/build/dependency/preference files, and versions already saved through Firmory."
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
