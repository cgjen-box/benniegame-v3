# Test Reporting & Logging

## Purpose

Comprehensive logging and reporting system for the recursive playthrough test to enable post-mortem analysis and debugging.

## Report Structure

### 1. Test Summary Report

```json
{
  "test_id": "playthrough_20260111_142530",
  "start_time": "2026-01-11T14:25:30Z",
  "end_time": "2026-01-11T14:58:42Z",
  "duration_seconds": 1992,
  "status": "SUCCESS",
  "coins_earned": 100,
  "youtube_minutes_watched": 100,
  "activities_completed": {
    "puzzle_matching": 28,
    "labyrinth": 22,
    "wuerfel": 24,
    "waehle_zahl": 26
  },
  "celebration_milestones_triggered": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100],
  "errors_encountered": 3,
  "errors_recovered": 3,
  "performance": {
    "average_memory_mb": 142.5,
    "peak_memory_mb": 187.2,
    "average_fps": 59.8,
    "lowest_fps": 56.1,
    "average_activity_duration_seconds": 14.2
  },
  "screenshots": [
    "screenshots/activity_failure_coin_47.png",
    "screenshots/recovery_successful_coin_47.png"
  ]
}
```

### 2. Detailed Activity Log

```swift
struct ActivityLogEntry: Codable {
    let timestamp: Date
    let activityType: String
    let subActivity: String
    let attemptNumber: Int
    let coinsBefore: Int
    let coinsAfter: Int
    let success: Bool
    let duration: TimeInterval
    let errorMessage: String?
    let memoryUsageMB: Float
    let fps: Float
}

class ActivityLogger {
    private var entries: [ActivityLogEntry] = []
    
    func logActivity(
        type: String,
        subActivity: String,
        attemptNumber: Int,
        coinsBefore: Int,
        coinsAfter: Int,
        success: Bool,
        duration: TimeInterval,
        error: String? = nil
    ) {
        let entry = ActivityLogEntry(
            timestamp: Date(),
            activityType: type,
            subActivity: subActivity,
            attemptNumber: attemptNumber,
            coinsBefore: coinsBefore,
            coinsAfter: coinsAfter,
            success: success,
            duration: duration,
            errorMessage: error,
            memoryUsageMB: PerformanceMonitor.currentMemoryUsage(),
            fps: PerformanceMonitor.currentFPS()
        )
        
        entries.append(entry)
        
        // Write to log file incrementally
        appendToLogFile(entry)
    }
    
    func generateReport() -> String {
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        encoder.outputFormatting = .prettyPrinted
        
        guard let data = try? encoder.encode(entries),
              let json = String(data: data, encoding: .utf8) else {
            return "Error generating report"
        }
        
        return json
    }
}
```

### 3. Performance Timeline

```swift
struct PerformanceSnapshot: Codable {
    let timestamp: Date
    let coinCount: Int
    let memoryUsageMB: Float
    let fps: Float
    let cpuUsagePercent: Float
    let batteryLevel: Float
}

class PerformanceMonitor {
    private var snapshots: [PerformanceSnapshot] = []
    private var timer: Timer?
    
    func startMonitoring() {
        timer = Timer.scheduledTimer(withTimeInterval: 5.0, repeats: true) { _ in
            self.captureSnapshot()
        }
    }
    
    func captureSnapshot() {
        let snapshot = PerformanceSnapshot(
            timestamp: Date(),
            coinCount: GameState.shared.coins,
            memoryUsageMB: Self.currentMemoryUsage(),
            fps: Self.currentFPS(),
            cpuUsagePercent: Self.currentCPUUsage(),
            batteryLevel: UIDevice.current.batteryLevel
        )
        
        snapshots.append(snapshot)
    }
    
    static func currentMemoryUsage() -> Float {
        var taskInfo = mach_task_basic_info()
        var count = mach_msg_type_number_t(MemoryLayout<mach_task_basic_info>.size)/4
        let kerr: kern_return_t = withUnsafeMutablePointer(to: &taskInfo) {
            $0.withMemoryRebound(to: integer_t.self, capacity: 1) {
                task_info(mach_task_self_, task_flavor_t(MACH_TASK_BASIC_INFO), $0, &count)
            }
        }
        
        if kerr == KERN_SUCCESS {
            return Float(taskInfo.resident_size) / 1_048_576.0 // Convert to MB
        }
        return 0
    }
    
    static func currentFPS() -> Float {
        // Use CADisplayLink to measure FPS
        return FPSCounter.shared.currentFPS
    }
    
    static func currentCPUUsage() -> Float {
        var threadsList: thread_act_array_t?
        var threadsCount = mach_msg_type_number_t(0)
        
        guard task_threads(mach_task_self_, &threadsList, &threadsCount) == KERN_SUCCESS,
              let threads = threadsList else {
            return 0
        }
        
        var totalCPU: Float = 0
        
        for i in 0..<Int(threadsCount) {
            var threadInfo = thread_basic_info()
            var threadInfoCount = mach_msg_type_number_t(THREAD_INFO_MAX)
            
            let kerr = withUnsafeMutablePointer(to: &threadInfo) {
                $0.withMemoryRebound(to: integer_t.self, capacity: 1) {
                    thread_info(threads[i], thread_flavor_t(THREAD_BASIC_INFO), $0, &threadInfoCount)
                }
            }
            
            if kerr == KERN_SUCCESS {
                totalCPU += Float(threadInfo.cpu_usage) / Float(TH_USAGE_SCALE) * 100.0
            }
        }
        
        vm_deallocate(mach_task_self_, vm_address_t(bitPattern: threads), vm_size_t(threadsCount))
        
        return totalCPU
    }
}
```

