# Veo 3.1 Video Generation - Starter Kit

> **API**: Google Veo 3.1 (veo-3.1-generate-preview)
> **Purpose**: Generate AI video clips with character reference support
> **Version**: Extracted from Bennie v1 (2025-12-30)

---

## Overview

Generate short AI video clips using Google's Veo 3.1 model. This starter kit provides:

- **Video generation** with configurable duration, resolution, and aspect ratio
- **Reference image support** for character consistency (up to 3 images)
- **Video extension** to add 7 seconds to existing clips
- **Long polling** for async operation handling

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp config/.env.example .env
# Edit .env with your GOOGLE_API_KEY

# 3. Generate video
python generate_video.py "Cartoon bear walking through forest" \
    --name bear-walk \
    --duration 6 \
    --resolution 720p
```

---

## API Reference

### Models

| Model ID | Type | Notes |
|----------|------|-------|
| `veo-3.1-generate-preview` | Primary | Full features |
| `veo-3.1-fast-generate-preview` | Fallback | Faster, lower quality |
| `veo-3.0-generate-001` | Fallback | Older version |

### Parameters

| Parameter | Options | Default | Notes |
|-----------|---------|---------|-------|
| `duration` | 4, 6, 8 | 8 | Seconds |
| `resolution` | 720p, 1080p | 720p | 1080p requires 8s duration |
| `aspect_ratio` | 16:9, 9:16 | 16:9 | Landscape or portrait |
| `reference_images` | Up to 3 | None | For character consistency |
| `negative_prompt` | String | None | What to avoid |

### Constraints

- 1080p resolution only supports 8-second duration
- Maximum 3 reference images per generation
- Generation takes 1-5 minutes typically
- Timeout after 20 minutes

---

## CLI Reference

### Generate Command

```bash
python generate_video.py PROMPT [OPTIONS]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--name, -n` | Output filename base (required) | - |
| `--duration, -d` | Duration in seconds (4, 6, 8) | 8 |
| `--resolution, -r` | Resolution (720p, 1080p) | 720p |
| `--aspect, -a` | Aspect ratio (16:9, 9:16) | 16:9 |
| `--reference` | Reference image(s) | None |
| `--negative` | Negative prompt | None |

### Extend Command

```bash
python generate_video.py extend SOURCE_VIDEO PROMPT [OPTIONS]
```

Adds 7 seconds to an existing video.

---

## Reference Images

### How It Works

Pass up to 3 reference images to guide the video generation:

```bash
python generate_video.py "Same character dancing" \
    --name character-dance \
    --reference path/to/character1.png \
    --reference path/to/character2.png
```

### Best Practices

1. Use high-quality reference images (PNG recommended)
2. Show character from multiple angles if possible
3. Keep backgrounds simple in reference images
4. Use consistent lighting across references

---

## Long Polling

Video generation is asynchronous with long polling:

```python
# Start generation (returns operation)
operation = client.models.generate_videos(...)

# Poll until complete (10s intervals)
while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)

# Check result
if operation.error:
    raise RuntimeError(operation.error)

video = operation.response.generated_videos[0]
```

### Timeouts

- Default poll interval: 10 seconds
- Maximum polls: 120 (20 minutes total)
- Log update every minute

---

## Output Format

- Format: MP4
- Filename: `{name}_{timestamp}.mp4`
- Location: `./generated/videos/`

---

## File Structure

```
veo-video-generation/
├── SKILL.md                    # This documentation
├── README.md                   # Quick start guide
├── requirements.txt            # Python dependencies
├── generate_video.py           # Main generation script
├── secret_guard.py             # Secure API key management
├── config/
│   ├── .env.example            # Environment template
│   └── video_presets.json      # Common configurations
└── examples/
    ├── basic_generation.py
    ├── reference_guided.py
    └── character_animation.py
```

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Duration must be 4, 6, or 8` | Invalid duration | Use allowed values |
| `1080p only supports 8s` | Resolution/duration mismatch | Use 8s with 1080p |
| `Timeout after 20 minutes` | Generation too slow | Try shorter duration or lower resolution |
| `GOOGLE_API_KEY not set` | Missing API key | Add to .env file |

### Retry Behavior

Video generation doesn't auto-retry on failures. If generation fails:
1. Check error message
2. Adjust parameters if needed
3. Retry manually

---

## Best Practices

1. **Start with 720p** - Faster and uses fewer resources
2. **Use 4s duration for tests** - Quicker iterations
3. **Include reference images** - Better character consistency
4. **Write descriptive prompts** - Be specific about motion and style
5. **Use negative prompts** - Exclude unwanted elements

---

## Example Prompts

### Character Animation
```
Cartoon bear character walking forward slowly, smooth animation,
side view, forest background, gentle movement, children's animation style
```

### Scene Transition
```
Camera slowly panning right through a magical forest,
golden hour lighting, soft focus, peaceful atmosphere
```

### Looping Animation
```
Single character performing idle breathing animation,
subtle chest rise and fall, seamless loop,
centered composition, solid color background
```

---

## Environment Variables

```bash
# Required
GOOGLE_API_KEY=your_api_key

# Optional - Model override
VEO_MODEL=veo-3.1-generate-preview
```

---

## Related Documentation

- `generate_video.py` - Implementation details
- `secret_guard.py` - Security module
- [Google Veo Documentation](https://cloud.google.com/vertex-ai/docs/generative-ai/video/overview)
