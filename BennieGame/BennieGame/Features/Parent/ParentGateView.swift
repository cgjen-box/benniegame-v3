import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// ParentGateView - Math challenge gate for parent area access
// ═══════════════════════════════════════════════════════════════════════════
// Requires solving a simple addition problem (sum 5-15) to access parent area
// Uses large touch targets (96pt+) and German-only UI
// ═══════════════════════════════════════════════════════════════════════════

/// Parent gate with math challenge to verify adult access
struct ParentGateView: View {
    // MARK: - Environment

    @Environment(AppCoordinator.self) private var coordinator

    // MARK: - State

    /// First number in addition (1-9)
    @State private var num1 = 0
    /// Second number in addition (1-9)
    @State private var num2 = 0
    /// User's entered answer as string
    @State private var userInput = ""
    /// Number of wrong attempts (max 3 before regenerating)
    @State private var attempts = 0
    /// Show success checkmark animation
    @State private var showSuccess = false
    /// Trigger shake animation for wrong answer
    @State private var shakeAnswer = false

    // MARK: - Computed Properties

    /// The correct answer to the math question
    private var correctAnswer: Int { num1 + num2 }

    /// Display the math question
    private var questionText: String {
        "\(num1) + \(num2) = ?"
    }

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
                .padding(.horizontal, 24)
                .padding(.top, 20)

                Spacer()

                // Lock icon and title
                headerSection

                // Math question display
                questionSection

                // Answer display
                answerDisplay

                // Number pad
                numberPad

                // Action buttons
                actionButtons

