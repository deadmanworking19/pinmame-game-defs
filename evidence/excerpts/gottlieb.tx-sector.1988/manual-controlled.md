---
source: gottlieb-tx-sector-fichier-pdf.pdf
source_sha256: 7b9d03dc3105d758b3603a14ef942f2219007ef1de0796bde8ae21a5ebbf6ec5
locator: PDF page 47; printed folio 41; title “PLAYBOARD ‘CONTROLLED’ SOLENOIDS AND ILLUMINATION”
method: Visual transcription from native page-47.png, checked against supplied Windows OCR page-47.txt
transcribed_by: curator transcription; curator source checks/corrections
reviewed: true
status: curator source-checked transcription; explicitly uncertain cells remain unresolved
---

# PLAYBOARD “CONTROLLED” SOLENOIDS AND ILLUMINATION

Wire-number boxes are kept as printed. The drawing's `XXX` convention is recorded in the notes; no wire code is filled by pattern.

## Relay coils, contacts and connector labels

| Source label | Printed connector/pin | Wire code | Printed device/part | Other visible connector, supply or wire labels |
|---|---|---:|---|---|
| A3J3 | pin B | 288 | L1; TILT RELAY “T” | P/O A9P7/J7 pin 8; relay coil marked 16890 |
| A3J3 | pin A | 277 | L3; GAME OVER RELAY “Q” | P/O A9P7/J7 pin 9; relay coil marked 16890 |
| A3J3 | pin 25 | 133 | L12; SWITCHING RELAY “S” | P/O A9P7/J7 pin 10; relay coil marked 16890 |
| Switched relay/contact supply | — | 388 / 222 | Contact outputs at A9J7/P7 | Connector pins 6, 7 carry boxed 388 labels; pins 5, 4 carry boxed 222 labels; “SWITCHED +24V DC” label is printed above the relay contacts |
| Switching-relay contact group | A9P7/J7 pins 11, 12, 13 | 088 / 588 / 888 | S contacts are drawn on the 088 and 888 branches; wire 222 is printed at the switched +24V DC branch | The image shows one S contact between 088 and 222, one 588 line, and a second S contact on 888; connector pin and wire labels are copied literally |

The connector drawing also prints `P/O A9J7/P7` with pin numbers 6, 7, 5 and 4. The relay/contact bus is crowded; the table preserves the neighboring callouts without asserting a pin-to-load path beyond what is legible.

## A19 switching-diode board: controlled solenoid feed rows

The dashed board outline is labelled `SWITCHING DIODE BOARD A19`, part `MA-1050`. The source says “OUTPUT FROM A3 MASTER DRIVER BOARD (SEE SCHEMATIC FOR LAMP DRIVER TRANSISTOR)” at the incoming harness.

| A3 connector pin | Solenoid label | Wire code | A19 connector/pin labels visible | Printed diode/coil/load text |
|---:|---|---:|---|---|
| A3J4 pin 7 | SOL. 1 | 266 | P/O A19J1/P1; pins 2 and 2 shown | D1, 1N5401; downstream coil text is elsewhere on this sheet |
| A3J4 pin 13 | SOL. 2 | 200 | P/O A19J1/P1; pins 5 and 5 shown | D3, 1N5401 |
| A3J4 pin 6 | SOL. 5 | 211 | P/O A19J2/P2; pins 2 and 2 shown | D5, 1N5401 |
| A3J4 pin 12 | SOL. 6 | 233 | P/O A19J2/P2; pins 5 and 5 shown | D7, 1N5401 |

The same sheet shows additional A19 diode labels D2, D4, D6 and D8, each marked `1N5401`, adjacent to the four hole-solenoid rows below. A19 connector pins 1, 4, 3 and 6 appear in paired connector drawings; the paired block layout is retained literally rather than converted into an inferred harness pinout.

## Controlled lamp strings on A19 and resistor board A13

Board outline: `RESISTOR BOARD A13`, drawing/assembly number `25231`. Resistors R1–R4 are each printed `4Ω, 7W, WW`.

