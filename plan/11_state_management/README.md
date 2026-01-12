# Phase 11: State Management & Navigation

**Duration**: 4-6 hours  
**Status**: Not Started  
**Dependencies**: Phase 10 (Data Persistence)

---

## 📚 Overview

Implement the complete game state machine and navigation flow as defined in the playbook. This phase ensures smooth transitions between screens, proper state persistence, and playbook-compliant navigation patterns.

**Key References:**
- 📖 `docs/playbook/02-screen-flow.md` - Complete state machine specification
- 📖 `docs/playbook/04-screens/` - All screen-specific behaviors
- 🎨 `design/references/screens/` - Visual screen references
- 🧩 `design/references/components/` - Navigation component assets

---

## 🎯 Deliverables

- [ ] GameStateManager with complete state machine
- [ ] Screen transition coordinator
- [ ] Navigation flow implementation
- [ ] State persistence across app lifecycle
- [ ] Deep linking support for parent dashboard
- [ ] State validation and recovery

---

## 📂 Files Structure

```
11_state_management/
├── README.md                      (this file)
├── PHASE_REFERENCES.md            (detailed playbook mapping)
├── game_state_machine.md          (state definitions)
├── navigation_coordinator.md      (screen transitions)
├── state_persistence.md           (state saving/loading)
└── validation_tests.md            (state validation tests)
```

---

## 🔗 Playbook References

### Primary Documentation

| Topic | Playbook File | Sections | Description |
|-------|--------------|----------|-------------|
| **State Machine** | `02-screen-flow.md` | 2.1-2.3 | Complete flow diagram, state definitions, transitions |
| **Core Loop** | `00-game-overview.md` | 0.2 | Primary game loop structure |
| **Data Models** | `05-technical-requirements.md` | 5.4 | PlayerData, AppSettings structures |
| **Quick Reference** | `07-quick-reference.md` | All | State machine rules summary |

### Screen-Specific Documentation

| Screen | Playbook File | Visual Reference | Key Behaviors |
|--------|--------------|------------------|---------------|
| Loading | `04-screens/loading-player.md` | `Reference_Loading_Screen.png` | Progress animation, 2-3s minimum display |
| Player Selection | `04-screens/loading-player.md` | `Reference_Player_Selection_Screen.png` | Profile cards, voice triggers |
| Home | `04-screens/home-activities.md` | `Reference_Menu_Screen.png` | Activity signs, locked states, chest |
| Puzzle Matching | `04-screens/home-activities.md` | `Reference_Matching_Game_Screen.png` | Grid validation, success triggers |
| Labyrinth | `04-screens/home-activities.md` | `Reference_Layrinth_Game_Screen.png` | Path tracking, completion detection |
| Numbers | `04-screens/home-activities.md` | `Reference_Numbers_Game_Screen.png` | Number selection, validation |
| Celebration | `04-screens/celebration-treasure.md` | `Reference_Celebration_Overlay.png` | **Overlay only**, 5-coin milestones |
| Treasure | `04-screens/celebration-treasure.md` | `Reference_Treasure_Screen.png` | Coin redemption, button states |
| Video | `04-screens/video-parent.md` | *(no visual ref)* | Controlled playback, time limits |
| Parent | `04-screens/video-parent.md` | *(no visual ref)* | Math gate, dashboard access |

### Navigation Component References

Components needed for state management implementation:

| Component | Asset File | Usage in Navigation |
|-----------|------------|---------------------|
| Home Button | `navigation-bar-top_20260110_122359.png` | Return to home from any screen |
| Settings Button | `settings-button-wooden_20260110_123306.png` | Access parent gate |
| Sound Button | `sound-button-wooden_20260110_123401.png` | Audio controls (persistent) |
| Activity Buttons | `activity-button-raetsel_20260110_123032.png`<br>`activity-button-zahlen_20260110_123105.png` | Activity selection from home |
| Treasure Chest | `treasure-chest-closed_20260110_122421.png`<br>`treasure-chest-open_20260110_122445.png` | State-based chest display (open at 10+ coins) |

