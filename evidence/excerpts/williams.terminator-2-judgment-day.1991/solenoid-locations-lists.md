# Terminator 2: Judgment Day - Solenoid Locations lists

Source: `Terminator 2 Judgement Day Operations Manual.pdf` (ARC ARC retained source SHA-256 `8540d654b39c58ad3b19ece0f42eb1dfdb8460d249e9480f8906385c8ecdb16b`), PDF page 105, printed page 2-39, headed `Solenoid Locations`. The left half of the page holds the three lists that key the balloon drawing on the right half (the drawing is the separate excerpt `solenoid-locations.md`); they are retained in two crops, `solenoid-locations-lists-1.webp` (the 01-28 list) and `solenoid-locations-lists-2.webp` (General Illumination Circuits and Flippers). Transcribed manually from the image-only scan and checked against a native-resolution render of the page. The edges of drawing balloons 28, 23, 25, 16, 6, 19 and 8 show at the crop's right edge; they belong to the drawing.

Header columns, as printed: `No.` | `Part No.` | `Description`.

| No. | Part No. | Description |
| --- | --- | --- |
| 01 | AE-23-800 | Ball Popper |
| 02 | AE-24-900 | Gun Kicker |
| 03 | AE-27-1200 | Outhole |
| 04 | AE-26-1200 | Trough |
| 05 | AE-26-1500 | Right Sling |
| 06 | AE-26-1500 | Left Sling |
| 07 | AE-23-800 | Knocker |
| 08 | AE-23-800 | Kickback |
| 09 | AE-23-800 | Plunger |
| 10 | AE-26-1500 | Top Lock |
| 11 | 14-7963 | Gun Motor |
| 12 | SM1-26-600 | Knock Down |
| 13 | AE-26-1200 | Left Jet |
| 14 | AE-26-1200 | Right Jet |
| 15 | AE-26-1200 | Bottom Jet |
| 16 | AE-26-1500 | Left Lock |
| 17 | #906 | Hot Dog Flashlamps |
| 18 | #906, #89 | Right Sling Flashlamps |
| 19 | #906, #89 | Left Sling Flashlamps |
| 20 | #906, #89 | Left Lock Flashlamps |
| 21 | #89 | Gun Flashlamps |
| 22 | #906, #89 | Right Ramp Flashlamps |
| 23 | #906, #89 | Left Ramp Flashlamps |
| 24 | #906 | Backglass Flashlamps |
| 25 | #89 | Targets Flashlamps |
| 26 | #89 | Left Popper Flashlamps |
| 27 | #89 | Right Popper Flashlamps |
| 28 | AE-26-1200 | Drop Target Flashlamp |

Row 28 is printed `Drop Target Flashlamp` beside the coil part number AE-26-1200; the solenoid tables name the same output `Drop Target` with that coil, so `Flashlamp` here is a misprint of the description, kept literally.

`General Illumination Circuits`

| No. | Part No. | Description |
| --- | --- | --- |
| 01 | #555 | Top Insert String |
| 02 | #555 | Bottom Insert String |
| 03 | #555 | Right Playfield String |
| 04 | #555 | CPU String |
| 05 | #555 | Left Playfield String |

`Flippers`

| No. | Part No. | Description |
| --- | --- | --- |
| (blank) | FL-11630 | Lower Right Flipper |
| (blank) | FL-11630 | Lower Left Flipper |

This list numbers the general-illumination circuits in the same order, with the same names, as the L-8 ROM's own T.6 GENERAL ILLUMINATION test (`evidence/runtime/wpc-alpha/terminator-2-t2_l8-gi-test.json`): 01 Top Insert, 02 Bottom Insert, 03 Right Playfield, 04 CPU String, 05 Left Playfield. The solenoid tables on printed pages 1-28 and 2-38 instead print `02 Left Playfield G.I.`, `04 Not Used` and `05 Bottom Insert G.I.`.
