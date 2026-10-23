# Twilight Zone — Flipper Circuit Diagram (printed 3-25) and Fliptronic II Board A-15472 (printed 3-28)

Transcribed from `Bally_1993_Twilight_Zone_Operations_Manual_OCR_searchable.pdf` (the complete IPDB copy of
operations manual 16-50020-101), PDF page 151 (printed 3-25, "Flipper Circuit Diagram") and PDF page 154 (printed
3-28, "FLIPTRONIC II BOARD A-15472"). Read from the 300 dpi renders; the PDF's OCR layer and a local OCR pass were
used only to find the pages. Page 3-28's connector list and board legend are transcribed whole, in their printed
order, left column then right column. Page 3-25 is a drawing; every connector pin, wire label and destination it
prints is written out below, with the routing of each line as drawn.

## Page 3-25, Flipper Circuit Diagram

J907, the four pins drawn at the board's upper edge, left to right "9 4 7 1". Four supply lines leave them, labelled
from the top: "Gray-Yellow +50Vdc", "Gray-Yellow +50Vdc", "Blue-Yellow +50Vdc", "Blue-Yellow +50Vdc". Followed as drawn:

| J907 pin | Line label | Ends at |
| --- | --- | --- |
| 9 | Gray-Yellow +50Vdc (top line) | LOWER LEFT FLIPPER COIL |
| 4 | Gray-Yellow +50Vdc | UPPER\* LEFT FLIPPER COIL |
| 7 | Blue-Yellow +50Vdc | LOWER RIGHT FLIPPER COIL |
| 1 | Blue-Yellow +50Vdc (lowest line) | UPPER\* RIGHT FLIPPER COIL |

J906, "END-OF-STROKE SWITCHES", pin, wire, label, switch as printed:

| Pin | Wire | Label | Switch |
| --- | --- | --- | --- |
| 5 | Black-Gray | U. Left Flipper | F7\* |
| 3 | Black-Blue | L. Left Flipper | F3 |
| 4 | Black-Violet | U. Right Flipper | F5\* |
| 1 | Black-Green | L. Right Flipper | F1 |
| 6 | Orange | Ground | (blank) |

J902, pin, wire, winding, transistor, coil as printed:

| Pin | Wire | Winding | Transistor | Coil |
| --- | --- | --- | --- | --- |
| 6 | Black-Yellow | Power | Q2 | UPPER\* RIGHT FLIPPER COIL |
| 4 | Orange-Violet | Holding | Q7 | UPPER\* RIGHT FLIPPER COIL |
| 13 | Blue-Violet | Power | Q4 | LOWER RIGHT FLIPPER COIL |
| 11 | Orange-Green | Holding | Q11 | LOWER RIGHT FLIPPER COIL |
| 3 | Black-Blue | Power | Q1 | UPPER\* LEFT FLIPPER COIL |
| 1 | Orange-Gray | Holding | Q5 | UPPER\* LEFT FLIPPER COIL |
| 9 | Blue-Gray | Power | Q3 | LOWER LEFT FLIPPER COIL |
| 7 | Orange-Blue | Holding | Q9 | LOWER LEFT FLIPPER COIL |

J905, to the "CABINET OPTO SWITCHES" box, pin, wire, label, switch as printed:

| Pin | Wire | Label | Switch |
| --- | --- | --- | --- |
| 5 | Black-Blue | U. Left Flipper | F8 |
| 2 | Blue-Gray | L. Left Flipper | F4 |
| 3 | Black-Yellow | U. Right Flipper | F6 |
| 1 | Blue-Violet | L. Right Flipper | F2 |
| 6 | Orange | Ground | (blank) |

The cabinet opto box is fed "Gray-Yellow +12V" from J116 pin 2 of the power driver board. J901 pin 1 "White-Blue
50Vac" runs to J105 pin 1 and J901 pin 5 "White-Blue 50Vac" to J105 pin 2. J904 pin 4 "Black Ground" runs to J114
pin 7 and pin 5 "Black Ground" to J114 pin 5, pin 1 "Gray +5V" to J114 pins 3 and 4 (joined), and pin 2 "Gray-Green +12V" to J114 pins 1 and 2
(joined). J903 is a ribbon cable to J202 of the CPU board.

