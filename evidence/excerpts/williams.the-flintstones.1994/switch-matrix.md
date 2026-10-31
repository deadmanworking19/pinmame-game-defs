# Williams The Flintstones (1994) — Switch matrix, dedicated switches and switch circuit

Source: Williams *The Flintstones* Operations Manual 16-50029-101 (July 1994), IPDB machine 888 file
`Williams_1994_The_Flintstones_English_Manual.pdf`. Read from the native 300 dpi renders; each section
names its page. Text is transcribed as printed; `[?]` marks a reading the scan leaves uncertain.

## Switch Circuit, PDF page 107 (printed page 2-42)

Source: Williams Electronics Games, "The Flintstones" Operations Manual 16-50029-101 (July 1994), Section 2, `Williams_1994_The_Flintstones_English_Manual.pdf`, PDF page 107, printed folio `2-42`. Table title: `Switch Circuit`. The page carries one table drawn as three blocks: the `Dedicated Grounded Switches` column (D1-D8), the 8 x 8 matrix with its column and row headers, and the `Flipper Grounded Switches` column (F1-F8). Each matrix cell prints the switch name in the upper part and the two-digit switch number (column digit first, then row digit) at the bottom right of the cell. The row header cell prints the row number at its bottom left. No shading, no legend and no other text appear on this page.

### Column drive headers

Corner cell: diagonal split, `COLUMN` (upper right) and `ROW` (lower left).

| Column | Wire | Connector pin | IC pin |
| --- | --- | --- | --- |
| 1 | Green-Brown | J207-1 | U20-18 |
| 2 | Green-Red | J207-2 | U20-17 |
| 3 | Green-Orange | J207-3 | U20-16 |
| 4 | Green-Yellow | J207-4 | U20-15 |
| 5 | Green-Black | J207-5 | U20-14 |
| 6 | Green-Blue | J207-6 | U20-13 |
| 7 | Green-Violet | J207-7 | U20-12 |
| 8 | Green-Gray | J207-9 | U20-11 |

(The wire names are printed broken across lines, e.g. `Green-` / `Brown`.)

### Row return headers and dedicated grounded switches

| Row | Row wire | Row connector pin | Row IC pin | Dedicated switch: wire | Connector pin | Label as printed | Item |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | White-Brown | J209-1 | U18-11 | Orange-Brown | J205-1 | Left Coin Chute | D1 |
| 2 | White-Red | J209-2 | U18-9 | Orange-Red | J205-2 | Center Coin Chute | D2 |
| 3 | White-Orange | J209-3 | U18-5 | Orange-Black | J205-3 | Right Coin Chute | D3 |
| 4 | White-Yellow | J209-4 | U18-7 | Orange-Yellow | J205-4 | 4th Coin Chute | D4 |
| 5 | White-Green | J209-4 | U19-11 | Orange-Green | J205-6 [?] | Normal Service Credit / Test Escape (printed as `Normal` `Test` / `Service` `Escape` / `Credit`) | D5 |
| 6 | White-Blue | J209-7 | U19-9 | Orange-Blue | J205-7 | Normal Vol. Dn / Test Down (printed `Normal` `Test` / `Vol. Dn` `Down`) | D6 |
| 7 | White-Violet | J209-8 | U19-5 | Orange-Violet | J205-8 [?] | Normal Vol. Up / Test Up (printed `Normal` `Test` / `Vol. Up` `Up`) | D7 |
| 8 | White-Gray | J209-9 | U19-7 | Orange-Gray | J205-9 | Normal Beg. Test / Test Enter (printed `Normal` `Test` / `Beg.` `Enter` / `Test`) | D8 |

For D5-D8 the small text is printed in two columns: the left column is the `Normal` function, the right column is the `Test` function.

### Matrix grid (switch name, number in brackets)

