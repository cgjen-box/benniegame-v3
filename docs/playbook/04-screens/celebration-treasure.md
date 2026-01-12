# 4.7-4.8 Celebration & Treasure Screens

> Part of [Screen Specifications](README.md)

---

## 4.7 Celebration Overlay

### Layout

```
+------------------------------------------------------------------------------+
|                                                                              |
|  +------------------------------------------------------------------------+  |
|  | +---------------------------------------------------------------------+ | |
|  | |                                                                     | | |
|  | |       +-----------------------------------------+                   | | |
|  | |       |        Celebration Overlay              |                   | | |
|  | |       |        (rounded wood frame)             |                   | | |
|  | |       |                                         |                   | | |
|  | |       |      "Wir haben 5 Goldmünzen!"         |                   | | |
|  | |       |                                         |                   | | |
|  | |       |              Bennie (celebrating)       |                   | | |
|  | |       |          L         L         L          |                   | | |
|  | |       |      (jumping)  (jumping)  (jumping)    |                   | | |
|  | |       |                                         |                   | | |
|  | |       |              +----------------+         |                   | | |
|  | |       |              |    Weiter ->   |         |                   | | |
|  | |       |              +----------------+         |                   | | |
|  | |       |                                         |                   | | |
|  | |       +-----------------------------------------+                   | | |
|  | |                                                                     | | |
|  | +---------------------------------------------------------------------+ | |
|  |                                                                        | |
|  +------------------------------------------------------------------------+  |
|                                                                              |
|                      Confetti particles over everything                      |
|                                                                              |
+------------------------------------------------------------------------------+
```

### Overlay Properties

| Property                  | Value                                      |
| ------------------------- | ------------------------------------------ |
| Background behind overlay | Activity screen (dimmed to 40% brightness) |
| Overlay background        | `#FAF5EB` @ 90% opacity                    |
| Overlay size              | 70% of screen width                        |
| Corner radius             | 24pt                                       |
| Entry animation           | Scale 0.8->1.0, spring ease, 0.4s          |
| Confetti                  | Full screen, multicolor, 3s duration       |
| Auto-dismiss              | Never (must tap "Weiter")                  |

### Voice per Milestone

| Coins | Bennie Says                                         |
| ----- | --------------------------------------------------- |
| 5     | "Wir haben schon fünf Goldmünzen!"                  |
| 10    | "Zehn Goldmünzen! Du kannst jetzt YouTube schauen." |
| 15    | "Fünfzehn! Weiter so!"                              |
| 20    | "Zwanzig Münzen! Du bekommst Bonuszeit!"            |

### Celebration Implementation

```swift
struct CelebrationOverlay: View {
    let coins: Int
    let onContinue: () -> Void

    @State private var showConfetti = false
    @State private var scale: CGFloat = 0.8

    var body: some View {
        ZStack {
            // Dimmed background
            Color.black.opacity(0.6)

            // Celebration card
            VStack(spacing: 24) {
                Text(celebrationMessage)
                    .font(.sfRounded(size: 28, weight: .bold))

                // Characters celebrating
                HStack {
                    BennieView(expression: .celebrating)
                    ForEach(0..<3) { _ in
                        LemmingeView(expression: .celebrating)
                    }
                }

                // Continue button
                WoodButton(text: "Weiter") {
                    onContinue()
                }
            }
            .padding(32)
            .background(
                RoundedRectangle(cornerRadius: 24)
                    .fill(Color(hex: "FAF5EB").opacity(0.9))
            )
            .scaleEffect(scale)

            // Confetti overlay
            if showConfetti {
                ConfettiView()
            }
        }
        .onAppear {
            withAnimation(.spring(response: 0.4)) {
                scale = 1.0
            }
            showConfetti = true
            playCelebrationVoice()
        }
    }

    var celebrationMessage: String {
        switch coins {
        case 5: return "Wir haben schon fünf Goldmünzen!"
        case 10: return "Zehn Goldmünzen! Du kannst jetzt YouTube schauen."
        case 15: return "Fünfzehn! Weiter so!"
        case 20: return "Zwanzig Münzen! Du bekommst Bonuszeit!"
        default: return "Toll gemacht!"
        }
    }
}
```

---

## 4.8 Treasure Screen

### Layout

```
+------------------------------------------------------------------------------+
|   +--------+                                                                 |
|   | Zurück |                    Coin [12 Münzen]                             |
|   +--------+                    (coin counter)                               |
|                                                                              |
|                     +-----------------------------------+                    |
|                     |                                   |                    |
|                     |      Treasure Chest               |                    |
|                     |        (open, glowing)            |                    |
|                     |                                   |                    |
|    L  L             |     Coins spilling out           |         Bennie     |
|   (excited)         +-----------------------------------+     (gesturing)    |
|                                                                              |
|    +-----------------------------+  +-----------------------------+         |
|    |                             |  |                             |         |
|    |  Play 5 Min YouTube         |  |  Play 10+2 Min YouTube      |         |
|    |                             |  |                             |         |
|    |  Coin 10 Münzen             |  |  Coin 20 Münzen (+2 Bonus)  |         |
|    |                             |  |                             |         |
|    |  [Active if >=10]           |  |  [Active if >=20]           |         |
|    +-----------------------------+  +-----------------------------+         |
|                                                                              |
|   L                                                               L          |
|  (hiding)                                                       (curious)   |
+------------------------------------------------------------------------------+
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
| coins >= 20        | Bennie   | "Wir können zwölf Minuten schauen!"           |
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

### Treasure Chest Animation

```swift
struct TreasureChestView: View {
    let coins: Int

    @State private var isOpen: Bool

    var body: some View {
        ZStack {
            // Chest base
            Image(isOpen ? "chest_open" : "chest_closed")
                .resizable()
                .frame(width: 200, height: 180)

            // Golden glow for active state
            if coins >= 10 {
                Circle()
                    .fill(Color(hex: "D9C27A").opacity(0.3))
                    .frame(width: 250, height: 250)
                    .blur(radius: 20)
            }

            // Coins spilling effect
            if isOpen {
                CoinsSpillingAnimation()
            }
        }
        .onAppear {
            isOpen = coins >= 10
        }
    }
}
```
