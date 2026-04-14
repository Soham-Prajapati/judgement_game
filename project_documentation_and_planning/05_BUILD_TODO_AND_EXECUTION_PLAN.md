# Build Todo and Execution Plan (4-Day Window)

Status: Active
Updated: 2026-04-14

## 1) Build Objective

Ship a playable Android V1 of Judgement (Kachuful) with:
- Room create/join flow
- Real-time multiplayer game loop (deal -> bid -> play -> score)
- Correct rule enforcement (especially last-bid illegal value)
- Redis-backed ephemeral rooms (2-hour TTL)
- Ads only on non-gameplay screens

UI component/style selection is intentionally deferred to a dedicated checkpoint after backend + event contracts are stable.

---

## 2) Master Todo (Execution Checklist)

## A. Project Foundation
- [ ] Create repository root structure: backend + frontend
- [x] Add backend Python environment setup files
- [x] Add frontend Flutter app scaffold
- [x] Add shared README with local run instructions

## B. Backend Core (FastAPI + Redis)
- [x] Set up FastAPI app entrypoint and CORS
- [x] Add health endpoint
- [x] Implement room creation endpoint with 6-char code generation
- [x] Implement room exists/check endpoint
- [x] Add async Redis client and room TTL handling
- [x] Add WebSocket router with room/user connection path
- [x] Add connection manager (per-room sockets)

## C. Game Engine (Pure Python)
- [x] Implement deck creation, shuffle, and deal
- [x] Implement trump rotation module (spades -> diamonds -> hearts -> clubs)
- [x] Implement bidding rules with illegal last-bid value
- [x] Implement trick winner logic (lead suit + trump precedence)
- [x] Implement round scoring (+10 exact else 0)
- [x] Add unit tests for all game modules

## D. Real-Time Game Flow
- [x] Implement server events for lobby state updates
- [x] Implement bidding phase orchestration
- [x] Implement turn-based card play orchestration
- [x] Implement trick resolution + trick winner updates
- [x] Implement round end + cumulative score updates
- [x] Implement game over + rematch flow

## E. Resilience and Edge Cases
- [x] Host migration when host disconnects
- [x] Auto-skip disconnected players in active game
- [x] Room cleanup on empty room
- [ ] Reconnect support contract for clients
- [x] Server-side validation for invalid bids/cards

## F. Frontend Functional Baseline (No Final UI Commitment Yet)
- [x] Initialize Flutter app services/state shell
- [x] Implement Home + username persistence
- [x] Implement Join Room flow with validation/error states
- [x] Implement Lobby real-time player updates
- [x] Implement gameplay state wiring to WS events
- [x] Implement scoreboard matrix rendering from server data

## G. Ads and Release Readiness
- [ ] Integrate AdMob test units (Home + Lobby only)
- [ ] Ensure no ads on Game Table and Scoreboard
- [x] Add production URL switching for API/WS bases
- [x] Build release APK for friend testing
- [ ] Build release AAB and run pre-release checklist

---

## 3) 4-Day Execution Plan

## Day 1 - Backend Skeleton + Game Rules Core
- [x] Create backend folder structure and baseline files
- [x] Implement: deck, trump, bidding, scoring modules
- [x] Add unit tests for these modules
- [x] Validate all rule logic with pytest

Exit criteria:
- Game rule modules pass tests
- Room create/check endpoints respond correctly

## Day 2 - WebSocket Game Orchestration
- [x] Add WebSocket connection manager + router events
- [x] Implement: lobby updates, deal, bid flow, turn flow
- [x] Implement disconnect handling + host promotion
- [x] Multiplayer sanity validation via automated 2-player game flow tests

Exit criteria:
- Full round completes server-side over WebSocket
- Disconnection paths do not break room state

## Day 3 - Flutter Wiring + UI Decision Checkpoint
- [x] Implement Flutter project skeleton and service wiring
- [x] Build functional screens with placeholder-safe components
- [x] Connect server events to client state updates
- [ ] Run UI Decision Checkpoint (below)

Exit criteria:
- Create -> Join -> Lobby -> Game loop works functionally
- UI stack/component direction locked for polish

## Day 4 - UI Polish + Ads + Release Packaging
- [ ] Apply finalized design system tokens/components
- [ ] Integrate AdMob in Home/Lobby
- [ ] Run edge-case and reconnection checks
- [ ] Build release artifacts (AAB) and deployment notes

Exit criteria:
- Stable end-to-end multiplayer flow
- V1 ready for internal testing release

---

## 4) Deferred UI Decision Checkpoint (Day 3)

Decision happens only after event contracts are stable.

Evaluate and choose:
- Base component strategy: custom widgets vs package-assisted widgets
- Animation approach for dealing/playing/trick resolution
- Final typography loading strategy and fallback handling
- SVG suit/icon pipeline and asset performance

Selection criteria:
- Gameplay clarity under network latency
- Low jank on mid-range Android devices
- Fast iteration speed for V1
- Clean maintainability for post-launch updates

---

## 5) Skill Usage Map (Available in Current Environment)

The path /soupz-agents/default/agents was not found locally.
Using installed skills under /Users/shubh/.agents/skills:

- soupz-team-lead: parallel execution splits when 2+ independent workstreams exist
- soupz-planner: dependency map and anti-collision planning before coding bursts
- soupz-orchestration-modes: choose party vs quick-dev mode per milestone
- soupz-architect: API contracts and game-state model hardening
- soupz-devops: deployment pipeline and release automation
- soupz-designer: final UI visual system selection and refinement
- soupz-researcher: package/library benchmarking during UI checkpoint

Recommended use sequence:
1. Day 1 start: soupz-planner
2. Day 2 start: soupz-architect
3. Day 3 checkpoint: soupz-team-lead + soupz-designer + soupz-researcher
4. Day 4 release: soupz-devops

---

## 6) Immediate Next Build Actions

- [x] Scaffold backend directories and baseline files now
- [x] Implement first test-backed game modules: trump, bidding, scoring
- [x] Wire minimal FastAPI routes: /health, /room/create, /room/{code}/exists

## 7) Build Progress Delta (2026-04-14)

- [x] Added `game/tricks.py` with lead-suit/trump winner logic and playable-card filtering
- [x] Added `services/game_service.py` for round orchestration (`start_game`, bidding, play, round end, rematch)
- [x] Upgraded `routers/websocket.py` to contract events (`client_start_game`, `client_place_bid`, `client_play_card`, `client_next_round`, `client_rematch`)
- [x] Added Redis-backed room join/leave lifecycle and host migration in `services/room_service.py`
- [x] Added tests: `tests/test_deck.py`, `tests/test_tricks.py`
- [x] Imported card pixel assets into `frontend/assets/cards/sprites` (68 PNG files)
- [x] Added frontend baseline files: `frontend/pubspec.yaml`, `frontend/lib/main.dart`, `frontend/lib/core/card_asset_path.dart`
- [x] Added root runbook `README.md` with local run, internet deployment, and APK distribution steps
- [x] Added Day 2 flow tests in `backend/tests/test_game_flow.py` (full round + disconnect handling)
- [x] Added runtime URL config via `frontend/lib/core/app_config.dart` and documented `--dart-define` usage
- [x] Implemented functional Flutter room/lobby/game shell in `frontend/lib/main.dart`
- [x] Generated Android build scaffold and validated release APK output in `frontend/build/app/outputs/flutter-apk/app-release.apk`
- [x] Added `frontend/build_friend_apk.sh` to build friend-test APKs against any public backend URL