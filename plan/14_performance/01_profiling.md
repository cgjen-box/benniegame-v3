# Stage 1: Profiling & Baseline

## Purpose
Establish comprehensive performance baseline before optimization work begins. Measure current performance against playbook targets to identify optimization priorities.

## Duration
1 day

## Playbook References
- **[Part 5.6]** Performance Requirements (all targets defined)
- **[Part 6.1]** Animation Principles (frame rate targets for animations)
- **[Part 6.2]** Transition Animations (timing requirements)
- **[Part 10.3]** QA Verification Matrix (testing methodology)

## Design References

### Screen References for Testing
All screens must be profiled according to their reference designs:

| Screen | Reference File | Performance Focus |
|--------|---------------|-------------------|
| Loading | `design/references/screens/Reference_Loading_Screen.png` | Cold start, asset loading |
| Player Selection | `design/references/screens/Reference_Player_Selection_Screen.png` | Touch response |
| Home | `design/references/screens/Reference_Menu_Screen.png` | Multiple animations (6 Lemminge + Bennie) |
| Puzzle Matching | `design/references/screens/Reference_Matching_Game_Screen.png` | Grid rendering (3×3 to 6×6) |
| Labyrinth | `design/references/screens/Reference_Layrinth_Game_Screen.png` | Path tracking latency |
| Numbers | `design/references/screens/Reference_Numbers_Game_Screen.png` | Touch targets |
| Celebration | `design/references/screens/Reference_Celebration_Overlay.png` | CRITICAL: Confetti + animations |
| Treasure | `design/references/screens/Reference_Treasure_Screen.png` | Chest animation |

### Character References for Animation Testing
- **Bennie**: `design/references/character/bennie/states/` - Test all 6 animation states
- **Lemminge**: `design/references/character/lemminge/states/` - Test multiple instances (3-6)

## Profiling Tools Setup

### 1. Xcode Instruments Configuration

```bash
# Essential instruments to configure:
1. Time Profiler - CPU usage analysis per method
2. Allocations - Memory allocation tracking
3. Leaks - Memory leak detection
4. System Trace - Overall system impact
5. Core Animation - Frame rate and rendering analysis
6. Metal System Trace - GPU performance for animations
```

**Launch Configuration**:
```
Product → Profile (⌘I)
Select: Time Profiler, Allocations, Leaks, Core Animation
Recording Duration: 5 minutes per screen
Device: iPad (10th generation) - primary target device
```

### 2. Custom Performance Monitor

**File**: `Sources/Services/BenniePerformanceMonitor.swift`

