# 🎨 Bennie Bear - Design QA Checklist

> **Version:** 1.0  
> **Last Updated:** January 10, 2026  
> **For:** iPad App Implementation Review

---

## 📋 How to Use This Checklist

**For Each Screen:**
1. Take a screenshot of the implemented screen
2. Open the corresponding reference image from `docs/design/references/screens/`
3. Go through each checklist item
4. Mark ✅ Pass, ⚠️ Needs Attention, or ❌ Fail
5. Document any issues found

**Acceptance Criteria:**
- ✅ **Pass:** 100% of Critical items + 90% of High Priority items
- ⚠️ **Review Required:** 100% Critical + 80-89% High Priority
- ❌ **Reject:** Any Critical failures OR <80% High Priority

---

# Part 1: Character Design Compliance

## 1.1 Bennie der Bär - Visual Checklist

**Reference Images:** `docs/design/references/characters/bennie/`

### Critical Requirements (Must Pass 100%)

| ✓ | Requirement | Specification | How to Verify |
|---|-------------|---------------|---------------|
| ☐ | **NO CLOTHING** | Bennie NEVER wears vest, shirt, or any clothing | Visual inspection - bare bear |
| ☐ | **Correct Brown** | Main fur: `#8C7259` (±5% tolerance) | Color picker on fur |
| ☐ | **Snout Color** | Tan snout ONLY: `#C4A574` | Color picker on snout area |
| ☐ | **NO Belly Patch** | Belly is SAME color as body | No separate lighter belly area |
| ☐ | **Adult Bear** | Pear-shaped body, NOT teddy/cub | Body proportions check |
| ☐ | **Cel-Shaded Style** | Clean vector art with bold outlines | Visual style consistency |

### High Priority (Target 90%+)

| ✓ | Requirement | Specification | Notes |
|---|-------------|---------------|-------|
| ☐ | Nose shape | Dark triangle (`#3D2B1F`) | Should be espresso brown |
| ☐ | Eye style | Small, round, kind | White highlight visible |
| ☐ | Body proportions | Narrow shoulders, wide hips, round belly | Pear-shaped silhouette |
| ☐ | Paw detail | Visible claws on paws | Subtle detail |
| ☐ | Expression | Never frustrated/angry | Always patient & friendly |

### Animation State Verification

| State | Reference File | Visual Check | Expression Check |
|-------|---------------|--------------|------------------|
| Idle | bennie-idle.png | ☐ Gentle breathing | ☐ Calm smile |
| Pointing | bennie-pointing.png | ☐ Extended arm toward target | ☐ Helpful |
| Encouraging | bennie-encouraging.png | ☐ Leaning forward | ☐ Soft eyes |
| Celebrating | bennie-celebrating.png | ☐ Arms up, jumping | ☐ Eyes squint |
| Thinking | bennie-thinking.png | ☐ Paw on chin, eyes up | ☐ Contemplative |
| Waving | bennie-waving.png | ☐ Consistent wave motion | ☐ Welcoming |

---

## 1.2 Die Lemminge - Visual Checklist

**Reference Images:** `docs/design/references/characters/lemminge/`

### Critical Requirements (Must Pass 100%)

| ✓ | Requirement | Specification | How to Verify |
|---|-------------|---------------|---------------|
| ☐ | **BLUE Body** | `#6FA8DC` (±5% tolerance) | Color picker on body |
| ☐ | **NOT Green/Brown** | NEVER any shade of green or brown | Visual inspection |
| ☐ | **Buck Teeth** | Prominent white buck teeth visible | Clear tooth display |
| ☐ | **Round Blob Shape** | Go-gopher mascot style potato | Shape verification |
| ☐ | **White/Cream Belly** | Fuzzy edge where meets blue | Belly patch visible |
| ☐ | **Cel-Shaded Style** | Thick black outlines, flat colors | Style consistency |

### High Priority (Target 90%+)

