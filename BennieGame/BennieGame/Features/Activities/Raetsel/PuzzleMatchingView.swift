import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// PuzzleMatchingView - Color Pattern Matching Game
// ═══════════════════════════════════════════════════════════════════════════
// Children match a target pattern (ZIEL) by selecting colors and filling grid (DU)
// Grid progression: 3×3 → 4×4 → 5×5 → 6×6 based on level
// Awards +1 coin per correct match, celebrates every 5 coins
// ═══════════════════════════════════════════════════════════════════════════

/// Main view for the Puzzle Matching activity
struct PuzzleMatchingView: View {
    // MARK: - Environment

    @Environment(AppCoordinator.self) private var coordinator
    @Environment(PlayerStore.self) private var playerStore
    @Environment(AudioManager.self) private var audioManager
    @Environment(NarratorService.self) private var narrator
    @Environment(BennieService.self) private var bennie

    // MARK: - Game State

    @State private var targetGrid: [[PuzzleColor?]] = []
    @State private var playerGrid: [[PuzzleColor?]] = []
    @State private var selectedColor: PuzzleColor? = nil
    @State private var currentLevel: Int = 1
    @State private var showingSuccess: Bool = false

    // MARK: - Coin Animation State

    @State private var showCoinAnimation: Bool = false
    @State private var coinStartPosition: CGPoint = .zero
    @State private var lastTappedCellCenter: CGPoint = .zero

    // MARK: - Computed Properties

    /// Grid size based on current level
    private var gridSize: Int {
        switch currentLevel {
        case 1...10: return 3
        case 11...20: return 4
        case 21...30: return 5
        default: return 6
        }
    }

    /// Available colors based on current level
    private var availableColors: [PuzzleColor] {
        if currentLevel <= 5 {
            return [.green, .yellow]
        } else {
            return [.green, .yellow, .gray]
        }
    }

    /// Check if player grid matches target grid
    private var isGridMatched: Bool {
        guard targetGrid.count == playerGrid.count else { return false }
        for row in 0..<targetGrid.count {
            guard targetGrid[row].count == playerGrid[row].count else { return false }
            for col in 0..<targetGrid[row].count {
                if targetGrid[row][col] != playerGrid[row][col] {
                    return false
                }
            }
        }
        return true
    }

    // MARK: - Body

