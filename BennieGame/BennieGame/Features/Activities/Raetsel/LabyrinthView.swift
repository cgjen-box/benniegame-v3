import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// LabyrinthView - Path Tracing Maze Game
// ═══════════════════════════════════════════════════════════════════════════
// Children trace a path from START to ZIEL by dragging their finger
// Path width: 44pt touch tolerance
// Awards +1 coin per successful maze completion
// ═══════════════════════════════════════════════════════════════════════════

/// Main view for the Labyrinth activity
struct LabyrinthView: View {
    // MARK: - Environment

    @Environment(AppCoordinator.self) private var coordinator
    @Environment(PlayerStore.self) private var playerStore
    @Environment(AudioManager.self) private var audioManager
    @Environment(NarratorService.self) private var narrator
    @Environment(BennieService.self) private var bennie

    // MARK: - Game State

    @State private var currentLevel: Int = 0
    @State private var isTracing: Bool = false
    @State private var hasStarted: Bool = false
    @State private var hasCompleted: Bool = false
    @State private var showError: Bool = false
    @State private var currentPath: [CGPoint] = []
    @State private var mazeSize: CGSize = .zero

    // MARK: - Coin Animation State

    @State private var showCoinAnimation: Bool = false
    @State private var coinStartPosition: CGPoint = .zero

    // MARK: - Constants

    private let pathWidth: CGFloat = 44
    private let startRadius: CGFloat = 30
    private let goalRadius: CGFloat = 30

    // MARK: - Maze Configurations

    /// Returns path points for the current level maze
    private var currentMazeConfig: MazeConfig {
        MazeConfig.mazes[currentLevel % MazeConfig.mazes.count]
    }

    // MARK: - Body

