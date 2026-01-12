# Phase 11: Detailed Playbook & Asset References

This document provides a comprehensive mapping of all playbook sections and design assets relevant to implementing the state management and navigation system.

---

## 📖 Playbook Section Mapping

### Core State Machine Specification

| Playbook Section | File | Content | Implementation Impact |
|-----------------|------|---------|----------------------|
| **Part 2.1** | `02-screen-flow.md` | Complete screen flow diagram | Defines all navigation paths |
| **Part 2.2** | `02-screen-flow.md` | State Machine Definition | Defines all GameState enum values |
| **Part 2.3** | `02-screen-flow.md` | State Transitions table | Defines valid state transitions |
| **Part 0.2** | `00-game-overview.md` | Core game loop | Defines primary game cycle |

### Screen-Specific Behaviors

#### Loading Screen
| Playbook Section | File | Key Requirements |
|-----------------|------|------------------|
| Part 4.1 | `04-screens/loading-player.md` | - Progress animation 0-100%<br>- **Minimum 2-3 second display**<br>- Narrator voice at 100%<br>- Fake loading (UX: processing time) |

**State Transitions:**
```
loading → playerSelection (when progress == 100% AND min 2s elapsed)
```

**Assets:**
- Visual: `design/references/screens/Reference_Loading_Screen.png`
- Bennie: idle → waving at 100%
- Lemminge: hiding/peeking animations

---

#### Player Selection Screen
| Playbook Section | File | Key Requirements |
|-----------------|------|------------------|
| Part 4.2 | `04-screens/loading-player.md` | - Two player cards (Alexander, Oliver)<br>- Show coin counts<br>- Voice trigger on screen appear<br>- Voice confirmation on tap |

**State Transitions:**
```
playerSelection → home (tap Alexander or Oliver)
```

**Assets:**
- Visual: `design/references/screens/Reference_Player_Selection_Screen.png`
- Bennie: waving
- Lemminge: hiding in various spots

---

#### Home Screen (Waldabenteuer)
| Playbook Section | File | Key Requirements |
|-----------------|------|------------------|
| Part 4.3 | `04-screens/home-activities.md` | - 4 activity signs (2 unlocked, 2 locked)<br>- Treasure chest (state-based)<br>- Settings button → parent gate<br>- Profile button → player selection |

**State Transitions:**
```
home → activitySelection (tap unlocked activity)
home → treasureScreen (tap chest, IF coins >= 10)
home → parentGate (tap settings)
home → playerSelection (tap profile)
```

**Assets:**
- Visual: `design/references/screens/Reference_Menu_Screen.png`
- Components:
  - `activity-button-raetsel_20260110_123032.png`
  - `activity-button-zahlen_20260110_123105.png`
  - `treasure-chest-closed_20260110_122421.png`
  - `treasure-chest-open_20260110_122445.png`
  - `settings-button-wooden_20260110_123306.png`
  - `sound-button-wooden_20260110_123401.png`
- Bennie: pointing
- Lemminge: mischievous

**Chest State Logic:**
```swift
func updateChestState(coins: Int) {
    if coins >= 10 {
        chestState = .open
        chestGlow = true
    } else {
        chestState = .closed
        chestGlow = false
    }
}
```

---

#### Activity Selection Screen
| Playbook Section | File | Key Requirements |
|-----------------|------|------------------|
| Part 4.3 | `04-screens/home-activities.md` | - Show sub-activities for selected activity<br>- Back button returns to home<br>- Voice prompt for selection |

**State Transitions:**
```
activitySelection → playing (tap sub-activity)
activitySelection → home (tap back)
```

**Assets:**
- Similar visual style to home screen
- Activity-specific icons

---

#### Activity Playing Screens

##### Puzzle Matching
| Playbook Section | File | Key Requirements |
|-----------------|------|------------------|
| Part 4.4 | `04-screens/home-activities.md` | - Dual grid (ZIEL/DU)<br>- Color palette<br>- Real-time validation<br>- Progress bar always visible |

**State Transitions:**
```
playing → levelComplete (pattern matches ZIEL)
playing → home (tap home button)
```

