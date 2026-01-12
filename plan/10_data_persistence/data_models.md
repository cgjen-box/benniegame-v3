# Data Models - Complete Specification

> **Purpose**: Define all data structures for local storage
> **Storage**: SwiftData + UserDefaults
> **Persistence**: Local only (no cloud sync)

---

## Core Data Models

### 1. PlayerData

**Purpose**: Store per-player game state and progress

```swift
@Model
class PlayerData: Codable {
    // Identity
    @Attribute(.unique) var id: String              // "alexander" or "oliver"
    var name: String                                // Display name
    var avatarName: String                          // Avatar image name
    var createdAt: Date
    
    // Currency & Progress
    var coins: Int                                  // Current coin balance
    var totalCoinsEarned: Int                       // Lifetime total
    var consecutiveDays: Int                        // Streak tracking
    var lastPlayedDate: Date?
    
    // Activity Progress
    var activityProgress: [String: ActivityProgress]
    
    // Today's Play Session
    var todayPlayTimeMinutes: Int                   // Resets daily
    var todayActivitiesCompleted: Int               // Count
    var todayVideosWatched: [VideoRecord]           // Today's videos
    
    // Learning Profile
    var learningProfile: LearningProfile
    
    // Preferences
    var preferredActivities: [ActivityType]
    
    init(id: String, name: String) {
        self.id = id
        self.name = name
        self.avatarName = "\(id)_avatar"
        self.createdAt = Date()
        self.coins = 0
        self.totalCoinsEarned = 0
        self.consecutiveDays = 0
        self.lastPlayedDate = nil
        self.activityProgress = [:]
        self.todayPlayTimeMinutes = 0
        self.todayActivitiesCompleted = 0
        self.todayVideosWatched = []
        self.learningProfile = LearningProfile()
        self.preferredActivities = []
    }
}
```

---

### 2. ActivityProgress

**Purpose**: Track progress within each activity type

```swift
struct ActivityProgress: Codable, Hashable {
    var activityType: ActivityType
    var currentLevel: Int                           // Highest unlocked
    var highestLevelCompleted: Int
    var totalLevelsCompleted: Int
    var totalTimeSpentSeconds: Int
    var averageSolveTimeSeconds: Double
    var successRate: Double                         // 0.0-1.0
    var lastPlayedDate: Date?
    var mistakeCount: Int                           // Total mistakes
    var hintRequestCount: Int                       // Times hints used
    var quitCount: Int                              // Times quit mid-level
    
    // Difficulty tracking
    var currentDifficulty: Float                    // 0.0 (easy) - 1.0 (hard)
    
    init(activityType: ActivityType) {
        self.activityType = activityType
        self.currentLevel = 1
        self.highestLevelCompleted = 0
        self.totalLevelsCompleted = 0
        self.totalTimeSpentSeconds = 0
        self.averageSolveTimeSeconds = 0
        self.successRate = 1.0
        self.lastPlayedDate = nil
        self.mistakeCount = 0
        self.hintRequestCount = 0
        self.quitCount = 0
        self.currentDifficulty = 0.3  // Start easy
    }
}

enum ActivityType: String, Codable, CaseIterable {
    case raetselPuzzle = "raetsel_puzzle"
    case raetselLabyrinth = "raetsel_labyrinth"
    case zahlenWuerfel = "zahlen_wuerfel"
    case zahlenWaehle = "zahlen_waehle"
    // Future:
    // case zeichnenFrei = "zeichnen_frei"
    // case logikSequenz = "logik_sequenz"
}
```

---

### 3. LearningProfile

**Purpose**: AI-powered adaptive difficulty tracking

