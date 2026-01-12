import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// HomeView - Main menu screen with activity selection
// ═══════════════════════════════════════════════════════════════════════════
// Shows 4 activity signs (2 unlocked, 2 locked), treasure chest, and settings
// Bennie placeholder on right side, cream background
// ═══════════════════════════════════════════════════════════════════════════

/// Home screen with activity selection and navigation
struct HomeView: View {
    // MARK: - Environment

    @Environment(AppCoordinator.self) private var coordinator
    @Environment(PlayerStore.self) private var playerStore

    // MARK: - State

    @State private var showingTreasureMessage = false

    // MARK: - Body

    var body: some View {
        ZStack {
            // Background
            BennieColors.cream
                .ignoresSafeArea()

            // Main content
            VStack(spacing: 0) {
                // Title sign at top
                titleSection
                    .padding(.top, 20)

                Spacer()

                // Activity signs in horizontal row
                activitySignsSection

                Spacer()

                // Bottom row: Settings, Treasure, Bennie
                bottomSection
                    .padding(.bottom, 32)
            }
            .padding(.horizontal, 24)
        }
    }

    // MARK: - Title Section

    private var titleSection: some View {
        WoodSign(title: "Waldabenteuer")
            .scaleEffect(1.3)
    }

    // MARK: - Activity Signs Section

    private var activitySignsSection: some View {
        HStack(spacing: 24) {
            ForEach(ActivityType.allCases, id: \.self) { activity in
                ActivitySignView(
                    activity: activity,
                    onTap: {
                        handleActivityTap(activity)
                    }
                )
            }
        }
    }

    // MARK: - Bottom Section

    private var bottomSection: some View {
        HStack {
            // Settings gear - bottom left
            settingsButton

            Spacer()

            // Player info (small)
            if let player = playerStore.activePlayer {
                playerInfoBadge(player: player)
            }

            Spacer()

            // Treasure chest - bottom right
            treasureChestButton

            // Bennie placeholder - far right
            bennieCharacter
        }
    }

    // MARK: - Settings Button

    private var settingsButton: some View {
        Button {
            coordinator.showParentGate()
        } label: {
            Image(systemName: "gearshape.fill")
                .font(.system(size: 36))
                .foregroundColor(BennieColors.woodDark)
                .frame(width: 96, height: 96)
                .background(
                    Circle()
                        .fill(BennieColors.woodLight)
                        .overlay(
                            Circle()
                                .stroke(BennieColors.woodDark, lineWidth: 2)
                        )
                )
        }
        .buttonStyle(.plain)
    }

    // MARK: - Player Info Badge

    private func playerInfoBadge(player: PlayerData) -> some View {
        VStack(spacing: 4) {
            Text(player.name)
                .font(BennieFont.label())
            HStack(spacing: 4) {
                Text("🪙")
                Text("\(player.coins)")
                    .font(BennieFont.button(20))
            }
        }
        .foregroundColor(BennieColors.textDark)
        .padding(.horizontal, 16)
        .padding(.vertical, 8)
        .background(
            RoundedRectangle(cornerRadius: 12)
                .fill(BennieColors.cream)
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(BennieColors.woodMedium, lineWidth: 1)
                )
        )
    }

    // MARK: - Treasure Chest Button

    private var treasureChestButton: some View {
        Button {
            handleTreasureTap()
        } label: {
            VStack(spacing: 4) {
                Image(systemName: canAccessTreasure ? "shippingbox.fill" : "shippingbox")
                    .font(.system(size: 48))
                    .foregroundColor(canAccessTreasure ? BennieColors.coinGold : BennieColors.woodMedium)
                Text("Schatztruhe")
                    .font(BennieFont.label(14))
                    .foregroundColor(BennieColors.textOnWood)
            }
            .frame(width: 120, height: 96)
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .fill(BennieColors.woodLight)
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(BennieColors.woodDark, lineWidth: 2)
                    )
            )
            .overlay(
                // Glow effect when accessible
                RoundedRectangle(cornerRadius: 12)
                    .stroke(BennieColors.coinGold, lineWidth: canAccessTreasure ? 3 : 0)
                    .blur(radius: canAccessTreasure ? 4 : 0)
            )
        }
        .buttonStyle(.plain)
        .overlay(
            // Message popup when not enough coins
            treasureMessageOverlay
        )
    }

    @ViewBuilder
    private var treasureMessageOverlay: some View {
        if showingTreasureMessage, let player = playerStore.activePlayer {
            let coinsNeeded = 10 - player.coins
            Text("Noch \(coinsNeeded) Münzen!")
                .font(BennieFont.label())
                .foregroundColor(BennieColors.textOnWood)
                .padding(.horizontal, 12)
                .padding(.vertical, 6)
                .background(
                    Capsule()
                        .fill(BennieColors.woodLight)
                        .shadow(radius: 2)
                )
                .offset(y: -60)
                .transition(.scale.combined(with: .opacity))
        }
    }

    // MARK: - Bennie Character

    private var bennieCharacter: some View {
        VStack(spacing: 4) {
            Image(systemName: "bear.fill")
                .font(.system(size: 80))
                .foregroundColor(BennieColors.bennieBrown)
            Text("Bennie")
                .font(BennieFont.label(12))
                .foregroundColor(BennieColors.textDark)
        }
        .padding(.leading, 16)
    }

    // MARK: - Computed Properties

    private var canAccessTreasure: Bool {
        (playerStore.activePlayer?.coins ?? 0) >= 10
    }

    // MARK: - Actions

    private func handleActivityTap(_ activity: ActivityType) {
        guard !activity.isLocked else {
            // Locked activities do nothing on tap (visual indication via WoodSign)
            return
        }
        coordinator.navigateToActivity(activity)
    }

    private func handleTreasureTap() {
        if canAccessTreasure {
            coordinator.navigateToTreasure()
        } else {
            // Show message briefly
            withAnimation(.spring(duration: 0.3)) {
                showingTreasureMessage = true
            }
            // Hide after delay
            DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                withAnimation(.easeOut(duration: 0.3)) {
                    showingTreasureMessage = false
                }
            }
        }
    }
}

// MARK: - Activity Sign View

/// Individual activity sign with locked/unlocked state
private struct ActivitySignView: View {
    let activity: ActivityType
    let onTap: () -> Void

    var body: some View {
        VStack(spacing: 0) {
            WoodSign(
                title: activity.displayName,
                isLocked: activity.isLocked,
                action: activity.isLocked ? nil : onTap
            )

            // Activity icon below sign
            Image(systemName: activity.iconName)
                .font(.system(size: 28))
                .foregroundColor(activity.isLocked ? BennieColors.chain : BennieColors.woodDark)
                .padding(.top, 8)
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

#Preview("HomeView - Many Coins") {
    let store = PlayerStore()
    store.selectPlayer(id: "alexander")
    // Award coins for testing
    for _ in 0..<15 {
        store.awardCoin()
    }

    return HomeView()
        .environment(AppCoordinator())
        .environment(store)
}
