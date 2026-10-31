# The Adventures of Rocky and Bullwinkle and Friends (Data East 1993) - Switch Matrix Chart and Switch Part Numbers

Transcribed by hand from native-resolution (300 dpi) renders of printed pages 24 and 25 (PDF 28 and 29) of the IPDB-hosted scan `Data_East_1993_Adventures_of_Rocky_and_Bullwinkle_and_Friends_Full_Manual.pdf`. The scan has no usable text layer; OCR text was used only to locate the pages, and every cell below was read from the render.

The chart prints a column header per column (column number, drive transistor, wire colour pair, CPU connector pin) and a row header per row (row number, wire colour pair, connector pin). Printed page 24 says switches are configured in an 8 x 8 matrix of columns (switch drives) and rows (switch returns). The chart is column-major: address = (column - 1) x 8 + row, and that is exactly the number printed in the lower right of each cell.

## Column drives (printed header row)

| Column | Drive transistor | Wire | Connector |
| --- | --- | --- | --- |
| 1 | Q55 | GRN-BRN | CN8-1 |
| 2 | Q54 | GRN-RED | CN8-2 |
| 3 | Q53 | GRN-ORN | CN8-3 |
| 4 | Q52 | GRN-YEL | CN8-4 |
| 5 | Q51 | GRN-BLK | CN8-5 |
| 6 | Q50 | GRN-BLU | CN8-7 |
| 7 | Q49 | GRN-VIO | CN8-8 |
| 8 | Q48 | GRN-GRY | CN8-9 |

CN8 pin 6 is not used by any column; the printed header skips from CN8-5 to CN8-7.

## Row returns (printed header column)

| Row | Wire | Connector |
| --- | --- | --- |
| 1 | WHT-BRN | CN10-9 |
| 2 | WHT-RED | CN10-8 |
| 3 | WHT-ORN | CN10-7 |
| 4 | WHT-YEL | CN10-6 |
| 5 | WHT-GRN | CN10-5 |
| 6 | WHT-BLU | CN10-3 |
| 7 | WHT-VIO | CN10-2 |
| 8 | WHT-GRY | CN10-1 |

CN10 pin 4 is not used by any row; the printed header skips from CN10-5 to CN10-3. The chart carries no shaded (opto) cell and no legend marking any cell as an opto or as normally closed.

## Switch Matrix Chart

| Addr | Column | Row | Printed cell |
| --- | --- | --- | --- |
| 1 | 1 | 1 | Plumb Tilt |
| 2 | 1 | 2 | 4th Coin |
| 3 | 1 | 3 | Credit Button |
| 4 | 1 | 4 | Right Coin |
| 5 | 1 | 5 | Center Coin |
| 6 | 1 | 6 | Left Coin |
| 7 | 1 | 7 | Slam Tilt |
| 8 | 1 | 8 | Not Used |
| 9 | 2 | 1 | Launch Button |
| 10 | 2 | 2 | Outhole |
| 11 | 2 | 3 | Trough #1 Left |
| 12 | 2 | 4 | Trough #2 Center |
| 13 | 2 | 5 | Trough #3 Right |
| 14 | 2 | 6 | Shooter Lane |
| 15 | 2 | 7 | Left EOS |
| 16 | 2 | 8 | Right EOS |
| 17 | 3 | 1 | #1 DropTar. Top |
| 18 | 3 | 2 | #2 DropTar. |
| 19 | 3 | 3 | #3 DropTar. |
| 20 | 3 | 4 | #4 DropTar. |
| 21 | 3 | 5 | #5 DropTar. Bottom |
| 22 | 3 | 6 | Hat Target Bottom |
| 23 | 3 | 7 | Hat Target Middle |
| 24 | 3 | 8 | Hat Target Top |
| 25 | 4 | 1 | "B" Stand-Up Target |
| 26 | 4 | 2 | "O" Stand-Up Target |
| 27 | 4 | 3 | "M" Stand-Up Target |
| 28 | 4 | 4 | "B" Stand-Up Target |
| 29 | 4 | 5 | Super VUK |
| 30 | 4 | 6 | Left Slingshot |
| 31 | 4 | 7 | Left Return |
| 32 | 4 | 8 | Left Outlane |
| 33 | 5 | 1 | Left Orbit Bottom |
| 34 | 5 | 2 | Left Orbit Top |
| 35 | 5 | 3 | Right Orbit Top |
| 36 | 5 | 4 | Right Orbit Bottom |
| 37 | 5 | 5 | Under Trough |
| 38 | 5 | 6 | Right Slingshot |
| 39 | 5 | 7 | Right Return |
| 40 | 5 | 8 | Right Outlane |
| 41 | 6 | 1 | Left Top Lane |
| 42 | 6 | 2 | Center Top Lane |
| 43 | 6 | 3 | Right Top Lane |
| 44 | 6 | 4 | Left Turbo Bumper |
| 45 | 6 | 5 | Center Turbo Bumper |
| 46 | 6 | 6 | Right Turbo Bumper |
| 47 | 6 | 7 | Left Ramp Entr. |
| 48 | 6 | 8 | Left Ramp Exit |
| 49 | 7 | 1 | Right Ramp Entr. |
| 50 | 7 | 2 | Right Ramp Exit |
| 51 | 7 | 3 | Not Used |
| 52 | 7 | 4 | VUK |
| 53 | 7 | 5 | Not Used |
| 54 | 7 | 6 | Not Used |
| 55 | 7 | 7 | Not Used |
| 56 | 7 | 8 | Not Used |
| 57 | 8 | 1 | Not Used |
| 58 | 8 | 2 | Not Used |
| 59 | 8 | 3 | Not Used |
| 60 | 8 | 4 | Not Used |
| 61 | 8 | 5 | Not Used |
| 62 | 8 | 6 | Not Used |
| 63 | 8 | 7 | Not Used |
| 64 | 8 | 8 | Not Used |

