# Williams Blackout (game 495) - Switch matrix, switch chart and switch wiring

Sources:

- Instruction Booklet 16P-495-103, PDF page 11 / printed 11, Figure 5 Switch Matrix; PDF page 10 / printed 10, Figure 4 Playfield Switch Locations and Switch Chart.
- Instruction Manual and Drawing Set, PDF page 22, left half / printed 26, Playfield Switch Wiring Diagram; PDF page 21, left half / printed 24, Cabinet Wiring Diagram (column 1 and the cabinet switches).

## Figure 5. Switch Matrix (booklet, printed page 11)

Column headers (column number and wire): 1 GRN-BRN, 2 GRN-RED, 3 GRN-ORN, 4 GRN-YEL, 5 GRN-BLK, 6 GRN-BLU, 7 GRN-VIO, 8 GRN-GRY.
Row headers (row number and wire): 1 WHT-BRN, 2 WHT-RED, 3 WHT-ORN, 4 WHT-YEL, 5 WHT-GRN, 6 WHT-BLU, 7 WHT-VIO, 8 WHT-GRY.

Each cell prints its switch number and name; all 64 cells, column by column:

| Column | Row 1 | Row 2 | Row 3 | Row 4 | Row 5 | Row 6 | Row 7 | Row 8 |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 PLUMB BOB TILT | 2 BALL ROLL TILT | 3 CREDIT BUTTON | 4 RIGHT COIN SWITCH | 5 CENTER COIN SWITCH | 6 LEFT COIN SWITCH | 7 SLAM SWITCH | 8 HIGH SCORE RESET |
| 2 | 9 OUTHOLE | 10 LEFT OUTSIDE ROLLOVER | 11 GREEN TARGET #1 (BOTTOM) | 12 GREEN TARGET #2 | 13 GREEN TARGET #3 | 14 GREEN TARGET #4 | 15 5 BANK #5 (TOP) | 16 NOT USED |
| 3 | 17 NOT USED | 18 LEFT SPINNER | 19 LEFT SPINNER STANDUP | 20 UPPER LEFT TARGET | 21 RIGHT JET BUMPER | 22 LEFT JET BUMPER | 23 BOTTOM JET BUMPER | 24 NOT USED |
| 4 | 25 CENTER 3 BANK (LEFT) | 26 CENTER 3 BANK (CENTER) | 27 CENTER 3 BANK (RIGHT) | 28 CENTER 3 BANK SERIES | 29 1 ROLLOVER | 30 2 ROLLOVER | 31 3 ROLLOVER | 32 PLAYFIELD TILT |
| 5 | 33 TOP 3 BANK (LEFT) | 34 TOP 3 BANK (CENTER) | 35 TOP 3 BANK (RIGHT) | 36 TOP 3 BANK SERIES | 37 UPPER RIGHT SPINNER | 38 MIDDLE RIGHT STANDUP | 39 MIDDLE RIGHT SPINNER | 40 EJECT HOLE |
| 6 | 41 RIGHT OUTSIDE ROLLOVER | 42 RIGHT INSIDE ROLLOVER | 43 RIGHT KICKER 10 | 44 LEFT KICKER 10 | 45 LEFT INSIDE ROLLOVER | 46 RIGHT FLIPPER LANE CHANGE SWITCH | 47 NOT USED | 48 NOT USED |
| 7 | 49 NOT USED | 50 NOT USED | 51 NOT USED | 52 NOT USED | 53 NOT USED | 54 NOT USED | 55 NOT USED | 56 NOT USED |
| 8 | 57 NOT USED | 58 NOT USED | 59 NOT USED | 60 NOT USED | 61 NOT USED | 62 NOT USED | 63 NOT USED | 64 NOT USED |

Cell 15 prints `5 BANK #5 (TOP)`; the chart below and the wiring sheet's list call switch 15 a green target.

## Figure 4. Switch Chart (booklet, printed page 10)

`Switch No.` and `Function (Score)` as printed; the note reads `Note: Second value is lit or flashing value.`

