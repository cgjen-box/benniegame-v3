# Stage 2: Memory Optimization

## Purpose
Reduce memory footprint to meet < 200MB target, especially during peak usage (celebrations).

## Duration
2 days

## Playbook References
- **Part 5.6**: Performance Requirements (< 200MB target)
- **Part 5.2**: Asset Specifications (image formats, resolutions)
- **Part 5.3**: Audio Specifications (formats, bitrates)
- **Part 6.1**: Animation Principles (Lottie optimization)
- **Part 9.2**: Gemini Image Generation (asset quality)
- **Part 9.3**: Ludo.ai Animation Pipeline (Lottie file sizes)
- **Part 9.4**: ElevenLabs Voice Generation (audio streaming)
- **Part 9.7**: Asset Export Specifications (resolution table)
- **Part 10.3**: QA Verification Matrix (memory testing)

## Design Asset References

### Screen Assets by Memory Priority
| Priority | Screen | Reference File | Est. Memory | Strategy |
|----------|--------|----------------|-------------|----------|
| **HIGH** | Celebration | `Reference_Celebration_Overlay.png` | ~45MB peak | Lazy load confetti |
| **HIGH** | Matching 6×6 | `Reference_Matching_Game_Screen.png` | ~30MB | Pool grid cells |
| MEDIUM | Home | `Reference_Menu_Screen.png` | ~25MB | Cache signs |
| MEDIUM | Treasure | `Reference_Treasure_Screen.png` | ~25MB | Preload chest |
| MEDIUM | Player Select | `Reference_Player_Selection_Screen.png` | ~20MB | Cache avatars |
| MEDIUM | Numbers | `Reference_Numbers_Game_Screen.png` | ~20MB | Pool buttons |
| LOW | Loading | `Reference_Loading_Screen.png` | ~15MB | Minimal load |
| LOW | Labyrinth | `Reference_Layrinth_Game_Screen.png` | ~15MB | Path only |

### Character Asset References
**Bennie Assets** (`design/references/character/bennie/`)
- `states/` - All 6 expression states (idle, waving, pointing, thinking, encouraging, celebrating)
- Memory per state: ~4MB (@3x resolution)
- **Strategy**: Load only 2-3 states per screen, cache current + next

**Lemminge Assets** (`design/references/character/lemminge/`)
- `states/` - All 6 expression states (idle, curious, excited, celebrating, hiding, mischievous)
- Memory per state: ~1.5MB (@3x resolution)
- **Strategy**: Shared pool across screens, max 3 states loaded

### Component Asset References
**UI Components** (`design/references/components/`)
- Wood buttons, signs, progress bars
- Memory budget: ~15MB total
- **Strategy**: Reuse views, single texture atlas

## Memory Budget

### Target Allocation
```
╔══════════════════════════════════════════════════════════╗
║                 MEMORY BUDGET (200MB TOTAL)              ║
║                  (Playbook Part 5.6 Target)              ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  System/Framework Overhead:        ~40MB (20%)          ║
║  Character Assets (Loaded):        ~25MB (12%)          ║
║    - Bennie (2-3 states):          ~12MB                ║
║    - Lemminge (3 states × 6):      ~13MB                ║
║  Background Images:                ~30MB (15%)          ║
║    - Current screen background:    ~15MB                ║
║    - Cached previous/next:         ~15MB                ║
║  UI Components:                    ~15MB ( 7%)          ║
║    - Buttons, signs, decorations:  ~15MB                ║
║  Lottie Animations:                ~20MB (10%)          ║
║    - Active animations:            ~10MB                ║
║    - Cached pool:                  ~10MB                ║
║  Audio (Cached):                   ~30MB (15%)          ║
║    - Current screen audio:         ~15MB                ║
║    - Preloaded next screen:        ~10MB                ║
║    - Background music stream:      ~5MB                 ║
║  Game State & Data:                ~10MB ( 5%)          ║
║  Video Player:                     ~20MB (10%)          ║
║  Buffer/Headroom:                  ~10MB ( 5%)          ║
║                                                          ║
║  TOTAL:                           200MB (100%)          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

### Peak Usage Scenarios
```
SCENARIO: Celebration at 10 coins
════════════════════════════════════════════════════════════
Reference: Reference_Celebration_Overlay.png

