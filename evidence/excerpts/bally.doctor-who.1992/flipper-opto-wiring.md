# Doctor Who — Flipper opto boards and Fliptronic II flipper wiring

Transcribed from `Bally_1992_Doctor_Who_Manual.pdf`, PDF pages 132-134, printed pages `DOCTOR WHO 3-9`, `3-10`
and `3-11` (`Flipper Opto Switch Board A-15894`, `FLIPTRONIC II FLIPPER END-OF-STROKE SWITCHES`,
`FLIPTRONIC II FLIPPER CABINET SWITCH CIRCUIT DIAGRAM`, `FLIPTRONIC II FLIPPER CIRCUITS`, `FLIPTRONIC II FLIPPER
CIRCUIT DIAGRAM`). Read from the rendered pages (300 dpi image-only scans), not from the OCR text.

## Flipper Opto Switch Board A-15894 (printed 3-9)

Left Side Flipper Opto Switch Board: J1-1 Blue-Gray (lower flipper) from Fliptronic II Board J905-2; J1-2
Black-Blue (upper flipper) from Fliptronic II Board J905-5; J1-3 Orange (Switch Grd) from Fliptronic II
Board J905-6; J1-4 Orange (Switch Grd) loop from J1-3; J1-5 Key; J1-6 Gray-Yellow (+12V) from Power Driver
Board J116-2; J1-7 Gray-Yellow (+12V) loop from J1-6.

Right Side Flipper Opto Switch Board: J1-1 Blue-Violet (lower flipper) from Fliptronic II Board J905-1;
J1-2 Black-Yellow (upper flipper) from Fliptronic II Board J905-3; J1-3 Orange ((Switch Grd) loop from Left
Side Board J1-4; J1-4 N/C; J1-5 Key; J1-6 Gray-Yellow (+12V) from Power Driver Board J116-2; J1-7
Gray-Yellow (+12V) loop from J1-6.

"Please Note: The Left Flipper Opto Switch Board must be connected in order for the Right Flipper Opto Switch
Board to operate because power and ground are connected though the printed circuit board."

The board drawing shows two optos on one board ("opto 1" and "opto 2", each an LED with a 470 ohm resistor
and a phototransistor, connector J1 pins 1-7 with +12VDC on 6, SW-1 on 1, SW-2 on 2, Key on 5, GND on 3/4).

## Flipper end-of-stroke switches (printed 3-9)

Fliptronic II Board connector J906: pin 1 `(U4A-5) Black-Green F1`, pin 4 `(U6A-5) Black-Violet F5`, pin 3
`(U4C-9) Black-Blue F3`, pin 5 `(U6C-9) Black-Gray F7`, pin 6 `Orange` (ground). Legend: F1 Lower Right
Flipper, F5 Upper Right Flipper, F3 Lower Left Flipper, F7 Upper Left Flipper. Text: "The flipper switch
circuits operate similar to the dedicated switch circuit. The circuits are active low and tied to ground
through the switch."

## Flipper cabinet switch circuit diagram (printed 3-10)

Left Flipper Opto Switch Board J1 carries `Blue-Gray L. Left Flipper F4` and `Black-Blue U. Left Flipper F8`;
Right Flipper Opto Switch Board J1 carries `Blue-Violet L. Right Flipper F2` and `Black-Yellow U. Right
Flipper F6`; both are fed `Gray-Yellow +12V` from Power Driver Board J116-2 and `Orange Ground`. The Fliptronic
II Board J905 side prints `(U4B-7) Blue-Violet F2`, `(U6B-7) Black-Yellow F6`, `(U4D-11) Blue-Gray F4` and
`(U6D-11) Black-Blue F8`, with J905 pins 1, 3, 2, 5 and ground 6. Legend: F2 Lower Right Flipper, F6 Upper
Right Flipper, F4 Lower Left Flipper, F8 Upper Left Flipper.

## Fliptronic II flipper circuits (printed 3-11)

- Left Flipper Circuit (Fliptronic II Board J901 / J902 / J906 / J907): the supply is printed `Gray-Yellow` at
  the J907 connector; the lower left flipper is driven by `Blue-Gray Power` (J902-9) and `Orange-Blue Holding`
  (J902-7), the upper left flipper by `Black-Blue Power` (J902-3) and `Orange-Gray Holding` (J902-1); the end-of-
  stroke switches are `Black-Blue Lower Left End-of-Stroke Switch` (J906-3) and `Black-Gray Upper Left
  End-of-Stroke Switch` (J906-5), each with an `Orange` ground return.
- Right Flipper Circuit: the supply is printed `Blue-Yellow` at the J907 connector; the lower right flipper is
  drawn driven by `Blue-Violet Power` (J902-13) and `Orange-Green Holding` (J902-11), the upper right flipper
  by `Black-Yellow Power` (J902-6) and `Orange-Violet Holding` (J902-4); the end-of-stroke switches are
  `Black-Green Lower Right End-of-Stroke Switch` (J906-1) and `Black-Violet Upper Right End-of-Stroke Switch`
  (J906-4).
- The circuit diagram below them draws `J907`, `J906`, `J905`, `J902`, `J901` and `J904` of the Fliptronic II
  Board with the cabinet, the CPU board (`J202` to `J903`) and the Power Driver Board (`J114`, `J105`,
  `J116`): `Gray-Yellow +50Vdc` and `Blue-Yellow +50Vdc` supply the coils, `White-Blue 50Vac` feeds J901,
  and the end-of-stroke switches F7, F3, F5 and F1 are drawn on J906 pins 5, 3, 4 and 1.

The Fliptronic circuit pages are generic board pages: they draw both an upper-right and an upper-left
position (including F5/F6 and the upper-right coil circuit) whether or not the game populates them. The
game-specific pages (`switch-locations.md`, `solenoid-flasher-locations.md`, `solenoid-flasher-table.md`)
list an upper left flipper but no upper right flipper. The J902 pins and wire colours on the Fliptronic wiring
pages differ in places from the Solenoid/Flasher Table's flipper rows and from the Handy Technician's Chart;
see `solenoid-flasher-table.md`.
