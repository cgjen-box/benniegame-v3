# Audio Manager Implementation

## 📚 Playbook References

**Read these playbook sections first:**
- **Part 5.3**: Audio Specifications - Technical requirements
- **Part 6**: Animation & Sound Guide - Sound effect library
- **Part 9.4**: ElevenLabs Voice Generation - Audio file production

**Voice Scripts:**
- **Part 3**: Narrator & Voice Script - Complete script for all screens

**Character Voice Guidelines:**
- **Part 1.2**: Character specifications (Bennie voice character)
- **Part 3.3**: Bennie Voice Guidelines

---

## 🔊 Overview

The Audio Manager controls three independent audio channels with priority-based ducking, ensuring voice lines are always clearly heard over music and effects.

## Three-Channel Architecture

```
╔══════════════════════════════════════════════════════════════════════╗
║                       AUDIO CHANNEL SYSTEM                           ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  🎵 MUSIC CHANNEL                                                    ║
║     - Background forest ambience                                    ║
║     - Default volume: 30%                                           ║
║     - Ducks to 15% when voice plays                                 ║
║     - Loops continuously                                            ║
║                                                                      ║
║  🗣️ VOICE CHANNEL                                                    ║
║     - Narrator + Bennie voices                                      ║
║     - Always 100% volume                                            ║
║     - HIGHEST PRIORITY                                              ║
║     - Triggers music ducking                                        ║
║                                                                      ║
║  🔔 EFFECTS CHANNEL                                                  ║
║     - UI sounds, celebrations, coins                                ║
║     - Default volume: 70%                                           ║
║     - NEVER plays during voice                                      ║
║     - Queued if voice is playing                                    ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

## Core AudioManager Class

```swift
import AVFoundation

class AudioManager: ObservableObject {
    static let shared = AudioManager()
    
    // Audio players
    private var musicPlayer: AVAudioPlayer?
    private var voicePlayer: AVAudioPlayer?
    private var effectsPlayer: AVAudioPlayer?
    
    // Volume levels
    @Published var musicVolume: Float = 0.30 {
        didSet { musicPlayer?.volume = musicVolume }
    }
    
    @Published var voiceVolume: Float = 1.00 {
        didSet { voicePlayer?.volume = voiceVolume }
    }
    
    @Published var effectsVolume: Float = 0.70 {
        didSet { effectsPlayer?.volume = effectsVolume }
    }
    
    @Published var isEnabled: Bool = true
    
    // State
    private var isVoicePlaying = false
    private var queuedEffect: String?
    
    // Volume constants
    private let defaultMusicVolume: Float = 0.30
    private let duckedMusicVolume: Float = 0.15
    
    private init() {
        configureAudioSession()
    }
    
    func configureAudioSession() {
        do {
            try AVAudioSession.sharedInstance().setCategory(.playback, mode: .default)
            try AVAudioSession.sharedInstance().setActive(true)
        } catch {
            print("Failed to set audio session: \(error)")
        }
    }
}
```

## Music Playback

```swift
extension AudioManager {
    func playBackgroundMusic(_ filename: String) {
        guard isEnabled else { return }
        
        guard let url = Bundle.main.url(forResource: filename, withExtension: nil) else {
            print("Music file not found: \(filename)")
            return
        }
        
        do {
            musicPlayer = try AVAudioPlayer(contentsOf: url)
            musicPlayer?.numberOfLoops = -1 // Infinite loop
            musicPlayer?.volume = musicVolume
            musicPlayer?.prepareToPlay()
            musicPlayer?.play()
        } catch {
            print("Failed to play music: \(error)")
        }
    }
    
    func stopBackgroundMusic() {
        musicPlayer?.stop()
        musicPlayer = nil
    }
    
    func duckMusic() {
        UIView.animate(withDuration: 0.2) {
            self.musicPlayer?.volume = self.duckedMusicVolume
        }
    }
    
    func restoreMusic() {
        UIView.animate(withDuration: 0.5) {
            self.musicPlayer?.volume = self.musicVolume
        }
    }
}
```

## Voice Playback (Priority)

```swift
extension AudioManager {
    func playNarrator(_ filename: String, completion: (() -> Void)? = nil) {
        playVoice(filename, speaker: .narrator, completion: completion)
    }
    
    func playBennie(_ filename: String, completion: (() -> Void)? = nil) {
        playVoice(filename, speaker: .bennie, completion: completion)
    }
    
