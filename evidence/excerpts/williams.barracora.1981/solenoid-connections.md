# Williams Barracora (game 510) - Solenoids

Sources:

- `Williams_1981_Barracora_Operators_Handbook.pdf` (instruction booklet 16P-510-103), PDF page 11 = printed page `11`, `Table 4. Solenoid Connections` with its notes.
- The same booklet, PDF page 10 = printed page `10`, the Solenoid Test text and `Figure 2. Playfield Solenoid Locations and Solenoid Chart`.
- `Williams_1981_Barracora_Instruction_and_Drawing_Set_paginated_schematics_cover_page_missing.pdf`, PDF page 20 = printed page `25`, `Playfield Solenoid Wiring Diagram`.

Method: the 300 dpi native page images were read visually. Every row and column of Table 4 is transcribed in printed order, including the duplicate first row. Capitals, punctuation and asterisks are as printed. A blank cell is written `(blank)`; `--` is a printed dash.

## Table 4. Solenoid Connections (all rows, printed order)

| SOL. NO. | FUNCTION | WIRE COLOR | CONNECTIONS | DRIVER TRANS. | SOLENOID PART NO. |
|---|---|---|---|---|---|
| 01 | Top Eject Hole | GRY-BRN | 2P11-4, 8P3-1 | Q15 | SG-23-850-DC |
| 01 | B Drop Target Reset | GRY-BRN | 2P11-4, 8P3-1 | Q15 | SA5-24-750-DC |
| 02 | A Drop Target Reset | GRY-RED | 2P11-5, 8P3-2 | Q17 | SA5-24-750-DC |
| 03 | RR Drop Target Reset | GRY-ORN | 2P11-7 | Q19 | SA5-24-750-DC |
| 04 | A Drop Target Reset | GRY-YEL | 2P11-8, 8P3-4 | Q21 | SA5-24-750-DC |
| 05 | C Drop Target Reset | GRY-GRN | 2P11-9, 8P3-5 | Q23 | SA5-24-750-DC |
| 06 | O Drop Target Reset | GRY-BLU | 2P11-3, 8P3-6 | Q25 | SA5-24-750-DC |
| 07 | R Drop Target Reset | GRY-VIO | 2P11-2, 8P3-7 | Q27 | SA5-24-750-DC |
| 08 | A Drop Target Reset | GRY-BLK | 2P11-1, 8P3-8 | Q29 | SA5-24-750-DC |
| 09 | B-A-RR Drop Target Bank Release | BRN-BLK | 2P9-9, 8P3-9 | Q31 | SA6-24-750-DC |
| 10 | A-C-O-R-A Drop Target Bank Release | BRN-RED | 2P9-7, 8P3-10 | Q33 | SA6-24-750-DC |
| 11 | Ball Release | BRN-ORN | 2P9-1, 8P3-11 | Q35 | SA3-23-850-DC |
| 12 | Ball Ramp Thrower | BRN-YEL | 2P9-2, 8P3-12 | Q37 | SG1-23-850-DC |
| 13 | Upper Eject Hole | BRN-GRN | 2P9-3, 8P3-13 | Q39 | SG1-23-850-DC |
| 14 | Lower Eject Hole | BRN-BLU | 2P9-4, 8P3-14 | Q41 | SG1-23-850-DC |
| 15 | Bell | BRN-VIO | 2P9-5, 7P1-17 | Q43 | SM-29-100-DC |
| 16 | Coin Lockout | BRN-GRY | 2P9-6, 7P1-18, 7P2-4 | Q45 | SM-35-4000-DC |
| 17 | Upper Eject Hole Gate | BLU-BRN | 2P12-7, 8P3-17 | Q2 | SM-35-4000-DC |
| *18 | Left Jet Bumper | BLU-RED | 2P12-4, 8P3-18 | Q4 | SG1-23-850-DC |
| *19 | Right Jet Bumper | BLU-ORN | 2P12-3, 8P3-19 | Q6 | SG1-23-850-DC |
| *20 | Bottom Jet Bumper | BLU-YEL | 2P12-6, 8P3-20 | Q8 | SG1-23-850-DC |
| *21 | Left Kicker | BLU-GRN | 2P12-8, 8P3-21 | Q10 | SG1-23-850-DC |
| *22 | Right Kicker | BLU-BLK | 2P12-9, 8P3-22 | Q12 | SG1-23-850-DC |
| (blank) | Right Flipper | BLU-VIO | 7P1-8, 8P3-34 | -- | SFL-19-400/ 30-750-DC |
| (blank) | Left Flipper | BLU-GRY | 7P1-10, 8P3-32 | -- | SFL-19-400/ 30-750-DC |

