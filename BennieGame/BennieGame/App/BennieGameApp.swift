import SwiftUI

@main
struct BennieGameApp: App {
    // MARK: - State

    /// The app coordinator manages navigation and state transitions
    @State private var coordinator = AppCoordinator()

    /// The player store manages player data and persistence
    @State private var playerStore = PlayerStore()

    // MARK: - Body

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(coordinator)
                .environment(playerStore)
        }
    }
}
