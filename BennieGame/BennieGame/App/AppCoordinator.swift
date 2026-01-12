import SwiftUI

/// Coordinates navigation and state flow across the app
@Observable
final class AppCoordinator {
    // MARK: - Properties

    /// Current game state
    var currentState: GameState = .loading

    /// History of states for potential back navigation
    private var stateHistory: [GameState] = []

    /// Allocated video time in minutes (set when redeeming coins)
    var allocatedVideoMinutes: Int = 0

    // MARK: - Navigation

    /// Transition to a new game state
    func transition(to state: GameState) {
        stateHistory.append(currentState)
        currentState = state
    }

    /// Navigate back to previous state if available
    func navigateBack() {
        guard let previousState = stateHistory.popLast() else { return }
        currentState = previousState
    }

    /// Navigate to home screen
    func navigateHome() {
        stateHistory.removeAll()
        currentState = .home
    }

    /// Navigate to a specific activity type selection
    func navigateToActivity(_ type: ActivityType) {
        guard !type.isLocked else { return }
        transition(to: .activitySelection(type))
    }

    /// Start playing a specific sub-activity
    func startPlaying(_ activity: ActivityType, _ subActivity: SubActivity) {
        transition(to: .playing(activity, subActivity))
    }

    /// Handle level completion
    func handleLevelComplete() {
        transition(to: .levelComplete)
    }

    /// Check if celebration should be shown (every 5 coins)
    func shouldShowCelebration(for coinCount: Int) -> Bool {
        coinCount > 0 && coinCount % 5 == 0
    }

    /// Show celebration overlay
    func showCelebration(coinsEarned: Int) {
        transition(to: .celebrationOverlay(coinsEarned: coinsEarned))
    }

    /// Navigate to treasure screen
    func navigateToTreasure() {
        transition(to: .treasureScreen)
    }

    /// Navigate to video selection
    func navigateToVideoSelection() {
        transition(to: .videoSelection)
    }

    /// Start video playback with time limit and video ID
    func startVideoPlayback(minutes: Int, videoId: String) {
        transition(to: .videoPlaying(minutesRemaining: minutes, videoId: videoId))
    }

    /// Show parent gate
    func showParentGate() {
        transition(to: .parentGate)
    }

    /// Navigate to parent dashboard (after passing gate)
    func navigateToParentDashboard() {
        transition(to: .parentDashboard)
    }
}
