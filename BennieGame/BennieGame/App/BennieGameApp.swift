import SwiftUI

@main
struct BennieGameApp: App {
    // MARK: - State

    /// The app coordinator manages navigation and state transitions
    @State private var coordinator = AppCoordinator()

    /// The player store manages player data and persistence
    @State private var playerStore = PlayerStore()

    /// The audio manager handles all audio playback (music, voice, effects)
    @State private var audioManager = AudioManager()

    // MARK: - Body

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(coordinator)
                .environment(playerStore)
                .environment(audioManager)
        }
    }
}
