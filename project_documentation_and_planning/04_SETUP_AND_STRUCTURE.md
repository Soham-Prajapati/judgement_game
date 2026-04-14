# File Structure & Setup Guide — Project Judgement

---

## 1. Repository Structure

```
judgement/
├── backend/                          # FastAPI server
│   ├── main.py                       # App entry point, CORS, router registration
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── room.py                   # POST /room/create, GET /room/{code}/exists
│   │   └── websocket.py              # WS /ws/{room_code}/{username}
│   │
│   ├── game/                         # Pure game logic, no I/O
│   │   ├── __init__.py
│   │   ├── deck.py                   # create_deck, shuffle, deal
│   │   ├── trump.py                  # Trump rotation logic
│   │   ├── bidding.py                # Bid validation, illegal bid calc
│   │   ├── tricks.py                 # Trick winner, playable cards
│   │   └── scoring.py                # Round + cumulative scoring
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── redis_client.py           # Async Redis connection, helper methods
│   │   ├── room_service.py           # Room CRUD on Redis
│   │   ├── game_service.py           # Orchestrates game flow using game/ modules
│   │   └── connection_manager.py     # WebSocket connection registry
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── events.py                 # Pydantic models for all WS event payloads
│   │   └── game_state.py             # Pydantic models for room/game state
│   │
│   └── tests/
│       ├── test_deck.py
│       ├── test_bidding.py
│       ├── test_tricks.py
│       └── test_scoring.py
│
└── frontend/                         # Flutter app
    ├── pubspec.yaml
    ├── android/
    │   └── app/
    │       └── src/main/AndroidManifest.xml   # AdMob App ID goes here
    │
    └── lib/
        ├── main.dart                 # App entry, Riverpod ProviderScope, GoRouter setup
        │
        ├── core/
        │   ├── constants.dart        # API_BASE_URL, WS_BASE_URL, shared_prefs keys
        │   ├── theme.dart            # ThemeData, all color tokens, text styles
        │   ├── router.dart           # GoRouter route definitions
        │   └── extensions.dart       # Dart extension methods (card comparisons etc.)
        │
        ├── models/
        │   ├── card_model.dart       # Card, Suit, Value enums + helpers
        │   ├── player_model.dart     # Player (name, bid, tricksWon, isHost, isConnected)
        │   ├── room_state.dart       # RoomState (players, host, roomCode, status)
        │   └── game_state.dart       # GameState (round, trump, phase, scores)
        │
        ├── providers/
        │   ├── username_provider.dart         # AsyncNotifier, reads/writes shared_prefs
        │   ├── websocket_provider.dart        # WebSocket channel + event dispatcher
        │   ├── room_provider.dart             # RoomState notifier
        │   ├── game_provider.dart             # GameState notifier
        │   ├── hand_provider.dart             # Player's own hand
        │   ├── bids_provider.dart             # Bids map
        │   ├── trick_provider.dart            # Current trick pile
        │   └── scores_provider.dart           # Full score matrix
        │
        ├── services/
        │   ├── api_service.dart               # dio client, createRoom, roomExists
        │   └── websocket_service.dart         # connect, send, disconnect, reconnect logic
        │
        ├── screens/
        │   ├── home/
        │   │   ├── home_screen.dart
        │   │   └── widgets/
        │   │       ├── username_display.dart
        │   │       └── set_username_sheet.dart
        │   │
        │   ├── join/
        │   │   └── join_screen.dart
        │   │
        │   ├── lobby/
        │   │   ├── lobby_screen.dart
        │   │   └── widgets/
        │   │       ├── player_list_tile.dart
        │   │       └── room_code_display.dart
        │   │
        │   ├── game/
        │   │   ├── game_screen.dart           # Main game table
        │   │   └── widgets/
        │   │       ├── player_hand.dart        # Scrollable card fan
        │   │       ├── play_area.dart          # Center trick display
        │   │       ├── opponent_strip.dart     # Top bar with opponent tiles
        │   │       ├── trump_indicator.dart
        │   │       ├── card_widget.dart        # Single card widget (face/back)
        │   │       └── bidding_overlay.dart    # Bidding modal overlay
        │   │
        │   └── scoreboard/
        │       ├── scoreboard_screen.dart
        │       └── widgets/
        │           └── score_matrix.dart
        │
        └── widgets/                           # Shared/reusable widgets
            ├── primary_button.dart
            ├── secondary_button.dart
            ├── admob_banner.dart
            └── connection_status_banner.dart
```

---

## 2. Backend Setup

### 2.1 Prerequisites
- Python 3.11+
- Redis 7.x (local or Railway plugin)
- pip