| ✓ | Requirement | Specification | Notes |
|---|-------------|---------------|-------|
| ☐ | Pink nose | Small, pink (`#E8A0A0`) | Cute detail |
| ☐ | Pink paws | Stubby nubs with pink pads (`#E8A0A0`) | Paw pad color |
| ☐ | Eye style | Large, round, white sclera, small dark pupils | Expressive eyes |
| ☐ | Ear shape | Two small rounds, same blue as body | Proportional |
| ☐ | Always friendly | Even "mischievous" is playful, never mean | Tone check |

### Animation State Verification

| State | Reference File | Visual Check | Expression Check |
|-------|---------------|--------------|------------------|
| Idle | lemminge-idle.png | ☐ Swaying, blinking | ☐ Content |
| Curious | lemminge-curious.png | ☐ Wide eyes, head tilt | ☐ Interested |
| Excited | lemminge-excited.png | ☐ Bouncing | ☐ Sparkly eyes |
| Celebrating | lemminge-celebrating.png | ☐ Jumping, arms up | ☐ Joyful |
| Hiding | lemminge-hiding.png | ☐ Peeking from edge | ☐ Playful |
| Mischievous | lemminge-mischievous.png | ☐ Sly grin | ☐ Scheming (friendly) |

---

# Part 2: Color Palette Compliance

## 2.1 Primary Palette Verification

| Color Name | Hex Code | RGB | Usage | ✓ |
|------------|----------|-----|-------|---|
| Woodland | `#738F66` | 115,143,102 | Primary buttons, safe areas | ☐ |
| Bark | `#8C7259` | 140,114,89 | Bennie fur, wood elements | ☐ |
| Sky | `#B3D1E6` | 179,209,230 | Accents, backgrounds | ☐ |
| Cream | `#FAF5EB` | 250,245,235 | Backgrounds, safe space | ☐ |

## 2.2 Secondary Palette Verification

| Color Name | Hex Code | RGB | Usage | ✓ |
|------------|----------|-----|-------|---|
| Success | `#99BF8C` | 153,191,140 | Positive feedback, progress | ☐ |
| CoinGold | `#D9C27A` | 217,194,122 | Rewards, treasure | ☐ |
| LemmingeBlue | `#6FA8DC` | 111,168,220 | Lemminge bodies | ☐ |
| LemmingePink | `#E8A0A0` | 232,160,160 | Lemminge noses/paws | ☐ |

## 2.3 Wood UI Colors

| Color Name | Hex Code | Usage | ✓ |
|------------|----------|-------|---|
| Wood Light | `#C4A574` | Highlights, top edges | ☐ |
| Wood Medium | `#A67C52` | Main plank color | ☐ |
| Wood Dark | `#6B4423` | Shadows, grain lines | ☐ |
| Rope | `#B8956B` | Sign mounting | ☐ |
| Chain | `#6B6B6B` | Lock system | ☐ |

## 2.4 Forbidden Colors Check

| ✓ | Forbidden | Why | Verification |
|---|-----------|-----|--------------|
| ☐ | Pure Red `#FF0000` | Triggers anxiety | No pure red anywhere |
| ☐ | Pure White `#FFFFFF` | Too harsh for large areas | Only small highlights |
| ☐ | Pure Black `#000000` | Too harsh for large areas | Only outlines |
| ☐ | Neon colors | Overstimulating | No neon/fluorescent |
| ☐ | Saturation >80% | Overstimulating | Check all colors |

---

# Part 3: Screen-by-Screen QA

## 3.1 Loading Screen

**Reference:** `docs/design/references/screens/Reference_Loading_Screen.png`

### Layout Elements

| ✓ | Element | Position | Size | Requirement |
|---|---------|----------|------|-------------|
| ☐ | Title Sign | Top center | 400×100pt | "Waldabenteuer" with rope mount |
| ☐ | Bennie | Left of center | 200×300pt | Waving animation |
| ☐ | Lemminge | Multiple spots | 60×80pt each | 4-5 peeking from tree holes |
| ☐ | Progress Bar | Bottom center | 600×40pt | Berry-decorated log |
| ☐ | Loading Text | Below bar | 17pt | "Lade Spielewelt..." |

