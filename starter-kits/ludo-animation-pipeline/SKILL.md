# Ludo.ai Animation Pipeline - Starter Kit

> **Pipeline**: Gemini 3.0 Keyframes → Ludo.ai Interpolation → Lottie JSON
> **Purpose**: Generate production-ready sprite animations
> **Version**: Extracted from Bennie v1 (2025-12-30)

---

## Overview

This starter kit provides a fully automated animation pipeline that generates production-ready Lottie animations:

1. **Gemini 3.0 Pro** - Character-consistent keyframe generation
2. **Ludo.ai** - AI-powered frame interpolation (2 → 42 frames)
3. **Chrome DevTools MCP** - Browser automation for Ludo.ai
4. **Spritesheet Processor** - Automatic Lottie conversion

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp config/.env.example .env
# Edit .env with your GOOGLE_API_KEY

# 3. Generate keyframes
python generate_keyframes.py mycharacter waving

# 4. Process downloaded ZIP (after Ludo.ai generation)
python process.py
```

---

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    LUDO.AI PIPELINE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PHASE 1: KEYFRAME GENERATION (Gemini 3.0)                     │
│  ─────────────────────────────────────────                     │
│  Input:  Character reference image + pose descriptions         │
│  Output: START frame + END frame (PNG)                         │
│  File:   generate_keyframes.py                                 │
│                                                                  │
│  ↓                                                               │
│                                                                  │
│  PHASE 2: BROWSER AUTOMATION (Chrome DevTools MCP)             │
│  ──────────────────────────────────────────────                │
│  Input:  START & END keyframes                                  │
│  Output: Ludo.ai spritesheet ZIP                               │
│  File:   ludo_automation.py                                    │
│                                                                  │
│  ↓                                                               │
│                                                                  │
│  PHASE 3: PROCESSING (Spritesheet → Lottie)                    │
│  ────────────────────────────────────────────                  │
│  Input:  ZIP with spritesheet PNG                              │
│  Output: Lottie JSON with embedded frames                       │
│  File:   spritesheet_processor.py                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Keyframe Generation

### Usage

```bash
# Generate keyframes for a character emotion
python generate_keyframes.py CHARACTER EMOTION

# Examples
python generate_keyframes.py bennie waving
python generate_keyframes.py lemminge excited

# Generate all emotions
python generate_keyframes.py bennie --all

# List available emotions
python generate_keyframes.py bennie --list
```

### Output

```
keyframes/
└── bennie_waving/
    ├── bennie_waving_start_TIMESTAMP_v1.png   # Initial pose
    ├── bennie_waving_end_TIMESTAMP_v1.png     # Peak pose
    ├── bennie_waving_prompt_log.txt           # Generation prompts
    └── keyframe_metadata.json                  # Metadata
```

### Character Emotions

**Bennie (7 emotions)**:
- idle, happy, thinking, encouraging, celebrating, waving, pointing

**Lemminge (6 emotions)**:
- idle, curious, excited, celebrating, hiding, mischievous

---

## Phase 2: Browser Automation

### Prerequisites

1. Chrome with Ludo.ai logged in
2. Chrome DevTools MCP connected

### MCP Tool Sequence

```python
# 1. Navigate to Ludo.ai
mcp__chrome-devtools__navigate_page(url="https://ludo.ai/sprite-generator")

# 2. Switch to Animate tab (requires JavaScript)
mcp__chrome-devtools__evaluate_script(function="() => {
  const tabs = document.querySelectorAll('[role=\"tab\"]');
  for (const tab of tabs) {
    if (tab.textContent.includes('Animate')) {
      tab.click();
      return 'Clicked';
    }
  }
}")

# 3. Upload START keyframe
mcp__chrome-devtools__upload_file(uid="...", filePath="keyframe_start.png")

# 4. Upload END keyframe
mcp__chrome-devtools__upload_file(uid="...", filePath="keyframe_end.png")

# 5. Fill description
mcp__chrome-devtools__fill(uid="...", value="gentle waving motion")

# 6. Click Animate (5 credits)
mcp__chrome-devtools__click(uid="...")

# 7. Wait for completion
mcp__chrome-devtools__wait_for(text="Download", timeout=180000)

# 8. Export and download ZIP
```

### Motion Hints

| Character | Emotion | Motion Hint |
|-----------|---------|-------------|
| bennie | idle | gentle breathing cycle, calm rhythmic motion |
| bennie | happy | gentle bounce up and down with cheerful rhythm |
| bennie | waving | hand waving side to side in friendly greeting |
| lemminge | excited | bouncing up and down rapidly, energetic jumping |
| lemminge | hiding | shrinking down motion, nervous shaking |

---

## Phase 3: Processing

### Downloads Folder

Place downloaded Ludo.ai ZIPs in the `downloads/` folder:

```
ludo-animation-pipeline/
└── downloads/
    ├── bennie_waving.zip
    ├── lemminge_excited.zip
    └── ...
