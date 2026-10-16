# Drawing excerpt — CPU board flipper relay K1

`reviewed: true`; read by the curator from the rendered crop and a 300 dpi render of the whole sheet on 2026-10-16
`source: Instruction Manual PDF page 24, printed folio 24, "SCHEMATIC, CPU SYS 9", sheet 1 of 3, part no. 16-8923`

Image: `cpu-flipper-relay.webp` beside this file (crop box and resolution in the source record's
`image_derivation`). Full-sheet render: `external:pinmame-manuals/by-machine/williams.sorcerer.1985/rendered-300/p-24.png`.

What the crop shows, as drawn:

- A dashed box labelled `K1` containing a relay coil and four contact pairs, annotated `RELAY SA-8994`.
- The coil's upper terminal goes straight to the supply rail; its lower terminal is the collector of transistor
  `Q86 2N4401`, whose emitter is grounded. Diode `D1 1N4001` and resistor `SR11-2 4.7K` each run from the supply
  rail to that collector node, in parallel with the coil, and `R34 10K` runs from the collector node to ground.
- Q86's base is driven from pin 10 of a `7402` NOR gate `U7`, with `R35 2.7K` pulling that node up to the supply.
- The contacts carry `SOLENOID GND` (to `2A1`) onto `1J19-1` (`FGR1`) and `1J19-2` (`FGR2`), the flipper-ground
  pins the backbox wiring sheet brackets as `18 AWG FLIPPER GND`.

Context outside the crop, from the same sheet: the six special-solenoid driver stages `Q75`/`Q77`/`Q79`/`Q81`/
`Q83`/`Q85` (outputs `1J19-7`, `-4`, `-3`, `-6`, `-8`, `-9`, labels `SS1D`-`SS6D`) are each gated by `7402`
NOR gates `U6`/`U7` from the same enable network as `U7`/`Q86`, with inputs `1J18-5`/`-3`/`-2`/`-4`/`-8`/`-9`
labelled `SS1T`-`SS6T`.

Also on this sheet, outside the crop: PIA `U5 6821` at address `2800` has its `PA7` line pulled up through
`SR14-10 4.7K` and tied to ground through jumper `W5`. The circuit-board paragraph on PDF page 6 reads `Only
jumpers W2, W5 through W7, W9 and W11 should be connected.`

The relay's printed part `SA-8994` corresponds to the `5580-08994-00` that the Solenoids parts list (PDF page
20) prints for item 8 `Flipper-Enable Relay`; the game's own solenoid table (PDF page 14) prints the same
part number for solenoid 08 `Flash Eyes (cabinet)`. The sheet does not name the PinMAME address of the K1
drive; the gameplay harness run shows public 23 asserting at game start and dropping on tilt, which is how
`s11.c` publishes the special-solenoid/flipper enable (`S11_GAMEONSOL`).
