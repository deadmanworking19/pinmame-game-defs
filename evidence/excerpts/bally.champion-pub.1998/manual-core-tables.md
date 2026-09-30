# Champion Pub manual table transcription

Source PDF SHA-256: `2f7029091efbb371d612504dbd09d44b7eda3528e896c924fb8fccef1afc1dbf`; path: manuals/by-machine/bally.champion-pub.1998/ipdb-4358/Bally_1998_The_Champion_Pub_Manual_OCR_searchable.pdf (166 PDF pages). Transcribed by Codex GPT-6 delegated mechanical extraction worker. Curator review: `true` (primary curator visually checked every accepted row against native render pages 120, 124–125 and 127–129).

Full-PDF text extraction was used only to locate candidate table pages. Literal table content was transcribed from native-resolution rendered page images and visually inspected. OCR was not used to fill cells. Printed blanks, dash strings, repeated item numbers, and merged cells are represented explicitly.

No coordinates are included. Empty source cells are written [blank]; printed dash strings remain -----.


## SWITCH MATRIX — PDF page 127, printed 2-53

Printed annotations: `J2XX = CPU BOARD`; `= OPTO, TYPICALLY CLOSED`.
Upper wire labels: White → Green. Gray fill is source shading; the printed legend reads `= OPTO, TYPICALLY CLOSED`.

Column wiring labels:

| Column | Wire color | CPU connector | CPU pin |
| :-- | :-- | :-- | :-- |
| 1 | Green-Brown | J206-1 | U20-18 |
| 2 | Green-Red | J206-2 | U20-17 |
| 3 | Green-Orange | J206-3 | U20-16 |
| 4 | Green-White | J206-4 | U20-15 |
| 5 | Green-Black | J206-5 | U20-14 |
| 6 | Green-Blue | J206-6 | U20-13 |
| 7 | Green-Violet | J206-7 | U20-12 |
| 8 | Green-Gray | J206-9 | U20-11 |

| Row | Row wire | CPU connector | CPU pin | Column 1 | Column 2 | Column 3 | Column 4 | Column 5 | Column 6 | Column 7 | Column 8 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | White-Brown | J208-1 | U18-11 | MADE RAMP (11) | SLAM TILT (21) | TROUGH EJECT (31) [gray] | BOXER POLE CENTER (41) [gray] | LEFT SLINGSHOT (51) | LEFT SCOOP UP (61) | EXIT ROPE (71) | NOT USED (81) |
| 2 | White-Red | J208-2 | U18-9 | HEAVY BAG (12) | COIN DOOR CLOSED (22) | TROUGH BALL 1 (32) [gray] | BEHIND LEFT SCOOP (42) [gray] | RIGHT SLINGSHOT (52) | RIGHT SCOOP UP (62) | ENTER SPEED BAG (72) | NOT USED (82) |
| 3 | White-Orange | J208-3 | U18-5 | START BUTTON (13) | BALL LAUNCH (23) | TROUGH BALL 2 (33) [gray] | BEHIND RIGHT SCOOP (43) [gray] | THREE BANK BOTTOM (53) | THROWN TOWEL (63) | DANGER ZONE (73) | NOT USED (83) |
| 4 | White-Yellow | J208-4 | U18-7 | PLUMB BOB TILT (14) | ALWAYS CLOSED (24) | TROUGH BALL 3 (34) [gray] | ENTER RAMP (44) [gray] | THREE BANK TOP (54) | ROPE CAM (64) [gray] | ENTER LOCK UP (74) | NOT USED (84) |
| 5 | White-Green | J208-5 | U19-11 | LOCK UP 1 (15) | THREE BANK MIDDLE (25) | TROUGH BALL 4 (35) [gray] | JUMP ROPE (45) [gray] | LEFT HALF GUY (55) | SPEED BAG (65) | UP/DOWN POST (75) | NOT USED (85) |
| 6 | White-Blue | J208-7 | U19-9 | LEFT OUTLANE (16) | LEFT RETURN (26) | LEFT JAB MADE (36) [gray] | BAG POLE CENTER (46) [gray] | RIGHT HALF GUY (56) | BOXER GUT 1 (66) | TOP OF RAMP (76) | NOT USED (86) |
| 7 | White-Violet | J208-8 | U19-5 | RIGHT RETURN (17) | RIGHT OUTLANE (27) | CORNER EJECT (37) | BOXER POLE RIGHT (47) [gray] | LOCK UP 2 (57) | BOXER GUT 2 (67) | NOT USED (77) | NOT USED (87) |
| 8 | White-Gray | J208-9 | U19-7 | SHOOTER LANE (18) | POPPER (28) | RIGHT JAB MADE (38) [gray] | BOXER POLE LEFT (48) [gray] | LOCK UP 3 (58) | BOXER HEAD (68) | ENTER ROPE (78) | NOT USED (88) |

