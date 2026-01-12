import Foundation

// MARK: - Game State

/// Represents all possible states in the game flow
/// Each state corresponds to a distinct screen or overlay in the app
enum GameState: Equatable {
    /// Initial loading screen with progress bar
    case loading

    /// Player selection screen (Alexander or Oliver)
    case playerSelection

    /// Main home screen with activity menu
    case home

    /// Activity selection within an activity type
    case activitySelection(ActivityType)

    /// Actively playing a sub-activity
    case playing(ActivityType, SubActivity)

    /// Level completed, showing success
    case levelComplete

    /// Celebration overlay shown every 5 coins
    case celebrationOverlay(coinsEarned: Int)

    /// Treasure screen for YouTube redemption
    case treasureScreen

    /// Video selection from approved list
    case videoSelection

    /// Playing YouTube video with countdown
    case videoPlaying(minutesRemaining: Int, videoId: String)

    /// Parent gate math challenge
    case parentGate

    /// Parent dashboard for settings
    case parentDashboard
}

// MARK: - Activity Type

/// The main activity categories available in the game
enum ActivityType: String, CaseIterable, Codable, Equatable {
    case raetsel = "Rätsel"
    case zahlen = "Zahlen"
    case zeichnen = "Zeichnen"  // Locked for future release
    case logik = "Logik"        // Locked for future release

    /// Whether this activity is currently locked
    var isLocked: Bool {
        self == .zeichnen || self == .logik
    }

    /// Display name for the activity
    var displayName: String {
        rawValue
    }

    /// Icon name for the activity (SF Symbol or custom)
    var iconName: String {
        switch self {
        case .raetsel: return "puzzlepiece"
        case .zahlen: return "123.rectangle"
        case .zeichnen: return "pencil.and.scribble"
        case .logik: return "brain"
        }
    }
}

// MARK: - Sub Activity

/// Specific activities within each activity type
enum SubActivity: String, CaseIterable, Codable, Equatable {
    // Rätsel sub-activities
    case puzzleMatching = "Puzzle"
    case labyrinth = "Labyrinth"

    // Zahlen sub-activities
    case wuerfel = "Würfel"
    case waehleZahl = "Wähle die Zahl"

    /// The parent activity type for this sub-activity
    var parentActivity: ActivityType {
        switch self {
        case .puzzleMatching, .labyrinth:
            return .raetsel
        case .wuerfel, .waehleZahl:
            return .zahlen
        }
    }

    /// Display name for the sub-activity
    var displayName: String {
        rawValue
    }

    /// Available sub-activities for a given activity type
    static func subActivities(for activityType: ActivityType) -> [SubActivity] {
        switch activityType {
        case .raetsel:
            return [.puzzleMatching, .labyrinth]
        case .zahlen:
            return [.wuerfel, .waehleZahl]
        case .zeichnen, .logik:
            return [] // Locked activities have no sub-activities yet
        }
    }
}