    var body: some View {
        ZStack {
            VStack(spacing: 0) {
                // Navigation header
                navigationHeader

                Spacer()

                // Dual grid display
                dualGridSection

                Spacer()

                // Color picker
                colorPickerSection
            }
            .background(BennieColors.cream.ignoresSafeArea())
            .onAppear {
                generateLevel()
                // Play activity start audio
                narrator.playPuzzleStart()
                bennie.playPuzzleStart()
            }
            .onChange(of: playerGrid) { _, _ in
                checkForMatch()
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

            // Mute toggle
            MuteButton()
        }
        .padding(.horizontal, 24)
        .padding(.top, 16)
    }

    // MARK: - Dual Grid Section

    private var dualGridSection: some View {
        HStack(spacing: 40) {
            // ZIEL (target) grid
            VStack(spacing: 12) {
                Text("ZIEL")
                    .font(BennieFont.screenHeader())
                    .foregroundColor(BennieColors.textDark)

                StoneTablet {
                    gridView(grid: targetGrid, isInteractive: false)
                }
            }

            // Arrow indicator
            Image(systemName: "arrow.right")
                .font(.system(size: 48, weight: .bold))
                .foregroundColor(BennieColors.coinGold)

            // DU (player) grid
            VStack(spacing: 12) {
                Text("DU")
                    .font(BennieFont.screenHeader())
                    .foregroundColor(BennieColors.textDark)

                StoneTablet {
                    gridView(grid: playerGrid, isInteractive: true)
                }
            }
        }
    }

    // MARK: - Grid View

    @ViewBuilder
    private func gridView(grid: [[PuzzleColor?]], isInteractive: Bool) -> some View {
        VStack(spacing: 8) {
            ForEach(0..<grid.count, id: \.self) { row in
                HStack(spacing: 8) {
                    ForEach(0..<grid[row].count, id: \.self) { col in
                        cellView(
                            color: grid[row][col],
                            row: row,
                            col: col,
                            isInteractive: isInteractive
                        )
                    }
                }
            }
        }
        .padding(16)
    }

    // MARK: - Cell View

    @ViewBuilder
    private func cellView(color: PuzzleColor?, row: Int, col: Int, isInteractive: Bool) -> some View {
        let cellSize: CGFloat = gridSize <= 4 ? 96 : (gridSize == 5 ? 80 : 70)

        GeometryReader { geometry in
            ZStack {
                // Cell background (using cream for empty cells per PLAYBOOK)
                RoundedRectangle(cornerRadius: 8)
                    .fill(color?.swiftUIColor ?? BennieColors.cream)
                    .overlay(
                        RoundedRectangle(cornerRadius: 8)
                            .stroke(BennieColors.woodDark.opacity(0.5), lineWidth: 2)
                    )
            }
            .onTapGesture {
                if isInteractive {
                    // Store cell center position for coin animation
                    let frame = geometry.frame(in: .global)
                    lastTappedCellCenter = CGPoint(
                        x: frame.midX,
                        y: frame.midY
                    )
                    handleCellTap(row: row, col: col)
                }
            }
        }
        .frame(width: cellSize, height: cellSize)
        .accessibilityLabel("Zelle \(row + 1), \(col + 1)")
        .accessibilityHint(isInteractive ? "Tippe um Farbe zu setzen" : "")
    }

    // MARK: - Color Picker Section

    private var colorPickerSection: some View {
        VStack(spacing: 16) {
            // Color buttons
            HStack(spacing: 20) {
                ForEach(availableColors, id: \.self) { color in
                    colorButton(for: color)
                }

                // Eraser
                eraserButton

                // Reset
                resetButton
            }
            .padding(.horizontal, 24)
            .padding(.vertical, 16)
            .background(
                RoundedRectangle(cornerRadius: 16)
                    .fill(BennieColors.woodLight)
                    .overlay(
                        RoundedRectangle(cornerRadius: 16)
                            .stroke(BennieColors.woodDark, lineWidth: 3)
                    )
            )
        }
        .padding(.bottom, 40)
    }

    // MARK: - Color Button

    private func colorButton(for color: PuzzleColor) -> some View {
        Button {
            selectedColor = color
        } label: {
            Circle()
                .fill(color.swiftUIColor)
                .frame(width: 96, height: 96)
                .overlay(
                    Circle()
                        .stroke(
                            selectedColor == color ? BennieColors.coinGold : BennieColors.woodDark,
                            lineWidth: selectedColor == color ? 4 : 2
                        )
                )
                .shadow(
                    color: selectedColor == color ? BennieColors.coinGold.opacity(0.5) : .clear,
                    radius: 8
                )
        }
        .buttonStyle(.plain)
        .accessibilityLabel(color.germanName)
    }

    // MARK: - Eraser Button

    private var eraserButton: some View {
        Button {
            selectedColor = nil
        } label: {
            ZStack {
                Circle()
                    .fill(BennieColors.cream)
                    .frame(width: 96, height: 96)
                    .overlay(
                        Circle()
                            .stroke(
                                selectedColor == nil ? BennieColors.coinGold : BennieColors.woodDark,
                                lineWidth: selectedColor == nil ? 4 : 2
                            )
                    )

                Image(systemName: "eraser.fill")
                    .font(.system(size: 32))
                    .foregroundColor(BennieColors.woodDark)
            }
            .shadow(
                color: selectedColor == nil ? BennieColors.coinGold.opacity(0.5) : .clear,
                radius: 8
            )
        }
        .buttonStyle(.plain)
        .accessibilityLabel("Radiergummi")
    }

    // MARK: - Reset Button

    private var resetButton: some View {
        Button {
            resetPlayerGrid()
        } label: {
            ZStack {
                Circle()
                    .fill(BennieColors.woodMedium)
                    .frame(width: 96, height: 96)
                    .overlay(
                        Circle()
                            .stroke(BennieColors.woodDark, lineWidth: 2)
                    )

                Image(systemName: "arrow.counterclockwise")
                    .font(.system(size: 32))
                    .foregroundColor(BennieColors.textOnWood)
            }
        }
        .buttonStyle(.plain)
        .accessibilityLabel("Zurücksetzen")
    }

    // MARK: - Game Logic

    /// Generate a new level with target pattern
    private func generateLevel() {
        let size = gridSize
        let colors = availableColors

        // Calculate fill density based on level
        let minFill: Int
        let maxFill: Int
        switch currentLevel {
        case 1...5:
            minFill = 2
            maxFill = 4
        case 6...10:
            minFill = 3
            maxFill = 5
        case 11...20:
            minFill = 4
            maxFill = 7
        default:
            minFill = 5
            maxFill = 10
        }

        let fillCount = Int.random(in: minFill...maxFill)

        // Create empty grids
        var newTargetGrid: [[PuzzleColor?]] = Array(
            repeating: Array(repeating: nil, count: size),
            count: size
        )

        // Fill random cells
        var filledCells = Set<String>()
        while filledCells.count < fillCount {
            let row = Int.random(in: 0..<size)
            let col = Int.random(in: 0..<size)
            let key = "\(row)-\(col)"

            if !filledCells.contains(key) {
                filledCells.insert(key)
                newTargetGrid[row][col] = colors.randomElement()
            }
        }

        targetGrid = newTargetGrid
        resetPlayerGrid()
    }

    /// Reset player grid to empty
    private func resetPlayerGrid() {
        let size = gridSize
        playerGrid = Array(
            repeating: Array(repeating: nil, count: size),
            count: size
        )
    }

    /// Handle tap on a player grid cell
    private func handleCellTap(row: Int, col: Int) {
        guard row < playerGrid.count && col < playerGrid[row].count else { return }
        playerGrid[row][col] = selectedColor
    }

    /// Check if grids match and handle success
    private func checkForMatch() {
        guard isGridMatched else { return }

        // Success! Play success audio and trigger coin animation
        audioManager.playEffect(.successChime)
        coinStartPosition = lastTappedCellCenter
        showCoinAnimation = true
    }

    /// Called when coin fly animation completes
    private func handleCoinAnimationComplete() {
        // Play coin collect sound
        audioManager.playEffect(.coinCollect)

        // Award coin after animation
        if let newCoins = playerStore.awardCoin() {
            // Check for celebration
            if coordinator.shouldShowCelebration(for: newCoins) {
                coordinator.showCelebration(coinsEarned: newCoins)
            } else {
                // Play success voice and generate next level
                narrator.playRandomSuccess()
                DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
                    currentLevel += 1
                    generateLevel()
                }
            }
        }
    }
}

