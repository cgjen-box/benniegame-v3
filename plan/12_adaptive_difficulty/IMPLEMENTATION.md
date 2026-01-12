# Implementation Guide

## Overview

SwiftUI integration for the adaptive difficulty system with complete code examples.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Activity Screen                             │
│  (PuzzleMatchingView, LabyrinthView, WuerfelView, etc.)         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────┐
        │    ActivityViewModel               │
        │  - currentMetrics: ActivityMetrics │
        │  - recordMistake()                 │
        │  - recordHint()                    │
        │  - completeLevel()                 │
        └────────────┬───────────────────────┘
                     │
                     ▼
       ┌──────────────────────────────────┐
       │   DifficultyManager               │
       │ - adjustDifficulty()              │
       │ - getNextLevelParams()            │
       │ - shouldTriggerHint()             │
       └────────────┬─────────────────────┘
                    │
                    ▼
        ┌───────────────────────────────┐
        │   PlayerDataStore             │
        │ - learningProfile: LearningProfile │
        │ - saveLearningProfile()       │
        └───────────────────────────────┘
```

## Core Components

### 1. DifficultyManager (Singleton)

```swift
import Foundation

class DifficultyManager: ObservableObject {
    static let shared = DifficultyManager()
    
    @Published var currentProfile: LearningProfile
    
    private init() {
        // Load from PlayerDataStore
        self.currentProfile = PlayerDataStore.shared.currentPlayer?.learningProfile ?? LearningProfile()
    }
    
    // MARK: - Difficulty Adjustment
    
    func adjustDifficulty(based on metrics: ActivityMetrics) {
        var adjustment: Float = 0.0
        
        // Solve time analysis
        if metrics.duration < 10 {
            adjustment += 0.1
        } else if metrics.duration > 60 {
            adjustment -= 0.1
        }
        
        // Mistake analysis
        if metrics.mistakes == 0 || metrics.mistakes == 1 {
            adjustment += 0.05
        } else if metrics.mistakes >= 3 {
            adjustment -= 0.15
        }
        
        // Long pause penalty
        if metrics.longPauses > 0 {
            adjustment -= 0.05 * Float(metrics.longPauses)
        }
        
        // Apply adjustment
        currentProfile.difficultyLevel = clamp(
            currentProfile.difficultyLevel + adjustment,
            min: 0.1,
            max: 0.9
        )
        
        // Update profile
        currentProfile.update(with: metrics)
        
        // Save to storage
        saveProfile()
    }
    
    // MARK: - Activity Configuration
    
    func getPuzzleConfig() -> PuzzleMatchingConfig {
        return PuzzleMatchingConfig.config(for: currentProfile.difficultyLevel)
    }
    
    func getLabyrinthConfig() -> LabyrinthConfig {
        return LabyrinthConfig.config(for: currentProfile.difficultyLevel)
    }
    
    func getWuerfelConfig() -> WuerfelConfig {
        return WuerfelConfig.config(for: currentProfile.difficultyLevel)
    }
    
    func getWaehleZahlConfig() -> WaehleZahlConfig {
        return WaehleZahlConfig.config(for: currentProfile.difficultyLevel)
    }
    
    // MARK: - Hint System
    
    func shouldTriggerHint(
        inactivityDuration: TimeInterval,
        currentMistakes: Int
    ) -> HintLevel {
        // Long inactivity
        if inactivityDuration > 30 {
            return .verySpecific
        } else if inactivityDuration > 20 {
            return .specific
        } else if inactivityDuration > 10 {
            return .gentle
        }
        
        // Multiple mistakes
        if currentMistakes >= 3 {
            return .specific
        }
        
        // Struggling pattern
        if currentProfile.mistakeFrequency > 1.5 {
            return .gentle
        }
        
        return .none
    }
    
    // MARK: - Persistence
    
    private func saveProfile() {
        PlayerDataStore.shared.updateLearningProfile(currentProfile)
    }
    
    private func clamp(_ value: Float, min: Float, max: Float) -> Float {
        return Swift.max(min, Swift.min(max, value))
    }
}

enum HintLevel {
    case none
    case gentle
    case specific
    case verySpecific
}
```

### 2. ActivityViewModel (Base Class)

```swift
import SwiftUI
import Combine

class ActivityViewModel: ObservableObject {
    @Published var currentMetrics: ActivityMetrics
    @Published var hintLevel: HintLevel = .none
    
    private var inactivityTimer: Timer?
    private var lastInteractionTime = Date()
    
    let difficultyManager = DifficultyManager.shared
    
    init(activityType: ActivityType) {
        let config = difficultyManager.getConfig(for: activityType)
        self.currentMetrics = ActivityMetrics(
            activityType: activityType,
            startTime: Date(),
            difficulty: config
        )
        
        startInactivityMonitoring()
    }
    
    // MARK: - Interaction Recording
    
    func recordInteraction() {
        lastInteractionTime = Date()
    }
    
    func recordMistake() {
        currentMetrics.mistakes += 1
        AudioManager.shared.playSoundEffect("gentle_boop.aac")
    }
    
