# Gemini Image Pro 3 - Quick Start

Generate character-consistent AI images using Google's Gemini 3.0 Pro Image Preview.

## Setup (5 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure API key
cp config/.env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 3. Verify setup
python generate_image.py --help
```

## Basic Usage

```bash
# Generate 4 variations
python generate_image.py generate "Friendly cartoon bear waving" --name bear-wave --count 4

# Output: ./generated/bear-wave_TIMESTAMP_v1.png through v4.png
```

## With Reference Image (Recommended)

```bash
# Use a reference to lock character identity
python generate_image.py generate "Same character celebrating" \
    --name bear-celebrate \
    --reference path/to/perfect_bear.png \
    --raw --count 4
```

## Training Mode (A/B Testing)

```bash
# Generate A/B variations for comparison
python generate_image.py generate "Happy bear" --name bear-happy --training
```

## Key Files

| File | Purpose |
|------|---------|
| `generate_image.py` | Main generation script |
| `reference_style.py` | Character specifications |
| `secret_guard.py` | Secure API key management |
| `LEARNINGS.md` | Pattern database |
| `SKILL.md` | Full documentation |

## Environment Variables

```bash
GOOGLE_API_KEY=your_gemini_api_key  # Required
ANTHROPIC_API_KEY=your_key          # Optional (auto-selection)
```

## See Also

- `SKILL.md` - Complete documentation
- `LEARNINGS.md` - Pattern database
- `examples/` - Usage examples
