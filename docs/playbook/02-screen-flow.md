# Part 2: Screen Flow & State Machine

> **Chapter 2** of the Bennie Brand Playbook
>
> Covers: Game flow diagram, state machine, coin system, progress bar

---

## 2.1 Screen Flow Diagram

```
+-----------------------------------------------------------------------------+
|                              COMPLETE GAME FLOW                              |
+-----------------------------------------------------------------------------+

    +----------+
    |  LAUNCH  |
    +----+-----+
         |
         v
+-----------------+
| LOADING SCREEN  | ------> Narrator: "Warte kurz. Wir sind gleich bereit."
|   (0-100%)      |
+--------+--------+
         | 100%
         v
+-----------------+
| PLAYER SELECT   | ------> Narrator: "Wie heisst du? Alexander oder Oliver?"
| [Alex] [Oliver] |
+--------+--------+
         | tap name
         v
+-----------------+------> Narrator: "Was möchtest du spielen?"
|   HOME SCREEN   | <-------------------------------------------+
|  (Waldabenteuer)|                                             |
|                 | ------> Bennie: "Hi [Name], ich bin Bennie" |
| [Rätsel][Zahlen]|                                             |
| [Locked] chest  |                                             |
+---+--------+----+                                             |
    |        |                                                  |
    | tap    | tap                                              |
    v        v                                                  |
+-------+ +-------+                                             |
|RÄTSEL | |ZAHLEN |  <- Activity Selection Screens              |
|       | |       |                                             |
|[Puzzle]| |[Würfel]|                                           |
|[Laby] | |[Wähle]|                                             |
+---+---+ +---+---+                                             |
    |         |                                                 |
    v         v                                                 |
+-----------------+                                             |
| ACTIVITY SCREEN |  <- Gameplay happens here                   |
|   (gameplay)    |                                             |
+--------+--------+                                             |
         | success                                              |
         v                                                      |
    +---------+                                                 |
    | +1 COIN | --> Coin animation flies to progress bar        |
    +----+----+                                                 |
         |                                                      |
         v                                                      |
    +===========+     NO      +------------+                    |
    | 5 COINS?  |------------>| Next Level |--------------------+
    | (mod 5=0) |             +------------+                    |
    +====+=====++                                               |
         | YES                                                  |
         v                                                      |
+-----------------+                                             |
|   CELEBRATION   | ------> Bennie: "Wir haben 5 Goldmünzen!"   |
|    OVERLAY      |         + Confetti + Characters jump        |
|  (transparent)  |                                             |
+--------+--------+                                             |
         | tap "Weiter"                                         |
         v                                                      |
    +===========+     NO                                        |
    | 10 COINS? |--------------------------------------------->-+
    +====+=====++
         | YES (user can also tap chest anytime when >=10)
         v
+-----------------+
| TREASURE SCREEN | ------> Bennie: "Du kannst YouTube schauen!"
|                 |
| [5min] [10+2min]|
+--------+--------+
         | tap option (deducts coins)
         v
+-----------------+
| VIDEO SELECTION | ------> Shows pre-approved video thumbnails
|  [thumbnails]   |
+--------+--------+
         | tap video
         v
+-----------------+
|  VIDEO PLAYER   | ------> Analog clock countdown
|  [analog clock] |         1 min warning: "Noch eine Minute."
+--------+--------+
         | time up
         v
         +------------> Bennie: "Die Zeit ist um. Lass uns spielen!"
                        +---------------------------------------------+
```

---

## 2.2 State Machine Definition

### Global States

```swift
enum GameState {
    case loading
    case playerSelection
    case home
    case activitySelection(ActivityType)
    case playing(ActivityType, SubActivity)
    case levelComplete
    case celebrationOverlay      // Only at 5-coin milestones
    case treasureScreen
    case videoSelection
    case videoPlaying
    case parentGate              // Math question gate
    case parentDashboard         // Settings screen
}

enum ActivityType {
    case raetsel    // Rätsel
    case zahlen     // Zahlen 1,2,3
    // Future phases:
    // case zeichnen
    // case logik
}

enum SubActivity {
    // Rätsel
    case puzzleMatching
    case labyrinth

    // Zahlen
    case wuerfel     // Dice game
    case waehleZahl  // Choose the number
}
```

