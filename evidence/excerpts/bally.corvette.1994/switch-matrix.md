# Corvette — Switch Matrix (wiring)

Transcribed from `Bally_1994_Corvette_Manual.pdf`, PDF page 108, printed page `2-46` (top part of the page): the
`SWITCH MATRIX` table with its `Dedicated Grounded Switches` column (D1-D8), its `Flipper Grounded Switches`
column (F1-F8), the 8 x 8 matrix cells, the legend and the switch drawing in the title line. The bottom part of
the same page is the `SWITCH LOCATIONS` list (`switch-locations.md`). The Section 3 reprint of the same table
(PDF page 116, printed page `3-2`) was compared cell by cell and is reported below, together with its
`SWITCH MATRIX CIRCUIT` drawing and text. The `DEDICATED SWITCHES` wiring drawing (PDF page 117, printed page
`3-3`) is transcribed below. Read from the rendered 300 dpi pages, not from the OCR text.

The title line prints `SWITCH MATRIX`, then at the right a switch drawing with the label `White` (left), a line
with a bar and an open switch contact (a knife-style contact with two open circles), and the label `Green`
(right).

## Matrix drive columns

Printed in the header row of the grid: column number (bold), then wire name over two lines (`Green-` over the
colour, bold), then the connector pin, then the IC pin.

| Column | Wire | Connector-pin | Drive IC pin |
| --- | --- | --- | --- |
| 1 | Green-Brown | J207-1 | U20-18 |
| 2 | Green-Red | J207-2 | U20-17 |
| 3 | Green-Orange | J207-3 | U20-16 |
| 4 | Green-Yellow | J207-4 | U20-15 |
| 5 | Green-Black | J207-5 | U20-14 |
| 6 | Green-Blue | J207-6 | U20-13 |
| 7 | Green-Violet | J207-7 | U20-12 |
| 8 | Green-Gray | J207-9 | U20-11 |

The top-left corner cell of the grid is divided diagonally and prints `Column` (upper right) and `Row` (lower
left). Column 8 prints `J207-9` (no `J207-8` is printed).

## Matrix return rows

Printed in the left header column of the grid: row number (bold), then wire name over two lines (`White-` over
the colour, bold), then the connector pin, then the IC pin.

| Row | Wire | Connector-pin | Return IC pin |
| --- | --- | --- | --- |
| 1 | White-Brown | J209-1 | U18-11 |
| 2 | White-Red | J209-2 | U18-9 |
| 3 | White-Orange | J209-3 | U18-5 |
| 4 | White-Yellow | J209-4 | U18-7 |
| 5 | White-Green | J209-5 | U19-11 |
| 6 | White-Blue | J209-7 | U19-9 |
| 7 | White-Violet | J209-8 | U19-5 |
| 8 | White-Gray | J209-9 | U19-7 |

Row 6 prints `J209-7` and row 7 prints `J209-8`; the pin `J209-6` is not printed on any row (row 5 is `J209-5`,
row 6 is `J209-7`).

## Dedicated grounded switches (left column)

Header cell prints `Dedicated` / `Grounded` / `Switches`. Each cell prints, top to bottom: wire (bold) with the
number in parentheses at the right, the connector pin (bold), then the label (bold), and the id (D1-D8) at the
bottom right. **No IC pin is printed in these cells on `2-46`** (nor on the `3-2` reprint); the IC pins in the
table below are the ones printed on the `3-3` dedicated-switch drawing, in parentheses after the wire name.

