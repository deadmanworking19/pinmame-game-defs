# Batman Forever coils, flashers, relays and flippers

Source: `Sega_1995_Batman_Forever_Manual_with_schematics_duplicate_pages_33_34_missing_pages_143_144.pdf`, SHA-256 `e4ffe85699953dcaa7f1882eae8d0e3b4d01926d60039800965d62616d34d3d4`, PDF 32-34 (printed 26-28). Sega Pinball, Inc. 1995; IPDB machine 3593. Transcribed by the curator from 300 dpi renders of the 300 dpi scan and visually checked. Line wraps inside a cell are joined with a space and connector spacing is normalized (`J 6-1, 2` is written `J6-1, 2`). A value repeated from a vertically merged cell is enclosed in `{}`; the braces are editorial, not printed. `---` preserves the printed dash marks. No blank cell is completed by pattern.

## Coils (1L-8L) & Flashers (1R-8R) and Constant Power Coils (9-22) (PDF 34, complete)

Rows 6L and 13 are printed shaded. The merged cells are Drive Transistor and On Which Board on the pairs 1L/1R, 2L/2R, 5L/5R, 7L/7R and 8L/8R; 3L/3R, 4L/4R and 6L/6R print their own cells.

| Coil No. | Description | Drive Transistor (D.T.) | On Which Board? | D.T. Control Line Color | D.T. Control Line Connect | Power Line Color | Power Line Connection | Power Voltage | Coil GA/Turn or Bulb Type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1L | 4-BALL LOCKOUT | Q46 | CPU | VIO-BRN | PPB J2-1 | BRN | PPB J6-1, 2 | 32v L | 25-1240 090-5034-00 |
| 1R | *FLASH* 4-BANK X2 LEFT INLANE X2 | {Q46} | {CPU} | BLK-BRN | PPB J9-1 | ORG | PPB J6-4, 5 | 32v R | 4X #89 0X #906 |
| 2L | TROUGH UP-KICKER | Q45 | CPU | VIO-RED | PPB J2-2 | BRN | PPB J6-1, 2 | 32v L | 23-800 090-5001-00 |
| 2R | *FLASH* LEFT RAMP X4 | {Q45} | {CPU} | BLK-RED | PPB J9-2 | ORG | PPB J6-4, 5 | 32v R | 4X #89 0X #906 |
| 3L | AUTOLAUNCH 50V | Q44/Q5 | CPU/PPB | VIO-ORG | PPB J8-2 | YEL-VIO | PPB J7-8 | 50v L | 23-800 090-5001-00 |
| 3R | *FLASH* LEFT ORBIT X4 | Q44 | CPU | BLK-ORG | PPB J9-3 | ORG | PPB J6-4, 5 | 32v R | 4X #89 0X #906 |
| 4L | VUK 50V | Q43/Q4 | CPU/PPB | VIO-YEL | PPB J8-4 | YEL-VIO | PPB J7-8, 9 | 50v L | 24-940 090-5036-00 |
| 4R | *FLASH* TOP LEFT X2 BACK PANEL X1 INSERT X1 | Q43 | CPU | BLK-YEL | PPB J9-4 | ORG | PPB J6-4, 5 | 32v R | 3X #89 1X #906 |
| 5L | TOP EJECT | Q42 | CPU | VIO-GRN | PPB J2-5 | BRN | PPB J6-1, 2 | 32v L | 24-940 090-5036-00 |
| 5R | *FLASH* LEFT RAMP X1 BACK PANEL X1 INSERT X2 | {Q42} | {CPU} | BLK-GRN | PPB J9-5 | ORG | PPB J6-4, 5 | 32v R | 3X #89 1X #906 |
| 6L | NOT USED | Q41 | CPU | VIO-BLU | PPB J2-6 | BRN | PPB J6-1, 2 | 32v L | --- |
| 6R | *FLASH* MINI RAMP X1 BACK PANEL X1 INSERT X2 | Q41 | CPU | BLK-BLU | PPB J9-6 | ORG | PPB J6-4, 5 | 32v R | 2X #89 2X #906 |
| 7L | 4-BANK DROP TARGET RESET | Q40 | CPU | VIO-BLK | PPB J2-7 | BRN | PPB J6-1, 2 | 32v L | 23-700 090-5022-00 |
| 7R | *FLASH* TOP RIGHT X2 BACK PANEL X1 INSERT X1 | {Q40} | {CPU} | BLK-VIO | PPB J9-7 | ORG | PPB J6-4, 5 | 32v R | 3X #89 1X #906 |
| 8L | KNOCKER | Q39 | CPU | VIO-GRY | PPB J2-8 | BRN | PPB J6-1, 2 | 32v L | 23-800 090-5001-00 |
| 8R | *FLASH* RIGHT 2-BANK X1 RIGHT INLANE X2 INSERT X1 | {Q39} | {CPU} | BLK-GRY | PPB J9-8 | ORG | PPB J6-4, 5 | 32V R | 3X #89 1X #906 |
| 9 | BATCAVE BALL LOCK | Q30 | CPU | BRN-BLK | CPU CN12-1 | RED | PS CN3-6, 7 | 32v | 24-900 090-5002-00 |
| 10 | LEFT & RIGHT (A/B) RELAY Loc: PPB (Not Shown in Display) | Q29 | CPU | BLK-RED | CPU CN12-2 | RED | PS CN3-6, 7 | 32v | 24v DC 10A DPDT |
| 11 | G.I. RELAY Loc: Power Supply | Q28 | CPU | BRN-ORG | CPU CN12-4 | RED | PS CN3-6, 7 | 32v | 24v DC 10A DPDT |
| 12 | BATWING RAMP DIVERTER | Q27 | CPU | BRN-YEL | CPU CN12-5 | RED | PS CN3-6, 7 | 32v | 27-1500 090-5004-00 |
| 13 | NOT USED | Q26 | CPU | BRN-GRN | CPU CN12-6 | RED | PS CN3-6, 7 | 32V | --- |
| 14 | BATWING MOTOR RELAY | Q25 | CPU | BRN-BLU | CPU CN12-7 | RED | PS CN3-6, 7 | 32v | 24v DC 10A DPDT |
| 15 | BATWING CANNON 50V | Q24/Q3 | CPU/PPB | BRN-VIO | PPB J8-6 | VIO-YEL | PPB J7-6, 7 | 50v | 23-800 090-5001-00 |
| 16 | BATCAVE KICKER 50V | Q23/Q2 | CPU/PPB | BRN-GRY | PPB J8-8 | VIO-YEL | PPB J7-6, 7 | 50v | 24-940 090-5036-00 |
| 17 | LEFT TURBO BUMPER | Q11 | CPU | BLU-BRN | CPU CN19-7 | RED | PS CN3-6 | 32v | 23-700 090-5022-00 |
| 18 | BOTTOM TURBO BUMPER | Q9 | CPU | BLU-RED | CPU CN19-4 | RED | PS CN3-6 | 32v | 23-700 090-5022-00 |
| 19 | RIGHT TURBO BUMPER | Q8 | CPU | BLU-ORG | CPU CN19-3 | RED | PS CN3-6 | 32v | 23-700 090-5022-00 |
| 20 | LEFT SLINGSHOT | Q10 | CPU | BLU-YEL | CPU CN19-6 | RED | PS CN6-6, 7 | 32v | 23-800 090-5001-00 |
| 21 | RIGHT SLINGSHOT | Q12 | CPU | BLU-GRN | CPU CN19-8 | RED | PS CN6-6, 7 | 32v | 23-800 090-5001-00 |
| 22 | LASER KICK 50V | Q13/Q1 | CPU/PPB | BLU-BLK | PPB J8-10 | VIO-YEL | PPB J7-6, 7 | 50v | 23-800 090-5001-00 |

