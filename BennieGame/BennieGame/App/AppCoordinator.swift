import SwiftUI

/// Coordinates navigation and state flow across the app
@Observable
final class AppCoordinator {
    // MARK: - Properties

    /// Current game state
    var currentState: GameState = .loading

    // MARK: - Navigation

    /// Transition to a new game state
    func transition(to state: GameState) {
        currentState = state
    }
}

// MARK: - Game State

/// Represents all possible states in the game flow
enum GameState {
    case loading
    case playerSelection
    case home
    // More states to be added in Phase 2
}
