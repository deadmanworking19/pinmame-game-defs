# The Limited Edition cabinet chart

`LOTR-LE-ONLY-Cabinet-Matrix-11x17.pdf`, published by an LE owner, Richard Harvey ("firepower"), as the `LOTR LE Cabinet Matrix`, an 11x17" page to go inside the LE's lower cabinet: https://firepowerpinball.com/2ya/lotr/LOTR-LE-ONLY-Cabinet-Matrix-11x17.pdf, byte-identical to the copy mirrored as https://www.pinballrebel.com/pinball/cards/Tech_Charts/Stern_Lord_of_the_Rings_LE_Tech_Chart.pdf (SHA-256 `a7eeefd8f739d48cea1c80ef18c48d42a08d5e9c2438ed7d2b2c6cbfe9e94d02`). It is Stern's Lord of the Rings cabinet chart (`SPI Nr. 755-5310-80`) as the owner corrected it for his Limited Edition, titled `LORD of the RINGS LE` and `Switch Matrix, Coils Detailed Chart Table, Lamp Matrix, Playfield Maps, Switch, Coil & Lamp Wiring & Schematics, and Bulb Types`. Its owner's page says it documents his own game's wiring and that other LEs may use different wire colours.

The three tables below are complete. They were read from the PDF's text layer by grid position (`tools/lotr_le_chart_transcription.py`), with runs of spaces folded to one, and checked against the page rendered at 300 dpi. The marks the chart draws as images rather than text were read from that rendering: the rotation mark beside a coil type, the fraction in `20½-480`, the DOTS badge on #7 and the flash-test note. The same sheet also carries the service-menu icon strips, the switch, coil and lamp location maps of the playfield and back panel, and the typical switch, coil and lamp wiring panels; those are drawings, cited by the records but not transcribed.

## Switch matrix: drive columns

| Column | Drive | Wire | Connector |
| --- | --- | --- | --- |
| 1 | Q1 | GRN-BRN | CN5-P1 |
| 2 | Q2 | GRN-RED | CN5-P3 |
| 3 | Q3 | GRN-ORG | CN5-P4 |
| 4 | Q4 | GRN-YEL | CN5-P5 |
| 5 | Q5 | GRN-BLK | CN5-P6 |
| 6 | Q6 | GRN-BLU | CN5-P7 |
| 7 | Q7 | GRN-VIO | CN5-P8 |
| 8 | Q8 | GRN-GRY | CN5-P9 |

## Switch matrix: return rows

| Row | IC | Wire | Connector |
| --- | --- | --- | --- |
| 1 | U400 | WHT-BRN | CN7-P9 |
| 2 | U400 | WHT-RED | CN7-P8 |
| 3 | U400 | WHT-ORG | CN7-P7 |
| 4 | U400 | WHT-YEL | CN7-P6 |
| 5 | U401 | WHT-GRN | CN7-P5 |
| 6 | U401 | WHT-BLU | CN7-P3 |
| 7 | U401 | WHT-VIO | CN7-P2 |
| 8 | U401 | WHT-GRY | CN7-P1 |

## Switch matrix: cells

A blank location or part cell is printed blank. The DOTS column says whether the cell carries the Diode On Terminal Strip badge.

