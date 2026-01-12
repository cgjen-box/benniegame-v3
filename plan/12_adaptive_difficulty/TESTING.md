# Testing Guide: Adaptive Difficulty System

## Overview

Comprehensive test scenarios to validate difficulty adaptation behavior.

## Test Environment Setup

### Test Profiles

Create these test player profiles for consistent testing:

```swift
struct TestProfiles {
    static let struggling = LearningProfile(
        averageSolveTime: 75.0,
        mistakeFrequency: 3.5,
        quitRate: 0.15,
        difficultyLevel: 0.2
    )
    
    static let fastLearner = LearningProfile(
        averageSolveTime: 12.0,
        mistakeFrequency: 0.3,
        quitRate: 0.0,
        difficultyLevel: 0.8
    )
    
    static let inconsistent = LearningProfile(
        averageSolveTime: 35.0,
        mistakeFrequency: 1.5,
        quitRate: 0.05,
        difficultyLevel: 0.5
    )
    
    static let newPlayer = LearningProfile()  // Default values
}
```

---

## Test Scenarios

### Scenario 1: Struggling Child

**Profile**: High mistake rate, slow solve times

**Expected Behavior**:
1. Difficulty decreases after 3+ mistakes
2. Hints trigger after 10s inactivity
3. Puzzle grid stays at 3×3
4. Encouraging messages on quit

**Test Steps**:

```swift
func testStrugglingChild() {
    // Setup
    let manager = DifficultyManager.shared
    manager.currentProfile = TestProfiles.struggling
    
    // Simulate level with many mistakes
    var metrics = ActivityMetrics(activityType: .raetsel, startTime: Date())
    metrics.mistakes = 5
    metrics.duration = 80.0
    metrics.endTime = Date()
    
    // Act
    manager.adjustDifficulty(based: metrics)
    
    // Assert
    XCTAssertLessThan(manager.currentProfile.difficultyLevel, 0.2,
                     "Difficulty should decrease for struggling child")
    
    XCTAssertEqual(manager.getPuzzleConfig().gridSize, 3,
                  "Grid should stay small for struggling child")
}
```

**Manual Test**:
1. Set difficulty to 0.2 in debug menu
2. Play Puzzle Matching
3. Make 5+ mistakes intentionally
4. Complete level slowly (70+ seconds)
5. Verify next level is easier (same grid size or fewer colors)

---

### Scenario 2: Fast Learner

**Profile**: Low mistakes, fast completion

**Expected Behavior**:
1. Difficulty increases rapidly
2. Grid size increases after 3 fast completions
3. No hints needed
4. Advanced to harder number ranges

**Test Steps**:

```swift
func testFastLearner() {
    // Setup
    let manager = DifficultyManager.shared
    manager.currentProfile = TestProfiles.fastLearner
    
    // Simulate 3 fast completions
    for _ in 0..<3 {
        var metrics = ActivityMetrics(activityType: .raetsel, startTime: Date())
        metrics.mistakes = 0
        metrics.duration = 8.0
        metrics.endTime = Date()
        
        manager.adjustDifficulty(based: metrics)
    }
    
    // Assert
    XCTAssertGreaterThan(manager.currentProfile.difficultyLevel, 0.85,
                        "Difficulty should increase significantly")
    
    XCTAssertGreaterThanOrEqual(manager.getPuzzleConfig().gridSize, 5,
                               "Grid should be large for fast learner")
}
```

**Manual Test**:
1. Set difficulty to 0.7 in debug menu
2. Complete 3 puzzles in < 10 seconds each with 0 mistakes
3. Verify 4th puzzle has larger grid or more colors

---

### Scenario 3: Quit Behavior

**Profile**: Normal performance but quits mid-level

**Expected Behavior**:
1. Major difficulty decrease (0.3)
2. Encouraging message plays
3. Next level is significantly easier

**Test Steps**:

```swift
func testQuitBehavior() {
    // Setup
    let manager = DifficultyManager.shared
    manager.currentProfile.difficultyLevel = 0.5
    
    // Simulate quit
    var metrics = ActivityMetrics(activityType: .raetsel, startTime: Date())
    metrics.didQuit = true
    metrics.mistakes = 2
    metrics.duration = 45.0
    metrics.endTime = Date()
    
    // Act
    manager.adjustDifficulty(based: metrics)
    
    // Assert
    XCTAssertLessThanOrEqual(manager.currentProfile.difficultyLevel, 0.25,
                           "Difficulty should drop significantly after quit")
}
```

**Manual Test**:
1. Start any activity at medium difficulty
2. Tap Home button mid-level (quit)
3. Verify Bennie plays encouraging message
4. Start same activity again
5. Verify next level is noticeably easier

---

### Scenario 4: Hint Triggering

**Profile**: Normal performance, occasional pauses

**Expected Behavior**:
1. No hint before 10s inactivity
2. Gentle hint at 10s
3. Specific hint at 20s
4. Very specific hint at 30s

**Test Steps**:

