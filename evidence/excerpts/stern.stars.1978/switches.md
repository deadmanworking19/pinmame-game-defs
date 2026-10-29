# Stars switch identification and matrix

Source: Stern Stars CAT. NO. 12G-5-103, PDF 18 (printed 13), full
SWITCH IDENTIFICATION / SELF TEST DISPLAY NUMBERS table. Manual transcription
checked against the native-resolution render by the primary curator. `[blank]`
means a printed empty location cell; it is not the words NOT USED. Dot leaders
are omitted; capitalization, numbering and parenthesized quantities are retained.

Note: Flipper button cabinet switches do not appear on test.

| SWITCH NO. | SWITCH LOCATION |
| --- | --- |
| 1 | LEFT SPINNER |
| 2 | [blank] |
| 3 | [blank] |
| 4 | LEFT OUT LANE |
| 5 | LEFT RETURN LANE |
| 6 | CREDIT BUTTON |
| 7 | TILT |
| 8 | OUTHOLE |
| 9 | COIN #3 (RT) |
| 10 | COIN #2 (CTR) |
| 11 | COIN #1 (LT) |
| 12 | RIGHT OUT LANE |
| 13 | RIGHT RETURN LANE |
| 14 | [blank] |
| 15 | ROLL - OVER (BONUS) |
| 16 | SLAM (3) |
| 17 | RIGHT SPINNER |
| 18 | [blank] |
| 19 | [blank] |
| 20 | STAR NO. 5 |
| 21 | STAR NO. 4 |
| 22 | STAR NO. 3 |
| 23 | STAR NO. 2 |
| 24 | STAR NO. 1 |
| 25 | (7) 10 POINT SWITCH |
| 26 | [blank] |
| 27 | DROP TARGET NO. 5 |
| 28 | DROP TARGET NO. 2 |
| 29 | DROP TARGET NO. 6 |
| 30 | DROP TARGET NO. 4 |
| 31 | DROP TARGET NO. 3 |
| 32 | DROP TARGET NO. 1 |
| 33 | [blank] |
| 34 | [blank] |
| 35 | [blank] |
| 36 | RIGHT SLINGSHOT |
| 37 | LEFT SLINGSHOT |
| 38 | THUMPER BUMPER |

The table ends at 38. It does not print 39 or 40.

PDF 29 and 31, drawing 12B-185-2 and 12B-185-3, full five-column
switch regions, transcribed by matrix position. A star glyph is written `*`;
the second form of star used for the slam footnote is written `*'`. Printed
labels differing from the identification table are preserved. The rows are
I0-I7 and columns ST0/A, ST1/B, ST2/C, ST3/D, ST4/E. Public numbers in the
last sentence below are derived, not printed in the drawing.

| Row | ST0/A | ST1/B | ST2/C | ST3/D | ST4/E |
| --- | --- | --- | --- | --- | --- |
| I0 | LEFT SPINNER | * | RIGHT SPINNER | 10 PTS (7) | N/U |
| I1 | N/U | * | N/U | N/U | N/U |
| I2 | N/U | * | N/U | DROP TARGET No.5 | N/U |
| I3 | LEFT OUT LANE | RIGHT OUT LANE | STAR 5 | DROP TARGET No.2 | RIGHT SLING SHOT |
| I4 | LEFT RETURN LANE | RIGHT RETURN LANE | STAR 4 | DROP TARGET No.6 | LEFT SLINGSHOT |
| I5 | * | N/U | STAR 3 | DROP TARGET No.4 | BUMPER |
| I6 | * | ROLL OVER | STAR 2 | DROP TARGET No.3 | N/U |
| I7 | OUT HOLE | SLAM (*') | STAR 1 | DROP TARGET No.1 | N/U |

Legend: `* = SWITCHES USED ON CABINET & DOOR`; `*' = SLAM SWITCH ON TILT
BOARD & DOOR`; `N/U = NOT USED`; `ALL DIODES ARE 1N-4004`; `CAPACITORS
ARE DISC .05 MF 100 V`.

| Playfield return | MPU connection | Literal wire |
| --- | --- | --- |
| I0 | A4J2-8 | BRN |
| I1 | A4J2-9 | GREY |
| I2 | A4J2-10 | W-O |
| I3 | A4J2-11 | W-B |
| I4 | A4J2-12 | W-G |
| I5 | A4J2-13 | W-BRN |
| I6 | A4J2-14 | BRN-Y |
| I7 | A4J2-15 | O |

| Strobe | MPU connection | Literal wire |
| --- | --- | --- |
| ST0/A | A4J2-1 | W-R |
| ST1/B | A4J2-2 | BRN-W |
| ST2/C | A4J2-3 | W-BLU |
| ST3/D | A4J2-4 | W-Y |
| ST4/E | A4J2-5 | Y-R |

Cabinet matrix region on PDF 31:

| Row | ST0/A | ST1/B | ST2/C | ST3/D | ST4/E |
| --- | --- | --- | --- | --- | --- |
| I0 | * | COIN #3 | * | * | N/U |
| I1 | N/U | COIN #2 | N/U | N/U | N/U |
| I2 | N/U | COIN #1 | N/U | * | N/U |
| I3 | * | * | * | * | * |
| I4 | * | * | * | * | * |
| I5 | CREDIT RESET | N/U | * | * | * |
| I6 | TILT PLUMB BOB / TILT ROLL CAGE | * | * | * | N/U |
| I7 | * | SLAM (NOTE 1) | * | * | N/U |

Here `* = SWITCHES USED ON PLAYFIELD`; `*' = SLAM SWITCH ON UNDERSIDE OF
PLAYFIELD ALSO`; `NOTE 1 = SLAM SWITCH TILT BOARD & FRONT DOOR`.
The tilt contacts are drawn in parallel. All fitted matrix contact symbols
are open at rest. The flipper EOS contacts drawn across the low-resistance
windings on PDF 29 are closed at rest; they are not matrix contacts.

| Cabinet return | MPU connection | Literal wire |
| --- | --- | --- |
| I0 | A4J3-9 | R-W |
| I1 | A4J3-10 | BRN-W |
| I2 | A4J3-11 | BLU |
| I3 | [not labelled at left margin] | [blank] |
| I4 | [not labelled at left margin] | [blank] |
| I5 | A4J3-14 | BLU-W |
| I6 | A4J3-15 | BLU-O |
| I7 | A4J3-16 | Y |

The cabinet strobe connections printed below the drawing are A4J3-2 (R-Y)
and A4J3-3 (R-G). Self-test is a separate normally-open TEST SWITCH from
A4J3-1 (R) to A3J2-7 (Y-R). The left flipper button is A3J2-2 (BLU), right
is A3J2-1 (R), common A2J2-9 (O); they directly switch the flipper circuits.

Derived public matrix address: `8 * strobe_index + row_index + 1`.
Unused fitted-matrix positions are 2, 3, 14, 18, 19, 26, 33, 34, 35, 39, 40.
Do not map the generic Bally ball-roll-tilt constant at 2 onto this machine;
both physical tilt contacts close address 7.