| Printed lamp group | Input wire code | A19 connector/pin label visible | Lamps drawn in group | A13 connector/pin | Output wire code | Resistor |
|---|---:|---|---:|---:|---:|---|
| LEFT “TELEPORT ACTIVE” | 133 | P/O A19P1/J1, pin 1 | 2 | A13J1/P1 pin 1 | 033 | R1, 4Ω, 7W, WW |
| RIGHT “TELEPORT ACTIVE” | 144 | P/O A19P1/J1, pin 4 | 2 | A13J1/P1 pin 2 | 044 | R2, 4Ω, 7W, WW |
| LEFT RAMP | 155 | P/O A19P2/J2, pin 1 | 2 | A13J1/P1 pin 3 | 055 | R3, 4Ω, 7W, WW |
| RIGHT RAMP | 166 | P/O A19P2/J2, pin 4 | 2 | A13J1/P1 pin 4 | 066 | R4, 4Ω, 7W, WW |

The dashed lamp group is annotated `ALL LAMPS *67`. The drawing shows two lamp symbols on each row; no separate bulb part number is written beside each individual symbol.

## Hole coils, single-bank circuits and outhole

| Printed load | Input/output wire code(s) | Printed coil/diode | Connector labels visible |
|---|---|---|---|
| TOP LEFT HOLE | 277 | Coil 5195 | P/O A19P1/J1 pin 3; output line also bears 277 |
| LOWER LEFT HOLE | 288 | Coil 5195 | P/O A19P1/J1 pin 6; output line also bears 288 |
| TOP RIGHT HOLE | 055 | Coil 5195 | P/O A19P2/J2 pin 3; output line also bears 055 |
| LOWER RIGHT HOLE | 077 | Coil 5195 | P/O A19P2/J2 pin 6; output line also bears 077 |
| SINGLE BANK TRIP | 122 / 488 | Coil 18642 with diode symbol | P/O A9P5/J5 pin 3 and P/O A9J5/P5 pin 5 are printed beside the circuit; F12, 1 AMP, SLO-BLO is on the 488 branch |
| SINGLE BANK RESET | 244 / 488 | Coil 5195 with diode symbol | P/O A9P5/J5 pin 4 and P/O A9J5/P5 pin 6 are printed beside the circuit; F12, 1 AMP, SLO-BLO is on the 488 branch |
| TOP 4 BANK RESET | 277 / 188 | Coil 5194 with diode symbol | P/O A9P3/J3 pin 6 and P/O A9J3/P3 pin 7 are printed beside the circuit; F13, 2 AMP, SLO-BLO is on the 188 branch |
| RIGHT 4 BANK RESET | 288 / 188 | Coil 5194 with diode symbol | P/O A9P4/J4 pin 6 and P/O A9J4/P4 pin 7 are printed beside the circuit; F13, 2 AMP, SLO-BLO is on the 188 branch |
| SOLENOID 9 / OUTHOLE | 244 | Coil 5195 with diode symbol | P/O A3J4 pin 8; common return continues to the switched supply bus |

**[Pin mapping caution]** Several adjacent connector labels on the bank-reset and outhole branches are close to bus lines. Values above are the legible connector/pin labels next to each named branch; no extra route is inferred where a line crossing is ambiguous.

## A16 transistor driver board and ball release

Board outline: `TRANSISTOR DRIVER BOARD 1A16`, part `MA-1051`.

