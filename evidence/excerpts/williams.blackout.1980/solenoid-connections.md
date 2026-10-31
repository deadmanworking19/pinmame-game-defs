# Williams Blackout (game 495) - Solenoid connections

Sources:

- Instruction Booklet 16P-495-103 (`Williams_1980_Blackout_Operators_Handbook.pdf`), PDF page 9 / printed 9, Table 3 Solenoid Connections, and PDF page 8 / printed 8, Figure 3 Playfield Solenoid Locations and Solenoid Chart.
- Instruction Manual and Drawing Set (`Williams_1980_Blackout_Manual_with_paginated_schematics.pdf`), PDF page 21, right half / printed 25, Playfield Solenoid Wiring Diagram; PDF page 21, left half / printed 24, Cabinet Wiring Diagram (cabinet coils).

## Table 3. Solenoid Connections (booklet, printed page 9)

Every row and column as printed. A `-` is a printed dash; an empty cell is blank on the page.

| SOL. NO. | FUNCTION | WIRE COLOR | CONNECTIONS | DRIVER TRANS. | SOLENOID PART NO. |
|---|---|---|---|---|---|
| 01 | Ball Release | GRY-BRN | 2P11-4, 8P3-17 | Q15 | SA-23-850-DC |
| 02 | Not Used | GRY-RED | 2P11-5, 8P3-18 | Q17 | - |
| 03 | Not Used | GRY-ORN | 2P11-7, 8P3-19 | Q19 | - |
| 04 | Center 3-Bank Reset | GRY-YEL | 2P11-8, 8P3-20 | Q21 | SA3-23-850-DC |
| 05 | Top 3-Bank Reset | GRY-GRN | 2P11-9, 8P3-21 | Q23 | SA3-23-850-DC |
| 06 | Eject Hole | GRY-BLU | 2P11-3, 8P3-22 | Q25 | SG-23-850-DC |
| 07 | Not Used | GRY-VIO | 2P11-2, 8P3-23 | Q27 | - |
| 08 | Not Used | GRY-BLK | 2P11-1, 8P3-24 | Q29 | - |
| 09 | Sound | BRN-BLK | 2P9-9, 10P3-3 | Q31 | - |
| 10 | Sound | BRN-RED | 2P9-7, 10P3-2 | Q33 | - |
| 11 | Sound | BRN-ORN | 2P9-1, 10P3-5 | Q35 | - |
| 12 | Sound | BRN-YEL | 2P9-2, 10P3-4 | Q37 | - |
| 13 | Sound | BRN-GRN | 2P9-3, 10P3-7 | Q39 | - |
| 14 | Credit Knocker | BRN-BLU | 2P9-4, 7P1-16 | Q41 | SA2-23-850-DC |
| 15 | Special Relay | BRN-VIO | 2P9-5, 6P2 | Q43 | 5A-9384 |
| 16 | Coin Lockout | BRN-GRY | 2P9-6, 7P1-18, 7P2-4 | Q45 | SM-35-4000-DC |
| *17 | Left Jet Bumper | BLU-BRN | 2P12-7, 8P3-11 | Q2 | SG-23-850-DC |
| *18 | Right Jet Bumper | BLU-RED | 2P12-4, 8P3-12 | Q4 | SG-23-850-DC |
| *19 | Bottom Jet Bumper | BLU-ORN | 2P12-3, 8P3-13 | Q6 | SG-23-850-DC |
| *20 | Left Kicker | BLU-YEL | 2P12-6, 8P3-14 | Q8 | SG-23-850-DC |
| *21 | Right Kicker | BLU-GRN | 2P12-8, 8P3-15 | Q10 | SG-23-850-DC |
| *22 | Not Used | BLU-BLK | 2P12-9, 8P3-16 | Q12 | - |
| * | Right Flipper | BLU-VIO | 7P1-8, 8P3-3 | - | SFL-19-400/30-750-DC |
| * | Left Flipper | BLU-GRY | 7P1-10, 8P3-4 | - | SFL-19-400/30-750-DC |

Row 02 carries a stray subscript mark after `2P11-5` on the scan; it is not read as part of the connection.

NOTES (printed under the table):

1. Special switch connections for solenoids 17 through 22 are as follows:
   17 - ORN-BRN - 2P13-5, 8P3-5;
   18 - ORN-RED - 2P13-3, 8P3-6;
   19 - ORN-BLK - 2P13-2, 8P3-7;
   20 - ORN-YEL - 2P13-4, 8P3-8;
   21 - ORN-GRN - 2P13-8, 8P3-9;
   22 - ORN-BLU - 2P13-9, 8P3-10
2. Flipper button connections are as follows:
   Right - ORN-VIO - 2P12-1, 7P1-7;
   Left - ORN-GRY - 2P12-2, 7P1-9
3. Typical wiring for solenoids and special switches: (a drawing, described) a coil with a diode on RED (B+), and a special switch with a resistor and a capacitor on BLK (GRD).

## Figure 3. Playfield Solenoid Locations and Solenoid Chart (booklet, printed page 8)

| Sol. No. | Function |
|---|---|
| 01 | Ball Release |
| 02 | Not Used |
| 03 | Not Used |
| 04 | Center 3-Bank Drop Targets Reset |
| 05 | Top 3-Bank Drop Targets Reset |
| 06 | Eject Hole |
| 07 | Not Used |
| 08 | Not Used |
| 09 | Sound |
| 10 | Sound |
| 11 | Sound |
| 12 | Sound |
| 13 | Sound |
| 14 | Credit Knocker |
| 15 | Special Relay |
| 16 | Coin Lockout |
| 17 | Left Jet Bumper |
| 18 | Right Jet Bumper |
| 19 | Bottom Jet Bumper |
| 20 | Left Kicker |
| 21 | Right Kicker |
| 22 | Not Used |