The Coil GA/Turn heading reads "Coil GA/Turn or Bulb Type" in the upper block and "Coil GA/Turn or Relay Type" in the constant-power block. 3L and 4L print `YEL-VIO` as the power line colour; 15, 16 and 22 print `VIO-YEL`.

## Flipper Coils (PDF 34, complete)

| SSFB No. | Flipper Coil | Cabinet Switch | Switch Drive | Switch Return | E.O.S. | GND | Flipper 50vDC Power | Flipper 8vAC Hold | Flipper Coil Output |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SSFB 1 | Lwr. Rt. Flipper 22-900 | BLU-VIO SSFB CN1-7 | GRN-GRY CPU CN8-9 TO SSFB CN1-4 | WHT-GRY CPU CN10-1 TO SSFB CN1-3 | BRN-VIO RT. EOS SW. TO CN1-1 | BLK CPU CN5 TO CN1-6 | BLK-WHT PPB J7-1, -5 to SSFB CN2-11, 12 | GRY-GRN-GRY P/S CN1-10, -11, to SSFB CN2-9, 10 | 50v Q2, Q3, / 8vAC SR1 / CN2-7, 8 |
| SSFB 1 | Lwr. Lt. Flipper 22-1080 | BLU-GRY SSFB CN1-10 | GRN-GRY CPU CN8-9 TO SSFB CN1-4 | WHT-VIO CPU CN10-2 TO SSFB CN1-5 | BRN-GRY LT. EOS SW. TO CN1-9 | BLK CPU CN5 TO CN1-6 | BLK-WHT PPB J7-1, -5 to SSFB CN2-11, 12 | GRY-GRN-GRY P/S CN1-10, -11, to SSFB CN2-9, 10 | 50v Q2, Q10, / 8vAC SR2 / CN2-4, 5 |
| SSFB 1 | Upr. Rt. Flipper 23-900 | GRY-VIO SSFB CN1-10 | GRN-GRY CPU CN8-9 TO SSFB CN1-4 | WHT-GRY CPU CN10-1 TO SSFB CN1-3 | Not Used | BLK CPU CN5 TO CN1-6 | BLK-WHT PPB J7-1, -5 to SSFB CN2-11, 12 | GRY-GRN-GRY P/S CN1-10, -11, to SSFB CN2-9, 10 | 50v Q16, Q15 / 8vAC SR3 / CN2-1, 2 |

