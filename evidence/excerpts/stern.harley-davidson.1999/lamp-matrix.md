# Harley-Davidson (Stern) — Lamp Matrix Grid

Read from `Stern_Harley_Davidson_3rd_Edition_Pinball_Game_Service_Manual.pdf`, PDF page 6 (lower part), the front-matter
drawing printed `DR. 4` ("LAMP MATRIX GRID"). Every cell was read from a 200 dpi render and checked against the page's
decoded text layer. Lamp number = (row − 1) × 8 + column. A hyphen inside a printed name is the cell's own line break and
is kept ("SUPER JACK-PO / T (RED)" prints across two lines). "DOTS" marks a cell carrying the grid's vertical "Diode On
Terminal Strip" tag. A NOT USED cell is black and has no bulb line. Every column and row heading carries a small pale
"NOT USED" line under its number, as on the switch grid; row 10's whole heading is black and reads NOT USED.

## Columns (18v) and rows (GND)

| Column | Driver | Wire | Connector |
| --- | --- | --- | --- |
| 1 | U17 | YEL-BRN | J13-P9 |
| 2 | U16 | YEL-RED | J13-P8 |
| 3 | U15 | YEL-ORG | J13-P7 |
| 4 | U14 | YEL-BLK | J13-P6 |
| 5 | U13 | YEL-GRN | J13-P5 |
| 6 | U12 | YEL-BLU | J13-P4 |
| 7 | U11 | YEL-VIO | J13-P3 |
| 8 | U10 | YEL-GRY | J13-P1 |

| Row | Driver | Wire | Connector | Row heading |
| --- | --- | --- | --- | --- |
| 1 | Q33 | RED-BRN | J12-P1 |  |
| 2 | Q34 | RED-BLK | J12-P2 |  |
| 3 | Q35 | RED-ORG | J12-P3 |  |
| 4 | Q36 | RED-YEL | J12-P4 |  |
| 5 | Q37 | RED-GRN | J12-P5 |  |
| 6 | Q38 | RED-BLU | J12-P6 |  |
| 7 | Q39 | RED-VIO | J12-P8 |  |
| 8 | Q40 | RED-GRY | J12-P9 |  |
| 9 | Q41 | RED-WHT | J12-P10 |  |
| 10 | Q42 | RED | J12-P11 | NOT USED (whole heading black) |

## Lamps

