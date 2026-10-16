# Corvette — Solenoid, Flasher and Related Wiring Pages (PDF 120-124)

Source: Bally "Corvette" (1994) service manual, PDF pages 120-124 (printed 3-6 to 3-10), transcribed from the 300 dpi grayscale renders `rendered-300/m-120.png` to `m-124.png`. Method: manual visual transcription of magnified crops (crops in `scratch/solenoid/`: `w120*.png`, `w121*.png`, `c122*.png`, `c123*.png`, `c124*.png`); not OCR. Drawing text is transcribed literally (including hyphens as printed, e.g. `Red-Violet`, and `Gray` / `Violet` / `Yellow` spelled out as on these drawings, which differ from the abbreviations in the PDF 110 table). Wire routing was traced by eye on the drawings; where a statement is an interpretation of line routing it is marked "traced".

---

## PDF 120 (printed 3-6): SOLENOID WIRING

Title: `SOLENOID WIRING`. Printed page number: `3-6`. The drawing shows a Fliptronic II Board block (top) and a Power Driver Board block (below), connector pin lists with wire names, and a box for each solenoid ("Function / Sol NN").

### Fliptronic II Board block (label printed `Fliptronic II` / `Board`)

| Connector | Pin | Wire label (as printed) | Voltage label | Goes to |
| --- | --- | --- | --- | --- |
| J907 | 6,7 | Red-Violet | +50VDC | Common top rail of Diverter Power Sol 33 and Diverter Hold Sol 34 (traced) |
| J902 | 6 | Yellow-Violet | (none) | Diverter Power, Sol 33 (traced) |
| J902 | 4 | Orange-Violet | (none) | Diverter Hold, Sol 34 (traced) |

Boxes: `Diverter Power / Sol 33`, `Diverter Hold / Sol 34`.

### Power Driver Board block (label printed `Power` / `Driver` / `Board`, beside J127)

Supply connector pins (voltage rails):

| Connector | Pin | Wire label (as printed) | Voltage label | Goes to (traced) |
| --- | --- | --- | --- | --- |
| J107 | 2 | Red-Brown | +50VDC | Outermost bus: common rail of the lower solenoid bank, Sol 01-08 |
| J107 | 3 | Red-Black | +50VDC | Second bus: common rail of the middle bank, Sol 09-16 |
| J107 | 6 | Red-White | +20VDC | Third bus: common rail of Race Direction / Left Race Enable / Right Race Enable, Sol 17, 18, 19 |

(The J107 pin numbers are printed as two stacked pins `2` and `3` in one box, and a separate box `6`.)

Motor drive board block: box labelled `A-18533` / `Motor Drive` / `Slave Board`.

| Connector | Pin | Wire label | Goes to (traced) |
| --- | --- | --- | --- |
| J126 | 1 | Black-Brown | into the left side of the A-18533 Motor Drive Slave Board |
| J126 | 2 | Black-Red | into the left side of the A-18533 board |
| J126 | 3 | Black-Orange | into the left side of the A-18533 board |

Three outputs leave the right side of the A-18533 board: top output to `Race Direction Sol 17`, middle output to `Left Race Enable Sol 18`, bottom output to `Right Race Enable Sol 19` (traced; the output lines carry no printed wire labels). Boxes: `Race Direction / Sol 17`, `Left Race Enable / Sol 18`, `Right Race Enable / Sol 19`.

J127 (pins printed 1, 3, 4, 5, 6, 7, 8, 9 — there is no pin 2 printed), middle bank (low power), with the box each wire reaches (traced):

| J127 pin | Wire label | Solenoid box |
| --- | --- | --- |
| 1 | Brown-Black | Left Slingshot, Sol 09 |
| 3 | Brown-Red | Right Slingshot, Sol 10 |
| 4 | Brown-Orange | Left Jet, Sol 11 |
| 5 | Brown-Yellow | Bottom Jet, Sol 12 |
| 6 | Brown-Green | Right Jet, Sol 13 |
| 7 | Not Used | Not Used, Sol 14 |
| 8 | Brown-Violet | ZR-1 Lockup, Sol 15 |
| 9 | Brown-Gray | Loop Gate, Sol 16 |

