# Phase 9: Asset Production Pipeline

## Overview

This phase covers the complete asset production workflow for **Bennie und die Lemminge** using AI-powered generation tools. All assets must comply with the brand playbook specifications.

## 📚 Playbook References

This phase implements specifications from:

### Core Design Documentation
- **[PLAYBOOK_CONDENSED.md](../../docs/playbook/PLAYBOOK_CONDENSED.md)** - Quick reference for design rules
- **[FULL_ARCHIVE.md](../../docs/playbook/FULL_ARCHIVE.md)** - Complete specifications:
  - **Part 1** (Brand Identity) - Character designs, color system
  - **Part 4** (Screen Specifications) - All screen layouts and components
  - **Part 6** (Animation & Sound Guide) - Animation parameters
  - **Part 9** (Asset Production Pipeline) - This phase's detailed specs

### Design References
- **Screen Mockups:** `../../design/references/screens/`
  - Reference_Menu_Screen.png
  - Reference_Matching_Game_Screen.png
  - Reference_Numbers_Game_Screen.png
  - Reference_Layrinth_Game_Screen.png
  - Reference_Loading_Screen.png
  - Reference_Player_Selection_Screen.png
  - Reference_Treasure_Screen.png
  - Reference_Celebration_Overlay.png

- **Character References:** `../../design/references/character/`
  - bennie/ (canonical reference images to be created)
  - lemminge/ (canonical reference images to be created)

- **Component References:** `../../design/references/components/`
  - activity_button_raetsel.png
  - activity_button_zahlen.png
  - navigation_bar.png
  - settings_button.png
  - sound_button.png
  - treasure_chest_closed.png
  - treasure_chest_open.png

---

## 🎯 Critical Design Rules

```
╔════════════════════════════════════════════════════════════════════╗
║  🐻 BENNIE: Brown (#8C7259) • NO VEST • NO CLOTHING • EVER         ║
║  🔵 LEMMINGE: Blue (#6FA8DC) • NEVER GREEN • NEVER BROWN           ║
║  👆 TOUCH TARGETS: Minimum 96pt                                    ║
║  🚫 FORBIDDEN: Red, neon colors, flashing, shaking, "wrong"        ║
║  🇩🇪 LANGUAGE: German only, literal (no metaphors/idioms)          ║
╚════════════════════════════════════════════════════════════════════╝
```

**Reference:** PLAYBOOK_CONDENSED.md - "CRITICAL DESIGN RULES" section

---

## 📁 Production Guides

### 1. Character Images
**File:** [character_images.md](./character_images.md)

**Tool:** Gemini Image Generation (gemini-image-pro-preview)

**Outputs:**
- 6 Bennie poses (idle, waving, pointing, thinking, encouraging, celebrating)
- 6 Lemminge expressions (idle, curious, excited, celebrating, hiding, mischievous)
- Each @ 2x, @3x resolutions
- **Total:** 36 PNG files

**Playbook Reference:** Part 1.2 (Characters), Part 9.2 (Gemini Generation)

**Screen References Used:** All screens use these characters

---

### 2. Backgrounds
**File:** [backgrounds.md](./backgrounds.md)

**Tool:** Gemini Image Generation

**Outputs:**
- 8 screen backgrounds matching mockups
- Forest environment with parallax layers
- **Total:** 24 PNG files (8 screens × @2x, @3x)

**Playbook Reference:** Part 1.4 (Super Forest Design), Part 4 (Screen Specs)

**Screen References:**
| Background | Mockup Reference | Screen |
|------------|------------------|--------|
| forest_loading.png | Reference_Loading_Screen.png | Loading |
| forest_menu.png | Reference_Menu_Screen.png | Home/Menu |
| forest_activity.png | Reference_Matching_Game_Screen.png | All activities |
| forest_treasure.png | Reference_Treasure_Screen.png | Treasure |

---

### 3. UI Elements
**File:** [ui_elements.md](./ui_elements.md)

