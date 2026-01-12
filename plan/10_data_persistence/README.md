# Phase 10: Data Persistence & Storage

> **Status**: Ready for Implementation  
> **Dependencies**: Phase 2 (Design System), Phase 5 (Reward System)  
> **Duration**: 2-3 days  
> **📖 COMPREHENSIVE REFERENCES**: See [PHASE_REFERENCES.md](./PHASE_REFERENCES.md) for complete playbook sections, code examples, validation rules, and integration points

---

> **⚡ Quick Links**:  
> - 📚 [Playbook Part 5.4: Data Persistence](../../docs/playbook/FULL_ARCHIVE.md) (Lines 1480-1550)  
> - 📊 [Data Models Specification](./data_models.md)  
> - 🔗 [Phase References Guide](./PHASE_REFERENCES.md)  

---

## 📋 Overview

Implement complete local data storage system using SwiftData for player progress, settings, and game state. This phase covers all persistence needs from player profiles to parent settings.

### Key Deliverables

1. ✅ SwiftData models for all game entities
2. ✅ Data managers and services
3. ✅ Migration strategy for version updates
4. ✅ Backup and restore functionality
5. ✅ Data validation and integrity checks
6. ✅ Testing fixtures and previews

---

## 📚 Playbook References

### Primary References
- **Part 5.4**: Data Persistence (FULL_ARCHIVE.md)
  - Local storage structure
  - SwiftData vs UserDefaults usage
  - Offline behavior requirements

- **Part 2.2**: Core Loop & Coin System (FULL_ARCHIVE.md)
  - Coin earning rules
  - Progress tracking requirements
  - Redemption rules

- **Part 9.6**: Adaptive Difficulty System (FULL_ARCHIVE.md)
  - Learning profile structure
  - Difficulty tracking requirements

### Supporting References
- **Part 4.11**: Parent Dashboard (FULL_ARCHIVE.md)
  - Parent settings structure
  - Time limits and activity locks
  - Video management

---

## 🎯 Tasks

### Task 10.1: Data Models
**Goal**: Implement all SwiftData models

**Playbook Reference**: Part 5.4, Section "Local Storage Structure"

**Files to Create**:
```
BennieGame/
├── Services/
│   └── Data/
│       ├── Models/
│       │   ├── PlayerData.swift
│       │   ├── AppSettings.swift
│       │   ├── ParentSettings.swift
│       │   ├── ActivityProgress.swift
│       │   ├── LearningProfile.swift
│       │   ├── ApprovedVideo.swift
│       │   ├── VideoRecord.swift
│       │   └── SessionMetrics.swift
│       └── Enums/
│           ├── ActivityType.swift
│           └── StorageKeys.swift
```

**Implementation Details**:
1. Copy base models from `data_models.md`
2. Add SwiftData attributes (@Model, @Attribute)
3. Add Codable conformance for all nested structs
4. Add validation logic to prevent invalid states
5. Add convenience initializers for testing

**Exit Criteria**:
- [ ] All 8 models compile without errors
- [ ] All models are Codable
- [ ] PlayerData has @Attribute(.unique) on id
- [ ] ActivityType enum includes all activities per playbook Part 0.3
- [ ] ApprovedVideo.extractVideoID handles all URL formats
- [ ] No force unwraps in any model code

**QA Checklist**:
```swift
// Verify coin rules from playbook
assert(PlayerData.maxDailyCoins == nil) // No daily cap mentioned
assert(ActivityProgress.coinsPerLevel == 1)

// Verify redemption tiers from Part 5
assert(tier1RequiresCoin == 10 && tier1Minutes == 5)
assert(tier2RequiresCoin == 20 && tier2Minutes == 12)

// Verify activity types match playbook Part 0.3
assert(ActivityType.allCases.count == 4) // Phase 1 MVP
```

---

### Task 10.2: Data Store Manager
**Goal**: Create centralized data access layer

**Playbook Reference**: Part 5.4, Section "Save Triggers" and "Load Points"

**File to Create**:
```
Services/Data/DataStoreManager.swift
```

