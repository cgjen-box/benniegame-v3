# 🐻 Bennie und die Lemminge
## SwiftUI Coding Guidelines for Claude Code

> **Version**: 1.0 | **Companion to**: BENNIE_BRAND_PLAYBOOK_v3_1.md
>
> *These guidelines ensure AI-assisted development produces code that matches design specifications exactly.*

---

## 🎯 CRITICAL RULES FOR CLAUDE CODE

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    RULES CLAUDE CODE MUST NEVER VIOLATE                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  1. TOUCH TARGETS: Minimum 96pt × 96pt for ALL interactive elements         ║
║     - This is NON-NEGOTIABLE for autism-friendly design                     ║
║     - Visual size can be smaller; hit area must be 96pt+                    ║
║                                                                              ║
║  2. BENNIE: NO clothing, NO vest, NO accessories - EVER                     ║
║     - Reject any asset showing Bennie with clothing                         ║
║                                                                              ║
║  3. LEMMINGE: MUST be blue #6FA8DC - NEVER green, NEVER brown               ║
║     - Reject any asset showing wrong color                                  ║
║                                                                              ║
║  4. LANGUAGE: German only in UI - Code comments can be English              ║
║     - Never say "Falsch", "Fehler", "Versuch nochmal"                       ║
║                                                                              ║
║  5. NO FORBIDDEN ANIMATIONS: No flashing, shaking, strobing                 ║
║     - Seizure risk and anxiety triggers for autistic children               ║
║                                                                              ║
║  6. COLORS: Never use pure red #FF0000, neon, or >80% saturation            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 1. Project Architecture

### 1.1 File Structure (MANDATORY)

```
BennieGame/
├── App/
│   ├── BennieGameApp.swift          // @main entry point
│   └── AppCoordinator.swift         // Navigation state machine
│
├── Core/
│   ├── State/
│   │   ├── GameState.swift          // @Observable game state
│   │   ├── PlayerData.swift         // Per-player persistent data
│   │   └── ParentSettings.swift     // Shared parent configuration
│   │
│   ├── Services/
│   │   ├── AudioManager.swift       // 3-channel audio system
│   │   ├── NarratorService.swift    // Voice line playback
│   │   ├── HapticManager.swift      // Haptic feedback
│   │   └── NetworkMonitor.swift     // Connectivity check
│   │
│   └── Utilities/
│       ├── ImageDownsampler.swift   // Memory-efficient image loading
│       └── Extensions.swift         // Color, Font extensions
│
├── Features/
│   ├── Loading/
│   ├── PlayerSelection/
│   ├── Home/
│   ├── Activities/
│   │   ├── Raetsel/
│   │   │   ├── PuzzleMatchingView.swift
│   │   │   └── LabyrinthView.swift
│   │   └── Zahlen/
│   │       ├── WuerfelView.swift
│   │       └── WaehleZahlView.swift
│   ├── Celebration/
│   ├── Treasure/
│   ├── Video/
│   └── Parent/
│
├── Design/
│   ├── Theme/
│   │   ├── BennieColors.swift       // All color definitions
│   │   └── BennieTypography.swift   // SF Rounded system
│   │
│   ├── Components/
│   │   ├── WoodButton.swift         // Primary button style
│   │   ├── WoodSign.swift           // Activity signs
│   │   ├── ProgressBar.swift        // Coin progress
│   │   ├── StoneTablet.swift        // Game grids
│   │   ├── AnalogClock.swift        // YouTube timer
│   │   └── NavigationHeader.swift   // Consistent header
│   │
│   ├── Characters/
│   │   ├── BennieView.swift         // Bennie with states
│   │   ├── LemmingeView.swift       // Lemminge with states
│   │   └── SpeechBubbleView.swift   // Character speech
│   │
│   └── Layout/
│       └── AdaptiveLayout.swift     // Screen size adaptation
│
└── Resources/
    ├── Assets.xcassets/
    ├── Lottie/
    └── Audio/
```

### 1.2 State Management Pattern