```swift
func testHintProgression() {
    let viewModel = PuzzleMatchingViewModel()
    
    // Simulate inactivity
    let expectations = [
        (duration: 5.0, expected: HintLevel.none),
        (duration: 10.0, expected: HintLevel.gentle),
        (duration: 20.0, expected: HintLevel.specific),
        (duration: 30.0, expected: HintLevel.verySpecific)
    ]
    
    for (duration, expectedHint) in expectations {
        viewModel.lastInteractionTime = Date().addingTimeInterval(-duration)
        let hintLevel = viewModel.difficultyManager.shouldTriggerHint(
            inactivityDuration: duration,
            currentMistakes: 1
        )
        
        XCTAssertEqual(hintLevel, expectedHint,
                      "Hint level mismatch at \(duration)s")
    }
}
```

**Manual Test**:
1. Start puzzle activity
2. Don't tap anything for 35 seconds
3. Listen for hint progression:
   - 10s: "Du schaffst das!"
   - 20s: "Welche Farbe fehlt noch?"
   - 30s: Bennie points at specific cell

---

### Scenario 5: Returning Player (Grace Period)

**Profile**: Normal performance, 10 days since last play

**Expected Behavior**:
1. No difficulty decrease for first 3 levels
2. Allow slower performance without penalty
3. Resume normal adjustment after grace period

**Test Steps**:

```swift
func testGracePeriod() {
    let manager = DifficultyManager.shared
    manager.currentProfile.difficultyLevel = 0.6
    manager.currentProfile.lastUpdated = Date().addingTimeInterval(-10 * 24 * 60 * 60)
    
    // Simulate slower performance (should be forgiven)
    var metrics = ActivityMetrics(activityType: .raetsel, startTime: Date())
    metrics.mistakes = 2
    metrics.duration = 55.0
    metrics.endTime = Date()
    
    // Act
    manager.adjustDifficulty(based: metrics)
    
    // Assert
    XCTAssertGreaterThanOrEqual(manager.currentProfile.difficultyLevel, 0.55,
                               "Should not decrease significantly during grace period")
}
```

---

### Scenario 6: Inconsistent Performance

**Profile**: Alternates between fast and slow

**Expected Behavior**:
1. Difficulty stabilizes at medium level
2. Doesn't swing wildly
3. Responds to overall trend, not single outliers

**Test Steps**:

```swift
func testInconsistentPerformance() {
    let manager = DifficultyManager.shared
    manager.currentProfile.difficultyLevel = 0.5
    
    // Simulate alternating performance
    let performances: [(mistakes: Int, duration: TimeInterval)] = [
        (0, 15.0),   // Fast
        (3, 70.0),   // Slow
        (1, 20.0),   // Fast
        (4, 80.0),   // Slow
        (0, 18.0)    // Fast
    ]
    
    for (mistakes, duration) in performances {
        var metrics = ActivityMetrics(activityType: .raetsel, startTime: Date())
        metrics.mistakes = mistakes
        metrics.duration = duration
        metrics.endTime = Date()
        
        manager.adjustDifficulty(based: metrics)
    }
    
    // Assert
    XCTAssertTrue((0.4...0.6).contains(manager.currentProfile.difficultyLevel),
                 "Difficulty should stabilize in middle range for inconsistent performance")
}
```

---

### Scenario 7: Activity-Specific Parameters

**Test**: Verify each activity uses correct difficulty mapping

```swift
func testActivitySpecificConfigs() {
    let manager = DifficultyManager.shared
    
    // Test at difficulty 0.3
    manager.currentProfile.difficultyLevel = 0.3
    
    // Puzzle should be 3×3 with 3 colors
    let puzzleConfig = manager.getPuzzleConfig()
    XCTAssertEqual(puzzleConfig.gridSize, 3)
    XCTAssertEqual(puzzleConfig.availableColors.count, 3)
    
    // Labyrinth should have 5-8 decision points
    let labyrinthConfig = manager.getLabyrinthConfig()
    XCTAssertTrue((5...8).contains(labyrinthConfig.decisionPoints))
    
    // Zahlen should use 1-5 range
    let zahlenConfig = manager.getWuerfelConfig()
    XCTAssertEqual(zahlenConfig.numberRange, 1...5)
}
```

---

## Integration Tests

### Test 1: Full Play Session

**Simulate**: Alexander plays for 15 minutes