Memory Components:
- Base screen (dimmed):           ~25MB
- Overlay background:             ~5MB
- Bennie celebrating animation:   ~4MB
- 3× Lemminge celebrating:        ~4.5MB
- Confetti particle system:       ~10MB
- Celebration audio:              ~2MB
─────────────────────────────────────────────────────────
TOTAL PEAK:                       ~50.5MB

STRATEGY: Release confetti after 3s, return to ~40MB
```

## Memory Optimization Strategies

### Strategy 1: Lazy Asset Loading
**Impact**: Reduce baseline memory by ~50MB
**Playbook**: Part 9.7 - Asset Export Specifications

#### Implementation
```swift
// File: Sources/Services/BennieAssetLoader.swift

class BennieAssetLoader {
    // Load assets on-demand per screen (Playbook Part 5.2)
    
    private var loadedAssets: [String: Any] = [:]
    private let cache = NSCache<NSString, AnyObject>()
    
    func loadAsset(for screen: Screen) async {
        switch screen {
        case .loading:
            // Reference: Reference_Loading_Screen.png
            // Load: loading background, Bennie idle, 5-6 Lemminge hiding
            await loadImage("forest_loading_background")
            await loadCharacter(.bennie, state: .idle)
            await loadCharacters(.lemminge, states: [.hiding], count: 6)
            
        case .playerSelect:
            // Reference: Reference_Player_Selection_Screen.png
            // Load: player avatars, Bennie waving, 4 Lemminge
            await loadImage("player_selection_background")
            await loadCharacter(.bennie, state: .waving)
            await loadPlayerAvatars()
            await loadCharacters(.lemminge, states: [.hiding], count: 4)
            
        case .home:
            // Reference: Reference_Menu_Screen.png
            // Load: home background, activity signs, chest, characters
            await loadImage("home_background")
            await loadCharacter(.bennie, state: .pointing)
            await loadCharacters(.lemminge, states: [.mischievous, .hiding], count: 2)
            await loadActivitySigns()
            await loadChest()
            
        case .puzzleMatching:
            // Reference: Reference_Matching_Game_Screen.png
            // Load: grid background, Bennie, Lemminge, color palette
            await loadImage("puzzle_background")
            await loadCharacter(.bennie, state: .pointing)
            await loadCharacters(.lemminge, states: [.curious], count: 2)
            await loadColorPalette()
            
        case .celebration:
            // Reference: Reference_Celebration_Overlay.png
            // CRITICAL: Highest memory usage - load minimal, release fast
            await loadCharacter(.bennie, state: .celebrating)
            await loadCharacters(.lemminge, states: [.celebrating], count: 3)
            await loadConfetti() // Will auto-release after 3s
            
        // ... other screens
        }
    }
    
    func unloadAsset(for screen: Screen) {
        // Unload assets when leaving screen
        // Keep in cache for quick return (Playbook Part 5.6 - 0.3s transition)
        switch screen {
        case .celebration:
            // Aggressive cleanup for high-memory screen
            releaseConfetti()
            releaseCharacterState(.celebrating)
        default:
            // Normal cleanup
            releaseNonCachedAssets()
        }
    }
    
    private func loadCharacter(_ character: Character, state: CharacterState) async {
        // Reference: design/references/character/{character}/states/
        let path = "design/references/character/\(character.rawValue)/states/\(state.rawValue)"
        // Load with downsampling if needed (Playbook Part 9.7 resolution table)
    }
}
```

**Reference**: See `design/references/screens/` for asset requirements per screen

### Strategy 2: Image Asset Optimization
**Impact**: Reduce image memory by ~30MB
**Playbook**: Part 5.2 - Asset Specifications, Part 9.7 - Resolution Table

#### 2.1 Texture Compression
```swift
// Enable asset compression in Xcode:
// Asset Catalog → Compression → Lossless/Lossy

