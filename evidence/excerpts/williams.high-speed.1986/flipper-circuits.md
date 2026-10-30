# High Speed — Flipper circuits on the Power Wiring Diagram

Transcribed from `high_speed_instruction_manual.pdf`, PDF page 80 (printed page 46, Section 3), the left
half of the **Power Wiring Diagram** whose right half is PDF page 81 (printed page 47). Read from the
page's native 300 dpi scan rendered with `pdftoppm -r 300`. The accompanying crop
`flipper-circuits.webp` is the lower-left quarter of the sheet: the `C-9939 FLIPPER POWER SUPPLY` box,
its `8P4`/`8J4` feed, the three flipper circuits and their returns to `1P19`, and the start of the hideout
relay circuit to their right. The fact transcribed here is a drawing (which button contact the third
flipper coil runs through), so the crop is kept.

## The three flipper circuits, traced left to right

Each circuit is drawn as a coil with a parallel diode and an `E.O.S` switch across part of the winding,
then a wire down through two playfield connectors and two cabinet connectors to a `FLIPPER BUTTON`
contact, and back up to the CPU board's `1P19`. Every connector is printed `P/O` (part of).

| Coil label as printed | Coil-side wire | Playfield connector | Cabinet connector | Button contact | Return wire | Return connector | CPU board |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `UPPER RIGHT FLIPPER` | `BLK-YEL` | `P/O 8J3` / `P/O 8P3` pin `33` | `P/O 7P1` / `P/O 7J1` pin `19` | a `FLIPPER BUTTON` contact drawn on its own, with no capacitor | `ORG-VIO`, which joins the right flipper's return node | (the right flipper's) `P/O 7J1` / `P/O 7P1` pin `20` | (the right flipper's) `1P19` pin `1` |
| `RIGHT FLIPPER` | `BLU-VIO` | `P/O 8J3` / `P/O 8P3` pin `34` | `P/O 7P1` / `P/O 7J1` pin `21` | `FLIPPER BUTTON` contact with a `.1uf` `500V` capacitor across it | `ORG-VIO` | `P/O 7J1` / `P/O 7P1` pin `20` | `1P19` pin `1` |
| `LEFT FLIPPER` | `BLU-GRY` | `P/O 8J3` / `P/O 8P3` pin `32` | `P/O 7P1` / `P/O 7J1` pin `25` | `FLIPPER BUTTON` contact with a capacitor across it, no value printed | `ORG-GRY` | `P/O 7J1` / `P/O 7P1` pin `23` | `1P19` pin `2` |

The connector cell order is the page's own: the playfield pair is printed `P/O 8J3` above the pin
number and `P/O 8P3` below it, and the cabinet pair `P/O 7P1` above and `P/O 7J1` below; on the return
side `P/O 7J1` is above the pin number and `P/O 7P1` below.

**The upper-right flipper's button contact.** The `FLIPPER BUTTON` contact in the upper-right flipper's
circuit and the one in the right flipper's circuit are joined by a dashed line drawn between their
actuators, and the label `FLIPPER BUTTON` is printed once, on that dashed line, between them. A dashed
line between two contacts is a mechanical link: both are contacts of one button. The other side of the
upper-right flipper's contact runs on an `ORG-VIO` wire to a junction dot on the right flipper's return
line, below its capacitor and above `P/O 7J1` pin `20`. So the right cabinet flipper button closes both
coils' circuits at once, through two contacts of its own, and both return on the right flipper's
`ORG-VIO` wire to `1P19-1`. The left button has one contact and fires only the left flipper.

## The coil supply

`C-9939 FLIPPER POWER SUPPLY` brings out `15J3`/`15P3` pins `1` and `2` (joined) on `BLU-YEL`, pin `5`
through a `2.5ASB` fuse on `VIO-YEL`, and pin `6` on `GRY-YEL`, into `P/O 8P4` / `P/O 8J4` pins `7`, `9`
and `8` (printed in that order under the connector). `BLU-YEL` feeds a common bus across the top of the
right flipper and upper-right flipper coils, `GRY-YEL` the left flipper coil, and `VIO-YEL` runs right to
the `LEFT HIDEOUT RELAY` circuit. No CPU-driven transistor appears in any flipper circuit: the coils are
fed from the flipper supply and switched by the cabinet buttons alone.

## What this settles

The Solenoid Table (printed page 25) and the Solenoids/Flashers list (printed page 34) name an "Upper
Flipper" coil with only its playfield connector pins, `7J1-19` and `8P3-33`, and never a side or a
button. This sheet draws that coil as `UPPER RIGHT FLIPPER` on the same pins and wire colour and wires
it through a second contact of the right flipper button.