---

## ✅ Exit Criteria

### Playbook Compliance

#### State Machine (from `02-screen-flow.md`)

- [ ] **All states defined** (Part 2.2):
  ```swift
  enum GameState {
      case loading
      case playerSelection
      case home
      case activitySelection(ActivityType)
      case playing(ActivityType, SubActivity)
      case levelComplete
      case celebrationOverlay      // Only at 5-coin milestones
      case treasureScreen
      case videoSelection
      case videoPlaying
      case parentGate              // Math question gate
      case parentDashboard         // Settings screen
  }
  ```

- [ ] **All transitions match Part 2.3 table**:
  - loading → playerSelection (at 100% progress)
  - playerSelection → home (tap player)
  - home → activitySelection (tap activity)
  - home → treasureScreen (tap chest, only if coins ≥ 10)
  - home → parentGate (tap settings)
  - playing → levelComplete (success)
  - levelComplete → celebrationOverlay (if coins % 5 == 0)
  - levelComplete → playing (if coins % 5 != 0)
  - celebrationOverlay → treasureScreen (if coins ≥ 10)
  - celebrationOverlay → playing (if coins < 10)
  - treasureScreen → videoSelection (tap YouTube button)
  - videoPlaying → home (time up)

#### Navigation Flow (from `02-screen-flow.md` Part 2.1)

- [ ] **Loading screen minimum display** (2-3 seconds)
  - See `04-screens/loading-player.md` for details
  - Fake loading animation to give processing time

- [ ] **Back button behavior**:
  - Activities → Home (NOT activity selection)
  - Activity Selection → Home
  - Treasure → Home
  - Parent Dashboard → Home (after math gate)

- [ ] **Home button** (always visible in activities):
  - Direct return to home screen
  - Saves progress automatically

#### Celebration Overlay (from `04-screens/celebration-treasure.md`)

- [ ] **Is an OVERLAY, not a separate screen**
  - Activity screen visible underneath (dimmed to 40%)
  - Transparent background over activity
  - No navigation away from activity screen

- [ ] **Only appears at 5-coin milestones** (5, 10, 15, 20...)
  - Check: `coins % 5 == 0 && coins > 0`
  - Never shows at 1, 2, 3, 4, 6, 7, 8, 9 coins

- [ ] **Auto-navigation after celebration**:
  - If coins ≥ 10: Navigate to treasure screen
  - If coins < 10: Continue in activity

#### State Persistence (from `05-technical-requirements.md` Part 5.4)

- [ ] **PlayerData structure implemented**:
  ```swift
  struct PlayerData: Codable {
      var id: String
      var coins: Int
      var totalCoinsEarned: Int
      var activityProgress: [String: Int]
      var lastPlayedDate: Date
      var totalPlayTimeToday: TimeInterval
      var videosWatched: [VideoRecord]
      var learningProfile: LearningProfile
  }
  ```

- [ ] **AppSettings structure implemented**:
  ```swift
  struct AppSettings: Codable {
      var parentSettings: ParentSettings
      var lastActivePlayer: String?
      var audioEnabled: Bool = true
      var musicVolume: Float = 0.3
  }
  ```

- [ ] **State saves on app background**
- [ ] **State restores on app foreground**
- [ ] **Invalid states caught and recovered**

### Technical Requirements

- [ ] State changes are atomic
- [ ] State transitions are logged for debugging
- [ ] Invalid state transitions are prevented
- [ ] State machine is thread-safe
- [ ] Navigation stack is properly maintained
- [ ] Deep links work for parent dashboard
- [ ] Celebration overlay preserves activity screen context

### Testing Requirements

