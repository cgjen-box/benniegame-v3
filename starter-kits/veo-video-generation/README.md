# Veo 3.1 Video Generation - Quick Start

Generate AI video clips using Google's Veo 3.1 model.

## Setup (5 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure API key
cp config/.env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 3. Verify setup
python generate_video.py --help
```

## Basic Usage

```bash
# Generate a 6-second video
python generate_video.py "Cartoon bear walking through forest" \
    --name bear-walk \
    --duration 6

# Output: ./generated/videos/bear-walk_TIMESTAMP.mp4
```

## With Reference Images

```bash
# Use references for character consistency
python generate_video.py "Same character dancing happily" \
    --name character-dance \
    --reference path/to/character.png \
    --duration 4
```

## Parameters

| Option | Values | Default |
|--------|--------|---------|
| `--duration` | 4, 6, 8 | 8 |
| `--resolution` | 720p, 1080p | 720p |
| `--aspect` | 16:9, 9:16 | 16:9 |

## Key Files

| File | Purpose |
|------|---------|
| `generate_video.py` | Main generation script |
| `secret_guard.py` | Secure API key management |
| `SKILL.md` | Full documentation |

## See Also

- `SKILL.md` - Complete documentation
- `examples/` - Usage examples
