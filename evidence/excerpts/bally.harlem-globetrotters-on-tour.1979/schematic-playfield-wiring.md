# Harlem Globetrotters On Tour - playfield wiring sheet: switch matrix, playfield coils, lamps and G.I.

Transcribed from `Bally_1979_Harlem_Globetrotters_On_Tour_Manual.pdf`, PDF page 45, the sheet titled "SWITCH MATRIX" / "HARLEM GLOBETROTTERS", part no. W-1192-14c (title block game "1161-E"), whose drawing is labelled "PLAYFIELD A6". The sheet is printed rotated; it was read from 206 dpi and 220-250 dpi renders of the scan. Every text element of the drawing is transcribed below. Wire numbers are printed beside the connector pins and are given in parentheses; the sheet's wire colour code is on the plug connectors sheet (`schematic-plug-connectors.md`).

The crop beside this file (`schematic-playfield-wiring.webp`) is the flipper and outhole circuit at the top of the coil column, kept as a picture because the left flipper end-of-stroke wiring is a drawing.

## Switch matrix

Returns I0-I7 enter from the left, strobes ST0-ST4 leave at the bottom; every matrix cell is drawn with a switch and a series diode whether or not it is labelled. An asterisk is printed over A4J2-9 to A4J2-15 and over ST0 to ST4 (note 3, AID test point). A blank cell below is drawn with a switch but carries no label.

| return | connector (wire) | ST0 | ST1 | ST2 | ST3 | ST4 |
| --- | --- | --- | --- | --- | --- | --- |
| I0 | A4J2-8 (54) | DROP TARGET "D" TOP | *(blank)* | LEFT SIDE SPINNER | RIGHT CENTER SPINNER | LEFT CENTER SPINNER |
| I1 | A4J2-9 (56) | "C" | *(blank)* | *(blank)* | LEFT SIDE TARGETS "1" (BOTTOM) | 300 POINT REBOUND |
| I2 | A4J2-10 (57) | "B" | *(blank)* | *(blank)* | "2" | DUNK SHOT TARGET |
| I3 | A4J2-11 (58) | "A" (BOTTOM) | *(blank)* | *(blank)* | "3" | RIGHT SLINGSHOT |
| I4 | A4J2-12 (60) | *(blank)* | *(blank)* | *(blank)* | "4" | LEFT SLINGSHOT |
| I5 | A4J2-13 (63) | *(blank)* | *(blank)* | RIGHT FLIPPER FEEDER LANE | "5" (TOP) | BOTTOM THUMPER BUMPER |
| I6 | A4J2-14 (65) | TILT | *(blank)* | RIGHT OUTLANE | LEFT OUTLANE | RIGHT THUMPER BUMPER |
| I7 | A4J2-15 (70) | OUTHOLE | *(blank)* | GLOBE SAUCER | TARGET SAUCER | LEFT THUMPER BUMPER |

| strobe | connector (wire) |
| --- | --- |
| ST0 | A4J2-1 (51) |
| ST1 | A4J2-2 (93) |
| ST2 | A4J2-3 (52) |
| ST3 | A4J2-4 (53) |
| ST4 | A4J2-5 (31) |

A capacitor is drawn across the cells ST3/I1, ST3/I2, ST3/I3, ST3/I4, ST3/I5, ST4/I2, ST4/I5, ST4/I6 and ST4/I7 (the five side targets, the dunk shot target and the three thumper bumpers); no other cell carries one.

## Playfield coils

All coils hang from "+ 43 VDC" (wire 60, from A2J1-6); each is drawn with a diode across it.

| coil (as printed) | return connector (wire) | notes on the drawing |
| --- | --- | --- |
| LEFT FLIPPER | A3J1-8 (40) | two windings; an "N.C." contact across the upper winding |
| UPPER LEFT FLIPPER | wire 91, through the "N.O." contact "LEFT FLIPPER E.O.S." to A3J1-8 | two windings; an unlabelled contact across the upper winding |
| RIGHT FLIPPER | A3J1-9 (70) | two windings; an "N.C." contact across the upper winding |
| OUTHOLE KICKER | A3J1-5 (95) | fed through a fuse "1A.S.B." (wire 30 after the fuse) |
| RIGHT THUMPER BUMPER | A3J5-10 (74) | |
| BOTTOM THUMPER BUMPER | A3J5-11 (78) | |
| LEFT THUMPER BUMPER | A3J5-12 (75) | |
| LEFT SLINGSHOT | A3J5-9 (71) | |
| RIGHT SLINGSHOT | A3J5-15 (85) | |
| GLOBE SAUCER | A3J5-13 (80) | |
| TARGET SAUCER | A3J5-14 (83) | |
| DROP TARGET RESET | A3J5-8 (18) | |
| RIGHT GATE | A3J5-7 (81) | |

