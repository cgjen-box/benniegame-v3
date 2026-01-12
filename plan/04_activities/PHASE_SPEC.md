# Phase 4: Activities Implementation

**Duration**: 8-10 hours  
**Status**: Not Started  
**Dependencies**: Phase 3 (Core Screens)

## Overview

Implement 4 playable activities: Puzzle Matching, Labyrinth, Würfel (Dice), and Wähle die Zahl (Number Selection) with full gameplay, validation, hints, and success states.

## Playbook References

**Primary Documentation:**
- `docs/playbook/04-screens/home-activities.md` - Sections 4.4-4.6
- `docs/playbook/00-game-overview.md` - Section 0.3 (Activities)
- `docs/playbook/01-brand-identity.md` - Section 1.2 (Characters)
- `docs/playbook/03-voice-script.md` - Activity voice lines
- `docs/playbook/06-animation-sound.md` - Character animations

**Design References:**
- `design/references/screens/Reference_Matching Game Screen.png`
- `design/references/screens/Reference_Layrinth_Game_Screen.png`
- `design/references/screens/Reference_Numbers_Game_Screen.png`

**Character Assets:**
- `design/references/character/bennie/states/bennie-pointing.png`
- `design/references/character/bennie/states/bennie-thinking.png`
- `design/references/character/bennie/states/bennie-encouraging.png`
- `design/references/character/lemminge/states/lemminge-curious.png`
- `design/references/character/lemminge/states/lemminge-excited.png`
- `design/references/character/lemminge/states/lemminge-celebrating.png`

**Component Assets:**
- `design/references/components/activity-button-raetsel_*.png`
- `design/references/components/activity-button-zahlen_*.png`
- `design/references/components/navigation-bar-top_*.png`

## Deliverables

- ✅ Puzzle Matching game (3×3 to 6×6 grids)
- ✅ Labyrinth path-tracing game
- ✅ Würfel dice number game
- ✅ Wähle die Zahl number tracing game
- ✅ Activity selection screens
- ✅ Difficulty progression system
- ✅ Hint system
- ✅ Success animations + coin awards

---

## Tasks

### 4.0 Create RätselSelectionView (30 min)

**Playbook Reference:** `docs/playbook/04-screens/home-activities.md` Section 4.3
**Screen Reference:** Use Home Screen layout as template

**Implementation:**
- Two sub-activity signs: "Puzzle" and "Labyrinth"
- Bennie pointing (`design/references/character/bennie/states/bennie-pointing.png`)
- Lemminge curious (`design/references/character/lemminge/states/lemminge-curious.png`)
- Navigation to selected game
- Use `activity-button-raetsel_*.png` for button styling

**Voice Lines:**
- Narrator: "Wähle ein Rätsel" (from `docs/playbook/03-voice-script.md`)

**Test:** Both buttons navigate correctly, characters appear in correct states

---

### 4.1 Implement PuzzleMatchingView (120 min)

**Playbook Reference:** `docs/playbook/04-screens/home-activities.md` Section 4.4
**Screen Reference:** `design/references/screens/Reference_Matching Game Screen.png`
**Character References:**
- Bennie pointing: `design/references/character/bennie/states/bennie-pointing.png`
- Lemminge curious: `design/references/character/lemminge/states/lemminge-curious.png`

**Layout:**
```
According to playbook Section 4.4:
- Dual grids side-by-side (ZIEL / DU)
- StoneTablet components for grid backgrounds
- Color picker at bottom (leaf-shaped buttons)
- Eraser and Reset buttons
- NavigationHeader with progress bar (use navigation-bar-top_*.png)
```

**Gameplay Logic (Per Playbook 4.4):**
1. Generate random pattern (ZIEL grid)
2. Player taps colors then cells (DU grid)
3. Real-time validation
4. When DU == ZIEL → Success!

**Difficulty Progression (Per Playbook Table 4.4):**
| Level Range | Grid Size | Colors | Filled Cells |
|-------------|-----------|--------|--------------|
| 1-5 | 3×3 | 2 (green, yellow) | 2-4 |
| 6-10 | 3×3 | 3 (add gray) | 3-5 |
| 11-20 | 4×4 | 3 colors | 4-7 |
| 21-30 | 5×5 | 3-4 colors | 5-10 |
| 31+ | 6×6 | 4 colors | 6-12 |

**Colors (From Playbook 1.3):**
- Green: `#99BF8C`
- Yellow: `#D9C27A`
- Gray: `#A8A090`

**Voice Lines (From Playbook 3.4):**
- **Activity start:**
  - Narrator: "Mach das Muster nach!" (4 words)
  - Bennie: "Das packen wir!" (3 words)