### 2.2 Initial Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy env file and fill in values
cp .env.example .env
```

### 2.3 .env.example

```env
REDIS_URL=redis://localhost:6379
ALLOWED_ORIGINS=*
ROOM_TTL_SECONDS=7200
MAX_PLAYERS_PER_ROOM=6
MIN_PLAYERS_TO_START=2
```

### 2.4 main.py (entry point)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import room, websocket
import os

app = FastAPI(title="Judgement API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(room.router, prefix="/room")
app.include_router(websocket.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
```

### 2.5 Run Locally

```bash
uvicorn main:app --reload --port 8000
```

WebSocket endpoint will be at: `ws://localhost:8000/ws/{room_code}/{username}`

---

## 3. Frontend Setup

### 3.1 Prerequisites
- Flutter 3.x SDK
- Android Studio + Android SDK (API 21+ target)
- Physical Android device or emulator

### 3.2 pubspec.yaml Dependencies

```yaml
dependencies:
  flutter:
    sdk: flutter

  # State management
  flutter_riverpod: ^2.5.1
  riverpod_annotation: ^2.3.5

  # WebSocket
  web_socket_channel: ^2.4.5

  # HTTP
  dio: ^5.4.3+1

  # Local storage
  shared_preferences: ^2.2.3

  # Ads
  google_mobile_ads: ^4.0.0

  # Navigation
  go_router: ^13.2.5

  # Fonts
  google_fonts: ^6.2.1

  # Icons
  phosphor_flutter: ^2.1.0

  # Utils
  uuid: ^4.3.3

dev_dependencies:
  flutter_test:
    sdk: flutter
  build_runner: ^2.4.9
  riverpod_generator: ^2.4.2
  flutter_lints: ^3.0.0
```

### 3.3 Initial Setup

```bash
cd frontend

# Get dependencies
flutter pub get

# Run code generation (for Riverpod annotations)
dart run build_runner build --delete-conflicting-outputs

# Run on connected device
flutter run
```

### 3.4 core/constants.dart

```dart
class AppConstants {
  // Change this to your deployed backend URL before release
  static const String apiBaseUrl = 'http://localhost:8000';
  static const String wsBaseUrl = 'ws://localhost:8000';

  // SharedPreferences keys
  static const String keyUsername = 'player_username';

  // Game limits
  static const int maxUsernameLength = 16;
  static const int roomCodeLength = 6;

  // AdMob (use test IDs during dev)
  static const String admobBannerTestId = 'ca-app-pub-3940256099942544/6300978111';
  static const String admobNativeTestId = 'ca-app-pub-3940256099942544/2247696110';
}
```

### 3.5 AndroidManifest.xml Changes

Add inside `<application>` tag:

```xml
<!-- AdMob App ID — replace with your real ID before release -->
<meta-data
    android:name="com.google.android.gms.ads.APPLICATION_ID"
    android:value="ca-app-pub-XXXXXXXX~XXXXXXXXXX"/>

<!-- Internet permission (add outside <application> if not already there) -->
<uses-permission android:name="android.permission.INTERNET"/>
```

---

## 4. Core Theme Setup (core/theme.dart)

```dart
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppColors {
  static const feltGreen    = Color(0xFF2D5016);
  static const feltMid      = Color(0xFF3A6B1E);
  static const earthBrown   = Color(0xFF5C3A1E);
  static const warmCream    = Color(0xFFF5E6C8);
  static const haldiYellow  = Color(0xFFE8A020);
  static const sindoorRed   = Color(0xFFC0392B);
  static const inkBlack     = Color(0xFF1A0F0A);
  static const woodDark     = Color(0xFF3D2010);
  static const woodMid      = Color(0xFF6B4226);
  static const mutedText    = Color(0xFFB8966A);
  static const successGreen = Color(0xFF4CAF50);
  static const neutralMiss  = Color(0xFF78716C);
}

class AppTheme {
  static ThemeData get dark => ThemeData(
    scaffoldBackgroundColor: AppColors.earthBrown,
    colorScheme: const ColorScheme.dark(
      primary: AppColors.haldiYellow,
      secondary: AppColors.warmCream,
      surface: AppColors.woodDark,
      error: AppColors.sindoorRed,
    ),
    textTheme: GoogleFonts.dmSansTextTheme().copyWith(
      displayLarge: GoogleFonts.playfairDisplay(
        color: AppColors.warmCream,
        fontSize: 32,
        fontWeight: FontWeight.w700,
      ),
      headlineMedium: GoogleFonts.playfairDisplay(
        color: AppColors.warmCream,
        fontSize: 22,
        fontWeight: FontWeight.w700,
      ),
      bodyLarge: GoogleFonts.dmSans(
        color: AppColors.warmCream,
        fontSize: 15,
      ),
      bodyMedium: GoogleFonts.dmSans(
        color: AppColors.mutedText,
        fontSize: 13,
      ),
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: AppColors.haldiYellow,
        foregroundColor: AppColors.inkBlack,
        minimumSize: const Size.fromHeight(56),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        textStyle: GoogleFonts.dmSans(
          fontSize: 14,
          fontWeight: FontWeight.w600,
          letterSpacing: 1.5,
        ),
      ),
    ),
  );
}
```