```swift
import SwiftUI
import Combine

/// Comprehensive performance monitoring for all screens
/// Reference: Playbook Part 5.6 - Performance Requirements
class BenniePerformanceMonitor: ObservableObject {
    static let shared = BenniePerformanceMonitor()
    
    // MARK: - Performance Metrics (Playbook Part 5.6)
    
    @Published var currentFPS: Double = 60.0
    @Published var memoryUsageMB: Double = 0.0
    @Published var lastTouchLatencyMS: Double = 0.0
    @Published var lastTransitionDurationMS: Double = 0.0
    
    private var displayLink: CADisplayLink?
    private var lastTimestamp: CFTimeInterval = 0
    private var frameCount: Int = 0
    
    // MARK: - Targets from Playbook
    
    enum PerformanceTarget {
        static let targetFPS: Double = 60.0            // Part 5.6
        static let maxMemoryMB: Double = 200.0         // Part 5.6
        static let maxTouchLatencyMS: Double = 100.0   // Part 5.6 (CRITICAL)
        static let maxTransitionMS: Double = 300.0     // Part 5.6
    }
    
    // MARK: - Screen-Specific Metrics
    
    struct ScreenMetrics {
        let screenName: String
        let avgFPS: Double
        let peakMemoryMB: Double
        let avgTouchLatencyMS: Double
        let transitionDurationMS: Double
        let timestamp: Date
        
        var meetsTargets: Bool {
            avgFPS >= PerformanceTarget.targetFPS - 5.0 &&  // Allow 5fps variance
            peakMemoryMB <= PerformanceTarget.maxMemoryMB &&
            avgTouchLatencyMS <= PerformanceTarget.maxTouchLatencyMS &&
            transitionDurationMS <= PerformanceTarget.maxTransitionMS
        }
    }
    
    private var screenMetrics: [String: ScreenMetrics] = [:]
    
    // MARK: - Monitoring Control
    
    func startMonitoring() {
        displayLink = CADisplayLink(target: self, selector: #selector(updateFPS))
        displayLink?.add(to: .main, forMode: .common)
        startMemoryMonitoring()
    }
    
    func stopMonitoring() {
        displayLink?.invalidate()
        displayLink = nil
    }
    
    @objc private func updateFPS(displayLink: CADisplayLink) {
        if lastTimestamp == 0 {
            lastTimestamp = displayLink.timestamp
            return
        }
        
        frameCount += 1
        let elapsed = displayLink.timestamp - lastTimestamp
        
        if elapsed >= 1.0 {
            DispatchQueue.main.async {
                self.currentFPS = Double(self.frameCount) / elapsed
                self.logPerformanceWarning()
            }
            
            frameCount = 0
            lastTimestamp = displayLink.timestamp
        }
    }
    
    private func startMemoryMonitoring() {
        Timer.scheduledTimer(withTimeInterval: 0.5, repeats: true) { _ in
            self.memoryUsageMB = self.getMemoryUsage()
        }
    }
    
    private func getMemoryUsage() -> Double {
        var info = mach_task_basic_info()
        var count = mach_msg_type_number_t(MemoryLayout<mach_task_basic_info>.size)/4
        
        let kerr: kern_return_t = withUnsafeMutablePointer(to: &info) {
            $0.withMemoryRebound(to: integer_t.self, capacity: 1) {
                task_info(mach_task_self_, task_flavor_t(MACH_TASK_BASIC_INFO), $0, &count)
            }
        }
        
        if kerr == KERN_SUCCESS {
            return Double(info.resident_size) / 1024.0 / 1024.0
        }
        return 0
    }
    
    // MARK: - Touch Latency Tracking
    
    private var touchStartTime: Date?
    
    func touchBegan() {
        touchStartTime = Date()
    }
    
    func touchResponseReceived() {
        guard let startTime = touchStartTime else { return }
        let latency = Date().timeIntervalSince(startTime) * 1000.0 // Convert to ms
        
        DispatchQueue.main.async {
            self.lastTouchLatencyMS = latency
            self.logTouchLatency(latency)
        }
    }
    
    // MARK: - Transition Tracking
    
    private var transitionStartTime: Date?
    
    func transitionBegan(from: String, to: String) {
        transitionStartTime = Date()
        print("📊 Transition: \(from) → \(to)")
    }
    
    func transitionCompleted(screenName: String) {
        guard let startTime = transitionStartTime else { return }
        let duration = Date().timeIntervalSince(startTime) * 1000.0 // Convert to ms
        
        DispatchQueue.main.async {
            self.lastTransitionDurationMS = duration
            self.logTransitionDuration(duration, screen: screenName)
        }
    }
    
    // MARK: - Screen Metrics Recording
    
    func recordScreenMetrics(
        screenName: String,
        avgFPS: Double,
        peakMemoryMB: Double,
        avgTouchLatencyMS: Double,
        transitionDurationMS: Double
    ) {
        let metrics = ScreenMetrics(
            screenName: screenName,
            avgFPS: avgFPS,
            peakMemoryMB: peakMemoryMB,
            avgTouchLatencyMS: avgTouchLatencyMS,
            transitionDurationMS: transitionDurationMS,
            timestamp: Date()
        )
        
        screenMetrics[screenName] = metrics
        
        print("""
        
        📊 SCREEN METRICS: \(screenName)
        ════════════════════════════════════════
        FPS:        \(String(format: "%.1f", avgFPS)) / 60.0 \(avgFPS >= 55.0 ? "✅" : "❌")
        Memory:     \(String(format: "%.1f", peakMemoryMB))MB / 200MB \(peakMemoryMB <= 200.0 ? "✅" : "❌")
        Touch:      \(String(format: "%.1f", avgTouchLatencyMS))ms / 100ms \(avgTouchLatencyMS <= 100.0 ? "✅" : "❌")
        Transition: \(String(format: "%.1f", transitionDurationMS))ms / 300ms \(transitionDurationMS <= 300.0 ? "✅" : "❌")
        ════════════════════════════════════════
        OVERALL: \(metrics.meetsTargets ? "✅ PASS" : "❌ NEEDS OPTIMIZATION")
        
        """)
    }
    
    // MARK: - Performance Warnings
    
    private func logPerformanceWarning() {
        if currentFPS < PerformanceTarget.targetFPS - 5.0 {
            print("⚠️ LOW FPS: \(String(format: "%.1f", currentFPS)) (Target: 60.0)")
        }
        
        if memoryUsageMB > PerformanceTarget.maxMemoryMB {
            print("⚠️ HIGH MEMORY: \(String(format: "%.1f", memoryUsageMB))MB (Target: <200MB)")
        }
    }
    
    private func logTouchLatency(_ latency: Double) {
        if latency > PerformanceTarget.maxTouchLatencyMS {
            print("⚠️ HIGH TOUCH LATENCY: \(String(format: "%.1f", latency))ms (Target: <100ms)")
        }
    }
    
    private func logTransitionDuration(_ duration: Double, screen: String) {
        if duration > PerformanceTarget.maxTransitionMS {
            print("⚠️ SLOW TRANSITION to \(screen): \(String(format: "%.1f", duration))ms (Target: <300ms)")
        }
    }
    
    // MARK: - Report Generation
    
    func generateBaselineReport() -> String {
        var report = """
        ╔══════════════════════════════════════════════════════════════╗
        ║          BENNIE PERFORMANCE BASELINE REPORT                   ║
        ║          Reference: Playbook Part 5.6                         ║
        ╚══════════════════════════════════════════════════════════════╝
        
        Generated: \(Date())
        Device: iPad (10th generation)
        
        """
        
        for (screenName, metrics) in screenMetrics.sorted(by: { $0.key < $1.key }) {
            report += """
            
            [\(screenName)]
            FPS:        \(String(format: "%.1f", metrics.avgFPS)) / 60.0 \(metrics.avgFPS >= 55.0 ? "✅" : "❌")
            Memory:     \(String(format: "%.1f", metrics.peakMemoryMB))MB / 200MB \(metrics.peakMemoryMB <= 200.0 ? "✅" : "❌")
            Touch:      \(String(format: "%.1f", metrics.avgTouchLatencyMS))ms / 100ms \(metrics.avgTouchLatencyMS <= 100.0 ? "✅" : "❌")
            Transition: \(String(format: "%.1f", metrics.transitionDurationMS))ms / 300ms \(metrics.transitionDurationMS <= 300.0 ? "✅" : "❌")
            Status:     \(metrics.meetsTargets ? "✅ PASS" : "❌ NEEDS OPTIMIZATION")
            
            """
        }
        
        return report
    }
}
```

