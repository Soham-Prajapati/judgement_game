# PRD — Project Judgement (Kachuful)
**Version:** 3.0 (Final)  
**Status:** Implemented  
**Stack:** Expo (React Native) + FastAPI + WebSockets + Upstash Redis  
**Hosting:** Hugging Face Spaces (Docker)

---

## 1. Product Summary

Project Judgement is a real-time multiplayer mobile card game based on the Indian trick-taking game **Kachuful (Judgement)**. It is frictionless by design — no sign-up, no login. Players open the app (or web link), enter a username, create or join a private 6-digit room, and play.

---

## 2. Goals

- **Zero-friction entry:** No account needed.
- **Global Multiplayer:** Works across different networks via Hugging Face hosting.
- **Resilient Gameplay:** Auto-reconnect for mobile signals and auto-skip for disconnected players.
- **U-Turn Logic:** Game flows from 1 card up to 7, and back down to 1.
- **Scalability:** Supports up to 8 players in a single room.

---

## 3. Core Game Rules

### 4.1 Players
- Minimum: 2, **Maximum: 8**
- Host migration enabled (next player becomes host if original leaves).

### 4.2 Round Structure (U-Turn)
The game follows a strict increasing and decreasing pattern:
- **Phase 1 (Up):** 1 card → 2 → 3 → 4 → 5 → 6 → 7
- **Phase 2 (Down):** 6 → 5 → 4 → 3 → 2 → 1
- **Total Rounds:** 13 rounds per game.

### 4.3 Bidding Phase
- **Critical constraint:** The last player to bid CANNOT place a bid that makes the total sum equal to the number of cards dealt in that round. 

### 4.4 Scoring
- **Exact bid hit:** +10 points.
- **Bid missed:** 0 points.
- Cumulative scores tracked in a global leaderboard within the room.

---

## 4. Technical Resilience
- **Auto-Reconnect:** Frontend attempts reconnection with exponential backoff if socket drops.
- **Player Cleanup:** Disconnected players are removed from Redis to prevent "ghost" players.
- **Auto-Skip:** If a player is disconnected during their turn, the server ensures the game continues.
