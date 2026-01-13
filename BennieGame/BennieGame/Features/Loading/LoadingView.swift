import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// LoadingView - Initial game loading screen
// ═══════════════════════════════════════════════════════════════════════════
// Matches Reference_Loading Screen.png:
// - Bennie on LEFT, Lemminge on RIGHT
// - Title sign centered top, progress bar centered bottom
// ═══════════════════════════════════════════════════════════════════════════

struct LoadingView: View {
    @Environment(AppCoordinator.self) private var coordinator
    @Environment(NarratorService.self) private var narrator

    @State private var progress: CGFloat = 0.0
    @State private var isComplete: Bool = false
    @State private var lemmingeBob: Bool = false

    private let loadingDuration: Double = 2.0
    private let transitionDelay: Double = 0.5

    var body: some View {
        GeometryReader { geometry in
            ZStack {
                // Forest background - use the layered background but subtle
                Image("Backgrounds/forest_layer_far")
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(width: geometry.size.width, height: geometry.size.height)
                    .clipped()

                // Main content layout matching reference
                VStack(spacing: 0) {
                    // TOP: Title sign hanging from branch
                    titleSignWithBranch
                        .padding(.top, 20)

                    Spacer()

                    // MIDDLE: Bennie LEFT, Lemminge RIGHT
                    HStack(alignment: .bottom, spacing: 0) {
                        // LEFT: Bennie
                        Image("Characters/Bennie/bennie_waving")
                            .resizable()
                            .aspectRatio(contentMode: .fit)
                            .frame(height: geometry.size.height * 0.55)
                            .padding(.leading, geometry.size.width * 0.05)

                        Spacer()

                        // RIGHT: Lemminge peeking from tree positions
                        lemmingeColumn(geometry: geometry)
                            .padding(.trailing, geometry.size.width * 0.03)
                    }

                    // BOTTOM: Progress bar centered
                    progressBarSection(geometry: geometry)
                        .padding(.bottom, 30)
                }

                // Bottom left corner lemminge (like in reference)
                VStack {
                    Spacer()
                    HStack {
                        Image("Characters/Lemminge/lemminge_idle")
                            .resizable()
                            .aspectRatio(contentMode: .fit)
                            .frame(height: 60)
                            .offset(y: lemmingeBob ? -3 : 3)
                            .padding(.leading, 20)
                            .padding(.bottom, 80)
                        Spacer()
                    }
                }
            }
        }
        .ignoresSafeArea()
        .onAppear {
            startLoading()
            withAnimation(.easeInOut(duration: 1.5).repeatForever(autoreverses: true)) {
                lemmingeBob = true
            }
        }
    }

    // MARK: - Title Sign with Branch (matching reference)