**Tool:** Gemini Image Generation + Figma

**Outputs:**
- Wooden buttons (all sizes)
- Progress bar components
- Coin icons
- Activity signs
- Lock/chain overlays
- **Total:** 60+ PNG files

**Playbook Reference:** Part 4.0 (Shared Components)

**Component References Used:** All files in `../../design/references/components/`

---

### 4. Animations
**File:** [animations.md](./animations.md)

**Tool:** Ludo.ai (character animation) + After Effects (effects)

**Outputs:**
- 6 Bennie animations (Lottie JSON)
- 6 Lemminge animations (Lottie JSON)
- 3 effect animations (confetti, coin_fly, progress_fill)
- **Total:** 15 JSON files

**Playbook Reference:** Part 6.2 (Character Animations), Part 9.3 (Ludo.ai Pipeline)

---

### 5. Voice Lines
**File:** [voice_lines.md](./voice_lines.md)

**Tool:** ElevenLabs TTS (German)

**Outputs:**
- 35+ Narrator lines
- 27+ Bennie lines
- All in German
- **Total:** 62 AAC files

**Playbook Reference:** Part 3 (Narrator & Voice Script), Part 9.4 (ElevenLabs)

---

## 🛠️ Production Tools

### Primary Tools
1. **Gemini Image Generation** (Google AI Studio)
   - All static images (characters, backgrounds, UI)
   - Access: https://aistudio.google.com/

2. **Ludo.ai** (Character Animation)
   - Character Lottie animations
   - Access: https://ludo.ai

3. **ElevenLabs** (Voice TTS)
   - German voice synthesis
   - Access: https://elevenlabs.io

### MCP Tool Support
- **bennie-image-generator** - Batch image generation with learnings
- **game-screen-designer** - Screen mockup generation
- **bennie-files** - File management

---

## ✅ Complete Asset Checklist

### Characters (12 images × 3 sizes = 36 files)
**Bennie (6 poses):**
- [ ] bennie_idle.png (@2x, @3x)
- [ ] bennie_waving.png (@2x, @3x)
- [ ] bennie_pointing.png (@2x, @3x)
- [ ] bennie_thinking.png (@2x, @3x)
- [ ] bennie_encouraging.png (@2x, @3x)
- [ ] bennie_celebrating.png (@2x, @3x)

**Lemminge (6 expressions):**
- [ ] lemminge_idle.png (@2x, @3x)
- [ ] lemminge_curious.png (@2x, @3x)
- [ ] lemminge_excited.png (@2x, @3x)
- [ ] lemminge_celebrating.png (@2x, @3x)
- [ ] lemminge_hiding.png (@2x, @3x)
- [ ] lemminge_mischievous.png (@2x, @3x)

### Backgrounds (8 screens × 3 sizes = 24 files)
- [ ] forest_loading.png (@2x, @3x)
- [ ] forest_menu.png (@2x, @3x)
- [ ] forest_activity.png (@2x, @3x)
- [ ] forest_treasure.png (@2x, @3x)
- [ ] forest_video_selection.png (@2x, @3x)
- [ ] forest_player_select.png (@2x, @3x)
- [ ] forest_celebration.png (@2x, @3x)
- [ ] forest_parent_dashboard.png (@2x, @3x)

### UI Elements (20+ components)
**Buttons:**
- [ ] wood_button_small.png (@2x, @3x)
- [ ] wood_button_medium.png (@2x, @3x)
- [ ] wood_button_large.png (@2x, @3x)

**Activity Signs:**
- [ ] sign_raetsel.png (@2x, @3x)
- [ ] sign_zahlen.png (@2x, @3x)
- [ ] sign_zeichnen_locked.png (@2x, @3x)
- [ ] sign_logik_locked.png (@2x, @3x)

