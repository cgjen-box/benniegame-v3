# Background Image Production

## Purpose

Complete specification for generating all screen backgrounds using Gemini Image Generation, matching the reference mockups.

## 🎨 Super Forest Design System

**Playbook Reference:** Part 1.4 (Super Forest Design), Part 4 (Screen Specifications)

### Visual Style
- Magical, safe, warm forest world
- Warm golden light from upper-left (perpetual golden hour)
- 4-layer parallax backgrounds
- Soft, muted colors (no harsh contrasts)

### Forest Color Palette

| Layer | Hex | Usage |
|-------|-----|-------|
| Far trees (misty) | #4A6B5C | Distant background |
| Mid trees (sage) | #738F66 | Main canopy |
| Near foliage | #7A9973 | Foreground bushes |
| Tree bark | #8C7259 | Tree trunks |
| Light rays | #F5E6C8 @ 30% | Golden sunbeams |
| Moss | #5D6B4D | Ground covering |
| Path stone | #A8A090 | Paths/clearings |

### Lighting Rules
- **Direction:** Upper-left (45° angle)
- **Quality:** Soft, diffused, warm
- **Color temperature:** Golden hour (5000K-6000K)
- **NO harsh shadows:** Everything is gentle
- **NO bright spots:** No overstimulation

---

## Background Specifications

### Core Requirements (ALL BACKGROUNDS)

```
CRITICAL RULES:
✅ 4-layer parallax (far, mid, near, foreground)
✅ Warm golden lighting from upper-left
✅ Forest color palette (muted sage greens, browns)
✅ Soft edges, no harsh contrasts
✅ Safe, welcoming atmosphere
✅ 16:9 aspect ratio (1194×834pt base)
❌ NO red colors
❌ NO bright/neon colors
❌ NO harsh shadows or bright spots
❌ NO scary elements (dark caves, dead trees)
```

---

## 1. forest_loading.png

**Screen:** Loading Screen
**Reference Mockup:** `../../design/references/screens/Reference_Loading_Screen.png`

**Prompt:**
```
Generate a magical forest background for a children's game loading screen.

SCENE COMPOSITION:
- 4-layer parallax forest scene
- Warm golden hour lighting from upper-left
- Gentle forest clearing with scattered tree holes (for Lemminge to peek from)
- Soft grass floor with scattered flowers (pink, purple, yellow)
- Tree trunks visible on sides (natural frame)
- Misty background trees fading into soft green haze
- Warm, welcoming, safe atmosphere

COLOR PALETTE:
- Background trees: #4A6B5C (misty sage)
- Mid canopy: #738F66 (sage green)
- Near foliage: #7A9973 (warm green)
- Tree bark: #8C7259 (warm brown)
- Light rays: #F5E6C8 at 30% opacity
- Ground moss: #5D6B4D
- Flowers: soft pink, purple, yellow (no red)
- Sky glimpses: #B3D1E6 (pale blue)

LIGHTING:
- Warm golden light streaming from upper-left
- Soft, diffused quality (no harsh shadows)
- Gentle light rays visible through canopy
- Perpetual golden hour feeling

ATMOSPHERE:
- Magical but not fantastical
- Safe and welcoming
- Inviting for children
- NO dark areas, NO scary elements

TECHNICAL:
- Style: Painterly digital illustration, soft edges
- Resolution: 2388×1668px minimum (for @2x)
- Aspect ratio: 16:9 (landscape iPad)
- NO UI elements, NO text, NO characters (pure background)
```

**Expected Output:** 1194×834pt base (@2x = 2388×1668px, @3x = 3582×2502px)

**Screen Layout Notes:**
- Center: Progress bar area (keep relatively clear)
- Edges: Tree holes for Lemminge peeking
- Top center: Space for wooden sign
- Bottom: Forest floor visible

**QA Checklist:**
- [ ] 4 distinct parallax layers visible?
- [ ] Warm golden lighting from upper-left?
- [ ] Colors from approved palette only?
- [ ] No red/neon colors?
- [ ] Soft edges, no harsh contrasts?
- [ ] Safe, welcoming atmosphere?
- [ ] No scary elements?
- [ ] 16:9 aspect ratio?
- [ ] High resolution (@3x ready)?

---

## 2. forest_menu.png

**Screen:** Home Screen (Waldabenteuer)
**Reference Mockup:** `../../design/references/screens/Reference_Menu_Screen.png`

