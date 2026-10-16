# Paragon - A5 lamp driver schematic (W-1182-15), connector functions

Source: `Bally_1979_Paragon_Schematic_Diagrams_paginated.pdf`, PDF page 3, a 5100 x 3295 scan at 300 dpi of the drawing titled "A5 LAMP DRIVER SCHEMATIC", material "PARAGON", Bally game "#1167-E", part number W-1182-15. The crop beside this file is the SCR column and the three output connectors. Read from the native render; the connector pin numbers and the function printed against each are transcribed in the order the page prints them, top to bottom, which is the order of the SCR traces that reach them. "N/U" and "KEY" are the page's own. The circled spinner numbers are written here as `(1)` to `(4)`.

The left half of the sheet (not cropped) draws the four MC14514CP binary-to-one-of-sixteen decoders U1-U4 (E-620-37), each enabled by one lamp-data line (U1 PD0 ... U4 PD3), all four addressed by AD0-AD3 from J4 (lamp address J4-14 to J4-17, lamp data J4-4 to J4-7, STROBE 1 on J4-13), and a column of sixty SCRs. Notes on the sheet: "1. * SCRs ARE MCR 106-1 (E-585-29), ALL OTHERS ARE 2N5060 (E-585-14) OR EQUIVALENTS." "2. ALL RESISTORS ARE 1/4W, ±5%." "3. PREFIX ALL REFERENCE DESIGNATIONS WITH "A5"." "4. * INDICATES 'AID' TEST POINT".

## J1 - "TO PLAYFIELD"

| pin | function |
| --- | --- |
| 22 | N/U |
| 21 | N/U |
| 20 | KEY |
| 18 | 1K BONUS |
| 19 | 5K BONUS |
| 17 | 9K BONUS |
| 23 | 40 K SUPER BONUS |
| 14 | 25 K DROP TARGET |
| 15 | 2X BONUS |
| 16 | SAUCER "P" |
| 28 | SAUCER "G" |
| 24 | CENTER "P" |
| 25 | CENTER "G" |
| 26 | N/U |
| 27 | 2K GOLDEN CLIFF |
| 1 | 2K BONUS |
| 9 | 6K BONUS |
| 8 | 10K BONUS |
| 3 | 10K DROP TARGET |
| 2 | WATER LANE SPECIAL |
| 10 | 3X BONUS |
| 7 | SAUCER "A" (LEFT) |
| 6 | SAUCER "O" |
| 5 | CENTER "A" (LEFT) |
| 11 | CENTER "O" |
| 13 | SAUCER "N" |
| 4 | N/U |
| 12 | 4K GOLDEN CLIFF |

## J2 - "TO BACKBOX"

| pin | function |
| --- | --- |
| 21 | SHOOT AGAIN |
| 13 | N/U |
| 22 | BALL IN PLAY |
| 16 | SPINNER (1) BOTTOM |
| 14 | 10 K WATERLANE |
| 8 | MATCH |
| 12 | N/U |
| 23 | HIGH SCORE TO DATE |
| 20 | SPINNER (2) |
| 15 | 5 K WATERLANE |
| 11 | GAME OVER |
| 6 | SPINNER (3) |
| 2 | 10 K GOLDEN CLIFF |
| 9 | N/U |
| 4 | N/U |
| 5 | N/U |
| 3 | N/U |
| 10 | TILT |
| 7 | SPINNER (4) (TOP) |
| 1 | 20 K GOLDEN CLIFF |
| 17 | N/U |
| 18 | KEY |
| 19 | N/U |

## J3 - "TO PLAYFIELD"

| pin | function |
| --- | --- |
| 26 | 3K BONUS |
| 25 | 7K BONUS |
| 19 | 20 K SUPER BONUS |
| 17 | 15 K DROP TARGET |
| 16 | PARAGON SAUCER SPECIAL |
| 23 | 5X BONUS |
| 27 | SAUCER "R" |
| 21 | CENTER "R" |
| 20 | CENTER "N" |
| 22 | SAME PLAYER S.A. |
| 24 | 6 K GOLDEN CLIFF |
| 1 | 4K BONUS |
| 12 | 8K BONUS |
| 15 | 30 K SUPER BONUS |
| 11 | 20 K DROP TARGET |
| 9 | 5X TREASURE SAUCER |
| 3 | EXTRA BALL TREASURE SAUCER |
| 4 | SAUCER "A" (RIGHT) |
| 2 | SPECIAL TREASURE SAUCER |
| 10 | CENTER "A" RIGHT |
| 18 | SPECIAL DROP TARGET |
| 13 | CREDIT INDICATOR |
| 14 | 8 K GOLDEN CLIFF |
| 5 | N/U |
| 6 | N/U |
| 7 | N/U |
| 8 | KEY |
| 28 | N/U |

J2 is bracketed "TO BACKBOX" as a whole, but eight of its lines carry playfield functions (the four spinner lamps, the two waterlane values and the 10 K and 20 K golden cliff values); the plug-connector sheet's Table B routes exactly those eight pins (J2-14, -2, -15, -16, -20, -1, -6, -7) on through the panel-to-back-cab plug to the playfield (see `schematic-plug-connectors.md`).