```swift
// ═══════════════════════════════════════════════════════════════════
// GAME STATE - Single source of truth
// ═══════════════════════════════════════════════════════════════════

@Observable
final class GameState {
    // Current session
    var currentPlayer: String?              // "alexander" or "oliver"
    var currentScreen: GameScreen = .loading
    
    // Player data (persisted)
    var players: [String: PlayerData] = [:]
    
    // UI state (transient)
    var isAudioEnabled: Bool = true
    var showCelebration: Bool = false
    var celebrationCoins: Int = 0
    
    // Computed
    var activePlayer: PlayerData? {
        guard let id = currentPlayer else { return nil }
        return players[id]
    }
}

// ═══════════════════════════════════════════════════════════════════
// INJECT AT APP ROOT - Access via @Environment
// ═══════════════════════════════════════════════════════════════════

@main
struct BennieGameApp: App {
    @State private var gameState = GameState()
    
    var body: some Scene {
        WindowGroup {
            AppCoordinator()
                .environment(gameState)
        }
    }
}

// ═══════════════════════════════════════════════════════════════════
// ACCESS IN VIEWS
// ═══════════════════════════════════════════════════════════════════

struct HomeView: View {
    @Environment(GameState.self) private var gameState
    
    var body: some View {
        // Use gameState directly
    }
}
```

---

## 2. Color System Implementation

### 2.1 BennieColors.swift (MANDATORY)

```swift
import SwiftUI

// ═══════════════════════════════════════════════════════════════════
// BENNIE COLOR SYSTEM - Use ONLY these colors
// ═══════════════════════════════════════════════════════════════════

enum BennieColors {
    
    // ─────────────────────────────────────────────────────────────────
    // CHARACTER COLORS (NON-NEGOTIABLE)
    // ─────────────────────────────────────────────────────────────────
    
    /// Bennie main fur - warm chocolate brown
    static let bennieBrown = Color(hex: "8C7259")
    
    /// Bennie snout ONLY - lighter tan
    static let bennieTan = Color(hex: "C4A574")
    
    /// Bennie nose - dark espresso
    static let bennieNose = Color(hex: "3D2B1F")
    
    /// Lemminge body - MUST BE THIS BLUE (never green, never brown)
    static let lemmingeBlue = Color(hex: "6FA8DC")
    
    /// Lemminge nose and paws - soft pink
    static let lemmingePink = Color(hex: "E8A0A0")
    
    /// Lemminge belly - cream white
    static let lemmingeBelly = Color(hex: "FAF5EB")
    
    // ─────────────────────────────────────────────────────────────────
    // UI COLORS
    // ─────────────────────────────────────────────────────────────────
    
    /// Success feedback, progress fill
    static let success = Color(hex: "99BF8C")
    
    /// Rewards, coins, treasure
    static let coinGold = Color(hex: "D9C27A")
    
    /// Wood UI - light highlight
    static let woodLight = Color(hex: "C4A574")
    
    /// Wood UI - main plank color
    static let woodMedium = Color(hex: "A67C52")
    
    /// Wood UI - shadows, grain
    static let woodDark = Color(hex: "6B4423")
    
    /// Rope texture
    static let rope = Color(hex: "B8956B")
    
    /// Lock chains
    static let chain = Color(hex: "6B6B6B")
    
    // ─────────────────────────────────────────────────────────────────
    // ENVIRONMENT COLORS
    // ─────────────────────────────────────────────────────────────────
    
    /// Primary green - woodland
    static let woodland = Color(hex: "738F66")
    
    /// Far trees - misty background
    static let farTrees = Color(hex: "4A6B5C")
    
    /// Near foliage
    static let nearFoliage = Color(hex: "7A9973")
    
    /// Sky accent
    static let sky = Color(hex: "B3D1E6")
    
    /// Cream background
    static let cream = Color(hex: "FAF5EB")
    
    /// Light rays (use with 30% opacity)
    static let lightRays = Color(hex: "F5E6C8")
    
    /// Moss ground
    static let moss = Color(hex: "5D6B4D")
    
    /// Labyrinth path stone
    static let pathStone = Color(hex: "A8A090")
    
    // ─────────────────────────────────────────────────────────────────
    // TEXT COLORS
    // ─────────────────────────────────────────────────────────────────
    
    /// Primary text on wood
    static let textOnWood = Color(hex: "4A4036")
    
    /// Dark text
    static let textDark = Color(hex: "2D2D2D")
}

// ═══════════════════════════════════════════════════════════════════
// COLOR EXTENSION
// ═══════════════════════════════════════════════════════════════════

extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 6: // RGB
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: // ARGB
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (255, 0, 0, 0)
        }
        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue: Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}

// ═══════════════════════════════════════════════════════════════════
// 🚫 FORBIDDEN COLORS - NEVER USE THESE
// ═══════════════════════════════════════════════════════════════════
//
// ❌ Pure Red #FF0000      - Triggers anxiety
// ❌ Pure White #FFFFFF    - Too harsh for large areas
// ❌ Pure Black #000000    - Too harsh for large areas
// ❌ Any Neon colors       - Overstimulating
// ❌ Saturation > 80%      - Overstimulating
// ❌ Green for Lemminge    - Design violation
// ❌ Brown for Lemminge    - Design violation
//
// ═══════════════════════════════════════════════════════════════════
```

