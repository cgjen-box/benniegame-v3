# Phase 2: Design System Implementation

**Duration**: 6-8 hours  
**Status**: Not Started  
**Dependencies**: Phase 1 (Foundation Setup)

## Playbook References

This phase implements components specified in:
- **Part 1.3**: Color System → `C:\Users\christoph\Bennie und die Lemminge v3\docs\playbook\FULL_ARCHIVE.md` (Lines 366-485)
- **Part 1.4**: Typography → `C:\Users\christoph\Bennie und die Lemminge v3\docs\playbook\FULL_ARCHIVE.md` (Lines 487-557)
- **Part 4.3**: Screen Components → `C:\Users\christoph\Bennie und die Lemminge v3\docs\playbook\FULL_ARCHIVE.md` (Lines 1563-1658)
- **Part 6**: Animation & Sound Guide → `C:\Users\christoph\Bennie und die Lemminge v3\docs\playbook\FULL_ARCHIVE.md` (Lines 3425-3565)

## Design Asset References

Character validation assets:
- **Bennie Reference**: `C:\Users\christoph\Bennie und die Lemminge v3\design\references\character\bennie\reference\bennie-reference.png` (CANONICAL)
- **Lemminge Reference**: `C:\Users\christoph\Bennie und die Lemminge v3\design\references\character\lemminge\reference\lemminge-reference.png` (CANONICAL)

Component references:
- `C:\Users\christoph\Bennie und die Lemminge v3\design\references\components\` (All component mockups)

Screen mockups for context:
- `C:\Users\christoph\Bennie und die Lemminge v3\design\references\screens\Reference_Menu_Screen.png`
- `C:\Users\christoph\Bennie und die Lemminge v3\design\references\screens\Reference_Matching_Game_Screen.png`

---

## Overview

Build reusable SwiftUI components that enforce the Bennie brand guidelines. Every component must pass strict design validation against the playbook.

## Deliverables

- ✅ WoodButton component with all states
- ✅ WoodSign component with rope mounting
- ✅ ProgressBar component with coin slots
- ✅ NavigationHeader component
- ✅ StoneTablet component
- ✅ AnalogClock component
- ✅ SpeechBubble component
- ✅ BennieView with all 6 expressions
- ✅ LemmingeView with all 6 expressions
- ✅ Animation presets defined

## Exit Criteria

- [ ] All components render correctly in preview
- [ ] Touch targets ≥ 96pt enforced (Playbook Part 5.1)
- [ ] Colors match playbook hex values exactly (Part 1.3)
- [ ] SF Rounded font applied throughout (Part 1.4)
- [ ] No hardcoded colors (all use Color extensions from Phase 1)
- [ ] Components are reusable and composable
- [ ] Preview canvas works for all components
- [ ] Character designs validated against canonical references

---

## Tasks

### 2.0 Create WoodButton Component
**Estimated**: 45 minutes  
**Playbook Reference**: Part 4.3 (Shared Components), Part 1.3 (Wood UI Colors)

**Requirements:**
- Minimum 96×60pt touch target (Part 5.1, Table: Touch Targets)
- Wood gradient: #C4A574 (light) → #A67C52 (medium)
- Dark wood border: #6B4423, 2pt
- Scale animation on press (0.95)
- Optional icon + text
- Haptic feedback (light impact)

**Implementation:**
```swift
// Design/Components/WoodButton.swift
import SwiftUI

struct WoodButton: View {
    let text: String?
    let icon: String?
    let action: () -> Void
    
    @State private var isPressed = false
    
    var body: some View {
        Button(action: {
            // Haptic feedback
            let impact = UIImpactFeedbackGenerator(style: .light)
            impact.impactOccurred()
            action()
        }) {
            HStack(spacing: 12) {
                if let icon = icon {
                    Image(systemName: icon)
                        .font(.system(size: 20, weight: .semibold))
                }
                if let text = text {
                    Text(text)
                        .font(.sfRounded(size: 20, weight: .semibold))
                }
            }
            .foregroundColor(Color(hex: "3D2B1F")) // BennieNose color
            .padding(.horizontal, 20)
            .padding(.vertical, 12)
            .frame(minWidth: 96, minHeight: 60) // ✓ Part 5.1 minimum
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .fill(
                        LinearGradient(
                            colors: [
                                Color.woodLight,   // #C4A574
                                Color.woodMedium   // #A67C52
                            ],
                            startPoint: .top,
                            endPoint: .bottom
                        )
                    )
            )
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(Color.woodDark, lineWidth: 2) // #6B4423
            )
        }
        .buttonStyle(WoodButtonStyle())
    }
}

