import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// VideoSelectionView - Video selection screen for approved YouTube videos
// ═══════════════════════════════════════════════════════════════════════════
// Displays a grid of pre-approved kid-friendly German videos
// Shows allocated time and allows video selection
// Uses VideoStore for parent-managed video list
// ═══════════════════════════════════════════════════════════════════════════

/// Video selection screen displaying approved videos
struct VideoSelectionView: View {
    // MARK: - Environment

    @Environment(AppCoordinator.self) private var coordinator
    @Environment(PlayerStore.self) private var playerStore
    @Environment(VideoStore.self) private var videoStore

    // MARK: - Grid Configuration

    private let columns = [
        GridItem(.flexible(), spacing: 24),
        GridItem(.flexible(), spacing: 24),
        GridItem(.flexible(), spacing: 24)
    ]

    // MARK: - Body

    var body: some View {
        ZStack {
            // Background
            BennieColors.cream
                .ignoresSafeArea()

            VStack(spacing: 20) {
                // Navigation header
                navigationHeader

                // Title sign
                WoodSign(title: "Wähle ein Video!")
                    .scaleEffect(1.3)

                // Time allocation display
                timeDisplay

                // Video grid
                ScrollView {
                    LazyVGrid(columns: columns, spacing: 24) {
                        ForEach(videoStore.approvedVideos) { video in
                            videoThumbnail(video)
                        }
                    }
                    .padding(.horizontal, 40)
                    .padding(.vertical, 16)
                }

                Spacer(minLength: 20)
            }
            .padding(.top)
        }
    }

    // MARK: - Navigation Header

    private var navigationHeader: some View {
        HStack {
            // Back button
            Button {
                coordinator.navigateToTreasure()
            } label: {
                HStack(spacing: 8) {
                    Image(systemName: "arrow.left")
                        .font(.system(size: 24))
                    Text("Zurück")
                        .font(BennieFont.button(18))
                }
                .foregroundColor(BennieColors.textOnWood)
                .frame(minWidth: 96, minHeight: 96)
                .background(
                    RoundedRectangle(cornerRadius: 16)
                        .fill(
                            LinearGradient(
                                colors: [BennieColors.woodLight, BennieColors.woodMedium],
                                startPoint: .top,
                                endPoint: .bottom
                            )
                        )
                )
                .overlay(
                    RoundedRectangle(cornerRadius: 16)
                        .stroke(BennieColors.woodDark, lineWidth: 2)
                )
            }
            .buttonStyle(.plain)

            Spacer()
        }
        .padding(.horizontal)
    }

    // MARK: - Time Display

    private var timeDisplay: some View {
        HStack(spacing: 12) {
            Image(systemName: "clock.fill")
                .font(.system(size: 32))
                .foregroundColor(BennieColors.success)

            Text("Du hast \(coordinator.allocatedVideoMinutes) Minuten Zeit!")
                .font(BennieFont.screenHeader())
                .foregroundColor(BennieColors.textDark)
        }
        .padding(.horizontal, 32)
        .padding(.vertical, 16)
        .background(
            RoundedRectangle(cornerRadius: 20)
                .fill(BennieColors.woodLight.opacity(0.4))
                .overlay(
                    RoundedRectangle(cornerRadius: 20)
                        .stroke(BennieColors.success, lineWidth: 3)
                )
        )
    }

    // MARK: - Video Thumbnail

    private func videoThumbnail(_ video: ApprovedVideo) -> some View {
        Button {
            coordinator.startVideoPlayback(minutes: coordinator.allocatedVideoMinutes, videoId: video.id)
        } label: {
            VStack(spacing: 12) {
                // Thumbnail image
                AsyncImage(url: video.thumbnailURL) { phase in
                    switch phase {
                    case .empty:
                        // Loading placeholder
                        RoundedRectangle(cornerRadius: 12)
                            .fill(BennieColors.woodLight.opacity(0.5))
                            .frame(height: 140)
                            .overlay(
                                ProgressView()
                                    .tint(BennieColors.woodDark)
                            )
                    case .success(let image):
                        image
                            .resizable()
                            .aspectRatio(16/9, contentMode: .fill)
                            .frame(height: 140)
                            .clipped()
                            .cornerRadius(12)
                    case .failure:
                        // Error placeholder
                        RoundedRectangle(cornerRadius: 12)
                            .fill(BennieColors.woodLight.opacity(0.5))
                            .frame(height: 140)
                            .overlay(
                                Image(systemName: "play.rectangle.fill")
                                    .font(.system(size: 40))
                                    .foregroundColor(BennieColors.woodDark)
                            )
                    @unknown default:
                        EmptyView()
                    }
                }

                // Video title
                Text(video.title)
                    .font(BennieFont.button(18))
                    .foregroundColor(BennieColors.textOnWood)
                    .lineLimit(2)
                    .multilineTextAlignment(.center)
                    .frame(height: 50)
            }
            .frame(minWidth: 200, minHeight: 200)
            .padding(12)
            .background(
                RoundedRectangle(cornerRadius: 16)
                    .fill(
                        LinearGradient(
                            colors: [BennieColors.woodLight, BennieColors.woodMedium],
                            startPoint: .top,
                            endPoint: .bottom
                        )
                    )
            )
            .overlay(
                RoundedRectangle(cornerRadius: 16)
                    .stroke(BennieColors.woodDark, lineWidth: 3)
            )
            .shadow(color: .black.opacity(0.15), radius: 4, x: 0, y: 2)
        }
        .buttonStyle(.plain)
    }
}

// MARK: - Previews

#Preview("VideoSelectionView") {
    let coordinator = AppCoordinator()
    coordinator.allocatedVideoMinutes = 5

    return VideoSelectionView()
        .environment(coordinator)
        .environment(PlayerStore())
        .environment(VideoStore())
}

#Preview("VideoSelectionView - 12 Minutes") {
    let coordinator = AppCoordinator()
    coordinator.allocatedVideoMinutes = 12

    return VideoSelectionView()
        .environment(coordinator)
        .environment(PlayerStore())
        .environment(VideoStore())
}
