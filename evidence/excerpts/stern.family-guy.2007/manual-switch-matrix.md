# Stern Family Guy (2007) — switch matrix and dedicated switches (manual transcription)

Status: **transcribed from the rendered factory page; not independently reviewed.** This is a literal transcription. It makes no source-authority, polarity or spatial decision.

## Source and transcription envelope

| Field | Value |
| --- | --- |
| Source | *Family Guy Pinball Service Game Manual*, Stern Pinball, Inc., January 2008, v12.0+ (Internet Archive item `Stern_Pinball_Family_Guy_Manual`) |
| Original PDF | `FG_FIND_IT_IN_FRONT.pdf` (170 pages) |
| PDF SHA-256 | `2bbcfa34ad70ab90c0fadabaf825850cecae58c8028af9aaabf8be1ad01979cd` |
| Locator | PDF page **23**, printed locator "FULL SIZE MATRIXES: FIND-IT-IN-FRONT (DR. 4 & DR. 6)", headings "SWITCH MATRIX GRID [#1 – #64]" and "Dedicated Switches (D-1 – D-32)" |
| Location drawing | PDF page **7**, printed "DR. 5", "SWITCH LOCATIONS"; legend: white box = switches above playfield, black box = switches below playfield, grey box = OPTO switch pairs above |
| Method | Visual transcription of 300 dpi renders of PDF page 23 (cropped by quadrant). The PDF's own text layer is unusable (font-encoding garbage), so no text extraction was used. |
| Blank-cell convention | `— (printed blank)` means the printed cell was visibly empty; it is never completed from a neighbouring row. |

Printed text is reproduced literally, including line breaks flattened to spaces and bracketed qualifiers such as `[STAND-UP]`. The part-number column of the printed grid prints a location word under each part number: `below playfield`, `above playfield`, `a / b playfield` (printed grey), `2 per Asm.`, `Front Molding`, `In Cabinet`, `Cabinet Side`, `Flipper Asm.`, `Coin Door`, `Below P/F`. The printed wire-colour legend is BLK Black, BLU Blue, BRN Brown, GRY Gray, GRN Green, LGN Light Grn., ORG Orange, PNK Pink, RED Red, TAN Tan, VIO Violet, WHT White, YEL Yellow.

## Matrix drive rows (CPU/Sound board)

| Drive row | Switches | Printed drive transistor | Wire | Connector pin |
| --- | --- | --- | --- | --- |
| 01 | 1–16 | Q1 | GRN-BRN | J1-P1 |
| 02 | 17–32 | Q2 | GRN-RED | J1-P3 |
| 03 | 33–48 | Q3 | GRN-ORG | J1-P4 |
| 04 | 49–64 | Q4 | GRN-YEL | J1-P5 |

## Matrix return columns (CPU/Sound board)

| Column | Printed IC | Wire | Connector pin |
| --- | --- | --- | --- |
| 01 | IC-U22A | WHT-BRN | J6-P9 |
| 02 | IC-U22B | WHT-RED | J6-P8 |
| 03 | IC-U22C | WHT-ORG | J6-P7 |
| 04 | IC-U22D | WHT-YEL | J6-P6 |
| 05 | IC-U16A | WHT-GRN | J6-P5 |
| 06 | IC-U16B | WHT-BLU | J6-P3 |
| 07 | IC-U16C | WHT-VIO | J6-P2 |
| 08 | IC-U16D | WHT-GRY | J6-P1 |
| 09 | IC-U36A | TAN-BLK | J12-P9 |
| 10 | IC-U36B | TAN-RED | J12-P8 |
| 11 | IC-U36C | TAN-ORG | J12-P7 |
| 12 | IC-U36D | TAN-YEL | J12-P6 |
| 13 | IC-U40A | TAN-GRN | J12-P4 |
| 14 | IC-U40B | TAN-BLU | J12-P3 |
| 15 | IC-U40C | TAN-VIO | J12-P2 |
| 16 | IC-U40D | TAN-WHT | J12-P1 |

## Switch matrix grid, switches 1–64

Switch number = 16 × (drive row − 1) + return column. Columns: printed switch name, printed part number, printed location word. "NOT USED" cells are shaded in the printed grid and carry no part number.

