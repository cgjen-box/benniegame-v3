# Stage 4: Animation Performance

## Purpose
Ensure 60fps constant frame rate during all animations.

## Duration
1 day

## Playbook References
- **Part 5.6**: Performance Requirements (60fps target)
- **Part 6.1**: Animation Principles
- **Part 6.2**: Transition Animations

## Animation Performance Targets

| Animation | Target FPS | Max Duration | Critical |
|-----------|------------|--------------|----------|
| Character breathing | 60 | Continuous | YES |
| Screen transitions | 60 | 0.3s | YES |
| Confetti effect | 60 | 3s | YES |
| Coin fly | 60 | 0.8s | YES |
| Grid color fill | 60 | Instant | YES |
| Button press | 60 | 0.1s | YES |

## Optimization Strategies

### 1. Use Metal for Particle Effects
```swift
// Replace UIKit confetti with Metal particle system
// Benefits: GPU acceleration, better performance
import MetalKit

class MetalConfettiRenderer: MTKView {
    // Render confetti particles on GPU
    // Target: 200 particles @ 60fps
}
```

### 2. Optimize Lottie Rendering
```swift
// Use low-quality rendering for subtle animations
let animationView = LottieAnimationView(name: "bennie_idle")
animationView.contentMode = .scaleAspectFit
animationView.loopMode = .loop
animationView.animationSpeed = 1.0

// Reduce rendering complexity:
animationView.shouldRasterizeWhenIdle = true
animationView.maxSize = CGSize(width: 300, height: 450) // Exact display size
```

### 3. Offscreen Rendering
```swift
// Pre-render complex animations offscreen
class AnimationCache {
    func prerenderAnimation(_ name: String) async -> UIImage? {
        // Render animation to image sequence
        // Cache frames for playback
        // Use for critical path animations
    }
}
```

### 4. Animation Scheduling
```swift
// Don't run multiple heavy animations simultaneously
class AnimationScheduler {
    private var activeAnimations: Set<String> = []
    
    func schedule(animation: String, priority: Priority) {
        // Wait for high-priority animations to complete
        // Stagger lower-priority animations
    }
}
```

## Testing Protocol

### Frame Rate Monitoring
```swift
class FrameRateMonitor {
    private var displayLink: CADisplayLink?
    private var frameCount = 0
    private var lastTimestamp: CFTimeInterval = 0
    
    func startMonitoring() {
        displayLink = CADisplayLink(target: self, selector: #selector(displayLinkFired))
        displayLink?.add(to: .main, forMode: .common)
    }
    
    @objc private func displayLinkFired(_ link: CADisplayLink) {
        frameCount += 1
        let elapsed = link.timestamp - lastTimestamp
        
        if elapsed >= 1.0 {
            let fps = Double(frameCount) / elapsed
            if fps < 55 { // Allow 5fps tolerance
                print("⚠️ LOW FPS: \(fps) on \(currentScreen)")
            }
            frameCount = 0
            lastTimestamp = link.timestamp
        }
    }
}
```

### Animation Test Suite
```
Test each animation:
☐ bennie_idle - 60fps sustained
☐ bennie_celebrating - 60fps during jump
☐ lemminge_idle - 60fps sustained
☐ confetti - 60fps with 200 particles
☐ coin_fly - 60fps during arc
☐ screen_transition - 60fps during fade
☐ grid_fill - 60fps during color change
```

## Deliverables

1. **Optimized Animation System**
   - Metal-based particle effects
   - Optimized Lottie rendering
   - Animation scheduling

2. **Frame Rate Monitor**
   - Real-time FPS tracking
   - Automatic warnings
   - Performance logging

3. **Animation Performance Report**
   - FPS measurements per animation
   - Optimization results
   - Remaining issues

## Success Criteria
- ✅ 60fps constant on all screens
- ✅ No frame drops during celebrations
- ✅ Smooth transitions
- ✅ Monitoring integrated

## Next Stage
**Stage 5: Load Time Optimization** - Achieve < 2s cold start

---

# Stage 5: Load Time Optimization

## Purpose
Achieve < 2s cold start and < 0.3s screen transitions.

## Duration
2 days

## Playbook References
- **Part 5.6**: Performance Requirements

## Load Time Targets

| Event | Current | Target | Critical |
|-------|---------|--------|----------|
| Cold start | ___ms | 2000ms | YES |
| Loading screen | ___ms | 2000-3000ms | NO (UX) |
| Screen transition | ___ms | 300ms | YES |
| Asset load | ___ms | 100ms | YES |

## Optimization Strategies

### 1. App Launch Optimization
```swift
// Defer non-critical initialization
class AppDelegate {
    func application(_ application: UIApplication, 
                    didFinishLaunchingWithOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        
        // CRITICAL PATH (< 2s):
        setupCoreServices()
        loadEssentialAssets() // Only Loading screen assets
        
        // DEFERRED (background):
        DispatchQueue.global(qos: .utility).async {
            self.setupAnalytics()
            self.loadAdditionalAssets()
            self.initializeGameState()
        }
        
        return true
    }
}
```

### 2. Parallel Asset Loading
```swift
// Load assets concurrently
class AssetLoader {
    func loadInitialAssets() async {
        await withTaskGroup(of: Void.self) { group in
            group.addTask { await self.loadImages() }
            group.addTask { await self.loadAnimations() }
            group.addTask { await self.loadAudio() }
        }
    }
}
```

