# Phase 14, Stage 5: Load Time Optimization

## Overview

**Purpose**: Achieve < 2s cold start and < 0.3s screen transitions  
**Duration**: 2 days  
**Status**: Not Started  
**Priority**: CRITICAL - Direct impact on user experience (Playbook Part 5.6)

## Playbook References

### Performance Targets
- **Part 5.6**: Performance Requirements
  - App launch to Loading Screen: < 2s (cold start)
  - Loading Screen minimum display: 2-3s (UX requirement for children)
  - Loading Screen to Player Select: 2-5s total
  - Screen transitions: < 0.3s
  - Touch response: < 100ms
  - Memory usage: < 200MB

### Screen Flow
- **Part 2.1**: Screen Flow Diagram - Complete navigation paths
- **Part 2.2**: State Machine Definition - All screen transitions

### Asset Specifications
- **Part 5.2**: Asset Specifications - Image sizes and formats
- **Part 5.3**: Audio Specifications - Voice and effect file sizes
- **Part 9.7**: Asset Export Specifications - Resolution requirements

## Design Asset References

### Critical Path Assets (Must Load First)
Located in: `design/references/screens/`

**Loading Screen** (Reference_Loading_Screen.png):
- Background: 2388×1668 @2x (~500KB)
- bennie_idle.png @2x (~150KB)
- bennie_waving.png @2x (~150KB)
- 5-6 lemminge_hiding.png @2x (~80KB each = 480KB)
- narrator_loading_complete.aac (~50KB)
- **Total: ~1.3MB** - Must load in < 1.5s

### Deferred Assets (Load in Background)
**Player Selection** (Reference_Player_Selection_Screen.png):
- Background (~500KB)
- Player avatars (~100KB each)
- bennie_waving.png (already loaded)
- Voice files (~150KB total)

**Home Screen** (Reference_Menu_Screen.png):
- Background (~600KB)
- Activity signs (~200KB each × 4 = 800KB)
- Character animations (~500KB)
- Voice files (~200KB)
- **Total: ~2.1MB**

### Progressive Loading Priority

| Priority | Assets | Size | Load When |
|----------|--------|------|-----------|
| P0 - Critical | Loading screen | 1.3MB | App launch (< 1.5s) |
| P1 - High | Player selection | 0.8MB | Loading screen display |
| P2 - Medium | Home screen | 2.1MB | Player selection |
| P3 - Low | Activity screens | ~3MB each | On navigation |
| P4 - Cached | Audio sprites | 1.5MB | Background |

## Load Time Targets

| Event | Current | Target | Playbook Ref | Critical |
|-------|---------|--------|--------------|----------|
| **Cold start** | ___ms | **2000ms** | Part 5.6 | YES |
| **Loading screen display** | ___ms | **2000-3000ms** | Part 4.1 | NO (UX) |
| **Screen transition** | ___ms | **300ms** | Part 5.6, 6.2 | YES |
| **Asset load** | ___ms | **100ms** | Part 5.6 | YES |
| **Audio playback** | ___ms | **50ms** | - | YES |
| **Image decode** | ___ms | **50ms** | - | YES |

## Optimization Strategies

### 1. Deferred App Initialization

**Problem**: Too much work on main thread during launch  
**Solution**: Separate critical path from background setup

