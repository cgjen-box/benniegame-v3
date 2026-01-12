"""
SecretGuard - Secure Secret Management for Bennie Bear Learning Game
Security Layer 1 - Code-Level Protection

This module provides secure access to secrets from environment variables,
with validation to prevent hardcoded secrets and ensure proper usage.

Usage:
    from secret_guard import SecretGuard

    # Get a required secret (raises error if not found)
    api_key = SecretGuard.get("ELEVENLABS_API_KEY")

    # Get an optional secret with default
    api_key = SecretGuard.get("OPTIONAL_KEY", default="")

    # Validate all required secrets at startup
    SecretGuard.validate_required([
        "GOOGLE_API_KEY",
        "ELEVENLABS_API_KEY"
    ])
"""

import os
import re
import sys
import math
from pathlib import Path
from typing import Optional, List, Dict, Set
from dataclasses import dataclass
from functools import lru_cache

# Load .env file if present
try:
    from dotenv import load_dotenv
    # Load from project root
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass  # dotenv not installed, rely on system env vars


class SecretNotFoundError(Exception):
    """Raised when a required secret is not found in environment."""
    pass


class SecretValidationError(Exception):
    """Raised when a secret appears to be hardcoded or invalid."""
    pass


class HardcodedSecretError(Exception):
    """Raised when hardcoded secrets are detected in code."""
    pass


@dataclass
class SecretPattern:
    """Definition of a secret pattern for detection."""
    name: str
    pattern: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW


# Comprehensive list of secret patterns
SECRET_PATTERNS: List[SecretPattern] = [
    # API Keys - Major Providers
    SecretPattern("ElevenLabs API Key", r"sk_[a-zA-Z0-9]{20,}", "CRITICAL"),
    SecretPattern("Google/Gemini API Key", r"AIza[0-9A-Za-z_-]{35}", "CRITICAL"),
    SecretPattern("OpenAI API Key", r"sk-[a-zA-Z0-9]{20,}", "CRITICAL"),
    SecretPattern("Anthropic API Key", r"sk-ant-[a-zA-Z0-9_-]{20,}", "CRITICAL"),
    SecretPattern("AWS Access Key ID", r"AKIA[0-9A-Z]{16}", "CRITICAL"),

    # Version Control
    SecretPattern("GitHub Token", r"ghp_[0-9a-zA-Z]{36}", "CRITICAL"),
    SecretPattern("GitLab Token", r"glpat-[0-9a-zA-Z_-]{20}", "CRITICAL"),

    # Communication
    SecretPattern("Slack Token", r"xox[baprs]-[0-9a-zA-Z-]{10,}", "CRITICAL"),
    SecretPattern("Discord Token", r"[MN][A-Za-z0-9]{23,}\.[A-Za-z0-9-_]{6}\.[A-Za-z0-9-_]{27}", "CRITICAL"),

    # Payment
    SecretPattern("Stripe Secret Key", r"sk_live_[0-9a-zA-Z]{24,}", "CRITICAL"),

    # Email
    SecretPattern("SendGrid API Key", r"SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}", "CRITICAL"),

    # Database
    SecretPattern("MongoDB URI", r"mongodb(\+srv)?://[^:]+:[^@]+@", "CRITICAL"),
    SecretPattern("PostgreSQL URI", r"postgres(ql)?://[^:]+:[^@]+@", "CRITICAL"),

    # Private Keys
    SecretPattern("Private Key", r"-----BEGIN.*PRIVATE KEY-----", "CRITICAL"),

    # JWT
    SecretPattern("JWT Token", r"eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}", "HIGH"),
]