---

## 5. GoRouter Setup (core/router.dart)

```dart
import 'package:go_router/go_router.dart';

final appRouter = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(path: '/',        builder: (ctx, state) => const HomeScreen()),
    GoRoute(path: '/join',    builder: (ctx, state) => const JoinScreen()),
    GoRoute(
      path: '/lobby/:roomCode',
      builder: (ctx, state) => LobbyScreen(
        roomCode: state.pathParameters['roomCode']!,
      ),
    ),
    GoRoute(
      path: '/game/:roomCode',
      builder: (ctx, state) => GameScreen(
        roomCode: state.pathParameters['roomCode']!,
      ),
    ),
    GoRoute(path: '/scores', builder: (ctx, state) => const ScoreboardScreen()),
  ],
);
```

---

## 6. Development Workflow

### Day 1–2: Backend Foundation
1. Set up FastAPI project structure
2. Implement Redis client helper
3. Implement `POST /room/create` and `GET /room/{code}/exists`
4. Write all game logic modules (`game/`) with unit tests
5. Verify tests pass: `pytest tests/`

### Day 3–4: Backend WebSocket
1. Implement `ConnectionManager`
2. Implement WebSocket router with join/leave handling
3. Implement full game flow: deal → bid → play → score
4. Manual test with `websocat` or a browser WebSocket client

### Day 5–6: Flutter Foundation
1. Set up project, install deps, run `build_runner`
2. Implement theme, constants, router
3. Implement `HomeScreen` with username flow
4. Implement `JoinScreen`
5. Implement `api_service.dart` (createRoom, roomExists)

### Day 7–9: Flutter Core Screens
1. Implement `LobbyScreen` + WebSocket connection
2. Implement `GameScreen` layout (static, no logic yet)
3. Implement `CardWidget` with correct theming
4. Implement `BiddingOverlay`
5. Wire all Riverpod providers to WebSocket events

### Day 10–11: Integration & Polish
1. Full end-to-end test: create room → join → play full game
2. Implement score matrix screen
3. Add AdMob (test IDs)
4. Implement reconnection logic
5. Edge case testing: host disconnect, player disconnect mid-game

### Day 12: Release Prep
1. Swap test AdMob IDs for real IDs
2. Update `apiBaseUrl` and `wsBaseUrl` to deployed backend
3. Deploy backend to Railway
4. `flutter build appbundle --release`
5. Upload to Google Play Internal Testing

---

## 7. Environment URLs Cheatsheet

| Environment | API Base | WS Base |
|---|---|---|
| Local dev | `http://localhost:8000` | `ws://localhost:8000` |
| Railway staging | `https://your-app.railway.app` | `wss://your-app.railway.app` |
| Production | `https://your-prod-domain.com` | `wss://your-prod-domain.com` |

Switch by updating `AppConstants.apiBaseUrl` and `AppConstants.wsBaseUrl` in `core/constants.dart`.

---

## 8. Testing Checklist (Pre-Release)

### Game Logic
- [ ] Trump rotates correctly across rounds
- [ ] Last bidder cannot make total = cards dealt (UI greys it out, server rejects it)
- [ ] Suit following enforced (unplayable cards are visually dimmed)
- [ ] Trick winner resolves correctly (trump vs non-trump)
- [ ] +10 for exact bid, 0 for miss
- [ ] Score matrix accumulates correctly across all rounds

### Multiplayer
- [ ] 2 players can complete a full game
- [ ] 6 players can complete a full game
- [ ] Player can join mid-lobby, before game starts
- [ ] Late join after game starts shows "Game already in progress"
- [ ] Host disconnect promotes next player
- [ ] Non-host disconnect skips their turns

### Ads
- [ ] Banner shows on Home screen
- [ ] Native/banner shows in Lobby
- [ ] Zero ads on Game Table or Scoreboard

### Edge Cases
- [ ] Invalid room code shows proper error
- [ ] Full room (6 players) shows "Room is full"
- [ ] WebSocket reconnect works after brief disconnect
- [ ] Room expires after 2 hours of inactivity