| Switch | Location | Name | Part | DOTS |
| --- | --- | --- | --- | --- |
| 1 | Cabinet Side | LT BUTTON (UK ONLY) | 180-5160-00 | no |
| 2 | Coin Door | 4TH COIN SLOT | 180-5204-00 | no |
| 3 | Coin Door | 6TH COIN SLOT | Future Use | no |
| 4 | Coin Door | RIGHT COIN SLOT | 180-5204-00 | no |
| 5 | Coin Door | CENTER COIN SLOT / DBA | 180-5204-00 | no |
| 6 | Coin Door | LEFT COIN SLOT | 180-5204-00 | no |
| 7 | Coin Door | 5TH COIN SLOT | Future Use | no |
| 8 | Cabinet Side | RT BUTTON (UK ONLY) | 180-5160-00 | no |
| 9 | Below P/F | LEFT VUK | 180-5116-01 | yes |
| 10 | Below P/F | STANDUP | 515-6027-08 | no |
| 11 | Below P/F | 4-BALL TROUGH #1 (LEFT) | 180-5119-02 | no |
| 12 | Below P/F | 4-BALL TROUGH #2 | 180-5119-02 | no |
| 13 | Below P/F | 4-BALL TROUGH #3 | 180-5119-02 | no |
| 14 | Below P/F | 4-BALL TROUGH VUK OPTO | See Sw. 14 Note | no |
| 15 | Below P/F | 4-BALL STACKING OPTO | See Sw. 15 Note | no |
| 16 | Below P/F | SHOOTER LANE | 180-5157-00 | no |
| 17 | Above P/F | SWORD LOCK HIGH | 180-5119-02 | no |
| 18 | Above P/F | SWORD LOCK MID | 180-5119-02 | no |
| 19 | Above P/F | SWORD LOCK LOW | 180-5119-02 | no |
| 20 | Below P/F | RIGHT ORBIT LOW | 500-6227-02 | no |
| 21 | Above P/F | RIGHT ORBIT HI | 180-5190-28 | no |
| 22 | Above P/F | RAIL RAMP EXIT | 180-5197-00 | no |
| 23 | Above P/F | RIGHT RAMP TARGET | 515-6027-08 | no |
| 24 | Above P/F | RIGHT RAMP MADE | 180-5198-00 | no |
| 25 | Above P/F | RIGHT RAMP ENTER | 180-5010-01 | yes |
| 26 | *(blank)* | NOT USED | *(blank)* | no |
| 27 | *(blank)* | NOT USED | *(blank)* | no |
| 28 | Above P/F | BALROG HIT | 180-5119-00 | no |
| 29 | Below P/F | PALANTIR | 515-5162-08 | no |
| 30 | Below P/F | RIGHT VUK | 180-5116-01 | yes |
| 31 | Below P/F | BALROG OPEN | 180-5119-02 | no |
| 32 | Below P/F | BALROG CLOSED | 180-5119-02 | no |
| 33 | Mini-P/F | MINI PF U.L. | 180-5057-00 | no |
| 34 | Mini-P/F | MINI PF U.R. | 180-5057-00 | no |
| 35 | Mini-P/F | MINI PF L.L. | 180-5057-00 | no |
| 36 | Mini-P/F | MINI PF L.R. | 180-5057-00 | no |
| 37 | Below P/F | LEFT ORBIT LOW | 500-6227-02 | no |
| 38 | Below P/F | LEFT ORBIT HI | 500-6227-02 | no |
| 39 | Below P/F | LEFT RAMP ENTER | 500-6227-02 | no |
| 40 | Above P/F | LEFT RAMP MADE | 180-5010-01 | no |
| 41 | Below P/F | TOP VUK | See Sw. 41 Note | no |
| 42 | Above P/F | INNER LOOP | 180-5190-28 | no |
| 43 | Below P/F | LEFT TOP LANE | 500-6227-02 | no |
| 44 | Below P/F | MIDDLE TOP LANE | 500-6227-02 | no |
| 45 | Below P/F | RIGHT TOP LANE | 500-6227-02 | no |
| 46 | Below P/F | TOP SAUCER | 180-5186-00 | no |
| 47 | Back Panel | RING MADE | See Sw. 47 Note | no |
| 48 | Back Panel | BACK TROUGH | 180-5057-00 | no |
| 49 | Below P/F | LEFT BUMPER | 180-5015-03 | no |
| 50 | Below P/F | RIGHT BUMPER | 180-5015-03 | no |
| 51 | Below P/F | BOTTOM BUMPER | 180-5015-03 | no |
| 52 | Above P/F | SPINNER | 180-5190-28 | no |
| 53 | Below P/F | SPOT RING | 515-5162-08 | no |
| 54 | In Cabinet | START BUTTON | 180-5174-00 | no |
| 55 | In Cabinet | TOURNAMENT START | 180-5174-00 | no |
| 56 | In Cabinet | PLUMB BOB TILT | See Sw. 56 Note | no |
| 57 | Below P/F | LEFT OUTLANE | 500-6227-02 | no |
| 58 | Below P/F | LEFT RETURN LANE | 500-6227-02 | no |
| 59 | Below P/F | LEFT SLINGSHOT | 180-5054-00 (x2) | no |
| 60 | Below P/F | RIGHT OUTLANE | 500-6227-02 | no |
| 61 | Below P/F | RIGHT RETURN LANE | 500-6227-02 | no |
| 62 | Below P/F | RIGHT SLINGSHOT | 180-5054-00 (x2) | no |
| 63 | *(blank)* | NOT USED | *(blank)* | no |
| 64 | *(blank)* | NOT USED | *(blank)* | no |

