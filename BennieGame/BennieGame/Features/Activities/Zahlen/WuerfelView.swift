import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// WuerfelView - Dice Number Recognition Game
// ═══════════════════════════════════════════════════════════════════════════
// Children identify the number shown on a dice by tapping the matching button
// Dice shows 1-6, number buttons in 3×2 grid below
// Awards +1 coin per correct answer
// ═══════════════════════════════════════════════════════════════════════════

/// Main view for the Würfel (Dice) activity
struct WuerfelView: View {
    // MARK: - Environment

    @Environment(AppCoordinator.self) private var coordinator
    @Environment(PlayerStore.self) private var playerStore

    // MARK: - Game State

    @State private var currentDiceValue: Int = 1
    @State private var isRolling: Bool = false
    @State private var showFeedback: Bool = false
    @State private var feedbackIsCorrect: Bool = false
    @State private var tappedNumber: Int? = nil
    @State private var score: Int = 0

    // MARK: - Coin Animation State

    @State private var showCoinAnimation: Bool = false
    @State private var coinStartPosition: CGPoint = .zero
    @State private var pendingCoinCount: Int? = nil

    // MARK: - Body

    var body: some View {
        ZStack {
            VStack(spacing: 0) {
                // Navigation header
                navigationHeader

                Spacer()

                // Dice display
                diceSection

                Spacer()

                // Number buttons
                numberButtonsSection

                Spacer()
            }
            .background(BennieColors.cream.ignoresSafeArea())
            .onAppear {
                rollDice()
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

    // MARK: - Dice Section

    private var diceSection: some View {
        VStack(spacing: 24) {
            // Instruction
            Text("Zeig mir die \(currentDiceValue)!")
                .font(BennieFont.screenHeader())
                .foregroundColor(BennieColors.textDark)

            // Dice face
            DiceFace(value: currentDiceValue, isRolling: isRolling)
                .frame(width: 150, height: 150)
        }
    }

    // MARK: - Number Buttons Section

    private var numberButtonsSection: some View {
        StoneTablet {
            VStack(spacing: 16) {
                // Row 1: 1, 2, 3
                HStack(spacing: 16) {
                    numberButton(1)
                    numberButton(2)
                    numberButton(3)
                }

                // Row 2: 4, 5, 6
                HStack(spacing: 16) {
                    numberButton(4)
                    numberButton(5)
                    numberButton(6)
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
                    // Background
                    RoundedRectangle(cornerRadius: 16)
                        .fill(buttonColor(for: number))
                        .overlay(
                            RoundedRectangle(cornerRadius: 16)
                                .stroke(buttonBorderColor(for: number), lineWidth: 3)
                        )

                    // Number
                    Text("\(number)")
                        .font(BennieFont.number(48))
                        .foregroundColor(BennieColors.textOnWood)
                }
                .shadow(
                    color: buttonShadowColor(for: number),
                    radius: showFeedback && tappedNumber == number ? 8 : 2,
                    x: 0,
                    y: 2
                )
            }
            .buttonStyle(.plain)
            .disabled(isRolling || showFeedback || showCoinAnimation)
            .accessibilityLabel("Zahl \(number)")
        }
        .frame(width: 96, height: 96)
    }

    // MARK: - Button Styling

    private func buttonColor(for number: Int) -> Color {
        if showFeedback && tappedNumber == number {
            return feedbackIsCorrect ? BennieColors.success : BennieColors.woodLight
        }
        if showFeedback && number == currentDiceValue && !feedbackIsCorrect {
            return BennieColors.coinGold.opacity(0.5)  // Highlight correct answer
        }
        return BennieColors.woodLight
    }

    private func buttonBorderColor(for number: Int) -> Color {
        if showFeedback && tappedNumber == number && feedbackIsCorrect {
            return BennieColors.success
        }
        return BennieColors.woodDark
    }

    private func buttonShadowColor(for number: Int) -> Color {
        if showFeedback && tappedNumber == number {
            return feedbackIsCorrect ? BennieColors.success.opacity(0.5) : .clear
        }
        return .black.opacity(0.2)
    }

    // MARK: - Game Logic

    private func rollDice() {
        isRolling = true
        var rollCount = 0

        Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { timer in
            currentDiceValue = Int.random(in: 1...6)
            rollCount += 1

            if rollCount >= 10 {
                timer.invalidate()
                currentDiceValue = Int.random(in: 1...6)
                isRolling = false
            }
        }
    }

    private func handleNumberTap(_ number: Int) {
        guard !isRolling && !showFeedback else { return }

        tappedNumber = number

        if number == currentDiceValue {
            handleCorrectAnswer()
        } else {
            handleWrongAnswer()
        }
    }

    private func handleCorrectAnswer() {
        feedbackIsCorrect = true
        showFeedback = true
        score += 1

        // Trigger coin animation after brief feedback
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
            showFeedback = false
            tappedNumber = nil
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
                // Roll next dice
                rollDice()
            }
        }
    }

    private func handleWrongAnswer() {
        feedbackIsCorrect = false
        showFeedback = true

        // Brief feedback then allow retry
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.2) {
            showFeedback = false
            tappedNumber = nil
        }
    }
}

