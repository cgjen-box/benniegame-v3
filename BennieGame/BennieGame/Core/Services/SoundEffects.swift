import Foundation

/// Sound effects available in the game.
/// Each effect maps to an audio file in the Effects directory.
enum SoundEffect: String, CaseIterable {
    /// Wood tap sound for button presses
    case tapWood = "tap_wood"

    /// Chime sound for successful actions
    case successChime = "success_chime"

    /// Coin collection sound
    case coinCollect = "coin_collect"

    /// Fanfare for celebration milestones
    case celebrationFanfare = "celebration_fanfare"

    /// Chest opening sound in treasure screen
    case chestOpen = "chest_open"

    /// Gentle boop for navigation feedback
    case gentleBoop = "gentle_boop"

    /// Path drawing sound for labyrinth
    case pathDraw = "path_draw"

    /// The filename used by AudioManager
    var filename: String { rawValue }
}

// MARK: - AudioManager Extension

extension AudioManager {
    /// Plays a typed sound effect.
    /// - Parameter effect: The SoundEffect to play
    func playEffect(_ effect: SoundEffect) {
        playEffect(effect.filename)
    }
}