Dedicated grounded switches:

| Item | Wire color | CPU connector | CPU pin | Description | Normal Function | Test Function |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| D1 | Orange-Brown | J205-1 | U17-5 | LEFT COIN CHUTE | [blank] | [blank] |
| D2 | Orange-Red | J205-2 | U17-7 | CENTER COIN CHUTE | [blank] | [blank] |
| D3 | Orange-Black | J205-3 | U17-11 | RIGHT COIN CHUTE | [blank] | [blank] |
| D4 | Orange-Yellow | J205-4 | U17-9 | 4TH COIN CHUTE | [blank] | [blank] |
| D5 | Orange-Green | J205-6 | U16-9 | [blank] | Serv Crdts | Escape |
| D6 | Orange-Blue | J205-7 | U16-11 | [blank] | Volume Dn | Down |
| D7 | Orange-Violet | J205-8 | U16-7 | [blank] | Volume Up | Up |
| D8 | Orange-Gray | J205-9 | U16-5 | [blank] | Begin Test | Enter |

Flipper grounded switches:

| Item | Wire color | CPU connector | Description |
| :-- | :-- | :-- | :-- |
| F1 | Black-Green | J208-13 | LOWER RIGHT FLIPPER E.O.S. |
| F2 | Blue-Violet | J212-12 | LOWER RIGHT FLIPPER OPTO |
| F3 | Black-Blue | J208-12 | LOWER LEFT FLIPPER E.O.S. |
| F4 | Blue-Gray | J212-11 | LOWER LEFT FLIPPER OPTO |
| F5 | Black-Violet | J208-11 | UPPER RIGHT FLIPPER E.O.S. |
| F6 | Black-Yellow | J212-10 | UPPER RIGHT FLIPPER OPTO |
| F7 | Black-Gray | J208-10 | UPPER LEFT FLIPPER E.O.S. |
| F8 | Black-Blue | J212-9 | UPPER LEFT FLIPPER OPTO |

## LAMP MATRIX — PDF page 128, printed 2-54

Printed annotations: `J1XX = Power Driver Board`; `Yellow (B+)`; `Red`.
Column wiring/transistor labels:

| Column | Wire color | Driver connector | Transistor |
| :-- | :-- | :-- | :-- |
| 1 | Yellow-Brown | J121-1 | Q96 |
| 2 | Yellow-Red | J121-2 | Q100 |
| 3 | Yellow-Orange | J121-3 | Q95 |
| 4 | Yellow-Black | J121-4 | Q99 |
| 5 | Yellow-Green | J121-5 | Q94 |
| 6 | Yellow-Blue | J121-6 | Q98 |
| 7 | Yellow-Violet | J121-7 | Q93 |
| 8 | Yellow-Gray | J121-9 | Q97 |

| Row | Wire color | Driver connector | Transistor | Column 1 | Column 2 | Column 3 | Column 4 | Column 5 | Column 6 | Column 7 | Column 8 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | Red-Brown | J125-1 | Q104 | HEAVY BAG COMPLETE (11) | BOUT 1 (21) | LOWER BLUE ARROW (31) | LEFT HOOK (41) | JACKPOTS COMPLETE (51) | ULTIMATE CHALLANGE (61) | RAID (71) | RIGHT KO (81) |
| 2 | Red-Black | J125-2 | Q108 | JUMP ROPE COMPLETE (12) | BOUT 2 (22) | LEFT HOOK TO WIN (32) | BODY BLOW (42) | PUB CHAMPION (52) | POKER NIGHT (62) | FISTICUFF (72) | LEFT SECOND WIND (82) |
| 3 | Red-Orange | J125-4 | Q103 | SPEED BAG COMPLETE (13) | BOUT 3 (23) | WHITE ARROW (33) | RIGHT HOOK (43) | WON BY KO (53) | EXTRA BALL (63) | MULTIBRAWL (73) | TOP BLUE ARROW (83) |
| 4 | Red-Yellow | J125-5 | Q107 | RIGHT JAB COMBO (14) | BOUT 4 (24) | THROWN TOWEL (34) | CENTER JACKPOT (44) | MULTIBALLS COMPLETE (54) | SPITTING GALLERY (64) | THREE BANK TOP (74) | CENTER KO (84) |
| 5 | Red-Green | J125-6 | Q102 | LOCK (15) | JUMP ROPE (25) | CENTER BLUE ARROW (35) | LEFT KO BOXER (45) | TRAINING COMPLETE (55) | LEFT START FIGHT (65) | THREE BANK MIDDLE (75) | BALL SAVE POST (85) |
| 6 | Red-Blue | J125-7 | Q106 | RIGHT START FIGHT (16) | LEFT JAB COMBO (26) | LOWER YELLOW ARROW (36) | HURRY-UP (46) | SPEED BAG (56) | THE CORNER (66) | THREE BANK BOTTOM (76) | SHOOT AGAIN (86) |
| 7 | Red-Violet | J125-8 | Q101 | RIGHT JACKPOT (17) | CENTER START FIGHT (27) | TOP YELLOW ARROW (37) | HEAVY BAG (47) | LEFT JACKPOT (57) | RIGHT RETURN (67) | LEFT RETURN (77) | LAUNCH BUTTON (87) |
| 8 | Red-Gray | J125-9 | Q105 | RIGHT JAB (18) | LEFT JAB (28) | NOT USED (38) | RIGHT KO BOXER (48) | BALCONY (58) | RIGHT SECOND WIND (68) | LEFT KO (78) | START BUTTON (88) |