| Row \ Column | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Launch Button (11) | Slam (21) | Trough #1 (31) | 4-Bnk #1 D.Tgt. (41) | Lt. & Rt. 3-Bnk. Bot. Tgt. (51) | Lt. Sling (61) | Lt. Out Rollover (71) | Not Used (81) |
| 2 | Ticket Disp. (12) | Door Closed (22) | Trough #2 (32) | 4-Bnk #2 D. Tgt. (42) | Lt. & Rt. 3-Bnk Mid. Tgt. (52) | Rt. Sling (62) | Lt. Return Rollover (72) | Not Used (82) |
| 3 | Start Button (13) | Extra Ball Button (23) | Trough #3 (33) | 4-Bnk #3 D. Tgt. (43) | Lt. & Rt. 3-Bnk Up. Tgt. (53) | Top Lt. Jet (63) | Rt. Return Rollover (73) | Not Used (83) |
| 4 | Plumb Tilt (14) | Always Closed (24) | Trough #4 (34) | 4-Bnk #4 D. Tgt. (44) | Low. Lt. Sngl. Tgt. (54) | Top Rt. Jet (64) | Rt. Out Rollover (74) | Not Used (84) |
| 5 | Shooter Lane (15) | "Machine" Exit (25) | Trough Jam (35) | 3-Bnk #1 D. Tgt. (45) | Rt. Sngl. Tgt. (55) | Bottom Jet (65) | Up. Rt. Lane Rollover (75) | Not Used (85) |
| 6 | Upper 3-Bnk Lt. Tgt. "I" (16) | Upper Lt. Sngl. Tgt. (26) | Ball Popper (36) | 3-Bnk #2 D. Tgt. (46) | Dicta-Bird Tgt. (56) | Top Lt. Rollover "D" (66) | Up. Rt. Lane Exit Rollover (76) | Not Used (86) |
| 7 | Upper 3-Bnk Cr. Tgt. "X" (17) | Lt. Lane Rollover (27) | Rt. Ramp Enter (37) | 3-Bnk #3 D. Tgt. (47) | Not Used (57) | Top Cr. Rollover "I" (67) | Rt. Ramp Exit (77) | Not Used (87) |
| 8 | Upper 3-Bnk Rt. Tgt. "I" (18) | In. Lt. Lane Rollover (28) | Lt. Ramp Enter (38) | Cr. Lane Rollover (48) | Not Used (58) | Top Rt. Rollover "G" (68) | Lt. Ramp Exit (78) | Not Used (88) |

Cell layout of multi-line names, as printed: `4-Bnk` / `#1` / `D.Tgt.`; `Lt. & Rt.` / `3-Bnk.` / `Bot. Tgt.`; `Lt. & Rt.` / `3-Bnk` / `Mid. Tgt.`; `Lt. & Rt.` / `3-Bnk` / `Up. Tgt.`; `Low. Lt.` / `Sngl.` / `Tgt.`; `Dicta-` / `Bird` / `Tgt.`; `Upper` / `3-Bnk` / `Lt. Tgt.` / `"I"`; `Upper` / `3-Bnk` / `Cr. Tgt.` / `"X"`; `Upper` / `3-Bnk` / `Rt. Tgt.` / `"I"`; `Up. Rt.` / `Lane Exit` / `Rollover`.
### Flipper grounded switches (right-hand block)

| Item | Wire | Connector pin | Label as printed |
| --- | --- | --- | --- |
| F1 | Black-Green | J906-1 | Lower Right E.O.S. |
| F2 | Blue-Violet | J905-1 | Lower Right Opto |
| F3 | Black-Blue | J906-3 | Lower Left E.O.S |
| F4 | Blue-Gray | J906-2 [?] | Lower Left Opto |
| F5 | Black-Violet | J906-4 | Upper Right E.O.S. |
| F6 | Black-Yellow | J905-3 [?] | Upper Right Opto |
| F7 | Black-Gray | J906-5 | Upper Left E.O.S. |
| F8 | Black-Blue | J905-5 | Upper Left Opto |

