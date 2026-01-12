# Build → Test → Fix Workflow

> Automated iOS app build, test, and fix loop using iOS Simulator MCP.

## Overview

This workflow enables continuous build-test-fix cycles without leaving Claude Code:

1. Pull latest code from git
2. Build with Xcode
3. Deploy to simulator
4. Take screenshots for analysis
5. Run automated tests
6. Fix any issues found
7. Commit and push
8. Repeat

## Prerequisites

- iOS Simulator MCP connected
- SSH key configured for MacinCloud
- Xcode project on remote Mac
- Git repository initialized

## The Loop

```
┌──────────────────────────────────────────────────────────────┐
│                     BUILD → TEST → FIX                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────────┐                                            │
│   │ git pull    │◀────────────────────────────────┐          │
│   └──────┬──────┘                                 │          │
│          ▼                                        │          │
│   ┌─────────────┐                                 │          │
│   │xcodebuild   │                                 │          │
│   └──────┬──────┘                                 │          │
│          ▼                                        │          │
│   ┌─────────────┐                                 │          │
│   │simctl install│                                │          │
│   └──────┬──────┘                                 │          │
│          ▼                                        │          │
│   ┌─────────────┐     ┌───────────┐               │          │
│   │ screenshot  │────▶│  Claude   │               │          │
│   └──────┬──────┘     │ analyzes  │               │          │
│          │            └─────┬─────┘               │          │
│          │                  │                     │          │
│          │            ┌─────▼─────┐               │          │
│          │            │  Issues?  │               │          │
│          │            └─────┬─────┘               │          │
│          │                  │                     │          │
│          │         ┌────────┴────────┐            │          │
│          │         │                 │            │          │
│          │        YES               NO            │          │
│          │         │                 │            │          │
│          │         ▼                 ▼            │          │
│          │   ┌───────────┐    ┌───────────┐       │          │
│          │   │ Fix code  │    │   Done!   │       │          │
│          │   └─────┬─────┘    └───────────┘       │          │
│          │         │                              │          │
│          │         ▼                              │          │
│          │   ┌───────────┐                        │          │
│          │   │git commit │                        │          │
│          │   └─────┬─────┘                        │          │
│          │         │                              │          │
│          │         ▼                              │          │
│          │   ┌───────────┐                        │          │
│          │   │ git push  │────────────────────────┘          │
│          │   └───────────┘                                   │
│          │                                                   │
└──────────┴───────────────────────────────────────────────────┘
```

## MCP Tools Used

| Tool | Purpose |
|------|---------|
| `build_and_deploy()` | Git pull + Xcode build + simctl install |
| `launch_app()` | Start app in simulator |
| `take_screenshot()` | Capture current screen |
| `tap(x, y)` | Navigate UI |
| `run_tests()` | Execute XCUITests |
| `get_logs()` | Check console output |

## Example Session

### Initial Build

```
# Start the loop
build_and_deploy()
# Output: "Build successful. App installed to iPad (10th generation)"

launch_app()
# Output: "App launched: com.bennie.BennieGame"
```

### Screenshot Analysis

```
screenshot = take_screenshot()
# Claude receives base64 PNG and analyzes:
# - Layout correctness
# - Color palette compliance
# - Touch target sizes
# - Character appearances
```

### UI Navigation

```
# Navigate through screens
tap(400, 350)  # Select player
screenshot = take_screenshot()

tap(600, 400)  # Open activities
screenshot = take_screenshot()

tap(300, 300)  # Start puzzle
screenshot = take_screenshot()
```

### Running Tests

```
run_tests()
# Output: Test results showing pass/fail status
```

### Getting Logs

```
logs = get_logs(lines=50)
# Check for errors, warnings, or unexpected behavior
```

## Design Verification Checklist

Claude automatically checks each screenshot for:

| Check | Requirement |
|-------|-------------|
| Touch targets | >= 96pt |
| Bennie color | Brown (#8C7259), no vest |
| Lemminge color | Blue (#6FA8DC), never green |
| Color saturation | < 80% for UI elements |
| Text language | German only |

## Iteration Pattern

```python
# Pseudo-code for the loop
while True:
    build_and_deploy(pull_latest=True)
    launch_app()

    for screen in test_screens:
        navigate_to(screen)
        screenshot = take_screenshot()
        issues = analyze(screenshot)

        if issues:
            fix_issues(issues)
            commit_and_push()
            break  # Restart loop

    if run_tests().all_passed:
        print("All tests pass!")
        break
```

## Tips

1. **Start simple**: Test one screen at a time
2. **Save baselines**: Capture "good" screenshots for comparison
3. **Check logs**: Console output often reveals issues before visual inspection
4. **Batch commits**: Group related fixes together
5. **Run full tests**: After UI fixes, run `run_tests()` to catch regressions

## Common Issues

| Problem | Solution |
|---------|----------|
| Build fails | Check Xcode errors in output |
| App crashes on launch | Check `get_logs()` for crash reason |
| Screenshot blank | Simulator may need boot: `boot_simulator()` |
| Touch not registering | Verify coordinates (1194x834 screen) |
| Tests timeout | Increase test timeout or check app responsiveness |
