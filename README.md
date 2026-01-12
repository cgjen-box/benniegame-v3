# Bennie Bear - MacinCloud Transfer Package

## 📁 Final Structure

```
Bennie und die Lemminge v3/
│
├── 📖 CLAUDE.md                      ← Main context (read first!)
├── 📋 PLAYBOOK_CONDENSED.md          ← Readable design spec (NEW!)
├── 🚀 CLAUDE_CODE_STARTUP_PROMPT.md  ← Copy into Claude Code
├── 🔧 MCP_SETUP.md                   ← MCP configuration guide (NEW!)
├── 📋 README.md                      ← This file
│
├── .gsd/                             ← GSD Workflow
│   ├── PROJECT.md
│   ├── STATE.md                      ← Current position
│   ├── PLAN.md                       ← 3 tasks ready
│   ├── ROADMAP.md
│   ├── ISSUES.md
│   └── SUMMARY.md
│
├── .claude/skills/ios-dev/           ← Skill docs
│   └── SKILL.md
│
├── design/references/                ← Design images (49 files)
│   ├── character/bennie/
│   ├── character/lemminge/
│   ├── screens/
│   └── components/
│
├── starter-kits/                     ← Tool templates
│
├── BENNIE_BRAND_PLAYBOOK_v3_1.md     ← Full spec (TOO LARGE for Claude)
├── DESIGN_QA_CHECKLIST.md
└── SWIFTUI_CODING_GUIDELINES.md
```

## ⚠️ Known Issues & Solutions

### Issue 1: Playbook Too Large
**Problem**: `BENNIE_BRAND_PLAYBOOK_v3_1.md` is 38K tokens (limit: 25K)

**Solution**: Use `PLAYBOOK_CONDENSED.md` instead - contains all essential info in readable size.

### Issue 2: MCP Tools Not Available
**Problem**: ios-simulator MCP tools not connected

**Solution**: 
1. Read `MCP_SETUP.md` for configuration
2. Or use manual bash commands (see below)

## 🎯 Quick Start on MacinCloud

### Step 1: Read Context
```bash
cat CLAUDE.md
cat PLAYBOOK_CONDENSED.md
cat .gsd/STATE.md
cat .gsd/PLAN.md
```

### Step 2: Check MCP or Use Manual Commands

**If MCP available:**
```python
boot_simulator()
build_and_deploy(pull_latest=True)
launch_app()
take_screenshot()
```

**If MCP NOT available (manual):**
```bash
# Boot simulator
xcrun simctl boot "iPad (10th generation)" 2>/dev/null || true
open -a Simulator

# Take screenshot
xcrun simctl io booted screenshot ~/screenshot.png
open ~/screenshot.png
```

### Step 3: Verify Design
For every screenshot, check:
- ✅ Bennie is BROWN (#8C7259), NO clothing
- ✅ Lemminge are BLUE (#6FA8DC), NEVER green
- ✅ Touch targets >= 96pt
- ✅ German text only

## 📋 Current Plan

| # | Task | Status |
|---|------|--------|
| 01 | Connect & Build | ⬜ Ready |
| 02 | Capture baselines | ⬜ Ready |
| 03 | Verify design | ⬜ Ready |

## 🗑️ Files to Delete (Optional)

These can be removed to save space:
- `compass_artifact_wf-*.md` - temp file
- `files.zip` - old archive
- `GSD start.zip` - old archive

---

**Ready for Claude Code on MacinCloud!**