- **Hints:**
  - 10s no action: "Wir können das, YouTube kommt bald." (6 words)
  - 20s no action: "Welche Farbe fehlt noch?" (4 words)
- **Success:** Random from pool (see section 4.6)

**Test Checklist:**
- [ ] Pattern generation correct for difficulty level
- [ ] Grid cells are ≥96pt (playbook requirement)
- [ ] Real-time validation works
- [ ] Color picker buttons ≥96pt
- [ ] Hints trigger at correct times
- [ ] Success flow awards coin
- [ ] Difficulty scales appropriately
- [ ] Characters animate on idle

---

### 4.2 Implement LabyrinthView (120 min)

**Playbook Reference:** `docs/playbook/04-screens/home-activities.md` Section 4.5
**Screen Reference:** `design/references/screens/Reference_Layrinth_Game_Screen.png`
**Character References:**
- Bennie pointing: `design/references/character/bennie/states/bennie-pointing.png`
- Lemminge scared: `design/references/character/lemminge/states/lemminge-hiding.png`
- Lemminge celebrating: `design/references/character/lemminge/states/lemminge-celebrating.png`

**Layout (Per Playbook 4.5):**
```
- Stone path labyrinth
- START marker (Bennie + Lemminge scared)
- ZIEL marker (celebrating Lemminge)
- Touch-based path drawing
- NavigationHeader with progress bar
```

**Gameplay Logic:**
Per Playbook 4.5 Path Detection:
```swift
struct LabyrinthPath {
    let validPathPoints: [CGPoint]  // Pre-defined correct route
    let pathWidth: CGFloat = 44     // Touch tolerance in points
    
    func isOnPath(_ point: CGPoint) -> Bool {
        validPathPoints.contains { pathPoint in
            distance(point, pathPoint) <= pathWidth
        }
    }
}
```

**Path Mechanics (From Playbook Table 4.5):**
| Action | Input | Validation | Feedback |
|--------|-------|------------|----------|
| Start path | Touch START marker | Must begin at START | Glow effect |
| Draw path | Drag finger along | Must stay on stone path | Path highlights |
| Leave path | Lift finger or go off | Show error, allow retry | Bennie voice |
| Complete | Reach ZIEL | Touch within 44pt of goal | Celebration! |

**Voice Lines (From Playbook 3.4):**
- **Activity start:**
  - Narrator: "Hilf Bennie den Weg finden!" (5 words)
  - Bennie: "Wie fange ich die Lemminge?" (5 words)
- **Wrong path:** Bennie: "Da komme ich nicht durch." (5 words)
- **Hints:**
  - 15s no action: "Wo ist der Anfang?" (4 words)

**Test Checklist:**
- [ ] Path validation works (44pt tolerance)
- [ ] START/ZIEL markers clear
- [ ] Touch tracking smooth
- [ ] Path highlighting works
- [ ] Wrong path feedback immediate
- [ ] Success detection accurate
- [ ] Voice lines trigger correctly

---

### 4.3 Create ZahlenSelectionView (30 min)

**Playbook Reference:** `docs/playbook/04-screens/home-activities.md` Section 4.3
**Component Reference:** `design/references/components/activity-button-zahlen_*.png`

**Implementation:**
- Two sub-activity signs: "Würfel" and "Wähle die Zahl"
- Bennie pointing (`design/references/character/bennie/states/bennie-pointing.png`)
- Lemminge excited (`design/references/character/lemminge/states/lemminge-excited.png`)
- Navigation to selected game

**Test:** Both buttons navigate correctly, characters display

---

### 4.4 Implement WürfelView (90 min)

**Playbook Reference:** `docs/playbook/04-screens/home-activities.md` Section 4.6
**Screen Reference:** `design/references/screens/Reference_Numbers_Game_Screen.png`
**Character References:**
- Bennie pointing: `design/references/character/bennie/states/bennie-pointing.png`
- Lemminge curious: `design/references/character/lemminge/states/lemminge-curious.png`

**Layout (Per Playbook 4.6):**
```
- Large dice in center (animated roll)
- Number buttons 1-6 below (stone tablet style)
- StoneTablet background
- NavigationHeader with progress bar
```

**Gameplay Logic:**
1. Tap dice → animate roll → show number (1-6)
2. Narrator: "Zeig mir die [N]!"
3. Child taps correct number → Success
4. Wrong number: Bennie "Das ist die [X]. Probier nochmal!"

**Dice Animation:**
- 3D rotation effect (0.5s duration)
- Random number 1-6
- Sound effect: `tap_wood.aac`

