# Table 4. Solenoid Connection

Source: Firepower II Service Manual 16-521-101, July 1983, PDF page 16,
printed page 20; PDF SHA-256
`c601834cd57c8cf01423355304d487f3143d92ef1374187344d264eab7e6e6d8`.
Method: manual transcription visually checked by the curator
against the native raster. The complete table and notes follow; [blank] denotes
a genuinely empty cell, not an inferred repeated value. Line breaks in part
numbers are joined. Asterisks on 17-22 are preserved.

| SOL. NO. | FUNCTION | WIRE COLOR | CONNECTIONS | DRIVER TRANS. | SOLENOID PART NO. |
| --- | --- | --- | --- | --- | --- |
| 01 | Outhole | GRY-BRN | 2P11-4, 8P3-1 | Q15 | SG1-23-850-DC |
| 02 | Ball Ramp Thrower | GRY-RED | 2P11-5, 8P3-2 | Q17 | SA3-23-850-DC |
| 03 | Eject Hole | GRY-ORN | 2P11-7, 8P3-3 | Q19 | SG1-23-850-DC |
| 04 | Orbit Complete Flash Lamps | GRY-YEL | 2P11-8, 8P3-4 | Q21 | Type 83 |
| 05 | Not Used | GRY-GRN | 2P11-9, 8P3-5 | Q23 | [blank] |
| 06 | Not Used | GRY-BLU | 2P11-3, 8P3-6 | Q25 | [blank] |
| 07 | Not Used | GRY-VIO | 2P11-2, 8P3-7 | Q27 | [blank] |
| 08 | Not Used | GRY-BLK | 2P11-1, 8P3-8 | Q29 | [blank] |
| 09 | Not Used | BRN-BLK | 2P9-9, 8P3-9 | Q31 | [blank] |
| 10 | Not Used | BRN-RED | 2P9-7, 8P3-10 | Q33 | [blank] |
| 11 | General Illumination Relay | BRN-ORN | 2P9-1, 3P7-1 | Q35 | 5580-09555 |
| 12 | Not Used | BRN-YEL | 2P9-2, 8P3-12 | Q37 | [blank] |
| 13 | Not Used | BRN-GRN | 2P9-3, 8P3-13 | Q39 | [blank] |
| 14 | Not Used | BRN-BLU | 2P9-4, 8P3-14 | Q41 | [blank] |
| 15 | Bell | BRN-VIO | 2P9-5, 7P1-17 | Q43 | SM-29-1000-DC |
| 16 | Coin Lockout | BRN-GRY | 2P9-6, 7P1-18, 7P2-4 | Q45 | 904218-696 |
| *17 | Left Kicker | BLU-BRN | 2P12-7, 8P3-17 | Q2 | SG1-23-850-DC |
| *18 | Right Kicker | BLU-RED | 2P12-4, 8P3-18 | Q4 | SG1-23-850-DC |
| *19 | Lower Left Jet Bumper | BLU-ORN | 2P12-4, 8P3-19 | Q6 | SG1-23-850-DC |
| *20 | Upper Right Jet Bumper | BLU-YEL | 2P12-6, 8P3-20 | Q8 | SG1-23-850-DC |
| *21 | Upper Left Jet Bumper | BLU-GRN | 2P12-8, 8P3-12 | Q10 | SG1-23-850-DC |
| *22 | Lower Right Jet Bumper | BLU-BLK | 2P12-9, 8P3-22 | Q12 | SG1-23-850-DC |
| [blank] | Right Flipper | BLU-VIO | 2P12-1, 7P1-7 | — | SFL-19-400/30-750-DC |
| [blank] | Left Flipper | BLU-GRY | 2P12-2, 7P1-9 | — | SFL-19-400/30-750-DC |

*NOTES:

1. Special switch connections for solenoids 17 through 21 are as follows:

| Solenoid | Wire | Connections |
| --- | --- | --- |
| 17 | ORN-BRN | 2P13-5, 8P3-24 |
| 18 | ORN-RED | 2P13-3, 8P3-25 |
| 19 | ORN-BLK | 2P13-2, 8P3-26 |
| 20 | ORN-YEL | 2P13-4, 8P3-27 |
| 21 | ORN-GRY | 2P13-8, 8P3-28 |

2. Flipper button connections are as follows:

| Button | Wire | Connections |
| --- | --- | --- |
| Right | ORN-VIO | 2P12-1, 7P1-7 |
| Left | ORN-GRY | 2P12-2, 7P1-9 |

3. Sol. 16 is Coin-Co part number.
4. Typical wiring for solenoids and special switches follows: the drawing places
   a diode across a coil fed by RED (B+); its second sketch shows a normally open
   switch to BLK (GND) with a series resistor/capacitor branch across the contact.

The note really stops at 21 and does not print a row for 22. Do not infer it in
this transcription. The solenoid wiring drawing on PDF page 52 supplies all six
special-switch rows. Table 4 repeats 2P12-4 for 18 and 19, prints 8P3-12 for 21,
and uses BLU-GRN/BLU-BLK for 21/22 where the schematic reverses those colors.
These are wiring-detail disagreements, not different coil identities.

Switch Test (same page): Auto-Up + Advance from Solenoid Test selects Test 03.
Stuck switches cycle in the Master/Match display with sound. Opening each
removes its number; with all open the Match display is blank and sound stops.
Operating a switch produces a sound and momentarily shows its number in the
ball-in-play display. Several reported in one row suggest a grounded row;
several columns suggest a short between column wires. If Test 03 passes but
play has matrix trouble, disconnect 2P5 and 2P7, recheck, then run CPU Self-Test;
a cleared problem points to a short between lamp matrix and bumper brackets.
