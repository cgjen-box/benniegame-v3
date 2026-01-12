import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// ParentDashboardView - Parent settings and statistics dashboard
// ═══════════════════════════════════════════════════════════════════════════
// Shows per-player statistics and provides reset controls
// Accessible after passing the math gate
// ═══════════════════════════════════════════════════════════════════════════

/// Parent dashboard showing player statistics and settings
struct ParentDashboardView: View {
    // MARK: - Environment

    @Environment(AppCoordinator.self) private var coordinator
    @Environment(PlayerStore.self) private var playerStore

    // MARK: - State

    /// Player ID for single reset confirmation
    @State private var playerToReset: String? = nil
    /// Show reset all confirmation
    @State private var showResetAllConfirmation = false
    /// Show video management sheet
    @State private var showVideoManagement = false
    /// Show time settings sheet
    @State private var showTimeSettings = false

    // MARK: - Body

    var body: some View {
        ZStack {
            // Background
            BennieColors.cream
                .ignoresSafeArea()

            VStack(spacing: 24) {
                // Header with back button
                headerSection

                // Player cards
                playerCardsSection

                // Quick actions
                quickActionsSection

                Spacer()
            }
            .padding(24)
        }
        .confirmationDialog(
            "Fortschritt zurücksetzen?",
            isPresented: Binding(
                get: { playerToReset != nil },
                set: { if !$0 { playerToReset = nil } }
            ),
            titleVisibility: .visible
        ) {
            Button("Zurücksetzen", role: .destructive) {
                if let playerId = playerToReset {
                    playerStore.resetProgress(for: playerId)
                }
                playerToReset = nil
            }
            Button("Abbrechen", role: .cancel) {
                playerToReset = nil
            }
        } message: {
            if let playerId = playerToReset,
               let player = playerStore.getPlayer(id: playerId) {
                Text("Alle Münzen und Fortschritt von \(player.name) werden gelöscht.")
            }
        }
        .confirmationDialog(
            "Alle Fortschritte zurücksetzen?",
            isPresented: $showResetAllConfirmation,
            titleVisibility: .visible
        ) {
            Button("Alle zurücksetzen", role: .destructive) {
                playerStore.resetAllProgress()
            }
            Button("Abbrechen", role: .cancel) {}
        } message: {
            Text("Alle Münzen und Fortschritte aller Spieler werden gelöscht.")
        }
        .sheet(isPresented: $showVideoManagement) {
            VideoManagementView()
        }
        .sheet(isPresented: $showTimeSettings) {
            TimeSettingsView()
        }
    }

    // MARK: - Header Section

