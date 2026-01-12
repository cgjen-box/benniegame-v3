# Part 9: Asset Production Pipeline

> **Chapter 9** of the Bennie Brand Playbook
>
> Covers: AI tools workflow for creating game assets

---

## 9.1 Pipeline Overview

```
+-----------------------------------------------------------------------------+
|                        ASSET PRODUCTION PIPELINE                            |
+-----------------------------------------------------------------------------+
|                                                                             |
|  STATIC IMAGES (Characters, Backgrounds)                                    |
|      |                                                                      |
|      v                                                                      |
|  Gemini Image Generation --> Manual QA --> Export @2x/@3x PNG               |
|                                                                             |
|  ANIMATIONS (Character movements)                                           |
|      |                                                                      |
|      v                                                                      |
|  Static Image (Base pose) --> Ludo.ai Animation --> Lottie JSON Export     |
|                                                                             |
|  VIDEO CONTENT (Cutscenes, Intros)                                         |
|      |                                                                      |
|      v                                                                      |
|  Reference Images --> Veo 3.1 Generation --> Video Edit + Export           |
|                                                                             |
|  VOICE/AUDIO (Narrator, Bennie)                                            |
|      |                                                                      |
|      v                                                                      |
|  Script Text (German) --> ElevenLabs TTS --> AAC Export 44.1kHz/128kbps    |
|                                                                             |
+-----------------------------------------------------------------------------+
```

---

## 9.2 Gemini Image Generation

### Character Generation Template

```
Generate a [CHARACTER] in the [POSE] pose for a children's game.

CHARACTER SPECIFICATIONS:
- [List all specifications from Part 1.2]
- Style: Cel-shaded, bold outlines, flat colors
- Background: Transparent (for game asset)

POSE DETAILS:
- [Describe the specific pose]
- Expression: [Describe facial expression]
- Arms/Paws position: [Describe]

CRITICAL RULES:
- NO clothing or accessories
- Colors MUST be exact hex values specified
- Clean vector art style
- 16:9 aspect ratio
- High resolution for @3x export
```

### Quality Assurance Checklist

```
BENNIE:
[ ] No clothing/vest/accessories?
[ ] Fur color is #8C7259 brown?
[ ] ONLY snout is tan #C4A574?
[ ] No separate belly patch?
[ ] Pear-shaped body?
[ ] Adult bear (not cub, not teddy)?

LEMMINGE:
[ ] Body is BLUE #6FA8DC?
[ ] NOT green, NOT brown?
[ ] Cream belly with fuzzy edge?
[ ] Buck teeth visible?
[ ] Pink nose and paws?
[ ] Go gopher style (round blob shape)?

GENERAL:
[ ] Transparent background?
[ ] Cel-shaded style with bold outlines?
[ ] High resolution (suitable for @3x)?
[ ] Correct pose/expression?
```

---

## 9.3 Ludo.ai Animation Pipeline

### Workflow

```
Step 1: Upload Base Image
├── Upload the approved static PNG from Gemini
├── Select "Character Animation" mode
└── Define animation region (full character)

Step 2: Define Animation
├── Select animation type:
│   ├── Idle: Breathing, subtle sway
│   ├── Waving: Arm wave gesture
│   ├── Jumping: Vertical bounce
│   └── Custom: Define keyframes
├── Set duration (0.5-2s for loops)
└── Preview animation

Step 3: Refine
├── Adjust easing curves (use "Ease In Out" for organic feel)
├── Set loop behavior (loop for idle, play-once for actions)
└── Preview at 30fps

Step 4: Export
├── Export as Lottie JSON
├── Verify file size (< 100KB ideal)
└── Test in Lottie preview tool
```

### Animation Parameters

| Animation Type | Duration | Loop | Easing      |
| -------------- | -------- | ---- | ----------- |
| Idle breathing | 2.0s     | Yes  | Ease In Out |
| Waving         | 1.5s     | No   | Ease Out    |
| Pointing       | 0.5s     | No   | Ease Out    |
| Thinking       | 2.0s     | Yes  | Ease In Out |
| Celebrating    | 1.0s     | No   | Spring      |
| Hiding (peek)  | 1.5s     | Yes  | Ease In Out |

---

## 9.4 ElevenLabs Voice Generation

### Voice Selection Criteria

| Voice    | Characteristics             | Settings                    |
| -------- | --------------------------- | --------------------------- |
| Narrator | Clear, warm, neutral, adult | Stability: 0.75, Sim: 0.75  |
| Bennie   | Deeper, friendly, bear-like | Stability: 0.65, Sim: 0.80  |

### Generation Workflow

```
Step 1: Prepare Script
├── Copy German text from Part 3 script tables
├── Add SSML markup if needed for pronunciation
└── Note: Max 7 words per sentence

Step 2: Generate Audio
├── Paste text into ElevenLabs
├── Select appropriate voice (Narrator or Bennie)
├── Set speaking rate to 85% (-15% from default)
├── Generate audio
└── Preview and verify pronunciation

Step 3: Export & Process
├── Download as MP3
├── Convert to AAC:
│   ffmpeg -i input.mp3 -c:a aac -b:a 128k output.aac
├── Verify sample rate: 44.1kHz
└── Name file according to convention
```

### Audio File Naming Convention

```
{speaker}_{screen}_{trigger}.aac

Examples:
- narrator_loading_complete.aac
- narrator_player_select_question.aac
- bennie_home_greeting_part1.aac
- bennie_celebration_5coins.aac
```

---

## 9.5 Asset Export Specifications

### Image Export

| Asset Type  | Format   | Sizes    | Notes                  |
| ----------- | -------- | -------- | ---------------------- |
| Characters  | PNG      | @2x, @3x | Transparent background |
| Backgrounds | PNG/JPEG | @2x, @3x | Full bleed             |
| UI elements | PNG      | @2x, @3x | 9-slice compatible     |

### Resolution Table

| Size                 | @1x      | @2x       | @3x       |
| -------------------- | -------- | --------- | --------- |
| Character (Bennie)   | 150x225  | 300x450   | 450x675   |
| Character (Lemminge) | 40x50    | 80x100    | 120x150   |
| Button               | 48x30    | 96x60     | 144x90    |
| Background           | 1194x834 | 2388x1668 | 3582x2502 |

### Lottie Export

| Setting          | Value                     |
| ---------------- | ------------------------- |
| Format           | JSON                      |
| FPS              | 30 (idle) or 60 (effects) |
| File size target | < 100KB                   |
| Compression      | Enabled                   |

### Audio Export

| Setting     | Value                            |
| ----------- | -------------------------------- |
| Format      | AAC                              |
| Sample rate | 44.1kHz                          |
| Bitrate     | 128kbps (voice), 192kbps (music) |
| Channels    | Stereo                           |
