# Technical Architecture — Project Judgement

**Version:** 2.0 (Hugging Face / Expo Update)

---

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Expo App (Android/iOS/Web)               │
│                                                             │
│  ┌─────────────┐   WebSocket (wss://)  ┌─────────────────┐ │
│  │  UI Layer   │ ◄──────────────────► │  WS Client      │ │
│  │ (Pixel Art) │                       │  + Auto-Reconnect│ │
│  └──────┬──────┘                       └────────┬────────┘ │
│         │ Zustand                                 │         │
│  ┌──────▼──────┐                       ┌────────▼────────┐ │
│  │ State Store │◄──────────────────────│ Event Reducers  │ │
│  └─────────────┘                       └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                             │ Secure WebSocket
                             │
┌────────────────────────────▼────────────────────────────────┐
│               Hugging Face Spaces (Docker)                  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              FastAPI Backend (Port 7860)             │   │
│  │         /ws/{room_code}/{username}                   │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     │                                        │
│  ┌──────────────────▼──────────────────────────────────┐   │
│  │              Game Engine (Pure Python)               │   │
│  │  - U-Turn Logic (1-7-1)  - 8 Player Capacity         │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     │                                        │
│  ┌──────────────────▼──────────────────────────────────┐   │
│  │              Upstash Redis (Remote Database)         │   │
│  │  room:{code}:meta  |  room:{code}:players           │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Key Changes from V1

### 2.1 Backend (FastAPI)
- **Deployment:** Dockerized for Hugging Face Spaces.
- **WebSocket Security:** Supports `wss://` for secure global communication.
- **Resilience:** Implemented host migration and auto-skip for disconnected players.

### 2.2 Frontend (Expo)
- **Framework:** Switched to Expo for better portability and storage efficiency.
- **Assets:** Integrated high-quality pixel art card pack.
- **Navigation:** Root-level Stack Navigator with Home, Lobby, Game, and Scoreboard.

### 2.3 Game Logic (U-Turn)
- **Round Scaling:** 1 to 7 cards, then back to 1.
- **Player Limit:** Increased to 8 players (Deck limit logic applied).
