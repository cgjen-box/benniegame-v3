# Phase 13.4: Haptic Feedback System

**Status**: 🔵 Not Started
**Priority**: Critical
**Estimated Time**: 1 day
**Dependencies**: Phase 3 (Core Screens), Phase 4 (Activities)

---

## 📋 Overview

Implement context-appropriate haptic feedback to enhance tactile experience without overwhelming autistic children.

**Playbook Reference**: `C:\Users\christoph\Bennie und die Lemminge v3\docs\playbook\05-technical-requirements.md` Section 5.7 "Haptic Feedback"

---

## 🎯 Requirements from Playbook

| Event | Haptic Type | Reason |
|-------|-------------|--------|
| Button tap | Light impact | Gentle confirmation |
| Correct answer | Success notification | Positive reinforcement |
| Coin earned | Medium impact | Tangible reward |
| Wrong answer | Soft notification | Gentle, not punishing |
| Celebration | Heavy impact | Major achievement |

**Critical Rule**: All haptics must be **optional** and **gentle** - no harsh vibrations.

---

## 🎯 Implementation Plan

### 13.4.1: Haptic Manager Service

Create centralized haptic management system.

```swift
// File: BennieGame/Services/HapticManager.swift

import UIKit
import SwiftUI

final class HapticManager: ObservableObject {
    static let shared = HapticManager()
    
    @AppStorage("hapticsEnabled") var isEnabled: Bool = true
    
    // Haptic generators
    private let light = UIImpactFeedbackGenerator(style: .light)
    private let medium = UIImpactFeedbackGenerator(style: .medium)
    private let heavy = UIImpactFeedbackGenerator(style: .heavy)
    private let success = UINotificationFeedbackGenerator()
    private let soft = UINotificationFeedbackGenerator()
    
    private init() {
        // Prepare generators for reduced latency
        light.prepare()
        medium.prepare()
        heavy.prepare()
        success.prepare()
        soft.prepare()
    }
    
    // MARK: - Public API
    
    /// Gentle tap feedback for buttons
    func buttonTap() {
        guard isEnabled else { return }
        light.impactOccurred()
    }
    
    /// Success feedback for correct answers
    func correctAnswer() {
        guard isEnabled else { return }
        success.notificationOccurred(.success)
    }
    
    /// Tangible coin earned feedback
    func coinEarned() {
        guard isEnabled else { return }
        medium.impactOccurred()
    }
    
    /// Soft, gentle feedback for incorrect attempts
    func softFeedback() {
        guard isEnabled else { return }
        soft.notificationOccurred(.warning)
    }
    
    /// Celebration feedback for milestones
    func celebration() {
        guard isEnabled else { return }
        heavy.impactOccurred()
        
        // Additional sequence for emphasis
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) { [weak self] in
            self?.heavy.impactOccurred()
        }
    }
    
    /// Selection changed feedback (color picker, etc.)
    func selectionChanged() {
        guard isEnabled else { return }
        UISelectionFeedbackGenerator().selectionChanged()
    }
    
    // MARK: - Testing Support
    
    func testAll() {
        let haptics: [(String, () -> Void)] = [
            ("Button Tap", buttonTap),
            ("Correct Answer", correctAnswer),
            ("Coin Earned", coinEarned),
            ("Soft Feedback", softFeedback),
            ("Celebration", celebration),
            ("Selection Changed", selectionChanged)
        ]
        
        for (index, (name, action)) in haptics.enumerated() {
            DispatchQueue.main.asyncAfter(deadline: .now() + Double(index)) {
                print("Testing: \(name)")
                action()
            }
        }
    }
}

// MARK: - View Extension for easy access

extension View {
    func hapticFeedback(_ type: HapticType) -> some View {
        self.onTapGesture {
            HapticManager.shared.trigger(type)
        }
    }
}

enum HapticType {
    case buttonTap
    case correctAnswer
    case coinEarned
    case softFeedback
    case celebration
    case selectionChanged
}

extension HapticManager {
    func trigger(_ type: HapticType) {
        switch type {
        case .buttonTap: buttonTap()
        case .correctAnswer: correctAnswer()
        case .coinEarned: coinEarned()
        case .softFeedback: softFeedback()
        case .celebration: celebration()
        case .selectionChanged: selectionChanged()
        }
    }
}
```

---

### 13.4.2: Integration with Components

