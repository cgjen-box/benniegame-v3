# Celebration Overlay Implementation

**📚 Playbook Reference**: [FULL_ARCHIVE.md Part 4.7](../../docs/playbook/FULL_ARCHIVE.md#47-celebration-overlay)  
**🎨 Design Reference**: [Reference_Celebration_Overlay.png](../../design/references/screens/Reference_Celebration_Overlay.png)  
**🐻 Character Assets Required**:
- [bennie_celebrating.png](../../design/references/character/bennie/bennie_celebrating.png) - Bennie with arms raised
- [lemminge_celebrating.png](../../design/references/character/lemminge/lemminge_celebrating.png) - Lemminge jumping

**🧩 Component Dependencies**:
- [WoodButton](../../Design/Components/WoodButton.swift) - For "Weiter" button
- [BennieView](../../Design/Characters/BennieView.swift) - Character display
- [LemmingeView](../../Design/Characters/LemmingeView.swift) - Character display

**🎬 Animation Assets**:
- [confetti.json](../../Resources/Lottie/confetti.json) - Full-screen confetti
- [bennie_celebrating.json](../../Resources/Lottie/bennie_celebrating.json) - Jump animation
- [lemminge_celebrating.json](../../Resources/Lottie/lemminge_celebrating.json) - Jump animation

**🔊 Audio Files Required**:
- `bennie_celebration_5.aac` - "Wir haben schon fünf Goldmünzen!"
- `bennie_celebration_10.aac` - "Zehn Goldmünzen! Du kannst jetzt YouTube schauen."
- `bennie_celebration_15.aac` - "Fünfzehn! Weiter so!"
- `bennie_celebration_20.aac` - "Zwanzig Münzen! Du bekommst Bonuszeit!"
- `bennie_celebration_general.aac` - "Super! Noch mehr Münzen!"

---

## 🎉 Overview

The celebration overlay appears at **5-coin milestones** (5, 10, 15, 20, 25...) as a transparent layer over the activity screen to keep context and avoid jarring transitions.

## Critical Design Principle

> **Playbook Section**: Part 4.7 - Design Principle

```
╔══════════════════════════════════════════════════════════════════════╗
║              CELEBRATION IS AN OVERLAY, NOT A SCREEN                 ║
║                                                                      ║
║  This keeps the child grounded in context—they see what they         ║
║  accomplished while receiving praise. No jarring screen transitions. ║
║                                                                      ║
║  ✅ Context preservation – Child sees their completed work            ║
║  ✅ No jarring transitions – Predictable, calm experience             ║
║  ✅ Immediate feedback – Success feels connected to action            ║
║  ✅ Autism-friendly – Reduces disorientation from screen changes      ║
╚══════════════════════════════════════════════════════════════════════╝
```

## Trigger Logic

> **Playbook Reference**: Part 4.7 - Trigger Condition

```swift
struct CoinManager: ObservableObject {
    @Published var currentCoins: Int = 0
    @Published var showCelebration: Bool = false
    
    func awardCoin() {
        currentCoins += 1
        
        // Trigger celebration at 5-coin milestones
        // Playbook: "ONLY show at 5-coin milestones: 5, 10, 15, 20, 25..."
        if currentCoins % 5 == 0 && currentCoins > 0 {
            showCelebration = true
            playBennieVoice(for: currentCoins)
            triggerHaptic(.success)
        }
    }
    
    private func playBennieVoice(for coins: Int) {
        let voiceFile: String
        switch coins {
        case 5: voiceFile = "bennie_celebration_5.aac"
        case 10: voiceFile = "bennie_celebration_10.aac"
        case 15: voiceFile = "bennie_celebration_15.aac"
        case 20: voiceFile = "bennie_celebration_20.aac"
        default: voiceFile = "bennie_celebration_general.aac"
        }
        
        AudioManager.shared.playBennie(voiceFile)
    }
}
```

## Visual Components

> **Design Reference**: See Reference_Celebration_Overlay.png for exact layout

### 1. Dimmed Background
```swift
struct CelebrationBackgroundDimmer: View {
    var body: some View {
        // Playbook: "Activity screen visible (dimmed to 40% brightness)"
        Color.black
            .opacity(0.6)
            .ignoresSafeArea()
            .transition(.opacity)
    }
}
```

### 2. Celebration Card

> **Color References**: Uses BennieColors from Part 1.3 Color System
> - Cream background: `#FAF5EB` @ 90% opacity
> - Bark text: `#8C7259`
> - CoinGold: `#D9C27A`

```swift
struct CelebrationCard: View {
    let coins: Int
    @Binding var isShowing: Bool
    
    var body: some View {
        VStack(spacing: 24) {
            // Title
            Text("Super gemacht!")
                .font(.sfRounded(size: 36, weight: .bold))
                .foregroundColor(BennieColors.bark)
            
            // Coin display
            HStack {
                Image("coin")
                    .resizable()
                    .frame(width: 60, height: 60)
                Text("+1")
                    .font(.sfRounded(size: 48, weight: .bold))
                    .foregroundColor(BennieColors.coinGold)
            }
            
            // Characters celebrating
            // Playbook: "Three Lemminge jumping"
            HStack(spacing: 20) {
                ForEach(0..<3, id: \.self) { _ in
                    LottieView(animation: "lemminge_celebrating")
                        .frame(width: 80, height: 100)
                }
            }
            
            // Playbook: "Bennie celebrating with arms raised"
            BennieView(expression: .celebrating)
                .frame(width: 200, height: 300)
            
            // Continue button
            // Playbook: "Must tap 'Weiter' - Never auto-dismiss"
            WoodButton(text: "Weiter →") {
                withAnimation {
                    isShowing = false
                    checkForTreasureNavigation()
                }
            }
        }
        .padding(40)
        .background(
            RoundedRectangle(cornerRadius: 24)
                .fill(BennieColors.cream.opacity(0.95))
                .shadow(radius: 20)
        )
        .frame(width: 600)
    }
    
    func checkForTreasureNavigation() {
        // Playbook: "At 10 coins, automatically navigate to treasure screen"
        if coins >= 10 {
            NavigationCoordinator.shared.navigate(to: .treasure)
        }
    }
}
```

### 3. Confetti Animation

> **Animation Asset**: confetti.json (Lottie, 3s duration, non-looping)

```swift
struct ConfettiLayer: View {
    @State private var isAnimating = false
    
    var body: some View {
        LottieView(animation: "confetti", loopMode: .playOnce)
            .ignoresSafeArea()
            .allowsHitTesting(false) // Don't block touches
    }
}
```

## Complete Overlay Implementation

> **Playbook**: Part 4.7 - Layout (Transparent Overlay)

```swift
struct CelebrationOverlay: View {
    @Binding var isShowing: Bool
    let coins: Int
    
    var body: some View {
        ZStack {
            // Dimmed background
            CelebrationBackgroundDimmer()
            
            // Confetti over everything
            ConfettiLayer()
            
            // Celebration card
            CelebrationCard(coins: coins, isShowing: $isShowing)
                .transition(.scale(scale: 0.8).combined(with: .opacity))
        }
        // Playbook: "Entry animation: Scale 0.8→1.0, spring ease, 0.4s"
        .animation(.spring(response: 0.4, dampingFraction: 0.8), value: isShowing)
    }
}
```

## Usage in Activity Screens

```swift
struct PuzzleMatchingView: View {
    @StateObject private var coinManager = CoinManager()
    
    var body: some View {
        ZStack {
            // Activity content
            ActivityContent()
            
            // Celebration overlay
            if coinManager.showCelebration {
                CelebrationOverlay(
                    isShowing: $coinManager.showCelebration,
                    coins: coinManager.currentCoins
                )
            }
        }
    }
}
```

## Voice Lines by Milestone

> **Playbook Reference**: Part 3.4 - Celebration Overlay Script

| Coins | German Text | File Name | Duration | Playbook Ref |
|-------|-------------|-----------|----------|--------------|
| 5 | "Wir haben schon fünf Goldmünzen!" | bennie_celebration_5.aac | 2s | Part 3.4 |
| 10 | "Zehn Goldmünzen! Du kannst jetzt YouTube schauen." | bennie_celebration_10.aac | 3s | Part 3.4 |
| 15 | "Fünfzehn! Weiter so!" | bennie_celebration_15.aac | 2s | Part 3.4 |
| 20 | "Zwanzig Münzen! Du bekommst Bonuszeit!" | bennie_celebration_20.aac | 3s | Part 3.4 |
| 25+ | "Super! Noch mehr Münzen!" | bennie_celebration_general.aac | 2s | Part 3.4 |

## Haptic Feedback

> **Playbook**: Part 5.7 - Accessibility - Haptic Feedback

```swift
func triggerHaptic(_ type: UINotificationFeedbackGenerator.FeedbackType) {
    let generator = UINotificationFeedbackGenerator()
    generator.notificationOccurred(type)
}

// Usage - Playbook: "Heavy impact for celebration"
triggerHaptic(.success)
```

## Testing Checklist

> **Playbook Reference**: Part 10.2 - QA Verification Matrix

```
TRIGGER LOGIC:
□ Overlay appears only at 5, 10, 15, 20, 25... coins
□ Does NOT appear at 1, 2, 3, 4, 6, 7, 8, 9... coins

VISUAL:
□ Activity screen visible (dimmed) beneath overlay
□ Confetti animation plays once (3s duration)
□ Bennie celebrates with proper animation (arms raised)
□ Three Lemminge jump in celebration
□ Correct voice line plays for milestone
□ "Weiter" button dismisses overlay
□ Overlay scales from 0.8 to 1.0 on appear
□ Spring animation with 0.4s duration

BEHAVIOR:
□ At 10+ coins, auto-navigates to treasure screen after dismiss
□ At <10 coins, returns to activity
□ No frame drops during animation (60fps maintained)
□ Haptic feedback triggers on appearance
□ Memory usage stays under 200MB

ACCESSIBILITY:
□ VoiceOver announces milestone correctly
□ Touch targets ≥ 96pt (Weiter button)
□ Overlay scales properly on all iPad sizes
□ Color contrast meets 4.5:1 minimum
```

## Performance Considerations

> **Playbook**: Part 5.6 - Performance Requirements

```swift
// Preload Lottie animations to prevent frame drops
class LottieCache {
    static let shared = LottieCache()
    
    private var animations: [String: LottieAnimation] = [:]
    
    func preload() {
        // Playbook: "Preload during loading screen"
        animations["confetti"] = LottieAnimation.named("confetti")
        animations["bennie_celebrating"] = LottieAnimation.named("bennie_celebrating")
        animations["lemminge_celebrating"] = LottieAnimation.named("lemminge_celebrating")
    }
    
    func get(_ name: String) -> LottieAnimation? {
        return animations[name]
    }
}
```

## Accessibility

> **Playbook**: Part 5.7 - VoiceOver Support

```swift
// VoiceOver support - Playbook: "Accessibility Label (German)"
.accessibilityElement(children: .combine)
.accessibilityLabel("Du hast \(coins) Münzen gesammelt! Super gemacht!")
.accessibilityHint("Tippe Weiter um fortzufahren")
```

---

## 📋 Implementation Checklist

**Phase 5A - Celebration Overlay**:
- [ ] Create CelebrationOverlay.swift
- [ ] Import confetti.json Lottie animation
- [ ] Import bennie_celebrating.json animation
- [ ] Import lemminge_celebrating.json animation
- [ ] Record all 5 voice lines with ElevenLabs
- [ ] Add to CoinManager trigger logic
- [ ] Test on all activity screens
- [ ] Verify accessibility with VoiceOver
- [ ] Performance test (60fps, <200MB)
- [ ] Test navigation to treasure at 10+ coins

**Asset Dependencies**:
- [ ] Reference_Celebration_Overlay.png reviewed
- [ ] bennie_celebrating.png (static)
- [ ] lemminge_celebrating.png (static)
- [ ] All voice files recorded and imported

**Integration Points**:
- [ ] PuzzleMatchingView
- [ ] LabyrinthView
- [ ] WürfelView
- [ ] WähleZahlView