## Solenoid/Flasher Locations — PDF page 120, printed 2-46

| Item | Assembly Part Number | Coil or Flasher Part Number | Description |
| :-- | :-- | :-- | :-- |
| 01 | A-16757-2 | AE-26-1200 | AUTO PLUNGER |
| 02 | A-19963 | AE-26-1500 | TROUGH EJECT |
| 03 | A-22176 | FL-22241 | LEFT SCOOP POWER |
| 04 | A-22176 | FL-22241 | RIGHT SCOOP POWER |
| 05 | A-22214 | AE-30-2000 | CORNER KICKOUT |
| 06 | A-22173 | FL-22241 | POST POWER |
| 07 | A-22147 | 20-10197 | ROPE MAGNET |
| 08 | A-22167 | AE-27-1200 | POST DIVERTER |
| 09 | A-22176 | FL-22241 | LEFT SCOOP HOLD |
| 10 | A-22176 | FL-22241 | RIGHT SCOOP HOLD |
| 11 | A-22177 | 04-11000 | RIGHT ARM |
| 12 | A-22173 | FL-22241 | POST HOLD |
| 13 | A-22177 | 04-11000 | LEFT ARM |
| 14 | A-22169 | AE-27-1200 | POPPER |
| 15 | A-22206-2 | AE-26-1200 | LEFT SLINGSHOT |
| 16 | A-22206-2 | AE-26-1200 | RIGHT SLINGSHOT |
| 17 | 04-11152.1-12 (2), A-17802 (1) | #906 (3) | BOXER FLASHER |
| 18 | A-17802 (2) | #906 (2) | DANGER ZONE FLASHER |
| 19 | A-22267-4 (1) | #906 (1) | JUMP ROPE FLASHER |
| 19 | ----- | #906 (1) | INSERT PANEL FLASHER |
| 20 | A-22267-2 (1) | #906 (1) | LOCK KICKOUT FLASHER |
| 20 | ----- | #906 (1) | INSERT PANEL FLASHER |
| 21 | A-22267-1 (1) | #906 (1) | LEFT KICKOUT FLASHER |
| 21 | ----- | #906 (2) | INSERT PANEL FLASHER |
| 22 | A-17802 (2) | #906 (2) | BOXER FLASHER |
| 22 | ----- | #906 (1) | INSERT PANEL FLASHER |
| 23 | 04-11152.1-16 | #906 (1) | JUMP ROPE FLASHER |
| 24 | 04-11152.1-16 | #906 (1) | SPEED BAG FLASHER |
| 25 | A-22147 | SEE NOTE 1 | ROPE MOTOR |
| 26 | A-22171 | SEE NOTE 2 | TOGGLE DIRECTION |
| 27 | A-22171 | SEE NOTE 2 | MOTOR ON/OFF |
| 28 | A-22221 | AE-26-1500 | LOCK PIN |


## Flippers — PDF page 120, printed 2-46

