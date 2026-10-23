# Creature from the Black Lagoon — Power Driver Board connectors J118, J120 and J126

Transcribed from `Creature_From_The_Black_Lagoon_OPS.pdf`, PDF page 127, printed page 3-23, the Power Driver Board
connector list. Read from the page's native 200 dpi scan; the OCR text layer was used only to find the page. The three
connector blocks this definition uses are reproduced whole, in printed order and spelling; only line breaks were
normalized.

| Pin | Printed text |
| --- | --- |
| J118-1 | Key |
| J118-2 | Gray-Yellow, +12VDC playfield/cabinet |
| J118-3 | Black, Ground |
| J118-4 | Not Used |
| J120-1 | Brown, Return G.I. to playfield |
| J120-2 | Orange, Return G.I. to playfield |
| J120-3 | Yellow, Return G.I. to playfield |
| J120-4 | Key |
| J120-5 | Green, Return G.I. to playfield |
| J120-6 | Violet, Return G.I. to playfield |
| J120-7 | White-Brown, 6.8VAC to playfield |
| J120-8 | White-Orange, 6.8VAC to playfield |
| J120-9 | White-Yellow, 6.8VAC to playfield |
| J120-10 | White-Green, 6.8VAC to playfield |
| J120-11 | White-Violet, 6.8VAC to playfield |
| J126-1 | Black-Brown, Sol 17 to playfield flasher |
| J126-2 | Black-Red, Sol 18 to playfield flasher |
| J126-3 | Black-Orange, Sol 19 to playfield flasher |
| J126-4 | Black-Yellow, Sol 20 to Chase Light II P.C. J2-2 |
| J126-5 | Blue-Green, Sol 21 to playfield motor |
| J126-6 | Blue-Black, Sol 22 to playfield flasher |
| J126-7 | Blue-Violet, Sol 23 to playfield motor |
| J126-8 | Blue-Gray, Sol 24 to Chase Light II P.C. J2-1 |
| J126-9 | Key |
| J126-10 | Not Used |
| J126-11 | Not Used |
| J126-12 | Violet-Green, Sol 22 to Tieback Diode |
| J126-13 | Not Used |

## Reading notes

- J120-7 (White-Brown) and J120-1 (Brown) are G.I. string 01, "Sequential G.I. #1", public G.I. 0; J120-10
  (White-Green) and J120-5 (Green) are string 04, "Sequential G.I. #2", public G.I. 3. The Solenoid/Flasher Table
  prints the same pins as each string's voltage (J120-1, J120-5) and drive (J120-7, J120-10) connections.
- This list sends solenoid 20 (Black-Yellow) to the Chase Light II board's J2-2 and solenoid 24 (Blue-Gray) to J2-1.
  The Chase Light II page (`chase-light-board.md`, printed 3-14) prints J2-1 Black-Yellow and J2-2 Blue-Gray, and its
  block diagram draws J126-4 BLK-YEL to J2-1 and J126-8 BLU-GRY to J2-2: two readings put solenoid 20 on J2-1 (the
  decoder's DRIV. 1, select bit A) and this one puts it on J2-2. Pinned PinMAME computes the select code as solenoid 20
  plus twice solenoid 24, which is the 3-14 reading. Under this page's reading strings 2 and 3 of each group would
  swap addresses.
- Printed "J126-12 Violet-Green, Sol 22 to Tieback Diode" names solenoid 22 where the Solenoid/Flasher Table's footnote
  prints `** J126-12, Violet-Green, Tieback Diode` against solenoid 23, the Up/Down Ramp (up) coil; the tieback diode
  belongs to that DC coil.