| Switch | Printed number | Wire | Connector-pin (2-46) | IC pin (3-3 drawing only) | Printed label |
| --- | --- | --- | --- | --- | --- |
| D1 | (1) | Orange-Brown | J205-1 | U17-5 | Left Coin Chute |
| D2 | (2) | Orange-Red | J205-2 | U17-7 | Center Coin Chute |
| D3 | (3) | Orange-Black | J205-3 | U17-11 | Right Coin Chute |
| D4 | (4) | Orange-Yellow | J205-4 | U17-9 | 4th Coin Chute |
| D5 | (5) | Orange-Green | J205-6 | U16-9 | Normal Function: Ser Credits; Test Function: Esc |
| D6 | (6) | Orange-Blue | J205-7 | U16-11 | Normal Function: Vol Down; Test Function: Down |
| D7 | (7) | Orange-Violet | J205-8 | U16-7 | Normal Function: Vol Up; Test Function: Up |
| D8 | (8) | Orange-Gray | J205-9 | U16-5 | Normal Function: Begin Test; Test Function: Enter |

Notes:
- D2's label is printed on two lines: `Center` (directly under the connector pin) and `Coin Chute` with `D2` at the
  right. D1, D3 and D4 print the label on one line with the id at its right (`Left Coin Chute   D1`,
  `Right Coin Chute D3`, `4th Coin Chute   D4`).
- For D5-D8 the label area is a two-column sub-table: the left column prints `Normal` / `Function` in small type
  over the function name (bold), the right column `Test` / `Function` in small type over the function name
  (bold), separated by a vertical rule; the id (`D5`-`D8`) is at the bottom right of the right column. Printed as
  `Ser Credits | Esc D5`, `Vol Down | Down D6`, `Vol Up | Up D7`, `Begin Test | Enter D8`.
- `J205-5` is not printed on any dedicated cell (D4 is `J205-4`, D5 is `J205-6`).
- None of the D cells is shaded.

## Flipper grounded switches (right column)

Header cell prints `Flipper` / `Grounded` / `Switches`. Each cell prints, top to bottom: wire (bold), connector pin,
then the label over two lines (bold), with the id (`F1`-`F8`) at the right of the second label line.

| Switch | Wire | Connector-pin | Printed label | Shaded (Opto, Typically Closed) |
| --- | --- | --- | --- | --- |
| F1 | Black-Green | J906-1 | Right Flipper EOS | no |
| F2 | Black-Violet | J905-1 | Right Flipper Opto | yes |
| F3 | Black-Blue | J906-3 | Left Flipper EOS | no |
| F4 | Black-Gray | J905-2 | Left Flipper Opto | yes |
| F5 | Black-Violet | J906-4 | Upper Right Flipper EOS | no |
| F6 | Black-Yellow | J905-3 | Upper Right Flipper Opto | yes |
| F7 | Black-Gray | J906-5 | Upper Left Flipper EOS | no |
| F8 | Black-Blue | J905-5 | Upper Left Flipper Opto | yes |

Notes:
- The connector prefix differs between the unshaded cells (`J906-`) and the shaded cells (`J905-`). The legend
  prints `J9XX = Fliptronic II Board`. The `J905` digit of the four shaded cells is read through the halftone
  shading and is the least certain print in this table (see "Uncertain readings").
- In the label of F5 (`Upper Right` / `Flipper EOS   F5`) and F7 (`Upper Left` / `Flipper EOS   F7`) the id is
  printed after `EOS` on the same line; F6 and F8 print `Flipper Opto   F6` / `Flipper Opto   F8`.
- The matrix labels call F2/F4/F6/F8 `... Flipper Opto`, F5/F6 `Upper Right ...`; the SWITCH LOCATIONS list
  (`switch-locations.md`) prints different words for the same ids (F2 `*Lower Right Flipper Cabinet`, F5 and F6
  `Not Used`, F8 `*Upper Left Flipper Cabinet`). Both are kept as printed; nothing is reconciled here.

## Matrix cells

Each cell prints its label over up to three lines (centred) and its two-digit number (column digit, then row
digit) at the bottom right. Shaded cells carry the halftone shading that the legend defines as
`= Opto, Typically Closed`. No cell prints anything other than the label and the number. Cells are listed in
number order (column by column, rows 1-8). 64 cells; every cell prints a label (no blank cells).

