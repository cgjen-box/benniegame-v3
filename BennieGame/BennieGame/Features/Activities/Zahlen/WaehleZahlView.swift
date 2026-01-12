import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// WaehleZahlView - Number Selection Game
// ═══════════════════════════════════════════════════════════════════════════
// Children select the correct number (1-10) based on audio/visual prompt
// Numbers displayed on stone tablet in rows: 1-4, 5-7, 8-10
// Awards +1 coin per correct answer
// ═══════════════════════════════════════════════════════════════════════════

/// Main view for the Wähle die Zahl (Choose the Number) activity
struct WaehleZahlView: View {
    // MARK: - Environment

    @Environment(AppCoordinator.self) private var coordinator
    @Environment(PlayerStore.self) private var playerStore

    // MARK: - Game State

    @State private var targetNumber: Int = 1
    @State private var selectedNumber: Int? = nil
    @State private var showFeedback: Bool = false
    @State private var feedbackIsCorrect: Bool = false
    @State private var questionsAnswered: Int = 0
    @State private var lastTargetNumber: Int = 0  // Avoid repeats

    // MARK: - Coin Animation State

    @State private var showCoinAnimation: Bool = false
    @State private var coinStartPosition: CGPoint = .zero

    // MARK: - Body

    var body: some View {
        ZStack {
            VStack(spacing: 0) {
                // Navigation header
                navigationHeader

                Spacer()

                // Target number display
                targetSection

                Spacer()

                // Number grid
                numberGridSection

                Spacer()
            }
            .background(BennieColors.cream.ignoresSafeArea())
            .onAppear {
                selectNewTarget()
            }

            // Coin fly animation overlay
            if showCoinAnimation {
                CoinFlyAnimation(
                    startPosition: coinStartPosition,
                    targetPosition: CGPoint(x: UIScreen.main.bounds.width / 2, y: 80),
                    onComplete: {
                        showCoinAnimation = false
                        handleCoinAnimationComplete()
                    }
                )
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
                Image(systemName: "house.fill")
                    .font(.system(size: 28))
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

            Spacer()

            // Progress bar
            ProgressBar(currentCoins: playerStore.activePlayerCoins)
                .frame(width: 400)

            Spacer()

            // Volume toggle (placeholder)
            Button {
                // Volume toggle action - Phase 9
            } label: {
                Image(systemName: "speaker.wave.2.fill")
                    .font(.system(size: 28))
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
        .padding(.horizontal, 24)
        .padding(.top, 16)
    }

    // MARK: - Target Section

    private var targetSection: some View {
        VStack(spacing: 16) {
            // Instruction text
            Text("Zeig mir die \(targetNumber)!")
                .font(BennieFont.screenHeader())
                .foregroundColor(BennieColors.textDark)

            // Large target number with golden highlight
            ZStack {
                Circle()
                    .fill(BennieColors.coinGold.opacity(0.3))
                    .frame(width: 120, height: 120)

                Circle()
                    .stroke(BennieColors.coinGold, lineWidth: 4)
                    .frame(width: 120, height: 120)
                    .shadow(color: BennieColors.coinGold.opacity(0.5), radius: 8)

                Text("\(targetNumber)")
                    .font(BennieFont.number(72))
                    .foregroundColor(BennieColors.coinGold)
            }
        }
    }

    // MARK: - Number Grid Section

    private var numberGridSection: some View {
        StoneTablet {
            VStack(spacing: 16) {
                // Row 1: 1, 2, 3, 4
                HStack(spacing: 16) {
                    numberButton(1)
                    numberButton(2)
                    numberButton(3)
                    numberButton(4)
                }

                // Row 2: 5, 6, 7
                HStack(spacing: 16) {
                    numberButton(5)
                    numberButton(6)
                    numberButton(7)
                }

                // Row 3: 8, 9, 10
                HStack(spacing: 16) {
                    numberButton(8)
                    numberButton(9)
                    numberButton(10)
                }
            }
            .padding(24)
        }
    }

    // MARK: - Number Button

    private func numberButton(_ number: Int) -> some View {
        GeometryReader { geometry in
            Button {
                // Store button center for coin animation
                let frame = geometry.frame(in: .global)
                coinStartPosition = CGPoint(x: frame.midX, y: frame.midY)
                handleNumberTap(number)
            } label: {
                ZStack {
                    // Background circle
                    Circle()
                        .fill(buttonColor(for: number))
                        .overlay(
                            Circle()
                                .stroke(buttonBorderColor(for: number), lineWidth: 3)
                        )

                    // Number text
                    Text(number == 10 ? "10" : "\(number)")
                        .font(BennieFont.number(number == 10 ? 32 : 40))
                        .foregroundColor(BennieColors.textOnWood)
                }
                .shadow(
                    color: buttonShadowColor(for: number),
                    radius: isHighlighted(number) ? 8 : 2,
                    x: 0,
                    y: 2
                )
            }
            .buttonStyle(.plain)
            .disabled(showFeedback || showCoinAnimation)
            .accessibilityLabel("Zahl \(number)")
        }
        .frame(width: 80, height: 80)
    }

    // MARK: - Button Styling

    private func buttonColor(for number: Int) -> Color {
        if showFeedback && selectedNumber == number {
            return feedbackIsCorrect ? BennieColors.success : BennieColors.woodLight
        }
        if showFeedback && number == targetNumber && !feedbackIsCorrect {
            return BennieColors.coinGold.opacity(0.5)  // Highlight correct answer
        }
        return BennieColors.woodLight
    }

    private func buttonBorderColor(for number: Int) -> Color {
        if showFeedback && selectedNumber == number && feedbackIsCorrect {
            return BennieColors.success
        }
        if showFeedback && number == targetNumber && !feedbackIsCorrect {
            return BennieColors.coinGold
        }
        return BennieColors.woodDark
    }

    private func buttonShadowColor(for number: Int) -> Color {
        if showFeedback && selectedNumber == number && feedbackIsCorrect {
            return BennieColors.success.opacity(0.5)
        }
        if showFeedback && number == targetNumber && !feedbackIsCorrect {
            return BennieColors.coinGold.opacity(0.5)
        }
        return .black.opacity(0.2)
    }

    private func isHighlighted(_ number: Int) -> Bool {
        showFeedback && (selectedNumber == number || (number == targetNumber && !feedbackIsCorrect))
    }

    // MARK: - Game Logic

    private func selectNewTarget() {
        var newTarget: Int
        repeat {
            newTarget = Int.random(in: 1...10)
        } while newTarget == lastTargetNumber

        lastTargetNumber = targetNumber
        targetNumber = newTarget
    }

    private func handleNumberTap(_ number: Int) {
        guard !showFeedback else { return }

        selectedNumber = number

        if number == targetNumber {
            handleCorrectAnswer()
        } else {
            handleWrongAnswer()
        }
    }

    private func handleCorrectAnswer() {
        feedbackIsCorrect = true
        showFeedback = true
        questionsAnswered += 1

        // Trigger coin animation after brief feedback
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
            showFeedback = false
            selectedNumber = nil
            showCoinAnimation = true
        }
    }

    /// Called when coin fly animation completes
    private func handleCoinAnimationComplete() {
        // Award coin after animation
        if let newCoins = playerStore.awardCoin() {
            // Check for celebration
            if coordinator.shouldShowCelebration(for: newCoins) {
                coordinator.showCelebration(coinsEarned: newCoins)
            } else {
                // Select new target
                selectNewTarget()
            }
        }
    }

    private func handleWrongAnswer() {
        feedbackIsCorrect = false
        showFeedback = true

        // Brief feedback showing correct answer, then allow retry
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
            showFeedback = false
            selectedNumber = nil
            // Don't change target - allow retry
        }
    }
}

// MARK: - Previews

#Preview("WaehleZahlView") {
    WaehleZahlView()
        .environment(AppCoordinator())
        .environment(PlayerStore())
}
