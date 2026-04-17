# Build Todo and Execution Plan (4-Day Window, React Native Reset)

Status: Complete
Updated: 2026-04-17

## 1) Build Objective

Ship a playable Android/iOS/Web V1 of Judgement (Kachuful) with:
- [x] Room create/join flow (Up to 8 players)
- [x] Real-time multiplayer game loop (U-Turn: 1-7-1 cards)
- [x] Correct rule enforcement (especially last-bid illegal value)
- [x] Cloud-backed ephemeral rooms (Upstash Redis)
- [x] UI Polish (Pixel Art Assets, Desi Theme)
- [x] Free-Forever Hosting (Hugging Face Spaces)

---

## 2) Final Todo (Post-Launch Refinement)

## A. Technical Foundations
- [x] Create repository root structure
- [x] Add backend environment and Docker configs
- [x] Add frontend Expo App scaffold (TypeScript)
- [x] Implement root-level master runner (`run.sh`)

## B. Game Engine & Logic
- [x] Implement deck, shuffle, and deal
- [x] Implement trump rotation
- [x] Implement U-Turn round scaling (1 to 7 to 1)
- [x] Implement trick winner resolution
- [x] Implement exact-bid scoring (+10 / 0)

## C. Real-Time Flow & Resilience
- [x] WebSocket bidding and play orchestration
- [x] Host migration on disconnect
- [x] Auto-skip disconnected players
- [x] Auto-reconnect with exponential backoff on frontend
- [x] Secure WebSocket support (`wss://`)

## D. UI & Assets
- [x] Integrate 52+ Pixel Art card assets
- [x] Build reusable `CardView`, `OpponentStrip`, and `TrumpIndicator`
- [x] Finalize Home, Lobby, Game, and Scoreboard screens
- [x] Add "How to Play" interactive rules guide

---

## 3) Deployment Strategy
- **Backend:** FastAPI (Python) on Hugging Face Spaces (Docker).
- **Database:** Redis on Upstash (Serverless).
- **Frontend:** Expo (Development) / Web (Global) / APK (Mobile).
