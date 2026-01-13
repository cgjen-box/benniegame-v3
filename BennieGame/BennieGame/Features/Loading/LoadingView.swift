import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// LoadingView - Initial game loading screen
// ═══════════════════════════════════════════════════════════════════════════
// Shows forest background, Bennie waving, Lemminge peeking, and progress bar
// Auto-transitions to player selection after completion
// ═══════════════════════════════════════════════════════════════════════════

/// Loading screen shown on app launch
/// Features forest background, title sign, Bennie character, Lemminge, and progress bar
struct LoadingView: View {
    // MARK: - Environment

    @Environment(AppCoordinator.self) private var coordinator
    @Environment(NarratorService.self) private var narrator

    // MARK: - State

    /// Loading progress from 0.0 to 1.0
    @State private var progress: CGFloat = 0.0

    /// Whether loading is complete
    @State private var isComplete: Bool = false

    /// Lemminge bob animation
    @State private var lemmingeBob: Bool = false

    // MARK: - Constants

    /// Duration of the loading animation in seconds
    private let loadingDuration: Double = 2.0

    /// Delay before transitioning after completion
    private let transitionDelay: Double = 0.5

    // MARK: - Body

    var body: some View {
        GeometryReader { geometry in
            ZStack {
                // Forest background with parallax layers
                ForestBackground()

                // Title sign (top center, hanging from branch)
                VStack {
                    titleSign
                        .padding(.top, 60)
                    Spacer()
                }

                // Main content area
                HStack(alignment: .bottom, spacing: 0) {
                    // Bennie on the left
                    bennieView
                        .frame(width: geometry.size.width * 0.35)

                    // Center content (progress bar)
                    VStack {
                        Spacer()
                        progressSection(geometry: geometry)
                            .padding(.bottom, 60)
                    }
                    .frame(width: geometry.size.width * 0.3)

                    // Right side (Lemminge peeking)
                    Spacer()
                        .frame(width: geometry.size.width * 0.35)
                }

                // Lemminge positioned around the edges
                lemmingeOverlay(geometry: geometry)
            }
        }
        .onAppear {
            startLoading()
            startLemmingeBob()
        }
    }

    // MARK: - Subviews

    /// Title sign hanging from branch
    private var titleSign: some View {
        VStack(spacing: 0) {
            // Branch and rope
            HStack(spacing: 0) {
                Image(systemName: "leaf.fill")
                    .font(.system(size: 24))
                    .foregroundColor(BennieColors.woodland)
                    .rotationEffect(.degrees(-45))

                Rectangle()
                    .fill(BennieColors.woodDark)
                    .frame(width: 200, height: 8)
                    .overlay(
                        // Wood grain lines
                        HStack(spacing: 20) {
                            ForEach(0..<4, id: \.self) { _ in
                                Rectangle()
                                    .fill(BennieColors.woodMedium)
                                    .frame(width: 2, height: 6)
                            }
                        }
                    )

                Image(systemName: "leaf.fill")
                    .font(.system(size: 24))
                    .foregroundColor(BennieColors.woodland)
                    .rotationEffect(.degrees(45))
            }

            // Rope segments
            HStack(spacing: 80) {
                RopeSegment()
                RopeSegment()
            }

            // Sign body
            ZStack {
                // Wood background with grain texture
                RoundedRectangle(cornerRadius: 12)
                    .fill(BennieColors.woodMedium)
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(BennieColors.woodDark, lineWidth: 3)
                    )
                    .overlay(
                        // Subtle grain lines
                        VStack(spacing: 12) {
                            ForEach(0..<3, id: \.self) { _ in
                                Rectangle()
                                    .fill(BennieColors.woodLight.opacity(0.3))
                                    .frame(height: 1)
                            }
                        }
                        .padding(.horizontal, 20)
                    )

                // Text
                VStack(spacing: 4) {
                    Text("Waldabenteuer")
                        .font(BennieFont.title(32))
                        .foregroundColor(BennieColors.textOnWood)

                    Text("lädt")
                        .font(BennieFont.button(24))
                        .foregroundColor(BennieColors.textOnWood.opacity(0.9))
                }
            }
            .frame(width: 280, height: 100)
            .shadow(color: BennieColors.woodDark.opacity(0.3), radius: 4, x: 2, y: 4)
        }
    }

    /// Rope segment connecting branch to sign
    private struct RopeSegment: View {
        var body: some View {
            VStack(spacing: 0) {
                ForEach(0..<3, id: \.self) { _ in
                    Capsule()
                        .fill(BennieColors.rope)
                        .frame(width: 8, height: 12)
                }
            }
        }
    }

    /// Bennie character view using actual asset
    private var bennieView: some View {
        VStack(spacing: 8) {
            Spacer()

            Image("bennie_waving")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(height: 280)
                .scaleEffect(isComplete ? 1.05 : 1.0)
                .animation(.easeInOut(duration: 0.3), value: isComplete)

            if isComplete {
                Text("Bereit!")
                    .font(BennieFont.button(20))
                    .foregroundColor(BennieColors.textDark)
                    .padding(.horizontal, 16)
                    .padding(.vertical, 8)
                    .background(
                        Capsule()
                            .fill(BennieColors.cream.opacity(0.9))
                    )
                    .transition(.scale.combined(with: .opacity))
            }
        }
        .padding(.bottom, 40)
        .padding(.leading, 40)
    }

    /// Progress section with berry-decorated log bar
    private func progressSection(geometry: GeometryProxy) -> some View {
        VStack(spacing: 16) {
            // Berry-decorated log progress bar
            LoadingProgressBar(progress: progress)
                .frame(width: min(geometry.size.width * 0.5, 450), height: 44)

            // Loading text
            Text("Lade Spielewelt...")
                .font(BennieFont.body())
                .foregroundColor(BennieColors.textDark)
                .padding(.horizontal, 16)
                .padding(.vertical, 8)
                .background(
                    Capsule()
                        .fill(BennieColors.cream.opacity(0.8))
                )
        }
    }

    /// Lemminge peeking from various positions
    private func lemmingeOverlay(geometry: GeometryProxy) -> some View {
        ZStack {
            // Top right Lemminge (curious, peeking from tree)
            Image("lemminge_curious")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(height: 80)
                .offset(x: geometry.size.width * 0.35, y: -geometry.size.height * 0.25)
                .offset(y: lemmingeBob ? -5 : 5)

            // Right side Lemminge (hiding, peeking from hole)
            Image("lemminge_hiding")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(height: 70)
                .offset(x: geometry.size.width * 0.40, y: -geometry.size.height * 0.05)
                .offset(y: lemmingeBob ? 5 : -5)

            // Far right Lemminge (excited)
            Image("lemminge_excited")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(height: 75)
                .offset(x: geometry.size.width * 0.38, y: geometry.size.height * 0.15)
                .offset(y: lemmingeBob ? -3 : 3)

            // Bottom left corner Lemminge (idle)
            Image("lemminge_idle")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(height: 60)
                .offset(x: -geometry.size.width * 0.40, y: geometry.size.height * 0.35)
                .offset(y: lemmingeBob ? 4 : -4)
        }
        .animation(.easeInOut(duration: 1.5).repeatForever(autoreverses: true), value: lemmingeBob)
    }

    // MARK: - Loading Logic

    /// Start the loading animation and transition
    private func startLoading() {
        // Animate progress from 0 to 1 over the loading duration
        withAnimation(.linear(duration: loadingDuration)) {
            progress = 1.0
        }

        // Mark as complete and transition after loading
        DispatchQueue.main.asyncAfter(deadline: .now() + loadingDuration) {
            withAnimation(.spring(response: 0.4, dampingFraction: 0.7)) {
                isComplete = true
            }

            // Play loading complete audio
            narrator.playLoadingComplete()

            // Transition to player selection after a brief delay
            DispatchQueue.main.asyncAfter(deadline: .now() + transitionDelay) {
                coordinator.transition(to: .playerSelection)
            }
        }
    }

    /// Start the Lemminge bobbing animation
    private func startLemmingeBob() {
        lemmingeBob = true
    }
}

