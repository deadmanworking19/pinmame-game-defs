# Literal transcription — Backbox Wiring: power-supply relay and CPU connector 1J19

`reviewed: true`; transcribed by the curator from a 300 dpi render and visually checked against it on 2026-10-16
`source: Instruction Manual PDF page 18, printed folio 18, "Backbox Wiring" ("C.P.U. BOARD SYSTEM 9" and "POWER SUPPLY D-8345-1914")`

Retained render: `external:pinmame-manuals/by-machine/williams.sorcerer.1985/rendered-300/p-18.png`
(pdftoppm -r 300 -gray, 5100 x 3300). Only the two connector blocks this definition relies on are transcribed;
the CPU board's lamp, switch and solenoid connectors repeat the matrix and solenoid tables.

## Power supply D-8345-1914

Relay `K1` is drawn on the board beside a `6.3 VAC` label. Its connector and the general-illumination
connectors read, pin by pin as printed:

| Connector | Label | Pin | Wire | Signal |
| --- | --- | --- | --- | --- |
| 3J7 | SPECIAL RELAY | 3 | RED | +28V |
| 3J7 | SPECIAL RELAY | 2 | ⟦blank⟧ | KEY |
| 3J7 | SPECIAL RELAY | 1 | BRN-ORN | SOL 11 |
| 3J8 | GEN. ILLUM. OUT | 9 | WHT-YEL | ⟦blank⟧ |
| 3J8 | GEN. ILLUM. OUT | 8 | WHT-GRN | ⟦blank⟧ |
| 3J8 | GEN. ILLUM. OUT | 7 | WHT-VIO | ⟦blank⟧ |
| 3J8 | GEN. ILLUM. OUT | 6 | WHT-BRN | ⟦blank⟧ |
| 3J8 | GEN. ILLUM. OUT | 5 | ⟦blank⟧ | KEY |
| 3J8 | GEN. ILLUM. OUT | 4 | YEL | ⟦blank⟧ |
| 3J8 | GEN. ILLUM. OUT | 3 | GRN | ⟦blank⟧ |
| 3J8 | GEN. ILLUM. OUT | 2 | VIO | ⟦blank⟧ |
| 3J8 | GEN. ILLUM. OUT | 1 | BRN | ⟦blank⟧ |
| 3J9 | GEN. ILLUM. IN | 2 | YEL | 6.3VAC |
| 3J9 | GEN. ILLUM. IN | 1 | YEL | 6.3VAC |

`SOL 11` on 3J7-1 with wire BRN-ORN matches row 11 of the solenoid table (`General Illumination`, BRN-ORN,
1J12-4, 3P7-1, Q56, 5580-09555-00).

## C.P.U. Board System 9, connector 1J19

Bracket labels printed beside the connector: `SPECIAL SOLENOIDS` (pins 3-9) and `18 AWG FLIPPER GND` (pins 1-2).

| Pin | Wire | Transistor | Signal |
| --- | --- | --- | --- |
| 1 | ORG/VIO | ⟦blank⟧ | ⟦flipper ground⟧ |
| 2 | ORG/GRY | ⟦blank⟧ | ⟦flipper ground⟧ |
| 3 | BLU/ORG | Q79 | SP SOL.-3 |
| 4 | BLU/RED | Q77 | SP SOL.-2 |
| 5 | ⟦blank⟧ | ⟦blank⟧ | KEY |
| 6 | BLU/YEL | Q81 | SP SOL.-4 |
| 7 | BLU/BRN | Q75 | SP SOL.-1 |
| 8 | BLU/GRN | Q83 | SP SOL.-5 |
| 9 | BLU/BLK | Q85 | SP SOL.-6 |

`⟦flipper ground⟧` marks pins whose signal column is blank but which the printed bracket names as flipper
ground. Wire colours here use the `ORG` abbreviation where the solenoid table prints `ORN`.

## C.P.U. Board System 9, connector 1J18 (`SPECIAL SOLENOID SWITCHES`)

| Pin | Wire | Signal |
| --- | --- | --- |
| 1 | ⟦blank⟧ | KEY |
| 2 | ORG/BLK | SP SOL.-3 SW |
| 3 | ORG/RED | SP SOL.-2 SW |
| 4 | ORG/YEL | SP SOL.-4 SW |
| 5 | ORG/BRN | SP SOL.-1 SW |
| 6 | ⟦blank⟧ | N.C. |
| 7 | ⟦blank⟧ | N.C. |
| 8 | ORG/GRN | SP SOL.-5 SW |
| 9 | ORG/BLU | SP SOL.-6 SW |

This agrees pin for pin with Note 1 of the solenoid table (17 ORN-BRN 1J18-5, 18 ORN-RED 1J18-3, 19 ORN-BLK
1J18-2, 20 ORN-YEL 1J18-4, 21 ORN-GRN 1J18-8), so special solenoid `n` is driver `SP SOL.-(n-16)`.