The flipper block has only the wire, connector pin and label columns; there is no IC pin column. The block header reads `Flipper Grounded Switches`.

### Notes

- Shading and legend: no cell on this page is shaded and no legend is printed. The opto switches are identified only by the word `Opto` in the flipper block labels (F2, F4, F6, F8); the matrix itself carries no opto marking on this page.
- Matrix cells `Not Used` are printed in 81-88 (whole column 8), 57 and 58.
- Rows 4 and 5 both print `J209-4` as the row connector pin; this is transcribed literally (rows 6, 7, 8 print J209-7, -8, -9). Column 8 prints `J207-9` (there is no J207-8 in the headers).
- D5 prints connector pin `J205-6` (no J205-5 appears in the D1-D8 sequence 1, 2, 3, 4, 6, 7, 8, 9).
- Wire colour "Gray" is spelled `Gray` on this page.

### Uncertain readings

- D5 connector pin printed `J205-6` or `J205-8` (last glyph blurred on this page; the same cell on PDF page 116 reads `J205-6`).
- D7 connector pin `J205-8` (last glyph blurred; the same cell on PDF page 116 reads `J205-8`).
- Row 5 row connector `J209-4`: last glyph blurred, identical in appearance to the row 4 `J209-4`; PDF page 116 prints `J209-4` for both rows as well.
- F4 connector `J906-2`: hundreds digit may be 5 or 6 (PDF page 116 prints `J905-2` for this cell).
- F6 connector `J905-3`: hundreds digit may be 5 or 6 (PDF page 116 prints `J905-3`).
- Switch numbers and small text are low-resolution; numbers are consistent with column digit then row digit throughout (76 verified at 3x zoom).

## SWITCH CIRCUIT, PDF page 116 (printed page 3-2)

Source: Williams Electronics Games, "The Flintstones" Operations Manual 16-50029-101 (July 1994), Section 3, `Williams_1994_The_Flintstones_English_Manual.pdf`, PDF page 116, printed folio `3-2`. Table title: `SWITCH CIRCUIT` (the page also carries the `SWITCH MATRIX CIRCUIT` schematic and an explanatory text). The matrix table repeats the one on PDF page 107 (folio 2-42); it is transcribed again here from this page's own image. Each matrix cell prints the switch name and the number at its bottom right; the row header cell prints the row number at its bottom left. No shading and no legend are printed.

### Column drive headers

Corner cell: diagonal split, `COLUMN` (upper right) and `ROW` (lower left).

| Column | Wire | Connector pin | IC pin |
| --- | --- | --- | --- |
| 1 | Green-Brown | J207-1 | U20-18 |
| 2 | Green-Red | J207-2 | U20-17 |
| 3 | Green-Orange | J207-3 | U20-16 |
| 4 | Green-Yellow | J207-4 | U20-15 |
| 5 | Green-Black | J207-5 | U20-14 |
| 6 | Green-Blue | J207-6 | U20-13 |
| 7 | Green-Violet | J207-7 | U20-12 |
| 8 | Green-Gray | J207-9 | U20-11 |

### Row return headers and dedicated grounded switches

| Row | Row wire | Row connector pin | Row IC pin | Dedicated switch: wire | Connector pin | Label as printed | Item |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | White-Brown | J209-1 | U18-11 | Orange-Brown | J205-1 | Left Coin Chute | D1 |
| 2 | White-Red | J209-2 | U18-9 | Orange-Red | J205-2 | Center Coin Chute | D2 |
| 3 | White-Orange | J209-3 | U18-5 | Orange-Black | J205-3 | Right Coin Chute | D3 |
| 4 | White-Yellow | J209-4 | U18-7 | Orange-Yellow | J205-4 | 4th Coin Chute | D4 |
| 5 | White-Green | J209-4 | U19-11 | Orange-Green | J205-6 | Normal Service Credit / Test Escape (printed `Normal` `Test` / `Service` `Escape` / `Credit`) | D5 |
| 6 | White-Blue | J209-7 | U19-9 | Orange-Blue | J205-7 | Normal Vol. On [?] / Test Down (printed `Normal` `Test` / `Vol. On` `Down`) | D6 |
| 7 | White-Violet | J209-8 | U19-5 | Orange-Violet | J205-8 | Normal Vol. Up / Test Up (printed `Normal` `Test` / `Vol. Up` `Up`) | D7 |
| 8 | White-Gray | J209-9 | U19-7 | Orange-Gray | J205-9 | Normal Beg. Test / Test Enter (printed `Normal` `Test` / `Beg.` `Enter` / `Test`) | D8 |

