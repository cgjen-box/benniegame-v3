import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// ProgressBar - Coin progress indicator
// ═══════════════════════════════════════════════════════════════════════════
// Shows current coins with animated fill, berry decorations, and chest icons
// Used in navigation header across all activity screens
// Enhanced with coin slot animations for satisfying reward feedback
// ═══════════════════════════════════════════════════════════════════════════

/// Progress bar showing coin collection toward YouTube rewards
/// Displays 0-20 coins with animated fill and milestone indicators
struct ProgressBar: View {
    let currentCoins: Int
    let maxCoins: Int

    // MARK: - Animation State

    /// Track which slot is currently animating (glowing)
    @State private var animatingSlot: Int? = nil

    /// Track previous coin count to detect changes
    @State private var previousCoins: Int = 0

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
        .onChange(of: currentCoins) { oldValue, newValue in
            handleCoinChange(from: oldValue, to: newValue)
        }
        .onAppear {
            previousCoins = currentCoins
        }
    }

    private var progressTrough: some View {
        GeometryReader { geo in
            ZStack(alignment: .leading) {
                // Wood trough background
                RoundedRectangle(cornerRadius: 8)
                    .fill(BennieColors.woodDark)

                // Success fill with spring animation
                RoundedRectangle(cornerRadius: 8)
                    .fill(BennieColors.success)
                    .frame(width: geo.size.width * fillPercentage)
                    .animation(.spring(response: 0.4, dampingFraction: 0.7), value: currentCoins)

                // Coin slots overlay with animation state
                CoinSlots(
                    currentCoins: currentCoins,
                    slotCount: min(maxCoins, 10),
                    animatingSlot: animatingSlot
                )
            }
        }
        .frame(height: 40)
    }

    // MARK: - Coin Change Animation

    private func handleCoinChange(from oldValue: Int, to newValue: Int) {
        // Only animate when coins increase
        guard newValue > oldValue else { return }

        // Calculate slot index (0-based, wrapping at 10)
        let slotIndex = (newValue - 1) % 10

        // Trigger slot glow animation
        withAnimation(.easeIn(duration: 0.1)) {
            animatingSlot = slotIndex
        }

        // Clear animation after pulse completes
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.6) {
            withAnimation(.easeOut(duration: 0.2)) {
                animatingSlot = nil
            }
        }

        previousCoins = newValue
    }

    @ViewBuilder
    private var chestIndicators: some View {
        HStack(spacing: 4) {
            if hasFirstChest {
                ChestIcon(
                    isGlowing: !hasSecondChest,
                    isNew: currentCoins == 10
                )
            }
            if hasSecondChest {
                ChestIcon(
                    isGlowing: true,
                    isNew: currentCoins == 20
                )
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

    /// Index of the slot currently being animated (newly earned coin)
    var animatingSlot: Int? = nil

    var body: some View {
        HStack(spacing: 4) {
            ForEach(0..<slotCount, id: \.self) { index in
                CoinSlot(
                    isFilled: index < (currentCoins % 10 == 0 && currentCoins >= 10 ? 10 : currentCoins % 10),
                    isAnimating: animatingSlot == index
                )
            }
        }
        .padding(.horizontal, 8)
    }
}

// MARK: - Individual Coin Slot

/// Single coin slot with animation support
private struct CoinSlot: View {
    let isFilled: Bool
    let isAnimating: Bool

    @State private var pulseScale: CGFloat = 1.0

    var body: some View {
        ZStack {
            // Base slot
            Circle()
                .fill(isFilled ? BennieColors.coinGold : Color.clear)
                .overlay(
                    Circle()
                        .stroke(BennieColors.woodLight.opacity(0.5), lineWidth: 1)
                )

            // Glow effect when animating
            if isAnimating {
                Circle()
                    .fill(BennieColors.coinGold)
                    .shadow(color: BennieColors.coinGold.opacity(0.8), radius: 8)
                    .scaleEffect(pulseScale)
            }
        }
        .frame(width: 12, height: 12)
        .scaleEffect(isAnimating ? pulseScale : 1.0)
        .onChange(of: isAnimating) { _, newValue in
            if newValue {
                // Pulse animation: 1.0 -> 1.3 -> 1.0
                withAnimation(.spring(response: 0.2, dampingFraction: 0.5)) {
                    pulseScale = 1.3
                }
                DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) {
                    withAnimation(.spring(response: 0.3, dampingFraction: 0.6)) {
                        pulseScale = 1.0
                    }
                }
            }
        }
    }
}

// MARK: - Chest Icon

/// Treasure chest icon shown at coin milestones
struct ChestIcon: View {
    var isGlowing: Bool = false

    /// Whether this chest just appeared (for entrance animation)
    var isNew: Bool = false

    @State private var scale: CGFloat = 0.5
    @State private var opacity: Double = 0.0

    var body: some View {
        Image(systemName: "shippingbox.fill")
            .font(.system(size: 24))
            .foregroundColor(BennieColors.coinGold)
            .shadow(
                color: isGlowing ? BennieColors.coinGold.opacity(0.6) : .clear,
                radius: isGlowing ? 4 : 0
            )
            .scaleEffect(isNew ? scale : 1.0)
            .opacity(isNew ? opacity : 1.0)
            .onAppear {
                if isNew {
                    // Bounce-in animation for new chest
                    withAnimation(.spring(response: 0.4, dampingFraction: 0.6)) {
                        scale = 1.0
                        opacity = 1.0
                    }
                }
            }
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
