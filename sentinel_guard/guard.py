import re
import yaml
from typing import List, Dict, Any

class SentinelGuard:
    """The core interception engine for OpenClaw-Sentinel."""

    def __init__(self, policy_path: str = None):
        self.blocked_commands: List[str] = []
        self.blocked_patterns: List[re.Pattern] = []
        self.allowed_tools: List[str] = []
        if policy_path:
            self.load_policy(policy_path)

    def load_policy(self, path: str):
        """Loads security policies from a YAML file."""
        try:
            with open(path, 'r') as f:
                policy = yaml.safe_load(f)
                self.blocked_commands = policy.get('blocked_commands', [])
                self.blocked_patterns = [re.compile(p) for p in policy.get('blocked_regex', [])]
                self.allowed_tools = policy.get('allowed_tools', [])
        except Exception as e:
            print(f"Error loading policy: {e}")

    def filter_command(self, command: str) -> bool:
        """
        Filters shell commands based on blocked keywords and patterns.
        Returns True if the command is allowed, False if blocked.
        """
        for cmd in self.blocked_commands:
            if cmd in command:
                print(f"BLOCKED: Command contains forbidden keyword '{cmd}'")
                return False

        for pattern in self.blocked_patterns:
            if pattern.search(command):
                print(f"BLOCKED: Command matches forbidden pattern '{pattern.pattern}'")
                return False

        return True

    def validate_tool_call(self, tool_name: str, args: Dict[str, Any]) -> bool:
        """Validates if a tool call is authorized."""
        if self.allowed_tools and tool_name not in self.allowed_tools:
            print(f"BLOCKED: Tool '{tool_name}' is not in the allowed list.")
            return False
        return True

# Default example policy for initial testing
DEFAULT_POLICY = {
    'blocked_commands': ['rm -rf /', 'mkfs', 'dd if=/dev/zero'],
    'blocked_regex': [r'rm\s+-rf\s+.*', r'sudo\s+.*'],
    'allowed_tools': ['read', 'write', 'edit', 'exec', 'web_search', 'web_fetch']
}

if __name__ == "__main__":
    # Quick test
    guard = SentinelGuard()
    guard.blocked_commands = DEFAULT_POLICY['blocked_commands']
    guard.blocked_patterns = [re.compile(p) for p in DEFAULT_POLICY['blocked_regex']]
    
    test_commands = [
        "ls -la",
        "rm -rf /some/path",
        "sudo apt update",
        "cat file.txt"
    ]
    
    for cmd in test_commands:
        allowed = guard.filter_command(cmd)
        print(f"Command: {cmd} -> {'ALLOWED' if allowed else 'BLOCKED'}")
