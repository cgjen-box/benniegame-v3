import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// LoadingView - Initial game loading screen
// ═══════════════════════════════════════════════════════════════════════════
// Shows animated progress bar and Bennie while app loads
// Auto-transitions to player selection after completion
// ═══════════════════════════════════════════════════════════════════════════

/// Loading screen shown on app launch
/// Features title sign, Bennie placeholder, and animated progress bar
struct LoadingView: View {
    // MARK: - Environment

    @Environment(AppCoordinator.self) private var coordinator

    // MARK: - State

    /// Loading progress from 0.0 to 1.0
    @State private var progress: CGFloat = 0.0

    /// Whether loading is complete
    @State private var isComplete: Bool = false

    // MARK: - Constants

    /// Duration of the loading animation in seconds
    private let loadingDuration: Double = 2.0

    /// Delay before transitioning after completion
    private let transitionDelay: Double = 0.5

    // MARK: - Body

    var body: some View {
        GeometryReader { geometry in
            ZStack {
                // Background
                BennieColors.cream
                    .ignoresSafeArea()

                VStack(spacing: 40) {
                    Spacer()

                    // Title sign
                    WoodSign(title: "Waldabenteuer lädt")
                        .scaleEffect(1.2)

                    Spacer()

                    // Bennie placeholder
                    bennieView

                    Spacer()

                    // Progress section
                    VStack(spacing: 16) {
                        // Custom loading progress bar
                        LoadingProgressBar(progress: progress)
                            .frame(width: min(geometry.size.width * 0.6, 500), height: 40)

                        // Loading text
                        Text("Lade Spielewelt...")
                            .font(BennieFont.body())
                            .foregroundColor(BennieColors.textDark)
                    }

                    Spacer()
                        .frame(height: 60)
                }
                .padding()
            }
        }
        .onAppear {
            startLoading()
        }
    }

    // MARK: - Subviews

    /// Bennie placeholder view using SF Symbol
    private var bennieView: some View {
        VStack(spacing: 8) {
            Image(systemName: isComplete ? "hand.wave.fill" : "bear.fill")
                .font(.system(size: 120))
                .foregroundColor(BennieColors.bennieBrown)
                .symbolEffect(.bounce, value: isComplete)

            if isComplete {
                Text("Bereit!")
                    .font(BennieFont.button())
                    .foregroundColor(BennieColors.textDark)
                    .transition(.opacity)
            }
        }
        .animation(.easeInOut, value: isComplete)
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
            isComplete = true

            // Transition to player selection after a brief delay
            DispatchQueue.main.asyncAfter(deadline: .now() + transitionDelay) {
                coordinator.transition(to: .playerSelection)
            }
        }
    }
}

// MARK: - Loading Progress Bar

/// Custom progress bar for the loading screen
/// Different from the coin-based ProgressBar component
private struct LoadingProgressBar: View {
    let progress: CGFloat

    var body: some View {
        GeometryReader { geometry in
            ZStack(alignment: .leading) {
                // Background trough
                RoundedRectangle(cornerRadius: 12)
                    .fill(BennieColors.woodDark)
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(BennieColors.woodDark, lineWidth: 2)
                    )

                // Fill bar
                RoundedRectangle(cornerRadius: 10)
                    .fill(
                        LinearGradient(
                            colors: [BennieColors.success, BennieColors.success.opacity(0.8)],
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
                    .frame(width: max(geometry.size.width * progress, 0))
                    .padding(4)

                // Percentage text
                Text("\(Int(progress * 100))%")
                    .font(BennieFont.button(18))
                    .foregroundColor(.white)
                    .shadow(color: .black.opacity(0.3), radius: 1, x: 0, y: 1)
                    .frame(maxWidth: .infinity, alignment: .center)
            }
        }
    }
}

// MARK: - Previews

#Preview("LoadingView") {
    LoadingView()
        .environment(AppCoordinator())
}

#Preview("LoadingProgressBar - Empty") {
    LoadingProgressBar(progress: 0)
        .frame(width: 400, height: 40)
        .padding()
}

#Preview("LoadingProgressBar - 50%") {
    LoadingProgressBar(progress: 0.5)
        .frame(width: 400, height: 40)
        .padding()
}

#Preview("LoadingProgressBar - Full") {
    LoadingProgressBar(progress: 1.0)
        .frame(width: 400, height: 40)
        .padding()
}
