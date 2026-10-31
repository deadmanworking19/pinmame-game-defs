# The Adventures of Rocky and Bullwinkle and Friends (Data East 1993) - Coil and flash-lamp drivers, Flipper Solenoids and the coil schematics

Transcribed by hand from native-resolution (300 dpi) renders of printed pages 28, 29, 46 and 47 (PDF 32, 33, 51-52 and 53-54) of the IPDB-hosted scan `Data_East_1993_Adventures_of_Rocky_and_Bullwinkle_and_Friends_Full_Manual.pdf`. OCR text was used only to locate the pages; every cell below was read from the render.

Printed page 28 states: `Twenty-Two regular (pulsed under microprocessor control) coil drivers are provided to switch ground to coils. The Left/Right relay is used in conjunction with drives 1 through 8 to switch +32 volts between coils or flash lamps; these sets are termed "left" and "right". This relay is located on the PPB board which provides isolation diodes and current limiting resistors. This effectively provides 29 regular coils.` It names the Flash Lamp test (`All Flash lamps will fire randomly`), the Automatic Test (`Player 1 and 2 displays indicate ALL COILS. The test pulses each regular solenoid or flash lamp sequentially with the coil/flash lamp name indicated in the Player 1 and 2 displays and the wire colors in the Player 3 and 4 displays.`), the Select Coil test (`Operate either Flipper push-button switch to select the coil or flash lamp to be tested. With the desired drive number indicated in the Player 4 display, depress the START push-button switch to cause it to be pulsed repeatedly.`) and `RETURN TO GAME OVER` (`From the Select Coil test, depress the STEP push-button switch once.`).

Unlike later Data East manuals, this one prints no table for drives 1-16; their names, transistors, wires and connectors come from the coil chart schematic on printed page 29 and the Playfield Coil / Flash Lamp Wiring Diagram on printed page 46, transcribed below.

## CPU Controlled Auxiliary Solenoids (printed page 28)

| Coil | Description | Control line | Power line | Drive transistor | Coil type |
| --- | --- | --- | --- | --- | --- |
| 17 | Left Turbo Bumper | BLU-BRN CPU CN19-7 | RED PS CN3-6 | Q11 | 23-800 |
| 18 | Cemter Turbo Bumper | BLU-RED CPU CN19-4 | RED PS CN3-6 | Q9 | 23-800 |
| 19 | Right Turbo Bumper | BLU-ORN CPU CN19-3 | RED PS CN3-6 | Q8 | 23-800 |
| 20 | Left Slingshot | BLU-YEL CPU CN19-6 | RED PS CN3-6 | Q10 | 23-800 |
| 21 | Right Slingshot | BLU-GRN CPU CN19-8 | RED PS CN3-6 | Q12 | 23-800 |
| 22 | Laser Kick (See Schematic) | BLU-BLK CPU CN19-9 | VIO-YEL PPB J7-3 | Q13 | 23-800 |

The printed headings are `Coil Number`, `Coil Description`, `Control Line (CPU to Coil)`, `Power Line (PS to Coil)`, `Drive Transistor` and `Coil Type`. `Cemter` (18) is the print's own spelling. Each control and power cell prints the wire colour on one line and the connector on the next; the transcription joins them with a space.

## Flipper Solenoids (printed page 28)

The printed headings are `Coil Description`, `Flipper GND` spanning `CPU to Coil` and `Sw. to Flip.PCB`, `Power Lines FlipPc toCoil`, `Coil Type` and `Power Input To Flip PCB`. The power-input cell is one merged cell for both rows; the transcription repeats it and marks the repetition.

| Coil description | Assembly | CPU to coil | Switch to Flip. PCB | Power line, Flip. PCB to coil | Coil type | Power input to Flip. PCB |
| --- | --- | --- | --- | --- | --- | --- |
| Left Flipper | 090-5020-30 | ORN-GRY CPU CN19-2 | BLU-GRY CN1-9 | GRY-YEL CN2-1,2 | 23-900 | BLK-WHT 50VDC GRY, GRY-GRN 8VAC |
| RightFlipper | 090-5020-30 | ORN-VIO CPU CN19-1 | BLU-VIO CN1-1 | BLK-WHT CN1-1 | 23-900 | BLK-WHT 50VDC GRY, GRY-GRN 8VAC (repeated) |

