# Phase 08.1: QA Checklist

## Overview
Comprehensive quality assurance checklist covering all screens, features, and edge cases before TestFlight deployment.

**📚 Primary References:**
- **Playbook (Full)**: `../../docs/playbook/FULL_ARCHIVE.md`
- **Playbook (Modular)**: `../../docs/playbook/README.md`
- **Design References**: `../../design/references/`

---

## Testing Methodology

### Testing Phases
1. **Component Testing** - Individual UI components work correctly
2. **Screen Testing** - Each screen functions as specified
3. **Flow Testing** - Navigation and state transitions work
4. **Integration Testing** - All systems work together
5. **Accessibility Testing** - VoiceOver, color contrast, haptics
6. **Performance Testing** - 60fps, memory < 200MB, no leaks
7. **Edge Case Testing** - Unusual inputs, interruptions, errors

### Testing Environment
- **Device**: iPad (10th gen) or newer
- **OS**: iPadOS 17.0+
- **Orientation**: Landscape only (rotation locked)
- **Network**: Test both online and offline modes

### Critical Design Rules (Must Verify Every Time)
```
📋 From Playbook: Part 1 - Brand Identity

✅ MUST HAVE:
  • Bennie: Brown #8C7259, NO clothing/vest, tan snout ONLY
  • Lemminge: BLUE #6FA8DC (NEVER green, NEVER brown)
  • Touch targets: ≥ 96pt minimum
  • German language: All UI text
  • Positive feedback: Never "Falsch" or "Fehler"

❌ FORBIDDEN:
  • Red #FF0000 (anxiety trigger)
  • Neon colors (overstimulating)
  • Flashing/shaking animations (seizure risk)
  • Saturation > 80%
  • Pure white/black for large areas
```

---

## 1. Loading Screen

**📚 References:**
- Playbook: `../../docs/playbook/04-screens/loading-player.md` (Section 1)
- Reference Image: `../../design/references/screens/Reference_Loading Screen.png`
- Character Refs: 
  - `../../design/references/character/bennie/reference/bennie-reference.png`
  - `../../design/references/character/lemminge/reference/lemminge-reference.png`

### Visual Tests - Character Compliance
```
□ Bennie idle animation plays smoothly
  ↳ Bennie is brown (#8C7259), NOT wearing clothing ⚠️ CRITICAL
  ↳ Tan snout ONLY (#C4A574), NO belly patch
  ↳ Pear-shaped body (narrow shoulders, wide hips)
  ↳ Adult bear (not cub, not teddy)
  
□ Lemminge peek animations (5-6 Lemminge)
  ↳ Lemminge are BLUE (#6FA8DC) ⚠️ CRITICAL
  ↳ NOT green, NOT brown, NOT any other color
  ↳ White belly with fuzzy edge
  ↳ Buck teeth visible
  ↳ Round blob shape (Go gopher style)
```

### Visual Tests - UI Elements
```
□ Forest background renders correctly
  ↳ Warm golden light from upper-left
  ↳ Layered parallax (far/mid/near trees)
  ↳ Colors match palette: #738F66 (woodland), #B3D1E6 (sky)

□ Progress bar renders with berry decorations
  ↳ Wooden log container
  ↳ Berry clusters on both ends
  ↳ Green fill (#99BF8C) animates left-to-right
  
□ Progress bar fills smoothly from 0-100%
  ↳ Takes ~5 seconds (not too fast, not too slow)
  ↳ No jumps or stuttering
  
□ Percentage text updates in sync with bar
  ↳ Font: SF Rounded, 24pt
  ↳ Color: #6B4423 (wood dark)
  
□ "Lade Spielewelt..." text displays
  ↳ Font: SF Rounded, 17pt
  ↳ Below progress bar, centered
```

### Functional Tests
```
□ Progress animates from 0-100% in ~5 seconds
  ↳ Fake loading (assets preload during splash)
  
□ Voice plays at 100%: "Wir sind gleich bereit zum Spielen."
  ↳ File: `narrator_loading_complete.aac`
  ↳ Volume: 100% (voice priority)
  ↳ Music ducks to 15% during voice
  
□ Bennie switches from idle to waving at 100%
  ↳ Smooth animation transition (0.3s)
  ↳ Spring easing
  
□ Transition to Player Selection happens after voice
  ↳ 2 second minimum display time
  ↳ Cross-fade transition (0.3s)
  
□ Loading never gets stuck
  ↳ Timeout at 10 seconds → Skip to Player Selection
  ↳ Log error for debugging
```

### Performance Tests
```
□ Loads in < 2 seconds (cold start)
  ↳ Time from app icon tap to Loading Screen visible
  
□ Memory usage < 50MB during loading
  ↳ Use Xcode Memory Debugger
  
□ No frame drops during animation
  ↳ 60fps constant (use Instruments)
  
□ All assets preloaded
  ↳ No lazy loading delays on next screen
  ↳ Verify asset catalogs fully loaded
```

---

## 2. Player Selection Screen

**📚 References:**
- Playbook: `../../docs/playbook/04-screens/loading-player.md` (Section 2)
- Reference Image: `../../design/references/screens/Reference_Player_Selection_Screen.png`
- Voice Script: `../../docs/playbook/03-voice-script.md` (Player Selection section)

### Visual Tests
```
□ "Wer spielt heute?" title displays
  ↳ Wooden sign hanging from branch with rope
  ↳ Font: SF Rounded Bold, 32pt
  ↳ Natural wood texture with grain
  
□ Both player cards render correctly
  ↳ Wooden sign frames (200×180pt minimum)
  ↳ Player avatars visible (emoji style)
  ↳ Player names: "Alexander" / "Oliver"
  ↳ Font: SF Rounded Semibold, 28pt
  
□ Coin counts display
  ↳ 🪙 emoji + number
  ↳ Font: SF Rounded Medium, 20pt
  ↳ Shows total earned coins
  
□ Bennie waving animation plays
  ↳ Character positioned center-bottom
  ↳ Smooth wave gesture loop
  
□ Lemminge hiding animations play
  ↳ 4-5 Lemminge peeking from corners
  ↳ Gentle breathing animation
  ↳ Verify BLUE color (#6FA8DC) ⚠️
  
□ Profile icon in top-right corner
  ↳ Size: 60×60pt (circular)
  ↳ Component ref: `../../design/references/components/` (if exists)
```

### Functional Tests
```
□ Voice plays on screen appear:
  ↳ Narrator: "Wie heisst du? Alexander oder Oliver?"
  ↳ File: `narrator_player_question.aac`
  
□ Tap Alexander:
  ↳ Narrator: "Hallo Alexander! Los geht's!"
  ↳ File: `narrator_hello_alexander.aac`
  ↳ Load Alexander's player data
  ↳ Navigate to Home Screen after voice
  
□ Tap Oliver:
  ↳ Narrator: "Hallo Oliver! Los geht's!"
  ↳ File: `narrator_hello_oliver.aac`
  ↳ Load Oliver's player data
  ↳ Navigate to Home Screen after voice
  
□ Selected player data loads correctly
  ↳ Coins persist from previous session
  ↳ Activity progress persists
  ↳ Today's play time carries over
  
□ Navigation timing correct
  ↳ Voice plays fully before transition
  ↳ 0.5s pause after voice ends
  ↳ Cross-fade transition (0.3s)
  
□ Profile icon placeholder
  ↳ No action on tap (Phase 2 feature)
  ↳ No visual feedback
```

### Touch Target Tests
```
□ Alexander card ≥ 200×180pt
  ↳ Exceeds 96pt minimum
  ↳ Center: (350, 350) from playbook
  
□ Oliver card ≥ 200×180pt
  ↳ Exceeds 96pt minimum
  ↳ Center: (850, 350) from playbook
  
□ Profile icon ≥ 60×60pt
  ↳ Positioned: (1140, 50) from playbook
  
□ All buttons respond to single tap only
  ↳ No double-tap
  ↳ No long-press
  ↳ No swipe gestures
```

---

## 3. Home Screen (Waldabenteuer)

**📚 References:**
- Playbook: `../../docs/playbook/04-screens/home-activities.md` (Section 1)
- Reference Image: `../../design/references/screens/Reference_Menu_Screen.png`
- Components:
  - Activity buttons: `../../design/references/components/activity-button-*.png`
  - Treasure chest: `../../design/references/components/treasure-chest-*.png`
  - Navigation: `../../design/references/components/navigation-bar-top_*.png`
  - Settings: `../../design/references/components/settings-button-wooden_*.png`
  - Sound: `../../design/references/components/sound-button-wooden_*.png`

### Visual Tests - Activity Signs
```
□ "Waldabenteuer" title sign hangs from branch
  ↳ Rope mount visible with natural rope texture
  ↳ Leaf decorations on corners
  ↳ Font: SF Rounded Bold, 36pt
  
□ Four activity signs render correctly:
  ↳ Rätsel: Magnifying glass icon (🔍)
  ↳ Zahlen: Numbers "1,2,3" visible
  ↳ Zeichnen: Pencil icon (✏️)
  ↳ Logik: Puzzle icon (🧩)
  
□ Locked signs show chains and padlock
  ↳ X-pattern chains cross the sign
  ↳ Padlock at center bottom
  ↳ Sign dimmed to 60% opacity
  ↳ Compare to ref: Reference_Menu_Screen.png
  
□ Unlocked signs glow subtly
  ↳ Golden glow around edges
  ↳ Slight pulsing (scale 1.0 → 1.03, 2s loop)
  ↳ Wood grain texture visible
```

### Visual Tests - UI Elements
```
□ Treasure chest renders in bottom-right
  ↳ Position: (1050, 700) from playbook
  ↳ Size: ~120×120pt
  ↳ State based on coins:
    - < 10 coins: Closed, dull (treasure-chest-closed.png)
    - 10-19 coins: Open, golden glow (treasure-chest-open.png)
    - 20+ coins: Open, glow + sparkles
  
□ Progress bar shows current coins (0-10)
  ↳ Berry-decorated wooden log
  ↳ Coin slots visible (10 slots total)
  ↳ Filled slots show coin icon
  ↳ Green fill progresses left-to-right
  
□ Settings (⚙️) button visible
  ↳ Position: Top-right area
  ↳ Size: ≥ 60×60pt
  ↳ Wooden circular button
  ↳ Ref: settings-button-wooden_*.png
  
□ Help (?) button visible
  ↳ Position: Near settings
  ↳ Size: ≥ 60×60pt
  ↳ Wooden circular button
```

### Visual Tests - Characters
```
□ Bennie pointing animation plays
  ↳ Position: Left-center area
  ↳ Arm extended toward activities
  ↳ Verify brown color (#8C7259) ⚠️
  ↳ NO clothing/vest ⚠️
  ↳ Ref: bennie/reference/bennie-reference.png
  
□ Lemminge mischievous animation plays
  ↳ Position: Bottom-left corner
  ↳ Sly grin expression
  ↳ Verify BLUE color (#6FA8DC) ⚠️
  ↳ Ref: lemminge/reference/lemminge-reference.png
```

