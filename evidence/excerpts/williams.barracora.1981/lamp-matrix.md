# Williams Barracora (game 510) - Lamp Matrix

Source: `Williams_1981_Barracora_Operators_Handbook.pdf` (IPDB 177, instruction booklet 16P-510-103), PDF page 9 = printed page `9`, caption `Figure 1. Lamp Matrix`.

- Printed sideways. Read from the page's native 300 dpi image (1760 x 2663, 1 bit), rotated 270 degrees (`Image.rotate(-90, expand=True)`) and checked upright, in two overlapping halves at native resolution.
- Normalization: none. Capitals as printed; a line break inside a cell is shown as ` / `. The quotation marks around the top-lane numbers `"1"` to `"6"` are printed.
- The cells carry **no lamp numbers**. The public lamp number in the last column of each table below is not printed; it is PinMAME's sequential System 7 numbering `(column - 1) * 8 + row`, added by the curator.
- Every one of the 64 cells is filled; no cell is blank or marked NOT USED.

## Column headers (as printed: column number, wire colour, 2J5 pin)

| Column | Wire colour | Connector pin |
|---|---|---|
| 1 | YEL-BRN | 2J5-8 |
| 2 | YEL-RED | 2J5-9 |
| 3 | YEL-ORN | 2J5-6 |
| 4 | YEL-BLK | 2J5-7 |
| 5 | YEL-GRN | 2J5-3 |
| 6 | YEL-BLU | 2J5-5 |
| 7 | YEL-VIO | 2J5-1 |
| 8 | YEL-GRY | 2J5-2 |

## Row headers (as printed; the wire colour is printed `RED-` / colour on two lines)

| Row | Wire colour | Connector pin |
|---|---|---|
| 1 | RED-BRN | 2J7-1 |
| 2 | RED-BLK | 2J7-2 |
| 3 | RED-ORN | 2J7-3 |
| 4 | RED-YEL | 2J7-4 |
| 5 | RED-GRN | 2J7-5 |
| 6 | RED-BLU | 2J7-6 |
| 7 | RED-VIO | 2J7-9 |
| 8 | RED-GRY | 2J7-8 |

Row 7 is printed on pin 2J7-9 and row 8 on 2J7-8, in that order. Pin 2J7-7 is not printed.

## Cells (64 of 64)

### Column 1 (YEL-BRN, 2J5-8)

| Row | Printed cell | Public lamp |
|---|---|---|
| 1 | SAME PLAYER / SHOOTS AGAIN / (BACKBOX) | 1 |
| 2 | BALL IN / PLAY | 2 |
| 3 | TILT | 3 |
| 4 | GAME / OVER | 4 |
| 5 | MATCH | 5 |
| 6 | HIGH / SCORE / TO DATE | 6 |
| 7 | B-A-RR / DROP TARGET / BANK | 7 |
| 8 | A-C-O-R-A / DROP TARGET / BANK | 8 |

### Column 2 (YEL-RED, 2J5-9)

| Row | Printed cell | Public lamp |
|---|---|---|
| 1 | B | 9 |
| 2 | A | 10 |
| 3 | RR | 11 |
| 4 | A | 12 |
| 5 | C | 13 |
| 6 | O | 14 |
| 7 | R | 15 |
| 8 | A | 16 |

### Column 3 (YEL-ORN, 2J5-6)

| Row | Printed cell | Public lamp |
|---|---|---|
| 1 | "1" | 17 |
| 2 | "2" | 18 |
| 3 | "3" | 19 |
| 4 | "4" | 20 |
| 5 | "5" | 21 |
| 6 | "6" | 22 |
| 7 | LEFT / SPECIAL | 23 |
| 8 | RIGHT / SPECIAL | 24 |

### Column 4 (YEL-BLK, 2J5-7)

| Row | Printed cell | Public lamp |
|---|---|---|
| 1 | SPINNER / (X 1000 W/LIT) | 25 |
| 2 | SHOOT AGAIN / (PLAYFIELD) | 26 |
| 3 | LOWER / EJECT HOLE / 30 | 27 |
| 4 | LOWER / EJECT HOLE / 60 | 28 |
| 5 | LOWER / EJECT HOLE / 90 | 29 |
| 6 | LOWER / EJECT HOLE / LOCK ARROW | 30 |
| 7 | UPPER / EJECT HOLE / LOCK ARROW | 31 |
| 8 | UPPER / EJECT HOLE / COLLECT BONUS | 32 |

### Column 5 (YEL-GRN, 2J5-3)

| Row | Printed cell | Public lamp |
|---|---|---|
| 1 | UPPER RIGHT / BULL'S-EYE / TARGET 20,000 | 33 |
| 2 | UPPER RIGHT / BULL'S-EYE / TARGET 40,000 | 34 |
| 3 | UPPER RIGHT / BULL'S-EYE / TARGET EXTRA / BALL W/LIT | 35 |
| 4 | LEFT / BULL'S-EYE / TARGET 5,000 | 36 |
| 5 | LEFT / BULL'S-EYE / TARGET 10,000 | 37 |
| 6 | LEFT / BULL'S-EYE / TARGET 15,000 | 38 |
| 7 | LEFT / BULL'S-EYE / TARGET 20,000 | 39 |
| 8 | LEFT / BULL'S-EYE / TARGET 25,000 | 40 |

### Column 6 (YEL-BLU, 2J5-5)

| Row | Printed cell | Public lamp |
|---|---|---|
| 1 | RIGHT / BULL'S-EYE / TARGET 2X | 41 |
| 2 | RIGHT / BULL'S-EYE / TARGET 3X | 42 |
| 3 | RIGHT / BULL'S-EYE / TARGET 4X | 43 |
| 4 | RIGHT / BULL'S-EYE / TARGET 5X | 44 |
| 5 | RIGHT / BULL'S-EYE / TARGET 10X | 45 |
| 6 | SUPER / 2X BONUS / MULTIPLIER | 46 |
| 7 | SUPER / 3X BONUS / MULTIPLIER | 47 |
| 8 | SUPER / 4X BONUS / MULTIPLIER | 48 |

### Column 7 (YEL-VIO, 2J5-1)

| Row | Printed cell | Public lamp |
|---|---|---|
| 1 | SUPER / 5X BONUS / MULTIPLIER | 49 |
| 2 | 2X BONUS / MULTIPLIER | 50 |
| 3 | 3X BONUS / MULTIPLIER | 51 |
| 4 | 4X BONUS / MULTIPLIER | 52 |
| 5 | 5X BONUS / MULTIPLIER | 53 |
| 6 | BONUS 1 | 54 |
| 7 | BONUS 2 | 55 |
| 8 | BONUS 3 | 56 |

### Column 8 (YEL-GRY, 2J5-2)

| Row | Printed cell | Public lamp |
|---|---|---|
| 1 | BONUS 4 | 57 |
| 2 | BONUS 5 | 58 |
| 3 | BONUS 6 | 59 |
| 4 | BONUS 7 | 60 |
| 5 | BONUS 8 | 61 |
| 6 | BONUS 9 | 62 |
| 7 | BONUS 10 | 63 |
| 8 | BONUS 20 | 64 |

## Notes

- The matrix does not say which lamps are in the backbox. Only lamp 1 carries `(BACKBOX)` in its cell and lamp 26 `(PLAYFIELD)`. The insert-board wiring (`insert-board.md`) and the playfield lamp wiring (`lamp-wiring.md`) settle the location of column 1.