    var body: some View {
        ZStack {
            VStack(spacing: 0) {
                // Navigation header
                navigationHeader

                Spacer()

                // Maze area
                mazeSection

                Spacer()

                // Instructions
                instructionSection
            }
            .background(BennieColors.cream.ignoresSafeArea())
            .overlay(errorOverlay)

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

    // MARK: - Maze Section

    private var mazeSection: some View {
        GeometryReader { geometry in
            ZStack {
                // Stone background
                RoundedRectangle(cornerRadius: 24)
                    .fill(BennieColors.pathStone.opacity(0.3))
                    .overlay(
                        RoundedRectangle(cornerRadius: 24)
                            .stroke(BennieColors.woodDark, lineWidth: 3)
                    )

                // Maze path
                mazePath(in: geometry.size)

                // Player's traced path
                tracedPath(in: geometry.size)

                // START marker
                startMarker(in: geometry.size)

                // ZIEL marker
                goalMarker(in: geometry.size)
            }
            .padding(20)
            .gesture(tracingGesture(in: geometry.size))
            .onAppear {
                mazeSize = geometry.size
                // Play activity start audio
                narrator.playLabyrinthStart()
                bennie.playLabyrinthStart()
            }
        }
        .aspectRatio(1.5, contentMode: .fit)
        .padding(.horizontal, 60)
    }

    // MARK: - Maze Path

    private func mazePath(in size: CGSize) -> some View {
        Path { path in
            let points = scaledPathPoints(in: size)
            guard points.count > 1 else { return }

            path.move(to: points[0])
            for i in 1..<points.count {
                path.addLine(to: points[i])
            }
        }
        .stroke(BennieColors.woodLight, style: StrokeStyle(lineWidth: pathWidth, lineCap: .round, lineJoin: .round))
        .shadow(color: .black.opacity(0.2), radius: 2, x: 2, y: 2)
    }

    // MARK: - Traced Path

    private func tracedPath(in size: CGSize) -> some View {
        Path { path in
            guard currentPath.count > 1 else { return }

            path.move(to: currentPath[0])
            for i in 1..<currentPath.count {
                path.addLine(to: currentPath[i])
            }
        }
        .stroke(BennieColors.success, style: StrokeStyle(lineWidth: pathWidth * 0.6, lineCap: .round, lineJoin: .round))
    }

    // MARK: - Start Marker

    private func startMarker(in size: CGSize) -> some View {
        let points = scaledPathPoints(in: size)
        guard let startPoint = points.first else {
            return AnyView(EmptyView())
        }

        return AnyView(
            ZStack {
                Circle()
                    .fill(BennieColors.success)
                    .frame(width: startRadius * 2, height: startRadius * 2)
                    .overlay(
                        Circle()
                            .stroke(BennieColors.woodDark, lineWidth: 3)
                    )
                    .shadow(color: hasStarted ? .clear : BennieColors.success.opacity(0.5), radius: hasStarted ? 0 : 8)

                Text("START")
                    .font(BennieFont.label(12))
                    .fontWeight(.bold)
                    .foregroundColor(.white)
            }
            .position(startPoint)
        )
    }

    // MARK: - Goal Marker

    private func goalMarker(in size: CGSize) -> some View {
        let points = scaledPathPoints(in: size)
        guard let goalPoint = points.last else {
            return AnyView(EmptyView())
        }

        return AnyView(
            ZStack {
                Circle()
                    .fill(BennieColors.coinGold)
                    .frame(width: goalRadius * 2, height: goalRadius * 2)
                    .overlay(
                        Circle()
                            .stroke(BennieColors.woodDark, lineWidth: 3)
                    )
                    .shadow(color: hasCompleted ? BennieColors.coinGold.opacity(0.8) : BennieColors.coinGold.opacity(0.3), radius: hasCompleted ? 12 : 4)

                Text("ZIEL")
                    .font(BennieFont.label(12))
                    .fontWeight(.bold)
                    .foregroundColor(BennieColors.woodDark)
            }
            .position(goalPoint)
        )
    }

    // MARK: - Error Overlay

    @ViewBuilder
    private var errorOverlay: some View {
        if showError {
            VStack {
                Image(systemName: "xmark.circle.fill")
                    .font(.system(size: 60))
                    .foregroundColor(BennieColors.woodMedium)

                Text("Versuche es nochmal!")
                    .font(BennieFont.button())
                    .foregroundColor(BennieColors.textDark)
            }
            .padding(40)
            .background(
                RoundedRectangle(cornerRadius: 20)
                    .fill(BennieColors.cream)
                    .shadow(radius: 10)
            )
            .transition(.scale.combined(with: .opacity))
            .onAppear {
                DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
                    withAnimation {
                        showError = false
                        resetTracing()
                    }
                }
            }
        }
    }

    // MARK: - Instruction Section

    private var instructionSection: some View {
        VStack(spacing: 8) {
            if !hasStarted {
                Text("Starte bei START und ziehe zum ZIEL!")
                    .font(BennieFont.body())
                    .foregroundColor(BennieColors.textDark)
            } else if hasCompleted {
                Text("Super gemacht!")
                    .font(BennieFont.celebration())
                    .foregroundColor(BennieColors.success)
            }
        }
        .padding(.bottom, 40)
    }

    // MARK: - Gesture Handling

    private func tracingGesture(in size: CGSize) -> some Gesture {
        DragGesture(minimumDistance: 0)
            .onChanged { value in
                handleDrag(at: value.location, in: size)
            }
            .onEnded { _ in
                handleDragEnd()
            }
    }

    private func handleDrag(at point: CGPoint, in size: CGSize) {
        guard !hasCompleted && !showError else { return }

        let scaledPoints = scaledPathPoints(in: size)
        guard !scaledPoints.isEmpty else { return }

        // Check if starting
        if !hasStarted {
            let startPoint = scaledPoints[0]
            if distance(point, startPoint) <= pathWidth {
                hasStarted = true
                isTracing = true
                currentPath = [point]
            }
            return
        }

        // Check if on valid path
        if isTracing {
            if isOnValidPath(point, pathPoints: scaledPoints) {
                currentPath.append(point)

                // Check if reached goal
                let goalPoint = scaledPoints[scaledPoints.count - 1]
                if distance(point, goalPoint) <= goalRadius + 10 {
                    handleSuccess()
                }
            } else {
                // Off path - play gentle feedback and show error
                audioManager.playEffect(.gentleBoop)
                bennie.playLabyrinthWrong()
                withAnimation {
                    showError = true
                    isTracing = false
                }
            }
        }
    }

    private func handleDragEnd() {
        if isTracing && !hasCompleted {
            // Finger lifted before reaching goal - allow retry
            isTracing = false
        }
    }

    // MARK: - Path Validation

    private func isOnValidPath(_ point: CGPoint, pathPoints: [CGPoint]) -> Bool {
        // Check distance to any segment of the path
        for i in 0..<(pathPoints.count - 1) {
            let segmentStart = pathPoints[i]
            let segmentEnd = pathPoints[i + 1]

            if distanceToSegment(point, from: segmentStart, to: segmentEnd) <= pathWidth {
                return true
            }
        }
        return false
    }

    private func distance(_ p1: CGPoint, _ p2: CGPoint) -> CGFloat {
        sqrt(pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2))
    }

