# UI/UX Design System — Project Judgement
**Theme: Desi-Coded**  
Warm, earthy, card-table felt. The feeling of playing cards at a family gathering — bajra-coloured walls, worn wooden tables, haldi-yellow light, the scuff of a deck being shuffled.

---

## 1. Design Philosophy

This is not a sterile fintech app. It's not neon cyberpunk. It's **warm, tactile, and familiar** — the visual equivalent of a card game on a Sunday afternoon.

Every screen should feel like a **physical space**, not a UI. Cards have weight. The table has texture. The type is confident and direct.

**Three words to test every design decision:**  
Warm. Grounded. Alive.

---

## 2. Color Palette

### Primary Palette

| Token | Hex | Usage |
|---|---|---|
| `--felt-green` | `#2D5016` | Card table felt — play area background |
| `--felt-mid` | `#3A6B1E` | Slightly lighter felt, card area highlight |
| `--earth-brown` | `#5C3A1E` | Primary dark surface (app background, nav) |
| `--warm-cream` | `#F5E6C8` | Primary text, card faces, light surfaces |
| `--haldi-yellow` | `#E8A020` | Primary accent — CTAs, highlights, trump indicator |
| `--sindoor-red` | `#C0392B` | Hearts/Diamonds suit colour, error states, danger |
| `--ink-black` | `#1A0F0A` | Spades/Clubs suit colour, deep backgrounds |

### Secondary / Utility

| Token | Hex | Usage |
|---|---|---|
| `--wood-dark` | `#3D2010` | Elevated surfaces, cards background tint |
| `--wood-mid` | `#6B4226` | Borders, dividers |
| `--muted-text` | `#B8966A` | Secondary text, placeholder, labels |
| `--success-green` | `#4CAF50` | Score hit (+10), connected indicators |
| `--neutral-miss` | `#78716C` | Score missed (0), disconnected state |
| `--overlay-dark` | `rgba(26, 15, 10, 0.85)` | Modal/overlay backgrounds |

### Suit Colors
```
♠ Spades   → --ink-black    (#1A0F0A)
♣ Clubs    → --ink-black    (#1A0F0A)
♥ Hearts   → --sindoor-red  (#C0392B)
♦ Diamonds → --sindoor-red  (#C0392B)
```

---

## 3. Typography

### Font Choices

| Role | Font | Weight | Notes |
|---|---|---|---|
| Display / Logo | **Tiro Devanagari Latin** | 400 | Has a subtle Indic script quality in its serifs. Gives the logo soul. |
| Headings | **Playfair Display** | 700 | Rich, editorial serif. Used for room codes, round numbers, score totals. |
| Body / UI | **DM Sans** | 400 / 500 | Clean, readable sans. All body copy, labels, buttons. |
| Monospace (room code) | **JetBrains Mono** | 600 | Room code display, card values |

All fonts available on Google Fonts, free for Flutter via `google_fonts` package.

### Type Scale

```
Display   → 32sp  Tiro Devanagari Latin  400   (App name, game over screen)
H1        → 28sp  Playfair Display        700   (Room code, round title)
H2        → 22sp  Playfair Display        700   (Score header, section titles)
H3        → 18sp  DM Sans                 600   (Player names in lobby)
Body      → 15sp  DM Sans                 400   (General body text)
Label     → 13sp  DM Sans                 500   (Button text, tags, badges)
Caption   → 11sp  DM Sans                 400   (Secondary info, tooltips)
Code      → 24sp  JetBrains Mono          600   (Room code input/display)
```

### Letter Spacing
- Room code display: `letter-spacing: 8px` — makes it scannable
- Button labels: `letter-spacing: 1.5px`, `text-transform: uppercase`

---

## 4. Component Specs

### 4.1 Buttons

**Primary CTA (Create Room):**
```
Background: --haldi-yellow (#E8A020)
Text: --ink-black (#1A0F0A)
Font: DM Sans 600, 14sp, uppercase, letter-spacing 1.5px
Border radius: 12px
Padding: 18px vertical, 32px horizontal
Shadow: 0px 4px 12px rgba(232, 160, 32, 0.4)
Pressed state: scale(0.97), brightness -10%
```

**Secondary (Join Room):**
```
Background: transparent
Border: 2px solid --warm-cream (#F5E6C8)
Text: --warm-cream
Same sizing as primary
Pressed state: background fills with rgba(245,230,200,0.1)
```

**Destructive / Ghost:**
```
Text: --sindoor-red
No border, no background
Used for: Leave Room, Exit
```

### 4.2 Cards (Playing Cards)

Card widget is central — spend time on this.