// MARK: - Loading Progress Bar

/// Custom progress bar styled as a berry-decorated log
/// Different from the coin-based ProgressBar component
private struct LoadingProgressBar: View {
    let progress: CGFloat

    var body: some View {
        GeometryReader { geometry in
            ZStack(alignment: .leading) {
                // Log background (trough)
                Capsule()
                    .fill(BennieColors.woodDark)
                    .overlay(
                        // Wood grain lines
                        HStack(spacing: 30) {
                            ForEach(0..<Int(geometry.size.width / 50), id: \.self) { _ in
                                Capsule()
                                    .fill(BennieColors.woodMedium.opacity(0.5))
                                    .frame(width: 3, height: geometry.size.height * 0.6)
                            }
                        }
                    )
                    .overlay(
                        Capsule()
                            .stroke(BennieColors.woodDark.opacity(0.6), lineWidth: 2)
                    )

                // Fill bar (berry-colored gradient)
                Capsule()
                    .fill(
                        LinearGradient(
                            colors: [
                                BennieColors.success,
                                BennieColors.success.opacity(0.85)
                            ],
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
                    .frame(width: max((geometry.size.width - 8) * progress, 0))
                    .padding(4)

                // Berry decorations along the top
                HStack(spacing: 40) {
                    ForEach(0..<4, id: \.self) { index in
                        Circle()
                            .fill(berryColor(for: index))
                            .frame(width: 12, height: 12)
                            .offset(y: -geometry.size.height * 0.35)
                    }
                }
                .padding(.horizontal, 30)

                // Percentage text
                Text("\(Int(progress * 100))%")
                    .font(BennieFont.button(18))
                    .foregroundColor(BennieColors.textOnWood)
                    .shadow(color: BennieColors.woodDark.opacity(0.5), radius: 1, x: 0, y: 1)
                    .frame(maxWidth: .infinity, alignment: .center)
            }
        }
    }

    /// Berry colors for decoration
    private func berryColor(for index: Int) -> Color {
        let colors: [Color] = [
            Color(hex: "#8B4513"), // Brown berry
            Color(hex: "#6B4423"), // Dark berry
            Color(hex: "#99BF8C"), // Green berry
            Color(hex: "#8B4513")  // Brown berry
        ]
        return colors[index % colors.count]
    }
}

// MARK: - Previews

#Preview("LoadingView") {
    let audioManager = AudioManager()
    return LoadingView()
        .environment(AppCoordinator())
        .environment(NarratorService(audioManager: audioManager))
}

#Preview("LoadingProgressBar - 20%") {
    LoadingProgressBar(progress: 0.2)
        .frame(width: 400, height: 44)
        .padding()
        .background(BennieColors.cream)
}

#Preview("LoadingProgressBar - 50%") {
    LoadingProgressBar(progress: 0.5)
        .frame(width: 400, height: 44)
        .padding()
        .background(BennieColors.cream)
}

#Preview("LoadingProgressBar - Full") {
    LoadingProgressBar(progress: 1.0)
        .frame(width: 400, height: 44)
        .padding()
        .background(BennieColors.cream)
}