### Functional Tests - First Visit
```
□ Voice sequence on first visit:
  Part 1: Narrator: "Was möchtest du spielen?"
    ↳ File: `narrator_home_question.aac`
  Part 2: Bennie: "Hi [Name], ich bin Bennie!"
    ↳ File: `bennie_greeting_part1.aac`
    ↳ [Name] = selected player name
  Part 3 (2s pause): Bennie: "Wir lösen Aktivitäten um YouTube zu schauen."
    ↳ File: `bennie_greeting_part2.aac`
```

### Functional Tests - Return Visit
```
□ Voice sequence on return:
  Part 1: Bennie: "Lösen wir noch mehr Aktivitäten."
    ↳ File: `bennie_return_part1.aac`
  Part 2 (2s pause): Bennie: "Dann können wir mehr YouTube schauen!"
    ↳ File: `bennie_return_part2.aac`
```

### Functional Tests - Navigation
```
□ Tap Rätsel (unlocked):
  ↳ Navigate to Rätsel selection screen
  ↳ Transition: cross-fade (0.3s)
  
□ Tap Zahlen (unlocked):
  ↳ Navigate to Zahlen selection screen
  
□ Tap Zeichnen (locked):
  ↳ Bennie: "Das ist noch gesperrt."
  ↳ File: `bennie_locked.aac`
  ↳ No navigation
  ↳ Gentle bounce animation on sign
  
□ Tap Logik (locked):
  ↳ Same behavior as Zeichnen
  
□ Tap chest (coins < 10):
  ↳ Bennie: "Noch [X] Münzen!"
  ↳ File: `bennie_treasure_under10.aac`
  ↳ [X] = 10 - current coins
  ↳ No navigation
  
□ Tap chest (coins ≥ 10):
  ↳ Navigate to Treasure Screen
  ↳ Transition: cross-fade (0.3s)
  
□ Tap settings:
  ↳ Parent Gate appears (math question)
  ↳ Overlay with blur background
  
□ Tap help:
  ↳ Phase 2 feature (placeholder)
  ↳ No action currently
```

### State Tests
```
□ Progress bar reflects actual coin count
  ↳ Matches player data exactly
  ↳ Updates immediately after earning coin
  
□ Locked activities remain locked
  ↳ Zeichnen and Logik always locked in MVP
  ↳ Chains visible
  
□ Unlocked activities accessible
  ↳ Rätsel and Zahlen always unlocked in MVP
  ↳ Glow visible
  
□ Chest glow state matches coin count
  ↳ < 10: No glow
  ↳ 10-19: Golden glow
  ↳ 20+: Glow + sparkles + 2 chest icons
```

---

## 4. Rätsel: Puzzle Matching

**📚 References:**
- Playbook: `../../docs/playbook/04-screens/home-activities.md` (Section 3)
- Reference Image: `../../design/references/screens/Reference_Matching Game Screen.png`
- Voice Script: `../../docs/playbook/03-voice-script.md` (Puzzle Matching section)
- Component: Navigation bar: `../../design/references/components/navigation-bar-top_*.png`

### Visual Tests - Grid Layout
```
□ Dual grid layout (ZIEL / DU) renders
  ↳ ZIEL on left, DU on right
  ↳ Arrow between grids (→)
  ↳ Grid cells: 96×96pt minimum
  
□ Stone tablet frames render correctly
  ↳ Vine/moss decorative border
  ↳ Weathered stone texture
  ↳ Labels: "ZIEL" and "DU" at top
  ↳ Font: SF Rounded Bold, 24pt
  
□ ZIEL grid shows pattern (non-interactive)
  ↳ Pattern varies by level
  ↳ Colors clearly visible
  ↳ No tap feedback on ZIEL cells
  
□ DU grid starts empty
  ↳ All cells show gray stone background
  ↳ Subtle grid lines visible
```

### Visual Tests - Controls
```
□ Color picker (leaf shapes) at bottom
  ↳ Wooden log container
  ↳ 2-4 leaf-shaped color buttons
  ↳ Each leaf ≥ 80×80pt
  ↳ Colors: Green (#99BF8C), Yellow (#D9C27A), Gray, White
  ↳ Selected color has glow effect
  
□ Eraser button (🧽) visible
  ↳ Size: ≥ 60×60pt
  ↳ Icon clearly recognizable
  
□ Reset button (🔄) visible
  ↳ Size: ≥ 60×60pt
  ↳ Icon clearly recognizable
  
□ Progress bar at top shows coins
  ↳ Same component as Home Screen
  ↳ Berry decorations
  ↳ Current coin count visible
  
□ Home button in top-left
  ↳ House icon (🏠)
  ↳ Size: ≥ 96×60pt
  ↳ Wooden button style
  ↳ Ref: navigation-bar-top_*.png
  
□ Volume button in top-right
  ↳ Speaker icon (🔊)
  ↳ Size: ≥ 60×60pt
  ↳ Wooden circular button
  ↳ Ref: sound-button-wooden_*.png
```

### Visual Tests - Characters
```
□ Bennie pointing animation
  ↳ Position: Right side
  ↳ Pointing at DU grid
  ↳ Verify brown #8C7259 ⚠️
  ↳ NO clothing ⚠️
  
□ Lemminge curious animation
  ↳ Position: Left side (1-2 Lemminge)
  ↳ Wide eyes, head tilted
  ↳ Verify BLUE #6FA8DC ⚠️
```

### Functional Tests - Voice & Intro
```
□ Voice plays on activity start:
  Part 1: Narrator: "Mach das Muster nach!"
    ↳ File: `narrator_puzzle_start.aac`
  Part 2: Bennie: "Das packen wir!"
    ↳ File: `bennie_puzzle_start.aac`
```

### Functional Tests - Gameplay
```
□ Tap color picker → Selects color
  ↳ Selected leaf shows glow
  ↳ Previously selected leaf glow removed
  ↳ Sound: `tap_wood.aac`
  
□ Tap empty cell → Fills with selected color
  ↳ Cell instantly shows color
  ↳ Sound: `tap_wood.aac`
  ↳ No animation (instant feedback)
  
□ Tap filled cell → Replaces with selected color
  ↳ Color changes instantly
  ↳ Sound: `tap_wood.aac`
  
□ Eraser mode:
  ↳ Tap eraser button → Enters eraser mode
  ↳ Eraser button shows glow
  ↳ Tap cell → Clears to gray
  ↳ Tap color → Exits eraser mode
  
□ Reset button:
  ↳ Tap reset → Confirmation dialog appears
  ↳ Confirm → All cells clear to gray
  ↳ Cancel → No change
  ↳ Sound: `tap_wood.aac`
```

### Functional Tests - Success
```
□ Pattern match detection:
  ↳ Real-time comparison (no "check" button)
  ↳ When DU matches ZIEL exactly → Success!
  
□ Success sequence:
  ↳ Sound: `success_chime.aac`
  ↳ Voice: Random from success pool
    • "Super!" / "Toll gemacht!" / "Wunderbar!" etc.
  ↳ Confetti animation plays
  ↳ Characters celebrate
  ↳ Coin flies to progress bar
  ↳ +1 coin added to balance
  
□ After success:
  ↳ Check if coins % 5 == 0
    - Yes → Show Celebration Overlay
    - No → Load next level automatically
  ↳ Transition delay: 2 seconds
```

### Hint System Tests
```
□ 10s no action:
  ↳ Bennie: "Wir können das, YouTube kommt bald."
  ↳ File: `bennie_puzzle_hint_10s.aac`
  ↳ Timer resets after child interacts
  
□ 20s no action:
  ↳ Bennie: "Welche Farbe fehlt noch?"
  ↳ File: `bennie_puzzle_hint_20s.aac`
  ↳ Timer resets after child interacts
  
□ Hints don't repeat
  ↳ If child is actively playing
  ↳ Timer only triggers if truly idle
```

### Difficulty Progression Tests
```
□ Level 1-5:
  ↳ Grid: 3×3
  ↳ Colors: 2 (green, yellow)
  ↳ Filled cells: 2-4
  
□ Level 6-10:
  ↳ Grid: 3×3
  ↳ Colors: 3 (add gray)
  ↳ Filled cells: 3-5
  
□ Level 11-20:
  ↳ Grid: 4×4
  ↳ Colors: 3
  ↳ Filled cells: 4-7
  
□ Level 21-30:
  ↳ Grid: 5×5
  ↳ Colors: 3-4
  ↳ Filled cells: 5-10
  
□ Level 31+:
  ↳ Grid: 6×6 (maximum)
  ↳ Colors: 4
  ↳ Filled cells: 6-12
```

---

## 5. Rätsel: Labyrinth

**📚 References:**
- Playbook: `../../docs/playbook/04-screens/home-activities.md` (Section 4)
- Reference Image: `../../design/references/screens/Reference_Layrinth_Game_Screen.png`
- Voice Script: `../../docs/playbook/03-voice-script.md` (Labyrinth section)

### Visual Tests
```
□ Labyrinth path renders with stone texture
  ↳ Winding path from START to ZIEL
  ↳ Path width visually clear (44pt minimum)
  ↳ Stone texture with subtle grain
  ↳ Grass areas around path
  
□ START marker clearly visible
  ↳ Wooden sign with "START" text
  ↳ Arrow pointing to path entrance
  ↳ Golden glow effect
  
□ ZIEL marker clearly visible
  ↳ Wooden sign with "ZIEL" text
  ↳ Position at path exit
  ↳ Golden glow effect
  
□ Bennie pointing at START
  ↳ Position: Near START marker
  ↳ Arm extended toward path
  ↳ Verify brown #8C7259 ⚠️
  
□ Lemminge scared at START
  ↳ Position: Next to Bennie
  ↳ Wide eyes, nervous expression
  ↳ Verify BLUE #6FA8DC ⚠️
  
□ Lemminge celebrating at ZIEL
  ↳ Position: At ZIEL marker
  ↳ Jumping, arms up
  ↳ Verify BLUE #6FA8DC ⚠️
```

### Functional Tests - Voice & Intro
```
□ Voice plays on activity start:
  Part 1: Narrator: "Hilf Bennie den Weg finden!"
    ↳ File: `narrator_labyrinth_start.aac`
  Part 2: Bennie: "Wie fange ich die Lemminge?"
    ↳ File: `bennie_labyrinth_start.aac`
```

### Functional Tests - Path Tracing
```
□ Tap START → Path tracing begins
  ↳ START marker pulses
  ↳ Touch feedback visible
  
□ Drag finger along path:
  ↳ Path highlights behind finger
  ↳ Highlight color: Success green (#99BF8C)
  ↳ Sound: `path_draw.aac` (looping)
  ↳ No lag in tracking
  
□ Stay on path:
  ↳ Continuous highlight
  ↳ Smooth tracking
  ↳ Works at different finger speeds
  
□ Leave path (stray outside):
  ↳ Highlight disappears
  ↳ Error state triggers
  ↳ Sound stops
  ↳ Bennie: "Da komme ich nicht durch."
  ↳ File: `bennie_labyrinth_wrong.aac`
  ↳ Can retry immediately (no penalty)
  ↳ Highlight clears
  
□ Reach ZIEL:
  ↳ Touch within 44pt of ZIEL marker
  ↳ Success celebration triggers
  ↳ Sound: `success_chime.aac`
  ↳ Voice: Random from success pool
  ↳ Confetti animation
  ↳ Coin flies to progress bar (+1)
```

