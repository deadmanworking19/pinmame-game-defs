# Coils detailed chart table, front reference

Source: Sega Godzilla manual, PDF page 8, printed `DR. 6`; SHA-256
`fc71e6584b2a8ad715100f94b5d4d690b0cd3864cd9abd6746c2441ad4d6c1c5`.
Method: Windows.Media.Ocr for navigation, then manual transcription from the
native-resolution render by `tools/render_excerpt_image.py` (150 dpi, embedded
1280-pixel scan). Transcribed by: curator. Review: candidate pending a second
visual check of the small part numbers, especially the dark UK-only rows.
`[unclear]` marks text that cannot yet be read reliably; it is not a blank.

Every row prints `I/O Pwr. Drvr.` in the Driver Output Board column. Repeating
that common value here is a transcription shorthand, not a merged printed cell.
The printed voltage and GA/turn designation are preserved independently of the
smaller manufacturer part number.

| Printed number and name | Drive transistor | D.T. control line color | D.T. control line connect | Power line color | Power line connection | Power voltage | Coil (GA/Turn), motor or bulb; part number |
|---|---|---|---|---|---|---|---|
| #1 TROUGH UP-KICKER | Q1 | BRN-BLK | J8-P1 | YEL-VIO | J10-P4/5 | 50v DC | 26-1200; 090-5044-00T |
| #2 AUTO LAUNCH | Q2 | BRN-RED | J8-P3 | YEL-VIO | J10-P4/5 | 50v DC | 24-940; 090-5036-00B |
| #3 TOP MAGNET (ORBIT) | Q3 | BRN-ORG | J8-P4 | VIO-YEL | J10-P3 | 50v DC | 22-650; 090-5042-01 |
| #4 MIDDLE MAGNET (PFLD) | Q4 | BRN-YEL | J8-P5 | VIO-YEL | J10-P3 | 50v DC | 22-650; 090-5042-01 |
| #5 BOTTOM MAGNET (PFLD) | Q5 | BRN-GRN | J8-P6 | VIO-YEL | J10-P3 | 50v DC | 22-650; 090-5042-01 |
| #6 SHAKER MOTOR | Q6 | BRN-BLU | J8-P7 | RED-WHT | J17-P7 | 16v AC / 12v DC | Motor Only; 041-5029-01 |
| #7 FLASH SPINNER*2 | Q7 | BRN-VIO | J8-P8 | ORG | J6-P10 | 20v DC | #89 Bulb; 165-5000-89 |
| #8 EUROPEAN TOKEN DISPENSER | Q8 | BRN-GRY | J8-P9 | YEL-VIO | J10-P4/5 | 50v DC | Various (Call) |
| #9 LEFT TURBO BUMPER | Q9 | BLU-BRN | J9-P1 | YEL-VIO | J10-P4/5 | 50v DC | 26-1200; 090-5044-00T |
| #10 RIGHT TURBO BUMPER | Q10 | BLU-RED | J9-P2 | YEL-VIO | J10-P4/5 | 50v DC | 26-1200; 090-5044-00T |
| #11 BOTTOM TURBO BUMPER | Q11 | BLU-ORG | J9-P4 | YEL-VIO | J10-P4/5 | 50v DC | 26-1200; 090-5044-00T |
| #12 LEFT SLINGSHOT | Q12 | BLU-YEL | J9-P5 | YEL-VIO | J10-P4/5 | 50v DC | 23-800; 090-5091-00T |
| #13 RIGHT SLINGSHOT | Q13 | BLU-GRN | J9-P6 | YEL-VIO | J10-P4/5 | 50v DC | 23-800; 090-5091-00T |
| #14 LEFT MAGNET (LANE) | Q14 | BLU-BLK | J9-P7 | VIO-YEL | J10-P3 | 50v DC | 22-650; 090-5042-01 |
| #15 LEFT FLIPPER (50V RED/YEL) | Q15 | ORG-GRY | J9-P8 | RED-YEL / GRY-YEL | J10-P1/2 | 50v DC | 23-1100; 090-5030-00T |
| #16 RIGHT FLIPPER (50V RED/YEL) | Q16 | ORG-VIO | J9-P9 | RED-YEL / BLU-YEL | J10-P1/2 | 50v DC | 23-1100; 090-5030-00T |
| #17 RAMP DIVERTER | Q17 | VIO-BRN | J7-P2 | BRN | J7-P1 | 20v DC | 32-1800; 090-5031-00T |
| #18 FLASH LT*1 | Q18 | VIO-RED | J7-P3 | ORG | J6-P10 | 20v DC | #89 Bulb; 165-5000-89 |
| #19 FLASH RT*1 | Q19 | VIO-ORG | J7-P4 | ORG | J6-P10 | 20v DC | #89 Bulb; 165-5000-89 |
| #20 FLASH INNER LT ORBIT*2 | Q20 | VIO-YEL | J7-P6 | ORG | J6-P10 | 20v DC | #89 Bulb; 165-5000-89 |
| #21 LT OUTLANE (UK ONLY) | Q21 | VIO-GRN | J7-P7 | BRN | J7-P1 | 20v DC | 28-1050; [part number unclear] |
| #22 RT OUTLANE (UK ONLY) | Q22 | VIO-BLU | J7-P8 | BRN | J7-P1 | 20v DC | 28-1050; [part number unclear] |
| #23 UP/DOWN POST (UK ONLY) | Q23 | VIO-BLK | J7-P9 | BRN | J7-P1 | 20v DC | 23-1100; [part number unclear] |
| #24 OPTIONAL COIN METER | Q24 | VIO-GRY | J7-P10 | RED | J16-P7 | 5v DC | Meter 5V; [part number unclear] |
| #F1 FLASH POPS*4 | Q25 | BLK-BRN | J6-P1 | ORG | J6-P10 | 20v DC | #89 Bulb; 165-5000-89 |
| #F2 FLASH TOP LT*2 | Q26 | BLK-RED | J6-P2 | ORG | J6-P10 | 20v DC | #89 Bulb; 165-5000-89 |
| #F3 FLASH CTR PFLD*1 | Q27 | BLK-ORG | J6-P3 | ORG | J6-P10 | 20v DC | #89 Bulb; 165-5000-89 |
| #F4 FLASH RAMP #4*1 | Q28 | BLK-YEL | J6-P4 | ORG | J6-P10 | 20v DC | #89 Bulb; 165-5000-89 |
| #F5 FLASH LITE GODZ*1 | Q29 | BLK-GRN | J6-P5 | ORG | J6-P10 | 20v DC | #89 Bulb; 165-5000-89 |
| #F6 FLASH SCORE DOES...*1 | Q30 | BLK-BLU | J6-P6 | ORG | J6-P10 | 20v DC | #89 Bulb; 165-5000-89 |
| #F7 FLASH SLINGS*4 | Q31 | BLK-VIO | J6-P7 | ORG | J6-P10 | 20v DC | #89 Bulb; 165-5000-89 |
| #F8 FLASH TOP RT*2 | Q32 | BLK-GRY | J6-P8 | ORG | J6-P10 | 20v DC | #89 Bulb; 165-5000-89 |

Printed section headings are `High Current Coils Group 1`, `High Current Coils
Group 2`, `Low Current Coils Group 1` and `Flash Lamps (FLASH)`. Rows 21–23 are
dark-shaded and explicitly say `UK ONLY`; rows 8 and 24 are shaded as well.
The flash-lamp note says the Flash Lamps menu tests F1–F8 only and directs the
reader to SINGLE or CYCLING COIL TESTS for the others. The note and the small
legend above the flash section still need a literal, character-by-character read.