The table has no row for 23, 24 or 25.

### Table 4 notes (as printed)

`*NOTES:`

1. Special switch connections for solenoids 18 through 22 are as follows:
   - 18 -- ORN-RED -- 2P13-3, 8P3-25
   - 19 -- ORN-BLK -- 2P13-2, 8P3-26
   - 20 -- ORN-YEL -- 2P13-4, 8P3-27
   - 21 -- ORN-GRN -- 2P13-8, 8P3-28
   - 22 -- ORN-BLU -- 2P13-9, 8P3-29
2. Flipper button connections are as follows:
   - Right -- ORN-VIO -- 2P12-1, 7P1-7
   - Left -- ORN-GRY -- 2P12-2, 7P1-9
3. Typical wiring for solenoids and special switches. (A drawing: the coil with a parallel diode between `RED (B+)` and the driver; the special switch with a parallel resistor and capacitor in series to `BLK (GRD)`.)

## Solenoid Test (printed page 10)

1. From Lamp Test depress ADVANCE with the switch set to AUTO-UP. Test 02 should be indicated in the Credits display. The Match display sequences from 01 thru 25. Corresponding solenoids 01 thru 24 are pulsed. Flipper relay is de-energized with subtest 25.
2. To continuously pulse a single solenoid set switch to MANUAL-DOWN. Operate ADVANCE pushbutton sequence through the solenoids one at a time. Set switch to AUTO-UP to resume sequencing.

## Figure 2 solenoid chart (as printed)

| Sol. No. | Function |
|---|---|
| 01 | B Drop Target Reset |
| 02 | A Drop Target Reset |
| 03 | RR Drop Target Reset |
| 04 | A Drop Target Reset |
| 05 | C Drop Target Reset |
| 06 | O Drop Target Reset |
| 07 | R Drop Target Reset |
| 08 | A Drop Target Reset |
| 09 | B-A-RR Drop Target / Bank Release |
| 10 | A-C-O-R-A Drop Target / Bank Release |
| 11 | Ball Release |
| 12 | Ball Ramp Thrower |
| 13 | Upper Eject Hole |
| 14 | Lower Eject Hole |
| 15 | Bell |
| 16 | Coin Lockout |
| 17 | Upper Eject Hole Gate |
| 18 | Left Jet Bumper |
| 19 | Right Jet Bumper |
| 20 | Bottom Jet Bumper |
| 21 | Left Kicker |
| 22 | Right Kicker |

Figure 2's playfield photograph carries callout labels 1-14 and 17-22; there is none for 15 or 16. Labels 13 and 17 are printed at the top left corner, 14 and 18 below them on the left, 1-3 and 9 at the left drop target bank, 4-8 and 10 at the right drop target bank, 21 and 22 at the kickers, 12 at the right above the outlane and 11 at the lower right. The leaders were not traced or measured, and no coordinate in this record comes from this figure.

## Playfield Solenoid Wiring Diagram (drawing set printed page 25)

Driver connectors to playfield connector 8P3/8J3, coil designators and printed coil labels:

