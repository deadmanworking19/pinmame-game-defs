# The Adventures of Rocky and Bullwinkle and Friends (Data East 1993) - Lamp Matrix Chart and Lamp Locations

Transcribed by hand from native-resolution (300 dpi) renders of printed pages 26 and 27 (PDF 30 and 31) of the IPDB-hosted scan `Data_East_1993_Adventures_of_Rocky_and_Bullwinkle_and_Friends_Full_Manual.pdf`. OCR text was used only to locate the pages; every cell below was read from the render.

Printed page 26 says controlled lamps are configured in an 8 x 8 matrix of columns (lamp drives) and rows (lamp returns) with up to 64 lamps possible. The chart is column-major: address = (column - 1) x 8 + row, and that is exactly the number printed in the lower right of each cell.

## Column drives (printed header row)

| Column | Drive transistor | Wire | Connector |
| --- | --- | --- | --- |
| 1 | Q71 | YEL-BRN | CN7-1 |
| 2 | Q70 | YEL- RED | CN7-2 |
| 3 | Q69 | YEL-ORN | CN7-3 |
| 4 | Q68 | YEL-BLK | CN7-4 |
| 5 | Q67 | YEL-GRN | CN7-6 |
| 6 | Q66 | YEL-BLU | CN7-7 |
| 7 | Q65 | YEL-VIO | CN7-8 |
| 8 | Q64 | YEL-GRY | CN7-9 |

Column 2 prints `YEL- RED` with a space after the hyphen; column 4 prints `YEL-BLK`. Both are literal. CN7 pin 5 is not used by any column; the printed header skips from CN7-4 to CN7-6.

## Row returns (printed header column)

| Row | Return transistor | Wire | Connector |
| --- | --- | --- | --- |
| 1 | Q72 | RED-BRN | CN6-1 |
| 2 | Q73 | RED-BLK | CN6-2 |
| 3 | Q74 | RED-ORN | CN6-3 |
| 4 | Q75 | RED-YEL | CN6-5 |
| 5 | Q76 | RED-GRN | CN6-6 |
| 6 | Q77 | RED-BLU | CN6-7 |
| 7 | Q78 | RED-VIO | CN6-8 |
| 8 | Q79 | RED-GRY | CN6-9 |

Row 2 prints `RED-BLK`; it is literal. CN6 pin 4 is not used by any row; the printed header skips from CN6-3 to CN6-5.

## Lamp Matrix Chart

| Addr | Column | Row | Printed cell |
| --- | --- | --- | --- |
| 1 | 1 | 1 | Top Blue |
| 2 | 1 | 2 | Middle Blue |
| 3 | 1 | 3 | Bottom Blue |
| 4 | 1 | 4 | Top Yellow |
| 5 | 1 | 5 | Middle Yellow |
| 6 | 1 | 6 | Bottom Yellow |
| 7 | 1 | 7 | Bottom Red |
| 8 | 1 | 8 | Middle Red |
| 9 | 2 | 1 | Top Red |
| 10 | 2 | 2 | Bottom Green |
| 11 | 2 | 3 | Middle Green |
| 12 | 2 | 4 | Top Green |
| 13 | 2 | 5 | Pie TRI-BALL |
| 14 | 2 | 6 | Spin & Win |
| 15 | 2 | 7 | Credit Button |
| 16 | 2 | 8 | Left Ramp Entr. |
| 17 | 3 | 1 | Drop Target 1 |
| 18 | 3 | 2 | Drop Target 2 |
| 19 | 3 | 3 | Drop Target 3 |
| 20 | 3 | 4 | Drop Target 4 |
| 21 | 3 | 5 | Drop Target 5 |
| 22 | 3 | 6 | Left Return Lane |
| 23 | 3 | 7 | Right Return Lane |
| 24 | 3 | 8 | Right Outlane |
| 25 | 4 | 1 | B Light |
| 26 | 4 | 2 | O Light |
| 27 | 4 | 3 | M Light |
| 28 | 4 | 4 | B Light |
| 29 | 4 | 5 | Laser Kick 1 Mil |
| 30 | 4 | 6 | Laser Kick 3 Mil |
| 31 | 4 | 7 | Laser Kick 5 Mil. |
| 32 | 4 | 8 | Advance X |
| 33 | 5 | 1 | WABAC ??? |
| 34 | 5 | 2 | Looping |
| 35 | 5 | 3 | Instant TRI-BALL |
| 36 | 5 | 4 | 10 Million |
| 37 | 5 | 5 | Lite Mystery Select |
| 38 | 5 | 6 | Loose Moose |
| 39 | 5 | 7 | Bomb Millions |
| 40 | 5 | 8 | Super Pops |
| 41 | 6 | 1 | Daisy S |
| 42 | 6 | 2 | Daisy E |
| 43 | 6 | 3 | Daisy L |
| 44 | 6 | 4 | Daisy E |
| 45 | 6 | 5 | Daisy C |
| 46 | 6 | 6 | Daisy T |
| 47 | 6 | 7 | Extra Ball |
| 48 | 6 | 8 | Launch Button |
| 49 | 7 | 1 | Left Top Lane |
| 50 | 7 | 2 | Center Top Lane |
| 51 | 7 | 3 | Right Top Lane |
| 52 | 7 | 4 | TRI-BALL |
| 53 | 7 | 5 | Right Ramp Entr. |
| 54 | 7 | 6 | Jackpot |
| 55 | 7 | 7 | Lite WABAC |
| 56 | 7 | 8 | Mystery Select |
| 57 | 8 | 1 | Top Hat Target |
| 58 | 8 | 2 | Middle Hat Target |
| 59 | 8 | 3 | Bottom Hat Target |
| 60 | 8 | 4 | Hat Trick |
| 61 | 8 | 5 | Rhino Bonus |
| 62 | 8 | 6 | Lite Laser Kick |
| 63 | 8 | 7 | Special |
| 64 | 8 | 8 | Shoot Again |