---

## 3. Typography System

### 3.1 BennieTypography.swift

```swift
import SwiftUI

// ═══════════════════════════════════════════════════════════════════
// TYPOGRAPHY - SF Rounded only
// ═══════════════════════════════════════════════════════════════════

enum BennieFont {
    /// Titles: 32-48pt Bold
    static func title(_ size: CGFloat = 40) -> Font {
        .system(size: size, weight: .bold, design: .rounded)
    }
    
    /// Body: 17-24pt Regular
    static func body(_ size: CGFloat = 20) -> Font {
        .system(size: size, weight: .regular, design: .rounded)
    }
    
    /// Buttons: 20-28pt Semibold
    static func button(_ size: CGFloat = 24) -> Font {
        .system(size: size, weight: .semibold, design: .rounded)
    }
    
    /// Labels: 14-17pt Medium
    static func label(_ size: CGFloat = 16) -> Font {
        .system(size: size, weight: .medium, design: .rounded)
    }
    
    /// Large numbers: 40-72pt Bold
    static func number(_ size: CGFloat = 56) -> Font {
        .system(size: size, weight: .bold, design: .rounded)
    }
}

// ═══════════════════════════════════════════════════════════════════
// USAGE EXAMPLE
// ═══════════════════════════════════════════════════════════════════

struct ExampleView: View {
    var body: some View {
        VStack {
            Text("Waldabenteuer")
                .font(BennieFont.title(48))
            
            Text("Wähle ein Spiel!")
                .font(BennieFont.body(20))
            
            Button("Weiter") { }
                .font(BennieFont.button(24))
        }
    }
}
```

---

## 4. Touch Target System (CRITICAL)

### 4.1 Minimum Touch Target: 96pt × 96pt

```swift
// ═══════════════════════════════════════════════════════════════════
// CHILD-FRIENDLY BUTTON - Minimum 96pt touch target
// ═══════════════════════════════════════════════════════════════════

struct ChildFriendlyButton<Label: View>: View {
    let action: () -> Void
    @ViewBuilder let label: () -> Label
    
    /// Minimum touch target for autism-friendly design
    /// Research shows 80-120pt optimal for ages 4-5
    static var minimumTouchTarget: CGFloat { 96 }
    
    @State private var isPressed = false
    @Environment(\.isEnabled) private var isEnabled
    
    var body: some View {
        Button(action: {
            // Haptic feedback
            let impact = UIImpactFeedbackGenerator(style: .light)
            impact.impactOccurred()
            action()
        }) {
            label()
                .frame(
                    minWidth: Self.minimumTouchTarget,
                    minHeight: Self.minimumTouchTarget
                )
                .contentShape(Rectangle()) // Expand hit area
        }
        .buttonStyle(ChildButtonStyle())
        .disabled(!isEnabled)
    }
}

// ═══════════════════════════════════════════════════════════════════
// BUTTON STYLE - Gentle feedback, no harsh animations
// ═══════════════════════════════════════════════════════════════════

struct ChildButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
            .animation(.easeOut(duration: 0.1), value: configuration.isPressed)
    }
}

// ═══════════════════════════════════════════════════════════════════
// WOOD BUTTON - Primary activity button
// ═══════════════════════════════════════════════════════════════════

struct WoodButton: View {
    let title: String
    let icon: String?
    let action: () -> Void
    
    var body: some View {
        ChildFriendlyButton(action: action) {
            VStack(spacing: 8) {
                if let icon = icon {
                    Image(systemName: icon)
                        .font(.system(size: 32))
                }
                Text(title)
                    .font(BennieFont.button(24))
            }
            .foregroundColor(BennieColors.textOnWood)
            .frame(minWidth: 160, minHeight: 140) // Exceeds 96pt requirement
            .padding(16)
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .fill(
                        LinearGradient(
                            colors: [BennieColors.woodLight, BennieColors.woodMedium],
                            startPoint: .top,
                            endPoint: .bottom
                        )
                    )
            )
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(BennieColors.woodDark, lineWidth: 2)
            )
        }
    }
}

// ═══════════════════════════════════════════════════════════════════
// GRID CELL - For puzzle games (96pt minimum)
// ═══════════════════════════════════════════════════════════════════

struct GridCell: View {
    let color: Color?
    let isSelected: Bool
    let onTap: () -> Void
    
    var body: some View {
        ChildFriendlyButton(action: onTap) {
            Rectangle()
                .fill(color ?? BennieColors.cream)
                .frame(width: 96, height: 96) // Exact minimum
                .cornerRadius(8)
                .overlay(
                    RoundedRectangle(cornerRadius: 8)
                        .stroke(
                            isSelected ? BennieColors.coinGold : BennieColors.woodDark,
                            lineWidth: isSelected ? 4 : 2
                        )
                )
        }
    }
}
```

