# South Park — Lamp Matrix Grid

Read from `Sega_1999_South_Park_Manual_English.pdf`, PDF page 4 (left half, lower part), the front-matter drawing printed
`DR. 4` ("LAMP MATRIX GRID"). The page is a scan with no text layer; every cell was read from a 220 dpi render. Lamp
number = (row − 1) × 8 + column. A hyphen inside a printed name is the cell's own line break and is kept. "DOTS" marks a
cell carrying the grid's vertical "Diode On Terminal Strip" tag. A cell printing NOT USED is shaded black and has no
bulb line.

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
| 9 | Q41 | RED-WHT | J12-P10 | NOT USED |
| 10 | Q42 | RED | J12-P11 | NOT USED |

## Lamps

| # | Row | Col | Name as printed | Bulb cell | DOTS |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | CHEF FACE | #555 Bulb |  |
| 2 | 1 | 2 | CHEF #2 | #555 Bulb |  |
| 3 | 1 | 3 | CHEF #3 | #555 Bulb |  |
| 4 | 1 | 4 | CHEF #4 | #555 Bulb |  |
| 5 | 1 | 5 | CHEF ARROW | #555 Bulb |  |
| 6 | 1 | 6 | MYSTERY | #555 Bulb |  |
| 7 | 1 | 7 | SPOOKY VISION | #555 Bulb |  |
| 8 | 1 | 8 | EXTRA BALL | #555 Bulb |  |
| 9 | 2 | 1 | STAN FACE | #555 Bulb |  |
| 10 | 2 | 2 | STAN #2 | #555 Bulb |  |
| 11 | 2 | 3 | STAN #3 | #555 Bulb |  |
| 12 | 2 | 4 | STAN #4 | #555 Bulb |  |
| 13 | 2 | 5 | STAN ARROW | #555 Bulb |  |
| 14 | 2 | 6 | SKILL SHOT | #555 Bulb |  |
| 15 | 2 | 7 | VOLCANO | #555 Bulb |  |
| 16 | 2 | 8 | ANAL PROBE | #555 Bulb |  |
| 17 | 3 | 1 | KENNY FACE | #555 Bulb |  |
| 18 | 3 | 2 | KENNY #2 | #555 Bulb |  |
| 19 | 3 | 3 | KENNY #3 | #555 Bulb |  |
| 20 | 3 | 4 | KENNY #4 | #555 Bulb |  |
| 21 | 3 | 5 | KENNY ARROW | #555 Bulb |  |
| 22 | 3 | 6 | SUPER JACKPOT | #555 Bulb | DOTS |
| 23 | 3 | 7 | MULTIBALL READY | 555# ulb | DOTS |
| 24 | 3 | 8 | SOUTH PARK SIGN | #555 Bulb |  |
| 25 | 4 | 1 | KYLE FACE | #555 Bulb |  |
| 26 | 4 | 2 | KYLE #2 | #555 Bulb |  |
| 27 | 4 | 3 | KYLE #3 | #555 Bulb |  |
| 28 | 4 | 4 | KYLE #4 | #555 Bulb |  |
| 29 | 4 | 5 | KYLE ARROW | #555 Bulb |  |
| 30 | 4 | 6 | KENNY ASSEMBLY | #555 Bulb | DOTS |
| 31 | 4 | 7 | NOT USED |  |  |
| 32 | 4 | 8 | NOT USED |  |  |
| 33 | 5 | 1 | CARTMAN FACE | #555 Bulb |  |
| 34 | 5 | 2 | CARTMAN #2 | #555 Bulb |  |
| 35 | 5 | 3 | CARTMAN #3 | #555 Bulb |  |
| 36 | 5 | 4 | CARTMAN #4 | #555 Bulb |  |
| 37 | 5 | 5 | CARTMAN ARROW | #555 Bulb |  |
| 38 | 5 | 6 | LEFT TUR- BO BUMPER | 555# Bulb | DOTS |
| 39 | 5 | 7 | RIGHT TUR- BO BUMPER | 555# Bulb | DOTS |
| 40 | 5 | 8 | BTTM TUR- BO BUMPER | 555# Bulb | DOTS |
| 41 | 6 | 1 | LEFT 5-BANK BOTTOM | #555 Bulb |  |
| 42 | 6 | 2 | LEFT 5-BANK #2 | #555 Bulb |  |
| 43 | 6 | 3 | LEFT 5-BANK #3 | #555 Bulb |  |
| 44 | 6 | 4 | LEFT 5-BANK #4 | #555 Bulb |  |
| 45 | 6 | 5 | LEFT 5-BANK TOP | #555 Bulb |  |
| 46 | 6 | 6 | TOILET S-U LT | #555 Bulb | DOTS |
| 47 | 6 | 7 | NOT USED |  |  |
| 48 | 6 | 8 | TOILET S-U RT | #555 Bulb | DOTS |
| 49 | 7 | 1 | NOT USED |  |  |
| 50 | 7 | 2 | RT. 3-BANK BOTTOM | #555 Bulb |  |
| 51 | 7 | 3 | RT. 3-BANK MIDDLE | #555 Bulb |  |
| 52 | 7 | 4 | RT. 3-BANK TOP | #555 Bulb |  |
| 53 | 7 | 5 | LEFT OUTLANE | #555 Bulb |  |
| 54 | 7 | 6 | LEFT RE- TURN LANE | #555 Bulb |  |
| 55 | 7 | 7 | RIGHT RE- TURN LANE | #555 Bulb |  |
| 56 | 7 | 8 | RIGHT OUTLANE | #555 Bulb |  |
| 57 | 8 | 1 | MR. HANKEY: BOTTOM | #555 Bulb |  |
| 58 | 8 | 2 | MR. HANKEY: BODY | #555 Bulb |  |
| 59 | 8 | 3 | MR. HANKEY: LT HAND | #555 Bulb |  |
| 60 | 8 | 4 | MR. HANKEY: RT HAND | #555 Bulb |  |
| 61 | 8 | 5 | MR. HANKEY: HEAD | #555 Bulb |  |
| 62 | 8 | 6 | MR. HANKEY: HAT | #555 Bulb |  |
| 63 | 8 | 7 | POP BUMPER TARGET LT | #555 Bulb |  |
| 64 | 8 | 8 | POP BUMPER TARGET RT | #555 Bulb |  |
| 65 | 9 | 1 | NOT USED |  |  |
| 66 | 9 | 2 | NOT USED |  |  |
| 67 | 9 | 3 | NOT USED |  |  |
| 68 | 9 | 4 | NOT USED |  |  |
| 69 | 9 | 5 | NOT USED |  |  |
| 70 | 9 | 6 | NOT USED |  |  |
| 71 | 9 | 7 | NOT USED |  |  |
| 72 | 9 | 8 | NOT USED |  |  |
| 73 | 10 | 1 | NOT USED |  |  |
| 74 | 10 | 2 | NOT USED |  |  |
| 75 | 10 | 3 | NOT USED |  |  |
| 76 | 10 | 4 | NOT USED |  |  |
| 77 | 10 | 5 | NOT USED |  |  |
| 78 | 10 | 6 | NOT USED |  |  |
| 79 | 10 | 7 | NOT USED |  |  |
| 80 | 10 | 8 | NOT USED |  |  |

No lamp in the grid names the Start button; rows 9 and 10 (65-80) are printed NOT USED in every cell.
