# File Structure & Setup Guide — Project Judgement (React Native)

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
│   │   ├── deck.py
│   │   ├── trump.py
│   │   ├── bidding.py
│   │   ├── tricks.py
│   │   └── scoring.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── redis_client.py
│   │   ├── room_service.py
│   │   ├── game_service.py
│   │   └── connection_manager.py
│   │
│   └── tests/
│       ├── test_deck.py
│       ├── test_bidding.py
│       ├── test_tricks.py
│       └── test_scoring.py
│
└── frontend/                         # React Native app (TypeScript)
    ├── package.json
    ├── tsconfig.json
    ├── babel.config.js
    ├── metro.config.js
    ├── android/
    │   └── app/src/main/AndroidManifest.xml
    ├── ios/
    ├── assets/
    │   └── cards/
    └── src/
        ├── App.tsx                   # App entry + provider wiring
        ├── core/
        │   ├── constants.ts          # API_BASE_URL, WS_BASE_URL, storage keys
        │   ├── theme.ts              # Color tokens + typography
        │   └── env.ts                # runtime env resolver
        ├── navigation/
        │   └── index.tsx             # React Navigation stacks
        ├── models/
        │   ├── card.ts
        │   ├── player.ts
        │   ├── roomState.ts
        │   └── gameState.ts
        ├── store/
        │   ├── useConnectionStore.ts
        │   ├── useRoomStore.ts
        │   ├── useGameStore.ts
        │   └── useUserStore.ts
        ├── services/
        │   ├── apiClient.ts          # axios instance + room APIs
        │   ├── socketClient.ts       # WS connect/send/reconnect
        │   └── eventDispatcher.ts    # WS event → store updates
        ├── screens/
        │   ├── HomeScreen.tsx
        │   ├── JoinRoomScreen.tsx
        │   ├── LobbyScreen.tsx
        │   ├── GameScreen.tsx
        │   └── ScoreboardScreen.tsx
        └── components/
            ├── CardView.tsx
            ├── BiddingOverlay.tsx
            ├── OpponentStrip.tsx
            ├── TrumpIndicator.tsx
            ├── ScoreMatrix.tsx
            └── AdBanner.tsx
```

---

## 2. Backend Setup

### 2.1 Prerequisites
- Python 3.11+
- Redis 7.x
- pip

### 2.2 Initial Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 2.3 Run Backend

```bash
uvicorn main:app --reload --port 8000
```

WebSocket endpoint:

```text
ws://localhost:8000/ws/{room_code}/{username}
```

---

## 3. Frontend Setup (React Native)

### 3.1 Prerequisites
- Node.js 20+
- JDK 17+
- Android Studio + SDK + emulator
- React Native CLI environment configured

### 3.2 Project Initialization

```bash
# if creating fresh
npx react-native@latest init frontend --template react-native-template-typescript

cd frontend
npm install
```

### 3.3 Core Dependencies

```bash
npm install axios zustand @react-native-async-storage/async-storage
npm install @react-navigation/native @react-navigation/native-stack
npm install react-native-screens react-native-safe-area-context
npm install react-native-svg react-native-google-mobile-ads
```

### 3.4 Local Run (Android Emulator)

```bash
# from frontend/
npx react-native run-android
```

Use this API/WS base for emulator:

```text
API_BASE_URL=http://10.0.2.2:8000
WS_BASE_URL=ws://10.0.2.2:8000
```

### 3.5 Release Builds

```bash
cd android
./gradlew assembleRelease     # APK
./gradlew bundleRelease       # AAB
```

Artifacts:

```text
android/app/build/outputs/apk/release/app-release.apk
android/app/build/outputs/bundle/release/app-release.aab
```

### 3.6 AdMob AndroidManifest

Add inside `android/app/src/main/AndroidManifest.xml`:

```xml
<meta-data
  android:name="com.google.android.gms.ads.APPLICATION_ID"
  android:value="ca-app-pub-XXXXXXXX~XXXXXXXXXX"/>
```

---

## 4. App Constants (src/core/constants.ts)

```ts
export const AppConstants = {
  apiBaseUrl: 'http://10.0.2.2:8000',
  wsBaseUrl: 'ws://10.0.2.2:8000',

  storageKeys: {
    username: 'player_username',
  },

  limits: {
    roomCodeLength: 6,
    maxUsernameLength: 16,
  },
};
```

---

## 5. Navigation Skeleton (src/navigation/index.tsx)

```tsx
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

export function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="JoinRoom" component={JoinRoomScreen} />
        <Stack.Screen name="Lobby" component={LobbyScreen} />
        <Stack.Screen name="Game" component={GameScreen} />
        <Stack.Screen name="Scoreboard" component={ScoreboardScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

---

## 6. Development Workflow (4-Day Window)

### Day 1: Backend Rules + APIs
1. Validate game modules and backend tests.
2. Confirm room create/check + WS contract.

### Day 2: WS Orchestration + Reliability
1. Validate full round flow via tests.
2. Validate disconnect/host migration paths.

### Day 3: React Native Functional Wiring
1. Scaffold RN app structure.
2. Implement Home/Join/Lobby/Game screens.
3. Wire WebSocket events into Zustand store.

### Day 4: Polish + Release
1. Add AdMob only on Home/Lobby.
2. Run reconnection + edge-case checks.
3. Generate signed APK/AAB and share for internal testing.

---

## 7. Testing Checklist (Pre-Release)

### Game Logic
- [ ] Trump rotation correct
- [ ] Last-bid illegal value enforced UI + server
- [ ] Follow-suit enforced
- [ ] Trick winner resolution correct
- [ ] Exact-bid scoring correct

### Multiplayer
- [ ] 2-player full game
- [ ] 6-player full game
- [ ] Host migration on disconnect
- [ ] Mid-game disconnect auto-skip

### Mobile
- [ ] Home and Lobby ads only
- [ ] No ads on Game/Scoreboard
- [ ] Emulator + physical Android device sanity pass
- [ ] Release APK and AAB generated successfully