**Prompt:**
```
Generate a magical forest background for a children's game home menu screen.

SCENE COMPOSITION:
- 4-layer parallax forest scene
- Central clearing with visible branch system across top third
- Strong horizontal branch for hanging wooden signs
- Open clearing in center for UI elements
- Tree trunks framing left and right sides
- Visible tree holes (3-4) for Lemminge hiding spots
- Gentle moss-covered ground
- Scattered berries and flowers

COLOR PALETTE:
[Same as forest_loading.png]

LIGHTING:
[Same as forest_loading.png]

SPECIFIC REQUIREMENTS:
- Top third: Strong branch system (for hanging activity signs)
- Center: Open clearing (for wooden signs and buttons)
- Bottom right: Space for treasure chest on ground
- Sides: Tree holes at various heights
- Ground level: Visible log (for hiding Lemminge)

ATMOSPHERE:
- Adventure hub feeling
- Multiple activity areas visible
- Clear sight lines to all important zones
- Welcoming, ready-to-explore feeling

TECHNICAL:
[Same as forest_loading.png]
```

**Screen Layout Notes:**
- Top: Branch system for 4 hanging signs (Rätsel, Zahlen, Zeichnen, Logik)
- Center-left: Space for Bennie character
- Center-right: Clear area for UI
- Bottom-right: Treasure chest location
- Edges: Lemminge hiding spots

**QA Checklist:**
[Same as forest_loading.png]

---

## 3. forest_activity.png

**Screen:** All Activity Gameplay Screens (Puzzle, Labyrinth, Numbers)
**Reference Mockups:** 
- `Reference_Matching_Game_Screen.png`
- `Reference_Numbers_Game_Screen.png`
- `Reference_Layrinth_Game_Screen.png`

**Prompt:**
```
Generate a magical forest background for children's game activity screens.

SCENE COMPOSITION:
- 4-layer parallax forest scene
- More open, less cluttered than menu
- Focus on center area (for game elements)
- Gentle framing with trees on sides
- Subtle ground detail (less busy than menu)
- Sky visible through canopy (more light)

COLOR PALETTE:
[Same as forest_loading.png]

LIGHTING:
- Slightly brighter than menu (more focused gameplay)
- Clear center area with good visibility
- Warm but not distracting

SPECIFIC REQUIREMENTS:
- Top: Space for navigation bar
- Center: Large clear area (60% of screen) for game grid/path
- Sides: Minimal detail, soft framing only
- Bottom: Progress bar area, ground detail
- Characters appear in front of this background

ATMOSPHERE:
- Focused, calm, clear
- Less busy than menu (reduce distractions)
- Still warm and safe
- Good contrast for game elements

TECHNICAL:
[Same as forest_loading.png]
```

**Screen Layout Notes:**
- Top: Home button, progress bar, volume button
- Center: Game area (must have clear visibility)
- Bottom: Tool palette for puzzle games
- Sides: Character positions

**QA Checklist:**
[Same as forest_loading.png]
- [ ] Center area clear and uncluttered?
- [ ] Good contrast for game elements?

---

## 4. forest_treasure.png

**Screen:** Treasure Screen
**Reference Mockup:** `../../design/references/screens/Reference_Treasure_Screen.png`

**Prompt:**
```
Generate a magical forest treasure room background for a children's game.

SCENE COMPOSITION:
- 4-layer parallax forest scene
- Special clearing with "treasure grove" feeling
- Visible tree roots creating natural shelves
- Warm golden light emphasizing center
- Scattered coins and gold sparkles
- Magical atmosphere (more fantastical than other screens)
- Berry bushes with gold berries (treasure theme)

COLOR PALETTE:
[Same base palette, with additions:]
- Coin gold: #D9C27A (warm gold accents)
- Sparkle highlights: #F5E6C8 (light gold)
- Special tree roots: #6B4423 (dark wood)

LIGHTING:
- Extra warm, treasure-grove feeling
- Spotlight effect on center (treasure chest location)
- Golden sparkles in air
- Inviting, celebratory mood

SPECIFIC REQUIREMENTS:
- Center: Open area for large treasure chest
- Background: More magical than other screens
- Ground: Scattered gold coins
- Atmosphere: Special, rewarding, celebratory

ATMOSPHERE:
- Treasure found!
- Magical reward space
- Celebratory but calm
- Still safe and warm

TECHNICAL:
[Same as forest_loading.png]
```

