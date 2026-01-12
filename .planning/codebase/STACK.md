# Technology Stack

**Analysis Date:** 2026-01-12

## Languages

**Primary:**
- Swift 5.x+ - All application code (to be created)

**Secondary:**
- Python 3.12.12 - Asset generation pipelines, MCP tools
- JavaScript - Build scripts, config files (Xcode)

## Runtime

**Environment:**
- iPadOS 17.0+ (iPad 10th gen, Air, Pro)
- Landscape orientation only
- Screen resolution: 1194×834 points

**Package Manager:**
- Swift Package Manager (SPM) - Xcode dependencies
- pip - Python dependencies for asset generation tools
- Lockfile: Various `requirements.txt` in `starter-kits/`

## Frameworks

**Core:**
- SwiftUI - Primary UI framework
- SwiftData - Local data persistence (player profiles, settings)
- UIKit - Hybrid support for YouTube embedding via WKWebView

**Testing:**
- XCTest - Unit/UI testing (built-in)

**Build/Dev:**
- Xcode - Primary IDE and build tool
- Lottie-iOS 4.x - Character animations (`https://github.com/airbnb/lottie-spm.git`)
- AVFoundation - 3-channel audio system

## Key Dependencies

**Critical:**
- Lottie-iOS 4.x - Character animations, confetti effects, visual feedback
- AVFoundation - Audio playback (music, voice, effects channels)
- WKWebView - YouTube video embedding

**Infrastructure:**
- SwiftData - Player data persistence (coins, progress)
- Combine (implicit) - Reactive state management via @Observable

**Python Tooling (Asset Generation):**
- google-genai >=0.4.0 - Gemini API for image generation
- python-dotenv >=1.0.0 - Environment configuration
- pillow >=10.0.0 - Image processing
- requests >=2.31.0 - HTTP client
- paramiko >=3.0.0 - SSH for MacinCloud

## Configuration

**Environment:**
- `.env` file for API keys and external service credentials
- Key configs: `GOOGLE_API_KEY`, `ELEVENLABS_API_KEY`, `MACINCLOUD_*`

**Build:**
- `BennieGame.xcodeproj` (to be created)
- `Info.plist` - iPad landscape-only, iOS 17+ deployment target
- Bundle ID: `com.bennie.game`

## Platform Requirements

**Development:**
- macOS (via MacinCloud remote: `FF775.macincloud.com`)
- Xcode latest version
- Python 3.12+ for asset generation

**Production:**
- iPad (10th generation, Air, Pro)
- iPadOS 17.0+
- Landscape orientation locked
- Local storage only (no cloud sync)

---

*Stack analysis: 2026-01-12*
*Update after major dependency changes*
