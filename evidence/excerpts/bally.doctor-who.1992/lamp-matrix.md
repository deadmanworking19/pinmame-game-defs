# Doctor Who — Lamp Matrix (wiring)

Transcribed from `Bally_1992_Doctor_Who_Manual.pdf`, PDF page 125, printed page `DOCTOR WHO 3-2`, the
`LAMPS` matrix table and its lamp-matrix circuit drawing. Read from the rendered page (300 dpi image-only
scan), not from the OCR text. A foldout reprint of the same table sits at PDF page 150; it is a copy of this
page and is not counted as a second source.

## Matrix drive columns

| Column | Wire | Connector-pin | Drive transistor |
| --- | --- | --- | --- |
| 1 | Yellow-Brown | J137-1 | Q98 |
| 2 | Yellow-Red | J137-2 | Q97 |
| 3 | Yellow-Orange | J137-3 | Q96 |
| 4 | Yellow-Black | J137-4 | Q95 |
| 5 | Yellow-Green | J137-5 | Q94 |
| 6 | Yellow-Blue | J137-6 | Q93 |
| 7 | Yellow-Violet | J137-7 | Q92 |
| 8 | Yellow-Gray | J138-9 | Q91 |

Column 8's connector-pin is printed `J138-9` on this page; every other column prints `J137`. The
Power Driver Board connector list (`power-driver-board-connectors.md`, printed 3-22) prints
`J137-9 Yellow-Gray, Col 8 to playfield lamps` and `J138-9 Yellow-Gray, Col 8 to speaker panel lamps`,
and the Handy Technician's Chart prints `J137-9` for column 8 (`handy-technician-chart.md`).

## Matrix return rows

| Row | Wire | Connector-pin | Return transistor |
| --- | --- | --- | --- |
| 1 | Red-Brown | J133-1 | Q90 |
| 2 | Red-Black | J133-2 | Q89 |
| 3 | Red-Orange | J133-4 | Q88 |
| 4 | Red-Yellow | J133-5 | Q87 |
| 5 | Red-Green | J133-6 | Q86 |
| 6 | Red-Blue | J133-7 | Q85 |
| 7 | Red-Violet | J133-8 | Q84 |
| 8 | Red-Gray | J133-9 | Q83 |

## Matrix cells

The page prints each cell as the description with the two-digit address in the cell's bottom-right
corner (column digit first, row digit second). Cell text as printed, including line breaks collapsed
to spaces:

| Addr | Printed cell | Addr | Printed cell | Addr | Printed cell | Addr | Printed cell |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | (E)-S-C-A-P-E | 21 | Right Return | 31 | 5 x 3, Top Left 1 | 41 | 5 x 3, Middle Left 1 |
| 12 | E-(S)-C-A-P-E | 22 | Right Drain | 32 | 5 x 3, Top Left 2 | 42 | 5 x 3, Middle Left 2 |
| 13 | E-S-(C)-A-P-E | 23 | Doctor 7 (2 lamps) | 33 | 5 x 3, Top Middle | 43 | 5 x 3, Middle Middle |
| 14 | E-S-C-(A)-P-E | 24 | ESCAPE Special | 34 | 5 x 3, Top Right 2 | 44 | 5 x 3, Middle Right 2 |
| 15 | E-S-C-A-(P)-E | 25 | ESCAPE 3,000,000 | 35 | 5 x 3, Top Right 1 | 45 | 5 x 3, Middle Right 1 |
| 16 | E-S-C-A-P-(E) | 26 | ESCAPE 2,000,000 | 36 | Doctor 2 (2 lamps) | 46 | Transmat Award |
| 17 | Left Drain | 27 | ESCAPE 1,000,000 | 37 | Hangon Score | 47 | Tardis |
| 18 | Left Return | 28 | ESCAPE 500,000 | 38 | Video Mode | 48 | Doctor 1 (2 lamps) |

| Addr | Printed cell | Addr | Printed cell | Addr | Printed cell | Addr | Printed cell |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 51 | 5 x 3, Bottom Left 1 | 61 | (R)-E-P-A-I-R | 71 | Doctor 4 (2 lamps) | 81 | (W)-H-O |
| 52 | 5 x 3, Bottom Left 2 | 62 | R-(E)-P-A-I-R | 72 | Doctor 6 (2 lamps) | 82 | Doctor 3 (2 lamps) |
| 53 | 5 x 3, Bottom Middle | 63 | R-E-(P)-A-I-R | 73 | 1.5X | 83 | W-H-O 1,000,000 |
| 54 | 5 x 3, Bottom Right 2 | 64 | R-E-P-(A)-I-R | 74 | 2X | 84 | W-H-O 2,000,000 |
| 55 | 5 x 3, Bottom Right 1 | 65 | R-E-P-A-(I)-R | 75 | 2.5X | 85 | W-H-O Lite Extra Ball |
| 56 | Mini-ply Left Lock | 66 | R-E-P-A-I-(R) | 76 | 3X | 86 | Ball Transmat & Advance Bonus X |
| 57 | Mini-ply Right Lock | 67 | Doctor 5 (2 lamps) | 77 | 3.5X | 87 | Launch Ball |
| 58 | Mini-ply Target | 68 | Shoot Again | 78 | 4X | 88 | Game Start |

The seven "Doctor N" cells are the only cells that print a lamp count, `(2 lamps)`. They agree with the
Lamp Locations parts list (`lamp-locations.md`), which prints each of those seven items as "(1 playfield)"
plus one second bulb. Items 17, 18, 21 and 22 are labelled Left Drain, Left Return, Right Return and
Right Drain here and on the parts list; the Handy Technician's Chart labels the same four cells Left
Outlane, Left Return Lane, Right Return Lane and Right Outlane.

## Circuit drawing

The drawing shows a column circuit (UNL-2803 driver, TIP107 transistor, +18V supply) feeding the lamp
through the `Yel-xxx` wire to a series diode and the `Red-xxx` row wire returning through a TIP102
transistor and an LM339 over-current comparator. Column drive A/B: A high, B low is Off; A low, B high is
On. Row drive C/D/E/F/G: normal operation H L H L H is Off, H L L H L is On. The text beneath says the
lamp turns On when the processor drives the column input low and the row input low, and that an
over-current condition shuts the lamp off through the LM339 comparator.
