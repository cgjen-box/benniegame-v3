# 4.1-4.2 Loading & Player Selection Screens

> Part of [Screen Specifications](README.md)

---

## 4.1 Loading Screen

### Layout

```
+------------------------------------------------------------------------------+
|                                                                              |
|               +-------------------------------------------+                  |
|               |      Forest Loading Screen                |   <- Wood sign   |
|               +-------------------------------------------+     hanging      |
|                                                                              |
|     +-----+                                              +------+            |
|     | L   |     +---------------+                        |  L   |            |
|     +-----+     |    Bennie     |                        +------+            |
|   (in log)      |   (idle)      |                       (peeking)            |
|                 +---------------+                                            |
|   +------+                             +------+        +------+             |
|   | L    |                             | L    |        | L    |             |
|   +------+                             +------+        +------+             |
|  (peeking)                            (curious)       (excited)             |
|                                                                              |
|          +===================================================+ Berry        |
|             |XXXXXXXXXXXXXXX                                 |  20%         |
|          +===================================================+              |
|                        Lade Spielewelt...                                    |
+------------------------------------------------------------------------------+
```

### Elements

| Element        | Position           | Size         | Asset                                           |
| -------------- | ------------------ | ------------ | ----------------------------------------------- |
| Title Sign     | Top center         | 400x100pt    | Wood plank with rope mount                      |
| Bennie         | Left of center     | 200x300pt    | `bennie_idle.png` -> `bennie_waving.png` at 100% |
| Lemminge (5-6) | Various tree holes | 60x80pt each | `lemminge_hiding.png`, `lemminge_curious.png`   |
| Progress Bar   | Bottom center      | 600x40pt     | Berry-decorated wooden log                      |
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

### Layout

```
+------------------------------------------------------------------------------+
|                                                                         P    |
|                                                                     (profile)|
|                        Wer spielt heute?                                     |
|                     (Who's playing today?)                                   |
|                                                                              |
|         +-------------------------+       +-------------------------+       |
|         |    +---------------+    |       |    +---------------+    |       |
|         |    |               |    |       |    |               |    |       |
|         |    |   Avatar      |    |       |    |   Avatar      |    |       |
|         |    |               |    |       |    |               |    |       |
|         |    +---------------+    |       |    +---------------+    |       |
|         |                         |       |                         |       |
|         |      Alexander          |       |        Oliver           |       |
|         |    Coin [coin count]    |       |    Coin [coin count]    |       |
|         +-------------------------+       +-------------------------+       |
|              Wooden sign frame                 Wooden sign frame            |
|                                                                              |
|                       +-------------------------+                           |
|                       |       Bennie            |                           |
|                       |      (waving)           |                           |
|                       +-------------------------+                           |
|                                                                              |
|     +------+                                                    +------+    |
|     | L    |                                                    | L    |    |
|     |hiding|                                                    |hiding|    |
|     +------+                                                    +------+    |
+------------------------------------------------------------------------------+
```

### Touch Targets (iPad 1194x834)

| Element          | Center X | Center Y | Touch Area |
| ---------------- | -------- | -------- | ---------- |
| Alexander button | 400      | 350      | 200x180pt  |
| Oliver button    | 800      | 350      | 200x180pt  |
| Profile icon     | 1140     | 50       | 60x60pt    |

### Voice Triggers

| Trigger          | Speaker  | German                                  |
| ---------------- | -------- | --------------------------------------- |
| Screen appears   | Narrator | "Wie heisst du? Alexander oder Oliver?" |
| Alexander tapped | Narrator | "Hallo Alexander! Los geht's!"          |
| Oliver tapped    | Narrator | "Hallo Oliver! Los geht's!"             |

### Player Card Design

```swift
struct PlayerCard: View {
    let player: Player
    let onSelect: () -> Void

    var body: some View {
        Button(action: onSelect) {
            VStack(spacing: 12) {
                // Avatar circle
                Circle()
                    .fill(Color(hex: "FAF5EB"))
                    .frame(width: 120, height: 120)
                    .overlay(
                        Image("avatar_\(player.id)")
                            .resizable()
                            .scaledToFit()
                    )

                // Name
                Text(player.name)
                    .font(.sfRounded(size: 24, weight: .bold))

                // Coin count
                HStack {
                    Image("coin_icon")
                        .resizable()
                        .frame(width: 24, height: 24)
                    Text("\(player.coins)")
                        .font(.sfRounded(size: 18, weight: .medium))
                }
            }
            .padding(24)
            .background(
                WoodPanelBackground()
            )
        }
        .buttonStyle(WoodButtonStyle())
        .frame(minWidth: 200, minHeight: 180)
    }
}
```