---

## 5. Adaptive Layout System

### 5.1 Screen Size Categories

```swift
// ═══════════════════════════════════════════════════════════════════
// ADAPTIVE LAYOUT - Supports all iPad sizes
// ═══════════════════════════════════════════════════════════════════

enum ScreenCategory {
    case compact    // iPad mini (744×1133 landscape = 1133×744)
    case regular    // iPad 10th gen (1194×834)
    case large      // iPad Pro 11" (1194×834)
    case extraLarge // iPad Pro 13" (1376×1032)
    
    static func current(for size: CGSize) -> ScreenCategory {
        let width = max(size.width, size.height) // Landscape width
        switch width {
        case ..<1000: return .compact
        case 1000..<1200: return .regular
        case 1200..<1350: return .large
        default: return .extraLarge
        }
    }
}

// ═══════════════════════════════════════════════════════════════════
// ADAPTIVE SPACING
// ═══════════════════════════════════════════════════════════════════

struct AdaptiveSpacing {
    let screen: ScreenCategory
    
    var gridGap: CGFloat {
        switch screen {
        case .compact: return 12
        case .regular: return 16
        case .large: return 20
        case .extraLarge: return 24
        }
    }
    
    var sectionPadding: CGFloat {
        switch screen {
        case .compact: return 16
        case .regular: return 24
        case .large: return 32
        case .extraLarge: return 40
        }
    }
    
    var characterSize: CGFloat {
        switch screen {
        case .compact: return 200
        case .regular: return 280
        case .large: return 320
        case .extraLarge: return 380
        }
    }
}

// ═══════════════════════════════════════════════════════════════════
// ENVIRONMENT KEY
// ═══════════════════════════════════════════════════════════════════

private struct AdaptiveSpacingKey: EnvironmentKey {
    static let defaultValue = AdaptiveSpacing(screen: .regular)
}

extension EnvironmentValues {
    var adaptiveSpacing: AdaptiveSpacing {
        get { self[AdaptiveSpacingKey.self] }
        set { self[AdaptiveSpacingKey.self] = newValue }
    }
}

// ═══════════════════════════════════════════════════════════════════
// ROOT VIEW SETUP
// ═══════════════════════════════════════════════════════════════════

struct AdaptiveRootView<Content: View>: View {
    @ViewBuilder let content: () -> Content
    
    var body: some View {
        GeometryReader { geometry in
            let category = ScreenCategory.current(for: geometry.size)
            let spacing = AdaptiveSpacing(screen: category)
            
            content()
                .environment(\.adaptiveSpacing, spacing)
        }
    }
}
```

---

## 6. Memory Management (CRITICAL)

### 6.1 Image Memory Optimization

```swift
import UIKit

// ═══════════════════════════════════════════════════════════════════
// IMAGE MEMORY CALCULATION
// Memory = width × height × 4 bytes (RGBA)
//
// Example: 2388×1668 @2x background
// = 2388 × 1668 × 4 = 15.9 MB in memory!
//
// Target: < 200MB total app memory
// ═══════════════════════════════════════════════════════════════════

struct ImageDownsampler {
    
    /// Downsample image to display size to save memory
    /// A 2388×1668 source loaded at 1194×834 display uses 4MB instead of 16MB
    static func downsample(
        imageAt url: URL,
        to pointSize: CGSize,
        scale: CGFloat = UIScreen.main.scale
    ) -> UIImage? {
        
        let imageSourceOptions = [kCGImageSourceShouldCache: false] as CFDictionary
        guard let imageSource = CGImageSourceCreateWithURL(url as CFURL, imageSourceOptions) else {
            return nil
        }
        
        let maxDimensionInPixels = max(pointSize.width, pointSize.height) * scale
        
        let downsampleOptions = [
            kCGImageSourceCreateThumbnailFromImageAlways: true,
            kCGImageSourceShouldCacheImmediately: true,
            kCGImageSourceCreateThumbnailWithTransform: true,
            kCGImageSourceThumbnailMaxPixelSize: maxDimensionInPixels
        ] as CFDictionary
        
        guard let downsampledImage = CGImageSourceCreateThumbnailAtIndex(
            imageSource, 0, downsampleOptions
        ) else {
            return nil
        }
        
        return UIImage(cgImage: downsampledImage)
    }
}

// ═══════════════════════════════════════════════════════════════════
// MEMORY-SAFE IMAGE VIEW
// ═══════════════════════════════════════════════════════════════════

struct MemorySafeImage: View {
    let name: String
    let displaySize: CGSize
    
    @State private var image: UIImage?
    
    var body: some View {
        Group {
            if let image = image {
                Image(uiImage: image)
                    .resizable()
                    .aspectRatio(contentMode: .fit)
            } else {
                Color.clear
            }
        }
        .frame(width: displaySize.width, height: displaySize.height)
        .task {
            await loadImage()
        }
        .onDisappear {
            // Release memory when not visible
            image = nil
        }
    }
    
    private func loadImage() async {
        guard let url = Bundle.main.url(forResource: name, withExtension: "png") else {
            return
        }
        
        // Load on background thread
        let loaded = await Task.detached(priority: .userInitiated) {
            ImageDownsampler.downsample(imageAt: url, to: displaySize)
        }.value
        
        await MainActor.run {
            self.image = loaded
        }
    }
}
```