| Item | Assembly Part Number | Coil Part Number | Description |
| :-- | :-- | :-- | :-- |
| 29-30 | A-15849-R-4 | FL-15411 | LOWER RIGHT FLIPPER |
| 31-32 | A-15849-L-4 | FL-15411 | LOWER LEFT FLIPPER |
| 33 | A-22147 | AE-30-2000 | ROPE POPPER |
| 34 | A-22172 | AE-26-1500 | RAMP DIVERTER |
| 35 | A-22148 | AE-27-1200 | LEFT SPEED BAG |
| 36 | A-22148 | AE-27-1200 | RIGHT SPEED BAG |


## 24 LED Circuits (SEE NOTE 3) — PDF page 120, printed 2-46

| Item | Driver Board | LED Board | Description |
| :-- | :-- | :-- | :-- |
| 37 | A-21967-2 | A-21991 | [blank] |
| 38 | A-21967-2 | A-21991 | [blank] |
| 39 | A-21967-2 | A-21991 | [blank] |
| 40 | A-21967-2 | A-21991 | [blank] |


## General Illumination locations — PDF page 120, printed 2-46

| Item | Bulb Number | Bulb Type | Description |
| :-- | :-- | :-- | :-- |
| 01 | 24-8768 | #555 | ILLUMINATION STRING 1 |
| 02 | 24-8768 | #555 | ILLUMINATION STRING 2 |
| 03 | 24-6549 | #44 | ILLUMINATION STRING 3 |
| 04 | 24-6549 | #44 | ILLUMINATION STRING 4 |
| 05 | 24-6549 | #44 | ILLUMINATION STRING 5 |



## SOLENOID/FLASHER TABLE — PDF page 129, printed 2-55

Duplicate printing on PDF page 135 (printed 3-5) was visually compared.

