import json
import time
from typing import Any, Dict

class SentinelAudit:
    """Sentinel-Audit: Records all tool calls and interactions."""

    def __init__(self, log_file: str = "audit.jsonl"):
        self.log_file = log_file

    def log_event(self, event_type: str, data: Dict[str, Any]):
        """Logs a structured event to a JSONL file."""
        log_entry = {
            "timestamp": time.time(),
            "event_type": event_type,
            "data": data
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

if __name__ == "__main__":
    audit = SentinelAudit()
    audit.log_event("tool_call", {"tool": "exec", "command": "ls -la"})
    print(f"Logged event to {audit.log_file}")
