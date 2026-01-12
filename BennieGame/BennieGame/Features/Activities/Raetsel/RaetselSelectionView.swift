import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// RaetselSelectionView - Puzzle activity selection screen
// ═══════════════════════════════════════════════════════════════════════════
// Placeholder showing available puzzle sub-activities
// Full implementation coming in Phase 3
// ═══════════════════════════════════════════════════════════════════════════

/// Selection screen for puzzle activities (Puzzle Matching, Labyrinth)
struct RaetselSelectionView: View {
    // MARK: - Environment

    @Environment(AppCoordinator.self) private var coordinator

    // MARK: - Body

    var body: some View {
        ZStack {
            // Background
            BennieColors.cream
                .ignoresSafeArea()

            VStack(spacing: 40) {
                // Title sign
                WoodSign(title: "Rätsel")
                    .scaleEffect(1.2)

                Spacer()

                // Sub-activity buttons
                VStack(spacing: 24) {
                    // Puzzle Matching - NOW PLAYABLE
                    Button {
                        coordinator.startPlaying(.raetsel, .puzzleMatching)
                    } label: {
                        subActivityButton(
                            title: "Puzzle",
                            subtitle: "Muster nachmachen",
                            icon: "puzzlepiece.fill",
                            comingSoon: false
                        )
                    }
                    .buttonStyle(.plain)

                    // Labyrinth - Coming in 03-02
                    subActivityButton(
                        title: "Labyrinth",
                        subtitle: "Den Weg finden",
                        icon: "arrow.triangle.turn.up.right.circle.fill",
                        comingSoon: true
                    )
                }

                Spacer()

                // Back button
                WoodButton("Zurück", icon: "arrow.left") {
                    coordinator.navigateHome()
                }
                .padding(.bottom, 40)
            }
            .padding()
        }
    }

    // MARK: - Sub-Activity Button

    private func subActivityButton(
        title: String,
        subtitle: String,
        icon: String,
        comingSoon: Bool
    ) -> some View {
        HStack(spacing: 20) {
            // Icon
            Image(systemName: icon)
                .font(.system(size: 40))
                .foregroundColor(BennieColors.woodDark)
                .frame(width: 60)

            // Text
            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(BennieFont.button())
                    .foregroundColor(BennieColors.textOnWood)
                Text(subtitle)
                    .font(BennieFont.label())
                    .foregroundColor(BennieColors.textOnWood.opacity(0.7))
                if comingSoon {
                    Text("Kommt in Phase 3")
                        .font(BennieFont.label(12))
                        .foregroundColor(BennieColors.woodMedium)
                }
            }

            Spacer()
        }
        .frame(minWidth: 300, minHeight: 96)
        .padding(.horizontal, 24)
        .padding(.vertical, 12)
        .background(
            RoundedRectangle(cornerRadius: 16)
                .fill(BennieColors.woodLight)
                .overlay(
                    RoundedRectangle(cornerRadius: 16)
                        .stroke(BennieColors.woodDark, lineWidth: 2)
                )
        )
    }
}

// MARK: - Previews

#Preview("RaetselSelectionView") {
    RaetselSelectionView()
        .environment(AppCoordinator())
}