**Touch Targets:**
- Number buttons: ≥96pt (critical accessibility requirement)

**Voice Lines (From Playbook 3.4):**
- **Activity start:**
  - Narrator: "Wirf den Würfel!" (3 words)
  - Narrator (after roll): "Zeig mir die [N]!" (4 words)
- **Wrong answer:** Bennie: "Das ist die [X]. Probier nochmal!" (6 words)
- **Hints:**
  - 10s: "Zähle die Punkte." (3 words)
  - 20s: "Du hast die [N] gewürfelt." (5 words)
  - 30s: "Wo ist die [N]?" (4 words)

**Test Checklist:**
- [ ] Dice roll animation smooth
- [ ] Number validation correct
- [ ] Wrong answer feedback clear
- [ ] Hints fire at 10s/20s/30s
- [ ] Touch targets ≥96pt
- [ ] Success flow works

---

### 4.5 Implement WähleZahlView (90 min)

**Playbook Reference:** `docs/playbook/04-screens/home-activities.md` Section 4.6
**Screen Reference:** `design/references/screens/Reference_Numbers_Game_Screen.png` (alternate view)

**Layout:**
```
Per Playbook 4.6:
- Stone tablet with numbers 1-10
- Each number has tracing guide (arrows)
- Color picker for tracing (optional)
- Eraser button
- NavigationHeader with progress bar
```

**Tracing System (From Playbook 4.6 Table):**
| Number | Stroke Guide | Arrow Indicators |
|--------|--------------|------------------|
| 1 | Single downstroke | ↓ |
| 2 | Curve right, down, right | ↷ ↓ → |
| 3 | Two curves right | ↷ ↷ |
| 4 | Down, right, down | ↓ → ↓ |
| 5 | Down, curve right | ↓ ↷ |
| 6 | Curve down and around | ↶ ○ |
| 7 | Right, diagonal down | → ↘ |
| 8 | Double loop | ∞ |
| 9 | Circle, down | ○ ↓ |
| 10 | "1" then "0" | Two separate strokes |

**Validation Algorithm (Per Playbook 4.6):**
```swift
struct NumberTracingValidator {
    let requiredPathCoverage: Float = 0.70  // 70%
    
    func validateTrace(
        userPath: [CGPoint],
        targetNumber: Int
    ) -> Bool {
        let targetPath = getPathForNumber(targetNumber)
        let coveredPoints = targetPath.filter { targetPoint in
            userPath.contains { userPoint in
                distance(userPoint, targetPoint) <= 30  // 30pt tolerance
            }
        }
        
        let coverage = Float(coveredPoints.count) / Float(targetPath.count)
        return coverage >= requiredPathCoverage
    }
}
```

**Voice Lines (From Playbook 3.4):**
- **Activity start:** Narrator: "Zeig mir die [N]!" (4 words)
- **Wrong answer:** Bennie: "Das ist die [X]. Probier nochmal!" (6 words)
- **Hints:**
  - 10s: "Der Erzähler hat [N] gesagt." (5 words)
  - 20s: "Wo ist die [N]?" (4 words)

**Test Checklist:**
- [ ] All numbers 1-10 have stroke paths defined
- [ ] Tracing validation works (70% coverage)
- [ ] 30pt tolerance for touch
- [ ] Arrow guides visible and helpful
- [ ] Hints trigger correctly
- [ ] Success detection accurate

---

### 4.6 Implement ActivityCompletionFlow (45 min)

**Playbook Reference:** `docs/playbook/03-voice-script.md` - Success Phrase Pool

**On Success (Per Playbook Section 4.1):**
1. Play success audio (random from pool)
2. Award +1 coin
3. Coin fly animation to progress bar
4. Check if coins % 5 == 0
   - Yes → Navigate to celebration overlay (Phase 5)
   - No → Auto-advance to next level

**Success Audio Pool (From Playbook 3.4):**
```swift
let successPhrases = [
    "Super!",                        // 1 word
    "Toll gemacht!",                 // 2 words
    "Wunderbar!",                    // 1 word
    "Ja, genau!",                    // 2 words
    "Das hast du super gemacht!",    // 5 words
    "Perfekt!",                      // 1 word
    "Bravo!"                         // 1 word
]
```

**Animation Sequence:**
1. Success sound plays (0.5s)
2. Characters celebrate (1.0s)
   - Bennie: `bennie-celebrating.png`
   - Lemminge: `lemminge-celebrating.png`
3. Coin appears and flies to progress bar (0.8s)
4. Progress bar fills (0.5s)
5. Check celebration milestone
6. Auto-advance or show overlay