    func recordHintUsed() {
        currentMetrics.usedHint = true
    }
    
    func recordQuit() {
        currentMetrics.didQuit = true
        currentMetrics.endTime = Date()
        
        // Major difficulty decrease
        difficultyManager.adjustDifficulty(based: currentMetrics)
        
        // Play encouraging message
        playEncouragingMessage()
    }
    
    func completeLevel() {
        currentMetrics.endTime = Date()
        
        // Adjust difficulty
        difficultyManager.adjustDifficulty(based: currentMetrics)
        
        // Play success sound
        AudioManager.shared.playSuccess()
        
        // Award coin
        PlayerDataStore.shared.awardCoin()
    }
    
    // MARK: - Inactivity Monitoring
    
    private func startInactivityMonitoring() {
        inactivityTimer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
            guard let self = self else { return }
            
            let inactivityDuration = Date().timeIntervalSince(self.lastInteractionTime)
            
            let newHintLevel = self.difficultyManager.shouldTriggerHint(
                inactivityDuration: inactivityDuration,
                currentMistakes: self.currentMetrics.mistakes
            )
            
            if newHintLevel != self.hintLevel {
                self.hintLevel = newHintLevel
                self.deliverHint(level: newHintLevel)
            }
            
            // Record long pauses
            if inactivityDuration >= 30 && 
               Int(inactivityDuration) % 30 == 0 {
                self.currentMetrics.longPauses += 1
            }
        }
    }
    
    private func deliverHint(level: HintLevel) {
        guard level != .none else { return }
        
        recordHintUsed()
        
        // Play appropriate hint audio
        switch level {
        case .gentle:
            playGentleHint()
        case .specific:
            playSpecificHint()
        case .verySpecific:
            playVerySpecificHint()
        case .none:
            break
        }
    }
    
    // MARK: - Hint Audio (Override in subclasses)
    
    func playGentleHint() {
        // Override in subclass
    }
    
    func playSpecificHint() {
        // Override in subclass
    }
    
    func playVerySpecificHint() {
        // Override in subclass
    }
    
    private func playEncouragingMessage() {
        let messages = [
            "bennie_encouraging_1.aac",
            "bennie_encouraging_2.aac",
            "bennie_encouraging_3.aac"
        ]
        AudioManager.shared.playBennie(messages.randomElement()!)
    }
    
    deinit {
        inactivityTimer?.invalidate()
    }
}
```

### 3. PuzzleMatchingViewModel (Example)

```swift
class PuzzleMatchingViewModel: ActivityViewModel {
    @Published var puzzleConfig: PuzzleMatchingConfig
    @Published var targetGrid: [[BennieColors?]]
    @Published var playerGrid: [[BennieColors?]]
    @Published var selectedColor: BennieColors?
    
    init() {
        let config = DifficultyManager.shared.getPuzzleConfig()
        self.puzzleConfig = config
        self.targetGrid = generatePattern(config: config)
        self.playerGrid = Array(repeating: Array(repeating: nil, count: config.gridSize), 
                               count: config.gridSize)
        
        super.init(activityType: .raetsel)
    }
    
    // MARK: - Gameplay
    
    func tapCell(row: Int, col: Int) {
        guard let color = selectedColor else { return }
        
        recordInteraction()
        
        playerGrid[row][col] = color
        AudioManager.shared.playSoundEffect("tap_wood.aac")
        
        // Check if mistake
        if targetGrid[row][col] != color && targetGrid[row][col] != nil {
            recordMistake()
        }
        
        // Check completion
        if playerGrid == targetGrid {
            completeLevel()
        }
    }
    
    func selectColor(_ color: BennieColors) {
        selectedColor = color
        recordInteraction()
    }
    
    func resetGrid() {
        playerGrid = Array(repeating: Array(repeating: nil, count: puzzleConfig.gridSize), 
                          count: puzzleConfig.gridSize)
        recordInteraction()
    }
    
    // MARK: - Hint Overrides
    
    override func playGentleHint() {
        AudioManager.shared.playBennie("bennie_puzzle_hint_10s.aac")
    }
    
    override func playSpecificHint() {
        AudioManager.shared.playBennie("bennie_puzzle_hint_20s.aac")
    }
    
    override func playVerySpecificHint() {
        // Show which cell needs to be filled
        // + Play very specific audio
    }
}
```

### 4. Integration in Activity View

```swift
struct PuzzleMatchingView: View {
    @StateObject private var viewModel = PuzzleMatchingViewModel()
    
