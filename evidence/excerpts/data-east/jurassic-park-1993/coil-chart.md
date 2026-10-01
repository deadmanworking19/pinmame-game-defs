# Coil / flash-lamp drives 1-8: printed page 31 / PDF 35, drive schematic

Visually checked against the rendered factory PDF by primary Sonnet 5.5 curator, 2026-10-01. Literal full table region; Not Used rows and printed misprints are retained. OCR was navigation only. Drives 1-8 drive a left-set coil and a right-set flash-lamp bank through the PPB board's left/right relay (public 10). Drives 3 and 5 pass through PPB board transistors Q5 and Q3 ('TIP SEC') at J8 and connect at J7; the printed PPB boxes show +32 VL / +32 VR. The J2 and J9 pin boxes are in the retained crop (coil-schematic) and are not transcribed.

| Drive | Printed left-set coil | ROM cycle-test coil name | CPU transistor | CPU connector pin | Control wire to PPB J1 | Coil lead wire | Flash-lamp lead wire | Printed right-set bulb text | ROM cycle-test flash name |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1L / 1R | Top Eject | TOP RGT EJECT | Q46 | CN11-1 | GRY-BRN | VIO-BRN | BLK-BRN | (3) RAPTOR PIT (1) INSERT | FL: 2-RAPTOR 1-INS |
| 2L / 2R | Ball Release | BALL RELEASE | Q45 | CN11-3 | GRY-RED | VIO-RED | BLK-RED | (3) PLFD RIGHT SIDE (1) INSERT | FL: 3-R SIDE 1-INS |
| 3L / 3R | Auto Launch | AUTO LAUNCH 50V | Q44 | CN11-4 | GRY-ORG | WHT-ORG / VIO-ORG | BLK-ORG | (4) ORBIT SHOT | FL: 4-ORBIT |
| 4L / 4R | Left Scoop | LEFT SCOOP | Q43 | CN11-5 | GRY-YEL | VIO-YEL | BLK-YEL | (3) UPPER RIGHT PLFD (1) UPPER RIGHT CORNER | FL: TOP RGT. RMP 1.3.5 |
| 5L / 5R | Right VUK | RIGHT VUK 50V | Q42 | CN11-6 | GRY-GRN | WHT-GRN / VIO-GRN | BLK-GRN | (3) UPPER RIGHT PLFD (1) UPPER LEFT CORNER | FL: TOP LFT. RMP 2.4.6 |
| 6L / 6R | Diverter | RAMP DIVERTER | Q41 | CN11-7 | GRY-BLU | VIO-BLU | BLK-BLU | (3) LEFT SIDE PLFD (1) INSERT | FL: 3-L SIDE 1-INS |
| 7L / 7R | Dino Eject | T-REX EJECT | Q40 | CN11-8 | GRY-VIO | VIO-BLK | BLK-VIO | (4) TURBO BUMPER | FL: 3-POPS 1-TREX |
| 8L / 8R | Knocker | KNOCKER | Q39 | CN11-9 | GRY-BLK | VIO-GRY | BLK-GRY | (1) MOSQUITO (1) PLFD (2) TOP DISPLAY | FL: 1-MSQ 1-PFD 2-TOP |

# Drives 9-16: printed page 31 / PDF 35 and CPU CN12 (PDF 51)

Visually checked against the rendered factory PDF by primary Sonnet 5.5 curator, 2026-10-01. Literal full table region; Not Used rows and printed misprints are retained. OCR was navigation only.

| Drive | Printed name | ROM cycle-test name | CPU transistor | CPU connection | Wire | What it switches |
| --- | --- | --- | --- | --- | --- | --- |
| 9 | Raptor Pit | RAPTOR PIT 50V | Q30 | CPU CN12-1 | WHT/BRN | Raptor-pit kicker coil through PPB board Q4 (TIP security), +50 VDC at J7-3 |
| 10 | L/R Coil Relay | (not named by the cycle test) | Q29 | CPU CN12-2 | BLK-RED | PPB left/right coil relay (J7 terminals 9 and 7); +32 V from PS CN3-5 |
| 11 | G.I. Relay | RELAY: G.I. RELAY | Q28 | CPU CN12-4 | BRN-ORG | K-1 general-illumination relay on the power-supply board (PS CN7-1/3) |
| 12 | Motor (Left/Right) select | RELAY: MOTOR L/R | Q27 | CPU CN12-5 | BRN-YEL | (LEFT/RIGHT) BRN/YEL input of the bi-directional relay board 520-5066-00 for the T-Rex rotation motor |
| 13 | Dino Mouth | COIL: T-REX MOUTH | Q26 | CPU CN12-6 | BRN-GRN | T-Rex jaw coil, RED supply (+32 V) |
| 14 | Motor Up/Down | RELAY: MOTOR UP/DWN | Q25 | CPU CN12-7 | BRN-BLU | relay board 520-5010-00 switching 28 VAC (from BR2) to the T-Rex up/down motor |
| 15 | Motor On/Off | RELAY: MOTOR ON/OFF | Q24 | CPU CN12-8 | BRN-VIO | 28 VAC feed of the T-Rex rotation motor through bi-directional relay 520-5066-00 |
| 16 | Lockout | COIL: LOCK OUT | Q23 | CPU CN12-9 | BRN-GRY | trough lock-out coil, RED supply (+32 V) |

