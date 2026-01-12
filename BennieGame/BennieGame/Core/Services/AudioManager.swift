import AVFoundation
import Foundation

/// AudioManager provides a 3-channel audio architecture for the BennieGame.
///
/// Channels:
/// - **Music**: Background ambient music (looping, ducked during voice)
/// - **Voice**: Narrator and Bennie voice lines (queued, full volume)
/// - **Effects**: Sound effects (immediate playback, no queuing)
///
/// Features:
/// - Voice ducking: Music automatically reduces to 15% during voice playback
/// - Voice queue: Multiple voice lines are queued and played sequentially
/// - Mute control: Global mute affects all channels
/// - Graceful fallback: Missing audio files are logged but don't crash
@Observable
class AudioManager {
    // MARK: - Audio Players

    private var musicPlayer: AVAudioPlayer?
    private var voicePlayer: AVAudioPlayer?
    private var effectsPlayer: AVAudioPlayer?

    // MARK: - Volume Controls

    /// Music channel volume (default: 30%)
    var musicVolume: Float = 0.30 {
        didSet {
            musicPlayer?.volume = isMuted ? 0 : (isVoicePlaying ? 0.15 : musicVolume)
        }
    }

    /// Voice channel volume (default: 100%)
    var voiceVolume: Float = 1.00 {
        didSet {
            voicePlayer?.volume = isMuted ? 0 : voiceVolume
        }
    }

    /// Effects channel volume (default: 70%)
    var effectsVolume: Float = 0.70 {
        didSet {
            effectsPlayer?.volume = isMuted ? 0 : effectsVolume
        }
    }

    // MARK: - State

    /// Global mute state
    var isMuted: Bool = false {
        didSet {
            updateAllVolumes()
        }
    }

    /// Indicates whether a voice line is currently playing
    private(set) var isVoicePlaying: Bool = false

    /// Stored music volume before ducking
    private var preDuckMusicVolume: Float = 0.30

    // MARK: - Voice Queue

    /// Queue for voice lines waiting to be played
    private var voiceQueue: [(filename: String, completion: (() -> Void)?)] = []

    /// Delegate to handle voice playback completion
    private var voiceDelegate: VoicePlayerDelegate?

    // MARK: - Initialization

    init() {
        setupAudioSession()
    }

    private func setupAudioSession() {
        do {
            try AVAudioSession.sharedInstance().setCategory(.playback, mode: .default)
            try AVAudioSession.sharedInstance().setActive(true)
        } catch {
            print("⚠️ AudioManager: Failed to setup audio session: \(error)")
        }
    }

    // MARK: - Music Channel

    /// Plays background music on the music channel.
    /// - Parameters:
    ///   - filename: The audio file name (without path, extension optional)
    ///   - loop: Whether to loop the music (default: true)
    func playMusic(_ filename: String, loop: Bool = true) {
        guard let url = getAudioURL(filename) else {
            print("⚠️ AudioManager: Music file not found: \(filename)")
            return
        }

        do {
            musicPlayer = try AVAudioPlayer(contentsOf: url)
            musicPlayer?.numberOfLoops = loop ? -1 : 0
            musicPlayer?.volume = isMuted ? 0 : musicVolume
            musicPlayer?.play()
            print("🎵 AudioManager: Playing music: \(filename)")
        } catch {
            print("⚠️ AudioManager: Failed to play music: \(error)")
        }
    }

    /// Stops the currently playing music.
    func stopMusic() {
        musicPlayer?.stop()
        musicPlayer = nil
        print("🎵 AudioManager: Music stopped")
    }

    /// Fades out the music over a specified duration.
    /// - Parameter duration: Fade duration in seconds (default: 1.0)
    func fadeOutMusic(duration: TimeInterval = 1.0) {
        guard let player = musicPlayer, player.isPlaying else { return }

        let steps = 20
        let stepDuration = duration / Double(steps)
        let volumeStep = player.volume / Float(steps)

        for i in 0..<steps {
            DispatchQueue.main.asyncAfter(deadline: .now() + stepDuration * Double(i)) { [weak self, weak player] in
                guard let player = player else { return }
                player.volume = max(0, player.volume - volumeStep)
                if i == steps - 1 {
                    self?.stopMusic()
                }
            }
        }
    }

    // MARK: - Voice Channel