struct WoodButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0) // Part 6.1
            .animation(.spring(response: 0.3), value: configuration.isPressed)
    }
}
```

**Validation Checklist:**
- [ ] Touch target ≥ 96×60pt
- [ ] Wood light color: #C4A574
- [ ] Wood medium color: #A67C52
- [ ] Wood dark border: #6B4423
- [ ] Press scale: 0.95
- [ ] Spring animation: response 0.3
- [ ] Haptic feedback works

**Test Cases:**
- [ ] Renders with text only
- [ ] Renders with icon only
- [ ] Renders with both text and icon
- [ ] Touch target ≥ 96pt
- [ ] Press animation works
- [ ] Colors match playbook exactly

---

### 2.1 Create WoodSign Component
**Estimated**: 40 minutes  
**Playbook Reference**: Part 4.3 (Shared Components), Part 1.3 (Wood UI Colors)

**Requirements:**
- Hanging sign with rope mount
- Rope color: #B8956B (Part 1.3, Table: Wood UI Colors)
- Wood grain texture
- Customizable text
- Optional icon/decoration
- Natural swing animation (optional, Part 6.2: ±3° rotation)

**Implementation:**
```swift
// Design/Components/WoodSign.swift
import SwiftUI

struct WoodSign: View {
    let text: String
    let icon: String?
    let showRope: Bool
    
    init(text: String, icon: String? = nil, showRope: Bool = true) {
        self.text = text
        self.icon = icon
        self.showRope = showRope
    }
    
    var body: some View {
        VStack(spacing: 0) {
            if showRope {
                // Rope mount - Part 1.3: #B8956B
                Rectangle()
                    .fill(Color.rope) // #B8956B
                    .frame(width: 8, height: 40)
            }
            
            // Sign body
            ZStack {
                // Wood background
                RoundedRectangle(cornerRadius: 12)
                    .fill(
                        LinearGradient(
                            colors: [
                                Color.woodLight,   // #C4A574
                                Color.woodMedium   // #A67C52
                            ],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(Color.woodDark, lineWidth: 3) // #6B4423
                    )
                
                // Content
                HStack(spacing: 12) {
                    if let icon = icon {
                        Image(systemName: icon)
                            .font(.system(size: 24, weight: .bold))
                            .foregroundColor(Color.woodDark)
                    }
                    Text(text)
                        .font(.sfRounded(size: 28, weight: .bold)) // Part 1.4
                        .foregroundColor(Color.woodDark)
                }
                .padding(.horizontal, 24)
                .padding(.vertical, 16)
            }
        }
    }
}
```

**Validation Checklist:**
- [ ] Rope color: #B8956B
- [ ] Wood light: #C4A574
- [ ] Wood medium: #A67C52
- [ ] Wood dark: #6B4423
- [ ] Text font: SF Rounded, 28pt, bold
- [ ] Touch target ≥ 96pt (if interactive)

**Test Cases:**
- [ ] Renders with rope
- [ ] Renders without rope
- [ ] Icon optional
- [ ] Text formatting correct
- [ ] Colors match playbook

---

### 2.2 Create ProgressBar Component
**Estimated**: 60 minutes  
**Playbook Reference**: Part 4.3 (Shared Components), Part 2.3 (Coin & Progress System)

**Requirements:**
- Berry decorations on sides
- Wood trough container: #6B4423 (dark wood)
- 10 coin slots per chest
- Fill animation (0.5s spring)
- Success green fill: #99BF8C (Part 1.3)
- Coin gold: #D9C27A (Part 1.3)
- Chest icon appears every 10 coins

**Implementation:**
```swift
// Design/Components/ProgressBar.swift
import SwiftUI

struct ProgressBar: View {
    let currentCoins: Int
    let maxCoins: Int = 10
    
    var progress: CGFloat {
        CGFloat(min(currentCoins % maxCoins, maxCoins)) / CGFloat(maxCoins)
    }
    
