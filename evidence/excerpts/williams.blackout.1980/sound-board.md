# Williams Blackout (game 495) - Sound board miniature switches DS1

Sources:

- Instruction Manual and Drawing Set (`Williams_1980_Blackout_Manual_with_paginated_schematics.pdf`), PDF page 13 / printed 15/16, `Sound Board Logic Diagram`, title block `SCHEMATIC, SOUND BOARD`, drawing `16D-8224`. The region read runs from DS1 at the lower left of the sheet to the port B pins of the 6821 IC10 at the top; the crop `sound-board-ds1.webp` beside this file shows it.
- Pinned PinMAME `src/wpc/wmssnd.c` and `src/wpc/s6.h` at `46e1a01a0f73dc5ce163d98db1ae435883ecc450`, for how the emulator presents the two switches.

## The drawing

DS1 is drawn as a two-position switch block labelled `DS1`, its positions printed `2` (upper) and `1` (lower), with `OFF` on the left and an arrow to `ON` on the right. One side of both contacts is joined and drawn to ground; the switches are drawn open.

| DS1 position | Line from the switch | Series part | Capacitor to ground | Route | IC10 pin |
|---|---|---|---|---|---|
| 2 | joined by one 4.7K resistor of the `SR1` pack (`ALL 4.7 K`) to the supply | `R2` `100` | `C2` `470 PFD.` | through jumper pad pair `W9`, whose far pad is linked to the far pad of `W4`; `W4`'s near pad is the output (pin 4) of the `IC7` `14069` inverter fed from the sound/speech select input | `15` `PB5` |
| 1 | joined by another `SR1` 4.7K resistor to the supply | `R4` `100` | `C4` `470 PFD.` | runs straight up the sheet | `16` `PB6` |

Each line was followed from the switch to the IC10 pin on the page image; neither crosses onto another line on the way. Neither jumper pad pair is drawn as fitted or omitted for this game; the sheet draws both pairs.

Reading: a switch set ON grounds its line, so the IC10 port B input reads 0; set OFF, the pull-up makes it read 1.

## The printed adjustments

The drawing set's Electrical Adjustments (`game-operation.md`): `Set miniature switch 2 to ON to enable speech; set it to OFF to inhibit speech.` and `Set switch 1 to OFF to select synthesized sounds, set it to ON to select musical notes.`

## How PinMAME presents them

- `s6.h` `S6_COMPORTS`, port 1: `Sound Dip 1` is mask `0x0001` (default `0x0000`) and `Sound Dip 2` is mask `0x0002` (default `0x0002`). The record's public DIP 1 and 2 are these two bits.
- `s6.c` initializes the sound board as `SNDBRD_S67S` with subtype 0, so `wmssnd.c` `s67s_cmd_w` takes its final branch: `s67slocals.sndCmd = (data & 0x1f) | (core_getDip(0)<<5);`, which is read back on the sound PIA's port B. Public DIP 1 is therefore PB5 and public DIP 2 is PB6, with no inversion.

Putting the two together:

| Public DIP | IC10 pin | DS1 position | Public 0 | Public 1 | PinMAME default |
|---|---|---|---|---|---|
| 1 | PB5 | 2 | ON: speech enabled | OFF: speech inhibited | 0, speech enabled |
| 2 | PB6 | 1 | ON: musical notes | OFF: synthesized sounds | 1, synthesized sounds |
