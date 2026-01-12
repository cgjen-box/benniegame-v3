# Phase 10 References - Complete Guide

> **Purpose**: Quick reference for all playbook sections, design assets, and specifications relevant to data persistence

---

## 📚 Playbook References

### Primary Sections

#### Part 5.4: Data Persistence
**File**: `docs/playbook/FULL_ARCHIVE.md` (Lines ~1480-1550)

**Key Information**:
- Local storage structure with SwiftData
- Save triggers table (when to persist data)
- Load points table (when to load data)
- PlayerData struct specification
- AppSettings struct specification
- ParentSettings struct specification

**Critical Rules**:
```swift
// From playbook - exact structure
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

#### Part 5.5: Offline Behavior
**File**: `docs/playbook/FULL_ARCHIVE.md` (Lines ~1550-1600)

**Offline Requirements Table**:
| Feature | Offline Support |
|---------|----------------|
| All activities | ✅ Fully offline |
| Narrator/Bennie audio | ✅ Bundled in app |
| Progress saving | ✅ Local storage |
| YouTube playback | ❌ Requires internet |
| Parent dashboard | ✅ Local settings |

**Implementation**:
```swift
// From playbook - Network monitoring
import Network

struct NetworkMonitor {
    static var isConnected: Bool { ... }
}

// In Treasure Screen
if !NetworkMonitor.isConnected {
    playBennie("wir_brauchen_internet.aac")
    youtubeButtonsEnabled = false
    showOfflineMessage = true
}
```

---

### Supporting Sections

#### Part 0.4: Coin Economy
**File**: `docs/playbook/FULL_ARCHIVE.md` (Lines ~200-250)

**Coin Rules**:
| Action | Coins |
|--------|-------|
| Complete activity | +1 |
| First-try bonus | +1 |
| Daily cap | 30 max |
| 5 min YouTube | -10 |
| 10 min YouTube | -20 |

**Validation Code**:
```swift
// Must match playbook
assert(coinsPerActivity == 1)
assert(tier1Cost == 10 && tier1Minutes == 5)
assert(tier2Cost == 20 && tier2Minutes == 10)
assert(tier2BonusMinutes == 2)
```

#### Part 0.3: Activities (Phase 1 - MVP)
**File**: `docs/playbook/FULL_ARCHIVE.md` (Lines ~150-200)

**Activity Types**:
```swift
// EXACTLY as defined in playbook
enum ActivityType: String, Codable {
    case raetselPuzzle = "raetsel_puzzle"
    case raetselLabyrinth = "raetsel_labyrinth"
    case zahlenWuerfel = "zahlen_wuerfel"
    case zahlenWaehle = "zahlen_waehle"
    // Future phases:
    // case zeichnenFrei
    // case logikSequenz
}
```

#### Part 9.6: Adaptive Difficulty System
**File**: `docs/playbook/FULL_ARCHIVE.md` (Lines ~1300-1400)

**LearningProfile Structure**:
```swift
struct LearningProfile: Codable {
    // Performance metrics
    var averageSolveTime: TimeInterval
    var mistakeFrequency: Double
    var quitRate: Double
    var sessionDuration: TimeInterval
    
    // Engagement indicators
    var hintUsageRate: Double
    var celebrationEngagement: Bool
    var preferredActivities: [ActivityType: Int]
    