**Progress & Rewards:**
- [ ] progress_bar_empty.png (@2x, @3x)
- [ ] progress_bar_fill.png (@2x, @3x)
- [ ] coin_icon.png (@2x, @3x)
- [ ] coin_slot_empty.png (@2x, @3x)
- [ ] coin_slot_filled.png (@2x, @3x)
- [ ] chest_closed.png (@2x, @3x)
- [ ] chest_open.png (@2x, @3x)

**Other:**
- [ ] lock_chain.png (@2x, @3x)
- [ ] berry_cluster_left.png (@2x, @3x)
- [ ] berry_cluster_right.png (@2x, @3x)
- [ ] rope_mount.png (@2x, @3x)

### Animations (15 Lottie JSON files)
**Bennie:**
- [ ] bennie_idle.json
- [ ] bennie_waving.json
- [ ] bennie_pointing.json
- [ ] bennie_thinking.json
- [ ] bennie_encouraging.json
- [ ] bennie_celebrating.json

**Lemminge:**
- [ ] lemminge_idle.json
- [ ] lemminge_curious.json
- [ ] lemminge_excited.json
- [ ] lemminge_celebrating.json
- [ ] lemminge_hiding.json
- [ ] lemminge_mischievous.json

**Effects:**
- [ ] confetti.json
- [ ] coin_fly.json
- [ ] progress_fill.json

### Voice Lines (62 AAC files)
**Narrator (35 files):**
- [ ] Loading: 1 file
- [ ] Player Selection: 3 files
- [ ] Home: 1 file
- [ ] Activities: 20 files
- [ ] Success Pool: 7 files
- [ ] Treasure: 2 files
- [ ] Video: 1 file

**Bennie (27 files):**
- [ ] Home: 5 files
- [ ] Activities: 10 files
- [ ] Celebrations: 4 files
- [ ] Treasure: 3 files
- [ ] Video: 2 files
- [ ] Hints: 3 files

---

## 📊 Export Specifications

### Image Export
| Asset Type | Format | Sizes | Notes |
|------------|--------|-------|-------|
| Characters | PNG | @2x, @3x | Transparent background |
| Backgrounds | PNG | @2x, @3x | Full bleed |
| UI Elements | PNG | @2x, @3x | 9-slice compatible |

### Resolution Table
| Asset | @1x | @2x | @3x |
|-------|-----|-----|-----|
| Bennie | 150×225pt | 300×450px | 450×675px |
| Lemminge | 40×50pt | 80×100px | 120×150px |
| Button | 48×30pt | 96×60px | 144×90px |
| Background | 1194×834pt | 2388×1668px | 3582×2502px |

### Animation Export
| Setting | Value |
|---------|-------|
| Format | Lottie JSON |
| FPS | 30 (idle) or 60 (effects) |
| File size | < 100KB |
| Compression | Enabled |

### Audio Export
| Setting | Value |
|---------|-------|
| Format | AAC |
| Sample rate | 44.1kHz |
| Bitrate | 128kbps (voice) |
| Channels | Stereo |

---

## 🔄 Production Workflow

```
┌────────────────────────────────────────────────────────────────────┐
│                    ASSET PRODUCTION WORKFLOW                       │
└────────────────────────────────────────────────────────────────────┘

Step 1: CHARACTER IMAGES
├─ Generate using Gemini (character_images.md)
├─ QA check against playbook
├─ Export @2x, @3x
└─ Save to Assets.xcassets/Characters/

Step 2: BACKGROUNDS
├─ Generate using Gemini (backgrounds.md)
├─ Match screen mockups
├─ Export @2x, @3x
└─ Save to Assets.xcassets/Backgrounds/

Step 3: UI ELEMENTS
├─ Generate using Gemini + Figma (ui_elements.md)
├─ Match component references
├─ Export @2x, @3x
└─ Save to Assets.xcassets/UI/

Step 4: ANIMATIONS
├─ Use character images as base
├─ Animate in Ludo.ai (animations.md)
├─ Export Lottie JSON
└─ Save to Resources/Lottie/

Step 5: VOICE LINES
├─ Generate in ElevenLabs (voice_lines.md)
├─ Convert to AAC
├─ Verify German pronunciation
└─ Save to Resources/Audio/

Step 6: QA & INTEGRATION
├─ Verify all assets against checklist
├─ Test in-app rendering
├─ Validate file sizes
└─ Update asset catalog
```