# CPU Controlled Auxiliary Solenoids: printed page 30 / PDF 34

Visually checked against the rendered factory PDF by primary Sonnet 5.5 curator, 2026-10-01. Literal full table region; Not Used rows and printed misprints are retained. OCR was navigation only.

| Coil | Printed name | Control wire | Control connection | Power wire | Power connection | Drive transistor | Printed coil type |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 17 | Top Turbo Bumper | BLU-BRN | CPU CN19-7 | RED | PS CN3-6 | Q11 | 23-800 |
| 18 | Left Turbo Bumper | BLU-RED | CPU CN19-4 | RED | PS CN3-6 | Q9 | 23-800 |
| 19 | Right Turbo Bumper | BLU-ORN | CPU CN19-3 | RED | PS CN3-6 | Q8 | 23-800 |
| 20 | Left Slingshot | BLU-YEL | CPU CN19-6 | RED | PS CN3-6 | Q10 | 23-800 |
| 21 | Right Slingshot | BLU-GRN | CPU CN19-8 | RED | PS CN3-6 | Q12 | 23-800 |
| 22 | Shaker Motor (See Schematic) | BLU-BLK | CPU CN19-9 | VIO-YEL | J7-3 | Q13 | 23-800 |

# Flipper solenoids: printed page 30 / PDF 34

Visually checked against the rendered factory PDF by primary Sonnet 5.5 curator, 2026-10-01. Literal full table region; Not Used rows and printed misprints are retained. OCR was navigation only.

| Coil | Part | Flipper GND (CPU to flip switch) | Flip switch to flip PCB | Power lines flip PCB to coil | Printed coil type | Power input to flip PCB |
| --- | --- | --- | --- | --- | --- | --- |
| Left Flipper | 090-5020-30 | ORN-GRY CPU CN19-2 | BLU-GRY CN1-9 | GRY-YEL CN2-4,5 | 23-900 | BLK-WHT 50VDC / GRY, GRY-GRN 8VAC |
| Right Flipper | 090-5020-30 | ORN-VIO CPU CN19-1 | BLU-VIO CN1-1 | BLU-YEL CN2-7,8 | 23-900 | BLK-WHT 50VDC / GRY, GRY-GRN 8VAC |
| Upper Right Flipper | 090-5041-00 | ORN-VIO CPU CN19-1 | GRY-VIO CN1-12 | BLK-YEL CN2-1,2 | 25-1800 | BLK-WHT 50VDC / GRY, GRY-GRN 8VAC |

# Coil parts from the unique-parts assembly pages: printed pages 33-43 / PDF 41-47

Visually checked against the rendered factory PDF by primary Sonnet 5.5 curator, 2026-10-01. Literal full table region; Not Used rows and printed misprints are retained. OCR was navigation only. The schematic prints coil type 23-840 for the whole left set; the unique-parts pages give each assembly's own coil.

| Coil | Assembly | Coil printed on that page | Coil part |
| --- | --- | --- | --- |
| 1 | 500-5664-00 | 24-940 | 090-5636-02 |
| 2 | 500-5683-00 | 23-800 | 090-5001-00 |
| 3 | 500-5477-00 | 23-800 | 090-5001-01 |
| 4 | 515-5772-00 | 23-800 | 090-5001-01 |
| 5 | 500-5116-04 | 23-800 | 090-5001-01 |
| 6 | 500-5661-00 | 27-1500 | 090-5004-02 |
| 7 | 500-5665-00 | 27-1500 | 090-5004-02 |
| 8 | 500-5081-00 | 23-800 | 090-5001-01 |
| 9 | 500-5081-00 | 23-800 | 090-5001-01 |
| 13 | 500-5667-00 | 25-1240 | 090-5034-00 |
| 16 | 500-5684-00 | 25-1240 | 090-5034-00 |
| 17 | 500-5227-00 | 23-800 | 090-5001-00 |
| 18 | 500-5227-00 | 23-800 | 090-5001-00 |
| 19 | 500-5227-00 | 23-800 | 090-5001-00 |
| 20 | 500-5226-00 | 23-800 | 090-5001-02 |
| 21 | 500-5226-00 | 23-800 | 090-5001-02 |
