# Gemini Image Pro 3 - Starter Kit

> **API**: Google Gemini 3.0 Pro Image Preview
> **Purpose**: Generate character-consistent AI images with learnable patterns
> **Version**: Extracted from Bennie v1 (2025-12-30)

---

## Overview

This starter kit provides a complete image generation pipeline using Google's Gemini 3.0 Pro Image Preview model. It includes:

- **Reference image technique** for character consistency
- **A/B variation system** with pattern learning
- **Three-layer prompt structure** for quality control
- **Multi-backend fallback** (Gemini → Imagen → Replicate)
- **Training session management** with feedback tracking

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp config/.env.example .env
# Edit .env with your GOOGLE_API_KEY

# 3. Generate images
python generate_image.py generate "Friendly cartoon bear" --name test --count 4
```

---

## The Reference Image Breakthrough

**The Holy Grail of character consistency** - instead of relying solely on prompt engineering, pass a "perfect" reference image to lock character identity.

### How It Works

```python
# Reference images go FIRST in the API contents list, then the text prompt
contents = [
    PIL.Image.open("reference.png"),  # Reference images first (max 6)
    "Generate this character in a new pose"  # Prompt last
]

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=contents,
    config=types.GenerateContentConfig(response_modalities=['IMAGE'])
)
```

### Usage

```bash
# Generate with reference (RECOMMENDED for consistency)
python generate_image.py generate "Same character celebrating with arms raised" \
    --name character-celebrating \
    --reference "path/to/perfect_reference.png" \
    --raw --count 4
```

### Results

- Character identity maintained from reference
- Proportions, colors, style preserved
- Works with pose variations, expressions, scenes
- Maximum 6 reference images per generation

---

## API Reference

### Models Supported

| Model ID | Type | Max References |
|----------|------|----------------|
| `gemini-3-pro-image-preview` | Primary | 6 |
| `gemini-2.5-flash-image` | Fallback | 3 |
| `imagen-4.0-generate-001` | Fallback | 0 (text only) |

### Environment Variables

```bash
# Required (one of these)
GOOGLE_API_KEY=your_key
GEMINI_API_KEY=your_key

# Optional
ANTHROPIC_API_KEY=your_key      # For auto-selection
REPLICATE_API_TOKEN=your_key    # Fallback backend
GEMINI_MODEL=model_override     # Override default model
```

---

## CLI Reference

### Generate Command

```bash
python generate_image.py generate PROMPT [OPTIONS]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--name, -n` | Output filename base (required) | - |
| `--count` | Number of variations | 4 |
| `--reference, -r` | Reference image(s) for consistency | None |
| `--raw` | Use prompt as-is (skip enhancement) | False |
| `--character` | Add character spec (`bennie`, `lemminge`) | None |
| `--category, -c` | Output category folder | - |
| `--aspect, -a` | Aspect ratio | 16:9 |
| `--training, -t` | A/B comparison mode | False |
| `--output-json, -j` | JSON output format | False |

### Session Commands

```bash
# Start training session
python generate_image.py session start --name my-session --character bennie

# List sessions
python generate_image.py session list --status active

# Continue session
python generate_image.py session continue SESSION_ID

# Complete session
python generate_image.py session complete SESSION_ID --notes "learnings here"
```

### Feedback Commands

```bash
# Record feedback on A/B comparison
python generate_image.py feedback SESSION_ID ROUND_ID {A|B|NEITHER|BOTH} \
    --notes "feedback notes" \
    --confirm "pattern1" "pattern2" \
    --reject "pattern3"

# Generate report
python generate_image.py report --session SESSION_ID --output json
```

---

## Three-Layer Prompt Structure

Every generation uses a three-layer prompt enhancement:

```
Layer 1: Reference Style Prefix
├── Global style requirements
├── Character-specific specs (if --character used)
└── Global exclusions (negatives)

Layer 2: User's Base Prompt
└── Your actual generation request