The drawing prints playfield callouts 17 and 18 on the two upper jet bumpers (17 left, 18 right), 19 on the bottom jet bumper, 04 under the center 3-bank below bumper 19, 05 on the top 3-bank at the upper right, 06 at the eject hole on the right side, 20 and 21 on the left and right kickers, and 01 below the outhole, under the apron at the center. No callout is printed for 02, 03, 07-16 or 22.

## Playfield Solenoid Wiring Diagram (drawing set, printed page 25)

Standard drivers, 2J11/2P11 to 8J3/8P3:

| Driver | 2P11 pin | Wire | Solenoid | 8P3 pin | Load drawn |
|---|---|---|---|---|---|
| Q29 | 1 | GRY-BLK | SOL. 8 | 24 | N/C |
| Q27 | 2 | GRY-VIO | SOL. 7 | 23 | N/C |
| Q25 | 3 | GRY-BLU | SOL. 6 | 22 | 8L6 EJECT HOLE, diode 8D135 |
| Q15 | 4 | GRY-BRN | SOL. 1 | 17 | 8L1 BALL RELEASE, diode 8D129 |
| Q17 | 5 | GRY-RED | SOL. 2 | 18 | N/C |
| Q19 | 7 | GRY-ORG | SOL. 3 | 19 | N/C |
| Q21 | 8 | GRY-YEL | SOL. 4 | 20 | 8L4 CENTER 3-BANK RESET, diode 8D132 |
| Q23 | 9 | GRY-GRN | SOL. 5 | 21 | 8L5 TOP 3-BANK RESET, diode 8D133 |

Coil supply: 3J3/3P3-6 RED SOL. B+ to 8P3-1; 3P3-3 BLK GRD. to 8P3-2 (special switch common).

Special drivers, 2J12/2P12 to 8J3/8P3:

| Driver | 2P12 pin | Wire | Solenoid | 8P3 pin | Load drawn |
|---|---|---|---|---|---|
| Q2 | 7 | BLU-BRN | SOL. 17 | 11 | 8L17 LEFT JET BUMPER, diode 8D137 |
| Q4 | 4 | BLU-RED | SOL. 18 | 12 | 8L18 RIGHT JET BUMPER, diode 8D138 |
| Q6 | 3 | BLU-ORG | SOL. 19 | 13 | 8L19 BOTTOM JET BUMPER, diode 8D139 |
| Q8 | 6 | BLU-YEL | SOL. 20 | 14 | 8L20 LEFT KICKER, diode 8D140 |
| Q10 | 8 | BLU-GRN | SOL. 21 | 15 | 8L21 RIGHT KICKER, diode 8D143 |
| Q12 | 9 | BLU-BLK | SOL. 22 | 16 | N/C |

2P12 pins 1 and 2 run from the driver board's relay Z1 contact to ground: `ORG-VIO 1 LEFT FLIPPER` and `ORG-GRY 2 RIGHT FLIPPER`.

Special switches, 2J13/2P13 to 8J3/8P3:

| Special switch input | 2P13 pin | Wire | 8P3 pin | Switch drawn |
|---|---|---|---|---|
| SOL. 17 SPEC. SW. | 5 | ORG-BRN | 5 | 8SW65 LEFT JET BUMPER, with 8C1 and 8R1 (printed 22 and 100) |
| SOL. 18 SPEC. SW. | 3 | ORG-RED | 6 | 8SW66 RIGHT JET BUMPER, with 8C2 and 8R2 |
| SOL. 19 SPEC. SW. | 2 | ORG-BLK | 7 | 8SW67 BOTTOM JET BUMPER, with 8C3 and 8R3 |
| SOL. 20 SPEC. SW. | 4 | ORG-YEL | 8 | 8SW68, two contacts drawn in parallel, with 8C4 and 8R4 |
| SOL. 21 SPEC. SW. | 8 | ORG-GRN | 9 | 8SW69, two contacts drawn in parallel, with 8C5 and 8R5 |
| SOL. 22 SPEC. SW. | 9 | ORG-BLU | 10 | N/C |

Flippers (drawn PART OF CABINET): the RIGHT FLIPPER BUTTON on 7J1/7P1 pins 9 and 10, and the LEFT FLIPPER BUTTON on pins 8 and 7. BLU-GRY 7P1-10 to 8P3-4 to 8L25 RIGHT FLIPPER, diode 8D148; BLU-VIO 7P1-8 to 8P3-3 to 8L24 LEFT FLIPPER, diode 8D146. FLIPPER B+ FROM POWER SUPPLY: 3J3/3P3-4 BLU to 8P2/8J2-23 (left flipper) and 3P3-5 BLU to 8P2-24 (right flipper). An end-of-stroke contact is drawn across each flipper coil.

This sheet's flipper sides disagree with Table 3, Table 3's note 2 and the cabinet sheet: they put the right flipper on BLU-VIO 7P1-8, 8P3-3 and its button between 7P1-7 and 7P1-8 (ORN-VIO 2P12-1), and the left flipper on BLU-GRY 7P1-10, 8P3-4 (ORN-GRY 2P12-2), while this sheet labels 2P12-1 LEFT and 8L24 on 8P3-3 LEFT. Both readings are kept literally here.

## Cabinet coils (drawing set, printed page 24)

- 7L14 CREDIT KNOCKER, diode 7D9: +28V RED from 3J3/3P3-7 to 7P1-3; SOL. 14 (Q41) BRN-BLU 2P9-4 to 7P1-16.
- 7L16 COIN LOCKOUT, diode 7D10: 7P2-3 (+28V from 7P1-3); SOL. 16 (Q45) BRN-GRY 2P9-6 to 7P1-18 to 7P2-4.
