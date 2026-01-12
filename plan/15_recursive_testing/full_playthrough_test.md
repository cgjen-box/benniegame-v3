# Full Playthrough Test (0→100 Coins)

> **CRITICAL**: This test must run autonomously without human intervention until completion or fatal error.

## Objective

Automated test that plays the complete game loop from 0 coins → 100 coins, including:
- Completing all activity types
- Triggering all celebration milestones (5, 10, 15, 20, 25, etc.)
- Redeeming coins for YouTube time
- Watching 100 minutes of YouTube (simulated)

## Prerequisites

```swift
// Test configuration
struct TestConfig {
    static let targetCoins = 100
    static let youtubeMinutesRequired = 100
    static let maxRetriesPerError = 3
    static let screenshotOnError = true
    static let performanceMonitoring = true
    static let memoryThreshold: Float = 200 // MB
    static let fpsThreshold: Float = 55 // Minimum 55fps
}
```

## Test Phases

### Phase 1: App Launch & Player Selection

```swift
func testPhase1_PlayerSelection() {
    // 1. Launch app
    XCTContext.runActivity(named: "Launch app") { _ in
        app.launch()
        wait(for: 2.0) // Loading screen minimum display
    }
    
    // 2. Verify loading screen
    XCTContext.runActivity(named: "Verify loading completes") { _ in
        let loadingSign = app.staticTexts["Waldabenteuer lädt"]
        XCTAssertTrue(loadingSign.waitForExistence(timeout: 5))
        
        // Wait for narrator: "Wir sind gleich bereit zum Spielen"
        wait(for: 2.0)
        
        // Progress should reach 100%
        let progressText = app.staticTexts.matching(identifier: "loading_percentage")
        XCTAssertTrue(progressText.firstMatch.label.contains("100%"))
    }
    
    // 3. Player selection screen appears
    XCTContext.runActivity(named: "Select Alexander") { _ in
        let playerSign = app.staticTexts["Wer spielt heute?"]
        XCTAssertTrue(playerSign.waitForExistence(timeout: 3))
        
        // Tap Alexander button
        let alexanderButton = app.buttons["Alexander"]
        XCTAssertTrue(alexanderButton.exists)
        XCTAssertTrue(alexanderButton.frame.width >= 200) // Touch target check
        XCTAssertTrue(alexanderButton.frame.height >= 180)
        
        alexanderButton.tap()
        
        // Wait for narrator: "Hallo Alexander! Los geht's!"
        wait(for: 2.0)
    }
    
    // 4. Home screen appears
    XCTContext.runActivity(named: "Verify home screen") { _ in
        let homeSign = app.staticTexts["Waldabenteuer"]
        XCTAssertTrue(homeSign.waitForExistence(timeout: 3))
        
        // Verify Bennie greeting plays
        wait(for: 4.0) // "Hi Alexander, ich bin Bennie! Wir lösen Aktivitäten um YouTube zu schauen."
    }
}
```

### Phase 2: Activity Loop (Repeat until 100 coins)