## Dedicated switches

Ground: `GROUND`, BLK CN6-P1, -P11.

| Input | IC | Wire | Connector | Location | Name | Part |
| --- | --- | --- | --- | --- | --- | --- |
| DS-1 | U206 | GRY-BRN | CN6-P2 | on Cabinet Side | #1 LEFT FLIPPER BUTTON | 180-5160-00 |
| DS-2 | U206 | GRY-RED | CN6-P3 | Below Playfield | #2 LEFT FLIPPER E.O.S (End-of-Stroke) | 180-5149-00 on Flipper |
| DS-3 | U206 | GRY-ORG | CN6-P4 | *(blank)* | #3 RIGHT FLIPPER BUTTON | 180-5160-00 |
| DS-4 | U206 | GRY-YEL | CN6-P6 | Below Playfield | #4 RIGHT FLIPPER E.O.S. (End-of-Stroke) | 180-5149-00 on Flipper |
| DS-5 | U206 | GRY-GRN | CN6-P7 | *(blank)* | NOT USED | *(blank)* |
| DS-6 | U206 | GRY-BLU | CN6-P8 | on Coin Door | #6 VOLUME (RED BUTTON) (In Test: LEFT) | 180-5192-02 |
| DS-7 | U206 | GRY-VIO | CN6-P9 | on Coin Door | #7 SERV. CRED. (GREEN BUTTON) (In Test: RIGHT) | 180-5192-04 |
| DS-8 | U206 | GRY-BLK | CN6-P10 | on Coin Door | #8 BEGIN TEST (BLACK BUTTON) (In Test: ENTER) | 180-5192-00 |

## Switch notes

> Switch Part Notes: ¥ Yen Coin Switch is 180-5091-00. Part Numbers
> which start with 515- or 500- include the bracket, target, and/or housing.
> Sw. 14, 15, 41 & 47 Part Note: OPTO PC Boards are used as Switches:
> Trans.: 515-0173-00 (Sw. 14 & 15); Receiver: 515-0174-00 (Sw.14&15);
> Transmitter 515-7307-00 (Sw. 41); Receiver 515-7308-00 (Sw. 41);
> Transmitter 500-6746-00 (Sw. 47); Receiver 500-6747-00 (Sw. 47);
> Sw. 56 Part Note: The Switch is comprised of a Hanger Bracket
> (535-5319-00) and Contact Wire (535-7563-01) located in the Cabinet.
> Some Switch Diodes may be located under the playfield, in the Cabinet
> or Backbox or on Terminal Strips, Diode Boards and not on the assemblies.
> DOTS: D iode O n T erminal S trip, see Sec. 5, Chp.2, Playfield Wiring

## Coils detailed chart table

