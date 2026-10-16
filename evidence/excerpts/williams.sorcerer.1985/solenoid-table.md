# Literal transcription — System-9 Solenoid Table

`reviewed: true`; transcribed by the curator from a 300 dpi render and visually checked against it on 2026-10-16
`source: Instruction Manual PDF page 14, printed folio 13`

Retained render: `external:pinmame-manuals/by-machine/williams.sorcerer.1985/rendered-300/p-14.png`
(pdftoppm -r 300 -gray).

Literal heading: `System-9 Solenoid Table`. A leading `*` on a number is printed and refers to Note 1. `—` is
a printed dash; `⟦blank⟧` is a visibly empty cell. `SORCERER` in row 07 is printed in bold capitals.

| SOL. NO. | FUNCTION | SOLENOID TYPE | WIRE COLOR | CPU BOARD | PLAYFIELD/CABINET | DRIVER TRANS. | SOLENOID PART NO. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Outhole | controlled | GRY-BRN | 1J11-1 | 8P3-1 | Q47 | SA-23-850-DC |
| 02 | Ramp Eject | controlled | GRY-RED | 1J11-3 | 8P3-2 | Q48 | SG1-23-850-DC |
| 03 | Multi-Ball Eject | controlled | GRY-ORN | 1J11-4 | 8P3-3 | Q49 | SG1-23-850-DC |
| 04 | 3-Bank Drop Target | controlled | GRY-YEL | 1J11-5 | 8P3-4 | Q50 | SA-3-23-850-DC |
| 05 | Demon Background | controlled | GRY-GRN | 1J11-6 | 8P3-5 | Q39 | #63 Flashlamp |
| 06 | 3-Bank Flash | controlled | GRY-BLU | 1J11-7 | 8P3-6 | Q40 | #63 Flashlamp |
| 07 | SORCERER Bank | controlled | GRY-VIO | 1J11-8 | 8P3-7 | Q41 | #63 Flashlamp |
| 08 | Flash Eyes (cabinet) | controlled | GRY-BLK | 1J11-9 | 8P3-8 | Q42 | 5580-08994-00 |
| 09 | Not Used | controlled | BRN-BLK | 1J12-1 | 8P3-9 | Q54 | — |
| 10 | Not Used | controlled | BRN-RED | 1J12-2 | 8P3-10 | Q55 | — |
| 11 | General Illumination | controlled | BRN-ORN | 1J12-4 | 3P7-1 | Q56 | 5580-09555-00 |
| 12 | Not Used | controlled | BRN-YEL | 1J12-5 | 8P3-12 | Q57 | — |
| 13 | Not Used | controlled | BRN-GRN | 1J12-6 | 8P3-13 | Q58 | — |
| 14 | Not Used | controlled | BRN-BLU | 1J12-7 | 8P3-14 | Q59 | SA-4-23-850-DC |
| 15 | Bell | controlled | BRN-VIO | 1J12-8 | 7P1-17 | Q60 | SM-29-1000-DC |
| 16 | Coin-Lockout Coil | controlled | BRN-GRY | 1P12-9 | 7P1-18, 7P2-4 | Q61 | SM-35-4000-DC |
| *17 | Left Kicker | special #1 | BLU-BRN | 1J19-7 | 8P3-17 | Q75 | SG1-23-850-DC |
| *18 | Right Kicker | special #2 | BLU-RED | 1J19-4 | 8P3-18 | Q77 | SG1-23-850-DC |
| *19 | Left Jet-Bumper | special #3 | BLU-ORN | 1J19-3 | 8P3-19 | Q79 | SG1-23-850-DC |
| *20 | Lower Jet-Bumper | special #4 | BLU-YEL | 1J19-6 | 8P3-20 | Q81 | SG1-23-850-DC |
| *21 | Right Jet-Bumper | special #5 | BLU-GRN | 1J19-8 | 8P3-21 | Q83 | SG1-23-850-DC |
| *22 | Not Used | special #6 | BLU-BLK | 1J19-9 | 8P3-22 | Q85 | — |
| — | Top Flipper | ⟦blank⟧ | BLK-BLU | 1J19-2 | 7P1-30 | — | FL24/600-30/2600-50VDC |
| — | Right Flipper* | ⟦blank⟧ | ORN-VIO | 1J19-1 | 7P1-7 | — | FL23/600-30/2600-50VDC |
| — | Left Flipper* | ⟦blank⟧ | ORN-GRY | 1J19-2 | 7P1-9 | — | FL23/600-30/2600-50VDC |

Notes as printed below the table (`*NOTES`):

1. Special-switch connections for solenoids 17 thru 21 are as follows:
   17—ORN-BRN—1J18-5, 8P3-24; 18—ORN-RED—1J18-3, 8P3-25; 19—ORN-BLK—1J18-2, 8P3-26;
   20—ORN-YEL—1J18-4, 8P3-27; 21—ORN-GRN—1J18-8, 8P3-28.
2. FLIPPER COILS. This game requires 50-volt flipper coils. For proper operation, the replacement part shown
   MUST be used.
3. Flipper-button connections: Right—ORN-VIO—1J19-1, 7P1-7; Left—ORN-GRY—1J19-2, 7P1-9;
   Top—BLK-BLU—1J19-2, 7P1-30.
4. Typical wiring for solenoids and special switches follows. (A drawing shows a coil with a parallel diode to
   `RED (B+)` and a switch with a parallel resistor-capacitor to `BLK (GND)`.)

Literal oddities kept as printed: row 16's CPU connection reads `1P12-9` where every other controlled row
reads `1J12-n`; row 14's function reads `Not Used` while its part-number cell carries `SA-4-23-850-DC` and its
playfield cell `8P3-14`; the flipper part number of the Left Flipper row in the parts list on PDF page 20 is
printed `FL23/600-30/2600-%)VDC`, which is a print defect of `50VDC`.