```swift
// App/BennieGameApp.swift
@main
struct BennieGameApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    
    var body: some Scene {
        WindowGroup {
            LoadingView() // Show immediately
                .onAppear {
                    // Background initialization
                    Task(priority: .utility) {
                        await AppDelegate.shared.completeSetup()
                    }
                }
        }
    }
}

// App/AppDelegate.swift
class AppDelegate: NSObject, UIApplicationDelegate {
    static let shared = AppDelegate()
    private var setupComplete = false
    
    func application(_ application: UIApplication,
                    didFinishLaunchingWithOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        
        // CRITICAL PATH (< 2s from Playbook Part 5.6):
        // Only what's needed to show LoadingView
        
        let startTime = Date()
        
        // 1. Setup core services (~100ms)
        BenniePerformanceMonitor.shared.start()
        AudioManager.shared.initializeChannels() // Part 3: 3-channel system
        
        // 2. Load Loading Screen assets only (~1.3MB, ~300ms)
        AssetLoader.shared.loadCriticalAssets()
        
        let elapsed = Date().timeIntervalSince(startTime)
        os_signpost(.event, log: .performanceLog, name: "App Launch",
                   "Duration: %.0fms", elapsed * 1000)
        
        return true
    }
    
    func completeSetup() async {
        // DEFERRED (background):
        // Everything else can wait
        
        await withTaskGroup(of: Void.self) { group in
            // Parallel background tasks
            group.addTask { await self.loadPlayerSelectionAssets() }
            group.addTask { await self.loadHomeScreenAssets() }
            group.addTask { await self.initializeGameState() }
            group.addTask { await self.warmupAnimationCache() }
        }
        
        setupComplete = true
    }
}
```

### 2. Parallel Asset Loading with Priority Queue

**Problem**: Sequential loading wastes time  
**Solution**: Load by priority in parallel

```swift
// Services/AssetLoader.swift
actor AssetLoader {
    static let shared = AssetLoader()
    
    private var loadedAssets: Set<String> = []
    private let imageCache = NSCache<NSString, UIImage>()
    private let animationCache = NSCache<NSString, LottieAnimation>()
    
    // Critical path - must complete in < 1.5s (Playbook Part 5.6)
    func loadCriticalAssets() async {
        let startTime = Date()
        
        await withTaskGroup(of: Void.self) { group in
            // Loading screen background (Reference_Loading_Screen.png)
            group.addTask {
                await self.loadImage("loading_background", size: .screen)
            }
            
            // Bennie animations for Loading screen
            group.addTask {
                await self.loadCharacterSet("bennie", states: ["idle", "waving"])
            }
            
            // Lemminge for Loading screen
            group.addTask {
                await self.loadCharacterSet("lemminge", states: ["hiding", "curious"])
            }
            
            // Narrator audio for Loading screen (Part 3.4)
            group.addTask {
                await self.loadAudio("narrator_loading_complete")
            }
        }
        
        let elapsed = Date().timeIntervalSince(startTime)
        os_signpost(.end, log: .performanceLog, name: "Critical Assets Loaded",
                   "Duration: %.0fms, Count: 4", elapsed * 1000)
    }
    
    func loadPlayerSelectionAssets() async {
        // From Reference_Player_Selection_Screen.png
        await withTaskGroup(of: Void.self) { group in
            group.addTask { await self.loadImage("player_select_background", size: .screen) }
            group.addTask { await self.loadImage("alexander_avatar", size: .small) }
            group.addTask { await self.loadImage("oliver_avatar", size: .small) }
            group.addTask { await self.loadAudio("narrator_player_question") }
            group.addTask { await self.loadAudio("narrator_hello_alexander") }
            group.addTask { await self.loadAudio("narrator_hello_oliver") }
        }
    }
    
    func loadHomeScreenAssets() async {
        // From Reference_Menu_Screen.png (Playbook Part 4.3)
        await withTaskGroup(of: Void.self) { group in
            group.addTask { await self.loadImage("home_background", size: .screen) }
            
            // Activity signs (4)
            for activity in ["raetsel", "zahlen", "zeichnen", "logik"] {
                group.addTask { await self.loadImage("sign_\(activity)", size: .medium) }
            }
            
            // Character poses
            group.addTask { await self.loadCharacterSet("bennie", states: ["pointing"]) }
            group.addTask { await self.loadCharacterSet("lemminge", states: ["mischievous"]) }
            
            // Voice files (Part 3.4)
            group.addTask { await self.loadAudio("narrator_home_question") }
            group.addTask { await self.loadAudio("bennie_greeting_part1") }
            group.addTask { await self.loadAudio("bennie_greeting_part2") }
        }
    }
    
    private func loadImage(_ name: String, size: ImageSize) async {
        guard !loadedAssets.contains(name) else { return }
        
        let startTime = Date()
        
        // Determine resolution based on size (Playbook Part 9.7)
        let scale: CGFloat = size == .screen ? 2.0 : 3.0 // iPadOnly: use @2x for backgrounds
        
        guard let image = UIImage(named: name, in: nil, compatibleWith: nil) else {
            print("⚠️ Failed to load image: \(name)")
            return
        }
        
        // Decode off main thread
        await MainActor.run {
            imageCache.setObject(image, forKey: name as NSString)
        }
        
        loadedAssets.insert(name)
        
        let elapsed = Date().timeIntervalSince(startTime)
        if elapsed > 0.05 { // Warn if > 50ms (Playbook Part 5.6)
            os_signpost(.event, log: .performanceLog, name: "Slow Image Load",
                       "Image: %{public}@, Duration: %.0fms", name, elapsed * 1000)
        }
    }
    
    private func loadCharacterSet(_ character: String, states: [String]) async {
        // Load character PNG and Lottie based on Playbook Part 5.2
        await withTaskGroup(of: Void.self) { group in
            for state in states {
                group.addTask {
                    await self.loadImage("\(character)_\(state)", size: .character)
                    await self.loadAnimation("\(character)_\(state)")
                }
            }
        }
    }
    
    private func loadAnimation(_ name: String) async {
        guard !loadedAssets.contains(name) else { return }
        
        // Load Lottie JSON (Playbook Part 9.3)
        guard let animation = LottieAnimation.named(name) else {
            print("⚠️ Failed to load animation: \(name)")
            return
        }
        
        animationCache.setObject(animation as! NSObject, forKey: name as NSString)
        loadedAssets.insert(name)
    }
    
    private func loadAudio(_ name: String) async {
        // Pre-cache audio file (Playbook Part 5.3)
        guard !loadedAssets.contains(name) else { return }
        
        AudioManager.shared.preloadAudio(name)
        loadedAssets.insert(name)
    }
    
    enum ImageSize {
        case screen   // Backgrounds
        case character // Bennie, Lemminge
        case medium   // Signs, UI elements
        case small    // Icons, avatars
    }
}
```

