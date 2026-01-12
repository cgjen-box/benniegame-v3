# Design Verification Workflow

> Screenshot-based design verification using iOS Simulator MCP with semantic analysis.

## Overview

Automated visual QA that checks screenshots against design specifications:

1. Build and launch app
2. Navigate to each screen
3. Capture screenshot
4. Claude analyzes against design spec
5. Report violations
6. Fix and repeat

## Prerequisites

- iOS Simulator MCP connected
- Design specification documented
- Baseline screenshots (optional)

## The Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    DESIGN VERIFICATION FLOW                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌───────────────────┐                                         │
│   │ Build and launch  │                                         │
│   └─────────┬─────────┘                                         │
│             │                                                   │
│             ▼                                                   │
│   ┌───────────────────┐                                         │
│   │ Navigate to screen│◀──────────────────────┐                 │
│   └─────────┬─────────┘                       │                 │
│             │                                 │                 │
│             ▼                                 │                 │
│   ┌───────────────────┐                       │                 │
│   │ Take screenshot   │                       │                 │
│   └─────────┬─────────┘                       │                 │
│             │                                 │                 │
│             ▼                                 │                 │
│   ┌───────────────────────────────────────┐   │                 │
│   │         CLAUDE ANALYZES               │   │                 │
│   ├───────────────────────────────────────┤   │                 │
│   │ - Touch targets >= 96pt?              │   │                 │
│   │ - Colors match BennieColor palette?   │   │                 │
│   │ - Bennie brown, no vest?              │   │                 │
│   │ - Lemminge blue, never green?         │   │                 │
│   │ - Typography .rounded, German?        │   │                 │
│   │ - Wooden UI elements have grain?      │   │                 │
│   │ - Layout matches mockup?              │   │                 │
│   │ - Accessibility labels present?       │   │                 │
│   └─────────────────┬─────────────────────┘   │                 │
│                     │                         │                 │
│                     ▼                         │                 │
│              ┌─────────────┐                  │                 │
│              │  Violations │                  │                 │
│              │   found?    │                  │                 │
│              └──────┬──────┘                  │                 │
│                     │                         │                 │
│           ┌─────────┴─────────┐               │                 │
│           │                   │               │                 │
│          YES                 NO               │                 │
│           │                   │               │                 │
│           ▼                   ▼               │                 │
│   ┌───────────────┐   ┌───────────────┐       │                 │
│   │ Report issues │   │ More screens? │───YES─┘                 │
│   └───────────────┘   └───────┬───────┘                         │
│                               │                                 │
│                              NO                                 │
│                               │                                 │
│                               ▼                                 │
│                       ┌───────────────┐                         │
│                       │   All pass!   │                         │
│                       └───────────────┘                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Design Checklist

### Character Colors (Critical)

| Character | Color | Hex | Violation |
|-----------|-------|-----|-----------|
| Bennie | Brown fur | #8C7259 | Any other color |
| Bennie | Tan snout | #C4A574 | Wrong snout color |
| Bennie | No clothing | - | Any vest, accessories |
| Lemminge | Blue body | #6FA8DC | Green or brown |
| Lemminge | White belly | White | Missing belly |
| Lemminge | Pink nose | #E8A0A0 | Wrong nose color |

### Touch Targets (Critical)

All interactive elements must be >= 96pt minimum dimension.

### Color Palette

| Name | Hex | Allowed Usage |
|------|-----|---------------|
| Woodland | #738F66 | Primary UI |
| Bark | #8C7259 | Secondary UI |
| Sky | #B3D1E6 | Accents |
| Cream | #FAF5EB | Backgrounds |
| Success | #99BF8C | Positive feedback |
| CoinGold | #D9C27A | Coin/treasure |

### Forbidden

- Pure white (#FFFFFF) for large areas
- Pure black (#000000) for large areas
- Bright red (#FF0000)
- Neon colors
- Saturation > 80%

## MCP Tools Used

| Tool | Purpose |
|------|---------|
| `build_and_deploy()` | Build latest code |
| `launch_app()` | Start app |
| `take_screenshot()` | Capture screen |
| `tap(x, y)` | Navigate UI |
| `save_baseline()` | Store reference |
| `compare_to_baseline()` | Visual diff |

## Example Session

### Initial Verification

```
# Build and launch
build_and_deploy()
launch_app()

# Verify player select screen
screenshot = take_screenshot()
# Claude analyzes and reports...

# Navigate to home
tap(400, 350)  # Select Alexander
screenshot = take_screenshot()
# Claude analyzes and reports...

# Check activities menu
tap(600, 400)  # Open activities
screenshot = take_screenshot()
# Claude analyzes and reports...
```

### Baseline Comparison

```
# Save baseline when design is correct
save_baseline("player_select")

# Later, after code changes
build_and_deploy(pull_latest=True)
launch_app()
compare_to_baseline("player_select")
# Returns both images for Claude comparison
```

## Screen Navigation Map

| Screen | Navigation | Coordinates |
|--------|------------|-------------|
| Player Select | App launch | - |
| Home (Alexander) | Tap left player | (400, 350) |
| Home (Oliver) | Tap right player | (800, 350) |
| Activities | From home | (600, 400) |
| Puzzle L1 | Tap Ratsel | TBD |
| Numbers L1 | Tap Zahlen | TBD |
| Treasure | Tap treasure | TBD |
| Parent Dashboard | PIN gate | TBD |

## Analysis Categories

### Critical (Must Fix)

- Touch targets < 96pt
- Character color wrong
- Missing accessibility labels
- Forbidden colors used

### Warning (Should Fix)

- Layout shift from baseline
- Font not .rounded
- Missing wood grain
- Shadow inconsistency

### Info (Optional)

- Minor alignment variation
- Animation frame difference
- Slight color temperature shift

## Report Format

```markdown
## Design Verification Report

### Screen: Player Select

**Status**: 2 violations found

| Issue | Severity | Location | Fix |
|-------|----------|----------|-----|
| Touch target 64pt | Critical | Play button | Increase to 96pt |
| Lemminge green tint | Critical | Background | Correct to #6FA8DC |

### Screen: Home

**Status**: Pass

All checks passed.
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Screenshot blank | `boot_simulator()` first |
| Wrong screen | Check navigation coordinates |
| Colors look different | Account for simulator rendering |
| Touch targets unclear | Use layout inspector |

## Best Practices

1. **Verify after every visual change**: Run verification before committing
2. **Update baselines carefully**: Only when design is approved
3. **Check all screens**: Don't skip "simple" screens
4. **Document exceptions**: If violation is intentional, note why
5. **Fix critical first**: Address touch targets and character colors immediately