The last column prints a vertical bar between the 50v and 8vAC parts; it is written ` / ` here. On the Lwr. Lt. row the bar is printed touching the `S` of `SR2`. Lwr. Lt. and Upr. Rt. both print `SSFB CN1-10` as the cabinet switch connector. The upper right flipper prints the same switch drive and return as the lower right flipper.

## Playfield Coil Locations table (PDF 33, complete)

Legend: open box = "Coils or Flash Lamps located above playfield"; filled box = "Coils or Flash Lamps located below playfield". "The following coils/relays are not noted in the Coil Diagram above (Location: 8L-Cabinet; 10/11-Backbox): 8L 10 11". "The following coils are not used: 6L 13". In the drawing 3L, 9, 15, 16 and 22 are open boxes; 1L, 2L, 4L, 5L, 7L, 12, 14 and 17-21 are filled boxes.

| Coil No. | Type | Coil Description |
| --- | --- | --- |
| 1L | Coil | 4-Ball Trough Lock Ball (25-1240) |
| 2L | Coil | Trough Up-Kicker (23-800) |
| 3L | Coil | Auto Ball Launch 50v (23-800) |
| 4L | Coil | VUK 50v (24-940) |
| 5L | Coil | Top Eject (24-940) |
| 6L | Coil | NOT USED |
| 7L | Coil | 4-Bank Drop Target Reset (23-700) |
| 8L | Coil | Knocker 32v (23-800) |
| 9 | Coil | Bat Cave Ball Lock (24-900) |
| 10 | Relay | Left / Right (A/B) Relay (24v DC 10A DPDT) |
| 11 | Relay | G.I. (General Illumination) Relay (24v DC 10A DPDT) |
| 12 | Coil | Batwing Ramp Ball Diverter (27-1500) |
| 13 | Coil | NOT USED |
| 14 | Coil | Batwing Motor Relay (24v DC 10A DPDT) |
| 15 | Coil | Batwing Cannon Ball Launch 50v (23-800) |
| 16 | Coil | Bat Cave Ramp Ball Kicker 50v (24-940) |
| 17 | Coil | Left Turbo Bumper (23-700) |
| 18 | Coil | Bottom Turbo Bumper (23-700) |
| 19 | Coil | Right Turbo Bumper (23-700) |
| 20 | Coil | Left Slingshot (23-800) |
| 21 | Coil | Right Slingshot (23-800) |
| 22 | Coil | Laser Kick 50v (23-800) |

## Playfield Flash Lamp Locations table (PDF 33, complete)

Drawing note: "All Flash Lamps which are located above the playfield are under Mini-Mars." Footnote: "See previous page for Backbox Insert Flash Lamp Locations." Legend bulb: "#R = Flasher #89 Bulb (Bayonet) 165-5000-89". The drawing prints 4R, 5R, 6R and 7R in open boxes on the rear edge (the back panel), a second open 4R box at the rear-left corner, and an open 5R box under an open "On the Ramp." label beside the left ramp. The filled boxes are 1R x4 (two at the 4-bank, two at the lower left), 2R x4, 3R x4 along the left orbit, 4R x1 at the top left, 6R x1 at the U-turn, 7R x2 at the top right and 8R x3 (one at the right stand-up, two at the lower right).

