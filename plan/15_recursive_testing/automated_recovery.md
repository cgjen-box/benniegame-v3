# Automated Error Recovery System

## Purpose

Enables Claude Code to autonomously detect, handle, and recover from errors during testing without human intervention.

## Error Detection Mechanisms

### 1. Crash Detection

```swift
class CrashDetector {
    func setupCrashHandling() {
        // Detect app crashes during test execution
        NSSetUncaughtExceptionHandler { exception in
            self.handleCrash(exception: exception)
        }
        
        signal(SIGABRT) { _ in
            CrashDetector.shared.handleSignal("SIGABRT")
        }
        
        signal(SIGSEGV) { _ in
            CrashDetector.shared.handleSignal("SIGSEGV")
        }
    }
    
    func handleCrash(exception: NSException) {
        let state = GameStateCapture.captureCurrentState()
        let report = CrashReport(
            timestamp: Date(),
            exception: exception,
            gameState: state,
            screenshot: captureScreen()
        )
        
        saveCrashReport(report)
        attemptRecovery()
    }
}
```

### 2. Freeze Detection

```swift
class FreezeDetector {
    private var watchdogTimer: Timer?
    private let freezeThreshold: TimeInterval = 5.0 // 5 seconds without UI update
    
    func startMonitoring() {
        watchdogTimer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
            self.checkForFreeze()
        }
    }
    
    func checkForFreeze() {
        let lastUIUpdate = UIUpdateTracker.shared.lastUpdateTime
        let timeSinceUpdate = Date().timeIntervalSince(lastUIUpdate)
        
        if timeSinceUpdate > freezeThreshold {
            handleFreeze(duration: timeSinceUpdate)
        }
    }
    
    func handleFreeze(duration: TimeInterval) {
        print("⚠️ Freeze detected: No UI updates for \(duration)s")
        takeScreenshot(named: "freeze_detected")
        
        // Attempt to unfreeze
        attemptUnfreeze()
    }
}
```

### 3. State Validation

```swift
class StateValidator {
    func validateCurrentState() -> ValidationResult {
        // Check if we're in a valid game state
        let currentScreen = getCurrentScreen()
        let expectedElements = getExpectedElementsFor(screen: currentScreen)
        
        var missingElements: [String] = []
        for element in expectedElements {
            if !element.exists {
                missingElements.append(element.identifier)
            }
        }
        
        if !missingElements.isEmpty {
            return .invalid(reason: "Missing elements: \(missingElements)")
        }
        
        // Check for error dialogs
        if app.alerts.count > 0 {
            let alertText = app.alerts.firstMatch.label
            return .invalid(reason: "Unexpected alert: \(alertText)")
        }
        
        return .valid
    }
}

enum ValidationResult {
    case valid
    case invalid(reason: String)
}
```

## Recovery Strategies

### Strategy 1: Soft Reset (Return to Home)

```swift
func attemptSoftReset() -> Bool {
    print("🔄 Attempting soft reset...")
    
    // Try tapping Home button
    let homeButton = app.buttons["Home"]
    if homeButton.exists {
        homeButton.tap()
        wait(for: 1.0)
        
        // Verify we're at home
        if app.staticTexts["Waldabenteuer"].exists {
            print("✓ Soft reset successful")
            return true
        }
    }
    
    // Try back button navigation
    var backAttempts = 0
    while backAttempts < 5 {
        let backButton = app.buttons["Zurück"]
        if backButton.exists {
            backButton.tap()
            wait(for: 0.5)
            backAttempts += 1
            
            if app.staticTexts["Waldabenteuer"].exists {
                print("✓ Soft reset successful after \(backAttempts) back taps")
                return true
            }
        } else {
            break
        }
    }
    
    print("✗ Soft reset failed")
    return false
}
```

### Strategy 2: App Restart

```swift
func attemptAppRestart() -> Bool {
    print("🔄 Attempting app restart...")
    
    // Terminate app
    app.terminate()
    wait(for: 2.0)
    
    // Relaunch
    app.launch()
    wait(for: 5.0) // Allow loading screen to complete
    
    // Verify successful launch
    if app.staticTexts["Wer spielt heute?"].waitForExistence(timeout: 5) {
        print("✓ App restart successful")
        
        // Restore state (select player, navigate to where we were)
        restoreGameState()
        return true
    }
    
    print("✗ App restart failed")
    return false
}

func restoreGameState() {
    let savedState = loadLastKnownGoodState()
    
    // Re-select player
    if let playerName = savedState.playerName {
        let playerButton = app.buttons[playerName]
        if playerButton.exists {
            playerButton.tap()
            wait(for: 2.0)
        }
    }
    
    // Navigate to last screen
    // (For activities, we'll start fresh from home)
}
```