Normalization: the printed cell breaks a name across lines (for example `#1` / `DropTar.` / `Top`) and the transcription joins those lines with a single space. The quotation marks of 25-28 are printed. Address 47 prints `Entr.` with its full stop; 49 prints `Entr.` the same way.

## Switch Part Numbers (complete table)

Printed page 25 heads the page `Rocky & Bullwinkle - Switch Part Numbers` and prints the table in two panels (01-09 above the location drawing, 10-53 in the right panel). The footnote reads `* Indicates Cabinet Switches`. The last row reads `53 Not Used Through 64`; the transcription expands it to one row per address with the printed text repeated and marked `(repeated)`.

| Addr | Description | Part no. |
| --- | --- | --- |
| 01* | Plumb Tilt | See Cabinet |
| 02* | 4th Coin | - |
| 03* | Credit Button | 500-5097-02 |
| 04* | Right Coin | 180-5024-00 |
| 05* | Center Coin | 180-5024-00 |
| 06* | Left Coin | 180-5024-00 |
| 07* | Slam Tilt | 180-5022-00 |
| 08 | Not Used | - |
| 09* | Launch Button | 500-5410-02 |
| 10 | Outhole | 180-5011-00 |
| 11 | Left Trough | 180-5009-00 |
| 12 | Center Trough | 180-5009-00 |
| 13 | Right Trough | 180-5010-00 |
| 14 | Shooter Lane | 180-5100-01 |
| 15* | Left Flip. Cab | 180-5048-01 |
| 16* | Right Flip. Cab. | 180-5048-01 |
| 17 | Drop Target Top | 180-5092-01 |
| 18 | Drop Target Top/Mid | 180-5092-01 |
| 19 | Drop Target Middle | 180-5092-01 |
| 20 | Drop Target Bot/Mid | 180-5092-01 |
| 21 | Drop Target Bottom | 180-5092-01 |
| 22 | Hat Target Bottom | 500-5640-36 |
| 23 | Hat Target Middle | 500-5640-36 |
| 24 | Hat Target Top | 500-5640-36 |
| 25 | Small Target "B" | 500-5607-05 |
| 26 | Small Target "O" | 500-5607-06 |
| 27 | Small Target "M" | 500-5607-02 |
| 28 | Small Target "B" | 500-5607-04 |
| 29 | Super VUK | 180-5064-00 |
| 30 | Left Slingshot | 180-5054-00 |
| 31 | Left Return Lane | 500-5142-00 |
| 32 | Left Outlane | 500-5142-00 |
| 33 | Left Orbit Bottom | 180-5090-00 |
| 34 | Left Orbit Top | 500-5142-00 |
| 35 | Right Orbit Top | 500-5142-00 |
| 36 | Right Orbit Bottom | 500-5142-00 |
| 37 | Under Trough | 500-5633-00 |
| 38 | Right Slingshot | 180-5054-00 |
| 39 | Right Return Lane | 500-5142-00 |
| 40 | Right Outlane | 500-5142-00 |
| 41 | Left Top Lane | 500-5142-00 |
| 42 | Center Top Lane | 500-5142-00 |
| 43 | Right Top Lane | 500-5142-00 |
| 44 | Left Turbo Bumper | 180-5015-00 |
| 45 | Center Turbo Bumper | 180-5015-00 |
| 46 | Right Turbo Bumper | 180-5015-00 |
| 47 | Left Ramp Enter | 500-5382-00 |
| 48 | Left Ramp Exit | 500-5633-00 |
| 49 | Right Ramp Enter | 500-5382-00 |
| 50 | Right Ramp Exit | 500-5633-00 |
| 51 | Not Used | - |
| 52 | VUK | 180-5063-00 |
| 53 | Not Used Through 64 | - |
| 54 | Not Used Through 64 (repeated) | - |
| 55 | Not Used Through 64 (repeated) | - |
| 56 | Not Used Through 64 (repeated) | - |
| 57 | Not Used Through 64 (repeated) | - |
| 58 | Not Used Through 64 (repeated) | - |
| 59 | Not Used Through 64 (repeated) | - |
| 60 | Not Used Through 64 (repeated) | - |
| 61 | Not Used Through 64 (repeated) | - |
| 62 | Not Used Through 64 (repeated) | - |
| 63 | Not Used Through 64 (repeated) | - |
| 64 | Not Used Through 64 (repeated) | - |

Normalization: `-` is the printed dash in the part column. `Left Flip. Cab` (15) prints no closing full stop while `Right Flip. Cab.` (16) does; both are literal. Addresses 15 and 16 carry the cabinet asterisk here although the matrix chart on page 24 names the same two addresses `Left EOS` and `Right EOS`; both printings are kept literally.

## Switch Locations drawing (printed page 25)

The page prints a playfield outline titled `Switch Locations` with a numbered callout for each playfield switch. The callouts are read as printed, not as the chart would have them: the three turbo bumpers carry the numbers `44` (left), `46` (upper right) and `47` (lower; no `45` appears on a bumper), a second `47` sits at the left ramp entrance, and the right ramp exit callout at the top right reads `58` or `50` (the print is filled in). `10` sits under the apron, `11`, `12`, `13` and `14` at the lower right beside the shooter lane, `29` in a box on the left rail, `52` in the upper left, and `17`-`21` beside the right-hand drop-target bank. The three stacked hat-target callouts on the left of the playfield read, top to bottom, `2` followed by a digit hidden under a leader line (read as `24`), then `23`, then `22`, which agrees with the part table's `Hat Target Top` at 24 and `Hat Target Bottom` at 22. The drawing is not used for any placement.
