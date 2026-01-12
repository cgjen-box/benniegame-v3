import SwiftUI
import WebKit

// ═══════════════════════════════════════════════════════════════════════════
// VideoPlayerView - YouTube video player with countdown timer
// ═══════════════════════════════════════════════════════════════════════════
// Embeds YouTube video using WKWebView with controls disabled
// Shows analog clock countdown with visual and audio warnings
// Auto-navigates home when time expires
// ═══════════════════════════════════════════════════════════════════════════

// MARK: - YouTube Player (UIViewRepresentable)

/// UIViewRepresentable wrapper for WKWebView to embed YouTube videos
struct YouTubePlayerView: UIViewRepresentable {
    let videoId: String

    func makeUIView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        config.allowsInlineMediaPlayback = true
        config.mediaTypesRequiringUserActionForPlayback = []

        let webView = WKWebView(frame: .zero, configuration: config)
        webView.scrollView.isScrollEnabled = false
        webView.backgroundColor = .black
        webView.isOpaque = false

        return webView
    }

    func updateUIView(_ webView: WKWebView, context: Context) {
        // Build YouTube embed URL with controls disabled
        // Using youtube-nocookie for enhanced privacy
        let embedURL = "https://www.youtube-nocookie.com/embed/\(videoId)?controls=0&rel=0&modestbranding=1&playsinline=1&autoplay=1&disablekb=1&fs=0&iv_load_policy=3&showinfo=0"

        if let url = URL(string: embedURL) {
            let request = URLRequest(url: url)
            webView.load(request)
        }
    }
}

// MARK: - Video Player View

/// Main video player screen with embedded YouTube and countdown timer
struct VideoPlayerView: View {
    // MARK: - Environment

    @Environment(AppCoordinator.self) private var coordinator
    @Environment(BennieService.self) private var bennie

    // MARK: - Properties

    let minutesRemaining: Int
    let videoId: String

    // MARK: - State

    @State private var secondsRemaining: Int
    @State private var showTimeUpMessage: Bool = false
    @State private var clockPulse: Bool = false
    @State private var timer: Timer?
    @State private var hasPlayedOneMinuteWarning: Bool = false

    // MARK: - Initialization

    init(minutesRemaining: Int, videoId: String) {
        self.minutesRemaining = minutesRemaining
        self.videoId = videoId
        self._secondsRemaining = State(initialValue: minutesRemaining * 60)
    }

    // MARK: - Body

    var body: some View {
        ZStack {
            // Background
            Color.black
                .ignoresSafeArea()

            VStack(spacing: 0) {
                // YouTube player (top 70%)
                YouTubePlayerView(videoId: videoId)
                    .frame(maxWidth: .infinity)
                    .frame(height: UIScreen.main.bounds.height * 0.70)

                // Countdown section (bottom 30%)
                countdownSection
            }

            // Time up overlay
            if showTimeUpMessage {
                timeUpOverlay
            }
        }
        .onAppear {
            startTimer()
        }
        .onDisappear {
            stopTimer()
        }
    }

    // MARK: - Countdown Section

    private var countdownSection: some View {
        VStack(spacing: 16) {
            Spacer()

            // Analog clock
            analogClock
                .scaleEffect(clockPulse ? 1.1 : 1.0)
                .animation(.easeInOut(duration: 0.5).repeatForever(autoreverses: true), value: clockPulse)

            // Digital time display
            Text(formattedTime)
                .font(BennieFont.number())
                .foregroundColor(isLowTime ? BennieColors.coinGold : .white)

            // Time remaining text
            Text(isLowTime ? "Gleich ist die Zeit um!" : "Verbleibende Zeit")
                .font(BennieFont.label())
                .foregroundColor(.white.opacity(0.7))

            Spacer()
        }
        .frame(maxWidth: .infinity)
        .frame(height: UIScreen.main.bounds.height * 0.30)
        .background(BennieColors.woodDark)
    }

    // MARK: - Analog Clock

