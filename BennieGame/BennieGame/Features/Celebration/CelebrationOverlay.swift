import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// CelebrationOverlay - Joyful milestone celebration
// ═══════════════════════════════════════════════════════════════════════════
// Displays when player reaches coin milestones (every 5 coins)
// Shows confetti, positive messages, and navigation options
// German only, positive feedback only - never "Falsch"
// ═══════════════════════════════════════════════════════════════════════════

/// Celebration overlay shown at coin milestones (5, 10, 15, 20...)
struct CelebrationOverlay: View {
    // MARK: - Environment

    @Environment(AppCoordinator.self) private var coordinator
    @Environment(PlayerStore.self) private var playerStore
    @Environment(AudioManager.self) private var audioManager
    @Environment(BennieService.self) private var bennie

    // MARK: - Properties

    /// The total coins the player now has
    let coinsEarned: Int

    // MARK: - Computed Properties

    /// Returns milestone-specific celebration message in German
    private var milestoneMessage: String {
        switch coinsEarned {
        case 5: return "Wir haben schon fünf Goldmünzen!"
        case 10: return "Zehn Goldmünzen! Du kannst jetzt YouTube schauen."
        case 15: return "Fünfzehn! Weiter so!"
        case 20: return "Zwanzig Münzen! Du bekommst Bonuszeit!"
        default: return "Super gemacht!"
        }
    }

    /// Whether the treasure button should be shown
    private var canAccessTreasure: Bool {
        coinsEarned >= 10
    }

    // MARK: - Body

    var body: some View {
        ZStack {
            // Semi-transparent background overlay (woodDark for autism-friendly dimming)
            BennieColors.woodDark.opacity(0.6)
                .ignoresSafeArea()

            // Confetti animation layer (behind content)
            ConfettiView()
                .ignoresSafeArea()

            // Content card
            VStack(spacing: 24) {
                // Main celebration title
                Text("Super gemacht!")
                    .font(BennieFont.celebration())
                    .foregroundColor(BennieColors.coinGold)

                // Large coin count display
                HStack(spacing: 8) {
                    Image(systemName: "circle.fill")
                        .font(.system(size: 48))
                        .foregroundColor(BennieColors.coinGold)

                    Text("\(coinsEarned)")
                        .font(BennieFont.number(72))
                        .foregroundColor(BennieColors.coinGold)
                }

                // Milestone-specific message
                Text(milestoneMessage)
                    .font(BennieFont.body(24))
                    .foregroundColor(BennieColors.textDark)
                    .multilineTextAlignment(.center)
                    .padding(.horizontal, 20)

                // Button stack
                VStack(spacing: 16) {
                    // Treasure button (only when >= 10 coins)
                    if canAccessTreasure {
                        GoldenTreasureButton {
                            coordinator.navigateToTreasure()
                        }
                    }

                    // Continue button
                    WoodButton("Weiter") {
                        coordinator.navigateHome()
                    }
                }
                .padding(.top, 8)
            }
            .padding(40)
            .background(
                RoundedRectangle(cornerRadius: 24)
                    .fill(BennieColors.cream)
            )
            .overlay(
                RoundedRectangle(cornerRadius: 24)
                    .stroke(BennieColors.woodDark, lineWidth: 4)
            )
            .shadow(color: .black.opacity(0.3), radius: 20, x: 0, y: 10)
        }
        .onAppear {
            // Play celebration audio
            audioManager.playEffect(.celebrationFanfare)
            bennie.playCelebration(coins: coinsEarned)
        }
    }
}

// MARK: - Golden Treasure Button

/// Special golden button for navigating to the treasure screen
private struct GoldenTreasureButton: View {
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack(spacing: 12) {
                Image(systemName: "shippingbox.fill")
                    .font(.system(size: 28))
                Text("Zur Schatztruhe!")
                    .font(BennieFont.button(24))
            }
            .foregroundColor(BennieColors.textOnWood)
            .frame(minWidth: 240, minHeight: 60)
            .padding(.horizontal, 24)
            .padding(.vertical, 12)
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .fill(
                        LinearGradient(
                            colors: [BennieColors.coinGold, BennieColors.coinGold.opacity(0.8)],
                            startPoint: .top,
                            endPoint: .bottom
                        )
                    )
            )
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(BennieColors.woodDark, lineWidth: 3)
            )
            .shadow(color: BennieColors.coinGold.opacity(0.5), radius: 8, x: 0, y: 4)
        }
        .buttonStyle(.plain)
        // Ensure 96pt minimum touch target
        .frame(minWidth: 96, minHeight: 96)
    }
}

// MARK: - Confetti View

/// Animated confetti particles for celebration effect
private struct ConfettiView: View {
    // MARK: - State

    @State private var particles: [ConfettiParticle] = []
    @State private var animationTimer: Timer?

