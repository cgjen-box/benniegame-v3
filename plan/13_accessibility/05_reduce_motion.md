# Phase 13.5: Reduce Motion Support

**Status**: 🔵 Not Started
**Priority**: Critical
**Estimated Time**: 2 days
**Dependencies**: Phase 6 (Animation & Sound)

---

## 📋 Overview

Implement animation fallbacks for users with motion sensitivity, ensuring the app remains fully functional with reduced motion enabled.

**Playbook Reference**: `C:\Users\christoph\Bennie und die Lemminge v3\docs\playbook\06-animation-sound.md` Section 6.1 "Animation Principles"

---

## 🎯 Requirements from Playbook

**Forbidden Animations** (Section 6.1):

| Animation | Reason | Always Forbidden |
|-----------|--------|------------------|
| Flashing | Seizure risk | ✅ |
| Shaking | Anxiety trigger | ✅ |
| Fast strobing | Overstimulating | ✅ |
| Sudden movements | Startling | ✅ |
| Rapid color changes | Disorienting | ✅ |
| Bouncing text | Distracting | ✅ |

**Reduce Motion Alternative**: Crossfades, fades, and position changes only.

---

## 🎯 Implementation Plan

### 13.5.1: Motion Detection Utility

Create system to detect reduce motion setting.

```swift
// File: BennieGame/Services/MotionManager.swift

import SwiftUI

final class MotionManager: ObservableObject {
    static let shared = MotionManager()
    
    @Published var reduceMotionEnabled: Bool
    
    private init() {
        // Check system setting
        self.reduceMotionEnabled = UIAccessibility.isReduceMotionEnabled
        
        // Listen for changes
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(reduceMotionChanged),
            name: UIAccessibility.reduceMotionStatusDidChangeNotification,
            object: nil
        )
    }
    
    @objc private func reduceMotionChanged() {
        reduceMotionEnabled = UIAccessibility.isReduceMotionEnabled
    }
    
    // MARK: - Animation Helpers
    
    /// Returns appropriate animation for current motion setting
    func animation(_ standard: Animation, reduced: Animation? = nil) -> Animation {
        if reduceMotionEnabled {
            return reduced ?? .linear(duration: 0.2)
        } else {
            return standard
        }
    }
    
    /// Conditionally animate based on motion setting
    func withAnimation<Result>(
        _ standard: Animation,
        reduced: Animation? = nil,
        _ body: () throws -> Result
    ) rethrows -> Result {
        if reduceMotionEnabled {
            return try SwiftUI.withAnimation(reduced ?? .linear(duration: 0.2), body)
        } else {
            return try SwiftUI.withAnimation(standard, body)
        }
    }
}

// MARK: - View Extension

extension View {
    /// Apply animation that respects reduce motion
    func motionSafeAnimation(
        _ standard: Animation,
        reduced: Animation? = nil,
        value: some Equatable
    ) -> some View {
        let motion = MotionManager.shared
        return self.animation(
            motion.animation(standard, reduced: reduced),
            value: value
        )
    }
}
```

---

### 13.5.2: Animation Fallbacks

Define fallback animations for each type.

```swift
// File: BennieGame/Design/Theme/BennieAnimations.swift

extension Animation {
    // MARK: - Motion-Safe Animations
    
    /// Button press animation
    static var bennieButtonPress: Animation {
        if MotionManager.shared.reduceMotionEnabled {
            return .linear(duration: 0.1)
        } else {
            return .spring(response: 0.3, dampingFraction: 0.6)
        }
    }
    
    /// Screen transition animation
    static var bennieScreenTransition: Animation {
        if MotionManager.shared.reduceMotionEnabled {
            return .linear(duration: 0.2)
        } else {
            return .easeInOut(duration: 0.3)
        }
    }
    
    /// Coin fly animation
    static var bennieCoinFly: Animation {
        if MotionManager.shared.reduceMotionEnabled {
            // Simple fade + position change
            return .linear(duration: 0.3)
        } else {
            // Arc animation
            return .spring(response: 0.8, dampingFraction: 0.7)
        }
    }
    
    /// Celebration animation
    static var bennieCelebration: Animation {
        if MotionManager.shared.reduceMotionEnabled {
            // Simple scale + fade
            return .linear(duration: 0.4)
        } else {
            // Bounce celebration
            return .spring(response: 0.4, dampingFraction: 0.5)
        }
    }
    
    /// Idle breathing animation
    static var bennieBreathing: Animation {
        if MotionManager.shared.reduceMotionEnabled {
            // No breathing animation
            return .linear(duration: 0)
        } else {
            // Gentle breathing loop
            return .easeInOut(duration: 2.0).repeatForever(autoreverses: true)
        }
    }
}
```

---

### 13.5.3: Character Animation Fallbacks

Update character views with reduce motion support.

