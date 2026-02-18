import re
from typing import List, Dict, Any

class SentinelMasking:
    """Sentinel-Masking (handled by Mar). Redacting or masking sensitive info."""

    def __init__(self):
        self.pii_patterns = [
            # Email addresses
            re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            # API Keys/Secrets (simple example)
            re.compile(r'(?:api_key|secret|password|key)\s*[:=]\s*["\']([a-zA-Z0-9\-_]{20,})["\']', re.IGNORECASE),
            # Phone numbers (US/standard)
            re.compile(r'\b(?:\+?1[-. ]?)?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})\b')
        ]

    def redact_text(self, text: str) -> str:
        """Masks PII and secrets in a given string."""
        for pattern in self.pii_patterns:
            text = pattern.sub('[REDACTED]', text)
        return text

    def redact_object(self, obj: Any) -> Any:
        """Recursively redacts PII and secrets in a JSON-like object."""
        if isinstance(obj, str):
            return self.redact_text(obj)
        elif isinstance(obj, list):
            return [self.redact_object(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: self.redact_object(v) for k, v in obj.items()}
        return obj

if __name__ == "__main__":
    masker = SentinelMasking()
    test_data = {
        "user_email": "test@example.com",
        "api_key": "sk-abc1234567890abcdef1234567890",
        "message": "Call me at 555-0199 for more info.",
        "nested": {
            "more_secrets": "password: 'top_secret_1234567890'"
        }
    }
    
    redacted = masker.redact_object(test_data)
    print("Original data:", test_data)
    print("Redacted data:", redacted)
