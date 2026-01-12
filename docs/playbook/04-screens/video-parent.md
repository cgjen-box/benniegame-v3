# 4.9-4.11 Video & Parent Dashboard

> Part of [Screen Specifications](README.md)

---

## 4.9 Video Selection Screen

### Design Philosophy

```
+------------------------------------------------------------------------------+
|                         VIDEO SELECTION PRINCIPLES                           |
|                                                                              |
|  CONTROLLED ENVIRONMENT                                                      |
|     - Only pre-approved videos from parent dashboard                        |
|     - NO YouTube search or browsing                                         |
|     - NO suggested videos or autoplay                                       |
|     - Child cannot access YouTube directly                                  |
|                                                                              |
|  SIMPLE SELECTION                                                           |
|     - Large thumbnails (touch-friendly)                                     |
|     - Video title visible                                                   |
|     - Maximum 6 videos visible at once                                      |
|     - Scroll for more (if > 6 approved)                                     |
+------------------------------------------------------------------------------+
```

### Layout

```
+------------------------------------------------------------------------------+
|   +--------+              Wähle ein Video!                      +--------+  |
|   | Zurück |              (Choose a video!)                     | Volume |  |
|   +--------+                                                    +--------+  |
|                                                                              |
|   +-----------------+  +-----------------+  +-----------------+            |
|   |                 |  |                 |  |                 |            |
|   |   [Thumbnail]   |  |   [Thumbnail]   |  |   [Thumbnail]   |            |
|   |                 |  |                 |  |                 |            |
|   |   Peppa Pig     |  |   Paw Patrol    |  |   Feuerwehr-    |            |
|   |   Deutsch       |  |   Deutsch       |  |   mann Sam      |            |
|   |                 |  |                 |  |                 |            |
|   +-----------------+  +-----------------+  +-----------------+            |
|                                                                              |
|   +-----------------+  +-----------------+  +-----------------+            |
|   |                 |  |                 |  |                 |            |
|   |   [Thumbnail]   |  |   [Thumbnail]   |  |   [Thumbnail]   |            |
|   |                 |  |                 |  |                 |            |
|   |   Bobo Sieben-  |  |   Conni         |  |   Bibi Block-   |            |
|   |   schläfer      |  |                 |  |   sberg         |            |
|   |                 |  |                 |  |                 |            |
|   +-----------------+  +-----------------+  +-----------------+            |
|                                                                              |
|   L (excited)                                           Bennie (encouraging) |
|                                                                              |
|              +---------------------------------------------+                |
|              |    Clock: Du hast [X] Minuten Zeit!         |                |
|              +---------------------------------------------+                |
+------------------------------------------------------------------------------+
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

## 4.10 Video Player Screen

### Layout

```
+------------------------------------------------------------------------------+
|                                                                              |
|  +------------------------------------------------------------------------+  |
|  |                                                                        |  |
|  |                                                                        |  |
|  |                                                                        |  |
|  |                      [YOUTUBE VIDEO PLAYER]                           |  |
|  |                                                                        |  |
|  |                      (No YouTube UI visible)                          |  |
|  |                      (Our controls only)                              |  |
|  |                                                                        |  |
|  |                                                                        |  |
|  |                                                                        |  |
|  +------------------------------------------------------------------------+  |
|                                                                              |
|                          +---------------------+                            |
|                          |                     |                            |
|                          |    ANALOG CLOCK     |                            |
|                          |    showing time     |                            |
|                          |    remaining        |                            |
|                          |                     |                            |
|                          +---------------------+                            |
|                                                                              |
|                        Noch [X] Minuten                                     |
|                                                                              |
+------------------------------------------------------------------------------+
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

## 4.11 Parent Dashboard

### Access Gate (Math Question)

```
+------------------------------------------------------------------------------+
|                                                                              |
|                                                                              |
|                     +-------------------------------------+                  |
|                     |                                     |                  |
|                     |         Lock Elternbereich          |                  |
|                     |                                     |                  |
|                     |    Bitte löse diese Aufgabe:       |                  |
|                     |                                     |                  |
|                     |         7 + 8 = ?                   |                  |
|                     |                                     |                  |
|                     |    +---------------------------+   |                  |
|                     |    |                           |   |                  |
|                     |    |     [Number Input]        |   |                  |
|                     |    |                           |   |                  |
|                     |    +---------------------------+   |                  |
|                     |                                     |                  |
|                     |    +----------+  +------------+    |                  |
|                     |    | Abbrechen|  | Bestätigen |    |                  |
|                     |    +----------+  +------------+    |                  |
|                     |                                     |                  |
|                     +-------------------------------------+                  |
|                                                                              |
|                                                                              |
+------------------------------------------------------------------------------+
```

