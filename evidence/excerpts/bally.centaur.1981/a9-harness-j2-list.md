# Centaur — A9 harness list for connector J2 (W-1207-11, left margin)

Transcribed from `Bally_1981_Centaur_Installation_and_General_Game_Operation_Instructions_with_schematics_OCR_searchable.pdf`,
PDF page 51, drawing **W-1207-11** (`(A9) AUXILIARY LAMP DRIVER BOARD`, `1239`). This is the
`J2 TO` block in the upper left of the sheet: the harness side of the connector, drawn as a cable
whose branches end on the pins they occupy, each branch labelled with its Bally wire-colour code.
The board side of the same connector is transcribed in `a9-schematic-j2.md`. The accompanying crop
is the same region of the native 590 dpi scan.

| J2 pin | wire drawn | code | printed function |
| ---: | --- | --- | --- |
| 1 | yes | 43 | TOP MIDDLE LANE |
| 2 | yes | 40 | LEFT SLINGSHOT |
| 3 | yes | 62 | # 2 CHAMBER (2) |
| 4 | no | | KEY |
| 5 | yes | 60 | # 1 CHAMBER (2) (FROM BOTTOM) |
| 6 | yes | 45 | RIGHT SLINGSHOT |
| 7 | yes | 54 | TOP-LEFT LANE |
| 8 | no | | |
| 9 | no | | |
| 10 | no | | |
| 11 | no | | |
| 12 | yes | 27 | LEFT THUMPER BUMPER |
| 13 | no | | |
| 14 | no | | |
| 15 | no | | |
| 16 | no | | |
| 17 | yes | 96 | # 4 CHAMBER (2) TOP |
| 18 | yes | 25 | TOP RIGHT LANE |
| 19 | yes | 82 | RIGHT THUMPER BUMPER |
| 20 | yes | 95 | # 3 CHAMBER (2) |

The sheet prints `TOP-LEFT LANE` with a hyphen and a stray dot before the `7`; both are reproduced.

## Pin 11

The board side of this sheet drives pin 11 from decoder U3B output Q0 through R15 and SCR Q7, like
its eleven siblings, but prints no function against it, while the pins it calls unused (10 and 13
to 16) are marked `N/U`. The harness side settles what that blank means: the cable has a branch on
exactly the eleven pins that print a function, and none on pin 11. The circuit is built on the
board and nothing is plugged onto it, so public lamp 113 drives no load.

The colour codes read as Bally's two-digit scheme, base colour then tracer, with 0 for none, 1 red,
2 blue, 3 yellow, 4 green, 5 white, 6 brown, 7 orange, 8 black and 9 gray: PinWiki's Centaur lamp
chart pairs every one of these eleven codes with that colour pair.