    private var headerSection: some View {
        HStack {
            // Back button (goes directly home, not through gate)
            ChildFriendlyButton(action: {
                coordinator.navigateHome()
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
            Text("Elternbereich")
                .font(BennieFont.title(32))
                .foregroundColor(BennieColors.textDark)

            Spacer()

            // Spacer to balance the back button
            Color.clear
                .frame(width: 120)
        }
    }

    // MARK: - Player Cards Section

    private var playerCardsSection: some View {
        HStack(spacing: 24) {
            ForEach(playerStore.players) { player in
                PlayerStatCard(
                    player: player,
                    onReset: {
                        playerToReset = player.id
                    }
                )
            }
        }
        .padding(.top, 16)
    }

    // MARK: - Quick Actions Section

    private var quickActionsSection: some View {
        VStack(spacing: 16) {
            Text("Schnellaktionen")
                .font(BennieFont.screenHeader(24))
                .foregroundColor(BennieColors.textDark)

            HStack(spacing: 20) {
                // Reset all button
                ChildFriendlyButton(action: {
                    showResetAllConfirmation = true
                }) {
                    VStack(spacing: 8) {
                        Image(systemName: "arrow.counterclockwise")
                            .font(.system(size: 28))
                        Text("Alle zurücksetzen")
                            .font(BennieFont.button(18))
                    }
                    .foregroundColor(BennieColors.textOnWood)
                    .frame(width: 180, height: 120)
                    .background(
                        RoundedRectangle(cornerRadius: 12)
                            .fill(BennieColors.woodLight.opacity(0.7))
                    )
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(BennieColors.woodMedium, lineWidth: 2)
                    )
                }

                // Video management button
                ChildFriendlyButton(action: {
                    showVideoManagement = true
                }) {
                    VStack(spacing: 8) {
                        Image(systemName: "video.fill")
                            .font(.system(size: 28))
                        Text("Video-Verwaltung")
                            .font(BennieFont.button(18))
                    }
                    .foregroundColor(BennieColors.textOnWood)
                    .frame(width: 180, height: 120)
                    .background(
                        RoundedRectangle(cornerRadius: 12)
                            .fill(BennieColors.woodLight.opacity(0.7))
                    )
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(BennieColors.woodMedium, lineWidth: 2)
                    )
                }

                // Time settings button
                ChildFriendlyButton(action: {
                    showTimeSettings = true
                }) {
                    VStack(spacing: 8) {
                        Image(systemName: "clock.fill")
                            .font(.system(size: 28))
                        Text("Zeit-Einstellungen")
                            .font(BennieFont.button(18))
                    }
                    .foregroundColor(BennieColors.textOnWood)
                    .frame(width: 180, height: 120)
                    .background(
                        RoundedRectangle(cornerRadius: 12)
                            .fill(BennieColors.woodLight.opacity(0.7))
                    )
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(BennieColors.woodMedium, lineWidth: 2)
                    )
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
}

// MARK: - Player Stat Card

/// Card displaying individual player statistics
private struct PlayerStatCard: View {
    let player: PlayerData
    let onReset: () -> Void

    /// German date formatter
    private var dateFormatter: DateFormatter {
        let formatter = DateFormatter()
        formatter.locale = Locale(identifier: "de_DE")
        formatter.dateStyle = .medium
        formatter.timeStyle = .short
        return formatter
    }

    var body: some View {
        VStack(spacing: 16) {
            // Player header
            HStack(spacing: 12) {
                // Avatar icon
                Image(systemName: player.id == "alexander" ? "person.fill" : "person.fill")
                    .font(.system(size: 36))
                    .foregroundColor(BennieColors.woodDark)
                    .frame(width: 60, height: 60)
                    .background(
                        Circle()
                            .fill(BennieColors.woodLight)
                    )

                VStack(alignment: .leading, spacing: 4) {
                    Text(player.name)
                        .font(BennieFont.screenHeader(28))
                        .foregroundColor(BennieColors.textDark)
                }

                Spacer()
            }

            Divider()
                .background(BennieColors.woodMedium)

            // Stats
            VStack(alignment: .leading, spacing: 12) {
                // Current coins
                statRow(
                    icon: "dollarsign.circle.fill",
                    iconColor: BennieColors.coinGold,
                    label: "Aktuelle Münzen",
                    value: "\(player.coins)"
                )

                // Total coins earned
                statRow(
                    icon: "star.fill",
                    iconColor: BennieColors.coinGold,
                    label: "Gesamt verdient",
                    value: "\(player.totalCoinsEarned)"
                )

                // Last played
                statRow(
                    icon: "clock.fill",
                    iconColor: BennieColors.woodDark,
                    label: "Zuletzt gespielt",
                    value: lastPlayedText
                )
            }

            Spacer()

            // Reset button
            ChildFriendlyButton(action: onReset) {
                HStack(spacing: 8) {
                    Image(systemName: "arrow.counterclockwise")
                        .font(.system(size: 18))
                    Text("Zurücksetzen")
                        .font(BennieFont.button(16))
                }
                .foregroundColor(BennieColors.textOnWood)
                .padding(.horizontal, 16)
                .padding(.vertical, 12)
                .frame(minWidth: 160, minHeight: 50)
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
        .padding(20)
        .frame(width: 320, height: 340)
        .background(
            RoundedRectangle(cornerRadius: 20)
                .fill(BennieColors.cream)
                .shadow(color: BennieColors.woodDark.opacity(0.2), radius: 8, x: 0, y: 4)
        )
        .overlay(
            RoundedRectangle(cornerRadius: 20)
                .stroke(BennieColors.woodMedium, lineWidth: 2)
        )
    }

    /// Creates a stat row with icon, label, and value
    private func statRow(icon: String, iconColor: Color, label: String, value: String) -> some View {
        HStack(spacing: 12) {
            Image(systemName: icon)
                .font(.system(size: 20))
                .foregroundColor(iconColor)
                .frame(width: 24)

            Text(label)
                .font(BennieFont.label(16))
                .foregroundColor(BennieColors.textDark.opacity(0.7))

            Spacer()

            Text(value)
                .font(BennieFont.button(18))
                .foregroundColor(BennieColors.textDark)
        }
    }

    /// Formatted last played text
    private var lastPlayedText: String {
        guard let date = player.lastPlayedDate else {
            return "Noch nie"
        }
        return dateFormatter.string(from: date)
    }
}

// MARK: - Previews

#Preview("ParentDashboardView") {
    ParentDashboardView()
        .environment(AppCoordinator())
        .environment(PlayerStore())
}

#Preview("PlayerStatCard") {
    PlayerStatCard(
        player: PlayerData(
            id: "alexander",
            name: "Alexander",
            coins: 15,
            totalCoinsEarned: 42,
            lastPlayedDate: Date()
        ),
        onReset: {}
    )
    .padding()
    .background(BennieColors.cream)
}