J130 (pins printed 1, 2, 4, 5, 6, 7, 8, 9 — there is no pin 3 printed), lower bank (high power):

| J130 pin | Wire label | Solenoid box |
| --- | --- | --- |
| 1 | Violet-Brown | Trough Eject, Sol 01 |
| 2 | Violet-Red | ZR-1 Low Rev Gate, Sol 02 |
| 4 | Violet-Orange | Kickback, Sol 03 |
| 5 | Violet-Yellow | Pit Stop Popper, Sol 04 |
| 6 | Violet-Green | ZR-1 Up Rev Gate, Sol 05 |
| 7 | Not Used | Not Used, Sol 06 |
| 8 | Violet-Black | Knocker, Sol 07 |
| 9 | Violet-Gray | Route 66 Kickout, Sol 08 |

Solenoid box labels as printed (each box: function line(s) then `Sol NN`): `Left Slingshot Sol 09`, `Right Slingshot Sol 10`, `Left Jet Sol 11`, `Bottom Jet Sol 12`, `Right Jet Sol 13`, `Not Used Sol 14`, `ZR-1 Lockup Sol 15`, `Loop Gate Sol 16`; `Trough Eject Sol 01`, `ZR-1 Low Rev Gate Sol 02`, `Kickback Sol 03`, `Pit Stop Popper Sol 04`, `ZR-1 Up Rev Gate Sol 05`, `Not Used Sol 06`, `Knocker Sol 07`, `Route 66 Kickout Sol 08`. Each bank's solenoid boxes are joined on a common top rail with a junction dot above every box (the common rail runs to the +50VDC bus described above).

No explanatory prose is printed on this page.

---

## PDF 121 (printed 3-7): FLASHER WIRING

Title: `FLASHER WIRING`. Printed page number: `3-7`. A vertical Power Driver Board edge (label printed `POWER` / `DRIVER` / `BOARD`, beside J125) at the left; flasher boxes to the right; a horizontal dashed line divides the upper half (label `INSERT FLASHERS`) from the lower half (label `PLAYFIELD FLASHERS`).

Supply wires:

| Connector | Pin | Wire label | Voltage label | Goes to (traced) |
| --- | --- | --- | --- | --- |
| J107 | 6 | Red-White | +20VDC | Outer rail running down the right side of the page, crossing the dashed line, to the common rails of the PLAYFIELD FLASHERS (Sol 25-28 row and Sol 21-24 row) |
| J106 | 5 | Red-White | +20VDC | Inner rail to the common rails of the INSERT FLASHERS (Sol 25-28 row and Sol 20, 22, 23, 24 row) |

INSERT FLASHERS (above dashed line) — first row, driven from J124 (J124 pins printed 1, 2, 3, 5):

| J124 pin | Wire label | Flasher box |
| --- | --- | --- |
| 1 | Blue-Brown | ZR-1 Ramp, Sol 25 |
| 2 | Blue-Red | ZR-1 Underside, Sol 26 |
| 3 | Blue-Orange | Right Rear Panel, Sol 27 |
| 5 | Blue-Yellow | Right Standup, Sol 28 |

INSERT FLASHERS — second row, driven from J125 (J125 pins printed 5, 7, 8, 9):

| J125 pin | Wire label | Flasher box |
| --- | --- | --- |
| 5 | Blue-Yellow | Tenth Corvette, Sol 20 |
| 7 | Blue-Black | Right Ramps, Sol 22 |
| 8 | Blue-Violet | Upper Left Flipper, Sol 23 |
| 9 | Blue-Gray | Catch Me, Sol 24 |

PLAYFIELD FLASHERS (below dashed line) — first row, driven from J122 (J122 pins printed 1, 2, 3, 4):

