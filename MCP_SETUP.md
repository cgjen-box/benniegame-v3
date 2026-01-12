# iOS Simulator MCP Setup - MacinCloud

## Quick Setup

The ios-simulator MCP tools require a Python MCP server running on MacinCloud.

### Step 1: Check if MCP server exists

```bash
ls -la ~/app/starter-kits/maestro-orchestration/mcp-servers/
```

You should see `ios_simulator_mcp.py`

### Step 2: Install dependencies

```bash
cd ~/app/starter-kits/maestro-orchestration
pip3 install -r requirements.txt
```

### Step 3: Configure Claude Code MCP

Create/edit `~/.claude/settings.local.json`:

```json
{
  "mcpServers": {
    "ios-simulator": {
      "command": "python3",
      "args": [
        "/Users/user289321/app/starter-kits/maestro-orchestration/mcp-servers/ios_simulator_mcp.py"
      ]
    }
  }
}
```

### Step 4: Restart Claude Code

Close and reopen Claude Code for MCP to connect.

### Step 5: Verify MCP tools

In Claude Code, try:
```
boot_simulator()
```

---

## Alternative: Manual Commands

If MCP isn't working, use these bash commands directly:

### Boot Simulator
```bash
xcrun simctl boot "iPad (10th generation)" 2>/dev/null || true
open -a Simulator
```

### Build & Deploy
```bash
cd ~/BennieGame  # or wherever the Xcode project is
git pull
xcodebuild -scheme BennieGame -destination "platform=iOS Simulator,name=iPad (10th generation)" build
xcrun simctl install booted ~/Library/Developer/Xcode/DerivedData/BennieGame-*/Build/Products/Debug-iphonesimulator/BennieGame.app
```

### Launch App
```bash
xcrun simctl launch booted com.bennie.BennieGame
```

### Take Screenshot
```bash
xcrun simctl io booted screenshot ~/screenshot.png
open ~/screenshot.png
```

### Tap (requires idb or appium)
```bash
# Using Facebook IDB (if installed)
idb ui tap 400 350
```

---

## Troubleshooting

### "No MCP tools available"
1. Check `~/.claude/settings.local.json` exists
2. Verify Python path: `which python3`
3. Restart Claude Code

### "Simulator not found"
```bash
xcrun simctl list devices | grep iPad
```

### "Build fails"
```bash
# Clean derived data
rm -rf ~/Library/Developer/Xcode/DerivedData/BennieGame-*
```
