import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// ContentView - Main routing view
// ═══════════════════════════════════════════════════════════════════════════
// Routes to the appropriate screen based on current game state
// Uses implemented views for Phase 2 screens, placeholders for future phases
// ═══════════════════════════════════════════════════════════════════════════

/// Main content view that routes to different screens based on game state
struct ContentView: View {
    // MARK: - Environment

    @Environment(AppCoordinator.self) private var coordinator
    @Environment(PlayerStore.self) private var playerStore

    // MARK: - Body

    var body: some View {
        ZStack {
            // Background color for all screens
            BennieColors.cream
                .ignoresSafeArea()

            // Route to the appropriate view based on current state
            viewForState(coordinator.currentState)
        }
        .animation(.easeInOut(duration: 0.3), value: coordinator.currentState)
    }

    // MARK: - View Routing

    /// Returns the appropriate view for the given game state
    @ViewBuilder
    private func viewForState(_ state: GameState) -> some View {
        switch state {
        // Phase 2 - Implemented screens
        case .loading:
            LoadingView()

        case .playerSelection:
            PlayerSelectionView()

        case .home:
            HomeView()

        case .activitySelection(let activityType):
            activitySelectionView(for: activityType)

        case .treasureScreen:
            TreasureView()

        case .parentGate:
            ParentGateView()

        // Phase 3 - Activity screens
        case .playing(let activityType, let subActivity):
            switch subActivity {
            case .puzzleMatching:
                PuzzleMatchingView()
            case .labyrinth:
                LabyrinthView()
            case .wuerfel:
                WuerfelView()
            case .waehleZahl:
                WaehleZahlView()
            default:
                // Placeholder for activities not yet implemented
                PlayingPlaceholder(activityType: activityType, subActivity: subActivity)
            }

        case .levelComplete:
            LevelCompletePlaceholder()

        case .celebrationOverlay(let coinsEarned):
            CelebrationOverlay(coinsEarned: coinsEarned)

        case .videoSelection:
            VideoSelectionPlaceholder()

        case .videoPlaying(let minutesRemaining, let videoId):
            VideoPlayingPlaceholder(minutesRemaining: minutesRemaining, videoId: videoId)

        case .parentDashboard:
            ParentDashboardPlaceholder()
        }
    }

    // MARK: - Activity Selection Routing

    /// Routes to the appropriate activity selection view based on activity type
    @ViewBuilder
    private func activitySelectionView(for activityType: ActivityType) -> some View {
        switch activityType {
        case .raetsel:
            RaetselSelectionView()

        case .zahlen:
            ZahlenSelectionView()

        case .zeichnen, .logik:
            // Locked activities should never reach here, but provide fallback
            LockedActivityFallback(activityType: activityType)
        }
    }
}

// MARK: - Locked Activity Fallback

/// Fallback view for locked activities (should not normally be shown)
private struct LockedActivityFallback: View {
    @Environment(AppCoordinator.self) private var coordinator
    let activityType: ActivityType

    var body: some View {
        VStack(spacing: 24) {
            Image(systemName: "lock.fill")
                .font(.system(size: 60))
                .foregroundColor(BennieColors.chain)

            Text("\(activityType.displayName) ist noch gesperrt")
                .font(BennieFont.screenHeader())
                .foregroundColor(BennieColors.textDark)

            WoodButton("Zurück") {
                coordinator.navigateHome()
            }
        }
    }
}

// MARK: - Placeholder Views

/// These placeholder views will be replaced with actual implementations in later phases

private struct ActivitySelectionPlaceholder: View {
    @Environment(AppCoordinator.self) private var coordinator
    let activityType: ActivityType

    var body: some View {
        VStack(spacing: 24) {
            Text(activityType.displayName)
                .font(BennieFont.title())
                .foregroundStyle(BennieColors.woodDark)

            HStack(spacing: 20) {
                ForEach(SubActivity.subActivities(for: activityType), id: \.self) { subActivity in
                    Button {
                        coordinator.startPlaying(activityType, subActivity)
                    } label: {
                        VStack {
                            Image(systemName: "gamecontroller")
                                .font(.system(size: 40))
                            Text(subActivity.displayName)
                                .font(BennieFont.button())
                        }
                        .frame(width: 150, height: 100)
                        .background(BennieColors.woodLight)
                        .cornerRadius(16)
                    }
                    .buttonStyle(.plain)
                    .foregroundStyle(BennieColors.woodDark)
                }
            }

            Button("Zurück") {
                coordinator.navigateHome()
            }
            .buttonStyle(.bordered)
        }
    }
}

private struct PlayingPlaceholder: View {
    @Environment(AppCoordinator.self) private var coordinator
    @Environment(PlayerStore.self) private var playerStore
    let activityType: ActivityType
    let subActivity: SubActivity

    var body: some View {
        VStack(spacing: 24) {
            Text("Spielen: \(subActivity.displayName)")
                .font(BennieFont.title())
                .foregroundStyle(BennieColors.woodDark)

            Text("(\(activityType.displayName))")
                .font(BennieFont.body())

            Button("Level abschliessen (+1 Münze)") {
                if let newCoins = playerStore.awardCoin() {
                    if coordinator.shouldShowCelebration(for: newCoins) {
                        coordinator.showCelebration(coinsEarned: newCoins)
                    } else {
                        coordinator.navigateHome()
                    }
                }
            }
            .buttonStyle(.borderedProminent)

            Button("Zurück") {
                coordinator.navigateHome()
            }
            .buttonStyle(.bordered)
        }
    }
}