**Assets:**
- Visual: `design/references/screens/Reference_Matching_Game_Screen.png`
- Navigation: `navigation-bar-top_20260110_122359.png`

---

##### Labyrinth
| Playbook Section | File | Key Requirements |
|-----------------|------|------------------|
| Part 4.5 | `04-screens/home-activities.md` | - Path tracking<br>- Start/Goal markers<br>- Path validation<br>- Wrong path feedback |

**State Transitions:**
```
playing → levelComplete (reach ZIEL on valid path)
playing → home (tap home button)
```

**Assets:**
- Visual: `design/references/screens/Reference_Layrinth_Game_Screen.png`
- Navigation: `navigation-bar-top_20260110_122359.png`

---

##### Numbers (Wähle die Zahl)
| Playbook Section | File | Key Requirements |
|-----------------|------|------------------|
| Part 4.6 | `04-screens/home-activities.md` | - Number stone tablet<br>- Tracing or tapping<br>- Voice number prompts<br>- Wrong answer feedback |

**State Transitions:**
```
playing → levelComplete (correct number selected/traced)
playing → home (tap home button)
```

**Assets:**
- Visual: `design/references/screens/Reference_Numbers_Game_Screen.png`
- Navigation: `navigation-bar-top_20260110_122359.png`

---

#### Level Complete → Celebration Logic

| Playbook Section | File | Key Requirements |
|-----------------|------|------------------|
| Part 4.7 | `04-screens/celebration-treasure.md` | - **ONLY at 5-coin milestones**<br>- Check: `coins % 5 == 0`<br>- Award +1 coin first<br>- Then check for celebration |

**State Transitions:**
```
levelComplete → celebrationOverlay (IF coins % 5 == 0 AND coins > 0)
levelComplete → playing (next level) (IF coins % 5 != 0)
```

**Critical Logic:**
```swift
func onLevelComplete() {
    // Award coin first
    player.coins += 1
    
    // Then check for celebration
    if shouldShowCelebration() {
        showCelebrationOverlay()
    } else {
        loadNextLevel()
    }
}

func shouldShowCelebration() -> Bool {
    return player.coins % 5 == 0 && player.coins > 0
}
```

---

#### Celebration Overlay

| Playbook Section | File | Key Requirements |
|-----------------|------|------------------|
| Part 4.7 | `04-screens/celebration-treasure.md` | - **OVERLAY, not screen**<br>- Activity screen visible (40% dim)<br>- Confetti animation<br>- "Weiter" button<br>- Post-dismissal navigation |

**State Transitions:**
```
celebrationOverlay → treasureScreen (tap Weiter AND coins >= 10)
celebrationOverlay → playing (tap Weiter AND coins < 10)
```

**Assets:**
- Visual: `design/references/screens/Reference_Celebration_Overlay.png`
- Bennie: celebrating
- Lemminge: jumping/celebrating

**Critical Design Rules:**
```
╔══════════════════════════════════════════════════════════════════════╗
║  THIS IS AN OVERLAY - NOT A SEPARATE SCREEN                          ║
║                                                                       ║
║  ✅ Activity screen remains visible underneath (dimmed to 40%)       ║
║  ✅ No navigation away from activity screen                          ║
║  ✅ Overlay appears on top of activity                               ║
║  ✅ Dismissal triggers navigation check (treasure or continue)       ║
╚══════════════════════════════════════════════════════════════════════╝
```

**Implementation:**
```swift
struct CelebrationOverlay: View {
    let activityScreenContent: AnyView
    let coins: Int
    let onDismiss: () -> Void
    
    var body: some View {
        ZStack {
            // Activity screen (dimmed)
            activityScreenContent
                .opacity(0.4)
                .disabled(true)
            
            // Overlay content
            VStack {
                Text("Super gemacht!")
                CoinAnimation()
                BennieView(state: .celebrating)
                
                Button("Weiter →") {
                    handleDismiss()
                }
            }
            .background(Color.cream.opacity(0.9))
            .cornerRadius(24)
            
            // Confetti on top
            ConfettiAnimation()
        }
    }
    
    func handleDismiss() {
        if coins >= 10 {
            navigateToTreasure()
        } else {
            onDismiss()  // Continue in activity
        }
    }
}
```