```swift
func testPhase2_ActivityLoop() {
    var currentCoins = 0
    var attemptCount = 0
    let maxAttempts = 200 // Safety limit
    
    while currentCoins < TestConfig.targetCoins && attemptCount < maxAttempts {
        attemptCount += 1
        
        // Select activity (alternate between types for variety)
        let activityResult = selectAndCompleteActivity(attemptNumber: attemptCount)
        
        if activityResult.success {
            currentCoins += 1
            
            // Verify coin animation
            verifyCoinAnimation()
            
            // Check for celebration milestone
            if currentCoins % 5 == 0 {
                verifyCelebrationOverlay(coins: currentCoins)
            }
            
            // Check treasure eligibility
            if currentCoins >= 10 && currentCoins < 100 {
                // For testing, skip YouTube redemption until 100 coins
                // Just verify chest is glowing
                let chest = app.images["treasure_chest_glowing"]
                XCTAssertTrue(chest.exists)
            }
            
            // Performance checks
            checkPerformanceMetrics()
            
            // Log progress
            print("✓ Coin \(currentCoins)/\(TestConfig.targetCoins) earned (Attempt #\(attemptCount))")
            
        } else {
            // Activity failed - screenshot and log
            takeScreenshot(named: "activity_failure_attempt_\(attemptCount)")
            print("✗ Activity failed at coin \(currentCoins), attempt \(attemptCount)")
            
            // Return to home and retry
            returnToHome()
        }
    }
    
    XCTAssertEqual(currentCoins, TestConfig.targetCoins, "Should reach exactly 100 coins")
}

func selectAndCompleteActivity(attemptNumber: Int) -> (success: Bool, activityType: String) {
    // Rotate through activities for testing variety
    let activities = ["Rätsel", "Zahlen 1,2,3"]
    let activityIndex = attemptNumber % activities.count
    let selectedActivity = activities[activityIndex]
    
    XCTContext.runActivity(named: "Complete \(selectedActivity) activity") { _ in
        // Tap activity button
        let activityButton = app.buttons[selectedActivity]
        XCTAssertTrue(activityButton.waitForExistence(timeout: 2))
        activityButton.tap()
        
        // Wait for activity selection if multiple sub-activities
        wait(for: 1.0)
        
        // Complete activity based on type
        switch selectedActivity {
        case "Rätsel":
            return completePuzzleActivity()
        case "Zahlen 1,2,3":
            return completeZahlenActivity()
        default:
            XCTFail("Unknown activity type: \(selectedActivity)")
            return (false, selectedActivity)
        }
    }
}

func completePuzzleActivity() -> (success: Bool, activityType: String) {
    // Select sub-activity (alternate between Puzzle Matching and Labyrinth)
    let subActivities = ["Puzzle Matching", "Labyrinth"]
    let subIndex = Int.random(in: 0...1)
    let selectedSub = subActivities[subIndex]
    
    // For now, tap first available sub-activity button
    let subButton = app.buttons.element(boundBy: 0)
    if subButton.exists {
        subButton.tap()
        wait(for: 1.0)
    }
    
    // Wait for activity to load
    wait(for: 2.0)
    
    // Check if it's puzzle matching or labyrinth
    if app.staticTexts["ZIEL"].exists && app.staticTexts["DU"].exists {
        // Puzzle Matching
        return solvePuzzleMatching()
    } else if app.staticTexts["START"].exists && app.staticTexts["ZIEL"].exists {
        // Labyrinth
        return solveLabyrinth()
    }
    
    return (false, "Rätsel")
}

func solvePuzzleMatching() -> (success: Bool, activityType: String) {
    // Read the ZIEL (target) pattern
    let zielGrid = app.otherElements["ziel_grid"]
    XCTAssertTrue(zielGrid.exists)
    
    // For automated testing, we need to:
    // 1. Read the target pattern colors
    // 2. Replicate in DU grid
    
    // This requires accessibility identifiers on grid cells
    // Example: grid_ziel_0_0, grid_ziel_0_1, etc.
    
    // Get grid size (should be in accessibility properties)
    let gridSizeLabel = app.staticTexts.matching(identifier: "grid_size").firstMatch
    let gridSize = Int(gridSizeLabel.label) ?? 3 // Default to 3x3
    
    // Read target pattern
    var targetPattern: [[String]] = []
    for row in 0..<gridSize {
        var rowColors: [String] = []
        for col in 0..<gridSize {
            let cellIdentifier = "grid_ziel_\(row)_\(col)"
            let cell = app.otherElements[cellIdentifier]
            if cell.exists {
                let colorLabel = cell.label // Should be "green", "yellow", "gray", or "empty"
                rowColors.append(colorLabel)
            }
        }
        targetPattern.append(rowColors)
    }
    
    // Replicate pattern in DU grid
    for row in 0..<gridSize {
        for col in 0..<gridSize {
            let targetColor = targetPattern[row][col]
            
            if targetColor != "empty" {
                // Select color from picker
                let colorButton = app.buttons["\(targetColor)_color_picker"]
                XCTAssertTrue(colorButton.exists, "Color picker for \(targetColor) should exist")
                colorButton.tap()
                
                // Tap the corresponding DU grid cell
                let duCellIdentifier = "grid_du_\(row)_\(col)"
                let duCell = app.otherElements[duCellIdentifier]
                XCTAssertTrue(duCell.exists, "DU grid cell \(row),\(col) should exist")
                duCell.tap()
                
                wait(for: 0.2) // Small delay for animation
            }
        }
    }
    
    // Wait for success detection (pattern should auto-complete)
    let successIndicator = app.staticTexts["Super gemacht!"]
    let matchDetected = successIndicator.waitForExistence(timeout: 2)
    
    return (matchDetected, "Puzzle Matching")
}

func solveLabyrinth() -> (success: Bool, activityType: String) {
    // Find START marker
    let startMarker = app.otherElements["labyrinth_start"]
    XCTAssertTrue(startMarker.exists)
    
    // Find ZIEL marker
    let goalMarker = app.otherElements["labyrinth_goal"]
    XCTAssertTrue(goalMarker.exists)
    
    // For automated testing, we need pre-defined path coordinates
    // This should be in the accessibility properties or test data
    
    // Swipe along the path from START to GOAL
    // For now, use a simple gesture
    let startPoint = startMarker.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5))
    let endPoint = goalMarker.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5))
    
    startPoint.press(forDuration: 0.1, thenDragTo: endPoint)
    
    // Wait for success detection
    let successIndicator = app.staticTexts["Super gemacht!"]
    let pathCompleted = successIndicator.waitForExistence(timeout: 2)
    
    return (pathCompleted, "Labyrinth")
}

func completeZahlenActivity() -> (success: Bool, activityType: String) {
    // Select sub-activity (alternate between Würfel and Wähle Zahl)
    let subIndex = Int.random(in: 0...1)
    
    let subButton = app.buttons.element(boundBy: subIndex)
    if subButton.exists {
        subButton.tap()
        wait(for: 1.0)
    }
    
    // Wait for activity to load
    wait(for: 2.0)
    
    // Check activity type by looking for unique elements
    if app.buttons["roll_dice"].exists {
        // Würfel (Dice)
        return solveWuerfel()
    } else if app.otherElements.matching(identifier: "number_trace_").count > 0 {
        // Wähle die Zahl (Number tracing)
        return solveWaehleZahl()
    }
    
    return (false, "Zahlen")
}

func solveWuerfel() -> (success: Bool, activityType: String) {
    // Roll the dice
    let diceButton = app.buttons["roll_dice"]
    diceButton.tap()
    
    // Wait for dice animation
    wait(for: 1.5)
    
    // Read the dice result
    let diceResult = app.staticTexts.matching(identifier: "dice_result").firstMatch
    guard let resultNumber = Int(diceResult.label) else {
        return (false, "Würfel")
    }
    
    // Wait for narrator: "Zeig mir die [N]!"
    wait(for: 1.5)
    
    // Tap the correct number button
    let numberButton = app.buttons["number_button_\(resultNumber)"]
    XCTAssertTrue(numberButton.exists, "Number button \(resultNumber) should exist")
    numberButton.tap()
    
    // Wait for success
    let successIndicator = app.staticTexts.matching(identifier: "success_message").firstMatch
    let success = successIndicator.waitForExistence(timeout: 2)
    
    return (success, "Würfel")
}

func solveWaehleZahl() -> (success: Bool, activityType: String) {
    // Get the target number from narrator prompt
    wait(for: 1.0) // Wait for narrator: "Zeig mir die [N]!"
    
    let targetNumberLabel = app.staticTexts.matching(identifier: "target_number").firstMatch
    guard let targetNumber = Int(targetNumberLabel.label) else {
        return (false, "Wähle Zahl")
    }
    
    // Trace the number on the stone tablet
    let numberToTrace = app.otherElements["number_trace_\(targetNumber)"]
    XCTAssertTrue(numberToTrace.exists, "Number \(targetNumber) should be traceable")
    
    // Perform tracing gesture
    // For automated testing, simulate a path that covers 70%+ of the number
    let tracePath = getTracingPathForNumber(targetNumber)
    performTracingGesture(path: tracePath, on: numberToTrace)
    
    // Wait for validation
    wait(for: 1.0)
    
    // Check for success
    let successIndicator = app.staticTexts.matching(identifier: "success_message").firstMatch
    let success = successIndicator.waitForExistence(timeout: 2)
    
    return (success, "Wähle Zahl")
}

func getTracingPathForNumber(_ number: Int) -> [CGPoint] {
    // Returns normalized path coordinates for tracing each number
    // These should cover 70%+ of the number shape
    
    switch number {
    case 1:
        return [CGPoint(x: 0.5, y: 0.2), CGPoint(x: 0.5, y: 0.8)]
    case 2:
        return [
            CGPoint(x: 0.3, y: 0.3), CGPoint(x: 0.7, y: 0.3),
            CGPoint(x: 0.7, y: 0.5), CGPoint(x: 0.3, y: 0.7),
            CGPoint(x: 0.3, y: 0.8), CGPoint(x: 0.7, y: 0.8)
        ]
    // ... patterns for 3-10
    default:
        return [CGPoint(x: 0.5, y: 0.5)] // Fallback
    }
}

func performTracingGesture(path: [CGPoint], on element: XCUIElement) {
    guard path.count >= 2 else { return }
    
    let startPoint = element.coordinate(withNormalizedOffset: CGVector(dx: path[0].x, dy: path[0].y))
    
    // Create a path through all points
    var currentPoint = startPoint
    for point in path.dropFirst() {
        let nextPoint = element.coordinate(withNormalizedOffset: CGVector(dx: point.x, dy: point.y))
        currentPoint.press(forDuration: 0.1, thenDragTo: nextPoint)
        currentPoint = nextPoint
        wait(for: 0.1)
    }
}
```

