import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// VideoManagementView - Parent interface for managing approved videos
// ═══════════════════════════════════════════════════════════════════════════
// Allows parents to add, remove, and reset the approved video list
// All UI in German with minimum 96pt touch targets
// ═══════════════════════════════════════════════════════════════════════════

/// Parent view for managing the approved video list
struct VideoManagementView: View {
    // MARK: - Environment

    @Environment(\.dismiss) private var dismiss
    @Environment(VideoStore.self) private var videoStore

    // MARK: - State

    @State private var newVideoId: String = ""
    @State private var newVideoTitle: String = ""
    @State private var showResetConfirmation: Bool = false
    @State private var videoToDelete: String? = nil

    // MARK: - Body

    var body: some View {
        ZStack {
            // Background
            BennieColors.cream
                .ignoresSafeArea()

            VStack(spacing: 20) {
                // Header
                headerSection

                // Add video section
                addVideoSection

                // Video list
                videoListSection

                Spacer()
            }
            .padding(24)
        }
        .confirmationDialog(
            "Alle Videos zurücksetzen?",
            isPresented: $showResetConfirmation,
            titleVisibility: .visible
        ) {
            Button("Zurücksetzen", role: .destructive) {
                videoStore.resetToDefaults()
            }
            Button("Abbrechen", role: .cancel) {}
        } message: {
            Text("Die Videoliste wird auf die Standardvideos zurückgesetzt.")
        }
        .confirmationDialog(
            "Video entfernen?",
            isPresented: Binding(
                get: { videoToDelete != nil },
                set: { if !$0 { videoToDelete = nil } }
            ),
            titleVisibility: .visible
        ) {
            Button("Entfernen", role: .destructive) {
                if let id = videoToDelete {
                    videoStore.removeVideo(id: id)
                }
                videoToDelete = nil
            }
            Button("Abbrechen", role: .cancel) {
                videoToDelete = nil
            }
        } message: {
            Text("Dieses Video wird aus der Liste entfernt.")
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
            Text("Video-Verwaltung")
                .font(BennieFont.title(32))
                .foregroundColor(BennieColors.textDark)

            Spacer()

            // Reset button
            ChildFriendlyButton(action: {
                showResetConfirmation = true
            }) {
                HStack(spacing: 8) {
                    Image(systemName: "arrow.counterclockwise")
                        .font(.system(size: 20))
                    Text("Zurücksetzen")
                        .font(BennieFont.button(16))
                }
                .foregroundColor(BennieColors.textOnWood)
                .padding(.horizontal, 16)
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
        }
    }

    // MARK: - Add Video Section

    private var addVideoSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Neues Video hinzufügen")
                .font(BennieFont.screenHeader(22))
                .foregroundColor(BennieColors.textDark)

            HStack(spacing: 16) {
                // Video ID input
                VStack(alignment: .leading, spacing: 4) {
                    Text("YouTube Video-ID")
                        .font(BennieFont.label(14))
                        .foregroundColor(BennieColors.textDark.opacity(0.7))
                    TextField("z.B. dQw4w9WgXcQ", text: $newVideoId)
                        .font(BennieFont.button(18))
                        .foregroundColor(BennieColors.textDark)
                        .padding(12)
                        .frame(height: 56)
                        .background(
                            RoundedRectangle(cornerRadius: 10)
                                .fill(Color.white)
                        )
                        .overlay(
                            RoundedRectangle(cornerRadius: 10)
                                .stroke(BennieColors.woodMedium, lineWidth: 2)
                        )
                }
                .frame(maxWidth: .infinity)

                // Title input
                VStack(alignment: .leading, spacing: 4) {
                    Text("Titel")
                        .font(BennieFont.label(14))
                        .foregroundColor(BennieColors.textDark.opacity(0.7))
                    TextField("z.B. Peppa Wutz", text: $newVideoTitle)
                        .font(BennieFont.button(18))
                        .foregroundColor(BennieColors.textDark)
                        .padding(12)
                        .frame(height: 56)
                        .background(
                            RoundedRectangle(cornerRadius: 10)
                                .fill(Color.white)
                        )
                        .overlay(
                            RoundedRectangle(cornerRadius: 10)
                                .stroke(BennieColors.woodMedium, lineWidth: 2)
                        )
                }
                .frame(maxWidth: .infinity)

                // Add button
                ChildFriendlyButton(action: {
                    addVideo()
                }) {
                    HStack(spacing: 8) {
                        Image(systemName: "plus")
                            .font(.system(size: 24))
                        Text("Hinzufügen")
                            .font(BennieFont.button(18))
                    }
                    .foregroundColor(.white)
                    .padding(.horizontal, 24)
                    .frame(width: 180, height: 96)
                    .background(
                        RoundedRectangle(cornerRadius: 12)
                            .fill(canAddVideo ? BennieColors.success : BennieColors.woodMedium.opacity(0.5))
                    )
                }
                .disabled(!canAddVideo)
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

    // MARK: - Video List Section

    private var videoListSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text("Genehmigte Videos")
                    .font(BennieFont.screenHeader(22))
                    .foregroundColor(BennieColors.textDark)

                Spacer()

                Text("\(videoStore.approvedVideos.count) Videos")
                    .font(BennieFont.label(16))
                    .foregroundColor(BennieColors.textDark.opacity(0.6))
            }

            ScrollView {
                LazyVGrid(columns: [
                    GridItem(.flexible(), spacing: 16),
                    GridItem(.flexible(), spacing: 16),
                    GridItem(.flexible(), spacing: 16),
                    GridItem(.flexible(), spacing: 16)
                ], spacing: 16) {
                    ForEach(videoStore.approvedVideos) { video in
                        videoCard(video)
                    }
                }
                .padding(4)
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

    // MARK: - Video Card

    private func videoCard(_ video: ApprovedVideo) -> some View {
        VStack(spacing: 8) {
            // Thumbnail
            AsyncImage(url: video.thumbnailURL) { phase in
                switch phase {
                case .empty:
                    RoundedRectangle(cornerRadius: 8)
                        .fill(BennieColors.woodLight.opacity(0.5))
                        .frame(height: 100)
                        .overlay(
                            ProgressView()
                                .tint(BennieColors.woodDark)
                        )
                case .success(let image):
                    image
                        .resizable()
                        .aspectRatio(16/9, contentMode: .fill)
                        .frame(height: 100)
                        .clipped()
                        .cornerRadius(8)
                case .failure:
                    RoundedRectangle(cornerRadius: 8)
                        .fill(BennieColors.woodLight.opacity(0.5))
                        .frame(height: 100)
                        .overlay(
                            Image(systemName: "play.rectangle.fill")
                                .font(.system(size: 30))
                                .foregroundColor(BennieColors.woodDark)
                        )
                @unknown default:
                    EmptyView()
                }
            }

            // Title
            Text(video.title)
                .font(BennieFont.button(14))
                .foregroundColor(BennieColors.textDark)
                .lineLimit(1)

            // Delete button
            ChildFriendlyButton(action: {
                videoToDelete = video.id
            }) {
                HStack(spacing: 4) {
                    Image(systemName: "xmark")
                        .font(.system(size: 14))
                    Text("Entfernen")
                        .font(BennieFont.button(12))
                }
                .foregroundColor(BennieColors.textOnWood)
                .padding(.horizontal, 12)
                .padding(.vertical, 8)
                .frame(minWidth: 96, minHeight: 44)
                .background(
                    RoundedRectangle(cornerRadius: 8)
                        .fill(BennieColors.woodLight.opacity(0.7))
                )
                .overlay(
                    RoundedRectangle(cornerRadius: 8)
                        .stroke(BennieColors.woodMedium, lineWidth: 1)
                )
            }
        }
        .padding(12)
        .background(
            RoundedRectangle(cornerRadius: 12)
                .fill(BennieColors.cream)
        )
        .overlay(
            RoundedRectangle(cornerRadius: 12)
                .stroke(BennieColors.woodMedium, lineWidth: 2)
        )
    }

    // MARK: - Helper Methods

    private var canAddVideo: Bool {
        !newVideoId.trimmingCharacters(in: .whitespaces).isEmpty &&
        !newVideoTitle.trimmingCharacters(in: .whitespaces).isEmpty
    }

    private func addVideo() {
        guard canAddVideo else { return }

        let trimmedId = newVideoId.trimmingCharacters(in: .whitespaces)
        let trimmedTitle = newVideoTitle.trimmingCharacters(in: .whitespaces)

        videoStore.addVideo(youtubeId: trimmedId, title: trimmedTitle)

        // Clear inputs
        newVideoId = ""
        newVideoTitle = ""
    }
}

// MARK: - Previews

#Preview("VideoManagementView") {
    VideoManagementView()
        .environment(VideoStore())
}
