# Stern Family Guy (2007) — lamp matrix (manual transcription)

Status: **transcribed from the rendered factory page; not independently reviewed.** Literal transcription; no source-authority or spatial decision.

## Source and transcription envelope

| Field | Value |
| --- | --- |
| Source | *Family Guy Pinball Service Game Manual*, Stern Pinball, Inc., January 2008, v12.0+ |
| PDF SHA-256 | `2bbcfa34ad70ab90c0fadabaf825850cecae58c8028af9aaabf8be1ad01979cd` |
| Locator | PDF page **23**, heading "LAMP MATRIX GRID [#1 – #80]" (printed "FULL SIZE MATRIXES", DR. 4 & DR. 6); location drawing PDF page **9**, printed "DR. 7", "LAMP LOCATIONS" |
| Method | Visual transcription of 300 dpi renders of PDF page 23, two-row bands read left and right half. |
| Blank-cell convention | `— (printed blank)` means the printed cell was visibly empty. |

The printed page states, on PDF page 9: "THERE ARE NO CONTROLLED LAMPS LOCATED ON THE BACK PANEL." Lamp-location legend: white box = lamps above playfield, black box = lamps below playfield. Part notes: "#555 Wedge Base (W.B.) Bulb Clear = 165-5002-00. #44 Bayonet Bulb (Heavy Filament) Clear = 165-5000-44-HF." The mini-playfield letters are labelled "THE 'LETTERS OF EACH NAME' LAMPS ARE NOT CONTROLLED LAMPS IN THE LAMP MATRIX. SEE SECTION 5, PAGES 142-143 FOR LEDs ON THE LED PCB." (transcribed separately in `manual-mini-playfield-led-board.md`).

## Lamp matrix columns (18VDC drive, I/O Power Driver board)

| Column | Printed IC | Voltage | Wire | Connector pin |
| --- | --- | --- | --- | --- |
| 01 | IC-U17 | 18VDC | YEL-BRN | J13-P9 |
| 02 | IC-U16 | 18VDC | YEL-RED | J13-P8 |
| 03 | IC-U15 | 18VDC | YEL-ORG | J13-P7 |
| 04 | IC-U14 | 18VDC | YEL-BLK | J13-P6 |
| 05 | IC-U13 | 18VDC | YEL-GRN | J13-P5 |
| 06 | IC-U12 | 18VDC | YEL-BLU | J13-P4 |
| 07 | IC-U11 | 18VDC | YEL-VIO | J13-P3 |
| 08 | IC-U10 | 18VDC | YEL-GRY | J13-P1 |

## Lamp matrix rows (ground return, I/O Power Driver board)

| Row | Printed transistor | Wire | Connector pin | Lamps |
| --- | --- | --- | --- | --- |
| 01 | Q33 | RED-BRN | J12-P1 | 1–8 |
| 02 | Q34 | RED-BLK | J12-P2 | 9–16 |
| 03 | Q35 | RED-ORG | J12-P3 | 17–24 |
| 04 | Q36 | RED-YEL | J12-P4 | 25–32 |
| 05 | Q37 | RED-GRN | J12-P5 | 33–40 |
| 06 | Q38 | RED-BLU | J12-P6 | 41–48 |
| 07 | Q39 | RED-VIO | J12-P8 | 49–56 |
| 08 | Q40 | RED-GRY | J12-P9 | 57–64 |
| 09 | Q41 | RED-WHT | J12-P10 | 65–72 |
| 10 | Q42 | RED | J12-P11 | 73–80 |

## Lamp grid, lamps 1–80

Lamp number = 8 × (row − 1) + column. "Bulb" is the faint grey bulb legend printed at the top of each cell and "P/N" the faint grey part number at the bottom of each cell; both are printed for every non-"NOT USED" cell, but only cells 1–3 and 61 print the part number in bold.

