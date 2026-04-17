# CODEBASE MAP

## Repository layout

```text
judgement/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── pytest.ini
│   ├── game/
│   │   ├── deck.py
│   │   ├── trump.py
│   │   ├── bidding.py
│   │   ├── tricks.py
│   │   └── scoring.py
│   ├── routers/
│   │   ├── room.py
│   │   └── websocket.py
│   ├── services/
│   │   ├── redis_client.py
│   │   ├── room_service.py
│   │   ├── game_service.py
│   │   └── connection_manager.py
│   └── tests/
│       ├── test_deck.py
│       ├── test_trump.py
│       ├── test_bidding.py
│       ├── test_tricks.py
│       └── test_scoring.py
├── frontend/
│   ├── package.json
│   ├── .eslintrc.js
│   ├── .eslintignore
│   ├── src/
│   │   ├── core/constants.ts
│   │   ├── navigation/index.tsx
│   │   ├── services/apiClient.ts
│   │   ├── services/socketClient.ts
│   │   ├── screens/
│   │   ├── components/
│   │   └── store/
│   └── assets/
├── Dockerfile
├── run.sh
└── project_documentation_and_planning/
```

## Runtime data flow

1. Frontend uses `frontend/src/core/constants.ts` for API and WebSocket base URLs.
2. REST calls hit backend routes in `backend/routers/room.py`.
3. Realtime game events use `backend/routers/websocket.py`.
4. Room/game state is stored in Redis through `backend/services/*`.
5. Pure game rules live in `backend/game/*` and are independently testable.

## Important generated/local-only folders

- `frontend/node_modules/` and `frontend/dist/`: generated, do not edit by hand.
- `backend/venv/`: local Python environment.
- `backend/__pycache__/`, `.pytest_cache/`: cache artifacts.