### 3. Screen Preloading Strategy

**Problem**: User waits for next screen to load  
**Solution**: Predict and preload next screen

```swift
// App/ScreenPreloader.swift
class ScreenPreloader {
    private let assetLoader = AssetLoader.shared
    
    // Playbook Part 2.2: State Machine transitions
    func predictNextScreen(from current: Screen) -> [Screen] {
        switch current {
        case .loading:
            return [.playerSelection] // 100% certain
            
        case .playerSelection:
            return [.home] // 100% certain
            
        case .home:
            // Most likely: Rätsel (unlocked) or Zahlen (unlocked)
            return [.raetselSelection, .zahlenSelection]
            
        case .raetselSelection:
            return [.puzzleMatching, .labyrinth] // 50/50
            
        case .zahlenSelection:
            return [.wuerfel, .waehleZahl] // 50/50
            
        case .puzzleMatching, .labyrinth, .wuerfel, .waehleZahl:
            // After activity: likely celebration if coins % 5 == 0
            return [.celebration, .home]
            
        case .celebration:
            // After celebration: treasure if coins >= 10, else continue
            return [.treasure, .home]
            
        case .treasure:
            return [.videoSelection] // if user taps YouTube button
            
        case .videoSelection:
            return [.videoPlayer] // 100% certain
            
        case .videoPlayer:
            return [.home] // 100% certain
            
        default:
            return []
        }
    }
    
    func preloadNextScreen(from current: Screen) {
        let predictions = predictNextScreen(from: current)
        
        Task(priority: .utility) {
            for screen in predictions {
                await preloadAssets(for: screen)
            }
        }
    }
    
    private func preloadAssets(for screen: Screen) async {
        switch screen {
        case .raetselSelection:
            // Preload Rätsel selection screen
            await assetLoader.loadImage("raetsel_selection_bg", size: .screen)
            
        case .puzzleMatching:
            // Preload puzzle assets (Reference_Matching_Game_Screen.png)
            await assetLoader.loadImage("puzzle_background", size: .screen)
            await assetLoader.loadImage("stone_tablet", size: .medium)
            
        case .celebration:
            // Preload celebration (Reference_Celebration_Overlay.png)
            await assetLoader.loadAnimation("confetti")
            await assetLoader.loadCharacterSet("bennie", states: ["celebrating"])
            await assetLoader.loadCharacterSet("lemminge", states: ["celebrating"])
            
        // ... other screens
            
        default:
            break
        }
    }
}

// Usage in navigation
extension AppCoordinator {
    func navigate(to screen: Screen) {
        // Update current screen
        currentScreen = screen
        
        // Preload next likely screens
        ScreenPreloader.shared.preloadNextScreen(from: screen)
    }
}
```