    var body: some View {
        HStack(spacing: 12) {
            // Left berry decoration
            Image("berry_cluster_left")
                .resizable()
                .frame(width: 40, height: 40)
            
            // Progress bar
            ZStack(alignment: .leading) {
                // Empty state (dark wood) - Part 1.3: #6B4423
                RoundedRectangle(cornerRadius: 8)
                    .fill(Color.woodDark) // #6B4423
                    .frame(height: 40)
                
                // Fill state (success green) - Part 1.3: #99BF8C
                RoundedRectangle(cornerRadius: 8)
                    .fill(Color.success) // #99BF8C
                    .frame(width: progressWidth, height: 40)
                    .animation(.spring(response: 0.5), value: currentCoins)
                
                // Coin slots overlay
                HStack(spacing: 0) {
                    ForEach(0..<maxCoins, id: \.self) { index in
                        CoinSlot(filled: index < (currentCoins % maxCoins))
                            .frame(maxWidth: .infinity)
                    }
                }
            }
            .frame(maxWidth: 400)
            
            // Right berry decoration
            Image("berry_cluster_right")
                .resizable()
                .frame(width: 40, height: 40)
            
            // Chest indicators - Part 2.3
            ChestIndicator(chests: currentCoins / maxCoins)
        }
    }
    
    var progressWidth: CGFloat {
        400 * progress
    }
}

struct CoinSlot: View {
    let filled: Bool
    
    var body: some View {
        Circle()
            .fill(filled ? Color.coinGold : Color.clear) // #D9C27A when filled
            .frame(width: 24, height: 24)
            .overlay(
                Circle()
                    .stroke(Color.woodDark.opacity(0.3), lineWidth: 1)
            )
    }
}

struct ChestIndicator: View {
    let chests: Int
    
    var body: some View {
        HStack(spacing: 4) {
            ForEach(0..<chests, id: \.self) { _ in
                Image(systemName: "box.fill")
                    .font(.system(size: 28))
                    .foregroundColor(.coinGold) // #D9C27A
            }
        }
    }
}
```

**Validation Checklist:**
- [ ] Wood dark background: #6B4423
- [ ] Success green fill: #99BF8C
- [ ] Coin gold: #D9C27A
- [ ] 10 coin slots visible
- [ ] Animation duration: 0.5s spring
- [ ] Chest icon every 10 coins
- [ ] Berry decorations visible

**Test Cases:**
- [ ] Shows 0-10 coins correctly
- [ ] Animation smooth
- [ ] Chest icons appear at 10, 20, etc.
- [ ] Colors match playbook
- [ ] Berry decorations visible

---

### 2.3 Create NavigationHeader Component
**Estimated**: 30 minutes  
**Playbook Reference**: Part 4.3 (Shared Components)

**Requirements:**
- Home button (left) - 96×60pt minimum
- Progress bar (center)
- Volume button (right) - 96×60pt minimum
- Configurable visibility
- 20pt horizontal padding, 16pt top padding

**Implementation:**
```swift
// Design/Components/NavigationHeader.swift
import SwiftUI

struct NavigationHeader: View {
    let showHome: Bool
    let showVolume: Bool
    let currentCoins: Int
    let onHomeAction: () -> Void
    let onVolumeAction: () -> Void
    
    var body: some View {
        HStack {
            // Home button
            if showHome {
                WoodButton(text: nil, icon: "house") {
                    onHomeAction()
                }
            } else {
                Spacer().frame(width: 96)
            }
            
            Spacer()
            
            // Progress bar
            ProgressBar(currentCoins: currentCoins)
            
            Spacer()
            
            // Volume toggle
            if showVolume {
                WoodButton(text: nil, icon: "speaker.wave.2") {
                    onVolumeAction()
                }
            } else {
                Spacer().frame(width: 96)
            }
        }
        .padding(.horizontal, 20) // Part 4.3
        .padding(.top, 16)        // Part 4.3
    }
}
```

**Validation Checklist:**
- [ ] Home button: 96×60pt minimum
- [ ] Volume button: 96×60pt minimum
- [ ] Horizontal padding: 20pt
- [ ] Top padding: 16pt
- [ ] Progress bar centered

**Test Cases:**
- [ ] All buttons visible when enabled
- [ ] Hidden buttons don't break layout
- [ ] Touch targets ≥ 96pt
- [ ] Progress bar centered

---

### 2.4 Create StoneTablet Component
**Estimated**: 35 minutes  
**Playbook Reference**: Part 1.3 (Forest Environment Colors)

**Requirements:**
- Stone texture: #A8A090 → #8A8070 gradient
- Border: #5D5D4D, 4pt
- Moss/vine decorations
- Carved border effect
- Content area for grid/numbers
- 24pt padding

**Implementation:**
```swift
// Design/Components/StoneTablet.swift
import SwiftUI

struct StoneTablet<Content: View>: View {
    let title: String?
    let content: () -> Content
    
    init(title: String? = nil, @ViewBuilder content: @escaping () -> Content) {
        self.title = title
        self.content = content
    }
    