**Implementation**:
```swift
@Observable
class DataStoreManager {
    private let modelContext: ModelContext
    
    // Player Management
    func loadPlayer(_ id: String) -> PlayerData?
    func savePlayer(_ player: PlayerData) throws
    func createPlayer(id: String, name: String) -> PlayerData
    func deletePlayer(_ id: String) throws
    
    // Settings Management
    func loadSettings() -> AppSettings
    func saveSettings(_ settings: AppSettings) throws
    
    // Session Management
    func startSession(for playerId: String) -> SessionMetrics
    func endSession(_ session: SessionMetrics) throws
    func updateSessionMetrics(_ session: inout SessionMetrics)
    
    // Daily Reset
    func checkDailyReset() // Called on app launch
    func resetDailyProgress(for playerId: String)
    
    // Backup & Restore
    func exportBackup() throws -> Data
    func importBackup(_ data: Data) throws
    
    // Validation
    func validateDataIntegrity() throws
}
```

**Exit Criteria**:
- [ ] All CRUD operations work for each model type
- [ ] Daily reset correctly zeros `todayPlayTimeMinutes` and `todayActivitiesCompleted`
- [ ] Session metrics automatically update learning profile on save
- [ ] Backup exports to JSON successfully
- [ ] Import validates data before applying
- [ ] Data integrity check catches corrupted states

---

### Task 10.3: Player Profile Service
**Goal**: High-level player operations

**File to Create**:
```
Services/PlayerProfileService.swift
```

**Implementation**:
```swift
class PlayerProfileService {
    private let dataStore: DataStoreManager
    
    // Coin Operations
    func awardCoin(to playerId: String) throws
    func deductCoins(_ amount: Int, from playerId: String) throws -> Bool
    func getCoinBalance(for playerId: String) -> Int
    
    // Activity Progress
    func recordActivityStart(_ type: ActivityType, for playerId: String)
    func recordActivityComplete(_ type: ActivityType, 
                                duration: TimeInterval,
                                mistakes: Int,
                                for playerId: String) throws
    func recordActivityQuit(_ type: ActivityType, for playerId: String) throws
    
    // Video Tracking
    func recordVideoWatch(videoId: String,
                          title: String,
                          duration: TimeInterval,
                          for playerId: String) throws
    
    // Learning Profile Updates
    func updateLearningProfile(with metrics: SessionMetrics) throws
    
    // Statistics
    func getStats(for playerId: String) -> PlayerStats
}

struct PlayerStats {
    let totalCoinsEarned: Int
    let activitiesCompleted: Int
    let averageSolveTime: TimeInterval
    let favoriteActivity: ActivityType?
    let consecutiveDays: Int
}
```

**Exit Criteria**:
- [ ] Coin awards trigger coin fly animation (integration with Phase 5)
- [ ] Activity completion updates both ActivityProgress and LearningProfile
- [ ] Video tracking prevents replay within same session
- [ ] Stats calculation is accurate across all players
- [ ] All operations are atomic (succeed or rollback)

---

### Task 10.4: Parent Settings Service
**Goal**: Parent dashboard data operations

**Playbook Reference**: Part 4.11 "Parent Dashboard"

**File to Create**:
```
Services/ParentSettingsService.swift
```

**Implementation**:
```swift
class ParentSettingsService {
    private let dataStore: DataStoreManager
    
    // Time Limits
    func setDailyTimeLimit(minutes: Int, for playerId: String) throws
    func getDailyTimeLimit(for playerId: String) -> Int
    func getTodayPlayTime(for playerId: String) -> Int
    func canContinuePlaying(_ playerId: String) -> Bool
    
    // Activity Locks
    func lockActivity(_ type: ActivityType, for playerId: String) throws
    func unlockActivity(_ type: ActivityType, for playerId: String) throws
    func isActivityLocked(_ type: ActivityType, for playerId: String) -> Bool
    
    // Video Management
    func addApprovedVideo(url: String) throws -> ApprovedVideo
    func removeApprovedVideo(_ videoId: String) throws
    func getApprovedVideos() -> [ApprovedVideo]
    func updateVideoStats(videoId: String) throws
    
    // Progress Reset
    func resetAllProgress(for playerId: String, confirm: Bool) throws
}
```

**Exit Criteria**:
- [ ] Time limit enforcement blocks play when exceeded
- [ ] Activity locks properly gray out buttons (integration with Phase 3)
- [ ] Video URL parsing handles all YouTube formats from playbook
- [ ] Progress reset requires confirmation parameter
- [ ] All operations persist immediately

---

### Task 10.5: Migration Strategy
**Goal**: Handle version upgrades gracefully

**Playbook Reference**: Part 5.4 (implied by data structure changes)

**File to Create**:
```
Services/Data/MigrationManager.swift
plan/10_data_persistence/migration_strategy.md
```

