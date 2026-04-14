# PRD — Project Judgement (Kachuful)
**Version:** 2.0  
**Status:** Ready for implementation  
**Stack:** Flutter (mobile) + FastAPI + WebSockets + Redis

---

## 1. Product Summary

Project Judgement is a real-time multiplayer mobile card game based on the Indian trick-taking game **Kachuful (Judgement)**. It is frictionless by design — no sign-up, no login, no accounts. Players open the app, enter a username stored locally, create or join a private 6-digit room, and play.

Monetization is handled via Google AdMob banner/native ads in non-gameplay screens only. The one-time Google Play Developer fee ($25) and hosting costs are recovered passively without disrupting the experience.

---

## 2. Goals & Non-Goals

### Goals
- Zero-friction entry: username stored on device, no account needed
- Real-time multiplayer via WebSockets (2–6 players)
- Full Kachuful rule implementation with correct bidding constraint
- Private rooms with auto-expiry (no persistent data)
- Monetization via AdMob without polluting gameplay screens
- Android-first launch (Google Play)

### Non-Goals
- No user accounts, profiles, or leaderboards (V1)
- No AI/bot opponents (V1)
- No iOS launch (V1)
- No in-app purchases (V1)
- No chat feature (V1)

---

## 3. User Personas

**The Instigator** — The one who sets up the room. Opens app, taps "Create Room", shares the code on WhatsApp. Probably on the way to a family gathering.

**The Joiner** — Gets a code shared by Instigator. Taps "Join Room", types code, waits in lobby. Low friction needed here or they drop off.

**The Occasional Player** — Plays once in a while. Must not be asked to remember a password or account. Username saved locally covers them.

---

## 4. Core Game Rules

### 4.1 Players
- Minimum: 2, Maximum: 6
- Host is the player who created the room

### 4.2 Deck
- Standard 52-card deck, no Jokers
- Card hierarchy (high to low): A, K, Q, J, 10, 9, 8, 7, 6, 5, 4, 3, 2

### 4.3 Round Structure
- Rounds decrease from N cards down to 1, then optionally increase back (configurable by host)
- Default: 7 cards → 6 → 5 → 4 → 3 → 2 → 1 (7 rounds total for default session)
- Each round: deal → bid → play tricks → score

### 4.4 Trump Rotation
Strict cyclic order per round, resetting at the start of each game:

```
Round 1: Spades ♠
Round 2: Diamonds ♦
Round 3: Hearts ♥
Round 4: Clubs ♣
Round 5: Spades ♠  (cycles again)
...and so on
```

Trump suit is displayed prominently at all times during play.

### 4.5 Bidding Phase
- Players bid in turn (clockwise from the player left of the dealer)
- Each player states how many tricks they expect to win
- **Critical constraint:** The last player to bid CANNOT place a bid that makes the total sum equal to the number of cards dealt in that round. The UI must enforce this — grey out the illegal bid value.
- Minimum bid: 0

### 4.6 Trick-Taking Rules
- The player who wins the previous trick leads the next one
- Players **must follow the lead suit** if they have a card of that suit
- If a player has no card of the lead suit, they may play any card (including trump)
- Trick winner determination:
  - If no trump played: highest card of lead suit wins
  - If trump played: highest trump card wins
  - If multiple trumps: highest trump wins

### 4.7 Scoring
- **Exact bid hit:** +10 points
- **Bid missed (over or under):** 0 points
- No incremental points per trick won
- Cumulative score tracked across all rounds in a matrix

### 4.8 Game End
- Game ends after all rounds are complete
- Player with highest cumulative score wins
- Rematch option available (same room, same players, new game)

---

## 5. Screen-by-Screen Spec

### Screen 1: Home Screen

**Purpose:** Entry point. Fast, no friction.

**Elements:**
- App logo + name "Judgement" (styled)
- Username display with inline edit ("Playing as: [name] ✏️")
- `Create Room` button (primary CTA)
- `Join Room` button (secondary CTA)
- AdMob Banner Ad — anchored bottom, full width

**Behaviour:**
- On first launch, prompt user to set a username (bottom sheet modal)
- Username saved via `shared_preferences`, pre-filled on all future opens
- "Create Room" → calls API to generate room → navigate to Waiting Room as Host
- "Join Room" → navigate to Join Room Screen

**Edge cases:**
- Empty username not allowed — show inline validation
- Username max length: 16 characters

---

### Screen 2: Join Room Screen

**Purpose:** Enter a room code to join.

**Elements:**
- Back arrow
- 6-character alphanumeric input (large, bold, monospace font)
- `Join` button
- Error state: "Room not found", "Room is full", "Game already started"

**Behaviour:**
- Auto-uppercase input
- On valid join: navigate to Waiting Room as Guest
- Disable `Join` button until 6 characters entered

---

### Screen 3: Waiting Room (Lobby)

**Purpose:** Wait for all players to join. Host starts game.

**Elements:**
- Room code displayed large (tap to copy)
- "Share code" icon (triggers native share sheet)
- Connected player list — real-time updating via WebSocket
- Host badge on the host's entry
- `Start Game` button — **visible to host only**, enabled when ≥2 players
- AdMob Native/Rectangular Banner — embedded in center/bottom of screen