```swift
// File: BennieGame/Design/Characters/BennieView.swift

struct BennieView: View {
    let expression: BennieExpression
    @StateObject private var motion = MotionManager.shared
    @State private var scale: CGFloat = 1.0
    
    var body: some View {
        Image("bennie_\(expression.rawValue)")
            .resizable()
            .aspectRatio(contentMode: .fit)
            .scaleEffect(motion.reduceMotionEnabled ? 1.0 : scale)
            .onAppear {
                if !motion.reduceMotionEnabled {
                    // Gentle breathing animation
                    withAnimation(.bennieBreathing) {
                        scale = 1.03
                    }
                }
            }
    }
}
```

```swift
// File: BennieGame/Design/Characters/LemmingeView.swift

struct LemmingeView: View {
    let expression: LemmingeExpression
    @StateObject private var motion = MotionManager.shared
    @State private var offset: CGFloat = 0
    
    var body: some View {
        Image("lemminge_\(expression.rawValue)")
            .resizable()
            .aspectRatio(contentMode: .fit)
            .offset(y: motion.reduceMotionEnabled ? 0 : offset)
            .onAppear {
                if !motion.reduceMotionEnabled && expression == .excited {
                    // Gentle bounce animation
                    withAnimation(.easeInOut(duration: 0.5).repeatForever(autoreverses: true)) {
                        offset = -10
                    }
                }
            }
    }
}
```

---

### 13.5.4: Screen Transition Fallbacks

Update navigation transitions.

```swift
// File: BennieGame/App/AppCoordinator.swift

struct AppCoordinator: View {
    @StateObject private var motion = MotionManager.shared
    @State private var currentScreen: GameScreen = .loading
    
    var body: some View {
        ZStack {
            currentScreenView
        }
        .transition(motion.reduceMotionEnabled ? .opacity : .asymmetric(
            insertion: .move(edge: .trailing).combined(with: .opacity),
            removal: .move(edge: .leading).combined(with: .opacity)
        ))
    }
    
    func navigateTo(_ screen: GameScreen) {
        motion.withAnimation(.bennieScreenTransition) {
            currentScreen = screen
        }
    }
}
```

---

### 13.5.5: Coin Fly Animation Fallback

Simplify coin animation for reduce motion.

```swift
// File: BennieGame/Features/Activities/Components/CoinFlyAnimation.swift

struct CoinFlyAnimation: View {
    let from: CGPoint
    let to: CGPoint
    let onComplete: () -> Void
    
    @StateObject private var motion = MotionManager.shared
    @State private var position: CGPoint
    @State private var opacity: Double = 1.0
    
    init(from: CGPoint, to: CGPoint, onComplete: @escaping () -> Void) {
        self.from = from
        self.to = to
        self.onComplete = onComplete
        self._position = State(initialValue: from)
    }
    
    var body: some View {
        Image("coin")
            .resizable()
            .frame(width: 40, height: 40)
            .position(position)
            .opacity(opacity)
            .onAppear {
                if motion.reduceMotionEnabled {
                    // Simple fade + move
                    withAnimation(.linear(duration: 0.3)) {
                        position = to
                        opacity = 0
                    }
                    DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
                        onComplete()
                    }
                } else {
                    // Arc path animation
                    let midPoint = CGPoint(
                        x: (from.x + to.x) / 2,
                        y: min(from.y, to.y) - 100
                    )
                    withAnimation(.spring(response: 0.8, dampingFraction: 0.7)) {
                        position = midPoint
                    }
                    DispatchQueue.main.asyncAfter(deadline: .now() + 0.4) {
                        withAnimation(.spring(response: 0.4, dampingFraction: 0.9)) {
                            position = to
                            opacity = 0
                        }
                    }
                    DispatchQueue.main.asyncAfter(deadline: .now() + 0.8) {
                        onComplete()
                    }
                }
            }
    }
}
```

---

### 13.5.6: Celebration Overlay Fallback

Simplify celebration for reduce motion.

```swift
// File: BennieGame/Features/Celebration/CelebrationOverlay.swift

struct CelebrationOverlay: View {
    @StateObject private var motion = MotionManager.shared
    @State private var isVisible = false
    
    var body: some View {
        ZStack {
            // Background dim
            Color.black.opacity(0.3)
            
            // Celebration card
            VStack(spacing: 20) {
                Text("Super gemacht!")
                    .font(.sfRounded(size: 32, weight: .bold))
                
                Image("coin")
                    .resizable()
                    .frame(width: 60, height: 60)
                
                // Characters
                HStack(spacing: 20) {
                    BennieView(expression: .celebrating)
                        .frame(height: 150)
                    LemmingeView(expression: .celebrating)
                        .frame(height: 80)
                    LemmingeView(expression: .celebrating)
                        .frame(height: 80)
                }
                
                WoodButton(text: "Weiter →", action: {})
            }
            .padding(40)
            .background(
                RoundedRectangle(cornerRadius: 24)
                    .fill(Color(hex: "FAF5EB").opacity(0.95))
            )
            .scaleEffect(isVisible ? 1.0 : (motion.reduceMotionEnabled ? 1.0 : 0.8))
            .opacity(isVisible ? 1.0 : 0)
            
            // Confetti (only if motion enabled)
            if !motion.reduceMotionEnabled {
                ConfettiView()
            }
        }
        .onAppear {
            withAnimation(.bennieCelebration) {
                isVisible = true
            }
        }
    }
}
```

