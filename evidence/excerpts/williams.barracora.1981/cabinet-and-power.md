# Williams Barracora (game 510) - Cabinet wiring, power wiring and board requirements

Sources, all in `Williams_1981_Barracora_Instruction_and_Drawing_Set_paginated_schematics_cover_page_missing.pdf` unless stated:

- PDF page 18 = printed page `23`, `Cabinet Wiring Diagram`.
- PDF page 11 = printed page `15`, `Power Wiring Diagram` (K1 and fuse area).
- PDF page 1, the foreword's board requirements.
- `Williams_1981_Barracora_Operators_Handbook.pdf` PDF page 1 = printed page `1`, the fuse sentence.

Method: native page images read visually, rotated upright and cropped where the labels are sideways. Labels, capitals and `NC` / `N.C.` markings are as printed. Where a pin could not be read with confidence it is said so rather than completed.

## Cabinet Wiring Diagram (printed 23)

### Solenoid-driven cabinet loads

| Driver | Driver pin | Wire | Cabinet pin | Load as drawn |
|---|---|---|---|---|
| SOL. 14 (Q41) | 2J9/2P9-4 | BRN-BLU | 7P1-3 | 7J1 side printed `NC` |
| SOL. 15 (Q43) | 2J9/2P9-5 | BRN-VIO | 7P1-17 | `7L15 BELL`: coil with diode 7D15; a contact also labelled `7L15` in series with the coil, shunted by `7C1` `0.1µF` |
| SOL. 16 (Q45) | 2J9/2P9-6 | BRN-GRY | 7P1-18, 7J2/7P2-4 | `7L16 COIN LOCKOUT`: one coil with diode 7D16 |

- Coil supply: `POWER SUPPLY +28V` 3J3/3P3-7 RED to 7P1-3 and on to 7J2/7P2-3, feeding 7L15 and 7L16. Both this line and the SOL. 14 line are printed as pin `3` of 7P1.
- Only one coin-lockout coil is drawn.

### Cabinet switches (switch column 1)

- `COL. 1` 2J2/2P2-9 GRN-BRN to 7P1-19 and 7J2/7P2-6; `COL. 2` 2J2/2P2-8 GRN-RED to 7P1-20, whose 7J1 side is printed `NC`.
- Rows from 2J3/2P3 to 7P1: ROW 1 pin 9 WHT-BRN 7P1-21; ROW 2 pin 8 WHT-RED 22; ROW 3 pin 7 WHT-ORN 23; ROW 4 pin 6 WHT-YEL 24; ROW 5 pin 5 WHT-GRN 25; ROW 6 pin 4 WHT-BLU 26; ROW 7 pin 3 WHT-VIO 27; ROW 8 pin 1 WHT-GRY 28. Rows 4-8 continue on 7J2/7P2-8 to 12.

| Switch | Printed label | Row | Diode | Drawn |
|---|---|---|---|---|
| 7SW1 | PLUMB BOB TILT | 1 | 7D1 | open |
| 7SW2 | BALL ROLL TILT | 2 | 7D2 | open |
| 7SW3 | CREDIT BUTTON | 3 | 7D3 | open |
| 7SW4 | RIGHT COIN CHUTE | 4 | 7D4 | open |
| 7SW5 | CENTER COIN CHUTE | 5 | 7D5 | open |
| 7SW6 | LEFT COIN CHUTE | 6 | 7D6 | open |
| 7SW7 | SLAM TILT | 7 | 7D7 | open |
| 7SW8 | HIGH SCORE RESET | 8 | 7D8 | open |

### Flipper buttons and flipper coils

- `FLIPPER GROUND` 2J12/2P12-2 ORN-GRY to 7P1-9 and 2J12/2P12-1 ORN-VIO to 7P1-7.
- `7SW72 RIGHT FLIPPER` between 7P1-7 and 7P1-8; `7SW73 LEFT FLIPPER` between 7P1-9 and 7P1-10. Both drawn open.
- `PLAYFIELD FLIPPER COILS` on 8J3/8P3: pin 3 BLU-VIO to 7P1-8; pin 15 BLK-YEL to 7P1-31 (`NC`); pin 4 BLU-GRY to 7P1-10; pin 9 BLK-BLU to 7P1-30 (`NC`).