**Behaviour:**
- WebSocket stays open; server pushes `server_room_state` on every player join/leave
- Non-host players see a "Waiting for host to start..." state
- If host disconnects: next player in order becomes host
- Room code is valid for 2 hours from creation (Redis TTL)

---

### Screen 4: Game Table

**Purpose:** Main gameplay screen. Zero ads, zero distractions.

**Layout (portrait):**
- **Top strip:** Opponent avatars in a row — each showing name, bid number, tricks won so far, and a turn indicator (glowing ring)
- **Center play area:** Cards played in current trick arranged in a fan/spread. Trump suit icon prominent.
- **Bottom panel:** Player's hand — horizontally scrollable, fanned card layout. Cards are tap-to-play.
- **Score icon:** Tap to peek at current scoreboard (modal overlay, doesn't navigate away)

**Bidding overlay (shown before tricks begin):**
- Full-screen modal overlay on the game table
- Turn-based: each player sees their bid input when it's their turn
- Number selector (0 to N cards)
- Illegal bid value is greyed out with tooltip "Can't make total equal cards dealt"
- Other players see "Waiting for [name] to bid..."

**Trick resolution:**
- Short animation when trick is won (cards slide to winner's side)
- Brief 1.5s pause before next trick starts (so players can see result)

**Edge cases:**
- If a player disconnects mid-game: their turns are auto-skipped, UI shows "[name] disconnected"
- If all other players disconnect: show "Everyone left" screen with exit option

---

### Screen 5: Round End / Scoreboard

**Purpose:** Show scores after each round ends.

**Elements:**
- Matrix table: rows = rounds, columns = players
- Each cell: shows score earned that round, colour-coded (green = hit bid, red/grey = missed)
- Running total row at bottom
- `Next Round` button (host only) or auto-advance after 5s countdown
- After final round: shows "Game Over" banner + winner highlight + `Play Again` / `Exit` buttons

---

## 6. WebSocket Event Protocol

All messages are JSON. Every event has a `type` field.

### Client → Server

| Event | Payload | Description |
|---|---|---|
| `client_join_room` | `{room_code, username}` | Player joins or creates a room |
| `client_place_bid` | `{room_code, username, bid}` | Player submits bid |
| `client_play_card` | `{room_code, username, card}` | Player plays a card from hand |
| `client_start_game` | `{room_code}` | Host starts the game |
| `client_next_round` | `{room_code}` | Host advances to next round |
| `client_rematch` | `{room_code}` | Host restarts with same players |

### Server → Client

| Event | Payload | Description |
|---|---|---|
| `server_room_state` | `{players: [], room_code, host}` | Broadcast on any lobby change |
| `server_deal_cards` | `{hand: [], trump_suit, round_num, total_cards}` | Per-player private deal |
| `server_bid_request` | `{current_bidder, bids_so_far, illegal_bid?}` | Broadcast during bidding phase |
| `server_bid_update` | `{bids: {username: bid}}` | Broadcast as each bid is placed |
| `server_turn_update` | `{current_player, trick_so_far: []}` | Broadcast on each card play |
| `server_trick_result` | `{winner, trick_cards: []}` | Broadcast when trick resolves |
| `server_round_end` | `{scores: {}, round_num}` | Broadcast when round ends |
| `server_game_over` | `{final_scores: {}, winner}` | Broadcast when all rounds done |
| `server_player_left` | `{username, new_host?}` | Broadcast when someone disconnects |
| `server_error` | `{code, message}` | Error response to client |

---

## 7. Monetization

| Placement | Format | Trigger |
|---|---|---|
| Home Screen | AdMob Banner (320x50 or adaptive) | Always visible, anchored bottom |
| Waiting Room | AdMob Native or Medium Rectangle (300x250) | Embedded while waiting |
| Game Table | **None** | — |
| Scoreboard | **None** | — |

Ad policy: No interstitials, no rewarded ads, no pop-ups. Ads only in waiting states, never during active gameplay.

---

## 8. Local Storage Schema

Stored via `shared_preferences` on device:

| Key | Type | Description |
|---|---|---|
| `player_username` | String | Display name, set on first launch |

No other persistent data on device.

---

## 9. Error States & Edge Cases

| Scenario | Handling |
|---|---|
| Room code not found | Show "Room not found" error on join screen |
| Room full (6 players) | Show "Room is full" error |
| Game already started | Show "Game already in progress" error |
| Player disconnects in lobby | Remove from list, broadcast updated `server_room_state` |
| Player disconnects in game | Auto-skip their turns, show disconnected indicator |
| Host disconnects | Promote next player in list to host |
| All players disconnect | Room deleted from Redis immediately |
| WebSocket connection lost | Flutter client shows reconnect banner, attempts reconnect x3 |
| Redis room TTL expires | Room silently cleaned up; if players still connected, show "Session expired" |

---

## 10. Out of Scope (V1)

- Sound effects and background music
- Card animations beyond basic slide/flip
- Custom avatars
- Game replay
- Tournament mode
- Push notifications
- iOS build
- Tablet layout
