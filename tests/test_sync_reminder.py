import importlib.util
import json
import subprocess
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "plugins/firmory/hooks/sync_reminder.py"
spec = importlib.util.spec_from_file_location("sync_reminder", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SyncReminderTests(unittest.TestCase):
    def test_local_edits_supply_context_without_uploading_or_leaking_content(self):
        for name in ("Write", "Edit", "apply_patch", "MultiEdit", "NotebookEdit"):
            with self.subTest(tool=name):
                event = {"hook_event_name": "PostToolUse", "tool_name": name,
                         "tool_input": {"content": "private-file-sentinel"},
                         "tool_response": {"success": True}}
                result = subprocess.run(["python3", str(SCRIPT)], input=json.dumps(event),
                                        text=True, capture_output=True, check=True)
                output = json.loads(result.stdout)
                self.assertEqual(output["hookSpecificOutput"]["hookEventName"], "PostToolUse")
                self.assertIn("Do not upload automatically", output["hookSpecificOutput"]["additionalContext"])
                self.assertNotIn("private-file-sentinel", result.stdout)
                self.assertNotIn("decision", output)

    def test_reads_remote_writes_and_failed_edits_do_not_trigger(self):
        for name in ("Read", "Bash", "mcp__firmory__write_text", "mcp__firmory__read_file"):
            self.assertIsNone(module.reminder({"hook_event_name": "PostToolUse", "tool_name": name}))
        for response in ({"isError": True}, {"success": False}, {"error": "failed"}, {"exit_code": 1}):
            self.assertIsNone(module.reminder({"hook_event_name": "PostToolUse", "tool_name": "Edit", "tool_response": response}))
        self.assertIsNone(module.reminder({"hook_event_name": "PreToolUse", "tool_name": "Edit"}))

    def test_malformed_input_reports_failure_without_echoing_input(self):
        result = subprocess.run(["python3", str(SCRIPT)], input="private-input-not-json", text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("private-input", result.stdout + result.stderr)