### Animation Check

| ✓ | Animation | Duration | Easing | Requirement |
|---|-----------|----------|--------|-------------|
| ☐ | Progress fill | Smooth | Linear | 0-100% with percentage display |
| ☐ | Bennie wave | 2s loop | Spring | Gentle, welcoming |
| ☐ | Lemminge peek | 3s offset | Ease-in-out | Staggered, playful |
| ☐ | Sparkles | Continuous | Random | Subtle, not distracting |

### Voice Narration

| ✓ | Trigger | German Text | Timing |
|---|---------|-------------|--------|
| ☐ | On appear | "Herzlich Willkommen. Lass uns das Abenteuer beginnen." | Start of load |
| ☐ | Voice quality | Warm, 85% speed, max 7 words/sentence | ElevenLabs voice |

---

## 3.2 Player Selection Screen

**Reference:** `docs/design/references/screens/Reference_Menu_Screen.png` (shows player area)

### Layout Elements

| ✓ | Element | Position | Size | Requirement |
|---|---------|----------|------|-------------|
| ☐ | Title Text | Top center | 32pt | "Wer spielt heute?" |
| ☐ | Alexander Button | Left (x≈400) | 160×180pt | Photo/avatar + name |
| ☐ | Oliver Button | Right (x≈800) | 160×180pt | Photo/avatar + name |
| ☐ | Bennie | Center bottom | 180×280pt | Waving, welcoming |
| ☐ | Lemminge | Corners | 60×80pt | 2 watching |

### Touch Targets

| ✓ | Element | Touch Area | Requirement |
|---|---------|------------|-------------|
| ☐ | Alexander | ≥160×180pt | Above 96pt minimum |
| ☐ | Oliver | ≥160×180pt | Above 96pt minimum |
| ☐ | Visual feedback | Scale 0.95 | Immediate on press |

### Voice Narration

| ✓ | Trigger | German Text | Timing |
|---|---------|-------------|--------|
| ☐ | On appear | "Wer bist du? Alexander oder Oliver?" | Immediately |
| ☐ | After selection | "[NAME], lass uns das Abenteuer beginnen" | After tap |

---

## 3.3 Home Screen (Waldabenteuer)

**Reference:** `docs/design/references/screens/Reference_Menu_Screen.png`

### Layout Elements

| ✓ | Element | Position | Size | Requirement |
|---|---------|----------|------|-------------|
| ☐ | Title Sign | Top center | ~500×100pt | "Waldabenteuer" wooden sign |
| ☐ | Player Icon | Top right | 60×60pt | Current player indicator |
| ☐ | Rätsel Button | Top left card | 160×140pt | Hanging from branch |
| ☐ | Zahlen Button | Top right card | 160×140pt | Hanging from branch |
| ☐ | Zeichnen Button | Bottom left card | 160×140pt | Hanging from branch |
| ☐ | Logik Button | Bottom right card | 160×140pt | Hanging from branch |
| ☐ | Treasure Chest | Bottom right | ~100×100pt | Open if ≥10 coins |
| ☐ | Settings Icon | Bottom left corner | 48×48pt | Gear icon |
| ☐ | Help Icon | Bottom center | 48×48pt | Question mark |
| ☐ | Bennie | Right side | 180×280pt | Pointing at activities |
| ☐ | Lemminge | In log/corners | 60×80pt | 1-2 visible |

### Activity Button States

| ✓ | State | Visual | Interaction |
|---|-------|--------|-------------|
| ☐ | Unlocked | Warm wood, golden glow | Tappable, slight swing |
| ☐ | Locked | Dimmed, X-pattern chains, padlock | Not tappable |
| ☐ | Pressed | Scale 0.95, darker shadow | Immediate feedback |

### Touch Targets

| ✓ | Element | Size | Requirement |
|---|---------|------|-------------|
| ☐ | Activity buttons | 160×140pt | Well above 96pt |
| ☐ | Settings/Help | 48×48pt | Meets 96pt via padding |
| ☐ | Treasure chest | ~100×100pt | Above minimum |

