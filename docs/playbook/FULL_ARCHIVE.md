# ARCHIVED - Full Playbook

> **This file is archived for reference.**
>
> **For maintainable versions, see the individual chapter files in this folder:**
> - [README.md](README.md) - Table of contents linking to all chapters
> - Each chapter is < 5k tokens for efficient context usage

---

# Bennie und die Lemminge
## Complete Brand & Screen Design Playbook

> **Version**: 3.1 | **Last Updated**: January 2026
>
> *A magical, autism-friendly forest adventure for Alexander & Oliver*

---

# Table of Contents

1. [Part 0: The Game](#part-0-the-game)
2. [Part 1: Brand Identity](#part-1-brand-identity)
3. [Part 2: Screen Flow & State Machine](#part-2-screen-flow--state-machine)
4. [Part 3: Narrator & Voice Script](#part-3-narrator--voice-script)
5. [Part 4: Screen Specifications](#part-4-screen-specifications)
6. [Part 5: Technical Requirements](#part-5-technical-requirements)
7. [Part 6: Animation & Sound Guide](#part-6-animation--sound-guide)
8. [Part 7: Quick Reference Card](#part-7-quick-reference-card)
9. [Part 8: File Structure](#part-8-file-structure)
10. [**Part 9: Asset Production Pipeline**](#part-9-asset-production-pipeline) ← NEW
11. [**Part 10: Implementation Checklist**](#part-10-implementation-checklist) ← NEW
12. [**Part 11: Coding Guidelines Reference**](#part-11-coding-guidelines-reference) ← NEW

---

# Part 0: The Game

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
┌─────────────────────────────────────────────────────────────────────┐
│                         CORE GAME LOOP                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│     ┌──────────────┐                                                 │
│     │ Play Activity │ ─── Complete level successfully ───┐           │
│     └──────────────┘                                     │           │
│            ↑                                             ↓           │
│            │                                    ┌──────────────┐     │
│            │                                    │  Earn 1 Coin │     │
│            │                                    └──────────────┘     │
│            │                                             │           │
│            │              NO                             ↓           │
│            └──────────── Have 10+ coins? ◄──────────────┤           │
│                               │ YES                      │           │
│                               ↓                          │ NO        │
│                    ┌────────────────────┐               │           │
│                    │ Trade for YouTube  │               │           │
│                    │ (5min or 10+2min)  │               │           │
│                    └────────────────────┘               │           │
│                               │                          │           │
│                               ↓                          │           │
│                    ┌────────────────────┐               │           │
│                    │    Watch Video     │               │           │
│                    │  (controlled time) │               │           │
│                    └────────────────────┘               │           │
│                               │                          │           │
│                               └──────────────────────────┘           │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 0.3 Activities (Phase 1 - MVP)

| Activity | German Name      | Description          | Sub-Activities                | Status     |
| -------- | ---------------- | -------------------- | ----------------------------- | ---------- |
| Puzzles  | **Rätsel**       | Visual pattern games | Puzzle Matching, Labyrinth    | ✅ In Scope |
| Numbers  | **Zahlen 1,2,3** | Number recognition   | Würfel (Dice), Wähle die Zahl | ✅ In Scope |
| Drawing  | Zeichnen         | *Future phase*       | —                             | 🔒 Locked   |
| Logic    | Logik            | *Future phase*       | —                             | 🔒 Locked   |

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

---

# Part 1: Brand Identity

## 1.1 Brand Essence

### The Soul of Bennie

**One-Line Mission**: *A safe, magical forest where every child succeeds through adventure play.*

**Core Emotional Promise**:
Every interaction feels like a warm hug from a trusted friend that takes the child on a mystical journey. Having fun together and solving activities to earn rewards for great work. Children never feel wrong—only guided toward discovery, with a friend by their side who solves activities together. Because we all love to watch YouTube, right? Yes, we do! But we have to work together to earn it. And activities are so much fun that YouTube time is just around the corner.

### Brand Personality Traits

| Trait         | Expression                                       | Never                                    |
| ------------- | ------------------------------------------------ | ---------------------------------------- |
| **Warm**      | Golden light, soft colors, gentle voices         | Cold blues, harsh whites, sharp sounds   |
| **Patient**   | Unlimited time, gentle hints, no pressure timers | Countdowns, rushing, time stress         |
| **Magical**   | Floating particles, glow effects, wonder         | Realistic, mundane, ordinary             |
| **Playful**   | Bouncy animations, silly Lemminge, celebration   | Serious, competitive, scoring pressure   |
| **Safe**      | Rounded shapes, predictable patterns, soft edges | Sharp corners, surprises, sudden changes |
| **Rewarding** | Clear progress, tangible goals, YouTube payoff   | Vague rewards, empty praise              |

### Brand Tagline

```
Primary:    "Im Wald ist jeder willkommen der gerne Youtube schaut"
            (In the forest, everyone is welcome who likes to watch YouTube)

Internal:   "Where every tap is a triumph"
```

---

## 1.2 The Characters

### 🐻 Bennie der Bär

**Role**: The Gentle Guide (sometimes clumsy)
**Personality**: Patient teacher, big-hearted protector, never frustrated. Also loves to watch YouTube and can't wait to watch together! Let's solve activities so we can watch!

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                           BENNIE - CANONICAL DESIGN                          ║
║                                                                              ║
║              ⛔ NO VEST • NO CLOTHING • NO ACCESSORIES ⛔                    ║
║                                                                              ║
║     This rule is ABSOLUTE. Bennie is a natural bear.                        ║
║     Any generated image showing Bennie with clothing must be rejected.      ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

#### Visual Specifications

| Attribute      | Specification             | Hex/Notes                                |
| -------------- | ------------------------- | ---------------------------------------- |
| **Species**    | Adult brown bear          | NOT teddy bear, NOT cub                  |
| **Body Shape** | Pear-shaped               | Narrow shoulders, wide hips, round belly |
| **Main Fur**   | Warm chocolate brown      | `#8C7259`                                |
| **Snout**      | Lighter tan               | `#C4A574` - ONLY the snout area          |
| **Belly**      | Same as body              | NO separate belly patch                  |
| **Nose**       | Dark espresso triangle    | `#3D2B1F`                                |
| **Eyes**       | Small, round, kind        | Dark brown with white highlight          |
| **Claws**      | Subtle, non-threatening   | Slightly visible, not sharp              |
| **Style**      | Cel-shaded, bold outlines | Clean vector art, flat colors            |

#### Expression States & Asset Names

| State         | Asset Name               | Use Case           | Visual Description                                         |
| ------------- | ------------------------ | ------------------ | ---------------------------------------------------------- |
| `idle`        | `bennie_idle.png`        | Default waiting    | Gentle breathing animation, calm smile, arms at sides      |
| `waving`      | `bennie_waving.png`      | Greeting           | Right paw raised, palm out, friendly smile                 |
| `pointing`    | `bennie_pointing.png`    | Direction/guidance | Left arm extended toward target, looking where pointing    |
| `thinking`    | `bennie_thinking.png`    | Child working      | Paw on chin, eyes looking up and to the side               |
| `encouraging` | `bennie_encouraging.png` | Giving hints       | Leaning forward, soft eyes, open body language             |
| `celebrating` | `bennie_celebrating.png` | Level complete     | Both arms up, jumping pose, big smile, eyes squeezed happy |

#### Bennie's Voice Character

- Warm, like a friendly bear
- Speaks after the narrator
- Appears with a cartoon speech bubble
- Words appear as he speaks
- NO mouth animation (cartoon style)

---

### 🔵 Die Lemminge

**Role**: Playful Troublemakers (a bit impatient to watch YouTube)
**Personality**: Goofy helpers, accident-prone, always friendly. Love to chase with Bennie, but full of love for him. "Lieben es zu necken" (love to tease)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         LEMMINGE - CANONICAL DESIGN                          ║
║                                                                              ║
║         🔵 MUST BE BLUE (#6FA8DC) • NEVER GREEN • NEVER BROWN 🔵             ║
║                                                                              ║
║     Any generated image showing green or brown Lemminge must be rejected.   ║
║     They are inspired by the Go gopher mascot - round, cute, blue.          ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

#### Visual Specifications

| Attribute      | Specification                    | Hex/Notes                               |
| -------------- | -------------------------------- | --------------------------------------- |
| **Shape**      | Round potato blob                | Go gopher mascot style                  |
| **Body Color** | Soft blue                        | `#6FA8DC` — **NON-NEGOTIABLE**          |
| **Belly**      | Cream/white                      | `#FAF5EB` - Fuzzy edge where meets blue |
| **Eyes**       | Large, round, white sclera       | Small dark pupils, expressive           |
| **Teeth**      | Prominent buck teeth             | White, goofy, always visible            |
| **Nose**       | Small, pink                      | `#E8A0A0`                               |
| **Paws**       | Stubby nubs, pink pads           | `#E8A0A0`                               |
| **Ears**       | Two small rounds on top          | Same blue as body                       |
| **Style**      | Cel-shaded, thick black outlines | Flat colors, clean vectors              |

#### Expression States & Asset Names

| State         | Asset Name                 | Use Case            | Visual Description                     |
| ------------- | -------------------------- | ------------------- | -------------------------------------- |
| `idle`        | `lemminge_idle.png`        | Background presence | Gentle swaying, occasional blinking    |
| `curious`     | `lemminge_curious.png`     | Watching child      | Wide eyes, head tilted, ears perked    |
| `excited`     | `lemminge_excited.png`     | Before success      | Bouncing pose, sparkly eyes            |
| `celebrating` | `lemminge_celebrating.png` | After success       | Jumping, arms up, huge smile           |
| `hiding`      | `lemminge_hiding.png`      | Peeking from spots  | Half-hidden, mischievous expression    |
| `mischievous` | `lemminge_mischievous.png` | Creating "chaos"    | Sly grin, squinted eyes, scheming pose |

#### The Character Dynamic

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        THE BENNIE-LEMMINGE DYNAMIC                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Lemminge: "Oops! Wir haben keine Zeit mehr bei Youtube"                   │
│                    ↓                                                        │
│  Bennie: "[Child] kann uns helfen!"                                      │
│                    ↓                                                        │
│  Bennie: "Lass uns mehr Aktivitäten machen damit wir wieder schauen können"
│                    ↓                                                        │
│  Child solves activity → Everyone celebrates → Repeat                       │
│                                                                             │
│  ⚠️ ALWAYS positive. NEVER conflict. NEVER blame.                          │
│  ⚠️ They love to watch YouTube together. Child is awesome!                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 1.3 Color System

### Primary Palette

| Name         | Hex       | RGB           | Usage                       |
| ------------ | --------- | ------------- | --------------------------- |
| **Woodland** | `#738F66` | 115, 143, 102 | Primary buttons, safe areas |
| **Bark**     | `#8C7259` | 140, 114, 89  | Bennie fur, wood elements   |
| **Sky**      | `#B3D1E6` | 179, 209, 230 | Sky areas, calm accents     |
| **Cream**    | `#FAF5EB` | 250, 245, 235 | Backgrounds, safe space     |

### Character Colors

| Name              | Hex       | RGB           | Usage              | Notes              |
| ----------------- | --------- | ------------- | ------------------ | ------------------ |
| **BennieBrown**   | `#8C7259` | 140, 114, 89  | Bennie main fur    | Primary body color |
| **BennieTan**     | `#C4A574` | 196, 165, 116 | Bennie snout       | ONLY snout area    |
| **BennieNose**    | `#3D2B1F` | 61, 43, 31    | Bennie nose        | Dark espresso      |
| **LemmingeBlue**  | `#6FA8DC` | 111, 168, 220 | Lemminge bodies    | **NON-NEGOTIABLE** |
| **LemmingePink**  | `#E8A0A0` | 232, 160, 160 | Lemminge nose/paws | Soft pink          |
| **LemmingeBelly** | `#FAF5EB` | 250, 245, 235 | Lemminge belly     | Same as Cream      |

### UI Colors

| Name            | Hex       | Usage                            |
| --------------- | --------- | -------------------------------- |
| **Success**     | `#99BF8C` | Positive feedback, progress fill |
| **CoinGold**    | `#D9C27A` | Rewards, treasure, coin icons    |
| **Wood Light**  | `#C4A574` | Highlights, top edges of planks  |
| **Wood Medium** | `#A67C52` | Main plank color                 |
| **Wood Dark**   | `#6B4423` | Shadows, grain lines             |
| **Rope**        | `#B8956B` | Sign mounting ropes              |
| **Chain**       | `#6B6B6B` | Lock chains for locked content   |

### Forest Environment Colors

| Layer            | Hex             | Usage                    |
| ---------------- | --------------- | ------------------------ |
| **Far Trees**    | `#4A6B5C`       | Distant misty background |
| **Mid Trees**    | `#738F66`       | Main canopy              |
| **Near Foliage** | `#7A9973`       | Foreground bushes        |
| **Light Rays**   | `#F5E6C8` @ 30% | Golden sunbeams          |
| **Moss**         | `#5D6B4D`       | Ground covering          |
| **Path Stone**   | `#A8A090`       | Labyrinth paths          |

### 🚫 Forbidden Colors

| Color           | Hex       | Why Forbidden                         |
| --------------- | --------- | ------------------------------------- |
| Pure Red        | `#FF0000` | Triggers anxiety in autistic children |
| Pure White      | `#FFFFFF` | Too harsh for large areas             |
| Pure Black      | `#000000` | Too harsh for large areas             |
| Any Neon        | Various   | Overstimulating                       |
| High Saturation | >80%      | Overstimulating                       |
| Green Lemminge  | Any green | Design violation                      |
| Brown Lemminge  | Any brown | Design violation                      |

---

## 1.4 Typography

### Font System

| Use         | Font       | Weight   | Size Range | Notes          |
| ----------- | ---------- | -------- | ---------- | -------------- |
| **Titles**  | SF Rounded | Bold     | 32-48pt    | Screen headers |
| **Body**    | SF Rounded | Regular  | 17-24pt    | Descriptions   |
| **Buttons** | SF Rounded | Semibold | 20-28pt    | All buttons    |
| **Labels**  | SF Rounded | Medium   | 14-17pt    | Small UI text  |
| **Numbers** | SF Rounded | Bold     | 40-72pt    | Game numbers   |

### Language Rules

```
✅ DO:
   • German only - all UI text in German
   • Literal language - no metaphors or idioms
   • Max 7 words per sentence (Narrator & Bennie)
   • Positive framing always
   • Simple, concrete vocabulary
   • Present tense preferred

❌ DON'T:
   • Never say "Falsch" (wrong)
   • Never say "Fehler" (error)
   • Never say "Versuch nochmal" (try again) alone - always add encouragement
   • Never use abstract concepts
   • Never use sarcasm or irony
   • Never use time pressure language
```

### Text Examples

| Situation     | ❌ Wrong            | ✅ Right                                 |
| ------------- | ------------------ | --------------------------------------- |
| Wrong answer  | "Falsch!"          | "Das ist die 5. Wir suchen die 3!"      |
| Timeout       | "Zeit ist um!"     | "Die Uhr ist fertig. Lass uns spielen!" |
| Encouragement | "Streng dich an!"  | "Du schaffst das!"                      |
| Success       | "Endlich richtig!" | "Super gemacht!"                        |

---

# Part 2: Screen Flow & State Machine

## 2.1 Screen Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              COMPLETE GAME FLOW                              │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────┐
    │  LAUNCH  │
    └────┬─────┘
         │
         ▼
┌─────────────────┐
│ LOADING SCREEN  │ ──────► Narrator: "Warte kurz. Wir sind gleich bereit."
│   (0-100%)      │
└────────┬────────┘
         │ 100%
         ▼
┌─────────────────┐
│ PLAYER SELECT   │ ──────► Narrator: "Wie heisst du? Alexander oder Oliver?"
│ [Alex] [Oliver] │
└────────┬────────┘
         │ tap name
         ▼
┌─────────────────┐──────► Narrator: "Was möchtest du spielen?"
│   HOME SCREEN   │ ◄───────────────────────────────────────────┐
│  (Waldabenteuer)│                                             │
│                 │ ──────► Bennie: "Hi [Name], ich bin Bennie" │
│ [Rätsel][Zahlen]│                                             │
│ [🔒][🔒] chest  │                                             │
└───┬─────────┬───┘                                             │
    │         │                                                 │
    │ tap     │ tap                                             │
    ▼         ▼                                                 │
┌───────┐ ┌───────┐                                             │
│RÄTSEL │ │ZAHLEN │  ← Activity Selection Screens               │
│       │ │       │                                             │
│[Puzzle]│ │[Würfel]│                                           │
│[Laby] │ │[Wähle]│                                             │
└───┬───┘ └───┬───┘                                             │
    │         │                                                 │
    ▼         ▼                                                 │
┌─────────────────┐                                             │
│ ACTIVITY SCREEN │  ← Gameplay happens here                    │
│   (gameplay)    │                                             │
└────────┬────────┘                                             │
         │ success                                              │
         ▼                                                      │
    ┌─────────┐                                                 │
    │ +1 COIN │ ──► Coin animation flies to progress bar        │
    └────┬────┘                                                 │
         │                                                      │
         ▼                                                      │
    ╔═══════════╗     NO      ┌────────────┐                   │
    ║ 5 COINS?  ║────────────►│ Next Level │───────────────────┤
    ║ (mod 5=0) ║             └────────────┘                   │
    ╚═════╤═════╝                                               │
          │ YES                                                 │
          ▼                                                     │
┌─────────────────┐                                             │
│   CELEBRATION   │ ──────► Bennie: "Wir haben 5 Goldmünzen!"   │
│    OVERLAY      │         + Confetti + Characters jump        │
│  (transparent)  │                                             │
└────────┬────────┘                                             │
         │ tap "Weiter"                                         │
         ▼                                                      │
    ╔═══════════╗     NO                                        │
    ║ 10 COINS? ║───────────────────────────────────────────────┘
    ╚═════╤═════╝
          │ YES (user can also tap chest anytime when ≥10)
          ▼
┌─────────────────┐
│ TREASURE SCREEN │ ──────► Bennie: "Du kannst YouTube schauen!"
│                 │
│ [5min] [10+2min]│
└────────┬────────┘
         │ tap option (deducts coins)
         ▼
┌─────────────────┐
│ VIDEO SELECTION │ ──────► Shows pre-approved video thumbnails
│  [thumbnails]   │
└────────┬────────┘
         │ tap video
         ▼
┌─────────────────┐
│  VIDEO PLAYER   │ ──────► Analog clock countdown
│  [analog clock] │         1 min warning: "Noch eine Minute."
└────────┬────────┘
         │ time up
         ▼
         └────────────► Bennie: "Die Zeit ist um. Lass uns spielen!"
                        └──────────────────────────────────────────┘
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
| `home`               | tap(chest)       | `treasureScreen`     | Only if coins ≥ 10              |
| `home`               | tap(settings)    | `parentGate`         | Show math question              |
| `parentGate`         | correctAnswer    | `parentDashboard`    | —                               |
| `activitySelection`  | tap(subActivity) | `playing`            | Start activity, play intro      |
| `playing`            | levelSuccess     | `levelComplete`      | +1 coin, success sound          |
| `playing`            | tap(home)        | `home`               | Save progress                   |
| `levelComplete`      | coins % 5 == 0   | `celebrationOverlay` | Celebration audio               |
| `levelComplete`      | coins % 5 != 0   | `playing` (next)     | Auto-advance                    |
| `celebrationOverlay` | tap(weiter)      | Check coins          | —                               |
| `celebrationOverlay` | coins ≥ 10       | `treasureScreen`     | Auto-navigate                   |
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

---

# Part 3: Narrator & Voice Script

## 3.1 Voice System Overview

The game has **two distinct voices**:

| Voice        | Role                                 | Characteristics                   |
| ------------ | ------------------------------------ | --------------------------------- |
| **Narrator** | Sets the scene, gives instructions   | Warm, clear, neutral German       |
| **Bennie**   | Buddy, helper, celebrates with child | Warm, bear-like, excited but calm |

### Voice Priority System

```swift
struct AudioManager {
    // Three independent channels
    var musicChannel: AVAudioPlayer      // Background forest ambience
    var voiceChannel: AVAudioPlayer      // Narrator + Bennie
    var effectsChannel: AVAudioPlayer    // UI sounds, celebrations

    // Default volumes
    var musicVolume: Float = 0.30
    var voiceVolume: Float = 1.00        // Always priority
    var effectsVolume: Float = 0.70

    // Voice ducking: when voice plays, music drops to 15%
    func playVoice(_ file: String, speaker: Speaker) {
        musicChannel.volume = 0.15
        voiceChannel.play(file)

        // On completion, restore music
        voiceChannel.onComplete = {
            self.musicChannel.volume = 0.30
        }
    }
}

enum Speaker {
    case narrator
    case bennie
}
```

---

## 3.2 Narrator Guidelines

| Property            | Value                              |
| ------------------- | ---------------------------------- |
| **Voice Provider**  | ElevenLabs                         |
| **Language**        | German (de-DE)                     |
| **Voice Character** | Warm, clear, adult, neutral gender |
| **Speaking Rate**   | 85% of normal speed                |
| **Max Words**       | 7 words per sentence               |
| **Tone**            | Warm, encouraging, never rushed    |

**Voice Selection**: Pick ONE voice in ElevenLabs and use consistently for all narrator lines. Never change mid-project.

---

## 3.3 Bennie Voice Guidelines

| Property            | Value                                      |
| ------------------- | ------------------------------------------ |
| **Voice Provider**  | ElevenLabs                                 |
| **Language**        | German (de-DE)                             |
| **Voice Character** | Warm, bear-like, friendly, slightly deeper |
| **Speaking Rate**   | 85% of normal speed                        |
| **Max Words**       | 7 words per sentence                       |
| **Tone**            | Excited but calm, buddy-like               |

**Bennie Speech Bubble Implementation**:
- Bennie walks into view
- Cartoon speech bubble appears
- Words appear as audio plays (typewriter style)
- NO mouth animation (cartoon style)

```swift
struct BennieSpeechView: View {
    let message: String
    @State private var displayedText = ""

    var body: some View {
        HStack(alignment: .bottom) {
            // Bennie character
            BennieView(expression: .speaking)

            // Speech bubble
            SpeechBubbleView {
                Text(displayedText)
                    .font(.sfRounded(size: 20, weight: .semibold))
            }
        }
        .onAppear {
            typewriterEffect(fullText: message)
        }
    }

    func typewriterEffect(fullText: String) {
        // Reveal text character by character synced to audio
    }
}
```

---

## 3.4 Complete Script Reference

### Loading Screen

| Speaker  | Trigger       | German                                | English (Reference)           |
| -------- | ------------- | ------------------------------------- | ----------------------------- |
| Narrator | Progress 100% | "Wir sind gleich bereit zum Spielen." | "We're almost ready to play." |

---

### Player Selection Screen

| Speaker  | Trigger          | German                                  | Notes   |
| -------- | ---------------- | --------------------------------------- | ------- |
| Narrator | Screen appears   | "Wie heisst du? Alexander oder Oliver?" | 5 words |
| Narrator | Alexander tapped | "Hallo Alexander! Los geht's!"          | 4 words |
| Narrator | Oliver tapped    | "Hallo Oliver! Los geht's!"             | 4 words |

---

### Home Screen

| Speaker  | Trigger                        | German                                         | Notes   |
| -------- | ------------------------------ | ---------------------------------------------- | ------- |
| Narrator | First visit                    | "Was möchtest du spielen?"                     | 4 words |
| Bennie   | First visit (Part A)           | "Hi [Name], ich bin Bennie!"                   | 5 words |
| Bennie   | First visit (Part B, 2s pause) | "Wir lösen Aktivitäten um YouTube zu schauen." | 7 words |
| Bennie   | Return from activity           | "Lösen wir noch mehr Aktivitäten."             | 5 words |
| Bennie   | After 2s pause                 | "Dann können wir mehr YouTube schauen!"        | 6 words |
| Bennie   | Tap locked activity            | "Das ist noch gesperrt."                       | 4 words |

---

### Rätsel: Puzzle Matching

| Speaker  | Trigger             | German                                | Notes     |
| -------- | ------------------- | ------------------------------------- | --------- |
| Narrator | Activity start      | "Mach das Muster nach!"               | 4 words   |
| Bennie   | Activity start      | "Das packen wir!"                     | 3 words   |
| —        | Correct cell tapped | *Sound effect only*                   | No voice  |
| Both     | Pattern complete    | Random from success pool              | See below |
| Bennie   | 10s no action       | "Wir können das, YouTube kommt bald." | 6 words   |
| Bennie   | 20s no action       | "Welche Farbe fehlt noch?"            | 4 words   |

---

### Rätsel: Labyrinth

| Speaker  | Trigger        | German                        | Notes     |
| -------- | -------------- | ----------------------------- | --------- |
| Narrator | Activity start | "Hilf Bennie den Weg finden!" | 5 words   |
| Bennie   | Activity start | "Wie fange ich die Lemminge?" | 5 words   |
| —        | Path started   | *Sound effect only*           | No voice  |
| Bennie   | Wrong path     | "Da komme ich nicht durch."   | 5 words   |
| Both     | Path complete  | Random from success pool      | See below |
| Bennie   | 15s no action  | "Wo ist der Anfang?"          | 4 words   |

---

### Zahlen: Würfel (Dice)

| Speaker  | Trigger        | German                              | Notes     |
| -------- | -------------- | ----------------------------------- | --------- |
| Narrator | Activity start | "Wirf den Würfel!"                  | 3 words   |
| Narrator | Dice shows N   | "Zeig mir die [N]!"                 | 4 words   |
| Both     | Correct number | Random from success pool            | See below |
| Bennie   | Wrong number   | "Das ist die [X]. Probier nochmal!" | 6 words   |
| Bennie   | 10s no action  | "Zähle die Punkte."                 | 3 words   |
| Bennie   | 20s no action  | "Du hast die [N] gewürfelt."        | 5 words   |
| Bennie   | 30s no action  | "Wo ist die [N]?"                   | 4 words   |

---

### Zahlen: Wähle die Zahl

| Speaker  | Trigger        | German                              | Notes     |
| -------- | -------------- | ----------------------------------- | --------- |
| Narrator | Activity start | "Zeig mir die [N]!"                 | 4 words   |
| Both     | Correct number | Random from success pool            | See below |
| Bennie   | Wrong number   | "Das ist die [X]. Probier nochmal!" | 6 words   |
| Bennie   | 10s no action  | "Der Erzähler hat [N] gesagt."      | 5 words   |
| Bennie   | 20s no action  | "Wo ist die [N]?"                   | 4 words   |

---

### Success Phrase Pool

```swift
let successPhrases = [
    "Super!",                        // 1 word
    "Toll gemacht!",                 // 2 words
    "Wunderbar!",                    // 1 word
    "Ja, genau!",                    // 2 words
    "Das hast du super gemacht!",    // 5 words
    "Perfekt!",                      // 1 word
    "Bravo!"                         // 1 word
]

// Randomly select one per success
func getRandomSuccessPhrase() -> String {
    successPhrases.randomElement()!
}
```

---

### Celebration Overlay

| Speaker | Trigger  | German                                              | Notes   |
| ------- | -------- | --------------------------------------------------- | ------- |
| Bennie  | 5 coins  | "Wir haben schon fünf Goldmünzen!"                  | 5 words |
| Bennie  | 10 coins | "Zehn Goldmünzen! Du kannst jetzt YouTube schauen." | 7 words |
| Bennie  | 15 coins | "Fünfzehn! Weiter so!"                              | 3 words |
| Bennie  | 20 coins | "Zwanzig Münzen! Du bekommst Bonuszeit!"            | 5 words |

---

### Treasure Screen

| Speaker  | Condition          | German                                        | Notes   |
| -------- | ------------------ | --------------------------------------------- | ------- |
| Bennie   | coins < 10         | "Wir haben [X] Münzen. Noch [Y] bis YouTube!" | 7 words |
| Bennie   | coins 10-19        | "Wir können fünf Minuten schauen!"            | 5 words |
| Bennie   | coins ≥ 20         | "Wir können zwölf Minuten schauen!"           | 5 words |
| Narrator | Tap YouTube button | "Film ab!"                                    | 2 words |

---

### Video Player

| Speaker | Trigger            | German                               | Notes   |
| ------- | ------------------ | ------------------------------------ | ------- |
| Bennie  | 1 minute remaining | "Noch eine Minute."                  | 3 words |
| Bennie  | Time up            | "Die Zeit ist um. Lass uns spielen!" | 6 words |

---

# Part 4: Screen Specifications

## 4.0 Shared Components

These components appear on multiple screens and should be implemented ONCE and reused:

### Navigation Header Component

```swift
struct NavigationHeader: View {
    let showHome: Bool
    let showVolume: Bool
    let currentCoins: Int

    var body: some View {
        HStack {
            // Home button (optional)
            if showHome {
                WoodButton(icon: "house", text: "Home") {
                    // Navigate home
                }
            }

            Spacer()

            // Progress bar (always shown in activities)
            ProgressBarView(currentCoins: currentCoins)

            Spacer()

            // Volume toggle
            if showVolume {
                WoodButton(icon: "speaker.wave.2") {
                    // Toggle volume
                }
            }
        }
        .padding(.horizontal, 20)
        .padding(.top, 16)
    }
}
```

### Wood Button Component

```swift
struct WoodButton: View {
    let text: String?
    let icon: String?
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack {
                if let icon = icon {
                    Image(systemName: icon)
                }
                if let text = text {
                    Text(text)
                        .font(.sfRounded(size: 20, weight: .semibold))
                }
            }
            .padding(.horizontal, 20)
            .padding(.vertical, 12)
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .fill(
                        LinearGradient(
                            colors: [Color(hex: "C4A574"), Color(hex: "A67C52")],
                            startPoint: .top,
                            endPoint: .bottom
                        )
                    )
            )
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(Color(hex: "6B4423"), lineWidth: 2)
            )
        }
        .buttonStyle(WoodButtonStyle())
    }
}

struct WoodButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
            .animation(.spring(response: 0.3), value: configuration.isPressed)
    }
}
```

---

## 4.1 Loading Screen

**Reference**: See Image 3 - Forest Loading Screen

### Layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│               ┌───────────────────────────────────────────┐                  │
│               │      🌿 Forest Loading Screen 🌿          │   ← Wood sign   │
│               └───────────────────────────────────────────┘     hanging      │
│                                                                              │
│     ┌─────┐                                              ┌──────┐            │
│     │ 🔵  │     ┌───────────────┐                        │  🔵  │            │
│     └─────┘     │    🐻         │                        └──────┘            │
│   (in log)      │   Bennie      │                       (peeking)            │
│                 │  (idle)       │                                            │
│   ┌──────┐      └───────────────┘      ┌──────┐        ┌──────┐             │
│   │ 🔵   │                             │ 🔵   │        │ 🔵   │             │
│   └──────┘                             └──────┘        └──────┘             │
│  (peeking)                            (curious)       (excited)             │
│                                                                              │
│          🫐╔═══════════════════════════════════════════════════╗ 🍓         │
│             ║▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░║  20%       │
│             ╚═══════════════════════════════════════════════════╝            │
│                        Lade Spielewelt...                                    │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Elements

| Element        | Position           | Size         | Asset                                           |
| -------------- | ------------------ | ------------ | ----------------------------------------------- |
| Title Sign     | Top center         | 400×100pt    | Wood plank with rope mount                      |
| Bennie         | Left of center     | 200×300pt    | `bennie_idle.png` → `bennie_waving.png` at 100% |
| Lemminge (5-6) | Various tree holes | 60×80pt each | `lemminge_hiding.png`, `lemminge_curious.png`   |
| Progress Bar   | Bottom center      | 600×40pt     | Berry-decorated wooden log                      |
| Percentage     | Right of bar       | 24pt         | Current % (synced with bar)                     |
| Loading Text   | Below bar          | 17pt         | "Lade Spielewelt..."                            |

### Behavior

```swift
struct LoadingScreenBehavior {
    // Progress animation:
    // - Each percentage stays visible for ~0.05s
    // - Creates smooth 5-second total load time
    // - Fake loading (actual load is faster)

    func animateProgress() async {
        for percent in 0...100 {
            self.currentPercent = percent
            try? await Task.sleep(nanoseconds: 50_000_000) // 50ms
        }

        // At 100%:
        playNarrator("wir_sind_bereit.aac")

        // Wait for audio, then transition
        try? await Task.sleep(nanoseconds: 2_000_000_000) // 2s
        transitionToPlayerSelection()
    }
}
```

### Voice Trigger

| Trigger         | Speaker  | Audio File             | German                                |
| --------------- | -------- | ---------------------- | ------------------------------------- |
| Progress = 100% | Narrator | `loading_complete.aac` | "Wir sind gleich bereit zum Spielen." |

---

## 4.2 Player Selection Screen

**Reference**: Based on design system

### Layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                         👤   │
│                                                                     (profile)│
│                        Wer spielt heute?                                     │
│                     (Who's playing today?)                                   │
│                                                                              │
│         ┌─────────────────────────┐       ┌─────────────────────────┐       │
│         │    ╭───────────────╮    │       │    ╭───────────────╮    │       │
│         │    │               │    │       │    │               │    │       │
│         │    │   👤 Avatar   │    │       │    │   👤 Avatar   │    │       │
│         │    │               │    │       │    │               │    │       │
│         │    ╰───────────────╯    │       │    ╰───────────────╯    │       │
│         │                         │       │                         │       │
│         │      Alexander          │       │        Oliver           │       │
│         │    🪙 [coin count]      │       │    🪙 [coin count]      │       │
│         └─────────────────────────┘       └─────────────────────────┘       │
│              Wooden sign frame                 Wooden sign frame            │
│                                                                              │
│                       ┌─────────────────────────┐                           │
│                       │       🐻 Bennie         │                           │
│                       │      (waving)           │                           │
│                       └─────────────────────────┘                           │
│                                                                              │
│     ┌──────┐                                                    ┌──────┐    │
│     │ 🔵   │                                                    │ 🔵   │    │
│     │hiding│                                                    │hiding│    │
│     └──────┘                                                    └──────┘    │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Touch Targets (iPad 1194×834)

| Element          | Center X | Center Y | Touch Area |
| ---------------- | -------- | -------- | ---------- |
| Alexander button | 350      | 350      | 200×180pt  |
| Oliver button    | 850      | 350      | 200×180pt  |
| Profile icon     | 1140     | 50       | 60×60pt    |

### Voice Triggers

| Trigger          | Speaker  | German                                  |
| ---------------- | -------- | --------------------------------------- |
| Screen appears   | Narrator | "Wie heisst du? Alexander oder Oliver?" |
| Alexander tapped | Narrator | "Hallo Alexander! Los geht's!"          |
| Oliver tapped    | Narrator | "Hallo Oliver! Los geht's!"             |

---

## 4.3 Home Screen (Waldabenteuer)

**Reference**: See Image 5 - Menu Screen

### Layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│   ┌────────────────────────────────────────────────────────────┐  ┌──┐      │
│   │               🌿 Waldabenteuer 🌿                           │  │👤│      │
│   └────────────────────────────────────────────────────────────┘  └──┘      │
│                                                                    profile   │
│                                                                              │
│    ┌─────────────────────────────┐ ┌─────────────────────────────┐          │
│    │      🔍                     │ │       123                   │          │
│    │    Rätsel                   │ │    Zahlen 1,2,3            │          │
│    │   (glowing - unlocked)      │ │   (chains 🔒 - locked)      │          │
│    └─────────────────────────────┘ └─────────────────────────────┘          │
│     ↑ hanging from branch           ↑ hanging from branch                   │
│                                                                              │
│    ┌─────────────────────────────┐ ┌─────────────────────────────┐          │
│    │    ✏️                        │ │    🧩                        │          │
│    │    Zeichnen                 │ │    Logik                    │          │
│    │   (chains 🔒 - locked)      │ │   (chains 🔒 - locked)      │          │
│    └─────────────────────────────┘ └─────────────────────────────┘          │
│                                                                              │
│    ┌─────────┐                              ┌────┐  ┌────┐                   │
│    │   🔵    │     🐻 (pointing)            │ ⚙️ │  │ ? │    [CHEST]       │
│    │mischief │                              └────┘  └────┘                   │
│    └─────────┘                             settings  help                   │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Activity Signs

| Activity | German         | Default State        | Tap Action                       |
| -------- | -------------- | -------------------- | -------------------------------- |
| Rätsel   | "Rätsel"       | ✅ Unlocked (glowing) | → Activity Selection             |
| Zahlen   | "Zahlen 1,2,3" | ✅ Unlocked (glowing) | → Activity Selection             |
| Zeichnen | "Zeichnen"     | 🔒 Locked (chains)    | Bennie: "Das ist noch gesperrt." |
| Logik    | "Logik"        | 🔒 Locked (chains)    | Bennie: "Das ist noch gesperrt." |

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
| 10-19 | Open            | Golden glow, coins visible | → Treasure Screen          |
| 20+   | Open + sparkles | Extra glow, 2 chest icons  | → Treasure Screen          |

---

## 4.4 Rätsel: Puzzle Matching Screen

**Reference**: See Image 4 - Matching Game Screen

### Layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│   ╭────────╮        ╔═══════════════════════════════════════╗    ╭────────╮ │
│   │  Home  │        ║  Progress Bar with Coin Slots         ║    │   🔊   │ │
│   ╰────────╯        ╚═══════════════════════════════════════╝    ╰────────╯ │
│                                                                              │
│       ╭──────────────────────╮    ➡️    ╭──────────────────────╮            │
│       │       ZIEL           │          │         DU           │            │
│       │   ┌───┬───┬───┐      │          │   ┌───┬───┬───┐      │            │
│       │   │   │🟨 │   │      │          │   │   │🟨 │   │      │            │
│       │   ├───┼───┼───┤      │          │   ├───┼───┼───┤      │            │
│       │   │🟩 │   │   │      │          │   │   │   │   │      │            │
│       │   ├───┼───┼───┤      │          │   ├───┼───┼───┤      │            │
│       │   │🟨 │🟨 │   │      │          │   │   │🟨 │   │      │            │
│       │   └───┴───┴───┘      │          │   └───┴───┴───┘      │            │
│       │      Stone tablet    │          │      Stone tablet    │            │
│       ╰──────────────────────╯          ╰──────────────────────╯            │
│                                                                              │
│   ┌───────┐                                                   ┌───────┐     │
│   │  🔵   │                                                   │  🐻   │     │
│   │curious│                                                   │pointing│    │
│   └───────┘                                                   └───────┘     │
│                                                                              │
│            ┌─────────────────────────────────────────────────────────┐      │
│            │   🟩     🟨     ⬜    │    🧽     🔄                    │      │
│            │  Grün  Gelb   Grau  │  Radierer Neustart              │      │
│            └─────────────────────────────────────────────────────────┘      │
│                    Color palette (wooden log container)                     │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Grid Progression (Adaptive Difficulty)

| Level Range | Grid Size | Colors            | Filled Cells |
| ----------- | --------- | ----------------- | ------------ |
| 1-5         | 3×3       | 2 (green, yellow) | 2-4          |
| 6-10        | 3×3       | 3 (add gray)      | 3-5          |
| 11-20       | 4×4       | 3 colors          | 4-7          |
| 21-30       | 5×5       | 3-4 colors        | 5-10         |
| 31+         | 6×6       | 4 colors          | 6-12         |

### Touch Targets

| Element       | Size            | Behavior                         |
| ------------- | --------------- | -------------------------------- |
| Grid cell     | 96×96pt minimum | Tap to fill with selected color  |
| Color picker  | 80×80pt         | Tap to select color (leaf shape) |
| Eraser button | 60×60pt         | Tap to enable eraser mode        |
| Reset button  | 60×60pt         | Clear entire player grid         |
| Home button   | 96×60pt         | Return to home                   |
| Volume button | 60×60pt         | Toggle sound                     |

### Gameplay Flow

```swift
struct PuzzleMatchingGame {
    // 1. Show target pattern (ZIEL)
    // 2. Player taps colors then cells (DU)
    // 3. Real-time comparison
    // 4. When DU matches ZIEL → Success!

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

**Reference**: See Image 7 - Labyrinth Game Screen

### Layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     ╭─────────────────────────────────╮                      │
│   ╭────────╮        │ Bennie & Lemminge Labyrinth     │        ╭────────╮   │
│   │  Home  │        ╰─────────────────────────────────╯        │   🔊   │   │
│   ╰────────╯              (wooden sign hanging)                ╰────────╯   │
│                                                                              │
│   🐻 (pointing)      START                                                   │
│        ↓               ↓                                                     │
│      🔵           ┌────○═══════════════════════════════○                    │
│    (scared)       │   ╱                                 ╲                    │
│                   │  ○      🏠          🏠         ○──────╮                 │
│                   │   ╲                           ╱       │                 │
│                   │    ○═══════○═══════○═══════○        │                 │
│                   │                                      │      ZIEL       │
│                   └─○════════════════════════════════○───────→ 🔵         │
│                                                              (celebrating)  │
│                                                                              │
│              ╭─────────────────────────────────────╮                        │
│              │    Progress Bar + Coins             │                        │
│              ╰─────────────────────────────────────╯                        │
└──────────────────────────────────────────────────────────────────────────────┘
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

**Reference**: See Image 6 - Numbers Game Screen

### Layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│   ╭────────╮        ╔═══════════════════════════════════════╗    ╭────────╮ │
│   │  Home  │        ║  Progress Bar with Coin Slots         ║    │   🔊   │ │
│   ╰────────╯        ╚═══════════════════════════════════════╝    ╰────────╯ │
│                                                                              │
│                      ╭───────────────────────────────────╮                   │
│                      │                                   │                   │
│           🔵         │   1   2   3   4                   │                   │
│        (curious)     │                                   │                   │
│                      │   5   6   7                       │      🐻           │
│                      │                                   │   (pointing)      │
│           🔵         │   8   9   10                      │                   │
│        (excited)     │                                   │                   │
│                      │      Stone tablet with            │                   │
│                      │      traceable numbers            │                   │
│                      ╰───────────────────────────────────╯                   │
│                                                                              │
│                      ╭─────────────────────────────────────╮                 │
│                      │   🟩     🟨     🧽     🔄          │                 │
│                      │  (color tools for tracing)         │                 │
│                      ╰─────────────────────────────────────╯                 │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Number Tracing System

| Number | Stroke Guide             | Arrow Indicators     |
| ------ | ------------------------ | -------------------- |
| 1      | Single downstroke        | ↓                    |
| 2      | Curve right, down, right | ↷ ↓ →                |
| 3      | Two curves right         | ↷ ↷                  |
| 4      | Down, right, down        | ↓ → ↓                |
| 5      | Down, curve right        | ↓ ↷                  |
| 6      | Curve down and around    | ↶ ○                  |
| 7      | Right, diagonal down     | → ↘                  |
| 8      | Double loop              | ∞                    |
| 9      | Circle, down             | ○ ↓                  |
| 10     | "1" then "0"             | Two separate strokes |

### Gameplay Flow

```
1. Narrator: "Zeig mir die [N]!"
2. Target number glows golden on stone tablet
3. Numbers have arrow guides showing stroke direction
4. Child traces the number with finger
5. Validation: 70% of path followed = success
6. Success → +1 coin, next number (random 1-10)
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

---

## 4.7 Celebration Overlay

**Reference**: Design system celebration specs

### Design Principle

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CELEBRATION IS AN OVERLAY, NOT A SCREEN                   ║
║                                                                              ║
║  This keeps the child grounded in context—they see what they accomplished   ║
║  while receiving praise. No jarring screen transitions.                     ║
║                                                                              ║
║  ✅ Context preservation — Child sees their completed work                   ║
║  ✅ No jarring transitions — Predictable, calm experience                    ║
║  ✅ Immediate feedback — Success feels connected to action                   ║
║  ✅ Autism-friendly — Reduces disorientation from screen changes             ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Trigger Condition

```swift
// ONLY show at 5-coin milestones: 5, 10, 15, 20, 25...
func shouldShowCelebration() -> Bool {
    return player.coins % 5 == 0 && player.coins > 0
}
```

### Layout (Transparent Overlay)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  ┌─ ACTIVITY SCREEN VISIBLE BENEATH (dimmed) ─────────────────────────────┐ │
│  │                                                                        │ │
│  │       ╭─────────────────────────────────────────────────────╮         │ │
│  │       │                                                     │         │ │
│  │       │           ✨ Super gemacht! ✨                       │         │ │
│  │       │                                                     │         │ │
│  │       │                  🪙 +1                               │         │ │
│  │       │                                                     │         │ │
│  │       │              🐻 (celebrating)                       │         │ │
│  │       │          🔵         🔵         🔵                   │         │ │
│  │       │      (jumping)  (jumping)  (jumping)                │         │ │
│  │       │                                                     │         │ │
│  │       │              ╭──────────────────╮                   │         │ │
│  │       │              │    Weiter →      │                   │         │ │
│  │       │              ╰──────────────────╯                   │         │ │
│  │       │                                                     │         │ │
│  │       ╰─────────────────────────────────────────────────────╯         │ │
│  │                                                                        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│                      🎊 Confetti particles over everything 🎊              │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Overlay Properties

| Property                  | Value                                      |
| ------------------------- | ------------------------------------------ |
| Background behind overlay | Activity screen (dimmed to 40% brightness) |
| Overlay background        | `#FAF5EB` @ 90% opacity                    |
| Overlay size              | 70% of screen width                        |
| Corner radius             | 24pt                                       |
| Entry animation           | Scale 0.8→1.0, spring ease, 0.4s           |
| Confetti                  | Full screen, multicolor, 3s duration       |
| Auto-dismiss              | Never (must tap "Weiter")                  |

### Voice per Milestone

| Coins | Bennie Says                                         |
| ----- | --------------------------------------------------- |
| 5     | "Wir haben schon fünf Goldmünzen!"                  |
| 10    | "Zehn Goldmünzen! Du kannst jetzt YouTube schauen." |
| 15    | "Fünfzehn! Weiter so!"                              |
| 20    | "Zwanzig Münzen! Du bekommst Bonuszeit!"            |

---

## 4.8 Treasure Screen

**Reference**: Design system treasure specs

### Layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│   ╭────────╮                                                                 │
│   │ Zurück │                    🪙 12 Münzen                                 │
│   ╰────────╯                    (coin counter)                               │
│                                                                              │
│                     ╭───────────────────────────────────╮                    │
│                     │                                   │                    │
│                     │      💰 Treasure Chest            │                    │
│                     │        (open, glowing)            │                    │
│                     │                                   │                    │
│    🔵  🔵           │     Coins spilling out           │         🐻         │
│   (excited)         ╰───────────────────────────────────╯     (gesturing)    │
│                                                                              │
│    ╭─────────────────────────────╮  ╭─────────────────────────────╮         │
│    │                             │  │                             │         │
│    │  ▶️ 5 Min YouTube           │  │  ▶️ 10+2 Min YouTube        │         │
│    │                             │  │                             │         │
│    │  🪙 10 Münzen               │  │  🪙 20 Münzen (+2 Bonus)   │         │
│    │                             │  │                             │         │
│    │  [Active if ≥10]           │  │  [Active if ≥20]           │         │
│    ╰─────────────────────────────╯  ╰─────────────────────────────╯         │
│                                                                              │
│   🔵                                                               🔵        │
│  (hiding)                                                       (curious)   │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Button States

| Coins | 5 Min Button                 | 10+2 Min Button                          |
| ----- | ---------------------------- | ---------------------------------------- |
| 0-9   | Grayed out, disabled, chains | Grayed out, disabled, chains             |
| 10-19 | **Active**, glowing gold     | Grayed out, disabled                     |
| 20+   | Active                       | **Active**, glowing gold, "BONUS!" badge |

### Voice Triggers

| Condition          | Speaker  | German                                        |
| ------------------ | -------- | --------------------------------------------- |
| coins < 10         | Bennie   | "Wir haben [X] Münzen. Noch [Y] bis YouTube!" |
| coins 10-19        | Bennie   | "Wir können fünf Minuten schauen!"            |
| coins ≥ 20         | Bennie   | "Wir können zwölf Minuten schauen!"           |
| Tap YouTube button | Narrator | "Film ab!"                                    |

### Redemption Logic

```swift
func redeemForYouTube(tier: YouTubeTier) {
    switch tier {
    case .fiveMinutes:
        guard player.coins >= 10 else { return }
        player.coins -= 10
        startYouTubeSession(minutes: 5)

    case .tenPlusTwoMinutes:
        guard player.coins >= 20 else { return }
        player.coins -= 20
        startYouTubeSession(minutes: 12)  // 10 + 2 bonus
    }

    playNarrator("film_ab.aac")
    navigateToVideoSelection()
}
```

---

## 4.9 Video Selection Screen ← NEW

**Reference**: New design specification

### Design Philosophy

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         VIDEO SELECTION PRINCIPLES                           ║
║                                                                              ║
║  🔒 CONTROLLED ENVIRONMENT                                                   ║
║     - Only pre-approved videos from parent dashboard                        ║
║     - NO YouTube search or browsing                                         ║
║     - NO suggested videos or autoplay                                       ║
║     - Child cannot access YouTube directly                                  ║
║                                                                              ║
║  🎯 SIMPLE SELECTION                                                        ║
║     - Large thumbnails (touch-friendly)                                     ║
║     - Video title visible                                                   ║
║     - Maximum 6 videos visible at once                                      ║
║     - Scroll for more (if > 6 approved)                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│   ╭────────╮                                                    ╭────────╮  │
│   │ Zurück │              Wähle ein Video!                      │   🔊   │  │
│   ╰────────╯              (Choose a video!)                     ╰────────╯  │
│                                                                              │
│   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│   │                 │  │                 │  │                 │            │
│   │   [Thumbnail]   │  │   [Thumbnail]   │  │   [Thumbnail]   │            │
│   │                 │  │                 │  │                 │            │
│   │   Peppa Pig     │  │   Paw Patrol    │  │   Feuerwehr-    │            │
│   │   Deutsch       │  │   Deutsch       │  │   mann Sam      │            │
│   │                 │  │                 │  │                 │            │
│   └─────────────────┘  └─────────────────┘  └─────────────────┘            │
│                                                                              │
│   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│   │                 │  │                 │  │                 │            │
│   │   [Thumbnail]   │  │   [Thumbnail]   │  │   [Thumbnail]   │            │
│   │                 │  │                 │  │                 │            │
│   │   Bobo Sieben-  │  │   Conni         │  │   Bibi Block-   │            │
│   │   schläfer      │  │                 │  │   sberg         │            │
│   │                 │  │                 │  │                 │            │
│   └─────────────────┘  └─────────────────┘  └─────────────────┘            │
│                                                                              │
│   🔵 (excited)                                           🐻 (encouraging)   │
│                                                                              │
│              ╭─────────────────────────────────────────╮                    │
│              │    ⏱️ Du hast [X] Minuten Zeit!         │                    │
│              ╰─────────────────────────────────────────╯                    │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Video Thumbnail Card

```swift
struct VideoThumbnailCard: View {
    let video: ApprovedVideo
    let onSelect: () -> Void

    var body: some View {
        Button(action: onSelect) {
            VStack(spacing: 8) {
                // Thumbnail image (cached from YouTube)
                AsyncImage(url: video.thumbnailURL) { image in
                    image
                        .resizable()
                        .aspectRatio(16/9, contentMode: .fill)
                } placeholder: {
                    Rectangle()
                        .fill(Color.gray.opacity(0.3))
                }
                .frame(width: 200, height: 112)
                .cornerRadius(12)

                // Video title (max 2 lines)
                Text(video.title)
                    .font(.sfRounded(size: 16, weight: .medium))
                    .lineLimit(2)
                    .multilineTextAlignment(.center)
            }
            .padding(12)
            .background(
                RoundedRectangle(cornerRadius: 16)
                    .fill(Color(hex: "FAF5EB"))
                    .shadow(radius: 4)
            )
        }
        .buttonStyle(WoodButtonStyle())
    }
}
```

### Technical Implementation: Controlled YouTube Playback

```swift
// CRITICAL: We do NOT use the YouTube app or YouTube website
// We embed YouTube videos directly with our own controls

import YouTubeiOSPlayerHelper

struct ControlledYouTubePlayer: View {
    let videoID: String
    let allowedDuration: TimeInterval

    @State private var playerView: YTPlayerView?
    @State private var remainingTime: TimeInterval

    var body: some View {
        ZStack {
            // YouTube player (no controls, no suggested videos)
            YouTubePlayerView(
                videoID: videoID,
                playerVars: [
                    "controls": 0,           // Hide YouTube controls
                    "rel": 0,                // No related videos
                    "showinfo": 0,           // No video info
                    "modestbranding": 1,     // Minimal YouTube branding
                    "iv_load_policy": 3,     // No annotations
                    "fs": 0,                 // No fullscreen button
                    "disablekb": 1,          // Disable keyboard controls
                    "playsinline": 1         // Play inline
                ]
            )

            // Our overlay controls
            VideoOverlayControls(
                remainingTime: remainingTime,
                onTimeUp: handleTimeUp
            )
        }
        .onAppear {
            startTimer()
        }
    }

    func startTimer() {
        remainingTime = allowedDuration
        // Timer decrements every second
    }

    func handleTimeUp() {
        // Stop video, show message, navigate home
    }
}
```

### Data Model

```swift
struct ApprovedVideo: Codable, Identifiable {
    let id: String           // YouTube video ID
    let title: String        // Display title
    let thumbnailURL: URL    // Cached thumbnail
    let addedAt: Date        // When parent added it
    let category: String?    // Optional category
}

// Stored in parent settings
struct ParentSettings: Codable {
    var approvedVideos: [ApprovedVideo]
    var dailyPlayTimeLimit: [String: Int]  // ["alexander": 60, "oliver": 45]
    var activityLocks: [String: [ActivityType]]  // Per-player locks
}
```

---

## 4.10 Video Player Screen ← NEW

### Layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                        │ │
│  │                                                                        │ │
│  │                                                                        │ │
│  │                      [YOUTUBE VIDEO PLAYER]                           │ │
│  │                                                                        │ │
│  │                      (No YouTube UI visible)                          │ │
│  │                      (Our controls only)                              │ │
│  │                                                                        │ │
│  │                                                                        │ │
│  │                                                                        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│                          ╭─────────────────────╮                            │
│                          │                     │                            │
│                          │    ⏱️ ANALOG CLOCK   │                            │
│                          │    showing time      │                            │
│                          │    remaining         │                            │
│                          │                     │                            │
│                          ╰─────────────────────╯                            │
│                                                                              │
│                        Noch [X] Minuten                                     │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Analog Clock Component

```swift
struct AnalogCountdownClock: View {
    let totalMinutes: Int
    @Binding var remainingSeconds: Int

    var body: some View {
        ZStack {
            // Clock face (wooden texture)
            Circle()
                .fill(Color(hex: "FAF5EB"))
                .overlay(
                    Circle()
                        .stroke(Color(hex: "8C7259"), lineWidth: 8)
                )

            // Minute markers
            ForEach(0..<12) { i in
                Rectangle()
                    .fill(Color(hex: "6B4423"))
                    .frame(width: 2, height: i % 3 == 0 ? 15 : 8)
                    .offset(y: -55)
                    .rotationEffect(.degrees(Double(i) * 30))
            }

            // Remaining time arc (fills counterclockwise)
            Circle()
                .trim(from: 0, to: progress)
                .stroke(
                    Color(hex: "99BF8C"),
                    style: StrokeStyle(lineWidth: 12, lineCap: .round)
                )
                .rotationEffect(.degrees(-90))

            // Clock hand
            Rectangle()
                .fill(Color(hex: "6B4423"))
                .frame(width: 4, height: 45)
                .offset(y: -22)
                .rotationEffect(handRotation)

            // Center dot
            Circle()
                .fill(Color(hex: "D9C27A"))
                .frame(width: 12, height: 12)
        }
        .frame(width: 150, height: 150)
    }

    var progress: CGFloat {
        CGFloat(remainingSeconds) / CGFloat(totalMinutes * 60)
    }

    var handRotation: Angle {
        .degrees(360 * (1 - progress))
    }
}
```

### Time-Up Behavior

```swift
struct VideoPlayerScreen {
    func handleTimeWarning() {
        // At 1 minute remaining
        playBennie("noch_eine_minute.aac")

        // Visual: clock pulses gently
        withAnimation(.easeInOut(duration: 0.5).repeatForever()) {
            clockScale = 1.05
        }
    }

    func handleTimeUp() {
        // Stop video
        youtubePlayer.pause()

        // Play message
        playBennie("zeit_ist_um.aac")

        // Show transition overlay
        showTimeUpOverlay = true

        // After 3 seconds, go to home
        DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
            navigateToHome()
        }
    }
}
```

---

## 4.11 Parent Dashboard ← NEW

### Access Gate (Math Question)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                                                                              │
│                     ╭─────────────────────────────────────╮                  │
│                     │                                     │                  │
│                     │         🔒 Elternbereich            │                  │
│                     │                                     │                  │
│                     │    Bitte löse diese Aufgabe:       │                  │
│                     │                                     │                  │
│                     │         7 + 8 = ?                   │                  │
│                     │                                     │                  │
│                     │    ╭───────────────────────────╮   │                  │
│                     │    │                           │   │                  │
│                     │    │     [Number Input]        │   │                  │
│                     │    │                           │   │                  │
│                     │    ╰───────────────────────────╯   │                  │
│                     │                                     │                  │
│                     │    ╭──────────╮  ╭──────────╮      │                  │
│                     │    │ Abbrechen│  │ Bestätigen│      │                  │
│                     │    ╰──────────╯  ╰──────────╯      │                  │
│                     │                                     │                  │
│                     ╰─────────────────────────────────────╯                  │
│                                                                              │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Math Gate Implementation

```swift
struct ParentGate: View {
    @State private var question: MathQuestion
    @State private var userAnswer: String = ""
    @State private var attempts: Int = 0

    var body: some View {
        VStack(spacing: 24) {
            Text("🔒 Elternbereich")
                .font(.sfRounded(size: 28, weight: .bold))

            Text("Bitte löse diese Aufgabe:")
                .font(.sfRounded(size: 18))

            Text("\(question.a) + \(question.b) = ?")
                .font(.sfRounded(size: 36, weight: .bold))

            TextField("", text: $userAnswer)
                .keyboardType(.numberPad)
                .font(.sfRounded(size: 24))
                .multilineTextAlignment(.center)
                .frame(width: 100)
                .padding()
                .background(Color.white)
                .cornerRadius(12)

            HStack(spacing: 20) {
                Button("Abbrechen") { dismiss() }
                Button("Bestätigen") { checkAnswer() }
            }
        }
    }

    func checkAnswer() {
        if Int(userAnswer) == question.answer {
            navigateToParentDashboard()
        } else {
            attempts += 1
            if attempts >= 3 {
                question = generateNewQuestion()
                attempts = 0
            }
            userAnswer = ""
        }
    }
}

struct MathQuestion {
    let a: Int
    let b: Int
    var answer: Int { a + b }

    static func generate() -> MathQuestion {
        MathQuestion(
            a: Int.random(in: 5...15),
            b: Int.random(in: 5...15)
        )
    }
}
```

### Parent Dashboard Layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│   ╭────────╮                                                                 │
│   │ Zurück │                    ⚙️ Elternbereich                             │
│   ╰────────╯                                                                 │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                         👤 Alexander                                 │   │
│   │  ─────────────────────────────────────────────────────────────────  │   │
│   │  Heute gespielt: 23 min / 60 min                    [████████░░]    │   │
│   │  Münzen: 7                                                          │   │
│   │  Aktivitäten: [Rätsel ✓] [Zahlen ✓] [Zeichnen 🔒] [Logik 🔒]        │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                         👤 Oliver                                    │   │
│   │  ─────────────────────────────────────────────────────────────────  │   │
│   │  Heute gespielt: 45 min / 60 min                    [██████████]    │   │
│   │  Münzen: 12                                                         │   │
│   │  Aktivitäten: [Rätsel ✓] [Zahlen ✓] [Zeichnen 🔒] [Logik 🔒]        │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │  📺 Genehmigte Videos                              [Videos bearbeiten]  │
│   │  ─────────────────────────────────────────────────────────────────  │   │
│   │  • Peppa Pig Deutsch                                                │   │
│   │  • Paw Patrol Deutsch                                               │   │
│   │  • Feuerwehrmann Sam                                                │   │
│   │  • Bobo Siebenschläfer                                              │   │
│   │  [+ Video hinzufügen]                                               │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │  ⏱️ Tägliche Spielzeit                                              │   │
│   │  ─────────────────────────────────────────────────────────────────  │   │
│   │  Alexander: [▼ 60 min ▼]                                            │   │
│   │  Oliver:    [▼ 60 min ▼]                                            │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   ╭──────────────────────────────────╮                                      │
│   │  🗑️ Fortschritt zurücksetzen     │                                      │
│   ╰──────────────────────────────────╯                                      │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Parent Settings Data Model

```swift
struct ParentSettings: Codable {
    // Per-player settings
    var playerSettings: [String: PlayerSettings]

    // Shared settings
    var approvedVideos: [ApprovedVideo]

    struct PlayerSettings: Codable {
        var dailyTimeLimitMinutes: Int = 60
        var unlockedActivities: Set<ActivityType> = [.raetsel, .zahlen]
        var todayPlayedMinutes: Int = 0
        var lastPlayDate: Date?
    }
}

// Approved video management
struct ApprovedVideo: Codable, Identifiable {
    let id: String           // YouTube video ID
    var title: String
    var thumbnailURL: URL
    var addedAt: Date

    // Extract video ID from various YouTube URL formats
    static func extractVideoID(from url: String) -> String? {
        // Handle: youtube.com/watch?v=XXX
        // Handle: youtu.be/XXX
        // Handle: youtube.com/embed/XXX
        // ... URL parsing logic
    }
}
```

### Add Video Flow

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                     ╭─────────────────────────────────────╮                  │
│                     │                                     │                  │
│                     │     📺 Video hinzufügen             │                  │
│                     │                                     │                  │
│                     │   YouTube Link einfügen:            │                  │
│                     │                                     │                  │
│                     │   ╭───────────────────────────────╮ │                  │
│                     │   │ https://youtube.com/watch?... │ │                  │
│                     │   ╰───────────────────────────────╯ │                  │
│                     │                                     │                  │
│                     │   [Einfügen aus Zwischenablage]     │                  │
│                     │                                     │                  │
│                     │   ─────────────────────────────     │                  │
│                     │                                     │                  │
│                     │   Vorschau:                         │                  │
│                     │   ┌─────────────────────────────┐   │                  │
│                     │   │       [Thumbnail]           │   │                  │
│                     │   │       Peppa Pig - Deutsch   │   │                  │
│                     │   └─────────────────────────────┘   │                  │
│                     │                                     │                  │
│                     │   ╭──────────╮  ╭──────────╮       │                  │
│                     │   │ Abbrechen│  │ Hinzufügen│       │                  │
│                     │   ╰──────────╯  ╰──────────╯       │                  │
│                     │                                     │                  │
│                     ╰─────────────────────────────────────╯                  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

# Part 5: Technical Requirements

## 5.1 Platform & Device

| Requirement       | Specification                       |
| ----------------- | ----------------------------------- |
| Platform          | iPadOS 17.0+                        |
| Target Devices    | iPad (10th gen), iPad Air, iPad Pro |
| Screen Resolution | 1194×834 points (landscape)         |
| Orientation       | **Landscape only** (locked)         |
| Framework         | SwiftUI + UIKit hybrid              |

---

## 5.2 Asset Specifications

### Image Assets

| Type        | Format           | Resolution | Notes                             |
| ----------- | ---------------- | ---------- | --------------------------------- |
| Characters  | PNG              | @2x, @3x   | Transparent background            |
| Backgrounds | PNG/JPEG         | @2x, @3x   | Full screen (2388×1668 @2x)       |
| UI Elements | PNG              | @2x, @3x   | Transparent, 9-slice where needed |
| Icons       | SF Symbols + PNG | @2x, @3x   | 96×96pt minimum touch targets     |

### Character Sprite Sizes

| Character | Idle Size | Notes                                 |
| --------- | --------- | ------------------------------------- |
| Bennie    | 300×450pt | All poses same height for consistency |
| Lemminge  | 80×100pt  | Consistent across all expressions     |

### Animation Assets

| Type                | Format      | FPS   | Duration     | Notes                  |
| ------------------- | ----------- | ----- | ------------ | ---------------------- |
| Bennie animations   | Lottie JSON | 30fps | 0.5-2s loops | All expressions        |
| Lemminge animations | Lottie JSON | 30fps | 0.5-1s loops | All expressions        |
| Confetti            | Lottie JSON | 60fps | 3s           | Non-looping            |
| Coin fly            | Lottie JSON | 60fps | 0.8s         | Non-looping            |
| Progress fill       | Lottie JSON | 30fps | 0.5s         | Triggered on coin earn |

---

## 5.3 Audio Specifications

### Audio Formats

| Type             | Format | Sample Rate | Bitrate |
| ---------------- | ------ | ----------- | ------- |
| Narrator voice   | AAC    | 44.1kHz     | 128kbps |
| Bennie voice     | AAC    | 44.1kHz     | 128kbps |
| Sound effects    | AAC    | 44.1kHz     | 128kbps |
| Background music | AAC    | 44.1kHz     | 192kbps |

### Sound Effect Library

| Event          | File Name                 | Duration | Notes               |
| -------------- | ------------------------- | -------- | ------------------- |
| Button tap     | `tap_wood.aac`            | 0.1s     | Wooden knock sound  |
| Correct answer | `success_chime.aac`       | 0.5s     | Gentle bell         |
| Coin earned    | `coin_collect.aac`        | 0.3s     | Metallic clink      |
| Celebration    | `celebration_fanfare.aac` | 2s       | Full fanfare        |
| Chest open     | `chest_open.aac`          | 1s       | Creaky wood         |
| Wrong answer   | `gentle_boop.aac`         | 0.2s     | Soft, not punishing |
| Path trace     | `path_draw.aac`           | Loop     | Soft scratching     |

---

## 5.4 Data Persistence

### Local Storage Structure

```swift
struct PlayerData: Codable {
    var id: String                    // "alexander" or "oliver"
    var coins: Int                    // Current balance
    var totalCoinsEarned: Int         // Lifetime total
    var activityProgress: [String: Int] // Activity -> highest level
    var lastPlayedDate: Date
    var totalPlayTimeToday: TimeInterval
    var videosWatched: [VideoRecord]
    var learningProfile: LearningProfile
}

struct VideoRecord: Codable {
    var videoId: String
    var watchedAt: Date
    var duration: TimeInterval
}

struct AppSettings: Codable {
    var parentSettings: ParentSettings
    var lastActivePlayer: String?
    var audioEnabled: Bool = true
    var musicVolume: Float = 0.3
}
```

---

## 5.5 Offline Behavior

| Feature               | Offline Support     |
| --------------------- | ------------------- |
| All activities        | ✅ Fully offline     |
| Narrator/Bennie audio | ✅ Bundled in app    |
| Progress saving       | ✅ Local storage     |
| YouTube playback      | ❌ Requires internet |
| Parent dashboard      | ✅ Local settings    |

### Offline YouTube Handling

```swift
struct NetworkMonitor {
    static var isConnected: Bool { ... }
}

// In Treasure Screen
if !NetworkMonitor.isConnected {
    // Show friendly message
    playBennie("wir_brauchen_internet.aac")
    // Disable YouTube buttons (grayed out)
    youtubeButtonsEnabled = false
    // Show offline indicator
    showOfflineMessage = true
}
```

---

## 5.6 Performance Requirements

| Metric                          | Target         | Notes                              |
| ------------------------------- | -------------- | ---------------------------------- |
| App launch to Loading Screen    | < 2s           | Cold start                         |
| Loading Screen minimum display  | 2-3s           | UX: children need processing time  |
| Loading Screen to Player Select | 2-5s total     | Min 2s display + actual asset load |
| Screen transitions              | < 0.3s         | Smooth fade/slide                  |
| Touch response                  | < 100ms        | Instant feedback                   |
| Frame rate                      | 60fps constant | No drops during animations         |
| Memory usage                    | < 200MB        | Peak during celebrations           |
| App size                        | < 150MB        | Including all audio                |

---

## 5.7 Accessibility

### VoiceOver Support

| Element          | Accessibility Label (German)          |
| ---------------- | ------------------------------------- |
| Activity buttons | "Rätsel spielen" / "Zahlen spielen"   |
| Grid cells       | "Reihe [N], Spalte [N], [Farbe/leer]" |
| Progress bar     | "[N] von 10 Münzen gesammelt"         |
| Chest            | "Schatzkiste, [N] Münzen"             |
| Video card       | "[Video title], zum Abspielen tippen" |

### Color Blindness Considerations

| Issue                  | Solution                             |
| ---------------------- | ------------------------------------ |
| Green/Yellow confusion | Add shape indicators (circle/square) |
| Progress bar           | Texture pattern in fill              |
| Grid colors            | Different shape overlays per color   |

### Haptic Feedback

| Event          | Haptic Type          |
| -------------- | -------------------- |
| Button tap     | Light impact         |
| Correct answer | Success notification |
| Coin earned    | Medium impact        |
| Wrong answer   | Soft notification    |
| Celebration    | Heavy impact         |

---

# Part 6: Animation & Sound Guide

## 6.1 Animation Principles

| Property      | Value                    | Reason                           |
| ------------- | ------------------------ | -------------------------------- |
| **Duration**  | 0.3-0.5s typical         | Not too fast, not too slow       |
| **Easing**    | Spring (response: 0.3)   | Natural, organic feel            |
| **Breathing** | Scale 1.0→1.03 (2s loop) | Subtle, calming, for idle states |
| **UI hover**  | Gentle swing (0.5s)      | Playful, inviting                |

### 🚫 Forbidden Animations

| Animation           | Reason          |
| ------------------- | --------------- |
| Flashing            | Seizure risk    |
| Shaking             | Anxiety trigger |
| Fast strobing       | Overstimulating |
| Sudden movements    | Startling       |
| Rapid color changes | Disorienting    |
| Bouncing text       | Distracting     |

---

## 6.2 Transition Animations

| Transition       | Animation                  | Duration  |
| ---------------- | -------------------------- | --------- |
| Screen to screen | Cross-fade                 | 0.3s      |
| Overlay appear   | Scale 0.8→1.0 + fade       | 0.4s      |
| Overlay dismiss  | Scale 1.0→0.9 + fade       | 0.3s      |
| Button press     | Scale 0.95                 | 0.1s      |
| Sign swing       | Rotation ±3°               | 0.5s loop |
| Coin fly         | Arc path to progress bar   | 0.8s      |
| Progress fill    | Left to right with sparkle | 0.5s      |

---

## 6.3 Character Animation States

### Bennie Animations

| State       | Animation        | Loop | Trigger       |
| ----------- | ---------------- | ---- | ------------- |
| Idle        | Gentle breathing | Yes  | Default       |
| Waving      | Wave gesture     | No   | Greeting      |
| Pointing    | Arm extend       | No   | Direction     |
| Thinking    | Paw to chin      | Yes  | Child working |
| Encouraging | Lean forward     | No   | Hint given    |
| Celebrating | Jump + arms up   | No   | Success       |

### Lemminge Animations

| State       | Animation    | Loop | Trigger      |
| ----------- | ------------ | ---- | ------------ |
| Idle        | Sway + blink | Yes  | Background   |
| Curious     | Head tilt    | Yes  | Watching     |
| Excited     | Bounce       | Yes  | Pre-success  |
| Celebrating | Jump         | No   | Success      |
| Hiding      | Peek in/out  | Yes  | Tree holes   |
| Mischievous | Scheme pose  | Yes  | Chaos moment |

---

# Part 7: Quick Reference Card

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                        BENNIE UND DIE LEMMINGE                                  │
│                        Quick Design Reference v3.0                              │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  🐻 BENNIE:     #8C7259 (brown) │ NO vest │ Tan snout only (#C4A574)          │
│                                                                                │
│  🔵 LEMMINGE:   #6FA8DC (BLUE!) │ Buck teeth │ White belly │ Pink paws        │
│                 ⚠️ NEVER green │ NEVER brown                                   │
│                                                                                │
│  🪵 WOOD UI:    #C4A574 (light) → #A67C52 (medium) → #6B4423 (dark)           │
│                                                                                │
│  🌲 FOREST:     #738F66 (woodland) │ #B3D1E6 (sky) │ #FAF5EB (cream)         │
│                                                                                │
│  📝 TEXT:       German only │ Max 7 words │ Never "Falsch"                    │
│                                                                                │
│  👆 TOUCH:      >= 96pt │ Single tap only │ No gestures                       │
│                                                                                │
│  🎉 CELEBRATE:  Only at 5-coin milestones (5, 10, 15, 20...)                  │
│                                                                                │
│  📺 YOUTUBE:    Pre-approved only │ Analog clock │ No browsing                │
│                                                                                │
│  🚫 NEVER:      Red, neon, >80% sat │ Flashing │ Pure white/black             │
│                                                                                │
│  🗣️ VOICES:     Narrator (neutral) + Bennie (bear-like) │ ElevenLabs German  │
│                                                                                │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

# Part 8: File Structure

```
BennieGame/
├── App/
│   ├── BennieGameApp.swift
│   └── AppCoordinator.swift
├── Features/
│   ├── Loading/
│   │   └── LoadingView.swift
│   ├── PlayerSelection/
│   │   └── PlayerSelectionView.swift
│   ├── Home/
│   │   └── HomeView.swift
│   ├── Activities/
│   │   ├── Raetsel/
│   │   │   ├── RaetselSelectionView.swift
│   │   │   ├── PuzzleMatchingView.swift
│   │   │   └── LabyrinthView.swift
│   │   └── Zahlen/
│   │       ├── ZahlenSelectionView.swift
│   │       ├── WuerfelView.swift
│   │       └── WaehleZahlView.swift
│   ├── Celebration/
│   │   └── CelebrationOverlay.swift
│   ├── Treasure/
│   │   └── TreasureView.swift
│   ├── Video/
│   │   ├── VideoSelectionView.swift
│   │   └── VideoPlayerView.swift
│   └── Parent/
│       ├── ParentGateView.swift
│       ├── ParentDashboardView.swift
│       └── VideoManagementView.swift
├── Design/
│   ├── Components/
│   │   ├── WoodButton.swift
│   │   ├── WoodSign.swift
│   │   ├── ProgressBar.swift
│   │   ├── NavigationHeader.swift
│   │   ├── StoneTablet.swift
│   │   └── AnalogClock.swift
│   ├── Theme/
│   │   ├── Colors.swift
│   │   └── Typography.swift
│   └── Characters/
│       ├── BennieView.swift
│       ├── LemmingeView.swift
│       └── SpeechBubbleView.swift
├── Services/
│   ├── AudioManager.swift
│   ├── NarratorService.swift
│   ├── GameStateManager.swift
│   ├── PlayerDataStore.swift
│   ├── YouTubeService.swift
│   └── NetworkMonitor.swift
├── Resources/
│   ├── Assets.xcassets/
│   │   ├── Characters/
│   │   │   ├── Bennie/
│   │   │   │   ├── bennie_idle.imageset/
│   │   │   │   ├── bennie_waving.imageset/
│   │   │   │   ├── bennie_pointing.imageset/
│   │   │   │   ├── bennie_thinking.imageset/
│   │   │   │   ├── bennie_encouraging.imageset/
│   │   │   │   └── bennie_celebrating.imageset/
│   │   │   └── Lemminge/
│   │   │       ├── lemminge_idle.imageset/
│   │   │       ├── lemminge_curious.imageset/
│   │   │       ├── lemminge_excited.imageset/
│   │   │       ├── lemminge_celebrating.imageset/
│   │   │       ├── lemminge_hiding.imageset/
│   │   │       └── lemminge_mischievous.imageset/
│   │   ├── Backgrounds/
│   │   └── UI/
│   ├── Lottie/
│   │   ├── bennie_idle.json
│   │   ├── bennie_waving.json
│   │   ├── bennie_celebrating.json
│   │   ├── lemminge_idle.json
│   │   ├── lemminge_celebrating.json
│   │   ├── confetti.json
│   │   ├── coin_fly.json
│   │   └── progress_fill.json
│   └── Audio/
│       ├── Narrator/
│       │   ├── loading_complete.aac
│       │   ├── player_select.aac
│       │   └── ...
│       ├── Bennie/
│       │   ├── greeting.aac
│       │   ├── celebration_5.aac
│       │   └── ...
│       ├── Music/
│       │   └── forest_ambient.aac
│       └── Effects/
│           ├── tap_wood.aac
│           ├── success_chime.aac
│           ├── coin_collect.aac
│           └── ...
└── ParentDashboard/
    ├── ParentGateView.swift
    └── SettingsView.swift
```

---

# Part 9: Asset Production Pipeline ← NEW

This section documents the complete workflow for creating game assets using AI tools.

## 9.1 Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ASSET PRODUCTION PIPELINE                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐                                                        │
│  │ STATIC IMAGES   │                                                        │
│  │ (Characters,    │                                                        │
│  │  Backgrounds)   │                                                        │
│  └────────┬────────┘                                                        │
│           │                                                                 │
│           ▼                                                                 │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐       │
│  │ Gemini Image    │────▶│  Manual QA      │────▶│ Export @2x/@3x  │       │
│  │ Generation      │     │  (Design Check) │     │ PNG assets      │       │
│  └─────────────────┘     └─────────────────┘     └─────────────────┘       │
│                                                                             │
│  ┌─────────────────┐                                                        │
│  │ ANIMATIONS      │                                                        │
│  │ (Character      │                                                        │
│  │  movements)     │                                                        │
│  └────────┬────────┘                                                        │
│           │                                                                 │
│           ▼                                                                 │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐       │
│  │ Static Image    │────▶│  Ludo.ai        │────▶│ Lottie JSON     │       │
│  │ (Base pose)     │     │  Animation      │     │ Export          │       │
│  └─────────────────┘     └─────────────────┘     └─────────────────┘       │
│                                                                             │
│  ┌─────────────────┐                                                        │
│  │ VIDEO CONTENT   │                                                        │
│  │ (Cutscenes,     │                                                        │
│  │  Intros)        │                                                        │
│  └────────┬────────┘                                                        │
│           │                                                                 │
│           ▼                                                                 │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐       │
│  │ Reference       │────▶│  Veo 3.1        │────▶│ Video Edit      │       │
│  │ Images          │     │  Generation     │     │ + Export        │       │
│  └─────────────────┘     └─────────────────┘     └─────────────────┘       │
│                                                                             │
│  ┌─────────────────┐                                                        │
│  │ VOICE/AUDIO     │                                                        │
│  │ (Narrator,      │                                                        │
│  │  Bennie)        │                                                        │
│  └────────┬────────┘                                                        │
│           │                                                                 │
│           ▼                                                                 │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐       │
│  │ Script Text     │────▶│  ElevenLabs     │────▶│ AAC Export      │       │
│  │ (German)        │     │  TTS            │     │ 44.1kHz/128kbps │       │
│  └─────────────────┘     └─────────────────┘     └─────────────────┘       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 9.2 Gemini Image Generation

### Tool: Google AI Studio (Gemini Image Generation)

**Purpose**: Generate all static character images, backgrounds, and UI elements.

### Setup

Use gemini image pro preview API. [ADD THIS CAPABILITIE]

### Prompting Strategy

#### Character Generation Template

```
Generate a [CHARACTER] in the [POSE] pose for a children's game.

CHARACTER SPECIFICATIONS:
- [List all specifications from Part 1.2]
- Style: Cel-shaded, bold outlines, flat colors
- Background: Transparent (for game asset)

POSE DETAILS:
- [Describe the specific pose]
- Expression: [Describe facial expression]
- Arms/Paws position: [Describe]

CRITICAL RULES:
- NO clothing or accessories
- Colors MUST be exact hex values specified
- Clean vector art style
- 16:9 aspect ratio
- High resolution for @3x export
```

#### Bennie Prompt Example

```
Generate Bennie the Bear in the "celebrating" pose for a children's game.

CHARACTER SPECIFICATIONS:
- Adult brown bear, NOT teddy bear, NOT cub
- Pear-shaped body: narrow shoulders, wide hips, round belly
- Main fur color: #8C7259 (warm chocolate brown)
- Snout ONLY lighter tan: #C4A574
- NO separate belly patch - body is uniform brown
- Dark espresso nose: #3D2B1F
- Small, round, kind eyes with white highlight
- Style: Cel-shaded, bold black outlines, flat colors
- Transparent background

POSE DETAILS:
- Both arms raised up high in celebration
- Slight jumping pose (one foot lifted)
- Big smile, eyes squeezed happy
- Body facing forward, slight 3/4 angle

CRITICAL RULES:
⛔ NO vest, NO clothing, NO accessories whatsoever
✅ Clean vector art style
✅ 16:9 aspect ratio
✅ High resolution
```

#### Lemminge Prompt Example

```
Generate a Lemminge character in the "curious" pose for a children's game.

CHARACTER SPECIFICATIONS:
- Round potato blob shape (Go gopher mascot style)
- Body color: #6FA8DC (soft blue) - ABSOLUTELY NOT GREEN OR BROWN
- Belly: #FAF5EB (cream/white) with fuzzy edge transition
- Large round eyes with white sclera, small dark pupils
- Prominent white buck teeth, always visible
- Small pink nose: #E8A0A0
- Stubby pink paw nubs: #E8A0A0
- Two small round ears on top, same blue as body
- Style: Cel-shaded, thick black outlines, flat colors
- Transparent background

POSE DETAILS:
- Head tilted to one side (curious)
- Wide eyes looking at something interesting
- Ears perked up
- Body in standing position, slight lean forward

CRITICAL RULES:
🔵 Body MUST be #6FA8DC blue
❌ NEVER green, NEVER brown, NEVER any other color
✅ Clean vector art style
✅ 16:9 aspect ratio
```

### Quality Assurance Checklist

After generating each image, verify:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         IMAGE QA CHECKLIST                                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  BENNIE:                                                                     ║
║  □ No clothing/vest/accessories?                                             ║
║  □ Fur color is #8C7259 brown (not too dark, not too light)?                ║
║  □ ONLY snout is tan #C4A574?                                                ║
║  □ No separate belly patch?                                                  ║
║  □ Pear-shaped body (narrow shoulders, wide hips)?                          ║
║  □ Adult bear (not cub, not teddy)?                                         ║
║                                                                              ║
║  LEMMINGE:                                                                   ║
║  □ Body is BLUE #6FA8DC?                                                     ║
║  □ NOT green, NOT brown, NOT any other color?                               ║
║  □ Cream belly with fuzzy edge?                                              ║
║  □ Buck teeth visible?                                                       ║
║  □ Pink nose and paws?                                                       ║
║  □ Go gopher style (round blob shape)?                                      ║
║                                                                              ║
║  GENERAL:                                                                    ║
║  □ Transparent background?                                                   ║
║  □ Cel-shaded style with bold outlines?                                     ║
║  □ High resolution (suitable for @3x)?                                      ║
║  □ Correct pose/expression?                                                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 9.3 Ludo.ai Animation Pipeline

### Tool: Ludo.ai (https://ludo.ai)

**Purpose**: Transform static character images into animated Lottie files.

### Workflow

```
Step 1: Upload Base Image
├── Upload the approved static PNG from Gemini
├── Select "Character Animation" mode
└── Define animation region (full character)

Step 2: Define Animation
├── Select animation type:
│   ├── Idle: Breathing, subtle sway
│   ├── Waving: Arm wave gesture
│   ├── Jumping: Vertical bounce
│   └── Custom: Define keyframes
├── Set duration (0.5-2s for loops)
└── Preview animation

Step 3: Refine
├── Adjust easing curves (use "Ease In Out" for organic feel)
├── Set loop behavior (loop for idle, play-once for actions)
└── Preview at 30fps

Step 4: Export
├── Export as Lottie JSON
├── Verify file size (< 100KB ideal)
└── Test in Lottie preview tool
```

### Animation Parameters

| Animation Type | Duration | Loop | Easing      |
| -------------- | -------- | ---- | ----------- |
| Idle breathing | 2.0s     | Yes  | Ease In Out |
| Waving         | 1.5s     | No   | Ease Out    |
| Pointing       | 0.5s     | No   | Ease Out    |
| Thinking       | 2.0s     | Yes  | Ease In Out |
| Celebrating    | 1.0s     | No   | Spring      |
| Hiding (peek)  | 1.5s     | Yes  | Ease In Out |

### Lottie File Naming Convention

```
{character}_{state}.json

Examples:
- bennie_idle.json
- bennie_waving.json
- bennie_celebrating.json
- lemminge_idle.json
- lemminge_curious.json
```

---

## 9.4 ElevenLabs Voice Generation

### Tool: ElevenLabs (https://elevenlabs.io)

**Purpose**: Generate all narrator and Bennie voice lines in German.

### Setup

1. Create account at ElevenLabs
2. Select or clone appropriate German voices:
   - **Narrator**: Warm, clear, neutral adult voice
   - **Bennie**: Slightly deeper, bear-like, friendly

### Voice Selection Criteria

| Voice    | Characteristics             | ElevenLabs Settings               |
| -------- | --------------------------- | --------------------------------- |
| Narrator | Clear, warm, neutral, adult | Stability: 0.75, Similarity: 0.75 |
| Bennie   | Deeper, friendly, bear-like | Stability: 0.65, Similarity: 0.80 |

### Generation Workflow
[USE API]
```
Step 1: Prepare Script
├── Copy German text from Part 3 script tables
├── Add SSML markup if needed for pronunciation
└── Note: Max 7 words per sentence

Step 2: Generate Audio
├── Paste text into ElevenLabs
├── Select appropriate voice (Narrator or Bennie)
├── Set speaking rate to 85% (-15% from default)
├── Generate audio
└── Preview and verify pronunciation

Step 3: Export & Process
├── Download as MP3
├── Convert to AAC:
│   ffmpeg -i input.mp3 -c:a aac -b:a 128k output.aac
├── Verify sample rate: 44.1kHz
└── Name file according to convention
```

### Audio File Naming Convention

```
{speaker}_{screen}_{trigger}.aac

Examples:
- narrator_loading_complete.aac
- narrator_player_select_question.aac
- bennie_home_greeting_part1.aac
- bennie_celebration_5coins.aac
- bennie_hint_puzzle_10s.aac
```

### Complete Voice Line Checklist

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         VOICE LINE CHECKLIST                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  LOADING SCREEN:                                                             ║
║  □ narrator_loading_complete.aac                                             ║
║                                                                              ║
║  PLAYER SELECTION:                                                           ║
║  □ narrator_player_question.aac                                              ║
║  □ narrator_hello_alexander.aac                                              ║
║  □ narrator_hello_oliver.aac                                                 ║
║                                                                              ║
║  HOME SCREEN:                                                                ║
║  □ narrator_home_question.aac                                                ║
║  □ bennie_greeting_part1.aac                                                 ║
║  □ bennie_greeting_part2.aac                                                 ║
║  □ bennie_return_part1.aac                                                   ║
║  □ bennie_return_part2.aac                                                   ║
║  □ bennie_locked.aac                                                         ║
║                                                                              ║
║  PUZZLE MATCHING:                                                            ║
║  □ narrator_puzzle_start.aac                                                 ║
║  □ bennie_puzzle_start.aac                                                   ║
║  □ bennie_puzzle_hint_10s.aac                                                ║
║  □ bennie_puzzle_hint_20s.aac                                                ║
║                                                                              ║
║  LABYRINTH:                                                                  ║
║  □ narrator_labyrinth_start.aac                                              ║
║  □ bennie_labyrinth_start.aac                                                ║
║  □ bennie_labyrinth_wrong.aac                                                ║
║  □ bennie_labyrinth_hint.aac                                                 ║
║                                                                              ║
║  ZAHLEN (DICE):                                                              ║
║  □ narrator_dice_start.aac                                                   ║
║  □ narrator_show_number_[1-6].aac (6 files)                                 ║
║  □ bennie_wrong_number.aac                                                   ║
║  □ bennie_dice_hint_[10s/20s/30s].aac (3 files)                             ║
║                                                                              ║
║  ZAHLEN (CHOOSE):                                                            ║
║  □ narrator_choose_number_[1-10].aac (10 files)                             ║
║  □ bennie_wrong_choose.aac                                                   ║
║  □ bennie_choose_hint_[10s/20s].aac (2 files)                               ║
║                                                                              ║
║  SUCCESS POOL (shared):                                                      ║
║  □ success_super.aac                                                         ║
║  □ success_toll.aac                                                          ║
║  □ success_wunderbar.aac                                                     ║
║  □ success_genau.aac                                                         ║
║  □ success_super_gemacht.aac                                                 ║
║                                                                              ║
║  CELEBRATION:                                                                ║
║  □ bennie_celebration_5.aac                                                  ║
║  □ bennie_celebration_10.aac                                                 ║
║  □ bennie_celebration_15.aac                                                 ║
║  □ bennie_celebration_20.aac                                                 ║
║                                                                              ║
║  TREASURE:                                                                   ║
║  □ bennie_treasure_under10.aac                                               ║
║  □ bennie_treasure_over10.aac                                                ║
║  □ bennie_treasure_over20.aac                                                ║
║  □ narrator_film_ab.aac                                                      ║
║                                                                              ║
║  VIDEO PLAYER:                                                               ║
║  □ bennie_video_1min.aac                                                     ║
║  □ bennie_video_timeup.aac                                                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 9.5 Veo 3.1 Video Generation (Optional)

### Tool: Google Veo 3.1

**Purpose**: Generate video content for cutscenes or promotional material.

### Use Cases

| Use Case      | Description                     |
| ------------- | ------------------------------- |
| Intro video   | Game launch cinematic           |
| Tutorial demo | Animated gameplay demonstration |
| Promotional   | App Store preview video         |

### Workflow

```
Step 1: Prepare Reference Images
├── Use approved Gemini-generated character images
├── Create storyboard of video sequence
└── Note key frames needed

Step 2: Generate Video
├── Upload reference images to Veo
├── Describe motion/animation in prompt:
│   "Bennie the brown bear walks from left to right,
│    waving at the camera. Forest background.
│    Friendly, warm lighting. Animation style. Add German what he speaks: "Lass das Abenteuer beginnen"
├── Set duration (4-8 seconds per clip)
└── Generate and review

Step 3: Post-Processing
├── Review for design compliance
├── Edit clips together if needed
├── Add audio track
└── Export in appropriate format

Step 4: Export Settings
├── Resolution: 1920x1080 (16:9)
├── Frame rate: 30fps
├── Format: H.264 MP4
└── Audio: AAC
```

### Quality Checklist for Video

```
□ Character designs match static images exactly?
□ No unwanted clothing or accessories added?
□ Lemminge are BLUE, not green or brown?
□ Animation is smooth (no jarring movements)?
□ Appropriate for autism-friendly audience?
□ No flashing or rapid movements?
```

---

## 9.6 MCP Tools Reference

### bennie-image-generator MCP

| Tool                     | Purpose                              | Example                                                                             |
| ------------------------ | ------------------------------------ | ----------------------------------------------------------------------------------- |
| `generate_image`         | Create character/scene images        | `generate_image(prompt="Bennie waving", character="bennie", category="characters")` |
| `generate_ab_comparison` | Create A/B variations for review     | `generate_ab_comparison(prompt="Lemminge celebrating", name="lemming-celebrate")`   |
| `record_feedback`        | Record style preferences             | `record_feedback(pattern="softer edges", score=3, source="review-001")`             |
| `get_learnings`          | Retrieve accumulated style learnings | `get_learnings()`                                                                   |

### game-screen-designer MCP

| Tool         | Purpose                         | Example                                                                    |
| ------------ | ------------------------------- | -------------------------------------------------------------------------- |
| `list_refs`  | List available reference images | `list_refs()`                                                              |
| `get_colors` | Get Bennie color palette        | `get_colors()`                                                             |
| `generate`   | Generate screen mockup          | `generate(prompt="Home screen with 4 activity signs", ref1="menu_screen")` |

### bennie-files MCP

| Tool             | Purpose            | Example                                                 |
| ---------------- | ------------------ | ------------------------------------------------------- |
| `read_file`      | Read project files | `read_file(path="/project/CLAUDE.md")`                  |
| `write_file`     | Write/update files | `write_file(path="/project/assets/...", content="...")` |
| `list_directory` | Browse folders     | `list_directory(path="/project/public/images/")`        |

---

## 9.7 Asset Export Specifications

### Image Export

| Asset Type  | Format   | Sizes    | Notes                  |
| ----------- | -------- | -------- | ---------------------- |
| Characters  | PNG      | @2x, @3x | Transparent background |
| Backgrounds | PNG/JPEG | @2x, @3x | Full bleed             |
| UI elements | PNG      | @2x, @3x | 9-slice compatible     |

### Resolution Table

| Size                 | @1x      | @2x       | @3x       |
| -------------------- | -------- | --------- | --------- |
| Character (Bennie)   | 150×225  | 300×450   | 450×675   |
| Character (Lemminge) | 40×50    | 80×100    | 120×150   |
| Button               | 48×30    | 96×60     | 144×90    |
| Background           | 1194×834 | 2388×1668 | 3582×2502 |

### Lottie Export

| Setting          | Value                     |
| ---------------- | ------------------------- |
| Format           | JSON                      |
| FPS              | 30 (idle) or 60 (effects) |
| File size target | < 100KB                   |
| Compression      | Enabled                   |

### Audio Export

| Setting     | Value                            |
| ----------- | -------------------------------- |
| Format      | AAC                              |
| Sample rate | 44.1kHz                          |
| Bitrate     | 128kbps (voice), 192kbps (music) |
| Channels    | Stereo                           |

---

# Part 10: Implementation Checklist ← NEW

## 10.1 Development Phase Checklist

### Phase 1: Setup

```
□ Create Xcode project with SwiftUI
□ Configure for iPad landscape only
□ Set up file structure per Part 8
□ Configure asset catalogs
□ Install dependencies:
  □ Lottie-iOS
  □ YouTubeiOSPlayerHelper (or custom implementation)
```

### Phase 2: Design System

```
□ Implement Colors.swift with all hex values
□ Implement Typography.swift with SF Rounded
□ Create WoodButton component
□ Create WoodSign component
□ Create ProgressBar component
□ Create NavigationHeader component
□ Create StoneTablet component
□ Create AnalogClock component
□ Create SpeechBubble component
□ Create BennieView with all expressions
□ Create LemmingeView with all expressions
```

### Phase 3: Core Screens

```
□ LoadingView
  □ Progress bar animation
  □ Bennie idle animation
  □ Lemminge peek animations
  □ Voice trigger at 100%

□ PlayerSelectionView
  □ Player cards with coin counts
  □ Bennie waving
  □ Voice interaction

□ HomeView
  □ Activity signs (4)
  □ Lock/unlock states
  □ Chest component
  □ Settings/help buttons
  □ Bennie pointing
  □ Lemminge hiding
```

### Phase 4: Activities

```
□ PuzzleMatchingView
  □ Dual grid display (ZIEL / DU)
  □ Color picker
  □ Pattern validation
  □ Difficulty progression
  □ Voice hints

□ LabyrinthView
  □ Path rendering
  □ Touch tracking
  □ Path validation
  □ Start/Goal markers

□ WuerfelView
  □ Dice animation
  □ Number buttons
  □ Voice prompts

□ WaehleZahlView
  □ Number tracing
  □ Trace validation
  □ Voice prompts
```

### Phase 5: Reward System

```
□ CelebrationOverlay
  □ Transparent overlay design
  □ Confetti animation
  □ Character celebrations
  □ Milestone messages

□ TreasureView
  □ Chest visualization
  □ YouTube buttons
  □ Coin counter
  □ Button states

□ VideoSelectionView
  □ Thumbnail grid
  □ Pre-approved videos only
  □ Time display

□ VideoPlayerView
  □ Controlled YouTube embed
  □ Analog clock countdown
  □ Time warnings
  □ Auto-exit on time up
```

### Phase 6: Parent Features

```
□ ParentGateView
  □ Math question generation
  □ Answer validation

□ ParentDashboardView
  □ Per-player settings
  □ Time tracking display
  □ Activity lock toggles

□ VideoManagementView
  □ Add video by URL
  □ Remove videos
  □ Thumbnail preview
```

### Phase 7: Audio Integration

```
□ AudioManager
  □ Three-channel system
  □ Voice ducking
  □ Volume controls

□ NarratorService
  □ Voice line playback
  □ Queue management

□ Import all voice files (see Part 9.4 checklist)
□ Import all sound effects
□ Import background music
```

### Phase 8: Testing

```
□ Touch target verification (≥96pt)
□ Color verification against hex values
□ Animation smoothness (60fps)
□ Voice timing verification
□ Offline mode testing
□ Progress persistence testing
□ Accessibility testing (VoiceOver)
 Play each acitivity without warning, error, bug until you reach 100 coins. Have agent fix all mistakes and restart. we need one clean run of 100 points including watching 100 min of youtube successfully.
```

---

## 10.2 Asset Production Checklist

### Character Images

```
BENNIE:
□ bennie_idle.png (@2x, @3x)
□ bennie_waving.png (@2x, @3x)
□ bennie_pointing.png (@2x, @3x)
□ bennie_thinking.png (@2x, @3x)
□ bennie_encouraging.png (@2x, @3x)
□ bennie_celebrating.png (@2x, @3x)

LEMMINGE:
□ lemminge_idle.png (@2x, @3x)
□ lemminge_curious.png (@2x, @3x)
□ lemminge_excited.png (@2x, @3x)
□ lemminge_celebrating.png (@2x, @3x)
□ lemminge_hiding.png (@2x, @3x)
□ lemminge_mischievous.png (@2x, @3x)
```

### Lottie Animations

```
□ bennie_idle.json
□ bennie_waving.json
□ bennie_celebrating.json
□ lemminge_idle.json
□ lemminge_celebrating.json
□ confetti.json
□ coin_fly.json
□ progress_fill.json
```

### Audio Files

```
See complete checklist in Part 9.4
```

---

## 10.3 QA Verification Matrix

| Screen           | Touch | Colors | Animation | Voice | Accessibility |
| ---------------- | ----- | ------ | --------- | ----- | ------------- |
| Loading          | □     | □      | □         | □     | □             |
| Player Select    | □     | □      | □         | □     | □             |
| Home             | □     | □      | □         | □     | □             |
| Puzzle           | □     | □      | □         | □     | □             |
| Labyrinth        | □     | □      | □         | □     | □             |
| Würfel           | □     | □      | □         | □     | □             |
| Wähle Zahl       | □     | □      | □         | □     | □             |
| Celebration      | □     | □      | □         | □     | □             |
| Treasure         | □     | □      | □         | □     | □             |
| Video Select     | □     | □      | □         | □     | □             |
| Video Player     | □     | □      | □         | □     | □             |
| Parent Gate      | □     | □      | □         | □     | □             |
| Parent Dashboard | □     | □      | □         | □     | □             |

---

# Part 11: Coding Guidelines Reference

## 11.1 Companion Document

This playbook has a companion technical document:

**📄 SWIFTUI_CODING_GUIDELINES.md**

The coding guidelines provide:
- Complete SwiftUI code implementations for every component
- Copy-paste ready code blocks for Claude Code
- Memory management patterns (200MB target)
- Touch target enforcement (96pt minimum)
- Color system as Swift enum
- Animation presets matching this playbook
- QA checklist for every PR

## 11.2 How to Use Together

| Document | Purpose | Audience |
|----------|---------|----------|
| **BENNIE_BRAND_PLAYBOOK_v3_1.md** | Design specs, screens, flow, assets | Designers, PM, QA |
| **SWIFTUI_CODING_GUIDELINES.md** | Implementation code, patterns | Claude Code, Developers |

### For Claude Code:

```
When implementing screens:
1. Read PLAYBOOK for design specs and behavior
2. Read CODING_GUIDELINES for exact code patterns
3. Use ONLY BennieColors enum values
4. Use ONLY BennieFont enum values
5. Use ONLY BennieAnimation presets
6. Enforce 96pt minimum touch targets
```

## 11.3 Critical Rules (Both Documents)

These rules appear in BOTH documents because they are **NON-NEGOTIABLE**:

| Rule | Violation Impact |
|------|------------------|
| Touch targets ≥ 96pt | Children can't tap, frustration |
| Bennie NO clothing | Character inconsistency |
| Lemminge BLUE #6FA8DC | Character inconsistency |
| German only UI | Children confusion |
| No "Falsch"/"Fehler" | Psychological harm |
| No flashing/shaking | Seizure/anxiety risk |
| No red #FF0000 | Overstimulation |

---

*Document Version: 3.1*
*Created: January 2026*
*For: Bennie und die Lemminge - iPad App*
*Target Audience: Alexander (5) & Oliver (4)*
*Development Team Reference Document*
