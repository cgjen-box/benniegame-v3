# Difficulty Adjustment Rules

## Overview

Logic for real-time difficulty adaptation based on player performance signals.

## Playbook Reference

**Source**: `docs/playbook/FULL_ARCHIVE.md`, Section 0.5
- Difficulty Adjustment Rules table

## Adjustment Thresholds

### Performance Signals

| Signal | Threshold | Interpretation | Action |
|--------|-----------|----------------|--------|
| **Solve Time** | < 10 seconds | Too easy | Increase difficulty by 0.1 |
| **Solve Time** | 10-45 seconds | Perfect | No change (sweet spot) |
| **Solve Time** | 45-60 seconds | Challenging | Monitor next level |
| **Solve Time** | > 60 seconds | Struggling | Decrease difficulty by 0.1 |
| **Mistakes** | 0-1 per level | Comfortable | Slight increase (0.05) |
| **Mistakes** | 2 per level | Appropriately challenging | No change |
| **Mistakes** | 3+ per level | Too hard | Decrease by 0.15, trigger hint |
| **Quit Rate** | 0% | Engaged | Continue current difficulty |
| **Quit Rate** | 1-10% | Normal exploration | No panic |
| **Quit Rate** | > 10% | Frustration | Major decrease (0.3) |
| **Long Pause** | > 30 seconds | Confused/distracted | Trigger gentle hint |
| **Successive Completions** | 3+ with 0-1 mistakes | Too easy | Increase by 0.15 |

### Difficulty Level Bounds

```swift
let minimumDifficulty: Float = 0.1  // Never go below this
let maximumDifficulty: Float = 0.9  // Never go above this
let startingDifficulty: Float = 0.3 // New players start here
```

## Adjustment Logic

### Primary Algorithm

```swift
func adjustDifficulty(profile: inout LearningProfile, metrics: ActivityMetrics) {
    var adjustment: Float = 0.0
    
    // 1. Solve Time Analysis
    if metrics.duration < 10 {
        adjustment += 0.1  // Too easy
    } else if metrics.duration > 60 {
        adjustment -= 0.1  // Too hard
    }
    
    // 2. Mistake Analysis
    if metrics.mistakes == 0 || metrics.mistakes == 1 {
        adjustment += 0.05  // Slightly increase
    } else if metrics.mistakes >= 3 {
        adjustment -= 0.15  // Significantly decrease
        triggerHintForNextLevel = true
    }
    
    // 3. Long Pause Penalty
    if metrics.longPauses > 0 {
        adjustment -= 0.05 * Float(metrics.longPauses)
    }
    
    // 4. Successive Success Bonus
    if hasThreeSuccessiveSuccesses(profile) {
        adjustment += 0.15
    }
    
    // 5. Quit Penalty
    if metrics.didQuit {
        adjustment -= 0.3  // Major decrease
        showEncouragingMessage = true
    }
    
    // Apply adjustment with bounds checking
    profile.difficultyLevel = clamp(
        profile.difficultyLevel + adjustment,
        min: minimumDifficulty,
        max: maximumDifficulty
    )
}

func hasThreeSuccessiveSuccesses(_ profile: LearningProfile) -> Bool {
    guard profile.recentMistakes.count >= 3 else { return false }
    let lastThree = profile.recentMistakes.suffix(3)
    return lastThree.allSatisfy { $0 <= 1 }
}
```

## Activity-Specific Mappings

### Puzzle Matching: Difficulty → Grid Parameters

```swift
func getPuzzleParameters(difficulty: Float) -> PuzzleParameters {
    switch difficulty {
    case 0.0..<0.3:
        return PuzzleParameters(
            gridSize: 3,
            colorCount: 2,
            filledCells: Int.random(in: 2...3)
        )
    case 0.3..<0.5:
        return PuzzleParameters(
            gridSize: 3,
            colorCount: 3,
            filledCells: Int.random(in: 3...5)
        )
    case 0.5..<0.7:
        return PuzzleParameters(
            gridSize: 4,
            colorCount: 3,
            filledCells: Int.random(in: 4...7)
        )
    case 0.7..<0.85:
        return PuzzleParameters(
            gridSize: 5,
            colorCount: 3,
            filledCells: Int.random(in: 5...10)
        )
    default:  // 0.85-1.0
        return PuzzleParameters(
            gridSize: 6,
            colorCount: 4,
            filledCells: Int.random(in: 6...12)
        )
    }
}
```

