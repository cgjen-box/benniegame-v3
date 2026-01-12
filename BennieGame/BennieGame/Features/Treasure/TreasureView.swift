import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// TreasureView - Treasure chest screen for YouTube redemption
// ═══════════════════════════════════════════════════════════════════════════
// Placeholder showing coin count and redemption options
// Full implementation with YouTube integration coming in Phase 4
// ═══════════════════════════════════════════════════════════════════════════

/// Treasure screen for redeeming coins for YouTube time
struct TreasureView: View {
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
                // Back button at top left
                HStack {
                    backButton
                    Spacer()
                }
                .padding(.horizontal)

                // Title sign
                WoodSign(title: "Schatztruhe")
                    .scaleEffect(1.2)

                Spacer()

                // Coin display
                if let player = playerStore.activePlayer {
                    coinDisplay(coins: player.coins)
                }

                // Treasure chest icon
                treasureChestIcon

                // Placeholder text
                placeholderInfo

                Spacer()
            }
            .padding()
        }
    }

    // MARK: - Back Button

    private var backButton: some View {
        Button {
            coordinator.navigateHome()
        } label: {
            HStack(spacing: 8) {
                Image(systemName: "arrow.left")
                    .font(.system(size: 24))
                Text("Zurück")
                    .font(BennieFont.button(20))
            }
            .foregroundColor(BennieColors.textOnWood)
            .frame(minWidth: 96, minHeight: 96)
            .background(
                Capsule()
                    .fill(BennieColors.woodLight)
                    .overlay(
                        Capsule()
                            .stroke(BennieColors.woodDark, lineWidth: 2)
                    )
            )
        }
        .buttonStyle(.plain)
    }

    // MARK: - Coin Display

    private func coinDisplay(coins: Int) -> some View {
        HStack(spacing: 12) {
            Text("🪙")
                .font(.system(size: 48))
            Text("\(coins)")
                .font(BennieFont.number())
                .foregroundColor(BennieColors.coinGold)
            Text("Münzen")
                .font(BennieFont.screenHeader())
                .foregroundColor(BennieColors.textDark)
        }
        .padding(.horizontal, 32)
        .padding(.vertical, 16)
        .background(
            RoundedRectangle(cornerRadius: 20)
                .fill(BennieColors.woodLight.opacity(0.5))
                .overlay(
                    RoundedRectangle(cornerRadius: 20)
                        .stroke(BennieColors.coinGold, lineWidth: 2)
                )
        )
    }

    // MARK: - Treasure Chest Icon

    private var treasureChestIcon: some View {
        VStack(spacing: 8) {
            Image(systemName: "shippingbox.fill")
                .font(.system(size: 120))
                .foregroundColor(BennieColors.coinGold)
                .shadow(color: BennieColors.coinGold.opacity(0.5), radius: 20)

            // Sparkle effect
            HStack(spacing: 30) {
                ForEach(0..<3, id: \.self) { _ in
                    Image(systemName: "sparkle")
                        .font(.system(size: 20))
                        .foregroundColor(BennieColors.coinGold.opacity(0.7))
                }
            }
        }
    }

    // MARK: - Placeholder Info

    private var placeholderInfo: some View {
        VStack(spacing: 16) {
            Text("YouTube-Belohnungen kommen in Phase 4")
                .font(BennieFont.body())
                .foregroundColor(BennieColors.textDark.opacity(0.7))

            Text("10 Münzen = 5 Minuten YouTube")
                .font(BennieFont.label())
                .foregroundColor(BennieColors.textDark.opacity(0.5))

            Text("20 Münzen = 12 Minuten YouTube")
                .font(BennieFont.label())
                .foregroundColor(BennieColors.textDark.opacity(0.5))
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 12)
                .stroke(BennieColors.woodMedium.opacity(0.3), lineWidth: 1)
        )
    }
}

// MARK: - Previews

#Preview("TreasureView - Few Coins") {
    let store = PlayerStore()
    store.selectPlayer(id: "alexander")

    return TreasureView()
        .environment(AppCoordinator())
        .environment(store)
}

#Preview("TreasureView - Many Coins") {
    let store = PlayerStore()
    store.selectPlayer(id: "alexander")
    for _ in 0..<15 {
        store.awardCoin()
    }

    return TreasureView()
        .environment(AppCoordinator())
        .environment(store)
}