    // Adaptive parameters
    var difficultyLevel: Float        // 0.0 (easiest) to 1.0 (hardest)
    var gridSizePreference: Int       // Preferred puzzle grid size
    var colorCount: Int               // Number of colors in puzzles
}
```

**Difficulty Adjustment Rules Table**:
| Signal | Interpretation | Adjustment |
|--------|---------------|------------|
| Solve time < 10s | Too easy | Increase difficulty |
| Solve time > 60s | Struggling | Decrease difficulty |
| 3+ mistakes per level | Too hard | Decrease difficulty, offer hints |
| Quit mid-activity | Frustration | Major decrease, encouraging message |

#### Part 4.11: Parent Dashboard
**File**: `docs/playbook/FULL_ARCHIVE.md` (Lines ~1100-1200)

**Parent Settings Structure**:
```swift
struct ParentSettings: Codable {
    var approvedVideos: [ApprovedVideo]
    var dailyPlayTimeLimit: [String: Int]  // ["alexander": 60, "oliver": 45]
    var activityLocks: [String: [ActivityType]]
}
```

**Video Management**:
```swift
struct ApprovedVideo: Codable, Identifiable {
    let id: String           // YouTube video ID
    var title: String
    var thumbnailURL: URL
    var addedAt: Date
    var category: String?
}
```

---

## 🎯 Design Assets

### No Direct Visual Assets for Data Layer

Data persistence is a backend concern without direct visual representation. However, the data models support these visual screens:

**Related Screens**:
1. **Player Selection** (`Reference_Player_Selection_Screen.png`)
   - Displays player coins from `PlayerData.coins`
   - Shows player avatars

2. **Home Screen** (`Reference_Menu_Screen.png`)
   - Shows current coin count from `PlayerData.coins`
   - Shows activity unlock states from `ParentSettings.activityLocks`

3. **Treasure Screen** (`Reference_Treasure_Screen.png`)
   - Displays coin balance
   - Shows approved videos from `ParentSettings.approvedVideos`

4. **Parent Dashboard** (Not yet designed)
   - Will display all `PlayerData` statistics
   - Will show all `ParentSettings` controls

---

## 🔗 Integration Points

### Phase 2: Design System
**Dependency**: BennieColors enum for validation display

```swift
// Error states use design system colors
if validationFailed {
    errorColor = BennieColors.error  // From design system
}
```

### Phase 3: Core Screens
**Dependency**: Screens display data from models

```swift
// HomeView depends on PlayerData
struct HomeView: View {
    @Environment(\.currentPlayer) var player: PlayerData
    
    var body: some View {
        CoinDisplay(count: player.coins)  // Display from model
    }
}
```

### Phase 5: Reward System
**Critical Integration**: Coin awards must persist

```swift
// CelebrationOverlay triggers data save
func onCelebration() {
    player.coins += 1
    try? modelContext.save()  // MUST persist immediately
}
```

### Phase 12: Adaptive Difficulty
**Critical Integration**: Learning profile drives difficulty

```swift
// ActivityView reads from learning profile
let difficulty = player.learningProfile.currentDifficulty
let gridSize = player.learningProfile.puzzleGridSizePreference
generateLevel(difficulty: difficulty, gridSize: gridSize)
```

---

## ✅ Validation Checklist

### Against Playbook Part 5.4

```swift
// Save triggers validation (from playbook table)
func validateSaveTriggers() {
    // ✓ Level completed -> PlayerData.coins, activityProgress, learningProfile
    // ✓ Activity quit -> ActivityProgress.quitCount, learningProfile.quitRate
    // ✓ Video finished -> VideoRecord, PlayerData.todayVideosWatched
    // ✓ Session end -> SessionMetrics, PlayerData.lastPlayedDate
    // ✓ Settings changed -> AppSettings, ParentSettings
    // ✓ App background -> All unsaved changes
}

// Load points validation (from playbook table)
func validateLoadPoints() {
    // ✓ App Launch -> AppSettings, last active PlayerData
    // ✓ Player Selection -> All PlayerData records
    // ✓ Home Screen -> Current player's coins, progress
    // ✓ Activity Screen -> ActivityProgress for specific activity
    // ✓ Treasure Screen -> Coins, approved videos
    // ✓ Parent Dashboard -> ParentSettings, all PlayerData stats
}
```

### Against Playbook Part 0.4

```swift
// Coin economy validation
func validateCoinEconomy() {
    assert(CoinSystem.coinsPerLevel == 1)
    assert(CoinSystem.celebrationMilestone == 5)
    assert(CoinSystem.tier1Redemption == 10)
    assert(CoinSystem.tier2Redemption == 20)
    assert(CoinSystem.tier2BonusMinutes == 2)
}
```

### Against Playbook Part 5.5

```swift
// Offline behavior validation
func validateOfflineBehavior() {
    // ✓ All activities work offline
    assert(allActivitiesOffline == true)
    
    // ✓ YouTube requires internet
    assert(youtubeRequiresInternet == true)
    
    // ✓ Progress saves locally
    assert(progressSavesLocally == true)
}
```

---

## 📊 Data Flow Diagrams

### Coin Flow
```
User completes level
    ↓
ActivityView calls PlayerProfileService.recordActivityComplete()
    ↓
PlayerProfileService.awardCoin()
    ↓
PlayerData.coins += 1
    ↓
DataStoreManager.savePlayer()
    ↓
SwiftData persists to disk
    ↓
CoinDisplay updates (via @Observable)
```

### Video Redemption Flow
```
User taps "5 Min YouTube" button
    ↓
