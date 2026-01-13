#!/bin/bash
# Security Setup Script for Unix/macOS
# Usage: ./setup-security.sh

echo "=========================================="
echo "  SecretGuard Security Setup"
echo "=========================================="
echo

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "ERROR: Not in a git repository."
    echo "Please run this script from your project root."
    exit 1
fi

# Create hooks directory if needed
mkdir -p .git/hooks

# Install pre-commit hook
echo "Installing pre-commit hook..."
if [ -f "hooks/pre-commit" ]; then
    cp hooks/pre-commit .git/hooks/pre-commit
    chmod +x .git/hooks/pre-commit
    echo "  ✓ Pre-commit hook installed"
else
    echo "  ✗ hooks/pre-commit not found"
fi

# Install pre-push hook
echo "Installing pre-push hook..."
if [ -f "hooks/pre-push" ]; then
    cp hooks/pre-push .git/hooks/pre-push
    chmod +x .git/hooks/pre-push
    echo "  ✓ Pre-push hook installed"
else
    echo "  ✗ hooks/pre-push not found"
fi

# Check for gitleaks
echo
echo "Checking for gitleaks..."
if command -v gitleaks &> /dev/null; then
    echo "  ✓ gitleaks is installed"
else
    echo "  ✗ gitleaks not found"
    echo "    Install with: brew install gitleaks (macOS)"
    echo "    Or: https://github.com/gitleaks/gitleaks"
fi

# Create .env from example if needed
echo
echo "Checking environment file..."
if [ ! -f ".env" ] && [ -f "config/.env.example" ]; then
    cp config/.env.example .env
    echo "  ✓ Created .env from template"
    echo "  ! Remember to fill in your actual values"
elif [ -f ".env" ]; then
    echo "  ✓ .env already exists"
else
    echo "  ✗ No .env.example template found"
fi

# Run initial scan
echo
echo "Running initial security scan..."
if [ -f "scripts/check_secrets.py" ]; then
    python scripts/check_secrets.py
else
    echo "  ✗ check_secrets.py not found"
fi

echo
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo
echo "Next steps:"
echo "  1. Edit .env with your actual API keys"
echo "  2. Never commit .env to version control"
echo "  3. Use SecretGuard.get() in your code"
echo
