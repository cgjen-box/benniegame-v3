# Activity-Specific Difficulty Configurations

## Overview

Detailed difficulty parameters for each activity type, with examples at each difficulty level.

## Playbook References

**Source**: `docs/playbook/FULL_ARCHIVE.md`
- Section 4.4: Puzzle Matching Grid Progression
- Section 4.5: Labyrinth mechanics
- Section 4.6: Zahlen number progression

**Design References**:
- `design/references/screens/Reference_Matching_Game_Screen.png` - Puzzle layout
- `design/references/screens/Reference_Layrinth_Game_Screen.png` - Labyrinth path example
- `design/references/screens/Reference_Numbers_Game_Screen.png` - Number tablet

---

## 1. Puzzle Matching (RÃ¤tsel)

### Difficulty Curve

| Difficulty Range | Grid Size | Colors | Filled Cells | Example Patterns |
|-----------------|-----------|--------|--------------|------------------|
| 0.0 - 0.29 | 3×3 | 2 (yellow, green) | 2-3 | Corner patterns, simple L-shapes |
| 0.3 - 0.49 | 3×3 | 3 (add gray) | 3-5 | Cross patterns, diagonals |
| 0.5 - 0.69 | 4×4 | 3 colors | 4-7 | Checkerboard variants, T-shapes |
| 0.7 - 0.84 | 5×5 | 3-4 colors | 5-10 | Complex asymmetric patterns |
| 0.85 - 1.0 | 6×6 | 4 colors | 6-12 | Very complex, multiple clusters |

### Configuration Code

```swift
struct PuzzleMatchingConfig {
    let gridSize: Int
    let availableColors: [BennieColors]
    let filledCellRange: ClosedRange<Int>
    
    static func config(for difficulty: Float) -> PuzzleMatchingConfig {
        switch difficulty {
        case 0.0..<0.3:
            return PuzzleMatchingConfig(
                gridSize: 3,
                availableColors: [.woodland, .coinGold],  // Green, Yellow
                filledCellRange: 2...3
            )
            
        case 0.3..<0.5:
            return PuzzleMatchingConfig(
                gridSize: 3,
                availableColors: [.woodland, .coinGold, .pathStone],  // Add Gray
                filledCellRange: 3...5
            )
            
        case 0.5..<0.7:
            return PuzzleMatchingConfig(
                gridSize: 4,
                availableColors: [.woodland, .coinGold, .pathStone],
                filledCellRange: 4...7
            )
            
        case 0.7..<0.85:
            return PuzzleMatchingConfig(
                gridSize: 5,
                availableColors: [.woodland, .coinGold, .pathStone, .sky],  // Add Blue
                filledCellRange: 5...10
            )
            
        default:  // 0.85-1.0
            return PuzzleMatchingConfig(
                gridSize: 6,
                availableColors: [.woodland, .coinGold, .pathStone, .sky],
                filledCellRange: 6...12
            )
        }
    }
}
```

### Pattern Generation

```swift
func generatePattern(config: PuzzleMatchingConfig) -> [[BennieColors?]] {
    let filledCount = Int.random(in: config.filledCellRange)
    var grid = Array(repeating: Array(repeating: nil as BennieColors?, 
                                     count: config.gridSize), 
                    count: config.gridSize)
    
    // Fill cells randomly but avoid isolated cells
    var filledCells = 0
    while filledCells < filledCount {
        let row = Int.random(in: 0..<config.gridSize)
        let col = Int.random(in: 0..<config.gridSize)
        
        if grid[row][col] == nil {
            grid[row][col] = config.availableColors.randomElement()
            filledCells += 1
        }
    }
    
    return grid
}
```

---

## 2. Labyrinth (RÃ¤tsel)

### Difficulty Curve

| Difficulty Range | Decision Points | Path Width | Visual Complexity |
|-----------------|-----------------|------------|-------------------|
| 0.0 - 0.39 | 5-7 | 60pt (wide) | Simple curves, obvious dead ends |
| 0.4 - 0.69 | 8-12 | 44pt (standard) | Multiple branches, some false paths |
| 0.7 - 1.0 | 13-16 | 36pt (narrow) | Complex maze, many dead ends |

### Configuration Code

```swift
struct LabyrinthConfig {
    let decisionPoints: Int
    let pathWidth: CGFloat
    let deadEndProbability: Float
    
    static func config(for difficulty: Float) -> LabyrinthConfig {
        let decisionPoints = Int(5 + (difficulty * 11))  // 5 to 16
        
        let pathWidth: CGFloat
        let deadEndProb: Float
        
        switch difficulty {
        case 0.0..<0.4:
            pathWidth = 60
            deadEndProb = 0.2  // Few dead ends
            
        case 0.4..<0.7:
            pathWidth = 44
            deadEndProb = 0.4  // Some dead ends
            
        default:
            pathWidth = 36
            deadEndProb = 0.6  // Many dead ends
        }
        
        return LabyrinthConfig(
            decisionPoints: decisionPoints,
            pathWidth: pathWidth,
            deadEndProbability: deadEndProb
        )
    }
}
```

### Path Generation

```swift
func generateLabyrinth(config: LabyrinthConfig) -> LabyrinthPath {
    // Use recursive backtracking to generate maze
    // Decision point = any intersection with 2+ choices
    
    var path = LabyrinthPath()
    path.startPoint = CGPoint(x: 100, y: 400)
    path.goalPoint = CGPoint(x: 1000, y: 400)
    path.pathWidth = config.pathWidth
    
    // Generate path with specified number of decision points
    // Add dead ends based on probability
    
    return path
}
```

---

## 3. Zahlen: WÃ¼rfel (Dice)

### Difficulty Curve

