# Maestro Orchestration System

> Complete Claude Code orchestration layer for multi-MCP coordination, automated workflows, and intelligent task execution.

## Overview

Maestro is the orchestration framework that coordinates:
- **3 MCP Servers**: iOS Simulator, Image Generation, Chrome DevTools
- **18+ Skills**: Domain-specific Claude Code capabilities
- **Automation Pipelines**: Keyframe→Animation, Build→Test→Fix loops
- **Security Infrastructure**: SecretGuard, API key management

## Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| Python | 3.11+ | MCP servers, automation scripts |
| Claude Code | Latest | Orchestration runtime |
| SSH Key | ED25519 | MacinCloud connectivity |
| Chrome | Latest | DevTools MCP |

### API Keys Required

| Key | Service | Required For |
|-----|---------|--------------|
| `GOOGLE_API_KEY` | Google Gemini | Image/video generation |
| `GEMINI_API_KEY` | Google Gemini | Alternative to above |
| `SSH_KEY_PATH` | SSH | MacinCloud iOS builds |
| `MACINCLOUD_HOST` | MacinCloud | Remote Mac access |

## Quick Start

### Windows Setup

```powershell
cd starter-kits\maestro-orchestration
.\scripts\setup-maestro.ps1
```

### Unix/macOS Setup

```bash
cd starter-kits/maestro-orchestration
./scripts/setup-maestro.sh
```

### Manual Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy environment template
cp config/.env.example .env

# 3. Edit .env with your API keys
notepad .env  # or vim/nano

# 4. Test connectivity
python scripts/test-mcp-connection.py
```

---

## MCP Servers Reference

### 1. iOS Simulator MCP

**Transport**: SSH stdio (remote Mac)
**Purpose**: iPad app build, deploy, test, and UI automation

#### Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `build_and_deploy()` | Git pull + Xcode build + simulator install | `pull_latest: bool = True` |
| `launch_app()` | Start app in simulator | `bundle_id: str` |
| `take_screenshot()` | Capture simulator screen | Returns base64 PNG |
| `tap(x, y)` | Touch at coordinates | `x: int, y: int` |
| `swipe(x1, y1, x2, y2)` | Drag gesture | Start/end coordinates |
| `type_text(text)` | Keyboard input | `text: str` |
| `run_tests()` | Execute XCUITests | `test_plan: str = None` |
| `get_logs()` | App console output | `lines: int = 100` |
| `boot_simulator()` | Start simulator if stopped | `device: str` |
| `shutdown_simulator()` | Stop simulator | - |

#### Configuration

```json
{
  "ios-simulator": {
    "command": "ssh",
    "args": [
      "-i", "${SSH_KEY_PATH}",
      "-o", "StrictHostKeyChecking=no",
      "${MACINCLOUD_USER}@${MACINCLOUD_HOST}",
      "cd ${MACINCLOUD_PROJECT} && python3 'mcp-servers/ios_simulator_mcp.py'"
    ]
  }
}
```

#### Example Usage

```
# Build and test loop
build_and_deploy()
launch_app()
screenshot = take_screenshot()
# Claude analyzes screenshot
tap(400, 350)  # Select player
screenshot = take_screenshot()
# Continue testing...
```

---

### 2. Image Generator MCP

**Transport**: stdio or SSE
**Purpose**: AI image/video generation via Google Gemini

#### Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `generate_image()` | Create image from prompt | `prompt, name, reference?, count` |
| `generate_video()` | Create video from prompt | `prompt, name, duration` |
| `get_learnings()` | Retrieve generation patterns | `character?: str` |
| `list_references()` | Show available references | `character?: str` |

#### Configuration

```json
{
  "image-generator": {
    "command": "python",
    "args": ["mcp-servers/mcp_image_server.py"],
    "env": {
      "GOOGLE_API_KEY": "${GOOGLE_API_KEY}"
    }
  }
}
```

#### Example Usage

```
# Generate character with reference
generate_image(
  prompt="Same character celebrating",
  name="bennie-celebrating",
  reference="bennie-reference.png",
  count=4
)

