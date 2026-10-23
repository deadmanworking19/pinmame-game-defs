# Creature from the Black Lagoon — Flipper Opto Switch Board and end-of-stroke switches

Transcribed from `Creature_From_The_Black_Lagoon_OPS.pdf`, PDF page 120, printed page 3-16, "Flipper Opto Switch
Board A-15894" and "FLIPTRONIC II FLIPPER END-OF-STROKE SWITCHES". Read from the page's native 200 dpi scan.
Printed wording is kept, including the doubled parenthesis in the right board's J1-3 line; only line breaks were
normalized.

## Left Side Flipper Opto Switch Board

| Pin | Printed text |
| --- | --- |
| J1 - 1 | Blue-Gray (lower flipper) from Fliptronic II Board J905-2 |
| J1 - 2 | Black-Blue (upper flipper) from Fliptronic II Board J905-5 |
| J1 - 3 | Orange (Switch Grd) from Fliptronic II Board J906-6 |
| J1 - 4 | Orange (Switch Grd) loop from J1-3 |
| J1 - 5 | Key |
| J1 - 6 | Gray-Yellow (+12V) from Power Driver Board J116-2 |
| J1 - 7 | Gray-Yellow (+12V) loop from J1-6 |

## Right Side Flipper Opto Switch Board

| Pin | Printed text |
| --- | --- |
| J1 - 1 | Blue-Violet (lower flipper) from Fliptronic II Board J905-1 |
| J1 - 2 | Black-Yellow (upper flipper) from Fliptronic II Board J905-3 |
| J1 - 3 | Orange ((Switch Grd) loop from Left Side Opto Board J1 -4 |
| J1 - 4 | N/C |
| J1 - 5 | Key |
| J1 - 6 | Gray-Yellow (+12V) from Power Driver Board J116-2 |
| J1 - 7 | Gray-Yellow (+12V) loop from J1-6 |

"Please Note: The Left Flipper Opto Switch Board must be connected in order for the Right Flipper Opto Switch
Board to operate because power and gound are connected though the printed circuit board." (sic)

The board drawing beside the lists shows two optos, `opto 1` and `opto 2`, each an LED with a 470 Ω resistor (R1,
R2) and a phototransistor; opto 1's transistor drives `SW-1` (J1-1) and opto 2's drives `SW-2` (J1-2), with +12VDC
on J1-6 and GND on J1-3/J1-4.

## Fliptronic II Flipper End-of-Stroke Switches (same page)

The end-of-stroke drawing wires J906 as: pin 1 `(U4A-5) Black-Green F1`, pin 4 `(U6A-5) Black-Violet F5`, pin 3
`(U4C-9) Black-Blue F3`, pin 5 `(U6C-9) Black-Gray F7`, pin 6 `Orange`, with the key `F1 Lower Right Flipper`, `F5
Upper Right Flipper`, `F3 Lower Left Flipper`, `F7 Upper Left Flipper`, and this table, whose fourth column has
no heading:

| Switch | A | B | (no heading) |
| --- | --- | --- | --- |
| Open | H | H | Off |
| Closed | L | L | On |

The text below it reads: "The flipper switch circuits operate similar to the dedicated switch circuit. The
circuits are active low and tied to ground through the switch."

## Reading notes

- Each cabinet flipper button has one A-15894 board with two optos. The second opto (`SW-2`, J1-2, printed "upper
  flipper") of the left board is wired to J905-5 (F8, public 118) and of the right board to J905-3 (F6, public
  116); the Fliptronic II connector list (`fliptronic-ii-board.md`) prints the same two pins "to left/right flipper
  opto". The machine has no upper flipper, so these are the cabinet buttons' second beams.
- The end-of-stroke drawing is the generic Fliptronic II circuit (it draws F5 and F7 for flippers this machine does
  not have); the game's own connector list prints J906-4 (F5) Not Used.