| Cell | Printed label (lines joined with a space) | Shaded (Opto, Typically Closed) | Anything else printed |
| --- | --- | --- | --- |
| 11 | Left Out Lane | no | - |
| 12 | Right Out Lane | no | - |
| 13 | Start Button | no | - |
| 14 | Plumb Bob Tilt | no | - |
| 15 | Plunger | no | - |
| 16 | Left Return Lane | no | - |
| 17 | Right Return Lane | no | - |
| 18 | Spinner | no | - |
| 21 | Slam Tilt | no | - |
| 22 | Coin Door Closed | no | - |
| 23 | Buy In Button | no | - |
| 24 | Always Closed | no | - |
| 25 | First Gear (optional) | no | - |
| 26 | Second Gear (optional) | no | - |
| 27 | Third Gear (optional) | no | - |
| 28 | Fourth Gear (optional) | no | - |
| 31 | Trough Ball 1 | yes | - |
| 32 | Trough Ball 2 | yes | - |
| 33 | Trough Ball 3 | yes | - |
| 34 | Trough Ball 4 | yes | - |
| 35 | Route 66 Entry | yes | - |
| 36 | Pit Stop Popper | yes | - |
| 37 | Trough Eject | yes | - |
| 38 | Inner Loop Entry | no | - |
| 41 | ZR-1 Bottom Entry | yes | - |
| 42 | ZR-1 Top Entry | yes | - |
| 43 | Skid Pad Entry | yes | - |
| 44 | Skid Pad Exit | no | - |
| 45 | Route 66 Exit | no | - |
| 46 | Left Standup 3 | no | - |
| 47 | Left Standup 2 | no | - |
| 48 | Left Standup 1 | no | - |
| 51 | Left Race Start | yes | - |
| 52 | Right Race Start | yes | - |
| 53 | Not Used | no | - |
| 54 | Not Used | no | - |
| 55 | Left Race Encoder | yes | - |
| 56 | Right Race Encoder | yes | - |
| 57 | Route 66 Kickout | no | - |
| 58 | Skid Route 66 Exit | no | - |
| 61 | Left Slingshot | no | - |
| 62 | Right Slingshot | no | - |
| 63 | Left Jet | no | - |
| 64 | Bottom Jet | no | - |
| 65 | Right Jet | no | - |
| 66 | Left Rollover | no | - |
| 67 | Middle Rollover | no | - |
| 68 | Right Rollover | no | - |
| 71 | ZR-1 Full Left | yes | - |
| 72 | ZR-1 Full Right | yes | - |
| 73 | Not Used | no | - |
| 74 | Not Used | no | - |
| 75 | ZR-1 Exit | no | - |
| 76 | ZR-1 Lock Ball 1 | no | - |
| 77 | ZR-1 Lock Ball 2 | no | - |
| 78 | ZR-1 Lock Ball 3 | no | - |
| 81 | Million Standup | no | - |
| 82 | Skid Pad Standup | no | - |
| 83 | Right Standup | no | - |
| 84 | Right Rubber | no | - |
| 85 | Not Used | no | - |
| 86 | Jet Rubber | no | - |
| 87 | Left Outer Loop | no | - |
| 88 | Right Outer Loop | no | - |

Shaded cells (16 matrix cells): 31, 32, 33, 34, 35, 36, 37 (column 3, rows 1-7), 41, 42, 43 (column 4, rows 1-3),
51, 52, 55, 56 (column 5) and 71, 72 (column 7). Plus the four shaded flipper cells F2, F4, F6, F8. Cell 38 is
not shaded although its column-3 neighbours above it are. Cells printed `Not Used`: 53, 54, 73, 74, 85. Cells
printed `(optional)`: 25, 26, 27, 28.

Printed-text note: the matrix prints `Million Standup` for 81; the SWITCH LOCATIONS list prints `Standup Million`
for the same item.

## Legend and footnote (below the grid)

Printed on one line, literally:

`J2XX = CPU Board;  J9XX = Fliptronic II Board;` then a sample of the halftone shading box, then
`= Opto, Typically Closed`

## Comparison with the 3-2 reprint (PDF page 116)

