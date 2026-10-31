# Frontier - A5 lamp driver schematic (W-1182-29c), connector functions

Source: `Bally_1980_Frontier_Schematic_Diagrams_paginated.pdf`, PDF page 7, the A5 lamp driver schematic for game #1217, drawing number W-1182-29c, read from the native 300 dpi render and its connector crops. The connector pin numbers and the function printed against each are transcribed in the order the page prints them, top to bottom, which is the order of the SCR traces that reach them. "N/U" and "KEY" are the page's own; spacing and punctuation inside a name are kept as printed.

The rest of the sheet draws the same board as the Kiss and Paragon lamp driver sheets: four MC14514 one-of-sixteen decoders U1-U4, each enabled by one lamp-data line, all four addressed by AD0-AD3 from J4, and a column of sixty SCRs. Notes on the sheet: "1. **SCR's ARE MCR 106-1 (E-585-29), ALL OTHERS ARE 2N5060 (E-585-14) OR EQUIVALENTS." "2. ALL RESISTORS ARE 1/4W, ±5%." "3. PREFIX ALL REFERENCE DESIGNATIONS WITH "A5"." "4. * INDICATES "AID" TEST POINT."

## J1 - "TO PLAYFIELD"

| pin | function |
| --- | --- |
| 22 | N/U |
| 21 | N/U |
| 20 | KEY |
| 18 | SNAKE (LEFT) |
| 19 | HAWK (LEFT) |
| 17 | LION(LEFT) |
| 23 | WOLF(LEFT) |
| 14 | BEAR(LEFT) |
| 15 | "A" ROLLOVER LANE |
| 16 | 10K FRONTIER |
| 28 | 50K FRONTIER |
| 24 | LEFT TARGET ARROW |
| 25 | LEFT THUMPER BUMPER |
| 26 | N/U |
| 27 | RIGHT FLIP. FEED LANE |
| 1 | SNAKE(CENTER) |
| 9 | HAWK(CENTER) |
| 8 | LION(CENTER) |
| 3 | WOLF(CENTER) |
| 2 | BEAR(CENTER) |
| 10 | "B" ROLLOVER LANE |
| 7 | 20K FRONTIER |
| 6 | 60K FRONTIER |
| 5 | CENTER TARGET ARROW |
| 11 | BOTTOM THUMPER BUMPER |
| 13 | SPINNER 1000 |
| 4 | N/U |
| 12 | LEFT FLIP. FEED LANE |

## J2 - "TO BACK BOX"

| pin | function |
| --- | --- |
| 21 | SHOOT AGAIN |
| 13 | N/U |
| 22 | BALL IN PLAY |
| 16 | 2X DROP TARGET |
| 14 | GATE ARROW |
| 8 | MATCH |
| 12 | N/U |
| 23 | HIGH SCORE TO DATE |
| 20 | 3X DROP TARGET |
| 15 | 2X PREDATORS |
| 11 | GAME OVER |
| 6 | 4X DROP TARGET |
| 2 | 3X PREDATORS |
| 9 | N/U |
| 4 | N/U |
| 5 | N/U |
| 3 | N/U |
| 10 | TILT |
| 7 | SPECIAL DROP TARGET |
| 1 | 4X PREDATORS |
| 17 | N/U |
| 18 | KEY |
| 19 | N/U |

## J3 - "TO PLAYFIELD"

| pin | function |
| --- | --- |
| 26 | SNAKE(RIGHT) |
| 25 | HAWK (RIGHT) |
| 19 | LION(RIGHT) |
| 17 | WOLF(RIGHT) |
| 16 | BEAR(RIGHT) |
| 23 | "C" ROLLOVER LANE |
| 27 | 30K FRONTIER |
| 21 | RIGHT TARGET ARROW |
| 20 | RIGHTTHUMPER BUMPER |
| 22 | SAME PLAYER S. A. |
| 24 | RIGHT OUT SPECIAL |
| 1 | A-B-C EXTRA BALL |
| 12 | A-B-C SPECIAL |
| 15 | 45K PREDATORS |
| 11 | 4X FRONTIER |
| 9 | PREDATORS SPECIAL |
| 3 | 4X GRIZZLY TARGET |
| 4 | 40K FRONTIER |
| 2 | 30K GRIZZLY TARGET |
| 10 | 2X FRONTIER |
| 18 | 3X FRONTIER |
| 13 | CREDIT INDICATOR |
| 14 | LEFT OUT SPECIAL |
| 5 | N/U |
| 6 | N/U |
| 7 | N/U |
| 8 | KEY |
| 28 | N/U |

## How a pin becomes a public lamp

PinMAME publishes the board as public lamp = 16 x d + a + 1, d the lamp-data line PD0-PD3 and a the latched decoder address 0-14. The pin each decoder output reaches through its SCR is board-internal and is taken from the Kiss record (the same AS-2518-23 board, derived from its own sheets), so that J1-18 is public 1, J1-27 public 12, J2-21 public 11, J3-24 public 44, J3-14 public 60 and so on; every one of the sixty decoder outputs lands on a named pin of this sheet. The retained ROM confirms the chain on this game where it can be checked without the table: the right-bank awards step 14 -> 30 -> 46 -> 62 (2X, 3X, 4X DROP TARGET, SPECIAL DROP TARGET) and 31 -> 47 -> 63 (2X, 3X, 4X PREDATORS); the in-line targets light 57 (2X FRONTIER), then 58 (3X FRONTIER) with 54 and 56 (the grizzly target lamps), and the grizzly target lights 52 (4X FRONTIER); with lamp 12 lit the right flipper feed lane (switch 3) scored 15,000 and the left (switch 4) 500; with lamp 60 lit the left outlane (switch 5) awarded the special and the right outlane (switch 2) did not.
