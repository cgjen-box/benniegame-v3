# Testing Patterns

**Analysis Date:** 2026-01-12

## Test Framework

**Runner:**
- XCTest (implicit from Xcode project template)
- Not yet configured - project in planning phase

**Assertion Library:**
- XCTest built-in assertions
- Expected: `XCTAssertEqual`, `XCTAssertTrue`, `XCTAssertThrows`

**Run Commands:**
```bash
# Xcode (once project created)
xcodebuild test -scheme BennieGame -destination "platform=iOS Simulator,name=iPad (10th generation)"

# Or via Xcode UI: Cmd+U
```

## Test File Organization

**Location:**
- Tests not yet created
- Expected: Co-located or `Tests/` directory

**Naming:**
- Expected: `*Tests.swift` (e.g., `GameStateTests.swift`)

**Structure:**
```
BennieGame/
└── Tests/                   # (To be created)
    ├── Core/
    │   ├── GameStateTests.swift
    │   └── PlayerDataTests.swift
    ├── Services/
    │   └── AudioManagerTests.swift
    └── Components/
        └── WoodButtonTests.swift
```

## Test Structure

**Suite Organization:**
```swift
import XCTest
@testable import BennieGame

final class GameStateTests: XCTestCase {
    var gameState: GameState!

    override func setUp() {
        super.setUp()
        gameState = GameState()
    }

    override func tearDown() {
        gameState = nil
        super.tearDown()
    }

    func testInitialState() {
        XCTAssertEqual(gameState.currentScreen, .loading)
        XCTAssertNil(gameState.currentPlayer)
    }

    func testCoinAward() {
        gameState.currentPlayer = "alexander"
        gameState.players["alexander"] = PlayerData(name: "Alexander")

        gameState.awardCoin()

        XCTAssertEqual(gameState.activePlayer?.coins, 1)
    }
}
```

**Patterns:**
- Use `setUp()` for shared setup
- Use `tearDown()` to clean up
- One logical assertion per test
- Descriptive test names

## Mocking

**Framework:**
- Protocol-based mocking (manual)
- No third-party mock framework configured

**Patterns:**
```swift
// Protocol for dependency injection
protocol AudioManagerProtocol {
    func playVoice(_ file: String)
    func playMusic(_ file: String, loop: Bool)
}

// Mock for testing
class MockAudioManager: AudioManagerProtocol {
    var playedVoices: [String] = []

    func playVoice(_ file: String) {
        playedVoices.append(file)
    }

    func playMusic(_ file: String, loop: Bool) {}
}
```

**What to Mock:**
- Audio playback (AVFoundation)
- External services (YouTube, API calls)
- File system operations
- Timer-based operations

**What NOT to Mock:**
- Pure functions (state calculations)
- SwiftUI view composition
- Color/font definitions

## Fixtures and Factories

**Test Data:**
```swift
// Factory for test data
extension PlayerData {
    static func testPlayer(
        name: String = "TestPlayer",
        coins: Int = 0
    ) -> PlayerData {
        return PlayerData(
            name: name,
            coins: coins,
            activityProgress: [:],
            learningProfile: LearningProfile()
        )
    }
}
```

**Location:**
- Factory functions: In test file or `Tests/Helpers/`
- Shared fixtures: `Tests/Fixtures/`

## Coverage

**Requirements:**
- No enforced coverage target
- Focus on critical paths (state machine, coin economy)
- Visual validation via Design QA Checklist

**Configuration:**
- Xcode built-in coverage
- Enable via scheme settings

**View Coverage:**
```bash
# Via Xcode: Product → Test → View Coverage Report
```

## Test Types

**Unit Tests:**
- Scope: Single function/class in isolation
- Mocking: Mock all external dependencies
- Speed: <100ms per test
- Focus: State machine, coin calculations, validation logic

**Integration Tests:**
- Scope: Multiple modules together
- Mocking: Mock external boundaries only
- Focus: Screen navigation flow, data persistence

**E2E Tests (Recursive Testing):**
- Location: `plan/15_recursive_testing/`
- Scope: Full user flows (100 coins, 100 min YouTube)
- Framework: Manual + MCP automation
- Focus: Complete gameplay validation

## Design QA Testing

**Framework:**
- Manual visual inspection
- Reference images: `design/references/screens/Reference_*.png`
- Checklist: `DESIGN_QA_CHECKLIST.md`

**Validation Checklist:**
```
| ✓ | Requirement | Specification | How to Verify |
|---|-------------|---------------|---------------|
| ☐ | Bennie color | #8C7259 brown | Color picker tool |
| ☐ | NO clothing | Never vest/accessories | Visual inspection |
| ☐ | Lemminge color | #6FA8DC blue | Color picker tool |
| ☐ | Touch targets | ≥96pt | Accessibility Inspector |
| ☐ | German text | No English in UI | Visual inspection |
```

**Pass Criteria:**
- 100% Critical + 90% High Priority = PASS
- 100% Critical + 80-89% High Priority = REVIEW REQUIRED
- Any Critical failure = REJECT

## Common Patterns

**Async Testing:**
```swift
func testAsyncOperation() async throws {
    let result = await service.fetchData()
    XCTAssertEqual(result.count, 10)
}
```

**Error Testing:**
```swift
func testThrowsOnInvalidInput() {
    XCTAssertThrowsError(try parser.parse(nil)) { error in
        XCTAssertEqual(error as? ParseError, .invalidInput)
    }
}
```

**State Machine Testing:**
```swift
func testValidTransition() {
    gameState.currentScreen = .loading

    XCTAssertTrue(gameState.canTransition(to: .playerSelection))
    XCTAssertFalse(gameState.canTransition(to: .treasureScreen))
}
```

**Snapshot Testing:**
- Not configured
- Consider for visual regression testing

## Recursive Testing Strategy

**Location:** `plan/15_recursive_testing/`

**Scenarios:**
1. Alexander complete journey (100 coins)
2. Oliver complete journey (100 coins)
3. Edge cases (force quit, time limits, offline)

**Goals:**
- Test every interaction path
- Earn 100+ coins
- Watch 100+ minutes YouTube
- Test all 4 activities

**Validation:**
- No crashes
- All voices play correctly
- Coins track accurately
- State persists across restarts

---

*Testing analysis: 2026-01-12*
*Update when test patterns change*
