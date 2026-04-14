# Frontend (Flutter)

## Run locally

1. Install packages:

```bash
flutter pub get
```

2. Run on Android emulator (backend on localhost:8000):

```bash
flutter run \
	--dart-define=API_BASE_URL=http://10.0.2.2:8000 \
	--dart-define=WS_BASE_URL=ws://10.0.2.2:8000
```

## Run tests

```bash
flutter test
```

## Build APK for friend testing

```bash
flutter build apk --release \
	--dart-define=API_BASE_URL=https://YOUR_PUBLIC_BACKEND_URL \
	--dart-define=WS_BASE_URL=wss://YOUR_PUBLIC_BACKEND_URL
```

APK output:

```text
build/app/outputs/flutter-apk/app-release.apk
```

## Important for internet multiplayer

- Use a publicly deployed backend URL, not localhost.
- Use `https` for API and `wss` for WebSocket.
- All players must run an APK built with the same backend URL.
