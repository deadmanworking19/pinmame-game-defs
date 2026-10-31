# Williams The Flintstones (1994) — Motor EMI board and Boulder Machine circuit

Source: Williams *The Flintstones* Operations Manual 16-50029-101 (July 1994), IPDB machine 888 file
`Williams_1994_The_Flintstones_English_Manual.pdf`, PDF page 138, printed page 3-24. Read from the
native 300 dpi render. Labels are transcribed as printed.

## A-15542 Motor EMI Board Assembly

Board layout: `L1`, `R1`, `Q1`, `D1`, `C1`, `L2`, connectors `J1` (three pins) and `J2` (two pins).

Schematic: `J1` pin 3 runs through `L1 4.7mH` to `J2` pin 1. `J1` pin 1 runs through `D1 1N4004` and
`L2 4.7mH` to `J2` pin 2. `J1` pin 2 is labelled `Key`.

| Pin | Printed text |
| --- | --- |
| J1-1 | Gray-Yellow, +12V from Power Driver Board J118-2 |
| J1-2 | Key |
| J1-3 | Blue-Violet, Solenoid Drive #23, from Power Driver Board J126-7 |
| J2-1 | White, to Motor |
| J2-2 | Red, to Motor |

## Boulder Machine Circuit Diagram

Boxes: `Power Driver Board` with `J118` pin `2` and `J126` pin `7`, joined by a ribbon cable from its
`J113` to `J211` on the `CPU Board`; `Motor EMI Board` with `J1` (pins `1` and `3`) and `J2` (pins `2`
and `1`); and the motor symbol labelled `Boulder Machine Motor`.

| From | Wire | To |
| --- | --- | --- |
| Power Driver Board J118-2 | GRY-YEL, +12V | Motor EMI Board J1-1 |
| Power Driver Board J126-7 | BLU-VIO, SOL. #23 | Motor EMI Board J1-3 |
| Motor EMI Board J2-2 | RED | Boulder Machine Motor |
| Motor EMI Board J2-1 | BLK | Boulder Machine Motor |

The board's connector list names the `J2-1` motor wire `White`, while the circuit diagram on the same
page labels it `BLK`.