The reprint prints the same table (same title line, same switch drawing, same legend line) shifted about 90 px
to the right on the page; it is followed by the `SWITCH MATRIX CIRCUIT` section (below). Compared cell by cell
against `2-46`:

- Column headers (number, wire, connector-pin, IC pin): no differences.
- Row headers (number, wire, connector-pin, IC pin): no differences.
- D1-D8 cells (wire, connector pin, label text, `(n)` numbers, Normal/Test Function text): no differences.
- F1-F8 cells (wire, connector pin incl. the `J905-`/`J906-` split, label, shading): no differences.
- All 64 matrix cells (label, number, shading): no differences.
- Legend line: identical.

There are no differences in label, wire, pin or shading. The only visible difference is page placement.

### Section 3 text on 3-2 only

Heading `SWITCH MATRIX CIRCUIT` (bold, underlined). Drawing: a dashed box `CPU BOARD`. Column example: `LS374SC`
latch into a `ULN-2803` inverter (output node `B`), a `1K` pull-up to `+12V`, a `470pf` capacitor to ground,
node `A`, connector `J207` (pin shown `X`), wire `Green-XXX` to the `Playfield` switch (open contact), diode
(arrow pointing from the switch towards the row side), and the wire returns to the row circuit. Row example:
`74LS240` inverter (input `E`), `10K` from `+5V` to node `D`, `LM339` comparator (`+` input from node D side,
`-` input tied to `+5V`), `1K` to node `C`, `1.2K` from `+12V` to node `C`, `470pf` to ground at `C`, `1N4148`
diode, connector `J209` (pin shown `X`), wire `White-XXX`. Two truth tables are printed:

| Column | A | B | |
| --- | --- | --- | --- |
| Inactive | H | L | Off |
| Active | L | H | On |

| Row | C | D | E | |
| --- | --- | --- | --- | --- |
| Switch Open | H | H | L | Off |
| Switch Closed | L | L | H | On |

Printed text under the drawing, two paragraphs, quoted literally:

> The microprocessor is constantly strobing the column side of the switch.  When point "A" on the column circuit
> toggles low, the column side is active.

> When a switch closes, the row side of the circuit activates.  The "+" input to the LM339 drops below +5V
> causing its output to go low.  Corresponding row and column switches must be low at the same time for the
> switch to be considered closed by the microprocessor.  When the switch opens, the "+" input to the LM339 is
> above +5V, its output is high and the row is inactive.

Page number printed: `3-2`.

## DEDICATED SWITCHES drawing (PDF page 117, printed 3-3)

Heading `DEDICATED SWITCHES` (bold, underlined). Three dashed boxes left to right: `CPU Board` (connector `J205`),
`Coin Door Interface Board` (connectors `J1` and `J3`), then outside the boxes the text `Coin Acceptor or Control
Switches` over a column of open switch contacts. Each wire row prints, from left: J205 pin, wire name,
`(IC pin)`, `Dn`, J1 pin, J3 pin, switch.

| Switch | J205 pin | Wire | (IC pin) | J1 pin | J3 pin | Switch contact drawn |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | 1 | Orange-Brown | (U17-5) | 14 | 4 | yes |
| D2 | 2 | Orange-Red | (U17-7) | 13 | 5 | no (line ends at J3 pin 5, no contact) |
| D3 | 3 | Orange-Black | (U17-11) | 12 | 6 | yes |
| D4 | 4 | Orange-Yellow | (U17-9) | 17 | none printed (line ends at J1 pin 17) | no |
| D5 | 6 | Orange-Green | (U16-9) | 11 | 7 | yes |
| D6 | 7 | Orange-Blue | (U16-11) | 10 | 8 | yes |
| D7 | 8 | Orange-Violet | (U16-7) | 9 | 9 | yes |
| D8 | 9 | Orange-Gray | (U16-5) | 8 | 11 | yes |
| (ground) | 11 | Black | (none) | 15 | 3 | return rail |

