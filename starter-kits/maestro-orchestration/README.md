# Maestro Orchestration Starter Kit

> Portable Claude Code orchestration layer with MCP servers, skills, and automation workflows.

## What's Included

- **3 MCP Servers**: iOS Simulator, Image Generator, Chrome DevTools
- **Config Templates**: Ready-to-customize settings
- **Setup Scripts**: Windows + Unix automated setup
- **Skill Templates**: Create your own skills
- **Workflow Examples**: Common automation patterns

## 5-Minute Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy template
cp config/.env.example .env

# Edit with your API keys
# Required: GOOGLE_API_KEY or GEMINI_API_KEY
# Optional: SSH_KEY_PATH, MACINCLOUD_HOST (for iOS)
```

### 3. Configure Claude Code

Copy `config/settings.local.json.template` to `~/.claude/settings.local.json` and update:

- `${SSH_KEY_PATH}` → Your SSH key path
- `${MACINCLOUD_USER}` → Your MacinCloud username
- `${MACINCLOUD_HOST}` → Your MacinCloud server
- `${MACINCLOUD_PROJECT}` → Project path on Mac

### 4. Test Connectivity

```bash
python scripts/test-mcp-connection.py
```

### 5. Done!

The MCP servers will auto-connect when you start Claude Code.

## Quick Reference

### iOS Simulator MCP

```
build_and_deploy()     # Build + install app
take_screenshot()      # Capture simulator
tap(x, y)              # Touch at coordinates
run_tests()            # Run XCUITests
```

### Image Generator MCP

```
generate_image(prompt, name, reference?, count)
generate_video(prompt, name, duration)
```

### Chrome DevTools MCP

```
navigate_page(url)     # Go to URL
take_snapshot()        # A11y tree
click(uid)             # Click element
fill(uid, value)       # Input text
```

## Directory Structure

```
maestro-orchestration/
├── SKILL.md                    # Full documentation
├── README.md                   # This file
├── requirements.txt            # Python dependencies
│
├── mcp-servers/                # MCP server implementations
│   ├── ios_simulator_mcp.py
│   ├── mcp_image_server.py
│   └── mcp_*.py
│
├── config/
│   ├── .env.example            # Environment template
│   ├── settings.local.json.template
│   └── capabilities.json       # Full capability manifest
│
├── scripts/
│   ├── setup-maestro.ps1       # Windows setup
│   ├── setup-maestro.sh        # Unix setup
│   └── test-mcp-connection.py  # Connectivity test
│
├── skills-templates/           # Skill creation templates
│   └── skill-template.md
│
└── examples/                   # Workflow examples
    ├── workflow-build-test.md
    └── workflow-animation.md
```

## Next Steps

1. Read `SKILL.md` for full documentation
2. Check `examples/` for workflow patterns
3. Use `skills-templates/` to create custom skills

## Troubleshooting

**MCP won't connect?**
```bash
python scripts/test-mcp-connection.py
```

**SSH permission denied?**
```bash
chmod 600 ~/.ssh/your_key
```

**Missing dependencies?**
```bash
pip install -r requirements.txt --upgrade
```

See `SKILL.md` for detailed troubleshooting.