# Generate video
generate_video(
  prompt="Character waving hello",
  name="bennie-waving",
  duration=2
)
```

---

### 3. Chrome DevTools MCP

**Transport**: Built-in (no configuration needed)
**Purpose**: Browser automation, testing, performance analysis

#### Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `navigate_page()` | Go to URL | `url: str` |
| `take_screenshot()` | Capture page | `fullPage?: bool` |
| `take_snapshot()` | A11y tree snapshot | `verbose?: bool` |
| `click(uid)` | Click element | `uid: str` |
| `fill(uid, value)` | Input text | `uid, value: str` |
| `hover(uid)` | Mouse over | `uid: str` |
| `press_key(key)` | Keyboard input | `key: str` |
| `list_pages()` | Open tabs | - |
| `select_page(idx)` | Switch tab | `pageIdx: int` |
| `list_network_requests()` | XHR/fetch logs | `resourceTypes?: array` |
| `list_console_messages()` | Console output | `types?: array` |
| `performance_start_trace()` | Begin perf recording | `reload, autoStop: bool` |
| `performance_stop_trace()` | End recording | - |

#### Example Usage

```
# Automated form filling
navigate_page(url="https://example.com/form")
snapshot = take_snapshot()
# Find input UIDs from snapshot
fill(uid="input-email", value="test@example.com")
fill(uid="input-password", value="secure123")
click(uid="button-submit")
```

---

## Capabilities Matrix

### What Maestro Can Do

| Capability | MCP Server | Use Case |
|------------|------------|----------|
| Build iOS apps | iOS Simulator | Compile and deploy |
| Screenshot analysis | iOS Simulator, Chrome | Visual verification |
| UI automation | iOS Simulator, Chrome | Tap, swipe, click, fill |
| Run tests | iOS Simulator | XCUITests |
| Generate images | Image Generator | Character art, backgrounds |
| Generate videos | Image Generator | Animations, cutscenes |
| Browser testing | Chrome DevTools | Web QA |
| Performance profiling | Chrome DevTools | Core Web Vitals |
| Network debugging | Chrome DevTools | API inspection |

### Skills Available

| Category | Skills |
|----------|--------|
| Development | `ios-dev`, `swiftui-ipad`, `testing` |
| Animation | `animation-system`, `ludo-automation` |
| Design | `visual-design`, `design-autism`, `image-generation` |
| Content | `story-characters`, `gameplay`, `audio-voice` |
| Infrastructure | `parent-dashboard`, `website-review` |

---

## Workflow Examples

### Build → Test → Fix Loop

```
┌─────────────────┐
│ build_and_deploy│
└────────┬────────┘
         ▼
┌─────────────────┐
│  launch_app()   │
└────────┬────────┘
         ▼
┌─────────────────┐
│take_screenshot()│
└────────┬────────┘
         ▼
┌─────────────────┐     ┌──────────────┐
│ Claude analyzes │────▶│ Issues found │
└────────┬────────┘     └──────┬───────┘
         │                     │
         ▼                     ▼
┌─────────────────┐     ┌──────────────┐
│   Tests pass    │     │  Fix code    │
└────────┬────────┘     └──────┬───────┘
         │                     │
         ▼                     ▼
┌─────────────────┐     ┌──────────────┐
│     Done!       │     │ git commit   │
└─────────────────┘     └──────┬───────┘
                               │
                               ▼
                        ┌──────────────┐
                        │   git push   │
                        └──────┬───────┘
                               │
                               └──────────▶ (loop back to build)