// MARK: - Dice Face

/// Displays a dice face with the correct dot pattern
struct DiceFace: View {
    let value: Int
    var isRolling: Bool = false

    var body: some View {
        ZStack {
            // White dice background
            RoundedRectangle(cornerRadius: 16)
                .fill(Color.white)
                .overlay(
                    RoundedRectangle(cornerRadius: 16)
                        .stroke(BennieColors.woodDark, lineWidth: 3)
                )
                .shadow(color: .black.opacity(0.2), radius: 4, x: 2, y: 2)

            // Dots pattern
            dotsPattern
        }
        .rotationEffect(.degrees(isRolling ? 360 : 0))
        .animation(isRolling ? .linear(duration: 0.1).repeatForever(autoreverses: false) : .default, value: isRolling)
    }

    @ViewBuilder
    private var dotsPattern: some View {
        let dotSize: CGFloat = 20
        let spacing: CGFloat = 35

        GeometryReader { geo in
            let center = CGPoint(x: geo.size.width / 2, y: geo.size.height / 2)

            ZStack {
                switch value {
                case 1:
                    // Center dot
                    dot(at: center, size: dotSize)

                case 2:
                    // Top-right and bottom-left
                    dot(at: CGPoint(x: center.x + spacing, y: center.y - spacing), size: dotSize)
                    dot(at: CGPoint(x: center.x - spacing, y: center.y + spacing), size: dotSize)

                case 3:
                    // Diagonal
                    dot(at: CGPoint(x: center.x + spacing, y: center.y - spacing), size: dotSize)
                    dot(at: center, size: dotSize)
                    dot(at: CGPoint(x: center.x - spacing, y: center.y + spacing), size: dotSize)

                case 4:
                    // Four corners
                    dot(at: CGPoint(x: center.x - spacing, y: center.y - spacing), size: dotSize)
                    dot(at: CGPoint(x: center.x + spacing, y: center.y - spacing), size: dotSize)
                    dot(at: CGPoint(x: center.x - spacing, y: center.y + spacing), size: dotSize)
                    dot(at: CGPoint(x: center.x + spacing, y: center.y + spacing), size: dotSize)

                case 5:
                    // Four corners + center
                    dot(at: CGPoint(x: center.x - spacing, y: center.y - spacing), size: dotSize)
                    dot(at: CGPoint(x: center.x + spacing, y: center.y - spacing), size: dotSize)
                    dot(at: center, size: dotSize)
                    dot(at: CGPoint(x: center.x - spacing, y: center.y + spacing), size: dotSize)
                    dot(at: CGPoint(x: center.x + spacing, y: center.y + spacing), size: dotSize)

                case 6:
                    // Two columns of 3
                    dot(at: CGPoint(x: center.x - spacing, y: center.y - spacing), size: dotSize)
                    dot(at: CGPoint(x: center.x - spacing, y: center.y), size: dotSize)
                    dot(at: CGPoint(x: center.x - spacing, y: center.y + spacing), size: dotSize)
                    dot(at: CGPoint(x: center.x + spacing, y: center.y - spacing), size: dotSize)
                    dot(at: CGPoint(x: center.x + spacing, y: center.y), size: dotSize)
                    dot(at: CGPoint(x: center.x + spacing, y: center.y + spacing), size: dotSize)

                default:
                    EmptyView()
                }
            }
        }
    }

    private func dot(at position: CGPoint, size: CGFloat) -> some View {
        Circle()
            .fill(BennieColors.textDark)
            .frame(width: size, height: size)
            .position(position)
    }
}

// MARK: - Previews

#Preview("WuerfelView") {
    WuerfelView()
        .environment(AppCoordinator())
        .environment(PlayerStore())
}

#Preview("DiceFace - All Values") {
    HStack(spacing: 20) {
        ForEach(1...6, id: \.self) { value in
            DiceFace(value: value)
                .frame(width: 80, height: 80)
        }
    }
    .padding()
}