Footnote as printed: "\*Note: Used as circuits other then flipper circuits in this game." (the asterisk is printed on
F5, F7 and both upper flipper coils).

## Page 3-28, Fliptronic II Board A-15472

Left column:

- J901-1 White-Blue, 50VAC loop from J104-1
- J901-2 White-Blue, loop from J901-1
- J901-3 White-Blue, 50VAC loop, from J104-2
- J901-4 Key
- J901-5 White-Blue, loop from J901-3
- J902-1 Orange-Gray, holding to upper left flipper
- J902-2 Not Used
- J902-3 Black-Blue, power to upper left flipper
- J902-4 Orange-Violet, holding to upper right flipper
- J902-5 Not Used
- J902-6 Black-Yellow, power to upper right flipper
- J902-7 Orange-Blue, holding to lower left flipper
- J902-8 Not Used
- J902-9 Blue-Gray, power to lower left flipper
- J902-10 Key
- J902-11 Orange-Green, holding to lower right flipper
- J902-12 Not Used
- J902-13 Blue-Violet, power to lower right flipper
- J903 Ribbon Cable, data to/from J202; J506; J601
- J904-1 Gray, +5V from J114-4
- J904-2 Gray-Green, +12V from J114-2
- J904-3 Key
- J904-4 Black, Ground from J114-7
- J904-5 Black, Ground from J114-5

Right column:

- J905-1 Blue-Violet, to right flipper opto
- J905-2 Blue-Gray, to left flipper opto
- J905-3 Black-Yellow, to right flipper opto
- J905-4 Key
- J905-5 Black-Blue, to left flipper opto
- J905-6 Orange, Switch Ground
- J906-1 Black-Green, to lower right end-of-stroke switch
- J906-2 Key
- J906-3 Black-Blue, to lower left end-of-stroke switch
- J906-4 Black-Violet, to upper right end-of-stroke switch
- J906-5 Black-Gray, to upper left end-of-stroke switch
- J906-6 Orange, Switch Ground
- J907-1 Blue-Yellow, +50V to lower right flipper
- J907-2 Blue-Yellow, loop from J907-1
- J907-3 Key
- J907-4 Gray-Yellow, +50V to lower left flipper
- J907-5 Gray-Yellow, loop from J907-4
- J907-6 Blue-Yellow, +50V to upper right flipper
- J907-7 Blue-Yellow, loop from J907-6
- J907-8 Gray-Yellow, loop from J907-9
- J907-9 Gray-Yellow, +50V to upper left flipper

P.C. Board Legend (boxed, lower right), as printed: "J1-J6 Coin Door Interface Board", "J1xx Power Driver Board",
"J2xx CPU Board", "J5xx Audio Board", "J6xx Dot Matrix Controller Board", "J9xx Fliptronic II Board".

## Three readings of the J907 supply pins

The Flipper Circuits rows of the Solenoid/Flasher Table (page 2-52, `solenoid-flasher-table.md`) print a third
reading. All three agree that the left flippers' supply is Gray-Yellow and the right flippers' Blue-Yellow; they
disagree on which J907 pin feeds which coil:

| Coil | Page 2-52 | Page 3-25 drawing | Page 3-28 list |
| --- | --- | --- | --- |
| Lower left | J907-7 (Gry-Yel) | 9 | J907-4 (loop J907-5) |
| Lower right | J907-9 (Blu-Yel) | 7 | J907-1 (loop J907-2) |
| Upper left | J907-1 (Gry-Yel) | 4 | J907-9 (loop J907-8) |
| Upper right | J907-4 (Blu-Yel) | 1 | J907-6 (loop J907-7) |

Pages 3-25 and 3-28 agree that pins 1 and 7 carry Blue-Yellow and pins 4 and 9 Gray-Yellow; page 2-52 pairs its
pins with the other colour. The J902 control pins, wires and transistors agree on all three pages.
