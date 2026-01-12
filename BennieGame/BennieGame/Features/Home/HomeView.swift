import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// HomeView - Main menu placeholder
// ═══════════════════════════════════════════════════════════════════════════
// Placeholder implementation showing active player info
// Full implementation coming in phase 02-03
// ═══════════════════════════════════════════════════════════════════════════

/// Home screen placeholder - full implementation in 02-03
/// Shows active player name and basic info
struct HomeView: View {
    // MARK: - Environment

    @Environment(AppCoordinator.self) private var coordinator
    @Environment(PlayerStore.self) private var playerStore

    // MARK: - Body

    var body: some View {
        ZStack {
            // Background
            BennieColors.cream
                .ignoresSafeArea()

            VStack(spacing: 32) {
                Spacer()

                // Title sign
                WoodSign(title: "Waldabenteuer")
                    .scaleEffect(1.4)

                Spacer()

                // Active player info
                if let player = playerStore.activePlayer {
                    VStack(spacing: 16) {
                        HStack(spacing: 8) {
                            Image(systemName: "person.fill")
                                .font(.system(size: 32))
                            Text("Hallo, \(player.name)!")
                                .font(BennieFont.screenHeader())
                        }
                        .foregroundColor(BennieColors.bennieBrown)

                        HStack(spacing: 4) {
                            Text("🪙")
                            Text("\(player.coins) Münzen")
                                .font(BennieFont.body())
                        }
                        .foregroundColor(BennieColors.textDark)
                    }
                    .padding()
                    .background(
                        RoundedRectangle(cornerRadius: 16)
                            .fill(BennieColors.woodLight.opacity(0.3))
                    )
                }

                Spacer()

                // Placeholder notice
                Text("Home screen coming in 02-03")
                    .font(BennieFont.label())
                    .foregroundColor(BennieColors.textDark.opacity(0.6))
                    .padding()
                    .background(
                        RoundedRectangle(cornerRadius: 8)
                            .stroke(BennieColors.woodMedium.opacity(0.5), lineWidth: 1)
                    )

                Spacer()

                // Bennie placeholder
                Image(systemName: "bear.fill")
                    .font(.system(size: 100))
                    .foregroundColor(BennieColors.bennieBrown)
                    .padding(.bottom, 40)
            }
            .padding()
        }
    }
}

// MARK: - Previews

#Preview("HomeView") {
    let store = PlayerStore()
    store.selectPlayer(id: "alexander")

    return HomeView()
        .environment(AppCoordinator())
        .environment(store)
}

#Preview("HomeView - Oliver") {
    let store = PlayerStore()
    store.selectPlayer(id: "oliver")

    return HomeView()
        .environment(AppCoordinator())
        .environment(store)
}
