---
name: animation
description: Create Lottie animations using Gemini keyframes and Ludo.ai interpolation pipeline
---

# Animation Skill - Bennie Bear

## Overview

Create Lottie animations using the Gemini keyframes + Ludo.ai interpolation pipeline.

**Starter Kits**:
- `starter-kits/ludo-animation-pipeline/` - Full keyframe → animation pipeline
- `starter-kits/lottie-animation-system/` - Lottie JSON tools

## Animation Pipeline

```
Gemini 3.0 (Keyframes) → Ludo.ai (Interpolation) → Lottie JSON
2 keyframes → 42 interpolated frames → PNG-embedded Lottie
```

## Commands

### Generate Keyframes
```bash
cd starter-kits/ludo-animation-pipeline
python generate_keyframes.py bennie waving
```

### Process Ludo.ai Downloads
```bash
cd starter-kits/ludo-animation-pipeline

# Show status
python process.py --status

# Process all new ZIPs
python process.py

# With custom settings
python process.py --fps 30 --grid 6x6
```

### Create Lottie from Frames
```bash
cd starter-kits/lottie-animation-system
python create_lottie.py frames --input ./frames/*.png --output animation.json
```

### Validate Lottie
```bash
python validate_lottie.py animation.json
```

## Animation Specs

From `config/animation_specs.json`:

| Animation | Character | Duration | Frames |
|-----------|-----------|----------|--------|
| idle | Bennie | 2000ms | 60 |
| happy | Bennie | 1400ms | 42 |
| thinking | Bennie | 2000ms | 60 |
| celebrating | Bennie | 1400ms | 42 |
| idle | Lemminge | 1000ms | 30 |
| curious | Lemminge | 800ms | 24 |
| excited | Lemminge | 600ms | 18 |

## Workflow

1. Generate keyframes via Gemini (START and END poses)
2. **CDP Automation** - Upload keyframes to Ludo.ai via Chrome DevTools Protocol
3. Wait for generation (~2 min per animation)
4. Export and download animation ZIP
5. Place ZIP in `starter-kits/ludo-animation-pipeline/downloads/`
6. Run `python process.py` to convert to Lottie
7. Output copied to `BennieGame/Resources/Lottie/`

## CDP Automation (Recommended)

For automated processing, use the CDP scripts instead of manual upload:

```bash
# 1. Launch Chrome in debug mode
./scripts/launch-chrome-debug.sh https://app.ludo.ai

# 2. Log in to Ludo.ai manually (one-time)

# 3. Run batch automation
python scripts/ludo_batch_process.py

# Or process single animation
python scripts/ludo_batch_process.py bennie waving
```

**Full CDP documentation**: `starter-kits/ludo-animation-pipeline/LUDO_CDP_WORKFLOW.md`

### Key CDP Learnings

- Click frame THUMBNAIL to open upload dialog (not buttons)
- Clear existing frame with trash icon before uploading
- Filter Animate button by `width > 200` (not sidebar tab)
- Export sprite selection: click `img.parentElement`, not coordinates
- Generation takes ~2 minutes per animation

## Output Locations

- Keyframes: `design/generated/Animations/keyframes/`
- Lottie files: `design/generated/Animations/lottie/`
- Xcode assets: `BennieGame/Resources/Lottie/`

## Full Documentation

- Ludo Pipeline: `starter-kits/ludo-animation-pipeline/SKILL.md`
- CDP Automation: `starter-kits/ludo-animation-pipeline/LUDO_CDP_WORKFLOW.md`
- Lessons Learned: `starter-kits/ludo-animation-pipeline/LESSONS_LEARNED.md`
- Lottie Tools: `starter-kits/lottie-animation-system/SKILL.md`