- [ ] Unit tests for all state transitions
- [ ] Integration tests for navigation flows
- [ ] State persistence tests (background/foreground)
- [ ] Recovery from invalid state tests
- [ ] Celebration overlay tests (5-coin milestone only)
- [ ] Performance tests (state changes < 50ms)

---

## 🚀 Implementation Order

### Step 1: Define State Machine (1 hour)
**See:** `game_state_machine.md`  
**References:** 
- `docs/playbook/02-screen-flow.md` (Parts 2.2-2.3)
- `docs/playbook/05-technical-requirements.md` (Part 5.4)

**Tasks:**
1. Define GameState enum with all states
2. Define ActivityType and SubActivity enums
3. Implement state transition validation
4. Create GameStateManager class
5. Add state change observers

**Critical Rules from Playbook:**
- Celebration overlay is a state, not a screen
- Parent gate always required for dashboard access
- Video playing requires internet (offline check)

---

### Step 2: Create Navigation Coordinator (2 hours)
**See:** `navigation_coordinator.md`  
**References:**
- `docs/playbook/02-screen-flow.md` (Part 2.1 flow diagram)
- All files in `docs/playbook/04-screens/`
- `design/references/screens/*.png` (visual reference)
- `design/references/components/navigation-*.png` (buttons)

**Tasks:**
1. Create AppCoordinator class
2. Implement screen transition logic
3. Add navigation animations (0.3s cross-fade)
4. Implement back button behavior
5. Implement home button (always returns to home)
6. Add deep linking for parent dashboard

**Navigation Rules from Playbook:**
- Loading → Player Selection (minimum 2s display first)
- Back from activity goes to Home, NOT activity selection
- Home button available in all activities
- Settings button triggers parent gate, not dashboard

**Component Integration:**
- Use `navigation-bar-top_20260110_122359.png` for top nav
- Use `activity-button-*.png` for activity selections
- Use `treasure-chest-*.png` with state-based open/closed display

---

### Step 3: Implement Celebration Overlay Special Handling (1 hour)
**See:** `game_state_machine.md` (celebration state section)  
**References:**
- `docs/playbook/04-screens/celebration-treasure.md`
- `design/references/screens/Reference_Celebration_Overlay.png`

**Tasks:**
1. Implement overlay view (transparent, over activity screen)
2. Dim underlying activity screen to 40% brightness
3. Add confetti animation (full screen)
4. Add "Weiter" button
5. Implement post-celebration navigation logic:
   ```swift
   func dismissCelebration() {
       if player.coins >= 10 {
           navigateToTreasure()
       } else {
           continueActivity()  // Stay in activity
       }
   }
   ```

**Critical Design Rules:**
- This is NOT a separate screen - it's an overlay
- Activity screen must remain visible (dimmed)
- Only appears at 5-coin milestones: 5, 10, 15, 20, 25...
- After dismissal, check coins and navigate accordingly

---

### Step 4: Add State Persistence (1 hour)
**See:** `state_persistence.md`  
**References:**
- `docs/playbook/05-technical-requirements.md` (Part 5.4)
- Phase 10 implementation (PlayerDataStore)

**Tasks:**
1. Save current GameState on app background
2. Save current screen context (e.g., which activity, level number)
3. Restore state on app foreground
4. Handle invalid states (reset to home)
5. Verify PlayerData and AppSettings persistence

**State Recovery Rules:**
- If state is `playing`, restore to activity selection (safer)
- If state is `celebrationOverlay`, restore to home
- If state is `videoPlaying`, restore to home (time expired)
- All other states can be restored directly

---

### Step 5: Testing & Validation (1-2 hours)
**See:** `validation_tests.md`  
**References:**
- `docs/playbook/10-implementation.md` (Part 10.3 QA matrix)

**Test Suites:**

1. **State Machine Tests**
   - All valid transitions work
   - Invalid transitions are blocked
   - State change observers fire correctly

2. **Navigation Flow Tests**
   - Complete game loop (loading → home → activity → celebration → treasure → video → home)
   - Back button behavior (activities return to home)
   - Home button always goes to home
   - Parent gate blocks dashboard access

