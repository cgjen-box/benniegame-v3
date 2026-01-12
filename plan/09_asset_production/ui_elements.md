# UI Element Production

## Purpose

Complete specification for generating all UI elements, icons, and interactive components using Gemini Image Generation and design tools.

## 🎨 Wooden UI Design System

**Playbook Reference:** Part 1.3 (Color System - Wood UI), Part 4.0 (Shared Components)

### Design Philosophy
- Hand-crafted wooden aesthetic
- Natural textures and grain
- Rope mounting for hanging elements
- 96pt minimum touch targets
- Warm, tactile feeling

### Wood Color Palette

| Element | Hex | Usage |
|---------|-----|-------|
| Wood Light | #C4A574 | Highlights, top edges |
| Wood Medium | #A67C52 | Main plank color |
| Wood Dark | #6B4423 | Shadows, grain lines |
| Rope | #B8956B | Sign mounting ropes |
| Chain | #6B6B6B | Lock chains |

---

## Component Reference Mapping

**Component References:** `../../design/references/components/`

| Component | Reference File | Usage |
|-----------|---------------|-------|
| Activity buttons | activity_button_raetsel.png, activity_button_zahlen.png | Menu screen |
| Navigation | navigation_bar.png | All screens |
| Settings | settings_button.png | Top-right corner |
| Sound | sound_button.png | Top-right corner |
| Treasure | treasure_chest_closed.png, treasure_chest_open.png | Home & treasure screens |

---

## Button Components

### Core Button Specifications

```
CRITICAL RULES:
✅ Minimum 96pt touch target (entire button)
✅ Wooden plank aesthetic with visible grain
✅ Gradient: Wood Light (#C4A574) → Wood Medium (#A67C52)
✅ Dark outline: Wood Dark (#6B4423) 2px
✅ Rounded corners: 12pt radius
✅ Shadow: 4px offset, 30% opacity
❌ NO flat colors (must have gradient)
❌ NO sharp corners
❌ NO red or neon highlights
```

### 1. wood_button_small.png (96×60pt)

**Usage:** Secondary actions, cancel buttons
**Component Reference:** Similar to settings_button.png styling

**Prompt:**
```
Generate a small wooden button for a children's forest-themed game UI.

SPECIFICATIONS:
- Size: 96×60 points (192×120px @2x)
- Style: Wooden plank with visible grain texture
- Gradient: Light tan #C4A574 (top) to medium tan #A67C52 (bottom)
- Outline: Dark wood #6B4423, 2px stroke
- Corner radius: 12pt (rounded corners)
- Shadow: 4px offset down, dark wood shadow at 30% opacity
- Texture: Visible wood grain (horizontal direction)
- NO text or icons (separate layer)
- Transparent background

MOOD:
- Tactile, hand-crafted feeling
- Natural wood material
- Warm and inviting
- Slight 3D effect (not flat)

TECHNICAL:
- Resolution: 288×180px minimum (for @3x)
- Format: PNG with transparency
- Clean edges
```

**Expected Output:** 96×60pt (@2x = 192×120px, @3x = 288×180px)

---

### 2. wood_button_medium.png (120×72pt)

**Usage:** Primary actions, navigation
**Component Reference:** Based on navigation_bar.png button styling

**Prompt:**
```
[Same as wood_button_small.png but:]
- Size: 120×72 points (240×144px @2x)
- Slightly more prominent grain detail
```

---

### 3. wood_button_large.png (200×96pt)

**Usage:** Activity selection, major actions

**Prompt:**
```
[Same as wood_button_small.png but:]
- Size: 200×96 points (400×192px @2x)
- Plank proportions (longer, traditional sign shape)
- More visible grain and wood knots
```

---

## Activity Signs

### Core Sign Specifications

```
HANGING WOODEN SIGNS:
✅ Rope mounting at top (2 ropes)
✅ Natural wood plank shape
✅ Decorative leaves/vines on rope knots
✅ Icon in left/center area
✅ Text area in right/center
✅ Subtle swing angle variation (2-3°)
✅ Shadow below sign
```

### 4. sign_raetsel.png (280×180pt)

**Usage:** Rätsel activity button on menu
**Component Reference:** `activity_button_raetsel.png`