Left column of the small text is the `Normal` function, right column the `Test` function.

### Matrix grid (switch name, number in brackets)

| Row \ Column | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Launch Button (11) | Slam (21) | Trough #1 (31) | 4-Bnk #1 D.Tgt. (41) | Lt. & Rt. 3-Bnk. Bot. Tgt. (51) | Lt. Sling (61) | Lt. Out Rollover (71) | Not Used (81) |
| 2 | Ticket Disp. (12) | Door Closed (22) | Trough #2 (32) | 4-Bnk #2 D. Tgt. (42) | Lt. & Rt. 3-Bnk Mid. Tgt. (52) | Rt. Sling (62) | Lt. Return Rollover (72) | Not Used (82) |
| 3 | Start Button (13) | Extra Ball Button (23) | Trough #3 (33) | 4-Bnk #3 D. Tgt. (43) | Lt. & Rt. 3-Bnk Up. Tgt. (53) | Top Lt. Jet (63) | Rt. Return Rollover (73) | Not Used (83) |
| 4 | Plumb Tilt (14) | Always Closed (24) | Trough #4 (34) | 4-Bnk #4 D. Tgt. (44) | Low. Lt. Sngl. Tgt. (54) | Top Rt. Jet (64) | Rt. Out Rollover (74) | Not Used (84) |
| 5 | Shooter Lane (15) | "Machine" Exit (25) | Trough Jam (35) | 3-Bnk #1 D. Tgt. (45) | Rt. Sngl. Tgt. (55) | Bottom Jet (65) | Up. Rt. Lane Rollover (75) | Not Used (85) |
| 6 | Upper 3-Bnk Lt. Tgt. "I" (16) | Upper Lt. Sngl. Tgt. (26) | Ball Popper (36) | 3-Bnk #2 D. Tgt. (46) | Dicta-Bird Tgt. (56) | Top Lt. Rollover "D" (66) | Up. Rt. Lane Exit Rollover (76) | Not Used (86) |
| 7 | Upper 3-Bnk Cr. Tgt. "X" (17) | Lt. Lane Rollover (27) | Rt. Ramp Enter (37) | 3-Bnk #3 D. Tgt. (47) | Not Used (57) | Top Cr. Rollover "I" (67) | Rt. Ramp Exit (77) | Not Used (87) |
| 8 | Upper 3-Bnk Rt. Tgt. "I" (18) | In. Lt. Lane Rollover (28) | Lt. Ramp Enter (38) | Cr. Lane Rollover (48) | Not Used (58) | Top Rt. Rollover "G" (68) | Lt. Ramp Exit (78) | Not Used (88) |

### Flipper grounded switches (right-hand block)

| Item | Wire | Connector pin | Label as printed |
| --- | --- | --- | --- |
| F1 | Black-Green | J906-1 | Lower Right E.O.S. |
| F2 | Blue-Violet | J905-1 | Lower Right Opto |
| F3 | Black-Blue | J906-3 | Lower Left E.O.S |
| F4 | Blue-Gray | J905-2 | Lower Left Opto |
| F5 | Black-Violet | J906-4 | Upper Right E.O.S. |
| F6 | Black-Yellow | J905-3 | Upper Right Opto |
| F7 | Black-Gray | J906-5 | Upper Left E.O.S. |
| F8 | Black-Blue | J905-5 | Upper Left Opto |