The thumper bumpers, slingshots, saucers, drop target reset and right gate share the fused supply after "1A.S.B." with the outhole kicker; the three flippers take +43 VDC before the fuse. The upper left flipper has no connector of its own: its coil returns through the left flipper's normally open end-of-stroke contact, so it fires only when the lower left flipper reaches end of stroke.

## Lamps

The lamp column is printed in this order, each line ending in one lamp symbol tied to the "5.4 VDC" bus. Every line is drawn with one lamp, including the N/U line, so the drawing does not state bulb quantities.

| wire | connector and printed function |
| ---: | --- |
| 58 | A5J1-18 1K BONUS |
| 60 | A5J1-19 5 K BONUS |
| 57 | A5J1-17 9 K BONUS |
| 56 | A5J1-23 SPINNERS ① BOTTOM |
| 54 | A5J1-14 SPINNERS ⑤ TOP |
| 13 | A5J1-15 LEFT SIDE SPINNER 100 |
| 12 | A5J1-16 SAUCER "G" |
| 78 | A5J1-28 SAUCER "E" |
| 50 | A5J1-24 SIDE TARGET ⑤ TOP |
| 90 | A5J1-25 SIDE TARGET ① BOTTOM |
| 91 | A5J1-26 CENTER "E" |
| 53 | A5J1-27 2 X BONUS |
| 41 | A5J1-1 2 K BONUS |
| 52 | A5J1-9 6 K BONUS |
| 51 | A5J1-8 DUNK SHOT 5K |
| 45 | A5J1-3 SPINNERS ② |
| 43 | A5J1-2 DUNK SHOT OPENS GATE |
| 23 | A5J1-10 LEFT SIDE SPINNER 200 (a circled "B" is printed beside this wire) |
| 34 | A5J1-7 SAUCER "L" |
| 25 | A5J1-6 DUNK SHOT SPECIAL |
| 48 | A5J1-5 SIDE TARGET ④ |
| 65 | A5J1-11 BOTTOM THUMPER BUMPER |
| 35 | A5J1-4 N/U |
| 61 | A5J1-12 3 X BONUS |
| 96 | A5J1-13 25K LEFT OUTLANE |
| 38 | A5J3-26 3 K BONUS |
| 36 | A5J3-25 7 K BONUS |
| 67 | A5J3-19 RIGHT SPIN. ADV. BONUS |
| 27 | A5J3-17 SPINNERS ③ |
| 25 | A5J3-16 GATE OPEN W/LIT |
| 98 | A5J3-23 LEFT SIDE SPINNER 1K |
| 40 | A5J3-27 SAUCER "O" |
| 30 | A5J3-21 SIDE TARGET ③ |
| 64 | A5J3-20 LEFT AND RIGHT THUMPER BUMPER |
| 23 | A5J3-22 S.P. S. A. |
| 72 | A5J3-24 5 X BONUS |
| 10 | A5J3-1 4 K BONUS |
| 21 | A5J3-12 8 K BONUS |
| 53 | A5J3-15 LEFT SPIN. ADV. BONUS |
| 20 | A5J3-11 SPINNERS ④ |
| 15 | A5J3-9 TARGET SAUCER 25K |
| 13 | A5J3-13 CREDIT INDICATOR |
| 14 | A5J3-4 SAUCER "B" |
| 95 | A5J3-2 SAUCER TARGET SPECIAL |
| 91 | A5J3-10 SIDE TARGET ② |
| 56 | A5J3-18 DUNK SHOT EXTRA BALL |
| 81 | A5J3-3 LEFT SIDE SPINNER 2 K |
| 84 | A5J3-14 G-L-O-B-E SPECIAL |
| 20 | A2J1-7 FEATURE LAMP BUS |

A separate group, bracketed with a circled "A" and led off "TO W-1187-14", carries the eight A5 J2 lamps that are on the playfield:

| wire | connector and printed function |
| ---: | --- |
| 60 | A5J2-1 CENTER "B" |
| 20 | A5J2-2 CENTER "O" |
| 12 | A5J2-14 CENTER "G" |
| 23 | A5J2-15 CENTER "L" |
| 34 | A5J2-16 10 K BONUS |
| 35 | A5J2-20 20 K BONUS |
| 85 | A5J2-6 30 K BONUS |
| 91 | A5J2-7 40 K BONUS |

## General illumination

| wire | connector | label |
| ---: | --- | --- |
| 10 | A2J1-8 | 5.9 VAC. |
| 70 | A2J1-5 | |
| 40 | A2J1-2 | RET. |
| 50 | A2J1-1 | |

One lamp symbol labelled "GEN. ILLUM." stands for the whole G.I. string; the sheet gives no G.I. bulb count.

## NOTES

> 1. INDICATES NOT USED
> 2. N/U = NOT USED ON PLAYFIELD
> 3. ✱ INDICATES AID TEST POINT
> 4. ALL DIODES ARE IN4004 ,(E-587-6)
> ALL CAPACITORS ARE .05 MFD. (E-586-80)

Note 1 is printed with a leading symbol that the scan does not resolve.
