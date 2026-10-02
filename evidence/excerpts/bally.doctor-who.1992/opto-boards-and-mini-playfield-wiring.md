# Doctor Who — Opto Switch 10 PCB, Bi-directional Motor Drive and mini-playfield wiring

Transcribed from `Bally_1992_Doctor_Who_Manual.pdf`, PDF pages 135, 137 and 138, printed pages `DOCTOR WHO 3-12`
(`Opto Switch 10 PCB Assembly A-15430`), `3-14` (`Bi-directional Motor Drive Assembly A-15680`) and `3-15`
(`Mini-playfield Wiring Block Diagram`). Read from the rendered pages (300 dpi image-only scans), not from the
OCR text. PDF page 136 is the Opto Sw10 PCB schematic drawing (printed 3-13) and is not transcribed.

## Opto Switch 10 PCB Assembly A-15430 (printed 3-12)

- J1-1 Gray-Violet, to opto transmitter Sw #77; J1-2 Gray-Blue, to opto transmitter Sw #76; J1-3 Gray-Green,
  to opto transmitter Sw #71; J1-4 Gray-Yellow, to opto transmitter Sw #72; J1-5 Gray-Orange, to opto
  transmitter Sw #73; J1-6 Gray-Red, to opto transmitter Sw #74; J1-7 Gray-Brown, to opto transmitter Sw #75;
  J1-8 Key; J1-9 Black, Ground.
- J2-1 Orange-Violet, to opto receiver Sw #77; J2-2 Orange-Blue, to opto receiver Sw #76; J2-3 Orange-Green,
  to opto receiver Sw #71; J2-4 Orange-Yellow, to opto receiver Sw #72; J2-5 Orange-Black, to opto receiver Sw
  #73; J2-6 Key; J2-7 Orange-Red, to opto receiver Sw #74; J2-8 Orange-Brown, to opto receiver Sw #75; J2-9
  Gray, +12VDC.
- J3-1 Black, Ground; J3-2 Gray-Yellow, +12VDC from J118-2; J3-3 Green-Orange, from J206-3, to playfield
  switches; J3-4 Green-Violet, from J206-7, to playfield switches; J3-5 Key; J3-6 White-Violet, from J208-8,
  to playfield switches; J3-7 White-Blue, from J208-7, to playfield switches; J3-8 White-Green, from J208-5,
  to playfield switches; J3-9 White-Yellow, from J208-4, to playfield switches; J3-10 White-Orange, from
  J208-3, to playfield switches; J3-11 White-Red, from J208-2, to playfield switches; J3-12 White-Brown, from
  J208-1, to playfield switches.
- J4-1 Gray, to opto transmitter Sw #33; J4-2 Key; J4-3 Black, to opto transmitter Sw #33; J4-4 White, to
  opto receiver Sw #33; J4-5 Green, to opto receiver Sw #33.
- J5-1 Gray-Yellow, to opto transmitter Sw #32; J5-2 Black, to opto transmitter Sw #32; J5-3 Key; J5-4 White,
  to opto receiver Sw #32; J5-5 Green, to opto receiver Sw #32.
- J6-1 Gray, to opto transmitter Sw #31; J6-2 Black, to opto transmitter Sw #31; J6-3 White, to opto
  receiver Sw #31; J6-4 Key; J6-5 Green, to opto receiver Sw #31.

The board carries the ten opto channels of switches 31, 32, 33 and 71-77 (J4, J5 and J6 for 33, 32 and 31;
J1 and J2 for the seven mini-playfield channels), and passes the column wires of switch columns 3 and 7 and
all eight row wires through J3.

## Mini-playfield Wiring Block Diagram (printed 3-15)

The block diagram (printed rotated) draws, from top to bottom: a `20V Motor Sol. #27` on the Bi-directional
Motor Drive Board connector J2 (pins 1 Black and 4 Red); the Bi-directional Motor Drive Board J1 fed by wires
`BLU-YEL` and `BLU-ORG` from Power Driver Board J122 (pins 3 and 4), `RED-WHT` from J107-6 and `BLK-BRN` from
J126-1 (`Flasher #17`); the Opto Switch 10 PCB Assembly with J4, J5 and J6 carrying `SW #31`, `SW #32` and `SW
#33` (wire colours WHT, GRN, GRY, BLK, GRY-GRN as drawn), J1 and J2 with a note "This represents only one of
the five opto switches at J1 and J2", and J3 with the matrix wires `WHT-BRN`, `WHT-RED`, `WHT-ORG`, `WHT-YEL`,
`WHT-GRN`, `WHT-BLU`, `WHT-VIO`, `GRN-VIO` and `GRN-ORG`, `GRY-YEL`; the Power Driver Board J113 ribbon to the
CPU Board J211, and CPU Board J208 / J206 connectors.

The drawing's motor label reads `Sol. #27`; the Solenoid/Flasher Table (`solenoid-flasher-table.md`) prints
27 as `Mini-playfield C.C.W./C.W.` and 28 as `Mini-playfield On/Off`.

## Bi-directional Motor Drive Assembly A-15680 (printed 3-14)

Connector list: J1-1 Blue-Yellow, from J122-3; J1-2 Blue-Orange, from J122-4; J1-3 Key; J1-4 Black, Ground;
J1-5 Red-White, +20VDC from J107-6. J2-1 Black, Gound [sic]; J2-2 Key; J2-3 Not Used; J2-4 Red, to cannon
motor, Sol 27.

The schematic below the board drawing labels the J1 pins `5 +12VDC`, `4 GROUND`, `3 KEY`, `2 DRIVER
UP/DOWN` and `1 ENABLE`, and the J2 pins `1 +MOTOR`, `2 KEY`, `3 NC` and `4 -MOTOR`; it draws four TIP102/TIP107
transistors (Q1-Q4) around the motor terminals with two LM339 comparators (U1A, U1B) and a fifth TIP102 (Q5).

The wire colours and the connector pins on this page disagree with the Power Driver Board connector list
(`power-driver-board-connectors.md`): that list prints J122-3 as `Blue-Orange, Sol 27, Special 7 Drive` and
J122-4 as `Blue-Yellow, Sol 28, Special 8 Drive`, so the colour on J1-1 (`Blue-Yellow`, the ENABLE pin) is
sol 28's and the colour on J1-2 (`Blue-Orange`, the DRIVER UP/DOWN pin) is sol 27's, while the "from J122-3" and
"from J122-4" notes name the other pins. The Solenoid/Flasher Table prints 27 as `Mini-playfield C.C.W./C.W.`
and 28 as `Mini-playfield On/Off`.