| Drive transistor | Driver pin | Wire | Printed `SOL.` | 8P3 pin | Coil | Printed coil label |
|---|---|---|---|---|---|---|
| Q15 | 2J11/2P11-4 | GRY-BRN | SOL. 1 | 1 | 8L1 | B DROP TARGET RESET |
| Q17 | 2J11/2P11-5 | GRY-RED | SOL. 2 | 2 | 8L2 | A DROP TARGET RESET |
| Q19 | 2J11/2P11-7 | GRY-ORN | SOL. 3 | 3 | 8L3 | RR DROP TARGET RESET |
| Q21 | 2J11/2P11-8 | GRY-YEL | SOL. 4 | 4 | 8L4 | A DROP TARGET RESET |
| Q23 | 2J11/2P11-9 | GRY-GRN | SOL. 5 | 5 | 8L5 | C DROP TARGET RESET |
| Q25 | 2J11/2P11-3 | GRY-BLU | SOL. 6 | 6 | 8L6 | O DROP TARGET RESET |
| Q27 | 2J11/2P11-2 | GRY-VIO | SOL. 7 | 7 | 8L7 | R DROP TARGET RESET |
| Q29 | 2J11/2P11-1 | GRY-BLK | SOL. 8 | 8 | 8L8 | A DROP TARGET RESET |
| Q31 | 2J9/2P9-9 | BRN-BLK | SOL. 9 | 9 | 8L9 | B-A-RR DROP TARGET BANK RELEASE |
| Q33 | 2J9/2P9-7 | BRN-RED | SOL. 10 | 10 | 8L10 | A-C-O-R-A DROP TARGET BANK RELEASE |
| Q35 | 2J9/2P9-1 | BRN-ORN | SOL. 11 | 11 | 8L11 | BALL RELEASE |
| Q37 | 2J9/2P9-2 | BRN-YEL | SOL. 12 | 12 | 8L12 | BALL RAMP THROWER |
| Q39 | 2J9/2P9-3 | BRN-GRN | SOL. 13 | 13 | 8L13 | TOP LEFT CORNER EJECT HOLE |
| Q41 | 2J9/2P9-4 | BRN-BLU | SOL. 14 | 14 | 8L14 | UPPER LEFT EJECT HOLE |
| Q2 | 2J12/2P12-7 | BLU-BRN | SOL. 17 | 17 | 8L17 | TOP EJECT HOLE GATE |
| Q4 | 2J12/2P12-4 | BLU-RED | SOL. 18 | 18 | 8L18 | LEFT JET BUMPER |
| Q6 | 2J12/2P12-3 | BLU-ORN | SOL. 19 | 19 | 8L19 | RIGHT JET BUMPER |
| Q8 | 2J12/2P12-6 | BLU-YEL | SOL. 20 | 20 | 8L20 | BOTTOM JET BUMPER |
| Q10 | 2J12/2P12-8 | BLU-GRN | SOL. 21 | 21 | 8L21 | LEFT KICKER |
| Q12 | 2J12/2P12-9 | BLU-BLK | SOL. 22 | 22 | 8L22 | RIGHT KICKER |

- Coil power: `POWER SUPPLY` P/O 3J3/3P3-6 RED `SOL. B+` to 8P3-36, and 3P3-3 BLK `GROUND` to 8P3-35. Each coil carries a parallel diode (8D129-8D138 for 1-10, 8D139-8D142 for 11-14, 8D145-8D150 for 17-22).
- Special switches, from `SOL. 18 SPEC. SW.` to `SOL. 17 SPEC. SW.` on 2J13/2P13: ORN-RED SOL. 18 pin 3 to 8P3-25; ORN-BLK SOL. 19 pin 2 to 8P3-26; ORN-YEL SOL. 20 pin 4 to 8P3-27; ORN-GRN SOL. 21 pin 8 to 8P3-28; ORN-BLU SOL. 22 pin 9 to 8P3-29; ORN-BRN SOL. 17 pin 5 to 8P3-24, which is printed `NC`.
- Special switch contacts: 8SW66 LEFT JET BUMPER, 8SW67 RIGHT JET BUMPER, 8SW68 BOTTOM JET BUMPER, 8SW69 LEFT KICKER, 8SW70 RIGHT KICKER; 8C2-8C6 `22` and 8R2-8R6 `100` beside the contacts. No special contact is drawn for 17.
- Flipper relay: 2J12/2P12-2 ORN-GRY and 2J12/2P12-1 ORN-VIO run to contacts of relay `Z1` on the driver board.
- `PART OF CABINET`: RIGHT FLIPPER BUTTON on 7J1/7P1-7 and 7P1-8, 7P1-8 to 8P3-34; LEFT FLIPPER BUTTON on 7P1-9 and 7P1-10, 7P1-10 to 8P3-32.
- Playfield flippers: 8SW45 LEFT FLIPPER contact with coil 8L25 and diode 8D153; 8SW46 RIGHT FLIPPER contact with coil 8L26 and diode 8D154. `FLIPPER B+ FROM POWER SUPPLY` P/O 3J3/3P3-4 BLU and 3P3-5 GRY to 8P2/8J2-23 and 8J2-24.
- Solenoids 15 and 16 are not on this sheet (cabinet loads; see `cabinet-and-power.md`).

## Notes

- Table 4's first row, `01 Top Eject Hole ... SG-23-850-DC`, repeats solenoid 01's wire, connections and transistor. Figure 2, the wiring sheet and the Test 02 sweep give 01 only as the B Drop Target Reset, and 13 is the eject hole kicker. The row is retained literally.
- Table 4 prints 03 with `2P11-7` and no 8P3 pin; the wiring sheet runs SOL. 3 to 8P3-3.
- The wiring sheet names 13 `TOP LEFT CORNER EJECT HOLE`, 14 `UPPER LEFT EJECT HOLE` and 17 `TOP EJECT HOLE GATE`, where Table 4 and Figure 2 say Upper Eject Hole, Lower Eject Hole and Upper Eject Hole Gate.
- Solenoid 17 is a special-driver output (Q2) without a special switch: its 2P13 special-switch wire ends at a pin printed `NC`.