```swift
func testFullPlaySession() {
    let manager = DifficultyManager.shared
    manager.currentProfile = TestProfiles.newPlayer
    
    // Simulate 10 levels with mixed performance
    let sessionResults: [(mistakes: Int, duration: TimeInterval)] = [
        (2, 45.0),  // Level 1: Comfortable
        (1, 35.0),  // Level 2: Good
        (0, 28.0),  // Level 3: Fast
        (0, 25.0),  // Level 4: Fast
        (0, 22.0),  // Level 5: Very fast - expect difficulty increase
        (3, 60.0),  // Level 6: Struggling with increased difficulty
        (2, 55.0),  // Level 7: Still challenging
        (1, 40.0),  // Level 8: Adapting
        (1, 35.0),  // Level 9: Comfortable again
        (0, 30.0)   // Level 10: Good
    ]
    
    for (mistakes, duration) in sessionResults {
        var metrics = ActivityMetrics(activityType: .raetsel, startTime: Date())
        metrics.mistakes = mistakes
        metrics.duration = duration
        metrics.endTime = Date()
        
        manager.adjustDifficulty(based: metrics)
    }
    
    // Assert final state
    XCTAssertTrue((0.4...0.6).contains(manager.currentProfile.difficultyLevel),
                 "Should settle in comfortable range")
}
```

---

## Performance Tests

### Test: Profile Save Performance

```swift
func testProfileSavePerformance() {
    measure {
        for _ in 0..<100 {
            PlayerDataStore.shared.savePlayers()
        }
    }
    // Should complete in < 1 second for 100 saves
}
```

### Test: Difficulty Calculation Performance

```swift
func testDifficultyCalculationPerformance() {
    let manager = DifficultyManager.shared
    var metrics = ActivityMetrics(activityType: .raetsel, startTime: Date())
    metrics.mistakes = 2
    metrics.duration = 30.0
    metrics.endTime = Date()
    
    measure {
        for _ in 0..<1000 {
            manager.adjustDifficulty(based: metrics)
        }
    }
    // Should complete in < 0.1 seconds for 1000 calculations
}
```

---

## Manual QA Checklist

### Pre-Release Testing

- [ ] **New Player Journey**
  - [ ] Starts at difficulty 0.3
  - [ ] First 5 levels feel appropriately challenging
  - [ ] Receives hints when needed
  - [ ] Difficulty adjusts smoothly upward if doing well

- [ ] **Struggling Player Support**
  - [ ] Hints trigger at correct intervals (10s, 20s, 30s)
  - [ ] Difficulty decreases after multiple mistakes
  - [ ] Encouraging messages play on quit
  - [ ] Never gets "stuck" at impossible difficulty

- [ ] **Advanced Player Challenge**
  - [ ] Difficulty increases for fast completions
  - [ ] Reaches maximum difficulty (0.9) for experts
  - [ ] 6×6 grid with 4 colors appears for top performers
  - [ ] Stays challenging without becoming frustrating

- [ ] **Profile Persistence**
  - [ ] Learning profile saves after each level
  - [ ] Profile loads correctly on app restart
  - [ ] Switching players loads correct profile
  - [ ] Parent can reset profile in dashboard

- [ ] **Edge Cases**
  - [ ] Handles very fast completion (< 5s)
  - [ ] Handles very slow completion (> 120s)
  - [ ] Handles repeated quits gracefully
  - [ ] Grace period works for returning players

---

## Automated Test Suite

Run all tests with:

```swift
class AdaptiveDifficultyTests: XCTestCase {
    func testAll() {
        testStrugglingChild()
        testFastLearner()
        testQuitBehavior()
        testHintProgression()
        testGracePeriod()
        testInconsistentPerformance()
        testActivitySpecificConfigs()
        testFullPlaySession()
    }
}
```

---

## Success Metrics

After deployment, track these metrics to validate system:

| Metric | Target | Measurement |
|--------|--------|-------------|
| Average solve time | 20-40 seconds | Should stabilize in this range |
| Quit rate | < 5% | Significantly lower than fixed difficulty |
| Hint usage | 10-20% | Most children self-sufficient |
| Difficulty spread | 0.2-0.8 | Children should reach varied levels |
| Session duration | 15+ minutes | Engaged, not frustrated |

---

## Debug Tools

### Difficulty Inspector

```swift
#if DEBUG
struct DifficultyInspectorView: View {
    @ObservedObject var manager = DifficultyManager.shared
    
    var body: some View {
        VStack(alignment: .leading) {
            Text("Current Difficulty: \(manager.currentProfile.difficultyLevel)")
            Text("Avg Solve Time: \(manager.currentProfile.averageSolveTime)s")
            Text("Mistakes/Level: \(manager.currentProfile.mistakeFrequency)")
            Text("Quit Rate: \(manager.currentProfile.quitRate * 100)%")
            
            Button("Reset to Beginner") {
                manager.currentProfile.difficultyLevel = 0.2
            }
            
            Button("Set to Expert") {
                manager.currentProfile.difficultyLevel = 0.85
            }
            
            Button("Simulate Struggle") {
                manager.simulateStrugglingChild()
            }
            
            Button("Simulate Fast Learner") {
                manager.simulateFastLearner()
            }
        }
    }
}
#endif
```

### Test Mode Toggle

Add to Settings screen:

```swift
#if DEBUG
Toggle("Test Mode: Fixed Difficulty", isOn: $useFixedDifficulty)
if useFixedDifficulty {
    Slider(value: $testDifficulty, in: 0.1...0.9)
    Text("Test Difficulty: \(testDifficulty)")
}
#endif
```
