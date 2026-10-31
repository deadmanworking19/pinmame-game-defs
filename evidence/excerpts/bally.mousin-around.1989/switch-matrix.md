# Mousin' Around! — Switch Matrix (printed page "Switches 2-28")

Source: `Bally_1989_Mousin_Around_Manual.pdf` (120 pages, image-only scans, SHA-256
`6dcd83d1485a1b2e9909cc65b07d9ce23e1e7757e87cdf4a002984465b02d9f0`), PDF page 82, footer `Switches 2-28`.
Read from the page rendered at 300 dpi and viewed whole and in strips; the scan carries no text layer, and
a Windows OCR pass was used only to find the page. The page prints the title `MOUSIN' AROUND SWITCH MATRIX`,
a wiring drawing with a `Typical Switch Circuit` inset, and the switch-matrix table below it. Every cell
is transcribed. Each table cell prints the switch name above or beside its number, which sits at the
lower right of the cell; nothing on the page is shaded, and the page prints no legend and no footnote.

## Wiring drawing (top of page)

Two boxed connector blocks. The drawing's wire labels set "rn" so tightly that it reads like "m" (`Gm/Gry`,
`Wht/Bm`); they are written here as the colour abbreviations the table spells out.

Connector `1P8` (column lines), from top to bottom:

| 1P8 pin | Wire | Label |
| --- | --- | --- |
| 9 | Grn/Gry | Column 8 |
| 8 | Grn/Vio | Column 7 |
| 7 | Grn/Blu | Column 6 |
| 5 | Grn/Blk | Column 5 |
| 4 | Grn/Yel | Column 4 |
| 3 | Grn/Orn | Column 3 |
| 2 | Grn/Red | Column 2 |
| 1 | Grn/Brn | Column 1 |

Connector `1P10` (row lines), from top to bottom:

| 1P10 pin | Wire | Label |
| --- | --- | --- |
| 9 | Wht/Brn | Row 1 |
| 8 | Wht/Red | Row 2 |
| 7 | Wht/Orn | Row 3 |
| 6 | Wht/Yel | Row 4 |
| 5 | Wht/Grn | Row 5 |
| 3 | Wht/Blu | Row 6 |
| 2 | Wht/Vio | Row 7 |
| 1 | Wht/Gry | Row 8 |

The grid numbers each crossing `01`-`64`, column by column (`01`-`08` on column 1, `09`-`16` on column 2, ...
`57`-`64` on column 8). The `Typical Switch Circuit` inset draws a switch and a diode in series between a
`Column` line and a `Row` line.

## Switch-matrix table

Column headings, as printed (column number, driver transistor, wire, connector):

| Column | Transistor | Wire | Connector |
| --- | --- | --- | --- |
| 1 | Q45 | GRN-BRN | 1J8-1 |
| 2 | Q49 | GRN-RED | 1J8-2 |
| 3 | Q44 | GRN-ORN | 1J8-3 |
| 4 | Q48 | GRN-YEL | 1J8-4 |
| 5 | Q43 | GRN-BLK | 1J8-5 |
| 6 | Q47 | GRN-BLU | 1J8-7 |
| 7 | Q42 | GRN-VIO | 1J8-8 |
| 8 | Q46 | GRN-GRY | 1J8-9 |

Row headings, as printed (row number, wire, connector):

| Row | Wire | Connector |
| --- | --- | --- |
| 1 | WHT-BRN | 1J10-9 |
| 2 | WHT-RED | 1J10-8 |
| 3 | WHT-ORN | 1J10-7 |
| 4 | WHT-YEL | 1J10-6 |
| 5 | WHT-GRN | 1J10-5 |
| 6 | WHT-BLU | 1J10-3 |
| 7 | WHT-VIO | 1J10-2 |
| 8 | WHT-GRY | 1J10-1 |

Cells, in switch-number order (`name` as printed, line breaks joined by a space):

| Switch | Column | Row | Printed name |
| ---: | ---: | ---: | --- |
| 1 | 1 | 1 | Plumb Bob Tilt |
| 2 | 1 | 2 | Not Used |
| 3 | 1 | 3 | Credit Button |
| 4 | 1 | 4 | Right Coin Chute |
| 5 | 1 | 5 | Center Coin Chute |
| 6 | 1 | 6 | Left Coin Chute |
| 7 | 1 | 7 | Slam Tilt |
| 8 | 1 | 8 | High Score Rset |
| 9 | 2 | 1 | Outhole |
| 10 | 2 | 2 | Not Used |
| 11 | 2 | 3 | Trough 1 Right |
| 12 | 2 | 4 | Trough 2 Middle |
| 13 | 2 | 5 | Trough 3 Left |
| 14 | 2 | 6 | Shooter Lane |
| 15 | 2 | 7 | Right Return Loop |
| 16 | 2 | 8 | Left Return Loop |
| 17 | 3 | 1 | M |
| 18 | 3 | 2 | O |
| 19 | 3 | 3 | U |
| 20 | 3 | 4 | S |
| 21 | 3 | 5 | E |
| 22 | 3 | 6 | Top Lanes Left |
| 23 | 3 | 7 | Top Lanes Middle |
| 24 | 3 | 8 | Top Lanes Right |
| 25 | 4 | 1 | T |
| 26 | 4 | 2 | R |
| 27 | 4 | 3 | A |
| 28 | 4 | 4 | P |
| 29 | 4 | 5 | Left Center Target |
| 30 | 4 | 6 | Middle Center Target |
| 31 | 4 | 7 | Right Center Target |
| 32 | 4 | 8 | Mouse Hole Enter |
| 33 | 5 | 1 | Trap 1 Up/Down |
| 34 | 5 | 2 | Trap 2 Up/Down |
| 35 | 5 | 3 | Center Ramp |
| 36 | 5 | 4 | Playfield Multiply |
| 37 | 5 | 5 | Left Ramp Exit |
| 38 | 5 | 6 | Left Return Lane |
| 39 | 5 | 7 | Right Return Lane |
| 40 | 5 | 8 | Right Outlane |
| 41 | 6 | 1 | Trap 1 Ball |
| 42 | 6 | 2 | Trap 2 Ball |
| 43 | 6 | 3 | Motor Bank Up |
| 44 | 6 | 4 | Right Ramp Enter |
| 45 | 6 | 5 | Not Used |
| 46 | 6 | 6 | Right Ramp Exit |
| 47 | 6 | 7 | Left Ramp Enter |
| 48 | 6 | 8 | Not Used |
| 49 | 7 | 1 | Ball Diverter |
| 50 | 7 | 2 | Motor Bank Down |
| 51 | 7 | 3 | Left Outlane |
| 52 | 7 | 4 | Left Jet |
| 53 | 7 | 5 | Right Jet |
| 54 | 7 | 6 | Bottom Jet |
| 55 | 7 | 7 | Left Sling |
| 56 | 7 | 8 | Right Sling |
| 57 | 8 | 1 | Right Flipper |
| 58 | 8 | 2 | Left Flipper |
| 59 | 8 | 3 | Mouse Hole Lock 1 |
| 60 | 8 | 4 | Mouse Hole Lock 2 |
| 61 | 8 | 5 | Mouse Hole Lock 3 |
| 62 | 8 | 6 | Not Used |
| 63 | 8 | 7 | Not Used |
| 64 | 8 | 8 | Not Used |
