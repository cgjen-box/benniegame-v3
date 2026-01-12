import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// TreasureView - Treasure chest screen for YouTube redemption
// ═══════════════════════════════════════════════════════════════════════════
// Complete implementation with redemption buttons for YouTube time
// 10 coins = 5 minutes, 20 coins = 12 minutes
// ═══════════════════════════════════════════════════════════════════════════

/// Treasure screen for redeeming coins for YouTube time
struct TreasureView: View {
    // MARK: - Environment

    @Environment(AppCoordinator.self) private var coordinator
    @Environment(PlayerStore.self) private var playerStore
    @Environment(AudioManager.self) private var audioManager
    @Environment(BennieService.self) private var bennie

    // MARK: - State

    @State private var chestScale: CGFloat = 1.0
    @State private var sparkleOpacity: Double = 1.0

    // MARK: - Body

    var body: some View {
        ZStack {
            // Background
            BennieColors.cream
                .ignoresSafeArea()

            VStack(spacing: 24) {
                // Navigation header
                navigationHeader

                // Title sign
                WoodSign(title: "Schatztruhe")
                    .scaleEffect(1.3)

                Spacer()

                // Coin display
                if let player = playerStore.activePlayer {
                    coinDisplay(coins: player.coins)
                }

                // Treasure chest
                treasureChest

                // Redemption buttons
                redemptionButtons

                Spacer()
            }
            .padding()
        }
        .onAppear {
            startAnimations()
            // Play treasure chest audio
            audioManager.playEffect(.chestOpen)
            if let player = playerStore.activePlayer {
                bennie.playTreasureMessage(coins: player.coins)
            }
        }
    }

    // MARK: - Navigation Header

