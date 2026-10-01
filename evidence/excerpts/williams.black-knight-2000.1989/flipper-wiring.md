# Black Knight 2000 — flipper wiring: cabinet wiring, interconnect signals and flipper assembly

Source: `Williams_1989_Black_Knight_2000_Operations_Manual.pdf` (102 pages): PDF page 80 (printed
"Black Knight 76", Cabinet Wiring), PDF page 97 (Interconnect Board Interboard Signals, unnumbered
Section 3 table pages, a 150 ppi scan), PDF page 52 (printed 48, Lower Right Flipper C-12898) and PDF
page 53 (printed 49, Lower Left Flipper, Upper Right Flipper and Flipper Link Assembly). Read from 345
dpi (pages 52, 53, 80) and 150 dpi (page 97, its native resolution) renders of bilevel scans with no
text layer. Every cell quoted is transcribed; connector rows are copied in connector order.

## Cabinet Wiring drawing (printed page 76), flipper section

The drawing shows, from the CPU board, the 1J19 header ("Flipper" pin 1, "Flipper Gnd" pin 2) carried
by 1P19 as wires ORN-VIO and ORN-GRY to 2P5 pins 5 and 4 (through 2J5), and on to 2J10 pins 7 and 8
(through 2P10). Pin 7 (ORN-VIO) goes to the contact of a switch labelled "Right Flipper Button"; pin 8
(ORN-GRY) goes to two contacts joined by a dashed line, labelled "Lwr Left Flipper Button" and
"Upr Left Flipper Button". Each of the three contacts carries a 0.1 µF capacitor. The switch outputs
return on 2J10 pins 1 (from the Right Flipper Button), 2 (from the Lwr Left Flipper Button) and 4 (from
the Upr Left Flipper Button), which the drawing carries to 2P8 pins 15, 14 and 12. The "Playfield Flipper
Coils" bracket beside 2P8 lists five wires: BLU-GRY (14), BLU-VIO (15), BLK-BLU (12), GRY-YEL (8) and
BLU-YEL (9). A "Flipper Power" header, 5J12 pins 4 and 2 (5P12), carries BLU-YEL and GRY-YEL through
2P5 pins 2 and 3 (2J5).

## Interconnect Board Interboard Signals (PDF page 97), flipper rows

Printed columns: Connector, Wire Color, Signal Designation/Description.

| Connector | Wire color | Signal designation / description |
| --- | --- | --- |
| 2J5-1 | RED/WHT | +50 Vdc / Sol. Power |
| 2J5-2 | BLU/YEL | +50 Vdc / Flippers |
| 2J5-3 | GRY/YEL | +50 Vdc / Flippers |
| 2J5-4 | ORG/GRY | Flipper Ground |
| 2J5-5 | ORG/VIO | Flipper Ground |
| 2J5-6 | BLK | (blank) |
| 2J8-8 | GRY/YEL | +50 Vdc / Flippers |
| 2J8-9 | BLU/YEL | +50 Vdc / Flippers |
| 2J8-10 | Key Pin | No Connection |
| 2J8-11 | RED/WHT | +50 Vdc / Sol. Power |
| 2J8-12 | --- | No Connection |
| 2J8-13 | --- | No Connection |
| 2J8-14 | BLU/GRY | Lwr L Flipper Switch, LPF |
| 2J8-15 | BLU/VIO | Lwr R Flipper Switch, LPF |
| 2J10-1 | BLU/VIO | Lwr R Flipper Switch, LPF |
| 2J10-2 | BLU/GRY | Lwr L Flipper Switch, LPF |
| 2J10-3 | --- | No Connection |
| 2J10-4 | --- | No Connection |
| 2J10-5 | RED | (blank) |
| 2J10-6 | Key Pin | No Connection |
| 2J10-7 | ORN/VIO | (blank) |
| 2J10-8 | ORN/GRY | (blank) |
| 2J10-9 | WHT/YEL | Gen Illum Power: 6V ac |
| 2J10-10 | YEL | Transformer: 6V ac |

No row of this table, or of its continuation on PDF page 98, gives 2J8 pin 12 or 2J10 pin 4 a
signal. The same table's 2J5-6 row prints a wire color (BLK) and no description.

## Lower Right Flipper C-12898 (printed page 48), flipper switch and wire rows

| Item | Part No. | Description |
| --- | --- | --- |
| 1 | HW-30018-6 | Wire, 18 AWG, Blue |
| 9 | FL-11630 | Flipper Coil (Red), (* - Refer to Note 3) |
| 23 | 03-7811 | End of Stroke (EOS) Switch |
| 24 | HW-30018-64 | Wire, 18 AWG, Blue/Yellow |
| 25 | 01-3670 | Switch Plate-Curve |
| 26 | SW-1A-183 | Flipper Switch |

Flipper Assembly Notes printed on the page include "3 Not Used" (the note the coil row refers to) and:
"9 Solid color blue wire connects to the banded end of each diode, mounted on the connector end of the
Flipper Coil (item 9). Trace color wire connects to the unbanded end of the diode."

## Lower Left Flipper and Upper Right Flipper (printed page 49)

The page lists the parts that replace the same items of C-12898. "Lower Left Flipper p/n C-11626-L-3":
13 B-10655-L Crank Link Assembly, Left; g) B-10657-L Flipper Crank Assembly, Left; 1.) 01-8073-L Flipper
Crank, Left; 18 C-11627-L Flipper Base Assembly, Left; 20 4105-01019-10 Sh. Metal Screw, #5 x 5/8;
"24-26 Not Used". "Upper Right Flipper p/n D-12702-R-1": "19 Not Used"; 20 4105-01019-10 Sh. Metal Screw,
#5 x 5/8; "24-26 Not Used". The "Flipper Link Assembly p/n B-10686-2" parts (13 f) 1.) 02-4219 Coil
Plunger, 2.) 20-9370-1 Spring Pin, 3.) 03-8050-1 Flipper Link) are listed on the same page.
