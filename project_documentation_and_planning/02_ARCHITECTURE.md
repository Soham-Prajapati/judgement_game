# Technical Architecture — Project Judgement

**Stack:** React Native (Android) + FastAPI + WebSockets + Redis
**Deployment:** Railway / Render (backend) + Google Play (frontend)
**Auth:** None (stateless rooms, no user accounts)

---

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   React Native App (Android)               │
│                                                             │
│  ┌─────────────┐   WebSocket (ws://)   ┌─────────────────┐ │
│  │  UI Layer   │ ◄──────────────────► │  WS Client      │ │
│  │  (Screens)  │                       │  + Event Bus    │ │
│  └──────┬──────┘                       └────────┬────────┘ │
│         │ Zustand/Context                         │         │
│  ┌──────▼──────┐                       ┌────────▼────────┐ │
│  │ State Store │◄──────────────────────│ Event Reducers  │ │
│  └─────────────┘                       └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                             │ WebSocket
                             │
┌────────────────────────────▼────────────────────────────────┐
│                    FastAPI Backend                           │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              WebSocket Router                        │   │
│  │         /ws/{room_code}/{username}                   │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     │                                        │
│  ┌──────────────────▼──────────────────────────────────┐   │
│  │              Game Engine (Pure Python)               │   │
│  │  - RoomManager   - BiddingEngine   - TrickEngine     │   │
│  │  - DeckManager   - ScoringEngine   - RoundManager    │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     │                                        │
│  ┌──────────────────▼──────────────────────────────────┐   │
│  │              Redis (In-Memory State)                 │   │
│  │  room:{code}:state  |  room:{code}:players           │   │
│  │  room:{code}:hands  |  room:{code}:scores            │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Backend (FastAPI)

### 2.1 Tech Stack

| Layer | Technology | Reason |
|---|---|---|
| Framework | FastAPI | Async-native, WebSocket support, fast |
| WebSockets | FastAPI WebSocket + `asyncio` | Built-in, no extra deps |
| In-memory store | Redis 7 via `redis-py` (async) | Fast, TTL support |
| Serialization | `pydantic` models | Type safety, clean validation |
| Room code gen | `secrets.token_urlsafe` | Cryptographically random |
| Python version | 3.11+ | `asyncio` improvements |

### 2.2 API Endpoints

```
GET  /health                          → { status: "ok" }
POST /room/create                     → { room_code: "XK9P2A" }
GET  /room/{room_code}/exists         → { exists: bool, player_count: int }
WS   /ws/{room_code}/{username}       → WebSocket connection (main game channel)
```

### 2.3 Redis Data Schema

All keys are namespaced under `room:{code}:`.

```
room:{code}:meta         → Hash
room:{code}:players      → List
room:{code}:hands        → Hash
room:{code}:bids         → Hash
room:{code}:tricks       → Hash
room:{code}:scores       → Hash
room:{code}:trick_pile   → List
room:{code}:turn         → String
room:{code}:lead_suit    → String
```

### 2.4 Game Engine Modules

```python
# game/deck.py
# game/trump.py
# game/bidding.py
# game/tricks.py
# game/scoring.py
```

### 2.5 Disconnection Handling

1. Remove player from socket registry.
2. If lobby: remove from room list, broadcast `server_room_state`.
3. If in game: mark disconnected, auto-skip turns, broadcast `server_player_left`.
4. If host leaves: promote next player and broadcast new host.

---

## 3. Frontend (React Native)

### 3.1 Tech Stack

| Layer | Technology |
|---|---|
| Framework | React Native 0.7x (TypeScript) |
| State Management | Zustand |
| Navigation | `@react-navigation/native` + native stack |
| HTTP | `axios` |
| WebSocket | Native `WebSocket` API |
| Local Storage | `@react-native-async-storage/async-storage` |
| Ads | `react-native-google-mobile-ads` |
| SVG Assets | `react-native-svg` |

### 3.2 Client State Slices

```ts
connectionSlice   // socket status + reconnect attempts
roomSlice         // room_code, host, players
gameSlice         // phase, round, trump, turn, bids, trick, scores
userSlice         // username (persisted)
```

### 3.3 WebSocket Event Handling

```ts
socket.onmessage = (raw) => {
  const event = JSON.parse(raw.data);
  switch (event.type) {
    case 'server_room_state':
    case 'server_deal_cards':
    case 'server_bid_request':
    case 'server_bid_update':
    case 'server_turn_update':
    case 'server_trick_result':
    case 'server_round_end':
    case 'server_game_over':
    case 'server_player_left':
    case 'server_error':
      // dispatch to zustand slices
      break;
  }
};
```

### 3.4 Reconnection Contract

On unintentional disconnect:
1. Show non-blocking reconnect banner.
2. Retry 3 times with exponential backoff (1s, 2s, 4s).
3. Re-send room join context.
4. On final failure: show exit/retry modal.

---

## 4. Deployment

### 4.1 Backend

Deploy FastAPI + Redis on Railway/Render.

Environment variables:

```env
REDIS_URL=redis://...
ALLOWED_ORIGINS=*
ROOM_TTL_SECONDS=7200
MAX_PLAYERS_PER_ROOM=6
```

### 4.2 React Native Build

```bash
# Run app on emulator
npx react-native run-android

# Release APK
cd android && ./gradlew assembleRelease

# Release AAB
cd android && ./gradlew bundleRelease
```

AdMob App ID goes in Android manifest (`android/app/src/main/AndroidManifest.xml`).

---

## 5. Security & Abuse Prevention

| Risk | Mitigation |
|---|---|
| Room code brute-force | Rate-limit room-check endpoint |
| Spamming room creation | Rate-limit room-create endpoint |
| Invalid card plays | Validate card ownership + suit-follow rules server-side |
| Invalid bids | Re-validate illegal-bid constraint server-side |
| Room squatting | Redis TTL auto-cleanup |
| Hand leakage | Private per-player deal events only |

---

## 6. Performance Targets

| Metric | Target |
|---|---|
| WebSocket event round-trip | < 100ms |
| Room creation response | < 200ms |
| Concurrent rooms | ~50–100 active rooms |
| Android cold start | < 2s |
| Release APK size | < 30MB |
