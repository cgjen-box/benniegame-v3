import Foundation

// MARK: - Player Store

/// Manages player data and persistence using UserDefaults
/// Uses @Observable for SwiftUI reactivity
@Observable
final class PlayerStore {
    // MARK: - Properties

    /// All players in the game
    private(set) var players: [PlayerData]

    /// Currently active player (nil if none selected)
    private(set) var activePlayer: PlayerData?

    /// UserDefaults storage key
    private let storageKey = "bennie.players"

    // MARK: - Initialization

    init() {
        // Initialize with default players
        self.players = PlayerData.allPlayers
        self.activePlayer = nil

        // Load any saved data
        load()
    }

    // MARK: - Player Selection

    /// Select a player by their ID
    /// - Parameter id: The player's unique identifier
    func selectPlayer(id: String) {
        guard let index = players.firstIndex(where: { $0.id == id }) else { return }
        players[index].lastPlayedDate = Date()
        activePlayer = players[index]
        save()
    }

    /// Deselect the current player (return to player selection)
    func deselectPlayer() {
        activePlayer = nil
    }

    // MARK: - Coin Management

    /// Award one coin to the active player
    /// - Returns: The new coin count, or nil if no active player
    @discardableResult
    func awardCoin() -> Int? {
        guard var player = activePlayer,
              let index = players.firstIndex(where: { $0.id == player.id }) else {
            return nil
        }

        player.coins += 1
        player.totalCoinsEarned += 1
        players[index] = player
        activePlayer = player
        save()

        return player.coins
    }

    /// Award multiple coins to the active player
    /// - Parameter amount: Number of coins to award
    /// - Returns: The new coin count, or nil if no active player
    @discardableResult
    func awardCoins(_ amount: Int) -> Int? {
        guard amount > 0 else { return activePlayer?.coins }
        guard var player = activePlayer,
              let index = players.firstIndex(where: { $0.id == player.id }) else {
            return nil
        }

        player.coins += amount
        player.totalCoinsEarned += amount
        players[index] = player
        activePlayer = player
        save()

        return player.coins
    }

    /// Spend coins from the active player
    /// - Parameter amount: Number of coins to spend
    /// - Returns: true if successful, false if insufficient coins or no active player
    @discardableResult
    func spendCoins(_ amount: Int) -> Bool {
        guard var player = activePlayer,
              let index = players.firstIndex(where: { $0.id == player.id }),
              player.coins >= amount else {
            return false
        }

        player.coins -= amount
        players[index] = player
        activePlayer = player
        save()

        return true
    }

    // MARK: - Data Access

    /// Get a player by their ID
    /// - Parameter id: The player's unique identifier
    /// - Returns: The player data if found
    func getPlayer(id: String) -> PlayerData? {
        players.first { $0.id == id }
    }

    /// Get the coin count for the active player
    var activePlayerCoins: Int {
        activePlayer?.coins ?? 0
    }

    /// Check if celebration should show for active player
    var shouldShowCelebration: Bool {
        activePlayer?.shouldCelebrate ?? false
    }

    // MARK: - Persistence

    /// Save player data to UserDefaults
    private func save() {
        do {
            let data = try JSONEncoder().encode(players)
            UserDefaults.standard.set(data, forKey: storageKey)
        } catch {
            print("Failed to save player data: \(error)")
        }
    }

    /// Load player data from UserDefaults
    private func load() {
        guard let data = UserDefaults.standard.data(forKey: storageKey) else {
            // No saved data, keep defaults
            return
        }

        do {
            let savedPlayers = try JSONDecoder().decode([PlayerData].self, from: data)
            // Merge saved data with preset players (in case new players are added)
            for savedPlayer in savedPlayers {
                if let index = players.firstIndex(where: { $0.id == savedPlayer.id }) {
                    players[index] = savedPlayer
                }
            }
        } catch {
            print("Failed to load player data: \(error)")
        }
    }

    // MARK: - Reset

    /// Reset all player progress (for parent dashboard)
    func resetAllProgress() {
        players = PlayerData.allPlayers
        activePlayer = nil
        save()
    }

    /// Reset progress for a specific player
    /// - Parameter id: The player's unique identifier
    func resetProgress(for id: String) {
        guard let index = players.firstIndex(where: { $0.id == id }) else { return }

        // Find the default player data
        if let defaultPlayer = PlayerData.allPlayers.first(where: { $0.id == id }) {
            players[index] = defaultPlayer

            // If this was the active player, update it too
            if activePlayer?.id == id {
                activePlayer = defaultPlayer
            }
        }

        save()
    }
}
