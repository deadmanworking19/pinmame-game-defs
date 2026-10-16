# Corvette — Opto Theory, LED List and Fuse List

Provenance: transcribed from the Bally "Corvette" (1994) service manual, PDF pages m-057 (printed page 1-39), m-058 (printed page 1-40) and m-059 (printed page 1-41), rendered at 300 dpi (`rendered-300/m-057.png`, `m-058.png`, `m-059.png`). Text is copied literally (spelling, capitalization, punctuation, line structure); the fuse table values were checked against 1:1 crops. Transcription draft, not yet reviewed against the rendered pages by a curator.

## m-057 (printed page 1-39): OPTO THEORY

```
OPTO THEORY
The opto receiver (Photo Transistor) should be approximately 0.1-0.7 volts when the opto beam
is unblocked and approximately 11-13 volts when the opto beam is blocked. The opto transmitter
(L.E.D.) should always be approximately 1.4 volts. Note, the transmitter (L.E.D.) is larger than
the receiver (Photo Transistor); it protrudes further from its case.
```

Drawing (two board sketches facing each other, a horizontal line between them). All printed labels:

Left sketch (transmitter):

```
LED Board
Transmitter
1.0-1.1 Volts
Green          (label above the board, at the top of the front view)
A   K          (pin labels on the front view; the two solder pads, A at left, K at right)
SOLDER
WHT            (label above the side view)
Gray           (wire at lower left)
Black          (wire at lower right)
```

Centre, between the two sketches:

```
Infrared Ray
```

Right sketch (receiver):

```
Photo Transistor Board
Receiver
0.1-0.7V Unblocked
11-13V Blocked
BLK            (label above the side view)
Blue           (label above the board, at the top of the front view)
C   E          (pin labels on the front view; the two solder pads, C at left, E at right)
SOLDER
White          (wire at lower left)
Green          (wire at lower right)
```

Note: the diagram prints the transmitter voltage as `1.0-1.1 Volts`, while the paragraph above it says approximately 1.4 volts; both are as printed.

```
1-39
```

## m-058 (printed page 1-40): LED List

Heading: `LED List`

Drawing 1: a boxed outline of the CPU board with its parts and three LED positions. Labels printed in the drawing: `U4`, `U6`, `U8`, `U9`, `B1`, `B2`, `B3` (a stacked group of three battery/part positions at the right), `D19`, `D20`, `D21` (each with a small circle beneath, left to right under U4/U6/U8) and the caption `CPU Board`.

```
CPU Board
D19, Blanking
D20, Diagnostic
D21, +5vdc
At Game Turn-On = D19 & D21 On, D20 Off
During Normal Operation = D19 Off, D20 flashing, D21 On
```

Drawing 2: a boxed outline of the Power Driver Board with fuse positions and seven LED positions. Labels printed in the drawing: fuses `F101`, `F102`, `F103`, `F104`, `F105` (a row of five vertical fuses at the top centre), `F106`, `F107`, `F108`, `F109`, `F110` (a cluster at the lower left: F108 above, F107 and F109 side by side, F106 and F110 side by side), `F111`, `F112`, `F113`, `F114` (a stack of four at the upper right), `F115` (below and left of the F101 row), `F116` (vertical, at the upper left), LEDs `LED 1` through `LED 7` (each with a small circle: LED 1 at the far left, LED 7 at the upper left next to F116, LED 2 and LED 3 below it side by side near F115, LED 4 below the F101-F105 row, LED 6 right of LED 4, LED 5 above LED 6 beside the F111-F114 stack), and the caption `Power Driver Board`.

```
Power Driver Board
LED 1, +12vdc, Switch Circuit, Normally On
LED 2, High/Low Line Voltage Sensor, Normally On
LED 3, High/Low Line Voltage Sensor, Normally Off
LED 4, +5vdc, Digital Circuit, Normally On
LED 5, +20vdc, Flashlamp Circuit, Normally On
LED 6, +18vdc, Lamps Circuit, Normally On
LED 7, +12vdc, Power Circuit (Motors, Relays, Etc.), Normally On
```