`RightFlipper` is printed without a space. The right flipper's power-line cell prints `BLK-WHT CN1-1`, the same connector pin as its switch line `BLU-VIO CN1-1`; both are literal.

## Coil chart schematic (printed page 29)

The drawing repeats one pattern for drives 1-8: a CPU-board `SIDE L 0n` / `SIDE R 0n` pair on one transistor, a `CN-11` pin and a `GRY-...` wire into PPB board `J1`, where diode `Dn` feeds the left (coil) path out of `J2` and a diode-resistor branch `D(n+8) - Rn` feeds the right (flash lamp) path out of `J9`. The right path of every drive runs to `J6` pins 4,5 of the PPD board and four `NO. 89` bulbs; the bulb note printed beside each drive is in the last column. Drives 3, 4 and 5 go through a `TIP 36C` booster on PPB `J8`.

| Drive | Side labels as printed | Transistor | CN-11 pin | CPU wire | PPB J1 pin | Coil path | Coil as drawn | Coil power | Flash path | Flash power | Bulb note as drawn |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIDE L 01 / SIDE R 01 | Q46 | 1 | GRY-RED | 1 | D1, J2-9, VIO-BRN | OUTHOLE 23-840 | BRN, PPD J6-1, + 50VL + 32VR | J9-5, BLK-RED | J6-4,5 ORN | (3) PLFD (1) INSERT (4) NO. 89 |
| 2 | SIDE L 02 / SIDE R 02 | Q45 | 3 | GRY-RED | 2 | D2, J2-8, VIO-RED | THROUGH EJECT 23-840 | BRN, PPD J6-1, + 50VL + 32VR | J9-6, BLK-RED | J6-4,5 ORN | (4) PLFD (4) NO. 89 |
| 3 | SIDE L 03 / SIDE R 03 | Q44 | 4 | GRY-YEL | 3 | D3, J2-7, WHT-ORN, PPB J8-1 Q5 TIP 36C J8-2, VIO-ORN | LION (INSERT) 23-800 | YEL-VIO, PPD J7-8,9, + 50VL + 32VR | J9-7, BLK-ORN | J6-4,5 ORG | (4) PLFD (4) NO. 89 |
| 4 | SIDE L 04 / SIDE R 04 | Q43 | 5 | GRY-YEL | 4 | D4, J2-6, WHT-YEL, PPB J8-6 Q3 TIP 36C J8-7, VIO-YEL | PLFD VUK 23-800 | YEL-VIO, PPD J7-8,9, + 50VL + 32VR | J9-8, BLK-YEL | J6-4,5 ORG | (3) PLFD (1) INSERT (4) NO. 89 |
| 5 | SIDE L 05 / SIDE R 06 | Q42 | 6 | GRY-GRN | 5 | D5, J2-5, WHT-GRN, PPB J8-3 Q4 TIP 36C J8-4, VIO-GRN | SUPER VUK 23-800 | YEL-VIO, PPD J7-8,9, + 50VL + 32VR | J9-9, BLK-GRN | J6-4,5 ORG | (2) LEFT RAMP (2) PLFD (4) NO. 89 |
| 6 | SIDE L 06 / SIDE R 06 | Q41 | 7 | GRY-BLU | 6 | D6, J2-4, VIO-BLU | ROCKY (INSERT) 23-800 | WHT, PPD J6-3, + 32VL + 32VR | J9-10, BLK-GRN | J6-4,5 ORG | (3) PLFD (1) INSERT (4) NO. 89 |
| 7 | SIDE L 07 / SIDE R 07 | Q40 | 8 | GRY-VIO | 7 | D7, J2-2, VIO-BLK | RHINO (INSERT) 23-800 | WHT, PPD J6-3, + 32VL + 32VR | J9-11, BLK-VIO | J6-4,5 ORG | (3) PLFD (1) INSERT (4) NO. 89 |
| 8 | SIDE L 08 / SIDE R 08 | Q39 | 9 | GRY-BLK | 8 | D8, J2-1, VIO-GRY | KNOCKER 23-800 | BRN, PPD J7-1, + (blank) + 32VR | J9-12, BLK-GRY | J6-4,5 ORN | (2) PLFD (2) INSERT (4) NO. 89 |