    private var titleSignWithBranch: some View {
        VStack(spacing: 0) {
            // Horizontal branch with leaves (more natural like reference)
            ZStack {
                // Natural branch shape
                Capsule()
                    .fill(
                        LinearGradient(
                            colors: [BennieColors.woodDark, Color(hex: "5D3A1A"), BennieColors.woodDark],
                            startPoint: .top,
                            endPoint: .bottom
                        )
                    )
                    .frame(width: 380, height: 16)
                    .rotationEffect(.degrees(-2))

                // Leaves cluster on left
                HStack(spacing: -8) {
                    Image(systemName: "leaf.fill")
                        .font(.system(size: 20))
                        .foregroundColor(BennieColors.woodland)
                        .rotationEffect(.degrees(-45))
                    Image(systemName: "leaf.fill")
                        .font(.system(size: 16))
                        .foregroundColor(Color(hex: "5A7A52"))
                        .rotationEffect(.degrees(-20))
                }
                .offset(x: -200, y: -8)

                // Leaves cluster on right
                HStack(spacing: -8) {
                    Image(systemName: "leaf.fill")
                        .font(.system(size: 16))
                        .foregroundColor(Color(hex: "5A7A52"))
                        .rotationEffect(.degrees(20))
                    Image(systemName: "leaf.fill")
                        .font(.system(size: 20))
                        .foregroundColor(BennieColors.woodland)
                        .rotationEffect(.degrees(45))
                }
                .offset(x: 200, y: -8)
            }

            // Ropes connecting branch to sign
            HStack(spacing: 200) {
                ropeSegment
                ropeSegment
            }

            // Wooden sign with natural wood grain appearance
            ZStack {
                // Main sign body
                RoundedRectangle(cornerRadius: 10)
                    .fill(
                        LinearGradient(
                            colors: [BennieColors.woodMedium, BennieColors.woodLight, BennieColors.woodMedium],
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
                    .frame(width: 300, height: 100)
                    .overlay(
                        RoundedRectangle(cornerRadius: 10)
                            .stroke(BennieColors.woodDark, lineWidth: 4)
                    )

                VStack(spacing: 4) {
                    Text("Waldabenteuer")
                        .font(BennieFont.title(30))
                        .foregroundColor(BennieColors.textOnWood)
                    Text("lädt")
                        .font(BennieFont.button(24))
                        .foregroundColor(BennieColors.textOnWood)
                }
            }
            .shadow(color: .black.opacity(0.3), radius: 6, y: 5)
        }
    }

    private var ropeSegment: some View {
        VStack(spacing: 1) {
            ForEach(0..<4, id: \.self) { _ in
                Capsule()
                    .fill(BennieColors.rope)
                    .frame(width: 6, height: 8)
            }
        }
    }

    // MARK: - Lemminge Column (right side, matching reference)

    private func lemmingeColumn(geometry: GeometryProxy) -> some View {
        VStack(spacing: 15) {
            // Top lemminge
            Image("Characters/Lemminge/lemminge_curious")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(height: 70)
                .offset(y: lemmingeBob ? -4 : 4)

            // Middle lemminge
            Image("Characters/Lemminge/lemminge_excited")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(height: 65)
                .offset(x: -10)
                .offset(y: lemmingeBob ? 3 : -3)

            // Another lemminge
            Image("Characters/Lemminge/lemminge_hiding")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(height: 60)
                .offset(y: lemmingeBob ? -2 : 2)

            // Bottom lemminge
            Image("Characters/Lemminge/lemminge_mischievous")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(height: 65)
                .offset(x: 5)
                .offset(y: lemmingeBob ? 4 : -4)
        }
    }

    // MARK: - Progress Bar (centered bottom, log style with berries matching reference)

    private func progressBarSection(geometry: GeometryProxy) -> some View {
        VStack(spacing: 8) {
            // Log-style progress bar with percentage to the right (like reference)
            HStack(spacing: 12) {
                ZStack {
                    // Log background with bark texture effect
                    Capsule()
                        .fill(
                            LinearGradient(
                                colors: [BennieColors.woodDark, BennieColors.woodMedium, BennieColors.woodDark],
                                startPoint: .top,
                                endPoint: .bottom
                            )
                        )
                        .frame(width: min(geometry.size.width * 0.45, 450), height: 40)
                        .overlay(
                            Capsule()
                                .stroke(BennieColors.woodDark.opacity(0.5), lineWidth: 2)
                        )

                    // Progress fill (green like reference)
                    HStack {
                        Capsule()
                            .fill(BennieColors.success)
                            .frame(width: max((min(geometry.size.width * 0.45, 450) - 10) * progress, 10), height: 30)
                            .padding(.leading, 5)
                        Spacer()
                    }
                    .frame(width: min(geometry.size.width * 0.45, 450))

                    // Berry/leaf decorations on the log (matching reference style)
                    HStack(spacing: 25) {
                        berryDecoration(color: Color(hex: "8B4513")) // brown berry
                        leafDecoration()
                        berryDecoration(color: Color(hex: "C04040")) // red berry
                        leafDecoration()
                        berryDecoration(color: Color(hex: "4040A0")) // blue berry
                    }
                    .offset(y: -24)
                }

                // Percentage to the right of bar (like reference)
                Text("\(Int(progress * 100))%")
                    .font(BennieFont.button(18))
                    .foregroundColor(BennieColors.textDark)
            }

            // Loading text
            Text("Lade Spielewelt...")
                .font(BennieFont.body())
                .foregroundColor(BennieColors.textDark)
        }
    }

    private func leafDecoration() -> some View {
        Image(systemName: "leaf.fill")
            .font(.system(size: 12))
            .foregroundColor(BennieColors.woodland)
            .rotationEffect(.degrees(-20))
    }

    private func berryDecoration(color: Color) -> some View {
        Circle()
            .fill(color)
            .frame(width: 14, height: 14)
            .overlay(
                Circle()
                    .fill(color.opacity(0.6))
                    .frame(width: 6, height: 6)
                    .offset(x: -2, y: -2)
            )
    }

    // MARK: - Loading Logic

    private func startLoading() {
        withAnimation(.linear(duration: loadingDuration)) {
            progress = 1.0
        }

        DispatchQueue.main.asyncAfter(deadline: .now() + loadingDuration) {
            isComplete = true
            narrator.playLoadingComplete()

            DispatchQueue.main.asyncAfter(deadline: .now() + transitionDelay) {
                coordinator.transition(to: .playerSelection)
            }
        }
    }
}

#Preview("LoadingView") {
    LoadingView()
        .environment(AppCoordinator())
        .environment(NarratorService(audioManager: AudioManager()))
}