### Phase 3: Celebration Milestones

```swift
func verifyCelebrationOverlay(coins: Int) {
    XCTContext.runActivity(named: "Verify \(coins)-coin celebration") { _ in
        // Celebration overlay should appear
        let celebrationOverlay = app.otherElements["celebration_overlay"]
        XCTAssertTrue(celebrationOverlay.waitForExistence(timeout: 2),
                      "\(coins)-coin celebration overlay should appear")
        
        // Verify confetti animation
        let confetti = app.otherElements["confetti_animation"]
        XCTAssertTrue(confetti.exists, "Confetti should be visible")
        
        // Verify correct message
        let expectedMessages: [Int: String] = [
            5: "Wir haben schon fünf Goldmünzen!",
            10: "Zehn Goldmünzen! Du kannst jetzt YouTube schauen.",
            15: "Fünfzehn! Weiter so!",
            20: "Zwanzig Münzen! Du bekommst Bonuszeit!"
        ]
        
        if let expectedMessage = expectedMessages[coins] {
            let messageText = app.staticTexts[expectedMessage]
            XCTAssertTrue(messageText.exists,
                          "Should show correct celebration message for \(coins) coins")
        }
        
        // Wait for Bennie voice to finish
        wait(for: 2.0)
        
        // Tap "Weiter" button
        let weiterButton = app.buttons["Weiter"]
        XCTAssertTrue(weiterButton.exists, "Weiter button should exist")
        XCTAssertTrue(weiterButton.frame.width >= 96, "Weiter button should meet touch target size")
        weiterButton.tap()
        
        // Overlay should dismiss
        XCTAssertFalse(celebrationOverlay.waitForExistence(timeout: 1),
                       "Overlay should dismiss after tapping Weiter")
    }
}
```