    private func distanceToSegment(_ point: CGPoint, from start: CGPoint, to end: CGPoint) -> CGFloat {
        let dx = end.x - start.x
        let dy = end.y - start.y
        let lengthSquared = dx * dx + dy * dy

        if lengthSquared == 0 {
            return distance(point, start)
        }

        var t = ((point.x - start.x) * dx + (point.y - start.y) * dy) / lengthSquared
        t = max(0, min(1, t))

        let projection = CGPoint(
            x: start.x + t * dx,
            y: start.y + t * dy
        )

        return distance(point, projection)
    }

    // MARK: - Path Scaling

    private func scaledPathPoints(in size: CGSize) -> [CGPoint] {
        let config = currentMazeConfig
        let paddedSize = CGSize(
            width: size.width - 80,  // Account for markers
            height: size.height - 80
        )
        let offset = CGPoint(x: 40, y: 40)

        return config.normalizedPoints.map { normalized in
            CGPoint(
                x: offset.x + normalized.x * paddedSize.width,
                y: offset.y + normalized.y * paddedSize.height
            )
        }
    }

    // MARK: - Game Flow

    private func handleSuccess() {
        hasCompleted = true
        isTracing = false

        // Play success audio
        audioManager.playEffect(.successChime)

        // Get goal position for coin animation start
        let scaledPoints = scaledPathPoints(in: mazeSize)
        if let goalPoint = scaledPoints.last {
            coinStartPosition = goalPoint
        } else {
            coinStartPosition = CGPoint(x: UIScreen.main.bounds.width / 2, y: 400)
        }

        // Trigger coin animation after brief delay
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
            showCoinAnimation = true
        }
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
                // Play success voice and next maze
                narrator.playRandomSuccess()
                currentLevel += 1
                resetTracing()
            }
        }
    }

    private func resetTracing() {
        hasStarted = false
        hasCompleted = false
        isTracing = false
        currentPath = []
    }
}

// MARK: - Maze Configuration

/// Defines a maze path as normalized points (0.0-1.0)
struct MazeConfig {
    /// Path points normalized to 0.0-1.0 coordinate space
    let normalizedPoints: [CGPoint]

    /// Predefined maze configurations
    static let mazes: [MazeConfig] = [
        // Maze 1: S-curve
        MazeConfig(normalizedPoints: [
            CGPoint(x: 0.1, y: 0.1),
            CGPoint(x: 0.3, y: 0.1),
            CGPoint(x: 0.4, y: 0.3),
            CGPoint(x: 0.3, y: 0.5),
            CGPoint(x: 0.5, y: 0.6),
            CGPoint(x: 0.7, y: 0.5),
            CGPoint(x: 0.8, y: 0.7),
            CGPoint(x: 0.9, y: 0.9),
        ]),

        // Maze 2: Zigzag
        MazeConfig(normalizedPoints: [
            CGPoint(x: 0.1, y: 0.2),
            CGPoint(x: 0.3, y: 0.2),
            CGPoint(x: 0.3, y: 0.5),
            CGPoint(x: 0.6, y: 0.5),
            CGPoint(x: 0.6, y: 0.3),
            CGPoint(x: 0.9, y: 0.3),
            CGPoint(x: 0.9, y: 0.8),
        ]),

        // Maze 3: L-shape with curves
        MazeConfig(normalizedPoints: [
            CGPoint(x: 0.1, y: 0.1),
            CGPoint(x: 0.1, y: 0.5),
            CGPoint(x: 0.2, y: 0.6),
            CGPoint(x: 0.4, y: 0.6),
            CGPoint(x: 0.5, y: 0.7),
            CGPoint(x: 0.5, y: 0.9),
            CGPoint(x: 0.9, y: 0.9),
        ]),

        // Maze 4: Spiral-ish
        MazeConfig(normalizedPoints: [
            CGPoint(x: 0.5, y: 0.1),
            CGPoint(x: 0.8, y: 0.1),
            CGPoint(x: 0.8, y: 0.4),
            CGPoint(x: 0.5, y: 0.4),
            CGPoint(x: 0.5, y: 0.6),
            CGPoint(x: 0.2, y: 0.6),
            CGPoint(x: 0.2, y: 0.9),
            CGPoint(x: 0.9, y: 0.9),
        ]),
    ]
}

// MARK: - Previews

#Preview("LabyrinthView") {
    let audioManager = AudioManager()
    return LabyrinthView()
        .environment(AppCoordinator())
        .environment(PlayerStore())
        .environment(audioManager)
        .environment(NarratorService(audioManager: audioManager))
        .environment(BennieService(audioManager: audioManager))
}
