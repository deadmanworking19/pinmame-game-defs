# Williams Blackout (game 495) - Lamp matrix

Source: Instruction Booklet 16P-495-103 (`Williams_1980_Blackout_Operators_Handbook.pdf`), PDF page 12 / printed 12, Figure 6 Lamp Matrix.

Column headers (column number and wire): 1 YEL-BRN, 2 YEL-RED, 3 YEL-ORN, 4 YEL-BLK, 5 YEL-GRN, 6 YEL-BLU, 7 YEL-VIO, 8 YEL-GRY.
Row headers (row number and wire): 1 RED-BRN, 2 RED-BLK, 3 RED-ORN, 4 RED-YEL, 5 RED-GRN, 6 RED-BLU, 7 RED-VIO, 8 RED-GRY.

Each cell prints its lamp number and name; all 64 cells, column by column:

| Column | Row 1 | Row 2 | Row 3 | Row 4 | Row 5 | Row 6 | Row 7 | Row 8 |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 SAME PLAYER SHOOTS AGAIN (PLAYFIELD) | 2 1,000 BONUS | 3 2,000 BONUS | 4 3,000 BONUS | 5 4,000 BONUS | 6 5,000 BONUS | 7 6,000 BONUS | 8 7,000 BONUS |
| 2 | 9 8,000 BONUS | 10 9,000 BONUS | 11 NOT USED | 12 10,000 BONUS | 13 2X | 14 3X | 15 4X | 16 5X |
| 3 | 17 GREEN TARGET #1 ARROW (BOTTOM) | 18 GREEN TARGET #2 ARROW | 19 GREEN TARGET #3 ARROW | 20 GREEN TARGET #4 ARROW | 21 GREEN TARGET #5 ARROW (TOP) | 22 CENTER 3 BANK ARROW (LEFT) | 23 CENTER 3 BANK ARROW | 24 CENTER 3 BANK ARROW |
| 4 | 25 RIGHT JET BUMPER | 26 LEFT JET BUMPER | 27 BOTTOM JET BUMPER | 28 "1" | 29 "2" | 30 "3" | 31 LEFT INSIDE ROLLOVER (CENTER) | 32 RIGHT INSIDE ROLLOVER (RIGHT) |
| 5 | 33 LOOP 5,000 | 34 LOOP 10,000 | 35 LOOP 15,000 | 36 LOOP 20,000 | 37 EXTRA BALL WHEN LIT | 38 TOP 3 BANK ARROW (LEFT) | 39 TOP 3 BANK ARROW (CENTER) | 40 TOP 3 BANK ARROW (RIGHT) |
| 6 | 41 TOP RIGHT SPINNER | 42 MIDDLE RIGHT SPINNER | 43 EJECT HOLE GREEN 5,000 | 44 EJECT HOLE YELLOW 5,000 | 45 EJECT HOLE RED 5,000 | 46 EJECT HOLE BLACKOUT | 47 LEFT SPECIAL | 48 RIGHT SPECIAL |
| 7 | 49 20,000 BONUS | 50 1 CAN PLAY | 51 2 CAN PLAY | 52 3 CAN PLAY | 53 4 CAN PLAY | 54 MATCH | 55 BALL IN PLAY | 56 CREDITS (PLAYFIELD) |
| 8 | 57 #1 PLAYER UP | 58 #2 PLAYER UP | 59 #3 PLAYER UP | 60 #4 PLAYER UP | 61 TILT | 62 GAME OVER | 63 SAME PLAYER SHOOTS (BACKBOX) | 64 HIGH SCORE TO DATE |

Cells 23 and 24 print no position qualifier, and cells 31 and 32 carry `(CENTER)` and `(RIGHT)`. The drawing set's bulb list gives the qualifiers to 23 and 24 instead: `Center 3 Bank Arrow (Center)` and `Center 3 Bank Arrow (Right)`, with 31 and 32 plain `Left Inside Rollover` and `Right Inside Rollover` (see `lamp-wiring.md`). Cell 44 prints `YELLOW`; the bulb list prints `Amber`.