**migration_strategy.md Contents**:
```markdown
# Data Migration Strategy

## Version History

### v1.0 (Initial Release)
- PlayerData, AppSettings, ParentSettings
- ActivityProgress for 4 activities
- Basic learning profile

### v1.1 (Future - Zeichnen & Logik)
**New ActivityTypes**:
- ActivityType.zeichnenFrei
- ActivityType.logikSequenz

**Migration Steps**:
1. Check app version in AppSettings
2. If < 1.1, add new activity types to enum
3. Initialize new ActivityProgress entries for existing players
4. Set currentLevel = 1, locked by default
5. Update appVersion to 1.1

### v1.2 (Future - Cloud Sync)
**New Models**:
- SyncToken (for conflict resolution)
- CloudBackup metadata

**Migration Steps**:
1. Add syncToken UUID to PlayerData
2. Add lastSyncDate to AppSettings
3. Initialize sync tokens for existing players
4. Mark all existing data as "needs upload"

## Migration Implementation

```swift
class MigrationManager {
    static func migrate(from oldVersion: String, 
                       to newVersion: String,
                       context: ModelContext) throws {
        // Version comparison
        let old = Version(oldVersion)
        let new = Version(newVersion)
        
        // Apply migrations in order
        if old < Version("1.1") && new >= Version("1.1") {
            try migrateToV1_1(context: context)
        }
        
        if old < Version("1.2") && new >= Version("1.2") {
            try migrateToV1_2(context: context)
        }
        
        // Update version
        let settings = try context.fetch(FetchDescriptor<AppSettings>())
        settings.first?.appVersion = newVersion
        try context.save()
    }
    
    private static func migrateToV1_1(context: ModelContext) throws {
        let players = try context.fetch(FetchDescriptor<PlayerData>())
        for player in players {
            // Add new activities
            player.activityProgress[.zeichnenFrei.rawValue] = 
                ActivityProgress(activityType: .zeichnenFrei)
            player.activityProgress[.logikSequenz.rawValue] = 
                ActivityProgress(activityType: .logikSequenz)
        }
        try context.save()
    }
}
```

## Testing Migration

```swift
func testMigrationV1_0ToV1_1() throws {
    // Create v1.0 data
    let player = PlayerData(id: "test", name: "Test")
    player.activityProgress = [
        "raetsel_puzzle": ActivityProgress(activityType: .raetselPuzzle),
        "raetsel_labyrinth": ActivityProgress(activityType: .raetselLabyrinth),
        "zahlen_wuerfel": ActivityProgress(activityType: .zahlenWuerfel),
        "zahlen_waehle": ActivityProgress(activityType: .zahlenWaehle)
    ]
    
    // Run migration
    try MigrationManager.migrate(from: "1.0", to: "1.1", context: context)
    
    // Verify new activities added
    XCTAssertNotNil(player.activityProgress["zeichnen_frei"])
    XCTAssertNotNil(player.activityProgress["logik_sequenz"])
    XCTAssertEqual(player.activityProgress.count, 6)
}
```
```

**Exit Criteria**:
- [ ] Migration code exists for each version transition
- [ ] Migration is idempotent (can run multiple times safely)
- [ ] User data is never lost during migration
- [ ] Tests cover all migration paths
- [ ] Migration runs automatically on app launch if needed

---

### Task 10.6: Offline Behavior
**Goal**: Ensure full offline functionality

**Playbook Reference**: Part 5.5 "Offline Behavior"

**Implementation Checklist**:

**Per Playbook Requirements**:
```
✅ All activities: Fully offline
✅ Narrator/Bennie audio: Bundled in app
✅ Progress saving: Local storage
❌ YouTube playback: Requires internet
✅ Parent dashboard: Local settings
```

**Network Monitor**:
```swift
// Services/NetworkMonitor.swift
@Observable
class NetworkMonitor {
    var isConnected: Bool = true
    
    private let monitor = NWPathMonitor()
    
    init() {
        monitor.pathUpdateHandler = { [weak self] path in
            DispatchQueue.main.async {
                self?.isConnected = path.status == .satisfied
            }
        }
        monitor.start(queue: DispatchQueue.global())
    }
}
```

**Offline UI States**:
```swift
// In TreasureView
if !networkMonitor.isConnected {
    // Per playbook Part 4.8
    playBennie("wir_brauchen_internet.aac")
    youtubeButtonsEnabled = false
    showOfflineMessage = true
}
```

**Exit Criteria**:
- [ ] NetworkMonitor detects connection changes
- [ ] Treasure screen disables YouTube buttons when offline per playbook
- [ ] All other screens work fully offline
- [ ] Offline indicator appears when network unavailable
- [ ] Data saves queue up if write fails, retry on next save