Update UI components to trigger haptics.

#### WoodButton Enhancement

```swift
// File: BennieGame/Design/Components/WoodButton.swift

struct WoodButton: View {
    let text: String?
    let icon: String?
    let action: () -> Void
    
    @StateObject private var haptics = HapticManager.shared
    
    var body: some View {
        Button(action: {
            haptics.buttonTap()  // ← ADD THIS
            action()
        }) {
            // ... existing button content
        }
        .buttonStyle(WoodButtonStyle())
    }
}
```

#### Puzzle Grid Cell Enhancement

```swift
// File: BennieGame/Features/Activities/Raetsel/Components/PuzzleGridCell.swift

struct PuzzleGridCell: View {
    let color: BennieColors.PuzzleColor?
    let onTap: () -> Void
    
    @StateObject private var haptics = HapticManager.shared
    
    var body: some View {
        // ... existing content
            .onTapGesture {
                haptics.selectionChanged()  // ← ADD THIS
                onTap()
            }
    }
}
```

---

### 13.4.3: Game Event Haptics

Add haptics to key game events.

```swift
// File: BennieGame/Services/GameStateManager.swift

final class GameStateManager: ObservableObject {
    @Published var player: PlayerData
    private let haptics = HapticManager.shared
    
    func awardCoin() {
        player.coins += 1
        haptics.coinEarned()  // ← ADD THIS
        
        // Check for celebration milestone
        if player.coins % 5 == 0 {
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
                self.haptics.celebration()  // ← ADD THIS
            }
        }
    }
    
    func handleCorrectAnswer() {
        haptics.correctAnswer()  // ← ADD THIS
        awardCoin()
    }
    
    func handleIncorrectAttempt() {
        haptics.softFeedback()  // ← ADD THIS
        // Show gentle hint
    }
}
```

---

### 13.4.4: Parent Dashboard Settings

Add haptic toggle in parent settings.

```swift
// File: BennieGame/Features/Parent/ParentDashboardView.swift

struct HapticSettingsSection: View {
    @StateObject private var haptics = HapticManager.shared
    
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Haptisches Feedback")
                .font(.sfRounded(size: 20, weight: .semibold))
            
            Toggle("Vibrationen aktivieren", isOn: $haptics.isEnabled)
                .font(.sfRounded(size: 17))
            
            if haptics.isEnabled {
                Button("Alle Effekte testen") {
                    haptics.testAll()
                }
                .font(.sfRounded(size: 15))
                .foregroundColor(.secondary)
            }
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 12)
                .fill(Color(hex: "FAF5EB"))
        )
    }
}
```

---

## 📋 Screen-by-Screen Haptic Map

### Loading Screen
- **No haptics** - passive loading

### Player Selection
- `buttonTap` - When player tapped

### Home Screen (Waldabenteuer)
- `buttonTap` - Activity signs
- `buttonTap` - Settings/Help
- `buttonTap` - Treasure chest (if available)

### Puzzle Matching
- `selectionChanged` - Color picker selection
- `selectionChanged` - Grid cell tap
- `correctAnswer` - Pattern complete
- `softFeedback` - (None - no wrong answers in this game)

### Labyrinth
- `selectionChanged` - Path start
- (Continuous light feedback while drawing path - optional)
- `softFeedback` - Path leaves valid route
- `correctAnswer` - Reach goal

### Numbers (Dice)
- `buttonTap` - Dice roll
- `selectionChanged` - Number selection
- `correctAnswer` - Correct number
- `softFeedback` - Wrong number

### Numbers (Choose)
- `selectionChanged` - Number traced
- `correctAnswer` - Correct trace
- `softFeedback` - Trace validation failed

### Celebration Overlay
- `celebration` - Overlay appears (triggered by GameStateManager)

### Treasure Screen
- `buttonTap` - YouTube duration buttons
- `buttonTap` - Back button

### Video Selection
- `buttonTap` - Video thumbnail

### Video Player
- (None during playback)
- `medium` - 1 minute warning
- `medium` - Time up

### Parent Gate
- `buttonTap` - Number input
- `buttonTap` - Confirm/Cancel

### Parent Dashboard
- `buttonTap` - All buttons
- `buttonTap` - Toggle switches

---

## 🧪 Testing Requirements

### Manual Testing Device

**Required**: Physical iPad (not simulator)
**Reason**: Simulator cannot generate haptics