## Baseline Measurements

### Test Scenario Matrix

Reference: **Playbook Part 10.3** - QA Verification Matrix

| Screen | Test Actions | Metrics to Capture | Reference Design |
|--------|--------------|-------------------|------------------|
| **Loading** | Cold start, wait for 100% | Launch time, memory, FPS | `Reference_Loading_Screen.png` |
| **Player Select** | Tap Alexander, tap Oliver | Touch latency, transition | `Reference_Player_Selection_Screen.png` |
| **Home** | Idle 10s, tap each activity | FPS with 6 Lemminge, memory | `Reference_Menu_Screen.png` |
| **Puzzle 3×3** | Complete 5 levels | FPS, memory, touch response | `Reference_Matching_Game_Screen.png` |
| **Puzzle 6×6** | Complete 3 levels | FPS under load, memory peak | `Reference_Matching_Game_Screen.png` |
| **Labyrinth** | Complete 5 paths | Touch tracking latency | `Reference_Layrinth_Game_Screen.png` |
| **Numbers** | Complete 10 numbers | Touch response, FPS | `Reference_Numbers_Game_Screen.png` |
| **Celebration 5** | Trigger at 5 coins | Memory spike, FPS during confetti | `Reference_Celebration_Overlay.png` |
| **Celebration 10** | Trigger at 10 coins | Peak memory, animation performance | `Reference_Celebration_Overlay.png` |
| **Treasure** | Open chest, view buttons | Chest animation FPS, memory | `Reference_Treasure_Screen.png` |
| **Video Player** | Play 5min video | Memory stability, FPS | N/A (YouTube embed) |