**Prompt:**
```
Generate a hanging wooden sign for "Rätsel" (puzzles) activity in a children's forest game.

SIGN STRUCTURE:
- Wooden plank: 280×180 points
- Hanging from branch with 2 ropes (rope color: #B8956B)
- Rope knots decorated with small green leaves
- Natural wood grain texture
- Gradient: #C4A574 (light top) to #A67C52 (medium bottom)
- Outline: #6B4423 dark wood, 3px
- Corner radius: 16pt
- Gentle swing (2° clockwise tilt)

ICON AREA (left side):
- Magnifying glass icon in #6B4423 (dark wood color)
- Simple, clear silhouette
- Positioned left-third of sign

TEXT AREA (right side):
- Large clear space for "Rätsel" text
- Text will be added separately
- Keep this area clean

DECORATIVE ELEMENTS:
- Small leaf clusters on rope knots (forest green #738F66)
- Tiny berries on leaves (red-orange #D9A679, NOT pure red)
- Subtle wood grain texture

LIGHTING:
- Warm golden light from upper-left
- Subtle shadow below sign (4px offset, 40% opacity)

TECHNICAL:
- Resolution: 840×540px minimum (for @3x)
- Transparent background
- PNG format
```

**Expected Output:** 280×180pt (@2x = 560×360px, @3x = 840×540px)

---

### 5. sign_zahlen.png (280×180pt)

**Usage:** Zahlen activity button on menu
**Component Reference:** `activity_button_zahlen.png`

**Prompt:**
```
[Same as sign_raetsel.png but:]

ICON AREA (left side):
- "123" numbers icon in #6B4423
- Bold, clear digits
- Stacked or side-by-side layout

[Rest identical to sign_raetsel.png]
```

---

### 6. sign_zeichnen_locked.png (280×180pt)

**Usage:** Locked Zeichnen activity (Phase 2)

**Prompt:**
```
[Same base as sign_raetsel.png but:]

LOCKED STATE MODIFICATIONS:
- Overall opacity: 60% (dimmed)
- X-pattern chains across sign (#6B6B6B dark gray chains)
- Padlock at center bottom (#6B6B6B)
- Icon area: Pencil icon (dimmed)
- Weathered, inactive appearance

CHAIN DETAIL:
- Two chains forming X pattern
- Link texture visible
- 4pt thickness
- Slightly drooping (weight feeling)

PADLOCK:
- Classic padlock silhouette
- 32×40pt size
- Positioned center-bottom
- Same dark gray as chains
```

---

### 7. sign_logik_locked.png (280×180pt)

**Usage:** Locked Logik activity (Phase 2)

**Prompt:**
```
[Same as sign_zeichnen_locked.png but:]

ICON AREA (left side):
- Puzzle piece icon (dimmed)
- Or gear icon for logic

[Rest identical to sign_zeichnen_locked.png]
```

---

## Progress & Reward Components

### 8. progress_bar_empty.png (600×40pt)

**Usage:** Progress bar container
**Component Reference:** Visible in all activity screen mockups

**Prompt:**
```
Generate an empty progress bar container for a children's forest game.

STRUCTURE:
- Wooden log/trough shape: 600×40 points
- Hollowed interior (dark wood: #6B4423)
- Raised edges (light wood: #C4A574)
- 10 visible coin slots evenly spaced
- Natural wood texture

COIN SLOTS:
- 10 circular indentations
- Each 32pt diameter
- Spaced evenly across bar
- Subtle depth shadow inside each slot

DECORATIVE:
- Small berry clusters on left end (#D9A679)
- Small berry clusters on right end
- Subtle moss detail at base (#5D6B4D)

LIGHTING:
- Top-lit (shows depth)
- Raised edges catch light

TECHNICAL:
- Resolution: 1800×120px minimum (@3x)
- Transparent background
```

---

### 9. progress_bar_fill.png (540×32pt)

**Usage:** Progress bar fill overlay

**Prompt:**
```
Generate a progress bar fill for a wooden coin collection bar.

STRUCTURE:
- Width: 540 points (9.5 slots filled effect)
- Height: 32 points (fits inside trough)
- Success green color: #99BF8C
- Gradient: Lighter top (#AED4A1) to darker bottom (#88AF7A)
- Soft glow around edges (subtle)

TEXTURE:
- Smooth, magical energy feeling
- Slight sparkle texture
- NOT wooden (this is magical progress)

EDGE TREATMENT:
- Rounded right edge (8pt radius)
- Straight left edge (starts at bar beginning)
- Smooth blend into slots

TECHNICAL:
- Resolution: 1620×96px minimum (@3x)
- Transparent background
- Designed to overlay on progress_bar_empty.png
```