### Math Gate Implementation

```swift
struct ParentGate: View {
    @State private var question: MathQuestion
    @State private var userAnswer: String = ""
    @State private var attempts: Int = 0

    var body: some View {
        VStack(spacing: 24) {
            Text("Elternbereich")
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
+------------------------------------------------------------------------------+
|   +--------+                                                                 |
|   | Zurück |                    Cog Elternbereich                            |
|   +--------+                                                                 |
|                                                                              |
|   +---------------------------------------------------------------------+   |
|   |                         Person Alexander                             |   |
|   |  ----------------------------------------------------------------   |   |
|   |  Heute gespielt: 23 min / 60 min                    [====-----]    |   |
|   |  Münzen: 7                                                          |   |
|   |  Aktivitäten: [Rätsel Y] [Zahlen Y] [Zeichnen Lock] [Logik Lock]   |   |
|   +---------------------------------------------------------------------+   |
|                                                                              |
|   +---------------------------------------------------------------------+   |
|   |                         Person Oliver                                |   |
|   |  ----------------------------------------------------------------   |   |
|   |  Heute gespielt: 45 min / 60 min                    [=========]    |   |
|   |  Münzen: 12                                                         |   |
|   |  Aktivitäten: [Rätsel Y] [Zahlen Y] [Zeichnen Lock] [Logik Lock]   |   |
|   +---------------------------------------------------------------------+   |
|                                                                              |
|   +---------------------------------------------------------------------+   |
|   |  TV Genehmigte Videos                              [Videos bearbeiten]  |
|   |  ----------------------------------------------------------------   |   |
|   |  - Peppa Pig Deutsch                                                |   |
|   |  - Paw Patrol Deutsch                                               |   |
|   |  - Feuerwehrmann Sam                                                |   |
|   |  - Bobo Siebenschläfer                                              |   |
|   |  [+ Video hinzufügen]                                               |   |
|   +---------------------------------------------------------------------+   |
|                                                                              |
|   +---------------------------------------------------------------------+   |
|   |  Clock Tägliche Spielzeit                                           |   |
|   |  ----------------------------------------------------------------   |   |
|   |  Alexander: [v 60 min v]                                            |   |
|   |  Oliver:    [v 60 min v]                                            |   |
|   +---------------------------------------------------------------------+   |
|                                                                              |
|   +----------------------------------+                                      |
|   |  Trash Fortschritt zurücksetzen  |                                      |
|   +----------------------------------+                                      |
+------------------------------------------------------------------------------+
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
+------------------------------------------------------------------------------+
|                                                                              |
|                     +-------------------------------------+                  |
|                     |                                     |                  |
|                     |     TV Video hinzufügen             |                  |
|                     |                                     |                  |
|                     |   YouTube Link einfügen:            |                  |
|                     |                                     |                  |
|                     |   +-----------------------------+   |                  |
|                     |   | https://youtube.com/watch?...|   |                  |
|                     |   +-----------------------------+   |                  |
|                     |                                     |                  |
|                     |   [Einfügen aus Zwischenablage]     |                  |
|                     |                                     |                  |
|                     |   -----------------------------     |                  |
|                     |                                     |                  |
|                     |   Vorschau:                         |                  |
|                     |   +-----------------------------+   |                  |
|                     |   |       [Thumbnail]           |   |                  |
|                     |   |       Peppa Pig - Deutsch   |   |                  |
|                     |   +-----------------------------+   |                  |
|                     |                                     |                  |
|                     |   +----------+  +------------+     |                  |
|                     |   | Abbrechen|  | Hinzufügen |     |                  |
|                     |   +----------+  +------------+     |                  |
|                     |                                     |                  |
|                     +-------------------------------------+                  |
|                                                                              |
+------------------------------------------------------------------------------+
```
