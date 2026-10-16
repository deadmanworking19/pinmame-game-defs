# Corvette — Security CPU Board Connectors

Transcribed from `Bally_1994_Corvette_Manual.pdf`: the `Security CPU Board` / `A-17651-50036` drawing and its connector pin list, both on PDF page 146 (printed folio `3-32`, drawing in the upper part, pin list under it in two text columns). The pin list is printed as plain text lines of the form `Jnnn-n <wire colour> <function/destination>` with the wire colour spelled out in full and, except on the Dir Sw lines of `J205`, no comma after the wire colour; connectors without pin rows are printed as one line such as `J203 Not Used`. Each line is given here as one table row, with everything printed after the pin designator kept literally in the `Printed text` column; misspellings are reproduced as printed. Blank lines between connectors on the page are not rows. Read from the rendered page (300 dpi scan), not from the OCR text. The pin list has no heading line of its own. Column layout: left column `J201`-`J208`, right column `J209`-`J213`.

## Printed page 3-32 (PDF page 146): board drawing

Title lines: `Security CPU Board` / `A-17651-50036`. The drawing is an unrotated landscape board outline with a notch at the right edge. Only designators and pin-number end labels are printed; one `*` marker appears at one pin position of the single-row headers (the keyed pin; star positions were not transcribed because the pin list names the `Key` pin of each connector).

| Connector as labelled on the drawing | Position on the drawing | Pin-number end labels printed |
| --- | --- | --- |
| J213 | top edge, left | `1` (left end), `5` (right end) |
| J211 | top edge, middle, two-row header | `33` and `34` (left end), `1` and `2` (right end) |
| J210 | top edge, right | `1` (left end), `7` (right end) |
| J201 | left edge, vertical two-row header | `26` and `25` (top end), `2` and `1` (bottom end) |
| J202 | left edge, vertical two-row header | `34` and `33` (top end), `2` and `1` (bottom end) |
| J203 | bottom left | `3` (left end), `1` (right end) |
| J204 | bottom middle, two-row header | `26` and `25` (left end), `1` and `2` (right end) |
| J206 (upper) | right edge, vertical, top of the left-hand column | `1` (top end), `9` (bottom end) |
| J209 | right edge, vertical, top of the right-hand column | `1` (top end), `9` (bottom end) |
| J206 (lower) | right edge, vertical, middle of the left-hand column | `1` (top end), `9` (bottom end) |
| J207 | right edge, vertical, middle of the right-hand column | `1` (top end), `9` (bottom end) |
| J212 | right edge, vertical, bottom of the left-hand column | `1` (top end), `8` (bottom end) |
| J205 | right edge, vertical, bottom of the right-hand column | `1` (top end), `12` (bottom end) |

The drawing prints the designator `J206` twice (two 9-pin vertical headers one above the other); the pin list has `J206 Not Used` and `J208 Not Used` and no connector labelled `J208` is drawn (see Uncertain readings).

Fuses printed: none. LEDs printed: none. Test points printed: none. Other printed labels: none. The drawing has no printed notes, no part numbers other than `A-17651-50036`, no IC or battery-holder designators and no pin function labels.

## Connector pin list

## Printed page 3-32 (PDF page 146): connector pin list

### Left column

#### J201

Printed as a single line (no pin rows): `J201 Ribbon Cable data to J602`

#### J202

Printed as a single line (no pin rows): `J202 Ribbon Cable data to J903; J506; J601`

#### J203

Printed as a single line (no pin rows): `J203 Not Used`

#### J204

Printed as a single line (no pin rows): `J204 Ribbon Cable data to A-16100 J1`

#### J205

| Pin | Printed text |
| --- | --- |
| J205-1 | Orange-Brown Dir Sw 1, Left Coin to J1-14 |
| J205-2 | Orange-Red Dir Sw 2, Center Coin to J1-13 |
| J205-3 | Orange-Black Dir Sw 3, Right Coin to J1-12 |
| J205-4 | Orange-Yellow Dir Sw 4, 4th Coin to J1-17 |
| J205-5 | Key |
| J205-6 | Orange-Green Dir Sw 5, Escape/Service to J1-11 |
| J205-7 | Orange-Blue Dir Sw 6, Down/Vol Down to J1-10 |
| J205-8 | Orange-Violet Dir Sw 7, Up/Vol Up to J1-9 |
| J205-9 | Orange-Gray Dir Sw 8, Enter/Test to J1-8 |
| J205-10 | Black ground to J1-15 |
| J205-11 | Not Used |
| J205-12 | Orange-White Enable to J1-18 |

