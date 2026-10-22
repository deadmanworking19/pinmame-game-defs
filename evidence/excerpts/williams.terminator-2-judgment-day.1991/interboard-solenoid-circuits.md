# Terminator 2: Judgment Day - Interboard Wiring, solenoid and flipper circuits

Source: `Terminator 2 Judgement Day Operations Manual.pdf` (ARC ARC retained source SHA-256 `8540d654b39c58ad3b19ece0f42eb1dfdb8460d249e9480f8906385c8ecdb16b`), PDF page 114, printed page 3-8 (footer `Terminator 2 pg. 3-8`), section 3 wiring. The whole page content is retained in three overlapping crops: `interboard-solenoid-circuits-1.webp` (solenoids 1-14), `-2.webp` (solenoids 14-28 and the tieback diode) and `-3.webp` (flipper circuits). Transcribed manually from the image-only scan and checked against a native-resolution render of the page.

`Solenoid Circuits`, header `Connectors from Power Driver Board`, columns `Wire Color` | `Function` | `To Playfield` | `To Insert` | `Transistor`. A blank cell is `(blank)`.

| Wire Color | Function | To Playfield | To Insert | Transistor |
| --- | --- | --- | --- | --- |
| Violet/Brown | Solenoid 1, High Power | J130-1 | (blank) | Q82 |
| Violet/Red | Solenoid 2, High Power | J130-2 | (blank) | Q80 |
| Violet/Orange | Solenoid 3, High Power | J130-4 | (blank) | Q78 |
| Violet/Yellow | Solenoid 4, High Power | J130-5 | (blank) | Q76 |
| Violet/Green | Solenoid 5, High Power | J130-6 | (blank) | Q64 |
| Violet/Blue | Solenoid 6, High Power | J130-7 | (blank) | Q66 |
| Violet/Black | Solenoid 7, High Power | J130-8 | (blank) | Q68 |
| Violet/Gray | Solenoid 8, High Power | J130-9 | (blank) | Q70 |
| Brown/Black | Solenoid 9, Low Power | J127-1 | (blank) | Q58 |
| Brown/Red | Solenoid 10, Low  Power | J127-3 | (blank) | Q56 |
| Brown/Orange | Solenoid 11, Low Power | J127-4 | (blank) | Q54 |
| Brown/Yellow | Solenoid 12, Low Power | J127-5 | (blank) | Q52 |
| Brown/Green | Solenoid 13, Low Power | J127-6 | (blank) | Q50 |
| Brown/Blue | Solenoid 14, Low Power | J127-7 | (blank) | Q48 |
| Brown/Violet | Solenoid 15, Low Power | J127-8 | (blank) | Q46 |
| Brown/Gray | Solenoid 16, Low Power | J127-9 | (blank) | Q44 |
| Black/Brown | Sol. 17, Flasher 1, No Diode | J126-1 | (blank) | Q42 |
| Black/Red | Sol. 18, Flasher 2, No Diode | J126-2 | (blank) | Q40 |
| Black/Orange | Sol. 19, Flasher 3, No Diode | J126-3 | (blank) | Q38 |
| Black/Yellow | Sol. 20, Flasher 4, No Diode | J126-4 | J125-2 | Q36 |
| Blue/Green | Sol. 21, Special 1 Drive | J126-5 | J125-3 | Q28 |
| Blue/Black | Sol. 22, Special 2 Drive | J126-6 | J125-5 | Q30 |
| Blue/Violet | Sol. 23, Special 3 Drive | J126-7 | (blank) | Q34 |
| Blue/Gray | Sol. 24, Special 4 Drive | (blank) | J125-7 | Q32 |
| Blue/Brown | Sol. 25, Special 5 Drive | J122-1 | J125-8 | Q26 |
| Blue/Red | Sol. 26, Special 6 Drive | J122-2 | J125-9 | Q24 |
| Blue/Orange | Sol. 27, Special 7 Drive | J122-3 | (blank) | Q22 |
| Blue/Yellow | Sol. 28, Special 8 Drive | J122-4 | (blank) | Q20 |
| Violet/Orange | Sol. 28, Tieback Diode | J122-9 | (blank) | (blank) |

`Solenoid 10, Low  Power` is printed with two spaces before `Power`.

`Flipper Circuits`, header `Connectors from Power Driver Board`, columns `Wire Color` | `Function` | `To Playfield`.

| Wire Color | Function | To Playfield |
| --- | --- | --- |
| Gray/Yellow | Left Flipper Power | J109-5 |
| Blue/Yellow | Right Flipper Power | J109-7 |
| Black/Blue | Upper Left Flipper | Not Used |
| Blue/Gray | Lower Left Flipper | J109-3 |
| Black/Yellow | Upper Right Flipper | Not Used |
| Blue/Violet | Lower Right Flipper | J109-4 |
| Black/Blue | Upper Left Flipper | J110-9, Not Used |
| Blue/Gray | Lower Left Flipper | J110-7 |
| Black/Yellow | Upper Right Flipper | J110-8, Not Used |
| Blue/Violet | Lower Right Flipper | J110-6 |
| Orange/Gray | Left Flipper Ground | J110-2, 1 |
| Orange/ Violet | Right Flipper Ground | J110-4, 3 |

A blank line separates the first six flipper rows from the last six, and the 1-16 solenoid rows from the 17-28 rows. The solenoid-12 row prints the same Brown/Yellow wire, J127-5 and Q52 as both solenoid tables; this table has no part-number or `Not Used` column.