---

### 10. coin_icon.png (32×32pt)

**Usage:** Coin counter, earned coin animations

**Prompt:**
```
Generate a gold coin icon for a children's forest game.

STRUCTURE:
- Circular gold coin: 32×32 points
- Coin gold color: #D9C27A
- Highlight on top edge: #F5E6C8
- Shadow on bottom edge: #B8956B
- Center: Subtle tree or leaf emblem

TEXTURE:
- Metallic shine (gradient)
- Slight sparkle at highlight point

VIEWING ANGLE:
- Slight 3/4 perspective (not flat)
- Shows depth/thickness of coin

TECHNICAL:
- Resolution: 96×96px minimum (@3x)
- Transparent background
```

---

### 11. coin_slot_empty.png (32×32pt)

**Usage:** Empty slots in progress bar

**Prompt:**
```
Generate an empty coin slot for a wooden progress bar.

STRUCTURE:
- Circular indentation: 32×32 points
- Dark wood interior: #6B4423
- Subtle shadow inside (shows depth)
- Fits into progress_bar_empty.png

TECHNICAL:
- Resolution: 96×96px (@3x)
- Transparent background (alpha channel for cutout effect)
```

---

### 12. coin_slot_filled.png (32×32pt)

**Usage:** Filled slots showing coins

**Prompt:**
```
Generate a filled coin slot with a gold coin inside.

STRUCTURE:
- Base: Same as coin_slot_empty.png
- Coin nested inside: Same as coin_icon.png but sized to fit
- Coin appears slightly recessed into slot

TECHNICAL:
- Resolution: 96×96px (@3x)
- Transparent background
- Combined asset (slot + coin)
```

---

### 13. chest_closed.png (120×120pt)

**Usage:** Home screen (not enough coins)
**Component Reference:** `treasure_chest_closed.png`

**Prompt:**
```
Generate a closed treasure chest for a children's forest game.

STRUCTURE:
- Wooden chest with metal bands
- Size: 120×120 points (square proportions)
- Wood color: Medium tan #A67C52
- Metal bands: Dark wood/iron #6B4423
- Padlock on front (gold: #D9C27A)
- Sits on ground (small shadow)

TEXTURE:
- Wood grain visible
- Metal bands have slight shine
- Padlock has metallic highlight

STATE:
- Closed, locked
- Dull appearance (no glow)
- Inactive/waiting state

VIEWING ANGLE:
- Front 3/4 view
- Slightly from above

TECHNICAL:
- Resolution: 360×360px (@3x)
- Transparent background
```

---

### 14. chest_open.png (120×140pt)

**Usage:** Home screen (can redeem coins), treasure screen
**Component Reference:** `treasure_chest_open.png`

**Prompt:**
```
[Same base as chest_closed.png but:]

STATE CHANGES:
- Lid open (tilted back ~45°)
- Golden glow emanating from inside
- Coins visible spilling out
- Active, inviting appearance

GLOW EFFECT:
- Warm golden light: #F5E6C8
- Radiating upward from chest
- Soft, magical quality
- NOT harsh or neon

COINS:
- 3-4 gold coins visible
- Some in chest, some spilling onto ground
- Coin color: #D9C27A

SPARKLES:
- Small sparkles around chest
- Gold/yellow colors only
- Subtle, not overwhelming

TECHNICAL:
- Height: 140 points (taller due to open lid)
- Resolution: 360×420px (@3x)
```

---

## Navigation Components

### 15. home_button.png (96×60pt)

**Usage:** Back to home navigation
**Component Reference:** Visible in navigation_bar.png

**Prompt:**
```
Generate a wooden home button for game navigation.

STRUCTURE:
- Wooden button base: 96×60 points
- Wood style: Same as wood_button_small.png
- Icon: House silhouette in dark wood #6B4423
- Centered on button

ICON DETAILS:
- Simple house shape (roof + walls)
- 32×32pt icon size
- Clear, recognizable silhouette

TECHNICAL:
- Resolution: 288×180px (@3x)
- Transparent background
```

---

### 16. settings_button.png (60×60pt)

