# File Structure & Setup — Project Judgement

---

## 1. Repository Structure

```
judgement/
├── Dockerfile                        # Multi-stage build (Frontend + Backend)
├── package.json                      # Root-level dev runner scripts
├── run.sh                            # Ultimate dev runner (Expo/HF/Local)
├── backend/                          # FastAPI server
│   ├── main.py                       # App entry point & static serving
│   ├── requirements.txt
│   ├── routers/
│   │   ├── room.py                   # Room management APIs
│   │   └── websocket.py              # Real-time game logic & events
│   ├── game/                         # Pure Python game engine
│   └── services/                     # Redis, Game, and Connection services
└── frontend/                         # Expo App (TypeScript)
    ├── App.tsx                       # App entry + theme
    ├── app.json                      # Expo config (no native icons needed)
    ├── assets/
    │   └── cards/                    # Pixel art card assets
    └── src/
        ├── core/assets.ts            # Dynamic asset mapping
        ├── navigation/
        ├── store/                    # Zustand stores (Game, Room, User)
        ├── services/                 # Socket and API clients
        ├── screens/                  # Game screens
        └── components/               # Custom UI (CardView, OpponentStrip)
```

---

## 2. Global Deployment (Hugging Face)

### Prerequisites
- Upstash Account (Free Redis)
- Hugging Face Account (Free Space)

### Deployment Steps
1.  **Redis:** Create a database on Upstash and copy the `REDIS_URL`.
2.  **Space:** Create a new Docker Space on Hugging Face.
3.  **Config:** In Space Settings, add the `REDIS_URL` secret.
4.  **Go Live:** Run `./run.sh`, select **Option 3**, and follow prompts.

---

## 3. Local Development

```bash
# 1. Start Local Redis
brew services start redis

# 2. Run Master Script
npm run dev
```
*Select **Option 2** for local simulator or same-WiFi phone testing.*
