# Batman Forever Tech Chart (820-6104-05)

Source: `Sega_1995_Batman_Forever_Tech_Chart_switch_matrix_lamp_matrix_fuse_list_coil_list.pdf`, SHA-256 `c8606a3d6c968f2ce04a028e38503430e76584ad3d614554a98517bf50c1fcc4`, one page, footer "820-6104-05 Game: Batman Forever™" and "© 1995 All Rights Reserved." IPDB machine 3593. Transcribed by the curator from a 300 dpi render of the 300 dpi colour scan and visually checked. The chart repeats the manual's lamp grid and coil table in the same layout and folds the parts list into its switch grid ("SWITCH MATRIX GRID (with Sw. Part N°s)"). The bulb column of the lamp grid and the switch grid's part numbers are reproduced in full here, with every cell where the chart's text differs from the manual (`switches.md`, `lamps.md`, `coils.md`).

## Switch Matrix Grid (with Sw. Part N°s), part numbers, all 64 cells

Switch: part. 1 —·—; 2 —·—; 3 500-5097-02; 4 180-5024-00; 5 180-5024-00; 6 180-5024-00; 7 180-5022-00; 8 180-5073-00; 9 NOT USED [shaded]; 10 NOT USED [shaded]; 11 180-5119-00; 12 180-5119-00; 13 180-5119-00; 14 180-5119-00; 15 520-5124/25; 16 180-5100-00; 17 NOT USED [shaded]; 18 180-5104-00; 19 180-5104-00; 20 180-5104-00; 21 180-5104-00; 22 500-5706-00; 23 500-5707-00; 24 500-5707-00; 25 180-5132-00; 26 180-5132-00; 27 180-5132-00; 28 180-5132-00; 29 180-5132-00; 30 500-5706-01; 31 NOT USED [shaded]; 32 180-5116-00; 33 500-5142-00; 34 500-5706-00; 35 180-5054-00; 36 180-5054-00; 37 500-5706-00; 38 500-5706-00; 39 500-5706-00; 40 180-5093-00; 41 180-5027-01; 42 180-5133-00; 43 180-5133-00; 44 180-5057-00; 45 180-5119-00; 46 180-5119-00; 47 500-5706-00; 48 500-5706-00; 49 180-5111-00; 50 180-5133-00; 51 180-5133-00; 52 180-5087-00; 53 180-5093-00; 54 180-5093-00; 55 180-5087-00; 56 180-5093-00; 57 180-5015-03; 58 180-5015-03; 59 180-5015-03; 60 180-5119-00; 61 180-5119-00; 62 180-5119-00; 63 180-5048-01; 64 180-5151-00.

The switch names read as the manual grid's (PDF 30), including 51 RIGHT BAD HEADS S-U, 53 LEFT RAMP EXIT and 54 MIDDLE RAMP EXIT; 58 is abbreviated "BOT. TURBO BUMPER", 63 reads "LT FLIPPER BUTTON VIA Q7/SSFB" and 64 "RT FLIPPER BUTTON VIA Q5/SSFB". Against the manual's parts list (PDF 31) the chart prints 180-5132-00 instead of 515-5967-11 for the five "?" stand-ups 25-29, and 180-5133-00 instead of 515-5162-08 for the four heads stand-ups 42, 43, 50 and 51.

## Lamp Matrix Grid (with Bulb #), bulb column, all 64 cells

Lamp: bulb. 1 #555; 2 #555; 3 #555; 4 #555; 5 #555; 6 #555; 7 #44; 8 #555; 9 #555; 10 #555; 11 #555; 12 #555; 13 #555; 14 #555; 15 #555; 16 #555; 17 #44; 18 #555; 19 #555; 20 #555; 21 #555; 22 #44; 23 #44; 24 #44; 25 #555; 26 #44; 27 #555; 28 #555; 29 #555; 30 #555; 31 #555; 32 #555; 33 #555; 34 #555; 35 #44; 36 NOT USED [shaded, no bulb]; 37 NOT USED [shaded, no bulb]; 38 NOT USED [shaded, no bulb]; 39 #44; 40 #555; 41 #555; 42 #555; 43 #555; 44 #555; 45 #555; 46 #555; 47 #555; 48 #44; 49 #44; 50 #44; 51 #555; 52 #44; 53 #44; 54 #555; 55 #555; 56 #555; 57 #555; 58 #555; 59 #555; 60 NOT USED [shaded, no bulb]; 61 #44; 62 #44; 63 #555; 64 #555.

The lamp names, wires and transistors in every cell read as in the manual grid. Differences from the manual: lamp 50 JACKPOT (LEFT RAMP) prints `#44` where the manual grid prints `#555`; column 5 prints `CN7-5` where the manual prints `GN7-5`.

## Coil table cells that differ from the manual

| Row | Column | Tech Chart | Manual (PDF 34) |
| --- | --- | --- | --- |
| 7L 4-BANK DROP TARGET RESET | Power Voltage | 50v L | 32v L |
| 10 LEFT & RIGHT (A/B) RELAY | Power Line Connection | PS CN 6-7 | PS CN 3-6, 7 |
| 10, 11, 14 | Description | each adds `520-5010-00` under the name | no part number |
| 22 LASER KICK 50V | Power Line Connection | PS CN 6-6, 7 | PPB J7-6, 7 |

Every other coil cell, including the bulb counts of 1R-8R and the shaded NOT USED rows 6L and 13, reads as in the manual.

## Other blocks

"Solid State 2-Flipper SSFB" fuse block (sic): F1 "3A 250vSlo-Blo 50v DC Output (All Fuses) Right Flipper"; F2 "3A 250v Slo-Blo 9v AC Holding"; F3 "3A 250v Slo-Blo 50v DC Output Left Flipper"; F4 "3A 250v Slo-Blo 9v AC Holding"; F5 "3A 250v Slo-Blo 50v DC Output Upper Right Flipper". "Typical Lamp Schematic": YEL 18V COL, RED GND ROW. Bulb legend: #555 Bulb (Wedge Base) 165-5002-00; #906 Bulb (Wedge Base) 165-5004-00; #44 Bulb (Bayonet) 165-5000-44; #455 Twinkle Bulb (Bayonet) 165-5003-00; #89 Bulb (Bayonet) 165-5000-89.
