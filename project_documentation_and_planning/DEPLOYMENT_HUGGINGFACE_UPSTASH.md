# Deployment Runbook: Hugging Face + Upstash Redis

## 1) Required infra

1. **Hugging Face Space** (Docker SDK).
2. **Upstash Redis** instance (TLS endpoint + token).

## 2) Backend deploy to Hugging Face

1. Create/Use a Space configured for **Docker**.
2. Connect the Space to this GitHub repository (`Soham-Prajapati/judgement_game`) or push this repo to the Space remote.
3. Ensure root `Dockerfile` exists (it does in this repo) so HF can build app image.

If your Space shows **"No application file"**, it means the Space is still empty template content and does not yet contain this repository code.

## 3) Configure environment variables in Space settings

Set these variables for backend:

```env
REDIS_URL=rediss://default:<UPSTASH_TOKEN>@<UPSTASH_ENDPOINT>:6379
ALLOWED_ORIGINS=*
ROOM_TTL_SECONDS=7200
MAX_PLAYERS_PER_ROOM=6
PORT=7860
```

Use `rediss://` (TLS), not `redis://`, for Upstash.

## 4) Frontend base URL update

Set `frontend/src/core/constants.ts`:

```ts
apiBaseUrl: 'https://<your-space-subdomain>.hf.space'
wsBaseUrl: 'wss://<your-space-subdomain>.hf.space'
```

Use `wss://` when backend is served on `https://`.

## 5) Smoke check after deploy

1. Open `https://<your-space-subdomain>.hf.space/` and confirm backend health/static response.
2. Create room from app.
3. Join with second client and verify WebSocket room state updates.