### Measurement Protocols

#### 1. Cold Start Performance (Playbook Part 5.6: Target < 2s)

```
TEST: APP_LAUNCH_COLD_START
REFERENCE: Playbook Part 5.6
DESIGN: design/references/screens/Reference_Loading_Screen.png

STEPS:
1. Force quit app (double-tap home, swipe up)
2. Clear memory (restart device if needed)
3. Start timer
4. Launch app from home screen
5. Stop timer when LoadingView appears

MEASUREMENTS:
- Time to LoadingView appears: _____ s
- Time to progress bar starts: _____ s
- Memory at launch: _____ MB
- Initial FPS: _____ fps

TARGET: < 2.0s to LoadingView
STATUS: [  ] PASS   [  ] FAIL
NOTES: _________________________________
```

#### 2. Screen Transition Performance (Playbook Part 5.6: Target < 0.3s)

```
TEST: SCREEN_TRANSITION_TIMING
REFERENCE: Playbook Part 5.6, Part 6.2

For each transition:
- PlayerSelection → Home
- Home → Activity Selection
- Activity → Game Screen
- Game Screen → Celebration
- Celebration → Next Level

STEPS:
1. Navigate to source screen
2. BenniePerformanceMonitor.transitionBegan()
3. Tap transition element
4. BenniePerformanceMonitor.transitionCompleted()
5. Record duration

MEASUREMENTS:
Transition: _____________ → _____________
- Tap to transition start: _____ ms
- Transition complete: _____ ms
- Total duration: _____ ms
- FPS during transition: _____ fps
- Memory change: _____ MB

TARGET: < 300ms total
STATUS: [  ] PASS   [  ] FAIL
```

#### 3. Touch Response Performance (Playbook Part 5.6: Target < 100ms CRITICAL)

```
TEST: TOUCH_RESPONSE_LATENCY
REFERENCE: Playbook Part 5.6 (CRITICAL requirement)

For each interactive element:
- Activity buttons
- Grid cells
- Number buttons
- Path start
- Player selection buttons

STEPS:
1. BenniePerformanceMonitor.touchBegan()
2. Tap element
3. BenniePerformanceMonitor.touchResponseReceived() when visual feedback appears
4. Record latency

MEASUREMENTS:
Element: _____________
- Touch to visual feedback: _____ ms
- Touch to action start: _____ ms
- FPS during response: _____ fps

TARGET: < 100ms (CRITICAL)
STATUS: [  ] PASS   [  ] FAIL
NOTES: _________________________________
```

#### 4. Frame Rate During Animations (Playbook Part 6.1: Target 60fps constant)

```
TEST: ANIMATION_FRAME_RATE
REFERENCE: Playbook Part 6.1, Part 6.2, Part 6.3
DESIGN: Character animation states in design/references/character/

Animations to test:
- bennie_idle (Loading, Home)
- bennie_celebrating (Celebration)
- lemminge_idle (Home - 6 instances)
- lemminge_celebrating (Celebration - 3 instances)
- confetti (Celebration)
- coin_fly (After level complete)
- grid_fill (Puzzle completion)

STEPS:
1. Navigate to screen with animation
2. Monitor FPS for 10 seconds
3. Record min, avg, max FPS
4. Note any frame drops

MEASUREMENTS:
Animation: _____________
Screen: _____________
- Min FPS: _____ fps
- Avg FPS: _____ fps
- Max FPS: _____ fps
- Frame drops: _____ count
- Duration: _____ s

TARGET: 60fps constant (no drops)
STATUS: [  ] PASS   [  ] FAIL
```

