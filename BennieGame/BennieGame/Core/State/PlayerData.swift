import Foundation

// MARK: - Player Data

/// Represents a player's profile and progress in the game
/// Codable for UserDefaults persistence
struct PlayerData: Codable, Identifiable, Equatable {
    /// Unique identifier for the player ("alexander" or "oliver")
    let id: String

    /// Display name for the player
    let name: String

    /// Current coin balance (can be spent on YouTube time)
    var coins: Int

    /// Total coins ever earned (for statistics)
    var totalCoinsEarned: Int

    /// Last date the player played
    var lastPlayedDate: Date?

    // MARK: - Preset Players

    /// Alexander - first preset player
    static let alexander = PlayerData(
        id: "alexander",
        name: "Alexander",
        coins: 0,
        totalCoinsEarned: 0,
        lastPlayedDate: nil
    )

    /// Oliver - second preset player
    static let oliver = PlayerData(
        id: "oliver",
        name: "Oliver",
        coins: 0,
        totalCoinsEarned: 0,
        lastPlayedDate: nil
    )

    /// All available players
    static let allPlayers: [PlayerData] = [.alexander, .oliver]
}

// MARK: - Player Data Extensions

extension PlayerData {
    /// Check if celebration should trigger (every 5 coins)
    var shouldCelebrate: Bool {
        coins > 0 && coins % 5 == 0
    }

    /// Check if player can redeem for 5 min YouTube (10 coins)
    var canRedeemTier1: Bool {
        coins >= 10
    }

    /// Check if player can redeem for 10 min YouTube (20 coins)
    var canRedeemTier2: Bool {
        coins >= 20
    }

    /// Coins needed for next YouTube redemption tier
    var coinsNeededForTier1: Int {
        max(0, 10 - coins)
    }

    /// Coins needed for tier 2 YouTube redemption
    var coinsNeededForTier2: Int {
        max(0, 20 - coins)
    }
}