| Source connector | Printed output/wire | Printed transistor/resistor | Drawn downstream label |
|---|---|---|---|
| P/O A3J6 pin 1 | SOL. 7; 633 | Q1, MJ2955 DRIVER; R2, 4.7K, 1/4W | 1A16 input pin2; output pin3 |
| P/O A3J6 pin 2 | SOL. 4; 644 | Q2, 2N5879 DRIVER; R5, 4.7K, 1/4W | 1A16 input pin4; output pin5 |
| P/O A3J6 pin 3 | SOL. 3; 655 | Q3, 2N5879 DRIVER; R8, 4.7K, 1/4W | 1A16 input pin9; output pin10 |
| P/O A9P1 pin 6 | 877; L2 | Q1, MJ2955 DRIVER; R1, 4.7K, 1/4W | BALL RELEASE coil 16570; wire code 266 at coil input and 088 at output; F10, 1 AMP, SLO-BLO; “GROUND FROM 1A18J2-5” |

P/O `1A16J1/P1` is printed beside the driver-board connector. Pins2,4,9 are input branches, pins3,5,10 outputs, and pin1 ground. A `9` wire label and `GROUND FROM 1A18J2-4` are printed at the ground branch.

### Fuse labels printed on this sheet

| Fuse | Printed rating/type | Adjacent wire/branch labels |
|---|---|---|
| F10 | 1 AMP, SLO-BLO | Ball Release branch; wire 266 / 088 |
| F11 | 1 AMP, SLO-BLO | +24V DC bus at wire 222 |
| F12 | 1 AMP, SLO-BLO | Single Bank Trip and Single Bank Reset outputs, wire 488 |
| F13 | 2 AMP, SLO-BLO | Top 4 Bank Reset and Right 4 Bank Reset outputs, wire 188 |

## Transformer-panel source and playboard illumination

### A12P1 (FROM TRANSFORMER PANEL)

| Pin | Wire code | Printed supply/return label |
|---:|---:|---|
| 3 | 222 | +24V DC (SOURCE) |
| 2 | 066 | 6.3V AC (SOURCE) |
| 1 | 000 | 6.3V AC RETURN |
| 4 | 255 | +6V DC (SOURCE) |

The drawing labels the lamp branch `PLAYBOARD ILLUMINATION`; P/O A9P7/J7 pins 1, 2 and 3 are shown beside it, with wire codes 066, 788 and 788. A relay contact marked `T` is drawn on the 066 branch. **[Exact individual bulb count and the tiny pin-to-contact routing are not expanded beyond the visible diagram.]**

## Printed reference/part list

| Reference | Part number |
|---|---|
| #44 LAMP | LA-0 |
| #67 LAMP | LA-5 |
| #86 LAMP | LA-6 |
| #455 LAMP | LA-1 |
| Q1 | XO-799 |
| R1 | XO-7 |
| R2 | XO-154 |
| **[blank reference row]** | **[blank]** |
| **[blank reference row]** | **[blank]** |
| **[blank reference row]** | **[blank]** |

## Color-code legend and notes

| Digit | Printed color |
|---:|---|
| 0 | BLACK |
| 1 | BROWN |
| 2 | RED |
| 3 | ORANGE |
| 4 | YELLOW |
| 5 | GREEN |
| 6 | BLUE |
| 7 | VIOLET |
| 8 | GRAY |
| 9 | WHITE |

1. ALL DIODES ARE TYPE 1N4004.
2. LAMPS L4 THRU L11 AND L32 THRU L43 ARE DRIVEN BY MPS-A13’S; EXCEPT FOR “A” LAMPS, ALL OTHER LAMPS ARE DRIVEN BY MPS-U45’S.
3. UNLESS OTHERWISE SPECIFIED, GROUND WIRE COLOR IS 9, 18 GAUGE.
4. `XXX` INDICATES WIRE COLOR.
5. UNLESS OTHERWISE SPECIFIED, ALL LAMPS ARE TYPE #44.

## Uncertainty markers

- Several connector blocks use two adjacent copies of the same pin number (for example `2` / `2`). Both printed marks are retained; the text does not assign an undocumented side as plug versus header.
- The sheet contains intersecting buses and adjacent connector callouts. Where the start/end point is not visually unambiguous, only the printed names/codes/pins are reported and the path is left unresolved.
- The individual bulb count for the playboard-illumination branch is not stated in text and is not counted from faint/dotted lamp symbols.