#### 5. Memory Usage Tracking (Playbook Part 5.6: Target < 200MB peak)

```
TEST: MEMORY_USAGE_PROFILE
REFERENCE: Playbook Part 5.6

STEPS:
1. Launch app
2. Navigate through all screens in order
3. Trigger celebration at 5, 10, 15, 20 coins
4. Play video for 5 minutes
5. Monitor peak memory throughout

MEASUREMENTS:
Screen: _____________
- Memory on enter: _____ MB
- Memory peak: _____ MB
- Memory on exit: _____ MB
- Memory leaked: _____ MB (if any)

CRITICAL SCREENS:
- Celebration Overlay peak: _____ MB (TARGET: < 200MB)
- Video Player peak: _____ MB (TARGET: < 200MB)
- Home with 6 Lemminge: _____ MB

TARGET: < 200MB peak
STATUS: [  ] PASS   [  ] FAIL
```

#### 6. Celebration Overlay Performance (CRITICAL TEST)

```
TEST: CELEBRATION_OVERLAY_CRITICAL
REFERENCE: Playbook Part 4.7, Part 6.2
DESIGN: design/references/screens/Reference_Celebration_Overlay.png

This is the MOST DEMANDING screen - confetti + 4 character animations

STEPS:
1. Play until earning 5 coins
2. Trigger celebration
3. Monitor for 5 seconds
4. Record all metrics

MEASUREMENTS:
- FPS during confetti: _____ fps
- Memory peak: _____ MB
- Animation smoothness: [  ] Smooth  [  ] Jerky
- Character animations fps: _____ fps
- Overlay transparency rendering: [  ] Smooth  [  ] Laggy

TARGETS:
- FPS: 60fps constant
- Memory: < 200MB
- Smooth animations (no stuttering)

STATUS: [  ] PASS   [  ] FAIL
PRIORITY: HIGH - This screen is most likely to fail
```

## Baseline Recording Template

### Dashboard Creation

Create `baseline_dashboard.md` with results:

```markdown
# Performance Baseline Dashboard

Generated: [DATE]
Device: iPad (10th generation)
iPadOS: 17.x

## Summary

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Cold Start | < 2s | ____ s | [PASS/FAIL] |
| Avg FPS | 60fps | ____ fps | [PASS/FAIL] |
| Peak Memory | < 200MB | ____ MB | [PASS/FAIL] |
| Touch Latency | < 100ms | ____ ms | [PASS/FAIL] |
| Transitions | < 0.3s | ____ ms | [PASS/FAIL] |

## Screen-by-Screen Results

[Use BenniePerformanceMonitor.generateBaselineReport()]

## Priority Optimization Areas

Based on baseline, identify:
1. [Screen/Feature] - [Issue] - [Priority: HIGH/MEDIUM/LOW]
2. ...

## Next Steps

Proceed to Stage 2: Memory Optimization for areas exceeding targets.
```

## Deliverables

### 1. Baseline Report
**File**: `baseline_report.md`
- Complete metrics for all screens
- Comparison against playbook targets
- Visual pass/fail indicators

### 2. Performance Dashboard
**File**: `baseline_dashboard.md`
- Quick summary view
- Trend charts (if multiple runs)
- Priority areas highlighted

### 3. Optimization Priorities
**File**: `optimization_priorities.md`
- Ranked list of issues
- Estimated impact of fixes
- Recommended stage assignments

## Success Criteria

- ✅ All screens profiled with Xcode Instruments
- ✅ BenniePerformanceMonitor integrated and logging
- ✅ Baseline measurements recorded for all test scenarios
- ✅ Comparison against playbook targets documented
- ✅ Optimization priorities identified
- ✅ Celebration Overlay (CRITICAL) tested and documented

---

**Next Stage**: [02_memory_optimization.md](02_memory_optimization.md)
