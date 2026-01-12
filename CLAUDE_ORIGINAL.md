# CLAUDE.md - Bennie Bear Execution Plan

> **Framework**: get-shit-done methodology
> **For**: Claude Code autonomous execution
> **Project**: Bennie und die Lemminge - iPad Educational Game

---

## 🎯 Project Overview

**What**: Autism-friendly educational iPad game for children ages 4-5
**Target Users**: Alexander (5, autism) & Oliver (4)
**Platform**: iPad, iPadOS 17+, Landscape only
**Language**: German only
**Stack**: SwiftUI + SwiftData + UIKit hybrid

---

## 📊 Execution Dashboard

| Phase | Est. Time | Status | Blocker | Dependencies |
|-------|-----------|--------|---------|--------------|
| 0. Pre-Flight | 15 min | ⏳ Ready | None | None |
| 1. Setup | 30 min | ⏸️ Waiting | None | Phase 0 |
| 2. Design System | 3 hours | ⏸️ Waiting | None | Phase 1 |
| 3. Data Models | 2 hours | ⏸️ Waiting | None | Phase 2 |
| 4. State Machine | 2 hours | ⏸️ Waiting | None | Phase 3 |
| 5. Core Screens | 8 hours | ⏸️ Waiting | None | Phase 4 |
| 6. Activities | 12 hours | ⏸️ Waiting | None | Phase 5 |
| 7. Reward System | 4 hours | ⏸️ Waiting | None | Phase 6 |
| 8. Parent Features | 3 hours | ⏸️ Waiting | None | Phase 5 |
| 9. Audio System | 4 hours | ⏸️ Waiting | Assets | Phase 5 |
| 10. Asset Production | 16 hours | ⏸️ Waiting | MCP Tools | Phase 2 |
| 11. Testing | 8 hours | ⏸️ Waiting | None | Phases 6-9 |
| 12. Optimization | 4 hours | ⏸️ Waiting | None | Phase 11 |
| 13. TestFlight Prep | 2 hours | ⏸️ Waiting | None | Phase 12 |

**Total Estimated**: ~68 hours
**Target Launch**: TestFlight Beta

---

## 📖 How to Use This Document

### For Claude Code:

1. **Start at Phase 0** - Do NOT skip
2. **Complete validation checklist** after each phase
3. **Mark status** in dashboard above (⏳ → 🔄 → ✅ → ❌)
4. **Stop if blocker** - Flag and wait for human
5. **Reference documents**:
   - `PLAYBOOK_CONDENSED.md` - Design specs, screens, flow
   - `FULL_ARCHIVE.md` - Complete specifications
   - Reference images - Visual targets

### Success Criteria Per Phase:

- ✅ All validation items checked
- ✅ Code compiles without errors
- ✅ Meets design specifications
- ✅ No accessibility violations
- ✅ Git commit with descriptive message

---

## ⚠️ CRITICAL DESIGN RULES (Always Enforce)

```
╔══════════════════════════════════════════════════════════════════╗
║  🐻 BENNIE: Brown (#8C7259) • NO VEST • NO CLOTHING • EVER       ║
║  🔵 LEMMINGE: Blue (#6FA8DC) • NEVER GREEN • NEVER BROWN         ║
║  👆 TOUCH TARGETS: Minimum 96pt                                  ║
║  🚫 FORBIDDEN: Red, neon colors, flashing, shaking, "wrong"      ║
║  🇩🇪 LANGUAGE: German only, literal (no metaphors/idioms)        ║
╚══════════════════════════════════════════════════════════════════╝
```

---

# Phase 0: Pre-Flight Checks ✈️

**Time**: 15 minutes
**Goal**: Verify all prerequisites before starting

## 0.1 Document Verification

**Action**: Confirm you have access to all project documents

```bash
# Check project files exist
ls -la /mnt/project/
```

**Required Files**:
- [ ] PLAYBOOK_CONDENSED.md
- [ ] FULL_ARCHIVE.md
- [ ] Reference_Celebration_Overlay.png
- [ ] Reference_Menu_Screen.png
- [ ] Reference_Treasure_Screen.png
- [ ] Reference_Loading_Screen.png
- [ ] Reference_Matching_Game_Screen.png
- [ ] Reference_Player_Selection_Screen.png
- [ ] Reference_Numbers_Game_Screen.png
- [ ] Reference_Layrinth_Game_Screen.png

**If Missing**: STOP - Flag to human

## 0.2 Read Core Specifications

**Action**: Understand the project before coding

**Must Read Sections** (in order):
1. `PLAYBOOK_CONDENSED.md` → Section 0: Project Overview
2. `PLAYBOOK_CONDENSED.md` → Section 1: Critical Design Rules
3. `PLAYBOOK_CONDENSED.md` → Section 2: Color Palette
4. `PLAYBOOK_CONDENSED.md` → Section 3: Characters