### Touch Tracking Tests
```
□ Path detection accurate
  ↳ 44pt tolerance from path center
  ↳ Accounts for finger width
  
□ No false positives
  ↳ Straying outside path always detected
  ↳ Even at path corners
  
□ No false negatives
  ↳ Staying on path always recognized
  ↳ Even with shaky finger movement
  
□ Smooth tracking with no lag
  ↳ < 50ms delay from finger to highlight
  
□ Works with different finger speeds
  ↳ Slow tracing: accurate
  ↳ Fast tracing: accurate
  ↳ Variable speed: accurate
```

### Hint System Tests
```
□ 15s no action:
  ↳ Bennie: "Wo ist der Anfang?"
  ↳ File: `bennie_labyrinth_hint.aac`
  ↳ START marker pulses
```

---

## 6. Zahlen: Würfel (Dice)

**📚 References:**
- Playbook: `../../docs/playbook/04-screens/home-activities.md` (Section 5)
- Reference Image: `../../design/references/screens/Reference_Numbers_Game_Screen.png`
- Voice Script: `../../docs/playbook/03-voice-script.md` (Dice section)

### Visual Tests
```
□ Dice renders in center
  ↳ Large, clearly visible
  ↳ White dice with black dots
  ↳ 3D appearance with shadow
  
□ Dice animation plays on roll
  ↳ Tumbling animation (0.5s)
  ↳ Lands on random face (1-6)
  ↳ Spring easing for natural feel
  
□ Numbers 1-6 render on dice correctly
  ↳ Dots arranged in standard patterns:
    1: center
    2: diagonal
    3: diagonal + center
    4: corners
    5: corners + center
    6: two columns
  
□ Number buttons (1-10) on stone tablet
  ↳ Grid layout (4 columns)
  ↳ Each button ≥ 96×96pt
  ↳ Carved number appearance
  ↳ Font: SF Rounded Bold, 40pt
  
□ Bennie pointing
  ↳ Position: Right side
  ↳ Pointing at number buttons
  ↳ Verify brown #8C7259 ⚠️
  
□ Lemminge curious
  ↳ Position: Left side (1-2)
  ↳ Watching dice
  ↳ Verify BLUE #6FA8DC ⚠️
```

### Functional Tests - Voice & Intro
```
□ Voice plays on activity start:
  Part 1: Narrator: "Wirf den Würfel!"
    ↳ File: `narrator_dice_start.aac`
```

### Functional Tests - Dice Roll
```
□ Tap dice → Rolls animation
  ↳ Tumbling animation plays
  ↳ Haptic feedback (light impact)
  ↳ Sound: `dice_roll.aac`
  
□ Dice shows random number 1-6
  ↳ Truly random (use secure random)
  ↳ All numbers have equal probability
  ↳ No patterns or predictability
  
□ After dice settles:
  ↳ Narrator: "Zeig mir die [N]!"
  ↳ File: `narrator_show_number_[1-6].aac`
  ↳ [N] = number shown on dice
  ↳ Target number glows on button grid
```

### Functional Tests - Number Selection
```
□ Tap correct number → Success
  ↳ Sound: `success_chime.aac`
  ↳ Voice: Random from success pool
  ↳ Confetti animation
  ↳ Coin flies to progress bar (+1)
  ↳ Next dice roll automatically
  
□ Tap wrong number → Gentle correction
  ↳ Bennie: "Das ist die [X]. Probier nochmal!"
  ↳ File: `bennie_wrong_number.aac`
  ↳ [X] = number that was tapped
  ↳ Wrong number button shakes slightly
  ↳ Correct number continues glowing
  ↳ Can retry immediately (no penalty)
```

### Hint System Tests
```
□ 10s no action:
  ↳ Bennie: "Zähle die Punkte."
  ↳ File: `bennie_dice_hint_10s.aac`
  
□ 20s no action:
  ↳ Bennie: "Du hast die [N] gewürfelt."
  ↳ File: `bennie_dice_hint_20s.aac`
  ↳ [N] = current dice number
  
□ 30s no action:
  ↳ Bennie: "Wo ist die [N]?"
  ↳ File: `bennie_dice_hint_30s.aac`
  ↳ Target number pulses glow
```

### Edge Cases
```
□ Tap number before dice roll
  ↳ No effect (buttons disabled)
  ↳ No sound
  
□ Tap multiple numbers rapidly
  ↳ Only first tap registers
  ↳ Debounce: 300ms
  
□ Dice roll is truly random
  ↳ Test 100 rolls
  ↳ Each number appears ~16-17 times
  ↳ No patterns detectable
```

---

## 7. Zahlen: Wähle die Zahl

**📚 References:**
- Playbook: `../../docs/playbook/04-screens/home-activities.md` (Section 6)
- Reference Image: `../../design/references/screens/Reference_Numbers_Game_Screen.png`
- Voice Script: `../../docs/playbook/03-voice-script.md` (Choose Number section)

### Visual Tests
```
□ Stone tablet with numbers 1-10 carved in
  ↳ Grid layout (4 columns × 3 rows)
  ↳ Weathered stone texture
  ↳ Number outlines show trace paths
  
□ Number outlines show trace paths
  ↳ Carved groove appearance
  ↳ Path width: 30pt
  ↳ Numbers 1-10 in standard font
  
□ Arrow guides display on numbers
  ↳ Show stroke direction
  ↳ Color: Success green (#99BF8C)
  ↳ Animated subtle pulse
  ↳ Arrows per number:
    1: ↓
    2: ↷ ↓ →
    3: ↷ ↷
    4: ↓ → ↓
    5: ↓ ↷
    6: ↶ ○
    7: → ↘
    8: ∞
    9: ○ ↓
    10: Two separate (1 and 0)
  
□ Color picker at bottom (tracing colors)
  ↳ Optional feature for decoration
  ↳ Leaf-shaped buttons
  ↳ Colors: Green, Yellow, Gray
  
□ Eraser and reset buttons visible
  ↳ Same as Puzzle Matching
  ↳ Size: ≥ 60×60pt each
```

### Functional Tests - Voice & Intro
```
□ Voice plays on activity start:
  ↳ Narrator: "Zeig mir die [N]!"
  ↳ File: `narrator_choose_number_[1-10].aac`
  ↳ [N] = random number 1-10
```

### Functional Tests - Number Highlighting
```
□ Target number glows golden
  ↳ Glow effect around number outline
  ↳ Pulsing animation (1.0 → 1.1 scale, 1s loop)
  ↳ All other numbers remain normal
```

### Functional Tests - Tracing
```
□ Trace finger over number:
  ↳ Path validates in real-time
  ↳ Highlighted trail shows progress
  ↳ Color: Success green (#99BF8C)
  ↳ Trail width: 30pt
  ↳ Works with any tracing color selected
  
□ 70% coverage → Success
  ↳ Coverage = percentage of path covered
  ↳ Tolerance: 30pt from ideal path
  ↳ Does NOT need perfect tracing
  ↳ Child-friendly validation
  
□ < 70% coverage → Gentle prompt
  ↳ Bennie: "Versuch es nochmal."
  ↳ File: `bennie_wrong_choose.aac`
  ↳ Trace clears
  ↳ Can retry immediately
  
□ Success sequence:
  ↳ Sound: `success_chime.aac`
  ↳ Voice: Random from success pool
  ↳ Confetti animation
  ↳ Coin flies to progress bar (+1)
  ↳ New random number appears (1-10)
```

### Trace Validation Tests
```
□ Trace follows number shape closely
  ↳ Accounts for natural hand wobble
  ↳ 30pt tolerance generous
  
□ Arrows guide stroke direction
  ↳ Can start from any point (forgiving)
  ↳ Direction doesn't matter (forgiving)
  
□ Fast tracing works
  ↳ No lag in validation
  ↳ Coverage calculated accurately
  
□ Slow tracing works
  ↳ Trail stays visible
  ↳ Coverage accumulates
  
□ Can restart trace mid-way
  ↳ Lift finger → Trail clears
  ↳ Start again from any point
```

### Hint System Tests
```
□ 10s no action:
  ↳ Bennie: "Der Erzähler hat [N] gesagt."
  ↳ File: `bennie_choose_hint_10s.aac`
  ↳ [N] = target number
  
□ 20s no action:
  ↳ Bennie: "Wo ist die [N]?"
  ↳ File: `bennie_choose_hint_20s.aac`
  ↳ Target number pulses glow
```

---

## 8. Celebration Overlay

**📚 References:**
- Playbook: `../../docs/playbook/04-screens/celebration-treasure.md` (Section 1)
- Reference Image: `../../design/references/screens/Reference_Celebration_Overlay.png`
- Voice Script: `../../docs/playbook/03-voice-script.md` (Celebration section)

### Critical Design Principle
```
╔═══════════════════════════════════════════════════════════════════╗
║  CELEBRATION IS AN OVERLAY, NOT A SCREEN                         ║
║                                                                   ║
║  Context preservation: Activity screen visible beneath (dimmed)  ║
║  No jarring transitions: Child sees what they accomplished       ║
║  Autism-friendly: Reduces disorientation                         ║
╚═══════════════════════════════════════════════════════════════════╝
```

### Visual Tests - Trigger Condition
```
□ Triggers ONLY at 5-coin milestones
  ↳ Test: 5, 10, 15, 20, 25, 30... ✅
  ↳ Test: 1, 2, 3, 4, 6, 7, 8, 9, 11... ❌
  
□ Does NOT trigger at other coin counts
  ↳ Verify with manual coin manipulation
  ↳ Verify in automated tests
```

### Visual Tests - Overlay Appearance
```
□ Activity screen visible beneath
  ↳ Dimmed to 40% brightness
  ↳ Blur effect (10pt radius)
  ↳ Child can see completed puzzle/game
  
□ Celebration card centered on screen
  ↳ Size: 70% of screen width
  ↳ Background: Cream (#FAF5EB) @ 90% opacity
  ↳ Corner radius: 24pt
  ↳ Shadow: subtle, not harsh
  
□ Entry animation smooth
  ↳ Scale: 0.8 → 1.0
  ↳ Spring easing (response: 0.3)
  ↳ Duration: 0.4s
  ↳ No jarring pop-in
  
□ Confetti animation plays
  ↳ Full screen coverage
  ↳ Multicolor pieces
  ↳ Physics-based falling
  ↳ Duration: 3s
  ↳ Fades out at end
```

### Visual Tests - Characters
```
□ Bennie celebrating animation
  ↳ Both arms up high
  ↳ Jumping pose (one foot lifted)
  ↳ Big smile, squeezed-happy eyes
  ↳ Verify brown #8C7259 ⚠️
  ↳ NO clothing ⚠️
  
□ Lemminge celebrating animations
  ↳ 3 Lemminge total
  ↳ All jumping with arms up
  ↳ Huge smiles
  ↳ Verify BLUE #6FA8DC ⚠️
  ↳ Positioned around Bennie
```

