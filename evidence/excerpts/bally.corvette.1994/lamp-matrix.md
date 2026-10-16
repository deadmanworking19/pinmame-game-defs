# Corvette — Lamp Matrix (wiring)

Transcribed from `Bally_1994_Corvette_Manual.pdf`, PDF page 106, printed page `2-44`: the `LAMP MATRIX` table (title
line, column headers, row headers, the 64 cells and the footnote). The lower part of the same PDF page is the first
`LAMP LOCATIONS` parts list (items 11-48), transcribed in `lamp-locations.md`. The Section 3 reprint on PDF page 118
(printed `3-4`) and a third printing on the unnumbered back foldout, PDF page 155, were compared cell by cell (see
"Comparison of the three printings"). Read from the rendered pages (300 dpi scans), not from the OCR text.

The title line prints `LAMP MATRIX`, then at the right the labels `Yellow (B+)`, a lamp (bulb) symbol drawn as a loop in
the line, and `Red`. A diode symbol (arrowhead and bar) is printed in the line between the lamp and `Red`.

## Matrix drive columns

| Column | Wire (as printed) | Connector-pin | Drive transistor |
| --- | --- | --- | --- |
| 1 | Yellow-Brown | J137-1 | Q98 |
| 2 | Yellow-Red | J137-2 | Q97 |
| 3 | Yellow-Orange | J137-3 | Q96 |
| 4 | Yellow-Black | J137-4 | Q95 |
| 5 | Yellow-Green | J137-5 | Q94 |
| 6 | Yellow-Blue | J137-6 | Q93 |
| 7 | Yellow-Violet | J138-7 | Q92 |
| 8 | Yellow-Gray | J138-9 | Q91 |

The top-left corner cell is divided diagonally and prints `Column` (upper right) and `Row` (lower left). Each column
header prints the column number (bold), the wire name on two lines (`Yellow-` over `Brown`, bold), the connector-pin
and the transistor on separate lines. The connector prefix changes from `J137` (columns 1-6) to `J138` (columns 7 and
8) as printed; column 8's pin is `J138-9` (there is no `J138-8` column).

## Matrix return rows

| Row | Wire (as printed) | Connector-pin | Return transistor |
| --- | --- | --- | --- |
| 1 | Red-Brown | J133-1 | Q90 |
| 2 | Red-Black | J133-2 | Q89 |
| 3 | Red-Orange | J133-4 | Q88 |
| 4 | Red-Yellow | J133-5 | Q87 |
| 5 | Red-Green | J133-6 | Q86 |
| 6 | Red-Blue | J133-7 | Q85 |
| 7 | Red-Violet | J133-8 | Q84 |
| 8 | Red-Gray | J133-9 | Q83 |

The row header prints the row number at the left, the wire name on two lines (`Red-` over `Brown`, bold) and the
connector-pin and transistor on one line (`J133-1 Q90`). The row pins skip `J133-3` (row 2 is `J133-2`, row 3 is
`J133-4`).

## Matrix cells

Each cell prints its description (multi-line text, joined here by single spaces) and a small two-digit lamp number in
its bottom-right corner, column digit first, row digit second. No cell is shaded, no cell is blank, and no cell prints
a colour or bulb marking; the only legend is the footnote below. Each entry below is `<printed lamp number> <printed
label>`.

| Row | Col 1 | Col 2 | Col 3 | Col 4 |
| --- | --- | --- | --- | --- |
| 1 | 11 Left Rollover | 21 Inner Loop Arrow | 31 Left Outer Loop Arrow | 41 Corvette 6 |
| 2 | 12 Middle Rollover | 22 Fuelie | 32 Lite Lock | 42 Corvette 3 |
| 3 | 13 Right Rollover | 23 Nitrous | 33 Qualify | 43 Corvette 1 |
| 4 | 14 Skid Pad Arrow | 24 Inner Loop Jackpot | 34 Big Block | 44 Corvette 2 |
| 5 | 15 Sticky Tires | 25 Right Outer Loop Arrow | 35 ZR-1 Ramp | 45 Corvette 4 |
| 6 | 16 Skid Pad Jackpot | 26 Z07 Suspension | 36 6 Speed Trans | 46 Left Standup 3 |
| 7 | 17 Route 66 Arrow | 27 Big Brakes | 37 Hi Lift Cams | 47 Left Standup 2 |
| 8 | 18 Race Today | 28 Super Charger | 38 ZR-1 Ramp Arrow | 48 Left Standup 1 |