| Coil No. | Type | Flash Lamps Description & Qty. |
| --- | --- | --- |
| 1R | Flash | 4-Bank x2 Left Bottom x2 |
| 2R | Flash | Left Ramp X4 |
| 3R | Flash | Left Orbit X4 |
| 4R | Flash | Top Left X2 Backpanel X1 |
| 5R | Flash | Middle Ramp X1 Backpanel X1 |
| 6R | Flash | U-Turn X1 Backpanel X1 |
| 7R | Flash | Top Right X2 Backpanel X1 |
| 8R | Flash | Right Bottom X2 Right Stand-Up X1 |

## Backbox Insert Flash Lamps table (PDF 32, complete)

"The flash lamp locations correspond with the coil numbers as seen in the Coil Test." Bulbs: G.I. "#555 Bulb (Wedge Base) 165-5002-00" and "#44 Bulb (Bayonet) 165-5000-44"; flasher "#906 Bulb (Wedge Base) 165-5004-00" and "#89 Bulb (Bayonet) 165-5000-89". "Both bulbs use an IDC Wedge Base Socket (077-5110-00)." "#44 Bulb uses 2-Lug Socket (077-5000-00). #89 Bulb uses a Stand-Up Short Socket (077-5101-00)." "Look at bulb style above to determine which Bulb & Sockets are required for replacements." The insert drawing shows 4R once, 5R twice, 6R twice, 7R once and 8R once among the G.I. sockets.

| Coil No. | Type | Qty. | Coil No. | Type | Qty. |
| --- | --- | --- | --- | --- | --- |
| 1R | Flash | Not used. | 5R | Flash | Insert X2 |
| 2R | Flash | Not used. | 6R | Flash | Insert X2 |
| 3R | Flash | Not used. | 7R | Flash | Insert X1 |
| 4R | Flash | Insert X1 | 8R | Flash | Insert X1 |

## Flasher branches on the Playfield Coil / Flashlamp Wiring Diagram (PDF 108, printed 100, complete)

Each branch is drawn with four bulb symbols fed "+32VDCR PPB J6-4/5 ORG". Read rotated from the 300 dpi render.

| Circuit | Branch label | Bulbs | Drive wire |
| --- | --- | --- | --- |
| 1R | (2)4 BANK X 2(2)LEFT BOTTOM | (4) 89 | BLK/BRN |
| 2R | (4)LEFT RAMP | (4) 89 | BLK/RED |
| 3R | (4)LEFT ORBIT | (4) 89 | BLK/ORG |
| 4R | (2)TOP LT CORNER(1)BACK PANEL(1)INSERT | (3) 89 (1) 906 | BLK/YEL |
| 5R | (1)2 BANK STAND UP(1)BACK PANEL(1)INSERT | (3) 89 (1) 906 | BLK/GRN |
| 6R | (1)U-TURN(1)BACK PANEL(2)INSERT | (2) 89 (2) 906 | BLK/BLU |
| 7R | (2)TOP RT(1)BACK PANEL(1)INSERT | (3) 89 (1) 906 | BLK/VIO |
| 8R | (2)RT BOTTOM(1)RT STAND UP(1)INSERT | (3) 89 (1) 906 | BLK/GRY |

Every branch's bulb counts equal the driver chart's. The 5R location words differ: this diagram names a 2-bank stand-up and one insert, the driver chart "LEFT RAMP X1 BACK PANEL X1 INSERT X2", the location table "Middle Ramp X1 Backpanel X1" and the location drawing an open 5R box beside the left ramp labelled "On the Ramp.". The backbox insert drawing prints 5R twice and its table "Insert X2".

## Coil menu text (PDF 32)

"Twenty-Two regular coil drivers (pulsed under microprocessor control) are provided to switch ground to coils. The Left/Right Relay is used in conjunction with Drives 1 through 8 to switch +32/50 volts between coils or flash lamps; these sets are termed "left" and "right". The first 8 coil numbers are followed by "L" for left; the first 8 flash lamp numbers are followed by "R". This relay is located on the PPB Board which provides isolation diodes and current limiting resistors. This effectively provides up to 30 drive controlled devices. The remaining (9-22) can be either coils or flashlamps (indicated in the display and the tables below)."