## Screenshot Management

```swift
class ScreenshotManager {
    private let screenshotDirectory = "test_results/screenshots/"
    private var screenshots: [Screenshot] = []
    
    struct Screenshot: Codable {
        let filename: String
        let timestamp: Date
        let coinCount: Int
        let screen: String
        let reason: String // "error", "milestone", "state_change"
    }
    
    func captureScreenshot(reason: String, screen: String) -> String {
        let screenshot = XCUIScreen.main.screenshot()
        let timestamp = DateFormatter.timestamp.string(from: Date())
        let coinCount = GameState.shared.coins
        
        let filename = "\(reason)_coin_\(coinCount)_\(timestamp).png"
        let filepath = screenshotDirectory + filename
        
        // Save screenshot
        let imageData = screenshot.pngRepresentation
        try? imageData.write(to: URL(fileURLWithPath: filepath))
        
        // Record metadata
        let meta = Screenshot(
            filename: filename,
            timestamp: Date(),
            coinCount: coinCount,
            screen: screen,
            reason: reason
        )
        screenshots.append(meta)
        
        return filepath
    }
    
    func captureOnError(errorType: String, errorMessage: String) {
        let filename = captureScreenshot(reason: "error_\(errorType)", screen: getCurrentScreen())
        print("📸 Error screenshot saved: \(filename)")
    }
    
    func captureOnMilestone(coins: Int) {
        let filename = captureScreenshot(reason: "milestone_\(coins)", screen: "celebration")
        print("📸 Milestone screenshot saved: \(filename)")
    }
}
```

## Console Log Capture

```swift
class ConsoleLogger {
    private var logBuffer: [String] = []
    private let maxBufferSize = 10000 // Keep last 10k lines
    
    func startCapturing() {
        // Redirect stdout and stderr to capture all console output
        let pipe = Pipe()
        dup2(pipe.fileHandleForWriting.fileDescriptor, STDOUT_FILENO)
        dup2(pipe.fileHandleForWriting.fileDescriptor, STDERR_FILENO)
        
        pipe.fileHandleForReading.readabilityHandler = { handle in
            let data = handle.availableData
            if let output = String(data: data, encoding: .utf8) {
                self.appendToLog(output)
            }
        }
    }
    
    func appendToLog(_ message: String) {
        let timestamp = DateFormatter.timestamp.string(from: Date())
        let logLine = "[\(timestamp)] \(message)"
        
        logBuffer.append(logLine)
        
        // Trim buffer if too large
        if logBuffer.count > maxBufferSize {
            logBuffer.removeFirst(logBuffer.count - maxBufferSize)
        }
    }
    
    func getFullLog() -> String {
        return logBuffer.joined(separator: "\n")
    }
    
    func saveToFile() -> String {
        let filename = "test_results/console_log_\(DateFormatter.timestamp.string(from: Date())).txt"
        let fullLog = getFullLog()
        try? fullLog.write(toFile: filename, atomically: true, encoding: .utf8)
        return filename
    }
}
```

## HTML Report Generation