---

## 📋 Animation Audit Checklist

### For Each Animation in App:

- [ ] **Has reduce motion fallback** defined
- [ ] **Fallback is functional** (not just disabled)
- [ ] **Fallback provides equivalent UX** (no information loss)
- [ ] **Fallback is tested** on device with reduce motion enabled
- [ ] **Duration is appropriate** (0.2-0.4s for fallbacks)

### Screens to Audit:

- [ ] Loading Screen: Loading progress, Bennie wave
- [ ] Player Selection: Button press, selection highlight
- [ ] Home Screen: Activity sign swing, character animations
- [ ] Puzzle Matching: Cell selection, pattern complete
- [ ] Labyrinth: Path drawing, completion
- [ ] Numbers: Dice roll, number selection
- [ ] Celebration: Overlay appearance, confetti
- [ ] Treasure: Chest open, button press
- [ ] Video Player: Clock animation

---

## 🧪 Testing Requirements

### Enable Reduce Motion on iPad

**Path**: Settings → Accessibility → Motion → Reduce Motion → ON

### Test Cases

```swift
// File: BennieGameTests/ReduceMotionTests.swift

import XCTest
@testable import BennieGame

final class ReduceMotionTests: XCTestCase {
    var motion: MotionManager!
    
    override func setUp() {
        super.setUp()
        motion = MotionManager.shared
    }
    
    func testReduceMotionDetection() {
        // Manual: Toggle reduce motion in Settings
        // Verify motion.reduceMotionEnabled changes
        print("Reduce Motion Enabled: \(motion.reduceMotionEnabled)")
    }
    
    func testButtonAnimation() {
        let standardAnimation = Animation.bennieButtonPress
        // Should return linear animation when reduce motion is on
        // Should return spring animation when reduce motion is off
    }
    
    func testCelebrationAnimation() {
        // Manual: Trigger celebration with reduce motion on/off
        // Verify: No bouncing with reduce motion on
        // Verify: Bouncing with reduce motion off
    }
    
    func testCoinFlyAnimation() {
        // Manual: Earn coin with reduce motion on/off
        // Verify: Simple path with reduce motion on
        // Verify: Arc path with reduce motion off
    }
    
    func testCharacterBreathing() {
        // Manual: View Bennie with reduce motion on/off
        // Verify: No breathing with reduce motion on
        // Verify: Breathing with reduce motion off
    }
}
```

### User Testing Protocol

1. **Enable reduce motion** on iPad
2. **Play through entire game** with reduce motion on
3. **Verify all functionality** works correctly
4. **Check for information loss** (no feedback missing)
5. **Disable reduce motion** and compare experience
6. **Document differences** and verify equivalence

---

## 📊 Success Criteria

### Phase 13.5 Complete When:

1. ✅ MotionManager.swift exists and detects system setting
2. ✅ BennieAnimations.swift has fallbacks for all animations
3. ✅ All character views respect reduce motion
4. ✅ All screen transitions have fallbacks
5. ✅ Coin fly animation has simple fallback
6. ✅ Celebration overlay has simple fallback
7. ✅ All animations tested with reduce motion on
8. ✅ No information or functionality lost with reduce motion

---

## ⚠️ Critical Guidelines

### What Reduce Motion Is NOT

- ❌ **NOT**: Disabling all animations
- ❌ **NOT**: Making the app boring
- ❌ **NOT**: Removing functionality

### What Reduce Motion IS

- ✅ **IS**: Simplifying motion to prevent discomfort
- ✅ **IS**: Using crossfades instead of slides
- ✅ **IS**: Using position changes instead of complex paths
- ✅ **IS**: Maintaining full functionality and information

### Design Philosophy

> "Reduce motion should feel like the calm, gentle version of the app—
> not a broken or inferior version."

---

## 🔗 Integration Points

### Services Updates
- Create MotionManager singleton
- Detect system reduce motion setting
- Provide animation helper methods

### Animation Updates
- BennieAnimations: Add fallbacks for all
- Character views: Respect reduce motion
- Transition views: Simple fallbacks

### Testing Updates
- Test all animations with reduce motion on
- Verify functionality equivalence
- Document differences

---

## 📚 References

### Playbook
- Section 6.1: Animation Principles
- Section 6.2: Transition Animations
- Section 0.1: Game Philosophy (avoid over-stimulation)

### Design References
- All screens: Verify animations can be simplified

### Apple Documentation
- [Human Interface Guidelines: Motion](https://developer.apple.com/design/human-interface-guidelines/accessibility#Motion)
- [UIAccessibility.isReduceMotionEnabled](https://developer.apple.com/documentation/uikit/uiaccessibility/1615133-isreducemotionenabled)

---

*Phase Owner*: Development Team
*Playbook Compliance*: Section 6.1
*Last Updated*: 2026-01-11