Readings: drive 5 prints `SIDE R 06` where every other drive repeats its own number; it is literal. Drives 1 and 2 both print `GRY-RED` and drives 3 and 4 both print `GRY-YEL` on the CPU side; both pairs are literal. Drives 5 and 6 both print `BLK-GRN` on the flash return. `THROUGH EJECT` is the print's own spelling. The flash-power wire is printed `ORN` on drives 1, 2 and 8 and `ORG` on the others. Drive 8's power box prints `+` with nothing after it on the left and `+ 32VR` on the right.

The lower half of the same page draws drives 09-16 from a `P/O CPU BOARD` block (no connector name is printed beside its pin column):

| Drive | Transistor | Pin | Wire | Load as drawn | Power |
| --- | --- | --- | --- | --- | --- |
| 09 | Q30 | 1 | BRN-BLK | RELAY on `RELAY BOARD #520-5010-00` (J8); its `NO` contact (`COIL`) takes `WHT-RED` `FROM BR2` `28 VAC`, its `NC` contact is unconnected, its `COMM` goes to `GND`, and `WHT-RED` runs to the `SAW MOTOR` | RED (+32V) |
| 10 | Q29 | 2 | BLK-RED | L/R COIL RELAY on the P/O PPD BOARD, J6-9 to J6-7 | RED-WHT, P/O P.S. BOARD CN3-5 +32V |
| 11 | Q28 | 4 | BRN-ORN | GENERAL ILLUM. RELAY on the P/O P.S. BOARD, CN7-1/3 | (on the P.S. board) |
| 12 | Q27 | 5 | BRN-YEL | RAMP DIVERTER 27-1400 | RED, P.S. CN3-6/7/8 +32V |
| 13 | Q26 | 6 | BRN-GRN | PLFD DIVERTER 23-800 | RED |
| 14 | Q25 | 7 | BRN-BLU | CONTROL GATE 31-1800 | RED |
| 15 | Q24 | 8 | BRN-VIO | DROP TARGET 22-600 | RED |
| 16 | Q23 | 9 | WHT-GRY | AUTO LAUNCH 23-800, through P/O PPB BOARD J8-11 Q1 TIP 36C J8-12 and VIO-GRY | VIO-YEL, P/O PPB BOARD J7-3 +50 V |

## Playfield Coil / Flash Lamp Wiring Diagram (printed page 46)

The two-page wiring diagram draws the same circuits. Its labels beside each coil read:

| Coil as labelled | Coil type | Position label |
| --- | --- | --- |
| AUTO LAUNCH | 22-600 | 5V SOL. 16 |
| LASER KICK | 23-800 | 50V SOL. 22 |
| KNOCKER | 22-600 | 8L |
| RHINO (INSERT) | 23-800 | 7L |
| ROCKY (INSERT) | 23-800 | 6L |
| SUPER VUK | 23-800 | 50V 5L |
| PLFD VUK | 23-800 | 50V 4L |
| LION (INSERT) | 23-800 | 50V 3L |
| TROUGH EJECT | 23-840 | 2L |
| OUTHOLE | 23-840 | 1L |

The laser kick hangs from `+50 VDC PPB J7-3 VIO-YEL` and returns on `BLU-BLK`; the auto launch hangs from the same `VIO-YEL` and returns on `BRN-GRY` into the PPB booster `Q1` (`TIP 36C`, `J8` pins 11 and 12), which `WHT-GRY` from `CN12` pin 9 drives. On the CPU `CN12` side the diagram draws `AUTO-LAUNCH 22-600` (pin 9, `WHT-GRY`), `DROP TARGET 22-600` (pin 8, `BRN-VIO`), `CONTROL GATE 31-1800` (pin 7, `BRN-BLU`), `PLFD DIVERTER 23-800` (pin 6, `BRN-GRN`), `RAMP DIVERTER 27-1400` (pin 5, `BRN-YEL`) and the `RELAY BOARD #520-5010-00` saw-motor relay (`BRN-BLK`), all on `RED` from `+32 VDC PS CN3-7/6` except the auto launch (`RED` from `+50 VDC PPB J7-3 VIO-YEL`). The CPU-board legend prints `CN11` pins 1, 3, 4, 5, 6, 7, 8, 9 as `SOL. DRIVE 1`-`8` on `Q46`, `Q45`, `Q44`, `Q43`, `Q42`, `Q41`, `Q40`, `Q39`, and `CN12` pins 1, 2, 4, 5, 6, 7, 8, 9 as `SOL. DRIVE 9`-`16` on `Q30`, `Q29`, `Q28`, `Q27`, `Q26`, `Q25`, `Q24`, `Q23`. The flash-lamp groups are drawn as `(3) PLFD (1) INSERT 1R`, `(4) PLFD 2R`, `(4) PLFD 3R`, `(3) PLFD (1) INSERT 4R`, `(2) PLFD (2) LEFT RAMP 5R`, `(3) PLFD (1) INSERT 6R`, `(3) PLFD (1) INSERT 7R` and `(2) PLFD (2) INSERT 8R`, each drawn with four bulbs on `+32 VDCR PPB J6-4/5 ORN`. Each group's bulb label reads `(4) NO. 89` except 4R's, which reads `(3) NO. 89` beside its four drawn bulbs. The relay note reads `A/B RELAY NORMALLY CLOSED SIDE = "N.C." = "LEFT" = "A" SIDE NORMALLY OPEN SIDE = "N.O." = "RIGHT" = "B" SIDE N.U. MEANS "NOT USED"`.