### Strategy 3: Simulator Restart

```swift
func attemptSimulatorRestart() -> Bool {
    print("🔄 Attempting simulator restart...")
    
    // This requires xcrun simctl commands
    let simulatorID = getSimulatorID()
    
    // Shutdown simulator
    let shutdownResult = shell("xcrun simctl shutdown \(simulatorID)")
    guard shutdownResult.success else {
        print("✗ Failed to shutdown simulator")
        return false
    }
    
    wait(for: 3.0)
    
    // Boot simulator
    let bootResult = shell("xcrun simctl boot \(simulatorID)")
    guard bootResult.success else {
        print("✗ Failed to boot simulator")
        return false
    }
    
    wait(for: 10.0) // Allow simulator to fully boot
    
    // Relaunch app
    return attemptAppRestart()
}

func shell(_ command: String) -> (success: Bool, output: String) {
    let task = Process()
    task.launchPath = "/bin/bash"
    task.arguments = ["-c", command]
    
    let pipe = Pipe()
    task.standardOutput = pipe
    task.standardError = pipe
    
    task.launch()
    task.waitUntilExit()
    
    let data = pipe.fileHandleForReading.readDataToEndOfFile()
    let output = String(data: data, encoding: .utf8) ?? ""
    
    return (task.terminationStatus == 0, output)
}
```

## Recovery Decision Tree

```
Error Detected
    │
    ├─ Is app responsive?
    │   YES ├─ Attempt Soft Reset
    │       │   ├─ Success? → Continue test
    │       │   └─ Failed? → Try App Restart
    │   NO  └─ Freeze detected → Force restart
    │
    ├─ App Restart
    │   ├─ Success? → Restore state, continue
    │   └─ Failed? → Try Simulator Restart
    │
    └─ Simulator Restart
        ├─ Success? → Fresh start from player selection
        └─ Failed? → FATAL ERROR, stop test, report
```

## State Preservation

```swift
struct GameStateSnapshot: Codable {
    let timestamp: Date
    let playerName: String
    let coins: Int
    let currentScreen: String
    let currentActivity: String?
    let lastCompletedActivity: String?
    let celebrationMilestones: [Int] // Which milestones already triggered
    let youtubeMinutesWatched: Int
}

class StateManager {
    static let snapshotInterval: TimeInterval = 10.0 // Save every 10 seconds
    
    func startAutoSaving() {
        Timer.scheduledTimer(withTimeInterval: StateManager.snapshotInterval, repeats: true) { _ in
            self.saveCurrentState()
        }
    }
    
    func saveCurrentState() {
        let snapshot = captureCurrentState()
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        
        if let data = try? encoder.encode(snapshot) {
            UserDefaults.standard.set(data, forKey: "lastKnownGoodState")
            UserDefaults.standard.synchronize()
        }
    }
    
    func loadLastKnownGoodState() -> GameStateSnapshot? {
        guard let data = UserDefaults.standard.data(forKey: "lastKnownGoodState"),
              let snapshot = try? JSONDecoder().decode(GameStateSnapshot.self, from: data) else {
            return nil
        }
        return snapshot
    }
}
```

## Retry Logic

```swift
class RetryManager {
    private let maxRetries = 3
    private var retryCount: [String: Int] = [:] // Track retries per error type
    
    func shouldRetry(errorType: String) -> Bool {
        let currentRetries = retryCount[errorType, default: 0]
        return currentRetries < maxRetries
    }
    
    func recordRetry(errorType: String) {
        retryCount[errorType, default: 0] += 1
    }
    
    func resetRetries(errorType: String) {
        retryCount[errorType] = 0
    }
    
    func executeWithRetry<T>(
        operation: () throws -> T,
        errorType: String,
        recoveryStrategy: () -> Bool
    ) throws -> T {
        while shouldRetry(errorType: errorType) {
            do {
                let result = try operation()
                resetRetries(errorType: errorType) // Success - reset counter
                return result
            } catch {
                recordRetry(errorType: errorType)
                print("⚠️ Error: \(error). Retry \(retryCount[errorType]!)/\(maxRetries)")
                
                // Attempt recovery
                if recoveryStrategy() {
                    continue // Try operation again
                } else {
                    throw RecoveryError.recoveryFailed
                }
            }
        }
        
        throw RecoveryError.maxRetriesExceeded
    }
}

enum RecoveryError: Error {
    case recoveryFailed
    case maxRetriesExceeded
}
```

