# Technical Architecture — Project Judgement

**Stack:** Flutter (Android) + FastAPI + WebSockets + Redis  
**Deployment:** Railway / Render (backend) + Google Play (frontend)  
**Auth:** None (stateless rooms, no user accounts)

---

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Flutter App (Android)                │
│                                                             │
│  ┌─────────────┐   WebSocket (ws://)   ┌─────────────────┐ │
│  │  UI Layer   │ ◄──────────────────► │  WS Connection  │ │
│  │  (Screens)  │                       │    Manager      │ │
│  └──────┬──────┘                       └────────┬────────┘ │
│         │ Riverpod                               │          │
│  ┌──────▼──────┐                       ┌────────▼────────┐ │
│  │  State      │                       │  Event Handler  │ │
│  │  Providers  │◄──────────────────────│  (JSON parse)   │ │
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
| In-memory store | Redis 7 via `redis-py` (async) | Fast, TTL support, pub/sub |
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

The `/room/create` endpoint generates a room code and seeds the initial Redis key with a 2-hour TTL. No other HTTP endpoints are needed — everything else flows through WebSocket.

### 2.3 Redis Data Schema

All keys are namespaced under `room:{code}:`.

```
room:{code}:meta         → Hash
    host: username
    status: lobby | bidding | playing | round_end | game_over
    round_num: int
    trump_suit: spades|diamonds|hearts|clubs
    total_cards: int
    created_at: timestamp
    TTL: 7200 seconds (2 hours, reset on any activity)

room:{code}:players      → List (ordered, insertion order = seat order)
    ["alice", "bob", "charlie"]

room:{code}:hands        → Hash (per-player, private)
    alice: "[{suit:'S',value:'A'}, ...]"   (JSON string)
    bob:   "[...]"

room:{code}:bids         → Hash
    alice: 2
    bob: 0

room:{code}:tricks       → Hash (tricks won this round)
    alice: 1
    bob: 0

room:{code}:scores       → Hash (cumulative, all rounds)
    alice: "[10, 0, 10, ...]"   (JSON array per round)
    bob:   "[0, 10, 0, ...]"

room:{code}:trick_pile   → List (cards played in current trick)
    ["{player:'alice', card:{suit:'S',value:'A'}}", ...]

room:{code}:turn         → String (username of current turn)
room:{code}:lead_suit    → String (suit of first card in current trick)
```

### 2.4 Game Engine Modules

All pure Python, no external deps. Stateless functions that take data, return data. Redis I/O handled separately in the router layer.

```python
# game/deck.py
def create_deck() -> list[dict]
def shuffle_deck(deck) -> list[dict]
def deal_cards(deck, num_players, cards_per_player) -> dict[str, list]

# game/trump.py
TRUMP_ORDER = ["spades", "diamonds", "hearts", "clubs"]
def get_trump_for_round(round_num: int) -> str

# game/bidding.py
def get_illegal_bid(current_bids: dict, total_cards: int, is_last_bidder: bool) -> int | None
def validate_bid(bid: int, illegal_bid: int | None) -> bool

# game/tricks.py
def determine_trick_winner(trick_pile: list, trump_suit: str, lead_suit: str) -> str
def must_follow_suit(hand: list, lead_suit: str) -> bool
def get_playable_cards(hand: list, lead_suit: str | None) -> list

# game/scoring.py
def calculate_round_scores(bids: dict, tricks_won: dict) -> dict[str, int]
def update_cumulative_scores(existing: dict, round_scores: dict) -> dict
```

### 2.5 WebSocket Connection Manager

```python
class ConnectionManager:
    # Maps room_code → {username: WebSocket}
    active_connections: dict[str, dict[str, WebSocket]]

    async def connect(room_code, username, websocket)
    async def disconnect(room_code, username)
    async def broadcast_to_room(room_code, message: dict)
    async def send_to_player(room_code, username, message: dict)
```

Private card deals (`server_deal_cards`) use `send_to_player`. All other events use `broadcast_to_room`.

### 2.6 Disconnection Handling

On WebSocket disconnect:
1. Remove player from `ConnectionManager`
2. If in **lobby**: remove from `room:{code}:players`, broadcast updated `server_room_state`. If 0 players left, delete all room keys.
3. If in **game**: mark player as `disconnected` in meta, auto-skip their turns. Broadcast `server_player_left`.
4. If disconnected player was **host**: promote next player in list, broadcast `server_room_state` with new host.

---

## 3. Frontend (Flutter)

### 3.1 Tech Stack

| Layer | Technology |
|---|---|
| Framework | Flutter 3.x (Android target) |
| State Management | Riverpod 2.x |
| WebSocket | `web_socket_channel` package |
| Local Storage | `shared_preferences` |
| Ads | `google_mobile_ads` |
| Navigation | `go_router` |
| HTTP (room create/check) | `dio` |

### 3.2 Riverpod Providers

```dart
// Core connection
websocketProvider          → WebSocket channel instance
connectionStatusProvider   → enum: connecting | connected | disconnected | error

// Game state (populated from server events)
roomStateProvider          → RoomState (players, host, room_code)
gameStateProvider          → GameState (round, trump, phase: lobby/bidding/playing/end)
myHandProvider             → List<Card>
bidsProvider               → Map<String, int>
tricksWonProvider          → Map<String, int>
scoresProvider             → Map<String, List<int>>  (per-round matrix)
currentTurnProvider        → String (username)
currentTrickProvider       → List<TrickCard>
illegalBidProvider         → int? (the one bid value to grey out)

// Local
usernameProvider           → String (from shared_preferences)
```

### 3.3 WebSocket Event Handling

Single stream listener on `websocketProvider`. Incoming JSON parsed to typed events and dispatched to update the appropriate Riverpod provider.

```dart
// In a StreamProvider or inside a Notifier
websocketChannel.stream.listen((raw) {
  final event = jsonDecode(raw);
  switch (event['type']) {
    case 'server_room_state':   ref.read(roomStateProvider.notifier).update(event);
    case 'server_deal_cards':   ref.read(myHandProvider.notifier).update(event);
    case 'server_bid_request':  ref.read(illegalBidProvider.notifier).update(event);
    case 'server_turn_update':  ref.read(currentTurnProvider.notifier).update(event);
    case 'server_trick_result': ref.read(currentTrickProvider.notifier).update(event);
    case 'server_round_end':    ref.read(scoresProvider.notifier).update(event);
    case 'server_game_over':    ref.read(gameStateProvider.notifier).setGameOver(event);
    case 'server_error':        // show snackbar
  }
});
```

### 3.4 Reconnection Logic

On WebSocket disconnect (outside of intentional leave):
1. Show non-blocking banner: "Connection lost. Reconnecting..."
2. Attempt reconnect 3 times with exponential backoff (1s, 2s, 4s)
3. On success: re-send `client_join_room` with same room_code + username (server restores state from Redis)
4. On all 3 failures: show "Could not reconnect" dialog with Exit option

### 3.5 Card Model

```dart
enum Suit { spades, diamonds, hearts, clubs }
enum Value { two, three, four, five, six, seven, eight, nine, ten, jack, queen, king, ace }

class Card {
  final Suit suit;
  final Value value;

  bool get isTrump => suit == GameState.currentTrump;
  int get rankValue => Value.values.indexOf(value);  // for comparison
}
```

---

## 4. Deployment

### 4.1 Backend

**Recommended: Railway (free tier sufficient for early traction)**

```
Service: FastAPI app
Build: Dockerfile or Railway's Python nixpack
Redis: Railway Redis plugin (same project)
Port: 8000
Environment variables:
  REDIS_URL=redis://...
  ALLOWED_ORIGINS=*  (or your Flutter app's origin)
```

**Dockerfile (backend):**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**requirements.txt:**
```
fastapi>=0.111.0
uvicorn[standard]>=0.29.0
redis[asyncio]>=5.0.0
pydantic>=2.0.0
python-dotenv
```

### 4.2 Flutter Build

```bash
# Debug on device
flutter run

# Release APK
flutter build apk --release

# Release AAB (for Play Store)
flutter build appbundle --release
```

AdMob App ID goes in `AndroidManifest.xml`:
```xml
<meta-data
    android:name="com.google.android.gms.ads.APPLICATION_ID"
    android:value="ca-app-pub-XXXXXXXX~XXXXXXXXXX"/>
```

---

## 5. Security & Abuse Prevention

| Risk | Mitigation |
|---|---|
| Room code brute-force | Room codes are 6-char alphanumeric = 2.1 billion combos. Rate-limit `/room/{code}/exists` to 10 req/min per IP |
| Spamming room creation | Rate-limit `POST /room/create` to 5 req/min per IP |
| Invalid card plays | Server validates every `client_play_card` against player's actual hand in Redis |
| Invalid bids | Server re-validates bid against illegal_bid constraint, rejects with `server_error` |
| Room squatting | 2-hour Redis TTL auto-cleans inactive rooms |
| Cheating hand knowledge | `server_deal_cards` is sent per-player via `send_to_player`, never broadcast |

---

## 6. Performance Targets

| Metric | Target |
|---|---|
| WebSocket event round-trip | < 100ms |
| Room creation response | < 200ms |
| Concurrent rooms (Railway free tier) | ~50–100 active rooms |
| Redis ops per trick | ~5–8 (read hand, validate, update pile, update turn, broadcast) |
| App cold start | < 2s |
| APK size | < 25MB |