---

## 7. Animation Guidelines

### 7.1 Safe Animations Only

```swift
// ═══════════════════════════════════════════════════════════════════
// ANIMATION PRESETS - Autism-friendly, no flashing/shaking
// ═══════════════════════════════════════════════════════════════════

enum BennieAnimation {
    
    // ─────────────────────────────────────────────────────────────────
    // TRANSITIONS (0.3-0.5s, spring easing)
    // ─────────────────────────────────────────────────────────────────
    
    /// Screen transitions - gentle cross-fade
    static let screenTransition = Animation.easeInOut(duration: 0.3)
    
    /// Overlay appear - scale + fade
    static let overlayAppear = Animation.spring(response: 0.4, dampingFraction: 0.8)
    
    /// Overlay dismiss - faster fade out
    static let overlayDismiss = Animation.easeOut(duration: 0.3)
    
    /// Button press - quick scale
    static let buttonPress = Animation.easeOut(duration: 0.1)
    
    // ─────────────────────────────────────────────────────────────────
    // LOOPING ANIMATIONS
    // ─────────────────────────────────────────────────────────────────
    
    /// Idle breathing - subtle, calming
    static let breathing = Animation
        .easeInOut(duration: 2.0)
        .repeatForever(autoreverses: true)
    
    /// Sign swing - playful hover
    static let signSwing = Animation
        .easeInOut(duration: 0.5)
        .repeatForever(autoreverses: true)
    
    // ─────────────────────────────────────────────────────────────────
    // ONE-SHOT ANIMATIONS
    // ─────────────────────────────────────────────────────────────────
    
    /// Coin fly to progress bar
    static let coinFly = Animation.spring(response: 0.8, dampingFraction: 0.7)
    
    /// Progress bar fill
    static let progressFill = Animation.easeOut(duration: 0.5)
    
    /// Celebration confetti
    static let confetti = Animation.linear(duration: 3.0)
}

// ═══════════════════════════════════════════════════════════════════
// 🚫 FORBIDDEN ANIMATIONS - NEVER IMPLEMENT THESE
// ═══════════════════════════════════════════════════════════════════
//
// ❌ Flashing         - Seizure risk
// ❌ Shaking          - Anxiety trigger
// ❌ Strobing         - Overstimulating
// ❌ Rapid color changes - Disorienting
// ❌ Bouncing text    - Distracting
// ❌ Sudden movements - Startling
//
// ═══════════════════════════════════════════════════════════════════
```

### 7.2 Celebration Overlay (Context-Preserving)

