# Build Todo and Execution Plan (4-Day Window, React Native Reset)

Status: Active
Updated: 2026-04-15

## 1) Build Objective

Ship a playable Android V1 of Judgement (Kachuful) with:
- [x] Room create/join flow
- [x] Real-time multiplayer game loop (deal -> bid -> play -> score)
- [x] Correct rule enforcement (especially last-bid illegal value)
- [x] Redis-backed ephemeral rooms (2-hour TTL)
- [ ] Ads only on non-gameplay screens
- [ ] React Native frontend + FastAPI backend

UI component/style selection is deferred until backend contracts are stable.

---

## 2) Master Todo (Execution Checklist)

## A. Project Foundation
- [x] Create repository root structure: backend + frontend
- [x] Add backend Python environment setup files
- [ ] Add frontend React Native app scaffold (TypeScript)
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
- [ ] Host migration when host disconnects
- [ ] Auto-skip disconnected players in active game
- [ ] Room cleanup on empty room
- [ ] Reconnect support contract for clients
- [ ] Server-side validation for invalid bids/cards

## F. Frontend Functional Baseline (React Native)
- [ ] Initialize React Native navigation, store, and services
- [ ] Implement Home + username persistence (AsyncStorage)
- [ ] Implement Join Room flow with validation/error states
- [ ] Implement Lobby real-time player updates
- [ ] Implement gameplay state wiring to WS events
- [ ] Implement scoreboard matrix rendering from server data

## G. Ads and Release Readiness
- [ ] Integrate AdMob test units (Home + Lobby only)
- [ ] Ensure no ads on Game Table and Scoreboard
- [ ] Add production URL switching for API/WS bases
- [ ] Build release APK for friend testing
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
- [ ] Implement disconnect handling + host promotion
- [x] Multiplayer sanity test with 2 clients

Exit criteria:
- Full round completes server-side over WebSocket
- Disconnection paths do not break room state (Pending refined migration)

## Day 3 - React Native Wiring + UI Decision Checkpoint
- [ ] Implement React Native project skeleton, navigation, state store, WS service, API service
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
- Base component strategy: custom components vs package-assisted UI components
- Animation approach for dealing/playing/trick resolution
- Typography strategy and fallback handling
- SVG suit/icon pipeline and render performance

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

- [ ] Scaffold React Native frontend and connect local backend
- [ ] Implement Home/Join/Lobby screens
- [ ] Wire WebSocket events to Zustand store