**Screen Layout Notes:**
- Center: Large treasure chest
- Around chest: Lemminge celebrating
- Top: Coin counter display
- Bottom: YouTube redemption buttons

**QA Checklist:**
[Same as forest_loading.png]
- [ ] Magical/special atmosphere?
- [ ] Gold accents present (coins, sparkles)?
- [ ] Center area clear for treasure chest?

---

## 5. forest_video_selection.png

**Screen:** Video Selection Screen

**Prompt:**
```
Generate a cozy forest viewing area background for a children's game.

SCENE COMPOSITION:
- 4-layer parallax forest scene
- Cozy clearing with theater/viewing feel
- Natural log seating area suggested
- Warm, settled-in atmosphere
- Less adventure, more relaxation mood

COLOR PALETTE:
[Same as forest_loading.png]
- Slightly warmer tones overall
- More ground visible (cozy space)

LIGHTING:
- Warm evening light (settling down)
- Softer than activity screens
- Cozy, ready-to-watch feeling

SPECIFIC REQUIREMENTS:
- Center: Clear area for video thumbnails grid
- Atmosphere: Cozy video-watching space
- Natural "screen area" feeling in composition

ATMOSPHERE:
- Cozy, settled
- Ready to watch and relax
- Still playful but calmer
- Reward time feeling

TECHNICAL:
[Same as forest_loading.png]
```

**QA Checklist:**
[Same as forest_loading.png]
- [ ] Cozy, relaxed atmosphere?
- [ ] Clear center for video grid?

---

## 6. forest_player_select.png

**Screen:** Player Selection Screen
**Reference Mockup:** `../../design/references/screens/Reference_Player_Selection_Screen.png`

**Prompt:**
```
Generate a welcoming forest entrance background for player selection.

SCENE COMPOSITION:
- 4-layer parallax forest scene
- Open welcoming entrance area
- Path leading into forest (invitation)
- Two distinct areas (left/right) for player cards
- Bennie visible in center-bottom (greeting position)

COLOR PALETTE:
[Same as forest_loading.png]

LIGHTING:
- Bright, welcoming
- Morning-light feeling
- Clear visibility for player cards

SPECIFIC REQUIREMENTS:
- Left side: Space for Alexander card
- Right side: Space for Oliver card
- Center-bottom: Bennie greeting area
- Top: Title sign area

ATMOSPHERE:
- First screen, very welcoming
- "Choose your adventure" feeling
- Open, inviting
- Clear character spaces

TECHNICAL:
[Same as forest_loading.png]
```

**QA Checklist:**
[Same as forest_loading.png]
- [ ] Two distinct player areas?
- [ ] Very welcoming, friendly?

---

## 7. forest_celebration.png

**Screen:** Celebration Overlay (semi-transparent background)

**Prompt:**
```
Generate a magical sparkly forest background for celebration overlay.

SCENE COMPOSITION:
- 4-layer parallax forest scene
- Extra magical, sparkly atmosphere
- Soft glow throughout
- Ethereal quality (for overlay use)
- Lighter, airier than other screens

COLOR PALETTE:
[Same base palette]
- Extra sparkle highlights: #F5E6C8
- Soft glow: #B3D1E6 at 20%
- More visible light rays

LIGHTING:
- Bright, celebratory
- Multiple light rays
- Sparkles throughout
- Magical but not overwhelming

SPECIFIC REQUIREMENTS:
- Will be dimmed to 40% in use (overlay effect)
- Should still look good when dimmed
- Extra detail for visual interest during celebration

ATMOSPHERE:
- Celebration!
- Success achieved
- Magical reward moment
- Joyful but not overstimulating

TECHNICAL:
[Same as forest_loading.png]
```

**QA Checklist:**
[Same as forest_loading.png]
- [ ] Extra magical atmosphere?
- [ ] Looks good at 40% brightness (test)?
- [ ] Sparkles visible but not overwhelming?

---

## 8. forest_parent_dashboard.png

**Screen:** Parent Dashboard (Settings)

**Prompt:**
```
Generate a organized forest office/workspace background for parent settings.

SCENE COMPOSITION:
- 4-layer parallax forest scene
- More organized, structured feeling
- Natural "workspace" vibe
- Tree desk/shelf elements
- Tidy clearing with purpose
- Less playful, more functional

COLOR PALETTE:
[Same as forest_loading.png]
- Slightly cooler tones (less golden)
- More browns (wood elements)
- Organized, structured feel

LIGHTING:
- Clear, functional lighting
- Less magical, more practical
- Good visibility for settings UI

SPECIFIC REQUIREMENTS:
- Clean, organized space
- Natural shelving/organizational elements
- Space for settings cards
- Less whimsical than child screens

ATMOSPHERE:
- Adult space (parent area)
- Organized, functional
- Still forest theme
- Calm, clear, purposeful

TECHNICAL:
[Same as forest_loading.png]
```