```swift
// ═══════════════════════════════════════════════════════════════════
// CELEBRATION OVERLAY - Not a separate screen!
// Activity remains visible beneath, preserving context
// ═══════════════════════════════════════════════════════════════════

struct CelebrationOverlay: View {
    let coins: Int
    let onContinue: () -> Void
    
    var body: some View {
        ZStack {
            // Dim the activity beneath (NOT hide it)
            Color.black.opacity(0.4)
                .ignoresSafeArea()
            
            // Celebration card
            VStack(spacing: 24) {
                Text("✨ Super gemacht! ✨")
                    .font(BennieFont.title(32))
                    .foregroundColor(BennieColors.textDark)
                
                HStack {
                    Image("coin_icon")
                        .resizable()
                        .frame(width: 40, height: 40)
                    Text("+1")
                        .font(BennieFont.number(32))
                        .foregroundColor(BennieColors.coinGold)
                }
                
                // Characters celebrating
                HStack(spacing: 20) {
                    BennieView(state: .celebrating)
                        .frame(height: 180)
                    
                    ForEach(0..<3) { _ in
                        LemmingeView(state: .celebrating)
                            .frame(height: 80)
                    }
                }
                
                WoodButton(title: "Weiter →", icon: nil, action: onContinue)
            }
            .padding(32)
            .frame(width: UIScreen.main.bounds.width * 0.6)
            .background(
                RoundedRectangle(cornerRadius: 24)
                    .fill(BennieColors.cream.opacity(0.95))
            )
            .scaleEffect(1.0) // Animate from 0.8 on appear
            
            // Confetti over everything
            ConfettiView()
                .allowsHitTesting(false)
        }
    }
}

// ═══════════════════════════════════════════════════════════════════
// USAGE IN ACTIVITY VIEW
// ═══════════════════════════════════════════════════════════════════

struct PuzzleMatchingView: View {
    @Environment(GameState.self) private var gameState
    
    var body: some View {
        ZStack {
            // Main game content
            VStack {
                // ... puzzle grids, color picker, etc.
            }
            
            // Celebration overlay ON TOP (not replacing!)
            if gameState.showCelebration {
                CelebrationOverlay(
                    coins: gameState.celebrationCoins,
                    onContinue: {
                        gameState.showCelebration = false
                        // Navigate to next level or home
                    }
                )
                .transition(.opacity.combined(with: .scale(scale: 0.8)))
            }
        }
    }
}
```

---

## 8. Audio System

### 8.1 Three-Channel Audio Manager

```swift
import AVFoundation

// ═══════════════════════════════════════════════════════════════════
// AUDIO MANAGER - Three independent channels with voice priority
// ═══════════════════════════════════════════════════════════════════

@Observable
final class AudioManager {
    
    // Channel players
    private var musicPlayer: AVAudioPlayer?
    private var voicePlayer: AVAudioPlayer?
    private var effectsPlayer: AVAudioPlayer?
    
    // Volume levels (0.0 to 1.0)
    var musicVolume: Float = 0.30 {
        didSet { musicPlayer?.volume = musicVolume }
    }
    var voiceVolume: Float = 1.00
    var effectsVolume: Float = 0.70
    
    // ─────────────────────────────────────────────────────────────────
    // VOICE PLAYBACK (with music ducking)
    // ─────────────────────────────────────────────────────────────────
    
    func playVoice(_ filename: String) {
        guard let url = Bundle.main.url(
            forResource: filename,
            withExtension: "aac",
            subdirectory: "Audio"
        ) else { return }
        
        // Duck music while voice plays
        let originalMusicVolume = musicVolume
        musicPlayer?.setVolume(0.15, fadeDuration: 0.2)
        
        do {
            voicePlayer = try AVAudioPlayer(contentsOf: url)
            voicePlayer?.volume = voiceVolume
            voicePlayer?.play()
            
            // Restore music after voice completes
            let duration = voicePlayer?.duration ?? 0
            DispatchQueue.main.asyncAfter(deadline: .now() + duration + 0.3) {
                self.musicPlayer?.setVolume(originalMusicVolume, fadeDuration: 0.3)
            }
        } catch {
            print("Voice playback error: \(error)")
        }
    }
    
    // ─────────────────────────────────────────────────────────────────
    // EFFECTS PLAYBACK
    // ─────────────────────────────────────────────────────────────────
    
    func playEffect(_ filename: String) {
        guard let url = Bundle.main.url(
            forResource: filename,
            withExtension: "aac",
            subdirectory: "Audio/Effects"
        ) else { return }
        
        do {
            effectsPlayer = try AVAudioPlayer(contentsOf: url)
            effectsPlayer?.volume = effectsVolume
            effectsPlayer?.play()
        } catch {
            print("Effect playback error: \(error)")
        }
    }
    
    // ─────────────────────────────────────────────────────────────────
    // BACKGROUND MUSIC
    // ─────────────────────────────────────────────────────────────────
    
    func startBackgroundMusic() {
        guard let url = Bundle.main.url(
            forResource: "forest_ambient",
            withExtension: "aac",
            subdirectory: "Audio/Music"
        ) else { return }
        
        do {
            musicPlayer = try AVAudioPlayer(contentsOf: url)
            musicPlayer?.numberOfLoops = -1 // Infinite loop
            musicPlayer?.volume = musicVolume
            musicPlayer?.play()
        } catch {
            print("Music playback error: \(error)")
        }
    }
}
```