### 4. Optimized Screen Transitions

**Problem**: Transitions feel sluggish  
**Solution**: GPU-accelerated animations with minimal layout

```swift
// App/TransitionManager.swift
struct TransitionManager {
    // Playbook Part 6.2: Transition animations (0.3s target)
    static func transition(from: Screen, to: Screen) -> AnyTransition {
        // Use GPU-accelerated asymmetric transitions
        .asymmetric(
            insertion: .opacity
                .combined(with: .scale(scale: 0.98))
                .animation(.easeOut(duration: 0.15)),
            removal: .opacity
                .animation(.easeIn(duration: 0.15))
        )
    }
}

// Optimize View hierarchy for fast transitions
struct OptimizedScreenContainer<Content: View>: View {
    let content: Content
    @State private var isReady = false
    
    var body: some View {
        ZStack {
            if isReady {
                content
                    .transition(TransitionManager.transition(from: .home, to: .raetselSelection))
            }
        }
        .task {
            // Prepare view off-screen
            await prepareView()
            withAnimation {
                isReady = true
            }
        }
    }
    
    private func prepareView() async {
        // Pre-layout and pre-render
        await MainActor.run {
            // Force layout pass off-screen
            _ = content.frame(width: 1194, height: 834)
        }
    }
}
```

### 5. Loading Screen Smart Duration

**Problem**: Loading screen needs to display 2-3s for UX (Playbook Part 4.1), but assets load faster  
**Solution**: Artificial delay after assets loaded

```swift
// Features/Loading/LoadingView.swift
struct LoadingView: View {
    @State private var progress: Double = 0
    @State private var assetsLoaded = false
    @State private var minimumDisplayMet = false
    
    var body: some View {
        ZStack {
            // Loading screen UI (Reference_Loading_Screen.png)
            LoadingScreenBackground()
            BennieLoadingAnimation()
            LemmingeLoadingAnimations()
            ProgressBar(progress: progress)
        }
        .task {
            await loadAssets()
        }
    }
    
    private func loadAssets() async {
        let startTime = Date()
        
        // Parallel: Load assets AND run minimum display timer
        await withTaskGroup(of: Void.self) { group in
            // Task 1: Load critical assets
            group.addTask {
                await AssetLoader.shared.loadCriticalAssets()
                await AssetLoader.shared.loadPlayerSelectionAssets()
                
                // Assets loaded
                await MainActor.run {
                    assetsLoaded = true
                    progress = 1.0
                }
            }
            
            // Task 2: Minimum display time (2s from Playbook Part 4.1)
            group.addTask {
                // Animate progress smoothly regardless of actual load time
                for percent in 0...100 {
                    await MainActor.run {
                        progress = Double(percent) / 100.0
                    }
                    try? await Task.sleep(nanoseconds: 20_000_000) // 20ms per %
                }
                
                await MainActor.run {
                    minimumDisplayMet = true
                }
            }
        }
        
        // Wait for BOTH conditions
        while !assetsLoaded || !minimumDisplayMet {
            try? await Task.sleep(nanoseconds: 100_000_000)
        }
        
        // Play narrator voice (Part 3.4)
        AudioManager.shared.playNarrator("narrator_loading_complete")
        
        // Wait for voice to finish (~2s)
        try? await Task.sleep(nanoseconds: 2_000_000_000)
        
        // Navigate to Player Selection (Playbook Part 2.2)
        AppCoordinator.shared.navigate(to: .playerSelection)
        
        let elapsed = Date().timeIntervalSince(startTime)
        os_signpost(.end, log: .performanceLog, name: "Loading Screen Complete",
                   "Total Duration: %.1fs", elapsed)
    }
}
```