```
1-40
```

## m-059 (printed page 1-41): Fuse List

Heading: `Fuse List`

Drawings (four boxed board outlines across the top, and a larger Power Driver Board outline below). Labels printed in the drawings: `Fliptronic II Controller Board` with fuses `F902`, `F901` (upper pair) and `F904`, `F903` (lower pair); `Audio Board` with `F501`, `F502`; `Dot Matrix Controller Board` with `F602`, `F601`; `Power Driver Board` with `F116`, `F101`-`F105`, `F111`-`F114`, `F115`, `F108`, `F107`, `F109`, `F106`, `F110` (same arrangement as on the LED List page).

### Audio Board

| Fuse | Description | Rating |
| --- | --- | --- |
| F501 | -25V Circuit | 3A, 250V, S.B. |
| F502 | +25V Circuit | 3A, 250V, S.B. |

### Dot Matrix Controller Board

| Fuse | Description | Rating |
| --- | --- | --- |
| F601 | +62V Circuit | 3/8A, 250V, F.B. |
| F602 | -113V and -125V Circuits | 3/8A, 250V, F.B. |

### Fliptronic II Controller Board

| Fuse | Description | Rating |
| --- | --- | --- |
| F901 | Upper Right Flipper | 3A, 250V, S.B. |
| F902 | Upper Left Flipper | 3A, 250V, S.B. |
| F903 | Lower Right Flipper | 3A, 250V, S.B. |
| F904 | Lower Left Flipper | 3A, 250V, S.B. |

### Power Driver Board

| Fuse | Description | Rating |
| --- | --- | --- |
| F101 | +50VDC General (Left Flipper) | 3A, 250V, S.B. |
| F102 | +50VDC General (Right Flipper) | 3A, 250V, S.B. |
| F103 | Solenoid #25-#28 | 3A, 250V, S.B. |
| F104 | Solenoid #9-#16 | 3A, 250V, S.B. |
| F105 | Solenoid #1-#8 | 3A, 250V, S.B. |
| F106 | G.I. #5 Wht-Vio | 5A, 250V, S.B. |
| F107 | G.I. #4 Wht-Grn | 5A, 250V, S.B. |
| F108 | G.I. #3 Wht-Yel | 5A, 250V, S.B. |
| F109 | G.I. #2 Wht-Org | 5A, 250V, S.B. |
| F110 | G.I. #1 Wht-Brn | 5A, 250V, S.B. |
| F111 | Flasher Secondary | 5A, 250V, S.B. |
| F112 | Solenoid Secondary | 7A, 250V, S.B. |
| F113 | +5V Logic | 5A, 250V, S.B. |
| F114 | +18V Lamp Matrix | 8A, 32V, N.B. |
| F115 | +12V Switch Matrix | 3/4A, 250V, F.B. |
| F116 | +12V Secondary | 3A, 250V, S.B. |

### Line Filter

| Item | Rating |
| --- | --- |
| Domestic Game | 8A |
| Foreign Game | 5A, S.B. |

```
1-41
```

## Uncertain readings

No unreadable words. Notes (crops under `review-artifacts/corvette-1994/scratch/rules/`):

- Fuse table values verified at 1:1 in `m059_left.png` and `m059_right.png` (F601/F602 are `3/8A`; F115 is `3/4A`; F112 is `7A`; F114 is `8A, 32V, N.B.`).
- Opto diagram labels verified in `m057_diagram.png`. The small pin letters on the sketches (`A`, `K` on the transmitter; `C`, `E` on the receiver) are printed very small; `A`/`K` and `C`/`E` are as read. Which wire colour attaches to which pad is not stated in text; only the colour labels are transcribed.
- The positions of the LED circles in the two board drawings are described approximately; only the label text is literal.