    /// Plays a voice line on the voice channel.
    /// Voice lines are queued if another voice is currently playing.
    /// Music is automatically ducked during voice playback.
    /// - Parameters:
    ///   - filename: The audio file name (without path, extension optional)
    ///   - completion: Optional completion handler called when voice finishes
    func playVoice(_ filename: String, completion: (() -> Void)? = nil) {
        // Queue if voice is already playing
        if isVoicePlaying {
            voiceQueue.append((filename: filename, completion: completion))
            print("🎤 AudioManager: Voice queued: \(filename) (queue size: \(voiceQueue.count))")
            return
        }

        guard let url = getAudioURL(filename) else {
            print("⚠️ AudioManager: Voice file not found: \(filename)")
            completion?()
            playNextInQueue()
            return
        }

        isVoicePlaying = true
        duckMusic()

        do {
            voicePlayer = try AVAudioPlayer(contentsOf: url)
            voicePlayer?.volume = isMuted ? 0 : voiceVolume

            // Create and retain delegate
            voiceDelegate = VoicePlayerDelegate { [weak self] in
                self?.restoreMusic()
                self?.isVoicePlaying = false
                completion?()
                self?.playNextInQueue()
            }
            voicePlayer?.delegate = voiceDelegate
            voicePlayer?.play()
            print("🎤 AudioManager: Playing voice: \(filename)")
        } catch {
            print("⚠️ AudioManager: Failed to play voice: \(error)")
            restoreMusic()
            isVoicePlaying = false
            completion?()
            playNextInQueue()
        }
    }

    /// Stops the currently playing voice and clears the queue.
    func stopVoice() {
        voicePlayer?.stop()
        voicePlayer = nil
        voiceQueue.removeAll()
        isVoicePlaying = false
        restoreMusic()
        print("🎤 AudioManager: Voice stopped and queue cleared")
    }

    // MARK: - Effects Channel

    /// Plays a sound effect on the effects channel.
    /// Effects play immediately and don't queue.
    /// - Parameter filename: The audio file name (without path, extension optional)
    func playEffect(_ filename: String) {
        guard let url = getAudioURL(filename) else {
            print("⚠️ AudioManager: Effect file not found: \(filename)")
            return
        }

        do {
            effectsPlayer = try AVAudioPlayer(contentsOf: url)
            effectsPlayer?.volume = isMuted ? 0 : effectsVolume
            effectsPlayer?.play()
            print("🔊 AudioManager: Playing effect: \(filename)")
        } catch {
            print("⚠️ AudioManager: Failed to play effect: \(error)")
        }
    }

    // MARK: - Global Controls

    /// Stops all audio playback on all channels.
    func stopAll() {
        musicPlayer?.stop()
        voicePlayer?.stop()
        effectsPlayer?.stop()
        musicPlayer = nil
        voicePlayer = nil
        effectsPlayer = nil
        voiceQueue.removeAll()
        isVoicePlaying = false
        print("🔇 AudioManager: All audio stopped")
    }

    /// Toggles the global mute state.
    func toggleMute() {
        isMuted.toggle()
        print("🔇 AudioManager: Mute \(isMuted ? "enabled" : "disabled")")
    }

    // MARK: - Private Helpers

    private func updateAllVolumes() {
        musicPlayer?.volume = isMuted ? 0 : (isVoicePlaying ? 0.15 : musicVolume)
        voicePlayer?.volume = isMuted ? 0 : voiceVolume
        effectsPlayer?.volume = isMuted ? 0 : effectsVolume
    }

    private func duckMusic() {
        preDuckMusicVolume = musicVolume
        musicPlayer?.volume = isMuted ? 0 : 0.15
        print("🎵 AudioManager: Music ducked to 15%")
    }

    private func restoreMusic() {
        musicPlayer?.volume = isMuted ? 0 : preDuckMusicVolume
        print("🎵 AudioManager: Music restored to \(Int(preDuckMusicVolume * 100))%")
    }

    private func playNextInQueue() {
        guard !voiceQueue.isEmpty else { return }
        let next = voiceQueue.removeFirst()
        print("🎤 AudioManager: Playing next in queue: \(next.filename)")
        playVoice(next.filename, completion: next.completion)
    }

    /// Resolves an audio filename to a URL.
    /// Tries multiple extensions if none is provided.
    private func getAudioURL(_ filename: String) -> URL? {
        // Check if filename already has an extension
        let hasExtension = filename.contains(".")

        if hasExtension {
            return Bundle.main.url(forResource: filename, withExtension: nil)
        }

        // Try common audio extensions
        let extensions = ["aac", "mp3", "m4a", "wav", "caf"]
        for ext in extensions {
            if let url = Bundle.main.url(forResource: filename, withExtension: ext) {
                return url
            }
        }

        return nil
    }
}

// MARK: - Voice Player Delegate

/// Internal delegate class to handle AVAudioPlayer completion callbacks.
private class VoicePlayerDelegate: NSObject, AVAudioPlayerDelegate {
    private let onFinish: () -> Void

    init(onFinish: @escaping () -> Void) {
        self.onFinish = onFinish
        super.init()
    }

    func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        DispatchQueue.main.async {
            self.onFinish()
        }
    }
}