---

## 9. Navigation Pattern

### 9.1 Screen State Machine

```swift
// ═══════════════════════════════════════════════════════════════════
// GAME SCREENS - Complete navigation state
// ═══════════════════════════════════════════════════════════════════

enum GameScreen: Equatable {
    case loading
    case playerSelection
    case home
    
    // Activities
    case raetselSelection
    case puzzleMatching
    case labyrinth
    case zahlenSelection
    case wuerfel
    case waehleZahl
    
    // Rewards
    case treasure
    case videoSelection
    case videoPlayer(videoId: String, minutes: Int)
    
    // Parent
    case parentGate
    case parentDashboard
    case videoManagement
}

// ═══════════════════════════════════════════════════════════════════
// APP COORDINATOR - Central navigation
// ═══════════════════════════════════════════════════════════════════

struct AppCoordinator: View {
    @Environment(GameState.self) private var gameState
    
    var body: some View {
        AdaptiveRootView {
            ZStack {
                // Background always visible
                ForestBackground()
                
                // Current screen
                screenView
                    .transition(.opacity)
            }
        }
        .animation(BennieAnimation.screenTransition, value: gameState.currentScreen)
    }
    
    @ViewBuilder
    private var screenView: some View {
        switch gameState.currentScreen {
        case .loading:
            LoadingView()
        case .playerSelection:
            PlayerSelectionView()
        case .home:
            HomeView()
        case .raetselSelection:
            RaetselSelectionView()
        case .puzzleMatching:
            PuzzleMatchingView()
        case .labyrinth:
            LabyrinthView()
        case .zahlenSelection:
            ZahlenSelectionView()
        case .wuerfel:
            WuerfelView()
        case .waehleZahl:
            WaehleZahlView()
        case .treasure:
            TreasureView()
        case .videoSelection:
            VideoSelectionView()
        case .videoPlayer(let videoId, let minutes):
            VideoPlayerView(videoId: videoId, minutes: minutes)
        case .parentGate:
            ParentGateView()
        case .parentDashboard:
            ParentDashboardView()
        case .videoManagement:
            VideoManagementView()
        }
    }
}
```

---

## 10. Loading Screen Implementation

### 10.1 Proper Loading Sequence

```swift
// ═══════════════════════════════════════════════════════════════════
// LOADING SCREEN - Minimum display time + actual loading
// ═══════════════════════════════════════════════════════════════════

struct LoadingView: View {
    @Environment(GameState.self) private var gameState
    @Environment(AudioManager.self) private var audio
    
    @State private var progress: Double = 0
    @State private var isLoadingComplete = false
    
    /// Minimum display time for UX (children need time to process)
    private let minimumDisplayDuration: TimeInterval = 2.0
    
    /// Additional delay after loading before transition
    private let postLoadDelay: TimeInterval = 0.5
    
    var body: some View {
        VStack(spacing: 40) {
            // Title sign
            WoodSign(title: "Waldabenteuer")
            
            // Bennie waving
            BennieView(state: .waving)
                .frame(height: 300)
            
            // Progress bar
            ProgressBar(progress: progress)
                .frame(width: 400, height: 40)
            
            // Loading text
            Text("Lade Spielewelt...")
                .font(BennieFont.body(18))
                .foregroundColor(BennieColors.textOnWood)
        }
        .task {
            await performLoading()
        }
    }
    
    private func performLoading() async {
        let startTime = Date()
        
        // Actual loading tasks
        async let loadAssets = preloadAssets()
        async let loadData = loadPlayerData()
        
        // Wait for both
        _ = await (loadAssets, loadData)
        
        // Ensure minimum display time
        let elapsed = Date().timeIntervalSince(startTime)
        if elapsed < minimumDisplayDuration {
            try? await Task.sleep(for: .seconds(minimumDisplayDuration - elapsed))
        }
        
        // Animate to 100%
        withAnimation(.easeOut(duration: 0.3)) {
            progress = 1.0
        }
        
        // Play narrator
        audio.playVoice("narrator_loading_complete")
        
        // Wait for voice + delay
        try? await Task.sleep(for: .seconds(postLoadDelay))
        
        // Transition to player selection
        gameState.currentScreen = .playerSelection
    }
    
    private func preloadAssets() async {
        // Preload critical images
        // Update progress incrementally
        for i in 1...10 {
            try? await Task.sleep(for: .milliseconds(100))
            await MainActor.run {
                withAnimation {
                    progress = Double(i) / 10.0 * 0.8 // 0-80%
                }
            }
        }
    }
    
    private func loadPlayerData() async {
        // Load saved player data from UserDefaults/files
    }
}
```