```
Card face:
  Background: --warm-cream (#F5E6C8)
  Border radius: 8px
  Shadow: 2px 4px 8px rgba(26,15,10,0.5)
  Size (in hand): 72px × 100px
  Size (in play area): 80px × 112px

Card back:
  Background: --earth-brown (#5C3A1E)
  Pattern: Subtle geometric (block-print style, can be an SVG asset)
  Border: 2px solid --wood-mid

Card value + suit (top-left and bottom-right):
  Font: JetBrains Mono 700
  Size: 16sp
  Color: --ink-black (spades/clubs) or --sindoor-red (hearts/diamonds)

Center suit icon:
  Large suit symbol, 32px
  Color: same as above

Selected card (in hand, tapped but not yet played):
  Translate up: -16px
  Border: 2px solid --haldi-yellow
  Shadow: 0px 0px 12px rgba(232,160,32,0.6)

Unplayable card (not your turn, or suit violation):
  Opacity: 0.4
  No hover/tap effect
```

### 4.3 Player Avatar Tiles (Game Table)

```
Container: 64px × 80px
Background: --wood-dark with 12px border radius
Player name: DM Sans 500, 11sp, --warm-cream, centered, truncated at 8 chars
Bid badge: small rounded pill, --haldi-yellow bg, --ink-black text, "Bid: N"
Tricks badge: below bid, muted text
Turn indicator: 2px animated glowing ring, --haldi-yellow, pulsing animation
Disconnected: red X overlay, opacity 0.5
```

### 4.4 Trump Indicator

```
Positioned: top-center of play area
Container: rounded pill, 40px height
Background: --wood-dark
Content: Suit icon (24px) + "TRUMP" label (DM Sans 500, 11sp, --muted-text)
Suit icon color: --sindoor-red or --ink-black based on suit
Animated: subtle pulse on round start (scale 1 → 1.1 → 1)
```

### 4.5 Score Matrix

```
Table background: --wood-dark
Header row: --earth-brown bg, --haldi-yellow text, DM Sans 600
Round rows: alternating --wood-dark / slightly lighter for readability
Score cell — hit bid: --success-green text, DM Sans 600
Score cell — missed: --neutral-miss text, DM Sans 400
Running total row: --haldi-yellow text, Playfair Display 700
Border color: --wood-mid, 1px
Cell padding: 12px vertical, 8px horizontal
```

### 4.6 Room Code Display

```
Font: JetBrains Mono 600, 32sp
Color: --haldi-yellow
Letter spacing: 8px
Background: --wood-dark pill container, padding 16px 24px
"Tap to copy" icon: copy icon in --muted-text beside code
Tap feedback: brief scale pulse + "Copied!" toast
```

### 4.7 Input Fields

```
Background: --wood-dark
Border: 2px solid --wood-mid
Border radius: 10px
Focus border: --haldi-yellow
Text: --warm-cream, DM Sans 400, 16sp
Placeholder: --muted-text
Room code input: JetBrains Mono 600, 24sp, letter-spacing 4px, centered
```

---

## 5. Screen-Level Layout Specs

### 5.1 Home Screen

```
Background: --earth-brown
Texture overlay: subtle noise/grain SVG at 8% opacity (adds tactile warmth)

Layout (top to bottom):
  Top 40%: Logo area
    - App name "Judgement" in Tiro Devanagari Latin, 32sp, --warm-cream
    - Subtitle "Kachuful •  2-6 players" in DM Sans 400, 13sp, --muted-text
    - Small card suit decorations (static SVGs, 4 suits in a loose arc)
  
  Middle 40%: Actions
    - "Playing as: [username]" with pencil icon, DM Sans 500, 13sp, --muted-text
    - Create Room button (primary)
    - Join Room button (secondary)
    - Buttons stacked, full width, with 16px gap

  Bottom: AdMob banner (56px height container, --ink-black bg)
```

### 5.2 Waiting Room

```
Background: --earth-brown with grain texture

Top section:
  "ROOM CODE" label, --muted-text, 11sp, uppercase
  Room code display (component 4.6)
  Share icon button

Middle section (scrollable):
  "Players" heading, Playfair Display 700, 22sp, --warm-cream
  Player list cards:
    Each card: 56px height, --wood-dark bg, 10px radius
    Left: colored dot (green = connected), player name (DM Sans 500, 16sp)
    Right: "HOST" badge if host (--haldi-yellow pill)
    Animated: new players slide in from bottom

Bottom section:
  AdMob native/rectangle ad — embedded in a --wood-dark container with "Advertisement" label above in --muted-text 9sp
  Start Game button (primary, full width) — host only
  "Waiting for host..." text — non-host only
```

### 5.3 Game Table

