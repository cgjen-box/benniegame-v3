# Bennie Brand Playbook - Condensed Reference

> **Use this for Claude Code. Full version: BENNIE_BRAND_PLAYBOOK_v3_1.md**

---

## 🎯 Project Overview

**Bennie und die Lemminge** - Autism-friendly educational iPad game for children ages 4-5.

- **Platform**: iPad (SwiftUI + SwiftData), iPadOS 17+
- **Language**: German only
- **Target**: Alexander (5, autism) & Oliver (4)

---

## ⛔ CRITICAL DESIGN RULES

```
╔════════════════════════════════════════════════════════════════════╗
║  🐻 BENNIE: Brown (#8C7259) • NO VEST • NO CLOTHING • EVER         ║
║  🔵 LEMMINGE: Blue (#6FA8DC) • NEVER GREEN • NEVER BROWN           ║
║  👆 TOUCH TARGETS: Minimum 96pt                                    ║
║  🚫 FORBIDDEN: Red, neon colors, flashing, shaking, "wrong"        ║
║  🇩🇪 LANGUAGE: German only, literal (no metaphors/idioms)          ║
╚════════════════════════════════════════════════════════════════════╝
```

---

## 🎨 Color Palette

### Safe Colors (USE THESE)
| Name | Hex | Usage |
|------|-----|-------|
| Woodland | #738F66 | Primary (sage green) |
| Bark | #8C7259 | Secondary (warm brown) |
| Sky | #B3D1E6 | Accents (pale blue) |
| Cream | #FAF5EB | Backgrounds |
| Success | #99BF8C | Positive feedback |
| CoinGold | #D9C27A | Coins/treasure |
| Lemminge Blue | #6FA8DC | Lemminge ONLY |

### 🚫 FORBIDDEN Colors
- Pure white (#FFFFFF) or black (#000000) for large areas
- Bright red (#FF0000)
- Any neon colors
- Saturation > 80%

### Wood UI Colors
| Element | Hex |
|---------|-----|
| Wood light | #C4A574 |
| Wood medium | #A67C52 |
| Wood dark | #6B4423 |
| Rope | #B8956B |

---

## 🐻 Character: Bennie der Bär

**Appearance**:
- Adult brown bear, pear-shaped body
- Chocolate brown fur: **#8C7259**
- Tan snout ONLY: **#C4A574** (NO belly patch!)
- **NEVER** wears clothing, vest, or accessories

**Expressions**: idle, happy, thinking, encouraging, celebrating, waving, pointing

**Role**: Patient teacher, asks child for help

---

## 🔵 Character: Die Lemminge

**CRITICAL**: Must be **BLUE (#6FA8DC)** - NEVER green, NEVER brown!

**Appearance**:
- Round blue potato-shaped blobs
- White belly with fuzzy edge
- Pink nose: #E8A0A0
- Buck teeth (2 visible)

**Expressions**: idle, curious, excited, celebrating, hiding, mischievous

**Role**: Create playful "problems" for child to solve

---

## 🌲 Super Forest Design

### Visual Style
- Magical, safe, warm forest world
- Warm golden light from upper-left (perpetual golden hour)
- 4-layer parallax backgrounds
- Hand-crafted wooden UI elements

### Wooden UI Elements
- Natural wood planks with visible grain
- Rope mounting on hanging signs
- 96pt+ touch targets
- Chains/locks for locked content

### Forest Layers
| Layer | Color |
|-------|-------|
| Far trees (misty) | #4A6B5C |
| Mid trees (sage) | #738F66 |
| Near foliage | #7A9973 |
| Tree bark | #8C7259 |
| Light rays | #F5E6C8 @ 30% |

---

## 📱 Screen Flow

```
App Launch
    ↓
Loading Screen (Bennie waving)
    ↓
Player Select (Alexander / Oliver)
    ↓
Home Screen (Waldabenteuer)
    ↓
┌─────────────────────────────────────┐
│  Activities:                        │
│  • Rätsel (Puzzles)                 │
│  • Zahlen (Numbers)                 │
│  • Logik (Logic)                    │
│  • Zeichnen (Drawing)               │
└─────────────────────────────────────┘
    ↓
Activity → Celebration → Coin Award
    ↓
Treasure Chest (YouTube redemption)
```

---

## 💰 Coin Economy

| Action | Coins |
|--------|-------|
| Complete activity | +1 |
| First-try bonus | +1 |
| Daily cap | 30 max |
| 5 min YouTube | -10 |
| 10 min YouTube | -20 |

---

## ♿ Accessibility Requirements

| Requirement | Value |
|-------------|-------|
| Touch targets | ≥ 96pt |
| Color contrast | 4.5:1 minimum |
| Animations | Reduce motion fallbacks |
| Text | German, literal language |
| Feedback | Positive only, never "wrong" |
| Audio | Independent volume channels |

---

## 🔊 Audio Rules

### Three Channels
- **Music**: 30% default, ducks to 15% during voice
- **Voice**: 100% (always priority)
- **Effects**: 70%

### Priority
1. Voice ALWAYS wins
2. Effects NEVER during voice
3. Music ducks during voice

---

## 📐 Screen Coordinates (iPad 1194×834)

| Element | Position |
|---------|----------|
| Alexander button | (400, 350) |
| Oliver button | (800, 350) |
| Rätsel | (300, 400) |
| Zahlen | (500, 400) |
| Logik | (700, 400) |
| Zeichnen | (900, 400) |
| Treasure | (1050, 700) |
| Back/Home | (60, 50) |
| Settings | (1134, 50) |

---

## ✅ Design QA Checklist

**For EVERY screen, verify:**

### Characters
- [ ] Bennie is brown (#8C7259)
- [ ] Bennie has NO clothing/vest/accessories
- [ ] Lemminge are BLUE (#6FA8DC)
- [ ] Lemminge are NOT green or brown

### UI
- [ ] Touch targets ≥ 96pt
- [ ] Wooden elements have grain texture
- [ ] Colors from approved palette only
- [ ] No red/neon colors

### Text
- [ ] German language only
- [ ] Literal language (no metaphors)
- [ ] Never says "wrong" or "falsch"
- [ ] Positive/encouraging tone

### Animation
- [ ] No flashing effects
- [ ] No shaking/jarring motion
- [ ] Reduce motion fallbacks exist

---

## 📁 Reference Files

```
design/references/
├── character/
│   ├── bennie/reference/bennie-reference.png    ← CANONICAL
│   └── lemminge/reference/lemminge-reference.png ← CANONICAL
├── screens/Reference_*.png
└── components/*.png
```

---

*For full specifications, see BENNIE_BRAND_PLAYBOOK_v3_1.md*