3. **Celebration Overlay Tests**
   - Only appears at 5-coin milestones
   - Activity screen visible underneath
   - Correct navigation after dismissal (treasure if ≥10, continue if <10)

4. **State Persistence Tests**
   - Background → Foreground restores state
   - Force quit → Relaunch restores state
   - Invalid states reset to home

5. **Performance Tests**
   - State transitions < 50ms
   - Navigation animations smooth (60fps)
   - No memory leaks on repeated navigation

---

## 🔍 Critical Notes

### From Playbook Section 2.1 (Screen Flow)

**ABSOLUTE RULES:**
1. Loading screen shows for **minimum 2-3 seconds** (gives child processing time)
2. Celebration overlay **ONLY** at 5-coin milestones (never at 1, 2, 3, 4, 6, 7, 8, 9)
3. Treasure screen **auto-navigates** at 10+ coins after celebration
4. Back button from activities goes to **home**, NOT activity selection
5. Parent dashboard **requires math gate** (prevents child access)

### From Playbook Section 4.7 (Celebration Overlay)

**CELEBRATION IS AN OVERLAY:**
```
╔══════════════════════════════════════════════════════════════════════╗
║                    CELEBRATION IS AN OVERLAY, NOT A SCREEN            ║
║                                                                       ║
║  This keeps the child grounded in context—they see what they          ║
║  accomplished while receiving praise. No jarring screen transitions.  ║
║                                                                       ║
║  ✅ Context preservation — Child sees their completed work            ║
║  ✅ No jarring transitions — Predictable, calm experience             ║
║  ✅ Immediate feedback — Success feels connected to action            ║
║  ✅ Autism-friendly — Reduces disorientation from screen changes      ║
╚══════════════════════════════════════════════════════════════════════╝
```

**Implementation:**
- Overlay appears **over** the activity screen
- Activity screen is **dimmed to 40%** but remains visible
- Confetti animation plays **on top** of overlay
- "Weiter" button dismisses overlay
- After dismissal, navigation logic runs (treasure or continue)

### From Playbook Section 2.3 (State Transitions)

**Special Transition Rules:**

| From State | Event | To State | Side Effects |
|------------|-------|----------|--------------|
| `levelComplete` | coins % 5 == 0 | `celebrationOverlay` | Show overlay over activity |
| `levelComplete` | coins % 5 != 0 | `playing` (next) | Auto-advance to next level |
| `celebrationOverlay` | tap(weiter) + coins ≥ 10 | `treasureScreen` | Auto-navigate |
| `celebrationOverlay` | tap(weiter) + coins < 10 | `playing` | Continue activity |
| `treasureScreen` | tap(5min) | `videoSelection` | Deduct 10 coins |
| `treasureScreen` | tap(10min) | `videoSelection` | Deduct 20 coins |
| `videoPlaying` | timeUp | `home` | Auto-exit, "Time up" audio |
| `home` | tap(chest) | `treasureScreen` | **Only if coins ≥ 10** |
| `home` | tap(settings) | `parentGate` | Math question required |
| `parentGate` | correctAnswer | `parentDashboard` | Access granted |

---

## 🧪 Testing Scenarios

### Scenario 1: First-Time User Flow
1. App launches → Loading screen (2-3s minimum)
2. Loading complete → Player selection
3. Tap "Alexander" → Home screen
4. Tap "Rätsel" → Activity selection
5. Tap "Puzzle Matching" → Activity screen
6. Complete level 1 → +1 coin (1 total, no celebration)
7. Complete level 2 → +1 coin (2 total, no celebration)
8. Complete level 3 → +1 coin (3 total, no celebration)
9. Complete level 4 → +1 coin (4 total, no celebration)
10. Complete level 5 → +1 coin (5 total, **CELEBRATION OVERLAY**)
11. Tap "Weiter" → Continue activity (coins < 10)