Each group's `Driver Ouput Board` cell is one merged `I/O Power Driver` cell, not repeated below. Rows #12, #14 and #24 are shaded grey; #12 and #14 print no power line, voltage or coil type. The DOTS column says whether the function cell carries the Diode On Terminal Strip badge; the last column, whether the coil-type cell carries the rotation mark that the coil note says lets -00B or -00T be used. Power-line cells printed on two lines are joined with a space.

| # | Function | Drive Transistor | Power Line Color | Power Line Connection | Power Voltage | D.T. Control Line Color | D.T. Control Line Connect | Coil GA-Turn or Bulb Type | DOTS | -00B or -00T |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| #1 | TROUGH UP-KICKER | Q1 | BRN-BLU | J10-P4/5 | 50v DC | BRN-BLK | J8-P1 | 26-1200 / 090-5044-00T | no | yes |
| #2 | AUTO LAUNCH | Q2 | BRN-BLU | J10-P4/5 | 50v DC | RED-BRN | J8-P3 | 24-940 / 090-5036-00T | no | yes |
| #3 | LEFT VUK | Q3 | BRN-BLU | J10-P4/5 | 50v DC | BRN-ORG | J8-P4 | 26-1200 / 090-5044-00B | no | yes |
| #4 | TOP VUK | Q4 | BRN-BLU | J10-P4/5 | 50v DC | BRN-YEL | J8-P5 | 26-1200 / 090-5044-00B | no | yes |
| #5 | RIGHT VUK | Q5 | BRN-BLU | J10-P4/5 | 50v DC | GRY-BLK | J8-P6 | 26-1200 / 090-5044-00B | no | yes |
| #6 | RING MAGNET | Q6 | VIO-YEL | J10-P3 | 50v DC | BRN-BLU | J8-P7 | 20½-480 / 090-5064-02 | no | yes |
| #7 | RIGHT TOWER | Q7 | BRN-BLU | J10-P4/5 | 50v DC | BRN-VIO | J8-P8 | 23-800 / 090-5001-NL | yes | no |
| #8 | LOOP DIVERTER | Q8 | `GRY-YEL~3A Fuse~BRN-BLU` | J10-P1/2 | 50v DC | BRN-GRY | J8-P9 | 22-1080 / 090-5032-00T | no | yes |
| #9 | LEFT BUMPER | Q9 | BRN-BLU | J10-P4/5 | 50v DC | GRY-YEL | J9-P1 | 26-1200 / 090-5044-00T | no | yes |
| #10 | RIGHT BUMPER | Q10 | BRN-BLU | J10-P4/5 | 50v DC | BLU-RED | J9-P2 | 26-1200 / 090-5044-00T | no | yes |
| #11 | BOTTOM BUMPER | Q11 | BRN-BLU | J10-P4/5 | 50v DC | BLU-ORG | J9-P4 | 26-1200 / 090-5044-00T | no | yes |
| #12 | OPTIONAL SHAKER MOTOR | Q12 | *(blank)* | *(blank)* | *(blank)* | BLU-YEL | J9-P5 | *(blank)* | no | no |
| #13 | ORBIT PIN | Q13 | YEL-BLU | J7-P1 | 20v DC | BLU-GRN | J9-P6 | 26-1200 / 090-5044-00B | no | yes |
| #14 | NOT USED NC J9-P7 | Q14 | *(blank)* | *(blank)* | *(blank)* | BLU-BLK | J9-P7 | *(blank)* | no | no |
| #15 | LEFT FLIPPER (50v YEL/BLK) | Q15 | `GRY-YEL~3A Fuse~YEL-BLK` | J10-P1/2 | 50v DC | ORG-GRY | J9-P8 | 22-900 / 090-5020-20T | no | yes |
| #16 | RIGHT FLIPPER (50v YEL/BLK) | Q16 | `BLU-YEL~3A Fuse~YEL-BLK` | J10-P1/2 | 50v DC | BRN-ORG | J9-P9 | 22-900 / 090-5020-20T | no | yes |
| #17 | LEFT SLINGSHOT | Q17 | YEL-BLU | J7-P1 | 20v DC | VIO-BRN | J7-P2 | 23-800 / 090-5001-00T | no | yes |
| #18 | RIGHT SLINGSHOT | Q18 | YEL-BLU | J7-P1 | 20v DC | VIO-RED | J7-P3 | 23-800 / 090-5001-00T | no | yes |
| #19 | TOP SAUCER | Q19 | YEL-BLU | J7-P1 | 20v DC | VIO-ORG | J7-P4 | 26-1200 / 090-5044-00B | no | yes |
| #20 | BALROG MOTOR RELAY | Q20 | YEL-BLU | J7-P1 | 20v DC | VIO-YEL | J7-P6 | DC Relay / 520-5066-00 | no | no |
| #21 | SWORD LOCK RELEASE | Q21 | YEL-BLU | J7-P1 | 20v DC | VIO-GRN | J7-P7 | 27-1500 / 090-5004-00T | no | yes |
| #22 | BALROG MOTOR | Q22 | YEL-BLU | J7-P1 | 20v DC | VIO-BLU | J7-P8 | Motor / 041-5088-01 | no | no |
| #23 | FLASH: HELMS DEEP LT | Q23 | YEL-ORG | J6-P10 | 20v DC | VIO-BLK | J7-P9 | #906 Bulb / 165-5004-00 | no | no |
| #24 | OPTIONAL COIL (KNOCKER) | Q24 | RED | J16-P7 | 5v DC | VIO-GRY | J7-P10 | Opt. 5v | no | no |
| #25 | FLASH: POPS X3 | Q25 | YEL-ORG | J6-P10 | 20v DC | BLK-BRN | J6-P1 | #906 Bulb / 165-5004-00 | no | no |
| #26 | FLASH: RING | Q26 | YEL-ORG | J6-P10 | 20v DC | BLK-RED | J6-P2 | #906 Bulb / 165-5004-00 | no | no |
| #27 | FLASH: BACK PANEL | Q27 | YEL-ORG | J6-P10 | 20v DC | BLK-ORG | J6-P3 | #906 Bulb / 165-5004-00 | no | no |
| #28 | FLASH: HELMS DEEP RT | Q28 | YEL-ORG | J6-P10 | 20v DC | BLU-BLK | J6-P4 | #906 Bulb / 165-5004-00 | no | no |
| #29 | FLASH: RINGWRAITH | Q29 | YEL-ORG | J6-P10 | 20v DC | BLK-GRN | J6-P5 | #906 Red / 165-5004-02 | no | no |
| #30 | FLASH: SWORD | Q30 | YEL-ORG | J6-P10 | 20v DC | BLK-BLU | J6-P6 | #906 Bulb / 165-5004-00 | no | no |
| #31 | FLASH: DESTROY THE RING | Q31 | YEL-ORG | J6-P10 | 20v DC | BLK-VIO | J6-P7 | #89 Bulb / 165-5000-89 | no | no |
| #32 | FLASH: BALROG | Q32 | YEL-ORG | J6-P10 | 20v DC | BLK-GRY | J6-P8 | #89 Bulb / 165-5000-89 | no | no |