```

### Usage

```bash
# Process all new ZIPs from downloads/
python process.py

# Show status only
python process.py --status

# Custom FPS
python process.py --fps 24

# Force grid dimensions
python process.py --grid 7x6

# Reprocess all
python process.py --reprocess
```

### Per-Animation Timing

The processor automatically uses per-animation timing from `config/animation_specs.json`:

| Character | Animation | Target Duration |
|-----------|-----------|-----------------|
| bennie | idle | 2.0s |
| bennie | happy | 1.4s |
| bennie | waving | 1.4s |
| lemminge | idle | 1.0s |
| lemminge | excited | 0.6s |
| lemminge | curious | 0.8s |

Timing is calculated as: `frame_hold = round(target_seconds * fps / frame_count)`

### QA Gate

After processing, the pipeline automatically runs:

1. **Lottie validation** - Structure, assets, timing
2. **Frame strip generation** - Visual inspection PNG
3. **Duration check** - Must be 0.5s - 3.0s

QA issues are printed to console but do not block output.

### Grid Detection

The spritesheet processor auto-detects grid dimensions using alpha-based gap detection:

1. Sum alpha values per row/column
2. Identify near-transparent separators (gaps)
3. Count gaps to determine grid size
4. Fallback to common sizes if detection fails

### Output

```
output/
├── bennie_waving.json           # Final Lottie
├── bennie_waving.strip.png      # QA frame strip
├── bennie_waving_frames/        # Extracted frames
│   ├── frame_000.png
│   ├── frame_001.png
│   └── ...
└── animation_status.json        # Progress tracking
```

---

## Lottie JSON Format

### Structure

```json
{
  "v": "5.7.4",
  "fr": 30,
  "ip": 0,
  "op": 84,
  "w": 96,
  "h": 288,
  "nm": "bennie_waving",
  "assets": [
    {
      "id": "frame_000",
      "w": 96,
      "h": 288,
      "e": 1,
      "p": "data:image/png;base64,..."
    }
  ],
  "layers": [
    {
      "ty": 2,
      "refId": "frame_000",
      "ip": 0,
      "op": 2,
      "ks": {...}
    }
  ]
}
```

### Key Properties

| Property | Value | Purpose |
|----------|-------|---------|
| `v` | "5.7.4" | Lottie version |
| `fr` | 30 | Frame rate |
| `e` | 1 | Embedded base64 image |
| `ty` | 2 | Image layer type |
| `ip/op` | int | In/out points |

---

## File Structure

```
ludo-animation-pipeline/
├── SKILL.md                    # This documentation
├── README.md                   # Quick start
├── requirements.txt            # Dependencies
│
├── generate_keyframes.py       # Phase 1: Gemini keyframes
├── ludo_automation.py          # Phase 2: MCP scripts
├── process.py                  # Phase 3: Quick processor
├── spritesheet_processor.py    # Grid detection + Lottie
├── pipeline.py                 # Full orchestration
├── validate_lottie.py          # Quality checks
├── generate_frame_strip.py     # Visual inspection
├── secret_guard.py             # Security module
│
├── config/
│   ├── .env.example
│   ├── keyframe_prompts.json
│   └── motion_hints.json
│
├── templates/
│   └── lottie_base.json
│
└── examples/
    ├── single_animation.py
    ├── batch_pipeline.py
    └── mcp_workflow.md
```

---

## Credits Usage

### Ludo.ai Pricing

| Plan | Cost | Credits/Month |
|------|------|---------------|
| Free | $0 | 50 |
| Starter | $15 | 250 |
| Pro | $35 | 1,000 |

### Per Animation

| Action | Credits |
|--------|---------|
| Single animation | 5 |
| All 13 animations | ~65 |
| With retries | ~100 |

---

## Troubleshooting

### Tab Not Switching
Use `evaluate_script` with JavaScript instead of direct click.

### Upload Not Working
1. Take fresh snapshot (UIDs change on reload)
2. Click "Choose Image" button first
3. Use correct UID in `upload_file`

### Generation Stuck
1. Take screenshot to check progress
2. Wait additional 60 seconds
3. If error, reload and retry

### Wrong Grid Detected
Override with: `python process.py --grid 7x6`

### Element UID Not Found
Always take fresh snapshot before interacting.

---

## Quality Standards

### Autism-Friendly Animation
- Motion must be gentle, not jarring
- No fast or sudden movements
- No flashing or strobing
- 2-4 second loop duration
- Celebrating animations controlled

### Technical Requirements
- Transparent background
- Character matches reference
- Smooth frame transitions
- Seamless loop

---

## Environment Variables

```bash
# Required
GOOGLE_API_KEY=your_api_key

# Ludo.ai credentials (stored in .env)
LUDO_USER=your_email
LUDO_PASS=your_password
```

---

## Related Documentation

- `LUDO_WORKFLOW.md` - Detailed workflow
- `validate_lottie.py` - Quality checks
- `spritesheet_processor.py` - Grid detection algorithm