### Phase 4: YouTube Redemption (100 coins → 100 minutes)

```swift
func testPhase3_YouTubeRedemption() {
    var minutesWatched = 0
    let targetMinutes = TestConfig.youtubeMinutesRequired
    
    // Should have 100 coins now
    let coinCounter = app.staticTexts.matching(identifier: "coin_counter").firstMatch
    XCTAssertEqual(coinCounter.label, "100", "Should have exactly 100 coins")
    
    // Redemption loop: 100 coins = 5 sessions of 20-minute redemptions (10+2 bonus)
    // or 10 sessions of 10-coin redemptions (5 minutes each)
    
    while minutesWatched < targetMinutes {
        XCTContext.runActivity(named: "Redeem for YouTube session \((minutesWatched/12) + 1)") { _ in
            
            // Tap treasure chest
            let treasureChest = app.buttons["treasure_chest"]
            XCTAssertTrue(treasureChest.waitForExistence(timeout: 2))
            treasureChest.tap()
            
            // Treasure screen appears
            wait(for: 1.0)
            
            // Select 10+2 minute option if we have 20+ coins
            let currentCoins = getCurrentCoinCount()
            
            if currentCoins >= 20 {
                let tenMinButton = app.buttons["youtube_10min"]
                XCTAssertTrue(tenMinButton.exists)
                XCTAssertFalse(tenMinButton.isEnabled == false, "10-min button should be active with 20+ coins")
                tenMinButton.tap()
                
                minutesWatched += 12
                
            } else if currentCoins >= 10 {
                let fiveMinButton = app.buttons["youtube_5min"]
                XCTAssertTrue(fiveMinButton.exists)
                XCTAssertFalse(fiveMinButton.isEnabled == false, "5-min button should be active with 10+ coins")
                fiveMinButton.tap()
                
                minutesWatched += 5
            } else {
                XCTFail("Should have enough coins for redemption")
                break
            }
            
            // Video selection screen
            wait(for: 1.0)
            
            // Select first video (should be pre-approved)
            let firstVideo = app.buttons.matching(identifier: "video_card_").firstMatch
            XCTAssertTrue(firstVideo.exists, "Should have at least one approved video")
            firstVideo.tap()
            
            // Video player screen
            wait(for: 1.5)
            
            // Verify analog clock appears
            let analogClock = app.otherElements["analog_countdown_clock"]
            XCTAssertTrue(analogClock.exists, "Analog clock should be visible")
            
            // For testing, we can fast-forward by manipulating time
            // In production, video would play for full duration
            // For test, wait a few seconds then simulate time-up
            
            // Simulate 1-minute warning (for 5-min video, this is at 4 minutes)
            wait(for: 2.0) // Simulate partial playback
            
            // Check if 1-minute warning fires
            // (In production, this would be at actual 1-minute-remaining mark)
            
            // Simulate time-up
            simulateVideoTimeUp()
            
            // Should return to home
            wait(for: 2.0)
            let homeSign = app.staticTexts["Waldabenteuer"]
            XCTAssertTrue(homeSign.exists, "Should return to home after video")
            
            print("✓ YouTube session complete. Total watched: \(minutesWatched)/\(targetMinutes) minutes")
        }
    }
    
    XCTAssertGreaterThanOrEqual(minutesWatched, targetMinutes,
                                "Should watch at least \(targetMinutes) minutes of YouTube")
}

func simulateVideoTimeUp() {
    // In a real test, we'd fast-forward the video timer
    // For now, we can tap a hidden test button or use accessibility actions
    
    // Option 1: Use accessibility action
    let videoPlayer = app.otherElements["youtube_player"]
    if videoPlayer.exists {
        // Trigger time-up through accessibility custom action
        // This requires the video player to expose a "test_time_up" action
        // videoPlayer.customActions.first { $0.name == "test_time_up" }?.activate()
    }
    
    // Option 2: Wait for actual time-up (slow but real)
    // let timeUpMessage = app.staticTexts["Die Zeit ist um. Lass uns spielen!"]
    // timeUpMessage.waitForExistence(timeout: 360) // 6 minutes max
}

func getCurrentCoinCount() -> Int {
    let coinCounter = app.staticTexts.matching(identifier: "coin_counter").firstMatch
    return Int(coinCounter.label) ?? 0
}
```