    var body: some View {
        ZStack {
            // Forest background
            ForestBackgroundView()
            
            VStack {
                // Navigation header with progress bar
                NavigationHeader(
                    showHome: true,
                    showVolume: true,
                    currentCoins: PlayerDataStore.shared.currentPlayer?.coins ?? 0
                )
                
                Spacer()
                
                // Puzzle grids
                HStack(spacing: 40) {
                    // Target grid (ZIEL)
                    PuzzleGrid(
                        grid: viewModel.targetGrid,
                        title: "ZIEL",
                        isInteractive: false
                    )
                    
                    // Player grid (DU)
                    PuzzleGrid(
                        grid: viewModel.playerGrid,
                        title: "DU",
                        isInteractive: true,
                        onCellTap: { row, col in
                            viewModel.tapCell(row: row, col: col)
                        }
                    )
                }
                
                Spacer()
                
                // Color picker + tools
                HStack(spacing: 20) {
                    ForEach(viewModel.puzzleConfig.availableColors, id: \.self) { color in
                        ColorPickerButton(
                            color: color,
                            isSelected: viewModel.selectedColor == color,
                            onTap: { viewModel.selectColor(color) }
                        )
                    }
                    
                    Spacer()
                    
                    Button(action: { viewModel.resetGrid() }) {
                        Image(systemName: "arrow.clockwise")
                            .font(.largeTitle)
                    }
                }
                .padding(.horizontal, 40)
                .padding(.bottom, 20)
            }
            
            // Characters
            BennieView(expression: viewModel.hintLevel == .none ? .pointing : .encouraging)
                .frame(width: 200, height: 300)
                .position(x: 1000, y: 500)
            
            LemmingeView(expression: .curious)
                .frame(width: 80, height: 100)
                .position(x: 150, y: 150)
        }
    }
}
```

## PlayerDataStore Extension

Add learning profile management to existing PlayerDataStore:

```swift
extension PlayerDataStore {
    func updateLearningProfile(_ profile: LearningProfile) {
        guard var player = currentPlayer else { return }
        player.learningProfile = profile
        
        // Save to disk
        savePlayers()
    }
    
    func getLearningProfile(for playerId: String) -> LearningProfile? {
        return players.first { $0.id == playerId }?.learningProfile
    }
    
    func resetLearningProfile(for playerId: String) {
        guard let index = players.firstIndex(where: { $0.id == playerId }) else { return }
        players[index].learningProfile = LearningProfile()
        savePlayers()
    }
}
```

## Parent Dashboard Integration

Add learning profile display to parent dashboard:

```swift
struct LearningProfileView: View {
    let profile: LearningProfile
    
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Lernprofil")
                .font(.bennieFont(.title))
            
            StatRow(label: "Schwierigkeitsgrad", 
                   value: String(format: "%.1f", profile.difficultyLevel * 10))
            
            StatRow(label: "Ø Lösungszeit", 
                   value: String(format: "%.0fs", profile.averageSolveTime))
            
            StatRow(label: "Fehlerrate", 
                   value: String(format: "%.1f/Level", profile.mistakeFrequency))
            
            StatRow(label: "Abbruchrate", 
                   value: String(format: "%.0f%%", profile.quitRate * 100))
            
            Button("Profil zurücksetzen") {
                resetProfile()
            }
        }
        .padding()
        .background(BennieColors.cream)
        .cornerRadius(16)
    }
}
```

## Testing Utilities

```swift
#if DEBUG
extension DifficultyManager {
    func setTestDifficulty(_ difficulty: Float) {
        currentProfile.difficultyLevel = clamp(difficulty, min: 0.1, max: 0.9)
    }
    
    func simulateStrugglingChild() {
        currentProfile.averageSolveTime = 75.0
        currentProfile.mistakeFrequency = 3.5
        currentProfile.difficultyLevel = 0.2
    }
    
    func simulateFastLearner() {
        currentProfile.averageSolveTime = 12.0
        currentProfile.mistakeFrequency = 0.3
        currentProfile.difficultyLevel = 0.8
    }
}
#endif
```

## Performance Considerations

### Memory Management

- DifficultyManager is a singleton (one instance)
- ActivityMetrics are transient (created/destroyed per level)
- LearningProfile is persisted to disk after each level

### CPU Usage

- Inactivity timer runs at 1Hz (very light)
- Difficulty calculation is O(1) complexity
- Pattern generation is O(n²) where n = grid size (max 6×6 = 36 operations)

### Disk I/O

- Save learning profile after each level (< 1KB)
- Load learning profile on app launch only
- Use Codable for efficient JSON encoding

## Error Handling

```swift
extension DifficultyManager {
    func adjustDifficulty(based on metrics: ActivityMetrics) {
        do {
            // Attempt adjustment
            performAdjustment(metrics)
            saveProfile()
        } catch {
            print("Difficulty adjustment failed: \(error)")
            // Fallback: keep current difficulty
        }
    }
}
```

## Debugging Tools

```swift
#if DEBUG
struct DifficultyDebugView: View {
    @ObservedObject var manager = DifficultyManager.shared
    
    var body: some View {
        VStack {
            Text("Difficulty: \(manager.currentProfile.difficultyLevel)")
            Text("Avg Solve Time: \(manager.currentProfile.averageSolveTime)s")
            Text("Mistakes: \(manager.currentProfile.mistakeFrequency)")
            
            Slider(value: Binding(
                get: { Double(manager.currentProfile.difficultyLevel) },
                set: { manager.setTestDifficulty(Float($0)) }
            ), in: 0.1...0.9)
        }
    }
}
#endif
```