---

## 3.4 Matching Game Screen (Rätsel - Pattern Match)

**Reference:** `docs/design/references/screens/Reference_Matching_Game_Screen.png`

### Layout Elements

| ✓ | Element | Position | Size | Requirement |
|---|---------|----------|------|-------------|
| ☐ | Home Button | Top left | 96×60pt | "Home" wooden button |
| ☐ | Progress Bar | Top center | ~600×40pt | Shows coins earned |
| ☐ | Volume Control | Top right | 60×60pt | Sound icon |
| ☐ | ZIEL Tablet | Center left | ~250×250pt | Stone tablet with grid |
| ☐ | DU Tablet | Center right | ~250×250pt | Stone tablet with grid |
| ☐ | Arrow | Between tablets | ~80pt | Wooden arrow pointing right |
| ☐ | Tool Tray | Bottom center | ~600×80pt | Wooden log with tools |
| ☐ | Bennie | Right side | ~180×280pt | Pointing, encouraging |
| ☐ | Lemminge | Left/bottom | 60×80pt | 2-3 watching |

### Grid Specifications

| ✓ | Property | Specification | Requirement |
|---|----------|---------------|-------------|
| ☐ | Cell size | 96×96pt | Meets touch target |
| ☐ | Grid lines | Carved grooves, golden inlay | Visible separation |
| ☐ | Stone texture | Mossy edges, weathered | Forest aesthetic |
| ☐ | Labels | "ZIEL" and "DU" in German | Clear labeling |

### Tool Tray Elements

| ✓ | Tool | Size | Function |
|---|------|------|----------|
| ☐ | Green button | ~80×80pt | Select green |
| ☐ | Yellow button | ~80×80pt | Select yellow |
| ☐ | Gray/Empty button | ~80×80pt | Clear cell |
| ☐ | Eraser | ~60×60pt | Erase mode |
| ☐ | Reset | ~60×60pt | Clear all |

### Visual States

| ✓ | State | Visual | Audio |
|---|-------|--------|-------|
| ☐ | Empty cell | Gray stone | Silent |
| ☐ | Filled cell | Colored (green/yellow) | Pop sound |
| ☐ | Match complete | Golden glow on both grids | Success chime |
| ☐ | Tool selected | Highlighted border | Tap sound |

---

## 3.5 Numbers Game Screen (Zahlen)

**Reference:** `docs/design/references/screens/Reference_Numbers_Game_Screen.png`

### Layout Elements

| ✓ | Element | Position | Size | Requirement |
|---|---------|----------|------|-------------|
| ☐ | Home Button | Top left | 96×60pt | "Home" wooden button |
| ☐ | Progress Bar | Top center | ~600×40pt | Shows coins earned |
| ☐ | Volume Control | Top right | 60×60pt | Sound icon |
| ☐ | Number Grid | Center | Variable | Stone tablet with numbers 1-10 |
| ☐ | Tool Tray | Bottom | ~600×80pt | Wooden log (fewer tools) |
| ☐ | Bennie | Right side | ~180×280pt | Encouraging |
| ☐ | Lemminge | Bottom corners | 60×80pt | 2 watching |

### Number Display

| ✓ | Property | Specification | Requirement |
|---|----------|---------------|-------------|
| ☐ | Numbers | 1-10 carved in stone | Clear, large |
| ☐ | Touch targets | ≥96×96pt per number | Generous spacing |
| ☐ | Font style | SF Rounded Bold | Consistent |
| ☐ | Number size | 32-48pt | Readable |

### Game Variants

| ✓ | Variant | Description | Check |
|---|---------|-------------|-------|
| ☐ | Würfel (Dice) | Roll dice, select number | Animated dice |
| ☐ | Wähle die Zahl | Narrator says number, child taps | Voice clear |

---

## 3.6 Labyrinth Game Screen (Rätsel - Maze)