                Spacer()
            }
            .padding()

            // Success overlay
            if showSuccess {
                successOverlay
            }
        }
        .onAppear {
            generateQuestion()
        }
    }

    // MARK: - Header Section

    private var headerSection: some View {
        VStack(spacing: 12) {
            Image(systemName: "lock.fill")
                .font(.system(size: 48))
                .foregroundColor(BennieColors.woodDark)

            Text("Elternbereich")
                .font(BennieFont.title(36))
                .foregroundColor(BennieColors.textDark)
        }
    }

    // MARK: - Question Section

    private var questionSection: some View {
        Text(questionText)
            .font(BennieFont.number(48))
            .foregroundColor(BennieColors.textDark)
            .padding(.vertical, 16)
    }

    // MARK: - Answer Display

    private var answerDisplay: some View {
        HStack {
            Text(userInput.isEmpty ? "_" : userInput)
                .font(BennieFont.number(56))
                .foregroundColor(BennieColors.textDark)
                .frame(minWidth: 120, minHeight: 80)
                .padding(.horizontal, 24)
                .background(
                    RoundedRectangle(cornerRadius: 12)
                        .fill(BennieColors.woodLight.opacity(0.3))
                        .overlay(
                            RoundedRectangle(cornerRadius: 12)
                                .stroke(BennieColors.woodMedium, lineWidth: 2)
                        )
                )
        }
        .offset(x: shakeAnswer ? -10 : 0)
        .animation(
            shakeAnswer ?
                Animation.easeInOut(duration: 0.08).repeatCount(5, autoreverses: true) :
                .default,
            value: shakeAnswer
        )
    }

    // MARK: - Number Pad

    private var numberPad: some View {
        VStack(spacing: 12) {
            // Row 1: 1-5
            HStack(spacing: 12) {
                ForEach(1...5, id: \.self) { number in
                    numberButton(number)
                }
            }

            // Row 2: 6-0
            HStack(spacing: 12) {
                ForEach(6...9, id: \.self) { number in
                    numberButton(number)
                }
                numberButton(0)
            }
        }
    }

    /// Creates a number button with proper touch target
    private func numberButton(_ number: Int) -> some View {
        ChildFriendlyButton(action: {
            appendNumber(number)
        }) {
            Text("\(number)")
                .font(BennieFont.number(32))
                .foregroundColor(BennieColors.textOnWood)
                .frame(width: 96, height: 96)
                .background(
                    RoundedRectangle(cornerRadius: 12)
                        .fill(
                            LinearGradient(
                                colors: [BennieColors.woodLight, BennieColors.woodMedium],
                                startPoint: .top,
                                endPoint: .bottom
                            )
                        )
                )
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(BennieColors.woodDark, lineWidth: 2)
                )
        }
    }

    // MARK: - Action Buttons

    private var actionButtons: some View {
        HStack(spacing: 24) {
            // Clear button
            ChildFriendlyButton(action: clearInput) {
                HStack(spacing: 8) {
                    Image(systemName: "delete.left.fill")
                        .font(.system(size: 24))
                    Text("Löschen")
                        .font(BennieFont.button(20))
                }
                .foregroundColor(BennieColors.textOnWood)
                .frame(width: 160, height: 96)
                .background(
                    RoundedRectangle(cornerRadius: 12)
                        .fill(BennieColors.woodLight.opacity(0.7))
                )
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(BennieColors.woodMedium, lineWidth: 2)
                )
            }

            // Submit button
            ChildFriendlyButton(action: checkAnswer) {
                HStack(spacing: 8) {
                    Image(systemName: "checkmark.circle.fill")
                        .font(.system(size: 24))
                    Text("Prüfen")
                        .font(BennieFont.button(20))
                }
                .foregroundColor(BennieColors.textOnWood)
                .frame(width: 160, height: 96)
                .background(
                    RoundedRectangle(cornerRadius: 12)
                        .fill(
                            LinearGradient(
                                colors: [BennieColors.woodLight, BennieColors.woodMedium],
                                startPoint: .top,
                                endPoint: .bottom
                            )
                        )
                )
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(BennieColors.woodDark, lineWidth: 2)
                )
            }
        }
    }

    // MARK: - Back Button

    private var backButton: some View {
        ChildFriendlyButton(action: {
            coordinator.navigateHome()
        }) {
            HStack(spacing: 8) {
                Image(systemName: "arrow.left")
                    .font(.system(size: 24))
                Text("Zurück")
                    .font(BennieFont.button(20))
            }
            .foregroundColor(BennieColors.textOnWood)
            .padding(.horizontal, 20)
            .padding(.vertical, 12)
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .fill(BennieColors.woodLight.opacity(0.7))
            )
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(BennieColors.woodMedium, lineWidth: 2)
            )
        }
    }

    // MARK: - Success Overlay

    private var successOverlay: some View {
        ZStack {
            Color.black.opacity(0.3)
                .ignoresSafeArea()

            VStack(spacing: 20) {
                Image(systemName: "checkmark.circle.fill")
                    .font(.system(size: 100))
                    .foregroundColor(BennieColors.success)

                Text("Richtig!")
                    .font(BennieFont.celebration())
                    .foregroundColor(BennieColors.success)
            }
            .padding(40)
            .background(
                RoundedRectangle(cornerRadius: 24)
                    .fill(BennieColors.cream)
            )
            .shadow(radius: 20)
        }
        .transition(.opacity)
    }

    // MARK: - Actions

    /// Generate a random math question with sum between 5-15
    private func generateQuestion() {
        // Generate numbers such that sum is between 5 and 15
        // num1 + num2 should be in range 5...15
        // With single digits 1-9, we need to ensure valid range

        repeat {
            num1 = Int.random(in: 1...9)
            num2 = Int.random(in: 1...9)
        } while (num1 + num2) < 5 || (num1 + num2) > 15

        userInput = ""
        attempts = 0
    }

    /// Append a digit to user input (max 2 digits for answers up to 15)
    private func appendNumber(_ number: Int) {
        guard userInput.count < 2 else { return }
        userInput += "\(number)"
    }

    /// Clear the user input
    private func clearInput() {
        userInput = ""
    }

    /// Check if the answer is correct
    private func checkAnswer() {
        guard let answer = Int(userInput) else { return }

        if answer == correctAnswer {
            // Correct answer
            showSuccess = true

            // Navigate after brief delay
            DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) {
                withAnimation {
                    showSuccess = false
                }
                coordinator.navigateToParentDashboard()
            }
        } else {
            // Wrong answer - gentle shake (no negative words)
            attempts += 1
            triggerShake()

            if attempts >= 3 {
                // After 3 wrong attempts, generate new question
                DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
                    generateQuestion()
                }
            } else {
                // Clear input for retry
                userInput = ""
            }
        }
    }

    /// Trigger shake animation
    private func triggerShake() {
        shakeAnswer = true
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.4) {
            shakeAnswer = false
        }
    }
}

// MARK: - Previews

#Preview("ParentGateView") {
    ParentGateView()
        .environment(AppCoordinator())
}
