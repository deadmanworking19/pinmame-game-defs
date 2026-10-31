# Williams The Flintstones (1994) — General illumination circuit

Source: Williams *The Flintstones* Operations Manual 16-50029-101 (July 1994), IPDB machine 888 file
`Williams_1994_The_Flintstones_English_Manual.pdf`. Read from the native 300 dpi renders; each section
names its page. Text is transcribed as printed; `[?]` marks a reading the scan leaves uncertain.

## GENERAL ILLUMINATION CIRCUIT, PDF page 124 (printed page 3-10)

Williams Electronics Games, Operations Manual 16-50029-101 (July 1994), "The Flintstones", PDF page 124, printed page 3-10. Title: "GENERAL ILLUMINATION CIRCUIT" (with a second diagram titled "BLOCK DIAGRAM OF GENERAL ILLUMINATION CIRCUIT"). The page holds two schematics and one paragraph of text; it contains no table, no per-string wire colours, no connector pin numbers per string and no string list.

### GENERAL ILLUMINATION CIRCUIT (schematic)

Dashed box label: `POWER DRIVER BOARD`. Sub-labels inside it: `Drive` (left part), `Power` (bottom part). Right of the box: `G.I. LIGHTS`.

Drive path, left to right:
- Connector `J113` (single pin marked X) -> `LS374` block -> point `A`
- `A` -> resistor `560Ω` -> node feeding the base of transistor `2N5401`; a `10KΩ` resistor from `VCC` to the same node
- Transistor `2N5401` emitter to `VCC`; collector/other lead is point `B`
- `B` -> resistor `51Ω` -> point `C` -> gate of the triac (drawn as a triac symbol)

Power / output path:
- Connector `J115`, upper pin (X) -> ground symbol and the triac's other terminal
- Connector `J115`, lower pin (X) -> fuse labelled `S.B.` -> connector `J120`, lower pin (X)
- Triac -> connector `J120`, upper pin (X)
- `J120` (two pins marked X: upper and lower) -> `G.I. LIGHTS` drawn as three bulbs in parallel

### Text below the schematic

"When point "A" toggles low, points "B" and "C" are high. This turns on the triac and the desired general illumination string lights."

### BLOCK DIAGRAM OF GENERAL ILLUMINATION CIRCUIT

Blocks as printed:
- `Playfield or Backbox` / `G.I. Lights:  Up to 18 bulbs per string.` (three bulbs in parallel drawn)
- `Power Driver Board` (left box) containing a fuse, fed from `6.3 volt secondary` (transformer winding)
- `Power Driver Board` (right box) containing `Triac Drivers` and `LS374 Latch`
- `Power Driver Board` (lower box) containing `Zero Cross Detection Circuit`, fed from `5 volt secondary`
- `CPU Board` containing `Microprocessor`

Connections: 6.3 volt secondary -> fuse -> G.I. bulbs (parallel) -> Triac Drivers -> back to 6.3 volt secondary. LS374 Latch -> Triac Drivers. Microprocessor -> LS374 Latch. Zero Cross Detection Circuit (5 volt secondary) -> Microprocessor.

Printed page number at the bottom: `3-10`

### Notes on apparent misprints

None observed.

### Uncertain readings

- Resistor between `B` and `C` is read as `51Ω`; the "5" and "1" are small and could conceivably be "5.1" or "5 1" [?] (best reading `51Ω`).