| # | Row | Col | Name as printed | Bulb cell | DOTS |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | (H) ARLEY | #555 Bulb |  |
| 2 | 1 | 2 | H (A) RLEY | #555 Bulb |  |
| 3 | 1 | 3 | HA (R) LEY | #555 Bulb |  |
| 4 | 1 | 4 | HAR (L) EY | #555 Bulb |  |
| 5 | 1 | 5 | HARL (E) Y | #555 Bulb |  |
| 6 | 1 | 6 | HARLE (Y) | #555 Bulb |  |
| 7 | 1 | 7 | SUPER JACK-PO T (RED) | #44 Bulb |  |
| 8 | 1 | 8 | SUPER JACK-PO T (GRN) | #44 Bulb |  |
| 9 | 2 | 1 | (L) IVE | #44 Bulb |  |
| 10 | 2 | 2 | L (I) VE | #555 Bulb |  |
| 11 | 2 | 3 | LI (V) E | #555 Bulb |  |
| 12 | 2 | 4 | LIV (E) | #555 Bulb |  |
| 13 | 2 | 5 | (R) IDE | #555 Bulb |  |
| 14 | 2 | 6 | R (I) DE | #555 Bulb |  |
| 15 | 2 | 7 | RI (D) E | #555 Bulb |  |
| 16 | 2 | 8 | RID (E) | #44 Bulb |  |
| 17 | 3 | 1 | LT ORBIT GRN LIGHT | #555 Bulb |  |
| 18 | 3 | 2 | LT ORBIT YEL LIGHT | #555 Bulb |  |
| 19 | 3 | 3 | LT ORBIT RED LIGHT | #555 Bulb |  |
| 20 | 3 | 4 | 1ST GEAR | #555 Bulb |  |
| 21 | 3 | 5 | 2ND GEAR | #555 Bulb |  |
| 22 | 3 | 6 | 3RD GEAR | #555 Bulb |  |
| 23 | 3 | 7 | 4TH GEAR | #555 Bulb |  |
| 24 | 3 | 8 | 5TH GEAR | #555 Bulb |  |
| 25 | 4 | 1 | M-CYCLE GRN LIGHT | #555 Bulb |  |
| 26 | 4 | 2 | M-CYCLE YEL LIGHT | #555 Bulb |  |
| 27 | 4 | 3 | M-CYCLE RED LIGHT | #555 Bulb |  |
| 28 | 4 | 4 | LEFT TURBO BUMPER | #555 Bulb | DOTS |
| 29 | 4 | 5 | RT TURBO BUMPER | #555 Bulb | DOTS |
| 30 | 4 | 6 | BOT TURBO BUMPER | #555 Bulb | DOTS |
| 31 | 4 | 7 | TOP TURBO BUMPER | #555 Bulb | DOTS |
| 32 | 4 | 8 | SPEEDO- METER X2 | #555 Bulb |  |
| 33 | 5 | 1 | SUPER VUK GRN LIGHT | #555 Bulb |  |
| 34 | 5 | 2 | SUPER VUK YEL LIGHT | #555 Bulb |  |
| 35 | 5 | 3 | SUPER VUK RED LIGHT | #555 Bulb |  |
| 36 | 5 | 4 | BIKE S-U TARGET (LT) | #555 Bulb |  |
| 37 | 5 | 5 | BIKE S-U TARGET (RT) | #555 Bulb |  |
| 38 | 5 | 6 | RAMP S-U TARGET (LT) | #555 Bulb |  |
| 39 | 5 | 7 | RAMP S-U TARGET (RT) | #555 Bulb |  |
| 40 | 5 | 8 | SLIPPERY WHEN WET | #555 Bulb |  |
| 41 | 6 | 1 | RT RAMP GRN LIGHT | #555 Bulb |  |
| 42 | 6 | 2 | RT RAMP YEL LIGHT | #555 Bulb |  |
| 43 | 6 | 3 | RT RAMP RED LIGHT | #555 Bulb |  |
| 44 | 6 | 4 | PATCH | #555 Bulb |  |
| 45 | 6 | 5 | BIKERS BACK | #555 Bulb |  |
| 46 | 6 | 6 | RED LIGHT MULTIBALL | #555 Bulb |  |
| 47 | 6 | 7 | AUTO LAUNCH | #555 Bulb |  |
| 48 | 6 | 8 | LITE MYST- ERY RIDER | #555 Bulb |  |
| 49 | 7 | 1 | RT ORBIT GRN LIGHT | #555 Bulb |  |
| 50 | 7 | 2 | RT ORBIT YEL LIGHT | #555 Bulb |  |
| 51 | 7 | 3 | RT ORBIT RED LIGHT | #555 Bulb |  |
| 52 | 7 | 4 | NOT USED | | |
| 53 | 7 | 5 | NOT USED | | |
| 54 | 7 | 6 | NOT USED | | |
| 55 | 7 | 7 | NOT USED | | |
| 56 | 7 | 8 | NOT USED | | |
| 57 | 8 | 1 | STOP LIGHT GRN LIGHT | #44 Bulb |  |
| 58 | 8 | 2 | STOP LIGHT YEL LIGHT | #44 Bulb |  |
| 59 | 8 | 3 | STOP LIGHT RED LIGHT | #44 Bulb |  |
| 60 | 8 | 4 | NOT USED | | |
| 61 | 8 | 5 | NOT USED | | |
| 62 | 8 | 6 | NOT USED | | |
| 63 | 8 | 7 | NOT USED | | |
| 64 | 8 | 8 | NOT USED | | |
| 65 | 9 | 1 | 2 XTRA BALLS LT OUTLANE | #555 Bulb |  |
| 66 | 9 | 2 | ADVANCE GEAR LT RETURN | #555 Bulb |  |
| 67 | 9 | 3 | LITE MYSTERY... RT RETURN | #555 Bulb |  |
| 68 | 9 | 4 | 2 XTRA BALLS RT OUTLANE | #555 Bulb |  |
| 69 | 9 | 5 | M-CYCLE HEADLIGHT | #555 Bulb |  |
| 70 | 9 | 6 | RIDE AGAIN X2 | #555 Bulb |  |
| 71 | 9 | 7 | MYSTERY RIDER | #44 Bulb |  |
| 72 | 9 | 8 | NEXT CITY | #44 Bulb |  |
| 73 | 10 | 1 | NOT USED | | |
| 74 | 10 | 2 | NOT USED | | |
| 75 | 10 | 3 | NOT USED | | |
| 76 | 10 | 4 | NOT USED | | |
| 77 | 10 | 5 | NOT USED | | |
| 78 | 10 | 6 | NOT USED | | |
| 79 | 10 | 7 | NOT USED | | |
| 80 | 10 | 8 | NOT USED | | |

The grid prints the heading "Diode On Terminal Strip:" above it. Lamp 47 (AUTO LAUNCH) is the cabinet launch-button lamp:
the Cabinet / Coin Door Wiring Diagram (cabinet-wiring excerpt) wires "LAUNCH (FIRE) BUTTON LAMP" as "Lamp 47 Launch".