    private func playVoice(_ filename: String, speaker: Speaker, completion: (() -> Void)? = nil) {
        guard isEnabled else {
            completion?()
            return
        }
        
        guard let url = Bundle.main.url(forResource: filename, withExtension: nil) else {
            print("Voice file not found: \(filename)")
            completion?()
            return
        }
        
        do {
            // Stop any current voice
            voicePlayer?.stop()
            
            // Duck music
            duckMusic()
            isVoicePlaying = true
            
            // Play voice
            voicePlayer = try AVAudioPlayer(contentsOf: url)
            voicePlayer?.volume = voiceVolume
            voicePlayer?.delegate = VoiceDelegate(manager: self, completion: completion)
            voicePlayer?.prepareToPlay()
            voicePlayer?.play()
            
        } catch {
            print("Failed to play voice: \(error)")
            restoreMusic()
            isVoicePlaying = false
            completion?()
        }
    }
    
    func onVoiceComplete() {
        isVoicePlaying = false
        restoreMusic()
        
        // Play queued effect if exists
        if let effect = queuedEffect {
            queuedEffect = nil
            playEffect(effect)
        }
    }
}

// Delegate to handle voice completion
class VoiceDelegate: NSObject, AVAudioPlayerDelegate {
    weak var manager: AudioManager?
    let completion: (() -> Void)?
    
    init(manager: AudioManager, completion: (() -> Void)?) {
        self.manager = manager
        self.completion = completion
    }
    
    func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        manager?.onVoiceComplete()
        completion?()
    }
}

enum Speaker {
    case narrator
    case bennie
}
```

## Effects Playback (Queued)

```swift
extension AudioManager {
    func playEffect(_ filename: String) {
        guard isEnabled else { return }
        
        // If voice is playing, queue the effect
        if isVoicePlaying {
            queuedEffect = filename
            return
        }
        
        guard let url = Bundle.main.url(forResource: filename, withExtension: nil) else {
            print("Effect file not found: \(filename)")
            return
        }
        
        do {
            effectsPlayer = try AVAudioPlayer(contentsOf: url)
            effectsPlayer?.volume = effectsVolume
            effectsPlayer?.prepareToPlay()
            effectsPlayer?.play()
        } catch {
            print("Failed to play effect: \(error)")
        }
    }
}
```

## Sound Effect Library

```swift
enum SoundEffect: String {
    // UI sounds
    case tapWood = "tap_wood.aac"
    case successChime = "success_chime.aac"
    case gentleBoop = "gentle_boop.aac"
    
    // Coin sounds
    case coinCollect = "coin_collect.aac"
    case coinSpend = "coin_spend.aac"
    
    // Celebrations
    case celebrationFanfare = "celebration_fanfare.aac"
    case chestOpen = "chest_open.aac"
    
    // Gameplay
    case pathDraw = "path_draw.aac"
    
    var filename: String {
        return rawValue
    }
}

// Usage
AudioManager.shared.playEffect(SoundEffect.coinCollect.filename)
```

## Preloading Audio

```swift
extension AudioManager {
    func preloadEssentialAudio() {
        // Preload frequently used sounds
        preloadEffect(SoundEffect.tapWood.filename)
        preloadEffect(SoundEffect.coinCollect.filename)
        preloadEffect(SoundEffect.successChime.filename)
        
        // Preload common voice lines
        preloadVoice("narrator_home_question.aac")
        preloadVoice("bennie_greeting_part1.aac")
    }
    
    private func preloadEffect(_ filename: String) {
        guard let url = Bundle.main.url(forResource: filename, withExtension: nil) else { return }
        
        do {
            let player = try AVAudioPlayer(contentsOf: url)
            player.prepareToPlay()
        } catch {
            print("Failed to preload effect: \(error)")
        }
    }
    
    private func preloadVoice(_ filename: String) {
        guard let url = Bundle.main.url(forResource: filename, withExtension: nil) else { return }
        
        do {
            let player = try AVAudioPlayer(contentsOf: url)
            player.prepareToPlay()
        } catch {
            print("Failed to preload voice: \(error)")
        }
    }
}
```

## Volume Controls (Settings)

```swift
struct VolumeControlView: View {
    @ObservedObject var audioManager = AudioManager.shared
    