**Reference:** `docs/design/references/screens/Reference_Labyrinth_Game_Screen.png`

### Layout Elements

| ✓ | Element | Position | Size | Requirement |
|---|---------|----------|------|-------------|
| ☐ | Title | Top center | ~400×80pt | "Bennie & Lemminge Labyrinth" |
| ☐ | Maze Canvas | Center | ~800×600pt | Path drawing area |
| ☐ | Start Point | Left side | Marked "START" | Bennie at start |
| ☐ | End Point | Right side | Marked "ZIEL" | Lemminge at goal |
| ☐ | Bennie Character | Start position | ~100×150pt | Waiting to chase |
| ☐ | Lemminge Target | Goal position | ~60×80pt | Destination |

### Drawing Mechanics

| ✓ | Property | Specification | Requirement |
|---|----------|---------------|-------------|
| ☐ | Line width | ~15pt | Visible, not too thick |
| ☐ | Line color | Green/woodland | Matches palette |
| ☐ | Touch response | Immediate | No lag |
| ☐ | Path validation | AI tracking | Accepts reasonable paths |

---

## 3.7 Celebration Overlay

**Reference:** Not a separate screen - overlay on activity completion

### Critical Requirements

| ✓ | Requirement | Specification | Why Critical |
|---|-------------|---------------|--------------|
| ☐ | **OVERLAY, not new screen** | Floats over activity | Context preservation (autism-friendly) |
| ☐ | Activity visible beneath | Semi-transparent `#FAF5EB` @ 85% | See completed work |
| ☐ | No jarring transition | Scale in 0.8→1.0, spring ease | Predictable, calm |

### Layout Elements

| ✓ | Element | Size | Content |
|---|---------|------|---------|
| ☐ | Praise text | 32pt | "Super gemacht!" |
| ☐ | Coin reward | 24pt + icon | "+1" with coin animation |
| ☐ | Bennie + Lemminge | 120×180pt | Celebrating together |
| ☐ | Continue button | 160×96pt | "Weiter" wooden button |
| ☐ | Confetti particles | Full screen | Over everything |

### Voice Narration

| ✓ | Trigger | German Text | Timing |
|---|---------|-------------|--------|
| ☐ | On overlay appear | "Super gemacht!" OR "Toll!" | Immediately |
| ☐ | Coin milestone (5) | "Wir haben schon 5 Goldmünzen. Nochmals 5 und wir können Youtube schauen" | After praise |

---

## 3.8 Treasure Screen (Schatzkiste)

**Reference:** Playbook description (no specific reference image for this screen)

### Layout Elements

| ✓ | Element | Position | Size | Requirement |
|---|---------|----------|------|-------------|
| ☐ | Back Button | Top left | 96×60pt | "Zurück" |
| ☐ | Coin Counter | Top center | 200×50pt | Current balance |
| ☐ | Treasure Chest | Center | 300×250pt | Open/glowing if ≥10 |
| ☐ | 5 Min Option | Bottom left | 200×100pt | 10 coins cost, grayed if <10 |
| ☐ | 10+2 Min Option | Bottom right | 200×100pt | 20 coins cost, grayed if <20 |
| ☐ | Bennie | Right side | 180×280pt | Gesturing to chest |
| ☐ | Lemminge | Corners | 60×80pt | Excited |

### Chest States

| ✓ | State | Visual | Coin Count |
|---|-------|--------|------------|
| ☐ | Closed | Locked, dim | <10 coins |
| ☐ | Open | Glowing gold | ≥10 coins |

### Voice Narration

| ✓ | Condition | German Text | Timing |
|---|-----------|-------------|--------|
| ☐ | <10 coins | "Du hast [X] Goldmünzen. Du musst noch [Y] Goldmünzen verdienen" | On screen appear |
| ☐ | 10-19 coins | "Du hast [X] Goldmünzen. Du kannst 5 Minuten Youtube schauen." | On screen appear |
| ☐ | ≥20 coins | "Du hast [X] Goldmünzen. Du kannst 5 Minuten Youtube schauen oder 12 Minuten Youtube schauen" | On screen appear |
| ☐ | Button tapped | "Film ab" | Immediately |