The note under the flasher rows, its last parenthesis printed in red: `Note: In Test Flash Lamps Menu ("Flash" Icon), Flashers tested are all Flash Lamps located between Q1-Q32 (This Game: Q14, Q23 & Q25-Q27, Q29-Q32)`. It lists Q14 and omits Q28, the 2003 machine's flasher set: the owner did not update it with the rows above it.

## Auxiliary (UK only)

Driver board, one merged cell: `UK 3X Trans. Driver Board`.

| Aux | Function | Drive Transistor | Power Line Color | Power Line Connection | Power Voltage | D.T. Control Line Color | D.T. Control Line Connect | Coil GA-Turn | -00B or -00T |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AUX 1 | LEFT UP/DOWN POST | Q1 | BRN | J7-P1 | 20v DC | WHT | J2-P3 | 26-1200 / 090-5044-00T | yes |
| AUX 2 | CENTER UP/DOWN POST | Q2 | BRN | J7-P1 | 20v DC | RED | J2-P4 | 23-1100 / 090-5030-00T | yes |
| AUX 3 | RIGHT UP/DOWN POST | Q3 | BRN | J7-P1 | 20v DC | ORG | J2-P7 | 26-1200 / 090-5044-00T | yes |

> ↻ Coil Note: ↻ Either -00B or -00T can be used for coil replacements. B/T listed is preferable for easier diode access & may differ on game.

