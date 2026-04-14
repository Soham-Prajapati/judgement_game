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
- [ ] Add backend Python environment setup files
- [ ] Add frontend Flutter app scaffold
- [ ] Add shared README with local run instructions

## B. Backend Core (FastAPI + Redis)
- [ ] Set up FastAPI app entrypoint and CORS
- [ ] Add health endpoint
- [ ] Implement room creation endpoint with 6-char code generation
- [ ] Implement room exists/check endpoint
- [ ] Add async Redis client and room TTL handling
- [ ] Add WebSocket router with room/user connection path
- [ ] Add connection manager (per-room sockets)

## C. Game Engine (Pure Python)
- [ ] Implement deck creation, shuffle, and deal
- [ ] Implement trump rotation module (spades -> diamonds -> hearts -> clubs)
- [ ] Implement bidding rules with illegal last-bid value
- [ ] Implement trick winner logic (lead suit + trump precedence)
- [ ] Implement round scoring (+10 exact else 0)
- [ ] Add unit tests for all game modules

## D. Real-Time Game Flow
- [ ] Implement server events for lobby state updates
- [ ] Implement bidding phase orchestration
- [ ] Implement turn-based card play orchestration
- [ ] Implement trick resolution + trick winner updates
- [ ] Implement round end + cumulative score updates
- [ ] Implement game over + rematch flow

## E. Resilience and Edge Cases
- [ ] Host migration when host disconnects
- [ ] Auto-skip disconnected players in active game
- [ ] Room cleanup on empty room
- [ ] Reconnect support contract for clients
- [ ] Server-side validation for invalid bids/cards

## F. Frontend Functional Baseline (No Final UI Commitment Yet)
- [ ] Initialize Flutter routing, providers, and services
- [ ] Implement Home + username persistence
- [ ] Implement Join Room flow with validation/error states
- [ ] Implement Lobby real-time player updates
- [ ] Implement gameplay state wiring to WS events
- [ ] Implement scoreboard matrix rendering from server data

## G. Ads and Release Readiness
- [ ] Integrate AdMob test units (Home + Lobby only)
- [ ] Ensure no ads on Game Table and Scoreboard
- [ ] Add production URL switching for API/WS bases
- [ ] Build release AAB and run pre-release checklist

---

## 3) 4-Day Execution Plan

## Day 1 - Backend Skeleton + Game Rules Core
- [ ] Create backend folder structure and baseline files
- [ ] Implement: deck, trump, bidding, scoring modules
- [ ] Add unit tests for these modules
- [ ] Validate all rule logic with pytest

Exit criteria:
- Game rule modules pass tests
- Room create/check endpoints respond correctly

## Day 2 - WebSocket Game Orchestration
- [ ] Add WebSocket connection manager + router events
- [ ] Implement: lobby updates, deal, bid flow, turn flow
- [ ] Implement disconnect handling + host promotion
- [ ] Manual multiplayer sanity test with 2 clients

Exit criteria:
- Full round completes server-side over WebSocket
- Disconnection paths do not break room state

## Day 3 - Flutter Wiring + UI Decision Checkpoint
- [ ] Implement Flutter project skeleton, providers, WS service, API service
- [ ] Build functional screens with placeholder-safe components
- [ ] Connect server events to client state updates
- [ ] Run UI Decision Checkpoint (below)

Exit criteria:
- Create -> Join -> Lobby -> Game loop works functionally
- UI stack/component direction locked for polish

## Day 4 - UI Polish + Ads + Release Packaging
- [ ] Apply finalized design system tokens/components
- [ ] Integrate AdMob in Home/Lobby
- [ ] Run edge-case and reconnection checks
- [ ] Build release artifacts (APK/AAB) and deployment notes

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

- [ ] Scaffold backend directories and baseline files now
- [ ] Implement first test-backed game modules: trump, bidding, scoring
- [ ] Wire minimal FastAPI routes: /health, /room/create, /room/{code}/exists