Block header: `Flipper Grounded Switches`. There is no IC pin column in this block.

### SWITCH MATRIX CIRCUIT (schematic and truth tables)

Schematic title: `SWITCH MATRIX CIRCUIT`. Two boxes: `CPU BOARD` (dashed outline) and `PLAYFIELD`.

Column (example) path, on the CPU board: `LS374SC` latch, then `ULN2803` inverter, output point `B`; a `1KΩ` resistor from `+12V` and a `470pf` capacitor to ground join at the node between `B` and connector `J207` (marked `X`); point `A` is on the line at the connector. Wire label to the playfield: `Green-XXX`. On the playfield the column line goes through the switch symbol and a diode (cathode toward the row line) to the row line.

Row (example) path: playfield row line wire label `White-XXX` into connector `J209` (`X`); then diode `1N4148`; node `C` with a `1KΩ` series resistor (printed `1KΩ`), a `1.2KΩ` resistor to `+12V` and a `470pf` capacitor to ground; the comparator `LM339` input `+` at `D` (the `-` input is tied to `+5V` through a `10KΩ` resistor network, supply `+5V`); output `D` to the `74LS240` (`Row (example)`), output `E`.

Truth table, column:

| COLUMN | A | B | |
| --- | --- | --- | --- |
| INACTIVE | H | L | OFF |
| ACTIVE | L | H | ON |

Truth table, row:

| ROW | C | D | E | |
| --- | --- | --- | --- | --- |
| SWITCH OPEN | H | H | L | OFF |
| SWITCH CLOSED | L | L | H | ON |

### Explanatory text (printed below the schematic)

"The microprocessor is constantly strobing the column side of the switch. When point "A" on the column circuit toggles low, the column side is active."

"When a switch closes the row side of the circuit activates. The "+" input to the LM339 drops below +5V, therefore, its output is low. Corresponding row and column switches must be low at the same time for the switch to be considered closed by the microprocessor. When the switch opens, the "+" input to the LM339 is above +5V, its output is high and the row is inactive."

### Notes

- Rows 4 and 5 both print `J209-4` as the row connector pin; transcribed literally. Column 8 prints `J207-9`. D5 prints `J205-6`.
- No shading and no legend appear on this page; opto switches are marked only by the word `Opto` in the flipper block.
- Differences from PDF page 107, same table: this page reads F4 as `J905-2` and F6 as `J905-3`, and D6 text as `Vol. On` (page 107 reads `Vol. Dn`).

### Uncertain readings

- D6 normal function printed `Vol. On` on this page versus `Vol. Dn` on PDF 107; low-resolution small print, probably `Vol. Dn`.
- Row 5 `J209-4`: last glyph is blurred; identical in form to row 4.
- Truth-table letters (H and L) and the schematic component labels were read at 1.3-1.5x and are small; the `-`/`+` input assignment of the `LM339` follows the printed `-` and `+` marks (the `-` input reaches the `+5V` network, the `+` input reaches D).

## DEDICATED SWITCHES, PDF page 117 (printed page 3-3)

Source: Williams Electronics Games, "The Flintstones" Operations Manual 16-50029-101 (July 1994), Section 3, `Williams_1994_The_Flintstones_English_Manual.pdf`, PDF page 117, printed folio `3-3`. Table title: `DEDICATED SWITCHES` (wiring drawing from the `CPU BOARD` connector `J205` through the `COIN DOOR INTERFACE BOARD` connectors `J1` and `J3` to the switches), followed by the legend lists and the `DEDICATED SWITCH CIRCUIT` schematic and explanatory text. No shading is used.

### Wiring table (CPU BOARD J205, wire, IC pin and item, COIN DOOR INTERFACE BOARD J1 and J3)

