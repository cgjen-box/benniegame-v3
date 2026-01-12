# Phase 12: Adaptive Difficulty System

## Overview

AI-powered learning profile system that tracks each child's engagement patterns and optimizes difficulty in real-time. Makes activities feel "just right" - not too easy, not too hard.

## Playbook References

**Primary Source**: `docs/playbook/FULL_ARCHIVE.md`
- **Section 0.5**: Adaptive Difficulty System (complete specification)
- **Section 4.4**: Grid Progression table (Puzzle Matching)
- **Section 4.5**: Labyrinth difficulty parameters
- **Section 4.6**: Zahlen number range progression

## Goals

1. **Automatic Difficulty Adjustment**: Game adapts to each player's skill level
2. **Engagement Optimization**: Keep children in "flow state" (challenging but achievable)
3. **Per-Player Profiles**: Alexander and Oliver have separate learning profiles
4. **Real-time Adaptation**: Difficulty adjusts within same play session
5. **Prevent Frustration**: Detect struggling early and offer help

## Key Metrics Tracked

From Playbook Section 0.5:

```swift
struct LearningProfile {
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

## Difficulty Adjustment Rules

| Signal | Interpretation | Adjustment |
|--------|---------------|------------|
| Solve time < 10s | Too easy | Increase difficulty |
| Solve time > 60s | Struggling | Decrease difficulty |
| 3+ mistakes per level | Too hard | Decrease difficulty, offer hints |
| Quit mid-activity | Frustration | Major decrease, encouraging message |
| Fast successive completions | Engaged & capable | Gradually increase |
| Long pause (>30s) | Confused or distracted | Offer gentle hint |

## Activity-Specific Difficulty Curves

### Puzzle Matching (Rätsel)

**Grid Progression** (from Playbook Section 4.4):

| Level Range | Grid Size | Colors | Filled Cells |
|-------------|-----------|--------|--------------|
| 1-5 | 3×3 | 2 (green, yellow) | 2-4 |
| 6-10 | 3×3 | 3 (add gray) | 3-5 |
| 11-20 | 4×4 | 3 colors | 4-7 |
| 21-30 | 5×5 | 3-4 colors | 5-10 |
| 31+ | 6×6 | 4 colors | 6-12 |

### Labyrinth (Rätsel)

**Path Complexity**:
- Easy: 5-8 decision points, wide paths (60pt)
- Medium: 9-12 decision points, standard paths (44pt)
- Hard: 13-16 decision points, narrow paths (36pt)

### Zahlen (Numbers)

**Number Range**:
- Easy: 1-5
- Medium: 1-7
- Hard: 1-10

## Implementation Files

1. **DATA_MODEL.md** - LearningProfile structure and persistence
2. **DIFFICULTY_RULES.md** - Adjustment logic and thresholds
3. **ACTIVITY_CONFIGS.md** - Per-activity difficulty parameters
4. **IMPLEMENTATION.md** - SwiftUI integration
5. **TESTING.md** - Test scenarios and validation

## Design References

No specific UI assets needed - this is a backend system. However, it affects:
- **Hint System**: Referenced in `design/references/components/speech-bubble.png`
- **Celebration Timing**: Referenced in `design/references/screens/Reference_Celebration_Overlay.png`

## Success Criteria

- [ ] Per-player profiles persist between sessions
- [ ] Difficulty adjusts within 3 completed levels
- [ ] Struggling children (3+ mistakes) receive hints within 10s
- [ ] Fast children advance to harder levels smoothly
- [ ] Quit rate decreases by 50% compared to fixed difficulty
- [ ] Average solve time stays between 15-45 seconds

## Dependencies

- **Phase 4**: Player Data Store (for profile persistence)
- **Phase 7**: Activity Screens (for metrics collection)
- **Phase 8**: Progress System (for level tracking)
- **Phase 11**: Voice System (for hint delivery)

## Related Documents

- `plan/04_player_data/DATA_MODEL.md` - PlayerData structure
- `plan/07_activities/METRICS.md` - Activity performance tracking
- `plan/11_voice_system/HINT_TRIGGERS.md` - When to deliver hints
