# Stars coil numbers, corrections and option switches

Primary curator transcription checked against native-resolution renders.
Dot leaders are omitted, `[blank]` denotes a printed empty cell. Source:
Stars manual PDF 20, printed 15, full SOLENOID IDENTIFICATION / SELF TEST
DISPLAY NUMBERS table. These are diagnostic numbers, not public addresses.

| SOLENOID NO. | SOLENOID LOCATION |
| --- | --- |
| 1 | CHIME (10) (SMALL) |
| 2 | [blank] |
| 3 | CHIME (100) |
| 4 | [blank] |
| 5 | CHIME (1,000) |
| 6 | THUMPER |
| 7 | CHIME (10,000) |
| 8 | OUT HOLE |
| 9 | RIGHT SLINGSHOT |
| 10 | DROP TARGET RESET (LEFT) |
| 11 | [blank] |
| 12 | [blank] |
| 13 | DROP TARGET RESET (RIGHT) |
| 14 | LEFT SLINGSHOT |
| 15 | KNOCKER |
| 16 | (2) FLIPPERS & RELAY ON SOL. DRIVER P.C. BOARD |
| 17 | COIN LOCK OUT |

PDF 15, printed 10, full MPU SWITCH ASSIGNMENT summary:

| Switch | Assignment |
| --- | --- |
| 1 Thru 5 | COIN CHUTE No. 2 CENTER |
| 6 | HIGH SCORE |
| 7 | BALLS PER GAME |
| 8 | CHIME MELODY |
| 9 Thru 13 | COIN CHUTE No. 3 |
| 14 | N/U |
| 15 | HIGH GAME TO DATE |
| 16 | N/U |
| 17, 18, 19 | MAXIMUM CREDITS |
| 20 | CREDIT DISPLAY |
| 21 | MATCH FEATURE |
| 22 | BONUS COUNT DOWN |
| 23 | N/U |
| 24 | TARGET SETS DOWN FOR 3X |
| 25 | 2 or 4 PLAYERS |
| 26 | EXTRA BALL ENABLE |
| 27, 28, 29 | N/U |
| 30 | STAR SPECIAL SELECTION |
| 31 & 32 | SPECIAL AWARD |

PDF 3, unnumbered corrections sheet headed `"STARS" CAT. NO. 12G-5-103
CORRECTIONS`, all corrections (the option summary above remains literal):

Page 1. Check adjustment of the three (normally open) tilt switches: Line 2 -
(15/16" dia), should read (gold 15/16" dia.)

Page 3. This page is - Figure 2.

Page 4. Bonus score 10,000 points listed in three places should read 1,000 points.
Third paragraph should read as follows - Shooting the ball initiates play.
Rebound switches score 10 points. Thumper-bumper scores 100 points in
5 ball, 1000 points in 3 ball.

Page 6. Bonus Score Feature: The bonus score would also advance one step when
one of the 5 stationary "Star" targets are hit.

Page 7. Credit/coin Adjustments: Should read as follows - The #1 Coin chute (next
to hinge) is adjustable to give 1 or 2 games per coin (Sw #16).

Page 8. Add Adjustment 6A. #1 Coin Chute Adjustment:

| Credit/Coin | Switch 16 |
| --- | --- |
| 1/Coin | OFF |
| 2/Coin | ON |

Page 10. MPU Switch Adjustment #16 should read: Coin Chute #1.
Last paragraph, last lines should read as follows: The feature is turned off
by positioning switch 15 to the "Off" position.
*Can be quickly set to '00' by pressing S33 on the MPU assembly in the
back box. See figure 3.

Service Bulletin #7, retained filename says July 7, 1978; PDF page 2
actually prints **JUNE 7, 1978**. Full ROM-set table:

| LOC. | 101 PINBALL | 102 STINGRAY | 103 STARS | 103 STARS | 104 MEMORY LANE | 104 MEMORY LANE |
| --- | --- | --- | --- | --- | --- | --- |
| U2 | 25A-ROM-P1 | 25A-ROM-P1 | 25A-ROM-P3 | 25A-ROM-P3A | 25A-ROM-P5A | 25A-ROM-P5B |
| U6 | 25A-ROM-P2 | 25A-ROM-P2 | 25A-ROM-P4 | 25A-ROM-P4A | 25A-ROM-P6A | 25A-ROM-P6B |

The two sets under a game share a printed game heading, repeated here rather
than pretending they are separate headings. Board less ROMs: C-433; board
with ROMs: C-433 & MODEL NO. ROMs must be used in sets. If either Stars P3
or P4 fails, both should be replaced by P3A and P4A; P3/P4 were unavailable.

Service Bulletin #8, PDF page 2, entire game-specific instruction:
`SWITCH 27 ON THE MPU BOARD MUST BE IN THE "ON" POSITION IF IT IS IN THE
"OFF" POSITION, THE GAME WILL ONLY PUT ONE PLAYER UP.`

This explicitly supersedes the manual's N/U for option S27. It is an MPU
option switch, not playfield switch 27. The bulletin does not identify the
ROM revision to which it applies; do not claim identical behavior for the
community modifications or the undumped A set without a further source.

Engineering Bulletin #9, PDF page 2, MOMENTARY COIL INFORMATION Q1 TO 14
& Q16: low-side SE9302 switches, flyback 1N4004, coil supply +43V. Full
numbered instruction region below; line wraps are normalized. The transcription
also normalizes printed `replace ship` to `replace chip`, `IN4004` to `1N4004`,
and adds quotes to point `D`. It describes
source circuit tests, not additional game-specific load assignments.

1. Momentary ground selected coil (Point A), coil should energize.
2. Momentary ground selected terminal on jack J1, J2 or J5 (Point B) coil should energize.
3. Using game schematic, momentary ground metal tab on selected Q1 to 14 or 16 (Point C), coil should energize.
4. Locate TP6 (right side of Q19 on SDU Board). Clip one end of test cord to TP6 and momentary touch point "D" of selected Q1 to Q14 or 16 coil (see game schematic), Coil should energize, if not replace "Q" transistor being tested.
5. U1, U2 & U4 (CA3081) is a transistor array chip.

Using the game schematic to locate coil and corresponding Q1 to Q14 or 16
transistor, the chart can be used.

From the chart go to the correct transistor chip and ground base pin no.
Coil should energize. If coil does not energize with base grounded and
collector does not have 5 VDC, replace chip. If 5 VDC is present replace
1N4004 diode (Point E) in circuit.

The following is the complete printed transistor-array table. Its collector
header is literally `Collect Pin No.`; omitted line separators normalized.

| Q1 to 14 or 16 | CA3081 chip | Base Pin No. | Collect Pin No. |
| --- | --- | --- | --- |
| Q1 | U1 | 16 | 1 |
| Q2 | U1 | 3 | 2 |
| Q3 | U1 | 6 | 4 |
| Q4 | U1 | 8 | 7 |
| Q5 | U1 | 13 | 14 |
| Q6 | U1 | 11 | 12 |
| Q7 | U1 | 10 | 9 |
| Q8 | U3 | 16 | 1 |
| Q9 | U3 | 3 | 2 |
| Q10 | U3 | 8 | 7 |
| Q11 | U3 | 6 | 4 |
| Q12 | U3 | 10 | 9 |
| Q13 | U3 | 11 | 12 |
| Q14 | U3 | 13 | 14 |
| Q16 | U4 | 8 | 7 |

The generic bulletin explains the switching circuit; game-specific load and
connector assignments still come from Stars' own wiring sheets.
