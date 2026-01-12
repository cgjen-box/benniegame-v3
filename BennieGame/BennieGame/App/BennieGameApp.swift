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

    /// The video store manages approved videos list
    @State private var videoStore = VideoStore()

    /// The parent settings manages time limits and parental controls
    @State private var parentSettings = ParentSettings()

    // MARK: - Voice Services (computed properties to use shared AudioManager)

    /// Narrator service for instructional voice lines
    private var narratorService: NarratorService { NarratorService(audioManager: audioManager) }

    /// Bennie character service for companion voice lines
    private var bennieService: BennieService { BennieService(audioManager: audioManager) }

    // MARK: - Body

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(coordinator)
                .environment(playerStore)
                .environment(audioManager)
                .environment(narratorService)
                .environment(bennieService)
                .environment(videoStore)
                .environment(parentSettings)
        }
    }
}
