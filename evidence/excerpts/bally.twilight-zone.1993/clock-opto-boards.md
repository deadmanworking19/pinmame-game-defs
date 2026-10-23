# Twilight Zone — Minute and Hour Opto PCB Assemblies (printed 2-17 and 3-18)

Transcribed from `Bally_1993_Twilight_Zone_Operations_Manual_OCR_searchable.pdf` (the complete IPDB copy of
operations manual 16-50020-101), PDF page 85 (printed 2-17, printed sideways, the two boards' drawings and parts
lists) and PDF page 144 (printed 3-18, "Minute Opto P.C.B. Assembly A-16220", its connector list and schematic).
Read from the 300 dpi renders; the PDF's OCR layer and a local OCR pass were used only to find the pages. Both parts
lists and the 3-18 connector list are transcribed whole; the board drawings and the schematic are drawings, and what
they print is written out below.

## Page 2-17, A-16220 Minute Opto PCB Assembly

Board drawing: OPTO1 to OPTO4 near the four edges, J1 at the top, J2 and J3 along the bottom edge, resistors R1-R4,
D1-D5, and four lamp outlines labelled LMP 1 (upper right), LMP 2 (upper left), LMP 3 (lower left) and LMP4 (lower
right) set diagonally around a large circle at the board's centre.

| Part Number | Designator | Description |
| --- | --- | --- |
| 5490-13451-00 | OPTO1 - OPTO4 | Opto Inter with Long Lead |
| 03-8840 | OPTO1 - OPTO4 | Spacer |
| 5010-08930-00 | R1 - R4 | resistor, 470Ω, 1/2w, 5% |
| 5070-09054-00 | D5 | Diode 1N4004 1.0A. |
| 24-8830 | LMP1 - LMP4 | Socket Sub-Mini Wedge PCB |
| 24-8829 | LMP1 - LMP4 | Bulb #86, 6.3, .2A |
| 5791-12622-08 | J2, J3 | Connector, 8-pin Header |
| 5792-11003-07 | J1 | PCB Connector |
| 5010-09034-00 | D1 - D4 | Resistor, 0Ω |

## Page 2-17, A-16219 Hour Opto PCB Assembly

Board drawing: OPTO5 to OPTO8 set diagonally, resistors R5-R8 and the 7-pin header J1; no lamp is drawn.

| Part Number | Designator | Description |
| --- | --- | --- |
| 5490-12451-00 | OPTO5 - OPTO8 | Opto Inter with Long 10mA. |
| 5010-08930-00 | R5 - R8 | Resistor, 470Ω, 1/2w, 5% |
| 5791-13458-07 | J1 | Connector, 7-pin Header |

## Page 3-18, Minute Opto P.C.B. Assembly A-16220

Connector list, left column:

- J1 from J1 on Hour Opto Bd., A-16219
- J2-1 Black-White
- J2-2 Gray-Yellow
- J2-3 Yellow-White
- J2-4 Yellow-White
- J2-5 Yellow
- J2-6 Yellow
- J2-7 Key
- J2-8 Gray-White

Right column:

- J3-1 White-Yellow from J5-9, A-16807
- J3-2 White-Brown from J5-12, A-16807
- J3-3 White-Blue from J5-7, A-16807
- J3-4 White-Green from J5-8, A-16807
- J3-5 White-Violet from J5-6, A-16807
- J3-6 White-Gray
- J3-7 White-Red from J5-11, A-16807
- J3-8 White-Orange from J5-10, A-16807

Schematic, as drawn:

- J2 pin 2 "+12VDC" feeds OPTO1-OPTO4 through R1-R4; pin 1 "GND"; pin 7 "KEY"; pin 8 "SW. COL" through D5 to the
  four opto transistors and on to J1 pin 7 "SW. COL".
- J3 pins 6, 5, 4, 3 carry OPTO4 B, OPTO3 B, OPTO1 B, OPTO2 B (labels R8, R7, R5, R6) through to J1 pins 1-4; J3 pins
  1, 8, 7, 2 carry OPTO4 A, OPTO3 A, OPTO2 A, OPTO1 A (labels R4, R3, R2, R1). J1 pins 6 "+12VDC" and 5 "GND".
- The lamps: J2 pin 6 joins LAMP 1 and LAMP 2, and J2 pin 5 joins LAMP 4 and LAMP 3. The other side of LAMP 1 and
  LAMP 4 returns to J2 pin 3 through D1 and D2, and the other side of LAMP 2 and LAMP 3 to J2 pin 4 through D3 and D4.
  D1-D4 are drawn as diodes; the 2-17 parts list fits 0Ω resistors (5010-09034-00) at D1 - D4.
- Nothing else on the board connects to J2 pins 3-6.

The page prints no bulb count of its own beyond LAMP 1 - LAMP 4, and no G.I. string number. The Power Driver Board
connector list (page 3-33, `power-driver-connectors.md`) prints G.I. string 03's playfield pair as J121-3 "Yellow,
Return G.I. to playfield" and J121-9 "White-Yellow, 6.8VAC to playfield"; this page prints the lamp pins' wires as
"Yellow" and "Yellow-White".
