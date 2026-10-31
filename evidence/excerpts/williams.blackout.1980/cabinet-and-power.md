# Williams Blackout (game 495) - Cabinet wiring, special relay and general illumination

Sources:

- Instruction Manual and Drawing Set (`Williams_1980_Blackout_Manual_with_paginated_schematics.pdf`), PDF page 20 / printed 23, Power Wiring Diagram; PDF page 21, left half / printed 24, Cabinet Wiring Diagram; PDF page 3 / printed 4-5, Inspection.
- Instruction Booklet 16P-495-103, PDF page 9 / printed 9, Table 3 row 15.
- IPDB machine 317 page (Wayback capture 20250218215702), notes paragraph.

## Special relay and general illumination (power wiring diagram, printed page 23)

- Coil: `6L15 SPECIAL RELAY`, drawn with a diode across it, on connector 6J2/6P2: pin 1 RED from the POWER SUPPLY +28V; pin 2 BRN-VIO from `DRIVER SOL. 15 BOARD (Q 43)`; pin 3 `N/C`.
- Contact: drawn in series with transformer terminal `6T1-19 YEL`, on the `6.3 V.A.C.` winding (terminals 17 and 19, both YEL). The contact is drawn closed, with a dashed line to the 6L15 coil.
- 6T1-17 YEL runs through fuse `6F1 20A` on the FUSE CARD (NOTE 5) and out as YEL to 7P1-1, 8P2-1, 9P1-1 and 9P1-4.
- The contact side runs through the fuse card without a fuse and out as YEL-WHT to 7P1-2 and as WHT-YEL to 8P2-2, 9P1-2 and 9P1-5.
- The bracket on the right labels these outputs `6.3 V.A.C. GENERAL ILLUMINATION`.

Table 3 (booklet) row 15: `15 Special Relay BRN-VIO 2P9-5, 6P2 Q43 5A-9384`.

IPDB notes (machine 317), quoted: "Blackout was the first Williams pin-game to have computer-controlled general illumination, used for the "BLACKOUT" sequence. This was accomplished using a relay mounted to the backbox floor, called the G.I. Relay, which cut power to all playfield lamps."

## Cabinet Wiring Diagram (printed page 24)

Flipper buttons and coils:

- `FLIPPER GRD` from 2J12/2P12: ORN-GRY 2P12-2 to 7P1-9; ORN-VIO 2P12-1 to 7P1-7.
- `PLAYFIELD FLIPPER COILS` on 8J3/8P3: BLU-VIO 8P3-3 to 7P1-8; BLK-YEL (NOTE 1) 8P3-15 to 7P1-31, dashed; BLU-GRY 8P3-4 to 7P1-10; BLK-BLU (NOTE 1) 8P3-9 to 7P1-30, dashed.
- `7SW72 RIGHT FLIPPER (NOTE 1)` is drawn between 7P1-7 and 7P1-8, with a dashed second contact to 7P1-31.
- `7SW73 LEFT FLIPPER (NOTE 1)` is drawn between 7P1-9 and 7P1-10, with a dashed second contact to 7P1-30.
- NOTE 1: the dashed flipper switch contacts are used only in games with dual action flippers.

Coin door and service:

- `7SW76 MEMORY PROTECT INTERLOCK`, drawn open, between BLK-RED from 1J4/1P4-1 (`MEM. PROT.`, 7P1-34) and GRD, WHT 1P4-2 (7P1-4, 7P2-13).
- ADVANCE: GRN 1P4-3 to 7P1-5 and 7P2-14. AUTO./MAN.: BLU 1P4-4 to 7P1-6 and 7P2-15.
- `7SW75 ADVANCE` and `7SW74 AUTO-UP / MANUAL-DOWN` on the coin door.
- Coin door GENERAL ILLUMINATION: three bulbs on 7P2-1 and 7P2-2, fed YEL and YEL-WHT from the fuse card's 6.3 V.A.C. outputs on 7P1-1 and 7P1-2.
- SPEAKER: BLK-BRN 10P2-2 to 7P1-33; BLACK 10P2-3 to 7P1-32. 7R1 REMOTE VOLUME on 10J4/10P4.

Cabinet switches and coils are transcribed in `switch-matrix.md` and `solenoid-connections.md`.

## Inspection (printed pages 4-5)

The inspection list places the transformer, rectifiers and power supply in the backbox. It lists the credit knocker, ball roll tilt, plumb bob tilt, coin lockout, volume control, AC outlet, memory protect interlock and the diagnostic switches in the cabinet or on the coin door.
