# Congo -- flipper opto and end-of-stroke wiring (printed 3-11, 3-14 and 3-24)

Transcribed from 200 dpi renders (the scan's native resolution) of `Congo_OPS.pdf` pages 124, 127
and 137. The image is the load-bearing page, PDF 127 (printed 3-14); pages 124 and 137 are
transcribed below and not imaged.

## Printed 3-11 (PDF 124), Flipper Circuit Diagram, CPU board side

CABINET OPTO SWITCHES, drawn from J212 to a block labelled "FLIPPER OPTO BOARDS":

| J212 pin | Wire | Name | Switch | Input |
| ---: | --- | --- | --- | --- |
| 13 | ORANGE | GROUND | | |
| 12 | BLUE-VIOLET | L. RIGHT FLIPPER | F2 | U25A-1 |
| 11 | BLUE-GRAY | L. LEFT FLIPPER | F4 | U25B-2 |
| 10 | BLACK-YELLOW | U. RIGHT FLIPPER | F6 | U25C-14 |
| 9 | BLACK-BLUE | U. LEFT FLIPPER | F8 | U25D-13 |

END-OF-STROKE SWITCHES, drawn from J208 to four switch symbols:

| J208 pin | Wire | Name | Switch | Input |
| ---: | --- | --- | --- | --- |
| 14 | ORANGE | GROUND | | |
| 13 | BLACK-GREEN | L. RIGHT FLIPPER | F1 | U26A-1 |
| 12 | BLACK-BLUE | L. LEFT FLIPPER | F3 | U26B-2 |
| 11 | BLACK-VIOLET | U. RIGHT FLIPPER | F5 | U26C-14 |
| 10 | BLACK-GRAY | U. LEFT FLIPPER | F7 | U26D-13 |

The blank Switch and Input cells of the two GROUND rows are blank on the page. The same page draws
an UPPER RIGHT FLIPPER COIL (POWER Q84, HOLD Q86) beside the other three coils, and prints below the
drawing: "The upper right flipper coil power circuit is used for the Upper Left Post, and the upper
right flipper coil hold circuit is used for the Mystery Eject."

## Printed 3-14 (PDF 127), Flipper Opto Board Assembly A-20207

The board drawing shows two optos, OPTO1 and OPTO2, each fed through a 680 ohm 1/2 W resistor (R1,
R2); OPTO1's output goes to J1 pin 1 (SW1) and OPTO2's to J1 pin 2 (SW2). J1 pins 3-4 are GND,
pin 5 KEY, pins 6-7 +12V.

| Left Flipper Opto Board Assembly | Right Flipper Opto Board Assembly |
| --- | --- |
| J1-1 Black-Blue from CPU Board J212-9 | J1-1 Black-Yellow from CPU Board J212-10 |
| J1-2 Blue-Gray from CPU Board J212-11 | J1-2 Blue-Violet from CPU Board J212-12 |
| J1-3 N/C | J1-3 Orange from CPU Board J212-13 |
| J1-4 Orange from CPU Board J212-13 | J1-4 Orange from Left Flipper Opto Board Assy. J1-4 |
| J1-5 N/C | J1-5 N/C |
| J1-6 Gray-Yellow from Power Driver Board J139-2 | J1-6 Gray-Yellow from Left Flipper Opto Board Assy. J1-6 |
| J1-7 Gray-Yellow from Power Driver Board J139-2 | J1-7 N/C |

## Printed 3-24 (PDF 137), CPU Board Assembly connector list (J208 and J212 rows)

- J208-10 Black-Gray, F7, to upper left E.O.S. switch
- J208-11 Black-Violet, F5, to upper right E.O.S. switch
- J208-12 Black-Blue, F3, to lower left E.O.S. switch
- J208-13 Black-Green, F1, to lower right E.O.S. switch
- J208-14 Orange, ground to E.O.S. switches
- J212-9 Black-Blue, F8, to left flipper opto board J1-1
- J212-10 Black-Yellow, F6, to right flipper opto board J1-1
- J212-11 Blue-Gray, F4, to left flipper opto board J1-2
- J212-12 Blue-Violet, F2, to right flipper opto board J1-2
- J212-13 Orange, Ground to left flipper opto board J1-4

## Reading

Each cabinet button has one two-opto board. The right button's board brings OPTO1 out as F6 and
OPTO2 as F2, and the left button's brings OPTO1 out as F8 and OPTO2 as F4, so F6 is the right
button's second opto, not an upper-right flipper switch. 3-11 and 3-24 still print F5 as an upper
right E.O.S. switch, and 3-11 draws an upper right flipper coil whose two circuits its own footnote
gives to the Upper Left Post and the Mystery Eject: those rows follow the generic Fliptronic
layout. No upper right flipper is fitted, so F5 has no switch. The Switch Locations list (printed
2-41) prints "F6 Not Used ... Upper Right Flipper Cabinet" and part A-17316 for F2/F4/F8, where 3-14
names the board A-20207. This curation records both readings and follows the wiring pages for F6.