class SecretGuard:
    """
    Secure secret management with validation.

    Features:
    - Retrieves secrets only from environment variables
    - Validates secrets don't appear hardcoded
    - Caches values for performance
    - Provides clear error messages
    """

    _cache: Dict[str, str] = {}
    _accessed_keys: Set[str] = set()

    @classmethod
    def get(cls, key: str, *, default: Optional[str] = None, required: bool = True) -> Optional[str]:
        """
        Get a secret from environment variables.

        Args:
            key: Environment variable name
            default: Default value if not found (only used if required=False)
            required: If True, raises error when not found

        Returns:
            The secret value

        Raises:
            SecretNotFoundError: If required secret is not found
            SecretValidationError: If secret appears invalid
        """
        # Check cache first
        if key in cls._cache:
            cls._accessed_keys.add(key)
            return cls._cache[key]

        # Get from environment
        value = os.environ.get(key)

        if value is None:
            if required and default is None:
                raise SecretNotFoundError(
                    f"\n{'='*60}\n"
                    f"SECRET NOT FOUND: {key}\n"
                    f"{'='*60}\n\n"
                    f"The environment variable '{key}' is not set.\n\n"
                    f"To fix this:\n"
                    f"  1. Add {key}=your_value to your .env file\n"
                    f"  2. Or set it in your environment:\n"
                    f"     export {key}=your_value  (Unix)\n"
                    f"     set {key}=your_value    (Windows)\n\n"
                    f"See .env.example for required variables.\n"
                    f"{'='*60}\n"
                )
            return default

        # Validate the value
        cls._validate_secret(key, value)

        # Cache and return
        cls._cache[key] = value
        cls._accessed_keys.add(key)
        return value

    @classmethod
    def _validate_secret(cls, key: str, value: str) -> None:
        """Validate that a secret value is properly formatted."""
        # Check for obviously wrong values
        if value.lower() in ('your_key_here', 'xxx', 'placeholder', 'changeme', 'todo'):
            raise SecretValidationError(
                f"Secret '{key}' appears to be a placeholder value. "
                f"Please set the actual secret in your .env file."
            )

        # Check for very short values (probably wrong)
        if len(value) < 8 and key.endswith(('_KEY', '_SECRET', '_TOKEN', '_PASSWORD')):
            raise SecretValidationError(
                f"Secret '{key}' is suspiciously short ({len(value)} chars). "
                f"Please verify you have the correct value."
            )

    @classmethod
    def validate_required(cls, keys: List[str]) -> None:
        """
        Validate that all required secrets are present.

        Args:
            keys: List of required environment variable names

        Raises:
            SecretNotFoundError: If any required secrets are missing
        """
        missing = []
        for key in keys:
            if os.environ.get(key) is None:
                missing.append(key)

        if missing:
            raise SecretNotFoundError(
                f"\n{'='*60}\n"
                f"MISSING REQUIRED SECRETS\n"
                f"{'='*60}\n\n"
                f"The following environment variables are not set:\n"
                + "\n".join(f"  - {k}" for k in missing) +
                f"\n\nAdd them to your .env file or environment.\n"
                f"See .env.example for reference.\n"
                f"{'='*60}\n"
            )

    @classmethod
    def get_accessed_keys(cls) -> Set[str]:
        """Get the set of secret keys that have been accessed."""
        return cls._accessed_keys.copy()

    @classmethod
    def clear_cache(cls) -> None:
        """Clear the secret cache (useful for testing)."""
        cls._cache.clear()

    @staticmethod
    def calculate_entropy(s: str) -> float:
        """
        Calculate Shannon entropy of a string.
        High entropy suggests randomness (potential secret).
        """
        if not s:
            return 0.0

        # Count character frequencies
        freq = {}
        for c in s:
            freq[c] = freq.get(c, 0) + 1

        # Calculate entropy
        length = len(s)
        entropy = 0.0
        for count in freq.values():
            p = count / length
            entropy -= p * math.log2(p)

        return entropy

    @classmethod
    def scan_file_for_secrets(cls, file_path: Path) -> List[Dict]:
        """
        Scan a file for potential hardcoded secrets.

        Args:
            file_path: Path to the file to scan

        Returns:
            List of findings with pattern name, line number, and severity
        """
        findings = []

        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            return findings

        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            # Skip comments
            stripped = line.strip()
            if stripped.startswith('#') or stripped.startswith('//'):
                continue

            for pattern in SECRET_PATTERNS:
                if re.search(pattern.pattern, line):
                    # Check if it's in a string assignment (likely hardcoded)
                    if re.search(r'["\'][^"\']*' + pattern.pattern + r'[^"\']*["\']', line):
                        findings.append({
                            'file': str(file_path),
                            'line': line_num,
                            'pattern': pattern.name,
                            'severity': pattern.severity,
                            'content': line[:80] + ('...' if len(line) > 80 else '')
                        })

        return findings

    @classmethod
    def scan_directory(cls, directory: Path, extensions: List[str] = None) -> List[Dict]:
        """
        Scan a directory for potential hardcoded secrets.

        Args:
            directory: Directory to scan
            extensions: File extensions to check (default: ['.py', '.swift', '.sh'])

        Returns:
            List of all findings
        """
        if extensions is None:
            extensions = ['.py', '.swift', '.sh', '.yml', '.yaml', '.json', '.md']

        all_findings = []
        exclude_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'DerivedData', 'Pods'}

        for root, dirs, files in os.walk(directory):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = Path(root) / file
                    findings = cls.scan_file_for_secrets(file_path)
                    all_findings.extend(findings)

        return all_findings

    @classmethod
    def audit(cls, directory: Path = None) -> bool:
        """
        Run a full security audit on the codebase.

        Args:
            directory: Directory to audit (default: project root)

        Returns:
            True if no issues found, False otherwise
        """
        if directory is None:
            directory = Path(__file__).parent.parent

        print("=" * 60)
        print("  SecretGuard Security Audit")
        print("=" * 60)
        print()

        findings = cls.scan_directory(directory)

        if not findings:
            print("No hardcoded secrets detected.")
            print()
            print("=" * 60)
            return True

        # Group by severity
        critical = [f for f in findings if f['severity'] == 'CRITICAL']
        high = [f for f in findings if f['severity'] == 'HIGH']
        other = [f for f in findings if f['severity'] not in ('CRITICAL', 'HIGH')]

        print(f"Found {len(findings)} potential issues:")
        print(f"  - CRITICAL: {len(critical)}")
        print(f"  - HIGH: {len(high)}")
        print(f"  - Other: {len(other)}")
        print()

        for finding in findings:
            severity_marker = "!!!" if finding['severity'] == 'CRITICAL' else "!!" if finding['severity'] == 'HIGH' else "!"
            print(f"[{finding['severity']}] {severity_marker}")
            print(f"  File: {finding['file']}:{finding['line']}")
            print(f"  Type: {finding['pattern']}")
            print(f"  Content: {finding['content']}")
            print()

        print("=" * 60)
        print("AUDIT FAILED: Potential secrets detected")
        print()
        print("To fix:")
        print("  1. Remove hardcoded secrets from the files listed above")
        print("  2. Use SecretGuard.get('KEY_NAME') instead")
        print("  3. Add secrets to .env file (which is gitignored)")
        print("=" * 60)

        return False


# Convenience function for common usage
def get_secret(key: str, *, default: Optional[str] = None, required: bool = True) -> Optional[str]:
    """Shorthand for SecretGuard.get()"""
    return SecretGuard.get(key, default=default, required=required)


# Run audit if executed directly
if __name__ == "__main__":
    import sys
    success = SecretGuard.audit()
    sys.exit(0 if success else 1)