- J205 pin 5 is not printed (pins 1, 2, 3, 4, 6, 7, 8, 9, 11 are). J205 pin 11 is tied to a ground symbol inside
  the CPU Board box. The wire `Black` goes J205-11 to J1-15 to J3-3, and J3-3 connects to the vertical rail
  that joins the right ends of the drawn switch contacts (junction dots at the contacts of J3 pins 6, 7, 8, 9, 11;
  the contact at J3 pin 4 is the top end of the rail).
- Drawn switch contacts (6): J3 pins 4, 6, 7, 8, 9, 11. J3 pin 5 (D2) has no contact drawn; D4 has no J3 pin
  printed at all.
- Legend text to the right of the switches, as printed: `Coin Acceptor Switches` (underlined) then
  `D1  Left Coin Chute`, `D2  Center Coin Chute`, `D3  Right Coin Chute`, `D4  Fourth Coin Chute`;
  `Control Switches` (underlined) then `D5  Normal Function: Service Credits / Test Function: Escape`,
  `D6  Normal Function: Volume Down / Test Function: Down`, `D7  Normal Function: Volume Up / Test Function: Up`,
  `D8  Normal Function: Begin Test / Test Function: Enter`.
- Note the wording differs from `2-46`: here `Service Credits`, `Escape`, `Volume Down`, `Volume Up`, `Fourth Coin
  Chute`; the matrix prints `Ser Credits`, `Esc`, `Vol Down`, `Vol Up`, `4th Coin Chute`.

Second section, heading `DEDICATED SWITCH CIRCUIT` (bold, underlined). Dashed box `CPU BOARD`: input `C` into a
`74LS240` inverter, `+5V`, `10K` to node `B`, `LM339` comparator (`+` input from node B, `-` input tied to `+5V`),
`1K`, node `A`, `1.2K` from `+12V` to node A, `470pf` to ground, `1N4148` diode, connector `J205` (pin shown `X`),
wire `Orange-XXX` to `Coin Door Interface Board` connectors `J1` (`X`) and `J3` (`X`), then `Coin Acceptor or
Control Switches` contact. Label under the CPU board: `Dedicated Input`. A second wire `Black` from `J205` pin `11`
(tied to ground) to `J1` pin `15` and `J3` pin `3`, returning to the switch. Truth table:

| Switch | A | B | C | |
| --- | --- | --- | --- | --- |
| Open | H | H | L | Off |
| Closed | L | L | H | On |

Printed text under the drawing, two paragraphs, quoted literally:

> The dedicated switches operate similar to switches in the matrix except that instead of a column circuit there
> is a direct tie to ground.  Therefore, the column side is constantly active (low).

> When a switch closes the row side (dedicated input) of the circuit activates.  The "+" input to the LM339 drops
> below +5V causing its output to go low.  Since the row circuit (dedicated input) is tied directly to ground
> through the switch, the switch is considered closed by the microprocessor.  When the switch opens, the "+" input
> to the LM339 is about +5V, its output is high and the row is inactive.

Page number printed: `3-3`.

## Uncertain readings

- F2 `J905-1`, F4 `J905-2`, F6 `J905-3`, F8 `J905-5` (shaded cells; connector letters read through halftone, the
  digit after `J90` could be 5 or 6 — it reads 5 on both `2-46` and `3-2`, while the unshaded F cells read `J906`).
  Crops: `Fall.png`, `r1R.png`, `r2R.png`, `r3R.png`, `r4R.png`.
- F4 `Black-Gray` (shaded; final letter read through halftone, could read `Grey`). Crop: `Fall.png`.
- Wire / label text inside the other shaded cells (31-37, 41-43, 51, 52, 55, 56, 71, 72) is legible but degraded by
  the halftone; the readings above were confirmed against both `2-46` and `3-2` and against the SWITCH LOCATIONS
  list. Crops: `b1L.png`, `b1R.png`, `b2L.png`, `b2R.png`, `b3L.png`, `b3R.png`.
