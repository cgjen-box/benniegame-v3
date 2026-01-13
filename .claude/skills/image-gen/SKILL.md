---
name: image-gen
description: Generate character-consistent AI images using Gemini 3.0 Pro with reference images for Bennie Bear project
---

# Image Generation Skill - Bennie Bear

## Overview

Generate character-consistent AI images using Google's Gemini 3.0 Pro with reference image technique.

**Starter Kit**: `starter-kits/gemini-image-pro-3/`

## Commands

```bash
# Basic generation
python generate_image.py generate "Prompt" --name output-name --count 4

# With reference image (recommended for character consistency)
python generate_image.py generate "Prompt" \
    --reference design/references/character/bennie/reference/bennie-reference.png \
    --name output-name --raw --count 4

# Training mode (A/B comparison for learning)
python generate_image.py generate "Prompt" --name output-name --training --character bennie
```

## Character References

| Character | Reference Path |
|-----------|----------------|
| Bennie | `design/references/character/bennie/reference/bennie-reference.png` |
| Lemminge | `design/references/character/lemminge/reference/lemminge-reference.png` |

## Character Rules

- **Bennie**: Brown (#8C7259), NO clothing, NO vest
- **Lemminge**: Blue (#6FA8DC), NEVER green or brown
- All images must follow PLAYBOOK_CONDENSED.md design rules

## A/B Training Workflow

```bash
# Start training session
python generate_image.py session start --name bennie-poses --category characters --character bennie

# Generate variants
python generate_image.py generate "Bennie waving" --training --character bennie

# Record feedback (A or B)
python generate_image.py feedback SESSION_ID ROUND_ID A --notes "Better proportions"

# Complete session
python generate_image.py session complete SESSION_ID
```

## Output Locations

- Generated images: `./generated/` (relative to script)
- For Xcode: Copy to `BennieGame/Resources/Assets.xcassets/`

## Environment Variables

Requires in `.env`:
```
GOOGLE_API_KEY=your_key
```

## Full Documentation

See: `starter-kits/gemini-image-pro-3/SKILL.md`
