# Corvette — Fliptronic II Board Connectors

Transcribed from `Bally_1994_Corvette_Manual.pdf`: the `Fliptronic II Board` / `A-15472-1` drawing and its connector pin list, both on PDF page 142 (printed folio `3-28`). The pin list sits under the drawing in two text columns: the left column runs `J901-1` to `J904-4` and the right column runs `J904-5` to `J907-9` (connector `J904` is split across the two columns). Each pin line is printed as plain text of the form `Jnnn-n <wire colour>, <function/destination>` with the wire colour spelled out in full and no column separators; each line is given here as one table row, with everything printed after the pin designator kept literally in the `Printed text` column. Blank lines between connectors on the page are not rows. Read from the rendered page (300 dpi scan), not from the OCR text. The pin list has no heading line of its own.

## Printed page 3-28 (PDF page 142): board drawing

Title lines: `Fliptronic II Board` / `A-15472-1`. The drawing is an unrotated board outline (notched at the upper left) with seven connectors. J902, J903, J904, J905 and J906 are drawn horizontally; J901 and J907 are drawn vertically along the right edge with rotated labels. Only designators and pin-number end labels are printed.

| Connector | Pin-number end labels printed | Notes |
| --- | --- | --- |
| J902 | `1` (left end), `13` (right end) | single-row header; one `*` marker at the 10th position from the `1` end |
| J907 | `1` (top end), `9` (bottom end) | vertical single-row header; one `*` marker at the 3rd position from the `1` end |
| J901 | `1` (top end), `5` (bottom end) | vertical single-row header; one `*` marker at the 4th position from the `1` end |
| J903 | `2` and `1` (left end), `34` and `33` (right end) | two-row header |
| J904 | `5` (left end), `1` (right end) | single-row header; one `*` marker at the 3rd position from the `1` end |
| J905 | `6` (left end), `1` (right end) | single-row header; one `*` marker at the 4th position from the `1` end |
| J906 | `6` (left end), `1` (right end) | single-row header; one `*` marker at the 2nd position from the `1` end |

Fuses printed: none. LEDs printed: none. Test points printed: none. Other printed labels: none. The drawing has no printed notes, no part numbers other than `A-15472-1`, no IC or other component designators and no pin function labels. The `*` marker positions agree with the `Key` pins named in the pin list below (`J901-4`, `J902-10`, `J904-3`, `J905-4`, `J906-2`, `J907-3`); `J903` has no `Key` line.

## Printed page 3-28 (PDF page 142): connector pin list

### Left column

#### J901

| Pin | Printed text |
| --- | --- |
| J901-1 | White-Blue, 50VAC from J104-1 |
| J901-2 | White-Blue, loop from J901-1 |
| J901-3 | White-Blue, 50VAC from J104-2 |
| J901-4 | Key |
| J901-5 | White-Blue, loop from J901-3 |

#### J902

| Pin | Printed text |
| --- | --- |
| J902-1 | Orange-Gray, holding upper left flipper |
| J902-2 | Not Used |
| J902-3 | Yellow-Gray, power upper left flipper |
| J902-4 | Orange-Violet, holding upper right flipper |
| J902-5 | Not Used |
| J902-6 | Yellow-Violet, power upper right flipper |
| J902-7 | Orange-Blue, holding lower left flipper |
| J902-8 | Not Used |
| J902-9 | Yellow-Blue, power lower left flipper |
| J902-10 | Key |
| J902-11 | Orange-Green, holding lower right flipper |
| J902-12 | Not Used |
| J902-13 | Yellow-Green, power lower right flipper |

#### J903

Printed as a single line (no pin rows): `J903 Ribbon Cable, data to/from J202; J506; J601`

#### J904 (pins 1-4; pin 5 continues in the right column)

| Pin | Printed text |
| --- | --- |
| J904-1 | Gray, +5V to/from J114-4; J210-4 |
| J904-2 | Gray-Green, +12V to/from J114-2; J210-6 |
| J904-3 | Key |
| J904-4 | Black, Ground to/from J114-7; J210-1 |

### Right column

#### J904 (pin 5, continued from the left column)

| Pin | Printed text |
| --- | --- |
| J904-5 | Black, Ground to/from J114-5; J210-3 |

#### J905

| Pin | Printed text |
| --- | --- |
| J905-1 | Black-Violet, to right flipper opto |
| J905-2 | Blue-Gray, to left flipper opto |
| J905-3 | Blue-Yellow, to right flipper opto |
| J905-4 | Key |
| J905-5 | Black-Blue, to left flipper opto |
| J905-6 | Orange, Switch Ground |

#### J906

| Pin | Printed text |
| --- | --- |
| J906-1 | Black-Green, to lower right E.O.S. switch |
| J906-2 | Key |
| J906-3 | Black-Blue, to lower left E.O.S. switch |
| J906-4 | Not Used |
| J906-5 | Black-Gray, to upper left E.O.S. switch |
| J906-6 | Orange, Switch Ground |

#### J907

| Pin | Printed text |
| --- | --- |
| J907-1 | Red-Green, +50V to lower right flipper |
| J907-2 | Red-Green, loop from J907-1 |
| J907-3 | Key |
| J907-4 | Red-Blue, +50V to lower left flipper |
| J907-5 | Red-Blue, loop from J907-4 |
| J907-6 | Red-Violet, +50V to upper right flipper |
| J907-7 | Red-Violet, loop from J907-6 |
| J907-8 | Red-Gray, +50V to upper left flipper |
| J907-9 | Red-Gray, loop from J907-8 |

## Uncertain readings

None. Crops read: `f142-L1.png`, `f142-L2.png`, `f142-R1.png`, `f142-R2.png`, `f142-draw.png`.