| SW. # | Literal printed name | Printed part number | Printed location / marking |
| ---: | --- | --- | --- |
| 1 | BALL SAVER UP | 180-5010-04 | below playfield |
| 2 | BALL SAVER DOWN | 180-5010-04 | below playfield |
| 3 | LEFT ORBIT STAND-UP | 515-5162-08 | below playfield |
| 4 | RIGHT 2-BANK BOTTOM | 515-5162-08 | below playfield |
| 5 | RIGHT 2-BANK TOP | 515-5162-08 | below playfield |
| 6 | LEFT NEWTON ROLLOVER | 500-6227-01 | below playfield |
| 7 | RIGHT NEWTON ROLLOVER | 500-6227-02 | below playfield |
| 8 | PIRATE [STAND-UP] TARGET | 515-5967-04 | below playfield |
| 9 | 1-BANK DROP TARGET | 520-5252-01 | below playfield |
| 10 | MEG [STAND-UP] TARGET | 515-5162-08 | below playfield |
| 11 | NOT USED | — (printed blank) | — (printed blank) |
| 12 | NOT USED | — (printed blank) | — (printed blank) |
| 13 | TV EJECT | 180-5183-00 | « D.O.T.S. » mark; a / b playfield |
| 14 | NOT USED | — (printed blank) | — (printed blank) |
| 15 | TOURNAMENT START | 180-5119-03 | CABINET; Front Molding |
| 16 | START BUTTON | 180-5174-00 | CABINET; In Cabinet |
| 17 | NOT USED | — (printed blank) | — (printed blank) |
| 18 | (4-BALL) TROUGH #4 (L) | 180-5119-02 | below playfield |
| 19 | (4-BALL) TROUGH #3 | 180-5119-02 | below playfield |
| 20 | (4-BALL) TROUGH #2 | 180-5119-02 | below playfield |
| 21 | (VUK OPTO) TROUGH #1 (R) | TRANS. / REC. TX 515-0173-00, RX 515-0174-00 | below playfield |
| 22 | (STACK OPTO) TROUGH JAM | TRANS. / REC. TX 515-0173-00, RX 515-0174-00 | below playfield |
| 23 | SHOOTER LANE | 180-5157-00 | below playfield |
| 24 | LEFT OUTLANE | 500-6227-02 | below playfield |
| 25 | LEFT RETURN [LANE] | 500-6227-02 | below playfield |
| 26 | LEFT SLING | 180-5054-00 | 2 per Asm. |
| 27 | RIGHT SLING | 180-5054-00 | 2 per Asm. |
| 28 | RIGHT RETURN [LANE] | 500-6227-01 | below playfield |
| 29 | RIGHT OUTLANE | 500-6227--01 (printed with a double hyphen) | below playfield |
| 30 | TOP BUMPER | 180-5015-04 | below playfield |
| 31 | RIGHT BUMPER | 180-5015-04 | below playfield |
| 32 | BOTTOM BUMPER | 180-5015-04 | below playfield |
| 33 | LEFT RAMP MADE | 180-5087-00 | a / b playfield |
| 34 | NOT USED | — (printed blank) | — (printed blank) |
| 35 | EVIL MONKEY | 180-5119-02 | above playfield |
| 36 | NOT USED | — (printed blank) | — (printed blank) |
| 37 | NOT USED | — (printed blank) | — (printed blank) |
| 38 | NOT USED | — (printed blank) | — (printed blank) |
| 39 | RIGHT ORBIT SPINNER | 180-5010-04 | above playfield |
| 40 | DEATH RETURN [INNER LT.] | 500-6227-02 | below playfield |
| 41 | 3 BANK [STAND-UP] BOTTOM | 515-5162-08 | below playfield |
| 42 | 3 BANK [STAND-UP] MIDDLE | 515-5162-08 | below playfield |
| 43 | 3 BANK [STAND-UP] TOP | 515-5162-08 | below playfield |
| 44 | ( F ) ART [4-BANK DROP TGT.] | 520-5252-04 | below playfield |
| 45 | F ( A ) RT [4-BANK DROP TGT.] | 520-5252-04 | below playfield |
| 46 | FA ( R ) T [4-BANK DROP TGT.] | 520-5252-04 | below playfield |
| 47 | FAR ( T ) [4-BANK DROP TGT.] | 520-5252-04 | below playfield |
| 48 | SNEAK RAMP | 180-5183-00 | below playfield |
| 49 | BEER CAN ( BRIAN ) | 180-5189-00 | a / b playfield |
| 50 | MINI MEG TARGET [STAND-UP] | 511-5081-00 | below playfield |
| 51 | MINI PETER TARGET [STAND-UP] | 511-5081-00 | below playfield |
| 52 | MINI RIGHT ORBIT | 500-6775-00 | mini-playfield |
| 53 | MINI LEFT ORBIT | 500-6775-00 | mini-playfield |
| 54 | MINI RAMP | 500-6775-00 | mini-playfield |
| 55 | MINI TROUGH | 500-6775-01 | mini-playfield |
| 56 | NOT USED | — (printed blank) | — (printed blank) |
| 57 | RIGHT ORBIT | 500-6227-02 | below playfield |
| 58 | NOT USED | — (printed blank) | — (printed blank) |
| 59 | NOT USED | — (printed blank) | — (printed blank) |
| 60 | NOT USED | — (printed blank) | — (printed blank) |
| 61 | NOT USED | — (printed blank) | — (printed blank) |
| 62 | NOT USED | — (printed blank) | — (printed blank) |
| 63 | NOT USED | — (printed blank) | — (printed blank) |
| 64 | CLAM EJECT | 180-5209-00 | « D.O.T.S. » mark; below playfield |

Notes on the printed grid:

- The grid has no halftone "opto" marking. The optos are identified by the grid's own words (`VUK OPTO`, `STACK OPTO`, `TRANS. / REC.` with TX/RX board numbers on 21–22) and by the part numbers `500-6775-00/-01` (mini OPTO transceivers on 52–55) and `520-5252-01/-04` (slotted OPTO interrupter PCBs on the 1-bank and 4-bank drop-target assemblies), which the assembly and PCB pages (PDF pages 100–105, 115, 118, 133–135, 159–163) identify as optical.
- The 2008-and-later production run replaced the piezo stand-up sensor PCB on 50 and 51 with mechanical switch `511-5081-00` (PDF page 115, "2008+ FAMILY GUY PRODUCTION RUN NOTE"); the grid prints the mechanical part number.
- `D.O.T.S.` expands, per the lamp-location legend on PDF page 9, to "Diode On Terminal Strip": the diode of that switch is on a playfield terminal strip rather than at the switch.

## Dedicated switches, D-1 to D-24 and the DIP switch D-25 to D-32

Dedicated switches share a ground: D-1 to D-8 BLK at J2-P1/11 and J3-P10, D-9 to D-16 BLK at J3-P10, D-17 to D-24 BLK at J13-P10. The printed column heading names the source IC: D-1 to D-8 `IC-U2`, D-9 to D-16 `IC-U4`, D-17 to D-24 `IC-41`.

| SW. | Literal printed name | Wire | Connector pin | Printed part number | Printed location / marking |
| --- | --- | --- | --- | --- | --- |
| D-1 | LEFT COIN SLOT | PNK-BRN | J2-P2 | 180-5204-00 | Coin Door |
| D-2 | CENTER COIN SLOT/DBA | PNK-RED | J2-P3 | 180-5204-00 | Coin Door |
| D-3 | RIGHT COIN SLOT | PNK-ORG | J2-P4 | 180-5204-00 | Coin Door |
| D-4 | 4TH COIN SLOT | PNK-YEL | J2-P6 | 180-5204-00 | Coin Door |
| D-5 | 5TH COIN SLOT | PNK-GRN | J2-P7 | — (printed blank) | IF USED |
| D-6 | NOT USED | PNK-BLU | J2-P8 | — (printed blank) | — (printed blank) |
| D-7 | NOT USED | PNK-VIO | J2-P9 | — (printed blank) | — (printed blank) |
| D-8 | NOT USED | PNK-GRY | J2-P10 | — (printed blank) | — (printed blank) |
| D-9 | LEFT FLIPPER BUTTON | GRY-BRN | J3-P1 | 180-5164-01 | Cabinet Side |
| D-10 | LEFT FLIPPER E.O.S. | GRY-RED | J3-P2 | 180-5149-00 | Flipper Asm. |
| D-11 | RIGHT FLIPPER BUTTON | GRY-ORG | J3-P4 | 180-5160-01 | Cabinet Side |
| D-12 | RIGHT FLIPPER E.O.S. | GRY-YEL | J3-P5 | 180-5149-00 | Flipper Asm. |
| D-13 | UPR. LT. FLIPPER BUTTON | GRY-GRN | J3-P6 | 180-5164-01 | Cabinet Side |
| D-14 | NOT USED | GRY-BLU | J3-P7 | — (printed blank) | — (printed blank) |
| D-15 | UPR. RT. FLIPPER BUTTON | GRY-VIO | J3-P8 | 180-5164-01 (printed greyed) | NOT USED (highlighted); Cabinet Side (greyed) |
| D-16 | NOT USED | GRY-BLK | J3-P9 | — (printed blank) | — (printed blank) |
| D-17 | TILT PENDULUM (PLUMB BOB) | LGN-BRN | J13-P1 | See Sec. 4, Chp. 1, Pg. 63 for cab. parts | — |
| D-18 | SLAM TILT | LGN-RED | J13-P3 | 502-5032-00 | OPTIONAL; Optional Kit |
| D-19 | TICKET NOTCH | LGN-ORG | J13-P4 | 180-5119-02 | IF USED; Below P/F |
| D-20 | NOT USED | LGN-YEL | J13-P5 | — (printed blank) | — (printed blank) |
| D-21 | BACK (GREEN BUTTON) | LGN-BLK | J13-P6 | 180-5192-04 | Coin Door |
| D-22 | MINUS (< / – RED BUTTON) | LGN-BLU | J13-P7 | 180-5192-02 | Coin Door |
| D-23 | PLUS (+ / > RED BUTTON) | LGN-VIO | J13-P8 | 180-5192-02 | Coin Door |
| D-24 | SELECT (BLACK BUTTON) | LGN-GRY | J13-P9 | 180-5192-00 | Coin Door |
| D-25 … D-32 | DIP SWITCH POSITION #1 … #8, "ON / OFF" | — | — | — | printed under "CPU/SOUND BD. SW1 DIP SWITCH (located between Connectors J3/J13)" |

The printed "Typical Switch Wiring & Schematic" box on PDF page 7 prints a dedicated switch as `Dedicated Switch Inputs GRY-XXX` → `N.O. Normally Open Switch Terminal` / `COM. Common Switch Terminal` → `Ground BLACK`; the matrix switch as `GRN-XXX` column drive, through a blocking diode (1N4004) in series, to the `WHT-XXX or TAN-XXX` row return (the diode's polarity drawing is not transcribed here).
