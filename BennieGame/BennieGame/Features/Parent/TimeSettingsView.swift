import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// TimeSettingsView - Parent interface for managing video time limits
// ═══════════════════════════════════════════════════════════════════════════
// Allows parents to configure daily video time limits
// Shows current usage per player and allows resetting daily tracking
// All UI in German with minimum 96pt touch targets
// ═══════════════════════════════════════════════════════════════════════════

/// Parent view for managing time limit settings
struct TimeSettingsView: View {
    // MARK: - Environment

    @Environment(\.dismiss) private var dismiss
    @Environment(ParentSettings.self) private var parentSettings
    @Environment(PlayerStore.self) private var playerStore

    // MARK: - State

    @State private var showResetConfirmation: Bool = false

    // MARK: - Time Limit Options

    private let timeLimitOptions: [(value: Int, label: String)] = [
        (15, "15 Minuten"),
        (30, "30 Minuten"),
        (45, "45 Minuten"),
        (60, "60 Minuten"),
        (0, "Unbegrenzt")
    ]

    // MARK: - Body

    var body: some View {
        ZStack {
            // Background
            BennieColors.cream
                .ignoresSafeArea()

            VStack(spacing: 24) {
                // Header
                headerSection

                // Toggle section
                toggleSection

                // Time limit picker
                if parentSettings.timeLimitsEnabled {
                    timeLimitSection
                }

                // Player usage section
                playerUsageSection

                Spacer()
            }
            .padding(24)
        }
        .confirmationDialog(
            "Tageszeit zurücksetzen?",
            isPresented: $showResetConfirmation,
            titleVisibility: .visible
        ) {
            Button("Zurücksetzen", role: .destructive) {
                parentSettings.resetDailyTracking()
            }
            Button("Abbrechen", role: .cancel) {}
        } message: {
            Text("Die heutige Videozeit wird für alle Spieler zurückgesetzt.")
        }
    }

    // MARK: - Header Section

