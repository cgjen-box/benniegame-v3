# External Integrations

**Analysis Date:** 2026-01-12

## APIs & External Services

**Payment Processing:**
- Not applicable - Private family app, no monetization

**Email/SMS:**
- Not applicable - Local app only

**AI/ML Services:**
- Google Gemini API - Character & background image generation
  - SDK/Client: google-genai >=0.4.0
  - Auth: `GOOGLE_API_KEY` env var
  - Usage: Asset generation pipeline (`starter-kits/gemini-image-pro-3/`)

- ElevenLabs - German voice synthesis (Narrator + Bennie voices)
  - API Endpoint: ElevenLabs API v2
  - Auth: `ELEVENLABS_API_KEY` env var
  - Config: Model `eleven_multilingual_v2`, German output
  - Usage: 77 voice files generation

- Google Veo 3.1 - Video generation (optional)
  - SDK/Client: google-genai >=0.4.0
  - Capabilities: 4-8 second videos
  - Location: `starter-kits/veo-video-generation/`

- Ludo.ai - Animation keyframe interpolation
  - Purpose: Convert 2 keyframes → 42 interpolated frames → Lottie JSON
  - Location: `starter-kits/ludo-animation-pipeline/`

## Data Storage

**Databases:**
- SwiftData - Local iPad storage for player profiles
  - Connection: In-app, no external connection
  - Client: SwiftData framework
  - Migrations: Not yet configured

- Neo4j (Development only)
  - URI: `bolt://localhost:7687`
  - Purpose: Knowledge graph (email drafting context, not game-related)
  - Location: `.env` lines 12-14

**File Storage:**
- Local file system - All assets bundled in app
- No cloud storage - Privacy requirement for children's app

**Caching:**
- Not applicable - All assets bundled

## Authentication & Identity

**Auth Provider:**
- None - No user authentication required
- Parent Gate: Math question verification (5-15 range addition)

**OAuth Integrations:**
- Microsoft Graph (Optional/Future)
  - Tenant ID: `f52ffe2b-23df-4557-a211-36c8416513d2`
  - Purpose: Parent notifications (not implemented)
  - Location: `.env` lines 19-24

- Jira Cloud (Development workflow only)
  - URL: `https://eatplanted.atlassian.net`
  - Purpose: Project tracking
  - Location: `.env` lines 28-36

## Monitoring & Observability

**Error Tracking:**
- Not configured - Local app

**Analytics:**
- Not configured - Privacy requirement for children

**Logs:**
- Xcode console during development
- No production logging service

## CI/CD & Deployment

**Hosting:**
- Local iPad device - TestFlight distribution
- Not App Store (private family app)

**CI Pipeline:**
- Not configured - Manual build via Xcode
- MCP Tools: iOS Simulator automation (`starter-kits/maestro-orchestration/`)

**Build Host:**
- MacinCloud - Remote macOS machine
  - Hostname: `FF775.macincloud.com`
  - Username: `user289321`
  - Connection: SSH via `~/.ssh/macincloud_key`

## Environment Configuration

**Development:**
- Required env vars: `GOOGLE_API_KEY`, `ELEVENLABS_API_KEY`
- Secrets location: `.env` (gitignored pattern configured)
- Mock/stub services: Gemini/ElevenLabs test modes

**Staging:**
- Not applicable - Single environment

**Production:**
- Secrets management: Bundled in app build
- All external API calls are asset generation only (not runtime)

## Webhooks & Callbacks

**Incoming:**
- None - Local app only

**Outgoing:**
- None - No external notifications

## YouTube Integration

**Video Embedding:**
- Implementation: WKWebView with custom parameters
- Embed Parameters:
  - `controls: 0` (no YouTube controls)
  - `rel: 0` (no related videos)
  - `modestbranding: 1` (minimal branding)
  - `playsinline: 1` (inline playback)
  - `disablekb: 1` (disable keyboard)
- Parent Control: Video approval in parent dashboard
- Time Management: Analog clock countdown, auto-exit

---

*Integration audit: 2026-01-12*
*Update when adding/removing external services*
