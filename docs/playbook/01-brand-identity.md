# Part 1: Brand Identity

> **Chapter 1** of the Bennie Brand Playbook
>
> Covers: Characters, colors, typography, language rules

---

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

### Bennie der Bär

**Role**: The Gentle Guide (sometimes clumsy)
**Personality**: Patient teacher, big-hearted protector, never frustrated. Also loves to watch YouTube and can't wait to watch together! Let's solve activities so we can watch!

```
+------------------------------------------------------------------------------+
|                           BENNIE - CANONICAL DESIGN                          |
|                                                                              |
|              NO VEST - NO CLOTHING - NO ACCESSORIES - EVER                   |
|                                                                              |
|     This rule is ABSOLUTE. Bennie is a natural bear.                        |
|     Any generated image showing Bennie with clothing must be rejected.      |
+------------------------------------------------------------------------------+
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

### Die Lemminge

**Role**: Playful Troublemakers (a bit impatient to watch YouTube)
**Personality**: Goofy helpers, accident-prone, always friendly. Love to chase with Bennie, but full of love for him. "Lieben es zu necken" (love to tease)

```
+------------------------------------------------------------------------------+
|                         LEMMINGE - CANONICAL DESIGN                          |
|                                                                              |
|         MUST BE BLUE (#6FA8DC) - NEVER GREEN - NEVER BROWN                   |
|                                                                              |
|     Any generated image showing green or brown Lemminge must be rejected.   |
|     They are inspired by the Go gopher mascot - round, cute, blue.          |
+------------------------------------------------------------------------------+
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
+-----------------------------------------------------------------------------+
|                        THE BENNIE-LEMMINGE DYNAMIC                          |
+-----------------------------------------------------------------------------+
|                                                                             |
|  Lemminge: "Oops! Wir haben keine Zeit mehr bei Youtube"                   |
|                    |                                                        |
|  Bennie: "[Child] kann uns helfen!"                                        |
|                    |                                                        |
|  Bennie: "Lass uns mehr Aktivitäten machen damit wir wieder schauen können"|
|                    |                                                        |
|  Child solves activity -> Everyone celebrates -> Repeat                     |
|                                                                             |
|  ALWAYS positive. NEVER conflict. NEVER blame.                              |
|  They love to watch YouTube together. Child is awesome!                     |
|                                                                             |
+-----------------------------------------------------------------------------+
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

### Forbidden Colors

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
DO:
   - German only - all UI text in German
   - Literal language - no metaphors or idioms
   - Max 7 words per sentence (Narrator & Bennie)
   - Positive framing always
   - Simple, concrete vocabulary
   - Present tense preferred

DON'T:
   - Never say "Falsch" (wrong)
   - Never say "Fehler" (error)
   - Never say "Versuch nochmal" (try again) alone - always add encouragement
   - Never use abstract concepts
   - Never use sarcasm or irony
   - Never use time pressure language
```

### Text Examples

| Situation     | Wrong              | Right                                   |
| ------------- | ------------------ | --------------------------------------- |
| Wrong answer  | "Falsch!"          | "Das ist die 5. Wir suchen die 3!"      |
| Timeout       | "Zeit ist um!"     | "Die Uhr ist fertig. Lass uns spielen!" |
| Encouragement | "Streng dich an!"  | "Du schaffst das!"                      |
| Success       | "Endlich richtig!" | "Super gemacht!"                        |