**Test Checklist:**
- [ ] Coin awards correctly
- [ ] Success audio plays
- [ ] Random phrase selection works
- [ ] Coin animation smooth
- [ ] Progress bar updates
- [ ] Milestone detection works
- [ ] Auto-advance timing good

---

### 4.7 Create AdaptiveDifficulty System (60 min)

**Playbook Reference:** `docs/playbook/00-game-overview.md` Section 0.5

**Learning Profile (From Playbook 0.5):**
```swift
struct LearningProfile: Codable {
    // Performance metrics
    var averageSolveTime: TimeInterval
    var mistakeFrequency: Double      // Mistakes per level
    var quitRate: Double              // Levels abandoned
    var sessionDuration: TimeInterval
    
    // Engagement indicators
    var hintUsageRate: Double
    var celebrationEngagement: Bool   // Did they tap Weiter quickly?
    var preferredActivities: [ActivityType: Int]
    
    // Adaptive parameters
    var difficultyLevel: Float        // 0.0 (easiest) to 1.0 (hardest)
    var gridSizePreference: Int       // Preferred puzzle grid size
    var colorCount: Int               // Number of colors in puzzles
}
```

**Difficulty Adjustment Rules (From Playbook 0.5 Table):**
| Signal | Interpretation | Adjustment |
|--------|----------------|------------|
| Solve time < 10s | Too easy | Increase difficulty |
| Solve time > 60s | Struggling | Decrease difficulty |
| 3+ mistakes per level | Too hard | Decrease difficulty, offer hints |
| Quit mid-activity | Frustration | Major decrease, encouraging message |
| Fast successive completions | Engaged & capable | Gradually increase |
| Long pause (>30s) | Confused or distracted | Offer gentle hint |

**Implementation:**
- Track metrics per activity session
- Adjust difficulty after every 3 levels
- Store in PlayerData
- Apply to next session

**Test Checklist:**
- [ ] Metrics tracked correctly
- [ ] Difficulty adjusts appropriately
- [ ] Stored in PlayerData
- [ ] Applied on next launch

---

### 4.8 Implement Hint System (45 min)

**Playbook Reference:** `docs/playbook/03-voice-script.md` - Activity sections

**Timer System:**
- First hint: 10-15s of inactivity (activity-dependent)
- Second hint: 20-30s
- Third hint: 30-40s (if applicable)

**Hint Categories (Per Playbook):**
1. **Encouraging:** "Du schaffst das!"
2. **Directional:** "Welche Farbe fehlt noch?"
3. **Specific:** "Wo ist die 5?"

**Implementation:**
```swift
class HintSystem {
    private var inactivityTimer: Timer?
    private var hintsGiven = 0
    private let maxHints = 3
    private let hintIntervals: [TimeInterval]  // Activity-specific
    
    func startTracking() {
        resetTimer()
    }
    
    func onUserInteraction() {
        resetTimer()
    }
    
    func triggerHint() {
        guard hintsGiven < maxHints else { return }
        let hint = getHintForActivity(hintsGiven)
        playVoice(hint)
        hintsGiven += 1
        resetTimer()
    }
}
```

**Per-Activity Timing (From Playbook 3.4):**
- **Puzzle Matching:** 10s, 20s
- **Labyrinth:** 15s
- **Würfel:** 10s, 20s, 30s
- **Wähle die Zahl:** 10s, 20s

**Test Checklist:**
- [ ] Timer starts on level load
- [ ] Timer resets on user interaction
- [ ] Hints fire at correct intervals
- [ ] Max 3 hints enforced
- [ ] Voice lines play correctly
- [ ] No overlapping voice

---

### 4.9 Add Loading Transitions (30 min)

**Playbook Reference:** `docs/playbook/06-animation-sound.md` Section 6.2

**Transition Specs (From Playbook 6.2 Table):**
| Transition | Animation | Duration |
|------------|-----------|----------|
| Screen to screen | Cross-fade | 0.3s |
| Activity load | Fade in | 0.3s |
| Activity complete | Fade to celebration | 0.4s |

**Animation Properties (From Playbook 6.1):**
- **Easing:** Spring (response: 0.3)
- **Duration:** 0.3-0.5s typical
- **Frame rate:** 60fps constant

**Implementation:**
```swift
extension View {
    func activityTransition() -> some View {
        self.transition(.opacity)
            .animation(.spring(response: 0.3), value: isPresented)
    }
}
```

**Test Checklist:**
- [ ] No jarring transitions
- [ ] Smooth fade effects
- [ ] 60fps maintained
- [ ] Loading indicators appear when needed