    private var headerSection: some View {
        HStack {
            // Back button
            ChildFriendlyButton(action: {
                dismiss()
            }) {
                HStack(spacing: 8) {
                    Image(systemName: "arrow.left")
                        .font(.system(size: 24))
                    Text("Zurück")
                        .font(BennieFont.button(20))
                }
                .foregroundColor(BennieColors.textOnWood)
                .padding(.horizontal, 20)
                .padding(.vertical, 12)
                .frame(minHeight: 96)
                .background(
                    RoundedRectangle(cornerRadius: 12)
                        .fill(BennieColors.woodLight.opacity(0.7))
                )
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(BennieColors.woodMedium, lineWidth: 2)
                )
            }

            Spacer()

            // Title
            Text("Zeit-Einstellungen")
                .font(BennieFont.title(32))
                .foregroundColor(BennieColors.textDark)

            Spacer()

            // Spacer to balance
            Color.clear
                .frame(width: 120)
        }
    }

    // MARK: - Toggle Section

    private var toggleSection: some View {
        @Bindable var settings = parentSettings

        return HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text("Zeitlimit aktiviert")
                    .font(BennieFont.screenHeader(22))
                    .foregroundColor(BennieColors.textDark)

                Text(parentSettings.timeLimitsEnabled ? "Videozeit wird begrenzt" : "Videozeit ist unbegrenzt")
                    .font(BennieFont.label(16))
                    .foregroundColor(BennieColors.textDark.opacity(0.6))
            }

            Spacer()

            Toggle("", isOn: $settings.timeLimitsEnabled)
                .labelsHidden()
                .toggleStyle(SwitchToggleStyle(tint: BennieColors.success))
                .scaleEffect(1.5)
                .frame(width: 96, height: 96)
        }
        .padding(20)
        .background(
            RoundedRectangle(cornerRadius: 16)
                .fill(BennieColors.woodLight.opacity(0.2))
                .overlay(
                    RoundedRectangle(cornerRadius: 16)
                        .stroke(BennieColors.woodMedium.opacity(0.3), lineWidth: 1)
                )
        )
    }

    // MARK: - Time Limit Section

    private var timeLimitSection: some View {
        @Bindable var settings = parentSettings

        return VStack(alignment: .leading, spacing: 16) {
            Text("Tägliches Limit")
                .font(BennieFont.screenHeader(22))
                .foregroundColor(BennieColors.textDark)

            HStack(spacing: 12) {
                ForEach(timeLimitOptions, id: \.value) { option in
                    timeLimitButton(value: option.value, label: option.label)
                }
            }
        }
        .padding(20)
        .background(
            RoundedRectangle(cornerRadius: 16)
                .fill(BennieColors.woodLight.opacity(0.2))
                .overlay(
                    RoundedRectangle(cornerRadius: 16)
                        .stroke(BennieColors.woodMedium.opacity(0.3), lineWidth: 1)
                )
        )
    }

    // MARK: - Time Limit Button

    private func timeLimitButton(value: Int, label: String) -> some View {
        @Bindable var settings = parentSettings
        let isSelected = parentSettings.dailyTimeLimitMinutes == value

        return ChildFriendlyButton(action: {
            settings.dailyTimeLimitMinutes = value
        }) {
            Text(label)
                .font(BennieFont.button(16))
                .foregroundColor(isSelected ? .white : BennieColors.textOnWood)
                .frame(minWidth: 120, minHeight: 96)
                .background(
                    RoundedRectangle(cornerRadius: 12)
                        .fill(isSelected ? BennieColors.success : BennieColors.woodLight.opacity(0.7))
                )
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(isSelected ? BennieColors.success : BennieColors.woodMedium, lineWidth: 2)
                )
        }
    }

    // MARK: - Player Usage Section

    private var playerUsageSection: some View {
        VStack(alignment: .leading, spacing: 16) {
            HStack {
                Text("Heutige Nutzung")
                    .font(BennieFont.screenHeader(22))
                    .foregroundColor(BennieColors.textDark)

                Spacer()

                // Reset button
                ChildFriendlyButton(action: {
                    showResetConfirmation = true
                }) {
                    HStack(spacing: 8) {
                        Image(systemName: "arrow.counterclockwise")
                            .font(.system(size: 18))
                        Text("Zurücksetzen")
                            .font(BennieFont.button(16))
                    }
                    .foregroundColor(BennieColors.textOnWood)
                    .padding(.horizontal, 16)
                    .padding(.vertical, 12)
                    .frame(minHeight: 56)
                    .background(
                        RoundedRectangle(cornerRadius: 10)
                            .fill(BennieColors.woodLight.opacity(0.7))
                    )
                    .overlay(
                        RoundedRectangle(cornerRadius: 10)
                            .stroke(BennieColors.woodMedium, lineWidth: 2)
                    )
                }
            }

            // Player usage cards
            HStack(spacing: 20) {
                ForEach(playerStore.players) { player in
                    playerUsageCard(player: player)
                }
            }
        }
        .padding(20)
        .background(
            RoundedRectangle(cornerRadius: 16)
                .fill(BennieColors.woodLight.opacity(0.2))
                .overlay(
                    RoundedRectangle(cornerRadius: 16)
                        .stroke(BennieColors.woodMedium.opacity(0.3), lineWidth: 1)
                )
        )
    }

    // MARK: - Player Usage Card

    private func playerUsageCard(player: PlayerData) -> some View {
        let watched = parentSettings.timeWatched(for: player.id)
        let remaining = parentSettings.remainingTimeToday(for: player.id)
        let progress: Double = {
            guard parentSettings.timeLimitsEnabled, parentSettings.dailyTimeLimitMinutes > 0 else { return 0 }
            return min(1.0, Double(watched) / Double(parentSettings.dailyTimeLimitMinutes))
        }()

        return VStack(spacing: 12) {
            // Player name
            Text(player.name)
                .font(BennieFont.screenHeader(22))
                .foregroundColor(BennieColors.textDark)

            // Progress ring
            ZStack {
                Circle()
                    .stroke(BennieColors.woodLight, lineWidth: 8)
                    .frame(width: 80, height: 80)

                Circle()
                    .trim(from: 0, to: progress)
                    .stroke(
                        progress >= 1.0 ? BennieColors.coinGold : BennieColors.success,
                        style: StrokeStyle(lineWidth: 8, lineCap: .round)
                    )
                    .frame(width: 80, height: 80)
                    .rotationEffect(.degrees(-90))

                Text("\(watched)")
                    .font(BennieFont.number(28))
                    .foregroundColor(BennieColors.textDark)
            }

            // Usage text
            VStack(spacing: 4) {
                Text("\(watched) Min. geschaut")
                    .font(BennieFont.label(14))
                    .foregroundColor(BennieColors.textDark.opacity(0.7))

                if parentSettings.timeLimitsEnabled && parentSettings.dailyTimeLimitMinutes > 0 {
                    Text(remaining > 0 ? "\(remaining) Min. übrig" : "Limit erreicht")
                        .font(BennieFont.button(14))
                        .foregroundColor(remaining > 0 ? BennieColors.success : BennieColors.coinGold)
                } else {
                    Text("Unbegrenzt")
                        .font(BennieFont.button(14))
                        .foregroundColor(BennieColors.textDark.opacity(0.5))
                }
            }
        }
        .padding(16)
        .frame(minWidth: 180)
        .background(
            RoundedRectangle(cornerRadius: 12)
                .fill(BennieColors.cream)
        )
        .overlay(
            RoundedRectangle(cornerRadius: 12)
                .stroke(BennieColors.woodMedium, lineWidth: 2)
        )
    }
}

// MARK: - Previews

#Preview("TimeSettingsView") {
    TimeSettingsView()
        .environment(ParentSettings())
        .environment(PlayerStore())
}
