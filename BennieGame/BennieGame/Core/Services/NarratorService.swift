import Foundation

/// NarratorService provides typed voice triggers for all narrator voice lines.
/// The narrator uses a warm, professional female German voice.
@Observable
class NarratorService {
    private let audioManager: AudioManager

    init(audioManager: AudioManager) {
        self.audioManager = audioManager
    }

    // MARK: - Loading Screen

    func playLoadingComplete() {
        audioManager.playVoice("narrator_loading_complete")
    }

    // MARK: - Player Selection

    func playPlayerQuestion() {
        audioManager.playVoice("narrator_player_question")
    }

    func playHello(playerName: String) {
        let filename = playerName.lowercased() == "alexander"
            ? "narrator_hello_alexander"
            : "narrator_hello_oliver"
        audioManager.playVoice(filename)
    }

    // MARK: - Home

    func playHomeQuestion() {
        audioManager.playVoice("narrator_home_question")
    }

    // MARK: - Activities

    func playPuzzleStart() {
        audioManager.playVoice("narrator_puzzle_start")
    }

    func playLabyrinthStart() {
        audioManager.playVoice("narrator_labyrinth_start")
    }

    func playDiceStart() {
        audioManager.playVoice("narrator_dice_start")
    }

    func playShowNumber(_ number: Int) {
        guard (1...6).contains(number) else { return }
        audioManager.playVoice("narrator_show_number_\(number)")
    }

    func playChooseNumber(_ number: Int) {
        guard (1...10).contains(number) else { return }
        audioManager.playVoice("narrator_choose_number_\(number)")
    }

    // MARK: - Video

    func playFilmAb() {
        audioManager.playVoice("narrator_film_ab")
    }

    // MARK: - Success Pool (random selection)

    private let successPhrases = [
        "success_super", "success_toll", "success_wunderbar",
        "success_genau", "success_super_gemacht", "success_perfekt", "success_bravo"
    ]
    private var recentSuccess: [String] = []

    func playRandomSuccess() {
        // Avoid repeating last 3 phrases
        let available = successPhrases.filter { !recentSuccess.contains($0) }
        guard let phrase = available.randomElement() else { return }

        recentSuccess.append(phrase)
        if recentSuccess.count > 3 { recentSuccess.removeFirst() }

        audioManager.playVoice(phrase)
    }
}