### Visual Tests - Content
```
□ Success message displays
  ↳ "Super gemacht!" or similar
  ↳ Font: SF Rounded Bold, 32pt
  ↳ Color: Woodland (#738F66)
  
□ Coin display shows milestone
  ↳ 🪙 +1 (visual)
  ↳ Large, centered
  ↳ Golden glow effect
  
□ "Weiter →" button clearly visible
  ↳ Size: ≥ 180×60pt
  ↳ Wooden button style
  ↳ Centered at bottom of card
  ↳ Font: SF Rounded Semibold, 24pt
```

### Functional Tests - Voice
```
□ Voice plays appropriate milestone message:
  5 coins:
    ↳ Bennie: "Wir haben schon fünf Goldmünzen!"
    ↳ File: `bennie_celebration_5.aac`
  
  10 coins:
    ↳ Bennie: "Zehn Goldmünzen! Du kannst jetzt YouTube schauen."
    ↳ File: `bennie_celebration_10.aac`
  
  15 coins:
    ↳ Bennie: "Fünfzehn! Weiter so!"
    ↳ File: `bennie_celebration_15.aac`
  
  20 coins:
    ↳ Bennie: "Zwanzig Münzen! Du bekommst Bonuszeit!"
    ↳ File: `bennie_celebration_20.aac`
  
  25+ coins:
    ↳ Repeat 15-coin message
    ↳ Or create additional milestone messages
```

### Functional Tests - User Interaction
```
□ Haptic feedback on appearance
  ↳ Heavy impact
  ↳ Feels significant
  
□ Tap "Weiter" → Dismisses overlay
  ↳ Exit animation: scale 1.0 → 0.9
  ↳ Fade out
  ↳ Duration: 0.3s
  ↳ Activity screen brightens back to 100%
  
□ At 10+ coins → Auto-navigate to Treasure
  ↳ After "Weiter" tapped
  ↳ Transition: cross-fade (0.3s)
  ↳ Treasure Screen loads
  
□ At < 10 coins → Return to activity
  ↳ After "Weiter" tapped
  ↳ Next level loads automatically
  ↳ Difficulty may increase
```

### Context Preservation Tests
```
□ Activity screen visible beneath overlay
  ↳ Child sees completed puzzle
  ↳ Child sees finished labyrinth path
  ↳ Child sees rolled dice number
  ↳ Context is clear: "I did this!"
  
□ No jarring transition
  ↳ Overlay fades in smoothly
  ↳ No screen replacement
  ↳ No disorienting cuts
  
□ Activity state preserved after dismissal
  ↳ If returning to activity (< 10 coins)
  ↳ State resets for next level
  ↳ If navigating to Treasure (10+ coins)
  ↳ Activity state doesn't matter
```

---

## 9. Treasure Screen

**📚 References:**
- Playbook: `../../docs/playbook/04-screens/celebration-treasure.md` (Section 2)
- Reference Image: `../../design/references/screens/Reference_Treasure_Screen.png`
- Components: 
  - `../../design/references/components/treasure-chest-open.png`
  - `../../design/references/components/treasure-chest-closed.png`
- Voice Script: `../../docs/playbook/03-voice-script.md` (Treasure section)

### Visual Tests - Treasure Chest
```
□ Treasure chest in center
  ↳ Open state (lid raised)
  ↳ Golden glow effect
  ↳ Sparkles around chest
  ↳ Ref: treasure-chest-open.png
  
□ Coins spilling out of chest
  ↳ Golden coins visible
  ↳ Overflow appearance
  ↳ Slight animation (subtle bounce)
  
□ Coin counter at top
  ↳ 🪙 [X] Münzen
  ↳ Font: SF Rounded Bold, 28pt
  ↳ Color: CoinGold (#D9C27A)
  ↳ Shows current balance
```

### Visual Tests - YouTube Buttons
```
□ Two wooden buttons side-by-side:
  
  5 Min Button:
    ↳ Text: "▶️ 5 Min YouTube"
    ↳ Text: "🪙 10 Münzen"
    ↳ Size: ≥ 280×120pt
    ↳ Wooden plank with rope mount
    
  10 Min Button:
    ↳ Text: "▶️ 10 Min YouTube"
    ↳ Text: "🪙 20 Münzen"
    ↳ Size: ≥ 280×120pt
    ↳ Wooden plank with rope mount
```

### Visual Tests - Button States
```
□ Coins < 10:
  ↳ Both buttons grayed out
  ↳ Opacity: 60%
  ↳ X-pattern chains visible on both
  ↳ Padlock icons on both
  ↳ No glow effect
  
□ Coins 10-19:
  ↳ 5 Min button: Active (golden glow)
  ↳ 10 Min button: Grayed out (chains)
  
□ Coins ≥ 20:
  ↳ Both buttons: Active (golden glow)
  ↳ 10 Min button: Shows "BONUS!" badge
    - Badge color: Success green (#99BF8C)
    - Badge text: "+2 MIN"
    - Positioned top-right of button
```

### Visual Tests - Characters
```
□ Bennie gesturing toward chest
  ↳ Position: Left of chest
  ↳ Arm extended toward buttons
  ↳ Encouraging expression
  ↳ Verify brown #8C7259 ⚠️
  ↳ NO clothing ⚠️
  
□ Lemminge excited animations
  ↳ 2-3 Lemminge total
  ↳ Jumping, arms up
  ↳ Wide eyes, big smiles
  ↳ Verify BLUE #6FA8DC ⚠️
  ↳ Positioned around chest
```

### Visual Tests - UI Elements
```
□ "Zurück" button in top-left
  ↳ House icon (🏠) or ← arrow
  ↳ Size: ≥ 96×60pt
  ↳ Wooden button style
```

### Functional Tests - Voice
```
□ Voice on screen appear (coins < 10):
  ↳ Bennie: "Wir haben [X] Münzen. Noch [Y] bis YouTube!"
  ↳ File: `bennie_treasure_under10.aac`
  ↳ [X] = current coins
  ↳ [Y] = 10 - current coins
  
□ Voice on screen appear (coins 10-19):
  ↳ Bennie: "Wir können fünf Minuten schauen!"
  ↳ File: `bennie_treasure_over10.aac`
  
□ Voice on screen appear (coins ≥ 20):
  ↳ Bennie: "Wir können zwölf Minuten schauen!"
  ↳ File: `bennie_treasure_over20.aac`
  ↳ Emphasizes 12 minutes (10 + 2 bonus)
```

### Functional Tests - Button Interactions
```
□ Tap 5 Min button (coins ≥ 10):
  ↳ Deduct 10 coins from balance
  ↳ Coin counter updates immediately
  ↳ Sound: `chest_open.aac`
  ↳ Narrator: "Film ab!"
  ↳ File: `narrator_film_ab.aac`
  ↳ Navigate to Video Selection
  ↳ Timer set to: 5 minutes
  
□ Tap 10 Min button (coins ≥ 20):
  ↳ Deduct 20 coins from balance
  ↳ Coin counter updates immediately
  ↳ Sound: `chest_open.aac`
  ↳ Narrator: "Film ab!"
  ↳ File: `narrator_film_ab.aac`
  ↳ Navigate to Video Selection
  ↳ Timer set to: 12 minutes (10 + 2 bonus)
  
□ Tap disabled button (coins insufficient):
  ↳ No effect (button not clickable)
  ↳ No sound
  ↳ No error message (visual state is clear)
  
□ Tap "Zurück":
  ↳ Return to Home Screen
  ↳ Transition: cross-fade (0.3s)
  ↳ Coin balance unchanged
```

### State Tests
```
□ Coin balance updates immediately after deduction
  ↳ Visual counter changes
  ↳ Persistent storage updated
  ↳ Progress bar on activities reflects new balance
  
□ Button states update after deduction
  ↳ If balance drops below thresholds:
    - < 10: Both buttons become grayed/locked
    - 10-19: Only 5 Min active
    - ≥ 20: Both active
  
□ Chest button on Home Screen updates
  ↳ State reflects current balance
  ↳ Glow effect updates
  ↳ Tap behavior reflects state
  
□ Navigation back to Home shows updated coins
  ↳ Progress bar accurate
  ↳ Chest state accurate
  ↳ Character comments reference correct balance
```

---

## 10. Video Selection Screen

**📚 References:**
- Playbook: `../../docs/playbook/04-screens/video-parent.md` (Section 1)
- Voice Script: `../../docs/playbook/03-voice-script.md` (Video Selection section)

### Visual Tests - Layout
```
□ "Wähle ein Video!" title displays
  ↳ Wooden sign hanging from branch
  ↳ Font: SF Rounded Bold, 32pt
  
□ Grid of video thumbnails
  ↳ Layout: 2 rows × 3 columns (max 6 visible)
  ↳ Each thumbnail: 200×112pt (16:9 ratio)
  ↳ Grid spacing: 20pt between thumbnails
```

### Visual Tests - Video Cards
```
□ Each thumbnail card shows:
  ↳ Video image preview (cached from YouTube)
  ↳ Video title below image
  ↳ Title: 2 lines max, truncated with "..."
  ↳ Font: SF Rounded Medium, 16pt
  ↳ Wooden frame around card
  ↳ Corner radius: 12pt
  ↳ Shadow: subtle depth
```

### Visual Tests - UI Elements
```
□ Time remaining displays prominently
  ↳ Text: "Du hast [X] Minuten Zeit!"
  ↳ Font: SF Rounded Semibold, 24pt
  ↳ Color: Woodland (#738F66)
  ↳ Positioned at bottom center
  ↳ [X] = minutes granted (5 or 12)
  
□ Bennie encouraging animation
  ↳ Position: Left side
  ↳ Gesturing toward video grid
  ↳ Verify brown #8C7259 ⚠️
  
□ Lemminge excited animations
  ↳ Position: Bottom corners (2 Lemminge)
  ↳ Bouncing, anticipating video
  ↳ Verify BLUE #6FA8DC ⚠️
  
□ "Zurück" button in top-left
  ↳ Size: ≥ 96×60pt
  ↳ Wooden button style
  
□ Volume button in top-right
  ↳ Size: ≥ 60×60pt
  ↳ Wooden circular button
```

### Functional Tests - Video Loading
```
□ Only displays pre-approved videos
  ↳ From Parent Dashboard approved list
  ↳ NO random YouTube videos
  ↳ NO suggested videos
  ↳ NO search functionality
  
□ Thumbnails load correctly
  ↳ Cached from YouTube API
  ↳ Fallback placeholder if cache fails
  ↳ Loading indicator while fetching
  
□ Scroll works if > 6 videos
  ↳ Vertical scroll only
  ↳ Smooth scrolling (60fps)
  ↳ Bounce effect at top/bottom
```

