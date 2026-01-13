# Bennie Game Asset Scripts

Scripts for generating and processing game assets.

## Quick Setup

```bash
# From project root
cd /Users/user289321/BennieGame-v3

# Activate virtual environment
source .venv/bin/activate

# Set your ElevenLabs API key
export ELEVENLABS_API_KEY='your-api-key-here'
```

## Scripts

### 1. Character Image Processor
Removes backgrounds and exports character images at @2x/@3x sizes.

```bash
python scripts/process_character_images.py
```

**Output:** `design/processed/Characters/`

### 2. Voice Line Generator
Generates all 69 voice lines using ElevenLabs API.

```bash
# First, list available voices to choose narrator and Bennie voices
python scripts/generate_voice_lines.py --list-voices

# Set voice IDs (choose German voices from the list)
export NARRATOR_VOICE_ID='voice-id-for-narrator'
export BENNIE_VOICE_ID='voice-id-for-bennie'

# Generate all voice lines
python scripts/generate_voice_lines.py

# Or generate specific categories
python scripts/generate_voice_lines.py --narrator-only
python scripts/generate_voice_lines.py --bennie-only
python scripts/generate_voice_lines.py --success-only
```

**Output:** `BennieGame/BennieGame/Resources/Audio/Voice/`

## Voice Line Summary

| Category | Count | Description |
|----------|-------|-------------|
| Narrator | 25 | Instructions, prompts, transitions |
| Bennie | 37 | Character dialogue, hints, celebrations |
| Success | 7 | Random success phrases |
| **Total** | **69** | |

## Recommended ElevenLabs Voices

For German voices, look for:
- **Narrator:** Warm, clear, neutral adult voice
- **Bennie:** Warm, friendly, slightly deeper voice

Settings per playbook:
- Speaking rate: 85% of normal (achieved via stability/similarity settings)
- Model: `eleven_multilingual_v2` (best for German)

## Playbook Compliance

All voice lines adhere to playbook rules:
- Max 7 words per sentence
- German language only
- Positive framing (never "Falsch" or "wrong")
- Literal language (no metaphors)
