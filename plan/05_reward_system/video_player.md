# Video Player Implementation

**📚 Playbook Reference**: [FULL_ARCHIVE.md Parts 4.9 & 4.10](../../docs/playbook/FULL_ARCHIVE.md#49-video-selection-screen--410-video-player-screen)  
**🎨 Design Reference**: Design screens for video selection and player (to be created)  
**🐻 Character Assets Required**:
- [bennie_excited.png](../../design/references/character/bennie/bennie_excited.png) - Bennie for video selection
- [lemminge_excited.png](../../design/references/character/lemminge/lemminge_excited.png) - Excited Lemminge

**🧩 Component Dependencies**:
- [NavigationHeader](../../Design/Components/NavigationHeader.swift) - With back button and volume
- [WoodButton](../../Design/Components/WoodButton.swift) - For video cards
- [AnalogClock](../../Design/Components/AnalogClock.swift) - Countdown clock
- [BennieView](../../Design/Characters/BennieView.swift) - Character display
- [LemmingeView](../../Design/Characters/LemmingeView.swift) - Character display

**🔊 Audio Files Required**:
- `bennie_video_1min.aac` - "Noch eine Minute."
- `bennie_video_timeup.aac` - "Die Zeit ist um. Lass uns spielen!"
- `bennie_video_greeting.aac` - "Wähle ein Video!"

**📦 External Dependencies**:
- YouTube iOS Player Helper (or custom iframe implementation)
- Network monitoring for offline detection

---

## 🎬 Overview

The video player system consists of two screens:
1. **Video Selection Screen** - Choose from pre-approved videos
2. **Video Player Screen** - Controlled YouTube playback with analog clock countdown

> **CRITICAL**: Playbook Part 4.9 - Design Philosophy
> - Only pre-approved videos from parent dashboard
> - NO YouTube search or browsing
> - NO suggested videos or autoplay
> - Child cannot access YouTube directly

## Part 1: Video Selection Screen

> **Playbook Reference**: Part 4.9 - Video Selection Screen
> **Design Philosophy**: Part 4.9 - Controlled Environment

### Data Model

```swift
// Playbook Part 4.9 - Data Model
struct ApprovedVideo: Codable, Identifiable {
    let id: String           // YouTube video ID
    let title: String        // Display title
    let thumbnailURL: URL    // Cached thumbnail
    let addedAt: Date        // When parent added it
    let category: String?    // Optional category
}

struct ParentSettings: Codable {
    var approvedVideos: [ApprovedVideo]
    var dailyPlayTimeLimit: [String: Int]  // ["alexander": 60, "oliver": 45]
    var activityLocks: [String: [ActivityType]]
}
```

### Screen Layout

> **Playbook Reference**: Part 4.9 - Layout diagram

```swift
struct VideoSelectionView: View {
    let allowedDuration: Int // 5 or 12 minutes
    @StateObject private var videoManager = VideoManager.shared
    @State private var selectedVideo: ApprovedVideo? = nil
    
    var body: some View {
        ZStack {
            // Forest background
            ForestBackground(style: .standard)
            
            VStack {
                // Header
                NavigationHeader(
                    showHome: true,
                    showVolume: true,
                    currentCoins: CoinManager.shared.currentCoins
                )
                
                // Title
                Text("Wähle ein Video!")
                    .font(.sfRounded(size: 32, weight: .bold))
                    .foregroundColor(BennieColors.bark)
                    .padding(.top, 20)
                
                // Video grid (3 columns, 2 rows = 6 videos visible)
                // Playbook: "Maximum 6 videos visible at once, scroll for more"
                ScrollView {
                    LazyVGrid(
                        columns: [
                            GridItem(.flexible(), spacing: 40),
                            GridItem(.flexible(), spacing: 40),
                            GridItem(.flexible(), spacing: 40)
                        ],
                        spacing: 40
                    ) {
                        ForEach(videoManager.approvedVideos) { video in
                            VideoThumbnailCard(
                                video: video,
                                onSelect: {
                                    selectedVideo = video
                                    navigateToPlayer()
                                }
                            )
                        }
                    }
                    .padding(.horizontal, 60)
                }
                
                // Time indicator
                TimeIndicatorBanner(minutes: allowedDuration)
                    .padding(.bottom, 20)
                
                // Characters
                HStack {
                    LemmingeView(expression: .excited)
                        .frame(width: 80, height: 100)
                    
                    Spacer()
                    
                    BennieView(expression: .encouraging)
                        .frame(width: 200, height: 300)
                }
                .padding(.horizontal, 60)
            }
        }
        .onAppear {
            AudioManager.shared.playBennie("bennie_video_greeting.aac")
        }
    }
    
    func navigateToPlayer() {
        guard let video = selectedVideo else { return }
        
        NavigationCoordinator.shared.navigate(
            to: .videoPlayer(
                videoID: video.id,
                duration: allowedDuration
            )
        )
    }
}
```

### Video Thumbnail Card

> **Playbook Reference**: Part 4.9 - Video Thumbnail Card component

```swift
struct VideoThumbnailCard: View {
    let video: ApprovedVideo
    let onSelect: () -> Void
    
    var body: some View {
        Button(action: onSelect) {
            VStack(spacing: 8) {
                // Thumbnail image (cached from YouTube)
                // Playbook: "AsyncImage with 16:9 aspect ratio"
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
                    .foregroundColor(BennieColors.bark)
                    .lineLimit(2)
                    .multilineTextAlignment(.center)
                    .frame(height: 40)
            }
            .padding(12)
            .background(
                RoundedRectangle(cornerRadius: 16)
                    .fill(BennieColors.cream)
                    .shadow(color: Color.black.opacity(0.1), radius: 4, x: 0, y: 2)
            )
        }
        .buttonStyle(WoodButtonStyle())
        // Playbook Part 5.7 - Accessibility
        .accessibilityLabel("\(video.title), zum Abspielen tippen")
    }
}

struct TimeIndicatorBanner: View {
    let minutes: Int
    
    var body: some View {
        HStack(spacing: 8) {
            Image(systemName: "clock.fill")
                .foregroundColor(BennieColors.bark)
            
            Text("Du hast \(minutes) Minuten Zeit!")
                .font(.sfRounded(size: 20, weight: .semibold))
                .foregroundColor(BennieColors.bark)
        }
        .padding(.horizontal, 24)
        .padding(.vertical, 12)
        .background(
            Capsule()
                .fill(BennieColors.cream)
                .shadow(radius: 4)
        )
    }
}
```

### Offline Detection

> **Playbook Reference**: Part 5.5 - Offline YouTube Handling

```swift
struct NetworkMonitor: ObservableObject {
    @Published var isConnected: Bool = true
    
    static let shared = NetworkMonitor()
    
    // Monitor network changes
    func startMonitoring() {
        // Implementation using Network framework
    }
}

// Usage in VideoSelectionView
.onAppear {
    if !NetworkMonitor.shared.isConnected {
        showOfflineAlert()
    }
}

func showOfflineAlert() {
    // Playbook: "Show friendly message, disable YouTube buttons"
    AudioManager.shared.playBennie("wir_brauchen_internet.aac")
    // Show offline indicator overlay
}
```

## Part 2: Video Player Screen

> **Playbook Reference**: Part 4.10 - Video Player Screen
> **Critical Implementation**: Part 4.9 - Controlled YouTube Playback

### Controlled YouTube Embed

**CRITICAL**: We do NOT use the YouTube app or YouTube website. We embed YouTube videos directly with our own controls.

```swift
import YouTubeiOSPlayerHelper

struct VideoPlayerView: View {
    let videoID: String
    let allowedDuration: TimeInterval // in seconds (5min = 300s, 12min = 720s)
    
    @State private var remainingTime: TimeInterval
    @State private var hasShownOneMinuteWarning = false
    @Environment(\.dismiss) var dismiss
    
    init(videoID: String, duration: Int) {
        self.videoID = videoID
        self.allowedDuration = TimeInterval(duration * 60) // Convert to seconds
        self._remainingTime = State(initialValue: TimeInterval(duration * 60))
    }
    
    var body: some View {
        ZStack {
            // Black background
            Color.black
                .ignoresSafeArea()
            
            VStack(spacing: 0) {
                // YouTube player (no controls)
                // Playbook Part 4.9: "No YouTube controls, no suggested videos"
                ControlledYouTubePlayer(
                    videoID: videoID,
                    onReady: startTimer
                )
                .frame(maxWidth: .infinity)
                .aspectRatio(16/9, contentMode: .fit)
                
                Spacer()
                
                // Analog clock countdown
                // Playbook Part 4.10: "Analog clock showing time remaining"
                AnalogCountdownClock(
                    totalMinutes: Int(allowedDuration / 60),
                    remainingSeconds: $remainingTime
                )
                .padding(.vertical, 40)
                
                // Time remaining text
                Text("Noch \(formatTime(remainingTime))")
                    .font(.sfRounded(size: 24, weight: .semibold))
                    .foregroundColor(.white)
                    .padding(.bottom, 40)
                
                Spacer()
            }
        }
        .navigationBarHidden(true)
        .onDisappear {
            stopTimer()
        }
    }
    
    // Timer management
    private var timer: Timer?
    
    func startTimer() {
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
            if remainingTime > 0 {
                remainingTime -= 1
                
                // One minute warning
                // Playbook Part 4.10: "1 min warning: 'Noch eine Minute.'"
                if remainingTime == 60 && !hasShownOneMinuteWarning {
                    AudioManager.shared.playBennie("bennie_video_1min.aac")
                    hasShownOneMinuteWarning = true
                    
                    // Visual: clock pulses gently
                    withAnimation(.easeInOut(duration: 0.5).repeatCount(3)) {
                        // Clock scale animation
                    }
                }
                
                // Time up
                if remainingTime <= 0 {
                    handleTimeUp()
                }
            }
        }
    }
    
    func stopTimer() {
        timer?.invalidate()
        timer = nil
    }
    
    func handleTimeUp() {
        // Playbook Part 4.10: Time-Up Behavior
        
        // Stop video
        // (YouTube player stop method)
        
        // Play message
        AudioManager.shared.playBennie("bennie_video_timeup.aac")
        
        // Show transition overlay
        showTimeUpOverlay = true
        
        // After 3 seconds, go to home
        DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
            NavigationCoordinator.shared.navigateToHome()
        }
    }
    
    func formatTime(_ seconds: TimeInterval) -> String {
        let mins = Int(seconds) / 60
        let secs = Int(seconds) % 60
        return String(format: "%d:%02d", mins, secs)
    }
}
```

### Controlled YouTube Player Component

> **Playbook Reference**: Part 4.9 - Technical Implementation: Controlled YouTube Playback

```swift
struct ControlledYouTubePlayer: UIViewRepresentable {
    let videoID: String
    let onReady: () -> Void
    
    func makeUIView(context: Context) -> YTPlayerView {
        let playerView = YTPlayerView()
        
        // Playbook Part 4.9: Player configuration
        let playerVars: [String: Any] = [
            "controls": 0,           // Hide YouTube controls
            "rel": 0,                // No related videos
            "showinfo": 0,           // No video info
            "modestbranding": 1,     // Minimal YouTube branding
            "iv_load_policy": 3,     // No annotations
            "fs": 0,                 // No fullscreen button
            "disablekb": 1,          // Disable keyboard controls
            "playsinline": 1         // Play inline (not fullscreen)
        ]
        
        playerView.load(
            withVideoId: videoID,
            playerVars: playerVars
        )
        
        playerView.delegate = context.coordinator
        
        return playerView
    }
    
    func updateUIView(_ uiView: YTPlayerView, context: Context) {}
    
    func makeCoordinator() -> Coordinator {
        Coordinator(onReady: onReady)
    }
    
    class Coordinator: NSObject, YTPlayerViewDelegate {
        let onReady: () -> Void
        
        init(onReady: @escaping () -> Void) {
            self.onReady = onReady
        }
        
        func playerViewDidBecomeReady(_ playerView: YTPlayerView) {
            playerView.playVideo()
            onReady()
        }
    }
}
```

### Analog Clock Component

> **Playbook Reference**: Part 4.10 - Analog Clock Component

```swift
struct AnalogCountdownClock: View {
    let totalMinutes: Int
    @Binding var remainingSeconds: TimeInterval
    
    var body: some View {
        ZStack {
            // Clock face (wooden texture)
            // Playbook: "Wooden texture with cream background"
            Circle()
                .fill(BennieColors.cream)
                .overlay(
                    Circle()
                        .stroke(BennieColors.bark, lineWidth: 8)
                )
            
            // Minute markers
            ForEach(0..<12) { i in
                Rectangle()
                    .fill(BennieColors.woodDark)
                    .frame(width: 2, height: i % 3 == 0 ? 15 : 8)
                    .offset(y: -55)
                    .rotationEffect(.degrees(Double(i) * 30))
            }
            
            // Remaining time arc (fills counterclockwise)
            // Playbook: "Green (#99BF8C) arc showing remaining time"
            Circle()
                .trim(from: 0, to: progress)
                .stroke(
                    BennieColors.success,
                    style: StrokeStyle(lineWidth: 12, lineCap: .round)
                )
                .rotationEffect(.degrees(-90))
            
            // Clock hand
            Rectangle()
                .fill(BennieColors.woodDark)
                .frame(width: 4, height: 45)
                .offset(y: -22)
                .rotationEffect(handRotation)
            
            // Center dot
            Circle()
                .fill(BennieColors.coinGold)
                .frame(width: 12, height: 12)
        }
        .frame(width: 150, height: 150)
    }
    
    var progress: CGFloat {
        // Playbook: "Progress from full to empty"
        CGFloat(remainingSeconds) / CGFloat(totalMinutes * 60)
    }
    
    var handRotation: Angle {
        // Playbook: "Hand rotates clockwise as time decreases"
        .degrees(360 * (1 - progress))
    }
}
```

### Time-Up Overlay

```swift
struct TimeUpOverlay: View {
    @Binding var isShowing: Bool
    
    var body: some View {
        ZStack {
            Color.black.opacity(0.8)
                .ignoresSafeArea()
            
            VStack(spacing: 30) {
                // Playbook: Bennie encouraging expression
                BennieView(expression: .encouraging)
                    .frame(width: 200, height: 300)
                
                Text("Die Zeit ist um!")
                    .font(.sfRounded(size: 36, weight: .bold))
                    .foregroundColor(.white)
                
                Text("Lass uns weiterspielen!")
                    .font(.sfRounded(size: 24, weight: .medium))
                    .foregroundColor(.white)
            }
        }
        .transition(.opacity)
    }
}
```

## Video Management (Parent Dashboard)

> **Playbook Reference**: Part 4.11 - Parent Dashboard - Video Management

### Add Video Flow

```swift
struct VideoManagementView: View {
    @State private var videoURL: String = ""
    @State private var previewVideo: ApprovedVideo? = nil
    @State private var isLoading = false
    
    var body: some View {
        VStack(spacing: 24) {
            Text("🎬 Video hinzufügen")
                .font(.sfRounded(size: 28, weight: .bold))
            
            Text("YouTube Link einfügen:")
                .font(.sfRounded(size: 18))
            
            // URL input
            TextField("https://youtube.com/watch?...", text: $videoURL)
                .textFieldStyle(.roundedBorder)
                .frame(width: 500)
                .autocapitalization(.none)
            
            Button("Einfügen aus Zwischenablage") {
                if let clipboard = UIPasteboard.general.string {
                    videoURL = clipboard
                    fetchVideoPreview()
                }
            }
            
            // Preview
            if let preview = previewVideo {
                VideoPreviewCard(video: preview)
            }
            
            HStack(spacing: 20) {
                Button("Abbrechen") {
                    dismiss()
                }
                
                Button("Hinzufügen") {
                    addVideo()
                }
                .disabled(previewVideo == nil)
            }
        }
        .onChange(of: videoURL) { _ in
            fetchVideoPreview()
        }
    }
    
    func fetchVideoPreview() {
        // Extract video ID from URL
        // Playbook Part 4.9: extractVideoID(from url: String)
        guard let videoID = ApprovedVideo.extractVideoID(from: videoURL) else {
            return
        }
        
        isLoading = true
        
        // Fetch video metadata from YouTube API
        YouTubeService.fetchMetadata(videoID: videoID) { result in
            isLoading = false
            
            switch result {
            case .success(let metadata):
                previewVideo = ApprovedVideo(
                    id: videoID,
                    title: metadata.title,
                    thumbnailURL: metadata.thumbnailURL,
                    addedAt: Date(),
                    category: nil
                )
            case .failure(let error):
                print("Error fetching video: \(error)")
            }
        }
    }
    
    func addVideo() {
        guard let video = previewVideo else { return }
        
        ParentSettings.shared.approvedVideos.append(video)
        ParentSettings.shared.save()
        
        dismiss()
    }
}

struct VideoPreviewCard: View {
    let video: ApprovedVideo
    
    var body: some View {
        HStack(spacing: 16) {
            AsyncImage(url: video.thumbnailURL) { image in
                image
                    .resizable()
                    .aspectRatio(contentMode: .fill)
            } placeholder: {
                Rectangle().fill(Color.gray.opacity(0.3))
            }
            .frame(width: 120, height: 68)
            .cornerRadius(8)
            
            VStack(alignment: .leading) {
                Text(video.title)
                    .font(.sfRounded(size: 16, weight: .semibold))
                    .lineLimit(2)
                
                Text("YouTube Video ID: \(video.id)")
                    .font(.sfRounded(size: 12))
                    .foregroundColor(.gray)
            }
            
            Spacer()
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 12)
                .fill(BennieColors.cream)
        )
    }
}
```

## Testing Checklist

> **Playbook Reference**: Part 10.2 - QA Verification Matrix

```
VIDEO SELECTION SCREEN:
□ Only shows pre-approved videos from parent settings
□ Maximum 6 videos visible, scroll for more
□ Thumbnail images load correctly (16:9 aspect ratio)
□ Video titles display (max 2 lines, truncated)
□ Time indicator shows correct duration (5 or 12 min)
□ Tapping video navigates to player
□ Touch targets >= 96pt
□ Back button returns to treasure screen
□ Bennie greeting voice plays on appear
□ Characters animate properly

OFFLINE DETECTION:
□ Detects when device is offline
□ Shows friendly message "Wir brauchen Internet"
□ Disables YouTube buttons (grayed out)
□ Shows offline indicator
□ Plays bennie voice explaining situation

VIDEO PLAYER SCREEN:
□ YouTube video loads and plays automatically
□ NO YouTube UI controls visible
□ NO related videos shown
□ NO annotations or suggestions
□ Analog clock displays correctly
□ Clock hand rotates as time decreases
□ Progress arc fills counterclockwise (green)
□ Time remaining text updates every second
□ One minute warning:
  □ Voice plays "Noch eine Minute"
  □ Clock pulses gently (3 times)
□ Time up behavior:
  □ Video stops playing
  □ Voice plays "Die Zeit ist um..."
  □ Overlay appears with Bennie
  □ Auto-navigates to home after 3 seconds

PARENT VIDEO MANAGEMENT:
□ Can paste YouTube URL
□ Extracts video ID correctly from various URL formats:
  □ youtube.com/watch?v=XXX
  □ youtu.be/XXX
  □ youtube.com/embed/XXX
□ Fetches video metadata (title, thumbnail)
□ Shows preview before adding
□ Adds to approved videos list
□ Saves to persistent storage
□ Can remove videos from list

PERFORMANCE:
□ Frame rate maintains 60fps during video playback
□ Memory usage stays under 200MB
□ Clock animation is smooth
□ Video loads within 3 seconds (good connection)
□ No lag when navigating between screens

ACCESSIBILITY:
□ VoiceOver labels correct for all elements
□ Video cards have descriptive labels
□ Clock has accessible time announcement
□ Touch targets clearly defined
□ Screen scales properly on all iPad sizes
```

## Accessibility

> **Playbook**: Part 5.7 - VoiceOver Support

```swift
// Video thumbnail card
.accessibilityLabel("\(video.title), zum Abspielen tippen")

// Analog clock
.accessibilityLabel("Verbleibende Zeit: \(formatTime(remainingSeconds))")
.accessibilityValue("\(Int(remainingSeconds / 60)) Minuten")

// Time up overlay
.accessibilityLabel("Die Zeit ist um. Zurück zum Spielen.")
```

---

## 📋 Implementation Checklist

**Phase 5C - Video Selection & Player**:
- [ ] Create VideoSelectionView.swift
- [ ] Create VideoPlayerView.swift
- [ ] Create ControlledYouTubePlayer.swift
- [ ] Create AnalogCountdownClock.swift
- [ ] Create VideoManagementView.swift (parent dashboard)
- [ ] Import/create youtube_icon.png
- [ ] Record voice lines:
  - [ ] bennie_video_greeting.aac
  - [ ] bennie_video_1min.aac
  - [ ] bennie_video_timeup.aac
  - [ ] wir_brauchen_internet.aac
- [ ] Implement ApprovedVideo data model
- [ ] Implement YouTubeService for metadata fetching
- [ ] Implement NetworkMonitor for offline detection
- [ ] Add YouTube iOS Player Helper dependency
- [ ] Test controlled YouTube embed (no controls)
- [ ] Test analog clock countdown
- [ ] Test one minute warning
- [ ] Test time-up behavior
- [ ] Test video management (add/remove)
- [ ] Verify accessibility with VoiceOver
- [ ] Performance test (60fps, <200MB)

**Asset Dependencies**:
- [ ] Create reference screens for video selection
- [ ] Create reference screen for video player
- [ ] bennie_excited.png (static)
- [ ] lemminge_excited.png (static)
- [ ] All voice files recorded and imported

**Integration Points**:
- [ ] TreasureScreen (navigation source)
- [ ] ParentDashboard (video management)
- [ ] NetworkMonitor (offline detection)
- [ ] HomeScreen (navigation target after time up)
- [ ] CoinManager (coin deduction before video selection)

**External Dependencies**:
- [ ] Add YouTubeiOSPlayerHelper to project
- [ ] Configure YouTube API for metadata fetching
- [ ] Set up proper YouTube embed permissions
- [ ] Test network connectivity monitoring
