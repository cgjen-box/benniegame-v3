# Lottie Animation System - Quick Start

Create and validate Lottie JSON animations with embedded PNG frames.

## Setup (5 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Verify setup
python create_lottie.py --help
```

## Basic Usage

```bash
# Create Lottie from frames
python create_lottie.py --frames ./frames/*.png --output animation.json

# Validate animation
python validate_lottie.py animation.json

# Generate visual frame strip
python generate_frame_strip.py animation.json --output strip.png
```

## Key Files

| File | Purpose |
|------|---------|
| `create_lottie.py` | Generate Lottie from frames |
| `validate_lottie.py` | Quality validation |
| `generate_frame_strip.py` | Visual inspection |
| `SKILL.md` | Full documentation |

## Templates

- `templates/micro_interaction.json` - UI effects (coin, button)
- `templates/character_loop.json` - Character breathing/idle

## See Also

- `SKILL.md` - Complete documentation with JSON format reference
- `examples/` - Working Lottie examples
