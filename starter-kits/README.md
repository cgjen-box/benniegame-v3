# Bennie v3 - Technical Starter Kits

Complete technical implementation knowledge transfer from "Bennie and the Lemmings" project.

## Overview

This package contains 5 standalone starter kits with full working code, documentation, and security infrastructure.

| Kit | Purpose | Key Files |
|-----|---------|-----------|
| **gemini-image-pro-3** | AI image generation with character consistency | `generate_image.py`, `reference_style.py` |
| **veo-video-generation** | AI video generation (Veo 3.1) | `generate_video.py` |
| **ludo-animation-pipeline** | Keyframe → Lottie animation pipeline | `generate_keyframes.py`, `process.py` |
| **lottie-animation-system** | Lottie JSON creation and validation | `create_lottie.py` |
| **security-infrastructure** | 7-layer SecretGuard protection | `secret_guard.py`, git hooks |

## Quick Start

```bash
# 1. Choose a kit
cd starter-kits/gemini-image-pro-3

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp config/.env.example .env
# Edit .env with your API keys

# 4. Test it works
python generate_image.py --help
```

## Environment Variables

All kits use the same secure secret management. Create a `.env` file with:

```bash
# Required for image generation
GOOGLE_API_KEY=your_gemini_api_key
# or
GEMINI_API_KEY=your_gemini_api_key

# Required for voice (optional for most kits)
ELEVENLABS_API_KEY=your_elevenlabs_key

# Optional - enhanced features
ANTHROPIC_API_KEY=your_anthropic_key
REPLICATE_API_TOKEN=your_replicate_token
```

## Kit Details

### 1. Gemini Image Pro 3
**Purpose**: Generate character-consistent images using Google's Gemini 3.0 Pro Image Preview.

**Key Features**:
- Reference image technique (pass "perfect" image to lock character identity)
- A/B variation system with learnable patterns
- 40+ pattern scoring database (+3 to -3)
- Multi-backend fallback (Gemini → Imagen → Replicate)

**Usage**:
```bash
# Basic generation
python generate_image.py generate "Friendly bear waving" --name bear-wave --count 4

# With reference image (recommended)
python generate_image.py generate "Same character celebrating" \
    --name bear-celebrate \
    --reference path/to/reference.png \
    --raw --count 4

# Training mode (A/B comparison)
python generate_image.py generate "Happy bear" --name bear-happy --training
```

### 2. Veo 3.1 Video Generation
**Purpose**: Generate short video clips using Google's Veo 3.1 model.

**Key Features**:
- Duration: 4, 6, or 8 seconds
- Resolution: 720p or 1080p
- Aspect ratios: 16:9 or 9:16
- Reference image support (up to 3 images)

**Usage**:
```bash
python generate_video.py "Bear walking through forest" \
    --name bear-walk \
    --duration 6 \
    --resolution 1080p
```

### 3. Ludo.ai Animation Pipeline
**Purpose**: Generate sprite animations using Gemini keyframes + Ludo.ai interpolation.

**Pipeline**:
```
Gemini 3.0 (Keyframes) → Ludo.ai (Interpolation) → Lottie JSON
```

**Key Features**:
- 2 keyframes → 42 interpolated frames
- Chrome DevTools MCP browser automation
- Alpha-based grid detection
- PNG-embedded Lottie output

**Usage**:
```bash
# Generate keyframes
python generate_keyframes.py bennie waving

# Process downloaded ZIP to Lottie
python process.py

# Full pipeline
python pipeline.py bennie waving
```

### 4. Lottie Animation System
**Purpose**: Create and validate Lottie JSON animations.

**Key Features**:
- PNG-embedded frame format
- Micro-interaction templates
- Frame timing calculations
- Quality validation

**Usage**:
```bash
# Create Lottie from frames
python create_lottie.py --frames ./frames/*.png --output animation.json

# Validate existing Lottie
python validate_lottie.py animation.json
```

### 5. Security Infrastructure
**Purpose**: Protect secrets across all projects with 7-layer defense.

**Layers**:
1. **Code-Level**: SecretGuard Python module
2. **Pre-commit**: Git hook blocks secret commits
3. **Pre-push**: Secondary scan before push
4. **CI/CD**: GitHub Actions scanning
5. **IDE**: VS Code highlighting
6. **Documentation**: Usage guidelines
7. **Audit**: Periodic scanning script

**Setup**:
```bash
# Unix/Mac
./setup-security.sh

# Windows
.\setup-security.ps1
```

## Architecture

```
starter-kits/
├── README.md                    # This file
│
├── gemini-image-pro-3/          # Image generation
│   ├── SKILL.md                 # Full documentation
│   ├── generate_image.py        # Main script (~2300 lines)
│   ├── reference_style.py       # Character specs
│   ├── secret_guard.py          # Security module
│   └── LEARNINGS.md             # Pattern database
│
├── veo-video-generation/        # Video generation
│   ├── SKILL.md
│   ├── generate_video.py
│   └── secret_guard.py
│
├── ludo-animation-pipeline/     # Animation pipeline
│   ├── SKILL.md
│   ├── generate_keyframes.py
│   ├── ludo_automation.py
│   ├── process.py
│   ├── spritesheet_processor.py
│   └── pipeline.py
│
├── lottie-animation-system/     # Lottie tools
│   ├── SKILL.md
│   ├── create_lottie.py
│   └── validate_lottie.py
│
├── security-infrastructure/     # Security system
│   ├── SKILL.md
│   ├── secret_guard.py
│   ├── hooks/pre-commit
│   └── config/.gitleaks.toml
│
└── docs/                        # Reference docs
    ├── TECHNICAL_OVERVIEW.md
    ├── API_REFERENCE.md
    └── TROUBLESHOOTING.md
```

## Dependencies

Each kit has its own `requirements.txt`. Common dependencies:

```
google-genai>=0.4.0      # Gemini API
pillow>=10.0.0           # Image processing
python-dotenv>=1.0.0     # Environment variables
requests>=2.31.0         # HTTP client
anthropic>=0.18.0        # Claude API (optional)
```

## License

Internal use only. Knowledge transfer package for Bennie v3 project.

## Support

See individual SKILL.md files in each kit for detailed documentation and troubleshooting.
