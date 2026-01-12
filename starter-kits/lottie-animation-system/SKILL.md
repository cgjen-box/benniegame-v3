# Lottie Animation System - Starter Kit

> **Format**: Lottie 5.7.4 JSON with embedded PNG frames
> **Purpose**: Create and validate production Lottie animations
> **Version**: Extracted from Bennie v1 (2025-12-30)

---

## Overview

This starter kit provides tools for creating and validating Lottie animations:

- **PNG-embedded format** - Self-contained JSON files
- **Micro-interaction templates** - Coin spin, sparkle, button press
- **Character loop templates** - Breathing, bouncing animations
- **Validation tools** - Quality assurance checks
- **Frame strip generator** - Visual inspection utility

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create Lottie from frames
python create_lottie.py --frames ./my_frames/*.png --output animation.json

# 3. Validate
python validate_lottie.py animation.json
```

---

## Lottie JSON Structure

### Core Format

```json
{
  "v": "5.7.4",              // Lottie version
  "fr": 30,                  // Frame rate (fps)
  "ip": 0,                   // In-point (start frame)
  "op": 60,                  // Out-point (end frame)
  "w": 100,                  // Canvas width
  "h": 100,                  // Canvas height
  "nm": "animation_name",    // Animation name
  "ddd": 0,                  // 3D flag (0 = 2D)
  "assets": [...],           // Embedded images
  "layers": [...]            // Animation layers
}
```

### Embedded Image Asset

```json
{
  "id": "frame_000",
  "w": 96,
  "h": 288,
  "e": 1,                    // 1 = embedded base64
  "u": "",
  "p": "data:image/png;base64,iVBORw0KGgo..."
}
```

### Image Layer

```json
{
  "ty": 2,                   // 2 = image layer
  "refId": "frame_000",      // References asset
  "ip": 0,                   // In-point
  "op": 2,                   // Out-point
  "ks": {                    // Transform keyframes
    "a": [48, 288, 0],       // Anchor point
    "p": [48, 288, 0],       // Position
    "s": [100, 100, 100],    // Scale
    "o": {"a": 0, "k": 100}  // Opacity
  }
}
```

### Shape Layer (for micro-interactions)

```json
{
  "ty": 4,                   // 4 = shape layer
  "shapes": [
    {
      "ty": "el",            // Ellipse
      "p": {"a": 0, "k": [50, 50]},  // Position
      "s": {"a": 1, "k": [...]}      // Animated size
    },
    {
      "ty": "fl",            // Fill
      "c": {"a": 0, "k": [0.85, 0.76, 0.48, 1]}  // Color (RGBA 0-1)
    }
  ],
  "ks": {...}                // Transform
}
```

---

## Key Properties Reference

### Layer Types (`ty`)

| Value | Type |
|-------|------|
| 0 | Precomp |
| 1 | Solid |
| 2 | Image |
| 3 | Null |
| 4 | Shape |
| 5 | Text |

### Shape Types (`ty`)

| Value | Type |
|-------|------|
| "el" | Ellipse |
| "rc" | Rectangle |
| "sr" | Star |
| "sh" | Path |
| "fl" | Fill |
| "st" | Stroke |
| "tr" | Transform |
| "gr" | Group |

### Animation Flags

| Property | Value | Meaning |
|----------|-------|---------|
| `a` | 0 | Static value |
| `a` | 1 | Animated keyframes |
| `e` | 1 | Embedded asset |

---

## Creating Animations

### From PNG Frames

```bash
python create_lottie.py \
    --frames ./frames/*.png \
    --output character_idle.json \
    --fps 30 \
    --frame-hold 2
```

### Animation Duration

```
Total Lottie frames = frame_count × frame_hold
Duration (seconds) = total_frames / fps

Example:
42 frames × 2 hold / 30 fps = 2.8 seconds
```

### Frame Hold Values

| frame_hold | ms/frame | Feel |
|------------|----------|------|
| 1 | 33ms | Fast, jerky |
| 2 | 67ms | Normal, smooth |
| 3 | 100ms | Slow, detailed |

---

## Templates

### Micro-Interaction: Coin Spin

```json
{
  "v": "5.7.4",
  "fr": 60,
  "ip": 0,
  "op": 60,
  "w": 100,
  "h": 100,
  "nm": "coin_spin",
  "layers": [
    {
      "ty": 4,
      "nm": "Coin",
      "shapes": [
        {
          "ty": "el",
          "p": {"a": 0, "k": [50, 50]},
          "s": {"a": 0, "k": [80, 80]}
        },
        {
          "ty": "fl",
          "c": {"a": 0, "k": [0.85, 0.76, 0.48, 1]}
        }
      ],
      "ks": {
        "r": {
          "a": 1,
          "k": [
            {"t": 0, "s": [0]},
            {"t": 60, "s": [360]}
          ]
        }
      }
    }
  ]
}
```

### Micro-Interaction: Button Press

```json
{
  "v": "5.7.4",
  "fr": 60,
  "ip": 0,
  "op": 10,
  "w": 100,
  "h": 100,
  "nm": "button_press",
  "layers": [
    {
      "ty": 4,
      "shapes": [...],
      "ks": {
        "s": {
          "a": 1,
          "k": [
            {"t": 0, "s": [100, 100]},
            {"t": 5, "s": [95, 95]},
            {"t": 10, "s": [100, 100]}
          ]
        }
      }
    }
  ]
}
```

### Character Loop: Breathing

For PNG-embedded character animations, use scale keyframes:

```json
{
  "ks": {
    "s": {
      "a": 1,
      "k": [
        {"t": 0, "s": [100, 100], "i": {"x": 0.4, "y": 0}, "o": {"x": 0.6, "y": 1}},
        {"t": 45, "s": [103, 103], "i": {"x": 0.4, "y": 0}, "o": {"x": 0.6, "y": 1}},
        {"t": 90, "s": [100, 100]}
      ]
    }
  }
}
```

---

## Validation

### Usage

```bash
# Validate single file
python validate_lottie.py animation.json

# Validate directory
python validate_lottie.py ./lottie_files/ --all

# Detailed output
python validate_lottie.py animation.json --verbose
```

### Checks Performed

- Valid JSON structure
- Required Lottie fields present (v, fr, ip, op, w, h)
- Frame rate and duration reasonable
- Canvas dimensions valid
- Assets embedded and decodable
- Frame size consistency
- Layer references valid

---

## Frame Strip Generator

Create horizontal strip showing all frames for visual inspection:

```bash
python generate_frame_strip.py animation.json --output strip.png
```

Shows all frames side-by-side for quality verification.

---

## File Structure

```
lottie-animation-system/
├── SKILL.md                    # This documentation
├── README.md                   # Quick start
├── requirements.txt            # Dependencies
│
├── create_lottie.py            # Lottie generator
├── validate_lottie.py          # Quality validation
├── generate_frame_strip.py     # Visual inspection
│
├── config/
│   └── lottie_specs.json       # Animation specifications
│
├── templates/
│   ├── micro_interaction.json  # UI effects template
│   └── character_loop.json     # Character animation template
│
└── examples/
    ├── coin_spin.json          # Working coin animation
    ├── success_burst.json      # Celebration effect
    └── button_press.json       # Button feedback
```

---

## Color Format

Colors in Lottie use RGBA with values 0-1:

```json
"c": {"a": 0, "k": [0.85, 0.76, 0.48, 1]}
```

### Converting from Hex

```python
def hex_to_lottie(hex_color):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255
    return [r, g, b, 1]

# Example: #D9C27A (Coin Gold)
# → [0.85, 0.76, 0.48, 1]
```

---

## Autism-Friendly Animation Guidelines

### Timing

| State | Duration | Scale | Feel |
|-------|----------|-------|------|
| idle | 3.0s | 5% | Calm breathing |
| happy | 2.0s | 8% | Gentle bounce |
| thinking | 4.0s | 3% | Very subtle |
| celebrating | 1.5s | 10-12% | Excited but controlled |

### Motion Rules

- No sudden movements
- No flashing or strobing
- Smooth ease-in/ease-out
- Seamless loops
- Reduce motion fallback support

---

## SwiftUI Integration

```swift
import Lottie

struct LottieView: UIViewRepresentable {
    let name: String
    var loopMode: LottieLoopMode = .loop

    func makeUIView(context: Context) -> LottieAnimationView {
        let view = LottieAnimationView(name: name)
        view.loopMode = loopMode
        view.play()
        return view
    }

    func updateUIView(_ uiView: LottieAnimationView, context: Context) {}
}

// Usage
LottieView(name: "coin_spin")
```

---

## File Sizes

Typical file sizes for PNG-embedded Lottie:

| Type | Frames | Size |
|------|--------|------|
| Micro-interaction | 10-30 | 5-15 KB |
| Character animation | 42 | 300-500 KB |
| Complex scene | 60+ | 500 KB - 1 MB |

---

## Related Documentation

- `create_lottie.py` - Full creation options
- `validate_lottie.py` - Validation details
- [Lottie Documentation](https://airbnb.io/lottie/)
