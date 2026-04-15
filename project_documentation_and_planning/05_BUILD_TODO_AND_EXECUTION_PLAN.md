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
- [x] React Native frontend + FastAPI backend

UI component/style selection is deferred until backend contracts are stable.

---

## 2) Master Todo (Execution Checklist)

## A. Project Foundation
- [x] Create repository root structure: backend + frontend
- [x] Add backend Python environment setup files
- [x] Add frontend React Native app scaffold (TypeScript)
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
- [x] Initialize React Native navigation, store, and services
- [x] Implement Home + username persistence (AsyncStorage)
- [x] Implement Join Room flow with validation/error states
- [x] Implement Lobby real-time player updates
- [x] Implement gameplay state wiring to WS events
- [x] Implement scoreboard matrix rendering from server data

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
- [x] Implement React Native project skeleton, navigation, state store, WS service, API service
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
- [ ] Build release artifacts (APK/AAB) and deployment notes

Exit criteria:
- Stable end-to-end multiplayer flow
- V1 ready for internal testing release

---

## 4) Deferred UI Decision Checkpoint (Day 3)

Selection criteria:
- Gameplay clarity under network latency
- Low jank on mid-range Android devices
- Fast iteration speed for V1
- Clean maintainability for post-launch updates

---

## 6) Immediate Next Build Actions

- [ ] Implement UI Polish (Cards, Animations, Desi Theme)
- [ ] Integrate AdMob
- [ ] Handle Edge cases (Disconnection migration)
