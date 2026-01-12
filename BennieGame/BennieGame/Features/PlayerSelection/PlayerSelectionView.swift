import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// PlayerSelectionView - Player selection screen
// ═══════════════════════════════════════════════════════════════════════════
// Shows buttons for Alexander and Oliver to select who is playing
// Displays current coin count for each player
// ═══════════════════════════════════════════════════════════════════════════

/// Player selection screen where children choose their profile
/// Features two large buttons for Alexander and Oliver with their coin counts
struct PlayerSelectionView: View {
    // MARK: - Environment

    @Environment(AppCoordinator.self) private var coordinator
    @Environment(PlayerStore.self) private var playerStore
    @Environment(NarratorService.self) private var narrator

    // MARK: - State

    /// Animation state for button selection feedback
    @State private var selectedPlayerId: String? = nil

    // MARK: - Constants

    /// Delay before navigation after selection
    private let navigationDelay: Double = 0.3

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
                    WoodSign(title: "Wer spielt heute?")
                        .scaleEffect(1.3)

                    Spacer()

                    // Player buttons
                    HStack(spacing: 60) {
                        // Alexander button - positioned around (400, 350)
                        playerButton(for: "alexander", position: 400 / 1194)

                        // Oliver button - positioned around (800, 350)
                        playerButton(for: "oliver", position: 800 / 1194)
                    }
                    .padding(.horizontal, 40)

                    Spacer()

                    // Bennie placeholder at bottom center
                    bennieView
                        .padding(.bottom, 40)
                }
            }
        }
        .onAppear {
            // Play player question audio
            narrator.playPlayerQuestion()
        }
    }

    // MARK: - Subviews

    /// Creates a player selection button
    private func playerButton(for playerId: String, position: CGFloat) -> some View {
        let player = playerStore.getPlayer(id: playerId)
        let isSelected = selectedPlayerId == playerId

        return PlayerButton(
            name: player?.name ?? playerId.capitalized,
            coins: player?.coins ?? 0,
            isSelected: isSelected
        ) {
            selectPlayer(id: playerId)
        }
    }

    /// Bennie placeholder showing waving gesture
    private var bennieView: some View {
        VStack(spacing: 8) {
            Image(systemName: "hand.wave.fill")
                .font(.system(size: 60))
                .foregroundColor(BennieColors.bennieBrown)

            Image(systemName: "bear.fill")
                .font(.system(size: 80))
                .foregroundColor(BennieColors.bennieBrown)
        }
    }

    // MARK: - Actions

    /// Handle player selection
    private func selectPlayer(id: String) {
        // Set selection for visual feedback
        selectedPlayerId = id

        // Select player in store
        playerStore.selectPlayer(id: id)

        // Play hello audio for selected player
        let playerName = playerStore.getPlayer(id: id)?.name ?? id.capitalized
        narrator.playHello(playerName: playerName)

        // Navigate to home after brief delay
        DispatchQueue.main.asyncAfter(deadline: .now() + navigationDelay) {
            coordinator.transition(to: .home)
        }
    }
}

// MARK: - Player Button

/// Individual player selection button with avatar, name, and coin count
private struct PlayerButton: View {
    let name: String
    let coins: Int
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        ChildFriendlyButton(action: action) {
            VStack(spacing: 12) {
                // Avatar placeholder
                Image(systemName: "person.fill")
                    .font(.system(size: 48))
                    .foregroundColor(BennieColors.textOnWood)

                // Player name
                Text(name)
                    .font(BennieFont.button(28))
                    .foregroundColor(BennieColors.textOnWood)

                // Coin count
                HStack(spacing: 4) {
                    Text("🪙")
                    Text("\(coins) Münzen")
                        .font(BennieFont.label(18))
                }
                .foregroundColor(BennieColors.textOnWood)
            }
            .frame(minWidth: 180, minHeight: 200)
            .padding(24)
            .background(
                RoundedRectangle(cornerRadius: 16)
                    .fill(
                        LinearGradient(
                            colors: [BennieColors.woodLight, BennieColors.woodMedium],
                            startPoint: .top,
                            endPoint: .bottom
                        )
                    )
            )
            .overlay(
                RoundedRectangle(cornerRadius: 16)
                    .stroke(
                        isSelected ? BennieColors.success : BennieColors.woodDark,
                        lineWidth: isSelected ? 4 : 3
                    )
            )
            .shadow(
                color: isSelected ? BennieColors.success.opacity(0.5) : .black.opacity(0.2),
                radius: isSelected ? 8 : 4,
                x: 0,
                y: 2
            )
            .scaleEffect(isSelected ? 1.05 : 1.0)
            .animation(.easeInOut(duration: 0.2), value: isSelected)
        }
    }
}

// MARK: - Previews

#Preview("PlayerSelectionView") {
    let audioManager = AudioManager()
    return PlayerSelectionView()
        .environment(AppCoordinator())
        .environment(PlayerStore())
        .environment(NarratorService(audioManager: audioManager))
}

#Preview("PlayerButton - Normal") {
    PlayerButton(name: "Alexander", coins: 5, isSelected: false) {
        print("Selected Alexander")
    }
    .padding()
}

#Preview("PlayerButton - Selected") {
    PlayerButton(name: "Oliver", coins: 12, isSelected: true) {
        print("Selected Oliver")
    }
    .padding()
}

#Preview("PlayerButton - Both") {
    HStack(spacing: 40) {
        PlayerButton(name: "Alexander", coins: 5, isSelected: false) { }
        PlayerButton(name: "Oliver", coins: 12, isSelected: true) { }
    }
    .padding()
}
