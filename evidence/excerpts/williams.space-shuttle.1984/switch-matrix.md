# Literal transcription — System 9 Switch-Matrix Table

`reviewed: true`; transcribed by the curator from a 300 dpi render and visually checked against it on 2026-10-30
`source: Instruction Manual PDF page 16 (the switch matrix, lower half of the page)`

Retained render: `external:pinmame-manuals/by-machine/williams.space-shuttle.1984/rendered-300/p-16.png` (pdftoppm 23.05.0 -r 300 -gray).

Literal heading: `System 9 Switch-Matrix Table`. Each cell is `printed name — printed number`. Line breaks
inside a cell are joined with a space; hyphenated breaks (`Plumb-` / `Tilt`) keep the printed hyphen. No
driver-transistor column is printed. Column 6's connector is printed `1J8-7`: pin 6 of 1J8 is the key.
The row connectors are printed `1J10-1`, `-3`, `-4`, `-5`, `-6`, `-7`, `-8`, `-9` for rows 1-8; the CPU
schematic and the backbox wiring diagram (excerpt `cpu-connectors`) wire row 1 to 1J10-9 down to row 8 on
1J10-1, with 1J10-4 the key. The printed cells are kept here as printed.

| row / wire / printed connection | 1 — GRN-BRN / 1J8-1 | 2 — GRN-RED / 1J8-2 | 3 — GRN-ORN / 1J8-3 | 4 — GRN-YEL / 1J8-4 | 5 — GRN-BLK / 1J8-5 | 6 — GRN-BLU / 1J8-7 | 7 — GRN-VIO / 1J8-8 | 8 — GRN-GRY / 1J8-9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 — WHT-BRN / 1J10-1 | Plumb-Tilt — 1 | Outhole — 9 | S Target — 17 | Left Jet — 25 | Left Drop-Tgt — 33 | Flipper (Lane Chg) — 41 | Play-Field Tilt — 49 | Not Used — 57 |
| 2 — WHT-RED / 1J10-3 | Ball-Roll Tilt — 2 | Top Ball Ramp — 10 | H Target — 18 | Right Jet — 26 | Center Drop-Tgt — 34 | Bot-L Standup Sw — 42 | Not Used — 50 | Not Used — 58 |
| 3 — WHT-ORN / 1J10-4 | Credit Button — 3 | Middle Ball Ramp — 11 | U Target — 19 | Lower Jet — 27 | Right Drop-Tgt — 35 | Mid-L Lwr S/U Sw — 43 | Not Used — 51 | Not Used — 59 |
| 4 — WHT-YEL / 1J10-5 | Right Coin — 4 | Lower Ball Ramp — 12 | T Drop Tgt — 20 | Left Outlane — 28 | Ball-Shooter Lane — 36 | Mid-L Upr S/U Sw — 44 | Not Used — 52 | Not Used — 60 |
| 5 — WHT-GRN / 1J10-6 | Center Coin — 5 | Right Outlane — 13 | T Target — 21 | U Lane — 29 | Spinner — 37 | Ramp (Lower Sw) — 45 | Not Used — 53 | Not Used — 61 |
| 6 — WHT-BLU / 1J10-7 | Left Coin — 6 | Left Flipper Ret — 14 | L Target — 22 | S Lane — 30 | Ramp Bull's-eye — 38 | Center Standup Sw — 46 | Not Used — 54 | Not Used — 62 |
| 7 — WHT-VIO / 1J10-8 | Slam Tilt — 7 | Right Flipper Ret — 15 | E Target — 23 | A Lane — 31 | Left Kicker — 39 | Upr-R Standup Sw — 47 | Not Used — 55 | Not Used — 63 |
| 8 — WHT-GRY / 1J10-9 | High-Score Reset — 8 | Left Eject-Hole — 16 | Right Eject Hole — 24 | Ramp (Upper SW) — 32 | Right Kicker — 40 | Lwr-R Standup Switch — 48 | Not Used — 56 | Not Used — 64 |

Uncertainty: the matrix is a wiring and name table. It does not print contact construction, polarity or
location. `Top`, `Middle` and `Lower Ball Ramp` are the three ball-trough positions and the `Kicker` cells are the
slingshot kicker switches; those readings come from the switch-location drawing and the retained script, not
from this table.
