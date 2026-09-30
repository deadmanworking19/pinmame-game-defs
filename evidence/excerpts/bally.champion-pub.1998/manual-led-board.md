# Factory 24-LED board and connector table

Literal schematic and connector transcription from PDF 157, printed 3-27, A-21991-1 (For Life Light Feature). The component diagram prints A-21991. The schematic contains 24 LEDs, twelve 330-ohm series resistors and twelve pairs. No public controller address is printed on this sheet.

| J1 pin | Series pair / purpose |
| --- | --- |
| 1 | COL (common) |
| 2 | KEY |
| 3 | L23 / L24 |
| 4 | L21 / L22 |
| 5 | L19 / L20 |
| 6 | L17 / L18 |
| 7 | L15 / L16 |
| 8 | L13 / L14 |
| 9 | L11 / L12 |
| 10 | L9 / L10 |
| 11 | L1 / L2 |
| 12 | L3 / L4 |
| 13 | L5 / L6 |
| 14 | L7 / L8 |

Every literal connector row follows. Asymmetry between the printed right and left mappings is retained, without a silent correction.

| J1 pin | Right wire | Right serial-board connection | Left wire | Left serial-board connection |
| --- | --- | --- | --- | --- |
| 1 | GRY | J3-10 | GRY | J5-10 |
| 2 | KEY |  | KEY |  |
| 3 | RED-YEL | J4-4 | RED-YEL | J6-4 |
| 4 | RED-BRN | J4-1 | RED-BRN | J6-1 |
| 5 | RED-BLK | J4-2 | RED-BLK | J6-2 |
| 6 | RED-ORG | J4-3 | RED-ORG | J6-3 |
| 7 | YEL-GRY | J3-8 | YEL-GRY | J5-9 |
| 8 | YEL-VIO | J3-7 | YEL-VIO | J5-8 |
| 9 | YEL-BLU | J3-6 | YEL-BLU | J5-6 |
| 10 | YEL-GRN | J3-5 | YEL-GRN | J5-5 |
| 11 | YEL-BRN | J3-1 | YEL-BRN | J5-1 |
| 12 | YEL-RED | J3-2 | YEL-RED | J5-2 |
| 13 | YEL-ORG | J3-3 | YEL-ORG | J5-3 |
| 14 | YEL-BLK | J3-4 | YEL-BLK | J5-4 |

Native schematic bands and the component strip retain drawing evidence for the pair construction and layout. The primary curator visually checked all rows against the native scan. Mapping the four 4094 output bytes to this connector table remains unresolved; retained VPX pair order is an observed display binding rather than validated factory L-number identity. The two series LEDs in one pair have separate physical positions.