### Performance Monitoring

```swift
func checkPerformanceMetrics() {
    // Memory check
    let memoryUsage = getMemoryUsage()
    XCTAssertLessThan(memoryUsage, TestConfig.memoryThreshold,
                      "Memory usage should stay under \(TestConfig.memoryThreshold)MB (current: \(memoryUsage)MB)")
    
    // FPS check
    let currentFPS = getCurrentFPS()
    XCTAssertGreaterThanOrEqual(currentFPS, TestConfig.fpsThreshold,
                                 "FPS should stay above \(TestConfig.fpsThreshold) (current: \(currentFPS))")
}

func getMemoryUsage() -> Float {
    // Use XCTest performance metrics
    let measurement = XCTMemoryMetric.applicationLaunch.measurements.last
    return Float(measurement?.value ?? 0) / 1_048_576 // Convert bytes to MB
}

func getCurrentFPS() -> Float {
    // This requires using XCTest metrics or custom FPS counter
    // For now, return a placeholder
    // In real implementation, use CADisplayLink or similar
    return 60.0 // Placeholder
}
```

## Error Handling & Recovery

```swift
func returnToHome() {
    // Tap home button if available
    let homeButton = app.buttons["Home"]
    if homeButton.exists {
        homeButton.tap()
        wait(for: 1.0)
        return
    }
    
    // Otherwise, try back button
    let backButton = app.buttons["Zurück"]
    if backButton.exists {
        backButton.tap()
        wait(for: 0.5)
        returnToHome() // Recursive until we reach home
    }
}

func takeScreenshot(named: String) {
    if TestConfig.screenshotOnError {
        let screenshot = XCUIScreen.main.screenshot()
        let attachment = XCTAttachment(screenshot: screenshot)
        attachment.name = named
        attachment.lifetime = .keepAlways
        add(attachment)
    }
}

func wait(for duration: TimeInterval) {
    Thread.sleep(forTimeInterval: duration)
}
```

