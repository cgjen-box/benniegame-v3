# Ludo.ai Animation Pipeline - Quick Start

Generate production-ready Lottie animations using Gemini keyframes + Ludo.ai interpolation.

## Setup (5 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure API key
cp config/.env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 3. Verify setup
python generate_keyframes.py --help
```

## Basic Usage

```bash
# Step 1: Generate keyframes
python generate_keyframes.py bennie waving

# Step 2: Use MCP to run Ludo.ai automation
# (See SKILL.md for MCP workflow)

# Step 3: Save downloaded ZIPs to downloads/
mkdir -p downloads
# Move your bennie_waving.zip here

# Step 4: Process downloaded ZIP (auto-timing + QA)
python process.py
```

The processor automatically:
- Applies per-animation timing from `config/animation_specs.json`
- Runs QA validation and generates frame strips
- Copies Lottie files to BennieGame/Resources/Lottie/

## Pipeline Overview

```
Gemini 3.0 → Ludo.ai → Lottie JSON
(Keyframes)   (Interpolation)   (Output)
```

## Key Files

| File | Purpose |
|------|---------|
| `generate_keyframes.py` | Generate START/END frames |
| `ludo_automation.py` | MCP browser automation |
| `process.py` | ZIP → Lottie processor |
| `validate_lottie.py` | Quality validation |
| `SKILL.md` | Full documentation |

## Output

- 42 interpolated frames from 2 keyframes
- ~2.8 second animation at 30fps
- PNG-embedded Lottie JSON

## See Also

- `SKILL.md` - Complete documentation
- `config/keyframe_prompts.json` - Pose definitions
- `config/motion_hints.json` - Ludo.ai descriptions