### 3. Transition Optimization
```swift
// Use GPU-accelerated transitions
extension View {
    func optimizedTransition() -> some View {
        self.transition(.asymmetric(
            insertion: .opacity.animation(.easeIn(duration: 0.15)),
            removal: .opacity.animation(.easeOut(duration: 0.15))
        ))
    }
}
```

### 4. Screen Preloading
```swift
// Preload next screen while current screen is active
class ScreenPreloader {
    func preloadNextScreen(from current: Screen) {
        let nextLikely = predictNextScreen(from: current)
        Task {
            await loadAssets(for: nextLikely)
            await prepareView(for: nextLikely)
        }
    }
}
```

## Deliverables
1. Optimized launch sequence
2. Parallel loading system
3. Screen preloader
4. Load time report

## Success Criteria
- ✅ Cold start < 2s
- ✅ Transitions < 0.3s
- ✅ No visible delays

---

# Stage 6: Touch Response Optimization

## Purpose
Achieve < 100ms touch latency for instant feedback.

## Duration
1 day

## Playbook References
- **Part 5.6**: Performance Requirements (< 100ms target)
- **Part 4**: Screen Specifications (touch targets ≥ 96pt)

## Touch Response Targets

| Element | Current | Target | Notes |
|---------|---------|--------|-------|
| Button tap | ___ms | 100ms | Visual feedback |
| Grid cell tap | ___ms | 100ms | Color fill |
| Number trace | ___ms | 100ms | Path drawing |
| Screen transition | ___ms | 100ms | Navigation |

## Optimization Strategies

### 1. Immediate Visual Feedback
```swift
struct ResponsiveButton: View {
    @State private var isPressed = false
    
    var body: some View {
        Button(action: action) {
            content
        }
        .buttonStyle(InstantFeedbackStyle())
    }
}

struct InstantFeedbackStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
            .animation(.easeOut(duration: 0.05), value: configuration.isPressed)
    }
}
```

### 2. Touch Prediction
```swift
// Pre-warm touch targets
class TouchPredictor {
    func predictNextTap(from current: CGPoint) -> [CGPoint] {
        // Analyze user patterns
        // Pre-load nearby targets
    }
}
```

### 3. Haptic Feedback
```swift
// Add haptic for instant response
class HapticManager {
    private let impact = UIImpactFeedbackGenerator(style: .light)
    
    func prepareForTouch() {
        impact.prepare() // Pre-warm engine
    }
    
    func provideFeedback() {
        impact.impactOccurred() // < 10ms
    }
}
```

## Success Criteria
- ✅ Visual feedback < 50ms
- ✅ Action complete < 100ms
- ✅ No delayed responses

---

# Stage 7: Network Optimization

## Purpose
Optimize YouTube integration for smooth video playback.

## Duration
1 day

## Optimization Strategies

### 1. Video Thumbnail Caching
```swift
class ThumbnailCache {
    private let cache = NSCache<NSString, UIImage>()
    
    func cacheThumbnail(_ image: UIImage, for videoID: String) {
        cache.setObject(image, forKey: videoID as NSString)
    }
}
```

### 2. Preload Next Video
```swift
// Preload video while watching current
class VideoPreloader {
    func preloadNext(after current: String, from list: [ApprovedVideo]) {
        guard let nextIndex = list.firstIndex(where: { $0.id == current }),
              nextIndex + 1 < list.count else { return }
        
        let next = list[nextIndex + 1]
        // Preload thumbnail and metadata
    }
}
```

### 3. Offline Graceful Degradation
```swift
class NetworkMonitor {
    func showOfflineMessage() {
        // Disable YouTube buttons
        // Show friendly message
        // Suggest activities instead
    }
}
```

## Success Criteria
- ✅ Video loads < 3s
- ✅ Thumbnails cached
- ✅ Offline handling graceful

---

# Stage 8: Performance Testing & Monitoring

## Purpose
Continuous performance monitoring and regression prevention.

## Duration
Ongoing

## Automated Performance Tests

### Test Suite
```swift
class PerformanceTestSuite: XCTestCase {
    func testColdStartTime() {
        measure {
            // Launch app
            // Measure time to LoadingView
        }
        // Assert: < 2000ms
    }
    
    func testScreenTransition() {
        measure {
            // Navigate between screens
            // Measure transition time
        }
        // Assert: < 300ms
    }
    
    func testMemoryUsage() {
        // Run complete user journey
        // Assert: < 200MB peak
    }
    
    func testFrameRate() {
        // Play all animations
        // Assert: 60fps ±5
    }
}
```

### CI/CD Integration
```yaml
# .github/workflows/performance.yml
name: Performance Tests
on: [push, pull_request]

jobs:
  performance:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run performance tests
        run: xcodebuild test -scheme Bennie -destination 'platform=iOS Simulator,name=iPad (10th generation)'
      - name: Check benchmarks
        run: ./scripts/check_performance_benchmarks.sh
```

## Performance Dashboard

**File**: `14_performance/dashboard.md`

```markdown
# Performance Dashboard

## Current Status (Updated: DATE)

### ✅ Passing
- Cold start: 1.8s (target: 2.0s)
- Memory peak: 185MB (target: 200MB)
- Frame rate: 60fps (target: 60fps)

### ⚠️ Monitoring
- Screen transitions: 0.28s (target: 0.30s)
- Touch response: 95ms (target: 100ms)

### ❌ Issues
- None

## Historical Trends
[Chart: Cold start time over last 30 days]
[Chart: Memory usage over last 30 days]
[Chart: Frame rate stability]
```

## Success Criteria
- ✅ All automated tests passing
- ✅ Dashboard updated
- ✅ No regressions detected
- ✅ Monitoring active in production