TreasureView calls PlayerProfileService.deductCoins(10)
    ↓
Check: PlayerData.coins >= 10?
    ↓ YES
PlayerData.coins -= 10
    ↓
Navigate to VideoSelectionView
    ↓
User selects video
    ↓
VideoPlayerView starts playback
    ↓
On completion: PlayerProfileService.recordVideoWatch()
    ↓
VideoRecord added to PlayerData.todayVideosWatched
    ↓
DataStoreManager.savePlayer()
```

### Daily Reset Flow
```
App launches
    ↓
DataStoreManager.checkDailyReset()
    ↓
Compare PlayerData.lastPlayedDate to today
    ↓ Different day
For each player: resetDailyProgress()
    ↓
PlayerData.todayPlayTimeMinutes = 0
PlayerData.todayActivitiesCompleted = 0
PlayerData.todayVideosWatched = []
    ↓
PlayerData.lastPlayedDate = today
    ↓
Save all players
```

---

## 🧪 Testing Against Playbook

### Test: Coin Economy Rules
```swift
func testCoinEconomyMatchesPlaybook() throws {
    // From playbook Part 0.4
    let player = PlayerData.empty
    
    // Complete activity -> +1 coin
    try profileService.recordActivityComplete(.raetselPuzzle, duration: 30, mistakes: 0, for: player.id)
    XCTAssertEqual(player.coins, 1)
    
    // Redeem tier 1 -> -10 coins
    let success = try profileService.deductCoins(10, from: player.id)
    XCTAssertTrue(success)
    XCTAssertEqual(player.coins, -9) // Should fail!
}
```

### Test: Activity Types Match MVP
```swift
func testActivityTypesMatchPlaybookMVP() {
    // From playbook Part 0.3
    let mvpActivities: Set<ActivityType> = [
        .raetselPuzzle,
        .raetselLabyrinth,
        .zahlenWuerfel,
        .zahlenWaehle
    ]
    
    // Ensure ONLY these 4 exist in Phase 1
    XCTAssertEqual(Set(ActivityType.allCases), mvpActivities)
}
```

### Test: Offline Behavior
```swift
func testOfflineBehaviorMatchesPlaybook() {
    // From playbook Part 5.5
    let networkMonitor = NetworkMonitor()
    networkMonitor.isConnected = false
    
    // All activities should work
    XCTAssertTrue(PuzzleMatchingView.worksOffline)
    XCTAssertTrue(LabyrinthView.worksOffline)
    XCTAssertTrue(WuerfelView.worksOffline)
    
    // YouTube should not work
    XCTAssertFalse(VideoPlayerView.worksOffline)
    
    // Progress saves should work
    XCTAssertTrue(DataStoreManager.savesOffline)
}
```

---

## 📝 Implementation Notes

### Critical Playbook Compliance Points

1. **Coin amounts are EXACT** (Part 0.4)
   - 1 coin per activity completion
   - 10 coins for 5 minutes
   - 20 coins for 10+2 minutes
   - DO NOT change these values

2. **Activity types are LOCKED for MVP** (Part 0.3)
   - Only 4 activities in Phase 1
   - Zeichnen and Logik are future phases
   - DO NOT add them to ActivityType enum yet

3. **Offline behavior is NON-NEGOTIABLE** (Part 5.5)
   - All activities MUST work offline
   - YouTube MUST require internet
   - Progress MUST save locally
   - DO NOT add cloud sync in Phase 1

4. **Save triggers are MANDATORY** (Part 5.4)
   - MUST save on level complete
   - MUST save on activity quit
   - MUST save on video complete
   - MUST save on app background
   - DO NOT defer or batch these saves

5. **Data validation is REQUIRED** (Part 5.4)
   - Validate on every save
   - Run integrity check on app launch
   - Prevent invalid states
   - DO NOT skip validation for performance

---

## 🚀 Quick Start Commands

### View All Playbook References
```bash
# Search for data persistence in playbook
rg "Data Persistence" docs/playbook/

# Search for coin system
rg "Coin Economy" docs/playbook/

# Search for offline behavior
rg "Offline Behavior" docs/playbook/
```

### Validate Implementation
```bash
# Run data model tests
swift test --filter DataModels

# Run service tests
swift test --filter Services

# Check playbook compliance
swift test --filter PlaybookCompliance
```

---

**Last Updated**: Phase 10 Implementation  
**Maintained By**: Development Team  
**Next Review**: After Phase 10 completion