**Usage:** Parent dashboard access
**Component Reference:** `settings_button.png`

**Prompt:**
```
Generate a wooden settings/gear button.

STRUCTURE:
- Circular wooden button: 60×60 points
- Wood gradient: #C4A574 to #A67C52
- Outline: #6B4423, 2px
- Icon: Gear/cog in #6B4423

ICON DETAILS:
- Gear with 8 teeth
- 40×40pt gear size
- Centered on button
- Simple, clear silhouette

TECHNICAL:
- Resolution: 180×180px (@3x)
- Transparent background
```

---

### 17. sound_button.png (60×60pt)

**Usage:** Volume toggle
**Component Reference:** `sound_button.png`

**Prompt:**
```
Generate a wooden sound/speaker button.

STRUCTURE:
- Circular wooden button: 60×60 points
- Wood style: Same as settings_button.png
- Icon: Speaker with sound waves in #6B4423

ICON DETAILS:
- Speaker cone facing right
- 2-3 sound waves emanating
- 40×40pt icon size

TECHNICAL:
- Resolution: 180×180px (@3x)
- Transparent background
```

---

## Lock & Chain Components

### 18. lock_chain.png (Overlay asset)

**Usage:** Locked activity signs

**Prompt:**
```
Generate crossed chains for locked content overlay.

STRUCTURE:
- Two chains forming X pattern
- Chain color: Dark gray #6B6B6B
- Each chain: 4pt thickness
- Link texture visible
- Length: Adjustable (280pt diagonal for signs)

TEXTURE:
- Metallic chain links
- Slight rust texture (aged)
- NOT shiny new chains

TECHNICAL:
- Resolution: Scalable vector style
- Transparent background
- Separate from padlock
```

---

### 19. padlock.png (32×40pt)

**Usage:** Lock icon for locked content

**Prompt:**
```
Generate a padlock icon for locked game content.

STRUCTURE:
- Classic padlock shape: 32×40 points
- Body: Dark gray #6B6B6B
- Shackle (top U-shape)
- Keyhole visible on body

TEXTURE:
- Metallic, slightly aged
- Not shiny new
- Functional appearance

TECHNICAL:
- Resolution: 96×120px (@3x)
- Transparent background
```

---

## Decorative Components

### 20. berry_cluster_left.png (40×40pt)

**Usage:** Progress bar decoration (left side)

**Prompt:**
```
Generate a small berry cluster decoration for forest UI.

STRUCTURE:
- Cluster of 3-4 berries: 40×40 points
- Berry color: Warm orange #D9A679 (NOT red)
- Small green leaves: #738F66
- Natural, organic arrangement

STYLE:
- Hand-painted look
- Soft edges
- Cute, decorative

TECHNICAL:
- Resolution: 120×120px (@3x)
- Transparent background
```

---

### 21. berry_cluster_right.png (40×40pt)

**Usage:** Progress bar decoration (right side)

**Prompt:**
```
[Mirror/variation of berry_cluster_left.png]
- Flipped or slightly different arrangement
- Same colors and style
```

---

### 22. rope_mount.png (60×100pt)

**Usage:** Sign hanging ropes

**Prompt:**
```
Generate a rope mounting system for hanging wooden signs.

STRUCTURE:
- Two rope strands: 60 points apart
- Each rope: 8pt thickness
- Length: 100 points visible
- Rope color: #B8956B (warm tan)
- Knot at top of each rope
- Small leaf decoration on knots

TEXTURE:
- Twisted rope fiber texture
- Natural hemp or vine appearance

LEAVES:
- 2-3 small leaves per knot
- Forest green #738F66
- Simple leaf shapes

TECHNICAL:
- Resolution: 180×300px (@3x)
- Transparent background
- Top edge has connection points for branch
```

---

## Generation Workflow

```bash
# For each UI element:

1. Copy prompt from above
2. Check component reference image (if available)
3. Generate in Gemini AI Studio
4. Compare to reference for consistency
5. Regenerate if style doesn't match
6. Export @2x and @3x versions
7. Test in Xcode with actual UI
8. Verify touch target size (minimum 96pt)
9. Save to Assets.xcassets/UI/
```

## Quality Assurance