---

# Part 4: UI Component Standards

## 4.1 Wooden Sign Buttons (Activity Cards)

### Visual Requirements

| ✓ | Property | Specification | Requirement |
|---|----------|---------------|-------------|
| ☐ | Minimum size | 160×140pt | Well above 96pt target |
| ☐ | Wood gradient | `#C4A574` (top) → `#A67C52` (bottom) | Warm wood look |
| ☐ | Text color | `#4A4036` (carved brown) | Readable contrast |
| ☐ | Border | 2pt `#6B4423` | Dark wood edge |
| ☐ | Rope color | `#B8956B` | Consistent mounting |
| ☐ | Corner radius | 12pt | Soft edges |
| ☐ | Wood grain | Visible texture | Realistic detail |

### Animation Requirements

| ✓ | State | Animation | Duration |
|---|-------|-----------|----------|
| ☐ | Default | Slight shadow | Static |
| ☐ | Hover | Gentle swing | 0.5s |
| ☐ | Pressed | Scale 0.95, darker shadow | Immediate |
| ☐ | Locked | Dimmed, chains visible | Static |
| ☐ | Unlocking | Chains fall with sound | 0.8s |

## 4.2 Progress Bar (Berry-Decorated Log)

| ✓ | Property | Specification | Requirement |
|---|----------|---------------|-------------|
| ☐ | Container | Wooden trough/log shape | Organic look |
| ☐ | Fill color | `#99BF8C` with gradient | Success green |
| ☐ | Empty color | `#6B4423` | Dark wood interior |
| ☐ | Decoration | Berry clusters at ends | Playful detail |
| ☐ | Fill animation | Smooth + sparkle at edge | Magical feel |
| ☐ | Coin icons | Show progress toward 10/20 | Clear milestones |

## 4.3 Stone Tablets (Game Grids)

| ✓ | Property | Specification | Requirement |
|---|----------|---------------|-------------|
| ☐ | Material | Stone with carved grid | Natural look |
| ☐ | Edges | Mossy/weathered texture | Forest integration |
| ☐ | Grid lines | Carved grooves, golden inlay | Visible separation |
| ☐ | Cell size | 96×96pt minimum | Touch target |
| ☐ | Labels | "ZIEL" (target) and "DU" (yours) | German text |

---

# Part 5: Touch & Interaction Standards

## 5.1 Touch Target Requirements

### Critical (100% Compliance)

| ✓ | Element Type | Minimum Size | Verification |
|---|--------------|--------------|--------------|
| ☐ | Primary buttons | 96×96pt | Measure in Xcode |
| ☐ | Activity cards | 160×140pt | Well above minimum |
| ☐ | Grid cells | 96×96pt | Touch-friendly |
| ☐ | Tool tray items | 60×60pt + padding | With padding ≥96pt |

### Touch Response

| ✓ | Interaction | Response Time | Visual Feedback |
|---|-------------|---------------|-----------------|
| ☐ | Button tap | <100ms | Scale 0.95 immediately |
| ☐ | Grid cell tap | <50ms | Color change immediate |
| ☐ | Drawing/drag | Real-time | Line follows finger |
| ☐ | No accidental taps | Debounce 300ms | Prevent double-taps |

## 5.2 Gesture Support

| ✓ | Gesture | Usage | Requirement |
|---|---------|-------|-------------|
| ☐ | Single tap only | All interactions | No multi-touch confusion |
| ☐ | Drag for drawing | Labyrinth game | Smooth path |
| ☐ | No pinch/rotate | Disabled | Autism-friendly simplicity |

---

# Part 6: Animation Standards

## 6.1 Animation Timing

### Critical Requirements

| ✓ | Property | Specification | Why Critical |
|---|----------|---------------|--------------|
| ☐ | Duration range | 0.3-0.5s typical | Not too fast/slow |
| ☐ | **NO flashing** | Never | Seizure risk |
| ☐ | **NO shaking** | Never | Anxiety trigger |
| ☐ | **NO rapid strobe** | Never | Overstimulating |

