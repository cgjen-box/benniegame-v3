import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// ZahlenSelectionView - Numbers activity selection screen
// ═══════════════════════════════════════════════════════════════════════════
// Placeholder showing available number sub-activities
// Full implementation coming in Phase 3
// ═══════════════════════════════════════════════════════════════════════════

/// Selection screen for number activities (Würfel, Wähle die Zahl)
struct ZahlenSelectionView: View {
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
                WoodSign(title: "Zahlen 1,2,3")
                    .scaleEffect(1.2)

                Spacer()

                // Sub-activity placeholders
                VStack(spacing: 24) {
                    subActivityButton(
                        title: "Würfel",
                        subtitle: "Punkte zählen",
                        icon: "die.face.5.fill",
                        comingSoon: true
                    )

                    subActivityButton(
                        title: "Wähle die Zahl",
                        subtitle: "Zahlen finden",
                        icon: "number.circle.fill",
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

#Preview("ZahlenSelectionView") {
    ZahlenSelectionView()
        .environment(AppCoordinator())
}