---

## 📈 Progress Tracking

| Category | Generated | QA Passed | Exported | Integrated | Complete |
|----------|-----------|-----------|----------|------------|----------|
| Characters | 0/12 | 0/12 | 0/12 | 0/12 | 0% |
| Backgrounds | 0/8 | 0/8 | 0/8 | 0/8 | 0% |
| UI Elements | 0/20 | 0/20 | 0/20 | 0/20 | 0% |
| Animations | 0/15 | 0/15 | 0/15 | 0/15 | 0% |
| Voice Lines | 0/62 | 0/62 | 0/62 | 0/62 | 0% |
| **TOTAL** | **0/117** | **0/117** | **0/117** | **0/117** | **0%** |

---

## 🚨 Common Issues & Solutions

### Issue: Bennie Generated with Vest
**Solution:** Regenerate with emphasis:
```
CRITICAL: NO vest, NO clothing, NO accessories of ANY kind.
Bennie is a natural bear - nothing on the body except fur.
```

### Issue: Lemminge Generated in Green/Brown
**Solution:** Regenerate with emphasis:
```
CRITICAL: Body color MUST be #6FA8DC (soft blue).
NEVER green (#738F66), NEVER brown (#8C7259).
The blue color is NON-NEGOTIABLE.
```

### Issue: Low Resolution Output
**Solution:** Add to prompt:
```
Generate at high resolution suitable for @3x Retina displays.
Minimum 1350×759 pixels for 16:9 assets.
```

### Issue: Voice Pronunciation Errors
**Solution:** Use SSML markup:
```xml
<speak>
  <phoneme alphabet="ipa" ph="ˈbenni">Bennie</phoneme>
  <break time="500ms"/>
  der <phoneme alphabet="ipa" ph="bɛːɐ̯">Bär</phoneme>
</speak>
```

---

## 📂 File Organization

```
Assets.xcassets/
├── Characters/
│   ├── Bennie/
│   │   ├── bennie_idle.imageset/
│   │   ├── bennie_waving.imageset/
│   │   └── ... (6 total)
│   └── Lemminge/
│       ├── lemminge_idle.imageset/
│       └── ... (6 total)
├── Backgrounds/
│   ├── forest_loading.imageset/
│   └── ... (8 total)
└── UI/
    ├── Buttons/
    ├── Signs/
    ├── Progress/
    └── Misc/

Resources/
├── Lottie/
│   ├── bennie_idle.json
│   ├── lemminge_celebrating.json
│   ├── confetti.json
│   └── ... (15 total)
└── Audio/
    ├── Narrator/
    │   ├── loading_complete.aac
    │   └── ... (35 total)
    └── Bennie/
        ├── greeting.aac
        └── ... (27 total)
```

---

## ✅ Phase Completion Criteria

Phase 9 is complete when:

- [ ] All 117 assets generated
- [ ] 100% QA pass rate (all design rules verified)
- [ ] All assets exported at required resolutions
- [ ] All assets integrated into Xcode project
- [ ] Asset catalog properly configured
- [ ] File sizes within target (<150MB total app size)
- [ ] Test app launch with all assets loaded
- [ ] No console warnings about missing assets

---

## 🔗 Related Documentation

- **Previous Phase:** [08_testing](../08_testing/) - Testing infrastructure
- **Next Phase:** [10_deployment](../10_deployment/) - App Store deployment
- **Design System:** [../../design/system/](../../design/system/) - Color, typography, spacing
- **Playbook:** [../../docs/playbook/](../../docs/playbook/) - Complete brand specifications

---

*Last Updated: January 2026*
*Phase Status: Not Started*
