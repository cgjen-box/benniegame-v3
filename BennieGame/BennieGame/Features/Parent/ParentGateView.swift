import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// ParentGateView - Parent area access gate
// ═══════════════════════════════════════════════════════════════════════════
// Placeholder showing math challenge for parent access
// Full implementation with proper validation coming in Phase 6
// ═══════════════════════════════════════════════════════════════════════════

/// Parent gate with math challenge to verify adult access
struct ParentGateView: View {
    // MARK: - Environment

    @Environment(AppCoordinator.self) private var coordinator

    // MARK: - Body

    var body: some View {
        ZStack {
            // Background
            BennieColors.cream
                .ignoresSafeArea()

            VStack(spacing: 40) {
                Spacer()

                // Lock icon and title
                VStack(spacing: 16) {
                    Image(systemName: "lock.fill")
                        .font(.system(size: 60))
                        .foregroundColor(BennieColors.woodDark)

                    Text("Elternbereich")
                        .font(BennieFont.title())
                        .foregroundColor(BennieColors.textDark)
                }

                Spacer()

                // Placeholder info
                placeholderInfo

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

    // MARK: - Placeholder Info

    private var placeholderInfo: some View {
        VStack(spacing: 20) {
            Text("Mathe-Frage kommt in Phase 6")
                .font(BennieFont.body())
                .foregroundColor(BennieColors.textDark.opacity(0.7))

            VStack(spacing: 8) {
                Text("Der Elternbereich wird folgendes enthalten:")
                    .font(BennieFont.label())
                    .foregroundColor(BennieColors.textDark.opacity(0.6))

                VStack(alignment: .leading, spacing: 4) {
                    featureItem("Spielzeit-Einstellungen")
                    featureItem("Video-Verwaltung")
                    featureItem("Fortschritts-Übersicht")
                    featureItem("Aktivitäten sperren/freigeben")
                }
            }
        }
        .padding(24)
        .background(
            RoundedRectangle(cornerRadius: 16)
                .fill(BennieColors.woodLight.opacity(0.3))
                .overlay(
                    RoundedRectangle(cornerRadius: 16)
                        .stroke(BennieColors.woodMedium.opacity(0.5), lineWidth: 1)
                )
        )
    }

    private func featureItem(_ text: String) -> some View {
        HStack(spacing: 8) {
            Image(systemName: "checkmark.circle")
                .font(.system(size: 14))
                .foregroundColor(BennieColors.success)
            Text(text)
                .font(BennieFont.label(14))
                .foregroundColor(BennieColors.textDark.opacity(0.7))
        }
    }
}

// MARK: - Previews

#Preview("ParentGateView") {
    ParentGateView()
        .environment(AppCoordinator())
}
