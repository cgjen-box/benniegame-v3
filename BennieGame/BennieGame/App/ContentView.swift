import SwiftUI

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
    }

    // MARK: - View Routing

    /// Returns the appropriate view for the given game state
    @ViewBuilder
    private func viewForState(_ state: GameState) -> some View {
        switch state {
        case .loading:
            LoadingPlaceholder()

        case .playerSelection:
            PlayerSelectionPlaceholder()

        case .home:
            HomePlaceholder()

        case .activitySelection(let activityType):
            ActivitySelectionPlaceholder(activityType: activityType)

        case .playing(let activityType, let subActivity):
            PlayingPlaceholder(activityType: activityType, subActivity: subActivity)

        case .levelComplete:
            LevelCompletePlaceholder()

        case .celebrationOverlay(let coinsEarned):
            CelebrationPlaceholder(coinsEarned: coinsEarned)

        case .treasureScreen:
            TreasurePlaceholder()

        case .videoSelection:
            VideoSelectionPlaceholder()

        case .videoPlaying(let minutesRemaining):
            VideoPlayingPlaceholder(minutesRemaining: minutesRemaining)

        case .parentGate:
            ParentGatePlaceholder()

        case .parentDashboard:
            ParentDashboardPlaceholder()
        }
    }
}

// MARK: - Placeholder Views

/// These placeholder views will be replaced with actual implementations in later phases

private struct LoadingPlaceholder: View {
    @Environment(AppCoordinator.self) private var coordinator

    var body: some View {
        VStack(spacing: 24) {
            Image(systemName: "bear.fill")
                .font(.system(size: 80))
                .foregroundStyle(BennieColors.bennieBrown)

            Text("Lade...")
                .font(BennieFont.title())
                .foregroundStyle(BennieColors.woodDark)

            Button("Weiter") {
                coordinator.transition(to: .playerSelection)
            }
            .buttonStyle(.borderedProminent)
        }
    }
}

private struct PlayerSelectionPlaceholder: View {
    @Environment(AppCoordinator.self) private var coordinator
    @Environment(PlayerStore.self) private var playerStore

    var body: some View {
        VStack(spacing: 24) {
            Text("Wer spielt heute?")
                .font(BennieFont.title())
                .foregroundStyle(BennieColors.woodDark)

            HStack(spacing: 40) {
                ForEach(playerStore.players) { player in
                    Button {
                        playerStore.selectPlayer(id: player.id)
                        coordinator.navigateHome()
                    } label: {
                        VStack {
                            Image(systemName: "person.circle.fill")
                                .font(.system(size: 60))
                            Text(player.name)
                                .font(BennieFont.button())
                            Text("\(player.coins) Munzen")
                                .font(BennieFont.label())
                        }
                        .padding()
                        .background(BennieColors.woodLight)
                        .cornerRadius(16)
                    }
                    .buttonStyle(.plain)
                    .foregroundStyle(BennieColors.woodDark)
                }
            }
        }
    }
}

private struct HomePlaceholder: View {
    @Environment(AppCoordinator.self) private var coordinator
    @Environment(PlayerStore.self) private var playerStore

