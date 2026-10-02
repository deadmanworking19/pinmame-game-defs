# Star Gazer — playfield sheet, switch matrix

Transcribed from `Stern_1980_Star_Gazer_Schematic_Diagrams_paginated.pdf`, PDF page 2, the playfield sheet captioned "PLAYFIELD" and "STAR GAZER" (a 2960 x 2000 scan of a hand-lettered drawing), read from the rendered page and checked against a native-resolution crop. The sheet draws the switch matrix as five vertical strobe columns, `ST0 A` to `ST4 E`, crossed by eight horizontal return rows, `I0` to `I7`, with a diode drawn beside every switch. It prints this legend at the foot: `R.O.B.= ROLL-OVER BUTTON`, `D.T. = DROP TARGET`, `S.U. = STAND-UP TARGET`.

## Connectors

Each return row is labelled with its MPU connector pin and wire colour, as printed:

| row | connector pin | wire |
| --- | --- | --- |
| I0 | A4J2-8 | BRN |
| I1 | A4J2-9 | GREY |
| I2 | A4J2-10 | W-O |
| I3 | A4J2-11 | W-B |
| I4 | A4J2-12 | W-G |
| I5 | A4J2-13 | W-BRN |
| I6 | A4J2-14 | BRN-Y |
| I7 | A4J2-15 | O |

Each strobe column ends in its own connector pin and wire at the bottom of the drawing:

| column | connector pin | wire |
| --- | --- | --- |
| ST0 (A) | A4J2-1 | W-R |
| ST1 (B) | A4J2-2 | BRN-W |
| ST2 (C) | A4J2-3 | W-BLU |
| ST3 (D) | A4J2-4 | W-Y |
| ST4 (E) | A4J2-5 | Y-R |

## Switch labels, exactly as drawn

A blank cell means the drawing prints no label beside that switch symbol. The drawing numbers no switch; the number column is the position `8 x column + row + 1` and was checked against the manual's switch-identification table, which agrees with every label below that it also prints. A cell marked `cap` carries a capacitor symbol drawn from the left terminal of the switch to the diode node under it.

| row | ST0 (A) | ST1 (B) | ST2 (C) | ST3 (D) | ST4 (E) |
| --- | --- | --- | --- | --- | --- |
| I0 | (blank) = 1 | (CNTR.) SPIN. = 9 | S.U. "LEO" = 17, cap | (L) CNTR. D.T. = 25 | OUT HOLE = 33 |
| I1 | (blank) = 2 | S.U. "GEMINI" = 10, cap | S.U. "VIRGO" = 18, cap | (M) CNTR. D.T. = 26 | (R) OUT LANE = 34 |
| I2 | (blank) = 3 | S.U. "CANCER" = 11, cap | S.U. "SCORPIO" = 19, cap | (R) CNTR D.T. = 27 | (L) OUT LANE = 35 |
| I3 | (L) SPIN. = 4 | (L) THUMPER = 12 | S.U. "LIBRA" = 20, cap | TOP (R) D.T. = 28 | (R) R.O.B. = 36, cap |
| I4 | (R) SPIN. = 5 | (R) THUMPER = 13 | S.U. "SAGITTARIUS" = 21, cap | MID.(R) D.T. = 29 | (L) R.O.B. = 37, cap |
| I5 | (blank) = 6 | (CNTR) THUMPER = 14 | BOT.(L) D.T. = 22 | BOT.(R) D.T. = 30 | S.U. "PISCES" = 38, cap |
| I6 | (blank) = 7, cap | (R) SLINGSHOT = 15, cap | MID.(L) D.T. = 23 | S.U. "CAPRICORN" = 31, cap | S.U. "ARIES" = 39, cap |
| I7 | SLAM = 8, cap | (L) SLINGSHOT = 16, cap | TOP (L) D.T. = 24 | S.U. "AQUARIUS" = 32, cap | S.U. "TAURUS" = 40, cap |

The drawing prints the sign names `SCORPIO` at row I2 of column ST2 (switch 19) and `LIBRA` at row I3 (switch 20). The ROM and the playfield art order those two targets the other way round; the definition's device notes for switches 19 and 20 state the disagreement and the runtime evidence that settles it.

## General illumination

Under the matrix the sheet draws one general-illumination lamp symbol labelled `GEN. ILLUM`, fed from `A2J1-8 (W)` marked `6 VAC` and returning through `A2J1-1 (R)` marked `RETURN`. No switch, relay or driver transistor is drawn in that circuit.