```swift
struct LearningProfile: Codable {
    // Performance Metrics
    var averageSolveTime: TimeInterval              // Across all activities
    var mistakeFrequency: Double                    // Mistakes per level
    var quitRate: Double                            // Quit % (0.0-1.0)
    var sessionDuration: TimeInterval               // Average session length
    
    // Engagement Indicators
    var hintUsageRate: Double                       // Hints per level
    var celebrationEngagement: Bool                 // Taps "Weiter" quickly?
    var preferredActivityTypes: [ActivityType: Int] // Play count per type
    var timeOfDayPreference: [Int: Int]             // Hour -> session count
    
    // Adaptive Parameters
    var globalDifficultyLevel: Float                // 0.0-1.0, affects all activities
    var puzzleGridSizePreference: Int               // 3, 4, 5, or 6
    var puzzleColorCount: Int                       // 2-4 colors
    var labyrinthComplexity: Float                  // 0.0-1.0
    var numberRange: Int                            // 1-10 or 1-20
    
    // Behavioral Patterns
    var respondsWellToHints: Bool                   // True if hints improve performance
    var needsMoreEncouragement: Bool                // True if quits often
    var prefersShortSessions: Bool                  // True if average < 10min
    
    // Last Updated
    var lastUpdated: Date
    
    init() {
        self.averageSolveTime = 30.0
        self.mistakeFrequency = 0.0
        self.quitRate = 0.0
        self.sessionDuration = 600.0  // 10 minutes
        self.hintUsageRate = 0.0
        self.celebrationEngagement = true
        self.preferredActivityTypes = [:]
        self.timeOfDayPreference = [:]
        self.globalDifficultyLevel = 0.3  // Start easy
        self.puzzleGridSizePreference = 3
        self.puzzleColorCount = 2
        self.labyrinthComplexity = 0.2
        self.numberRange = 10
        self.respondsWellToHints = true
        self.needsMoreEncouragement = false
        self.prefersShortSessions = false
        self.lastUpdated = Date()
    }
    
    mutating func update(with metrics: SessionMetrics) {
        // Update profile based on session metrics
        // See adaptive_difficulty.md for update logic
    }
}
```

---

### 4. AppSettings

**Purpose**: Global app configuration and parent settings

```swift
@Model
class AppSettings: Codable {
    // Active Session
    var lastActivePlayerId: String?
    var currentSessionStartTime: Date?
    
    // Audio Settings
    var audioEnabled: Bool
    var musicVolume: Float                          // 0.0-1.0
    var voiceVolume: Float                          // 0.0-1.0
    var effectsVolume: Float                        // 0.0-1.0
    
    // Parent Settings
    var parentSettings: ParentSettings
    
    // App State
    var appVersion: String
    var lastLaunchDate: Date?
    var totalLaunches: Int
    
    init() {
        self.lastActivePlayerId = nil
        self.currentSessionStartTime = nil
        self.audioEnabled = true
        self.musicVolume = 0.30
        self.voiceVolume = 1.00
        self.effectsVolume = 0.70
        self.parentSettings = ParentSettings()
        self.appVersion = Bundle.main.appVersion
        self.lastLaunchDate = nil
        self.totalLaunches = 0
    }
}
```

---

### 5. ParentSettings

**Purpose**: Parent dashboard configuration

```swift
struct ParentSettings: Codable {
    // Per-Player Time Limits (minutes per day)
    var dailyTimeLimits: [String: Int]              // ["alexander": 60, "oliver": 60]
    
    // Activity Locks
    var lockedActivities: [String: [ActivityType]]  // Per-player locked activities
    
    // YouTube Settings
    var approvedVideos: [ApprovedVideo]
    var videoAutoplay: Bool                         // False = require selection
    
    // Notifications
    var sendDailyProgressEmail: Bool
    var parentEmail: String?
    
    init() {
        self.dailyTimeLimits = ["alexander": 60, "oliver": 60]
        self.lockedActivities = [
            "alexander": [],
            "oliver": []
        ]
        self.approvedVideos = []
        self.videoAutoplay = false
        self.sendDailyProgressEmail = false
        self.parentEmail = nil
    }
}
```

---

### 6. ApprovedVideo

**Purpose**: Pre-approved YouTube videos for redemption

```swift
struct ApprovedVideo: Codable, Identifiable {
    let id: String                                  // YouTube video ID
    var title: String                               // Display title
    var thumbnailURL: URL                           // Cached thumbnail
    var duration: TimeInterval                      // Video length
    var addedAt: Date                               // When parent added it
    var category: String?                           // Optional grouping
    var watchCount: Int                             // Times watched
    var lastWatchedAt: Date?
    
    init(id: String, title: String, thumbnailURL: URL, duration: TimeInterval) {
        self.id = id
        self.title = title
        self.thumbnailURL = thumbnailURL
        self.duration = duration
        self.addedAt = Date()
        self.category = nil
        self.watchCount = 0
        self.lastWatchedAt = nil
    }
    
    static func extractVideoID(from url: String) -> String? {
        // Parse various YouTube URL formats:
        // - youtube.com/watch?v=XXX
        // - youtu.be/XXX
        // - youtube.com/embed/XXX
        
        let patterns = [
            "(?:v=|/)([0-9A-Za-z_-]{11}).*",  // Standard format
            "youtu.be/([0-9A-Za-z_-]{11})",   // Short format
        ]
        
        for pattern in patterns {
            if let regex = try? NSRegularExpression(pattern: pattern),
               let match = regex.firstMatch(in: url, range: NSRange(url.startIndex..., in: url)),
               let range = Range(match.range(at: 1), in: url) {
                return String(url[range])
            }
        }
        
        return nil
    }
}
```

---

### 7. VideoRecord

