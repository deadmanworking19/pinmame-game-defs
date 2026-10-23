# Creature from the Black Lagoon — Fliptronic II board connector list

Transcribed from `Creature_From_The_Black_Lagoon_OPS.pdf`, PDF page 123, printed page 3-19, "FLIPTRONIC II
BOARD A-15472". Read from the page's native 200 dpi scan; the OCR text layer was used only to find the page.
Every connector line is reproduced in printed order and printed spelling; only line breaks were normalized.

| Pin | Printed text |
| --- | --- |
| J901-1 | White-Blue, 50VAC loop from J105-1 |
| J901-2 | White-Blue, loop from J901-1 |
| J901-3 | White-Blue, 50VAC loop, from J105-2 |
| J901-4 | Key |
| J901-5 | White-Blue, loop from J901-3 |
| J902-1 | Orange-Gray, to insert flashers |
| J902-2 | Not Used |
| J902-3 | Black-Blue, to insert flashers |
| J902-4 | Orange-Violet, to insert flashers |
| J902-5 | Not Used |
| J902-6 | Black-Yellow, to insert flashers |
| J902-7 | Orange-Blue, holding to lower left flipper |
| J902-8 | Not Used |
| J902-9 | Blue-Gray, power to lower left flipper |
| J902-10 | Key |
| J902-11 | Orange-Green, holding to lower right flipper |
| J902-12 | Not Used |
| J902-13 | Blue-Violet, power to lower right flipper |
| J903 | Ribbon Cable, data to/from J202; J506; J601 |
| J904-1 | Gray, +5V from J114-4 |
| J904-2 | Gray-Green, +12V from J114-2 |
| J904-3 | Key |
| J904-4 | Black, Ground from J114-7 |
| J904-5 | Black, Ground from J114-5 |
| J905-1 | Blue-Violet, to right flipper opto |
| J905-2 | Blue-Gray, to left flipper opto |
| J905-3 | Black-Yellow, to right flipper opto |
| J905-4 | Key |
| J905-5 | Black-Blue, to left flipper opto |
| J905-6 | Orange, Switch Ground |
| J906-1 | Black-Green, to lower right end-of-stroke switch |
| J906-2 | Key |
| J906-3 | Black-Blue, to lower left end-of-stroke switch |
| J906-4 | Not Used |
| J906-5 | Black-Gray, to upper left end-of-stroke switch |
| J906-6 | Orange, Switch Ground |
| J907-1 | Blue-Yellow, +50V to lower right flipper |
| J907-2 | Blue-Yellow, loop from J907-1 |
| J907-3 | Key |
| J907-4 | Gray-Yellow, +50V to lower left flipper |
| J907-5 | Gray-Yellow, loop from J907-4 |
| J907-6 | Not Used |
| J907-7 | Not Used |
| J907-8 | Gray-Yellow, loop from J907-9 |
| J907-9 | Gray-Yellow, +50V to upper left flipper |

The P.C. Board Legend box on the same page prints `J1-J6 Coin Door Interface Board`, `J1xx Power Driver Board`,
`J2xx CPU Board`, `J5xx Audio Board`, `J6xx Dot Matrix Controller Board` and `J9xx Fliptronic II Board`.

## Reading notes

- J902 is the Fliptronic II drive header. Its four upper-flipper lines (J902-1, -3, -4, -6, which the generic
  Fliptronic II Flipper Circuits page 3-18 draws as upper-left holding/power and upper-right holding/power) are
  printed "to insert flashers". The ROM's T.5 flasher test pulses public solenoids 33, 34, 35 and 36 as
  `CREATURE FL. 1`-`4` and prints their drive wires BLK-YEL, ORN-VIO, BLK-BLU and ORN-GRY, which are J902-6, J902-4,
  J902-3 and J902-1 here (runtime evidence `evidence/runtime/wpc-fliptronic/creature-cftbl_l4-flasher-test.json`).
- J906-4 (F5, upper right end-of-stroke) is printed Not Used. J906-5 (F7) and J907-8/J907-9 still name an upper
  left flipper, but the machine has none: J902-1 and J902-3, that flipper's holding and power lines, go to the
  insert flashers, the Lower Playfield Parts list (2-39) and the Solenoid/Flasher Locations flipper table (2-43)
  list only the two lower flipper assemblies, and the ROM's T.12 flipper coil test steps only the two lower
  flippers' power and holding windings.
- J905-3 and J905-5 (F6 and F8) run to the cabinet flipper opto boards: see `flipper-opto-board.md`.