## Lamp matrix: columns (18v)

| Column | IC | Wire | Connector |
| --- | --- | --- | --- |
| 1 | U17 | YEL-BRN | J13-P9 |
| 2 | U16 | BLK-YEL | J13-P8 |
| 3 | U15 | GRN-ORG | J13-P7 |
| 4 | U14 | YEL-BLK | J13-P6 |
| 5 | U13 | GRY-BLK | J13-P5 |
| 6 | U12 | GRY-RED | J13-P4 |
| 7 | U11 | BLU-WHT | J13-P3 |
| 8 | U10 | YEL-GRY | J13-P1 |

## Lamp matrix: rows (ground)

| Row | Transistor | Wire | Connector |
| --- | --- | --- | --- |
| 1 | Q33 | RED-BRN | J12-P1 |
| 2 | Q34 | BRN-BLK | J12-P2 |
| 3 | Q35 | BRN-BLK | J12-P3 |
| 4 | Q36 | ORG-YEL | J12-P4 |
| 5 | Q37 | RED-GRN | J12-P5 |
| 6 | Q38 | ORG-VIO | J12-P6 |
| 7 | Q39 | RED-VIO | J12-P8 |
| 8 | Q40 | BRN-BLK | J12-P9 |
| 9 | Q41 | ORG-WHT | J12-P10 |
| 10 | Q42 | RED | J12-P11 |

## Lamp matrix: cells

The chart prints lamp 5's number as `4`; its position, between lamps 4 and 6 in row 1, makes it lamp 5.