---

#### Treasure Screen
| Playbook Section | File | Key Requirements |
|-----------------|------|------------------|
| Part 4.8 | `04-screens/celebration-treasure.md` | - Show current coins<br>- Two YouTube buttons<br>- Button states based on coins<br>- Coin deduction on selection |

**State Transitions:**
```
treasureScreen → videoSelection (tap 5min button, deduct 10 coins)
treasureScreen → videoSelection (tap 10min button, deduct 20 coins)
treasureScreen → home (tap back)
```

**Assets:**
- Visual: `design/references/screens/Reference_Treasure_Screen.png`
- Treasure chest: open state
- YouTube buttons (state-based)

**Button State Logic:**
```swift
func updateButtonStates(coins: Int) {
    button5min = coins >= 10 ? .active : .disabled
    button10min = coins >= 20 ? .active : .disabled
}
```

---

#### Video Selection Screen
| Playbook Section | File | Key Requirements |
|-----------------|------|------------------|
| Part 4.9 | `04-screens/video-parent.md` | - Pre-approved videos only<br>- Thumbnail grid<br>- Time indicator<br>- No YouTube browsing |

**State Transitions:**
```
videoSelection → videoPlaying (tap video)
videoSelection → treasureScreen (tap back)
```

**Assets:**
- No visual reference (need to create)
- Cached YouTube thumbnails

---

#### Video Player Screen
| Playbook Section | File | Key Requirements |
|-----------------|------|------------------|
| Part 4.10 | `04-screens/video-parent.md` | - Controlled playback<br>- Analog clock countdown<br>- 1-minute warning<br>- Auto-exit on time up |

**State Transitions:**
```
videoPlaying → home (time expires, automatic)
```

**Assets:**
- Analog clock component
- "Noch eine Minute" voice trigger
- "Die Zeit ist um" voice trigger

**Time-Up Logic:**
```swift
func onTimeExpired() {
    // Stop video
    youtubePlayer.pause()
    
    // Play message
    playBennie("zeit_ist_um.aac")
    
    // Show transition overlay
    showTimeUpOverlay = true
    
    // Navigate after 3 seconds
    DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
        navigateToHome()
    }
}
```

---

#### Parent Gate
| Playbook Section | File | Key Requirements |
|-----------------|------|------------------|
| Part 4.11 | `04-screens/video-parent.md` | - Math question (random addition)<br>- Answer validation<br>- New question after 3 wrong attempts<br>- Cancel button |

**State Transitions:**
```
parentGate → parentDashboard (correct answer)
parentGate → home (tap cancel)
```

**Math Question Logic:**
```swift
struct MathQuestion {
    let a: Int  // 5-15
    let b: Int  // 5-15
    var answer: Int { a + b }
    
    static func generate() -> MathQuestion {
        MathQuestion(
            a: Int.random(in: 5...15),
            b: Int.random(in: 5...15)
        )
    }
}
```

---

#### Parent Dashboard
| Playbook Section | File | Key Requirements |
|-----------------|------|------------------|
| Part 4.11 | `04-screens/video-parent.md` | - Per-player settings<br>- Video management<br>- Time limit controls<br>- Activity locks |

**State Transitions:**
```
parentDashboard → home (tap back)
```

---

## 🎯 State Transition Summary Table

Complete mapping of all state transitions:

