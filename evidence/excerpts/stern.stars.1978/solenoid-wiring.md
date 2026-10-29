# Solenoid driver B-432-S-103

Full decoder and load/connector regions on Stars manual PDF 25-26, visually read on the
native renders by the primary curator. Connector prefixes A3 are expanded
from the board identity. `N/U` remains literal, `[blank]` means no wire
colour printed. Brackets and parentheses are column separators here;
the schematic uses brackets for colours and parentheses for diagnostic
numbers. Public numbers are derived from the retained ROM coil test, not
printed on this drawing. Public routing is derived from the U2 selector
and the complete collector paths, including bends and junction dots.
Crossing wires without a dot are not connected. **Blank printed test
numbers remain blank**, even where the public address is established by
routing. Every N/U connector branch is retained separately below.

| Public, derived | Driver | Connector | Printed load | Wire | Printed test |
| --- | --- | --- | --- | --- | --- |
| 1 | Q2 | A3J2-4 | CHIME 10 | W-B | 1 |
| 1 | Q2 | A3J1-3 | N/U | [blank] | [blank] |
| 2 | Q1 | A3J2-9 | CHIME 100 | W-O | 3 |
| 2 | Q1 | A3J1-2 | N/U | [blank] | [blank] |
| 3 | Q5 | A3J2-10 | CHIME 1000 | W-BRN | 5 |
| 4 | Q6 | A3J2-11 | EXTRA CHIME | W-G | 7 |
| 5 | Q7 | A3J2-12 | N/U | [blank] | [blank] |
| 6 | Q3 | A3J3-4 | KNOCKER | BLU-Y | 15 |
| 6 | Q3 | A3J2-5 | N/U | [blank] | [blank] |
| 7 | Q4 | A3J1-5 | OUT HOLE | BRN-Y | 8 |
| 8 | Q8 | A3J5-10 | N/U | [blank] | [blank] |
| 9 | Q13 | A3J5-12 | LEFT DROP TARGET RESET | R-W | 10 |
| 10 | Q14 | A3J5-11 | RIGHT DROP TARGET RESET | O-W | 13 |
| 11 | Q9 | A3J5-9 | N/U | [blank] | [blank] |
| 12 | Q10 | A3J5-15 | N/U | [blank] | [blank] |
| 13 | Q12 | A3J5-13 | TOP BUMPER | B-BLU | 6 |
| 14 | Q11 | A3J5-14 | RIGHT SLING SHOT | B-Y | 9 |
| 15 | Q16 | A3J5-8 | LEFT SLING SHOT | R-B | 14 |
| 15 | Q16 | A3J2-6 | N/U | [blank] | [blank] |
| 15 | Q16 | A3J3-7 | N/U | [blank] | [blank] |
| 17 | Q17 | A3J5-7 | N/U | [blank] | [blank] |
| 18 | Q19 | A3J2-8 | COIN L.O. | Y-W | [blank] |
| 19 | Q15 | On-board relay terminal 8 | FLIPPER ENABLE RELAY | [blank] | [blank] |
| 19 supply | [not a collector endpoint] | A3J3-5 | TO A2J3-8 | Y-W | [blank] |
| 20 | Q18 | A3J5-3 | N/U | [blank] | [blank] |
| 20 | Q18 | A3J2-15 | N/U | [blank] | [blank] |
| 20 | Q18 | A3J3-9 | N/U | [blank] | [blank] |

The last three Q18 branches join at a dot before A3J2-15. Q15 collector
ends at relay terminal8 on the board. Its terminal7 is fed by +43V through
A3J3-5, not driven out through that connector. N/U branches on fitted
drivers do not add loads or quantities; wire colours above belong only to
the branches where they are printed. The J1 P box on PDF26 positively
labels pins5 OUT HOLE, 2 N/U, 3 N/U; it is not J5.

## PDF25 decoder drawing, literal reading

The complete native-resolution decoder/stage region is retained in
`solenoid-decoder.webp`, including all U2 inputs and outputs, intermediate
stages, transistor labels, and printed legends. This is drawing evidence,
not a replacement for the load/connector transcription above.

Printed text: `PINS 3, 4, 5 & 6 MOMENTARY SOLENOID DATA`;
`PIN 7 SOLENOID BANK SELECT LOW WHEN SELECTED`; `U2 74L154`.

| J4 B pin | Wire, literal | U2 pin | Printed weight | Pull-up |
| --- | --- | --- | --- | --- |
| 6 | BLU-Y | 23 | 1 | R4 100K |
| 5 | BLU-R | 22 | 2 | R3 100K |
| 4 | O-B | 21 | 4 | R2 100K |
| 3 | R-W | 20 | 8 | R1 100K |
| 7 | BRN-R | 19 | [blank] | [none drawn] |

U2 pin24 is the upper supply rail; pins18 and12 are grounded. R1-R4
connect to the separately marked `+5` rail. The following table retains
every decoder output route. Pin numbers are printed; selector indices
and public addresses are **derived separately**, never printed here.