Normalization: line breaks inside a cell are joined with a single space. Cell 16 prints `Entr` followed by a faint mark that is read as a full stop. Cell 31 prints `5 Mil.` with a full stop while 29 and 30 print `Mil` without one. Cell 14 prints `Spin` / `&` / `Win` on three lines.

## Lamp Matrix No. and Description (printed page 27)

Printed page 27 lists every lamp number with a description in two panels (01-11 above the location drawing, 12-64 in the right panel) and prints a playfield outline titled `Lamp Locations`. In rows 25-28 the print sets the letter of `BOMB` that the lamp stands for in bold (B, O, M, B), and in rows 41-46 the letter of `SELECT` (S, E, L, E, C, T); the transcription marks the bold letter in brackets.

| No. | Description |
| --- | --- |
| 01 | Top Blue |
| 02 | Middle Blue |
| 03 | Bottom Blue |
| 04 | Top Yellow |
| 05 | Middle Yellow |
| 06 | Bottom Yellow |
| 07 | Bottom Red |
| 08 | Middle Red |
| 09 | Top Red |
| 10 | Bottom Green |
| 11 | Middle Green |
| 12 | Top Green |
| 13 | Pie TRI-BALL |
| 14 | Spin & Win |
| 15 | Credit Button |
| 16 | Left Ramp Entrance |
| 17 | Drop Target 1 |
| 18 | Drop Target 2 |
| 19 | Drop Target 3 |
| 20 | Drop Target 4 |
| 21 | Drop Target 5 |
| 22 | Left Return Lane |
| 23 | Right Return Lane |
| 24 | Right Outlane |
| 25 | BOMB Light [B] |
| 26 | BOMB Light [O] |
| 27 | BOMB Light [M] |
| 28 | BOMB Light [B] |
| 29 | Laser Kick 1 Mil |
| 30 | Laser Kick 3 Mil |
| 31 | Laser Kick 5 Mil |
| 32 | Advance X |
| 33 | WABAC ??? |
| 34 | Looping |
| 35 | Instant TRI-BALL |
| 36 | 10 Million |
| 37 | Lite Mystery Select |
| 38 | Loose Moose |
| 39 | Bomb Millions |
| 40 | Super Pops |
| 41 | Daisy SELECT [S] |
| 42 | Daisy SELECT [E] |
| 43 | Daisy SELECT [L] |
| 44 | Daisy SELECT [E] |
| 45 | Daisy SELECT [C] |
| 46 | Daisy SELECT [T] |
| 47 | Extra Ball |
| 48 | Launch Button |
| 49 | Left Top Lane |
| 50 | Center Top Lane |
| 51 | Right Top Lane |
| 52 | TRI-BALL |
| 53 | Right Ramp Entrance |
| 54 | Jackpot |
| 55 | Lite WABAC |
| 56 | Mystery Select |
| 57 | Top Hat Target |
| 58 | Middle Hat Target |
| 59 | Bottom Hat Target |
| 60 | Hat Trick |
| 61 | Rhino Bonus |
| 62 | Lite Laser Kick |
| 63 | Special |
| 64 | Shoot Again |

## Lamp Locations drawing (printed page 27)

The drawing places a numbered callout for each playfield lamp. Read as printed: `16` appears twice, once at the left ramp entrance (beside `60`) and once at the upper right between the right ramp and the right orbit (above `54`); `1`-`14` sit on the round pie insert at the top right, `13` at its centre; `15` (Credit Button) and `48` (Launch Button) have no callout. The callouts around `54`, `52`, `28` and `61` at the right ramp entrance overlap and are not read individually. The drawing is not used for any placement.
