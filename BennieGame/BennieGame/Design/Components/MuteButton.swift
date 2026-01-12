import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// MuteButton - Audio toggle control
// ═══════════════════════════════════════════════════════════════════════════
// Provides mute/unmute functionality with visual feedback
// Minimum 96pt touch target per playbook requirements
// ═══════════════════════════════════════════════════════════════════════════

/// Mute toggle button for audio control
/// Uses 96pt touch target per playbook requirements
struct MuteButton: View {
    // MARK: - Environment

    @Environment(AudioManager.self) private var audioManager

    // MARK: - Body

    var body: some View {
        Button {
            audioManager.toggleMute()
        } label: {
            Image(systemName: audioManager.isMuted ? "speaker.slash.fill" : "speaker.wave.2.fill")
                .font(.system(size: 28))
                .foregroundColor(BennieColors.woodDark)
                .frame(width: 96, height: 96)
                .background(
                    Circle()
                        .fill(BennieColors.woodLight)
                        .overlay(
                            Circle()
                                .stroke(BennieColors.woodDark, lineWidth: 2)
                        )
                )
        }
        .buttonStyle(.plain)
        .accessibilityLabel(audioManager.isMuted ? "Ton einschalten" : "Ton ausschalten")
        .accessibilityHint("Schaltet alle Töne ein oder aus")
    }
}

// MARK: - Previews

#Preview("MuteButton - Unmuted") {
    MuteButton()
        .environment(AudioManager())
}

#Preview("MuteButton - Muted") {
    let manager = AudioManager()
    manager.toggleMute()
    return MuteButton()
        .environment(manager)
}