### Labyrinth: Difficulty → Path Complexity

```swift
func getLabyrinthParameters(difficulty: Float) -> LabyrinthParameters {
    let decisionPoints = Int(5 + (difficulty * 11))  // 5-16 decision points
    let pathWidth: CGFloat
    
    switch difficulty {
    case 0.0..<0.4:
        pathWidth = 60  // Wide paths for beginners
    case 0.4..<0.7:
        pathWidth = 44  // Standard paths
    default:
        pathWidth = 36  // Narrow paths for experts
    }
    
    return LabyrinthParameters(
        decisionPoints: decisionPoints,
        pathWidth: pathWidth
    )
}
```

### Zahlen: Difficulty → Number Range

```swift
func getZahlenParameters(difficulty: Float) -> ZahlenParameters {
    let numberRange: Int
    
    switch difficulty {
    case 0.0..<0.4:
        numberRange = 5  // 1-5
    case 0.4..<0.7:
        numberRange = 7  // 1-7
    default:
        numberRange = 10  // 1-10
    }
    
    return ZahlenParameters(numberRange: numberRange)
}
```

## Hint Timing Logic

### When to Trigger Hints

```swift
func shouldTriggerHint(
    profile: LearningProfile,
    currentInactivityDuration: TimeInterval,
    currentMistakes: Int
) -> Bool {
    // Condition 1: Long inactivity
    if currentInactivityDuration > 30 {
        return true
    }
    
    // Condition 2: Multiple mistakes
    if currentMistakes >= 3 {
        return true
    }
    
    // Condition 3: Struggling pattern
    if profile.mistakeFrequency > 1.5 {
        return true
    }
    
    return false
}
```

### Hint Escalation

First hint: After 10 seconds of inactivity
Second hint: After 20 seconds (more specific)
Third hint: After 30 seconds (very specific)

```swift
func getHintLevel(inactivityDuration: TimeInterval) -> HintLevel {
    switch inactivityDuration {
    case 0..<10:
        return .none
    case 10..<20:
        return .gentle     // "Du schaffst das!"
    case 20..<30:
        return .specific   // "Welche Farbe fehlt noch?"
    default:
        return .verySpecific  // "Schau mal hier!" + pointing animation
    }
}
```

## Encouraging Messages

### After Quit Event

```swift
let encouragingMessages = [
    "Das war schwer! Lass uns etwas Einfacheres probieren.",
    "Kein Problem! Wir versuchen etwas Leichteres.",
    "Das schaffen wir beim nÃ¤chsten Mal!"
]

func playEncouragingMessage() {
    let message = encouragingMessages.randomElement()!
    playBennieVoice(message)
}
```

## Adjustment Frequency

### Rate Limiting

Do NOT adjust after every single level. Instead:

```swift
struct AdjustmentSchedule {
    static let minimumLevelsBetweenAdjustments = 3
    static let minimumTimeBetweenAdjustments: TimeInterval = 60  // 1 minute
}

func shouldAdjustNow(profile: LearningProfile) -> Bool {
    let levelsSinceLastAdjustment = profile.totalLevelsCompleted % 3
    let timeSinceLastAdjustment = Date().timeIntervalSince(profile.lastUpdated)
    
    return levelsSinceLastAdjustment == 0 && 
           timeSinceLastAdjustment >= AdjustmentSchedule.minimumTimeBetweenAdjustments
}
```

This prevents jarring difficulty swings and gives children time to adapt.

## Edge Cases

### Very Fast Learners

If a child consistently completes levels in < 5 seconds with 0 mistakes:

```swift
if metrics.duration < 5 && metrics.mistakes == 0 {
    // They might be pattern-recognizing without learning
    // Skip one difficulty level
    profile.difficultyLevel += 0.2
}
```

### Regression After Break

If a child returns after 7+ days, don't punish them for slower performance:

```swift
let daysSinceLastPlay = Calendar.current.dateComponents(
    [.day], 
    from: profile.lastUpdated, 
    to: Date()
).day ?? 0

if daysSinceLastPlay >= 7 {
    // Grace period: don't decrease difficulty for first 3 levels
    isInGracePeriod = true
}
```

## Testing Scenarios

See `TESTING.md` for complete test scenarios including:
- Struggling child (high mistake rate)
- Fast learner (rapid completion)
- Inconsistent performer (variable results)
- Returning after break
- Quit-prone behavior