    // MARK: - Constants

    private let particleCount = 50
    private let colors: [Color] = [
        BennieColors.coinGold,
        BennieColors.success,
        BennieColors.woodLight,
        BennieColors.coinGold.opacity(0.7),
        BennieColors.success.opacity(0.7)
    ]

    // MARK: - Body

    var body: some View {
        GeometryReader { geometry in
            ZStack {
                ForEach(particles) { particle in
                    ConfettiParticleView(particle: particle)
                }
            }
            .onAppear {
                initializeParticles(in: geometry.size)
                startAnimation(in: geometry.size)
            }
            .onDisappear {
                animationTimer?.invalidate()
                animationTimer = nil
            }
        }
    }

    // MARK: - Particle Management

    /// Initialize all particles at random starting positions
    private func initializeParticles(in size: CGSize) {
        particles = (0..<particleCount).map { index in
            createParticle(index: index, in: size, initialSpawn: true)
        }
    }

    /// Create a single particle with random properties
    private func createParticle(index: Int, in size: CGSize, initialSpawn: Bool) -> ConfettiParticle {
        let randomX = CGFloat.random(in: 0...size.width)
        // For initial spawn, distribute vertically; for respawn, start above screen
        let randomY = initialSpawn ? CGFloat.random(in: -100...size.height) : CGFloat.random(in: -150...(-50))
        let randomSize = CGFloat.random(in: 8...16)
        let randomRotation = Double.random(in: 0...360)
        let randomHorizontalDrift = CGFloat.random(in: -1...1)
        let randomFallSpeed = CGFloat.random(in: 2...5)
        let randomColor = colors.randomElement() ?? BennieColors.coinGold
        let randomShape = ConfettiShape.allCases.randomElement() ?? .circle

        return ConfettiParticle(
            id: UUID(),
            x: randomX,
            y: randomY,
            size: randomSize,
            rotation: randomRotation,
            horizontalDrift: randomHorizontalDrift,
            fallSpeed: randomFallSpeed,
            color: randomColor,
            shape: randomShape
        )
    }

    /// Start the animation timer
    private func startAnimation(in size: CGSize) {
        animationTimer = Timer.scheduledTimer(withTimeInterval: 1.0 / 60.0, repeats: true) { _ in
            updateParticles(in: size)
        }
    }

    /// Update particle positions each frame
    private func updateParticles(in size: CGSize) {
        for index in particles.indices {
            // Update vertical position (falling)
            particles[index].y += particles[index].fallSpeed

            // Update horizontal position (drift)
            particles[index].x += particles[index].horizontalDrift

            // Update rotation
            particles[index].rotation += 2

            // Respawn if off screen
            if particles[index].y > size.height + 50 {
                particles[index] = createParticle(index: index, in: size, initialSpawn: false)
            }
        }
    }
}

// MARK: - Confetti Particle Model

/// Model for a single confetti particle
private struct ConfettiParticle: Identifiable {
    let id: UUID
    var x: CGFloat
    var y: CGFloat
    let size: CGFloat
    var rotation: Double
    let horizontalDrift: CGFloat
    let fallSpeed: CGFloat
    let color: Color
    let shape: ConfettiShape
}

/// Available shapes for confetti particles
private enum ConfettiShape: CaseIterable {
    case circle
    case rectangle
}

// MARK: - Confetti Particle View

/// View for a single confetti particle
private struct ConfettiParticleView: View {
    let particle: ConfettiParticle

    var body: some View {
        Group {
            switch particle.shape {
            case .circle:
                Circle()
                    .fill(particle.color)
                    .frame(width: particle.size, height: particle.size)
            case .rectangle:
                Rectangle()
                    .fill(particle.color)
                    .frame(width: particle.size, height: particle.size * 0.6)
            }
        }
        .rotationEffect(.degrees(particle.rotation))
        .position(x: particle.x, y: particle.y)
    }
}

// MARK: - Preview

#Preview("Celebration - 5 Coins") {
    let audioManager = AudioManager()
    return CelebrationOverlay(coinsEarned: 5)
        .environment(AppCoordinator())
        .environment(PlayerStore())
        .environment(audioManager)
        .environment(BennieService(audioManager: audioManager))
}

#Preview("Celebration - 10 Coins") {
    let audioManager = AudioManager()
    return CelebrationOverlay(coinsEarned: 10)
        .environment(AppCoordinator())
        .environment(PlayerStore())
        .environment(audioManager)
        .environment(BennieService(audioManager: audioManager))
}

#Preview("Celebration - 20 Coins") {
    let audioManager = AudioManager()
    return CelebrationOverlay(coinsEarned: 20)
        .environment(AppCoordinator())
        .environment(PlayerStore())
        .environment(audioManager)
        .environment(BennieService(audioManager: audioManager))
}
