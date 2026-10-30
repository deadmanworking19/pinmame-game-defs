# Literal transcription — CPU Board matrix connectors (Back Box Wiring Diagram and CPU schematic)

`reviewed: true`; transcribed by the curator from 300 dpi renders and visually checked against them on 2026-10-30
`source: Instruction Manual PDF page 18 (Back Box Wiring Diagram, C.P.U. BOARD SYSTEM-9 D-10534) and PDF page 25 (CPU schematic, switch-matrix drives and lamp strobes)`

Retained renders: `external:pinmame-manuals/by-machine/williams.space-shuttle.1984/rendered-300/p-18.png` and
`p-25.png` (pdftoppm 23.05.0 -r 300 -gray).

The backbox sheet labels every CPU connector pin. The schematic was read for the switch drives, the 1J10 key and
row-8 return and the lamp strobes; where both show a pin they agree. `/` is printed between wire colours.

## 1J10 SWITCH ROW (backbox sheet)

| label | wire | pin |
| --- | --- | --- |
| SW. ROW-1 | WHT/BRN | 9 |
| SW. ROW-2 | WHT/RED | 8 |
| SW. ROW-3 | WHT/ORG | 7 |
| SW. ROW-4 | WHT/YEL | 6 |
| SW. ROW-5 | WHT/GRN | 5 |
| KEY | — | 4 |
| SW. ROW-6 | WHT/BLU | 3 |
| SW. ROW-7 | WHT/VIO | 2 |
| SW. ROW-8 | WHT/GRY | 1 |

The schematic draws `KEY 1J10-4` and `1J10-1 SR8` at the return comparators. 1J9 is `OPTO ROW (USED ONLY IN
OPTO CIRCUIT)`; the page-3 corrections sheet says the switch-test text's `1J9 (Rows)` should read 1J10.

## 1J8 switch-matrix drives (schematic `SWITCH MATRIX DRIVES`)

`1J8-1 ST1`, `1J8-2 ST2`, `1J8-3 ST3`, `1J8-4 ST4`, `1J8-5 ST5`, `1J8-7 ST6`, `1J8-8 ST7`, `1J8-9 ST8`,
`1J8-6 KEY`, each through a 2N3904 (Q7-Q14).

## 1J7 LAMP COLUMN (backbox sheet) and lamp strobes (schematic)

| label | wire | pin |
| --- | --- | --- |
| LAMP COL-8 | YEL/GRY | 9 |
| LAMP COL-7 | YEL/VIO | 8 |
| LAMP COL-6 | YEL/BLU | 7 |
| LAMP COL-5 | YEL/GRN | 6 |
| KEY | — | 5 |
| LAMP COL-4 | YEL/BLK | 4 |
| LAMP COL-3 | YEL/ORG | 3 |
| LAMP COL-2 | YEL/RED | 2 |
| LAMP COL-1 | YEL/BRN | 1 |

The schematic agrees: `1J7-1 STROBE1` to `1J7-4 STROBE4`, `1J7-5 KEY`, `1J7-6 STROBE5` to `1J7-9 STROBE8`, each
driven by a TIP42 (Q23-Q30).

## 1J6 LAMP ROW (backbox sheet)

| label | wire | pin |
| --- | --- | --- |
| LAMP ROW-8 | RED/GRY | 9 |
| LAMP ROW-7 | RED/VIO | 8 |
| LAMP ROW-6 | RED/BLU | 7 |
| LAMP ROW-5 | RED/GRN | 6 |
| LAMP ROW-4 | RED/YEL | 5 |
| KEY | — | 4 |
| LAMP ROW-3 | RED/ORG | 3 |
| LAMP ROW-2 | RED/BLK | 2 |
| LAMP ROW-1 | RED/BRN | 1 |

Disagreement kept: the switch-matrix table prints rows 1-8 on 1J10-1, -3, -4, -5, -6, -7, -8, -9 (the reverse
order, through the key pin), and the lamp-matrix table prints column 4 on 1J7-5 and row 4 on 1J6-4 (both key
pins). Both board drawings agree with each other against the tables, so the structured wiring follows the
drawings; the table cells stay literal in their excerpts.