Layer 3: Anchor Constraints
├── Proportion anchoring (prevents drift to chibi/cute)
└── Learned patterns from LEARNINGS.md
```

### Skip Enhancement (Raw Mode)

Use `--raw` to bypass all enhancement and use your prompt exactly:

```bash
python generate_image.py generate "exact prompt here --no negatives" --name output --raw
```

---

## Pattern Learning System

### Scoring System

| Score | Meaning | Application |
|-------|---------|-------------|
| +3 | Strong Positive | Always include in prompts |
| +1 | Positive | Include when relevant |
| 0 | Neutral | Test and evaluate |
| -1 | Negative | Avoid unless specified |
| -3 | Strong Negative | Never include |

### Pattern Evolution

```python
PROMOTION_THRESHOLD = 5   # Positive votes to promote (+2 score)
DEMOTION_THRESHOLD = 3    # Negative votes to demote (-2 score)
MIN_APPEARANCES = 3       # Required before evolution possible
```

Patterns automatically evolve based on feedback:
- Consistent positive feedback promotes patterns toward +3
- Consistent negative feedback demotes patterns toward -3

### Managing Patterns

Patterns are stored in `LEARNINGS.md`. To add new patterns:

1. Add to appropriate section (Strong Positive, Positive, etc.)
2. Include source and date
3. Patterns with +3 are automatically included in all prompts

---

## A/B Variation Testing

Training mode generates two variations for comparison:

```bash
python generate_image.py generate "Happy bear" --name bear-happy --training
```

**Option A**: Base prompt with learned enhancements
**Option B**: Same + color temperature adjustments

### Key Discovery

> **Shape modifiers cause drift!** Using "softer edges" caused unwanted proportion drift to cute/chibi styles. Only color temperature changes are safe for Option B.

---

## Character Specifications

### Defining Characters

Characters are defined in `reference_style.py`:

```python
BENNIE_STYLE = """
CORE SUBJECT & APPEARANCE:
- Subject: Large ADULT brown bear (NOT chibi)
- Physique: Pear-shaped body, prominent round belly
...
"""

BENNIE_NEGATIVES = """
NEVER include:
- Chibi/kawaii proportions
- Large eyes
- Cream belly patch
...
"""
```

### Using Character Specs

```bash
# Add character specification to prompt
python generate_image.py generate "Bear waving hello" --name wave --character bennie
```

---

## Retry Logic

Built-in exponential backoff for API reliability:

```python
@retry_with_backoff(
    max_retries=3,
    base_delay=2.0,
    max_delay=60.0
)
def _call_gemini_api(...):
    # Retries on: rate limits (429), server errors (5xx), timeouts
```

Retry delays: 2s → 4s → 8s (capped at 60s)

---

## Image Validation

All generated images are validated:

```python
def validate_image(image_data: bytes) -> Tuple[bool, str]:
    # Checks:
    # - Non-empty data
    # - Minimum file size (1KB)
    # - Can open with PIL
    # - Minimum dimensions (100x100)
    # - Valid image mode (RGB, RGBA, L, P)
```

---

## File Structure

```
gemini-image-pro-3/
├── SKILL.md                    # This documentation
├── README.md                   # Quick start guide
├── requirements.txt            # Python dependencies
├── generate_image.py           # Main generation script
├── reference_style.py          # Character specifications
├── secret_guard.py             # Secure API key management
├── LEARNINGS.md                # Pattern database
├── config/
│   ├── .env.example            # Environment template
│   └── character_specs.json    # Character definitions
└── examples/
    ├── generate_with_reference.py
    ├── training_session.py
    └── batch_generation.py
```

---

## Troubleshooting

### Issue: Multiple characters appearing
**Fix**: Add to negatives: `multiple characters, two characters, group`
Add to prompt: `ONE character only centered in frame`

### Issue: Character drifting from reference
**Fix**: Use `--reference` flag with approved image

### Issue: Limbs look like stamps/flat
**Fix**: Add to negatives: `stamps, flat paws, 2D limbs`
Add to prompt: `ARMS extending outward as separate 3D shapes`

### Issue: Too glossy/shiny
**Fix**: Add to negatives: `glossy, shiny, plastic, wet, reflective, chrome, metallic`

### Issue: Text appearing in image
**Fix**: Remove triggering words like "FLUFFY" from prompt
Add to negatives: `text, words, letters, watermark, logo`

### Issue: Rate limit errors
**Fix**: Built-in retry handles this. If persistent, reduce `--count` or add delays.

### Issue: API key not found
**Fix**: Ensure `.env` file exists with `GOOGLE_API_KEY` or `GEMINI_API_KEY`

---

## Best Practices

1. **Always use reference images** for character consistency
2. **Start with `--raw`** to understand base model output
3. **Build learnings incrementally** through training sessions
4. **Keep negatives comprehensive** - be explicit about what to avoid
5. **Use character specs** for known characters
6. **Review outputs** before approving to learnings
7. **Maintain frozen references** for each character

---

## API Limits

| Model | Max References | Notes |
|-------|----------------|-------|
| gemini-3-pro-image-preview | 6 object, 5 human | Primary model |
| gemini-2.5-flash-image | 3 high-fidelity | Fallback |
| imagen-4.0 | 0 | Text-only generation |

---

## Related Documentation

- `LEARNINGS.md` - Full pattern database
- `reference_style.py` - Character specifications
- `secret_guard.py` - Security module documentation