---

### Task 10.7: Data Validation
**Goal**: Prevent invalid data states

**File to Create**:
```
Services/Data/DataValidator.swift
```

**Validation Rules from Playbook**:

```swift
class DataValidator {
    // Coin validation (Part 2.2)
    static func validateCoinBalance(_ coins: Int) -> Bool {
        return coins >= 0 // No negative coins
    }
    
    // Activity progress validation
    static func validateActivityProgress(_ progress: ActivityProgress) -> Bool {
        return progress.currentLevel >= 1 &&
               progress.highestLevelCompleted <= progress.currentLevel &&
               progress.successRate >= 0.0 && progress.successRate <= 1.0 &&
               progress.currentDifficulty >= 0.0 && progress.currentDifficulty <= 1.0
    }
    
    // Time limit validation (Part 4.11)
    static func validateDailyTimeLimit(_ minutes: Int) -> Bool {
        return minutes >= 0 && minutes <= 240 // Max 4 hours per day
    }
    
    // Learning profile validation
    static func validateLearningProfile(_ profile: LearningProfile) -> Bool {
        return profile.globalDifficultyLevel >= 0.0 &&
               profile.globalDifficultyLevel <= 1.0 &&
               profile.puzzleGridSizePreference >= 3 &&
               profile.puzzleGridSizePreference <= 6 &&
               profile.puzzleColorCount >= 2 &&
               profile.puzzleColorCount <= 4 &&
               profile.numberRange >= 10 && profile.numberRange <= 20
    }
    
    // Video validation
    static func validateVideoURL(_ url: String) -> Bool {
        guard let videoId = ApprovedVideo.extractVideoID(from: url) else {
            return false
        }
        return videoId.count == 11 // YouTube IDs are always 11 chars
    }
    
    // Run all validations
    static func validatePlayerData(_ player: PlayerData) throws {
        guard validateCoinBalance(player.coins) else {
            throw ValidationError.invalidCoinBalance
        }
        
        for progress in player.activityProgress.values {
            guard validateActivityProgress(progress) else {
                throw ValidationError.invalidActivityProgress
            }
        }
        
        guard validateLearningProfile(player.learningProfile) else {
            throw ValidationError.invalidLearningProfile
        }
    }
}

enum ValidationError: Error {
    case invalidCoinBalance
    case invalidActivityProgress
    case invalidLearningProfile
    case invalidTimeLimit
    case invalidVideoURL
}
```

**Exit Criteria**:
- [ ] All setter methods validate before accepting values
- [ ] DataStoreManager.validateDataIntegrity() calls all validators
- [ ] Invalid data throws specific errors with helpful messages
- [ ] Validation runs on app launch
- [ ] Corrupted data can be repaired or reset with user consent

---

### Task 10.8: Testing Fixtures
**Goal**: Provide test data for previews and unit tests

**Files to Create**:
```
BennieGame/Testing/
├── Fixtures/
│   ├── PlayerDataFixtures.swift
│   ├── AppSettingsFixtures.swift
│   └── TestModelContainer.swift
└── README.md
```

**Implementation**:

```swift
// Testing/Fixtures/PlayerDataFixtures.swift
extension PlayerData {
    static var alexander: PlayerData {
        let player = PlayerData(id: "alexander", name: "Alexander")
        player.coins = 12
        player.totalCoinsEarned = 47
        player.todayPlayTimeMinutes = 23
        
        // Add activity progress per playbook Part 0.3
        player.activityProgress = [
            ActivityType.raetselPuzzle.rawValue: {
                var progress = ActivityProgress(activityType: .raetselPuzzle)
                progress.currentLevel = 5
                progress.highestLevelCompleted = 4
                progress.totalLevelsCompleted = 12
                return progress
            }(),
            ActivityType.zahlenWuerfel.rawValue: {
                var progress = ActivityProgress(activityType: .zahlenWuerfel)
                progress.currentLevel = 3
                progress.highestLevelCompleted = 2
                progress.totalLevelsCompleted = 8
                return progress
            }()
        ]
        
        return player
    }
    
    static var oliver: PlayerData {
        let player = PlayerData(id: "oliver", name: "Oliver")
        player.coins = 7
        player.totalCoinsEarned = 31
        player.todayPlayTimeMinutes = 15
        return player
    }
    
    static var empty: PlayerData {
        PlayerData(id: "test", name: "Test Player")
    }
}

// Testing/Fixtures/AppSettingsFixtures.swift
extension AppSettings {
    static var standard: AppSettings {
        let settings = AppSettings()
        settings.audioEnabled = true
        settings.musicVolume = 0.30
        settings.voiceVolume = 1.00
        settings.effectsVolume = 0.70
        
        // Add approved videos per playbook Part 4.11
        settings.parentSettings.approvedVideos = [
            ApprovedVideo(
                id: "dQw4w9WgXcQ",
                title: "Test Video 1",
                thumbnailURL: URL(string: "https://i.ytimg.com/vi/dQw4w9WgXcQ/default.jpg")!,
                duration: 300
            )
        ]
        
        return settings
    }
}

// Testing/Fixtures/TestModelContainer.swift
extension ModelContainer {
    static var preview: ModelContainer {
        let schema = Schema([
            PlayerData.self,
            AppSettings.self
        ])
        
        let config = ModelConfiguration(isStoredInMemoryOnly: true)
        let container = try! ModelContainer(for: schema, configurations: config)
        
        // Populate with test data
        let context = container.mainContext
        context.insert(PlayerData.alexander)
        context.insert(PlayerData.oliver)
        context.insert(AppSettings.standard)
        
        return container
    }
}
```