### Functional Tests - Video Selection
```
□ Tap video thumbnail:
  ↳ Thumbnail scales slightly (feedback)
  ↳ Haptic feedback (light impact)
  ↳ Sound: `tap_wood.aac`
  ↳ Navigate to Video Player
  ↳ Selected video loads
  ↳ Timer starts immediately
  
□ Tap "Zurück":
  ↳ Return to Treasure Screen
  ↳ Transition: cross-fade (0.3s)
  ↳ Time NOT consumed (coins NOT deducted)
  ↳ Can select different redemption option
```

### Network Tests
```
□ Online mode:
  ↳ Thumbnails load from cache or network
  ↳ If cache empty, fetch from YouTube
  ↳ Show loading indicator during fetch
  ↳ Timeout after 10s if no response
  
□ Offline mode:
  ↳ Show only cached thumbnails
  ↳ If no cache: Show friendly message
    - "Keine Videos verfügbar"
    - "Bitte verbinde dich mit dem Internet"
  ↳ Bennie voice: "Wir brauchen Internet."
  ↳ Disable video cards (grayed out)
  
□ Network loss during thumbnail load:
  ↳ Show cached thumbnails
  ↳ Partially loaded: Use cached subset
  ↳ No cached: Show offline message
  
□ No approved videos configured:
  ↳ Show friendly message
    - "Keine Videos verfügbar"
    - "Bitte frage Mama oder Papa"
  ↳ "Zurück" button to return
```

### Edge Cases
```
□ Very long video titles
  ↳ Truncate to 2 lines
  ↳ Add "..." at end
  
□ Thumbnail load failure
  ↳ Show placeholder image
  ↳ Title still visible
  
□ Only 1 approved video
  ↳ Grid shows single card centered
  ↳ No scroll needed
  
□ More than 12 approved videos
  ↳ Scroll works smoothly
  ↳ All videos accessible
```

---

## 11. Video Player Screen

**📚 References:**
- Playbook: `../../docs/playbook/04-screens/video-parent.md` (Section 2)
- Voice Script: `../../docs/playbook/03-voice-script.md` (Video Player section)

### Visual Tests - YouTube Player
```
□ YouTube video plays embedded
  ↳ No YouTube controls visible
  ↳ No video info overlay
  ↳ No suggested videos at end
  ↳ No comments visible
  ↳ No channel subscribe button
  ↳ Full-screen video fills available space
  ↳ Maintains 16:9 aspect ratio
```

### Visual Tests - Analog Clock
```
□ Analog clock countdown displays prominently
  ↳ Position: Bottom center
  ↳ Size: 150×150pt
  ↳ Wooden frame (circular)
  ↳ Visible against video background
  
□ Clock face elements:
  ↳ Minute markers (12 marks)
  ↳ Hour markers bolder (every 3)
  ↳ Remaining time arc (fills counterclockwise)
  ↳ Arc color: Success green (#99BF8C)
  ↳ Arc width: 12pt
  ↳ Clock hand (single hand, not hour/minute)
  ↳ Center dot: CoinGold (#D9C27A)
  
□ Clock hand rotates to show progress
  ↳ Starts at 12 o'clock (top)
  ↳ Rotates clockwise as time elapses
  ↳ Smooth rotation (no ticking)
  
□ Text displays: "Noch [X] Minuten"
  ↳ Position: Below clock
  ↳ Font: SF Rounded Semibold, 20pt
  ↳ Color: Cream (#FAF5EB) with shadow
  ↳ Updates every minute
```

### Functional Tests - Video Playback
```
□ Video starts playing automatically
  ↳ No "play" button to tap
  ↳ Starts from beginning
  ↳ Audio plays at device volume
  
□ Timer starts counting down immediately
  ↳ Starts from granted time (5 or 12 min)
  ↳ Decrements in real-time
  ↳ 1-second precision
  
□ Clock updates every second
  ↳ Arc depletes counterclockwise
  ↳ Hand rotates clockwise
  ↳ Smooth animation (60fps)
  ↳ Text updates every 60 seconds
```

### Functional Tests - Time Warnings
```
□ 1 minute remaining:
  ↳ Bennie voice: "Noch eine Minute."
  ↳ File: `bennie_video_1min.aac`
  ↳ Clock pulses gently
    - Scale: 1.0 → 1.05
    - Duration: 0.5s
    - Repeat 3 times
  ↳ Haptic feedback (medium impact)
  ↳ Arc color changes to yellow (#D9C27A)
```

### Functional Tests - Time Up
```
□ Timer reaches 0:
  ↳ Video pauses immediately
  ↳ Sound: `gentle_bell.aac`
  ↳ Bennie voice: "Die Zeit ist um. Lass uns spielen!"
  ↳ File: `bennie_video_timeup.aac`
  ↳ Overlay appears: "Zeit ist um!" message
  ↳ Overlay semi-transparent
  ↳ After 3 seconds → Auto-navigate to Home Screen
  
□ No way to extend time
  ↳ By design - strict time limit
  ↳ No "5 more minutes" button
  
□ No way to restart video
  ↳ By design - one-time redemption
  ↳ Must earn more coins to watch again
```

### YouTube Integration Tests
```
□ Video plays without buffering issues
  ↳ Test with good network: smooth playback
  ↳ Test with slow network: may buffer, but plays
  
□ Video quality adjusts to network
  ↳ Auto quality setting enabled
  ↳ Starts at lower quality, upgrades if bandwidth allows
  
□ No related videos shown at end
  ↳ Player config: `rel=0`
  ↳ Black screen when video ends
  
□ No autoplay to next video
  ↳ Player config: no autoplay
  ↳ Video stops at end
  
□ No annotations or cards overlay
  ↳ Player config: `iv_load_policy=3`
  ↳ Clean viewing experience
  
□ Player respects time limit strictly
  ↳ Even if video is longer than time
  ↳ Even if video ends before time
  ↳ Timer is authoritative, not video length
```

### App Lifecycle Tests
```
□ Background app:
  ↳ Video pauses
  ↳ Timer pauses
  ↳ State preserved
  
□ Resume app:
  ↳ Video resumes from same point
  ↳ Timer resumes countdown
  ↳ No time lost
  
□ Lock screen:
  ↳ Video pauses
  ↳ Timer pauses
  ↳ Unlock → Resume
  
□ Low power mode:
  ↳ Video continues playing
  ↳ Timer remains accurate
  ↳ Clock animation may reduce to 30fps
  
□ Network loss mid-video:
  ↳ Video buffering indicator
  ↳ If buffer empty: Show error overlay
  ↳ Error: "Verbindung verloren"
  ↳ After 5s no reconnect → Return to Home
  ↳ Time NOT consumed (coins NOT deducted retroactively)
```

### Edge Cases
```
□ Video shorter than granted time:
  ↳ Video ends, screen goes black
  ↳ Timer continues until 0
  ↳ Child can watch video multiple times in window
  
□ Video longer than granted time:
  ↳ Video stops mid-playback when timer hits 0
  ↳ Expected behavior, not a bug
  
□ Skip ahead/back in video:
  ↳ Not possible (controls disabled)
  ↳ Must watch from start
  
□ Rapid app switching:
  ↳ Video pauses on every switch
  ↳ Timer pauses on every switch
  ↳ State always preserved
```

---

## 12. Parent Gate

**📚 References:**
- Playbook: `../../docs/playbook/04-screens/video-parent.md` (Section 3)
- Design: Math question overlay to prevent child access

### Visual Tests
```
□ Math question displays clearly
  ↳ Question format: "[A] + [B] = ?"
  ↳ Font: SF Rounded Bold, 36pt
  ↳ [A] and [B] range: 5-15
  ↳ Color: Wood Dark (#6B4423)
  
□ Number input field has focus
  ↳ Keyboard appears automatically
  ↳ Number pad keyboard (digits 0-9)
  ↳ Field shows placeholder: "___"
  ↳ Large input font: 32pt
  
□ "Abbrechen" button visible
  ↳ Position: Bottom-left
  ↳ Size: ≥ 120×60pt
  ↳ Wooden button style
  ↳ Text: "Abbrechen"
  
□ "Bestätigen" button visible
  ↳ Position: Bottom-right
  ↳ Size: ≥ 120×60pt
  ↳ Wooden button style
  ↳ Text: "Bestätigen"
  
□ Background dimmed
  ↳ Semi-transparent overlay (60% black)
  ↳ Blurs background slightly (10pt radius)
  ↳ Home Screen visible beneath
```

### Visual Tests - Error State
```
□ Error message displays when wrong
  ↳ Text: "Versuch es nochmal"
  ↳ Font: SF Rounded Medium, 20pt
  ↳ Color: Red (#CC0000) - exception to no-red rule
  ↳ Position: Below input field
  ↳ Appears with fade-in animation
  ↳ Disappears after 2 seconds
```

### Functional Tests - Question Generation
```
□ Question generates random addition
  ↳ Both numbers: 5-15 range
  ↳ Sum: Always < 31 (max two digits)
  ↳ New question each time gate shown
  ↳ Example questions:
    - "7 + 8 = ?"
    - "12 + 9 = ?"
    - "5 + 15 = ?"
```

### Functional Tests - Answer Validation
```
□ Correct answer:
  ↳ Input matches sum exactly
  ↳ Success feedback (haptic: light)
  ↳ Dismiss gate immediately
  ↳ Navigate to Parent Dashboard
  ↳ Transition: fade (0.3s)
  
□ Wrong answer:
  ↳ Error message appears: "Versuch es nochmal"
  ↳ Input field clears (resets to empty)
  ↳ Error disappears after 2 seconds
  ↳ Can retry immediately
  ↳ No penalty for wrong answers
  
□ 3 wrong answers:
  ↳ Generate new question
  ↳ Different numbers
  ↳ Reset attempt counter
  ↳ No lockout (child-proof, not parent-proof)
  
□ Tap "Abbrechen":
  ↳ Dismiss gate immediately
  ↳ Return to Home Screen
  ↳ No navigation to dashboard
  
□ Tap "Bestätigen" with empty input:
  ↳ No effect (button disabled)
  ↳ Or: Show error "Bitte gib eine Zahl ein"
```

### Edge Cases
```
□ Rapid tap "Bestätigen":
  ↳ Debounced (300ms)
  ↳ Only one check per tap
  ↳ Prevents double-submission
  
□ Very large numbers entered:
  ↳ Input validation: max 2 digits
  ↳ Cannot enter 3+ digit numbers
  
□ Non-numeric input:
  ↳ Impossible (number pad keyboard)
  ↳ Only digits 0-9 available
  
□ Correct answer after 2 wrong attempts:
  ↳ Still succeeds (no lockout)
  ↳ Navigate to dashboard normally
  
□ Background app during gate:
  ↳ Gate remains visible on resume
  ↳ Input field retains value
  ↳ Attempt counter persists
```

---

## 13. Parent Dashboard

**📚 References:**
- Playbook: `../../docs/playbook/04-screens/video-parent.md` (Section 4)
- Design: Settings and monitoring interface for parents