    private var analogClock: some View {
        ZStack {
            // Clock face background
            Circle()
                .fill(BennieColors.woodLight)
                .frame(width: 120, height: 120)

            // Clock border
            Circle()
                .stroke(BennieColors.woodDark, lineWidth: 4)
                .frame(width: 120, height: 120)

            // Progress arc (remaining time)
            Circle()
                .trim(from: 0, to: progressPercentage)
                .stroke(
                    BennieColors.success,
                    style: StrokeStyle(lineWidth: 10, lineCap: .round)
                )
                .frame(width: 100, height: 100)
                .rotationEffect(.degrees(-90))

            // Warning arc when low time
            if isLowTime {
                Circle()
                    .trim(from: 0, to: progressPercentage)
                    .stroke(
                        BennieColors.coinGold,
                        style: StrokeStyle(lineWidth: 10, lineCap: .round)
                    )
                    .frame(width: 100, height: 100)
                    .rotationEffect(.degrees(-90))
            }

            // Clock hand
            Rectangle()
                .fill(BennieColors.woodDark)
                .frame(width: 4, height: 35)
                .offset(y: -17.5)
                .rotationEffect(.degrees(handRotation))

            // Center dot
            Circle()
                .fill(BennieColors.woodDark)
                .frame(width: 12, height: 12)

            // Minute markers
            ForEach(0..<12, id: \.self) { index in
                Rectangle()
                    .fill(BennieColors.woodDark.opacity(0.5))
                    .frame(width: 2, height: 8)
                    .offset(y: -50)
                    .rotationEffect(.degrees(Double(index) * 30))
            }
        }
    }

    // MARK: - Time Up Overlay

    private var timeUpOverlay: some View {
        ZStack {
            // Dark background
            Color.black.opacity(0.8)
                .ignoresSafeArea()

            VStack(spacing: 24) {
                // Clock icon
                Image(systemName: "clock.badge.checkmark.fill")
                    .font(.system(size: 80))
                    .foregroundColor(BennieColors.success)

                // Message
                Text("Zeit ist um!")
                    .font(BennieFont.title())
                    .foregroundColor(.white)

                Text("Zurück zum Spielen!")
                    .font(BennieFont.screenHeader())
                    .foregroundColor(.white.opacity(0.8))
            }
            .padding(48)
            .background(
                RoundedRectangle(cornerRadius: 24)
                    .fill(BennieColors.woodDark)
            )
        }
    }

    // MARK: - Timer Logic

    private func startTimer() {
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
            if secondsRemaining > 0 {
                secondsRemaining -= 1

                // Check for 1-minute warning (60 seconds)
                if secondsRemaining == 60 && !hasPlayedOneMinuteWarning {
                    hasPlayedOneMinuteWarning = true
                    startClockPulse()
                    bennie.playOneMinuteWarning()
                }

                // Check for time up
                if secondsRemaining == 0 {
                    handleTimeUp()
                }
            }
        }
    }

    private func stopTimer() {
        timer?.invalidate()
        timer = nil
    }

    private func startClockPulse() {
        clockPulse = true
    }

    private func handleTimeUp() {
        stopTimer()
        showTimeUpMessage = true

        // Play time up audio
        bennie.playTimeUp()

        // Navigate home after 2 seconds
        DispatchQueue.main.asyncAfter(deadline: .now() + 2.0) {
            coordinator.navigateHome()
        }
    }

    // MARK: - Computed Properties

    /// Progress percentage for the clock arc (0.0 to 1.0)
    private var progressPercentage: CGFloat {
        let totalSeconds = CGFloat(minutesRemaining * 60)
        return CGFloat(secondsRemaining) / totalSeconds
    }

    /// Rotation angle for the clock hand in degrees
    private var handRotation: Double {
        let progress = Double(secondsRemaining) / Double(minutesRemaining * 60)
        return 360.0 * (1.0 - progress)
    }

    /// Formatted time string (M:SS)
    private var formattedTime: String {
        let minutes = secondsRemaining / 60
        let seconds = secondsRemaining % 60
        return String(format: "%d:%02d", minutes, seconds)
    }

    /// Check if time is low (1 minute or less)
    private var isLowTime: Bool {
        secondsRemaining <= 60
    }
}

// MARK: - Previews

#Preview("VideoPlayerView - 5 Minutes") {
    let audioManager = AudioManager()
    return VideoPlayerView(minutesRemaining: 5, videoId: "qw0Jz5zJkgE")
        .environment(AppCoordinator())
        .environment(BennieService(audioManager: audioManager))
}

#Preview("VideoPlayerView - 1 Minute") {
    let audioManager = AudioManager()
    return VideoPlayerView(minutesRemaining: 1, videoId: "qw0Jz5zJkgE")
        .environment(AppCoordinator())
        .environment(BennieService(audioManager: audioManager))
}
