# Project Judgement (Kachuful)

A real-time multiplayer mobile card game built with React Native and FastAPI.

## Tech Stack
- **Frontend:** React Native (TypeScript) + Pixel Art Assets
- **Backend:** FastAPI (Python)
- **Real-time:** WebSockets
- **Store:** Redis (Ephemeral state)

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 20+
- Redis 7.x (`brew install redis`)
- Android Emulator or Physical Device

### Quick Run
The easiest way to run the project is using the root script:

```bash
./run.sh
```

### Manual Setup

#### 1. Start Redis
```bash
brew services start redis
```

#### 2. Start Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

#### 3. Start Frontend
```bash
cd frontend
npm install
npx react-native run-android
```

## Game Rules
- 2-6 players.
- Rounds decrease from 7 cards down to 1.
- Trump suit rotates every round (S -> D -> H -> C).
- **The Bidding Rule:** The last player cannot bid a number that makes the total bids equal to the cards dealt.
- Score 10 points for an exact bid match, 0 otherwise.