    var body: some View {
        VStack(spacing: 20) {
            // Master toggle
            Toggle("Sounds", isOn: $audioManager.isEnabled)
                .font(.sfRounded(size: 20, weight: .semibold))
            
            if audioManager.isEnabled {
                // Music volume
                VStack(alignment: .leading) {
                    Text("🎵 Musik")
                        .font(.sfRounded(size: 18, weight: .medium))
                    Slider(value: $audioManager.musicVolume, in: 0...1)
                }
                
                // Effects volume
                VStack(alignment: .leading) {
                    Text("🔔 Effekte")
                        .font(.sfRounded(size: 18, weight: .medium))
                    Slider(value: $audioManager.effectsVolume, in: 0...1)
                }
                
                // Voice volume (optional)
                VStack(alignment: .leading) {
                    Text("🗣️ Stimme")
                        .font(.sfRounded(size: 18, weight: .medium))
                    Slider(value: $audioManager.voiceVolume, in: 0...1)
                }
            }
        }
        .padding()
    }
}
```

## App Lifecycle Integration

```swift
@main
struct BennieGameApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .onAppear {
                    AudioManager.shared.preloadEssentialAudio()
                    AudioManager.shared.playBackgroundMusic("forest_ambient.aac")
                }
        }
    }
}

class AppDelegate: NSObject, UIApplicationDelegate {
    func applicationDidEnterBackground(_ application: UIApplication) {
        // Pause music when app goes to background
        AudioManager.shared.musicPlayer?.pause()
    }
    
    func applicationWillEnterForeground(_ application: UIApplication) {
        // Resume music when app returns to foreground
        AudioManager.shared.musicPlayer?.play()
    }
}
```

## Testing Checklist

```
MUSIC:
□ Background music plays on app launch
□ Music loops infinitely
□ Music volume is 30% by default
□ Music ducks to 15% when voice plays
□ Music restores to 30% after voice completes
□ Music pauses when app goes to background
□ Music resumes when app returns to foreground
□ Music stops when app is terminated
□ Volume slider controls music level

VOICE:
□ Narrator voice plays at 100% volume
□ Bennie voice plays at 100% volume
□ Music ducks immediately when voice starts
□ Music restores smoothly after voice ends
□ Voice always audible over music
□ Stopping mid-voice restores music correctly
□ Multiple voice calls queue properly
□ Voice completion callback fires

EFFECTS:
□ UI sounds play at 70% volume
□ Effects NEVER play during voice
□ Effects queue if voice is playing
□ Queued effects play after voice ends
□ Effects don't duck music
□ Volume slider controls effects level

INTEGRATION:
□ All audio files bundled correctly
□ No audio lag (< 100ms from trigger)
□ No audio clipping or distortion
□ Simultaneous sounds don't crash
□ Memory usage stable during playback
□ Audio session configured properly
□ Works with system volume buttons
□ Works with mute switch (respects it)
□ Works with AirPlay/Bluetooth

EDGE CASES:
□ Missing audio file → logs error, continues
□ Multiple rapid voice calls → queues properly
□ App interrupted (phone call) → pauses/resumes
□ Low battery mode → still plays audio
□ iPad in silent mode → still plays (playback category)
```

## Performance Monitoring

```swift
extension AudioManager {
    func printDebugInfo() {
        print("=== Audio Manager Debug ===")
        print("Music playing: \(musicPlayer?.isPlaying ?? false)")
        print("Music volume: \(musicVolume)")
        print("Voice playing: \(isVoicePlaying)")
        print("Voice volume: \(voiceVolume)")
        print("Effects volume: \(effectsVolume)")
        print("Enabled: \(isEnabled)")
        print("Queued effect: \(queuedEffect ?? "none")")
        print("========================")
    }
}
```

## Error Handling

```swift
enum AudioError: Error {
    case fileNotFound(String)
    case playbackFailed(Error)
    case sessionConfigFailed(Error)
}

extension AudioManager {
    private func handleError(_ error: AudioError) {
        switch error {
        case .fileNotFound(let filename):
            print("❌ Audio file not found: \(filename)")
            // Log to analytics
            
        case .playbackFailed(let underlying):
            print("❌ Playback failed: \(underlying)")
            // Log to analytics
            
        case .sessionConfigFailed(let underlying):
            print("❌ Session config failed: \(underlying)")
            // Log to analytics
        }
    }
}
```

## Audio File Checklist

See `plan/09_asset_production/voice_lines.md` for complete voice line checklist.

### Essential Files to Bundle

```
Resources/Audio/
├── Music/
│   └── forest_ambient.aac
├── Narrator/
│   ├── narrator_loading_complete.aac
│   ├── narrator_player_question.aac
│   ├── narrator_home_question.aac
│   └── [see voice_lines.md for complete list]
├── Bennie/
│   ├── bennie_greeting_part1.aac
│   ├── bennie_greeting_part2.aac
│   └── [see voice_lines.md for complete list]
└── Effects/
    ├── tap_wood.aac
    ├── success_chime.aac
    ├── coin_collect.aac
    ├── celebration_fanfare.aac
    └── gentle_boop.aac
```
