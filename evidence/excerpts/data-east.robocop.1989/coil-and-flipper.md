# RoboCop coil, flash, relay, flipper and special-solenoid transcription

Source: PDF pages 28-29, printed pages 24-25. Read from 300 dpi renders, the coil schematic re-rendered at 600 dpi.

## Coil schematic (printed page 25)

The A/B bank pairs share one TIP122 driver and CN-11 wire; side R carries no R07 or R08 branch.

| Printed driver | Transistor | Wire | Device | Type / bulbs |
| --- | --- | --- | --- | --- |
| SIDE L 01 | Q46 | GRY-BRN | Jackpot Flash | (3) No.89 + (1) No.906 |
| SIDE L 02 | Q45 | GRY-RED | Special Flash | (1) No.906 |
| SIDE L 03 | Q44 | GRY-ORN | ED209 1 MEG | (2) #89 + (1) #906 |
| SIDE L 04 | Q43 | GRY-YEL | Jones Flash | (1) #89 + (1) #906 |
| SIDE L 05 | Q42 | GRY-GRN | Bodd Flash | (1) #89 + (1) #906 |
| SIDE L 06 | Q41 | GRY-BLU | Emil Flash | (1) #89 + (1) #906 |
| SIDE L 07 | Q40 | GRY-VIO | Left Middle | (3) #89 + (1) #906 |
| SIDE L 08 | Q39 | GRY-BLK | Top Left | (1) #906 |
| SIDE R 01 | Q46 | GRY-BRN | Outhole | 23-840 |
| SIDE R 02 | Q45 | GRY-RED | Trough | 23-840 |
| SIDE R 03 | Q44 | GRY-ORN | Middle Eject | 27-1300 |
| SIDE R 04 | Q43 | GRY-YEL | Ball Guide Eject | 27-1300 |
| SIDE R 05 | Q42 | GRY-GRN | Right Eject | 27-1300 |
| SIDE R 06 | Q41 | GRY-BLU | Vertical Up Kicker | 23-800 |
| SIDE R 07 | Q40 | GRY-VIO | no branch printed | — |
| SIDE R 08 | Q39 | GRY-BLK | no branch printed | — |
| 09 | Q30 | BRN-BLK | Middle Blue | (2) #89 + (2) #906 |
| 10 | Q29 | BLK-RED | Left/Right Coil Relay K1 (PPB) | K1 |
| 11 | Q28 | BRN-ORN | General Illum. Relay K1 (PS board) | K1 |
| 12 | Q27 | BRN-YEL | Middle Red | (2) #89 + (2) #906 |
| 13 | Q26 | BRN-GRN | Right Blue | (2) #89 + (2) #906 |
| 14 | Q25 | BRN-BLU | Ramp Red | (1) #89 + (3) #906 |
| 15 | Q24 | BRN-VIO | Ramp Blue | (1) #89 + (3) #906 |
| 16 | Q23 | WHT-GRY | Laserkick | 23-800 |

Output 16 drives the Laserkick 23-800 coil through `Q5 TIP36C`, `BRN-GRY`, `+50V`.

## Switch-triggered solenoids (printed page 24)

| Printed | Device | Control | Trigger | Transistor | Coil |
| --- | --- | --- | --- | --- | --- |
| SP1 | Right Turbo Bumper | BLU-ORN CPU CN19-3 | ORN-BLK CPU CN18-2 | Q8 | 23-800 |
| SP2 | Center Turbo Bumper | BLU-RED CPU CN19-4 | ORN-RED CPU CN18-3 | Q9 | 23-800 |
| SP3 | Left Slingshot | BLU-YEL CPU CN19-6 | ORN-YEL CPU CN18-4 | Q10 | 23-800 |
| SP4 | Left Turbo Bumper | BLU-BRN CPU CN19-7 | ORN-BRN CPU CN18-5 | Q11 | 23-800 |
| SP5 | Right Slingshot | BLU-GRN CPU CN19-8 | ORN-GRN CPU CN18-8 | Q12 | 23-800 |
| SP6 | NOT USED | CPU CN19-9 | CPU CN18-9 | Q13 | — |

Every SP row prints power `RED PS CN3-6` (written once and repeated for SP2-SP5; printed again on SP6).

## Flippers (printed page 24)

| Flipper | CPU | Flipper board | Power | Coil |
| --- | --- | --- | --- | --- |
| Left Flipper | ORN-GRY CPU CN19-2 | BLU-GRY CN1-8 | GRY-YEL CN2-1,2 | 22-900 |
| Right Flipper | ORN-VIO CPU CN19-1 | BLU-VIO CN1-1 | BLU-YEL CN2-3,4 | 22-900 |

Power input: `BLK-WHT 50VDC`; `GRY,GRY GRN 8VAC`.

## ROBOCOP COIL PART NUMBER CHART (printed page 24)

| Quantity used | Coil type | Data East Pinball part number |
| --- | --- | --- |
| 6 | 23-800 | 090-5001-00 |
| 3 | 27-1300 | 090-5003-00 |
| 2 | 23-840 | 090-5005-00 |
| 2 | 22-900 | 090-5020-20 |

The schematic itself draws seven 23-800 coils (Vertical Up Kicker, Laserkick and SP1-SP5) against the chart's six; both readings are kept.

## Coil location drawing (printed page 24)

Callouts on the playfield plan: `L08` top left; `R04` top center; `R05` top right; `R03` upper left; `R06` at the left kicker; `L07` left; `L06`, `L05`, `L04`, `L03`, `L02`, `L01` top to bottom down the center-right ladder; `12` and `09` center; `13` lower center right; `15`, `14`, `15`, `14`, `15`, `14` alternating up the right ramp; `16` lower left outlane; `R02` and `R01` at the trough below the flippers. No flipper, slingshot or turbo-bumper callout is printed.

The separate `Backbox Flash lamps` inset prints nineteen bulb circles labelled `L09`, `L09`, `L07`, `L01`, `L07`, `L01`, `L07`, `L01`, `13`, `13` (top row), `15`, `L03`, `14`, `L03` (middle row) and `12`, `12`, `L06`, `L04`, `L05` (bottom row). `L09` is printed with an L prefix although output 9 is a direct driver.