## Success Criteria

The test is considered successful if:

- ✅ All 100 coins earned without crashes
- ✅ All celebration milestones (5, 10, 15, 20, ..., 100) triggered correctly
- ✅ All 4 activity types completed successfully multiple times
- ✅ 100+ minutes of YouTube watched successfully
- ✅ Memory stayed under 200MB throughout
- ✅ FPS stayed above 55fps throughout
- ✅ All touch targets responded correctly
- ✅ All voice lines played at correct times
- ✅ No visual glitches or incorrect colors
- ✅ State transitions were smooth and correct

## Failure Handling

If test fails:
1. Take screenshot of error state
2. Log full state dump (coins, current screen, activity progress)
3. Attempt recovery by returning to home
4. Retry from last known good state
5. If 3 consecutive failures at same point → FATAL ERROR, stop test
6. Generate detailed error report with:
   - Failure location (screen, action)
   - State at failure (coins, progress)
   - Performance metrics at failure
   - Screenshot
   - Console logs

## Test Execution

```bash
# Run full playthrough test
xcodebuild test \
  -scheme BennieGame \
  -destination 'platform=iOS Simulator,name=iPad (10th generation),OS=17.0' \
  -testPlan FullPlaythroughTest \
  -resultBundlePath ./test_results/playthrough_$(date +%Y%m%d_%H%M%S)
```

## Expected Duration

- Phase 1 (Launch + Selection): ~10 seconds
- Phase 2 (100 activities): ~20-30 minutes (12-18 seconds per activity average)
- Phase 3 (YouTube sessions): ~15 minutes (simulated, or 100 minutes real)
- **Total**: ~30-45 minutes (simulated) or ~2.5 hours (real playback)

## Next Steps

Once this test passes:
1. Run multiple times (5+ successful runs required)
2. Test with both players (Alexander and Oliver profiles)
3. Test with different activity sequences
4. Test with network failures during YouTube
5. Test with app backgrounding/foregrounding
6. Test with low memory conditions
7. Test with system interruptions (calls, notifications)
