# Security Infrastructure - Starter Kit

> **System**: 7-Layer SecretGuard Protection
> **Purpose**: Prevent secret leaks across all projects
> **Version**: Extracted from Bennie v1 (2025-12-30)

---

## Overview

This starter kit provides comprehensive defense-in-depth secret protection:

```
┌─────────────────────────────────────────────────────────────────┐
│                    7-LAYER SECRET PROTECTION                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Layer 1: CODE-LEVEL      → SecretGuard Python module           │
│  Layer 2: PRE-COMMIT      → Git hook blocks secret commits      │
│  Layer 3: PRE-PUSH        → Secondary check before push         │
│  Layer 4: CI/CD           → GitHub Actions secret scanning      │
│  Layer 5: IDE             → VS Code secret highlighting         │
│  Layer 6: DOCUMENTATION   → Usage guidelines                    │
│  Layer 7: AUDIT           → Periodic codebase scanning          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

```bash
# 1. Run setup script
./setup-security.sh      # Unix/Mac
.\setup-security.ps1     # Windows

# 2. Copy environment template
cp config/.env.example .env

# 3. Run audit
python secret_guard.py
```

---

## Layer 1: SecretGuard Module

### Usage

```python
from secret_guard import SecretGuard

# Get required secret (raises error if not found)
api_key = SecretGuard.get("GOOGLE_API_KEY")

# Get optional secret with default
api_key = SecretGuard.get("OPTIONAL_KEY", default="", required=False)

# Validate all required secrets at startup
SecretGuard.validate_required([
    "GOOGLE_API_KEY",
    "ELEVENLABS_API_KEY"
])
```

### Features

- Retrieves secrets only from environment variables
- Validates secrets aren't placeholders
- Caches values for performance
- Clear error messages
- Pattern detection for hardcoded secrets

### Error Messages

```
==========================================================
SECRET NOT FOUND: GOOGLE_API_KEY
==========================================================

The environment variable 'GOOGLE_API_KEY' is not set.

To fix this:
  1. Add GOOGLE_API_KEY=your_value to your .env file
  2. Or set it in your environment:
     export GOOGLE_API_KEY=your_value  (Unix)
     set GOOGLE_API_KEY=your_value    (Windows)

See .env.example for required variables.
==========================================================
```

---

## Layer 2: Pre-Commit Hook

### Installation

```bash
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Detected Patterns (40+)

**API Keys:**
- ElevenLabs (`sk_*`)
- Google/Gemini (`AIza*`)
- OpenAI (`sk-*`, `sk-proj-*`)
- Anthropic (`sk-ant-*`)
- AWS (`AKIA*`)
- Stripe (`sk_live_*`, `pk_live_*`)
- SendGrid (`SG.*`)

**Tokens:**
- GitHub (`ghp_*`, `gho_*`, `github_pat_*`)
- GitLab (`glpat-*`)
- Slack (`xox[baprs]-*`)
- Discord tokens
- JWT (`eyJ*`)

**Database:**
- MongoDB connection strings
- PostgreSQL connection strings
- MySQL connection strings

**Keys:**
- RSA/OpenSSH private keys
- Generic private keys

---

## Layer 3: Pre-Push Hook

Secondary scan before pushing to remote.

### Installation

```bash
cp hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

---

## Layer 4: CI/CD - GitHub Actions

### Installation

```bash
mkdir -p .github/workflows
cp github/secret-scan.yml .github/workflows/
```

### Workflow

```yaml
name: Secret Scan
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run gitleaks
        uses: gitleaks/gitleaks-action@v2
```

---

## Layer 5: IDE Integration

### VS Code Settings

Add to `.vscode/settings.json`:

```json
{
  "editor.tokenColorCustomizations": {
    "textMateRules": [
      {
        "scope": "string",
        "settings": {
          "foreground": "#FF0000"
        }
      }
    ]
  }
}
```

---

## Layer 6: Documentation

### .env.example Template

Always provide `.env.example` with placeholder values:

```bash
# API Keys
GOOGLE_API_KEY=your_google_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here

# Optional
ANTHROPIC_API_KEY=
```

### README Guidelines

Document required secrets without exposing values:

```markdown
## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | Yes | Gemini API access |
| `ANTHROPIC_API_KEY` | No | Claude auto-selection |
```

---

## Layer 7: Audit Script

### Usage

```bash
# Scan all tracked files
python scripts/check_secrets.py

