# Data Model: Learning Profile System

## Overview

Complete data structures for tracking player performance and adapting difficulty.

## Playbook Reference

**Source**: `docs/playbook/FULL_ARCHIVE.md`, Section 0.5

## Core Data Structures

### LearningProfile

```swift
struct LearningProfile: Codable {
    // MARK: - Performance Metrics
    
    /// Average time to complete a level (in seconds)
    var averageSolveTime: TimeInterval = 30.0
    
    /// Mistakes per level (taps on wrong answers)
    var mistakeFrequency: Double = 0.5
    
    /// Percentage of levels quit before completion
    var quitRate: Double = 0.0
    
    /// Average session duration (in seconds)
    var sessionDuration: TimeInterval = 300.0
    
    // MARK: - Engagement Indicators
    
    /// How often hints are used (0.0 = never, 1.0 = every level)
    var hintUsageRate: Double = 0.0
    
    /// Did player tap "Weiter" quickly after celebration? (engagement signal)
    var celebrationEngagement: Bool = true
    
    /// Activity preference counts (higher = more played)
    var preferredActivities: [ActivityType: Int] = [:]
    
    // MARK: - Adaptive Parameters
    
    /// Current difficulty level (0.0 = easiest, 1.0 = hardest)
    var difficultyLevel: Float = 0.3
    
    /// Preferred grid size for puzzles (3, 4, 5, or 6)
    var gridSizePreference: Int = 3
    
    /// Number of colors in puzzles (2-4)
    var colorCount: Int = 2
    
    /// Current number range for Zahlen (5, 7, or 10)
    var numberRange: Int = 5
    
    /// Labyrinth path complexity (decision points: 5-16)
    var labyrinthComplexity: Int = 5
    
    // MARK: - Historical Data
    
    /// Last 10 solve times (for trending)
    var recentSolveTimes: [TimeInterval] = []
    
    /// Last 10 mistake counts
    var recentMistakes: [Int] = []
    
    /// Total levels completed
    var totalLevelsCompleted: Int = 0
    
    /// Total levels quit
    var totalLevelsQuit: Int = 0
    
    /// Last updated timestamp
    var lastUpdated: Date = Date()
}
```

### ActivityMetrics

Used to track performance during a single level:

```swift
struct ActivityMetrics: Codable {
    let activityType: ActivityType
    let startTime: Date
    var endTime: Date?
    
    /// Time spent on this level (in seconds)
    var duration: TimeInterval {
        guard let end = endTime else { return 0 }
        return end.timeIntervalSince(startTime)
    }
    
    /// Number of incorrect taps/attempts
    var mistakes: Int = 0
    
    /// Did player quit before completing?
    var didQuit: Bool = false
    
    /// Did player use hint?
    var usedHint: Bool = false
    
    /// Number of long pauses (>30s of inactivity)
    var longPauses: Int = 0
    
    /// Current difficulty parameters
    var difficulty: DifficultyParameters
}
```

### DifficultyParameters

Activity-specific difficulty settings:

```swift
struct DifficultyParameters: Codable {
    // MARK: - Puzzle Matching
    var gridSize: Int = 3
    var colorCount: Int = 2
    var filledCells: Int = 2
    
    // MARK: - Labyrinth
    var decisionPoints: Int = 5
    var pathWidth: CGFloat = 60
    
    // MARK: - Zahlen
    var numberRange: Int = 5  // 1-5, 1-7, or 1-10
    
    // MARK: - Universal
    var hintDelay: TimeInterval = 10.0  // Seconds before first hint
}
```

## Integration with PlayerData

The `LearningProfile` is stored as part of each player's data:

```swift
struct PlayerData: Codable {
    var id: String
    var coins: Int
    var totalCoinsEarned: Int
    var activityProgress: [String: Int]
    var lastPlayedDate: Date
    var totalPlayTimeToday: TimeInterval
    var videosWatched: [VideoRecord]
    
    // ADDED: Learning profile for adaptive difficulty
    var learningProfile: LearningProfile = LearningProfile()
}
```