| From State | Event | To State | Validation | Side Effects |
|------------|-------|----------|-----------|--------------|
| `loading` | progress=100% | `playerSelection` | Min 2s elapsed | Play narrator voice |
| `playerSelection` | tap(player) | `home` | - | Load player data |
| `home` | tap(activity) | `activitySelection` | Activity unlocked | - |
| `home` | tap(chest) | `treasureScreen` | coins ≥ 10 | - |
| `home` | tap(settings) | `parentGate` | - | Show math question |
| `activitySelection` | tap(subActivity) | `playing` | - | Start activity, play intro |
| `playing` | levelSuccess | `levelComplete` | - | +1 coin, success sound |
| `playing` | tap(home) | `home` | - | Save progress |
| `levelComplete` | coins % 5 == 0 | `celebrationOverlay` | - | Show overlay over activity |
| `levelComplete` | coins % 5 != 0 | `playing` (next) | - | Auto-advance to next level |
| `celebrationOverlay` | tap(weiter) | Check coins | - | Navigate based on coins |
| `celebrationOverlay` | coins ≥ 10 | `treasureScreen` | - | Auto-navigate |
| `celebrationOverlay` | coins < 10 | `playing` | - | Continue activity |
| `treasureScreen` | tap(5min) | `videoSelection` | coins ≥ 10 | Deduct 10 coins |
| `treasureScreen` | tap(10min) | `videoSelection` | coins ≥ 20 | Deduct 20 coins |
| `videoSelection` | tap(video) | `videoPlaying` | - | Start timer |
| `videoPlaying` | timeUp | `home` | - | "Time up" audio, save stats |
| `parentGate` | correctAnswer | `parentDashboard` | - | Grant access |
| `parentDashboard` | tap(back) | `home` | - | - |

---

## 🧩 Component Reference Mapping

### Navigation Components

| Component | File | States | Usage |
|-----------|------|--------|-------|
| **Navigation Bar** | `navigation-bar-top_20260110_122359.png` | Active | All activity screens |
| **Home Button** | Part of nav bar | Active, Pressed | Returns to home from any screen |
| **Sound Button** | `sound-button-wooden_20260110_123401.png` | On, Off | All screens except loading |
| **Settings Button** | `settings-button-wooden_20260110_123306.png` | Active | Home screen only |

### Activity Components

| Component | File | States | Usage |
|-----------|------|--------|-------|
| **Rätsel Button** | `activity-button-raetsel_20260110_123032.png` | Unlocked, Locked | Home screen |
| **Zahlen Button** | `activity-button-zahlen_20260110_123105.png` | Unlocked, Locked | Home screen |
| **Zeichnen Sign** | *(locked design needed)* | Locked (chains) | Home screen |
| **Logik Sign** | *(locked design needed)* | Locked (chains) | Home screen |

### Treasure Components

| Component | File | States | Usage |
|-----------|------|--------|-------|
| **Treasure Chest** | `treasure-chest-closed_20260110_122421.png` | Closed (coins < 10) | Home screen |
| **Treasure Chest** | `treasure-chest-open_20260110_122445.png` | Open, Glowing (coins ≥ 10) | Home, Treasure screen |

**Chest State Management:**
```swift
func getChestAsset(coins: Int) -> String {
    if coins >= 10 {
        return "treasure-chest-open_20260110_122445.png"
    } else {
        return "treasure-chest-closed_20260110_122421.png"
    }
}

func chestGlows(coins: Int) -> Bool {
    return coins >= 10
}

func chestTappable(coins: Int) -> Bool {
    return coins >= 10
}
```

---

## 📊 State Persistence Requirements

### From Playbook Part 5.4

**PlayerData Structure:**
```swift
struct PlayerData: Codable {
    var id: String                          // "alexander" or "oliver"
    var coins: Int                          // Current balance
    var totalCoinsEarned: Int               // Lifetime total
    var activityProgress: [String: Int]     // Activity -> highest level
    var lastPlayedDate: Date
    var totalPlayTimeToday: TimeInterval
    var videosWatched: [VideoRecord]
    var learningProfile: LearningProfile
}
```

**AppSettings Structure:**
```swift
struct AppSettings: Codable {
    var parentSettings: ParentSettings
    var lastActivePlayer: String?
    var audioEnabled: Bool = true
    var musicVolume: Float = 0.3
}
```

**State Save Points:**
- App background → Save current state
- Screen transition → Save navigation history
- Coin earned → Save player data
- Video watched → Save video record
- Settings changed → Save app settings

**State Restore Logic:**
```swift
func restoreState() {
    guard let savedState = loadSavedState() else {
        // No saved state, start fresh
        navigateToLoading()
        return
    }
    
    switch savedState {
    case .loading, .playerSelection:
        // These are initial states, restart
        navigateToLoading()
        
    case .home:
        // Safe to restore
        navigateToHome()
        
    case .activitySelection(let activity):
        // Restore to activity selection
        navigateToActivitySelection(activity)
        
    case .playing, .levelComplete:
        // Don't restore mid-activity, go to selection
        navigateToActivitySelection(savedActivity)
        
    case .celebrationOverlay:
        // Don't restore overlay, go to home
        navigateToHome()
        
    case .treasureScreen, .videoSelection:
        // Safe to restore
        restoreExactState(savedState)
        
    case .videoPlaying:
        // Video time expired, go home
        navigateToHome()
        
    case .parentGate, .parentDashboard:
        // Require re-authentication
        navigateToHome()
    }
}
```

