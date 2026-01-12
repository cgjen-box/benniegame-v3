import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// CoinFlyAnimation - Animated coin flying to progress bar
// ═══════════════════════════════════════════════════════════════════════════
// Shows an animated coin flying from a source point to the progress bar
// Used when children earn coins for correct answers
// Duration: 0.8s with arc trajectory
// ═══════════════════════════════════════════════════════════════════════════

/// Animated coin that flies from source position to progress bar with arc trajectory
struct CoinFlyAnimation: View {
    // MARK: - Properties

    /// Starting position for the animation (in global coordinates)
    let startPosition: CGPoint

    /// Target position for the coin (typically progress bar location)
    var targetPosition: CGPoint = CGPoint(x: UIScreen.main.bounds.width / 2, y: 80)

    /// Callback when animation completes
    var onComplete: (() -> Void)? = nil

    // MARK: - Animation State

    @State private var animationProgress: CGFloat = 0
    @State private var opacity: CGFloat = 1
    @State private var scale: CGFloat = 1.2
    @State private var sparkles: [SparkleData] = []

    // MARK: - Constants

    private let animationDuration: Double = 0.8
    private let coinSize: CGFloat = 50
    private let arcHeight: CGFloat = -80 // Negative for upward arc

    // MARK: - Computed Properties

    /// Current position along the arc trajectory
    private var currentPosition: CGPoint {
        let progress = animationProgress

        // Linear interpolation for x
        let x = startPosition.x + (targetPosition.x - startPosition.x) * progress

        // Parabolic arc for y (quadratic bezier-like curve)
        let linearY = startPosition.y + (targetPosition.y - startPosition.y) * progress
        let arcOffset = arcHeight * 4 * progress * (1 - progress) // Parabola peaking at 0.5
        let y = linearY + arcOffset

        return CGPoint(x: x, y: y)
    }

    // MARK: - Body

    var body: some View {
        ZStack {
            // Sparkle trail
            ForEach(sparkles) { sparkle in
                Circle()
                    .fill(BennieColors.coinGold.opacity(sparkle.opacity))
                    .frame(width: sparkle.size, height: sparkle.size)
                    .position(sparkle.position)
            }

            // Main coin
            coinView
                .position(currentPosition)
                .scaleEffect(scale)
                .opacity(opacity)
        }
        .onAppear {
            startAnimation()
        }
    }

    // MARK: - Coin View

    private var coinView: some View {
        ZStack {
            // Outer ring
            Circle()
                .fill(BennieColors.coinGold)
                .frame(width: coinSize, height: coinSize)
                .shadow(color: BennieColors.coinGold.opacity(0.6), radius: 8)

            // Inner detail
            Circle()
                .fill(BennieColors.coinGold.opacity(0.8))
                .frame(width: coinSize * 0.75, height: coinSize * 0.75)

            // Shine effect (using cream for autism-friendly highlight)
            Circle()
                .fill(
                    LinearGradient(
                        colors: [BennieColors.cream.opacity(0.6), .clear],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )
                .frame(width: coinSize * 0.6, height: coinSize * 0.6)
                .offset(x: -5, y: -5)

            // Center emblem
            Text("★")
                .font(.system(size: coinSize * 0.4, weight: .bold))
                .foregroundColor(BennieColors.woodDark.opacity(0.5))
        }
    }

    // MARK: - Animation Logic

    private func startAnimation() {
        // Generate initial sparkles
        generateSparkleTrail()

        // Animate position along arc
        withAnimation(.easeOut(duration: animationDuration)) {
            animationProgress = 1.0
        }

        // Animate scale (shrink as it lands)
        withAnimation(.easeInOut(duration: animationDuration)) {
            scale = 0.6
        }

        // Fade out at the end
        withAnimation(.easeIn(duration: 0.2).delay(animationDuration - 0.2)) {
            opacity = 0
        }

        // Complete callback
        DispatchQueue.main.asyncAfter(deadline: .now() + animationDuration) {
            onComplete?()
        }
    }

    private func generateSparkleTrail() {
        // Create sparkles that follow the coin with delay
        for i in 0..<8 {
            let delay = Double(i) * 0.08

            DispatchQueue.main.asyncAfter(deadline: .now() + delay) {
                let sparkle = SparkleData(
                    id: UUID(),
                    position: currentPosition,
                    size: CGFloat.random(in: 4...12),
                    opacity: Double.random(in: 0.4...0.8)
                )
                sparkles.append(sparkle)

                // Fade out sparkle
                withAnimation(.easeOut(duration: 0.4)) {
                    if let index = sparkles.firstIndex(where: { $0.id == sparkle.id }) {
                        sparkles[index].opacity = 0
                    }
                }

                // Remove sparkle after fade
                DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
                    sparkles.removeAll { $0.id == sparkle.id }
                }
            }
        }
    }
}