    private var navigationHeader: some View {
        HStack {
            // Home button
            Button {
                coordinator.navigateHome()
            } label: {
                HStack(spacing: 8) {
                    Image(systemName: "house.fill")
                        .font(.system(size: 24))
                    Text("Zurück")
                        .font(BennieFont.button(18))
                }
                .foregroundColor(BennieColors.textOnWood)
                .frame(minWidth: 96, minHeight: 96)
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
                        .stroke(BennieColors.woodDark, lineWidth: 2)
                )
            }
            .buttonStyle(.plain)

            Spacer()

            // Coin display in header
            if let player = playerStore.activePlayer {
                HStack(spacing: 8) {
                    Text("🪙")
                        .font(.system(size: 28))
                    Text("\(player.coins)")
                        .font(BennieFont.number())
                        .foregroundColor(BennieColors.coinGold)
                }
                .padding(.horizontal, 20)
                .padding(.vertical, 12)
                .background(
                    Capsule()
                        .fill(BennieColors.woodLight.opacity(0.8))
                        .overlay(
                            Capsule()
                                .stroke(BennieColors.coinGold, lineWidth: 2)
                        )
                )
            }
        }
        .padding(.horizontal)
    }

    // MARK: - Coin Display

    private func coinDisplay(coins: Int) -> some View {
        VStack(spacing: 8) {
            HStack(spacing: 16) {
                Text("🪙")
                    .font(.system(size: 64))
                Text("\(coins)")
                    .font(BennieFont.number())
                    .foregroundColor(BennieColors.coinGold)
                Text("Münzen")
                    .font(BennieFont.screenHeader())
                    .foregroundColor(BennieColors.textDark)
            }

            // Show coins needed message if not enough
            if coins < 10 {
                Text("Noch \(10 - coins) Münzen bis YouTube!")
                    .font(BennieFont.body())
                    .foregroundColor(BennieColors.textDark.opacity(0.7))
            }
        }
        .padding(.horizontal, 40)
        .padding(.vertical, 20)
        .background(
            RoundedRectangle(cornerRadius: 24)
                .fill(BennieColors.woodLight.opacity(0.4))
                .overlay(
                    RoundedRectangle(cornerRadius: 24)
                        .stroke(BennieColors.coinGold, lineWidth: 3)
                )
        )
    }

    // MARK: - Treasure Chest

    private var treasureChest: some View {
        VStack(spacing: 12) {
            // Chest icon using SF Symbol
            ZStack {
                // Glow behind chest
                Circle()
                    .fill(
                        RadialGradient(
                            colors: [
                                BennieColors.coinGold.opacity(0.4),
                                BennieColors.coinGold.opacity(0.1),
                                Color.clear
                            ],
                            center: .center,
                            startRadius: 40,
                            endRadius: 120
                        )
                    )
                    .frame(width: 240, height: 240)

                // Chest
                Image(systemName: "shippingbox.fill")
                    .font(.system(size: 140))
                    .foregroundStyle(
                        LinearGradient(
                            colors: [BennieColors.coinGold, BennieColors.woodMedium],
                            startPoint: .top,
                            endPoint: .bottom
                        )
                    )
                    .shadow(color: BennieColors.coinGold.opacity(0.5), radius: 20)
                    .scaleEffect(chestScale)
            }

            // Sparkles
            HStack(spacing: 40) {
                ForEach(0..<3, id: \.self) { index in
                    Image(systemName: "sparkle")
                        .font(.system(size: 24))
                        .foregroundColor(BennieColors.coinGold)
                        .opacity(sparkleOpacity)
                        .offset(y: index == 1 ? -10 : 0)
                }
            }
        }
    }

    // MARK: - Redemption Buttons

    private var redemptionButtons: some View {
        HStack(spacing: 40) {
            // 5 Min YouTube Button (10 coins)
            redemptionButton(
                title: "5 Min YouTube",
                cost: 10,
                minutes: 5,
                isEnabled: playerStore.activePlayer?.canRedeemTier1 ?? false
            )

            // 12 Min YouTube Button (20 coins)
            redemptionButton(
                title: "12 Min YouTube",
                cost: 20,
                minutes: 12,
                isEnabled: playerStore.activePlayer?.canRedeemTier2 ?? false
            )
        }
    }

    private func redemptionButton(
        title: String,
        cost: Int,
        minutes: Int,
        isEnabled: Bool
    ) -> some View {
        Button {
            if playerStore.spendCoins(cost) {
                coordinator.allocatedVideoMinutes = minutes
                coordinator.navigateToVideoSelection()
            }
        } label: {
            VStack(spacing: 12) {
                // YouTube icon
                Image(systemName: "play.rectangle.fill")
                    .font(.system(size: 40))

                // Title
                Text(title)
                    .font(BennieFont.button(22))

                // Cost
                HStack(spacing: 4) {
                    Text("🪙")
                        .font(.system(size: 20))
                    Text("\(cost) Münzen")
                        .font(BennieFont.label())
                }

                // Lock icon if disabled
                if !isEnabled {
                    Image(systemName: "lock.fill")
                        .font(.system(size: 24))
                        .foregroundColor(BennieColors.chain)
                }
            }
            .foregroundColor(isEnabled ? BennieColors.textOnWood : BennieColors.textOnWood.opacity(0.5))
            .frame(width: 200, height: 200)
            .background(
                RoundedRectangle(cornerRadius: 20)
                    .fill(
                        LinearGradient(
                            colors: isEnabled
                                ? [BennieColors.woodLight, BennieColors.woodMedium]
                                : [BennieColors.woodLight.opacity(0.5), BennieColors.woodMedium.opacity(0.5)],
                            startPoint: .top,
                            endPoint: .bottom
                        )
                    )
            )
            .overlay(
                RoundedRectangle(cornerRadius: 20)
                    .stroke(
                        isEnabled ? BennieColors.coinGold : BennieColors.chain,
                        lineWidth: 3
                    )
            )
            .shadow(
                color: isEnabled ? BennieColors.coinGold.opacity(0.3) : Color.clear,
                radius: 10
            )
            .opacity(isEnabled ? 1.0 : 0.6)
        }
        .buttonStyle(.plain)
        .disabled(!isEnabled)
    }

    // MARK: - Animations

    private func startAnimations() {
        // Chest breathing animation
        withAnimation(.easeInOut(duration: 2.0).repeatForever(autoreverses: true)) {
            chestScale = 1.05
        }

        // Sparkle pulsing animation
        withAnimation(.easeInOut(duration: 1.5).repeatForever(autoreverses: true)) {
            sparkleOpacity = 0.4
        }
    }
}

// MARK: - Previews

#Preview("TreasureView - No Coins") {
    let store = PlayerStore()
    store.selectPlayer(id: "alexander")
    let audioManager = AudioManager()

    return TreasureView()
        .environment(AppCoordinator())
        .environment(store)
        .environment(audioManager)
        .environment(BennieService(audioManager: audioManager))
}

#Preview("TreasureView - 10 Coins") {
    let store = PlayerStore()
    store.selectPlayer(id: "alexander")
    for _ in 0..<10 {
        store.awardCoin()
    }
    let audioManager = AudioManager()

    return TreasureView()
        .environment(AppCoordinator())
        .environment(store)
        .environment(audioManager)
        .environment(BennieService(audioManager: audioManager))
}

#Preview("TreasureView - 20 Coins") {
    let store = PlayerStore()
    store.selectPlayer(id: "alexander")
    for _ in 0..<20 {
        store.awardCoin()
    }
    let audioManager = AudioManager()

    return TreasureView()
        .environment(AppCoordinator())
        .environment(store)
        .environment(audioManager)
        .environment(BennieService(audioManager: audioManager))
}
