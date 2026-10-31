# Frontier - playfield wiring sheet "SWITCH MATRIX" (W-1192-25c, PLAYFIELD A6)

Source: `Bally_1980_Frontier_Schematic_Diagrams_paginated.pdf`, PDF page 10, the sheet titled "SWITCH MATRIX", material "FRONTIER", game 1217, drawing number W-1192-25c, captioned "PLAYFIELD A6". Read from the native 300 dpi render and gridded crops of the matrix, the coil column, the two lamp lists, the G.I. block and the notes. Every region of the sheet is transcribed below. Names are kept as printed; a drawn switch with no name against it is written `(blank)`.

## Switch matrix

The matrix is drawn as eight return rows I0-I7 crossed by five strobe columns ST0-ST4. Every one of the forty cells draws a switch and a series diode, including the cells that carry no name. A `*` marks an AID test point; the sheet prints it over A4J2-9 to A4J2-15 and over ST0-ST4, and not over A4J2-8.

Row and strobe leads, as printed on the left edge:

| line | wire | connector |
| --- | --- | --- |
| I0 | 54 | A4J2-8 |
| I1 | 56 | A4J2-9 * |
| I2 | 57 | A4J2-10 * |
| I3 | 78 | A4J2-11 * |
| I4 | 60 | A4J2-12 * |
| I5 | 56 | A4J2-13 * |
| I6 | 65 | A4J2-14 * |
| I7 | 52 | A4J2-15 * |
| ST0 | 51 | A4J2-1 * |
| ST1 | 70 | A4J2-2 * |
| ST2 | 93 | A4J2-3 * |
| ST3 | 53 | A4J2-4 * |
| ST4 | 31 | A4J2-5 * |

The I1 lead prints wire 56, the same number as I5; the plug-connector sheet (W-1187-25c) prints wire 63 on A4J2-9. It is a wire-number disagreement and changes no switch.

Cell names, column by column. "cap" marks a cell whose switch is drawn with a capacitor across it.

| row | ST0 | ST1 | ST2 | ST3 | ST4 |
| --- | --- | --- | --- | --- | --- |
| I0 | 30 POINT REBOUND (4) | (blank) | (blank) | SAUCER ROLLOVER BUTTON | BOTTOM SIDE DROP TARGET |
| I1 | RIGHT OUT SPECIAL | (blank) | (blank) | (blank) | MIDDLE SIDE DROP TARGET |
| I2 | RIGHT FLIPPER FEED LANE | (blank) | (blank) | SPINNER | TOP SIDE DROP TARGET |
| I3 | LEFT FLIPPER FEED LANE | SAUCER | (blank) | (blank) | RIGHT SLINGSHOT |
| I4 | LEFT OUT SPECIAL | "A" ROLLOVER LANE | 3RD. IN LINE DROP TARGET | LEFT TARGET (cap) | LEFT SLINGSHOT |
| I5 | (blank) | "B" ROLLOVER LANE | 2ND IN LINE DROP TARGET | CENTER TARGET (cap) | BOTTOM THUMPER BUMPER (cap) |
| I6 | TILT | "C" ROLLOVER LANE | 1ST. IN LINE DROP TARGET | RIGHT TARGET (cap) | RIGHT THUMPER BUMPER (cap) |
| I7 | OUTHOLE | (blank) | GRIZZLY TARGET (cap) | (blank) | LEFT THUMPER BUMPER (cap) |

The 1ST. cell's first character is printed as a numeral one that the scan renders like a capital I. The blank cells are the cabinet switches the plug-connector sheet brings out on A4J3 (credit, coins, slam) and the unused crossings; this sheet names only the playfield ones. TILT at ST0/I6 is the playfield panel tilt the manual describes.

## Coil column

A +43 VDC bus enters on wire 60 from A2J1-6, passes a fuse marked "1A. S.B." and continues on wire 30. Each coil is drawn with a diode across it. The two flipper coils are drawn as two windings with an end-of-stroke switch and capacitor across one winding; the right flipper carries a "SEE NOTE 5" pointer.

| wire | connector | coil |
| --- | --- | --- |
| 40 | A3J1-8 | LEFT FLIPPER |
| 70 | A3J1-9 | RIGHT FLIPPER |
| 95 | A3J1-5 | OUTHOLE KICKER |
| 85 | A3J5-10 | IN LINE DROP TARGET |
| 78 | A3J5-11 | SAUCER |
| 80 | A3J5-12 | 3 DROP TARGET |
| 71 | A3J5-9 | LEFT THUMPER BUMPER |
| 74 | A3J5-15 | RIGHT THUMPER BUMPER |
| 67 | A3J5-13 | BOTTOM THUMPER BUMPER |
| 83 | A3J5-14 | LEFT SLINGSHOT |
| 18 | A3J5-8 | RIGHT SLINGSHOT |
| 81 | A3J5-7 | GATE |

## Playfield lamp list, A5J1 and A5J3

Each line runs from its wire through a drawn bulb to a common bus marked 5.4 VDC; the list ends on the feature lamp bus.