---

## 🔧 Implementation Checklist

Use this checklist while implementing Phase 11:

### GameState Enum

- [ ] Defined all states from playbook Part 2.2
- [ ] Added associated values for `activitySelection` and `playing`
- [ ] Implemented `Codable` for state persistence
- [ ] Added state validation logic

### State Transitions

- [ ] Implemented all transitions from playbook Part 2.3
- [ ] Added transition validation (prevent invalid transitions)
- [ ] Added transition logging for debugging
- [ ] Added state change observers

### Navigation Coordinator

- [ ] Created AppCoordinator class
- [ ] Implemented screen transition animations (0.3s cross-fade)
- [ ] Added back button behavior (activities → home)
- [ ] Added home button (always goes to home)
- [ ] Added deep linking for parent dashboard

### Celebration Overlay

- [ ] Implemented as overlay (NOT separate screen)
- [ ] Activity screen visible underneath (40% dim)
- [ ] Confetti animation on top
- [ ] Only shows at 5-coin milestones
- [ ] Post-dismissal navigation logic (treasure or continue)

### State Persistence

- [ ] Save state on app background
- [ ] Restore state on app foreground
- [ ] Handle invalid states (reset to safe state)
- [ ] Save navigation history
- [ ] Save player data on coin changes

### Component Integration

- [ ] Navigation bar in all activities
- [ ] Home button functional
- [ ] Sound button functional
- [ ] Settings button triggers parent gate
- [ ] Treasure chest state-based display
- [ ] Activity buttons show lock/unlock states

### Testing

- [ ] Unit tests for all state transitions
- [ ] Integration tests for navigation flows
- [ ] State persistence tests
- [ ] Celebration overlay tests (5-coin only)
- [ ] Invalid state recovery tests
- [ ] Performance tests (state changes < 50ms)

---

## 📚 Quick Reference Links

### Playbook Files
- `docs/playbook/00-game-overview.md` - Core game loop
- `docs/playbook/02-screen-flow.md` - **PRIMARY: State machine**
- `docs/playbook/04-screens/loading-player.md` - Loading, Player Selection
- `docs/playbook/04-screens/home-activities.md` - Home, Activities
- `docs/playbook/04-screens/celebration-treasure.md` - **Celebration overlay rules**
- `docs/playbook/04-screens/video-parent.md` - Video, Parent
- `docs/playbook/05-technical-requirements.md` - Data structures
- `docs/playbook/07-quick-reference.md` - State rules summary

### Reference Screens
- `design/references/screens/Reference_Loading_Screen.png`
- `design/references/screens/Reference_Player_Selection_Screen.png`
- `design/references/screens/Reference_Menu_Screen.png`
- `design/references/screens/Reference_Matching_Game_Screen.png`
- `design/references/screens/Reference_Layrinth_Game_Screen.png`
- `design/references/screens/Reference_Numbers_Game_Screen.png`
- `design/references/screens/Reference_Celebration_Overlay.png`
- `design/references/screens/Reference_Treasure_Screen.png`

### Reference Components
- `design/references/components/navigation-bar-top_20260110_122359.png`
- `design/references/components/activity-button-raetsel_20260110_123032.png`
- `design/references/components/activity-button-zahlen_20260110_123105.png`
- `design/references/components/settings-button-wooden_20260110_123306.png`
- `design/references/components/sound-button-wooden_20260110_123401.png`
- `design/references/components/treasure-chest-closed_20260110_122421.png`
- `design/references/components/treasure-chest-open_20260110_122445.png`

---

**Document Version**: 1.0  
**Last Updated**: January 2026  
**For**: Phase 11 - State Management & Navigation  
**Status**: Ready for Implementation
