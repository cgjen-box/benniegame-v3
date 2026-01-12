# 4.3-4.6 Home & Activity Screens

> Part of [Screen Specifications](README.md)

---

## 4.3 Home Screen (Waldabenteuer)

### Layout

```
+------------------------------------------------------------------------------+
|   +------------------------------------------------------------+  +--+      |
|   |               Waldabenteuer                                |  |P |      |
|   +------------------------------------------------------------+  +--+      |
|                                                                    profile   |
|                                                                              |
|    +-----------------------------+ +-----------------------------+          |
|    |      ?                      | |       123                   |          |
|    |    Rätsel                   | |    Zahlen 1,2,3            |          |
|    |   (glowing - unlocked)      | |   (glowing - unlocked)      |          |
|    +-----------------------------+ +-----------------------------+          |
|     ^ hanging from branch           ^ hanging from branch                   |
|                                                                              |
|    +-----------------------------+ +-----------------------------+          |
|    |    Pencil                   | |    Puzzle                   |          |
|    |    Zeichnen                 | |    Logik                    |          |
|    |   (chains - locked)         | |   (chains - locked)         |          |
|    +-----------------------------+ +-----------------------------+          |
|                                                                              |
|    +---------+                              +----+  +----+                   |
|    |   L     |     Bennie (pointing)        | Cog|  | ? |    [CHEST]       |
|    |mischief |                              +----+  +----+                   |
|    +---------+                             settings  help                   |
+------------------------------------------------------------------------------+
```

### Activity Signs

| Activity | German         | Default State  | Tap Action                       |
| -------- | -------------- | -------------- | -------------------------------- |
| Rätsel   | "Rätsel"       | Unlocked (glowing) | -> Activity Selection        |
| Zahlen   | "Zahlen 1,2,3" | Unlocked (glowing) | -> Activity Selection        |
| Zeichnen | "Zeichnen"     | Locked (chains)    | Bennie: "Das ist noch gesperrt." |
| Logik    | "Logik"        | Locked (chains)    | Bennie: "Das ist noch gesperrt." |

### Locked Sign Visual

```swift
struct LockedSignView: View {
    var body: some View {
        ZStack {
            // Base wooden sign (dimmed)
            WoodSignView()
                .opacity(0.6)

            // X-pattern chains
            ChainPattern()

            // Padlock at center bottom
            Image("padlock")
                .offset(y: 60)
        }
    }
}
```

### Chest Behavior

| Coins | Chest State     | Visual                     | Tap Action                 |
| ----- | --------------- | -------------------------- | -------------------------- |
| 0-9   | Closed          | Dull wood, no glow         | Bennie: "Noch [X] Münzen!" |
| 10-19 | Open            | Golden glow, coins visible | -> Treasure Screen         |
| 20+   | Open + sparkles | Extra glow, 2 chest icons  | -> Treasure Screen         |

---

## 4.4 Rätsel: Puzzle Matching Screen

### Layout

```
+------------------------------------------------------------------------------+
|   +--------+        +=================================+    +--------+         |
|   |  Home  |        |  Progress Bar with Coin Slots  |    | Volume |         |
|   +--------+        +=================================+    +--------+         |
|                                                                              |
|       +----------------------+    -->    +----------------------+            |
|       |       ZIEL           |          |         DU           |            |
|       |   +---+---+---+      |          |   +---+---+---+      |            |
|       |   |   | Y |   |      |          |   |   | Y |   |      |            |
|       |   +---+---+---+      |          |   +---+---+---+      |            |
|       |   | G |   |   |      |          |   |   |   |   |      |            |
|       |   +---+---+---+      |          |   +---+---+---+      |            |
|       |   | Y | Y |   |      |          |   |   | Y |   |      |            |
|       |   +---+---+---+      |          |   +---+---+---+      |            |
|       |      Stone tablet    |          |      Stone tablet    |            |
|       +----------------------+          +----------------------+            |
|                                                                              |
|   +-------+                                                   +-------+     |
|   |  L    |                                                   | Bennie|     |
|   |curious|                                                   |pointing     |
|   +-------+                                                   +-------+     |
|                                                                              |
|            +-----------------------------------------------------------+    |
|            |   G     Y     W    |    Eraser     Reset                   |    |
|            |  Grün  Gelb   Grau |                                       |    |
|            +-----------------------------------------------------------+    |
|                    Color palette (wooden log container)                     |
+------------------------------------------------------------------------------+
```

### Grid Progression (Adaptive Difficulty)

| Level Range | Grid Size | Colors            | Filled Cells |
| ----------- | --------- | ----------------- | ------------ |
| 1-5         | 3x3       | 2 (green, yellow) | 2-4          |
| 6-10        | 3x3       | 3 (add gray)      | 3-5          |
| 11-20       | 4x4       | 3 colors          | 4-7          |
| 21-30       | 5x5       | 3-4 colors        | 5-10         |
| 31+         | 6x6       | 4 colors          | 6-12         |

### Touch Targets

| Element       | Size            | Behavior                         |
| ------------- | --------------- | -------------------------------- |
| Grid cell     | 96x96pt minimum | Tap to fill with selected color  |
| Color picker  | 80x80pt         | Tap to select color (leaf shape) |
| Eraser button | 60x60pt         | Tap to enable eraser mode        |
| Reset button  | 60x60pt         | Clear entire player grid         |
| Home button   | 96x60pt         | Return to home                   |
| Volume button | 60x60pt         | Toggle sound                     |

### Gameplay Flow