## Integration with Test Runner

```swift
class ResilientTestRunner {
    let retryManager = RetryManager()
    let stateManager = StateManager()
    
    func runFullPlaythrough() {
        stateManager.startAutoSaving()
        
        do {
            // Phase 1: Player Selection
            try retryManager.executeWithRetry(
                operation: testPhase1_PlayerSelection,
                errorType: "playerSelection",
                recoveryStrategy: attemptAppRestart
            )
            
            // Phase 2: Activity Loop
            var currentCoins = 0
            while currentCoins < 100 {
                let result = try retryManager.executeWithRetry(
                    operation: { try completeNextActivity() },
                    errorType: "activityCompletion",
                    recoveryStrategy: attemptSoftReset
                )
                
                if result.success {
                    currentCoins += 1
                }
            }
            
            // Phase 3: YouTube Redemption
            try retryManager.executeWithRetry(
                operation: testPhase3_YouTubeRedemption,
                errorType: "youtubeRedemption",
                recoveryStrategy: attemptSoftReset
            )
            
            print("✅ FULL PLAYTHROUGH SUCCESSFUL")
            
        } catch {
            print("❌ FATAL ERROR: Test could not complete after all recovery attempts")
            generateFailureReport(error: error)
        }
    }
}
```

## Error Reporting

```swift
struct ErrorReport: Codable {
    let timestamp: Date
    let errorType: String
    let errorMessage: String
    let gameState: GameStateSnapshot
    let screenshotPath: String
    let consoleLog: String
    let recoveryAttempts: Int
    let recoverySuccessful: Bool
}

func generateFailureReport(error: Error) {
    let report = ErrorReport(
        timestamp: Date(),
        errorType: String(describing: type(of: error)),
        errorMessage: error.localizedDescription,
        gameState: StateManager.shared.captureCurrentState(),
        screenshotPath: takeScreenshot(named: "fatal_error"),
        consoleLog: captureConsoleLog(),
        recoveryAttempts: retryManager.retryCount.values.reduce(0, +),
        recoverySuccessful: false
    )
    
    // Save report
    let encoder = JSONEncoder()
    encoder.dateEncodingStrategy = .iso8601
    encoder.outputFormatting = .prettyPrinted
    
    if let data = try? encoder.encode(report),
       let json = String(data: data, encoding: .utf8) {
        let timestamp = DateFormatter().string(from: Date())
        let filename = "error_report_\(timestamp).json"
        try? json.write(toFile: filename, atomically: true, encoding: .utf8)
        print("📄 Error report saved: \(filename)")
    }
}
```

## Success Criteria

Recovery system is working correctly if:
- ✅ Soft resets succeed 90%+ of the time
- ✅ App restarts succeed 95%+ of the time
- ✅ No more than 3 retries needed per error
- ✅ State is preserved across restarts
- ✅ Test can complete despite transient errors
- ✅ All errors are logged with full context

## Testing the Recovery System

```swift
// Test recovery system itself
func testRecoverySystem() {
    // Inject deliberate errors to verify recovery works
    
    // Test 1: Simulate freeze
    simulateFreeze(duration: 10.0)
    XCTAssertTrue(FreezeDetector.shared.detectedFreeze)
    XCTAssertTrue(attemptUnfreeze())
    
    // Test 2: Simulate crash
    // (This requires careful setup to not actually crash the test runner)
    
    // Test 3: Simulate invalid state
    navigateToInvalidState()
    XCTAssertEqual(StateValidator.shared.validateCurrentState(), .invalid)
    XCTAssertTrue(attemptSoftReset())
    XCTAssertEqual(StateValidator.shared.validateCurrentState(), .valid)
}
```