Benefits (Playbook Part 5.2):
- PNG → Compressed PNG: 30-50% reduction
- No quality loss for UI elements
- Automatic for all @2x/@3x assets

Apply to:
- All screens: design/references/screens/*.png
- All characters: design/references/character/**/*.png
- All components: design/references/components/*.png
```

#### 2.2 Image Downsampling
```swift
// For large backgrounds, downsample to exact display size
// Target: iPad 1194×834 points = 2388×1668 @2x (Playbook Part 9.7)

func downsampleImage(at url: URL, to size: CGSize) -> UIImage? {
    let options = [
        kCGImageSourceCreateThumbnailFromImageAlways: true,
        kCGImageSourceShouldCacheImmediately: true,
        kCGImageSourceCreateThumbnailWithTransform: true,
        kCGImageSourceThumbnailMaxPixelSize: max(size.width, size.height) * UIScreen.main.scale
    ] as CFDictionary
    
    guard let imageSource = CGImageSourceCreateWithURL(url as CFURL, nil),
          let image = CGImageSourceCreateThumbnailAtIndex(imageSource, 0, options) else {
        return nil
    }
    
    return UIImage(cgImage: image)
}
```

**Apply to**: All background images from `design/references/screens/`
- Reference_Loading_Screen.png → 2388×1668 @2x
- Reference_Menu_Screen.png → 2388×1668 @2x
- Reference_Matching_Game_Screen.png → 2388×1668 @2x
- Reference_Numbers_Game_Screen.png → 2388×1668 @2x
- Reference_Treasure_Screen.png → 2388×1668 @2x
- Reference_Layrinth_Game_Screen.png → 2388×1668 @2x
- Reference_Player_Selection_Screen.png → 2388×1668 @2x
- Reference_Celebration_Overlay.png → Transparent overlay only

#### 2.3 Character Sprite Optimization
```swift
// Cache commonly used character poses
// Reference: Playbook Part 5.2 - Character Sprite Sizes
// - Bennie: 300×450pt (@2x = 600×900px, @3x = 900×1350px)
// - Lemminge: 80×100pt (@2x = 160×200px, @3x = 240×300px)

class CharacterCache {
    private let cache = NSCache<NSString, UIImage>()
    
    init() {
        // Set memory limit to 25MB for character assets (Playbook Part 5.6)
        cache.totalCostLimit = 25 * 1024 * 1024
        cache.countLimit = 20 // Max 20 character images
    }
    
    func image(for character: Character, pose: Pose) -> UIImage? {
        let key = "\(character.id)_\(pose.rawValue)" as NSString
        
        if let cached = cache.object(forKey: key) {
            return cached
        }
        
        // Load from design/references/character/{character}/states/{pose}.png
        if let image = loadImage(character: character, pose: pose) {
            cache.setObject(image, forKey: key, cost: imageCost(image))
            return image
        }
        
        return nil
    }
    
    private func imageCost(_ image: UIImage) -> Int {
        // Calculate actual memory cost
        // Formula: width × height × 4 (RGBA) × scale²
        let size = image.size
        let scale = image.scale
        return Int(size.width * size.height * 4 * scale * scale)
    }
}
```

**Reference**: `design/references/character/` for character assets
- `bennie/states/` - 6 poses × ~4MB = 24MB total (load 2-3 at time)
- `lemminge/states/` - 6 poses × ~1.5MB = 9MB total (load 3 at time)

### Strategy 3: Lottie Animation Optimization
**Impact**: Reduce animation memory by ~15MB
**Playbook**: Part 6.1 - Animation Principles, Part 9.3 - Ludo.ai Pipeline

#### 3.1 Animation Compression
```swift
// Optimize Lottie JSON files (Playbook Part 9.3):
// 1. Remove unused layers
// 2. Simplify paths
// 3. Reduce keyframe density

Target: < 100KB per animation (Playbook Part 5.2)

Animations by Priority:
HIGH (must optimize):
- confetti.json (Celebration) - Target < 80KB
- bennie_celebrating.json - Target < 100KB
- lemminge_celebrating.json - Target < 80KB

MEDIUM:
- bennie_idle.json, bennie_waving.json
- lemminge_idle.json, lemminge_curious.json
- coin_fly.json, progress_fill.json

Tool: lottie-optimizer
npm install -g lottie-optimizer
lottie-optimizer input.json output.json --quality 0.8
```

#### 3.2 Animation Pooling
```swift
// Reuse animation instances across screens (Playbook Part 6.1)
class AnimationPool {
    private var pool: [String: LottieAnimationView] = [:]
    private let maxPoolSize = 10 // Limit memory
    
    func getAnimation(named: String) -> LottieAnimationView {
        if let existing = pool[named] {
            existing.stop()
            return existing
        }
        
        // Check pool size
        if pool.count >= maxPoolSize {
            // Remove least recently used
            releaseLRU()
        }
        
        let animation = LottieAnimationView(name: named)
        pool[named] = animation
        return animation
    }
    
    func releaseAnimation(named: String) {
        pool[named]?.stop()
        // Keep in pool for reuse unless memory pressure
    }
    
    func releaseAll() {
        pool.values.forEach { $0.stop() }
        pool.removeAll()
    }
}
```

**Animation Files** (Part 9.3 - Ludo.ai Animation Pipeline):
- bennie_idle.json, bennie_waving.json, bennie_celebrating.json
- lemminge_idle.json, lemminge_celebrating.json
- confetti.json (Release after 3s!)
- coin_fly.json, progress_fill.json

### Strategy 4: Audio Memory Management
**Impact**: Reduce audio memory by ~20MB
**Playbook**: Part 5.3 - Audio Specifications, Part 9.4 - Voice Generation

#### 4.1 Stream Long Audio
```swift
// Don't load entire audio files into memory (Playbook Part 5.3)
// - Narrator voice: AAC, 44.1kHz, 128kbps
// - Bennie voice: AAC, 44.1kHz, 128kbps
// - Sound effects: AAC, 44.1kHz, 128kbps
// - Background music: AAC, 44.1kHz, 192kbps

class BennieAudioManager {
    func playAudio(_ file: String, streaming: Bool = true) {
        if streaming {
            // Stream from file system (Playbook Part 9.4)
            player = AVPlayer(url: fileURL)
        } else {
            // Load into memory (only for short sounds < 1s)
            player = try AVAudioPlayer(contentsOf: fileURL)
        }
    }
}

Rules (Playbook Part 5.3):
- Narrator/Bennie voice: STREAM (1-3s files, ~50-150KB each)
- Sound effects: LOAD (< 0.5s files, ~10-30KB each)
  * tap_wood.aac, success_chime.aac, coin_collect.aac
  * gentle_boop.aac, path_draw.aac
- Background music: STREAM (loop, ~500KB)
  * forest_ambient.aac
- Celebration: PRELOAD (2s, ~100KB)
  * celebration_fanfare.aac
```

#### 4.2 Audio Caching Strategy
```swift
// Cache only currently active screen's audio
// Preload next screen's audio while current screen is active

class AudioPreloader {
    private var preloadedAudio: [String: Data] = [:]
    private let maxCacheSize = 30 * 1024 * 1024 // 30MB limit (Playbook Part 5.6)
    
    func preloadForNextScreen(_ screen: Screen) async {
        let audioFiles = getAudioFiles(for: screen)
        
        for file in audioFiles {
            // Only preload if within memory budget
            if getCurrentCacheSize() < maxCacheSize {
                await cache.preload(file)
            }
        }
    }
    
    private func getAudioFiles(for screen: Screen) -> [String] {
        // Map screens to their audio requirements
        switch screen {
        case .loading:
            return ["narrator_loading_complete.aac"]
        case .playerSelect:
            return ["narrator_player_question.aac", "narrator_hello_alexander.aac", "narrator_hello_oliver.aac"]
        case .home:
            return ["narrator_home_question.aac", "bennie_greeting_part1.aac", "bennie_greeting_part2.aac"]
        case .celebration:
            return ["celebration_fanfare.aac", "bennie_celebration_5.aac", "bennie_celebration_10.aac"]
        // ... other screens
        default:
            return []
        }
    }
}
```

**Audio File Checklist** (Part 9.4 - Complete Voice Line Checklist):
See Playbook Part 9.4 for complete list of 50+ audio files

### Strategy 5: View Hierarchy Optimization
**Impact**: Reduce UI memory by ~10MB
**Playbook**: Part 5.2 - Touch Targets (≥96pt minimum)

#### 5.1 View Recycling
```swift
// Recycle complex views (e.g., grid cells, buttons)
// Important for Puzzle 6×6 grid (36 cells) and Number buttons (10 buttons)

class ViewPool<T: UIView> {
    private var pool: [T] = []
    private let maxPoolSize: Int
    
    init(maxSize: Int = 50) {
        self.maxPoolSize = maxSize
    }
    
    func dequeue() -> T? {
        return pool.isEmpty ? nil : pool.removeLast()
    }
    
    func recycle(_ view: T) {
        view.prepareForReuse()
        
        if pool.count < maxPoolSize {
            pool.append(view)
        }
        // else: let view deallocate
    }
}

// Usage:
let gridCellPool = ViewPool<PuzzleGridCell>(maxSize: 36)
let buttonPool = ViewPool<WoodButton>(maxSize: 15)
```

**Apply to**:
- Puzzle grid cells (Reference_Matching_Game_Screen.png) - Up to 36 cells for 6×6
- Number buttons (Reference_Numbers_Game_Screen.png) - 10 buttons (0-9)
- Color picker buttons (Reference_Matching_Game_Screen.png) - 3-4 colors

#### 5.2 Remove Hidden View Layers
```swift
// When screen is not visible, remove from hierarchy
// Critical for maintaining 200MB limit (Playbook Part 5.6)

struct SmartNavigationStack: View {
    @State private var activeScreens: [Screen] = []
    
    var body: some View {
        ZStack {
            // Only keep current screen + adjacent screens in memory
            ForEach(activeScreens) { screen in
                screenView(for: screen)
            }
        }
        .onChange(of: currentScreen) { newScreen in
            updateActiveScreens(current: newScreen)
        }
    }
    
    private func updateActiveScreens(current: Screen) {
        // Keep only: previous + current + next
        activeScreens = [
            current.previous,
            current,
            current.next
        ].compactMap { $0 }
        
        // Remove others from hierarchy to free memory
    }
}
```

### Strategy 6: Data Structure Optimization
**Impact**: Reduce data memory by ~5MB

#### 6.1 Optimize PlayerData
```swift
// BEFORE:
struct PlayerData {
    var coins: Int
    var activityProgress: [String: Int]  // String keys = waste
    var videosWatched: [VideoRecord]  // Could be hundreds = 2-3MB
    var learningProfile: LearningProfile  // Large nested structure = 2MB
}

// AFTER:
struct PlayerData {
    var coins: Int  // 8 bytes
    var activityProgress: [ActivityType: Int]  // Use enum = 32 bytes
    var recentVideos: [VideoRecord]  // Last 50 only = ~500KB
    var learningProfile: CompactLearningProfile  // Optimized = ~200KB
}

enum ActivityType: UInt8 {
    case raetsel = 0
    case zahlen = 1
    // Future:
    // case zeichnen = 2
    // case logik = 3
}

struct CompactLearningProfile {
    var averageSolveTime: UInt16  // Seconds, max 65535
    var mistakeFrequency: UInt8   // Percentage 0-100
    var difficultyLevel: UInt8    // 0-100
    // Packed into ~20 bytes vs 200+ bytes before
}
```

## Memory Leak Prevention

### Common Leak Patterns to Fix

#### 1. Retain Cycles in Closures
```swift
// BAD:
class ViewModel {
    var completion: (() -> Void)?
    
    func setup() {
        completion = {
            self.doSomething()  // Strong reference cycle
        }
    }
}

// GOOD:
class ViewModel {
    var completion: (() -> Void)?
    
    func setup() {
        completion = { [weak self] in
            self?.doSomething()
        }
    }
}
```

#### 2. Timer Leaks
```swift
// BAD:
class Screen {
    var timer: Timer?
    
    func start() {
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
            self.update()  // Timer holds strong reference to self
        }
    }
}

// GOOD:
class Screen {
    var timer: Timer?
    
    func start() {
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
            self?.update()
        }
    }
    
    func stop() {
        timer?.invalidate()
        timer = nil
    }
    
    deinit {
        stop()
    }
}
```

#### 3. Notification Observer Leaks
```swift
// BAD:
class Screen {
    init() {
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(handleNotification),
            name: .gameStateChanged,
            object: nil
        )
    }
}

// GOOD:
class Screen {
    private var observers: [NSObjectProtocol] = []
    
    init() {
        let observer = NotificationCenter.default.addObserver(
            forName: .gameStateChanged,
            object: nil,
            queue: .main
        ) { [weak self] notification in
            self?.handleNotification(notification)
        }
        observers.append(observer)
    }
    
    deinit {
        observers.forEach { NotificationCenter.default.removeObserver($0) }
    }
}
```

#### 4. Lottie Animation Leaks
```swift
// BAD:
class CelebrationView {
    var confettiAnimation: LottieAnimationView?
    
    func showCelebration() {
        confettiAnimation = LottieAnimationView(name: "confetti")
        confettiAnimation?.play()
        // Never released! Memory leak!
    }
}

// GOOD:
class CelebrationView {
    var confettiAnimation: LottieAnimationView?
    
    func showCelebration() {
        confettiAnimation = LottieAnimationView(name: "confetti")
        confettiAnimation?.play { [weak self] finished in
            // Release after animation completes (3s per Playbook Part 6.1)
            self?.confettiAnimation?.stop()
            self?.confettiAnimation = nil
        }
    }
    
    deinit {
        confettiAnimation?.stop()
        confettiAnimation = nil
    }
}
```

## Memory Monitoring

### Real-Time Monitor
```swift
// File: Sources/Services/BennieMemoryMonitor.swift

class BennieMemoryMonitor {
    static let shared = BennieMemoryMonitor()
    
    // CRITICAL THRESHOLDS (Playbook Part 5.6)
    private let targetMemory: UInt64 = 200 * 1024 * 1024  // 200MB
    private let warningThreshold: UInt64 = 180 * 1024 * 1024  // 180MB (90%)
    private let criticalThreshold: UInt64 = 190 * 1024 * 1024  // 190MB (95%)
    
    var currentUsage: UInt64 {
        var info = mach_task_basic_info()
        var count = mach_msg_type_number_t(MemoryLayout<mach_task_basic_info>.size)/4
        
        let kerr: kern_return_t = withUnsafeMutablePointer(to: &info) {
            $0.withMemoryRebound(to: integer_t.self, capacity: 1) {
                task_info(mach_task_self_,
                         task_flavor_t(MACH_TASK_BASIC_INFO),
                         $0,
                         &count)
            }
        }
        
        return kerr == KERN_SUCCESS ? info.resident_size : 0
    }
    
    var usageInMB: Double {
        Double(currentUsage) / 1024.0 / 1024.0
    }
    
    var percentOfTarget: Double {
        Double(currentUsage) / Double(targetMemory) * 100.0
    }
    
    func checkMemoryPressure() -> MemoryPressure {
        if currentUsage >= criticalThreshold {
            return .critical
        } else if currentUsage >= warningThreshold {
            return .warning
        } else {
            return .normal
        }
    }
    
    func logMemoryWarning(screen: String) {
        let pressure = checkMemoryPressure()
        
        switch pressure {
        case .critical:
            print("🔴 CRITICAL MEMORY: \(usageInMB) MB (\(percentOfTarget)%) on \(screen)")
            print("   Target: 200MB | Current: \(usageInMB) MB | OVER LIMIT!")
        case .warning:
            print("⚠️  WARNING MEMORY: \(usageInMB) MB (\(percentOfTarget)%) on \(screen)")
            print("   Target: 200MB | Current: \(usageInMB) MB | Approaching limit")
        case .normal:
            print("✅ Memory OK: \(usageInMB) MB (\(percentOfTarget)%) on \(screen)")
        }
    }
    
    enum MemoryPressure {
        case normal
        case warning
        case critical
    }
}
```

### Memory Pressure Handling
```swift
// In each major view:
.onReceive(NotificationCenter.default.publisher(for: UIApplication.didReceiveMemoryWarningNotification)) { _ in
    handleMemoryWarning()
}

func handleMemoryWarning() {
    // Step 1: Clear caches
    BennieAssetLoader.shared.clearCache()
    AnimationPool.shared.releaseAll()
    
    // Step 2: Release unused assets
    releaseNonVisibleScreenAssets()
    
    // Step 3: Reduce quality if needed
    if BennieMemoryMonitor.shared.checkMemoryPressure() == .critical {
        // Load @2x instead of @3x temporarily
        enableLowMemoryMode()
    }
}
```

## Testing Protocol

### Memory Test Suite

#### Test 1: Baseline Memory (Per Screen)
```
REFERENCE: All 8 screen reference files

STEPS:
1. Launch app → Loading Screen
   - Measure: Should be ~60MB (Reference_Loading_Screen.png)
2. Navigate to Player Select
   - Measure: Should be ~65MB (Reference_Player_Selection_Screen.png)
3. Select player → Home Screen
   - Measure: Should be ~75MB (Reference_Menu_Screen.png)
4. Enter Puzzle Matching 3×3
   - Measure: Should be ~80MB (Reference_Matching_Game_Screen.png)
5. Enter Puzzle Matching 6×6
   - Measure: Should be ~95MB (HIGH MEMORY SCREEN)
6. Enter Numbers Game
   - Measure: Should be ~75MB (Reference_Numbers_Game_Screen.png)
7. Enter Labyrinth
   - Measure: Should be ~70MB (Reference_Layrinth_Game_Screen.png)
8. Trigger Celebration (5 coins)
   - Measure: Should be ~110MB (Reference_Celebration_Overlay.png)
9. Trigger Celebration (10 coins)
   - Measure: Should be ~115MB (PEAK SCENARIO)
10. Treasure Screen
    - Measure: Should be ~85MB (Reference_Treasure_Screen.png)

TARGET: Each screen within budget allocation
PASS: All screens < 200MB, peak < 115MB
FAIL: Any screen exceeds 200MB
```

#### Test 2: Memory Stability
```
STEPS:
1. Complete full user journey 10 times:
   - Loading → Player Select → Home
   - Play Puzzle (earn 5 coins) → Celebration
   - Play Numbers (earn 5 more coins) → Celebration
   - Treasure Screen → Back to Home
2. Measure memory at START of each lap
3. Calculate memory growth

EXPECTED: Memory stable within ±10MB across all laps
PASS: Memory variance < 10MB
FAIL: Memory grows > 10MB per lap (indicates leak)
```

#### Test 3: Peak Memory (Celebration Stress Test)
```
SCENARIO: Rapid celebrations
REFERENCE: Reference_Celebration_Overlay.png

STEPS:
1. Earn 5 coins → Trigger celebration → Tap "Weiter"
2. Immediately earn 5 more coins → Trigger celebration
3. Repeat 4 times (total 20 coins, 4 celebrations)
4. Measure peak memory during each celebration

EXPECTED:
- 1st celebration: ~110MB
- 2nd celebration: ~112MB (cache warming)
- 3rd celebration: ~112MB (stable)
- 4th celebration: ~112MB (stable)

PASS: Peak < 200MB, stable after 2nd celebration
FAIL: Peak >= 200MB OR memory grows with each celebration
```

#### Test 4: Leak Detection (Instruments)
```
TOOL: Xcode Instruments - Leaks

STEPS:
1. Launch Instruments with Leaks template
2. Navigate through all screens in sequence:
   Loading → Player Select → Home → Puzzle → Numbers → 
   Labyrinth → Celebration → Treasure → Home
3. Return to Home screen
4. Wait 30 seconds
5. Check for leaks

CRITICAL AREAS TO WATCH:
- Celebration overlay (confetti animation)
- Character animations (Lottie views)
- Audio players
- Timers
- Notification observers

PASS: Zero leaks detected
FAIL: Any leaks found, especially in critical areas
```

#### Test 5: Extended Play Session
```
DURATION: 30 minutes continuous play

STEPS:
1. Launch app
2. Play activities continuously for 30 minutes
3. Record memory every 5 minutes
4. Complete multiple celebrations

EXPECTED MEMORY PROFILE:
- 0 min:  ~75MB (home)
- 5 min:  ~85MB (in activity)
- 10 min: ~90MB (celebrations)
- 15 min: ~90MB (stable)
- 20 min: ~90MB (stable)
- 25 min: ~90MB (stable)
- 30 min: ~90MB (stable)

PASS: Memory plateaus by 15 min, stays < 200MB
FAIL: Memory continuously grows OR exceeds 200MB
```

#### Test 6: Low Memory Simulation
```
STEPS:
1. Enable iOS Simulator → Debug → Simulate Memory Warning
2. Verify app responds correctly:
   - Clears caches
   - Releases non-essential assets
   - Continues functioning
3. Measure memory before and after warning

EXPECTED:
- Before warning: ~90MB (normal operation)
- After warning: ~70MB (aggressive cleanup)
- App continues to work normally

PASS: Memory reduces by >15%, no crashes
FAIL: App crashes OR memory doesn't reduce
```

## Deliverables

### 1. Optimized Asset Loader
**File**: `Sources/Services/BennieAssetLoader.swift`
- Lazy loading implementation
- Screen-specific asset loading per reference files
- Asset caching strategy
- Memory-aware loading with budget checks
- **References**: All 8 screen reference files

### 2. Memory Monitor Dashboard
**File**: `Sources/Services/BennieMemoryMonitor.swift`
- Real-time memory tracking
- Automatic warnings at 180MB, 190MB thresholds
- Performance logging
- Integration with Stage 1 BenniePerformanceMonitor

### 3. Character Cache System
**File**: `Sources/Services/CharacterCache.swift`
- Bennie state caching (6 poses)
- Lemminge state caching (6 poses)
- LRU eviction strategy
- 25MB memory limit enforcement
- **References**: design/references/character/

### 4. Animation Pool
**File**: `Sources/Services/AnimationPool.swift`
- Lottie animation reuse
- Confetti auto-release after 3s
- 10 animation pool size limit
- **References**: Part 9.3 animation files

### 5. Memory Optimization Report
**File**: `14_performance/reports/memory_optimization_report.md`
- Before/after measurements per screen
- Strategies applied with playbook citations
- Impact assessment
- Leak test results
- Peak memory analysis

## Success Criteria

### Stage Complete When:
- ✅ Memory < 200MB on all screens (Playbook Part 5.6)
- ✅ Memory < 200MB during celebrations (Reference_Celebration_Overlay.png)
- ✅ Zero memory leaks detected (Instruments test)
- ✅ Memory stable over 30-minute session
- ✅ Asset loading optimized with screen references
- ✅ Memory monitor integrated
- ✅ All 6 memory tests passing
- ✅ Peak memory < 115MB (10-coin celebration scenario)
- ✅ Memory pressure handler working
- ✅ Character cache functioning (25MB limit)
- ✅ Animation pool functioning (10 animation limit)
- ✅ Audio streaming implemented per Playbook Part 5.3

## Next Stage Preview
**Stage 3: Asset Optimization**
- Will optimize actual asset files using specifications from Playbook Part 9
- Reduce app bundle size using asset catalog compression
- Improve load times with optimized resolutions
- Reference all design assets for optimization targets
