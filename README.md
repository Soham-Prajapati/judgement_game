# Judgement Multiplayer

End-to-end runbook for local development, internet testing, and APK distribution.

## 1) Backend local setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Run Redis locally (Docker):

```bash
docker run --name judgement-redis -p 6379:6379 -d redis:7
```

Start FastAPI:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Run backend tests:

```bash
pytest -q
```

## 2) Frontend local setup

```bash
cd frontend
flutter pub get
flutter test
```

Run on Android emulator (uses local backend):

```bash
flutter run \
  --dart-define=API_BASE_URL=http://10.0.2.2:8000 \
  --dart-define=WS_BASE_URL=ws://10.0.2.2:8000
```

## 3) Internet multiplayer (friends on any network)

You must deploy backend publicly first.

Recommended:
- Railway or Render (backend service)
- Managed Redis attached to the same environment

Minimum environment variables:

```env
REDIS_URL=redis://...or rediss://...
ALLOWED_ORIGINS=*
ROOM_TTL_SECONDS=7200
MAX_PLAYERS_PER_ROOM=6
```

After deploy, verify:

```bash
curl https://YOUR_PUBLIC_BACKEND_URL/health
```

Expected:

```json
{"status":"ok"}
```

Then build APK pointing to that public URL.

## 4) Build release APK

```bash
cd frontend
flutter build apk --release \
  --dart-define=API_BASE_URL=https://YOUR_PUBLIC_BACKEND_URL \
  --dart-define=WS_BASE_URL=wss://YOUR_PUBLIC_BACKEND_URL
```

APK path:

```text
frontend/build/app/outputs/flutter-apk/app-release.apk
```

## 5) Friend test checklist

- Install APK on 2+ Android phones
- One player creates room, shares room code
- Other player joins from different internet connection
- Start game, complete at least one full round
- Force disconnect host, verify host migration
- Rejoin flow to be validated in next frontend iteration

## 6) Current implementation scope

- Backend game flow events are implemented and covered by tests.
- Frontend is scaffolded and APK-buildable with runtime backend URL defines.
- Full UI wiring for create/join/lobby/game screens is the next workstream.