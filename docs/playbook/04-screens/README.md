# Part 4: Screen Specifications

> **Chapter 4** of the Bennie Brand Playbook
>
> This chapter is split into multiple files for manageability.

---

## Sub-Files

| Section | File | Contents |
|---------|------|----------|
| 4.0 | This file | Shared components overview |
| 4.1-4.2 | [loading-player.md](loading-player.md) | Loading screen, Player selection |
| 4.3-4.6 | [home-activities.md](home-activities.md) | Home, Puzzle, Labyrinth, Numbers |
| 4.7-4.8 | [celebration-treasure.md](celebration-treasure.md) | Celebration overlay, Treasure screen |
| 4.9-4.11 | [video-parent.md](video-parent.md) | Video selection, Video player, Parent dashboard |

---

## 4.0 Shared Components

These components appear on multiple screens and should be implemented ONCE and reused.

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

### Screen Coordinates (iPad 1194x834)

| Element | Center X | Center Y | Touch Area |
|---------|----------|----------|------------|
| Alexander button | 400 | 350 | 200x180pt |
| Oliver button | 800 | 350 | 200x180pt |
| Rätsel | 300 | 400 | 180x150pt |
| Zahlen | 500 | 400 | 180x150pt |
| Logik | 700 | 400 | 180x150pt |
| Zeichnen | 900 | 400 | 180x150pt |
| Treasure chest | 1050 | 700 | 120x120pt |
| Back/Home | 60 | 50 | 96x60pt |
| Settings | 1134 | 50 | 60x60pt |

### Touch Target Requirements

| Element       | Minimum Size    | Notes                         |
| ------------- | --------------- | ----------------------------- |
| Buttons       | 96x96pt         | All interactive elements      |
| Grid cells    | 96x96pt         | Activity game boards          |
| Color picker  | 80x80pt         | Palette selection             |
| Navigation    | 96x60pt         | Home, back buttons            |
