---
name: security
description: 7-layer secret protection system with SecretGuard module and git hooks
---

# Security Skill - Bennie Bear

## Overview

7-layer defense system to prevent API key and credential leaks.

**Starter Kit**: `starter-kits/security-infrastructure/`

## Protection Layers

1. **Code-Level**: SecretGuard Python module
2. **Pre-commit Hook**: Git hook blocks commits with secrets
3. **Pre-push Hook**: Secondary scan before push
4. **CI/CD**: GitHub Actions scanning
5. **IDE**: VS Code highlighting
6. **Documentation**: `.env.example` template
7. **Audit**: Manual audit script

## Using SecretGuard

```python
from secret_guard import SecretGuard

# Required key (raises error if missing)
api_key = SecretGuard.get("GOOGLE_API_KEY")

# Optional key with default
api_key = SecretGuard.get("OPTIONAL_KEY", default="", required=False)
```

## Environment Variables

All kits use the same `.env` file at project root:

```bash
# Required for image/video generation
GOOGLE_API_KEY=your_key

# Required for voice generation
ELEVENLABS_API_KEY=your_key

# Optional
ANTHROPIC_API_KEY=your_key
REPLICATE_API_TOKEN=your_key
```

## Git Hooks

Installed at `.git/hooks/`:
- `pre-commit` - Scans staged files for secrets
- `pre-push` - Double-checks before push

## Testing Hooks

```bash
# Try committing a fake secret
echo "API_KEY=sk-test123" > test.txt
git add test.txt
git commit -m "test"  # Should be blocked!
```

## Manual Audit

```bash
cd starter-kits/security-infrastructure
python scripts/check_secrets.py
```

## Full Documentation

See: `starter-kits/security-infrastructure/SKILL.md`