    var body: some View {
        VStack(spacing: 24) {
            Text("Waldabenteuer")
                .font(BennieFont.title())
                .foregroundStyle(BennieColors.woodDark)

            if let player = playerStore.activePlayer {
                Text("Hallo, \(player.name)!")
                    .font(BennieFont.screenHeader())
                    .foregroundStyle(BennieColors.bennieBrown)

                Text("\(player.coins) Munzen")
                    .font(BennieFont.body())
            }

            HStack(spacing: 20) {
                ForEach(ActivityType.allCases, id: \.self) { activity in
                    Button {
                        coordinator.navigateToActivity(activity)
                    } label: {
                        VStack {
                            Image(systemName: activity.iconName)
                                .font(.system(size: 40))
                            Text(activity.displayName)
                                .font(BennieFont.button())
                            if activity.isLocked {
                                Image(systemName: "lock.fill")
                                    .font(.caption)
                            }
                        }
                        .frame(width: 120, height: 120)
                        .background(activity.isLocked ? Color.gray.opacity(0.5) : BennieColors.woodLight)
                        .cornerRadius(16)
                    }
                    .buttonStyle(.plain)
                    .disabled(activity.isLocked)
                    .foregroundStyle(BennieColors.woodDark)
                }
            }

            HStack(spacing: 40) {
                Button("Schatztruhe") {
                    coordinator.navigateToTreasure()
                }
                .buttonStyle(.borderedProminent)
                .disabled((playerStore.activePlayer?.coins ?? 0) < 10)

                Button("Einstellungen") {
                    coordinator.showParentGate()
                }
                .buttonStyle(.bordered)
            }
        }
    }
}

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

            Button("Zuruck") {
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

            Button("Level abschliessen (+1 Munze)") {
                if let newCoins = playerStore.awardCoin() {
                    if coordinator.shouldShowCelebration(for: newCoins) {
                        coordinator.showCelebration(coinsEarned: newCoins)
                    } else {
                        coordinator.navigateHome()
                    }
                }
            }
            .buttonStyle(.borderedProminent)

            Button("Zuruck") {
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

private struct CelebrationPlaceholder: View {
    @Environment(AppCoordinator.self) private var coordinator
    @Environment(PlayerStore.self) private var playerStore
    let coinsEarned: Int

    var body: some View {
        VStack(spacing: 24) {
            Text("Super gemacht!")
                .font(BennieFont.title())
                .foregroundStyle(BennieColors.coinGold)

            Text("\(coinsEarned) Munzen!")
                .font(BennieFont.number())
                .foregroundStyle(BennieColors.coinGold)

            if playerStore.activePlayer?.canRedeemTier1 == true {
                Button("Zur Schatztruhe!") {
                    coordinator.navigateToTreasure()
                }
                .buttonStyle(.borderedProminent)
            }

            Button("Weiter spielen") {
                coordinator.navigateHome()
            }
            .buttonStyle(.bordered)
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
                Text("\(player.coins) Munzen")
                    .font(BennieFont.screenHeader())

                VStack(spacing: 16) {
                    Button("5 Min YouTube (10 Munzen)") {
                        if playerStore.spendCoins(10) {
                            coordinator.startVideoPlayback(minutes: 5)
                        }
                    }
                    .buttonStyle(.borderedProminent)
                    .disabled(!player.canRedeemTier1)

                    Button("12 Min YouTube (20 Munzen)") {
                        if playerStore.spendCoins(20) {
                            coordinator.startVideoPlayback(minutes: 12)
                        }
                    }
                    .buttonStyle(.borderedProminent)
                    .disabled(!player.canRedeemTier2)
                }
            }

            Button("Zuruck") {
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
            Text("Video auswahlen")
                .font(BennieFont.title())
                .foregroundStyle(BennieColors.woodDark)

            Text("(Videos werden spater hinzugefugt)")
                .font(BennieFont.body())

            Button("Zuruck") {
                coordinator.navigateHome()
            }
            .buttonStyle(.bordered)
        }
    }
}

private struct VideoPlayingPlaceholder: View {
    @Environment(AppCoordinator.self) private var coordinator
    let minutesRemaining: Int

    var body: some View {
        VStack(spacing: 24) {
            Text("Video lauft...")
                .font(BennieFont.title())
                .foregroundStyle(BennieColors.woodDark)

            Text("\(minutesRemaining) Minuten")
                .font(BennieFont.number())

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

                Button("Bestatigen") {
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
                    Text("\(player.coins) Munzen")
                    Text("Gesamt: \(player.totalCoinsEarned)")
                        .foregroundStyle(.secondary)
                }
                .padding()
                .background(BennieColors.woodLight)
                .cornerRadius(8)
            }

            Button("Fortschritt zurucksetzen") {
                playerStore.resetAllProgress()
            }
            .buttonStyle(.bordered)
            .tint(.red)

            Button("Zuruck") {
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
