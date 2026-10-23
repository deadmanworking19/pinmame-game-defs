Source: `Stern_1980_Big_Game_Schematics_And_Wiring_Diagrams_Hi_resolution.pdf` (IPDB machine 249), PDF page 5, drawing `12B-432-S-121`, `SOLENOID DRIVER VOLTAGE REGULATOR SCHEMATIC FOR BIG GAME` (stored sideways; read rotated a quarter turn clockwise at native resolution and at 1.3 times that). The continuous-output and flipper section at the upper right of the sheet.

Four `SE9302` drivers (marked `*`, substitute X44E198), each behind a `U4` pre-driver, take the PIA port-B high nibble from connector `J4`:

| J4 pin | Input, verbatim | Driver | Output, verbatim |
| ---: | --- | --- | --- |
| 8 | FLIPPER DISABLE PB6 [BLU-W] | Q15 | `FLIPPER ENABLE RELAY` coil (with `CR20 IN4004` across it), fed from `43VDC`, also brought out on `J3` pin 5 `TO A2J3-8 [Y-W]` |
| 11 | PB4 [Y-W] | Q17 | `J5` pin 7, the line continuing to the label `GEN. ILLUM. RELAY` |
| 10 | PB7 [Y-R] | Q18 | a vertical line to `J5` pin 3 `N/U`, `J2` pin 15 `N/U` and `J3` pin 9 `N/U` |
| 9 | PB5 [BLU-O] | Q19 | `J2` pin 8, labelled `COIN LO.` and `COIN LOCK-OUT [Y-W]` |

The flipper enable relay's contacts are drawn as a two-pole switch: the `LEFT FLIPPER SW.` pole joins `J2` pin 2 `To LEFT [BLU] FLIPPER BUTTON` to `J1` pin 8 `To LEFT FLIPPER COIL [G]`, and the `RIGHT FLIPPER SW.` pole joins `J2` pin 1 `To RIGHT [R] FLIPPER BUTTON` to `J1` pin 9 `TO RIGHT FLIPPER COIL [O]`.

The `GEN. ILLUM. RELAY` label is the only place in this game's documents where a general-illumination relay appears: the playfield wiring diagram feeds `GEN. ILLUM` from `A2J1-8 (W)` `6 VAC` to `A2J1-1 (R)` with nothing in between, the transformer schematic draws the general-illumination buses straight from the transformer, and neither the Solenoid Identification table (17 `OPEN`) nor the parts list names a relay.