| J122 pin | Wire label | Flasher box |
| --- | --- | --- |
| 1 | Blue-Brown | ZR-1 Ramp, Sol 25 |
| 2 | Blue-Red | ZR-1 Underside, Sol 26 |
| 3 | Blue-Orange | Right Rear Panel, Sol 27 |
| 4 | Blue-Yellow | Right Standup, Sol 28 |

PLAYFIELD FLASHERS — second row, driven from J126 (J126 pins printed 5, 6, 7, 8):

| J126 pin | Wire label | Flasher box |
| --- | --- | --- |
| 5 | Blue-Green | Jets, Sol 21 |
| 6 | Blue-Black | Right Ramps, Sol 22 |
| 7 | Blue-Violet | Upper Left Flipper, Sol 23 |
| 8 | Blue-Gray | Catch Me, Sol 24 |

Box labels as printed: `ZR-1 Ramp Sol 25`, `ZR-1 Underside Sol 26`, `Right Rear Panel Sol 27`, `Right Standup Sol 28`, `Tenth Corvette Sol 20`, `Right Ramps Sol 22`, `Upper Left Flipper Sol 23`, `Catch Me Sol 24`, `Jets Sol 21`. Solenoids 25-28, 22, 23 and 24 each appear twice, once in the insert half and once in the playfield half; Sol 20 (Tenth Corvette) appears only in the insert half and Sol 21 (Jets) only in the playfield half.

No explanatory prose is printed on this page.

---

## PDF 122 (printed 3-8): High Power Solenoid Circuit and Low Power Solenoid Circuit

Printed page number: `3-8`. Two schematics, each inside a dashed box labelled `POWER DRIVER BOARD`.

### High Power Solenoid Circuit (heading, bold underlined: `High Power Solenoid Circuit`)

