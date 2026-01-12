import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// ProgressBar - Coin progress indicator
// ═══════════════════════════════════════════════════════════════════════════
// Shows current coins with animated fill, berry decorations, and chest icons
// Used in navigation header across all activity screens
// ═══════════════════════════════════════════════════════════════════════════

/// Progress bar showing coin collection toward YouTube rewards
/// Displays 0-20 coins with animated fill and milestone indicators
struct ProgressBar: View {
    let currentCoins: Int
    let maxCoins: Int

    /// Initialize with current coin count
    /// - Parameters:
    ///   - currentCoins: Number of coins earned (0+)
    ///   - maxCoins: Maximum coins for full bar (default 20)
    init(currentCoins: Int, maxCoins: Int = 20) {
        self.currentCoins = currentCoins
        self.maxCoins = maxCoins
    }

    private var fillPercentage: CGFloat {
        min(CGFloat(currentCoins) / CGFloat(maxCoins), 1.0)
    }

    private var hasFirstChest: Bool { currentCoins >= 10 }
    private var hasSecondChest: Bool { currentCoins >= 20 }

    var body: some View {
        HStack(spacing: 12) {
            // Berry decoration (left)
            BerryCluster()

            // Progress trough
            progressTrough

            // Berry decoration (right)
            BerryCluster()

            // Chest icons for milestones
            chestIndicators
        }
        .padding(.horizontal, 16)
    }

    private var progressTrough: some View {
        GeometryReader { geo in
            ZStack(alignment: .leading) {
                // Wood trough background
                RoundedRectangle(cornerRadius: 8)
                    .fill(BennieColors.woodDark)

                // Success fill
                RoundedRectangle(cornerRadius: 8)
                    .fill(BennieColors.success)
                    .frame(width: geo.size.width * fillPercentage)
                    .animation(.easeInOut(duration: 0.3), value: currentCoins)

                // Coin slots overlay
                CoinSlots(currentCoins: currentCoins, slotCount: min(maxCoins, 10))
            }
        }
        .frame(height: 40)
    }

    @ViewBuilder
    private var chestIndicators: some View {
        HStack(spacing: 4) {
            if hasFirstChest {
                ChestIcon(isGlowing: !hasSecondChest)
            }
            if hasSecondChest {
                ChestIcon(isGlowing: true)
                    .overlay(
                        Text("BONUS")
                            .font(BennieFont.label(10))
                            .foregroundColor(BennieColors.coinGold)
                            .offset(y: 20)
                    )
            }
        }
    }
}

// MARK: - Berry Cluster

/// Decorative berry cluster for progress bar ends
struct BerryCluster: View {
    var body: some View {
        HStack(spacing: -4) {
            berry(size: 12)
            berry(size: 16)
            berry(size: 12)
        }
    }

    private func berry(size: CGFloat) -> some View {
        Circle()
            // Using a muted red, not pure #FF0000 (forbidden)
            .fill(Color(red: 0.75, green: 0.2, blue: 0.2))
            .frame(width: size, height: size)
    }
}

// MARK: - Coin Slots

/// Individual coin slot indicators within the progress bar
struct CoinSlots: View {
    let currentCoins: Int
    let slotCount: Int

    var body: some View {
        HStack(spacing: 4) {
            ForEach(0..<slotCount, id: \.self) { index in
                Circle()
                    .fill(index < currentCoins ? BennieColors.coinGold : Color.clear)
                    .overlay(
                        Circle()
                            .stroke(BennieColors.woodLight.opacity(0.5), lineWidth: 1)
                    )
                    .frame(width: 12, height: 12)
            }
        }
        .padding(.horizontal, 8)
    }
}

// MARK: - Chest Icon

/// Treasure chest icon shown at coin milestones
struct ChestIcon: View {
    var isGlowing: Bool = false

    var body: some View {
        Image(systemName: "shippingbox.fill")
            .font(.system(size: 24))
            .foregroundColor(BennieColors.coinGold)
            .shadow(
                color: isGlowing ? BennieColors.coinGold.opacity(0.6) : .clear,
                radius: isGlowing ? 4 : 0
            )
    }
}

// MARK: - Previews

#Preview("ProgressBar - Empty") {
    ProgressBar(currentCoins: 0)
        .frame(width: 400)
        .padding()
}

#Preview("ProgressBar - Partial") {
    ProgressBar(currentCoins: 7)
        .frame(width: 400)
        .padding()
}

#Preview("ProgressBar - First Chest") {
    ProgressBar(currentCoins: 12)
        .frame(width: 400)
        .padding()
}

#Preview("ProgressBar - Full") {
    ProgressBar(currentCoins: 20)
        .frame(width: 400)
        .padding()
}

#Preview("ProgressBar - Animation") {
    struct AnimatedPreview: View {
        @State private var coins = 0

        var body: some View {
            VStack {
                ProgressBar(currentCoins: coins)
                    .frame(width: 400)

                Button("Add Coin") {
                    if coins < 20 {
                        coins += 1
                    }
                }
                .padding()
            }
        }
    }

    return AnimatedPreview()
}
