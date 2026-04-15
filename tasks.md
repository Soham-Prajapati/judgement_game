# Project Judgement (Kachuful) Task Tracking

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
- [/] Implement trick resolution + trick winner updates
- [ ] Implement round end + cumulative score updates
- [ ] Implement game over + rematch flow

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

## X. CLI Extensions
- [x] Create Browser Agent tool (Playwright-based) for internet access, login automation, and CAPTCHA solving.