| wire | connector | name |
| --- | --- | --- |
| 58 | A5J1-18 | SNAKE (LEFT) |
| 60 | A5J1-19 | HAWK (LEFT) |
| 57 | A5J1-17 | LION (LEFT) |
| 12 | A5J1-23 | WOLF (LEFT) |
| 54 | A5J1-14 | BEAR (LEFT) |
| 13 | A5J1-15 | "A" ROLLOVER LANE |
| 90 | A5J1-16 | 10K FRONTIER |
| 78 | A5J1-28 | 50K FRONTIER |
| 50 | A5J1-24 | LEFT TARGET ARROW |
| 75 | A5J1-25 | LEFT THUMPER BUMPER |
| 91 | A5J1-26 | N/U |
| 53 | A5J1-27 | RIGHT FLIP. FEED LANE |
| 41 | A5J1-1 | SNAKE (CENTER) |
| 43 | A5J1-9 | HAWK (CENTER) |
| 51 | A5J1-8 | LION (CENTER) |
| 45 | A5J1-3 | WOLF (CENTER) |
| 52 | A5J1-2 | BEAR (CENTER) |
| 23 | A5J1-10 | "B" ROLLOVER LANE |
| 34 | A5J1-7 | 20K FRONTIER |
| 25 | A5J1-6 | 60K FRONTIER |
| 48 | A5J1-5 | CENTER TARGET ARROW |
| 65 | A5J1-11 | BOTTOM THUMPER BUMPER |
| 35 | A5J1-4 | N/U |
| 61 | A5J1-12 | LEFT FLIP. FEED LANE |
| 96 | A5J1-13 | SPINNER 1000 |
| 43 | A5J3-26 | SNAKE (RIGHT) |
| 36 | A5J3-25 | HAWK (RIGHT) |
| 67 | A5J3-19 | LION (RIGHT) |
| 13 | A5J3-17 | WOLF (RIGHT) |
| 25 | A5J3-16 | BEAR (RIGHT) |
| 98 | A5J3-23 | "C" ROLLOVER LANE |
| 40 | A5J3-27 | 30K FRONTIER |
| 30 | A5J3-21 | RIGHT TARGET ARROW |
| 64 | A5J3-20 | RIGHT THUMPER BUMPER |
| 23 | A5J3-22 | SAME PLAYER S.A. |
| 72 | A5J3-24 | RIGHT OUT SPECIAL |
| 10 | A5J3-1 | A-B-C EXTRA BALL |
| 21 | A5J3-12 | A-B-C SPECIAL |
| 53 | A5J3-15 | 45K PREDATORS |
| 20 | A5J3-11 | 4X FRONTIER |
| 15 | A5J3-9 | PREDATORS SPECIAL |
| 35 | A5J3-13 | CREDIT INDICATOR |
| 14 | A5J3-4 | 40K FRONTIER |
| 95 | A5J3-2 | 30K GRIZZLY TARGET |
| 91 | A5J3-10 | 2X FRONTIER |
| 56 | A5J3-18 | 3X FRONTIER |
| 81 | A5J3-3 | 4X GRIZZLY TARGET |
| 84 | A5J3-14 | LEFT OUT SPECIAL |
| 20 | A2J1-7 | FEATURE LAMP BUS |

Every wire and pin agrees with the plug-connector sheet's A5 J1 and J3 blocks.

## Playfield lamps routed from the back box, A5J2

A second, shorter list in the lower middle of the sheet, its lines also drawn through bulbs, with an arrow "TO W-1187-25":

| wire | connector | name |
| --- | --- | --- |
| 60 | A5J2-1 | CENTER "B" |
| 20 | A5J2-2 | CENTER "O" |
| 12 | A5J2-14 | CENTER "G" |
| 23 | A5J2-15 | CENTER "L" |
| 34 | A5J2-16 | 10K BONUS |
| 35 | A5J2-20 | 20K BONUS |
| 85 | A5J2-6 | 30K BONUS |
| 91 | A5J2-7 | 40K BONUS |

These are the same eight pins and wires as the plug-connector sheet's Table "B" (panel to back cabinet plug), and wire 35 on A5J2-20 agrees with Table B. The names do not: the lamp driver and plug-connector sheets call these pins 4X PREDATORS, 3X PREDATORS, GATE ARROW, 2X PREDATORS, 2X DROP TARGET, 3X DROP TARGET, 4X DROP TARGET and SPECIAL DROP TARGET, and no "B-O-G-L" or 10K-40K bonus feature appears anywhere in the Frontier manual or on the playfield. The retained ROM runs light these pins' public lamps as the lamp driver sheet names them (the right-bank awards step 14, 30, 46, 62 and 31, 47, 63; lamp 15 lights when the gate opens).

## General illumination

| wire | connector | |
| --- | --- | --- |
| 10 | A2J1-8 | 5.9 VAC |
| 70 | A2J1-5 | 5.9 VAC |
| 40 | A2J1-2 | RET. |
| 50 | A2J1-1 | RET. |

The four leads feed one drawn bulb labelled "GEN. ILLUM."; the sheet gives no bulb count or socket positions.

## Notes, verbatim

> NOTES
> 1. INDICATES NOT USED
> 2. N/U = NOT USED ON PLAYFIELD
> 3. * INDICATES AID TEST POINT
> 4. COIL DIODES ARE IN4004 ,(E-587-6) SWITCH DIODES ARE IN 4148,(E-587-14)
> ALL CAPACITORS ARE .05 MFD. (E-586-80)
> 5. GERMANY ONLY-CAPACITOR .01 MFD. @ 500V. (E-586-65)

Note 1 prints no symbol before "INDICATES" in this scan.
