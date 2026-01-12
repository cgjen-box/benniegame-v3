# Security Infrastructure - Quick Start

7-layer secret protection system to prevent API key and credential leaks.

## Setup (5 minutes)

```bash
# Unix/Mac
./setup-security.sh

# Windows PowerShell
.\setup-security.ps1
```

Or manually:

```bash
# 1. Copy git hooks
cp hooks/pre-commit .git/hooks/
cp hooks/pre-push .git/hooks/
chmod +x .git/hooks/*

# 2. Copy environment template
cp config/.env.example .env

# 3. Run audit
python secret_guard.py
```

## Usage in Code

```python
from secret_guard import SecretGuard

# Get required secret
api_key = SecretGuard.get("GOOGLE_API_KEY")

# Get optional secret
api_key = SecretGuard.get("OPTIONAL_KEY", default="", required=False)
```

## 7 Protection Layers

| Layer | File | Purpose |
|-------|------|---------|
| 1 | `secret_guard.py` | Code-level validation |
| 2 | `hooks/pre-commit` | Block commits with secrets |
| 3 | `hooks/pre-push` | Secondary scan before push |
| 4 | `github/secret-scan.yml` | CI/CD scanning |
| 5 | IDE config | VS Code highlighting |
| 6 | `.env.example` | Documentation |
| 7 | `scripts/check_secrets.py` | Manual audit |

## See Also

- `SKILL.md` - Complete documentation with all patterns
- `config/.gitleaks.toml` - Pattern definitions
