# Paragon - plug connectors (W-1187-11)

Source: `Bally_1979_Paragon_Schematic_Diagrams_paginated.pdf`, PDF page 5, a 5100 x 3295 scan at 300 dpi of the drawing titled "PLUG CONNECTORS", material "PARAGON", Bally game "#1167-E", part number W-1187-11. Read from the native render. Each block below is one connector list on the sheet; every printed row is kept, with the printed wire code (the two-digit number drawn on the wire, decoded by the sheet's own WIRE COLOR CODE: 1-red, 2-blue, 3-yellow, 4-green, 5-white, 6-brown, 7-orange, 8-black, 9-gray, 0-no trace). An empty wire cell means the sheet draws no wire code on that pin. Quotation marks, abbreviations and spacing are the page's own; circled spinner numbers are written `(1)` to `(4)`.

Notes printed on the sheet: "1. THESE PINS ARE RESERVED FOR FUTURE USE." "2. WIRE COLORS ARE SHOWN FOR ALL CONNECTOR PINS, SOME WIRES MAY NOT BE USED IN ALL GAMES." "3 * INDICATES AID TEST POINT."

## LAMP DRIVER A5 - J1

| pin | wire | to |
| --- | --- | --- |
| 1 | 41 | 2K BONUS |
| 2 | 43 | WATER LANE SPEC. |
| 3 | 45 | 10K DROP TARGET |
| 4 | 35 | N/U |
| 5 | 48 | CENTER "A" (LEFT) |
| 6 | 25 | SAUCER "O" |
| 7 | 34 | SAUCER "A" (LEFT) |
| 8 | 51 | 10K BONUS |
| 9 | 52 | 6K BONUS |
| 10 | 32 | 3X BONUS |
| 11 | 65 | CENTER "O" |
| 12 | 61 | 4K GOLDEN CLIFF |
| 13 | 96 | SAUCER "N" |
| 14 | 54 | 25 K DROP TARGET |
| 15 | 13 | 2X BONUS |
| 16 | 12 | SAUCER "P" |
| 17 | 57 | 9K BONUS |
| 18 | 58 | 1K BONUS |
| 19 | 60 | 5K BONUS |
| 20 | | KEY |
| 21 | | N/U |
| 22 | | N/U |
| 23 | 56 | 40 K SUPER BONUS |
| 24 | 50 | CENTER "P" |
| 25 | 90 | CENTER "G" |
| 26 | 91 | N/U |
| 27 | 53 | 2K GOLDEN CLIFF |
| 28 | 78 | SAUCER "G" |

## LAMP DRIVER A5 - J2

| pin | wire | to |
| --- | --- | --- |
| 1 | 60 | 20K GOLDEN CLIFF |
| 2 | 20 | 10K GOLDEN CLIFF |
| 3 | 84 | N/U |
| 4 | 72 | N/U |
| 5 | | N/U |
| 6 | 85 | SPINNER (3) |
| 7 | 91 | SPINNER (4) TOP |
| 8 | 93 | MATCH |
| 9 | | N/U |
| 10 | 98 | TILT |
| 11 | 95 | GAME OVER |
| 12 | 61 | N/U |
| 13 | 53 | N/U |
| 14 | 12 | 10 K WATER LANE |
| 15 | 32 | 5 K WATER LANE |
| 16 | 34 | SPINNER (1) BOTTOM |
| 17 | | N/U |
| 18 | | KEY |
| 19 | | N/U |
| 20 | 35 | SPINNER (2) |
| 21 | 47 | SHOOT AGAIN |
| 22 | 62 | BALL IN PLAY |
| 23 | 97 | HIGH SCORE TO DATE |

## LAMP DRIVER A5 - J3

| pin | wire | to |
| --- | --- | --- |
| 1 | 10 | 4K BONUS |
| 2 | 95 | SPECIAL TREASURE SAUCER |
| 3 | 81 | E.B. TREAS. SAUCER |
| 4 | 14 | SAUCER "A" (RIGHT) |
| 5 | | N/U |
| 6 | | N/U |
| 7 | | N/U |
| 8 | | KEY |
| 9 | 15 | 5X TREAS. SAUCER |
| 10 | 91 | CENTER "A" (RIGHT) |
| 11 | 20 | 20K DROP TARGET |
| 12 | 21 | 8K BONUS |
| 13 | 13 | CREDIT INDICATOR |
| 14 | 84 | 8K GOLDEN CLIFF |
| 15 | 53 | 30 K SUPER BONUS |
| 16 | 25 | PARAGON SAUCER SPECIAL |
| 17 | 27 | 15 K DROP TARGET |
| 18 | 56 | SPEC. DROP TARGET |
| 19 | 67 | 20 K SUPER BONUS |
| 20 | 64 | CENTER "N" |
| 21 | 30 | CENTER "R" |
| 22 | 23 | SAME PLAYER S.A. |
| 23 | 98 | 5X BONUS |
| 24 | 72 | 6K GOLDEN CLIFF |
| 25 | 36 | 7K BONUS |
| 26 | 38 | 3K BONUS |
| 27 | 40 | SAUCER "R" |
| 28 | | N/U |

The function names agree with the A5 lamp driver schematic (W-1182-15) pin for pin; the J1, J2 and J3 lists here are in pin order, the schematic's in trace order.

## A1 INSERT - lamp lines from A5 J2

Printed beside the insert's switched-illumination bus (5.4 V.D.C.), one socket symbol per line:

| wire | from | label |
| --- | --- | --- |
| 12 | A5J2-14 | |
| 32 | A5J2-15 | |
| 20 | A5J2-2 | |
| 60 | A5J2-1 | |
| 47 | A5J2-21 | SHOOT AGAIN |
| 95 | A5J2-11 | GAME OVER |
| 98 | A5J2-10 | TILT |
| 34 | A5J2-16 | |
| 35 | A5J2-20 | |
| 85 | A5J2-6 | |
| 91 | A5J2-7 | |
| 97 | A5J2-23 | HIGH SCORE |
| 93 | A5J2-8 | MATCH |
| 62 | A5J2-22 | BALL IN PLAY |
| 84 | A5J2-3 | |
| 72 | A5J2-4 | |
| | A5J2-5 | NOTE 1 |
| | A5J2-9 | NOTE 1 |
| 61 | A5J2-12 | |
| 53 | A5J2-13 | |

The insert drawing puts a socket symbol on every line, including the N/U and NOTE 1 lines, so it is a generic drawing of the insert board; only the six lines it labels are named back box lamps.

## TABLE A - A1J2, INSERT TO BACK CAB. PLUG

| FROM | PIN | WIRE |
| --- | --- | --- |
| A2J3-6 | 1 | 20 |
| A5J2-14 | 2 | 12 |
| A2J3-2 | 3 | 50 |
| A2J3-11 | 4 | 10 |
| A5J2-23 | 5 | 97 |
| A5J2-15 | 6 | 32 |
| A5J2-22 | 7 | 62 |
| A5J2-8 | 8 | 93 |
| A5J2-1 | 9 | 60 |
| A5J2-2 | 10 | 20 |
| A5J2-11 | 11 | 95 |
| A5J2-21 | 12 | 47 |
| A5J2-10 | 13 | 98 |
| A5J2-7 | 14 | 91 |
| A5J2-6 | 15 | 85 |
| A5J2-20 | 16 | 35 |
| A5J2-16 | 17 | 34 |
| A2J3-1 | 18 | 40 |
| A2J3-10 | 19 | 70 |
| A5J2-13 | 20 | 53 |
| A5J2-12 | 21 | 61 |
| A5J2-4 | 22 | 72 |
| A5J2-3 | 23 | 84 |
| | 24 | |

The pin-5 source is printed "A5J2-2-3" with the middle digit struck through; it reads A5J2-23 (wire 97, HIGH SCORE TO DATE).

## TABLE "B" - PANEL TO BACK CAB. PLUG

| FROM | TO | WIRE |
| --- | --- | --- |
| A5J2-14 | 1 | 12 |
| A5J2-2 | 2 | 20 |
| A5J2-15 | 3 | 32 |
| A5J2-16 | 4 | 34 |
| A5J2-20 | 5 | 35 |
| A5J2-1 | 6 | 60 |
| A5J2-6 | 7 | 85 |
| A5J2-7 | 8 | 91 |

An arrow beside the A5 block reads "SEE TABLE "B" — TO PLAY FIELD (W-1192-11)".

## VOLTAGE REGULATOR / SOLENOID DRIVER A3 - load connectors

J1:

| pin | wire | to |
| --- | --- | --- |
| 1 | | N/U |
| 2 | 67 | DR. TAR. (IN LINE) |
| 3 | 81 | LT. BOT. T.B. |
| 4 | | N/U |
| 5 | 95 | OUTHOLE |
| 6 | | N/U |
| 7 | | KEY |
| 8 | 40 | L. FLIP COIL |
| 9 | 70 | R. FLIP COIL |

J2:

| pin | wire | to |
| --- | --- | --- |
| 1 | 10 | R. FLIP SW. |
| 2 | 20 | L. FLIP SW. |
| 3 | | KEY |
| 4 | | N/U |
| 5 | 85 | KNOCKER |
| 6 | | NOTE 1. |
| 7 | 31 | TEST SW. RET. |
| 8 | 36 | COIN LOCKOUT |
| 9 | 58 | N/U |
| 10 | 57 | N/U |
| 11 | 56 | N/U |
| 12 | 54 | N/U |
| 13 | | |
| 14 | | |
| 15 | | |

J5:

| pin | wire | to |
| --- | --- | --- |
| 1 | | N/U |
| 2 | | N/U |
| 3 | | N/U |
| 4 | | N/U |
| 5 | | N/U |
| 6 | | KEY |
| 7 | 81 | DROP TARGET (3) |
| 8 | 18 | RIGHT SLINGSHOT |
| 9 | 71 | LEFT THUMPER BUMPER |
| 10 | 74 | TREASURE CHAMBER SAUCER |
| 11 | 78 | PARAGON SAUCER |
| 12 | 75 | GOLDEN CLIFFS SAUCER |
| 13 | 80 | CENTER THUMPER BUMPER |
| 14 | 83 | LEFT SLINGSHOT |
| 15 | 85 | RIGHT THUMPER BUMPER |

The A3 J3 and J4 blocks on the same sheet are board-to-board interconnects (to A2, A4, A5 and A1) and are not transcribed here.

## MPU A4 - switch matrix connectors

J2:

| pin | wire | to |
| --- | --- | --- |
| 1 | 51 | ST 0 |
| 2 | | ST 1 |
| 3 | 52 | ST 2 |
| 4 | 53 | ST 3 |
| 5 | 31 | ST 4 |
| 6 | | KEY |
| 7 | | N/U |
| 8 | 54 | I 0 |
| 9 | 56 | I 1 |
| 10 | 57 | I 2 |
| 11 | 58 | I 3 |
| 12 | 60 | I 4 |
| 13 | 63 | I 5 |
| 14 | 65 | I 6 |
| 15 | 70 | I 7 |

Pins 1-5 are bracketed "PLAY-FIELD SW STROBE" and pins 8-15 "PLAY-FIELD SW RETURN".

J3:

| pin | wire | to |
| --- | --- | --- |
| 1 | 10 | SELF TEST SW. |
| 2 | 13 | ST 0 |
| 3 | 14 | ST 1 |
| 4 | | KEY |
| 5 | | N/U |
| 6 | | N/U |
| 7 | | N/U |
| 8 | | N/U |
| 9 | 15 | I 0 |
| 10 | 65 | I 1 |
| 11 | 20 | I 2 |
| 12 | 21 | I 3 |
| 13 | 23 | I 4 |
| 14 | 25 | I 5 |
| 15 | 27 | I 6 |
| 16 | 30 | I 7 |

Pins 2-3 are bracketed "SW. CAB. STROBE" and pins 9-16 "CAB. SW. RET.".

Column 2 of the matrix (public switches 9-16) has no wire code on its playfield strobe A4J2-2: every switch the manual lists in that column (coins 9, 10 and 11, and slam 16) is a cabinet or door switch on the A4J3 strobe.