| J205 pin | Wire | IC pin | Item | J1 pin | J3 pin | Switch symbol drawn |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Orange-Brown | (U17-5) | D1 | 14 | 4 | yes |
| 2 | Orange-Red | (U17-7) | D2 | 13 | 5 | yes |
| 3 | Orange-Black | (U17-11) | D3 | 12 | 6 | yes |
| 4 | Orange-Yellow | (U17-9) | D4 | 17 | (blank) | no |
| 6 | Orange-Green | (U16-9) | D5 | 11 | 7 | yes |
| 7 | Orange-Blue | (U16-11) | D6 | 10 | 8 | yes |
| 8 | Orange-Violet | (U16-7) | D7 | 9 | 9 | yes |
| 9 | Orange-Gray | (U16-5) | D8 | 8 | 11 | yes |
| 11 | Black | (blank) | (blank) | 15 | 3 | common return line to all switches |

Notes on this table: there is no J205 pin 5 row (the pins run 1, 2, 3, 4, 6, 7, 8, 9, 11). The Black wire at J205-11 is also tied to a ground symbol at the CPU board. For D4 the line reaches J1-17 and ends at the J3 box without a pin number or a switch symbol; for D3 the line runs from J1-12 toward J3-6 with a short gap in the drawn line before J3. The right-hand side of each switch symbol is tied to a common vertical line that returns to J3-3 (Black).

### Legend lists (printed under the wiring drawing)

Coin Acceptor Switches:

| Item | Description as printed |
| --- | --- |
| D1 | Left Coin Chute |
| D2 | Center Coin Chute |
| D3 | Right Coin Chute |
| D4 | Forth Coin Chute |

Control Switches:

| Item | Description as printed |
| --- | --- |
| D5 | Normal Function, Service Credits; Test Function, Escape |
| D6 | Normal Function, Volume Down; Test Function, Down |
| D7 | Normal Function, Volume Up; Test Function, Up |
| D8 | Normal Function, Begin Test; Test Function, Enter |

### DEDICATED SWITCH CIRCUIT

Truth table printed at the top right of the schematic:

| SWITCH | A | B | C | |
| --- | --- | --- | --- | --- |
| OPEN | H | H | L | OFF |
| CLOSED | L | L | H | ON |

Schematic labels, as printed: box `CPU BOARD` with `+5V`, `10KΩ`, `LM339`, `+12V`, `1.2KΩ`, `1KΩ`, points `A`, `B`, `C`, `470pf`, `1N4148`, `74LS240`, `Dedicated Input`, connector `J205` (pin `X` and pin `11`); wire labels `Orange-XXX` and `Black`; box `COIN DOOR INTERFACE BOARD` with connectors `J1` (pins `X` and `15`) and `J3` (pins `X` and `3`); the switch is labelled `Coin Acceptor or Control Switch`.

### Explanatory text (printed below the schematic)

"The dedicated switches operate similar to switches in the matrix, except that instead of a column circuit there is a direct tie to ground. Therefore, the column side is constantly active (low)."

"When a switch closes, the row side (dedicated input) of the circuit activates. The "+" input to the LM339 drops below +5V, therefore the output is low. Since the row circuit (dedicated input) is tied directly to ground through the switch, the switch is considered closed by the microprocessor. When the switch opens, the "+" input to the LM339 is above +5V, its output is high and the row is inactive."

### Notes

- The legend spells `Forth Coin Chute` for D4 as printed.
- Wire names are printed as `Orange-Brown`, `Orange-Red`, `Orange-Black`, `Orange-Yellow`, `Orange-Green`, `Orange-Blue`, `Orange-Violet`, `Orange-Gray`, `Black`.
- The wiring drawing prints the IC pins in parentheses beside each wire name, e.g. `(U17-5)`, followed by the item letter-number.

### Uncertain readings

- None for the wiring table digits; all pin numbers were read at about 1x on clean print. The D3 and D4 drawing details (gap in line, absent J3 pin and switch for D4) are transcribed as seen.