```swift
struct PuzzleMatchingGame {
    // 1. Show target pattern (ZIEL)
    // 2. Player taps colors then cells (DU)
    // 3. Real-time comparison
    // 4. When DU matches ZIEL -> Success!

    func checkMatch() -> Bool {
        return playerGrid == targetGrid
    }

    func onCellTap(row: Int, col: Int) {
        guard selectedColor != nil else { return }

        playerGrid[row][col] = selectedColor
        playSound("tap_wood.aac")

        if checkMatch() {
            onSuccess()
        }
    }

    func onSuccess() {
        playSound("success_chime.aac")
        awardCoin()

        // Check for celebration milestone
        if player.coins % 5 == 0 {
            showCelebrationOverlay()
        } else {
            loadNextLevel()
        }
    }
}
```

---

## 4.5 Rätsel: Labyrinth Screen

### Layout

```
+------------------------------------------------------------------------------+
|                     +-------------------------------+                        |
|   +--------+        | Bennie & Lemminge Labyrinth   |        +--------+     |
|   |  Home  |        +-------------------------------+        | Volume |     |
|   +--------+              (wooden sign hanging)              +--------+     |
|                                                                              |
|   Bennie (pointing)      START                                               |
|        |                   |                                                 |
|      L              +----O===========================O                      |
|    (scared)         |   /                             \                      |
|                     |  O      House      House     O------+                 |
|                     |   \                         /       |                 |
|                     |    O=======O=======O=======O        |                 |
|                     |                                      |      ZIEL       |
|                     +-O================================O------> L           |
|                                                              (celebrating)  |
|                                                                              |
|              +-------------------------------------+                        |
|              |    Progress Bar + Coins            |                        |
|              +-------------------------------------+                        |
+------------------------------------------------------------------------------+
```

### Gameplay Mechanics

| Action     | Input                 | Validation                | Feedback                            |
| ---------- | --------------------- | ------------------------- | ----------------------------------- |
| Start path | Touch START marker    | Must begin at START       | Glow effect                         |
| Draw path  | Drag finger along     | Must stay on stone path   | Path highlights                     |
| Leave path | Lift finger or go off | Show error, allow retry   | Bennie: "Da komme ich nicht durch." |
| Complete   | Reach ZIEL            | Touch within 44pt of goal | Celebration!                        |

### Path Detection

```swift
struct LabyrinthPath {
    let validPathPoints: [CGPoint]  // Pre-defined correct route
    let pathWidth: CGFloat = 44     // Touch tolerance in points

    func isOnPath(_ point: CGPoint) -> Bool {
        validPathPoints.contains { pathPoint in
            distance(point, pathPoint) <= pathWidth
        }
    }

    func hasReachedGoal(_ point: CGPoint) -> Bool {
        distance(point, goalPosition) <= pathWidth
    }

    func distance(_ a: CGPoint, _ b: CGPoint) -> CGFloat {
        sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2))
    }
}
```

---

## 4.6 Zahlen: Wähle die Zahl Screen

### Layout

```
+------------------------------------------------------------------------------+
|   +--------+        +=================================+    +--------+         |
|   |  Home  |        |  Progress Bar with Coin Slots  |    | Volume |         |
|   +--------+        +=================================+    +--------+         |
|                                                                              |
|                      +-----------------------------------+                   |
|                      |                                   |                   |
|           L          |   1   2   3   4                   |                   |
|        (curious)     |                                   |                   |
|                      |   5   6   7                       |      Bennie       |
|                      |                                   |   (pointing)      |
|           L          |   8   9   10                      |                   |
|        (excited)     |                                   |                   |
|                      |      Stone tablet with            |                   |
|                      |      traceable numbers            |                   |
|                      +-----------------------------------+                   |
|                                                                              |
|                      +-------------------------------------+                 |
|                      |   G     Y     Eraser     Reset     |                 |
|                      |  (color tools for tracing)         |                 |
|                      +-------------------------------------+                 |
+------------------------------------------------------------------------------+
```

### Number Tracing System

| Number | Stroke Guide             | Arrow Indicators     |
| ------ | ------------------------ | -------------------- |
| 1      | Single downstroke        | Down                 |
| 2      | Curve right, down, right | Curve, Down, Right   |
| 3      | Two curves right         | Curve, Curve         |
| 4      | Down, right, down        | Down, Right, Down    |
| 5      | Down, curve right        | Down, Curve          |
| 6      | Curve down and around    | Curve, Circle        |
| 7      | Right, diagonal down     | Right, Diagonal      |
| 8      | Double loop              | Figure-8             |
| 9      | Circle, down             | Circle, Down         |
| 10     | "1" then "0"             | Two separate strokes |

### Gameplay Flow

```
1. Narrator: "Zeig mir die [N]!"
2. Target number glows golden on stone tablet
3. Numbers have arrow guides showing stroke direction
4. Child traces the number with finger
5. Validation: 70% of path followed = success
6. Success -> +1 coin, next number (random 1-10)
```

### Validation Algorithm

```swift
struct NumberTracingValidator {
    let requiredPathCoverage: Float = 0.70  // 70%

    func validateTrace(
        userPath: [CGPoint],
        targetNumber: Int
    ) -> Bool {
        let targetPath = getPathForNumber(targetNumber)
        let coveredPoints = targetPath.filter { targetPoint in
            userPath.contains { userPoint in
                distance(userPoint, targetPoint) <= 30  // 30pt tolerance
            }
        }

        let coverage = Float(coveredPoints.count) / Float(targetPath.count)
        return coverage >= requiredPathCoverage
    }
}
```
