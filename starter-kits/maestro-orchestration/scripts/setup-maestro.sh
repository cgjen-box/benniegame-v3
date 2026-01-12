#!/bin/bash
# =============================================================================
# Maestro Orchestration - Unix/macOS Setup Script
# =============================================================================
# Usage: ./scripts/setup-maestro.sh

set -e

echo "========================================"
echo "  Maestro Orchestration Setup"
echo "========================================"
echo

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Step 1: Check Python
echo "[1/5] Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "  [OK] $PYTHON_VERSION"
else
    echo "  [ERROR] Python 3 not found. Please install Python 3.11+"
    exit 1
fi

# Step 2: Create .env from template
echo "[2/5] Setting up environment..."
if [ ! -f "$ROOT_DIR/.env" ]; then
    if [ -f "$ROOT_DIR/config/.env.example" ]; then
        cp "$ROOT_DIR/config/.env.example" "$ROOT_DIR/.env"
        echo "  [OK] Created .env from template"
        echo "  [!] Edit .env with your API keys"
    else
        echo "  [WARN] No .env.example found"
    fi
else
    echo "  [OK] .env already exists"
fi

# Step 3: Install Python dependencies
echo "[3/5] Installing dependencies..."
if [ -f "$ROOT_DIR/requirements.txt" ]; then
    pip3 install -r "$ROOT_DIR/requirements.txt" --quiet
    echo "  [OK] Dependencies installed"
else
    echo "  [WARN] requirements.txt not found"
fi

# Step 4: Check SSH key
echo "[4/5] Checking SSH key..."
SSH_KEY="$HOME/.ssh/macincloud_key"
if [ -f "$SSH_KEY" ]; then
    echo "  [OK] SSH key found at $SSH_KEY"
else
    echo "  [WARN] SSH key not found at $SSH_KEY"
    echo "  Generate with: ssh-keygen -t ed25519 -f $SSH_KEY"
fi

# Step 5: Create Claude settings directory
echo "[5/5] Setting up Claude Code..."
CLAUDE_DIR="$HOME/.claude"
mkdir -p "$CLAUDE_DIR"

if [ -f "$ROOT_DIR/config/settings.local.json.template" ]; then
    if [ ! -f "$CLAUDE_DIR/settings.local.json" ]; then
        echo "  [INFO] Copy and customize settings.local.json.template to:"
        echo "         $CLAUDE_DIR/settings.local.json"
    else
        echo "  [OK] Claude settings already configured"
    fi
fi

echo
echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo
echo "Next steps:"
echo "  1. Edit .env with your API keys"
echo "  2. Configure settings.local.json with your SSH host"
echo "  3. Test: python3 scripts/test-mcp-connection.py"
echo