### Test Cases

```swift
// File: BennieGameTests/HapticTests.swift

import XCTest
@testable import BennieGame

final class HapticTests: XCTestCase {
    var haptics: HapticManager!
    
    override func setUp() {
        super.setUp()
        haptics = HapticManager.shared
    }
    
    func testButtonTap() {
        // Manual verification: Should feel like gentle tap
        haptics.buttonTap()
        wait(seconds: 1)
    }
    
    func testCorrectAnswer() {
        // Manual verification: Should feel positive/successful
        haptics.correctAnswer()
        wait(seconds: 1)
    }
    
    func testCoinEarned() {
        // Manual verification: Should feel tangible/medium
        haptics.coinEarned()
        wait(seconds: 1)
    }
    
    func testSoftFeedback() {
        // Manual verification: Should feel gentle, not harsh
        haptics.softFeedback()
        wait(seconds: 1)
    }
    
    func testCelebration() {
        // Manual verification: Should feel like celebration
        haptics.celebration()
        wait(seconds: 1)
    }
    
    func testSelectionChanged() {
        // Manual verification: Should feel like selection change
        haptics.selectionChanged()
        wait(seconds: 1)
    }
    
    func testHapticsDisabled() {
        haptics.isEnabled = false
        haptics.buttonTap()
        // Manual verification: Should feel nothing
        wait(seconds: 1)
        haptics.isEnabled = true
    }
    
    private func wait(seconds: TimeInterval) {
        let expectation = XCTestExpectation()
        DispatchQueue.main.asyncAfter(deadline: .now() + seconds) {
            expectation.fulfill()
        }
        wait(for: [expectation], timeout: seconds + 1)
    }
}
```

### User Testing Protocol

**Participants**: Alexander (5, autism) & Oliver (4)

1. **Enable haptics** in parent dashboard
2. **Play through activities** with haptics on
3. **Observe reactions**: Look for any signs of overstimulation
4. **Ask questions** (if verbal): "Do you feel the iPad?"
5. **Test disabled**: Play same activities with haptics off
6. **Compare experience**: Which did they prefer?

**Success Criteria**:
- No signs of distress or overstimulation
- Haptics enhance rather than distract
- Children don't disable haptics themselves
- Parents approve of intensity levels

---

## 📊 Success Criteria

### Phase 13.4 Complete When:

1. ✅ HapticManager.swift exists with all methods
2. ✅ All components trigger appropriate haptics
3. ✅ Parent dashboard has haptic toggle
4. ✅ Test suite exists for manual verification
5. ✅ All haptics tested on physical iPad
6. ✅ Haptic intensity feels appropriate
7. ✅ Haptics can be fully disabled
8. ✅ User testing with Alexander & Oliver complete

---

## ⚠️ Critical Considerations

### Autism-Specific Concerns

Some autistic children are **hypersensitive** to haptic feedback. We must:
- Keep all haptics **gentle** and **brief**
- Make haptics **fully optional** (off by default for some users)
- **Never** use harsh or sustained vibrations
- Provide **easy access** to disable haptics
- **Test extensively** with target users

### Technical Considerations

- Haptic generators have **latency** (~50ms) - prepare them early
- **Battery impact** - haptics drain battery faster
- **Device support** - not all iPads have Taptic Engine
- **Graceful degradation** - app must work without haptics

---

## 🔗 Integration Points

### Services Updates
- Create HapticManager singleton
- Integrate with GameStateManager

### Component Updates
- WoodButton: Add haptic on tap
- PuzzleGridCell: Add haptic on selection
- All interactive elements: Appropriate haptic

### Settings Updates
- Parent Dashboard: Haptic toggle
- Persist setting across launches
- Test all haptics function

---

## 📚 References

### Playbook
- Section 5.7: Accessibility - Haptic Feedback
- Section 1.4: Brand Personality (warm, gentle, safe)

### Apple Documentation
- [Human Interface Guidelines: Haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics)
- [UIFeedbackGenerator](https://developer.apple.com/documentation/uikit/uifeedbackgenerator)

### Autism Resources
- [Sensory Processing in Autism](https://www.autism.org.uk/advice-and-guidance/topics/sensory-differences)

---

*Phase Owner*: Development Team
*Playbook Compliance*: Section 5.7
*User Testing Required*: Yes
*Last Updated*: 2026-01-11
