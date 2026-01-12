import Foundation

/// BennieService provides typed voice triggers for all Bennie character voice lines.
/// Bennie uses a warm, friendly male German voice as the main character companion.
@Observable
class BennieService {
    private let audioManager: AudioManager

    init(audioManager: AudioManager) {
        self.audioManager = audioManager
    }

    // MARK: - Home Screen

    func playGreetingPart1(playerName: String) {
        // "Hi [Name], ich bin Bennie!"
        let filename = playerName.lowercased() == "alexander"
            ? "bennie_greeting_alexander_part1"
            : "bennie_greeting_oliver_part1"
        audioManager.playVoice(filename)
    }

    func playGreetingPart2() {
        audioManager.playVoice("bennie_greeting_part2")
    }

    func playReturnPart1() {
        audioManager.playVoice("bennie_return_part1")
    }

    func playReturnPart2() {
        audioManager.playVoice("bennie_return_part2")
    }

    func playLocked() {
        audioManager.playVoice("bennie_locked")
    }

    // MARK: - Activities

    func playPuzzleStart() {
        audioManager.playVoice("bennie_puzzle_start")
    }

    func playLabyrinthStart() {
        audioManager.playVoice("bennie_labyrinth_start")
    }

    func playLabyrinthWrong() {
        audioManager.playVoice("bennie_labyrinth_wrong")
    }

    func playWrongNumber() {
        audioManager.playVoice("bennie_wrong_number")
    }

    // MARK: - Hints (idle timeouts)

    func playPuzzleHint10s() {
        audioManager.playVoice("bennie_puzzle_hint_10s")
    }

    func playPuzzleHint20s() {
        audioManager.playVoice("bennie_puzzle_hint_20s")
    }

    func playLabyrinthHint() {
        audioManager.playVoice("bennie_labyrinth_hint")
    }

    func playDiceHint10s() {
        audioManager.playVoice("bennie_dice_hint_10s")
    }

    func playDiceHint20s() {
        audioManager.playVoice("bennie_dice_hint_20s")
    }

    func playDiceHint30s() {
        audioManager.playVoice("bennie_dice_hint_30s")
    }

    func playChooseHint10s() {
        audioManager.playVoice("bennie_choose_hint_10s")
    }

    func playChooseHint20s() {
        audioManager.playVoice("bennie_choose_hint_20s")
    }

    // MARK: - Celebration

    func playCelebration(coins: Int) {
        let milestone = (coins / 5) * 5
        switch milestone {
        case 5: audioManager.playVoice("bennie_celebration_5")
        case 10: audioManager.playVoice("bennie_celebration_10")
        case 15: audioManager.playVoice("bennie_celebration_15")
        case 20: audioManager.playVoice("bennie_celebration_20")
        default: audioManager.playVoice("bennie_celebration_5")
        }
    }

    // MARK: - Treasure

    func playTreasureMessage(coins: Int) {
        if coins < 10 {
            audioManager.playVoice("bennie_treasure_under10")
        } else if coins < 20 {
            audioManager.playVoice("bennie_treasure_over10")
        } else {
            audioManager.playVoice("bennie_treasure_over20")
        }
    }

    // MARK: - Video

    func playOneMinuteWarning() {
        audioManager.playVoice("bennie_video_1min")
    }

    func playTimeUp() {
        audioManager.playVoice("bennie_video_timeup")
    }
}