## Testing Protocol

### Cold Start Tests

```swift
// Tests/PerformanceTests/LoadTimeTests.swift
class LoadTimeTests: XCTestCase {
    
    func testColdStartTime() {
        // Measure from app launch to LoadingView visible
        measure(metrics: [XCTClockMetric(), XCTMemoryMetric()]) {
            let app = XCUIApplication()
            app.launch()
            
            // Wait for LoadingView
            let loadingScreen = app.otherElements["LoadingView"]
            XCTAssertTrue(loadingScreen.waitForExistence(timeout: 2.0))
        }
        
        // Assert: < 2s (Playbook Part 5.6)
        // Xcode will report if metric exceeds baseline
    }
    
    func testScreenTransitions() {
        let app = XCUIApplication()
        app.launch()
        
        // Playbook Part 2.2: Test all transitions
        let transitions: [(from: String, to: String, maxDuration: TimeInterval)] = [
            ("LoadingView", "PlayerSelectionView", 0.3),
            ("PlayerSelectionView", "HomeView", 0.3),
            ("HomeView", "PuzzleMatchingView", 0.3),
            ("PuzzleMatchingView", "CelebrationOverlay", 0.3),
        ]
        
        for (from, to, maxDuration) in transitions {
            let startTime = Date()
            
            // Trigger transition
            app.buttons[from].tap()
            
            // Wait for next screen
            let nextScreen = app.otherElements[to]
            XCTAssertTrue(nextScreen.waitForExistence(timeout: maxDuration))
            
            let elapsed = Date().timeIntervalSince(startTime)
            XCTAssertLessThan(elapsed, maxDuration, "Transition \(from) -> \(to) too slow")
        }
    }
    
    func testAssetLoadTime() {
        // Measure individual asset loads
        measure {
            Task {
                await AssetLoader.shared.loadImage("bennie_idle", size: .character)
            }
        }
        
        // Assert: < 100ms (Playbook Part 5.6)
    }
}
```

## Deliverables

1. **Optimized Launch Sequence**
   - `App/AppDelegate.swift` - Deferred initialization
   - `Services/AssetLoader.swift` - Parallel loading
   - Verification: Cold start < 2s

2. **Screen Preloader**
   - `App/ScreenPreloader.swift` - Predictive loading
   - Verification: Next screen loads instantly

3. **Transition Manager**
   - `App/TransitionManager.swift` - GPU-accelerated transitions
   - Verification: All transitions < 0.3s

4. **Load Time Report**
   - `14_performance/reports/load_time_report.md`

## Success Criteria

- ✅ Cold start < 2s (Playbook Part 5.6)
- ✅ Loading screen displays 2-3s (UX requirement)
- ✅ Screen transitions < 0.3s
- ✅ Asset loads < 100ms each
- ✅ No visible delays in navigation

## Next Stage
**Stage 6: Touch Response Optimization** - Achieve < 100ms touch latency