```
Background: --felt-green with subtle diagonal weave texture

Zones (portrait layout):

ZONE A — Top bar (64px):
  Background: rgba(26,15,10,0.6)
  Scrollable row of opponent avatar tiles (component 4.3)
  Horizontally scrollable if 5+ players

ZONE B — Trump indicator strip (48px):
  Centered trump indicator pill (component 4.4)

ZONE C — Play area (fills remaining space):
  Background: --felt-mid with subtle texture
  Border radius: 16px inset
  Current trick cards arranged in a slight fan/spread
  Each card shows player name underneath it in --warm-cream 10sp

ZONE D — Hand area (200px):
  Background: rgba(26,15,10,0.7)
  Horizontally scrollable fan of cards
  Cards overlap: each card offset by 48px from previous
  Playable cards have full opacity; unplayable are dimmed
  
FAB — Score peek button:
  Bottom-right, 48px circle
  Background: --haldi-yellow
  Icon: grid/table icon
  Opens scoreboard as bottom sheet
```

### 5.4 Bidding Overlay

```
Background: --overlay-dark (covers game table)
Center modal: --wood-dark, 16px radius, 80% screen width

Title: "Place Your Bid" — Playfair Display 700, 22sp, --warm-cream
Subtext: "Round [N] • [M] cards dealt" — DM Sans 400, 13sp, --muted-text

Number selector:
  Row of number buttons (0 to M)
  Each: 44px × 44px, --earth-brown bg, --warm-cream text, 8px radius
  Selected: --haldi-yellow bg, --ink-black text
  Illegal bid: --sindoor-red border, strikethrough, tooltip on press: "This bid would make total equal cards dealt"

Confirm button: primary CTA, full width

Waiting state (other players):
  "[Username] is bidding..." — centered, DM Sans 400, --muted-text
  Small animated dots
```

---

## 6. Animation & Motion

Keep animations snappy. Nothing lingers. Respect that this is a game — motion should communicate state, not show off.

| Moment | Animation | Duration |
|---|---|---|
| Card dealt to hand | Slide in from top + slight rotation settle | 300ms, ease-out |
| Card played to table | Slide from hand position to center | 250ms, ease-in-out |
| Trick won (cards collected) | Cards slide to winner's avatar | 400ms, ease-in |
| Player turn indicator | Pulsing glow ring | Infinite, 1.2s cycle |
| New player joins lobby | Slide up from bottom | 200ms, ease-out |
| Score row reveal | Fade in row by row | 100ms stagger |
| Room code copy | Scale pulse on code | 150ms |
| Trump reveal on round start | Scale 1 → 1.2 → 1 with glow | 500ms |

No page transitions longer than 300ms. Use `go_router` with a simple fade transition.

---

## 7. Iconography

Use **Phosphor Icons** Flutter package — warm, rounded, varied weight options.

| Element | Icon |
|---|---|
| Create Room | `ph_plus_circle` |
| Join Room | `ph_arrow_square_in` |
| Share code | `ph_share_network` |
| Copy code | `ph_copy` |
| Edit username | `ph_pencil_simple` |
| Score peek | `ph_table` |
| Host badge | `ph_crown_simple` |
| Disconnected | `ph_wifi_slash` |

Suit icons: Custom SVG assets. Create 4 files: `spade.svg`, `club.svg`, `heart.svg`, `diamond.svg`. Keep them simple and slightly chunky — not thin-line fintech style.

---

## 8. Spacing & Grid

Base unit: **8px**

```
Screen horizontal padding: 20px
Section vertical gap: 24px
Component internal padding: 16px
Small gaps (labels to content): 8px
Button height: 56px
Bottom safe area: respect Android gesture bar (use SafeArea)
```

---

## 9. AdMob Integration Guidelines

**Rule: Ads should feel like they belong, not like intrusions.**

- Always wrap AdMob banner in a `--ink-black` or `--wood-dark` container with 1px border in `--wood-mid`
- Above native ads in waiting room: small "Advertisement" label in `--muted-text`, 9sp
- Never place an ad within scrollable game content
- Use adaptive banner width (fills screen width naturally)
- Test with test ad unit IDs during development; swap to real IDs only before release

---

## 10. Accessibility

- Minimum touch target: 44px × 44px (all interactive elements)
- Contrast: --warm-cream on --felt-green = 7.2:1 (passes AA)
- Contrast: --haldi-yellow on --earth-brown = 5.8:1 (passes AA)
- All suit icons have semantic labels (for screen readers)
- Room code input: `inputAction = done`, auto-focus on screen load
- Font scaling: use `sp` units throughout (Flutter default), cap scale factor at 1.3 to prevent layout breaks
