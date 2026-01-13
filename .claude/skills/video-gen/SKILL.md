---
name: video-gen
description: Generate short AI video clips using Google Veo 3.1 model
---

# Video Generation Skill - Bennie Bear

## Overview

Generate short AI video clips using Google's Veo 3.1 model.

**Starter Kit**: `starter-kits/veo-video-generation/`

## Commands

```bash
cd starter-kits/veo-video-generation

# Generate video
python generate_video.py generate "Prompt describing the scene" \
    --name output-name \
    --duration 6 \
    --resolution 1080p

# With reference image (for character consistency)
python generate_video.py generate "Bear walking through forest" \
    --name bear-walk \
    --reference path/to/reference.png
```

## Options

| Option | Values | Default |
|--------|--------|---------|
| --duration | 4, 6, 8 seconds | 6 |
| --resolution | 720p, 1080p | 1080p |
| --aspect-ratio | 16:9, 9:16 | 16:9 |
| --reference | Path to image | None |

## Usage Guidelines

- Videos are 4-8 seconds, good for UI transitions or celebrations
- Reference images help maintain character consistency
- Async operation with long polling (may take 1-2 minutes)

## Output Locations

- Generated videos: `./output/` (relative to script)

## Environment Variables

Requires in `.env`:
```
GOOGLE_API_KEY=your_key
```

## Full Documentation

See: `starter-kits/veo-video-generation/SKILL.md`