Labels and parts as printed:
- Block labels: `DRIVE`, `VCC`, `+50V`, `POWER`.
- Connector `J113` (single pin marked `X`) into a block labelled `LS374`; its output node is labelled `A`.
- `470Ω` series resistor from `A`; `4.7KΩ` resistor from `VCC` to the node between the 470Ω and the base of transistor `2N5401` (the 2N5401's emitter is tied to `VCC`); the 2N5401 collector node is labelled `B`.
- From `B`: `68Ω` series resistor to the base of `TIP102` (Darlington pair, drawn as two transistors); `2.7KΩ` resistor from that base node to ground; TIP102 emitter to ground. The TIP102 collector node is labelled `C`.
- `220Ω` resistor from `C` up to the node below the `1N4004` diode, whose other end goes to `+50V`; that node also goes to the emitter of transistor `TIP36C` (PNP), whose base is the node `C`; the TIP36C collector node (to the output) is labelled `D`.
- `D` goes to connector `J130` (pin marked `X`), then the wire label `Violet-XXX`, then the coil (inductor symbol). Text beside it: `Playfield or Backbox Coil`.
- The coil's other end returns on wire label `Red-Brown` to connector `J107` (pin marked `X`).
- Power section (`J102` connector, label `POWER`): `J102` pins `9`, `8`, `6`, `5`; pins 9 and 8 are tied together and go through fuse `F112` to one AC input of bridge `BR3`; pins 6 and 5 are tied together and go to the other AC input of `BR3`. BR3 `-` to ground; BR3 `+` to a `100µf 50V` capacitor to ground and a `10KΩ` resistor to ground, then fuse `F105` to `J107` (pin `X`, wire `Red-Brown`).

Printed explanatory text (quoted literally):

> The microprocessor toggles the output of the 74LS374.  When point "A" drops low, point "B" the collector of the 2N5401 transistor is high.  A high at point "B" causes point "C" the collector of the TIP102 transistor, and point "D" the emitter of the TIP36 transistor to drop low.  When point "D" is low the coil is grounded through the transistor and the coil turns On.  The coil shuts Off when point "A" toggles high.

### Low Power Solenoid Circuit (heading, bold underlined: `Low Power Solenoid Circuit`)

Labels and parts as printed:
- Block labels: `DRIVE`, `VCC`, `+50V`, `POWER`.
- Same input stage as above: `J113` (`X`) to `LS374`, point `A`, `470Ω`, `4.7KΩ` to `VCC`, `2N5401`, point `B`, `68Ω`, `2.7KΩ` to ground, `TIP102` (emitter to ground).
- The TIP102 collector node is labelled `C`; the `1N4004` diode connects node `C` to `+50V`; no 220Ω and no TIP36C are present in this circuit.
- `C` goes to connector `J127` (pin `X`), then the wire label `Brown-XXX`, then the coil. Text beside it: `Playfield or Backbox Coil`.
- The coil's other end returns on wire label `Red-Black` to connector `J107` (pin `X`).
- Power section: `J102` pins `9`, `8`, `6`, `5` wired as above (9+8 through `F112`, 6+5 direct) to bridge `BR3`; `BR3 +` to `100µf 50V` capacitor and `10KΩ` to ground, then fuse `F104` to `J107` (wire `Red-Black`).

Printed explanatory text (quoted literally):

> The microprocessor toggles the output of the 74LS374.  When point "A" is low, point "B" the collector of the 2N5401 transistor is driven high.  A high at point "B" turns On the TIP102 transistor, and causes point "C" to drop low.  When point "C" is low the coil is grounded through the transistor and the coil turns On.  The coil shuts Off when point "A" toggles high.

---

## PDF 123 (printed 3-9): Flashlamp Circuit and Special (General Purpose) Solenoid Circuit

Printed page number: `3-9`.

### Flashlamp Circuit (heading, bold underlined: `Flashlamp Circuit`)

Inside a dashed box `POWER DRIVER BOARD`:
- Block labels: `DRIVE`, `VCC`, `POWER`.
- Input stage as above: `J113` (`X`) to `LS374`, point `A`, `470Ω`, `4.7KΩ` to `VCC`, `2N5401`, point `B`, `68Ω`, `2.7KΩ` to ground, `TIP102` (emitter to ground), collector node `C`.
- `C` goes to connector `J125` (pin `X`), then text `Flashlamp` and wire label `Black-XXX`, then a lamp symbol (circle with filament).
- The lamp's other end returns on wire label `Red-White` to connector `J107` (pin `X`).
- Power section: connector `J102` pins `3`, `4`, `1`, `2`; pins 3 and 4 tied and go through fuse `F111` to one AC input of bridge `BR3`; pins 1 and 2 tied and go to the other AC input. `BR3 +` to a `15,000µf` capacitor to ground and, in parallel, an LED symbol in series with a `1.5KΩ` resistor to ground, then directly to `J107` (no fuse is printed in this branch).

Printed explanatory text (quoted literally):

> The microprocessor toggles the output of the 74LS374.  When point "A" is low, point "B" the collector of the 2N5401 transistor is high.  Once point "B" is high, point "C" the collector of the TIP102 transistor is low.  When point "C" is low the flashlamp is grounded through the transistor and the flashlamp turns On.  When point "A" toggles high the circuit shuts Off.

### Special (General Purpose) Solenoid Circuit (heading, bold underlined: `Special (General Purpose) Solenoid Circuit`)

Inside a dashed box `POWER DRIVER BOARD`:
- Block labels: `DRIVE`, `VCC`, `POWER`.
- Input stage as above (`J113` / `LS374` / `A` / `470Ω` / `4.7KΩ` / `2N5401` / `B` / `68Ω` / `2.7KΩ` / `TIP102`), collector node `C`.
- Connector `J121` is drawn as a tall connector with two pins marked `X`: the upper pin connects through a `1N4004` diode (labelled `1N4004`) to node `C`; the lower pin connects directly to node `C` (the output). Text beside the lower pin: `Flashlamp*` / `or Coil`, wire label `Blue-XXX`, then the coil symbol; a lamp symbol is drawn in a parallel bracket to the right of the coil (alternative load).
- The load's return wire is labelled `Red-White`, going to connector `J107` (pin `X`); a vertical line from this Red-White node also runs up to the upper `J121` pin (the diode's far end) — the tieback path.
- Power section: `J102` pins `9`, `8`, `6`, `5` wired as in the solenoid circuits (9+8 through fuse `F112`, 6+5 direct) to `BR3`; `BR3 +` to `100µf 50V` capacitor and `10KΩ` to ground, then fuse `F103` to `J107` (wire `Red-White`).