**Purpose**: Track individual video watch sessions

```swift
struct VideoRecord: Codable, Identifiable {
    let id: UUID
    var videoId: String                             // YouTube video ID
    var videoTitle: String
    var watchedAt: Date
    var duration: TimeInterval                      // How long watched
    var completed: Bool                             // Watched to end?
    var playerId: String                            // Who watched
    
    init(videoId: String, videoTitle: String, duration: TimeInterval, playerId: String) {
        self.id = UUID()
        self.videoId = videoId
        self.videoTitle = videoTitle
        self.watchedAt = Date()
        self.duration = duration
        self.completed = false
        self.playerId = playerId
    }
}
```

---

### 8. SessionMetrics

**Purpose**: Track single gameplay session for profile updates

```swift
struct SessionMetrics: Codable {
    var sessionId: UUID
    var playerId: String
    var startTime: Date
    var endTime: Date
    var duration: TimeInterval
    
    // Activity Metrics
    var activitiesCompleted: Int
    var activitiesQuit: Int
    var totalMistakes: Int
    var hintsUsed: Int
    var averageSolveTime: TimeInterval
    
    // Engagement Metrics
    var celebrationTapDelay: TimeInterval           // Avg time to tap "Weiter"
    var idleTimeTotal: TimeInterval                 // Total time inactive
    var voiceLineCompletions: Int                   // Times listened fully
    
    // Performance Metrics
    var avgFPS: Double
    var peakMemoryMB: Double
    var crashCount: Int
    
    init(playerId: String) {
        self.sessionId = UUID()
        self.playerId = playerId
        self.startTime = Date()
        self.endTime = Date()
        self.duration = 0
        self.activitiesCompleted = 0
        self.activitiesQuit = 0
        self.totalMistakes = 0
        self.hintsUsed = 0
        self.averageSolveTime = 0
        self.celebrationTapDelay = 0
        self.idleTimeTotal = 0
        self.voiceLineCompletions = 0
        self.avgFPS = 60.0
        self.peakMemoryMB = 0
        self.crashCount = 0
    }
}
```

---

## Data Flow

### Save Triggers

| Event | What Gets Saved |
|-------|-----------------|
| Level completed | PlayerData.coins, activityProgress, learningProfile |
| Activity quit | ActivityProgress.quitCount, learningProfile.quitRate |
| Video finished | VideoRecord, PlayerData.todayVideosWatched |
| Session end | SessionMetrics, PlayerData.lastPlayedDate |
| Settings changed | AppSettings, ParentSettings |
| App background | All unsaved changes |

### Load Points

| Screen | What Gets Loaded |
|--------|------------------|
| App Launch | AppSettings, last active PlayerData |
| Player Selection | All PlayerData records |
| Home Screen | Current player's coins, progress |
| Activity Screen | ActivityProgress for specific activity |
| Treasure Screen | Coins, approved videos |
| Parent Dashboard | ParentSettings, all PlayerData stats |

---

## Storage Implementation

### SwiftData Usage

```swift
// In BennieGameApp.swift
@main
struct BennieGameApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: [
            PlayerData.self,
            AppSettings.self
        ])
    }
}

// In any View
@Environment(\.modelContext) private var modelContext
@Query private var players: [PlayerData]
@Query private var settings: [AppSettings]

// Save
modelContext.insert(newPlayer)
try? modelContext.save()

// Update
player.coins += 1
try? modelContext.save()
```

### UserDefaults Usage

For lightweight, frequently accessed data:

```swift
extension UserDefaults {
    // Quick access keys
    private enum Keys {
        static let lastActivePlayerId = "lastActivePlayerId"
        static let audioEnabled = "audioEnabled"
        static let musicVolume = "musicVolume"
    }
    
    var lastActivePlayerId: String? {
        get { string(forKey: Keys.lastActivePlayerId) }
        set { set(newValue, forKey: Keys.lastActivePlayerId) }
    }
    
    var audioEnabled: Bool {
        get { bool(forKey: Keys.audioEnabled) }
        set { set(newValue, forKey: Keys.audioEnabled) }
    }
}
```

---

## Migration Strategy

See `migration_strategy.md` for version upgrade handling.

---

## Testing Data Models

```swift
// Test fixtures
extension PlayerData {
    static var preview: PlayerData {
        let player = PlayerData(id: "alexander", name: "Alexander")
        player.coins = 12
        player.totalCoinsEarned = 47
        return player
    }
}

// Usage in previews
struct HomeView_Previews: PreviewProvider {
    static var previews: some View {
        HomeView(player: .preview)
            .modelContainer(for: PlayerData.self, inMemory: true)
    }
}
```

---

*Complete specification for all game data models*
