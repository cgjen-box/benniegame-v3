# Part 0: The Game

> **Chapter 0** of the Bennie Brand Playbook
>
> Covers: Philosophy, core loop, activities, reward system, adaptive difficulty

---

## 0.1 Game Overview

**Bennie und die Lemminge** is a fun, friendly educational game designed for neurodivergent children (ages 4-5) to learn core skills before elementary school starts.

### The Philosophy

We want to help children learn. Neurodivergent children often experience lower baseline excitement, making it difficult to engage with traditional learning methods. They can't just sit down and study—we must take them on a journey. We need to excite them on what we do and motivate with clear and tangible reward. Youtube.

**Our approach:**
- **Make learning fun** — Every activity is a playful adventure
- **Challenge appropriately** — Difficulty adapts to maintain engagement without frustration
- **Celebrate success** — Success creates neural excitement, reinforcing positive associations
- **Avoid over-stimulation** — We balance excitement carefully to prevent overwhelm
- **Personalize experience** — Individual profiles track preferences and adapt accordingly
- **End positively** — Always leave on a good note with gentle wind-down reminders

### The YouTube Motivation

Let's be honest: kids love YouTube. Instead of fighting this, we use it as healthy motivation:
- Complete activities → Earn coins → Trade for YouTube time
- This creates a positive association with learning
- Screen time is controlled and pre-approved
- The reward feels earned, not entitled

### Graceful Exit Strategy

When total play time approaches the daily limit:
1. Gentle reminder: "Dein iPad braucht bald eine Pause."
2. Final activity notice: "Noch eine Aktivität, dann laden wir die Batterie."
3. Positive closure: "Du hast heute so toll gespielt! Bis morgen! Bring das IPad zu Mama oder Papa"

---

## 0.2 Core Loop

```
+---------------------------------------------------------------------+
|                         CORE GAME LOOP                               |
+---------------------------------------------------------------------+
|                                                                       |
|     +---------------+                                                 |
|     | Play Activity | --- Complete level successfully ---+           |
|     +---------------+                                     |           |
|            ^                                             v           |
|            |                                    +---------------+     |
|            |                                    |  Earn 1 Coin  |     |
|            |                                    +---------------+     |
|            |                                             |           |
|            |              NO                             v           |
|            +------------ Have 10+ coins? <---------------+           |
|                               | YES                      |           |
|                               v                          | NO        |
|                    +--------------------+               |           |
|                    | Trade for YouTube  |               |           |
|                    | (5min or 10+2min)  |               |           |
|                    +--------------------+               |           |
|                               |                          |           |
|                               v                          |           |
|                    +--------------------+               |           |
|                    |    Watch Video     |               |           |
|                    |  (controlled time) |               |           |
|                    +--------------------+               |           |
|                               |                          |           |
|                               +--------------------------+           |
|                                                                       |
+---------------------------------------------------------------------+
```

---

## 0.3 Activities (Phase 1 - MVP)

| Activity | German Name      | Description          | Sub-Activities                | Status     |
| -------- | ---------------- | -------------------- | ----------------------------- | ---------- |
| Puzzles  | **Rätsel**       | Visual pattern games | Puzzle Matching, Labyrinth    | In Scope |
| Numbers  | **Zahlen 1,2,3** | Number recognition   | Würfel (Dice), Wähle die Zahl | In Scope |
| Drawing  | Zeichnen         | *Future phase*       | —                             | Locked   |
| Logic    | Logik            | *Future phase*       | —                             | Locked   |

### Activity Rotation Strategy

To prevent boredom, we rotate sub-activities:

```swift
// Example: Rätsel rotation
enum RaetselSubActivity {
    case puzzleMatching
    case labyrinth
}

// After completing 3 levels of one type, suggest switching
func getNextActivity(current: RaetselSubActivity, levelsCompleted: Int) -> RaetselSubActivity {
    if levelsCompleted % 3 == 0 {
        return current == .puzzleMatching ? .labyrinth : .puzzleMatching
    }
    return current
}
```

---

## 0.4 Reward System

### Coin Economy

| Action                      | Coins |
| --------------------------- | ----- |
| Complete any activity level | +1    |
| Lose/quit activity          | 0     |

### Redemption Options

| Milestone | Coins Required | Reward               | Visual        |
| --------- | -------------- | -------------------- | ------------- |
| Tier 1    | 10 coins       | 5 minutes YouTube    | 1 chest icon  |
| Tier 2    | 20 coins       | 10 + 2 bonus minutes | 2 chest icons |

### Celebration Milestones

Celebration overlays appear at **every 5 coins**: 5, 10, 15, 20, 25...

```swift
let shouldCelebrate = (coins % 5 == 0) && (coins > 0)
```

---

## 0.5 Adaptive Difficulty System

### AI-Powered Learning Profile

We track each child's engagement patterns to optimize difficulty:

```swift
struct LearningProfile {
    // Performance metrics
    var averageSolveTime: TimeInterval
    var mistakeFrequency: Double      // Mistakes per level
    var quitRate: Double              // Levels abandoned
    var sessionDuration: TimeInterval

    // Engagement indicators
    var hintUsageRate: Double
    var celebrationEngagement: Bool   // Did they tap Weiter quickly?
    var preferredActivities: [ActivityType: Int]

    // Adaptive parameters
    var difficultyLevel: Float        // 0.0 (easiest) to 1.0 (hardest)
    var gridSizePreference: Int       // Preferred puzzle grid size
    var colorCount: Int               // Number of colors in puzzles
}
```

### Difficulty Adjustment Rules

| Signal                      | Interpretation         | Adjustment                          |
| --------------------------- | ---------------------- | ----------------------------------- |
| Solve time < 10s            | Too easy               | Increase difficulty                 |
| Solve time > 60s            | Struggling             | Decrease difficulty                 |
| 3+ mistakes per level       | Too hard               | Decrease difficulty, offer hints    |
| Quit mid-activity           | Frustration            | Major decrease, encouraging message |
| Fast successive completions | Engaged & capable      | Gradually increase                  |
| Long pause (>30s)           | Confused or distracted | Offer gentle hint                   |