## Playfield Special Coil Diagram (printed page 47)

| Position | Coil as drawn | Coil type | CPU wire | CPU board CN19 | Printed drive |
| --- | --- | --- | --- | --- | --- |
| SP1 | RIGHT THUMPER BUMPER | 23-800 | BLU-ORN | 3 | SW.SOL DRIVE 1Q8 |
| SP2 | CENTER THUMPER BUMPER | 23-800 | BLU-RED | 4 | SW.SOL DRIVE 2Q9 |
| SP3 | LEFT SLINGSHOT | 23-800 | BLU-YEL | 6 | SW.SOL DRIVE 3Q10 |
| SP4 | LEFT THUMPER BUMPER | 23-800 | BLU-BRN | 7 | SW.SOL DRIVE 4Q11 |
| SP5 | RIGHT SLINGSHOT | 23-800 | BLU-GRN | 8 | SW.SOL DRIVE 5Q12 |
| SP6 | LASER KICK | 23-800 | WHT-BRN | 9 | SW.SOL DRIVE 6Q13 |

SP1-SP5 hang from `RED` `+32 VDC CN3 6 POWER SUPPLY`. SP6 hangs from `50 VDC PPB J7-3 VIO - YEL` and returns on `BLK - BLU` through a `Q2` booster on `PPB J8` pins 10 and 9 before the `WHT-BRN` line to CN19-9.

## Coil and flash-lamp location drawings (printed page 28)

Beside the text, page 28 draws the playfield with a balloon at each coil or flash-lamp position, and a backbox outline. Read as printed (several playfield balloons overlap ramps and are only partly legible): the playfield carries `1L` under the apron, `2L` and `16` at the shooter lane, `22` at the lower left beside the left outlane, `20` and `21` on the slingshots, `17`, `18` and `19` on the three turbo bumpers, `15` beside the right-hand drop-target bank, `9` on the right side above the shooter lane, `12`, `13` and `14` in the upper left and top, `4L` at the upper left, `5L` on the left rail, and flash-lamp balloons `1R` (three), `2R`, `3R`, `4R`, `5R`, `6R` (three), `7R` (three) and `8R`. The backbox outline carries `7R`, `4R`, `8R` (two), `1R` and `6R`, and three boxed balloons `7L`, `6L` and `3L` side by side at its bottom.

## Disagreements between these pages, kept literally

- Knocker coil type: `23-800` on page 29, `22-600` on page 46.
- Auto launch coil type: `23-800` on page 29, `22-600` on page 46; its coil-to-booster wire `VIO-GRY` on page 29, `BRN-GRY` on page 46, and the booster pins drawn `J8-11` (input) / `J8-12` (output) on page 29 and the other way round on page 46.
- Laser kick control wire: `BLU-BLK` on pages 28 and 46, `WHT-BRN` at CN19-9 with `BLK - BLU` between booster and coil on page 47.
- Bumper wording: `Turbo Bumper` on page 28, `THUMPER BUMPER` on page 47; the SP numbering on page 47 runs right-to-left and differs from the public solenoid numbers 17-22, which follow page 28.