// MARK: - Sparkle Data

/// Data for individual sparkle particles in the trail
private struct SparkleData: Identifiable {
    let id: UUID
    var position: CGPoint
    var size: CGFloat
    var opacity: Double
}

// MARK: - View Extension for Easy Usage

extension View {
    /// Overlays a coin fly animation when triggered
    /// - Parameters:
    ///   - isPresented: Binding to control animation visibility
    ///   - startPosition: Starting point for the coin
    ///   - targetPosition: End point (defaults to progress bar area)
    ///   - onComplete: Callback when animation finishes
    func coinFlyAnimation(
        isPresented: Binding<Bool>,
        startPosition: CGPoint,
        targetPosition: CGPoint = CGPoint(x: UIScreen.main.bounds.width / 2, y: 80),
        onComplete: @escaping () -> Void
    ) -> some View {
        self.overlay {
            if isPresented.wrappedValue {
                CoinFlyAnimation(
                    startPosition: startPosition,
                    targetPosition: targetPosition,
                    onComplete: {
                        isPresented.wrappedValue = false
                        onComplete()
                    }
                )
            }
        }
    }
}

// MARK: - Previews

#Preview("CoinFlyAnimation") {
    struct PreviewContainer: View {
        @State private var showAnimation = false
        @State private var startPoint = CGPoint(x: 200, y: 500)

        var body: some View {
            ZStack {
                BennieColors.cream.ignoresSafeArea()

                VStack {
                    // Target area (simulated progress bar)
                    HStack {
                        Spacer()
                        RoundedRectangle(cornerRadius: 8)
                            .fill(BennieColors.woodDark)
                            .frame(width: 200, height: 40)
                            .overlay(
                                Text("Fortschritt")
                                    .font(BennieFont.label())
                                    .foregroundColor(BennieColors.textOnWood)
                            )
                        Spacer()
                    }
                    .padding(.top, 40)

                    Spacer()

                    // Trigger button
                    Button {
                        startPoint = CGPoint(x: 200, y: 500)
                        showAnimation = true
                    } label: {
                        Text("Richtige Antwort!")
                            .font(BennieFont.button())
                            .foregroundColor(BennieColors.textOnWood)
                            .padding()
                            .background(
                                RoundedRectangle(cornerRadius: 16)
                                    .fill(BennieColors.success)
                            )
                    }
                    .padding(.bottom, 100)
                }

                // Animation overlay
                if showAnimation {
                    CoinFlyAnimation(
                        startPosition: startPoint,
                        targetPosition: CGPoint(x: UIScreen.main.bounds.width / 2, y: 60),
                        onComplete: {
                            showAnimation = false
                        }
                    )
                }
            }
        }
    }

    return PreviewContainer()
}

#Preview("CoinFlyAnimation - Multiple") {
    struct MultiplePreview: View {
        @State private var animations: [UUID] = []

        var body: some View {
            ZStack {
                BennieColors.cream.ignoresSafeArea()

                VStack {
                    Text("Tippe um Muenzen zu sammeln!")
                        .font(BennieFont.body())
                        .padding(.top, 100)

                    Spacer()
                }

                ForEach(animations, id: \.self) { id in
                    CoinFlyAnimation(
                        startPosition: CGPoint(
                            x: CGFloat.random(in: 100...300),
                            y: CGFloat.random(in: 400...600)
                        ),
                        onComplete: {
                            animations.removeAll { $0 == id }
                        }
                    )
                }
            }
            .onTapGesture {
                animations.append(UUID())
            }
        }
    }

    return MultiplePreview()
}