## Persistence

### File Location

```
/Users/[username]/Library/Application Support/BennieGame/
├── alexander_learning_profile.json
└── oliver_learning_profile.json
```

### Save Trigger Events

Profile is updated and saved after:
1. **Level completion** - Update all metrics
2. **Level quit** - Update quit rate, show as struggling
3. **Hint used** - Update hint usage rate
4. **Session end** - Update session duration

### Example JSON

```json
{
  "averageSolveTime": 25.5,
  "mistakeFrequency": 0.3,
  "quitRate": 0.05,
  "sessionDuration": 450.0,
  "hintUsageRate": 0.1,
  "celebrationEngagement": true,
  "preferredActivities": {
    "raetsel": 15,
    "zahlen": 12
  },
  "difficultyLevel": 0.45,
  "gridSizePreference": 4,
  "colorCount": 3,
  "numberRange": 7,
  "labyrinthComplexity": 9,
  "recentSolveTimes": [22.0, 28.0, 25.0, 30.0, 18.0],
  "recentMistakes": [1, 0, 2, 1, 0],
  "totalLevelsCompleted": 47,
  "totalLevelsQuit": 2,
  "lastUpdated": "2026-01-11T14:30:00Z"
}
```

## Data Collection Points

### During Gameplay

```swift
class ActivityViewModel: ObservableObject {
    @Published var currentMetrics = ActivityMetrics(...)
    
    func recordMistake() {
        currentMetrics.mistakes += 1
    }
    
    func recordHintUsed() {
        currentMetrics.usedHint = true
    }
    
    func recordLongPause() {
        currentMetrics.longPauses += 1
    }
    
    func completeLevel() {
        currentMetrics.endTime = Date()
        updateLearningProfile(with: currentMetrics)
    }
}
```

### Profile Update Logic

```swift
extension LearningProfile {
    mutating func update(with metrics: ActivityMetrics) {
        // Update rolling averages
        recentSolveTimes.append(metrics.duration)
        if recentSolveTimes.count > 10 {
            recentSolveTimes.removeFirst()
        }
        averageSolveTime = recentSolveTimes.reduce(0, +) / Double(recentSolveTimes.count)
        
        // Update mistake tracking
        recentMistakes.append(metrics.mistakes)
        if recentMistakes.count > 10 {
            recentMistakes.removeFirst()
        }
        mistakeFrequency = Double(recentMistakes.reduce(0, +)) / Double(recentMistakes.count)
        
        // Update quit rate
        if metrics.didQuit {
            totalLevelsQuit += 1
        } else {
            totalLevelsCompleted += 1
        }
        quitRate = Double(totalLevelsQuit) / Double(totalLevelsCompleted + totalLevelsQuit)
        
        // Update hint usage
        if metrics.usedHint {
            hintUsageRate = (hintUsageRate * 0.9) + 0.1  // Weighted average
        }
        
        lastUpdated = Date()
    }
}
```

## Privacy & Data Safety

- All data stored locally only (no cloud sync)
- No personally identifiable information collected
- Parents can reset profiles via Parent Dashboard
- Data automatically deleted if player is removed

## Testing Data

For development/testing, provide realistic test profiles:

```swift
extension LearningProfile {
    static var alexanderTest: LearningProfile {
        var profile = LearningProfile()
        profile.averageSolveTime = 35.0
        profile.mistakeFrequency = 0.8
        profile.difficultyLevel = 0.25
        profile.gridSizePreference = 3
        profile.colorCount = 2
        return profile
    }
    
    static var oliverTest: LearningProfile {
        var profile = LearningProfile()
        profile.averageSolveTime = 28.0
        profile.mistakeFrequency = 0.4
        profile.difficultyLevel = 0.4
        profile.gridSizePreference = 4
        profile.colorCount = 3
        return profile
    }
}
```
