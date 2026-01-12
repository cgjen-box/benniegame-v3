import Foundation

// ═══════════════════════════════════════════════════════════════════════════
// VideoStore - Manages the list of approved YouTube videos
// ═══════════════════════════════════════════════════════════════════════════
// Provides persistence for parent-approved video list
// Allows adding, removing, and resetting videos
// ═══════════════════════════════════════════════════════════════════════════

/// Model for approved YouTube videos
struct ApprovedVideo: Identifiable, Codable, Equatable {
    let id: String  // YouTube video ID
    let title: String

    /// URL for the video thumbnail from YouTube
    var thumbnailURL: URL {
        URL(string: "https://img.youtube.com/vi/\(id)/mqdefault.jpg")!
    }

    /// Default kid-friendly German videos
    static let defaultVideos: [ApprovedVideo] = [
        ApprovedVideo(id: "qw0Jz5zJkgE", title: "Peppa Wutz"),
        ApprovedVideo(id: "eTxkAarT5Sg", title: "Conni"),
        ApprovedVideo(id: "dBwwePP4dNo", title: "Benjamin Blümchen"),
        ApprovedVideo(id: "6F53J-sYPhU", title: "Feuerwehrmann Sam"),
        ApprovedVideo(id: "WvQpDBXZDv4", title: "Bibi Blocksberg"),
        ApprovedVideo(id: "JE8_TBbW2yE", title: "Bobo Siebenschläfer")
    ]
}

/// Observable store managing the approved video list with persistence
@Observable
final class VideoStore {
    // MARK: - Properties

    /// The current list of approved videos
    private(set) var approvedVideos: [ApprovedVideo]

    /// UserDefaults key for persistence
    private let storageKey = "bennie.approved_videos"

    // MARK: - Initialization

    init() {
        self.approvedVideos = ApprovedVideo.defaultVideos
        load()
    }

    // MARK: - Public Methods

    /// Add a new video to the approved list
    /// - Parameters:
    ///   - youtubeId: The YouTube video ID
    ///   - title: The display title for the video
    func addVideo(youtubeId: String, title: String) {
        // Don't add duplicates
        guard !approvedVideos.contains(where: { $0.id == youtubeId }) else { return }

        let video = ApprovedVideo(id: youtubeId, title: title)
        approvedVideos.append(video)
        save()
    }

    /// Remove a video from the approved list
    /// - Parameter id: The YouTube video ID to remove
    func removeVideo(id: String) {
        approvedVideos.removeAll { $0.id == id }
        save()
    }

    /// Reset the video list to default values
    func resetToDefaults() {
        approvedVideos = ApprovedVideo.defaultVideos
        save()
    }

    // MARK: - Persistence

    private func save() {
        if let data = try? JSONEncoder().encode(approvedVideos) {
            UserDefaults.standard.set(data, forKey: storageKey)
        }
    }

    private func load() {
        guard let data = UserDefaults.standard.data(forKey: storageKey),
              let videos = try? JSONDecoder().decode([ApprovedVideo].self, from: data) else {
            return
        }
        approvedVideos = videos
    }
}