### Standard Animations

| ✓ | Animation | Duration | Easing | Usage |
|---|-----------|----------|--------|-------|
| ☐ | Button press | 0.1s | Linear | Immediate feedback |
| ☐ | Screen transition | 0.3s | Spring | Gentle |
| ☐ | Character appear | 0.4s | Ease-out | Smooth entry |
| ☐ | Breathing idle | 2s loop | Ease-in-out | Calm presence |
| ☐ | Success celebration | 0.8s | Spring | Joyful but contained |

## 6.2 Character Animations

### Bennie Animations

| ✓ | Animation | Loop | Speed | Notes |
|---|-----------|------|-------|-------|
| ☐ | Idle breathing | Yes | 2s | Scale 1.0→1.03 |
| ☐ | Waving | Yes | 2s | Arm wave cycle |
| ☐ | Pointing | Hold | Static | Directed pose |
| ☐ | Celebrating | Once | 0.8s | Arms up, bounce |
| ☐ | Thinking | Yes | 3s | Paw on chin |

### Lemminge Animations

| ✓ | Animation | Loop | Speed | Notes |
|---|-----------|------|-------|-------|
| ☐ | Idle sway | Yes | 2.5s | Gentle rock |
| ☐ | Peek out | Once | 0.6s | From hiding |
| ☐ | Bounce excited | Yes | 1s | Anticipation |
| ☐ | Celebrate jump | Once | 0.8s | Arms up |

---

# Part 7: Typography & Text Standards

## 7.1 Font Standards

| ✓ | Use Case | Font | Weight | Size |
|---|----------|------|--------|------|
| ☐ | Titles | SF Rounded | Bold | 32-48pt |
| ☐ | Body text | SF Rounded | Regular | 17-24pt |
| ☐ | Buttons | SF Rounded | Semibold | 20-28pt |
| ☐ | Labels | SF Rounded | Medium | 14-17pt |

## 7.2 Language Rules

### Critical (100% Compliance)

| ✓ | Rule | Specification | Verification |
|---|------|---------------|--------------|
| ☐ | **German only** | All UI text in German | No English |
| ☐ | **Literal language** | No metaphors or idioms | Plain speech |
| ☐ | **Max 7 words** | Per Bennie sentence | Count words |
| ☐ | **Positive framing** | Always | No "wrong/error" |

### Forbidden Words

| ✓ | NEVER Use | Use Instead |
|---|-----------|-------------|
| ☐ | "Falsch" (wrong) | "Versuch's nochmal" (try again) |
| ☐ | "Fehler" (error) | "Fast!" (almost) |
| ☐ | Abstract concepts | Concrete descriptions |
| ☐ | Idioms | Literal statements |

---

# Part 8: Audio Standards

## 8.1 Voice Narration

### Voice Characteristics

| ✓ | Property | Specification | Verification |
|---|----------|---------------|--------------|
| ☐ | Voice type | Warm German male | ElevenLabs |
| ☐ | Speed | 85% of normal | Slower pacing |
| ☐ | Sentence length | Max 7 words | Count |
| ☐ | Tone | Patient, encouraging | Never frustrated |

### Audio Mixing

| ✓ | Channel | Volume Level | Priority |
|---|---------|--------------|----------|
| ☐ | Voice | 100% (1.0) | Highest |
| ☐ | Music | 30% (0.3), ducks to 15% during voice | Background |
| ☐ | Effects | 70% (0.7) | Medium |

## 8.2 Sound Effects

### Critical Requirements

| ✓ | Requirement | Specification | Why |
|---|-------------|---------------|-----|
| ☐ | Volume control | Accessible in-game | User comfort |
| ☐ | No sudden loud sounds | Max volume consistent | Autism-friendly |
| ☐ | Positive sounds only | No "wrong" buzzer | Encouraging environment |

---

