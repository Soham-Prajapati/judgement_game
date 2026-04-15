# Project Judgement (Kachuful)

A real-time multiplayer mobile card game built with Expo (React Native) and FastAPI.

## Tech Stack
- **Frontend:** Expo / React Native (TypeScript) + Pixel Art Assets
- **Backend:** FastAPI (Python)
- **Real-time:** WebSockets
- **Store:** Redis (Ephemeral state)

## Getting Started

### 1. Prerequisites
- Python 3.11+
- Node.js 20+
- Redis 7.x (`brew install redis`)
- **Mobile Phone:** Install the **Expo Go** app from the App Store or Play Store.

### 2. Quick Run (Recommended)
1. Start Redis: `brew services start redis`
2. Run the master script: `./run.sh`
3. Select **Option 2** (Start Frontend).
4. A **QR Code** will appear in your terminal.
5. Open the **Expo Go** app on your phone and **Scan the QR Code**.

---

## Playing with Friends (Public Hosting)
If your backend is hosted on Railway:
1. Open `frontend/src/core/constants.ts`.
2. Update `apiBaseUrl` and `wsBaseUrl` to your Railway URLs.
3. Run `npx expo start` in the `frontend` folder.
4. Anyone with the Expo Go app can scan your QR code and play with you!

## Game Rules
- 2-6 players.
- Rounds decrease from 7 cards down to 1.
- Trump suit rotates every round (S -> D -> H -> C).
- **The Bidding Rule:** The last player cannot bid a number that makes the total bids equal to the cards dealt.
- Score 10 points for an exact bid match, 0 otherwise.