**QA Checklist:**
[Same as forest_loading.png]
- [ ] More structured, organized feel?
- [ ] Less playful than child screens?
- [ ] Clear functional space?

---

## Generation Workflow

```bash
# For each background:

1. Copy prompt from above
2. Open Gemini AI Studio
3. Paste prompt
4. Generate 4 variations
5. Select best matching mockup
6. Regenerate if needed for refinement
7. Download at highest resolution
8. Export @2x (2388×1668px) and @3x (3582×2502px)
9. Save to Assets.xcassets/Backgrounds/
10. Test in Xcode with UI overlays
```

## Quality Assurance

**Universal Background Checklist:**
```
✓ 4 distinct parallax layers?
✓ Warm golden lighting from upper-left?
✓ Colors from approved forest palette?
✓ NO red colors?
✓ NO bright/neon colors?
✓ NO harsh shadows or bright spots?
✓ Soft edges throughout?
✓ Safe, welcoming atmosphere?
✓ NO scary elements (dark caves, dead trees)?
✓ 16:9 aspect ratio (landscape)?
✓ High resolution (@3x = 3582×2502px minimum)?
✓ Matches reference mockup composition?
✓ Works well with UI elements overlaid?
```

**Screen-Specific Checks:**
- Loading: Tree holes for Lemminge visible?
- Menu: Strong branch system for signs?
- Activity: Center 60% clear and uncluttered?
- Treasure: Magical atmosphere with gold accents?
- Video Selection: Cozy theater feeling?
- Player Select: Two distinct player areas?
- Celebration: Extra sparkly, looks good at 40%?
- Parent Dashboard: Organized, functional feel?

## Parallax Layer Breakdown

Each background should have these distinct layers:

```
Layer 1 (Farthest): Misty background trees
├─ Color: #4A6B5C (darkest, lowest saturation)
├─ Detail: Minimal, silhouettes only
└─ Blur: 8px Gaussian blur

Layer 2 (Far): Mid-ground canopy
├─ Color: #738F66 (main forest color)
├─ Detail: Branch structures visible
└─ Blur: 4px Gaussian blur

Layer 3 (Near): Foreground foliage
├─ Color: #7A9973 (warmest green)
├─ Detail: Leaves, flowers visible
└─ Blur: None (sharp)

Layer 4 (Foreground): Ground & tree trunks
├─ Color: #8C7259 (bark), #5D6B4D (moss)
├─ Detail: Highest detail level
└─ Blur: None (sharpest)

Overlay: Light rays
├─ Color: #F5E6C8
├─ Opacity: 30%
└─ Blend mode: Screen or Add
```

## Testing in Context

After generating each background:

1. **Import to Xcode** at @2x and @3x
2. **Test with UI overlay:**
   - Load screen with progress bar
   - Menu screen with activity signs
   - Activity screen with game grid
3. **Check visibility:**
   - Can you read text on wooden signs?
   - Do game elements have good contrast?
   - Are touch targets clearly visible?
4. **Check atmosphere:**
   - Does it match the screen's purpose?
   - Is it appropriately busy/calm?
5. **Test with characters:**
   - Place Bennie in expected position
   - Place Lemminge in hiding spots
   - Do they stand out from background?

## Total Asset Count

- **Backgrounds:** 8 screens × 3 sizes (@1x for reference, @2x, @3x) = 24 files
- **Storage:** ~15-20MB total (optimized PNG)

## Delivery Format

```
Assets.xcassets/
└── Backgrounds/
    ├── forest_loading.imageset/
    │   ├── forest_loading@2x.png
    │   ├── forest_loading@3x.png
    │   └── Contents.json
    ├── forest_menu.imageset/
    ├── forest_activity.imageset/
    ├── forest_treasure.imageset/
    ├── forest_video_selection.imageset/
    ├── forest_player_select.imageset/
    ├── forest_celebration.imageset/
    └── forest_parent_dashboard.imageset/
```

---

*Reference: PLAYBOOK Part 1.4 (Super Forest Design), Part 4 (Screen Specifications)*