### Scenario 2: Reaching Treasure
1. Player has 8 coins
2. Complete level → +1 coin (9 total, no celebration)
3. Complete level → +1 coin (10 total, **CELEBRATION OVERLAY**)
4. Tap "Weiter" → **Auto-navigate to Treasure** (coins ≥ 10)
5. Treasure screen shows 10 coins, 5min button active

### Scenario 3: YouTube Redemption
1. Player at treasure screen with 12 coins
2. Tap "5 Min YouTube" → Deduct 10 coins (2 remaining)
3. Video selection screen appears
4. Tap video → Video player with analog clock
5. Clock counts down 5 minutes
6. Time up → "Die Zeit ist um" audio → Home screen

### Scenario 4: Back Navigation
1. Home screen
2. Tap "Zahlen" → Activity selection
3. Tap back → Home screen (NOT activity selection)
4. Tap "Rätsel" → Activity selection
5. Tap "Puzzle" → Activity playing
6. Tap back → Home screen (NOT activity selection)

### Scenario 5: Parent Dashboard Access
1. Home screen
2. Tap settings button → Parent gate (math question)
3. Enter wrong answer → Question remains, tries again
4. Enter correct answer → Parent dashboard
5. Change settings → Tap back → Home screen

### Scenario 6: State Persistence
1. Player in activity screen with 7 coins
2. Press home button on iPad → App backgrounds
3. State saves: current screen, coins, activity progress
4. Reopen app → Restores to activity selection (safe state)
5. Player can continue or pick different activity

---

## 📝 Next Steps After Completion

1. **Phase 12**: Adaptive Difficulty
   - Uses state machine to track performance metrics
   - Adjusts difficulty based on quit rate, mistakes

2. **Phase 13**: Accessibility
   - Uses navigation coordinator for VoiceOver navigation
   - Announces screen changes

3. **Phase 16**: Recursive Testing
   - Validates complete state machine works end-to-end
   - Tests all transition paths

---

## 📚 Additional Reference Files

### Playbook Files to Reference

```
docs/playbook/
├── 00-game-overview.md          (Core loop structure)
├── 02-screen-flow.md            (State machine - PRIMARY REFERENCE)
├── 04-screens/
│   ├── loading-player.md        (Loading, Player Selection)
│   ├── home-activities.md       (Home, Activities)
│   ├── celebration-treasure.md  (Celebration, Treasure - OVERLAY RULES)
│   └── video-parent.md          (Video, Parent)
├── 05-technical-requirements.md (Data structures)
└── 07-quick-reference.md        (State rules summary)
```

### Design Assets to Reference

```
design/references/
├── screens/
│   ├── Reference_Loading_Screen.png
│   ├── Reference_Player_Selection_Screen.png
│   ├── Reference_Menu_Screen.png
│   ├── Reference_Matching_Game_Screen.png
│   ├── Reference_Layrinth_Game_Screen.png
│   ├── Reference_Numbers_Game_Screen.png
│   ├── Reference_Celebration_Overlay.png    (OVERLAY, not screen!)
│   └── Reference_Treasure_Screen.png
└── components/
    ├── navigation-bar-top_20260110_122359.png
    ├── activity-button-raetsel_20260110_123032.png
    ├── activity-button-zahlen_20260110_123105.png
    ├── settings-button-wooden_20260110_123306.png
    ├── sound-button-wooden_20260110_123401.png
    ├── treasure-chest-closed_20260110_122421.png
    └── treasure-chest-open_20260110_122445.png
```

---

**Phase Owner**: Development Team  
**Review Required**: After Step 2 (Navigation Coordinator), After Step 3 (Celebration Overlay)  
**Testing Required**: After Step 5 (complete test suite must pass)

**Estimated Completion**: 4-6 hours  
**Actual Completion**: ___ hours  
**Completion Date**: ___________