| U2 output pin | Series resistor | Stage | Input pin | Output pin | Driver |
| --- | --- | --- | --- | --- | --- |
| 1 | R57 | U1 | 3 | 2 | Q2 |
| 2 | R58 | U1 | 16 | 1 | Q1 |
| 3 | R59 | U1 | 13 | 14 | Q5 |
| 4 | R60 | U1 | 11 | 12 | Q6 |
| 5 | R61 | U1 | 10 | 9 | Q7 |
| 6 | R62 | U1 | 6 | 4 | Q3 |
| 7 | R63 | U1 | 8 | 7 | Q4 |
| 8 | R64 | U3 | 16 | 1 | Q8 |
| 9 | R65 | U3 | 11 | 12 | Q13 |
| 10 | R66 | U3 | 13 | 14 | Q14 |
| 11 | R67 | U3 | 3 | 2 | Q9 |
| 13 | R68 | U3 | 8 | 7 | Q10 |
| 14 | R69 | U3 | 10 | 9 | Q12 |
| 15 | R70 | U3 | 6 | 4 | Q11 |
| 16 | R71 | U4 | 8 | 7 | Q16 |
| 17 | [none drawn] | [open stub] | [blank] | [blank] | [none drawn] |

Printed component annotations include `1.2K (x15)` at R57;
`120Ω (x15)` at R5; `.002 (x15)` at C1; `330Ω (x15)` at R6;
`1N4004 (x15)` at CR2; `Q2 * X44E198 (x15)`.
Printed bottom legends: `U1, U2 & U3 = CA3081`;
`* X44E198 SUBSTITUTE SE9302`; `[BRN-Y] = WIRE COLOR`;
`(8) = SOLENOID TEST DISPLAY No.`

## Public address derivation

Reading the printed weights as the U2 selector's low-to-high bits gives
selector0..14 routed to Q2,Q1,Q5,Q6,Q7,Q3,Q4,Q8,Q13,Q14,Q9,Q10,Q12,Q11,Q16.
The pinned `by35.c:331-360` `pia1b_w` publishes bit `(1 << (data & 0x0f))
& 0x7fff` when the bank is selected; public solenoids are one-based. The
resulting routes are retained in
`tools/seeds/stern/stars-1978-coil-decoder.json`, including stage pins and
all collector endpoints. Q2 at public1 reaches CHIME10 at A3J2-4; Q4 at
public7 reaches OUT HOLE at A3J1-5. The decoder, collector paths, numbered
fitted loads and retained ROM traces agree on all fifteen momentary rows.
Public5/8/11/12 are derived by routing; their printed test cells are still
blank. Engineering Bulletin9 page2 independently corroborates the complete
CA3081 chart, including Q1/U1 and Q8/U3 base16/collector1. Its factual
transcription is in `coils-and-options.md`; its jack instruction explicitly
names J1, J2 and J5. The game's own sheet also identifies J3's branches.

Native source-pixel collector overlays, path coordinates and hashes are
retained externally in review-artifacts/stern.stars.1978/retrace-r2,
`collector-traces-v2.json`. Each branch is followed through bends and
junction dots, rather than assigning transistors by the horizontal order
of the printed loads. Continuous routes are PB4/Q17/public17 to A3J5-7;
PB5/Q19/public18 to A3J2-8; PB6/Q15/public19 to the on-board relay; and
PB7/Q18/public20 to all three N/U branches listed above.

Q15 switches FLIPPER ENABLE RELAY. Its contact connects A3J1-8 to the LEFT
FLIPPER SW. (A3J2-2, BLU) and A3J1-9 to RIGHT FLIPPER SW. (A3J2-1, R).
The two contact poles are mechanically linked. A3J1-8 goes TO LEFT FLIPPER
COIL (G) (16), A3J1-9 TO RIGHT FLIPPER COIL (O) (16). Relay supply is
43VDC. MPU data labels on A3J4 are PB6 FLIPPER DISABLE (pin 8, BLU-W),
PB4 (pin 11, Y-W), PB7 (pin 10, Y-R), PB5 COIN LOCK OUT (pin 9, BLU-O).
PinMAME publishes complemented continuous bits; its public 19 enables
synthetic flippers. Do not invert this public output again because the
physical data line is labelled DISABLE.

Factory table on printed p15 names EXTRA CHIME as CHIME (10,000). The
coil-test numbers 2,4,11,12 are blank there; the actual driver sheet
positively prints N/U for those loads. The ROM sweeps them nevertheless.
The brief public 17/20 power-up pulse is the initialization write to all
continuous bits and does not assert fitted loads.

PDF 29 draws both dual-winding flippers with a normally-closed contact
across one winding. The cabinet button is normally open; the EOS opens
the winding bypass near the end of travel. This circuit has no MPU matrix
feedback and cannot be represented as a measured EOS callback.

G.I. on PDF 29: A2J1-8 (W), 6 VAC, GEN. ILLUM; A2J1-1 (R), RETURN.
PDF 30 controlled lamps: A2J1-7 (BLU), FEATURE LAMP BUS. These are
distinct circuits. The shared power transformer sheet B-464-S is labelled
STINGRAY SOLID STATE; only its board-internal information is reusable.
Stars' own harness pages above decide which branches are populated.