| No. | Function (Score) |
|---|---|
| 01 | Plumb Bob Tilt |
| 02 | Ball Roll Tilt |
| 03 | Credit Button |
| 04 | Right Coin Switch |
| 05 | Center Coin Switch |
| 06 | Left Coin Switch |
| 07 | Slam Switch |
| 08 | High Score Reset |
| 09 | Outhole |
| 10 | Left Outside Rollover (2,000) |
| 11 | Green Target #1 Bottom (2,000/5,000) |
| 12 | Green Target #2 (2,000/5,000) |
| 13 | Green Target #3 (2,000/5,000) |
| 14 | Green Target #4 (2,000/5,000) |
| 15 | Green Target #5 Top (2,000/5,000) |
| 16 | Not Used |
| 17 | Not Used |
| 18 | Left Spinner (100) |
| 19 | Left Spinner Standup (50) |
| 20 | Upper Left Target (1,000) |
| 21 | Right Jet Bumper (100/1,000) |
| 22 | Left Jet Bumper (100/1,000) |
| 23 | Bottom Jet Bumper (100/1,000) |
| 24 | Not Used |
| 25 | Center 3 Bank Left (2,000/5,000) |
| 26 | Center 3 Bank Center (2,000/5,000) |
| 27 | Center 3 Bank Right (2,000/5,000) |
| 28 | Center 3 Bank Series (10,000) |
| 29 | 1 Rollover (1,000) |
| 30 | 2 Rollover (1,000) |
| 31 | 3 Rollover (1,000) |
| 32 | Playfield Tilt |
| 33 | Top 3 Bank Left (2,000/5,000) |
| 34 | Top 3 Bank Center (2,000/5,000) |
| 35 | Top 3 Bank Right (2,000/5,000) |
| 36 | Top 3 Bank Series (10,000) |
| 37 | Upper Right Spinner (100/1,000) |
| 38 | Middle Right Standup (50) |
| 39 | Middle Right Spinner (100/1,000) |
| 40 | Eject Hole (1,000 lit value) |
| 41 | Right Outside Rollover (2,000) |
| 42 | Right Inside Rollover (1,000/3,000) |
| 43 | Right Kicker (10) |
| 44 | Left Kicker (10) |
| 45 | Left Inside Rollover (1,000/3,000) |
| 46 | Right Flipper Lane Change Switch |

The location drawing beside the chart prints switch numbers on the playfield. 09 (outhole), 43 and 44 (kicker switches) and 46 (lane change) are drawn in dashed circles (the drawing does not say what the dashes mean); 32 is printed near the base of the right flipper.

## Playfield Switch Wiring Diagram (drawing set, printed page 26)

Columns, 2J2/2P2 to 8P1/8J1:

| Wire | 2P2 pin | 8P1 pin | Use |
|---|---|---|---|
| GRN-GRY | 1 | 7 | N/C |
| GRN-VIO | 2 | 6 | N/C |
| GRN-BLU | 3 | 5 | COLUMN 6 |
| GRN-BLK | 5 | 4 | COLUMN 5 |
| GRN-YEL | 6 | 3 | COLUMN 4 |
| GRN-ORG | 7 | 2 | COLUMN 3 |
| GRN-RED | 8 | 1 | COLUMN 2 |

Rows, 2J3/2P3 to 8P1:

| Wire | 2P3 pin | 8P1 pin | Use |
|---|---|---|---|
| WHT-BRN | 9 | 8 | ROW 1 |
| WHT-RED | 8 | 9 | ROW 2 |
| WHT-ORG | 7 | 10 | ROW 3 |
| WHT-YEL | 6 | 11 | ROW 4 |
| WHT-GRN | 5 | 12 | ROW 5 |
| WHT-BLU | 4 | 13 | ROW 6 |
| WHT-VIO | 3 | 14 | ROW 7 |
| WHT-GRY | 1 | 15 | ROW 8 |

Matrix drawing: each switch is drawn as an open contact in series with its diode 8Dn. Column 2 draws 8SW9 to 8SW15 (8SW15 in lighter print); column 3 draws 8SW18 to 8SW23; column 4 draws 8SW25 to 8SW32; column 5 draws 8SW33 to 8SW38 and 8SW40, with the row 7 position empty (no 8SW39 is drawn); column 6 draws 8SW41 to 8SW46. No 8SW16, 8SW17 or 8SW24 is drawn. The sheet's switch list runs 09 to 47 with the chart's names, 47 printed Not Used.

## Cabinet switches (drawing set, printed page 24)

Column 1: GRN-BRN from 2J2/2P2-9 to 7P1-19 and on to 7J2/7P2-6.

Rows: ROW 1 WHT-BRN 2P3-9 to 7P1-21; ROW 2 WHT-RED 2P3-8 to 7P1-22; ROW 3 WHT-ORN 2P3-7 to 7P1-23; ROW 4 WHT-YEL 2P3-6 to 7P1-24 (7P2-8); ROW 5 WHT-GRN 2P3-5 to 7P1-25 (7P2-9); ROW 6 WHT-BLU 2P3-4 to 7P1-26 (7P2-10); ROW 7 WHT-VIO 2P3-3 to 7P1-27 (7P2-11); ROW 8 WHT-GRY 2P3-1 to 7P1-28 (7P2-12).

| Switch | Diode | Connector |
|---|---|---|
| 7SW1 PLUMB BOB TILT | 7D1 | 7P1 |
| 7SW2 BALL ROLL TILT | 7D2 | 7P1 |
| 7SW3 CREDIT BUTTON | 7D3 | 7P1 |
| 7SW4 RIGHT COIN CHUTE | 7D4 | coin door, 7P2 |
| 7SW5 CENTER COIN CHUTE | 7D5 | coin door, 7P2 |
| 7SW6 LEFT COIN CHUTE | 7D6 | coin door, 7P2 |
| 7SW7 SLAM TILT | 7D7 | coin door, 7P2 |
| 7SW8 HIGH SCORE RESET | 7D8 | coin door, 7P2 |

Each is drawn as an open contact in series with its diode.