### Visual Tests - Header
```
□ "⚙️ Elternbereich" title displays
  ↳ Position: Top center
  ↳ Font: SF Rounded Bold, 32pt
  ↳ Color: Wood Dark (#6B4423)
  
□ "Zurück" button in top-left
  ↳ Size: ≥ 96×60pt
  ↳ Wooden button style
  ↳ Text or icon: ← or "Zurück"
```

### Visual Tests - Player Cards
```
□ Player cards for Alexander and Oliver
  ↳ Each card: Full width, stacked vertically
  ↳ Card height: ~250pt
  ↳ Card background: Cream (#FAF5EB)
  ↳ Card border: Woodland (#738F66), 2pt
  ↳ Corner radius: 16pt
  ↳ Shadow: subtle depth
  
□ Each card shows avatar emoji
  ↳ Size: 60×60pt
  ↳ Position: Top-left of card
  
□ Each card shows name
  ↳ Font: SF Rounded Bold, 28pt
  ↳ Position: Next to avatar
  
□ Each card shows play time today
  ↳ Text: "Heute gespielt: [X] min / [Y] min"
  ↳ Font: SF Rounded Medium, 20pt
  ↳ [X] = minutes played today
  ↳ [Y] = daily limit
  ↳ Progress bar below text
  
□ Progress bar visualization
  ↳ Background: Gray (#CCCCCC)
  ↳ Fill: Success green (#99BF8C) if < 80%
  ↳ Fill: Yellow (#D9C27A) if 80-100%
  ↳ Fill: Red (#CC0000) if > 100%
  ↳ Percentage text: "[X]%"
  ↳ Width: Full card width minus padding
  ↳ Height: 20pt
  
□ Each card shows coin count
  ↳ Text: "Münzen: [X]"
  ↳ Font: SF Rounded Semibold, 24pt
  ↳ Icon: 🪙
  
□ Each card shows activity toggles
  ↳ Label: "Aktivitäten:"
  ↳ Four toggles in a row:
    - Rätsel
    - Zahlen
    - Zeichnen
    - Logik
  ↳ Toggle style: iOS switch
  ↳ On: Woodland (#738F66)
  ↳ Off: Gray (#999999)
  
□ Each card shows reset button
  ↳ Position: Bottom-right of card
  ↳ Size: ≥ 100×40pt
  ↳ Background: Red (#CC0000)
  ↳ Text: "Zurücksetzen" or trash icon (🗑️)
  ↳ Font: SF Rounded Semibold, 16pt
  ↳ Color: White
```

### Functional Tests - Player Cards
```
□ Play time displays correctly
  ↳ Updates from actual gameplay data
  ↳ Resets at midnight (daily counter)
  ↳ Persists through app restarts
  
□ Progress bar fills proportionally
  ↳ 30 min played / 60 min limit = 50% filled
  ↳ Color changes based on percentage
  
□ Coin count matches actual player data
  ↳ Updates immediately when child earns coins
  ↳ Updates immediately when coins spent
  
□ Activity toggles show correct state
  ↳ On: Activity unlocked in game
  ↳ Off: Activity locked in game (chains shown)
  
□ Tap activity toggle:
  ↳ State changes immediately
  ↳ Haptic feedback (light impact)
  ↳ Change persists (saves to storage)
  ↳ Locked activity not accessible in game
  ↳ Unlocked activity accessible in game
  ↳ Changes take effect immediately (no app restart)
  
□ Tap reset button:
  ↳ Confirmation alert appears
  ↳ Alert text: "Fortschritt zurücksetzen?"
  ↳ Alert message: "Alle Münzen, Level und Spielzeit werden gelöscht."
  ↳ Two buttons: "Abbrechen" (gray) and "Zurücksetzen" (red)
  
□ Confirm reset:
  ↳ All player progress cleared:
    - Coins → 0
    - Activity levels → 1
    - Today's play time → 0
    - Learning profile → reset to defaults
  ↳ Card updates immediately
  ↳ Coin counter in game reflects reset
  ↳ Home Screen chest shows 0 coins
```

### Visual Tests - Video Management Section
```
□ Section title: "📺 Genehmigte Videos"
  ↳ Font: SF Rounded Bold, 24pt
  
□ "Videos bearbeiten" button in header
  ↳ Position: Right side of section header
  ↳ Size: ≥ 120×40pt
  ↳ Wooden button style
  ↳ Text: "Bearbeiten"
  
□ Video list displays all approved videos
  ↳ Each video row:
    - Thumbnail (80×45pt)
    - Title (truncated if long)
    - Remove button (🗑️ icon, red)
  ↳ Row height: 60pt
  ↳ Separator line between rows
  
□ "+ Video hinzufügen" button at bottom
  ↳ Size: Full width, 60pt height
  ↳ Background: Woodland (#738F66)
  ↳ Text: "+ Video hinzufügen"
  ↳ Font: SF Rounded Semibold, 20pt
  ↳ Color: White
```

### Functional Tests - Video Management
```
□ List displays all approved videos
  ↳ Sorted by date added (newest first)
  ↳ Thumbnail images load correctly
  ↳ Titles display (1 line, truncated with "...")
  
□ Video thumbnails load correctly
  ↳ Fetched from YouTube API
  ↳ Cached locally
  ↳ Placeholder if fetch fails
  
□ Tap "Videos bearbeiten":
  ↳ Navigate to Video Management screen
  ↳ Transition: push right-to-left
  
□ Tap "+ Video hinzufügen":
  ↳ Navigate to Add Video screen
  ↳ Transition: modal (slides up from bottom)
  
□ Tap remove button (🗑️):
  ↳ Confirmation alert appears
  ↳ Alert text: "Video entfernen?"
  ↳ Alert message: "[Video Title] wird aus der Liste entfernt."
  ↳ Two buttons: "Abbrechen" and "Entfernen" (red)
  
□ Confirm remove:
  ↳ Video deleted from approved list
  ↳ Video row disappears (fade out animation)
  ↳ List updates immediately
  ↳ Removed video NOT available in game
  ↳ Change persists (saves to storage)
```

### Add Video Screen Tests
```
□ URL input field displays
  ↳ Placeholder: "YouTube Link einfügen..."
  ↳ Keyboard: URL keyboard type
  ↳ Large input field (full width)
  
□ "Einfügen aus Zwischenablage" button
  ↳ Size: Full width, 50pt height
  ↳ Position: Below input field
  ↳ Only enabled if clipboard contains URL
  
□ Video preview section
  ↳ Initially hidden (no video yet)
  ↳ Appears after valid URL entered
  
□ "Abbrechen" and "Hinzufügen" buttons
  ↳ Bottom of screen
  ↳ Abbrechen: Gray
  ↳ Hinzufügen: Woodland green (disabled until valid)
```

### Add Video Functionality Tests
```
□ Paste YouTube URL:
  ↳ Accepts: youtube.com/watch?v=XXX
  ↳ Accepts: youtu.be/XXX
  ↳ Accepts: youtube.com/embed/XXX
  ↳ Extracts video ID correctly
  
□ Invalid URL:
  ↳ Show error: "Ungültiger YouTube Link"
  ↳ Error color: Red (#CC0000)
  ↳ "Hinzufügen" button remains disabled
  
□ Valid URL:
  ↳ Fetch video metadata (title, thumbnail)
  ↳ Show loading indicator during fetch
  ↳ Video preview appears:
    - Thumbnail image
    - Video title
    - Duration (if available)
  ↳ "Hinzufügen" button becomes enabled
  
□ Tap "Hinzufügen":
  ↳ Save video to approved list
  ↳ Video appears in Video Selection screen
  ↳ Dismiss Add Video screen (modal down)
  ↳ Return to Parent Dashboard
  ↳ New video visible in list
  
□ Tap "Abbrechen":
  ↳ Dismiss without saving
  ↳ Return to Parent Dashboard
```

### Visual Tests - Time Limit Section
```
□ Section title: "⏱️ Tägliche Spielzeit"
  ↳ Font: SF Rounded Bold, 24pt
  
□ Time limit row for each player
  ↳ Label: "[Player name]:"
  ↳ Dropdown menu showing current limit
  ↳ Dropdown options:
    - 30 min
    - 45 min
    - 60 min (default)
    - 75 min
    - 90 min
    - 120 min
```

### Functional Tests - Time Limits
```
□ Dropdown shows current limit
  ↳ Default: 60 min
  ↳ Matches player's actual limit
  
□ Tap dropdown:
  ↳ Menu opens (iOS picker style)
  ↳ Shows all time options
  
□ Select new time limit:
  ↳ Dropdown updates immediately
  ↳ Change saves to player data
  ↳ Change takes effect immediately
  ↳ Progress bar on player card updates
  
□ Time limit enforced in game:
  ↳ (Future phase - not MVP)
  ↳ Gentle reminder at 80% of limit
  ↳ Final reminder at 95% of limit
  ↳ Graceful exit at 100% of limit
```

### Navigation Tests
```
□ Tap "Zurück" button:
  ↳ Dismiss Parent Gate (if came from settings)
  ↳ Return to Home Screen
  ↳ Transition: fade out
  ↳ All changes saved and persisted
```

---

## 14. Cross-Screen Integration Tests

**📚 References:**
- Playbook: `../../docs/playbook/02-screen-flow.md`

### Navigation Flow Tests
```
□ Loading → Player Selection → Home (full cycle):
  ↳ No crashes
  ↳ All voice lines play correctly
  ↳ All transitions smooth
  ↳ Player data loads correctly
  ↳ Time: < 10 seconds total
  
□ Home → Activity → Celebration → Activity (loop):
  ↳ Activity loads quickly (< 0.5s)
  ↳ Celebration triggers at correct milestones
  ↳ Return to activity seamless
  ↳ Next level loads automatically
  
□ Home → Treasure (10+ coins) → Video Selection → Video Player → Home:
  ↳ Coin deduction accurate
  ↳ Timer starts correctly
  ↳ Video plays without issues
  ↳ Time-up returns to Home gracefully
  ↳ Coin balance persists
  
□ Home → Settings → Parent Gate → Parent Dashboard → Home:
  ↳ Math question appears
  ↳ Correct answer grants access
  ↳ Dashboard loads with current data
  ↳ Changes made persist
  ↳ Return to Home shows updated state
```

### State Persistence Tests
```
□ Close app → Reopen:
  ↳ Player data persists
  ↳ Coin count correct
  ↳ Activity progress saved
  ↳ Today's play time carries over
  ↳ Returns to Player Selection screen
  
□ Background app → Resume:
  ↳ State intact (no data loss)
  ↳ If in activity: Activity state preserved
  ↳ If watching video: Video paused, timer paused
  ↳ If on Home: Home Screen visible
  
□ Memory warning:
  ↳ App continues running
  ↳ No data loss
  ↳ State intact
  ↳ May clear some cached assets (non-critical)
```