#### J206

Printed as a single line (no pin rows): `J206 Not Used`

#### J207

| Pin | Printed text |
| --- | --- |
| J207-1 | Green-Brown Sw Col 1 to playfield switches |
| J207-2 | Not Used |
| J207-3 | Green-Orange Sw Col 3 to playfield switches |
| J207-4 | Green-Yellow Sw Col 4 to playfield switches |
| J207-5 | Green-Black Sw Col 5 to playfield switches |
| J207-6 | Green-Blue Sw Col 6 to playfield switches |
| J207-7 | Green-Violet Sw Col 7 to playfield switches |
| J207-8 | Key |
| J207-9 | Green-Gray Sw Col 8 to playfield switches |
| J207-10 | Not Used |
| J207-11 | Not Used |

#### J208

Printed as a single line (no pin rows): `J208 Not Used`

### Right column

#### J209

| Pin | Printed text |
| --- | --- |
| J209-1 | White-Brown Sw Row 1 to playfield switches |
| J209-2 | White-Red Sw Row 2 to playfield switches |
| J209-3 | White-Orange Sw Row 3 to playfield switches |
| J209-4 | White-Yellow Sw Row 4 to playfield switches |
| J209-5 | White-Green Sw Row 5 to playfield switches |
| J209-6 | Key |
| J209-7 | White-Blue Sw Row 6 to playfield switches |
| J209-8 | White-Violet Sw Row 7 to playfield switches |
| J209-9 | White-Gray Sw Row 8 to playfield switches |

#### J210

| Pin | Printed text |
| --- | --- |
| J210-1 | Black ground from J904-4;J3-4 Sound Bd; J114-7 |
| J210-2 | Key |
| J210-3 | Black ground from J904-4; J3-5 Sound Bd; J114-5 |
| J210-4 | Gray +5VDC from J901-1; J3-1 Sound Bd; J114-4 |
| J210-5 | Gray +5VDC from J3-3 Sound Bd; J114-3 |
| J210-6 | Gray-Green +12VDC from J904-2; J114-2 |
| J210-7 | Gray-Green +12VDC from J114-1 |

#### J211

Printed as a single line (no pin rows): `J211 Ribbon Cable data from J113`

#### J212

| Pin | Printed text |
| --- | --- |
| J212-1 | Green-Brown Sw Col 1 to J1-1 |
| J212-2 | Green-Red Sw Col 2 to J1-7 |
| J212-3 | Not Used |
| J212-4 | White-Brown Sw Row 1 to J1-6 |
| J212-5 | Key |
| J212-6 | White-Red Sw Row 2 to J1-5 |
| J212-7 | White-Orange Sw Row 3 to J1-4 |
| J212-8 | White-Yellow Sw Row 4 to J1-3 |

#### J213

| Pin | Printed text |
| --- | --- |
| J213-1 | Black to battery holder J1-1 |
| J213-2 | Black to battery holder J1-2 |
| J213-3 | Key |
| J213-4 | Gray to battery holder J1-4 |
| J213-5 | Gray to batter holder J1-5 |

## Uncertain readings

No pin list text is uncertain; all lines were read from legible crops (`c146-L0.png` to `c146-L2.png`, `c146-R0.png` to `c146-R2.png`, `c146-draw1.png`, `c146-draw2.png`, `c146-draw3.png`). Notes on literal printing, not readings that are in doubt:

- The drawing prints the designator `J206` on two different 9-pin headers; no `J208` is drawn although the pin list has `J208 Not Used`. Which of the two drawn headers is `J206` and which is `J208` is not printed. Crop: `c146-draw2.png`.
- `J213-5` prints `batter holder` (sic).
- `J210-1` prints `J904-4;J3-4 Sound Bd; J114-7` with no space after the first semicolon; `J210-3` prints `from J904-4` (not `J904-5`) for the ground; the Fliptronic board list prints `J904-5` for the corresponding ground pin. The three PDB/Fliptronic/CPU lists are transcribed as printed and not reconciled here.
- `J201`, `J202`, `J204` and `J211` are drawn as two-row headers (26, 34, 26 and 34 pins by their end labels); the list gives each of them as a single line only. `J203` is drawn with 3 pins and `J213` with 5 pins.
