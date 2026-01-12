# Part 5: Technical Requirements

> **Chapter 5** of the Bennie Brand Playbook
>
> Covers: Platform specs, asset requirements, audio, data persistence, performance

---

## 5.1 Platform & Device

| Requirement       | Specification                       |
| ----------------- | ----------------------------------- |
| Platform          | iPadOS 17.0+                        |
| Target Devices    | iPad (10th gen), iPad Air, iPad Pro |
| Screen Resolution | 1194x834 points (landscape)         |
| Orientation       | **Landscape only** (locked)         |
| Framework         | SwiftUI + UIKit hybrid              |

---

## 5.2 Asset Specifications

### Image Assets

| Type        | Format           | Resolution | Notes                             |
| ----------- | ---------------- | ---------- | --------------------------------- |
| Characters  | PNG              | @2x, @3x   | Transparent background            |
| Backgrounds | PNG/JPEG         | @2x, @3x   | Full screen (2388x1668 @2x)       |
| UI Elements | PNG              | @2x, @3x   | Transparent, 9-slice where needed |
| Icons       | SF Symbols + PNG | @2x, @3x   | 96x96pt minimum touch targets     |

### Character Sprite Sizes

| Character | Idle Size | Notes                                 |
| --------- | --------- | ------------------------------------- |
| Bennie    | 300x450pt | All poses same height for consistency |
| Lemminge  | 80x100pt  | Consistent across all expressions     |

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
| All activities        | Fully offline       |
| Narrator/Bennie audio | Bundled in app      |
| Progress saving       | Local storage       |
| YouTube playback      | Requires internet   |
| Parent dashboard      | Local settings      |

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