### Coin Economy Tests
```
□ Complete activity → +1 coin:
  ↳ Coin flies to progress bar
  ↳ Animation smooth (0.8s)
  ↳ Progress bar updates immediately
  ↳ Count increments by exactly 1
  
□ Progress bar updates in real-time:
  ↳ Fill level changes
  ↳ Coin slots show filled coins
  ↳ Matches actual count exactly
  
□ Celebration triggers at correct milestones:
  ↳ 5 coins: ✅
  ↳ 10 coins: ✅
  ↳ 15 coins: ✅
  ↳ 20 coins: ✅
  ↳ Other counts: ❌
  
□ Treasure chest button state updates:
  ↳ < 10 coins: Closed, no glow
  ↳ 10-19 coins: Open, golden glow
  ↳ 20+ coins: Open, glow + sparkles
  ↳ State changes immediately after earning coin
  
□ YouTube redemption deducts correct amount:
  ↳ 5 min: -10 coins exactly
  ↳ 10 min: -20 coins exactly
  ↳ Coin counter updates immediately
  ↳ Button states update after deduction
  
□ Coin balance never goes negative:
  ↳ Buttons disabled if insufficient coins
  ↳ No way to spend coins you don't have
  
□ Multiple coins earned in succession:
  ↳ No race conditions
  ↳ Each coin animation queues properly
  ↳ Final count accurate (no lost coins)
  ↳ Example: Complete 3 activities rapidly
    - Coin count: 0 → 1 → 2 → 3 ✅
    - Not: 0 → 2 (skipped) ❌
```

---

## 15. Audio Integration Tests

**📚 References:**
- Playbook: `../../docs/playbook/06-animation-sound.md`
- Voice Script: `../../docs/playbook/03-voice-script.md`

### Music Channel Tests
```
□ Background music starts on app launch:
  ↳ File: `forest_ambient.aac`
  ↳ Starts playing automatically
  ↳ No delay (preloaded)
  
□ Music volume: 30% (default):
  ↳ Measured relative to system volume
  ↳ Comfortable background level
  
□ Music loops infinitely without gaps:
  ↳ Seamless loop transition
  ↳ No click or pop at loop point
  ↳ Plays continuously through all screens
  
□ Music ducks to 15% when voice plays:
  ↳ Fade down animation (0.2s)
  ↳ Music doesn't stop, just quieter
  ↳ Voice clearly audible over music
  
□ Music returns to 30% after voice completes:
  ↳ Fade up animation (0.3s)
  ↳ Smooth transition, no jarring jump
```

### Voice Channel Tests
```
□ All voice lines play at 100% volume:
  ↳ Measured relative to system volume
  ↳ Always loudest audio element
  
□ Voice has highest priority:
  ↳ Always plays when triggered
  ↳ Never interrupted by effects
  ↳ Music ducks during voice
  ↳ Effects queue during voice
  
□ Music ducks during voice (verified):
  ↳ Music volume: 30% → 15%
  ↳ Fade down starts before voice starts
  ↳ Fade up completes after voice ends
  
□ Effects queued if voice playing:
  ↳ Effect plays after voice completes
  ↳ Queue preserves order (FIFO)
  ↳ No effect interrupts voice
  
□ Voice files load without delay:
  ↳ All voice files preloaded at launch
  ↳ Playback starts < 50ms after trigger
  
□ Voice playback speed: 85%:
  ↳ Slightly slower than normal
  ↳ Easier for children to understand
  ↳ Sounds natural, not robotic
  
□ German pronunciation correct for all lines:
  ↳ Narrator voice: Clear, neutral
  ↳ Bennie voice: Warm, bear-like
  ↳ Numbers pronounced correctly (1-10)
  ↳ Names pronounced correctly (Alexander, Oliver)
  ↳ No mispronunciations or odd inflections
```

### Effects Channel Tests
```
□ Button tap sound plays correctly:
  ↳ File: `tap_wood.aac`
  ↳ Duration: 0.1s
  ↳ Sound: Wooden knock
  ↳ Volume: 70%
  
□ Correct answer sound plays correctly:
  ↳ File: `success_chime.aac`
  ↳ Duration: 0.5s
  ↳ Sound: Gentle bell chime
  ↳ Volume: 70%
  
□ Coin collect sound plays correctly:
  ↳ File: `coin_collect.aac`
  ↳ Duration: 0.3s
  ↳ Sound: Metallic clink
  ↳ Volume: 70%
  
□ Celebration sound plays correctly:
  ↳ File: `celebration_fanfare.aac`
  ↳ Duration: 2s
  ↳ Sound: Full fanfare
  ↳ Volume: 70%
  
□ Chest open sound plays correctly:
  ↳ File: `chest_open.aac`
  ↳ Duration: 1s
  ↳ Sound: Creaky wood
  ↳ Volume: 70%
  
□ Wrong answer sound plays correctly:
  ↳ File: `gentle_boop.aac`
  ↳ Duration: 0.2s
  ↳ Sound: Soft boop (not harsh)
  ↳ Volume: 70%
  ↳ NOT punishing or scary
  
□ Effects queue if voice playing:
  ↳ Effect waits for voice to finish
  ↳ Then plays immediately
  ↳ No stacking (only plays once)
```

### Audio Priority Tests
```
□ Voice + Music:
  ↳ Music ducks to 15%
  ↳ Voice plays at 100%
  ↳ Music returns to 30% after voice
  
□ Voice + Effects:
  ↳ Effects queue (wait for voice)
  ↳ Voice plays first
  ↳ Effects play after voice completes
  
□ Voice + Music + Effects:
  ↳ Music ducks to 15%
  ↳ Voice plays at 100%
  ↳ Effects queue
  ↳ After voice: Music returns to 30%, effects play
  
□ Multiple voices queued:
  ↳ Play in order (FIFO)
  ↳ No overlap
  ↳ No skipping
  
□ Multiple effects queued:
  ↳ Play in order (FIFO)
  ↳ No overlap
  ↳ Fast succession: slight delay between (50ms)
```

### App Lifecycle Audio Tests
```
□ Background app:
  ↳ All audio pauses
  ↳ Music pauses
  ↳ Voice pauses (if playing)
  ↳ Effects paused
  
□ Resume app:
  ↳ Audio resumes from same point
  ↳ Music continues from pause point
  ↳ Voice continues (if was playing)
  ↳ Effects queue preserved
  
□ Interrupt (phone call):
  ↳ All audio pauses immediately
  ↳ No audio during call
  
□ End interrupt:
  ↳ Audio resumes automatically
  ↳ No user action required
  
□ Silent mode (hardware switch):
  ↳ Respects system setting
  ↳ No audio in silent mode
  ↳ Visual feedback still works
  
□ Volume buttons:
  ↳ Control all audio channels equally
  ↳ Maintains relative volumes
  ↳ Volume slider in Control Center works
```

---

## 16. Accessibility Tests

**📚 References:**
- Playbook: `../../docs/playbook/05-technical-requirements.md` (Section 5.7)

### VoiceOver Tests
```
□ All buttons have descriptive labels:
  ↳ Activity buttons: "Rätsel spielen", "Zahlen spielen"
  ↳ Player buttons: "Alexander wählen", "Oliver wählen"
  ↳ Navigation: "Zurück zur Startseite", "Einstellungen"
  ↳ YouTube buttons: "5 Minuten YouTube", "10 Minuten YouTube"
  
□ All screens have page titles:
  ↳ Loading: "Spiel lädt"
  ↳ Player Selection: "Spieler auswählen"
  ↳ Home: "Waldabenteuer"
  ↳ Activities: "[Activity name]"
  ↳ Treasure: "Schatzkiste"
  ↳ Parent Dashboard: "Elternbereich"
  
□ Navigation order is logical:
  ↳ Left-to-right, top-to-bottom
  ↳ VoiceOver swipe follows expected order
  ↳ No random jumps
  
□ Grid cells announce position and state:
  ↳ "Reihe 1, Spalte 2, Gelb"
  ↳ "Reihe 3, Spalte 1, Leer"
  ↳ Pattern clear from announcements
  
□ Progress bar announces progress:
  ↳ "[X] von 10 Münzen gesammelt"
  ↳ Updates after each coin earned
  
□ Activity cards announce name and locked state:
  ↳ "Rätsel, entsperrt"
  ↳ "Logik, gesperrt"
  
□ Celebration overlay announces milestone:
  ↳ "Fünf Münzen erreicht! Weiter"
  ↳ "Zehn Münzen erreicht! YouTube verfügbar"
  
□ Video thumbnails announce title:
  ↳ "[Video Title], zum Abspielen tippen"
  
□ Parent gate announces question:
  ↳ "[A] plus [B] gleich wie viel?"
  
□ Form inputs have labels:
  ↳ Math input: "Antwort"
  ↳ Video URL: "YouTube Link"
```

### Haptic Feedback Tests
```
□ Button tap → Light impact:
  ↳ All wooden buttons
  ↳ Activity signs
  ↳ Player cards
  ↳ Color picker buttons
  
□ Correct answer → Success notification:
  ↳ Puzzle match
  ↳ Labyrinth complete
  ↳ Correct dice number
  ↳ Correct number trace
  
□ Coin earned → Medium impact:
  ↳ When coin flies to progress bar
  ↳ Feels significant
  
□ Wrong answer → Soft notification:
  ↳ Wrong dice number
  ↳ Wrong labyrinth path
  ↳ NOT harsh or punishing
  
□ Celebration → Heavy impact:
  ↳ 5-coin milestones
  ↳ Feels like achievement
  
□ 1 min warning → Medium impact:
  ↳ During video playback
  ↳ Attention-grabbing
```

### Color Contrast Tests
```
□ All text has 4.5:1 contrast minimum:
  ↳ Use WCAG contrast checker
  ↳ Test on actual device (not just simulator)
  
□ Button text readable on wood background:
  ↳ White text on medium wood: ✅
  ↳ Dark text on light wood: ✅
  
□ Grid cells distinguishable when empty/filled:
  ↳ Empty: Gray stone texture visible
  ↳ Filled: Color clearly different from empty
  ↳ Colors distinguishable from each other
  
□ Progress bar fill visible against background:
  ↳ Green fill (#99BF8C) on dark wood: ✅
  ↳ Clear boundary between filled/empty
  
□ Locked activity chains clearly visible:
  ↳ Dark chains on dimmed sign: ✅
  ↳ Padlock icon readable
  
□ Error messages readable:
  ↳ Red text on cream background: ✅
  ↳ Sufficient contrast
```

### Color Blindness Considerations
```
□ Add shape indicators to colors:
  ↳ Green: Circle ○
  ↳ Yellow: Square □
  ↳ Gray: Triangle △
  ↳ Shapes visible in grid cells
  
□ Progress bar texture pattern in fill:
  ↳ Diagonal stripes or dots
  ↳ Distinguishable from empty
  
□ Grid colors have different shapes:
  ↳ Not relying only on color
  ↳ Shapes overlay color fills
```

