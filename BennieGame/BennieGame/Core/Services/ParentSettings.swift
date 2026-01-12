import Foundation

// ═══════════════════════════════════════════════════════════════════════════
// ParentSettings - Manages parental control settings
// ═══════════════════════════════════════════════════════════════════════════
// Provides time limit configuration and tracking for video watching
// Persists settings across app restarts
// ═══════════════════════════════════════════════════════════════════════════

/// Observable store for parent settings with persistence
@Observable
final class ParentSettings {
    // MARK: - Properties

    /// Daily video time limit in minutes (0 = unlimited)
    var dailyTimeLimitMinutes: Int = 30 {
        didSet { save() }
    }

    /// Track video time watched today per player (playerId -> minutes)
    private(set) var timeWatchedToday: [String: Int] = [:]

    /// Whether time limits are enabled
    var timeLimitsEnabled: Bool = true {
        didSet { save() }
    }

    /// UserDefaults key for persistence
    private let storageKey = "bennie.parent_settings"

    // MARK: - Initialization

    init() {
        load()
    }

    // MARK: - Public Methods

    /// Record time watched for a player
    /// - Parameters:
    ///   - playerId: The player's ID
    ///   - minutes: Number of minutes watched
    func recordTimeWatched(playerId: String, minutes: Int) {
        timeWatchedToday[playerId, default: 0] += minutes
        save()
    }

    /// Get remaining time for today for a player
    /// - Parameter playerId: The player's ID
    /// - Returns: Remaining minutes (Int.max if unlimited)
    func remainingTimeToday(for playerId: String) -> Int {
        guard timeLimitsEnabled, dailyTimeLimitMinutes > 0 else { return Int.max }
        let watched = timeWatchedToday[playerId] ?? 0
        return max(0, dailyTimeLimitMinutes - watched)
    }

    /// Get time watched today for a player
    /// - Parameter playerId: The player's ID
    /// - Returns: Minutes watched today
    func timeWatched(for playerId: String) -> Int {
        timeWatchedToday[playerId] ?? 0
    }

    /// Reset daily tracking for all players
    func resetDailyTracking() {
        timeWatchedToday = [:]
        save()
    }

    /// Get a description of the current time limit setting
    var timeLimitDescription: String {
        if !timeLimitsEnabled {
            return "Aus"
        } else if dailyTimeLimitMinutes == 0 {
            return "Unbegrenzt"
        } else {
            return "\(dailyTimeLimitMinutes) Minuten"
        }
    }

    // MARK: - Persistence

    private func save() {
        let data: [String: Any] = [
            "dailyLimit": dailyTimeLimitMinutes,
            "enabled": timeLimitsEnabled,
            "watched": timeWatchedToday
        ]
        UserDefaults.standard.set(data, forKey: storageKey)
    }

    private func load() {
        guard let data = UserDefaults.standard.dictionary(forKey: storageKey) else { return }
        dailyTimeLimitMinutes = data["dailyLimit"] as? Int ?? 30
        timeLimitsEnabled = data["enabled"] as? Bool ?? true
        timeWatchedToday = data["watched"] as? [String: Int] ?? [:]
    }
}
