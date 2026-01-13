---
name: ios-dev
description: Build, test, and debug Bennie Bear iPad app on MacinCloud with MCP tools
---

# iOS Development Skill - Bennie Bear

## Overview

This skill covers building, testing, and debugging the Bennie Bear iPad app on MacinCloud.

## MCP Tools (ios-simulator)

| Tool | Description |
|------|-------------|
| `boot_simulator()` | Start iPad simulator |
| `build_and_deploy(pull_latest=True)` | Git pull + build + install |
| `launch_app()` | Open BennieGame |
| `terminate_app()` | Close app |
| `take_screenshot()` | Capture screen as base64 PNG |
| `tap(x, y)` | Touch at coordinates |
| `swipe(x1, y1, x2, y2)` | Drag gesture |
| `type_text(text)` | Keyboard input |
| `save_baseline("name")` | Save screenshot as reference |
| `compare_to_baseline("name")` | Compare current vs saved |
| `list_baselines()` | Show all baselines |
| `run_tests()` | Execute XCUITests |
| `get_logs()` | App console output |

## Screen Coordinates

iPad 10th Gen Landscape: **1194 × 834 points**

| Element | Coordinates |
|---------|-------------|
| Alexander button | (400, 350) |
| Oliver button | (800, 350) |
| Rätsel (Puzzles) | (300, 400) |
| Zahlen (Numbers) | (500, 400) |
| Logik (Logic) | (700, 400) |
| Zeichnen (Drawing) | (900, 400) |
| Treasure chest | (1050, 700) |
| Back/Home | (60, 50) |
| Settings | (1134, 50) |

## Build Workflow

```python
# Standard build + test cycle
boot_simulator()
build_and_deploy(pull_latest=True)
launch_app()
take_screenshot()  # Analyze result
```

## Visual Regression

```python
# Capture baselines (when app looks correct)
save_baseline("player_select")
tap(400, 350)
save_baseline("home_screen")

# Later: compare against baselines
compare_to_baseline("player_select")
```

## Design Verification

For every screenshot, check:
- [ ] Bennie is brown (#8C7259), no clothing
- [ ] Lemminge are blue (#6FA8DC), never green
- [ ] Touch targets >= 96pt
- [ ] German text only
- [ ] No red/neon colors

## Troubleshooting

### Build fails
```bash
# Clean derived data
rm -rf ~/Library/Developer/Xcode/DerivedData/BennieGame-*
build_and_deploy(pull_latest=True)
```

### Simulator not responding
```python
terminate_app()
boot_simulator()
launch_app()
```

### App crashes on launch
```python
get_logs()  # Check console output
```