private struct LevelCompletePlaceholder: View {
    @Environment(AppCoordinator.self) private var coordinator

    var body: some View {
        VStack(spacing: 24) {
            Text("Level Geschafft!")
                .font(BennieFont.title())
                .foregroundStyle(BennieColors.success)

            Button("Weiter") {
                coordinator.navigateHome()
            }
            .buttonStyle(.borderedProminent)
        }
    }
}

private struct TreasurePlaceholder: View {
    @Environment(AppCoordinator.self) private var coordinator
    @Environment(PlayerStore.self) private var playerStore

    var body: some View {
        VStack(spacing: 24) {
            Text("Schatztruhe")
                .font(BennieFont.title())
                .foregroundStyle(BennieColors.woodDark)

            if let player = playerStore.activePlayer {
                Text("\(player.coins) Münzen")
                    .font(BennieFont.screenHeader())

                VStack(spacing: 16) {
                    Button("5 Min YouTube (10 Münzen)") {
                        if playerStore.spendCoins(10) {
                            coordinator.startVideoPlayback(minutes: 5, videoId: "qw0Jz5zJkgE")
                        }
                    }
                    .buttonStyle(.borderedProminent)
                    .disabled(!player.canRedeemTier1)

                    Button("12 Min YouTube (20 Münzen)") {
                        if playerStore.spendCoins(20) {
                            coordinator.startVideoPlayback(minutes: 12, videoId: "qw0Jz5zJkgE")
                        }
                    }
                    .buttonStyle(.borderedProminent)
                    .disabled(!player.canRedeemTier2)
                }
            }

            Button("Zurück") {
                coordinator.navigateHome()
            }
            .buttonStyle(.bordered)
        }
    }
}

private struct VideoSelectionPlaceholder: View {
    @Environment(AppCoordinator.self) private var coordinator

    var body: some View {
        VStack(spacing: 24) {
            Text("Video auswählen")
                .font(BennieFont.title())
                .foregroundStyle(BennieColors.woodDark)

            Text("(Videos werden später hinzugefügt)")
                .font(BennieFont.body())

            Button("Zurück") {
                coordinator.navigateHome()
            }
            .buttonStyle(.bordered)
        }
    }
}

private struct VideoPlayingPlaceholder: View {
    @Environment(AppCoordinator.self) private var coordinator
    let minutesRemaining: Int
    let videoId: String

    var body: some View {
        VStack(spacing: 24) {
            Text("Video läuft...")
                .font(BennieFont.title())
                .foregroundStyle(BennieColors.woodDark)

            Text("\(minutesRemaining) Minuten")
                .font(BennieFont.number())

            Text("Video ID: \(videoId)")
                .font(BennieFont.label())
                .foregroundStyle(BennieColors.woodMedium)

            Button("Fertig") {
                coordinator.navigateHome()
            }
            .buttonStyle(.borderedProminent)
        }
    }
}

private struct ParentGatePlaceholder: View {
    @Environment(AppCoordinator.self) private var coordinator
    @State private var answer = ""

    var body: some View {
        VStack(spacing: 24) {
            Text("Elternbereich")
                .font(BennieFont.title())
                .foregroundStyle(BennieColors.woodDark)

            Text("7 + 5 = ?")
                .font(BennieFont.screenHeader())

            TextField("Antwort", text: $answer)
                .textFieldStyle(.roundedBorder)
                .keyboardType(.numberPad)
                .frame(width: 100)

            HStack(spacing: 20) {
                Button("Abbrechen") {
                    coordinator.navigateHome()
                }
                .buttonStyle(.bordered)

                Button("Bestätigen") {
                    if answer == "12" {
                        coordinator.navigateToParentDashboard()
                    }
                }
                .buttonStyle(.borderedProminent)
            }
        }
    }
}

private struct ParentDashboardPlaceholder: View {
    @Environment(AppCoordinator.self) private var coordinator
    @Environment(PlayerStore.self) private var playerStore

    var body: some View {
        VStack(spacing: 24) {
            Text("Einstellungen")
                .font(BennieFont.title())
                .foregroundStyle(BennieColors.woodDark)

            ForEach(playerStore.players) { player in
                HStack {
                    Text(player.name)
                        .font(BennieFont.button())
                    Spacer()
                    Text("\(player.coins) Münzen")
                    Text("Gesamt: \(player.totalCoinsEarned)")
                        .foregroundStyle(.secondary)
                }
                .padding()
                .background(BennieColors.woodLight)
                .cornerRadius(8)
            }

            Button("Fortschritt zurücksetzen") {
                playerStore.resetAllProgress()
            }
            .buttonStyle(.bordered)
            .tint(.red)

            Button("Zurück") {
                coordinator.navigateHome()
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }
}

// MARK: - Preview

#Preview {
    ContentView()
        .environment(AppCoordinator())
        .environment(PlayerStore())
}