| Sol. No. | Function | Solenoid Type | Voltage Playfield | Voltage Insert | Voltage Cabinet | Drive Xistor | Drive Playfield | Drive Insert | Drive Cabinet | Drive Wire Color | Part Number Playfield | Part Number Insert |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 01 | AUTO PLUNGER | High Power | J133-2 | [blank] | [blank] | Q72 | J116-1 | [blank] | [blank] | VIO-BRN | AE-26-1200 | [blank] |
| 02 | TROUGH EJECT | High Power | J133-2 | [blank] | [blank] | Q68 | J116-2 | [blank] | [blank] | VIO-RED | AE-26-1500 | [blank] |
| 03 | LEFT SCOOP POWER | High Power | J133-2 | [blank] | [blank] | Q71 | J116-4 | [blank] | [blank] | VIO-ORG | FL-22241 | [blank] |
| 04 | RIGHT SCOOP POWER | High Power | J133-2 | [blank] | [blank] | Q67 | J116-5 | [blank] | [blank] | VIO-YEL | FL-22241 | [blank] |
| 05 | CORNER KICKOUT | High Power | J133-2 | [blank] | [blank] | Q70 | J116-6 | [blank] | [blank] | VIO-GRN | AE-30-2000 | [blank] |
| 06 | POST POWER | High Power | J133-2 | [blank] | [blank] | Q66 | J116-7 | [blank] | [blank] | VIO-BLU | FL-22241 | [blank] |
| 07 | ROPE MAGNET | High Power | J133-2 | [blank] | [blank] | Q69 | J116-8 | [blank] | [blank] | VIO-BLK | 20-10197 | [blank] |
| 08 | POST DIVERTER | High Power | J133-2 | [blank] | [blank] | Q65 | J116-9 | [blank] | [blank] | VIO-GRY | AE-27-1200 | [blank] |
| 09 | LEFT SCOOP HOLD | Low Power | J133-2 | [blank] | [blank] | Q44 | J113-1 | [blank] | [blank] | BRN-BLK | FL-22241 | [blank] |
| 10 | RIGHT SCOOP HOLD | Low Power | J133-2 | [blank] | [blank] | Q48 | J113-3 | [blank] | [blank] | BRN-RED | FL-22241 | [blank] |
| 11 | RIGHT ARM | Low Power | J133-3 | [blank] | [blank] | Q43 | J113-4 | [blank] | [blank] | BRN-ORG | 04-11000 | [blank] |
| 12 | POST HOLD | Low Power | J133-2 | [blank] | [blank] | Q47 | J113-5 | [blank] | [blank] | BRN-YEL | FL-22241 | [blank] |
| 13 | LEFT ARM | Low Power | J133-3 | [blank] | [blank] | Q42 | J113-6 | [blank] | [blank] | BRN-GRN | 04-11000 | [blank] |
| 14 | POPPER | Low Power | J133-3 | [blank] | [blank] | Q46 | J113-7 | [blank] | [blank] | BRN-BLU | AE-27-1200 | [blank] |
| 15 | LEFT SLINGSHOT | Low Power | J133-3 | [blank] | [blank] | Q41 | J113-8 | [blank] | [blank] | BRN-VIO | AE-26-1200 | [blank] |
| 16 | RIGHT SLINGSHOT | Low Power | J133-3 | [blank] | [blank] | Q45 | J113-9 | [blank] | [blank] | BRN-GRY | AE-26-1200 | [blank] |
| 17 | BOXER FLASHER (3) | Flasher | J133-6 | [blank] | [blank] | Q28 | J111-1 | [blank] | [blank] | BLK-BRN | #906 (3) | [blank] |
| 18 | DANGER ZONE FLASHER (2) | Flasher | J133-6 | [blank] | [blank] | Q32 | J111-2 | [blank] | [blank] | BLK-RED | #906 (2) | [blank] |
| 19 | JUMP ROPE FLASHER (2) | Flasher | J133-6 | J134-5 | [blank] | Q27 | J111-3 | J112-3 | [blank] | BLK-ORG | #906 (1) | #906 (1) |
| 20 | LOCK KICKOUT (2) | Flasher | J133-6 | J134-5 | [blank] | Q31 | J111-4 | J112-5 | [blank] | BLK-YEL | #906 (1) | #906 (1) |
| 21 | LEFT KICKOUT (3) | Flasher | J133-6 | J134-5 | [blank] | Q26 | J111-5 | J112-6 | [blank] | BLU-GRN | #906 (1) | #906 (2) |
| 22 | BOXER FLASHER (3) | Flasher | J133-6 | J134-5 | [blank] | Q30 | J111-6 | J112-7 | [blank] | BLU-BLK | #906 (2) | #906 (1) |
| 23 | JUMP ROPE FLASHER | Flasher | J133-6 | [blank] | [blank] | Q25 | J111-7 | [blank] | [blank] | BLU-VIO | #906 (1) | [blank] |
| 24 | SPEED BAG FLASHER | Flasher | J133-6 | [blank] | [blank] | Q29 | J111-8 | [blank] | [blank] | BLU-GRY | #906 (1) | [blank] |
| 25 | ROPE MOTOR | Gen. Purpose | J141-2 | [blank] | [blank] | Q16 | J109-1 | [blank] | [blank] | BLU-BRN | SEE NOTE 1 | [blank] |
| 26 | TOGGLE DIRECTION | Gen. Purpose | J141-2 | [blank] | [blank] | Q15 | J109-2 | [blank] | [blank] | BLU-RED | SEE NOTE 2 | [blank] |
| 27 | MOTOR ON/OFF | Gen. Purpose | J141-2 | [blank] | [blank] | Q14 | J109-3 | [blank] | [blank] | BLU-ORG | SEE NOTE 2 | [blank] |
| 28 | †LOCK PIN | Gen. Purpose | J133-1 | [blank] | [blank] | Q13 | J109-4 | [blank] | [blank] | BLU-YEL | AE-26-1500 | [blank] |

Footnotes:

- †The tieback diode for solenoid 28, Lock Pin, is at J109-9.
- NOTE 1: Solenoid 25, Rope Motor, uses a Motor EMI board, p/n A-15542 (Qty. 1), and a motor, p/n 14-8038 (Qty. 1).
- NOTE 2: Solenoid 26 Toggle Direction, and solenoid 27 Motor On/Off, work in tandem and use a TTL Bi-direct Motor board, p/n A-22013 (Qty. 1), and a motor, p/n 14-8036 (Qty.1).
- NOTE 3: The 24 LED Display uses two boards: The Serial 24 Driver Board, part number A-21967-2 (Qty. 1), and the 24 LED Assembly, part number A-21991 (Qty. 2).

## Flipper Circuits — PDF page 129, printed 2-55

