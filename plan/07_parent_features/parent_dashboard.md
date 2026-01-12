# Phase 07.2: Parent Dashboard

## 📚 Playbook References

### Primary References
- **Playbook**: `docs/playbook/FULL_ARCHIVE.md` → Part 4.11 "Parent Dashboard"
- **Condensed Playbook**: `docs/playbook/PLAYBOOK_CONDENSED.md` → Quick Reference Card
- **Design Rules**: CRITICAL - No reference screens exist for Parent Dashboard (new design)

### Color Palette (CRITICAL)
Reference: `PLAYBOOK_CONDENSED.md` - Color System
- **Background**: `#FAF5EB` (Cream)
- **Text**: `#8C7259` (Bark)
- **Card Background**: `#FFFFFF` (White)
- **Success**: `#99BF8C` (Success green)
- **Woodland**: `#738F66` (Primary buttons)

### Components Required
- `WoodButton` - See `design/references/components/settings-button-wooden_20260110_123306.png`
- `NavigationHeader` - Basic implementation (simplified, not full game nav)
- `BennieColors` - All colors from playbook
- `BennieFont` - SF Rounded system

### Character References (Background Context)
While Parent Dashboard doesn't show characters prominently, maintain brand consistency:
- **Bennie**: `design/references/character/bennie/` (brown #8C7259, no clothing)
- **Lemminge**: `design/references/character/lemminge/` (blue #6FA8DC)

---

## Overview
Comprehensive control panel for parents to manage game settings, monitor children's progress, and approve YouTube videos.

## Component Location
```
Features/Parent/ParentDashboardView.swift
Features/Parent/VideoManagementView.swift
Services/ParentSettingsService.swift
```

## Design Philosophy

```
╔══════════════════════════════════════════════════════════════════╗
║              PARENT DASHBOARD DESIGN PRINCIPLES                  ║
║                                                                  ║
║  👥 Per-Player Management:                                       ║
║     Each child has individual settings, time limits, progress   ║
║                                                                  ║
║  📊 Clear Visibility:                                            ║
║     Parents see at-a-glance: time played, coins, locks         ║
║                                                                  ║
║  🎬 YouTube Control:                                             ║
║     Pre-approve videos, NO browsing, NO suggested content       ║
║                                                                  ║
║  ⏱️ Time Management:                                             ║
║     Daily limits per child, visual progress bars               ║
║                                                                  ║
║  🔒 Activity Locks:                                              ║
║     Toggle activities on/off per child (Zeichnen, Logik)       ║
╚══════════════════════════════════════════════════════════════════╝
```

## Purpose
- Monitor each child's play time and progress
- Set daily time limits per child
- Lock/unlock activities per child
- Manage approved YouTube videos (shared across both players)
- Reset progress if needed

## UI Layout

```
┌─────────────────────────────────────────────────────────────────┐
│   ╭────────╮                                       ╭────────╮   │
│   │ Zurück │         ⚙️ Elternbereich              │  User  │   │
│   ╰────────╯                                       ╰────────╯   │
│   96x60pt                                             (future)  │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                     👤 Alexander                         │  │
│   │  ─────────────────────────────────────────────────────  │  │
│   │  Heute gespielt: 23 min / 60 min        [████████░░]   │  │
│   │                                          Progress bar    │  │
│   │  Münzen: 7                                              │  │
│   │                                                         │  │
│   │  Aktivitäten:                                           │  │
│   │  [Rätsel ✓] [Zahlen ✓] [Zeichnen 🔒] [Logik 🔒]         │  │
│   │   48x32pt each toggle button                            │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                     👤 Oliver                            │  │
│   │  ─────────────────────────────────────────────────────  │  │
│   │  Heute gespielt: 45 min / 60 min        [██████████]   │  │
│   │  Münzen: 12                                             │  │
│   │  Aktivitäten: [Rätsel ✓] [Zahlen ✓] [Zeichnen 🔒] [Logik 🔒]│
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │  📺 Genehmigte Videos              [Videos bearbeiten]  │  │
│   │  ─────────────────────────────────────────────────────  │  │
│   │  • Peppa Pig Deutsch                                    │  │
│   │  • Paw Patrol Deutsch                                   │  │
│   │  • Feuerwehrmann Sam                                    │  │
│   │  • Bobo Siebenschläfer                                  │  │
│   │  [+ Video hinzufügen]   ← 120x48pt button               │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │  ⏱️ Tägliche Spielzeit                                   │  │
│   │  ─────────────────────────────────────────────────────  │  │
│   │  Alexander: [▼ 60 min ▼]  ← Picker                      │  │
│   │  Oliver:    [▼ 60 min ▼]                                │  │
│   │                                                         │  │
│   │  Optionen: 30, 45, 60, 75, 90, 120 Minuten             │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│   ╭──────────────────────────────╮                             │
│   │  🗑️ Fortschritt zurücksetzen  │  ← Danger button          │
│   ╰──────────────────────────────╯     120x48pt               │
│                                                                 │
│   Spacer(minLength: 40)  ← Bottom padding                      │
└─────────────────────────────────────────────────────────────────┘
```

**Design Notes:**
- **ScrollView** - Content scrolls if needed (vertical only)
- **Cream Background** - #FAF5EB (consistent with game)
- **White Cards** - Each section is a card with shadow
- **Touch Targets** - Buttons ≥ 96pt where possible, minimum 48pt for toggles
- **Spacing** - 24pt between cards, 16pt within cards

## Data Model

### Parent Settings
```swift
struct ParentSettings: Codable {
    var playerSettings: [String: PlayerSettings] = [:]
    var approvedVideos: [ApprovedVideo] = []
    
    struct PlayerSettings: Codable {
        var dailyTimeLimitMinutes: Int = 60
        var unlockedActivities: Set<ActivityType> = [.raetsel, .zahlen]
        var todayPlayedMinutes: Int = 0
        var lastPlayDate: Date?
        
        // Reset daily counter if date changed
        mutating func checkDailyReset() {
            let calendar = Calendar.current
            if let lastDate = lastPlayDate,
               !calendar.isDateInToday(lastDate) {
                todayPlayedMinutes = 0
            }
            lastPlayDate = Date()
        }
    }
}

struct ApprovedVideo: Codable, Identifiable {
    let id: String           // YouTube video ID
    var title: String        // Display title
    var thumbnailURL: URL    // Cached thumbnail
    var addedAt: Date        // When parent added it
    var category: String?    // Optional grouping
}

enum ActivityType: String, Codable, CaseIterable {
    case raetsel    // Rätsel
    case zahlen     // Zahlen 1,2,3
    case zeichnen   // Drawing (Phase 2)
    case logik      // Logic (Phase 2)
}
```

### Settings Service
```swift
class ParentSettingsService: ObservableObject {
    @Published var settings: ParentSettings
    
    private let storageKey = "parent_settings"
    private let userDefaults = UserDefaults.standard
    
    init() {
        // Load settings from UserDefaults
        if let data = userDefaults.data(forKey: storageKey),
           let decoded = try? JSONDecoder().decode(ParentSettings.self, from: data) {
            self.settings = decoded
        } else {
            self.settings = ParentSettings()
        }
    }
    
    func save() {
        if let encoded = try? JSONEncoder().encode(settings) {
            userDefaults.set(encoded, forKey: storageKey)
        }
    }
    
    // MARK: - Player Management
    
    func getPlayerSettings(_ playerID: String) -> ParentSettings.PlayerSettings {
        return settings.playerSettings[playerID] ?? ParentSettings.PlayerSettings()
    }
    
    func updatePlayerSettings(_ playerID: String, _ update: (inout ParentSettings.PlayerSettings) -> Void) {
        var playerSettings = getPlayerSettings(playerID)
        update(&playerSettings)
        settings.playerSettings[playerID] = playerSettings
        save()
    }
    
    func setDailyTimeLimit(_ playerID: String, minutes: Int) {
        updatePlayerSettings(playerID) { $0.dailyTimeLimitMinutes = minutes }
    }
    
    func toggleActivity(_ playerID: String, _ activity: ActivityType) {
        updatePlayerSettings(playerID) {
            if $0.unlockedActivities.contains(activity) {
                $0.unlockedActivities.remove(activity)
            } else {
                $0.unlockedActivities.insert(activity)
            }
        }
    }
    
    func incrementPlayTime(_ playerID: String, minutes: Int) {
        updatePlayerSettings(playerID) {
            $0.checkDailyReset()
            $0.todayPlayedMinutes += minutes
        }
    }
    
    func hasTimeRemaining(_ playerID: String) -> Bool {
        let settings = getPlayerSettings(playerID)
        return settings.todayPlayedMinutes < settings.dailyTimeLimitMinutes
    }
    
    // MARK: - Video Management
    
    func addVideo(_ video: ApprovedVideo) {
        settings.approvedVideos.append(video)
        save()
    }
    
    func removeVideo(_ videoID: String) {
        settings.approvedVideos.removeAll { $0.id == videoID }
        save()
    }
    
    func getApprovedVideos() -> [ApprovedVideo] {
        return settings.approvedVideos
    }
    
    // MARK: - Reset
    
    func resetPlayerProgress(_ playerID: String) {
        settings.playerSettings[playerID] = ParentSettings.PlayerSettings()
        save()
    }
}
```

## Component Implementation

### Parent Dashboard View
```swift
struct ParentDashboardView: View {
    @StateObject private var settingsService = ParentSettingsService()
    @StateObject private var playerDataStore = PlayerDataStore.shared
    @Environment(\.dismiss) private var dismiss
    
    @State private var showVideoManagement = false
    @State private var showResetConfirmation: String? = nil
    
    let playerIDs = ["alexander", "oliver"]
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 24) {
                    // Header
                    Text("⚙️ Elternbereich")
                        .font(.sfRounded(size: 32, weight: .bold))
                        .foregroundColor(BennieColors.bark)
                    
                    // Player cards
                    ForEach(playerIDs, id: \.self) { playerID in
                        PlayerSettingsCard(
                            playerID: playerID,
                            settingsService: settingsService,
                            playerDataStore: playerDataStore,
                            onReset: { showResetConfirmation = playerID }
                        )
                    }
                    
                    // Video management
                    VideoManagementSection(
                        settingsService: settingsService,
                        onManage: { showVideoManagement = true }
                    )
                    
                    // Time limit settings
                    TimeLimitSection(
                        playerIDs: playerIDs,
                        settingsService: settingsService
                    )
                    
                    Spacer(minLength: 40)
                }
                .padding()
            }
            .background(BennieColors.cream)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Zurück") {
                        dismiss()
                    }
                    .buttonStyle(WoodButtonStyle())
                    .frame(minWidth: 96, minHeight: 60) // Enforce touch target
                }
            }
            .sheet(isPresented: $showVideoManagement) {
                VideoManagementView(settingsService: settingsService)
            }
            .alert("Fortschritt zurücksetzen?", isPresented: .constant(showResetConfirmation != nil)) {
                Button("Abbrechen", role: .cancel) {
                    showResetConfirmation = nil
                }
                Button("Zurücksetzen", role: .destructive) {
                    if let playerID = showResetConfirmation {
                        resetPlayer(playerID)
                    }
                    showResetConfirmation = nil
                }
            } message: {
                if let playerID = showResetConfirmation {
                    Text("Alle Münzen und Fortschritte von \(playerID.capitalized) werden gelöscht.")
                }
            }
        }
    }
    
    func resetPlayer(_ playerID: String) {
        settingsService.resetPlayerProgress(playerID)
        playerDataStore.resetPlayer(playerID)
    }
}
```

### Player Settings Card
```swift
struct PlayerSettingsCard: View {
    let playerID: String
    @ObservedObject var settingsService: ParentSettingsService
    @ObservedObject var playerDataStore: PlayerDataStore
    
    let onReset: () -> Void
    
    var playerData: PlayerData? {
        playerDataStore.getPlayer(playerID)
    }
    
    var settings: ParentSettings.PlayerSettings {
        settingsService.getPlayerSettings(playerID)
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            // Header with avatar
            HStack {
                Text(playerAvatar)
                    .font(.system(size: 32))
                Text(playerID.capitalized)
                    .font(.sfRounded(size: 24, weight: .bold))
                    .foregroundColor(BennieColors.bark)
                Spacer()
            }
            
            Divider()
            
            // Play time progress
            HStack {
                Text("Heute gespielt:")
                    .font(.sfRounded(size: 16))
                    .foregroundColor(BennieColors.bark)
                Spacer()
                Text("\(settings.todayPlayedMinutes) min / \(settings.dailyTimeLimitMinutes) min")
                    .font(.sfRounded(size: 16, weight: .semibold))
                    .foregroundColor(BennieColors.bark)
            }
            
            ProgressView(value: Double(settings.todayPlayedMinutes), 
                        total: Double(settings.dailyTimeLimitMinutes))
                .tint(BennieColors.success)
                .frame(height: 8)
            
            // Coins
            HStack {
                Text("Münzen:")
                    .font(.sfRounded(size: 16))
                    .foregroundColor(BennieColors.bark)
                Text("\(playerData?.coins ?? 0)")
                    .font(.sfRounded(size: 16, weight: .semibold))
                    .foregroundColor(BennieColors.bark)
            }
            
            // Activity toggles
            HStack {
                Text("Aktivitäten:")
                    .font(.sfRounded(size: 16))
                    .foregroundColor(BennieColors.bark)
                Spacer()
            }
            
            HStack(spacing: 12) {
                ForEach(ActivityType.allCases, id: \.self) { activity in
                    ActivityToggleButton(
                        activity: activity,
                        isUnlocked: settings.unlockedActivities.contains(activity),
                        onToggle: {
                            settingsService.toggleActivity(playerID, activity)
                        }
                    )
                }
            }
            
            // Reset button
            Button(action: onReset) {
                HStack {
                    Image(systemName: "trash")
                    Text("Fortschritt zurücksetzen")
                }
                .font(.sfRounded(size: 14))
                .foregroundColor(.red)
            }
            .buttonStyle(.plain)
            .frame(minHeight: 48) // Minimum touch target
        }
        .padding()
        .background(Color.white)
        .cornerRadius(16)
        .shadow(radius: 4)
    }
    
    var playerAvatar: String {
        playerID == "alexander" ? "👦" : "👦"
    }
}

struct ActivityToggleButton: View {
    let activity: ActivityType
    let isUnlocked: Bool
    let onToggle: () -> Void
    
    var body: some View {
        Button(action: onToggle) {
            HStack(spacing: 4) {
                Text(activityIcon)
                Text(isUnlocked ? "✓" : "🔒")
            }
            .font(.sfRounded(size: 14))
            .padding(.horizontal, 12)
            .padding(.vertical, 8)
            .background(isUnlocked ? BennieColors.success.opacity(0.2) : Color.gray.opacity(0.2))
            .cornerRadius(8)
        }
        .frame(minWidth: 48, minHeight: 32) // Minimum touch target for toggle
    }
    
    var activityIcon: String {
        switch activity {
        case .raetsel: return "🔍"
        case .zahlen: return "123"
        case .zeichnen: return "✏️"
        case .logik: return "🧩"
        }
    }
}
```

## Video Management

### Video Management View
```swift
struct VideoManagementView: View {
    @ObservedObject var settingsService: ParentSettingsService
    @Environment(\.dismiss) private var dismiss
    
    @State private var showAddVideo = false
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 16) {
                    // Approved videos list
                    ForEach(settingsService.getApprovedVideos()) { video in
                        VideoRow(
                            video: video,
                            onRemove: {
                                settingsService.removeVideo(video.id)
                            }
                        )
                    }
                    
                    // Add video button
                    Button {
                        showAddVideo = true
                    } label: {
                        HStack {
                            Image(systemName: "plus.circle.fill")
                            Text("Video hinzufügen")
                        }
                        .font(.sfRounded(size: 18, weight: .semibold))
                        .foregroundColor(BennieColors.woodland)
                    }
                    .frame(minWidth: 120, minHeight: 48) // Touch target
                    .padding()
                }
                .padding()
            }
            .background(BennieColors.cream)
            .navigationTitle("Genehmigte Videos")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Fertig") {
                        dismiss()
                    }
                    .buttonStyle(WoodButtonStyle())
                }
            }
            .sheet(isPresented: $showAddVideo) {
                AddVideoView(
                    settingsService: settingsService,
                    onDismiss: { showAddVideo = false }
                )
            }
        }
    }
}

struct VideoRow: View {
    let video: ApprovedVideo
    let onRemove: () -> Void
    
    var body: some View {
        HStack {
            // Thumbnail
            AsyncImage(url: video.thumbnailURL) { image in
                image
                    .resizable()
                    .aspectRatio(16/9, contentMode: .fill)
            } placeholder: {
                Rectangle()
                    .fill(Color.gray.opacity(0.3))
            }
            .frame(width: 120, height: 68)
            .cornerRadius(8)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(video.title)
                    .font(.sfRounded(size: 16, weight: .medium))
                    .foregroundColor(BennieColors.bark)
                    .lineLimit(2)
                
                Text("Hinzugefügt: \(video.addedAt, style: .date)")
                    .font(.sfRounded(size: 12))
                    .foregroundColor(.gray)
            }
            
            Spacer()
            
            Button(action: onRemove) {
                Image(systemName: "trash")
                    .foregroundColor(.red)
                    .frame(width: 48, height: 48) // Touch target
            }
        }
        .padding()
        .background(Color.white)
        .cornerRadius(12)
        .shadow(radius: 2)
    }
}
```

### Add Video Flow
```swift
struct AddVideoView: View {
    @ObservedObject var settingsService: ParentSettingsService
    let onDismiss: () -> Void
    
    @State private var urlInput: String = ""
    @State private var isLoading = false
    @State private var previewVideo: ApprovedVideo?
    @State private var errorMessage: String?
    
    var body: some View {
        NavigationView {
            VStack(spacing: 24) {
                Text("📺 Video hinzufügen")
                    .font(.sfRounded(size: 28, weight: .bold))
                    .foregroundColor(BennieColors.bark)
                
                Text("YouTube Link einfügen:")
                    .font(.sfRounded(size: 16))
                    .foregroundColor(BennieColors.bark)
                
                TextField("https://youtube.com/watch?...", text: $urlInput)
                    .textFieldStyle(.roundedBorder)
                    .autocapitalization(.none)
                    .keyboardType(.URL)
                    .frame(height: 48) // Touch target
                
                Button("Einfügen aus Zwischenablage") {
                    if let clipboard = UIPasteboard.general.string {
                        urlInput = clipboard
                    }
                }
                .buttonStyle(WoodButtonStyle())
                
                if isLoading {
                    ProgressView("Lade Vorschau...")
                        .foregroundColor(BennieColors.bark)
                }
                
                if let preview = previewVideo {
                    VStack {
                        Text("Vorschau:")
                            .font(.sfRounded(size: 16))
                            .foregroundColor(BennieColors.bark)
                        
                        VideoRow(video: preview, onRemove: {})
                    }
                }
                
                if let error = errorMessage {
                    Text(error)
                        .font(.sfRounded(size: 14))
                        .foregroundColor(.red)
                }
                
                Spacer()
                
                HStack(spacing: 20) {
                    Button("Abbrechen") {
                        onDismiss()
                    }
                    .buttonStyle(WoodButtonStyle())
                    .frame(minWidth: 96, minHeight: 60)
                    
                    Button("Hinzufügen") {
                        addVideo()
                    }
                    .buttonStyle(WoodButtonStyle(isPrimary: true))
                    .frame(minWidth: 96, minHeight: 60)
                    .disabled(previewVideo == nil)
                }
            }
            .padding()
            .background(BennieColors.cream)
            .onChange(of: urlInput) { newValue in
                loadPreview(from: newValue)
            }
        }
    }
    
    func loadPreview(from url: String) {
        guard let videoID = extractYouTubeID(from: url) else {
            errorMessage = "Ungültige YouTube URL"
            previewVideo = nil
            return
        }
        
        isLoading = true
        errorMessage = nil
        
        // Fetch video metadata from YouTube
        YouTubeService.shared.fetchVideoMetadata(videoID) { result in
            DispatchQueue.main.async {
                isLoading = false
                
                switch result {
                case .success(let video):
                    previewVideo = video
                case .failure(let error):
                    errorMessage = "Video konnte nicht geladen werden"
                    previewVideo = nil
                }
            }
        }
    }
    
    func addVideo() {
        guard let video = previewVideo else { return }
        settingsService.addVideo(video)
        onDismiss()
    }
    
    func extractYouTubeID(from url: String) -> String? {
        // Handle: youtube.com/watch?v=XXX
        if let range = url.range(of: "v=") {
            let idStart = range.upperBound
            let idEnd = url[idStart...].firstIndex(of: "&") ?? url.endIndex
            return String(url[idStart..<idEnd])
        }
        
        // Handle: youtu.be/XXX
        if url.contains("youtu.be/") {
            let components = url.components(separatedBy: "youtu.be/")
            if components.count > 1 {
                let id = components[1].components(separatedBy: "?")[0]
                return id
            }
        }
        
        return nil
    }
}
```

## Time Limit Section
```swift
struct TimeLimitSection: View {
    let playerIDs: [String]
    @ObservedObject var settingsService: ParentSettingsService
    
    let timeLimitOptions = [30, 45, 60, 75, 90, 120]
    
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("⏱️ Tägliche Spielzeit")
                .font(.sfRounded(size: 20, weight: .bold))
                .foregroundColor(BennieColors.bark)
            
            Divider()
            
            ForEach(playerIDs, id: \.self) { playerID in
                HStack {
                    Text("\(playerID.capitalized):")
                        .font(.sfRounded(size: 16))
                        .foregroundColor(BennieColors.bark)
                    
                    Spacer()
                    
                    Picker("", selection: binding(for: playerID)) {
                        ForEach(timeLimitOptions, id: \.self) { minutes in
                            Text("\(minutes) min").tag(minutes)
                        }
                    }
                    .pickerStyle(.menu)
                    .frame(minHeight: 48) // Touch target
                }
            }
        }
        .padding()
        .background(Color.white)
        .cornerRadius(16)
        .shadow(radius: 4)
    }
    
    func binding(for playerID: String) -> Binding<Int> {
        Binding(
            get: {
                settingsService.getPlayerSettings(playerID).dailyTimeLimitMinutes
            },
            set: { newValue in
                settingsService.setDailyTimeLimit(playerID, minutes: newValue)
            }
        )
    }
}
```

## Testing Checklist

### ✅ Playbook Compliance
```
□ Background is Cream (#FAF5EB)?
□ Card backgrounds are White (#FFFFFF)?
□ Text is Bark (#8C7259)?
□ Progress bars use Success (#99BF8C)?
□ WoodButton component used?
□ ALL major buttons ≥ 96pt touch target?
□ Toggle buttons ≥ 48pt?
□ SF Rounded font used?
□ German text only?
□ No character design violations?
```

### Parent Gate Tests
```
□ Math question generates correctly
□ Correct answer opens dashboard
□ Wrong answer shows error
□ Three attempts generate new question
□ Cancel returns to home
```

### Dashboard Tests
```
□ Player data displays correctly
□ Time progress bar updates
□ Coin count matches actual
□ Activity toggles work
□ Activity locks enforce in game
□ Time limit enforced in game
□ Reset confirmation shows
□ Reset clears all progress
□ Daily time resets at midnight
□ Back button navigates correctly
```

### Video Management Tests
```
□ Video list displays thumbnails
□ Add video from URL works
□ Clipboard paste works
□ Invalid URLs show error
□ Video preview loads
□ Add button saves video
□ Remove button deletes video
□ Videos appear in VideoSelectionView
□ YouTube embed works (Phase 5)
```

### Edge Cases
```
□ Empty video list (show message?)
□ Network error during preview (show error)
□ Duplicate video URL (prevent or allow?)
□ Time limit = 0 (prevent or allow infinite?)
□ All activities locked (prevent or allow?)
□ Reset with no progress (harmless)
□ Multiple rapid toggles (debounce?)
```

---

## 🎯 Success Criteria

**This phase is complete when:**
1. ✅ Parents can monitor both children's progress
2. ✅ Time limits are enforced correctly
3. ✅ Activity locks work in game
4. ✅ Video management adds/removes videos
5. ✅ Videos appear in video selection screen
6. ✅ All touch targets meet minimum requirements
7. ✅ Colors match playbook exactly
8. ✅ Reset functionality works without data corruption

---

**Status**: Ready for Implementation
**Dependencies**: 
- Phase 02 (Design System) - WoodButton, BennieColors
- Phase 03 (Core Screens) - HomeView integration
- Phase 05 (Reward System) - VideoSelectionView integration
- Phase 10 (Data Persistence) - PlayerDataStore

**Next**: Phase 08 - Polish & Testing
