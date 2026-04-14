# Card Sprite Pack

Source: imported from local sprite attachment on 2026-04-14.

Directory:
- `frontend/assets/cards/sprites`

Naming convention used by the pack:
- `Card Back 1.png`, `Card Back 2.png`, `Card Back 3.png`
- `<Suit> <N>.png` where `Suit` is `Spades`, `Hearts`, `Diamonds`, or `Clubs`
- `N` maps as: `1=A`, `11=J`, `12=Q`, `13=K`, others are numeric cards
- `Empty <N>.png` are blank placeholders with card frame only

Quick Flutter mapping tip:
- Build image paths using suit + numeric rank, for example:
  - `assets/cards/sprites/Spades 1.png` for Ace of Spades
  - `assets/cards/sprites/Hearts 12.png` for Queen of Hearts

Total files imported: 68 PNGs.