# Part 9: Accessibility Requirements

## 9.1 Autism-Friendly Design

### Critical (100% Compliance)

| ✓ | Requirement | Specification | Verification |
|---|-------------|---------------|--------------|
| ☐ | **Predictable patterns** | Consistent UI placement | Check all screens |
| ☐ | **No jarring transitions** | Smooth, overlay-based | No screen flashes |
| ☐ | **Context preservation** | See activity under celebration | Overlay visible |
| ☐ | **Gentle session endings** | Gradual transitions | No abrupt stops |
| ☐ | **No timers** | Unlimited time | Never pressure |
| ☐ | **Clear cause-effect** | Immediate feedback | No delayed responses |

### Color Sensitivity

| ✓ | Check | Requirement |
|---|-------|-------------|
| ☐ | No red | Pure red (`#FF0000`) forbidden |
| ☐ | No neon | All saturation ≤80% |
| ☐ | Soft palette | Muted, forest tones |

## 9.2 Touch Accessibility

| ✓ | Feature | Specification |
|---|---------|---------------|
| ☐ | Large targets | All ≥96pt |
| ☐ | Generous spacing | No crowded buttons |
| ☐ | Single tap only | No complex gestures |
| ☐ | Immediate feedback | Visual response <100ms |

---

# Part 10: Performance Standards

## 10.1 Frame Rate

| ✓ | Metric | Target | Minimum Acceptable |
|---|--------|--------|-------------------|
| ☐ | Frame rate | 60 FPS | 55 FPS |
| ☐ | Animation smoothness | No dropped frames | <5% drops |
| ☐ | Touch response | <50ms | <100ms |

## 10.2 Loading Times

| ✓ | Screen | Target | Maximum |
|---|--------|--------|---------|
| ☐ | App launch | <2s | <3s |
| ☐ | Screen transition | <0.3s | <0.5s |
| ☐ | Asset loading | Invisible | <1s |

---

# Part 11: Final Acceptance Criteria

## 11.1 Critical Items (Must Be 100%)

- [ ] All character designs match references (Bennie, Lemminge)
- [ ] No forbidden colors used (pure red, neon, high saturation)
- [ ] All touch targets ≥96pt
- [ ] German-only UI text
- [ ] No "wrong/error" language
- [ ] No flashing/shaking animations
- [ ] Voice narration at 85% speed, max 7 words
- [ ] Context-preserving overlays (not jarring transitions)

## 11.2 High Priority (Must Be ≥90%)

- [ ] Color palette accuracy (±5% hex tolerance)
- [ ] Animation timing (0.3-0.5s range)
- [ ] Wood UI element styling
- [ ] Character animation states
- [ ] Touch response time (<100ms)
- [ ] Layout matches reference screens

## 11.3 Sign-Off Checklist

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Design Lead | __________ | _______ | _________ |
| iOS Developer | __________ | _______ | _________ |
| QA Tester | __________ | _______ | _________ |
| Accessibility Review | __________ | _______ | _________ |

---

# Appendix: Quick Reference Cards

## Character Color Quick Check

```
Bennie:  Body=#8C7259  Snout=#C4A574  Nose=#3D2B1F  NO CLOTHING
Lemminge: Body=#6FA8DC  Belly=Cream  Nose=#E8A0A0  Paws=#E8A0A0
```

## Forbidden Elements

```
❌ Red (#FF0000)
❌ Pure white/black backgrounds
❌ Neon colors
❌ Flashing
❌ Shaking
❌ "Falsch" / "Fehler"
❌ Clothing on Bennie
❌ Green/brown Lemminge
❌ Complex gestures
❌ Timers/pressure
```

## Touch Target Sizes

```
Minimum: 96×96pt
Activity Cards: 160×140pt
Character Size: ~180×280pt (Bennie), ~60×80pt (Lemminge)
```

---

**Document Version:** 1.0  
**Created:** January 10, 2026  
**For:** Bennie Bear iPad App QA  
**Reference Location:** `docs/design/references/`