### Reduce Motion Tests
```
□ Confetti animation can be disabled:
  ↳ System Setting: Reduce Motion ON
  ↳ Result: No confetti, simple fade
  
□ Character animations can be disabled:
  ↳ System Setting: Reduce Motion ON
  ↳ Result: Static poses (no breathing)
  
□ Coin fly animation can be simplified:
  ↳ System Setting: Reduce Motion ON
  ↳ Result: Instant jump to progress bar
  
□ Screen transitions can be instant:
  ↳ System Setting: Reduce Motion ON
  ↳ Result: No fade, instant cut
  
□ Progress bar fill can be instant:
  ↳ System Setting: Reduce Motion ON
  ↳ Result: No animation, instant fill
```

---

## 17. Performance Tests

**📚 References:**
- Playbook: `../../docs/playbook/05-technical-requirements.md` (Section 5.6)

### Frame Rate Tests (Target: 60fps)
```
□ All screens maintain 60fps:
  ↳ Use Instruments: Core Animation tool
  ↳ Measure during typical gameplay
  ↳ Loading: ✅
  ↳ Home: ✅
  ↳ Activities: ✅
  ↳ Celebration: ✅
  ↳ Video Player: ✅ (clock animation)
  
□ Scrolling is smooth:
  ↳ Video Selection screen
  ↳ Parent Dashboard
  ↳ No stuttering or frame drops
  
□ Animations play at target frame rate:
  ↳ Character animations: 30fps (intentional)
  ↳ UI animations: 60fps
  ↳ Confetti: 60fps
  ↳ No visible lag
  
□ Character animations don't drop frames:
  ↳ Bennie breathing: smooth loop
  ↳ Lemminge bouncing: smooth loop
  ↳ Celebration jumps: smooth
  
□ Grid interactions don't cause lag:
  ↳ Tap cell: < 100ms response
  ↳ Color change: instant
  ↳ Pattern validation: < 50ms
  
□ Video playback smooth:
  ↳ 30fps or 60fps (depends on video)
  ↳ No dropped frames
  ↳ Clock animation: 60fps
```

### Memory Tests (Target: < 200MB peak)
```
□ App launch: < 50MB:
  ↳ Use Xcode Memory Debugger
  ↳ Measure after splash screen
  
□ Home screen: < 80MB:
  ↳ After player selection
  ↳ All assets loaded
  
□ Activity screen: < 120MB:
  ↳ During gameplay
  ↳ Characters animated
  
□ Celebration: < 150MB:
  ↳ With confetti effect
  ↳ Peak usage
  
□ Video player: < 200MB (peak):
  ↳ Including video buffer
  ↳ Including clock animation
  ↳ Acceptable peak
  
□ No memory leaks after 30 minutes of play:
  ↳ Use Instruments: Leaks tool
  ↳ Play through all activities
  ↳ Watch video multiple times
  ↳ Memory should not continuously grow
  
□ No memory leaks after 100 screen transitions:
  ↳ Navigate Home → Activity → Home (loop 100x)
  ↳ Memory should stabilize, not grow
```

### Loading Time Tests
```
□ Cold start: < 2 seconds to Loading Screen:
  ↳ Time from icon tap to Loading Screen visible
  ↳ Includes splash screen
  
□ Loading Screen to Player Select: < 3 seconds:
  ↳ Total loading time (fake + real)
  ↳ All assets preloaded
  
□ Player Select to Home: < 1 second:
  ↳ Fast transition
  ↳ Player data loads quickly
  
□ Activity load: < 0.5 seconds:
  ↳ Home → Activity
  ↳ Activity ready to play
  
□ Video selection load: < 1 second (with network):
  ↳ Thumbnails load from cache or network
  ↳ Acceptable if network slow
```

### Battery Tests
```
□ 30 min gameplay: < 15% battery drain:
  ↳ Mix of activities
  ↳ No video playback
  ↳ Test on iPad at 100% charge
  
□ Video playback (10 min): < 8% battery drain:
  ↳ Continuous playback
  ↳ Clock animation running
  
□ Idle on Home Screen (5 min): < 1% battery drain:
  ↳ Music playing
  ↳ Character animations running
  ↳ Minimal battery usage
```

---

## 18. Edge Case Tests

### Network Edge Cases
```
□ No internet on launch:
  ↳ Offline mode works
  ↳ All activities accessible
  ↳ Parent Dashboard accessible
  ↳ Only YouTube unavailable (expected)
  
□ Internet loss during video selection:
  ↳ Show error message
  ↳ Bennie: "Wir brauchen Internet."
  ↳ Can return to Treasure Screen
  ↳ Coins NOT deducted
  
□ Internet loss during video playback:
  ↳ Video buffering if possible
  ↳ If buffer empty: Pause video
  ↳ Show error overlay
  ↳ After 5s: Return to Home
  ↳ Time NOT consumed
  
□ Internet returns:
  ↳ Resume normally
  ↳ Video Selection: Thumbnails load
  ↳ Video Player: Playback resumes
  
□ Slow network:
  ↳ Thumbnails load eventually (10s timeout)
  ↳ Show loading indicators
  ↳ No crash if timeout
```

### Storage Edge Cases
```
□ Full storage:
  ↳ Save operations fail gracefully
  ↳ Show error: "Speicher voll"
  ↳ App continues running
  ↳ No crash
  
□ Corrupted player data:
  ↳ Detect on load
  ↳ Reset to defaults
  ↳ Show message: "Daten wurden zurückgesetzt"
  ↳ App continues running
  
□ Missing audio file:
  ↳ Silent (no crash)
  ↳ Log error for debugging
  ↳ Gameplay continues
  
□ Missing image asset:
  ↳ Show placeholder (gray rectangle)
  ↳ Log error for debugging
  ↳ App continues running
```

### Interruption Edge Cases
```
□ Phone call during gameplay:
  ↳ All audio pauses
  ↳ Game state preserved
  ↳ After call: Resume normally
  
□ Notification during gameplay:
  ↳ No interruption (notifications don't stop app)
  ↳ Notification banner appears/dismisses
  ↳ Gameplay continues
  
□ Siri activated:
  ↳ Audio ducks
  ↳ Game state preserved
  ↳ After Siri: Audio resumes
  
□ Control Center opened:
  ↳ State persists
  ↳ Resume normally when closed
  
□ Screenshot taken:
  ↳ No interruption
  ↳ Flash animation (system)
  ↳ Gameplay continues
```

### User Input Edge Cases
```
□ Rapid button tapping:
  ↳ Debounced (300ms)
  ↳ No double-action
  ↳ No crash
  
□ Tap during transition:
  ↳ Ignored (transition lock)
  ↳ No crash
  ↳ No unintended navigation
  
□ Swipe gestures:
  ↳ Not recognized (by design)
  ↳ Only single tap works
  
□ Two-finger tap:
  ↳ Treated as single tap
  ↳ First touch point registered
  
□ Long press:
  ↳ No special action
  ↳ Treated as single tap
```

### Display Edge Cases
```
□ iPad Pro 11":
  ↳ UI scales correctly
  ↳ Touch targets still ≥ 96pt
  ↳ Aspect ratio preserved
  
□ iPad Pro 12.9":
  ↳ UI scales correctly
  ↳ Larger screen utilized well
  ↳ Elements not stretched
  
□ iPad 10th gen (design target):
  ↳ UI perfect (1194×834pt)
  ↳ Exact design match
  
□ Older iPads (9th gen):
  ↳ UI acceptable
  ↳ Performance may be slightly slower
  ↳ Still playable
  
□ Rotation attempt:
  ↳ Locked to landscape
  ↳ No accidental rotation
  ↳ Gyroscope ignored
```

---

## 19. Regression Testing

**Critical**: After ANY code change, verify the following to ensure no new bugs were introduced.

### Smoke Test (5 minutes)
```
□ App launches without crash
□ Loading screen displays and completes
□ Player selection works
□ Home screen loads
□ Can start any activity
□ Activity completes and earns coin
□ Celebration triggers at 5 coins
□ Can access Treasure Screen at 10+ coins
□ YouTube flow works (selection → player → time-up → home)
□ Parent gate works
□ No obvious visual glitches
```

### Full Regression (30 minutes)
```
□ Complete Loading → Player → Home flow
□ Complete at least one level in each activity:
  ↳ Puzzle Matching
  ↳ Labyrinth
  ↳ Würfel
  ↳ Wähle die Zahl
□ Trigger celebration overlay (earn 5 coins)
□ Trigger celebration overlay at 10 coins
□ Complete YouTube flow:
  ↳ Redeem 10 coins
  ↳ Select video
  ↳ Watch for 1 minute
  ↳ Wait for time-up
  ↳ Return to Home
□ Access Parent Dashboard:
  ↳ Solve math question
  ↳ Toggle activity lock
  ↳ Change time limit
  ↳ Add video to approved list
  ↳ Remove video from approved list
  ↳ Reset player progress
□ Test offline mode:
  ↳ Disable network
  ↳ Play activities (should work)
  ↳ Try to access YouTube (should show error)
□ Performance check:
  ↳ No frame drops during gameplay
  ↳ Memory < 200MB during video
  ↳ No crashes after 30 minutes
```

---

## 20. Sign-Off Criteria

**Before submitting to TestFlight:**

### Critical Requirements (Must Fix)
```
□ No crashes during normal gameplay
□ No data loss (coins, progress persist)
□ Coin economy accurate (no coin duplication or loss)
□ All voice files present and play correctly
□ All critical animations (Bennie, Lemminge) work
□ YouTube flow works end-to-end
□ Parent Dashboard functional
□ Touch targets ≥ 96pt everywhere
□ Bennie is brown, NO clothing ⚠️
□ Lemminge are BLUE, NOT green/brown ⚠️
```

### Major Requirements (Should Fix)
```
□ All UI glitches fixed (overlapping text, wrong colors)
□ All audio issues fixed (wrong voice, missing sounds)
□ All navigation issues fixed (wrong screen, stuck)
□ Memory usage < 200MB peak
□ Frame rate 60fps stable
□ Battery drain acceptable (< 15% per 30 min)
```

### Minor Requirements (Nice to Fix)
```
□ 90%+ of minor bugs fixed:
  ↳ Cosmetic issues (alignment, spacing)
  ↳ Edge cases (rare scenarios)
  ↳ Polish items (animation timing)
```

### Content Requirements
```
□ All voice files recorded and imported
□ All animations created and imported
□ All character assets finalized (Bennie poses, Lemminge expressions)
□ All background images finalized
□ All UI components finalized
□ No placeholder content remaining
```

### Accessibility Requirements
```
□ VoiceOver labels complete
□ Color contrast verified (4.5:1)
□ Reduce Motion support implemented
□ Haptic feedback working
```

### Documentation Requirements
```
□ App icon finalized (1024×1024)
□ Screenshots prepared for App Store (all required sizes)
□ Privacy policy prepared
□ Age rating confirmed (4+)
□ App Store description written
□ Release notes prepared
```

### Final Checks
```
□ Version number correct (e.g., 1.0.0)
□ Build number incremented
□ Code signing configured
□ TestFlight metadata complete
□ Internal testing group defined
□ External testing plan ready
```

---

**Status**: ✅ Phase 8 QA Checklist Complete
**Dependencies**: All previous phases (1-7) must be complete
**Next**: Begin testing cycle, document bugs, iterate until sign-off criteria met
