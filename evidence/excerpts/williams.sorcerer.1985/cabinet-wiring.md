# Drawing excerpt — System 9 Cabinet Wiring Diagram

`reviewed: true`; read by the curator from the rendered crop and a 300 dpi render of the whole sheet on 2026-10-16
`source: Instruction Manual PDF page 21, printed folio 21, "SYSTEM 9 CABINET WIRING DIAGRAM"`

Image: `cabinet-wiring.webp` beside this file (upper-left block of the sheet; crop and resolution in the source
record's `image_derivation`). Full-sheet render: `external:pinmame-manuals/by-machine/williams.sorcerer.1985/rendered-300/p-21.png`.

The connections this definition relies on, as drawn:

| CPU jack and pin | Signal label | Plug pin | Wire | Cabinet end |
| --- | --- | --- | --- | --- |
| 1J12-7 | SOL.14 (Q59) | 1P12-7 | ⟦none⟧ | `NC` |
| 1J12-8 | SOL.15 (Q60) | 1P12-8 | BRN-VIO | 7J1-17 to `BELL` coil `7L15`, diode `7D15`, with a `.1MF 500V` capacitor across its contacts |
| 1J12-9 | SOL.16 (Q61) | 1P12-9 | BRN-GRY | 7J1-18 to 7J2-4 and coin lockout `7L16` (right of the crop) |
| 1J19-2 / 1J19-1 | FLIPPER GND | 1P19-2 / 1P19-1 | ORG-GRY / ORG-VIO | 7J1-9 and 7J1-7 to the flipper buttons |

Flipper buttons drawn in the cabinet: `7SW72 RIGHT FLIPPER` between 7J1-7 and 7J1-8 (BLU-VIO to playfield
8P3-34); `7SW73 LEFT FLIPPER` between 7J1-9 and 7J1-10 (BLU-GRY to 8P3-32); and a second contact labelled
`UPPER LEFT FLIPPER` on the left button, from 7J1-9 to 7J1-30 (BLK-BLU to 8P3-31). Each contact has a `.1 MF`
capacitor across it. 8P3/7J1-31 is marked `NC`.

Cabinet switches on the same sheet (outside the crop): `7SW1 PLUMB BOB TILT`, `7SW2 BALL ROLL TILT`,
`7SW3 CREDIT BUTTON` (column 1J8-1 GRN-BRN, rows WHT-BRN/WHT-RED/WHT-ORG with diodes 7D1-7D3), and on the coin door
`7SW4 RIGHT COIN CHUTE`, `7SW5 CENTER COIN CHUTE`, `7SW6 LEFT COIN CHUTE`, `7SW7 SLAM TILT`, `7SW8 HIGH SCORE
RESET` (diodes 7D4-7D8), `7SW74` AUTO-UP / MANUAL-DOWN, `7SW75 ADVANCE` and `7SW76 MEMORY PROTECT INTERLOCK`, and
three coin-door `GENERAL ILLUMINATION` lamps fed from power-supply 3J8-4 / 3J8-9 (6.3VAC, YEL / YEL-WHT).

This is a System 9 sheet, not one drawn for Sorcerer alone; the `NC` end of SOL.14 agrees with the game's own
solenoid table and coil list, which both print row 14 `Not Used`.
