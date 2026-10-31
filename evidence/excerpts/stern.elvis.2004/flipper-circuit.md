# Elvis (Stern) — 4-Flipper Circuit Wiring Diagram

Read from `Elvis_Manual.pdf`, PDF page 123, printed `Section 5, Chapter 2, Page 106` ("Playfield Wiring"), from a
200 dpi render checked against the page's text layer. Italics and bold are the page's own.

## Dedicated switch wiring (CPU-Sound Board CN6, "DEDICATED SWITCH INPUTS (SWITCH TO GROUND)")

The drawing runs five wires from the CN6 header (pins numbered 1 2 3 4 6 7 … 12, pin 5 not wired) to five switches
whose other side joins a common `BLK (GROUND)` wire to `POWER OUT J16` pin 11 of the I/O Power Driver Board.

| Wire | CN6 pin | Switch label as printed | Contact as printed |
| --- | --- | --- | --- |
| GRY-BRN | 2 | LEFT FLIPPER IN CABINET DEDICATED SWITCH DS-1 | N.O. |
| GRY-RED | 3 | LEFT E.O.S. ON ASSY. DEDICATED SWITCH DS-2 | N.C. |
| GRY-ORG | 4 | RIGHT FLIPPER IN CABINET DEDICATED SWITCH DS-3 | N.O. |
| GRY-YEL | 6 | RIGHT E.O.S. ON ASSY. DEDICATED SWITCH DS-4 | N.C. |
| GRY-GRN | 7 | UPPER RIGHT FLIPPER IN CABINET DEDICATED SWITCH DS-5 | N.O. |

The CN6 pin of each wire is read from where its line lands on the drawn header. DS-5's top terminal is drawn as a filled
dot where the others are open circles. "NOTE: N.C. = Normally Closed / N.O. = Normally Open".

## Coil wiring (I/O Power Driver Board, partial view)

Four MOSFETs drawn as `Q13`, `Q14`, `Q15`, `Q16` and labelled "MOS FET STP20N10L" drive the `J9 HIGH CURRENT
SOLENOIDS` header (pins 9 8 7 6 used, pin 1 at the far end). `J10 VOLTAGE OUTPUTS` pins 1 and 2 feed the bus
"↕ RED-YEL 50V DC ↕". Each coil is fed through its own fuse.

| Coil label as printed | Coil | Coil wrap | Drive wire | Fuse as printed | Fuse-to-coil wire |
| --- | --- | --- | --- | --- | --- |
| LOWER RIGHT FLIPPER COIL | 22-900 | YELLOW | ORG-VIO | 3A SLO-BLO (Located under Playfield) | BLU-YEL |
| LOWER LEFT FLIPPER COIL | 22-900 | YELLOW | ORG-GRY | 3A SLO-BLO (Located under Playfield) | GRY-YEL |
| UPPER RIGHT FLIPPER COIL | 23-900 | GREEN | BLU-BLK | 3A SLO-BLO (Located under Playfield) | BLU-YEL |
| UPPER LEFT FLIPPER COIL | 23-900 | GREEN | BLU-GRN | 3A SLO-BLO (Located under Playfield) | GRY-YEL |

Each fuse's supply side is labelled "RED-YEL 50V DC". Note beside the fuses: "*The 3A 250v Slo-Blo Fuses are located
under the playfield NEAR the Flipper Assembly, see previous page for locations.*" The drawing does not print which
MOSFET drives which drive wire; the four drive lines leave the MOSFET drains as an unlabelled bundle.

## Printed text

> The Outside **LEFT FLIPPER BUTTON** located on the Cabinet operates both the Left Flipper & Upper Left Flipper (if
> used). The Outside **RIGHT FLIPPER BUTTON** located on the Cabinet operates both the Right Flipper & Upper Right
> Flipper (if used). **RIGHT BUTTON ONLY:** This switch is ***Double-stacked***. Pressing half-way down operates the
> Lower Right Flipper; pressing full down operates both the Lower Flipper & Upper Right Flipper(if used) simultaneously.
>
> ***Note on this Game:*** 4-Flippers are used (Lower & Upper Left, Lower & Upper Right).

"Technical Overview":

> Our ***Flipper System*** uses one supply voltage (50v DC) for both ***kick*** & ***hold***. Once the **Game CPU**
> detects a Flipper Cabinet Switch closure (during game play) it applies a 40*msec* pulse to the gate of the Flipper
> Drive Transistor (STP-20N10L). If it continues to detect a Flipper Cabinet Switch closure *(the player holding the
> button in)* it will continue to pulse the flipper drive transistor 1*msec* every 12*msecs* for the duration of the
> hold cycle.
>
> The **E.O.S.** (End-Of-Stroke) **Switch** serves the same function as before as it prevents foldback when the player
> has the flipper energized to capture balls. The **E.O.S. Switch** is a normally closed switch which opens
> approximately 1/16" when the flipper is energized. The **Game CPU** will detect a switch closure if the flipper bat is
> forced back by a high velocity shot or rebound on the playfield and will apply another 40*msec* pulse of 50v DC to
> the coil.