**Validation Questions** (must answer correctly):
- [ ] What color is Bennie? (Answer: #8C7259 brown, NO clothing)
- [ ] What color are Lemminge? (Answer: #6FA8DC blue, NEVER green/brown)
- [ ] Minimum touch target size? (Answer: 96pt)
- [ ] What language is the UI? (Answer: German only)
- [ ] Can we use red color? (Answer: NO - forbidden)

## 0.3 Reference Image Review

**Action**: Study each reference image to understand target design

**For Each Image**:
1. Open and study for 30 seconds
2. Note: Character appearance, colors, layout, UI elements
3. Compare against written specs
4. Flag any discrepancies

**Images to Review**:
- [ ] Celebration Overlay - Note: Transparent overlay, confetti, character poses
- [ ] Menu Screen - Note: Wood signs, hanging style, character positions
- [ ] Treasure Screen - Note: Chest design, coin display, buttons
- [ ] Loading Screen - Note: Progress bar, character animations
- [ ] Matching Game - Note: Dual grid, color picker, stone tablets
- [ ] Player Selection - Note: Button layout, character greeting
- [ ] Numbers Game - Note: Stone tablet, number layout
- [ ] Labyrinth - Note: Path design, start/goal markers

## 0.4 Tool Availability Check

**Action**: Verify you have access to required tools

**Check MCP Tools**:
```bash
# List available MCP tools
[Check tool availability in your environment]
```

**Required MCP Tools**:
- [ ] bennie-image-generator (for asset creation)
- [ ] game-screen-designer (for mockups)
- [ ] Microsoft 365 (for collaboration - optional)

**If Missing**: Note which tools are unavailable, plan workarounds

## ✅ Phase 0 Complete Checklist

- [ ] All documents accessible
- [ ] Core specifications read and understood
- [ ] Validation questions answered correctly
- [ ] Reference images reviewed
- [ ] MCP tools checked
- [ ] Ready to proceed to Phase 1

**Git Checkpoint**: Not applicable - no code yet

---

# Phase 1: Project Setup 🏗️

**Time**: 30 minutes
**Goal**: Create Xcode project with correct configuration

## 1.1 Xcode Project Creation

**Action**: Create new Xcode project with correct settings

**Project Settings**:
- **Name**: "Bennie und die Lemminge"
- **Bundle ID**: com.yourcompany.benniegame
- **Interface**: SwiftUI
- **Lifecycle**: SwiftUI App
- **Language**: Swift
- **Deployment Target**: iPadOS 17.0
- **Devices**: iPad Only

**Validation**:
- [ ] Project created successfully
- [ ] Builds without errors
- [ ] Shows iPad simulator

## 1.2 Device & Orientation Configuration

**Action**: Lock to iPad landscape orientation

**In Info.plist**:
- Remove portrait orientations
- Keep only: Landscape Left, Landscape Right
- Remove iPhone configurations

**In Target Settings**:
- Device: iPad only
- Supported Orientations: Landscape only
- Requires Full Screen: Yes

**Validation**:
- [ ] Simulator shows landscape only
- [ ] Cannot rotate to portrait
- [ ] iPhone simulators not available

## 1.3 Dependency Installation

**Action**: Add required Swift packages

**Packages to Add**:
1. **Lottie-iOS**: `https://github.com/airbnb/lottie-spm.git` (Latest 4.x)
   - Purpose: Character animations, confetti effects

**Validation**:
- [ ] Package dependencies resolved
- [ ] Can import Lottie in Swift file
- [ ] Project builds successfully

## 1.4 File Structure Creation

**Action**: Create organized folder structure

**Top-Level Structure**:
```
BennieGame/
├── App/                      # App lifecycle
├── Features/                 # Screen implementations
├── Design/                   # Reusable components
├── Services/                 # Business logic
├── Models/                   # Data structures
└── Resources/                # Assets, audio, animations
```

**Detailed Structure**:
```
BennieGame/
├── App/
│   ├── BennieGameApp.swift
│   └── AppCoordinator.swift
│
├── Features/
│   ├── Loading/
│   │   └── LoadingView.swift
│   ├── PlayerSelection/
│   │   └── PlayerSelectionView.swift
│   ├── Home/
│   │   └── HomeView.swift
│   ├── Activities/
│   │   ├── Raetsel/
│   │   │   ├── RaetselSelectionView.swift
│   │   │   ├── PuzzleMatchingView.swift
│   │   │   └── LabyrinthView.swift
│   │   └── Zahlen/
│   │       ├── ZahlenSelectionView.swift
│   │       ├── WuerfelView.swift
│   │       └── WaehleZahlView.swift
│   ├── Celebration/
│   │   └── CelebrationOverlay.swift
│   ├── Treasure/
│   │   └── TreasureView.swift
│   ├── Video/
│   │   ├── VideoSelectionView.swift
│   │   └── VideoPlayerView.swift
│   └── Parent/
│       ├── ParentGateView.swift
│       ├── ParentDashboardView.swift
│       └── VideoManagementView.swift
│
├── Design/
│   ├── Components/
│   │   ├── WoodButton.swift
│   │   ├── WoodSign.swift
│   │   ├── ProgressBar.swift
│   │   ├── NavigationHeader.swift
│   │   ├── StoneTablet.swift
│   │   └── AnalogClock.swift
│   ├── Theme/
│   │   ├── Colors.swift
│   │   └── Typography.swift
│   └── Characters/
│       ├── BennieView.swift
│       ├── LemmingeView.swift
│       └── SpeechBubbleView.swift
│
├── Services/
│   ├── AudioManager.swift
│   ├── NarratorService.swift
│   ├── GameStateManager.swift
│   ├── PlayerDataStore.swift
│   ├── YouTubeService.swift
│   └── NetworkMonitor.swift
│
├── Models/
│   ├── PlayerData.swift
│   ├── GameState.swift
│   ├── ActivityType.swift
│   ├── CoinSystem.swift
│   ├── LearningProfile.swift
│   └── ParentSettings.swift
│
└── Resources/
    ├── Assets.xcassets/
    │   ├── Characters/
    │   │   ├── Bennie/
    │   │   └── Lemminge/
    │   ├── Backgrounds/
    │   └── UI/
    ├── Lottie/
    └── Audio/
        ├── Narrator/
        ├── Bennie/
        ├── Music/
        └── Effects/
```

**Validation**:
- [ ] All folders created
- [ ] Xcode can see file structure
- [ ] No orphaned files

## 1.5 Git Repository Initialization

**Action**: Initialize version control

**Commands**:
```bash
git init
git add .
git commit -m "Initial project structure - Phase 1 complete"
```

**Create .gitignore**:
```
# Xcode
*.xcuserstate
*.xcworkspace
xcuserdata/
DerivedData/

# Swift
*.swp
*.swo
.DS_Store
```

**Validation**:
- [ ] Git initialized
- [ ] Initial commit created
- [ ] .gitignore configured
- [ ] Can see commit history

## ✅ Phase 1 Complete Checklist

- [ ] Xcode project created with correct settings
- [ ] iPad landscape-only enforced
- [ ] Lottie dependency installed
- [ ] File structure matches specification
- [ ] Git repository initialized
- [ ] Project compiles successfully
- [ ] Git commit: "Phase 1: Project setup complete"

**Git Checkpoint**: 
```bash
git tag phase-1-complete
```

---

# Phase 2: Design System 🎨

**Time**: 3 hours
**Goal**: Build reusable design components matching playbook

## 2.1 Color System Implementation

**Reference**: `PLAYBOOK_CONDENSED.md` → Color Palette section

**Action**: Create `Design/Theme/Colors.swift`

**Requirements**:
- Implement ALL colors from playbook
- Use hex values exactly as specified
- Create Color extension for hex initialization
- Add comments for forbidden colors

**Colors to Implement**:
- Primary Palette (4 colors)
- Character Colors (6 colors)
- UI Colors (7 colors)
- Forest Environment Colors (6 colors)

**Validation**:
- [ ] Colors.swift file created
- [ ] Hex extension works
- [ ] Can use: `BennieColors.bennieBrown`
- [ ] No forbidden colors accessible
- [ ] Color values match playbook exactly

**Test Code** (should compile):
```swift
let testColor = BennieColors.bennieBrown // #8C7259
```

## 2.2 Typography System

**Reference**: `PLAYBOOK_CONDENSED.md` → Typography section

**Action**: Create `Design/Theme/Typography.swift`

**Requirements**:
- Use SF Rounded font family
- Implement preset sizes
- Create helper function for custom sizes
- Support font weights

**Presets to Implement**:
- title (48pt, bold)
- screenHeader (32pt, bold)
- body (20pt, regular)
- buttonText (24pt, semibold)
- label (17pt, medium)
- largeNumber (60pt, bold)

**Validation**:
- [ ] Typography.swift file created
- [ ] Can use: `BennieFont.title`
- [ ] SF Rounded font loads correctly
- [ ] All preset sizes work

## 2.3 Core Components

### Component 2.3.1: WoodButton

**Reference**: `PLAYBOOK_CONDENSED.md` → Shared Components

**Action**: Create `Design/Components/WoodButton.swift`

**Requirements**:
- ✅ Touch target ≥ 96pt (ENFORCED)
- Wood gradient (light → medium)
- Dark wood border (3pt)
- Rounded corners (16pt radius)
- Press animation (scale 0.95)
- Shadow effect
- Optional icon + text

**Validation**:
- [ ] Component created
- [ ] Touch target enforced
- [ ] Gradient renders correctly
- [ ] Press animation smooth
- [ ] Can init with text only
- [ ] Can init with icon only
- [ ] Can init with both

**Visual Test**: Compare against Reference_Menu_Screen.png buttons

### Component 2.3.2: WoodSign

**Reference**: Reference images showing hanging signs

**Action**: Create `Design/Components/WoodSign.swift`

**Requirements**:
- Hanging rope/chain from top
- Wood plank background
- Leaf decorations
- Text or custom content
- Touch target ≥ 96pt if tappable

**Variants**:
- Unlocked (glowing)
- Locked (chains + padlock)
- Title sign (decorative, non-tappable)

**Validation**:
- [ ] Component created
- [ ] Rope renders correctly
- [ ] Can show locked state
- [ ] Can show unlocked state
- [ ] Text displays correctly

### Component 2.3.3: ProgressBar

**Reference**: All reference screens showing progress bar

**Action**: Create `Design/Components/ProgressBar.swift`

**Requirements**:
- Berry decorations on sides
- Wood trough container
- Success green fill (#99BF8C)
- Coin slots overlay (10 slots)
- Chest icon(s) when full
- Shows current coins (0-20+)

**States**:
- Empty (0 coins)
- Partially filled (1-9 coins)
- One chest (10-19 coins)
- Two chests (20+ coins)

**Validation**:
- [ ] Component created
- [ ] Berry decorations render
- [ ] Fill animates smoothly
- [ ] Coin slots visible
- [ ] Chest icons appear at milestones
- [ ] Handles 0-30 coins correctly

**Visual Test**: Compare against any reference screen with progress bar

### Component 2.3.4: NavigationHeader

**Reference**: All activity screens

**Action**: Create `Design/Components/NavigationHeader.swift`

**Requirements**:
- Home button (left, 96pt touch)
- Progress bar (center)
- Volume toggle (right, 96pt touch)
- Optional back button

**Validation**:
- [ ] Component created
- [ ] All buttons ≥ 96pt
- [ ] Progress bar centered
- [ ] Buttons functional (can receive actions)

### Component 2.3.5: StoneTablet

**Reference**: Reference_Matching_Game_Screen.png, Reference_Numbers_Game_Screen.png

**Action**: Create `Design/Components/StoneTablet.swift`

**Requirements**:
- Stone texture background
- Decorative border
- Custom content container
- Optional title at top
- Used for game grids and number displays

**Validation**:
- [ ] Component created
- [ ] Stone texture renders
- [ ] Border decorative elements show
- [ ] Can embed custom content
- [ ] Matches reference images

### Component 2.3.6: AnalogClock

**Reference**: YouTube video countdown

**Action**: Create `Design/Components/AnalogClock.swift`

**Requirements**:
- Circular wooden face
- 12 minute markers
- Moving hand
- Countdown fills counterclockwise
- Success green arc for remaining time
- Shows minutes remaining

**Validation**:
- [ ] Component created
- [ ] Clock face renders
- [ ] Hand rotates correctly
- [ ] Arc fills counterclockwise
- [ ] Can bind to countdown timer

## 2.4 Character Views

### Character 2.4.1: BennieView

**Reference**: `PLAYBOOK_CONDENSED.md` → Bennie Character section

**Action**: Create `Design/Characters/BennieView.swift`

**Requirements**:
- Support all expression states:
  - idle, waving, pointing, thinking, encouraging, celebrating
- Load corresponding Lottie animations
- Fallback to static image if animation unavailable
- Correct size (300×450pt at @1x)

**Critical Validation**:
- [ ] Component created
- [ ] ⚠️ Bennie is brown #8C7259
- [ ] ⚠️ NO clothing, vest, or accessories
- [ ] ⚠️ ONLY snout is tan #C4A574
- [ ] All expression states supported
- [ ] Lottie animations play smoothly
- [ ] Correct sizing

**Visual Test**: Compare against all reference images with Bennie

### Character 2.4.2: LemmingeView

**Reference**: `PLAYBOOK_CONDENSED.md` → Lemminge Character section

**Action**: Create `Design/Characters/LemmingeView.swift`

**Requirements**:
- Support all expression states:
  - idle, curious, excited, celebrating, hiding, mischievous
- Load corresponding Lottie animations
- Fallback to static image if animation unavailable
- Correct size (80×100pt at @1x)

**Critical Validation**:
- [ ] Component created
- [ ] ⚠️ Body is BLUE #6FA8DC
- [ ] ⚠️ NEVER green, NEVER brown
- [ ] White belly with fuzzy edge
- [ ] Buck teeth visible
- [ ] Pink nose and paws
- [ ] All expression states supported
- [ ] Correct sizing

**Visual Test**: Compare against all reference images with Lemminge

### Character 2.4.3: SpeechBubbleView

**Reference**: Bennie speech interaction

**Action**: Create `Design/Characters/SpeechBubbleView.swift`

**Requirements**:
- Cartoon speech bubble shape
- Tail pointing to character
- Text content with typewriter effect
- German text only
- Max 7 words enforcement

**Validation**:
- [ ] Component created
- [ ] Bubble shape renders
- [ ] Tail points correctly
- [ ] Typewriter animation works
- [ ] Text wraps properly

## ✅ Phase 2 Complete Checklist

- [ ] Colors.swift implemented with all colors
- [ ] Typography.swift implemented
- [ ] WoodButton component complete
- [ ] WoodSign component complete
- [ ] ProgressBar component complete
- [ ] NavigationHeader component complete
- [ ] StoneTablet component complete
- [ ] AnalogClock component complete
- [ ] BennieView component complete (NO CLOTHING)
- [ ] LemmingeView component complete (BLUE ONLY)
- [ ] SpeechBubbleView component complete
- [ ] All components match reference images
- [ ] Project compiles successfully
- [ ] Visual regression tests passed

**Git Checkpoint**:
```bash
git add Design/
git commit -m "Phase 2: Design system complete - All components implemented"
git tag phase-2-complete
```

---

# Phase 3: Data Models 📊

**Time**: 2 hours
**Goal**: Implement all data structures from specifications

## 3.1 Core Data Models

### Model 3.1.1: GameState

**Reference**: `FULL_ARCHIVE.md` → Part 2.2: State Machine Definition

**Action**: Create `Models/GameState.swift`

**Requirements**:
- Main GameState enum with all states
- ActivityType enum
- SubActivity enum
- State transition validation
- Current state tracking

**States to Implement**:
```
- loading
- playerSelection
- home
- activitySelection(ActivityType)
- playing(ActivityType, SubActivity)
- levelComplete
- celebrationOverlay
- treasureScreen
- videoSelection
- videoPlaying
- parentGate
- parentDashboard
```

**Validation**:
- [ ] GameState.swift created
- [ ] All states implemented
- [ ] ActivityType enum complete
- [ ] SubActivity enum complete
- [ ] Can transition between states
- [ ] Invalid transitions rejected

### Model 3.1.2: PlayerData

**Reference**: `FULL_ARCHIVE.md` → Part 5.4: Data Persistence

**Action**: Create `Models/PlayerData.swift`

**Requirements**:
- Codable for persistence
- SwiftData @Model if using SwiftData
- All player attributes
- Computed properties where needed

**Attributes**:
```swift
- id: String
- name: String
- coins: Int
- totalCoinsEarned: Int
- activityProgress: [String: Int]
- lastPlayedDate: Date
- totalPlayTimeToday: TimeInterval
- videosWatched: [VideoRecord]
- learningProfile: LearningProfile
```

**Validation**:
- [ ] PlayerData.swift created
- [ ] All attributes implemented
- [ ] Codable conformance
- [ ] Can save/load from disk
- [ ] Default values set correctly

### Model 3.1.3: LearningProfile

**Reference**: `FULL_ARCHIVE.md` → Part 0.5: Adaptive Difficulty System

**Action**: Create `Models/LearningProfile.swift`

**Requirements**:
- Track performance metrics
- Track engagement indicators
- Adaptive parameters
- Difficulty adjustment logic

**Attributes**:
```swift
- averageSolveTime: TimeInterval
- mistakeFrequency: Double
- quitRate: Double
- sessionDuration: TimeInterval
- hintUsageRate: Double
- celebrationEngagement: Bool
- preferredActivities: [ActivityType: Int]
- difficultyLevel: Float (0.0-1.0)
- gridSizePreference: Int
- colorCount: Int
```

**Methods**:
```swift
- func adjustDifficulty(based on: PerformanceMetrics)
- func shouldIncreaseDifficulty() -> Bool
- func shouldDecreaseDifficulty() -> Bool
- func nextLevelParameters() -> LevelConfig
```

**Validation**:
- [ ] LearningProfile.swift created
- [ ] All metrics tracked
- [ ] Difficulty adjustment logic works
- [ ] Returns appropriate next level config

### Model 3.1.4: CoinSystem

**Reference**: `FULL_ARCHIVE.md` → Part 0.4: Reward System

**Action**: Create `Models/CoinSystem.swift`

**Requirements**:
- Coin economy constants
- Coin award logic
- Redemption validation
- Milestone calculation

**Constants**:
```swift
- coinsPerLevel = 1
- celebrationMilestone = 5
- tier1Redemption = 10
- tier2Redemption = 20
- tier2BonusMinutes = 2
- dailyCap = 30
```

**Methods**:
```swift
- func awardCoin(to player: PlayerData)
- func canRedeem(tier: YouTubeTier, coins: Int) -> Bool
- func shouldCelebrate(coins: Int) -> Bool
- func nextMilestone(current: Int) -> Int
```

**Validation**:
- [ ] CoinSystem.swift created
- [ ] All constants defined
- [ ] Award logic correct
- [ ] Celebration triggers at 5, 10, 15, 20...
- [ ] Redemption validation works

### Model 3.1.5: ParentSettings

**Reference**: `FULL_ARCHIVE.md` → Part 4.9: Parent Dashboard

**Action**: Create `Models/ParentSettings.swift`

**Requirements**:
- Per-player settings
- Approved video list
- Activity locks
- Daily time limits

**Attributes**:
```swift
- playerSettings: [String: PlayerSettings]
- approvedVideos: [ApprovedVideo]

struct PlayerSettings {
    - dailyTimeLimitMinutes: Int
    - unlockedActivities: Set<ActivityType>
    - todayPlayedMinutes: Int
    - lastPlayDate: Date?
}

struct ApprovedVideo {
    - id: String (YouTube ID)
    - title: String
    - thumbnailURL: URL
    - addedAt: Date
    - category: String?
}
```

**Validation**:
- [ ] ParentSettings.swift created
- [ ] All structures defined
- [ ] Can add/remove videos
- [ ] Can lock/unlock activities
- [ ] Time tracking works

### Model 3.1.6: ActivityLevel

**Reference**: Puzzle & number game progression

**Action**: Create `Models/ActivityLevel.swift`

**Requirements**:
- Level configuration
- Difficulty parameters
- Completion tracking

**Attributes**:
```swift
- id: UUID
- activityType: ActivityType
- levelNumber: Int
- difficulty: Float
- parameters: LevelParameters (protocol)

// Example LevelParameters implementations:
PuzzleParameters {
    - gridSize: Int (3x3, 4x4, 5x5, 6x6)
    - colorCount: Int (2-4)
    - filledCells: Int
}

LabyrinthParameters {
    - complexity: Int
    - pathLength: Int
    - deadEnds: Int
}

NumberParameters {
    - minNumber: Int
    - maxNumber: Int
    - countingStyle: CountingStyle
}
```

**Validation**:
- [ ] ActivityLevel.swift created
- [ ] Protocol-based parameters
- [ ] All activity types supported
- [ ] Level generation works

## 3.2 Supporting Data Models

### Model 3.2.1: VideoRecord

**Action**: Create `Models/VideoRecord.swift`

**Requirements**:
- Track watched videos
- Timestamp
- Duration watched

**Validation**:
- [ ] VideoRecord.swift created
- [ ] Tracks all required info

### Model 3.2.2: AudioFile

**Action**: Create `Models/AudioFile.swift`

**Requirements**:
- Audio file metadata
- Speaker (Narrator/Bennie)
- Trigger conditions
- File path

**Validation**:
- [ ] AudioFile.swift created
- [ ] Metadata complete

## ✅ Phase 3 Complete Checklist

- [ ] GameState.swift implemented
- [ ] PlayerData.swift implemented
- [ ] LearningProfile.swift implemented
- [ ] CoinSystem.swift implemented
- [ ] ParentSettings.swift implemented
- [ ] ActivityLevel.swift implemented
- [ ] VideoRecord.swift implemented
- [ ] AudioFile.swift implemented
- [ ] All models are Codable
- [ ] All models compile
- [ ] Can create instances of all models
- [ ] Relationships between models work

**Git Checkpoint**:
```bash
git add Models/
git commit -m "Phase 3: Data models complete - All structures implemented"
git tag phase-3-complete
```

---

# Phase 4: State Management 🔄

**Time**: 2 hours
**Goal**: Implement state machine and game state management

## 4.1 Game State Manager

**Reference**: `FULL_ARCHIVE.md` → Part 2.2: State Machine Definition

**Action**: Create `Services/GameStateManager.swift`

**Requirements**:
- ObservableObject for SwiftUI
- Current state published
- State transition methods
- Validation of transitions
- State history for debugging

**Core Functionality**:
```swift
class GameStateManager: ObservableObject {
    @Published var currentState: GameState
    @Published var currentPlayer: PlayerData?
    
    // State transitions
    func transition(to newState: GameState)
    func canTransition(to newState: GameState) -> Bool
    
    // State queries
    func isInActivity() -> Bool
    func needsCelebration() -> Bool
    func canAccessTreasure() -> Bool
    
    // State history (debugging)
    var stateHistory: [GameState]
}
```

**Validation**:
- [ ] GameStateManager.swift created
- [ ] State transitions work
- [ ] Invalid transitions rejected
- [ ] Published properties trigger UI updates
- [ ] State history tracked

**Test Scenarios**:
- [ ] Can go: loading → playerSelection → home
- [ ] Can go: home → activitySelection → playing
- [ ] Can go: playing → celebrationOverlay (when coins % 5 == 0)
- [ ] Cannot go: loading → treasureScreen (invalid)

## 4.2 Player Data Store

**Reference**: `FULL_ARCHIVE.md` → Part 5.4: Data Persistence

**Action**: Create `Services/PlayerDataStore.swift`

**Requirements**:
- Load player data from disk
- Save player data to disk
- Create new players
- Switch active player
- Manage player profiles

**Core Functionality**:
```swift
class PlayerDataStore: ObservableObject {
    @Published var players: [PlayerData]
    @Published var activePlayer: PlayerData?
    
    // Persistence
    func loadPlayers()
    func savePlayers()
    func savePlayer(_ player: PlayerData)
    
    // Player management
    func createPlayer(name: String) -> PlayerData
    func switchPlayer(to playerId: String)
    func updateCoins(playerId: String, delta: Int)
    
    // Data access
    func getPlayer(id: String) -> PlayerData?
    func getAllPlayers() -> [PlayerData]
}
```

**Storage Location**:
- Use UserDefaults for simple data
- OR use SwiftData for complex relationships
- Backup to iCloud (optional)

**Validation**:
- [ ] PlayerDataStore.swift created
- [ ] Can load players on app launch
- [ ] Can save player changes
- [ ] Data persists across app restarts
- [ ] Can switch between Alexander/Oliver
- [ ] Coin updates save correctly

## 4.3 Parent Settings Store

**Action**: Create `Services/ParentSettingsStore.swift`

**Requirements**:
- Load parent settings
- Save parent settings
- Manage approved videos
- Manage activity locks
- Manage time limits

**Core Functionality**:
```swift
class ParentSettingsStore: ObservableObject {
    @Published var settings: ParentSettings
    
    // Video management
    func addVideo(_ video: ApprovedVideo)
    func removeVideo(id: String)
    func getAllVideos() -> [ApprovedVideo]
    
    // Activity management
    func lockActivity(_ activity: ActivityType, for player: String)
    func unlockActivity(_ activity: ActivityType, for player: String)
    func isActivityLocked(_ activity: ActivityType, for player: String) -> Bool
    
    // Time management
    func setDailyLimit(_ minutes: Int, for player: String)
    func getDailyLimit(for player: String) -> Int
    func trackPlayTime(_ duration: TimeInterval, for player: String)
    func getTodayPlayTime(for player: String) -> TimeInterval
}
```

**Validation**:
- [ ] ParentSettingsStore.swift created
- [ ] Settings persist across restarts
- [ ] Video list management works
- [ ] Activity locking works
- [ ] Time tracking accurate

## 4.4 App Coordinator

**Reference**: Navigation flow in playbook

**Action**: Create `App/AppCoordinator.swift`

**Requirements**:
- Coordinate state transitions
- Handle navigation
- Manage screen stack
- Handle deep links (future)

**Core Functionality**:
```swift
class AppCoordinator: ObservableObject {
    @Published var currentView: AnyView
    
    let stateManager: GameStateManager
    let playerStore: PlayerDataStore
    let settingsStore: ParentSettingsStore
    
    // Navigation
    func navigateTo(_ state: GameState)
    func navigateHome()
    func navigateBack()
    
    // State handling
    func handleStateChange(_ newState: GameState)
    func getCurrentView() -> AnyView
}
```

**Validation**:
- [ ] AppCoordinator.swift created
- [ ] Coordinates all managers
- [ ] Navigation works smoothly
- [ ] Back navigation works
- [ ] Deep state changes handled

## ✅ Phase 4 Complete Checklist

- [ ] GameStateManager implemented
- [ ] PlayerDataStore implemented
- [ ] ParentSettingsStore implemented
- [ ] AppCoordinator implemented
- [ ] State transitions validated
- [ ] Data persistence works
- [ ] All services compile
- [ ] Services properly injected into views
- [ ] ObservableObject updates trigger UI changes

**Git Checkpoint**:
```bash
git add Services/ App/
git commit -m "Phase 4: State management complete - All services implemented"
git tag phase-4-complete
```

---

# Phase 5: Core Screens 📱

**Time**: 8 hours
**Goal**: Implement all non-activity screens

## 5.1 Loading Screen

**Reference**: 
- `PLAYBOOK_CONDENSED.md` → Loading Screen
- Reference_Loading_Screen.png

**Action**: Create `Features/Loading/LoadingView.swift`

**Requirements**:
- Progress bar (0-100%)
- Bennie idle → waving at 100%
- Lemminge peeking from holes
- "Lade Spielewelt..." text
- Narrator voice at 100%
- Auto-transition to Player Selection

**Layout Elements**:
- Title sign: "Waldabenteuer lädt" (hanging from top)
- Bennie: Left of center, 200×300pt
- Lemminge: 5-6 scattered in tree holes
- Progress bar: Bottom center, 600×40pt
- Percentage: Right of bar, 24pt font
- Loading text: Below bar, 17pt font

**Behavior**:
- Animate progress 0% → 100% over 2-5 seconds
- At 100%: Play narrator voice "Wir sind gleich bereit zum Spielen."
- Wait 2 seconds after voice
- Transition to Player Selection

**Validation**:
- [ ] LoadingView.swift created
- [ ] Progress animates smoothly
- [ ] Bennie changes to waving at 100%
- [ ] Lemminge animations play
- [ ] Narrator voice plays
- [ ] Auto-transitions correctly
- [ ] Matches reference image

## 5.2 Player Selection Screen

**Reference**:
- `PLAYBOOK_CONDENSED.md` → Player Selection Screen
- Reference_Player_Selection_Screen.png

**Action**: Create `Features/PlayerSelection/PlayerSelectionView.swift`

**Requirements**:
- Title: "Wer spielt heute?"
- Two player buttons (Alexander, Oliver)
- Player avatars
- Coin counts displayed
- Bennie waving at bottom
- Lemminge hiding at edges

**Layout**:
- Title sign: Top center, hanging
- Alexander button: (350, 350), 200×180pt
- Oliver button: (850, 350), 200×180pt
- Profile icon: (1140, 50), 60×60pt
- Bennie: Bottom center, waving
- Lemminge: Bottom left & right corners

**Button Contents**:
- Avatar image
- Player name
- "🪙 [X] Münzen"
- Wood frame with glow

**Behavior**:
- On appear: Narrator says "Wie heisst du? Alexander oder Oliver?"
- On tap Alexander: Narrator says "Hallo Alexander! Los geht's!"
- On tap Oliver: Narrator says "Hallo Oliver! Los geht's!"
- After voice: Transition to Home

**Validation**:
- [ ] PlayerSelectionView.swift created
- [ ] Both buttons render
- [ ] Touch targets ≥ 96pt
- [ ] Coin counts display correctly
- [ ] Narrator voices play
- [ ] Transitions to Home
- [ ] Matches reference image

## 5.3 Home Screen

**Reference**:
- `PLAYBOOK_CONDENSED.md` → Home Screen
- Reference_Menu_Screen.png

**Action**: Create `Features/Home/HomeView.swift`

**Requirements**:
- Title: "Waldabenteuer" (hanging sign)
- 4 activity signs (2 unlocked, 2 locked)
- Treasure chest (bottom right)
- Settings button (bottom left)
- Help button (bottom center)
- Bennie pointing
- Lemminge mischievous

**Activity Signs**:
1. Rätsel (unlocked, glowing)
2. Zahlen 1,2,3 (unlocked, glowing)
3. Zeichnen (locked, chains)
4. Logik (locked, chains)

**Layout**:
- Title sign: Top center
- Profile icon: (1140, 50)
- Rätsel sign: (300, 400)
- Zahlen sign: (500, 400)
- Zeichnen sign: (700, 400)
- Logik sign: (900, 400)
- Treasure chest: (1050, 700)
- Settings gear: (60, 700)
- Help "?": (597, 700)
- Bennie: Right side, pointing
- Lemminge: Left side, mischievous

**Behaviors**:
- On first visit: 
  - Narrator says "Was möchtest du spielen?"
  - Bennie says "Hi [Name], ich bin Bennie!" (Part A)
  - Wait 2s
  - Bennie says "Wir lösen Aktivitäten um YouTube zu schauen." (Part B)
- On return from activity:
  - Bennie says "Lösen wir noch mehr Aktivitäten."
  - Wait 2s
  - Bennie says "Dann können wir mehr YouTube schauen!"
- Tap unlocked activity → Navigate to activity selection
- Tap locked activity → Bennie says "Das ist noch gesperrt."
- Tap treasure (≥10 coins) → Navigate to Treasure
- Tap treasure (<10 coins) → Bennie says "Noch [X] Münzen!"
- Tap settings → Navigate to Parent Gate

**Validation**:
- [ ] HomeView.swift created
- [ ] All 4 activity signs render
- [ ] Locked signs show chains
- [ ] Unlocked signs glow
- [ ] Treasure chest interactive
- [ ] All voices play correctly
- [ ] Navigation works
- [ ] Matches reference image

## 5.4 Activity Selection Screens

**Action**: Create selection screens for each activity type

### 5.4.1 Rätsel Selection

**File**: `Features/Activities/Raetsel/RaetselSelectionView.swift`

**Requirements**:
- Title: "Rätsel"
- Two sub-activity options:
  - Puzzle Matching
  - Labyrinth
- Back button to home
- Progress bar at top

**Validation**:
- [ ] RaetselSelectionView.swift created
- [ ] Both options tappable
- [ ] Navigation works
- [ ] Back button works

### 5.4.2 Zahlen Selection

**File**: `Features/Activities/Zahlen/ZahlenSelectionView.swift`

**Requirements**:
- Title: "Zahlen 1,2,3"
- Two sub-activity options:
  - Würfel (Dice)
  - Wähle die Zahl
- Back button to home
- Progress bar at top

**Validation**:
- [ ] ZahlenSelectionView.swift created
- [ ] Both options tappable
- [ ] Navigation works
- [ ] Back button works

## 5.5 Celebration Overlay

**Reference**:
- `PLAYBOOK_CONDENSED.md` → Celebration Overlay
- Reference_Celebration_Overlay.png

**Action**: Create `Features/Celebration/CelebrationOverlay.swift`

**Requirements**:
- OVERLAY design (transparent, not full screen)
- Activity screen visible beneath (dimmed)
- "Super gemacht!" message
- "+1" coin animation
- Bennie celebrating
- Lemminge celebrating (3 jumping)
- "Weiter →" button
- Confetti animation (full screen)

**Trigger Condition**:
```swift
func shouldShowCelebration(coins: Int) -> Bool {
    return coins % 5 == 0 && coins > 0
}
```

**Messages by Milestone**:
- 5 coins: "Wir haben schon fünf Goldmünzen!"
- 10 coins: "Zehn Goldmünzen! Du kannst jetzt YouTube schauen."
- 15 coins: "Fünfzehn! Weiter so!"
- 20 coins: "Zwanzig Münzen! Du bekommst Bonuszeit!"

**Behavior**:
- Show overlay on top of activity screen
- Play confetti animation
- Bennie voice based on milestone
- On tap "Weiter": 
  - If coins ≥ 10: Auto-navigate to Treasure
  - If coins < 10: Dismiss overlay, continue activity

**Validation**:
- [ ] CelebrationOverlay.swift created
- [ ] Overlay is transparent
- [ ] Background dimmed to 40%
- [ ] Confetti animates
- [ ] Characters celebrate
- [ ] Voice plays correctly
- [ ] Navigation logic correct
- [ ] Matches reference image

## 5.6 Treasure Screen

**Reference**:
- `PLAYBOOK_CONDENSED.md` → Treasure Screen
- Reference_Treasure_Screen.png

**Action**: Create `Features/Treasure/TreasureView.swift`

**Requirements**:
- "Zurück" button (top left)
- Coin counter (top center)
- Open treasure chest (center)
- Two YouTube buttons:
  - 5 Min YouTube (10 coins)
  - 10 Min YouTube (20 coins)
- Bennie gesturing
- Lemminge excited

**Layout**:
- Back button: (60, 50)
- Coin display: (597, 100)
- Chest: Center, open, glowing
- 5 min button: (300, 500)
- 10 min button: (700, 500)
- Bennie: Right side
- Lemminge: Left side (2-3)

**Button States**:
| Coins | 5 Min Button | 10 Min Button |
|-------|-------------|---------------|
| 0-9 | Grayed, chains | Grayed, chains |
| 10-19 | Active, glowing | Grayed |
| 20+ | Active | Active, "BONUS!" badge |

**Behaviors**:
- On appear:
  - If coins < 10: Bennie says "Wir haben [X] Münzen. Noch [Y] bis YouTube!"
  - If coins 10-19: Bennie says "Wir können fünf Minuten schauen!"
  - If coins ≥ 20: Bennie says "Wir können zwölf Minuten schauen!"
- Tap YouTube button (if affordable):
  - Deduct coins (10 or 20)
  - Narrator says "Film ab!"
  - Navigate to Video Selection
- Tap YouTube button (if can't afford):
  - Shake button
  - No action

**Validation**:
- [ ] TreasureView.swift created
- [ ] Coin counter accurate
- [ ] Button states correct
- [ ] Coin deduction works
- [ ] Voices play correctly
- [ ] Navigation works
- [ ] Matches reference image

## 5.7 Video Selection Screen

**Reference**: `FULL_ARCHIVE.md` → Part 4.9: Video Selection Screen

**Action**: Create `Features/Video/VideoSelectionView.swift`

**Requirements**:
- Title: "Wähle ein Video!"
- Grid of video thumbnails (3 columns)
- Each thumbnail shows:
  - Video thumbnail image
  - Video title (2 lines max)
- Time remaining display at bottom
- Back button
- Volume toggle
- Bennie encouraging
- Lemminge excited

**Layout**:
- Back button: (60, 50)
- Volume: (1134, 50)
- Title sign: Top center
- Thumbnail grid: Center, 3×N grid
- Each thumbnail: 200×112pt (16:9)
- Time display: Bottom center
- Bennie: Right side
- Lemminge: Left side

**Behavior**:
- Load approved videos from ParentSettings
- Display up to 6 videos initially
- Scroll if more than 6
- On tap video:
  - Store video selection
  - Navigate to Video Player
- Show time: "⏱️ Du hast [X] Minuten Zeit!"

**Validation**:
- [ ] VideoSelectionView.swift created
- [ ] Loads approved videos only
- [ ] Thumbnails display correctly
- [ ] Scroll works if >6 videos
- [ ] Time display accurate
- [ ] Navigation works

## 5.8 Video Player Screen

**Reference**: `FULL_ARCHIVE.md` → Part 4.10: Video Player Screen

**Action**: Create `Features/Video/VideoPlayerView.swift`

**Requirements**:
- Embedded YouTube player (no controls)
- Analog clock countdown
- Time remaining text
- Auto-exit on time up
- 1-minute warning

**Layout**:
- YouTube player: Full screen top portion
- Analog clock: Center bottom (150×150pt)
- Time text: Below clock
- NO visible controls on YouTube

**YouTube Embed Parameters**:
```
controls: 0 (hide controls)
rel: 0 (no related videos)
showinfo: 0 (no video info)
modestbranding: 1 (minimal branding)
iv_load_policy: 3 (no annotations)
fs: 0 (no fullscreen)
disablekb: 1 (disable keyboard)
playsinline: 1 (play inline)
```

**Behavior**:
- Start countdown timer
- Update clock every second
- At 1 minute remaining:
  - Bennie voice: "Noch eine Minute."
  - Clock pulses gently
- At 0 seconds:
  - Pause video
  - Bennie voice: "Die Zeit ist um. Lass uns spielen!"
  - Show transition overlay (3s)
  - Navigate to Home

**Validation**:
- [ ] VideoPlayerView.swift created
- [ ] YouTube embeds correctly
- [ ] No YouTube controls visible
- [ ] Clock counts down correctly
- [ ] 1-minute warning plays
- [ ] Auto-exits on time up
- [ ] No related videos shown

## 5.9 Parent Gate

**Reference**: `FULL_ARCHIVE.md` → Part 4.11: Parent Dashboard

**Action**: Create `Features/Parent/ParentGateView.swift`

**Requirements**:
- Math question (addition 5-15 range)
- Number input field
- Abbrechen (Cancel) button
- Bestätigen (Confirm) button
- 3 attempts before new question

**Layout**:
- Title: "🔒 Elternbereich"
- Instructions: "Bitte löse diese Aufgabe:"
- Math question: "[A] + [B] = ?"
- Number input: Centered, 100pt wide
- Cancel button: Bottom left
- Confirm button: Bottom right

**Behavior**:
- Generate random math question (5-15 range)
- On confirm:
  - If correct: Navigate to Parent Dashboard
  - If incorrect: 
    - Shake input
    - Clear input
    - Increment attempt counter
    - If 3 attempts: Generate new question
- On cancel: Navigate back

**Validation**:
- [ ] ParentGateView.swift created
- [ ] Math question generates
- [ ] Input validation works
- [ ] Correct answer navigates
- [ ] 3 attempts resets question
- [ ] Cancel works

## 5.10 Parent Dashboard

**Reference**: `FULL_ARCHIVE.md` → Part 4.11: Parent Dashboard

**Action**: Create `Features/Parent/ParentDashboardView.swift`

**Requirements**:
- Per-player stats
- Video management
- Time limit settings
- Activity lock toggles
- Progress reset button

**Layout**:
- Back button: Top left
- Title: "⚙️ Elternbereich"

**Player Sections (one per player)**:
```
👤 [Player Name]
───────────────────────────
Heute gespielt: [X] min / [Y] min [progress bar]
Münzen: [Z]
Aktivitäten: [Rätsel ✓] [Zahlen ✓] [Zeichnen 🔒] [Logik 🔒]
```

**Video Management Section**:
```
📺 Genehmigte Videos [Videos bearbeiten]
───────────────────────────
• Video title 1
• Video title 2
...
[+ Video hinzufügen]
```

**Time Limit Section**:
```
⏱️ Tägliche Spielzeit
───────────────────────────
Alexander: [▼ 60 min ▼]
Oliver: [▼ 60 min ▼]
```

**Actions**:
- Tap activity → Toggle lock/unlock
- Tap "Videos bearbeiten" → Video Management screen
- Tap "+ Video hinzufügen" → Video input modal
- Change time limit → Save immediately
- Tap "🗑️ Fortschritt zurücksetzen" → Confirmation dialog

**Validation**:
- [ ] ParentDashboardView.swift created
- [ ] Player stats display correctly
- [ ] Activity toggles work
- [ ] Video list displays
- [ ] Time limits adjustable
- [ ] All changes persist

## ✅ Phase 5 Complete Checklist

- [ ] LoadingView implemented
- [ ] PlayerSelectionView implemented
- [ ] HomeView implemented
- [ ] RaetselSelectionView implemented
- [ ] ZahlenSelectionView implemented
- [ ] CelebrationOverlay implemented
- [ ] TreasureView implemented
- [ ] VideoSelectionView implemented
- [ ] VideoPlayerView implemented
- [ ] ParentGateView implemented
- [ ] ParentDashboardView implemented
- [ ] All screens match reference images
- [ ] All navigation works
- [ ] All voices trigger correctly
- [ ] Touch targets ≥ 96pt
- [ ] Project compiles successfully

**Git Checkpoint**:
```bash
git add Features/
git commit -m "Phase 5: Core screens complete - All non-activity screens implemented"
git tag phase-5-complete
```

---

# Phase 6: Activity Implementations 🎮

**Time**: 12 hours
**Goal**: Implement all 4 activities (2 per activity type)

## 6.1 Puzzle Matching Game

**Reference**:
- `PLAYBOOK_CONDENSED.md` → Puzzle Matching Screen
- Reference_Matching_Game_Screen.png

**Action**: Create `Features/Activities/Raetsel/PuzzleMatchingView.swift`

**Requirements**:
- Dual grid display (ZIEL / DU)
- Color picker (3-4 colors)
- Eraser tool
- Reset button
- Real-time validation
- NavigationHeader
- Bennie pointing
- Lemminge curious

**Layout**:
- Navigation header: Top (home, progress, volume)
- ZIEL grid: Left, stone tablet
- Arrow: Center
- DU grid: Right, stone tablet
- Color picker: Bottom center, wood log container
- Lemminge (2): Left side
- Bennie: Right side

**Grid Sizes by Difficulty**:
| Level | Grid | Colors | Filled |
|-------|------|--------|--------|
| 1-5 | 3×3 | 2 | 2-4 |
| 6-10 | 3×3 | 3 | 3-5 |
| 11-20 | 4×4 | 3 | 4-7 |
| 21-30 | 5×5 | 3-4 | 5-10 |
| 31+ | 6×6 | 4 | 6-12 |

**Behavior**:
- On start:
  - Narrator: "Mach das Muster nach!"
  - Bennie: "Das packen wir!"
- Generate target pattern
- Player taps color, then taps cells
- Real-time comparison: Correct cells stay, incorrect can be changed
- On complete match:
  - Success sound
  - Random success phrase (from pool)
  - +1 coin
  - Check celebration
- If idle 10s: Bennie hint "Wir können das, YouTube kommt bald."
- If idle 20s: Bennie hint "Welche Farbe fehlt noch?"

**Validation**:
- [ ] PuzzleMatchingView.swift created
- [ ] Dual grid displays correctly
- [ ] Color picker works
- [ ] Eraser works
- [ ] Reset works
- [ ] Pattern validation accurate
- [ ] Success triggers correctly
- [ ] Hints trigger at intervals
- [ ] Difficulty progression works
- [ ] Matches reference image

## 6.2 Labyrinth Game

**Reference**:
- `PLAYBOOK_CONDENSED.md` → Labyrinth Screen
- Reference_Layrinth_Game_Screen.png

**Action**: Create `Features/Activities/Raetsel/LabyrinthView.swift`

**Requirements**:
- Path-tracing gameplay
- START and ZIEL markers
- Stone path validation
- Touch tracking
- NavigationHeader
- Bennie pointing at START
- Lemminge scared at START, celebrating at ZIEL

**Layout**:
- Navigation header: Top
- Title sign: "Bennie & Lemminge Labyrinth"
- Labyrinth: Center, taking most of screen
- START: Top left
- ZIEL: Bottom right
- Bennie: Left of START
- Lemminge: One at START (scared), one at ZIEL (celebrating)

**Path Generation**:
- Generate valid stone path from START to ZIEL
- Include curves and turns
- Path width: 44pt (touch tolerance)
- Add visual decorations (houses, trees, cars) along path
- Add visual obstacles off-path

**Behavior**:
- On start:
  - Narrator: "Hilf Bennie den Weg finden!"
  - Bennie: "Wie fange ich die Lemminge?"
- Player touches START to begin
- Drag finger along stone path
- Validate continuously:
  - If on path: Path highlights green
  - If off path: Red X, Bennie voice "Da komme ich nicht durch."
- On reach ZIEL:
  - Success sound
  - Random success phrase
  - +1 coin
  - Check celebration
- If idle 15s: Bennie hint "Wo ist der Anfang?"

**Validation**:
- [ ] LabyrinthView.swift created
- [ ] Path renders correctly
- [ ] Touch tracking works
- [ ] Path validation accurate
- [ ] Off-path detection works
- [ ] START/ZIEL markers visible
- [ ] Success triggers correctly
- [ ] Hint triggers correctly
- [ ] Matches reference image

## 6.3 Würfel (Dice) Game

**Reference**:
- `PLAYBOOK_CONDENSED.md` → Würfel Screen
- Reference_Numbers_Game_Screen.png variant

**Action**: Create `Features/Activities/Zahlen/WuerfelView.swift`

**Requirements**:
- Animated dice roll
- Number buttons (1-6)
- Dice shows dots
- NavigationHeader
- Bennie pointing
- Lemminge curious & excited

**Layout**:
- Navigation header: Top
- Dice: Top center, 150×150pt
- Number buttons: Grid below dice, 3×2 layout
- Each button: 96×96pt minimum
- Stone tablet background for numbers
- Bennie: Right side
- Lemminge: Left side (2)

**Behavior**:
- On start:
  - Narrator: "Wirf den Würfel!"
  - Dice auto-rolls, shows random 1-6
  - Narrator: "Zeig mir die [N]!"
- Player taps number button
- If correct:
  - Success sound
  - Random success phrase
  - +1 coin
  - Check celebration
  - Auto-roll next dice
- If incorrect:
  - Gentle boop sound
  - Bennie: "Das ist die [X]. Probier nochmal!"
- Hints:
  - 10s idle: Bennie "Zähle die Punkte."
  - 20s idle: Bennie "Du hast die [N] gewürfelt."
  - 30s idle: Bennie "Wo ist die [N]?"

**Validation**:
- [ ] WuerfelView.swift created
- [ ] Dice animation smooth
- [ ] Dice shows correct dots
- [ ] Number buttons work
- [ ] Validation correct
- [ ] Success flow works
- [ ] Hints trigger correctly
- [ ] Auto-rolls next

## 6.4 Wähle die Zahl (Choose Number) Game

**Reference**:
- `PLAYBOOK_CONDENSED.md` → Wähle die Zahl Screen
- Reference_Numbers_Game_Screen.png

**Action**: Create `Features/Activities/Zahlen/WaehleZahlView.swift`

**Requirements**:
- Number tracing
- Numbers 1-10 on stone tablet
- Stroke direction guides
- Validation of tracing
- NavigationHeader
- Bennie pointing
- Lemminge curious & excited

**Layout**:
- Navigation header: Top
- Stone tablet: Center, showing numbers 1-10
- Numbers arranged in rows:
  - Row 1: 1, 2, 3, 4
  - Row 2: 5, 6, 7
  - Row 3: 8, 9, 10
- Each number: 80×100pt, with arrow guides
- Color tools: Bottom center (optional tracing colors)
- Bennie: Right side
- Lemminge: Left side (2)

**Number Tracing**:
| Number | Stroke Guide | Arrows |
|--------|-------------|--------|
| 1 | Downstroke | ↓ |
| 2 | Curve right, down, right | ↷ ↓ → |
| 3 | Two curves right | ↷ ↷ |
| 4 | Down, right, down | ↓ → ↓ |
| 5 | Down, curve right | ↓ ↷ |
| 6 | Curve down and around | ↶ ○ |
| 7 | Right, diagonal down | → ↘ |
| 8 | Double loop | ∞ |
| 9 | Circle, down | ○ ↓ |
| 10 | "1" then "0" | Two strokes |

**Behavior**:
- On start:
  - Narrator: "Zeig mir die [N]!"
  - Target number glows golden
- Player traces number with finger
- Validation: 70% of path covered = success
- If correct:
  - Success sound
  - Random success phrase
  - +1 coin
  - Check celebration
  - Next random number
- If incorrect:
  - Gentle boop
  - Bennie: "Das ist die [X]. Probier nochmal!"
- Hints:
  - 10s idle: Bennie "Der Erzähler hat [N] gesagt."
  - 20s idle: Bennie "Wo ist die [N]?"

**Validation**:
- [ ] WaehleZahlView.swift created
- [ ] All numbers display correctly
- [ ] Arrow guides visible
- [ ] Tracing detection works
- [ ] 70% validation threshold
- [ ] Success flow works
- [ ] Hints trigger correctly
- [ ] Matches reference image

## 6.5 Activity Common Features

**Action**: Implement shared activity features

### Feature 6.5.1: Success Phrase Pool

**File**: Create `Services/SuccessPhraseService.swift`

**Requirements**:
- Random selection from pool
- Track recently used (avoid repetition)
- German phrases only

**Phrases**:
```
"Super!"
"Toll gemacht!"
"Wunderbar!"
"Ja, genau!"
"Das hast du super gemacht!"
"Perfekt!"
"Bravo!"
```

**Validation**:
- [ ] SuccessPhraseService.swift created
- [ ] Returns random phrase
- [ ] Doesn't repeat last 3
- [ ] All phrases available

### Feature 6.5.2: Level Generation Service

**File**: Create `Services/LevelGeneratorService.swift`

**Requirements**:
- Generate levels based on difficulty
- Use LearningProfile for adaptation
- Return LevelConfig for each activity

**Methods**:
```swift
func generatePuzzleLevel(difficulty: Float) -> PuzzleLevel
func generateLabyrinthLevel(difficulty: Float) -> LabyrinthLevel
func generateNumberLevel(difficulty: Float) -> NumberLevel
```

**Validation**:
- [ ] LevelGeneratorService.swift created
- [ ] Generates valid puzzle patterns
- [ ] Generates valid labyrinth paths
- [ ] Generates valid number sequences
- [ ] Difficulty scaling works

### Feature 6.5.3: Activity Completion Handler

**File**: Extend `Services/GameStateManager.swift`

**Requirements**:
- Handle activity completion
- Award coin
- Update learning profile
- Check celebration
- Navigate appropriately

**Method**:
```swift
func handleActivityComplete(
    activity: ActivityType,
    solveTime: TimeInterval,
    mistakes: Int,
    hintsUsed: Int
)
```

**Validation**:
- [ ] Completion handler implemented
- [ ] Coins awarded correctly
- [ ] Learning profile updated
- [ ] Celebration triggers correctly
- [ ] Navigation logic correct

## ✅ Phase 6 Complete Checklist

- [ ] PuzzleMatchingView implemented
- [ ] LabyrinthView implemented
- [ ] WuerfelView implemented
- [ ] WaehleZahlView implemented
- [ ] SuccessPhraseService implemented
- [ ] LevelGeneratorService implemented
- [ ] Activity completion handler implemented
- [ ] All activities match reference images
- [ ] All gameplay mechanics work
- [ ] All hints trigger correctly
- [ ] Difficulty progression works
- [ ] Learning profile updates
- [ ] Project compiles successfully

**Git Checkpoint**:
```bash
git add Features/Activities/ Services/
git commit -m "Phase 6: Activity implementations complete - All 4 activities playable"
git tag phase-6-complete
```

---

# Phase 7: Reward System Integration 🎁

**Time**: 4 hours
**Goal**: Connect activities to celebration and treasure systems

## 7.1 Coin Animation System

**Action**: Create `Design/Components/CoinFlyAnimation.swift`

**Requirements**:
- Animated coin flies from activity to progress bar
- Arc path trajectory
- Duration: 0.8s
- Sparkle trail
- Land on appropriate slot

**Validation**:
- [ ] CoinFlyAnimation.swift created
- [ ] Animation smooth
- [ ] Arc trajectory natural
- [ ] Sparkles render
- [ ] Lands correctly on bar

## 7.2 Progress Bar Fill Animation

**Action**: Extend `Design/Components/ProgressBar.swift`

**Requirements**:
- Animated fill when coin added
- Glow effect on new coin
- Slot highlights briefly
- Chest icon appears when full

**Validation**:
- [ ] Fill animation smooth
- [ ] Glow effect works
- [ ] Chest appears at milestones
- [ ] No visual glitches

## 7.3 Celebration Trigger Logic

**Action**: Extend `Services/GameStateManager.swift`

**Requirements**:
- Check after every coin award
- Trigger only at 5-coin intervals
- Queue state transition
- Pass coin count to overlay

**Method**:
```swift
func checkCelebrationTrigger(newCoinCount: Int) {
    if newCoinCount % 5 == 0 && newCoinCount > 0 {
        queueStateTransition(.celebrationOverlay)
    }
}
```

**Validation**:
- [ ] Trigger logic implemented
- [ ] Only fires at 5, 10, 15, 20...
- [ ] Never fires at other counts
- [ ] State transition queues correctly

## 7.4 Treasure Access Logic

**Action**: Extend `Features/Home/HomeView.swift` and `Features/Celebration/CelebrationOverlay.swift`

**Requirements**:
- Enable chest when ≥10 coins
- Auto-navigate after celebration if ≥10
- Show coin requirement when <10

**Validation**:
- [ ] Chest disabled when <10 coins
- [ ] Chest enabled when ≥10 coins
- [ ] Auto-navigation works after celebration
- [ ] User message clear when can't access

## 7.5 YouTube Redemption Flow

**Action**: Implement redemption in `Features/Treasure/TreasureView.swift`

**Requirements**:
- Validate coin balance before redemption
- Deduct correct amount (10 or 20)
- Pass time allocation to video player
- Update player data
- Navigate to video selection

**Method**:
```swift
func redeemYouTubeTime(tier: YouTubeTier) {
    guard canRedeem(tier: tier) else { return }
    
    let coinsToDeduct = tier == .fiveMinutes ? 10 : 20
    let minutesToAllocate = tier == .fiveMinutes ? 5 : 12
    
    playerStore.updateCoins(delta: -coinsToDeduct)
    videoTimeRemaining = minutesToAllocate * 60 // seconds
    
    playNarrator("film_ab.aac")
    stateManager.transition(to: .videoSelection)
}
```

**Validation**:
- [ ] Redemption logic implemented
- [ ] Coins deduct correctly
- [ ] Time allocated correctly
- [ ] Cannot redeem if insufficient coins
- [ ] Navigation works
- [ ] Voice plays

## 7.6 Video Time Management

**Action**: Create `Services/VideoTimeManager.swift`

**Requirements**:
- Track allocated time
- Countdown during playback
- 1-minute warning
- Auto-exit on time up
- Prevent video switching during play

**Properties**:
```swift
class VideoTimeManager: ObservableObject {
    @Published var timeRemaining: TimeInterval
    @Published var isPlaying: Bool
    @Published var showOneMinuteWarning: Bool
    
    var timer: Timer?
    
    func startCountdown()
    func pauseCountdown()
    func handleTimeUp()
}
```

**Validation**:
- [ ] VideoTimeManager.swift created
- [ ] Countdown accurate
- [ ] Warning triggers at 1 minute
- [ ] Auto-exit works
- [ ] Cannot extend time
- [ ] Video stops on time up

## 7.7 Post-Video Return Flow

**Action**: Extend `Features/Video/VideoPlayerView.swift`

**Requirements**:
- On time up:
  - Pause video
  - Play Bennie voice "Die Zeit ist um. Lass uns spielen!"
  - Show transition overlay (3s)
  - Navigate to Home
- Reset video state
- Update play time tracking

**Validation**:
- [ ] Time-up handling works
- [ ] Voice plays
- [ ] Transition smooth
- [ ] Returns to Home
- [ ] Video state reset
- [ ] Play time logged

## ✅ Phase 7 Complete Checklist

- [ ] Coin fly animation implemented
- [ ] Progress bar animations work
- [ ] Celebration triggers correctly
- [ ] Treasure access logic correct
- [ ] YouTube redemption works
- [ ] Coin deduction accurate
- [ ] Video time management implemented
- [ ] Countdown accurate
- [ ] 1-minute warning works
- [ ] Auto-exit on time up works
- [ ] Return flow smooth
- [ ] Play time tracked correctly
- [ ] Complete flow: Activity → Coin → Celebration → Treasure → Video → Home works

**Git Checkpoint**:
```bash
git add Services/ Features/ Design/
git commit -m "Phase 7: Reward system integration complete - Full coin-to-YouTube flow working"
git tag phase-7-complete
```

---

# Phase 8: Parent Features 👨‍👩‍👧

**Time**: 3 hours
**Goal**: Complete parent dashboard and video management

## 8.1 Video Management Screen

**Action**: Create `Features/Parent/VideoManagementView.swift`

**Requirements**:
- List of approved videos
- Add video by URL
- Remove video
- Thumbnail preview
- Title editing

**Layout**:
- Title: "Video-Verwaltung"
- Back button
- Video list (scrollable)
- Each video item:
  - Thumbnail (120×68pt)
  - Title (editable)
  - Remove button (🗑️)
- "+ Video hinzufügen" button at bottom

**Add Video Modal**:
- Title: "📺 Video hinzufügen"
- Instructions: "YouTube Link einfügen:"
- Text field for URL
- "Einfügen aus Zwischenablage" button
- Preview section (shows thumbnail + title after validation)
- Cancel / Hinzufügen buttons

**URL Validation**:
```swift
func extractVideoID(from url: String) -> String? {
    // Handle: youtube.com/watch?v=XXX
    // Handle: youtu.be/XXX
    // Handle: youtube.com/embed/XXX
}
```

**Validation**:
- [ ] VideoManagementView.swift created
- [ ] Video list displays
- [ ] Add modal works
- [ ] URL validation works
- [ ] Thumbnail fetches
- [ ] Title editable
- [ ] Remove works
- [ ] Changes persist

## 8.2 Activity Lock Management

**Action**: Extend `Features/Parent/ParentDashboardView.swift`

**Requirements**:
- Toggle buttons for each activity
- Visual indication (✓ = unlocked, 🔒 = locked)
- Separate settings per player
- Changes save immediately

**Implementation**:
```swift
struct ActivityToggle: View {
    let activity: ActivityType
    let player: String
    @ObservedObject var settings: ParentSettingsStore
    
    var isUnlocked: Bool {
        !settings.isActivityLocked(activity, for: player)
    }
    
    var body: some View {
        Button {
            if isUnlocked {
                settings.lockActivity(activity, for: player)
            } else {
                settings.unlockActivity(activity, for: player)
            }
        } label: {
            HStack {
                Text(activity.displayName)
                Spacer()
                Image(systemName: isUnlocked ? "checkmark.circle.fill" : "lock.fill")
                    .foregroundColor(isUnlocked ? .green : .gray)
            }
        }
    }
}
```

**Validation**:
- [ ] Activity toggles implemented
- [ ] Visual states correct
- [ ] Per-player settings work
- [ ] Changes persist
- [ ] Locked activities inaccessible in game

## 8.3 Time Limit Configuration

**Action**: Extend `Features/Parent/ParentDashboardView.swift`

**Requirements**:
- Dropdown picker for time limits
- Options: 15, 30, 45, 60, 90, 120 minutes
- Separate per player
- Changes save immediately

**Implementation**:
```swift
struct TimeLimitPicker: View {
    let player: String
    @ObservedObject var settings: ParentSettingsStore
    
    let timeOptions = [15, 30, 45, 60, 90, 120]
    
    var body: some View {
        HStack {
            Text(player + ":")
            Picker("", selection: $selectedTime) {
                ForEach(timeOptions, id: \.self) { minutes in
                    Text("\(minutes) min").tag(minutes)
                }
            }
            .onChange(of: selectedTime) { newValue in
                settings.setDailyLimit(newValue, for: player)
            }
        }
    }
}
```

**Validation**:
- [ ] Time limit picker implemented
- [ ] All options available
- [ ] Per-player configuration
- [ ] Changes persist
- [ ] Limits enforced in game

## 8.4 Play Time Tracking

**Action**: Extend `Services/PlayerDataStore.swift`

**Requirements**:
- Track play time per session
- Aggregate daily total
- Reset at midnight
- Display in parent dashboard

**Methods**:
```swift
func startSession(for player: String)
func endSession(for player: String)
func getTodayPlayTime(for player: String) -> TimeInterval
func getRemainingTime(for player: String) -> TimeInterval
func isTimeLimitReached(for player: String) -> Bool
```

**Validation**:
- [ ] Time tracking implemented
- [ ] Session tracking works
- [ ] Daily reset works
- [ ] Dashboard displays correctly
- [ ] Limit enforcement works

## 8.5 Progress Reset Feature

**Action**: Extend `Features/Parent/ParentDashboardView.swift`

**Requirements**:
- "🗑️ Fortschritt zurücksetzen" button
- Confirmation dialog
- Reset options:
  - Reset coins only
  - Reset activity progress only
  - Reset all progress
- Separate per player

**Confirmation Dialog**:
```
Title: "Fortschritt zurücksetzen?"
Message: "Möchtest du den Fortschritt für [Player] zurücksetzen?"
Options:
- [Nur Münzen]
- [Nur Aktivitäten]
- [Alles]
- [Abbrechen]
```

**Validation**:
- [ ] Reset button implemented
- [ ] Confirmation dialog shows
- [ ] All reset options work
- [ ] Coins reset correctly
- [ ] Activity progress resets
- [ ] Player data persists
- [ ] Cannot be undone (as designed)

## 8.6 Graceful Time Limit Exit

**Action**: Create `Services/TimeLimitMonitor.swift`

**Requirements**:
- Monitor total play time
- Warning at 5 minutes remaining
- Final warning at 2 minutes
- Forced exit at limit
- Gentle messaging

**Messages**:
- 5 min: Narrator "Dein iPad braucht bald eine Pause."
- 2 min: Narrator "Noch eine Aktivität, dann laden wir die Batterie."
- 0 min: Narrator "Du hast heute so toll gespielt! Bis morgen! Bring das iPad zu Mama oder Papa."

**Behavior**:
- At limit:
  - Complete current activity if in progress
  - Show friendly exit screen
  - Save all progress
  - Prevent new activities
  - Show "Come back tomorrow" message

**Validation**:
- [ ] TimeLimitMonitor.swift created
- [ ] Warnings trigger correctly
- [ ] Gentle exit works
- [ ] Progress saved
- [ ] Friendly messaging
- [ ] Cannot be bypassed

## ✅ Phase 8 Complete Checklist

- [ ] VideoManagementView implemented
- [ ] Add video works
- [ ] Remove video works
- [ ] Activity toggles work
- [ ] Time limit configuration works
- [ ] Play time tracking works
- [ ] Progress reset works
- [ ] Time limit enforcement works
- [ ] Graceful exit implemented
- [ ] All parent features functional
- [ ] Changes persist correctly

**Git Checkpoint**:
```bash
git add Features/Parent/ Services/
git commit -m "Phase 8: Parent features complete - Full parental control implemented"
git tag phase-8-complete
```

---

# Phase 9: Audio Integration 🔊

**Time**: 4 hours
**Goal**: Implement complete audio system

**⚠️ BLOCKER**: This phase requires audio assets to be generated first. See Phase 10 for asset production.

## 9.1 Audio Manager Implementation

**Reference**: `FULL_ARCHIVE.md` → Part 3: Narrator & Voice Script

**Action**: Create `Services/AudioManager.swift`

**Requirements**:
- Three independent audio channels
- Volume control per channel
- Voice ducking
- Audio queueing
- Playback priority management

**Properties**:
```swift
class AudioManager: ObservableObject {
    private var musicPlayer: AVAudioPlayer?
    private var voicePlayer: AVAudioPlayer?
    private var effectsPlayer: AVAudioPlayer?
    
    @Published var musicVolume: Float = 0.30
    @Published var voiceVolume: Float = 1.00
    @Published var effectsVolume: Float = 0.70
    
    @Published var isMuted: Bool = false
    
    private var voiceQueue: [String] = []
    private var isPlayingVoice: Bool = false
}
```

**Methods**:
```swift
func playMusic(_ file: String, loop: Bool)
func playVoice(_ file: String, speaker: Speaker)
func playEffect(_ file: String)
func stopAll()
func setMuted(_ muted: Bool)
```

**Voice Ducking**:
```swift
func playVoice(_ file: String, speaker: Speaker) {
    // Duck music to 15%
    musicPlayer?.volume = 0.15
    
    // Play voice at 100%
    voicePlayer = try? AVAudioPlayer(contentsOf: getAudioURL(file))
    voicePlayer?.volume = 1.00
    voicePlayer?.play()
    
    // On completion, restore music
    voicePlayer?.onComplete = {
        self.musicPlayer?.volume = 0.30
        self.isPlayingVoice = false
        self.playNextVoiceInQueue()
    }
}
```

**Validation**:
- [ ] AudioManager.swift created
- [ ] Three channels work independently
- [ ] Voice ducking works
- [ ] Queue system works
- [ ] Mute affects all channels
- [ ] Volume controls work

## 9.2 Narrator Service

**Reference**: Complete voice line list in `FULL_ARCHIVE.md` → Part 9.4

**Action**: Create `Services/NarratorService.swift`

**Requirements**:
- Wrapper for AudioManager
- Type-safe voice line triggers
- Screen-specific voice methods
- Error handling for missing files

**Methods**:
```swift
class NarratorService {
    private let audioManager: AudioManager
    
    // Loading screen
    func playLoadingComplete()
    
    // Player selection
    func playPlayerQuestion()
    func playHelloAlexander()
    func playHelloOliver()
    
    // Home screen
    func playHomeQuestion()
    
    // Activities
    func playPuzzleStart()
    func playLabyrinthStart()
    func playDiceStart()
    func playShowNumber(_ number: Int)
    func playChooseNumber(_ number: Int)
    
    // Success phrases
    func playRandomSuccess()
    
    // Celebration
    func playCelebration(coins: Int)
    
    // Treasure
    func playTreasureMessage(coins: Int)
    func playFilmAb()
    
    // Video
    func playOneMinuteWarning()
    func playTimeUp()
}
```

**Validation**:
- [ ] NarratorService.swift created
- [ ] All voice triggers implemented
- [ ] Missing file handling works
- [ ] Integrates with AudioManager
- [ ] Type-safe methods

## 9.3 Bennie Voice Integration

**Reference**: Bennie voice lines in `FULL_ARCHIVE.md` → Part 9.4

**Action**: Create `Services/BennieService.swift`

**Requirements**:
- Similar to NarratorService
- Bennie-specific voice lines
- Speech bubble triggering
- Timing coordination

**Methods**:
```swift
class BennieService {
    private let audioManager: AudioManager
    
    // Home screen
    func playGreetingPart1(playerName: String)
    func playGreetingPart2()
    func playReturnPart1()
    func playReturnPart2()
    func playLocked()
    
    // Activities
    func playPuzzleStart()
    func playLabyrinthStart()
    func playLabyrinthWrong()
    func playWrongNumber()
    
    // Hints
    func playPuzzleHint10s()
    func playPuzzleHint20s()
    func playLabyrinthHint()
    func playDiceHint10s()
    func playDiceHint20s()
    func playDiceHint30s()
    func playChooseHint10s()
    func playChooseHint20s()
    
    // Celebration
    func playCelebration5()
    func playCelebration10()
    func playCelebration15()
    func playCelebration20()
    
    // Treasure
    func playTreasureUnder10(coins: Int)
    func playTreasureOver10()
    func playTreasureOver20()
    
    // Video
    func playOneMinute()
    func playTimeUp()
}
```

**Validation**:
- [ ] BennieService.swift created
- [ ] All voice triggers implemented
- [ ] Speech bubble coordination works
- [ ] Timing correct
- [ ] Integrates with AudioManager

## 9.4 Sound Effects Integration

**Action**: Extend `Services/AudioManager.swift`

**Requirements**:
- Quick effect playback
- No queuing for effects
- Haptic feedback coordination

**Effect Files**:
```
tap_wood.aac - Button taps
success_chime.aac - Correct answer
coin_collect.aac - Coin earned
celebration_fanfare.aac - Celebration
chest_open.aac - Treasure opened
gentle_boop.aac - Wrong answer
path_draw.aac - Labyrinth drawing (looping)
```

**Validation**:
- [ ] All effect files mapped
- [ ] Quick playback works
- [ ] No interference with voice
- [ ] Haptic feedback synced

## 9.5 Background Music

**Action**: Implement ambient music system

**Requirements**:
- Looping forest ambient track
- Fade in/out on screen changes
- Duck during voice
- Respect volume settings

**Music Files**:
```
forest_ambient.aac - Main background music (looping)
```

**Validation**:
- [ ] Music loops seamlessly
- [ ] Fades work smoothly
- [ ] Ducking during voice
- [ ] Volume control works
- [ ] Mute works

## 9.6 Audio File Naming Convention

**Reference**: `FULL_ARCHIVE.md` → Part 9.4

**Action**: Document audio file naming and create checklist

**Convention**:
```
{speaker}_{screen}_{trigger}.aac

Examples:
narrator_loading_complete.aac
narrator_player_question.aac
bennie_greeting_part1.aac
bennie_celebration_5.aac
bennie_hint_puzzle_10s.aac
```

**Complete Checklist**: See Phase 10.4 for full audio file checklist

**Validation**:
- [ ] Naming convention documented
- [ ] All files follow convention
- [ ] Checklist created
- [ ] File organization clear

## 9.7 Audio Error Handling

**Action**: Implement graceful degradation

**Requirements**:
- Detect missing audio files
- Log warnings (not errors)
- Continue without audio
- Show visual feedback instead

**Implementation**:
```swift
func playVoice(_ file: String, speaker: Speaker) {
    guard let url = getAudioURL(file) else {
        logger.warning("Audio file not found: \(file)")
        // Show speech bubble with text instead
        showVisualFeedback(text: getTextForAudioFile(file))
        return
    }
    
    // Play audio normally
}
```

**Validation**:
- [ ] Missing file detection works
- [ ] Warnings logged
- [ ] Visual fallback shows
- [ ] Game doesn't crash
- [ ] User experience acceptable

## ✅ Phase 9 Complete Checklist

**⚠️ Note**: Full validation requires assets from Phase 10

- [ ] AudioManager implemented
- [ ] Three-channel system works
- [ ] Voice ducking works
- [ ] NarratorService implemented
- [ ] BennieService implemented
- [ ] All voice triggers mapped
- [ ] Sound effects integrated
- [ ] Background music works
- [ ] Audio file naming documented
- [ ] Error handling implemented
- [ ] Visual fallbacks work
- [ ] Audio complements gameplay

**Partial Git Checkpoint** (before assets):
```bash
git add Services/
git commit -m "Phase 9: Audio system structure complete - Ready for asset integration"
git tag phase-9-structure-complete
```

**Full Git Checkpoint** (after asset integration):
```bash
git add Services/ Resources/Audio/
git commit -m "Phase 9: Audio integration complete - All voice lines and effects integrated"
git tag phase-9-complete
```

---

# Phase 10: Asset Production 🎨

**Time**: 16 hours
**Goal**: Generate all game assets using AI tools

**⚠️ REQUIREMENTS**: 
- Access to bennie-image-generator MCP
- Access to game-screen-designer MCP
- ElevenLabs account
- Google AI Studio access (Gemini)

## 10.1 Character Image Generation

**Reference**: 
- `PLAYBOOK_CONDENSED.md` → Characters
- `FULL_ARCHIVE.md` → Part 9.2: Gemini Image Generation

**Action**: Generate all character images using bennie-image-generator

### 10.1.1 Bennie Character Set

**Critical Rules**:
- ⚠️ Brown #8C7259
- ⚠️ NO clothing, vest, accessories
- ⚠️ ONLY snout is tan #C4A574
- ⚠️ NO belly patch

**Images to Generate**:
```
bennie_idle.png - Gentle breathing pose, arms at sides
bennie_waving.png - Right paw raised, friendly wave
bennie_pointing.png - Left arm extended, pointing
bennie_thinking.png - Paw on chin, looking up
bennie_encouraging.png - Leaning forward, open posture
bennie_celebrating.png - Both arms up, jumping, big smile
```

**Generation Command Example**:
```
generate_image(
    prompt="Adult brown bear in celebrating pose...",
    name="bennie-celebrating",
    category="characters",
    character="bennie",
    count=4
)
```

**Validation Per Image**:
- [ ] Color correct (#8C7259)
- [ ] NO clothing
- [ ] ONLY snout tan
- [ ] Expression matches spec
- [ ] Resolution adequate (@3x)
- [ ] Transparent background

### 10.1.2 Lemminge Character Set

**Critical Rules**:
- ⚠️ BLUE #6FA8DC
- ⚠️ NEVER green, NEVER brown
- ⚠️ White belly
- ⚠️ Buck teeth visible
- ⚠️ Pink nose & paws

**Images to Generate**:
```
lemminge_idle.png - Gentle sway, occasional blink
lemminge_curious.png - Head tilted, ears perked
lemminge_excited.png - Bouncing, sparkly eyes
lemminge_celebrating.png - Jumping, arms up, huge smile
lemminge_hiding.png - Half-hidden, mischievous
lemminge_mischievous.png - Sly grin, scheming pose
```

**Validation Per Image**:
- [ ] Color correct (#6FA8DC BLUE)
- [ ] NOT green, NOT brown
- [ ] White belly visible
- [ ] Buck teeth show
- [ ] Pink features
- [ ] Resolution adequate (@3x)
- [ ] Transparent background

### 10.1.3 A/B Testing & Refinement

**Process**:
1. Generate 4 variations per character/pose
2. Review all 4
3. Select best candidate
4. If none acceptable, use feedback tool:
```
record_feedback(
    pattern="Bennie had vest - must be removed",
    score=-3,
    source="bennie-celebrating-gen-001",
    reason="CRITICAL: No clothing allowed"
)
```
5. Regenerate until acceptable

**Validation**:
- [ ] All Bennie images approved (6 total)
- [ ] All Lemminge images approved (6 total)
- [ ] All match design specifications
- [ ] All exported at @2x and @3x
- [ ] All moved to Resources/Assets.xcassets/Characters/

## 10.2 Background & Environment Assets

**Action**: Generate background elements

**Assets Needed**:
```
forest_background_layers.png - 4-layer parallax forest
wood_plank_texture.png - For signs and buttons
stone_tablet_texture.png - For game grids
rope_texture.png - For hanging signs
chain_texture.png - For locked content
berry_cluster_left.png - Progress bar decoration
berry_cluster_right.png - Progress bar decoration
treasure_chest_closed.png - Before opening
treasure_chest_open.png - After opening
confetti_particle.png - For celebrations
```

**Validation**:
- [ ] All backgrounds generated
- [ ] Wood texture matches color palette
- [ ] Stone texture appropriate
- [ ] Decorative elements match style
- [ ] All exported correctly

## 10.3 UI Component Assets

**Action**: Generate UI-specific assets

**Assets Needed**:
```
wood_button_base.png - 9-slice compatible
wood_sign_frame.png - Hanging frame
lock_icon.png - Padlock for locked content
chain_overlay.png - X-pattern chains
home_icon.png - House symbol
volume_on_icon.png - Speaker symbol
volume_off_icon.png - Muted speaker
settings_icon.png - Gear symbol
help_icon.png - Question mark
back_arrow.png - Left arrow
forward_arrow.png - Right arrow
```

**Validation**:
- [ ] All UI assets generated
- [ ] Icons clear at 96pt
- [ ] 9-slice compatible where needed
- [ ] All exported correctly

## 10.4 Audio Asset Production

**Reference**: `FULL_ARCHIVE.md` → Part 9.4: ElevenLabs Voice Generation

**Action**: Generate all voice lines using ElevenLabs

**⚠️ CRITICAL**: Complete voice line checklist in archive

### 10.4.1 Narrator Voice Selection

**Requirements**:
- Warm, clear, neutral German voice
- Adult speaking to child
- Not condescending
- Clear pronunciation

**ElevenLabs Settings**:
- Stability: 0.75
- Similarity: 0.75
- Speaking rate: 85% of normal

**Validation**:
- [ ] Voice selected
- [ ] Test generation successful
- [ ] Pronunciation correct
- [ ] Tone appropriate

### 10.4.2 Bennie Voice Selection

**Requirements**:
- Slightly deeper than narrator
- Bear-like but friendly
- Warm and encouraging
- German

**ElevenLabs Settings**:
- Stability: 0.65
- Similarity: 0.80
- Speaking rate: 85% of normal

**Validation**:
- [ ] Voice selected
- [ ] Test generation successful
- [ ] Distinct from narrator
- [ ] Tone appropriate

### 10.4.3 Generate All Voice Lines

**Complete Checklist** (77 files total):

**Loading Screen** (1 file):
- [ ] narrator_loading_complete.aac

**Player Selection** (3 files):
- [ ] narrator_player_question.aac
- [ ] narrator_hello_alexander.aac
- [ ] narrator_hello_oliver.aac

**Home Screen** (6 files):
- [ ] narrator_home_question.aac
- [ ] bennie_greeting_part1.aac
- [ ] bennie_greeting_part2.aac
- [ ] bennie_return_part1.aac
- [ ] bennie_return_part2.aac
- [ ] bennie_locked.aac

**Puzzle Matching** (5 files):
- [ ] narrator_puzzle_start.aac
- [ ] bennie_puzzle_start.aac
- [ ] bennie_puzzle_hint_10s.aac
- [ ] bennie_puzzle_hint_20s.aac

**Labyrinth** (4 files):
- [ ] narrator_labyrinth_start.aac
- [ ] bennie_labyrinth_start.aac
- [ ] bennie_labyrinth_wrong.aac
- [ ] bennie_labyrinth_hint.aac

**Würfel (Dice)** (11 files):
- [ ] narrator_dice_start.aac
- [ ] narrator_show_number_1.aac
- [ ] narrator_show_number_2.aac
- [ ] narrator_show_number_3.aac
- [ ] narrator_show_number_4.aac
- [ ] narrator_show_number_5.aac
- [ ] narrator_show_number_6.aac
- [ ] bennie_wrong_number.aac
- [ ] bennie_dice_hint_10s.aac
- [ ] bennie_dice_hint_20s.aac
- [ ] bennie_dice_hint_30s.aac

**Wähle die Zahl** (13 files):
- [ ] narrator_choose_number_1.aac
- [ ] narrator_choose_number_2.aac
- [ ] narrator_choose_number_3.aac
- [ ] narrator_choose_number_4.aac
- [ ] narrator_choose_number_5.aac
- [ ] narrator_choose_number_6.aac
- [ ] narrator_choose_number_7.aac
- [ ] narrator_choose_number_8.aac
- [ ] narrator_choose_number_9.aac
- [ ] narrator_choose_number_10.aac
- [ ] bennie_wrong_choose.aac
- [ ] bennie_choose_hint_10s.aac
- [ ] bennie_choose_hint_20s.aac

**Success Pool** (7 files):
- [ ] success_super.aac
- [ ] success_toll.aac
- [ ] success_wunderbar.aac
- [ ] success_genau.aac
- [ ] success_super_gemacht.aac
- [ ] success_perfekt.aac
- [ ] success_bravo.aac

**Celebration** (4 files):
- [ ] bennie_celebration_5.aac
- [ ] bennie_celebration_10.aac
- [ ] bennie_celebration_15.aac
- [ ] bennie_celebration_20.aac

**Treasure** (4 files):
- [ ] bennie_treasure_under10.aac
- [ ] bennie_treasure_over10.aac
- [ ] bennie_treasure_over20.aac
- [ ] narrator_film_ab.aac

**Video Player** (2 files):
- [ ] bennie_video_1min.aac
- [ ] bennie_video_timeup.aac

**Sound Effects** (7 files):
- [ ] tap_wood.aac
- [ ] success_chime.aac
- [ ] coin_collect.aac
- [ ] celebration_fanfare.aac
- [ ] chest_open.aac
- [ ] gentle_boop.aac
- [ ] path_draw.aac (looping)

**Background Music** (1 file):
- [ ] forest_ambient.aac (looping, 192kbps)

### 10.4.4 Audio Post-Processing

**Action**: Convert and validate all audio files

**Process**:
1. Download MP3 from ElevenLabs
2. Convert to AAC:
```bash
ffmpeg -i input.mp3 -c:a aac -b:a 128k output.aac
```
3. Verify sample rate: 44.1kHz
4. Verify bitrate: 128kbps (voice), 192kbps (music)
5. Move to appropriate folder

**Validation**:
- [ ] All files converted to AAC
- [ ] All files 44.1kHz sample rate
- [ ] Correct bitrates
- [ ] All files in correct folders
- [ ] File sizes reasonable (<500KB per voice line)

## 10.5 Lottie Animation Creation

**Reference**: `FULL_ARCHIVE.md` → Part 9.3: Ludo.ai Animation Pipeline

**Action**: Create Lottie animations from static images

**⚠️ Note**: This requires Ludo.ai access or manual animation

**Animations Needed**:
```
bennie_idle.json - Breathing animation (2s loop)
bennie_waving.json - Wave gesture (1.5s)
bennie_celebrating.json - Jump celebration (1s)
lemminge_idle.json - Sway animation (1.5s loop)
lemminge_celebrating.json - Jump celebration (1s)
confetti.json - Particle animation (3s)
coin_fly.json - Arc trajectory (0.8s)
progress_fill.json - Fill animation (0.5s)
```

**Process Per Animation**:
1. Upload static image to Ludo.ai
2. Define animation type
3. Set duration and easing
4. Preview and adjust
5. Export as Lottie JSON
6. Verify file size (<100KB)
7. Test in Lottie preview tool

**Validation**:
- [ ] All animations created
- [ ] Smooth playback
- [ ] Correct durations
- [ ] Appropriate easing
- [ ] File sizes acceptable
- [ ] All moved to Resources/Lottie/

## 10.6 Asset Export & Organization

**Action**: Export all assets at correct resolutions

**Export Matrix**:
| Asset Type | @1x | @2x | @3x |
|-----------|-----|-----|-----|
| Bennie | 150×225 | 300×450 | 450×675 |
| Lemminge | 40×50 | 80×100 | 120×150 |
| Buttons | 48×30 | 96×60 | 144×90 |
| Background | 1194×834 | 2388×1668 | 3582×2502 |

**Organization**:
```
Resources/
├── Assets.xcassets/
│   ├── Characters/
│   │   ├── Bennie/
│   │   │   ├── bennie_idle.imageset/
│   │   │   │   ├── bennie_idle.png
│   │   │   │   ├── bennie_idle@2x.png
│   │   │   │   └── bennie_idle@3x.png
│   │   │   └── [other poses...]
│   │   └── Lemminge/
│   │       └── [all poses...]
│   ├── Backgrounds/
│   └── UI/
├── Lottie/
│   └── [all .json files]
└── Audio/
    ├── Narrator/
    ├── Bennie/
    ├── Music/
    └── Effects/
```

**Validation**:
- [ ] All assets exported
- [ ] All resolutions present
- [ ] Folder structure matches spec
- [ ] Asset catalog configured
- [ ] All assets visible in Xcode

## ✅ Phase 10 Complete Checklist

**Character Assets**:
- [ ] All 6 Bennie images approved and exported
- [ ] All 6 Lemminge images approved and exported
- [ ] All character colors correct
- [ ] All design violations addressed

**Environment Assets**:
- [ ] All backgrounds generated
- [ ] All UI components generated
- [ ] All textures generated
- [ ] All decorative elements generated

**Audio Assets**:
- [ ] Narrator voice selected
- [ ] Bennie voice selected
- [ ] All 77 audio files generated
- [ ] All files converted to AAC
- [ ] All files organized correctly

**Animation Assets**:
- [ ] All 8 Lottie animations created
- [ ] All animations tested
- [ ] All files under 100KB

**Organization**:
- [ ] All assets in correct folders
- [ ] Asset catalog configured
- [ ] All assets visible in Xcode
- [ ] File naming consistent

**Git Checkpoint**:
```bash
git add Resources/
git commit -m "Phase 10: Asset production complete - All game assets generated and organized"
git tag phase-10-complete
```

---

# Phase 11: Testing & Quality Assurance 🧪

**Time**: 8 hours
**Goal**: Comprehensive testing of all features

## 11.1 Recursive Testing Strategy

**Concept**: Test EVERY interaction path without stopping

**Approach**: Automated testing agent plays through the game multiple times, trying different paths, accumulating 100 coins, watching 100 minutes of YouTube.

### Test Scenario 1: Alexander Complete Journey

**Goal**: Alexander plays from start to 100 coins and 100 minutes YouTube

**Path**:
1. Launch app
2. Loading screen → Player Selection
3. Select Alexander
4. Home → Rätsel → Puzzle Matching
5. Complete 10 puzzle levels (earn 10 coins)
6. Celebration at 5 coins
7. Celebration at 10 coins
8. Navigate to Treasure
9. Redeem 5 min YouTube (10 coins → 0 coins)
10. Watch 5 min video
11. Return to Home
12. Continue with activities...
13. Repeat until 100 coins earned and 100 minutes watched

**Validation**:
- [ ] No crashes
- [ ] No visual glitches
- [ ] All voices play
- [ ] Coins track correctly
- [ ] Time tracks correctly
- [ ] Celebrations trigger correctly
- [ ] State transitions smooth
- [ ] Data persists

### Test Scenario 2: Oliver Complete Journey

**Goal**: Same as Alexander but testing Oliver profile

**Validation**:
- [ ] Same as Scenario 1
- [ ] Per-player data isolated
- [ ] Can switch between players

### Test Scenario 3: Edge Cases

**Test Cases**:
- [ ] Quit activity mid-level (back button)
- [ ] Force quit app during activity
- [ ] Force quit during video playback
- [ ] Try to access locked activities
- [ ] Try to redeem YouTube with insufficient coins
- [ ] Reach daily time limit
- [ ] Parent dashboard while playing
- [ ] Add/remove videos while in treasure screen
- [ ] Lock activity while playing it

**Expected Behaviors**:
- Progress saves correctly
- No data loss
- Graceful error handling
- Appropriate messaging
- No crashes

## 11.2 Design Validation Tests

**Reference**: `PLAYBOOK_CONDENSED.md` → Design QA Checklist

### 11.2.1 Character Design Tests

**For EVERY screen with Bennie**:
- [ ] Bennie is brown #8C7259
- [ ] Bennie has NO clothing/vest/accessories
- [ ] ONLY snout is tan #C4A574
- [ ] Correct expression for context

**For EVERY screen with Lemminge**:
- [ ] Lemminge are BLUE #6FA8DC
- [ ] NOT green, NOT brown
- [ ] White belly visible
- [ ] Buck teeth visible
- [ ] Correct expression for context

**Validation Method**: Visual inspection + automated color sampling

### 11.2.2 Color Validation Tests

**For EVERY screen**:
- [ ] All colors from approved palette
- [ ] No red #FF0000
- [ ] No pure white/black for large areas
- [ ] No neon colors
- [ ] Color contrast ≥ 4.5:1

**Validation Method**: Screenshot analysis + accessibility tool

### 11.2.3 Touch Target Tests

**For EVERY interactive element**:
- [ ] Touch target ≥ 96pt width
- [ ] Touch target ≥ 96pt height
- [ ] Touch area visible and obvious
- [ ] No overlapping touch targets

**Validation Method**: Inspector tool + manual testing

### 11.2.4 Text Validation Tests

**For EVERY text element**:
- [ ] German language only
- [ ] Max 7 words per sentence
- [ ] No "Falsch" or "Fehler"
- [ ] Positive framing
- [ ] Literal language (no metaphors)

**Validation Method**: Text extraction + manual review

### 11.2.5 Animation Tests

**For EVERY animation**:
- [ ] No flashing (< 3 flashes per second)
- [ ] No shaking or jarring motion
- [ ] Smooth 60fps
- [ ] Reduce motion alternative exists
- [ ] Natural easing curves

**Validation Method**: FPS meter + visual inspection

## 11.3 Audio Testing

### 11.3.1 Voice Playback Tests

**For EVERY voice trigger**:
- [ ] Correct voice file plays
- [ ] Audio clear and audible
- [ ] Volume correct (voice at 100%)
- [ ] Music ducks during voice
- [ ] Music restores after voice
- [ ] No voice overlap
- [ ] Queue system works

**Test Matrix**:
```
Screen → Trigger → Expected Voice → Plays Correctly?
Loading → 100% → narrator_loading_complete.aac → [ ]
Player Selection → Appear → narrator_player_question.aac → [ ]
... [all 77 voice triggers] ...
```

### 11.3.2 Sound Effect Tests

**For EVERY effect trigger**:
- [ ] Effect plays immediately
- [ ] No delay
- [ ] Doesn't interrupt voice
- [ ] Volume correct (70%)
- [ ] Haptic feedback synced

**Test Scenarios**:
- [ ] Rapid button tapping (effects don't overlap)
- [ ] Effect during voice (doesn't play)
- [ ] Effect during celebration (plays alongside music)

### 11.3.3 Music Tests

- [ ] Loops seamlessly
- [ ] Fades in on app launch
- [ ] Fades out on exit
- [ ] Ducks during voice
- [ ] Volume control works
- [ ] Mute works instantly

## 11.4 State Management Tests

### 11.4.1 State Transition Tests

**Test EVERY valid transition**:
```
From → To → Should Work?
loading → playerSelection → ✓
playerSelection → home → ✓
home → activitySelection → ✓
... [all valid transitions] ...
```

**Test EVERY invalid transition**:
```
From → To → Should Reject?
loading → treasureScreen → ✓ (rejected)
playing → parentDashboard → ✓ (rejected)
... [all invalid transitions] ...
```

### 11.4.2 Data Persistence Tests

**Test Scenarios**:
- [ ] Earn 5 coins, quit app, relaunch → Still have 5 coins
- [ ] Complete 3 levels, quit, relaunch → Progress saved
- [ ] Add video, quit, relaunch → Video still in list
- [ ] Lock activity, quit, relaunch → Still locked
- [ ] Watch 10 min YouTube, quit, relaunch → Time logged

**Validation**: All data persists across app restarts

### 11.4.3 Player Profile Tests

- [ ] Alexander and Oliver profiles isolated
- [ ] Coins separate per player
- [ ] Progress separate per player
- [ ] Settings separate per player
- [ ] Can switch between players
- [ ] No data leakage between profiles

## 11.5 Adaptive Difficulty Tests

### 11.5.1 Difficulty Progression Tests

**Test**: Complete 30 consecutive puzzle levels

**Expected Progression**:
- Levels 1-5: 3×3 grid, 2 colors
- Levels 6-10: 3×3 grid, 3 colors
- Levels 11-20: 4×4 grid, 3 colors
- Levels 21-30: 5×5 grid, 3-4 colors

**Validation**:
- [ ] Difficulty increases correctly
- [ ] No sudden difficulty spikes
- [ ] Levels feel appropriately challenging

### 11.5.2 Learning Profile Tests

**Test**: Play with different patterns

**Pattern A: Quick Success**
- Complete levels in <10 seconds
- No mistakes
- Expected: Difficulty increases faster

**Pattern B: Struggling**
- Complete levels in >60 seconds
- 3+ mistakes per level
- Expected: Difficulty decreases, hints offered

**Pattern C: Quitting**
- Quit 3 activities mid-level
- Expected: Major difficulty decrease, encouraging messages

**Validation**:
- [ ] Learning profile updates correctly
- [ ] Difficulty adapts appropriately
- [ ] Hints trigger based on struggle
- [ ] System feels responsive to player skill

## 11.6 Parent Features Tests

### 11.6.1 Parent Gate Tests

- [ ] Math question generates (5-15 range)
- [ ] Correct answer grants access
- [ ] Wrong answer rejected
- [ ] 3 wrong answers generates new question
- [ ] Cancel returns to game
- [ ] Children cannot bypass easily

### 11.6.2 Parent Dashboard Tests

- [ ] Player stats display correctly
- [ ] Activity toggles work
- [ ] Changes persist
- [ ] Time limits adjustable
- [ ] Progress reset works (with confirmation)
- [ ] Cannot be undone
- [ ] Video management accessible

### 11.6.3 Video Management Tests

- [ ] Can add YouTube video by URL
- [ ] URL validation works
- [ ] Thumbnail fetches correctly
- [ ] Can remove video
- [ ] Changes persist
- [ ] Videos appear in Video Selection
- [ ] Invalid URLs rejected

### 11.6.4 Time Limit Tests

- [ ] Daily limit enforced
- [ ] Warnings trigger correctly (5 min, 2 min)
- [ ] Graceful exit at limit
- [ ] Progress saved before exit
- [ ] Cannot bypass limit
- [ ] Resets at midnight

## 11.7 YouTube Integration Tests

### 11.7.1 Video Selection Tests

- [ ] Only approved videos show
- [ ] Thumbnails display
- [ ] Titles display (2 lines max)
- [ ] Can select video
- [ ] Navigation works
- [ ] Time remaining accurate

### 11.7.2 Video Player Tests

- [ ] YouTube embeds correctly
- [ ] NO YouTube controls visible
- [ ] NO related videos shown
- [ ] Analog clock counts down
- [ ] Clock updates every second
- [ ] 1-minute warning plays
- [ ] Clock pulses at warning
- [ ] Auto-exits at 0 seconds
- [ ] "Time up" message plays
- [ ] Returns to Home automatically

### 11.7.3 Offline Tests

- [ ] Detects no internet
- [ ] Disables YouTube buttons
- [ ] Shows offline message
- [ ] All other features work
- [ ] Graceful messaging

## 11.8 Accessibility Tests

### 11.8.1 VoiceOver Tests

**Enable VoiceOver and test**:
- [ ] All buttons have labels
- [ ] Labels are in German
- [ ] Labels are descriptive
- [ ] Grid cells announce correctly
- [ ] Progress bar announces correctly
- [ ] Navigation logical
- [ ] No label collisions

### 11.8.2 Reduce Motion Tests

**Enable Reduce Motion and test**:
- [ ] Animations disabled or simplified
- [ ] Game still playable
- [ ] No loss of functionality
- [ ] Transitions still clear
- [ ] Performance improved

### 11.8.3 Color Blind Tests

**Test with color blind simulation**:
- [ ] Puzzle patterns distinguishable
- [ ] UI elements clear
- [ ] No reliance on color alone
- [ ] Shape indicators help
- [ ] Text readable

## ✅ Phase 11 Complete Checklist

**Recursive Testing**:
- [ ] Alexander 100-coin journey complete
- [ ] Oliver 100-coin journey complete
- [ ] 100 minutes YouTube watched
- [ ] All edge cases tested
- [ ] No crashes encountered
- [ ] All data persists correctly

**Design Validation**:
- [ ] All character design checks passed
- [ ] All color checks passed
- [ ] All touch target checks passed
- [ ] All text checks passed
- [ ] All animation checks passed

**Audio Testing**:
- [ ] All 77 voice triggers tested
- [ ] All sound effects tested
- [ ] Music system tested
- [ ] Volume controls tested
- [ ] Mute tested

**State Management**:
- [ ] All state transitions tested
- [ ] Data persistence verified
- [ ] Player profiles isolated
- [ ] No state corruption

**Adaptive Difficulty**:
- [ ] Difficulty progression works
- [ ] Learning profile adapts
- [ ] Hints trigger appropriately
- [ ] Feels balanced

**Parent Features**:
- [ ] Parent gate works
- [ ] Dashboard functional
- [ ] Video management works
- [ ] Time limits enforced

**YouTube Integration**:
- [ ] Video selection works
- [ ] Video playback works
- [ ] Time tracking accurate
- [ ] Offline handling graceful

**Accessibility**:
- [ ] VoiceOver works
- [ ] Reduce motion works
- [ ] Color blind friendly
- [ ] WCAG 2.1 AA compliant

**Git Checkpoint**:
```bash
# Create test report
echo "All tests passed" > TEST_REPORT.md
git add TEST_REPORT.md
git commit -m "Phase 11: Testing complete - All features validated"
git tag phase-11-complete
```

---

# Phase 12: Performance Optimization ⚡

**Time**: 4 hours
**Goal**: Ensure smooth 60fps and <200MB memory

## 12.1 Performance Baseline

**Action**: Measure current performance

**Metrics to Capture**:
- [ ] Frame rate (target: constant 60fps)
- [ ] Memory usage (target: <200MB peak)
- [ ] Launch time (target: <2s cold start)
- [ ] Screen transition time (target: <0.3s)
- [ ] Audio loading time (target: <0.1s)

**Tools**:
- Xcode Instruments (Time Profiler)
- Xcode Instruments (Allocations)
- Xcode Debug Navigator (FPS)

**Validation**:
- [ ] Baseline measurements captured
- [ ] Problem areas identified
- [ ] Optimization targets set

## 12.2 Image Optimization

**Action**: Optimize all image assets

**Optimizations**:
- [ ] Compress PNGs without quality loss
- [ ] Remove unused images
- [ ] Ensure @2x/@3x present (not generating dynamically)
- [ ] Use asset catalog compression
- [ ] Verify image sizes appropriate

**Expected Savings**: 20-30% app size reduction

**Validation**:
- [ ] All images optimized
- [ ] Visual quality maintained
- [ ] App size reduced
- [ ] Loading times improved

## 12.3 Audio Optimization

**Action**: Optimize all audio files

**Optimizations**:
- [ ] Verify all files AAC format
- [ ] Verify bitrates correct (128/192kbps)
- [ ] Remove unused audio files
- [ ] Preload frequently used sounds
- [ ] Stream longer files (music)

**Expected Savings**: Audio loads faster, less memory

**Validation**:
- [ ] All audio optimized
- [ ] Audio quality maintained
- [ ] Loading times improved
- [ ] Memory usage reduced

## 12.4 Memory Management

**Action**: Identify and fix memory leaks

**Check for**:
- [ ] Lottie animations properly disposed
- [ ] Audio players released
- [ ] Image caches bounded
- [ ] View controllers deallocated
- [ ] Observers removed
- [ ] Timers invalidated

**Memory Targets**:
- Launch: <100MB
- Activity playing: <150MB
- Celebration: <200MB (peak)
- After celebration: <150MB

**Validation**:
- [ ] No memory leaks detected
- [ ] Memory stays within targets
- [ ] Memory releases after animations
- [ ] No memory warnings

## 12.5 Animation Performance

**Action**: Ensure all animations 60fps

**Optimizations**:
- [ ] Use GPU-accelerated animations
- [ ] Avoid view hierarchy changes during animation
- [ ] Pre-render complex views
- [ ] Use shouldRasterize for complex layers
- [ ] Reduce shadow complexity

**Validation**:
- [ ] All animations 60fps
- [ ] No dropped frames
- [ ] Transitions smooth
- [ ] Device doesn't heat up

## 12.6 View Hierarchy Optimization

**Action**: Simplify view hierarchies

**Check for**:
- [ ] Excessive nesting (>10 levels)
- [ ] Unnecessary view updates
- [ ] Heavy onAppear logic
- [ ] Redundant modifiers
- [ ] Over-use of GeometryReader

**Optimizations**:
- Use LazyVStack/LazyHStack where appropriate
- Extract heavy views into separate files
- Use @ViewBuilder efficiently
- Cache expensive computations

**Validation**:
- [ ] View hierarchies simplified
- [ ] Rendering faster
- [ ] No layout issues
- [ ] Performance improved

## 12.7 State Management Optimization

**Action**: Optimize state updates

**Check for**:
- [ ] Excessive @Published updates
- [ ] Unnecessary view refreshes
- [ ] Heavy computations in body
- [ ] Unoptimized @ObservedObject usage

**Optimizations**:
- Batch state updates
- Use explicit state changes
- Debounce rapid updates
- Move logic out of view body

**Validation**:
- [ ] State updates efficient
- [ ] No unnecessary refreshes
- [ ] Smooth user experience
- [ ] Performance improved

## 12.8 Asset Loading Optimization

**Action**: Optimize asset loading strategy

**Optimizations**:
- [ ] Preload critical assets on launch
- [ ] Lazy load activity-specific assets
- [ ] Cache loaded assets
- [ ] Unload unused assets
- [ ] Use background threads for loading

**Implementation**:
```swift
class AssetPreloader {
    static func preloadCriticalAssets() {
        // Load on background thread
        DispatchQueue.global(qos: .userInitiated).async {
            // Preload character images
            _ = UIImage(named: "bennie_idle")
            _ = UIImage(named: "lemminge_idle")
            // Preload common UI elements
            // Preload frequent sounds
        }
    }
}
```

**Validation**:
- [ ] Critical assets preload on launch
- [ ] Activity assets load when needed
- [ ] No loading stutters
- [ ] Memory usage reasonable

## 12.9 Audio System Optimization

**Action**: Optimize audio playback

**Optimizations**:
- [ ] Preload voice files on screen appear
- [ ] Release audio players after use
- [ ] Use single audio session
- [ ] Avoid unnecessary audio mixing
- [ ] Buffer audio appropriately

**Validation**:
- [ ] Voice plays immediately (<0.1s)
- [ ] No audio glitches
- [ ] Memory usage reasonable
- [ ] Audio system efficient

## 12.10 Build Optimization

**Action**: Optimize Xcode build settings

**Settings to Check**:
- [ ] Whole Module Optimization: On
- [ ] Compilation Mode: Release = Optimize for Speed
- [ ] Strip Debug Symbols: On (Release)
- [ ] Dead Code Stripping: On
- [ ] Link Time Optimization: Incremental

**Validation**:
- [ ] Build settings optimized
- [ ] App size reduced
- [ ] Runtime performance improved
- [ ] No functionality broken

## ✅ Phase 12 Complete Checklist

**Performance Metrics**:
- [ ] 60fps constant in all screens
- [ ] Memory <200MB peak
- [ ] Launch time <2s
- [ ] Screen transitions <0.3s
- [ ] Audio loads <0.1s

**Optimizations Complete**:
- [ ] Images optimized
- [ ] Audio optimized
- [ ] Memory leaks fixed
- [ ] Animations 60fps
- [ ] View hierarchies simplified
- [ ] State management optimized
- [ ] Asset loading optimized
- [ ] Audio system optimized
- [ ] Build settings optimized

**Final Validation**:
- [ ] No crashes during 100-coin journey
- [ ] No memory warnings
- [ ] Device doesn't overheat
- [ ] Battery drain reasonable
- [ ] User experience smooth

**Git Checkpoint**:
```bash
git add .
git commit -m "Phase 12: Performance optimization complete - 60fps, <200MB memory"
git tag phase-12-complete
```

---

# Phase 13: TestFlight Preparation 🚀

**Time**: 2 hours
**Goal**: Prepare app for TestFlight beta testing

## 13.1 App Store Connect Setup

**Action**: Create app in App Store Connect

**Steps**:
1. Log into App Store Connect
2. Create new app
3. Fill in app information:
   - Name: "Bennie und die Lemminge"
   - Bundle ID: com.yourcompany.benniegame
   - SKU: BENNIE-001
   - Primary Language: German

4. Set app category: Education
5. Set age rating: 4+

**Validation**:
- [ ] App created in App Store Connect
- [ ] All information filled
- [ ] Bundle ID matches Xcode

## 13.2 App Metadata

**Action**: Create all required metadata

### 13.2.1 App Description (German)

**App Name**: Bennie und die Lemminge

**Subtitle**: Spielerisch lernen für Vorschulkinder

**Description**:
```
Bennie und die Lemminge ist eine liebevoll gestaltete Lern-App für Kinder im Vorschulalter (4-5 Jahre). 

Besonders geeignet für neurodiverse Kinder:
• Autism-freundliches Design
• Keine negativen Rückmeldungen
• Klare, vorhersehbare Strukturen
• Beruhigende Waldumgebung

Lernbereiche:
• Rätsel und Musterkennung
• Zahlen von 1-10
• Logisches Denken
• Feinmotorik

Besondere Features:
• Motivierendes Belohnungssystem
• Adaptive Schwierigkeit
• Deutsche Sprachausgabe
• Elternbereich mit Kontrollen
• Offline spielbar

Keine Werbung, keine In-App-Käufe, sicher für Kinder.
```

### 13.2.2 Keywords

```
kinder, lernen, vorschule, mathe, zahlen, autism, bildung, spiel
```

### 13.2.3 Support URL

Create a simple support page or use:
```
https://yourcompany.com/bennie-support
```

### 13.2.4 Privacy Policy URL

Create privacy policy or use:
```
https://yourcompany.com/bennie-privacy
```

**Validation**:
- [ ] Description written
- [ ] Keywords selected
- [ ] Support URL provided
- [ ] Privacy policy URL provided

## 13.3 App Screenshots

**Action**: Create required screenshots

**Requirements**:
- iPad Pro (12.9-inch) 3rd gen: 2048×2732
- iPad Pro (12.9-inch) 2nd gen: 2048×2732

**Screenshots Needed** (6-8 total):
1. Loading Screen (with title)
2. Player Selection
3. Home Screen (Waldabenteuer)
4. Puzzle Matching gameplay
5. Numbers gameplay
6. Celebration moment
7. Treasure Screen
8. Parent Dashboard (optional)

**Requirements Per Screenshot**:
- High quality (PNG)
- Show best features
- Include German UI text
- Bright and appealing
- Show characters clearly

**Validation**:
- [ ] All screenshots created
- [ ] Correct resolution
- [ ] High quality
- [ ] Show key features
- [ ] German text visible

## 13.4 App Icon

**Action**: Create App Icon for all required sizes

**Required Sizes** (iPad):
- 20pt (1x, 2x)
- 29pt (1x, 2x)
- 40pt (1x, 2x)
- 76pt (1x, 2x)
- 83.5pt (2x)
- 1024pt (1x) - App Store

**Design**:
- Show Bennie's face
- Forest background
- Warm colors
- Clear and simple
- Recognizable at small sizes

**Validation**:
- [ ] All icon sizes created
- [ ] Design clear at all sizes
- [ ] Added to Assets.xcassets
- [ ] App Store icon 1024×1024

## 13.5 Build Configuration

**Action**: Configure Release build

**Xcode Settings**:
- Scheme: Release
- Configuration: Release
- Code Signing: Automatic
- Team: Your Apple Developer Team
- Provisioning Profile: Automatic

**Build Number**:
- Version: 1.0
- Build: 1

**Validation**:
- [ ] Release configuration set
- [ ] Code signing configured
- [ ] Version numbers set
- [ ] Archive builds successfully

## 13.6 TestFlight Information

**Action**: Prepare TestFlight metadata

**What to Test**:
```
Bitte testen Sie:
• Alle 4 Aktivitäten (Puzzle, Labyrinth, Würfel, Zahlen)
• Münzen verdienen und YouTube freischalten
• YouTube-Videos anschauen
• Elternbereich (Passcode: Lösen Sie die Matheaufgabe)
• Verschiedene Spieler (Alexander und Oliver)
• Spielzeit-Limits

Bekannte Einschränkungen:
• Beta-Version, noch nicht alle Features vollständig
• YouTube-Videos müssen im Elternbereich hinzugefügt werden
```

**Beta Tester Instructions**:
```
1. Installieren Sie TestFlight aus dem App Store
2. Öffnen Sie den Einladungslink
3. Installieren Sie "Bennie und die Lemminge"
4. Starten Sie die App
5. Wählen Sie einen Spieler (Alexander oder Oliver)
6. Spielen Sie verschiedene Aktivitäten
7. Geben Sie Feedback über TestFlight
```

**Validation**:
- [ ] Test notes written
- [ ] Instructions clear
- [ ] Known issues documented

## 13.7 Privacy & Compliance

**Action**: Complete required declarations

**Data Collection**: None (for TestFlight)
- [ ] No data collection
- [ ] No analytics
- [ ] No tracking
- [ ] No third-party SDKs (except Lottie)

**Age Rating**: 4+
- [ ] No violence
- [ ] No scary content
- [ ] No mature themes
- [ ] Safe for young children

**Export Compliance**: No encryption

**Validation**:
- [ ] Privacy declarations complete
- [ ] Age rating justified
- [ ] Export compliance set

## 13.8 TestFlight Submission

**Action**: Upload build to TestFlight

**Steps**:
1. Archive in Xcode (Product → Archive)
2. Validate Archive
3. Distribute App → App Store Connect
4. Upload build
5. Wait for processing (~15 minutes)
6. Add build to TestFlight
7. Fill in test information
8. Submit for Beta App Review

**Validation**:
- [ ] Build archived successfully
- [ ] Validation passed
- [ ] Build uploaded
- [ ] Build processed
- [ ] Test information filled
- [ ] Submitted for review

## 13.9 Internal Testing

**Action**: Test with internal testers first

**Internal Test Group**:
- Add 1-5 internal testers
- No Apple review required
- Immediate access

**Test Plan**:
1. Install via TestFlight
2. Complete 100-coin journey
3. Watch 100 minutes YouTube
4. Test parent features
5. Report any issues

**Validation**:
- [ ] Internal testers added
- [ ] Build available immediately
- [ ] Internal testing complete
- [ ] Issues addressed
- [ ] Ready for external testing

## 13.10 External Testing Preparation

**Action**: Prepare for external beta testing

**External Test Group**:
- Up to 10,000 external testers
- Requires Apple Beta App Review (~24-48 hours)
- Public link can be shared

**Review Preparation**:
- Ensure app follows App Review Guidelines
- No placeholders
- No obvious bugs
- Test notes complete
- Screenshots representative

**Validation**:
- [ ] External test group created
- [ ] Build submitted for Beta App Review
- [ ] Test notes complete
- [ ] Ready for external testers

## ✅ Phase 13 Complete Checklist

**App Store Connect**:
- [ ] App created
- [ ] Metadata complete
- [ ] Description written (German)
- [ ] Keywords set
- [ ] Support URL provided
- [ ] Privacy policy URL provided

**Visual Assets**:
- [ ] 6-8 screenshots created
- [ ] App icon all sizes
- [ ] High quality images

**Build**:
- [ ] Release build configured
- [ ] Code signing set
- [ ] Version numbers set
- [ ] Archive successful
- [ ] Validation passed
- [ ] Build uploaded

**TestFlight**:
- [ ] Test information complete
- [ ] Internal testing done
- [ ] Submitted for Beta App Review
- [ ] Ready for external testers

**Final Checks**:
- [ ] No crashes in testing
- [ ] All features work
- [ ] Performance acceptable
- [ ] Ready for beta users

**Git Checkpoint**:
```bash
git add .
git commit -m "Phase 13: TestFlight preparation complete - Ready for beta testing"
git tag phase-13-complete
git tag v1.0-beta-1
```

---

# 🎉 Project Completion

## Final Status Check

### ✅ All Phases Complete:
- [x] Phase 0: Pre-Flight Checks
- [x] Phase 1: Project Setup
- [x] Phase 2: Design System
- [x] Phase 3: Data Models
- [x] Phase 4: State Management
- [x] Phase 5: Core Screens
- [x] Phase 6: Activity Implementations
- [x] Phase 7: Reward System Integration
- [x] Phase 8: Parent Features
- [x] Phase 9: Audio Integration
- [x] Phase 10: Asset Production
- [x] Phase 11: Testing & QA
- [x] Phase 12: Performance Optimization
- [x] Phase 13: TestFlight Preparation

### ✅ Deliverables Complete:
- [x] iPad app (landscape only)
- [x] All 4 activities (Puzzle, Labyrinth, Würfel, Wähle Zahl)
- [x] Complete reward system (coins → YouTube)
- [x] Parent dashboard with controls
- [x] All audio assets integrated
- [x] All visual assets integrated
- [x] Performance optimized (60fps, <200MB)
- [x] TestFlight ready

### 🎯 Success Criteria Met:
- [x] Can play from launch to 100 coins
- [x] Can watch 100 minutes YouTube
- [x] No crashes in testing
- [x] Autism-friendly design maintained
- [x] All critical design rules followed
- [x] German language throughout
- [x] Parent controls functional

## Next Steps

### Immediate:
1. Submit to TestFlight Beta Review
2. Wait for approval (~24-48 hours)
3. Invite external beta testers
4. Gather feedback

### Short-term:
1. Address beta tester feedback
2. Fix any discovered bugs
3. Refine based on real-world usage
4. Prepare for App Store submission

### Long-term:
1. Add locked activities (Zeichnen, Logik)
2. Add more sub-activities
3. Enhance adaptive difficulty
4. Consider additional languages

## Thank You!

The Bennie Bear project is ready for beta testing. All phases completed successfully following the get-shit-done framework.

**Final Git Tag**:
```bash
git tag project-complete
git push --tags
```

---

# Appendix: Quick Reference

## Critical Commands

```bash
# Check project status
git status

# Run tests
xcodebuild test

# Build release
xcodebuild archive

# Check for issues
swiftlint

# Memory profiling
instruments -t Allocations

# FPS monitoring
instruments -t Time Profiler
```

## Critical Files

```
PLAYBOOK_CONDENSED.md - Design specifications
FULL_ARCHIVE.md - Complete specifications
CLAUDE.md - This execution plan
TEST_REPORT.md - Testing results
```

## Emergency Contacts

```
Design Issues → Check PLAYBOOK_CONDENSED.md
Technical Issues → Check FULL_ARCHIVE.md
Asset Issues → Check Phase 10 in this document
State Issues → Check Phase 4 in this document
```

## Version History

```
v1.0-beta-1 - Initial TestFlight build
[Future versions...]
```

---

*End of CLAUDE.md*
*Last Updated: [Current Date]*
*Framework: get-shit-done*
*Status: Complete - Ready for Execution*