| Difficulty Range | Dice Range | Visual Aids | Hint Availability |
|-----------------|------------|-------------|-------------------|
| 0.0 - 0.39 | 1-5 | Large dots | Hints after 10s |
| 0.4 - 0.69 | 1-7 | Standard dots | Hints after 15s |
| 0.7 - 1.0 | 1-10 | Smaller numbers | Hints after 20s |

### Configuration Code

```swift
struct WuerfelConfig {
    let numberRange: ClosedRange<Int>
    let hintDelay: TimeInterval
    let dotSize: CGFloat
    
    static func config(for difficulty: Float) -> WuerfelConfig {
        switch difficulty {
        case 0.0..<0.4:
            return WuerfelConfig(
                numberRange: 1...5,
                hintDelay: 10.0,
                dotSize: 24.0  // Large dots
            )
            
        case 0.4..<0.7:
            return WuerfelConfig(
                numberRange: 1...7,
                hintDelay: 15.0,
                dotSize: 20.0  // Standard dots
            )
            
        default:
            return WuerfelConfig(
                numberRange: 1...10,
                hintDelay: 20.0,
                dotSize: 16.0  // Smaller numbers
            )
        }
    }
}
```

---

## 4. Zahlen: WÃ¤hle die Zahl

### Difficulty Curve

| Difficulty Range | Number Range | Distractor Count | Distractor Similarity |
|-----------------|--------------|------------------|----------------------|
| 0.0 - 0.39 | 1-5 | 4 distractors | Very different (1 vs 5) |
| 0.4 - 0.69 | 1-7 | 6 distractors | Somewhat similar (3 vs 5) |
| 0.7 - 1.0 | 1-10 | 9 distractors | Very similar (6 vs 9) |

### Configuration Code

```swift
struct WaehleZahlConfig {
    let numberRange: ClosedRange<Int>
    let distractorCount: Int
    let similarityThreshold: Int
    
    static func config(for difficulty: Float) -> WaehleZahlConfig {
        switch difficulty {
        case 0.0..<0.4:
            return WaehleZahlConfig(
                numberRange: 1...5,
                distractorCount: 4,
                similarityThreshold: 3  // Numbers at least 3 apart
            )
            
        case 0.4..<0.7:
            return WaehleZahlConfig(
                numberRange: 1...7,
                distractorCount: 6,
                similarityThreshold: 2  // Numbers at least 2 apart
            )
            
        default:
            return WaehleZahlConfig(
                numberRange: 1...10,
                distractorCount: 9,
                similarityThreshold: 1  // Adjacent numbers allowed
            )
        }
    }
}

func generateNumberGrid(config: WaehleZahlConfig, target: Int) -> [Int] {
    var numbers: Set<Int> = [target]
    
    while numbers.count < config.distractorCount + 1 {
        let candidate = Int.random(in: config.numberRange)
        
        // Check similarity constraint
        let minDistance = numbers.map { abs($0 - candidate) }.min() ?? 10
        if minDistance >= config.similarityThreshold {
            numbers.insert(candidate)
        }
    }
    
    return numbers.shuffled()
}
```

---

## Common Parameters

### Hint System

All activities share this hint timing logic:

```swift
struct HintConfig {
    let firstHintDelay: TimeInterval
    let secondHintDelay: TimeInterval
    let thirdHintDelay: TimeInterval
    
    static func config(for difficulty: Float) -> HintConfig {
        // Easier difficulties get faster hints
        let baseDelay = 10.0 + (difficulty * 10.0)  // 10-20 seconds
        
        return HintConfig(
            firstHintDelay: baseDelay,
            secondHintDelay: baseDelay + 10,
            thirdHintDelay: baseDelay + 20
        )
    }
}
```

### Success Threshold

Touch precision required for success:

```swift
struct SuccessThreshold {
    let pathTolerance: CGFloat  // For labyrinth
    let traceTolerance: CGFloat  // For number tracing
    
    static func config(for difficulty: Float) -> SuccessThreshold {
        return SuccessThreshold(
            pathTolerance: 44 + ((1.0 - difficulty) * 16),  // 44-60pt
            traceTolerance: 30 + ((1.0 - difficulty) * 10)   // 30-40pt
        )
    }
}
```

---

## Testing Configurations

### Preset Difficulty Profiles

For testing, provide named difficulty presets:

```swift
enum DifficultyPreset {
    case veryEasy
    case easy
    case medium
    case hard
    case veryHard
    
    var difficultyLevel: Float {
        switch self {
        case .veryEasy: return 0.15
        case .easy: return 0.35
        case .medium: return 0.55
        case .hard: return 0.75
        case .veryHard: return 0.92
        }
    }
}
```

### Example Test Cases

```swift
// Test: Very Easy Puzzle
let easyPuzzle = PuzzleMatchingConfig.config(for: 0.15)
// Expected: 3×3 grid, 2 colors, 2-3 filled cells

// Test: Hard Labyrinth
let hardLabyrinth = LabyrinthConfig.config(for: 0.75)
// Expected: 13 decision points, 36pt paths, 60% dead ends

// Test: Medium Numbers
let mediumNumbers = WuerfelConfig.config(for: 0.55)
// Expected: 1-7 range, 15s hint delay
```

---

## Parent Dashboard Override

Parents can manually set difficulty via Parent Dashboard:

```swift
struct ParentOverride {
    let isEnabled: Bool
    let forcedDifficulty: Float?
    
    func apply(to profile: inout LearningProfile) {
        if isEnabled, let forced = forcedDifficulty {
            profile.difficultyLevel = forced
            profile.lastUpdated = Date()
        }
    }
}
```

This allows parents to:
1. Lock difficulty at a specific level
2. Override automatic adjustments
3. Reset to default adaptive behavior