---

### 4.10 QA Pass on All Activities (90 min)

**Playbook Reference:** `docs/playbook/DESIGN_QA_CHECKLIST.md`

**For EACH activity (4 total), verify:**

**Characters (From Playbook 1.2):**
- [ ] Bennie is brown (#8C7259)
- [ ] Bennie has NO clothing/vest/accessories
- [ ] Lemminge are BLUE (#6FA8DC)
- [ ] Lemminge are NOT green or brown
- [ ] Character states match playbook specs

**UI (From Playbook 5.0):**
- [ ] Touch targets ≥ 96pt
- [ ] Wooden elements have grain texture
- [ ] Colors from approved palette only
- [ ] No red/neon colors
- [ ] Progress bar displays correctly

**Text (From Playbook 1.4):**
- [ ] German language only
- [ ] Literal language (no metaphors)
- [ ] Never says "wrong" or "falsch"
- [ ] Positive/encouraging tone
- [ ] Max 7 words per sentence

**Animation (From Playbook 6.1):**
- [ ] No flashing effects
- [ ] No shaking/jarring motion
- [ ] Reduce motion fallbacks exist
- [ ] 60fps maintained

**Gameplay:**
- [ ] Gameplay logic works correctly
- [ ] Validation accurate
- [ ] Voice triggers fire at correct times
- [ ] Hints work
- [ ] Success flow complete
- [ ] Coin awards correctly
- [ ] No crashes or bugs
- [ ] Difficulty progression appropriate

**Performance:**
- [ ] Smooth 60fps
- [ ] No frame drops
- [ ] No memory leaks
- [ ] Loading times acceptable

**Complete Playthrough Test:**
- [ ] Play each activity for 5+ levels
- [ ] Test all hint triggers
- [ ] Verify coin awards at milestones
- [ ] Check celebration overlay triggers (coins % 5 == 0)
- [ ] Confirm smooth progression

---

## Exit Criteria

### Functional Requirements
- [ ] All 4 activities fully playable
- [ ] Validation logic accurate for all activities
- [ ] Hint system working across all activities
- [ ] Adaptive difficulty implemented and tracking
- [ ] Success flow complete with coin awards
- [ ] Activity selection screens navigate correctly

### Technical Requirements
- [ ] No critical bugs or crashes
- [ ] Performance: 60fps constant
- [ ] Memory: < 200MB peak
- [ ] Touch targets: ALL ≥ 96pt
- [ ] Colors: Match playbook exactly

### Design Compliance
- [ ] All characters match reference images
- [ ] All colors from approved palette
- [ ] All voice lines max 7 words
- [ ] No forbidden elements (red, flashing, etc.)

### Playbook Compliance
- [ ] Every screen matches playbook spec
- [ ] Every voice line from playbook script
- [ ] Every animation follows playbook timing
- [ ] Every color uses playbook hex values

### User Experience
- [ ] Can complete each activity successfully
- [ ] Hints helpful and timely
- [ ] Feedback positive and encouraging
- [ ] Progression feels natural
- [ ] Celebration feels rewarding

---

## Next Phase

**Phase 5: Reward System**
- Celebration overlay (at 5-coin milestones)
- Treasure screen (YouTube redemption)
- Video selection
- Video player with analog clock timer

**Dependencies for Phase 5:**
- Coin counting system (from this phase)
- Success flow (from this phase)
- Progress bar component (from Phase 2)
- Voice lines for celebration (from Phase 6)

---

## Notes

### Development Tips
1. **Start with one activity completely** - Don't try to implement all 4 simultaneously
2. **Test voice timing early** - Voice interactions are critical for UX
3. **Use real devices for touch testing** - Simulator touch is not accurate
4. **Check playbook frequently** - Colors, sizing, and timing are exact
5. **Reference screens constantly** - Layout must match exactly

### Common Pitfalls to Avoid
- ❌ Touch targets < 96pt (accessibility violation)
- ❌ Colors not matching hex values exactly
- ❌ Voice lines > 7 words (cognitive overload)
- ❌ Skipping hint system (engagement drops)
- ❌ Not testing on actual iPad (layout issues)
- ❌ Forgetting to reset timers on user interaction
- ❌ Hard-coding difficulty (should be adaptive)

### Useful Commands
```bash
# View character references
open design/references/character/bennie/states/

# View screen references
open design/references/screens/

# Check playbook section
cat docs/playbook/04-screens/home-activities.md

# Run QA checklist
cat DESIGN_QA_CHECKLIST.md
```
