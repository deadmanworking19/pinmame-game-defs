# Williams Blackout (game 495) - Playfield lamp wiring

Source: Instruction Manual and Drawing Set (`Williams_1980_Blackout_Manual_with_paginated_schematics.pdf`), PDF page 22, right half / printed 27, Playfield Lamp Wiring Diagram.

## Column and row wiring

Columns, 2J5/2P5 to 8P2/8J2:

| Wire | 2P5 pin | 8P2 pin | Use |
|---|---|---|---|
| YEL-VIO | 1 | 9 | COLUMN 7 |
| YEL-BLU | 5 | 8 | COLUMN 6 |
| YEL-GRN | 3 | 7 | COLUMN 5 |
| YEL-BLK | 7 | 6 | COLUMN 4 |
| YEL-ORG | 6 | 5 | COLUMN 3 |
| YEL-RED | 9 | 4 | COLUMN 2 |
| YEL-BRN | 8 | 3 | COLUMN 1 |

Rows, 2J7/2P7 to 8P2:

| Wire | 2P7 pin | 8P2 pin | Use |
|---|---|---|---|
| RED-BRN | 1 | 11 | ROW 1 |
| RED-BLK | 2 | 12 | ROW 2 |
| RED-ORG | 3 | 13 | ROW 3 |
| RED-YEL | 4 | 14 | ROW 4 |
| RED-GRN | 5 | 15 | ROW 5 |
| RED-BLU | 6 | 16 | ROW 6 |
| RED-VIO | 9 | 17 | ROW 7 |
| RED-GRY | 8 | 18 | ROW 8 |

Column 8 (YEL-GRY) does not come to the playfield; it runs to the insert board (`insert-board.md`).

## Matrix drawing

Every playfield cell is drawn as one bulb 8Bn with its own diode 8D(64+n): 8B1/8D65 to 8B49/8D113 and 8B56/8D120. Columns 1-6 are fully drawn except the column 2, row 3 position, which is blank (no 8B11 and no 8D75). Column 7 draws only 8B49 (row 1) and 8B56 (row 8). No cell draws more than one bulb.

## Bulb list (printed beside the matrix)

| Bulb No. | Function |
|---|---|
| 01 | Same Player Shoots Again |
| 02 | 1,000 Bonus |
| 03 | 2,000 Bonus |
| 04 | 3,000 Bonus |
| 05 | 4,000 Bonus |
| 06 | 5,000 Bonus |
| 07 | 6,000 Bonus |
| 08 | 7,000 Bonus |
| 09 | 8,000 Bonus |
| 10 | 9,000 Bonus |
| 11 | Not Used |
| 12 | 10,000 Bonus |
| 13 | 2X |
| 14 | 3X |
| 15 | 4X |
| 16 | 5X |
| 17 | Green Target #1 Arrow (Bottom) |
| 18 | Green Target #2 Arrow |
| 19 | Green Target #3 Arrow |
| 20 | Green Target #4 Arrow |
| 21 | Green Target #5 Arrow (Top) |
| 22 | Center 3 Bank Arrow (Left) |
| 23 | Center 3 Bank Arrow (Center) |
| 24 | Center 3 Bank Arrow (Right) |
| 25 | Right Jet Bumper |
| 26 | Left Jet Bumper |
| 27 | Bottom Jet Bumper |
| 28 | "1" |
| 29 | "2" |
| 30 | "3" |
| 31 | Left Inside Rollover |
| 32 | Right Inside Rollover |
| 33 | Loop 5,000 |
| 34 | Loop 10,000 |
| 35 | Loop 15,000 |
| 36 | Loop 20,000 |
| 37 | Extra Ball When Lit |
| 38 | Top 3 Bank Arrow (Left) |
| 39 | Top 3 Bank Arrow (Center) |
| 40 | Top 3 Bank Arrow (Right) |
| 41 | Top Right Spinner |
| 42 | Middle Right Spinner |
| 43 | Eject Hole Green 5,000 |
| 44 | Eject Hole Amber 5,000 |
| 45 | Eject Hole Red 5,000 |
| 46 | Eject Hole BLACKOUT |
| 47 | Left Special |
| 48 | Right Special |
| 49 | 20,000 Bonus |
| 56 | Credits (Playfield) |

## General illumination

`6.3 V.A.C. GENERAL ILLUMINATION` from the FUSE CARD on YEL 8P2-1 and YEL-WHT 8P2-2: a parallel string drawn with four bulbs and a dashed continuation. No bulb count or bulb designators are printed for it.