### Service switches

| CPU 1J4/1P4 pin | Printed label | Wire | Cabinet pin | Switch |
|---|---|---|---|---|
| 1 | MEM PROT. | BLK-RED | 7P1-34 | `7SW76 MEMORY PROTECT INTERLOCK`, to the ground line |
| 2 | GROUND | WHT | 7P1-4, 7J2/7P2-13 | common |
| 3 | ADVANCE | GRN | 7P1-5, 7P2-14 | `7SW75 ADVANCE` |
| 4 | AUTO./MAN. | BLU | 7P1-6, 7P2-15 | `7SW74` with positions `AUTO-UP` and `MANUAL-DOWN` |

### Lighting and sound

- `GENERAL ILLUMINATION`: three bulbs drawn across 7J2/7P2-1 and 7P2-2, fed from 7P1-1 and 7P1-2. These two lines drop to the 8J8/8P8 block; the read did not resolve which 8J8 pins they reach.
- `POWER SUPPLY 6.3 VAC` 3J8/3P8-4 YEL and 3P8-9 WHT-YEL enter the 8J8/8P8 block, where 8P8 pins 6 (WHT-YEL), 3 (YEL), 2 and 5 are printed and one bulb labelled `PLAYFIELD` is drawn.
- `SOUND BOARD`: 10J4/10P4 AUDIO OUT 2, AUDIO IN 1, SHIELD 4 to `7R1 REMOTE VOLUME`; 10J2/10P2 AUDIO 2 BLK-BRN to 7P1-33 and GND 3 BLACK to 7P1-32, to the `SPEAKER`.

## Power Wiring Diagram (printed 15), relay K1 and fuses

- `K1 SPECIAL RELAY`: coil with a parallel diode between 3J7-1 and 3J7-3. On the harness side 3P7-1 is labelled `BRN-ORN` and `N.C.`, 3P7-2 `N.C.` and 3P7-3 `N.C.`
- K1's contact is drawn closed in the 3J9/3P9-1 line. 3J9/3P9-2 carries fuse `F6` `20A`.
- Fuses read on the same sheet: `F1` 0.25ASB, `F2` 2.5ASB (solenoid B+, +28VDC), `F3` 8ASB (+18VDC), `F4` 10A (flipper B+), `F5` 7ASB, `F6` 20A (6.3 VAC).

## Board requirements (drawing set foreword, PDF page 1)

- CPU: Revision level 7 CPU boards or later; blue-labelled Flipper and Game ROMs; jumpers W3, W10, W11, W14, W17, W19, W20, W22 connected and W4, W9, W12, W15, W16, W18, W21, W23 removed.
- Driver Board: zero-ohm resistors or wire jumpers (W9-W16) in place of switch matrix drive series resistors R204-R211.
- Sound: ROM operation with Sound ROM 4 (jumpers W3, W5, W7, W9, W10, W12, W15 connected; W2, W4, W6, W8, W11, W13 removed).
- Power Supply: Model D 8345 board required (equipped with relay); `Fuse F4 (20A SB) for flipper solenoids and magnets must be installed.`
- Display: Model C 8363 Master Display and 7-digit Slave Displays.

The instruction booklet's page 1 instead reads `Fuse F4 (10A SB) for flipper solenoids must be installed.`

## Notes

- The K1 coil's harness pins are all printed `N.C.`, so on this game nothing drives K1 and its contact stays closed. `BRN-ORN` is the colour of the 2P9-1 driver line, which on Barracora is solenoid 11 Ball Release (8P3-11, `solenoid-connections.md`).
- The SOL. 14 branch to 7P1-3 (`NC`) and the flipper-coil pins 8P3-3/15/4/9 on this sheet do not match the playfield solenoid sheet, which runs SOL. 14 to 8P3-14 and the flipper buttons to 8P3-34 and 8P3-32 (as Table 4 does), and uses 8P3-3 for SOL. 3.
- F4 is 10A on the power sheet and in the booklet, 20A SB in the drawing-set foreword.