| LP. # | Literal printed name | Bulb legend | P/N | Marking |
| ---: | --- | --- | --- | --- |
| 1 | START BUTTON | #555 Clear | 165-5002-00 | — |
| 2 | TOURNAMENT START BUTTON | #CM86 Clear | 165-5103-00 | — |
| 3 | FAMILY PETER | #555 Clear | 165-5002-00 | — |
| 4 | FAMILY LOIS | #44 Clear | 165-5000-44-HF | — |
| 5 | FAMILY BRIAN | #44 Clear | 165-5000-44-HF | — |
| 6 | FAMILY CHRIS | #44 Clear | 165-5000-44-HF | — |
| 7 | FAMILY MEG | #44 Clear | 165-5000-44-HF | — |
| 8 | FAMILY STEWIE | #44 Clear | 165-5000-44-HF | — |
| 9 | ( P ) INBALL | #555 Clear | 165-5002-00 | — |
| 10 | P ( I ) NBALL | #44 Clear | 165-5000-44-HF | — |
| 11 | PI ( N ) BALL | #44 Clear | 165-5000-44-HF | — |
| 12 | PIN ( B ) ALL | #44 Clear | 165-5000-44-HF | — |
| 13 | PINB ( A ) LL | #44 Clear | 165-5000-44-HF | — |
| 14 | PINBA ( L ) L | #44 Clear | 165-5000-44-HF | — |
| 15 | PINBAL ( L ) | #44 Clear | 165-5000-44-HF | — |
| 16 | LEFT OUTLANE [NOT SPECIAL] | #44 Clear | 165-5000-44-HF | — |
| 17 | LEFT RETURN [2X LOIS] | #555 Clear | 165-5002-00 | — |
| 18 | RAISE DEATH [LEFT INNER] | #44 Clear | 165-5000-44-HF | — |
| 19 | GOOD OLD BOYS | #44 Clear | 165-5000-44-HF | — |
| 20 | SUPER GRIFFINS | #44 Clear | 165-5000-44-HF | — |
| 21 | CHICKEN FIGHT | #44 Clear | 165-5000-44-HF | — |
| 22 | SEXY PARTY | #44 Clear | 165-5000-44-HF | — |
| 23 | IPECAC CONTEST | #44 Clear | 165-5000-44-HF | — |
| 24 | ( 1 ) [BY RT. SLING] | #44 Clear | 165-5000-44-HF | — |
| 25 | ( 2 ) [BY RT. SLING.] | #555 Clear | 165-5002-00 | — |
| 26 | ( 3 ) [BY RT. SLING] | #44 Clear | 165-5000-44-HF | — |
| 27 | RT RETURN [2X MEG] | #44 Clear | 165-5000-44-HF | — |
| 28 | RT. OUTLANE [SPECIAL] | #44 Clear | 165-5000-44-HF | — |
| 29 | TV [SCOOP] | #44 Clear | 165-5000-44-HF | — |
| 30 | PINBALL [SCOOP] | #44 Clear | 165-5000-44-HF | — |
| 31 | MULTIBALL [SCOOP] | #44 Clear | 165-5000-44-HF | — |
| 32 | MEG JACKPOT | #44 Clear | 165-5000-44-HF | — |
| 33 | PIRATE [STAND-UP] | #555 Clear | 165-5002-00 | — |
| 34 | RT. NEWTON JACKPOT | #44 Clear | 165-5000-44-HF | — |
| 35 | FAR ( T ) [4-BNK DRP/TRG] | #44 Clear | 165-5000-44-HF | — |
| 36 | FA ( R ) T [4-BNK DRP/TRG] | #44 Clear | 165-5000-44-HF | — |
| 37 | F ( A ) RT [4-BNK DRP/TRG] | #44 Clear | 165-5000-44-HF | — |
| 38 | ( F ) ART [4-BNK DRP/TRG] | #44 Clear | 165-5000-44-HF | — |
| 39 | LEFT ORBIT CHRIS | #44 Clear | 165-5000-44-HF | — |
| 40 | LEFT ORBIT JACKPOT | #44 Clear | 165-5000-44-HF | — |
| 41 | DEATH [1-BNK DRP/TRG] | #555 Clear | 165-5002-00 | — |
| 42 | SKILL SHOT | #44 Clear | 165-5000-44-HF | — |
| 43 | 200K [TO LEFT RAMP] | #44 Clear | 165-5000-44-HF | — |
| 44 | 300K [TO LEFT RAMP] | #44 Clear | 165-5000-44-HF | — |
| 45 | 400K [TO LEFT RAMP] | #44 Clear | 165-5000-44-HF | — |
| 46 | 500K [TO LEFT RAMP] | #44 Clear | 165-5000-44-HF | — |
| 47 | CRAZY CHRIS [TO LEFT RAMP] | #44 Clear | 165-5000-44-HF | — |
| 48 | COLLECT BEERS [BEER CAN] | #44 Clear | 165-5000-44-HF | — |
| 49 | GIGGITY GIGGITY [BEER CAN] | #555 Clear | 165-5002-00 | — |
| 50 | HAPPY HOUR [BEER CAN] | #44 Clear | 165-5000-44-HF | — |
| 51 | REMEMBER WHEN [BEER CAN] | #44 Clear | 165-5000-44-HF | — |
| 52 | LARD MULTIBALL [BEER CAN] | #44 Clear | 165-5000-44-HF | — |
| 53 | EXTRA BALL [LEFT NEWTON] | #44 Clear | 165-5000-44-HF | — |
| 54 | LEFT NEWTON JACKPOT | #44 Clear | 165-5000-44-HF | — |
| 55 | EVIL MONKEY JACKPOT | #44 Clear | 165-5000-44-HF | — |
| 56 | 3-BANK TOP [ 'X' STAND-UP] | #44 Clear | 165-5000-44-HF | — |
| 57 | 3-BANK MID [ 'X' STAND-UP] | #555 Clear | 165-5002-00 | — |
| 58 | 3-BANK BOT [ 'X' STAND-UP] | #44 Clear | 165-5000-44-HF | — |
| 59 | NOT USED | — (printed blank) | — (printed blank) | — |
| 60 | NOT USED | — (printed blank) | — (printed blank) | — |
| 61 | BOTTOM BUMPER | LED WB WHT | 112-5024-08 | « D.O.T.S. » |
| 62 | DRUNKEN CLAM [MYSTERY] | #44 Clear | 165-5000-44-HF | — |
| 63 | STEWIE [STAND-UP X2] | #44 Clear | 165-5000-44-HF | — |
| 64 | SHOOT AGAIN | #44 Clear | 165-5000-44-HF | — |
| 65 | RIGHT ORBIT LOIS | #555 Clear | 165-5002-00 | — |
| 66 | RIGHT ORBIT JACKPOT | #44 Clear | 165-5000-44-HF | — |
| 67 | SPINNER [LOIS] | #44 Clear | 165-5000-44-HF | — |
| 68 | MINI SHOOT AGAIN | #44 Clear | 165-5000-44-HF | — |
| 69 | BALL SAVER POST | #44 Clear | 165-5000-44-HF | — |
| 70 | STEWIE SPOT LIGHT | #44 Clear | 165-5000-44-HF | « D.O.T.S. » |
| 71 | NOT USED | — (printed blank) | — (printed blank) | — |
| 72 | NOT USED | — (printed blank) | — (printed blank) | — |
| 73 | NOT USED | — (printed blank) | 165-5002-00 (faint, printed in a shaded cell) | — |
| 74 | NOT USED | — (printed blank) | 165-5000-44-HF (faint, printed in a shaded cell) | — |
| 75 | NOT USED | — (printed blank) | 165-5000-44-HF (faint, printed in a shaded cell) | — |
| 76 | NOT USED | — (printed blank) | 165-5000-44-HF (faint, printed in a shaded cell) | — |
| 77 | NOT USED | — (printed blank) | 165-5000-44-HF (faint, printed in a shaded cell) | — |
| 78 | NOT USED | — (printed blank) | 165-5000-44-HF (faint, printed in a shaded cell) | — |
| 79 | NOT USED | — (printed blank) | 165-5000-44-HF (faint, printed in a shaded cell) | — |
| 80 | NOT USED | — (printed blank) | 165-5000-44-HF (faint, printed in a shaded cell) | — |

Lamp-location drawing (PDF page 9, DR. 7): numbered boxes 61, 68 and 70 are drawn white (lamps above the playfield); every other numbered box that was read is black (below the playfield). Lamp 68 is the only box drawn on the "MINI-PLAYFIELD" inset. No box for lamp 1 or 2 (the cabinet start buttons) or for the NOT USED addresses 59, 60 and 71–80 was found on the drawing.