```

### Keyframe → Animation Pipeline

```
┌─────────────────────┐
│ Load character ref  │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Generate START frame│ (Gemini 3.0)
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Generate END frame  │ (Gemini 3.0)
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Browser automation  │ (Chrome DevTools MCP)
│ - Upload keyframes  │
│ - Click "Animate"   │
│ - Download ZIP      │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Process spritesheet │
│ - Extract frames    │
│ - Generate Lottie   │
│ - QA validation     │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Copy to Resources/  │
└─────────────────────┘
```

### Design Verification Flow

```
┌─────────────────────┐
│ Build and launch    │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Navigate to screen  │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Take screenshot     │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Claude checks:      │
│ - Touch targets 96pt│
│ - Color palette     │
│ - Character colors  │
│ - Layout alignment  │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Report findings     │
└─────────────────────┘
```

---

## Creating New Skills

### Skill Template

```markdown
# Skill Name

> One-line description

## When to Use

- Trigger condition 1
- Trigger condition 2

## Prerequisites

- Required tools/MCPs
- Required environment variables

## Workflow

1. Step one
2. Step two
3. Step three

## Examples

\`\`\`
Example usage...
\`\`\`

## Common Issues

| Problem | Solution |
|---------|----------|
| Issue 1 | Fix 1 |
```

### Skill Registration

Add to `.claude/skills/your-skill.md` and reference in `config/capabilities.json`:

```json
{
  "skills": [
    "existing-skill",
    "your-new-skill"
  ]
}
```

---

## Troubleshooting

### MCP Connection Issues

**Problem**: iOS Simulator MCP won't connect

```bash
# Test SSH manually
ssh -i ~/.ssh/macincloud_key user@host "echo OK"

# Check Python on remote
ssh user@host "python3 --version"

# Verify MCP server exists
ssh user@host "ls -la ~/BennieGame/mcp-servers/"
```

**Problem**: Chrome DevTools not responding

```bash
# Ensure Chrome is running with remote debugging
# Check that no other process is using port 9222
```

**Problem**: Image generation fails

```bash
# Verify API key
python -c "import os; print(bool(os.getenv('GOOGLE_API_KEY')))"

# Test Gemini connectivity
python -c "import google.genai; print('OK')"
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Connection refused` | MCP server not running | Start server manually |
| `Permission denied` | SSH key permissions | `chmod 600 ~/.ssh/key` |
| `API key invalid` | Wrong/expired key | Regenerate in console |
| `Timeout` | Network/server slow | Increase timeout |
| `Module not found` | Missing dependency | `pip install -r requirements.txt` |

### Logging

Enable verbose logging:

```bash
export MCP_DEBUG=1
export CLAUDE_LOG_LEVEL=debug
```

---

## Security

### Secret Management

All secrets must be stored in `.env` and accessed via environment variables:

```python
# CORRECT
import os
api_key = os.getenv("GOOGLE_API_KEY")

# WRONG - Never hardcode!
api_key = "AIza..."
```

### SSH Key Security

```bash
# Generate secure key
ssh-keygen -t ed25519 -f ~/.ssh/macincloud_key -C "maestro@local"

# Set correct permissions
chmod 600 ~/.ssh/macincloud_key
chmod 644 ~/.ssh/macincloud_key.pub
```

### API Key Rotation

Rotate keys periodically:
1. Generate new key in provider console
2. Update `.env` file
3. Test connectivity
4. Revoke old key

---

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | Yes | Gemini image generation |
| `GEMINI_API_KEY` | Yes | Alternative to above |
| `SSH_KEY_PATH` | For iOS | Path to SSH private key |
| `MACINCLOUD_HOST` | For iOS | Mac server hostname |
| `MACINCLOUD_USER` | For iOS | SSH username |
| `MACINCLOUD_PROJECT` | For iOS | Project path on Mac |
| `MCP_MAX_RESPONSE_KB` | No | Max response size (default 400) |
| `MCP_DEBUG` | No | Enable debug logging |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-01 | Initial release |

---

## Support

- **Documentation**: This file + `README.md`
- **Issues**: Check `TROUBLESHOOTING.md`
- **Skills**: See `skills-templates/` directory