**Universal UI Element Checklist:**
```
✓ Correct size specifications?
✓ Wooden aesthetic consistent?
✓ Colors from wood palette?
✓ Transparent background?
✓ High resolution (@3x ready)?
✓ Matches reference image style (if applicable)?
✓ Touch targets ≥ 96pt (for interactive elements)?
✓ NO red or neon colors?
✓ Visible grain/texture on wood?
✓ Appropriate shadow/depth?
✓ Clean edges (no artifacts)?
```

**Component-Specific Checks:**
- Buttons: Gradient top-to-bottom? Rounded corners?
- Signs: Rope mount visible? Decorative leaves?
- Locked signs: Chains form clear X? Padlock centered?
- Progress bar: 10 coin slots evenly spaced?
- Coins: Metallic shine visible? Tree emblem clear?
- Chest: Wood grain visible? Correct state (open/closed)?

## Touch Target Verification

**Critical:** All interactive elements must meet 96pt minimum:

```
INTERACTIVE ELEMENTS:
✓ wood_button_small: 96×60pt ✅
✓ wood_button_medium: 120×72pt ✅
✓ wood_button_large: 200×96pt ✅
✓ sign_raetsel: 280×180pt ✅
✓ sign_zahlen: 280×180pt ✅
✓ chest_closed: 120×120pt ✅
✓ chest_open: 120×140pt ✅
✓ home_button: 96×60pt ✅
✓ settings_button: 60×60pt ❌ → Make 96×96pt
✓ sound_button: 60×60pt ❌ → Make 96×96pt

ACTION: Increase settings and sound buttons to 96pt minimum!
```

## Testing in Context

After generating each UI element:

1. **Import to Xcode** at @2x and @3x
2. **Place in actual screen layout:**
   - Does it match the mockup?
   - Does it fit the space?
   - Is it clearly visible?
3. **Test interactivity:**
   - Can you easily tap it?
   - Does the size feel right?
   - Is the touch area clear?
4. **Test with characters:**
   - Do elements overlap characters appropriately?
   - Is visual hierarchy clear?
5. **Check against reference:**
   - Does it match the component reference image?
   - Is the style consistent?

## Component Consistency Rules

**Maintain consistency across all UI elements:**

1. **Wood Gradient:** Always light (#C4A574) at top, medium (#A67C52) at bottom
2. **Outlines:** Always dark wood (#6B4423), always 2-3px
3. **Corner Radius:** 12pt for buttons, 16pt for signs
4. **Shadows:** Always 4px offset, 30-40% opacity
5. **Icons:** Always dark wood (#6B4423) silhouettes
6. **Rope:** Always #B8956B warm tan
7. **Chains/Locks:** Always #6B6B6B dark gray

## Total Asset Count

- **Buttons:** 3 sizes × 3 resolutions = 9 files
- **Signs:** 4 signs × 3 resolutions = 12 files
- **Progress:** 5 components × 3 resolutions = 15 files
- **Navigation:** 3 buttons × 3 resolutions = 9 files
- **Locks:** 2 components × 3 resolutions = 6 files
- **Decorative:** 3 components × 3 resolutions = 9 files
- **Total:** 60 UI element files

## Delivery Format

```
Assets.xcassets/
└── UI/
    ├── Buttons/
    │   ├── wood_button_small.imageset/
    │   ├── wood_button_medium.imageset/
    │   └── wood_button_large.imageset/
    ├── Signs/
    │   ├── sign_raetsel.imageset/
    │   ├── sign_zahlen.imageset/
    │   ├── sign_zeichnen_locked.imageset/
    │   └── sign_logik_locked.imageset/
    ├── Progress/
    │   ├── progress_bar_empty.imageset/
    │   ├── progress_bar_fill.imageset/
    │   ├── coin_icon.imageset/
    │   ├── coin_slot_empty.imageset/
    │   └── coin_slot_filled.imageset/
    ├── Navigation/
    │   ├── home_button.imageset/
    │   ├── settings_button.imageset/
    │   └── sound_button.imageset/
    ├── Locks/
    │   ├── lock_chain.imageset/
    │   └── padlock.imageset/
    ├── Treasure/
    │   ├── chest_closed.imageset/
    │   └── chest_open.imageset/
    └── Decorative/
        ├── berry_cluster_left.imageset/
        ├── berry_cluster_right.imageset/
        └── rope_mount.imageset/
```

---

*Reference: PLAYBOOK Part 1.3 (Wood UI Colors), Part 4.0 (Shared Components)*
