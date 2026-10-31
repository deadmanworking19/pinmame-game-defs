# Williams Barracora (game 510) - Insert Board Wiring Diagram

Source: `Williams_1981_Barracora_Instruction_and_Drawing_Set_paginated_schematics_cover_page_missing.pdf`, PDF page 14 = printed page `19`, title `Insert Board Wiring Diagram`, game number `510` printed at the top.

Method: the page's native image (2552 x 1651) was rotated upright and read visually; the lamp section was cropped and rotated to read its sideways labels. Capitals and spelling are as printed, including `REN-GRN`.

## Lamp section (connector 9P1)

| 9P1 pin | Printed pin label | Wire | Diode | Bulb | Printed label |
|---|---|---|---|---|---|
| 1 | 6.3 VAC | BRN | (none) | GI | (none) |
| 3 | 6.3 VAC | GRN | (none) | GI | (none) |
| 2 | 6.3 VAC | WHT-BRN | (none) | GI | (none) |
| 4 | 6.3 VAC | WHT-BRN | (none) | GI | (none) |
| 13 | COL. 1 | YEL-BRN | (none) | (common to all six rows below) | (none) |
| 5 | ROW 1 | RED-BRN | 9D1 | 9B1 (two bulbs drawn in parallel) | SHOOT AGAIN |
| 6 | ROW 2 | RED-BLK | 9D2 | 9B2 | BALL IN PLAY |
| 7 | ROW 3 | RED-ORN | 9D3 | 9B3 | TILT |
| 8 | ROW 4 | RED-YEL | 9D4 | 9B4 | GAME OVER |
| 9 | ROW 5 | REN-GRN | 9D5 | 9B5 | MATCH |
| 10 | ROW 6 | RED-BLU | 9D6 | 9B6 | HIGH SCORE |

- The `6.3 VAC` bracket spans pins 1, 3, 2 and 4. BRN (1) and GRN (3) are joined, and the two WHT-BRN wires (2, 4) are joined. Five general-illumination bulbs are drawn between the two joined lines: three on solid connections and two on dashed ones. No bulb count is printed.
- Each lamp row runs from its 9P1 pin through its diode and bulb to the common `COL. 1` line on pin 13.

## Display section (same page)

- `PLAYERS #1 & #3` and `PLAYERS #2 & #4` seven-digit display boards on 5J1/5J3 and 5J2/5J4, strobes 2-8 and 10-16, with pin lists `4J1/5J1 (PLAYER 1)`, `4J3/5J3 (PLAYER 3)`, `4J2/5J2 (PLAYER 2)` and `4J4/5J4 (PLAYER 4)`.
- `CREDITS / BALL IN PLAY` board on 5J5, two digit pairs on strobes 1 and 9, with the pin list `4J8/5J5 (CREDIT/MATCH)` grouping its segments under `Credit` and `Match`.
- `MASTER DISPLAY` with connectors 4J1-4J4 (PLAYER 1-4), 4J8 (CREDIT/MATCH), 4J5 (STROBE INPUTS), 4J6 (POWER INPUTS) and 4J7 (BCD INPUTS).

## Notes

- `REN-GRN` on row 5 is printed so; the lamp matrix and the playfield lamp wiring give row 5 as RED-GRN.
- These six circuits are column 1, rows 1-6 of the lamp matrix, which are public lamps 1-6. The playfield lamp wiring (`lamp-wiring.md`) marks the same six cells BACKBOX and refers to this sheet for their connections.