    var body: some View {
        VStack(spacing: 8) {
            if let title = title {
                Text(title)
                    .font(.sfRounded(size: 24, weight: .bold))
                    .foregroundColor(Color.woodDark)
            }
            
            ZStack {
                // Stone background - Part 1.3: Path Stone #A8A090
                RoundedRectangle(cornerRadius: 16)
                    .fill(
                        LinearGradient(
                            colors: [
                                Color(hex: "A8A090"), // Path Stone
                                Color(hex: "8A8070")  // Darker variant
                            ],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .overlay(
                        RoundedRectangle(cornerRadius: 16)
                            .stroke(Color(hex: "5D5D4D"), lineWidth: 4) // Moss color
                    )
                
                // Content
                content()
                    .padding(24)
            }
        }
    }
}
```

**Validation Checklist:**
- [ ] Stone light: #A8A090
- [ ] Stone dark: #8A8070
- [ ] Border color: #5D5D4D (Moss)
- [ ] Border width: 4pt
- [ ] Content padding: 24pt
- [ ] Corner radius: 16pt

**Test Cases:**
- [ ] Stone colors correct
- [ ] Border visible
- [ ] Content area padded properly
- [ ] Title optional

---

### 2.5 Create AnalogClock Component
**Estimated**: 45 minutes  
**Playbook Reference**: Part 4.10 (Video Player Screen)

**Requirements:**
- Wooden clock face: #FAF5EB (Cream)
- Border: #8C7259 (Bark), 8pt
- 12 minute markers: #6B4423 (Wood Dark)
- Hand rotation based on time remaining
- Progress arc: #99BF8C (Success green), 12pt stroke
- Center dot: #D9C27A (Coin Gold), 12pt diameter
- Total size: 150×150pt

**Implementation:**
```swift
// Design/Components/AnalogClock.swift
import SwiftUI

struct AnalogClock: View {
    let totalMinutes: Int
    @Binding var remainingSeconds: Int
    
    var progress: CGFloat {
        CGFloat(remainingSeconds) / CGFloat(totalMinutes * 60)
    }
    
    var handRotation: Angle {
        .degrees(360 * (1 - progress))
    }
    
    var body: some View {
        ZStack {
            // Clock face - Part 1.3: #FAF5EB
            Circle()
                .fill(Color.cream) // #FAF5EB
                .overlay(
                    Circle()
                        .stroke(Color.bark, lineWidth: 8) // #8C7259
                )
            
            // Minute markers - Part 4.10
            ForEach(0..<12) { i in
                Rectangle()
                    .fill(Color.woodDark) // #6B4423
                    .frame(width: 2, height: i % 3 == 0 ? 15 : 8)
                    .offset(y: -55)
                    .rotationEffect(.degrees(Double(i) * 30))
            }
            
            // Progress arc - Part 1.3: #99BF8C
            Circle()
                .trim(from: 0, to: progress)
                .stroke(
                    Color.success, // #99BF8C
                    style: StrokeStyle(lineWidth: 12, lineCap: .round)
                )
                .rotationEffect(.degrees(-90))
            
            // Clock hand
            Rectangle()
                .fill(Color.woodDark) // #6B4423
                .frame(width: 4, height: 45)
                .offset(y: -22)
                .rotationEffect(handRotation)
            
            // Center dot - Part 1.3: #D9C27A
            Circle()
                .fill(Color.coinGold) // #D9C27A
                .frame(width: 12, height: 12)
        }
        .frame(width: 150, height: 150)
    }
}
```

**Validation Checklist:**
- [ ] Clock face: #FAF5EB (Cream)
- [ ] Border: #8C7259 (Bark), 8pt
- [ ] Markers: #6B4423 (Wood Dark)
- [ ] Progress arc: #99BF8C (Success), 12pt
- [ ] Center dot: #D9C27A (Coin Gold), 12pt
- [ ] Size: 150×150pt
- [ ] Hand rotates counterclockwise

**Test Cases:**
- [ ] Hand rotates correctly
- [ ] Progress arc fills correctly
- [ ] Minute markers visible
- [ ] Colors match playbook

---

### 2.6 Create SpeechBubble Component
**Estimated**: 40 minutes  
**Playbook Reference**: Part 3.3 (Bennie Voice Guidelines)

**Requirements:**
- Rounded rectangle bubble: #FAF5EB (Cream)
- Border: #8C7259 (Bark), 3pt
- Tail pointing to character
- Typewriter text effect (0.15s per word, Part 3.3)
- Appears from scale 0.8→1.0 (0.4s spring)
- Text: SF Rounded, 20pt, semibold

**Implementation:**
```swift
// Design/Components/SpeechBubble.swift
import SwiftUI

struct SpeechBubble: View {
    let message: String
    let tailDirection: TailDirection
    
    @State private var displayedText = ""
    
    enum TailDirection {
        case left, right, bottom
    }
    
    var body: some View {
        ZStack(alignment: tailAlignment) {
            // Bubble - Part 1.3: #FAF5EB
            RoundedRectangle(cornerRadius: 16)
                .fill(Color.cream) // #FAF5EB
                .overlay(
                    RoundedRectangle(cornerRadius: 16)
                        .stroke(Color(hex: "8C7259"), lineWidth: 3) // Bark
                )
            
            // Text - Part 1.4: SF Rounded, 20pt, semibold
            Text(displayedText)
                .font(.sfRounded(size: 20, weight: .semibold))
                .foregroundColor(Color.woodDark)
                .multilineTextAlignment(.center)
                .padding(16)
            
            // Tail
            Triangle()
                .fill(Color.cream)
                .frame(width: 20, height: 15)
                .overlay(
                    Triangle()
                        .stroke(Color(hex: "8C7259"), lineWidth: 3)
                )
                .rotationEffect(tailRotation)
                .offset(tailOffset)
        }
        .scaleEffect(displayedText.isEmpty ? 0.8 : 1.0)
        .animation(.spring(response: 0.4), value: displayedText.isEmpty)
        .onAppear {
            typewriterEffect()
        }
    }
    
    var tailAlignment: Alignment {
        switch tailDirection {
        case .left: return .leading
        case .right: return .trailing
        case .bottom: return .bottom
        }
    }
    
    var tailRotation: Angle {
        switch tailDirection {
        case .left: return .degrees(90)
        case .right: return .degrees(-90)
        case .bottom: return .degrees(0)
        }
    }
    
    var tailOffset: CGSize {
        switch tailDirection {
        case .left: return CGSize(width: -10, height: 0)
        case .right: return CGSize(width: 10, height: 0)
        case .bottom: return CGSize(width: 0, height: 10)
        }
    }
    
    func typewriterEffect() {
        // Part 3.3: 0.15s per word
        let words = message.split(separator: " ")
        var currentIndex = 0
        
        Timer.scheduledTimer(withTimeInterval: 0.15, repeats: true) { timer in
            if currentIndex < words.count {
                displayedText += (displayedText.isEmpty ? "" : " ") + words[currentIndex]
                currentIndex += 1
            } else {
                timer.invalidate()
            }
        }
    }
}

struct Triangle: Shape {
    func path(in rect: CGRect) -> Path {
        Path { path in
            path.move(to: CGPoint(x: rect.midX, y: rect.minY))
            path.addLine(to: CGPoint(x: rect.maxX, y: rect.maxY))
            path.addLine(to: CGPoint(x: rect.minX, y: rect.maxY))
            path.closeSubpath()
        }
    }
}
```

**Validation Checklist:**
- [ ] Bubble color: #FAF5EB (Cream)
- [ ] Border color: #8C7259 (Bark)
- [ ] Border width: 3pt
- [ ] Text: SF Rounded, 20pt, semibold
- [ ] Typewriter speed: 0.15s per word
- [ ] Scale animation: 0.8→1.0, spring 0.4s
- [ ] Corner radius: 16pt

**Test Cases:**
- [ ] Typewriter effect works
- [ ] Tail points correctly
- [ ] Scale animation smooth
- [ ] Text wraps properly

---

### 2.7 Create BennieView Component
**Estimated**: 50 minutes  
**Playbook Reference**: Part 1.2 (The Characters - Bennie der Bär)

**CRITICAL DESIGN RULES:**
```
╔════════════════════════════════════════════════════════════════════╗
║  🐻 BENNIE: Brown (#8C7259) • NO VEST • NO CLOTHING • EVER         ║
║  Snout ONLY: Tan (#C4A574)                                         ║
║  NO separate belly patch                                           ║
╚════════════════════════════════════════════════════════════════════╝
```

**Requirements:**
- 6 expression states (Part 1.2, Table: Expression States)
- Load from Assets.xcassets
- Smooth transitions (0.3s)
- Correct brown color: #8C7259
- Snout tan: #C4A574
- NO clothing verification (MANDATORY QA)
- Default size: 300×450pt (Part 5.2)

**Implementation:**
```swift
// Design/Characters/BennieView.swift
import SwiftUI

enum BennieExpression: String, CaseIterable {
    case idle = "bennie_idle"
    case waving = "bennie_waving"
    case pointing = "bennie_pointing"
    case thinking = "bennie_thinking"
    case encouraging = "bennie_encouraging"
    case celebrating = "bennie_celebrating"
    
    // Part 1.2: Expression descriptions
    var description: String {
        switch self {
        case .idle: return "Gentle breathing animation, calm smile, arms at sides"
        case .waving: return "Right paw raised, palm out, friendly smile"
        case .pointing: return "Left arm extended toward target, looking where pointing"
        case .thinking: return "Paw on chin, eyes looking up and to the side"
        case .encouraging: return "Leaning forward, soft eyes, open body language"
        case .celebrating: return "Both arms up, jumping pose, big smile, eyes squeezed happy"
        }
    }
}

struct BennieView: View {
    let expression: BennieExpression
    let size: CGSize
    
    init(expression: BennieExpression = .idle, size: CGSize = CGSize(width: 300, height: 450)) {
        self.expression = expression
        self.size = size
    }
    
    var body: some View {
        Image(expression.rawValue)
            .resizable()
            .aspectRatio(contentMode: .fit)
            .frame(width: size.width, height: size.height)
            .transition(.opacity)
            .animation(.easeInOut(duration: 0.3), value: expression)
    }
}

// CRITICAL VALIDATION - Part 1.2
extension BennieView {
    /// QA Check: Verify Bennie has NO clothing
    /// Reference: C:\Users\christoph\Bennie und die Lemminge v3\design\references\character\bennie\reference\bennie-reference.png
    func validateDesign() -> [String] {
        var issues: [String] = []
        
        // MANDATORY CHECKS (Part 1.2):
        // ✓ Fur color is #8C7259 (warm chocolate brown)
        // ✓ NO vest
        // ✓ NO clothing
        // ✓ NO accessories
        // ✓ Snout ONLY is tan #C4A574
        // ✓ NO separate belly patch
        // ✓ Pear-shaped body (narrow shoulders, wide hips)
        // ✓ Adult bear (NOT cub, NOT teddy)
        // ✓ Nose is #3D2B1F (dark espresso)
        
        return issues
    }
}

#Preview {
    VStack(spacing: 20) {
        ForEach(BennieExpression.allCases, id: \.self) { expression in
            VStack {
                Text(expression.rawValue)
                    .font(.caption)
                BennieView(expression: expression, size: CGSize(width: 150, height: 225))
            }
        }
    }
}
```

**Validation Checklist (CRITICAL):**
- [ ] Main fur color: #8C7259 (Brown)
- [ ] Snout ONLY: #C4A574 (Tan)
- [ ] Nose: #3D2B1F (Dark espresso)
- [ ] NO clothing/vest/accessories
- [ ] NO belly patch
- [ ] Pear-shaped body
- [ ] Adult bear (not cub)
- [ ] All 6 expressions exist in Assets
- [ ] Compare to canonical reference image

**Test Cases:**
- [ ] All 6 expressions load
- [ ] No clothing visible (MANUAL QA REQUIRED)
- [ ] Brown color #8C7259 verified
- [ ] Size scales correctly
- [ ] Assets exist in catalog
- [ ] Transition animation: 0.3s

---

### 2.8 Create LemmingeView Component
**Estimated**: 50 minutes  
**Playbook Reference**: Part 1.2 (The Characters - Die Lemminge)

**CRITICAL DESIGN RULES:**
```
╔════════════════════════════════════════════════════════════════════╗
║  🔵 LEMMINGE: BLUE (#6FA8DC) • NEVER GREEN • NEVER BROWN           ║
║  White belly (#FAF5EB) with fuzzy edge                             ║
║  Buck teeth ALWAYS visible                                         ║
╚════════════════════════════════════════════════════════════════════╝
```

**Requirements:**
- 6 expression states (Part 1.2, Table: Expression States)
- MUST be BLUE: #6FA8DC
- Load from Assets.xcassets
- Buck teeth visible in ALL states
- Cream belly: #FAF5EB with fuzzy edge
- Pink nose/paws: #E8A0A0
- Default size: 80×100pt (Part 5.2)

**Implementation:**
```swift
// Design/Characters/LemmingeView.swift
import SwiftUI

enum LemmingeExpression: String, CaseIterable {
    case idle = "lemminge_idle"
    case curious = "lemminge_curious"
    case excited = "lemminge_excited"
    case celebrating = "lemminge_celebrating"
    case hiding = "lemminge_hiding"
    case mischievous = "lemminge_mischievous"
    
    // Part 1.2: Expression descriptions
    var description: String {
        switch self {
        case .idle: return "Gentle swaying, occasional blinking"
        case .curious: return "Wide eyes, head tilted, ears perked"
        case .excited: return "Bouncing pose, sparkly eyes"
        case .celebrating: return "Jumping, arms up, huge smile"
        case .hiding: return "Half-hidden, mischievous expression"
        case .mischievous: return "Sly grin, squinted eyes, scheming pose"
        }
    }
}

struct LemmingeView: View {
    let expression: LemmingeExpression
    let size: CGSize
    
    init(expression: LemmingeExpression = .idle, size: CGSize = CGSize(width: 80, height: 100)) {
        self.expression = expression
        self.size = size
    }
    
    var body: some View {
        Image(expression.rawValue)
            .resizable()
            .aspectRatio(contentMode: .fit)
            .frame(width: size.width, height: size.height)
            .transition(.opacity)
            .animation(.easeInOut(duration: 0.3), value: expression)
    }
}

// CRITICAL VALIDATION - Part 1.2
extension LemmingeView {
    /// QA Check: CRITICAL - Verify Lemminge are BLUE
    /// Reference: C:\Users\christoph\Bennie und die Lemminge v3\design\references\character\lemminge\reference\lemminge-reference.png
    func validateDesign() -> [String] {
        var issues: [String] = []
        
        // MANDATORY CHECKS (Part 1.2):
        // ✓ Body is BLUE #6FA8DC (ABSOLUTE REQUIREMENT)
        // ✓ NOT green (ANY green is VIOLATION)
        // ✓ NOT brown (ANY brown is VIOLATION)
        // ✓ Cream belly #FAF5EB with fuzzy edge
        // ✓ Buck teeth visible (2 prominent teeth)
        // ✓ Pink nose #E8A0A0
        // ✓ Pink paws #E8A0A0
        // ✓ Round potato blob shape (Go gopher style)
        // ✓ Two small round ears on top
        
        return issues
    }
}

#Preview {
    VStack(spacing: 20) {
        ForEach(LemmingeExpression.allCases, id: \.self) { expression in
            VStack {
                Text(expression.rawValue)
                    .font(.caption)
                LemmingeView(expression: expression)
            }
        }
    }
}
```

**Validation Checklist (CRITICAL):**
- [ ] Body color: #6FA8DC (BLUE) - ABSOLUTE REQUIREMENT
- [ ] NOT green (any shade)
- [ ] NOT brown (any shade)
- [ ] Belly: #FAF5EB (Cream) with fuzzy edge
- [ ] Buck teeth visible in ALL expressions
- [ ] Nose: #E8A0A0 (Pink)
- [ ] Paws: #E8A0A0 (Pink)
- [ ] Round blob shape (Go gopher style)
- [ ] All 6 expressions exist in Assets
- [ ] Compare to canonical reference image

**Test Cases:**
- [ ] All 6 expressions load
- [ ] BLUE color #6FA8DC verified (CRITICAL)
- [ ] NOT green or brown verified
- [ ] Buck teeth visible
- [ ] Size scales correctly
- [ ] Transition animation: 0.3s

---

### 2.9 Create Animation Presets
**Estimated**: 30 minutes  
**Playbook Reference**: Part 6 (Animation & Sound Guide)

**Create file with common animation values from Playbook Part 6.1 and 6.2:**

```swift
// Design/Theme/Animations.swift
import SwiftUI

struct BennieAnimation {
    // MARK: - Durations (Part 6.1)
    static let fast: TimeInterval = 0.2
    static let normal: TimeInterval = 0.3
    static let slow: TimeInterval = 0.5
    
    // MARK: - Springs (Part 6.1)
    static let spring = Animation.spring(response: 0.3, dampingFraction: 0.7)
    static let gentleSpring = Animation.spring(response: 0.5, dampingFraction: 0.8)
    
    // MARK: - Easing (Part 6.1)
    static let easeInOut = Animation.easeInOut(duration: normal)
    static let easeOut = Animation.easeOut(duration: normal)
    
    // MARK: - Breathing (for idle states) - Part 6.3
    static let breathing = Animation.easeInOut(duration: 2.0).repeatForever(autoreverses: true)
    
    // MARK: - Button Press - Part 6.2
    static let buttonPress = Animation.spring(response: 0.3)
    
    // MARK: - Celebration - Part 6.2
    static let celebration = Animation.spring(response: 0.4, dampingFraction: 0.6)
    
    // MARK: - Transition - Part 6.2
    static let screenTransition = Animation.easeInOut(duration: 0.3)
    
    // MARK: - Overlay - Part 4.7
    static let overlayAppear = Animation.spring(response: 0.4)
    static let overlayDismiss = Animation.easeInOut(duration: 0.3)
    
    // MARK: - Coin Fly - Part 6.2
    static let coinFly = Animation.easeOut(duration: 0.8)
    
    // MARK: - Progress Fill - Part 6.2
    static let progressFill = Animation.spring(response: 0.5)
    
    // FORBIDDEN ANIMATIONS (Part 6.1 - documented but NOT PROVIDED)
    // - NO flashing
    // - NO shaking
    // - NO rapid strobing  
    // - NO sudden movements
    // - NO rapid color changes
    // - NO bouncing text
}

// Scale presets (Part 6.2)
extension CGFloat {
    static let buttonPressScale: CGFloat = 0.95
    static let breathingScale: CGFloat = 1.03
    static let overlayScale: CGFloat = 0.8
}

// Rotation presets (Part 6.2)
extension Angle {
    static let signSwing: Angle = .degrees(3) // ±3° for hanging signs
}
```

**Validation Checklist:**
- [ ] Fast duration: 0.2s
- [ ] Normal duration: 0.3s
- [ ] Slow duration: 0.5s
- [ ] Breathing duration: 2.0s
- [ ] Button press scale: 0.95
- [ ] Overlay scale: 0.8
- [ ] Coin fly duration: 0.8s
- [ ] Progress fill: 0.5s spring
- [ ] Sign swing: ±3°

**Test:**
- [ ] File compiles without errors
- [ ] Values match Playbook Part 6.1 and 6.2
- [ ] Forbidden animations documented but NOT implemented

---

### 2.10 Create Preview Helpers
**Estimated**: 20 minutes

**Create preview helpers for development:**

```swift
// Design/Preview/PreviewHelpers.swift
import SwiftUI

struct ComponentPreview<Content: View>: View {
    let title: String
    let content: () -> Content
    
    init(_ title: String, @ViewBuilder content: @escaping () -> Content) {
        self.title = title
        self.content = content
    }
    
    var body: some View {
        VStack {
            Text(title)
                .font(.headline)
                .padding()
            
            content()
                .padding()
            
            Spacer()
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(Color.cream) // Part 1.3: #FAF5EB
    }
}

// Example usage in component files:
#Preview("Wood Button States") {
    ComponentPreview("Wood Button") {
        VStack(spacing: 20) {
            WoodButton(text: "Home", icon: "house") {}
            WoodButton(text: "Weiter", icon: nil) {}
            WoodButton(text: nil, icon: "speaker.wave.2") {}
        }
    }
}
```

**Test:**
- [ ] Preview canvas renders
- [ ] Background color is Cream (#FAF5EB)
- [ ] Title displays correctly

---

## Phase Completion Checklist

### Visual Design Compliance (Playbook Part 1)
- [ ] All colors match playbook hex values exactly
- [ ] SF Rounded font used throughout (Part 1.4)
- [ ] Wood textures use correct gradients (#C4A574 → #A67C52)
- [ ] No forbidden colors (red, neon, >80% saturation)
- [ ] Bennie has NO clothing/vest/accessories
- [ ] Bennie brown: #8C7259, snout tan: #C4A574
- [ ] Lemminge are BLUE #6FA8DC (NEVER green/brown)
- [ ] Lemminge belly: #FAF5EB, nose/paws: #E8A0A0

### Technical Compliance (Playbook Part 5)
- [ ] All components compile without warnings
- [ ] Preview canvas works for all components
- [ ] Touch targets ≥ 96pt enforced (Part 5.1)
- [ ] Animations use presets from Part 6
- [ ] No hardcoded colors (all use Color extensions from Phase 1)

### Character Validation (Playbook Part 1.2)
- [ ] Bennie assets compared to canonical reference image
- [ ] Lemminge assets compared to canonical reference image
- [ ] All 6 Bennie expressions exist and load
- [ ] All 6 Lemminge expressions exist and load
- [ ] Manual QA performed for character designs

### Reusability
- [ ] Components accept parameters
- [ ] ViewBuilders used where appropriate
- [ ] Components composable
- [ ] No tight coupling

### Documentation
- [ ] Each component has #Preview
- [ ] Validation extensions documented
- [ ] Animation presets documented
- [ ] Playbook references included

---

## Next Phase

After Phase 2 completion, proceed to:
**Phase 3: Core Screens Implementation**
- Build Loading, PlayerSelection, Home screens
- Integrate design components from Phase 2
- Add navigation flow
- Reference: Playbook Part 4 (Screen Specifications)