---

## 11. Quick Reference Constants

```swift
// ═══════════════════════════════════════════════════════════════════
// BENNIE CONSTANTS - Use these values everywhere
// ═══════════════════════════════════════════════════════════════════

enum BennieConstants {
    
    // Touch targets
    static let minimumTouchTarget: CGFloat = 96
    static let buttonMinWidth: CGFloat = 160
    static let buttonMinHeight: CGFloat = 140
    static let gridCellSize: CGFloat = 96
    
    // Animation durations
    static let transitionDuration: Double = 0.3
    static let overlayAppearDuration: Double = 0.4
    static let breathingDuration: Double = 2.0
    
    // Coin system
    static let coinsPerLevel: Int = 1
    static let coinsForFiveMinYouTube: Int = 10
    static let coinsForTenPlusTwoMinYouTube: Int = 20
    static let celebrationMilestone: Int = 5 // Every 5 coins
    
    // Audio
    static let defaultMusicVolume: Float = 0.30
    static let defaultVoiceVolume: Float = 1.00
    static let defaultEffectsVolume: Float = 0.70
    static let musicDuckVolume: Float = 0.15
    
    // Performance
    static let targetFrameRate: Int = 60
    static let maxMemoryMB: Int = 200
    
    // Validation
    static let pathTracingTolerance: CGFloat = 30 // points
    static let pathCoverageRequired: Float = 0.70 // 70%
}
```

---

## 12. File Naming Conventions

```
═══════════════════════════════════════════════════════════════════
ASSET NAMING - Consistent patterns for all files
═══════════════════════════════════════════════════════════════════

CHARACTER IMAGES:
{character}_{state}.png
Examples:
  bennie_idle.png
  bennie_waving.png
  lemminge_curious.png

LOTTIE ANIMATIONS:
{character}_{state}.json
Examples:
  bennie_idle.json
  lemminge_celebrating.json
  confetti.json

AUDIO - VOICE:
{speaker}_{screen}_{trigger}.aac
Examples:
  narrator_loading_complete.aac
  bennie_home_greeting.aac
  bennie_celebration_5coins.aac

AUDIO - EFFECTS:
{action}.aac
Examples:
  tap_wood.aac
  success_chime.aac
  coin_collect.aac

SWIFT FILES:
{Feature}{Type}.swift
Examples:
  HomeView.swift
  WoodButton.swift
  AudioManager.swift
  BennieColors.swift

═══════════════════════════════════════════════════════════════════
```

---

## 13. QA Verification Checklist for Claude Code

Before submitting any code, verify:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CLAUDE CODE PRE-SUBMIT CHECKLIST                          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  TOUCH TARGETS:                                                              ║
║  □ All buttons have minWidth/minHeight >= 96pt?                              ║
║  □ All interactive grid cells are >= 96pt × 96pt?                            ║
║  □ contentShape(Rectangle()) used for expanded hit areas?                    ║
║                                                                              ║
║  COLORS:                                                                     ║
║  □ Using ONLY BennieColors enum values?                                      ║
║  □ No hardcoded hex strings outside BennieColors?                            ║
║  □ Lemminge are #6FA8DC blue (not green, not brown)?                         ║
║                                                                              ║
║  TYPOGRAPHY:                                                                 ║
║  □ Using BennieFont enum for all text?                                       ║
║  □ All UI text is in German?                                                 ║
║  □ No "Falsch", "Fehler", "Versuch nochmal"?                                 ║
║                                                                              ║
║  ANIMATIONS:                                                                 ║
║  □ Using BennieAnimation presets?                                            ║
║  □ No flashing, shaking, or strobing?                                        ║
║  □ Durations between 0.3-2.0s?                                               ║
║                                                                              ║
║  MEMORY:                                                                     ║
║  □ Large images use MemorySafeImage or ImageDownsampler?                     ║
║  □ Images released in onDisappear?                                           ║
║  □ No retained references to unused assets?                                  ║
║                                                                              ║
║  STRUCTURE:                                                                  ║
║  □ File in correct folder per architecture?                                  ║
║  □ @Environment(GameState.self) for state access?                            ║
║  □ Named according to conventions?                                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

*Document Version: 1.0*
*Companion to: BENNIE_BRAND_PLAYBOOK_v3_1.md*
*For: Claude Code AI-assisted development*