**Usage in Previews**:
```swift
#Preview {
    HomeView()
        .modelContainer(.preview)
        .environment(\.currentPlayer, PlayerData.alexander)
}
```

**Exit Criteria**:
- [ ] Fixtures exist for all models
- [ ] TestModelContainer provides realistic data
- [ ] All SwiftUI previews use fixtures
- [ ] Unit tests use fixtures for consistency
- [ ] Fixtures cover edge cases (0 coins, max coins, no progress, etc.)

---

### Task 10.9: Unit Tests
**Goal**: Comprehensive test coverage

**Files to Create**:
```
BennieGameTests/
├── DataModels/
│   ├── PlayerDataTests.swift
│   ├── ActivityProgressTests.swift
│   └── LearningProfileTests.swift
├── Services/
│   ├── DataStoreManagerTests.swift
│   ├── PlayerProfileServiceTests.swift
│   └── ParentSettingsServiceTests.swift
└── Migration/
    └── MigrationManagerTests.swift
```

**Test Coverage Requirements**:

**PlayerData Tests**:
```swift
func testCoinAward() {
    let player = PlayerData.empty
    player.coins = 5
    player.coins += 1 // Award coin
    XCTAssertEqual(player.coins, 6)
    player.totalCoinsEarned += 1
    XCTAssertEqual(player.totalCoinsEarned, 1)
}

func testCoinDeduction() {
    let player = PlayerData.empty
    player.coins = 10
    let success = player.coins >= 10
    if success {
        player.coins -= 10
    }
    XCTAssertEqual(player.coins, 0)
}

func testDailyReset() {
    let player = PlayerData.empty
    player.todayPlayTimeMinutes = 45
    player.todayActivitiesCompleted = 12
    player.todayVideosWatched = [
        VideoRecord(videoId: "test", videoTitle: "Test", duration: 300, playerId: "test")
    ]
    
    // Reset
    player.todayPlayTimeMinutes = 0
    player.todayActivitiesCompleted = 0
    player.todayVideosWatched = []
    
    XCTAssertEqual(player.todayPlayTimeMinutes, 0)
    XCTAssertEqual(player.todayActivitiesCompleted, 0)
    XCTAssertTrue(player.todayVideosWatched.isEmpty)
}
```

**ActivityProgress Tests**:
```swift
func testDifficultyBounds() {
    var progress = ActivityProgress(activityType: .raetselPuzzle)
    progress.currentDifficulty = 0.0
    XCTAssertTrue(DataValidator.validateActivityProgress(progress))
    
    progress.currentDifficulty = 1.0
    XCTAssertTrue(DataValidator.validateActivityProgress(progress))
    
    progress.currentDifficulty = -0.1
    XCTAssertFalse(DataValidator.validateActivityProgress(progress))
    
    progress.currentDifficulty = 1.1
    XCTAssertFalse(DataValidator.validateActivityProgress(progress))
}
```

