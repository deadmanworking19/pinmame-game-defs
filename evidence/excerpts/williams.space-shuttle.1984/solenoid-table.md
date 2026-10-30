# Literal transcription — System-9 Solenoid Table

`reviewed: true`; transcribed by the curator from a 300 dpi render and visually checked against it on 2026-10-30
`source: Instruction Manual PDF page 14`

Retained render: `external:pinmame-manuals/by-machine/williams.space-shuttle.1984/rendered-300/p-14.png` (pdftoppm 23.05.0 -r 300 -gray).

Literal heading: `System-9 Solenoid Table`. A leading `*` on a number is printed and refers to Note 1. `-` is a
printed dash; `⟦blank⟧` is a visibly empty cell. The CPU column prints `1P11-n`/`1P12-n` for the controlled
solenoids and `1P-19-n` for the specials.

| SOL. NO. | FUNCTION | WIRE COLOR | CPU BOARD | PLAYFIELD/CABINET | DRIVER TRANS. | SOLENOID PART NO. |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | Outhole | GRY-BRN | 1P11-1 | 8P3-1 | Q47 | SA-23-850-DC |
| 02 | Ball-Ramp Release | GRY-RED | 1P11-3 | 8P3-2 | Q46 | SG 1-23-850-DC |
| 03 | Left Eject-Hole | GRY-ORN | 1P11-4 | 8P3-3 | Q49 | SG 1-23-850-DC |
| 04 | Right Eject-Hole | GRY-YEL | 1P11-5 | 8P3-4 | Q50 | SG 1-23-850-DC |
| 05 | "T" Drop-Target | GRY-GRN | 1P11-6 | 8P3-5 | Q39 | SA 5-24-750-DC |
| 06 | 3-Bank Drop-Target | GRY-BLU | 1P11-7 | 8P3-6 | Q40 | SA 3-23-850-DC |
| 07 | Up Post | GRY-VIO | 1P11-8 | 8P3-7 | Q41 | SG-23-850-DC |
| 08 | Down Post | GRY-BLK | 1P11-9 | 8P3-8 | Q42 | SM-29-1100-DC |
| 09 | Space Flash-Lamps | BRN-BLK | 1P12-1 | 8P3-9 | Q54 | - |
| 10 | Shuttle Flash-Lamps | BRN-RED | 1P12-2 | 8P3-10 | Q55 | - |
| 11 | General Illumination | BRN-ORN | 1P12-4 | 3P7-1 | Q56 | 5580-09555-00 |
| 12 | Not Used | BRN-YEL | 1P12-5 | 8P3-12 | Q57 | - |
| 13 | Gate | BRN-GRN | 1P12-6 | 8P3-13 | Q58 | SZ-35-4000-DC |
| 14 | Insert Flash-Lamps | BRN-BLU | 1P12-7 | 8P3-14 | Q59 | - |
| 15 | Bell | BRN-VIO | 1P12-8 | 7P1-17 | Q60 | SM-29-1000-DC |
| 16 | Coin-Lockout Coil | BRN-GRY | 1P12-9 | 7P1-18, 7P2-4 | Q61 | SM-35-4000-DC |
| *17 | Left Kicker | BLU-BRN | 1P-19-7 | 8P3-17 | Q75 | SG1-23-850-DC |
| *18 | Right Kicker | BLU-RED | 1P-19-4 | 8P3-18 | Q77 | SG1-23-850-DC |
| *19 | Left Jet-Bumper | BLU-ORN | 1P-19-3 | 8P3-19 | Q79 | SG1-23-850-DC |
| *20 | Lower Jet-Bumper | BLU-YEL | 1P-19-6 | 8P3-20 | Q81 | SG1-23-850-DC |
| *21 | Right Jet-Bumper | BLU-GRN | 1P-19-8 | 8P3-12 | Q83 | SG1-23-850-DC |
| *22 | Not Used | BLU-BLK | 1P-19-9 | 8P3-22 | Q85 | - |
| — | Top Flipper | ⟦blank⟧ | ⟦blank⟧ | ⟦blank⟧ | - | FL23/600-30-2600-50VDC |
| — | Right Flipper* | BLU-VIO | 1P19-1 | 7P1-7 | - | FL23/600-30-2600-50VDC |
| — | Left Flipper* | BLU-GRY | 1P19-2 | 7P1-9 | - | FL23/600-30-2600-50VDC |

Notes as printed below the table (`*NOTES`):

1. Special-switch connections for solenoids 17 thru 21 are as follows:
   17—ORN-BRN—2P1-5, 8P3-24; 18—ORN-RED—2P1-7, 8P3-25; 19—ORN-BLK—2P1-8, 8P3-26;
   20—ORN-YEL—2P1-6, 8P3-27; 21—ORN-GRN—2P1-2, 8P3-28.
2. FLIPPER COILS. This game requires 50-volt flipper coils. For proper operation, the replacement part shown
   MUST be used.
3. Flipper-button connections: Right—ORN-VIO— 2P2-9, 7P1-7; Left—ORN-GRY—2P2-8, 7P1-9.
4. Typical wiring for solenoids and special switches follows. (A `TYPICAL WIRING` drawing shows a switch
   between `ORN-BRN` and `BLK (GRD)` and a special solenoid between `BLU-BRN` and `RED (B+)`.)

Literal oddities kept as printed, each compared with the playfield-solenoid wiring diagram (excerpt
`playfield-solenoid-wiring`): row 02 prints driver `Q46` where the diagram draws `Q48` against SOL. 2 (and the
table prints no other Q48); row 21 prints playfield pin `8P3-12`, the pin row 12 also carries, where the diagram
runs SP. SOL. 5 on 8P3-21; Note 1 prints the special-switch inputs on `2P1-n` where the diagram draws them on
CPU connector 1J18/1P18 (17 on 1J18-5, 18 on -3, 19 on -2, 20 on -4, 21 on -8). The `Top Flipper` row has no
wiring at all, and the drawings, the flipper-button note 3 and IPDB show two flippers: it is a printed row for a
part that is not fitted. The page-3 corrections sheet says of page 15 that the `Solenoid Diagrams are reversed`;
that concerns the logic diagrams, not this table.
