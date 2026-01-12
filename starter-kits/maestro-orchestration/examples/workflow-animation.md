# Keyframe → Animation Workflow

> Automated sprite animation pipeline using Gemini keyframes + Ludo.ai interpolation + Chrome DevTools MCP.

## Overview

This workflow generates smooth character animations from just 2 keyframes:

1. Load frozen character reference
2. Generate START keyframe (Gemini 3.0)
3. Generate END keyframe (Gemini 3.0)
4. Upload to Ludo.ai (Chrome DevTools MCP)
5. Download interpolated spritesheet
6. Process into Lottie JSON
7. Copy to app resources

## Prerequisites

- Image Generator MCP connected
- Chrome DevTools MCP connected
- Ludo.ai account (5 credits per animation)
- Character reference images

## The Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                  KEYFRAME → ANIMATION PIPELINE                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌───────────────────┐                                         │
│   │ Load character    │                                         │
│   │ reference image   │                                         │
│   └─────────┬─────────┘                                         │
│             │                                                   │
│             ▼                                                   │
│   ┌───────────────────┐                                         │
│   │ Generate START    │  Gemini 3.0 Pro Image Preview           │
│   │ keyframe (pose 1) │                                         │
│   └─────────┬─────────┘                                         │
│             │                                                   │
│             ▼                                                   │
│   ┌───────────────────┐                                         │
│   │ Generate END      │  Gemini 3.0 Pro Image Preview           │
│   │ keyframe (pose 2) │                                         │
│   └─────────┬─────────┘                                         │
│             │                                                   │
│             ▼                                                   │
│   ┌───────────────────────────────────────────────────────────┐ │
│   │              BROWSER AUTOMATION (Chrome MCP)              │ │
│   ├───────────────────────────────────────────────────────────┤ │
│   │ 1. Navigate to ludo.ai/sprite-generator                  │ │
│   │ 2. Upload START keyframe (First Frame input)             │ │
│   │ 3. Upload END keyframe (Final Frame input)               │ │
│   │ 4. Enter animation description                           │ │
│   │ 5. Click "Animate" button (costs 5 credits)              │ │
│   │ 6. Wait for processing (~30-60 seconds)                  │ │
│   │ 7. Click "Export" → download ZIP                         │ │
│   └─────────────────────────┬─────────────────────────────────┘ │
│                             │                                   │
│                             ▼                                   │
│   ┌───────────────────────────────────────────────────────────┐ │
│   │              POST-PROCESSING                              │ │
│   ├───────────────────────────────────────────────────────────┤ │
│   │ 1. Extract ZIP to get spritesheet                        │ │
│   │ 2. Detect grid (typically 6x7 = 42 frames)               │ │
│   │ 3. Extract individual frames                             │ │
│   │ 4. Calculate frame timing from animation_specs.json      │ │
│   │ 5. Generate Lottie JSON with embedded PNGs               │ │
│   │ 6. Run QA validation                                     │ │
│   │ 7. Generate frame strip for visual review                │ │
│   └─────────────────────────┬─────────────────────────────────┘ │
│                             │                                   │
│                             ▼                                   │
│   ┌───────────────────┐                                         │
│   │ Copy to app       │                                         │
│   │ Resources/Lottie/ │                                         │
│   └───────────────────┘                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## MCP Tools Used

### Image Generator MCP

| Tool | Purpose |
|------|---------|
| `generate_image()` | Create keyframes with reference |
| `list_references()` | Show available character refs |

### Chrome DevTools MCP

| Tool | Purpose |
|------|---------|
| `navigate_page()` | Go to ludo.ai |
| `take_snapshot()` | Get page element UIDs |
| `upload_file()` | Upload keyframe images |
| `fill()` | Enter animation description |
| `click()` | Trigger actions |
| `wait_for()` | Wait for processing |

## Example Session

### Step 1: Generate Keyframes

```
# List available references
list_references(character="bennie")
# Output: ["bennie-reference.png"]

# Generate START keyframe (neutral pose)
generate_image(
  prompt="Same character standing in neutral pose, arms at sides",
  name="bennie-waving-start",
  reference="bennie-reference.png",
  count=1
)

# Generate END keyframe (peak pose)
generate_image(
  prompt="Same character waving hello, arm raised high",
  name="bennie-waving-end",
  reference="bennie-reference.png",
  count=1
)
```

### Step 2: Browser Automation

```
# Navigate to Ludo.ai
navigate_page(url="https://ludo.ai/sprite-generator")

# Get page snapshot to find element UIDs
snapshot = take_snapshot()

# Upload keyframes
upload_file(uid="first-frame-input", filePath="keyframes/bennie-waving-start.png")
upload_file(uid="final-frame-input", filePath="keyframes/bennie-waving-end.png")

# Enter description
fill(uid="description-input", value="brown bear character waving hello")

# Click animate button
click(uid="animate-button")

# Wait for processing
wait_for(text="Export", timeout=90000)

# Download result
click(uid="export-button")
```

### Step 3: Process Result

```
# Processing happens automatically via process.py
# Or manually:
# 1. Extract ZIP
# 2. Run spritesheet processor
# 3. Generate Lottie JSON
# 4. Copy to Resources/Lottie/
```

## Animation Results

| Metric | Typical Value |
|--------|---------------|
| Input | 2 keyframes |
| Output | 42 frames |
| Duration | 1.4 - 2.8 seconds |
| Format | Lottie JSON (PNG-embedded) |
| Credits | 5 per animation |

## Timing Configuration

Configure per-animation timing in `config/animation_specs.json`:

```json
{
  "characters": {
    "bennie": {
      "waving": { "target_duration_ms": 1400 },
      "idle": { "target_duration_ms": 2000 },
      "celebrating": { "target_duration_ms": 1200 }
    }
  }
}
```

Frame hold formula:
```
frame_hold = round(target_seconds * fps / frame_count)
```

## Keyframe Best Practices

### START Frame
- Neutral pose
- Character centered
- Clear silhouette
- Consistent lighting with reference

### END Frame
- Peak of action
- Maximum extension/expression
- Same character position (centered)
- Same lighting and style

### Common Animations

| Animation | START Pose | END Pose |
|-----------|------------|----------|
| Waving | Arms at sides | Arm raised, palm open |
| Celebrating | Standing | Arms up, slight jump |
| Thinking | Standing | Hand on chin |
| Encouraging | Arms at sides | Arms extended forward |
| Idle | Standing | Slight breathing motion |

## QA Validation

The pipeline automatically validates:

| Check | Requirement |
|-------|-------------|
| Lottie structure | Valid JSON with assets/layers |
| Duration | 0.5s - 3.0s range |
| Frame count | Consistent with grid |
| File size | < 2MB for mobile |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Keyframes inconsistent | Use same reference image for both |
| Animation too fast | Increase target_duration_ms |
| Upload fails | Check file path is absolute |
| Processing stuck | Refresh page, try again |
| Export missing | Wait longer for processing |
| Lottie invalid | Check spritesheet grid detection |

## File Locations

| File | Location |
|------|----------|
| Keyframes | `downloads/keyframes/` |
| ZIPs | `downloads/` |
| Spritesheets | `downloads/extracted/` |
| Lotties | `output/` |
| Final | `Resources/Lottie/` |