Printed explanatory text (quoted literally):

> The microprocessor toggles the output of the 74LS374.  When point "A" drops low, point "B" is high.  A high at point "B" causes a low at point "C".  When point "C" is low the coil/flashlamp is grounded through the transistor and the coil/flashlamp turns On.  When point "A" toggles high the coil/flashlamp turns Off.
>
> *Tieback Diode is not used for flashlamp circuit.

---

## PDF 124 (printed 3-10): General Illumination Circuit and Block Diagram of General Illumination Circuit

Printed page number: `3-10`.

### General Illumination Circuit (heading, bold underlined: `General Illumination Circuit`)

Inside a dashed box `POWER DRIVER BOARD`:
- Block labels: `DRIVE`, `VCC`, `POWER`.
- `J113` (`X`) into `LS374`, point `A`; `560Ω` series resistor; `10K Ω` resistor from `VCC` to the node before the base of `2N5401` (emitter to `VCC`); collector node `B`; `51Ω` resistor to the triac gate, node labelled `C`.
- Triac (bidirectional thyristor symbol): gate at `C`; its upper main terminal goes to the upper pin (`X`) of connector `J120`; its lower main terminal goes down and left to the upper pin (`X`) of connector `J115`, which is also drawn to a ground symbol; the lower `J115` pin (`X`) goes through the fuse labelled `S.B.` to the lower `J120` pin (`X`) (traced).
- Connector `J115` (two pins marked `X`, label `POWER`) and `J120` (two pins marked `X`, one tall connector).
- Off-board: label `G.I. Lights` on the wire from the upper `J120` pin; three lamp symbols shown connected in parallel; the lower `J120` pin wire returns to the lamps.

Printed explanatory text, placed under the Block Diagram (quoted literally):

> When point "A" toggles low, then points "B" and "C" are high.  This turns On the triac and the desired general illumination string lights.

### Block Diagram of General Illumination Circuit (heading, bold underlined: `Block Diagram of General Illumination Circuit`)

Blocks and labels as printed:
- Transformer windings: `6.3 Volt Secondary` (upper) and `5 Volt Secondary` (lower), drawn with a shared core at the left.
- 6.3 V Secondary loop runs through a dashed block `Power Driver Board` containing a fuse symbol, then through a dashed block `Playfield or Backbox (up to 18 bulbs)` containing three lamp symbols in parallel, then through a dashed block `Power Driver Board` containing two boxes `Triac Drivers` and `LS374 Latch`, then back to the secondary (the loop returns along the lower line from `Triac Drivers`).
- 5 Volt Secondary feeds a box `Zero Cross Detection Circuit` / `Power Driver Board`; its output goes to a box `Microprocessor` / `CPU Board`; the CPU board's output goes up to the `LS374 Latch`, which connects to `Triac Drivers`.

---

## Uncertain readings

- The routing of the A-18533 Motor Drive Slave Board's three output lines to Sol 17, 18 and 19 (PDF 120) and the exact triac-terminal-to-J115/J120 routing on PDF 124 were traced by eye; the component and connector labels themselves were legible. Crops: `w120b.png`, `c124e.png`, `c124b.png`.
- On PDF 123's Special (General Purpose) circuit, the parallel lamp bracket beside the coil carries no printed label other than `Flashlamp*` / `or Coil` (crop `c123d.png`).
- No cell or label was unreadable.
