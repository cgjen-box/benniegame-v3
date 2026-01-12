#!/usr/bin/env python3
"""
Maestro MCP Connection Test
============================
Verifies that MCP servers and dependencies are properly configured.

Usage:
    python scripts/test-mcp-connection.py
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple


def check_python_version() -> Tuple[bool, str]:
    """Check Python version is 3.11+."""
    version = sys.version_info
    if version >= (3, 11):
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    return False, f"Python {version.major}.{version.minor} (need 3.11+)"


def check_dependencies() -> Tuple[bool, List[str]]:
    """Check required Python packages are installed."""
    required = ["mcp", "PIL", "dotenv", "requests"]
    missing = []

    for package in required:
        try:
            if package == "PIL":
                __import__("PIL")
            elif package == "dotenv":
                __import__("dotenv")
            else:
                __import__(package)
        except ImportError:
            missing.append(package)

    return len(missing) == 0, missing


def check_env_file() -> Tuple[bool, str]:
    """Check .env file exists."""
    script_dir = Path(__file__).parent.parent
    env_file = script_dir / ".env"

    if env_file.exists():
        return True, str(env_file)
    return False, "No .env file found"


def check_api_keys() -> Dict[str, bool]:
    """Check required API keys are set."""
    from dotenv import load_dotenv

    script_dir = Path(__file__).parent.parent
    load_dotenv(script_dir / ".env")

    keys = {
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "SSH_KEY_PATH": os.getenv("SSH_KEY_PATH"),
        "MACINCLOUD_HOST": os.getenv("MACINCLOUD_HOST"),
    }

    return {k: bool(v and v != f"your_{k.lower()}") for k, v in keys.items()}


def check_ssh_key() -> Tuple[bool, str]:
    """Check SSH key exists."""
    from dotenv import load_dotenv

    script_dir = Path(__file__).parent.parent
    load_dotenv(script_dir / ".env")

    ssh_path = os.getenv("SSH_KEY_PATH", "~/.ssh/macincloud_key")
    ssh_path = Path(ssh_path).expanduser()

    if ssh_path.exists():
        return True, str(ssh_path)
    return False, f"SSH key not found at {ssh_path}"


def check_capabilities() -> Tuple[bool, str]:
    """Check capabilities.json is valid."""
    script_dir = Path(__file__).parent.parent
    cap_file = script_dir / "config" / "capabilities.json"

    if not cap_file.exists():
        return False, "capabilities.json not found"

    try:
        with open(cap_file) as f:
            data = json.load(f)
        return True, f"v{data.get('version', '?')} - {len(data.get('mcp_servers', {}))} servers"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"


def main():
    print()
    print("=" * 50)
    print("  Maestro MCP Connection Test")
    print("=" * 50)
    print()

    tests = [
        ("Python Version", check_python_version),
        ("Dependencies", lambda: (check_dependencies()[0],
                                  "OK" if check_dependencies()[0] else f"Missing: {check_dependencies()[1]}")),
        ("Environment File", check_env_file),
        ("SSH Key", check_ssh_key),
        ("Capabilities", check_capabilities),
    ]

    all_passed = True

    for name, check in tests:
        try:
            passed, info = check()
            status = "[OK]" if passed else "[FAIL]"
            color = "\033[92m" if passed else "\033[91m"
            reset = "\033[0m"
            print(f"{color}{status:8}{reset} {name}: {info}")
            if not passed:
                all_passed = False
        except Exception as e:
            print(f"\033[91m[ERROR]\033[0m {name}: {e}")
            all_passed = False

    # Check API keys separately
    print()
    print("API Keys:")
    try:
        keys = check_api_keys()
        for key, configured in keys.items():
            status = "[OK]" if configured else "[MISSING]"
            color = "\033[92m" if configured else "\033[93m"
            reset = "\033[0m"
            print(f"  {color}{status:10}{reset} {key}")
    except Exception as e:
        print(f"  \033[91m[ERROR]\033[0m Could not check keys: {e}")

    print()
    print("=" * 50)
    if all_passed:
        print("\033[92m  All checks passed!\033[0m")
    else:
        print("\033[93m  Some checks failed. See above for details.\033[0m")
    print("=" * 50)
    print()

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