| Row | Col 5 | Col 6 | Col 7 | Col 8 |
| --- | --- | --- | --- | --- |
| 1 | 51 Corvette 9 | 61 Left Outer Tail | 71 Kickback Arrow | 81 Right Tree Red |
| 2 | 52 Corvette 8 | 2 [sic, printed as a single digit] Left Inner Tail | 72 Left Return Lane | 82 Left Tree Red |
| 3 | 53 Pit Stop | 63 Catch Me | 73 Right Return lane | 83 Tree Bottom Yellow |
| 4 | 54 Corvette 7 | 64 Right Inner Tail | 74 Right Our Lane | 84 Tree Top Yellow |
| 5 | 55 Corvette 5 | 65 Right Outer Tail | 75 Million Standup | 85 Right Tree Green |
| 6 | 56 Pit Stop Arrow | 66 Right Standup Arrow | 76 Side Pipe 1 | 86 Left Tree Green |
| 7 | 57 Spinner Arrow | 67 Lite Kickback | 77 Side Pipe 2 | 87 Buy In |
| 8 | 58 Drive Again | 68 Start Challenge | 78 Side Pipe 3 | 88 Start Button |

Footnote printed below the table, at the lower left: `J1XX = Power Driver Board`.

Notes on the cell text:

- Cell at column 6, row 2 prints the lamp number as a single digit `2` (not `62`) in all three printings; the position
  (column 6, row 2) and the Lamp Locations list (item 62 `Left Inner Tail`) show it is lamp 62. Printed literally here;
  suspected typo.
- Cell 74 prints `Right Our Lane`; the Lamp Locations list item 74 prints `Right Out Lane`. Suspected typo for `Out`.
- Cell 73 prints `Right Return lane` with a lower-case `l` (cell 72 prints `Left Return Lane`; the Lamp Locations item 73 prints
  `Right Return Lane`).
- Cell 35 prints `ZR-1 Ramp`; the Lamp Locations item 35 prints `ZR-1 Ramp Lock`.
- Cell 36 prints the digit `6` on its own line before `Speed Trans` (`6` / `Speed` / `Trans`).
- Cells 25 and 31 print `Right Outer Loop Arrow` and `Left Outer Loop Arrow` where the Lamp Locations list abbreviates
  `R Outer Loop Arrow` (item 25) and `L Outer Loop Arrow` (item 31).
- Cells 41-45 and 51, 52, 54, 55 print `Corvette 6, 3, 1, 2, 4, 9, 8, 7, 5` (the number on a second line, as printed).
- On the PDF 106 scan only, a horizontal rule stub extends past the right edge of the table at the row 3 / row 4
  boundary (scan or layout artefact, not part of the table); it is absent from PDF pages 118 and 155.

## Comparison of the three printings

PDF 106 (printed 2-44) against PDF 118 (printed 3-4) and PDF 155 (back foldout), compared cell by cell on 300 dpi
renders: header labels, wire names, connector-pins and transistors of all eight columns and eight rows, all 64
cell labels, all 64 printed lamp numbers, the `Yellow (B+)` / `Red` title-line legend and the `J1XX = Power Driver
Board` footnote.

- Differences in label, wire, pin, transistor or footnote: none.
- All three printings reproduce the same oddities: the single-digit `2` for lamp 62, `Right Our Lane` in cell 74,
  `Right Return lane` in cell 73, and `J138-7` / `J138-9` for columns 7 and 8.
- Layout-only differences: page position and scale, and PDF 118 and 155 print the matrix without the stray rule stub
  noted above. PDF 118 additionally carries a `LAMP MATRIX CIRCUIT` schematic and its description text below the
  matrix (not transcribed here); PDF 155 additionally carries a `SWITCH MATRIX` below the matrix (not transcribed
  here).

## Uncertain readings

None. Every label, pin, transistor and lamp number was read from a legible 1.4x crop of PDF 106, 118 and 155
(`scratch/lamp/p106-a..d.png`, `p118-a..d.png`, `p155-a..d.png`).