### State Transitions

| From State           | Event            | To State             | Side Effects                    |
| -------------------- | ---------------- | -------------------- | ------------------------------- |
| `loading`            | progress=100%    | `playerSelection`    | Play narrator welcome           |
| `playerSelection`    | tap(player)      | `home`               | Load player data, play greeting |
| `home`               | tap(activity)    | `activitySelection`  | —                               |
| `home`               | tap(chest)       | `treasureScreen`     | Only if coins >= 10             |
| `home`               | tap(settings)    | `parentGate`         | Show math question              |
| `parentGate`         | correctAnswer    | `parentDashboard`    | —                               |
| `activitySelection`  | tap(subActivity) | `playing`            | Start activity, play intro      |
| `playing`            | levelSuccess     | `levelComplete`      | +1 coin, success sound          |
| `playing`            | tap(home)        | `home`               | Save progress                   |
| `levelComplete`      | coins % 5 == 0   | `celebrationOverlay` | Celebration audio               |
| `levelComplete`      | coins % 5 != 0   | `playing` (next)     | Auto-advance                    |
| `celebrationOverlay` | tap(weiter)      | Check coins          | —                               |
| `celebrationOverlay` | coins >= 10      | `treasureScreen`     | Auto-navigate                   |
| `celebrationOverlay` | coins < 10       | `playing`            | Continue activity               |
| `treasureScreen`     | tap(5min)        | `videoSelection`     | Deduct 10 coins                 |
| `treasureScreen`     | tap(10min)       | `videoSelection`     | Deduct 20 coins                 |
| `videoSelection`     | tap(video)       | `videoPlaying`       | Start timer                     |
| `videoPlaying`       | timeUp           | `home`               | "Time up" audio                 |

---

## 2.3 Coin & Progress System

### Coin Constants

```swift
struct CoinSystem {
    static let coinsPerLevel = 1
    static let celebrationMilestone = 5    // Show overlay every 5 coins
    static let tier1Redemption = 10        // 5 minutes YouTube
    static let tier2Redemption = 20        // 10 + 2 minutes YouTube
    static let tier2BonusMinutes = 2
}
```

### Progress Bar Behavior

| Coins | Visual State                | Action on Level Complete       |
| ----- | --------------------------- | ------------------------------ |
| 0-4   | Empty slots + earned coins  | Coin flies to bar, subtle glow |
| 5     | 50% filled                  | **CELEBRATION OVERLAY**        |
| 6-9   | Continue filling to 100%    | Coin flies to bar              |
| 10    | Full (1 chest icon appears) | **CELEBRATION** + can redeem   |
| 11-19 | Second bar starts           | Coin flies to bar              |
| 20    | Two chest icons             | **CELEBRATION** + bonus option |

### Progress Bar Component

This component is **shared across all activity screens**:

```swift
struct ProgressBarView: View {
    let currentCoins: Int
    let maxCoins: Int = 10  // Per chest

    var body: some View {
        HStack {
            // Berry decoration left
            Image("berry_cluster_left")

            // Wood trough progress bar
            ZStack(alignment: .leading) {
                // Empty state (dark wood interior)
                RoundedRectangle(cornerRadius: 8)
                    .fill(Color(hex: "6B4423"))

                // Fill state (success green)
                RoundedRectangle(cornerRadius: 8)
                    .fill(Color(hex: "99BF8C"))
                    .frame(width: progressWidth)

                // Coin slots overlay
                CoinSlotsView(filled: currentCoins % 10)
            }
            .frame(height: 40)

            // Berry decoration right
            Image("berry_cluster_right")

            // Chest icon(s)
            ChestIndicator(chests: currentCoins / 10)
        }
    }
}
```