# Scan staged files only
python scripts/check_secrets.py --staged-only

# Scan specific file
python scripts/check_secrets.py --file path/to/file.py
```

### Output

```
==========================================================
  SecretGuard Security Audit
==========================================================

No hardcoded secrets detected.

==========================================================
```

Or with findings:

```
Found 2 potential issues:
  - CRITICAL: 1
  - HIGH: 1

[CRITICAL] !!!
  File: src/api.py:15
  Type: Google/Gemini API Key
  Content: api_key = "AIza..."

AUDIT FAILED: Potential secrets detected
```

---

## Secret Patterns

### Full Pattern List

```python
SECRET_PATTERNS = [
    # API Keys - Major Providers
    ("ElevenLabs API Key", r"sk_[a-zA-Z0-9]{20,}", "CRITICAL"),
    ("Google/Gemini API Key", r"AIza[0-9A-Za-z_-]{35}", "CRITICAL"),
    ("OpenAI API Key", r"sk-[a-zA-Z0-9]{20,}", "CRITICAL"),
    ("Anthropic API Key", r"sk-ant-[a-zA-Z0-9_-]{20,}", "CRITICAL"),
    ("AWS Access Key ID", r"AKIA[0-9A-Z]{16}", "CRITICAL"),

    # Version Control
    ("GitHub Token", r"ghp_[0-9a-zA-Z]{36}", "CRITICAL"),
    ("GitLab Token", r"glpat-[0-9a-zA-Z_-]{20}", "CRITICAL"),

    # Communication
    ("Slack Token", r"xox[baprs]-[0-9a-zA-Z-]{10,}", "CRITICAL"),
    ("Discord Token", r"[MN][A-Za-z0-9]{23,}\.[A-Za-z0-9-_]{6}\.[A-Za-z0-9-_]{27}", "CRITICAL"),

    # Payment
    ("Stripe Secret Key", r"sk_live_[0-9a-zA-Z]{24,}", "CRITICAL"),

    # Email
    ("SendGrid API Key", r"SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}", "CRITICAL"),

    # Database
    ("MongoDB URI", r"mongodb(\+srv)?://[^:]+:[^@]+@", "CRITICAL"),
    ("PostgreSQL URI", r"postgres(ql)?://[^:]+:[^@]+@", "CRITICAL"),

    # Private Keys
    ("Private Key", r"-----BEGIN.*PRIVATE KEY-----", "CRITICAL"),

    # JWT
    ("JWT Token", r"eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}", "HIGH"),
]
```

---

## File Structure

```
security-infrastructure/
├── SKILL.md                    # This documentation
├── README.md                   # Quick start
├── secret_guard.py             # Core Python module
│
├── setup-security.sh           # Unix setup script
├── setup-security.ps1          # Windows setup script
│
├── scripts/
│   └── check_secrets.py        # Manual scan tool
│
├── hooks/
│   ├── pre-commit              # Git pre-commit hook
│   └── pre-push                # Git pre-push hook
│
├── config/
│   ├── .gitleaks.toml          # Gitleaks patterns
│   ├── .gitignore.template     # Gitignore with secrets
│   └── .env.example            # Environment template
│
└── github/
    └── secret-scan.yml         # GitHub Actions workflow
```

---

## If You Accidentally Commit a Secret

1. **Immediately rotate the key** at the provider's dashboard
2. Remove from code and use SecretGuard
3. Consider using BFG Repo-Cleaner:

```bash
# Install BFG: https://rtyley.github.io/bfg-repo-cleaner/
bfg --replace-text secrets.txt repo.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

---

## Best Practices

1. **Never hardcode secrets** - Always use environment variables
2. **Use SecretGuard.get()** - Never use `os.environ.get()` directly
3. **Provide .env.example** - Document required variables
4. **Run audit regularly** - Before each commit/push
5. **Rotate exposed keys immediately** - Don't wait
6. **Review CI/CD logs** - Ensure no secrets in build output

---

## Environment Variables

```bash
# This kit doesn't require API keys
# It protects other kits that do
```

---

## Related Documentation

- `secret_guard.py` - Module implementation
- `config/.gitleaks.toml` - Pattern configuration
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
