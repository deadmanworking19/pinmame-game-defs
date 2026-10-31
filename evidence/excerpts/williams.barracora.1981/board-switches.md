# Williams Barracora (game 510) - Switches on the CPU and sound boards

Source: `Williams_1981_Barracora_Instruction_and_Drawing_Set_paginated_schematics_cover_page_missing.pdf`:

- PDF page 12 = printed page `16`, caption `Sound Board Assembly Drawing`, title block `SOUND BOARD SUB-ASSEM`, drawing `D-8223`.
- PDF page 5 = printed page `8`, caption `CPU Board Assembly Drawing` (its bill of material and its assembly view).

Method: the pages' native images (2552 x 1651) were cropped, rotated and read visually. Scope is deliberately narrow and stated below; nothing outside it is transcribed or asserted.

## Sound board bill of material, last two items (PDF page 12)

Only the two switch rows are transcribed. Items 1-45 (ICs, resistors, capacitors) are not transcribed and no assertion uses them. The part-number column of these two rows was not read with confidence at the scan's resolution and is left out.

| ITEM | PART DESIGNATION | DESCRIPTION | REQ'D |
|---|---|---|---|
| 46 | SW1 | MOMENTARY SWITCH SPDT | 1 |
| 47 | DS1 | 2 STD. DIP SWITCH | 1 |

The same sheet carries strapping notes that list jumper settings for many Williams games by name (among them World Cup, Disco Fever, Contact, Flash, Stellar Wars, Tri Zone and Time Warp). The drawing is the generic System 6/7 sound board drawing bound into this set, not a Barracora-specific sheet; Barracora's own jumper requirement is in the drawing set foreword (`cabinet-and-power.md`).

## CPU board assembly drawing (PDF page 5)

Read labels, as printed:

- A test-point inset: `TP1 +12V. UNREG.` and `TP2 NMI`, with a waveform labelled `DIAGNOSTIC SWITCH DEPRESSED` (`0V` / `+5V`).
- Connector `1J4`, labelled `MEM. PROT. & DIAGNOSTIC SW.` (the cabinet sheet gives its pins: MEM. PROT., GROUND, ADVANCE and AUTO./MAN.; `cabinet-and-power.md`).
- A board region labelled `COIN DOOR DIAGNOSTIC SWITCHES`.

### CPU board bill of material, switch rows only (PDF page 5)

The bill of material is printed sideways at the lower right of the sheet; it was cropped from the native image and rotated upright. Only its switch rows are transcribed; the other rows (ICs, resistors, capacitors, diodes, transistors) are not, and no assertion uses them. The note that row 55 refers to was not read.

| ITEM NO. | PART NO. | PART DESIGNATION | DESCRIPTION | REQ'D NO. |
|---|---|---|---|---|
| 24 | 5645-09025-00 | DS1,DS2 | 8 STD DIP SWITCHES | 2 |
| 55 | SEE NOTE | (blank) | SWITCH MOMENTARY | 2 |

### CPU board assembly view (PDF page 5)

The assembly view on the same sheet was inspected for the parts these rows list: the whole board at half the native resolution, and at native resolution the region labelled `COIN DOOR DIAGNOSTIC SWITCHES` (which holds R44, R45, C36, C37 and C86, the input parts for the coin-door switches) and the `BCD OUPUTS` region beside it (printed so; IC28 and IC29). No part labelled DS1 or DS2 and no DIP-switch bank was found. The only switch drawn on the board is the pushbutton labelled `DIAGNOSTIC SWITCH` beside IC24; the second momentary switch that row 55 counts is not drawn. The bill of material and the assembly view of this one drawing therefore disagree, and this record does not settle whether any production board carried DS1, DS2 or a second pushbutton.

## Notes

- PinMAME's `S7_COMPORTS` (`src/wpc/s7.h`) names `Sound Dip 1`, `Sound Dip 2` and a `Sound Diagnostic` button, and `src/wpc/wmssnd.c` folds the two sound DIP bits into the command byte the sound CPU reads. DS1 (2 positions) and SW1 (momentary) above are the physical parts these correspond to.
- The CPU board's diagnostic switch drives the NMI line, which PinMAME publishes as `CPU Diagnostic` (-5).
- PinMAME's `s7_dips_r` returns two 8-bit banks (its F1-F8 and D1-D8, public DIP 9-24) only while `Master Command Enter` (-3) is held. The BOM's two 8-position banks DS1 and DS2 are the parts those bits would read; the instruction booklet's adjustment procedure uses the coin-door ADVANCE and AUTO-UP/MANUAL-DOWN switches and never mentions CPU DIP switches.