| Item | Function | Solenoid Type | Voltage Connection | Drive Xistor Power | Drive Xistor Hold | Drive Connection | Wire Color Power | Wire Color Hold | Coil Part No. | Coil Colors |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 29 | LOWER RIGHT FLIPPER [merged rows 29–30] | Power | J119-1 (RED-GRN) | Q90 | [blank] | J120-13 | YEL-GRN | [blank] | FL-15411 [merged rows 29–30] | BLU [merged rows 29–30] |
| 30 | [merged from 29] | Hold | J119-1 (RED-GRN) | [blank] | Q92 | J120-11 | [blank] | ORG-GRN | [merged from 29] | [merged from 29] |
| 31 | LOWER LEFT FLIPPER [merged rows 31–32] | Power | J119-4 (RED-BLU) | Q87 | [blank] | J120-9 | YEL-BLU | [blank] | FL-15411 [merged rows 31–32] | BLU [merged rows 31–32] |
| 32 | [merged from 31] | Hold | J119-4 (RED-BLU) | [blank] | Q89 | J120-7 | [blank] | ORG-BLU | [merged from 31] | [merged from 31] |
| 33 | ROPE POPPER | Power | J119-6 (RED-VIO) | Q84 | [blank] | J120-6 | YEL-VIO | [blank] | AE-30-2000 | VIO |
| 34 | RAMP DIVERTER | Hold | J119-6 (RED-VIO) | [blank] | Q86 | J120-4 | [blank] | ORG-VIO | [blank] | [blank] |
| 35 | LEFT SPEED BAG | Power | J119-8 (RED-GRY) | Q81 | [blank] | J120-3 | YEL-GRY | [blank] | AE-27-1200 | WHT |
| 36 | RIGHT SPEED BAG | Hold | J119-8 (RED-GRY) | [blank] | Q83 | J120-1 | [blank] | ORG-GRY | AE-27-1200 | WHT |

## 24 LED Display circuit table — PDF page 129, printed 2-55

| Item | Solenoid Type | Playfield Voltage Connection | Drive Gates | Playfield Drive Connection | Drive Wire Colors | Device Part Number |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 37 | Low Power | J138-2 | U3A, U3B | J110-1 | BRN-WHT | SEE NOTE 3 |
| 38 | Low Power | J138-2 | U3C, U3D | J110-3 | ORG-WHT | SEE NOTE 3 |
| 39 | Low Power | J138-2 | U3G, U3H | J110-4 | YEL-WHT | SEE NOTE 3 |
| 40 | Low Power | J138-2 | U3E, U3F | J110-5 | BLU-WHT | SEE NOTE 3 |

## General Illumination circuit table — PDF page 129, printed 2-55

| Item | Function | Solenoid Type | Voltage Playfield | Voltage Insert | Voltage Cabinet | Drive Xistor | Drive Playfield | Drive Insert | Drive Cabinet | Drive Wire Color | Bulb Playfield | Bulb Insert |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 01 | ILLUMINATION STRING 1 | G.I. | [blank] | J106-1 | [blank] | Q5 | [blank] | J106-7 | [blank] | WHT-BRN | [blank] | #555 |
| 02 | ILLUMINATION STRING 2 | G.I. | [blank] | J106-2 | [blank] | Q4 | [blank] | J106-8 | [blank] | WHT-ORG | [blank] | #555 |
| 03 | ILLUMINATION STRING 3 | G.I. | J105-3 | [blank] | [blank] | Q3 | J105-9 | [blank] | [blank] | WHT-YEL | #44 | [blank] |
| 04 | *ILLUMINATION STRING 4 | G.I. | J105-5 | [blank] | [blank] | Q2 | J105-10 | [blank] | [blank] | WHT-GRN | #44 | [blank] |
| 05 | *ILLUMINATION STRING 5 | G.I. | J105-6 | [blank] | J104-3 | Q1 | J105-11 | [blank] | J104-1 | WHT-VIO | #44 | [blank] |

Footnotes: `*These general illumination strings do not brighten and dim, they are always on.` `24-6549 = #44 bulb; 24-8768 = #555 bulb; 24-8704 = #89 bulb; 24-8802 = #906 bulb.`


## Literal differences and uncertainties

- PDF page 124 (printed 2-50), Switch Locations, item 31, Description: TROUGH ELECT PDF page 127 (printed 2-53), switch matrix item 31 reads TROUGH EJECT; PDF page 120 (printed 2-46), item 02 also reads TROUGH EJECT.
- PDF page 120 (printed 2-46), Solenoid/Flasher Locations items 19–22: Printed item numbers 19, 20, 21, and 22 each occur on multiple distinct rows. Every printed row and repeated item number is retained in source order; no rows were deduplicated.
- PDF pages 127–129 (printed 2-53–2-55): Connector labels visibly skip some numeric pin positions (including J206-8, J208-6, J121-8, and J125-3). Only printed labels were transcribed; no missing connector entries were inferred.
- PDF page 129 (printed 2-55), Flipper Circuits: Function and coil part/color cells span paired rows 29–30 and 31–32. Merged cells are marked as merged and continuation cells are explicit in the JSON.