// MARK: - Stone Tablet Component

/// Stone tablet background container for game grids
struct StoneTablet<Content: View>: View {
    let content: Content

    init(@ViewBuilder content: () -> Content) {
        self.content = content()
    }

    var body: some View {
        content
            .background(
                RoundedRectangle(cornerRadius: 16)
                    .fill(BennieColors.pathStone)
                    .overlay(
                        RoundedRectangle(cornerRadius: 16)
                            .stroke(BennieColors.woodDark, lineWidth: 3)
                    )
                    .shadow(color: .black.opacity(0.2), radius: 4, x: 2, y: 2)
            )
    }
}

// MARK: - Puzzle Color

/// Colors available for puzzle matching game
enum PuzzleColor: String, CaseIterable, Codable, Equatable {
    case green
    case yellow
    case gray

    /// SwiftUI Color representation
    var swiftUIColor: Color {
        switch self {
        case .green: return BennieColors.success     // #99BF8C
        case .yellow: return BennieColors.coinGold   // #D9C27A
        case .gray: return BennieColors.woodLight    // #C4A574
        }
    }

    /// German name for accessibility
    var germanName: String {
        switch self {
        case .green: return "Grün"
        case .yellow: return "Gelb"
        case .gray: return "Grau"
        }
    }
}

// MARK: - Previews

#Preview("PuzzleMatchingView") {
    let audioManager = AudioManager()
    return PuzzleMatchingView()
        .environment(AppCoordinator())
        .environment(PlayerStore())
        .environment(audioManager)
        .environment(NarratorService(audioManager: audioManager))
        .environment(BennieService(audioManager: audioManager))
}

#Preview("StoneTablet") {
    StoneTablet {
        Text("Test Content")
            .padding(40)
    }
    .padding()
}