**ApprovedVideo Tests**:
```swift
func testExtractVideoID() {
    // Standard format
    let url1 = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    XCTAssertEqual(ApprovedVideo.extractVideoID(from: url1), "dQw4w9WgXcQ")
    
    // Short format
    let url2 = "https://youtu.be/dQw4w9WgXcQ"
    XCTAssertEqual(ApprovedVideo.extractVideoID(from: url2), "dQw4w9WgXcQ")
    
    // Embed format
    let url3 = "https://www.youtube.com/embed/dQw4w9WgXcQ"
    XCTAssertEqual(ApprovedVideo.extractVideoID(from: url3), "dQw4w9WgXcQ")
    
    // Invalid
    let url4 = "https://www.google.com"
    XCTAssertNil(ApprovedVideo.extractVideoID(from: url4))
}
```

**Exit Criteria**:
- [ ] All data models have >90% test coverage
- [ ] All services have >80% test coverage
- [ ] Migration tests cover all version transitions
- [ ] Validation tests cover all edge cases
- [ ] Tests run in <5 seconds total

---

## 🎓 Learning Resources

### SwiftData
- [Apple SwiftData Documentation](https://developer.apple.com/documentation/swiftdata)
- [WWDC23: Meet SwiftData](https://developer.apple.com/videos/play/wwdc2023/10187/)
- [SwiftData Migration Guide](https://developer.apple.com/documentation/swiftdata/migrating-your-app-to-swiftdata)

### Data Modeling
- [Core Data to SwiftData Migration](https://www.hackingwithswift.com/quick-start/swiftdata)
- [SwiftData Best Practices](https://www.avanderlee.com/swiftdata/getting-started/)

---

## ✅ Phase Exit Criteria

### Functionality
- [ ] All 8 data models compile and work
- [ ] DataStoreManager handles all CRUD operations
- [ ] PlayerProfileService integrates with Phase 5 (coins)
- [ ] ParentSettingsService enforces all rules from playbook Part 4.11
- [ ] Migration strategy handles version upgrades
- [ ] Offline mode works per playbook Part 5.5
- [ ] Data validation prevents invalid states
- [ ] Backup/restore functions work

### Code Quality
- [ ] All models documented with inline comments
- [ ] All services have unit tests
- [ ] No force unwraps in production code
- [ ] All errors are handled gracefully
- [ ] Code follows BennieGame naming conventions

### Integration
- [ ] SwiftData container configured in BennieGameApp
- [ ] All views can access ModelContext
- [ ] Fixtures work in all SwiftUI previews
- [ ] Data persists across app restarts
- [ ] Daily reset triggers correctly

### Performance
- [ ] Data saves complete in <100ms
- [ ] Data loads complete in <50ms
- [ ] No memory leaks in data operations
- [ ] Background saves don't block UI

### Playbook Compliance
- [ ] Coin rules match Part 2.2 exactly
- [ ] Redemption tiers match Part 0.4 exactly
- [ ] Activity types match Part 0.3 MVP list
- [ ] Time limits enforce playbook Part 4.11 rules
- [ ] Offline behavior matches Part 5.5 table
- [ ] YouTube URL validation per Part 4.9

---

## 📊 Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Test Coverage | >85% | Xcode coverage report |
| Save Latency | <100ms | Performance test |
| Load Latency | <50ms | Performance test |
| Data Integrity | 100% | Validation passes on all data |
| Migration Success | 100% | All version upgrades work |

---

## 🚨 Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Data loss on migration | HIGH | Backup before migration, rollback on failure |
| Corrupted data state | MEDIUM | Validation on every save, integrity checks |
| SwiftData bugs | MEDIUM | Fallback to UserDefaults for critical data |
| Performance degradation | LOW | Background saves, lazy loading |

---

## 📝 Notes

### SwiftData vs UserDefaults Decision

**Use SwiftData for**:
- PlayerData (complex, relational)
- AppSettings (structured)
- SessionMetrics (historical data)

**Use UserDefaults for**:
- Last active player ID (quick access)
- Audio enabled flag (frequently read)
- Simple flags and preferences

### Backup Strategy

Per playbook requirements (no cloud sync in MVP):
- Backup exports to JSON file
- User can save to Files app
- Import validates before applying
- No automatic cloud backup

### Future Enhancements (Post-MVP)

1. **Cloud Sync** (v1.2)
   - iCloud sync for multi-device
   - Conflict resolution strategy
   - Sync status indicators

2. **Analytics** (v1.3)
   - Anonymized usage tracking
   - Performance metrics
   - Crash reporting

3. **Export for Parents** (v1.4)
   - PDF progress reports
   - CSV data export
   - Email reports

---

**Phase Owner**: Data/Backend Developer  
**Review Required**: Lead Developer, QA  
**Integration Points**: All phases depend on this