| Lamp | Printed number | Bulb | Name |
| --- | --- | --- | --- |
| 1 | 1 | #555 | ( K ) EEP |
| 2 | 2 | #555 | K ( E ) EP |
| 3 | 3 | #555 | KE ( E ) P |
| 4 | 4 | #555 | KEE ( P ) |
| 5 | 4 | #555 | THE FELLOWSHIP OF THE RING |
| 6 | 6 | #555 | THE TWO TOWERS |
| 7 | 7 | #555 | THE RETURN OF THE KING |
| 8 | 8 | #555 | SHOOT AGAIN |
| 9 | 9 | #555 | PIPPIN |
| 10 | 10 | #555 | MERRY |
| 11 | 11 | #555 | SAM |
| 12 | 12 | #555 | ARAGORN |
| 13 | 13 | #555 | FRODO |
| 14 | 14 | #555 | GANDALF |
| 15 | 15 | #555 | LEGOLAS |
| 16 | 16 | #555 | GIMLI |
| 17 | 17 | #555 | BOROMIR |
| 18 | 18 | #555 | MYSTERY |
| 19 | 19 | #555 | FRODO ARROW |
| 20 | 20 | #44 | DESTROY RING |
| 21 | 21 | #555 | MODE START |
| 22 | 22 | #555 | PALANTIR |
| 23 | 23 | #44 | PALANTIR GLOBE |
| 24 | 24 | #555 | SPOT RING |
| 25 | 25 | #555 | PIPPIN ARROW |
| 26 | 26 | #555 | GIFT OF THE ELVES |
| 27 | 27 | #555 | LIGHT EXTRA BALL |
| 28 | 28 | #555 | RING MULTIBALL |
| 29 | 29 | #555 | BIG POINTS |
| 30 | 30 | #555 | LIGHT SPECIAL |
| 31 | 31 | #555 | SUPER RING FRENZY |
| 32 | 32 | #555 | 2X SCORING |
| 33 | 33 | #555 | LEGOLAS ARROW |
| 34 | 34 | #555 | L RAMP MAN RING |
| 35 | 35 | #555 | L RAMP DWARF RING |
| 36 | 36 | #555 | L RAMP ELF RING |
| 37 | 37 | #555 | GANDALF ARROW |
| 38 | 38 | #555 | C LOOP MAN RING |
| 39 | 39 | #555 | C LOOP DWARF RING |
| 40 | 40 | #555 | C LOOP ELF RING |
| 41 | 41 | #555 | GIMLI ARROW |
| 42 | 42 | #555 | EXTRA BALL |
| 43 | 43 | #555 | GOLLUM MULTIBALL |
| 44 | 44 | #555 | SPECIAL |
| 45 | 45 | #555 | MERRY ARROW |
| 46 | 46 | #555 | R ORBIT MAN RING |
| 47 | 47 | #555 | R ORBIT DWARF RING |
| 48 | 48 | #555 | R ORBIT ELF RING |
| 49 | 49 | #555 | ARAGORN ARROW |
| 50 | 50 | #555 | R RAMP MAN RING |
| 51 | 51 | #555 | R RAMP DWARF RING |
| 52 | 52 | #555 | R RAMP ELF RING |
| 53 | 53 | #555 | LOCK |
| 54 | 54 | #555 | LANES |
| 55 | 55 | #555 | TOWER |
| 56 | 56 | #555 | FLIPPER |
| 57 | 57 | #555 | ( O ) RC |
| 58 | 58 | #555 | O ( R ) C |
| 59 | 59 | #555 | OR ( C ) |
| 60 | 60 | #555 Grn. | POTD U.L. |
| 61 | 61 | #555 Grn. | POTD U.R. |
| 62 | 62 | #555 Grn. | POTD L.L. |
| 63 | 63 | #555 Grn. | POTD L.R. |
| 64 | 64 | #44 | SHOOTER LANE #1 BOT |
| 65 | 65 | #44 | SHOOTER LANE #2 |
| 66 | 66 | #44 | SHOOTER LANE #3 |
| 67 | 67 | #44 | SHOOTER LANE #4 |
| 68 | 68 | #44 | SHOOTER LANE #5 |
| 69 | 69 | #44 | SHOOTER LANE #6 |
| 70 | 70 | #44 | SHOOTER LANE #7 |
| 71 | 71 | #44 | SHOOTER LANE #8 |
| 72 | 72 | #44 | SHOOTER LANE #9 TOP |
| 73 | 73 | #44 | ESCAPE THE RINGWRAITHS |
| 74 | 74 | #44 | GANDALF VS SARUMAN |
| 75 | 75 | #44 | WARG ATTACK |
| 76 | 76 | #44 | WAR OF THE ENTS |
| 77 | 77 | #44 | BATTLE WITH SHELOB |
| 78 | 78 | #44 | DESTROY THE WITCH-KING |
| 79 | 79 | #555 | TOURNAMENT BUTTON |
| 80 | 80 | #555 | START BUTTON |

## Lamp notes

> Lamp Part Notes: 555 Bulb Clear = 165-5002-00. #555 Bulb Green =
> 165-5054-04 . #44 Bulb Clear = 165-5000-44. See Section 4, Chapter 1,
> Parts Identification and Location, Pages 72-74 for more details on bulbs and
> corresponding sockets.
> Some Lamp Diodes may be located under the playfield, in the Cabinet or
> Backbox on Terminal Strips and not on or with the Lamp Socket.
> DOTS: Diode On Terminal S trip, see Sec. 5, Chapter 2, Playfield Wiring.