```swift
class HTMLReportGenerator {
    func generate(testRun: TestRun) -> String {
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Bennie Test Report - \(testRun.testID)</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto; margin: 40px; }
                .header { background: #738F66; color: white; padding: 20px; border-radius: 10px; }
                .status-success { color: #99BF8C; font-weight: bold; }
                .status-failure { color: #C84848; font-weight: bold; }
                .section { margin: 30px 0; padding: 20px; background: #FAF5EB; border-radius: 10px; }
                .metric { display: inline-block; margin: 10px 20px 10px 0; }
                .metric-label { color: #8C7259; font-size: 12px; text-transform: uppercase; }
                .metric-value { font-size: 24px; font-weight: bold; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { text-align: left; padding: 10px; border-bottom: 1px solid #ddd; }
                th { background: #738F66; color: white; }
                .timeline { margin: 20px 0; }
                .timeline-item { padding: 10px; margin: 5px 0; border-left: 3px solid #6FA8DC; }
                .screenshot { max-width: 300px; margin: 10px; border: 2px solid #8C7259; }
                canvas { max-width: 100%; height: 300px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🐻 Bennie und die Lemminge - Test Report</h1>
                <p>Test ID: \(testRun.testID)</p>
                <p>Status: <span class="status-\(testRun.status.lowercased())">\(testRun.status)</span></p>
            </div>
            
            <div class="section">
                <h2>📊 Summary</h2>
                <div class="metric">
                    <div class="metric-label">Duration</div>
                    <div class="metric-value">\(formatDuration(testRun.durationSeconds))</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Coins Earned</div>
                    <div class="metric-value">\(testRun.coinsEarned) / 100</div>
                </div>
                <div class="metric">
                    <div class="metric-label">YouTube Minutes</div>
                    <div class="metric-value">\(testRun.youtubeMinutesWatched) min</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Errors</div>
                    <div class="metric-value">\(testRun.errorsEncountered)</div>
                </div>
            </div>
            
            <div class="section">
                <h2>🎮 Activities Completed</h2>
                <table>
                    <tr><th>Activity</th><th>Count</th><th>Avg Duration</th></tr>
                    \(generateActivityTable(testRun.activitiesCompleted))
                </table>
            </div>
            
            <div class="section">
                <h2>⚡ Performance</h2>
                <canvas id="performanceChart"></canvas>
                <div class="metric">
                    <div class="metric-label">Avg Memory</div>
                    <div class="metric-value">\(testRun.performance.averageMemoryMB) MB</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Peak Memory</div>
                    <div class="metric-value">\(testRun.performance.peakMemoryMB) MB</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Avg FPS</div>
                    <div class="metric-value">\(testRun.performance.averageFPS)</div>
                </div>
            </div>
            
            <div class="section">
                <h2>🎉 Celebration Milestones</h2>
                <p>\(testRun.celebrationMilestonesTriggered.map { String($0) }.joined(separator: ", ")) coins</p>
            </div>
            
            <div class="section">
                <h2>📸 Screenshots</h2>
                \(generateScreenshotGallery(testRun.screenshots))
            </div>
            
            <div class="section">
                <h2>📝 Activity Timeline</h2>
                <div class="timeline">
                    \(generateTimeline(testRun.activityLog))
                </div>
            </div>
            
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <script>
                // Performance chart
                const ctx = document.getElementById('performanceChart').getContext('2d');
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: \(generateChartLabels(testRun.performanceTimeline)),
                        datasets: [{
                            label: 'Memory (MB)',
                            data: \(generateMemoryData(testRun.performanceTimeline)),
                            borderColor: '#738F66',
                            yAxisID: 'y'
                        }, {
                            label: 'FPS',
                            data: \(generateFPSData(testRun.performanceTimeline)),
                            borderColor: '#6FA8DC',
                            yAxisID: 'y1'
                        }]
                    },
                    options: {
                        scales: {
                            y: { position: 'left', title: { display: true, text: 'Memory (MB)' }},
                            y1: { position: 'right', title: { display: true, text: 'FPS' }, grid: { drawOnChartArea: false }}
                        }
                    }
                });
            </script>
        </body>
        </html>
        """
    }
}
```

## Reporting Output Locations

```
test_results/
├── playthrough_20260111_142530/
│   ├── summary.json              # High-level summary
│   ├── activity_log.json         # Detailed activity entries
│   ├── performance_timeline.json # Performance snapshots
│   ├── console_log.txt           # Full console output
│   ├── report.html               # Human-readable HTML report
│   └── screenshots/
│       ├── milestone_5_142532.png
│       ├── milestone_10_142545.png
│       ├── error_freeze_142612.png
│       └── recovery_successful_142615.png
```

## Success Criteria

Reporting system is effective if:
- ✅ All test events are logged with timestamps
- ✅ Performance data captured every 5 seconds
- ✅ Screenshots automatically captured on errors and milestones
- ✅ HTML report generated within 10 seconds of test completion
- ✅ Console log captures all print statements
- ✅ Activity log includes all completion attempts
- ✅ Report is readable and actionable for debugging

## Integration

```swift
class TestOrchestrator {
    let activityLogger = ActivityLogger()
    let performanceMonitor = PerformanceMonitor()
    let screenshotManager = ScreenshotManager()
    let consoleLogger = ConsoleLogger()
    
    func runTest() {
        // Start all monitoring
        consoleLogger.startCapturing()
        performanceMonitor.startMonitoring()
        
        let startTime = Date()
        
        // Run test phases...
        
        // Generate report
        let testRun = TestRun(
            testID: "playthrough_\(DateFormatter.timestamp.string(from: startTime))",
            startTime: startTime,
            endTime: Date(),
            status: testPassed ? "SUCCESS" : "FAILURE",
            // ... all other data
        )
        
        let htmlReport = HTMLReportGenerator().generate(testRun: testRun)
        try? htmlReport.write(toFile: "test_results/report.html", atomically: true, encoding: .utf8)
        
        print("📊 Test report generated: test_results/report.html")
    }
}
```
