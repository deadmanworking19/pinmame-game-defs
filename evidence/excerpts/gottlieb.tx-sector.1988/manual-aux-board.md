---
source: gottlieb-tx-sector-fichier-pdf.pdf
source_sha256: 7b9d03dc3105d758b3603a14ef942f2219007ef1de0796bde8ae21a5ebbf6ec5
locator: PDF page 49; printed folio 43
method: Visual transcription from native page-49.png, checked against supplied Windows OCR page-49.txt
transcribed_by: curator transcription; curator source checks/corrections
reviewed: true
status: curator source-checked transcription; explicitly uncertain cells remain unresolved
---

# AUXILIARY LAMP DRIVER BOARD (A11)

## Connector and supply labels

### A11P1 (4-position connector)

| Pin | Printed connection |
|---:|---|
| 1 | (NOT USED); adjacent callout: “NOT USED IN THIS GAME” |
| 2 | Ground |
| 3 | **[blank/no connection drawn]** |
| 4 | +5V DC; C4, 47 UF 10V, is drawn from this supply to ground |

Other printed parts near P1: R1 3K; C1 .01UF; C2 .01UF; C4 47 UF 10V. A separate timing network shows R12 3K, R13 680K and U5 LM555M.

### A11P2 output channels

The schematic and component-location drawing show ten channels. No lamp/load names are printed for these outputs.

| Channel transistor | Driver IC output pin | Series/base resistor | A11P2 output pin | Printed device label |
|---|---:|---|---:|---|
| Q1 | U2 pin 2 | R2, 12K | 1 | **[blank; no load name printed]** |
| Q2 | U2 pin 4 | R3, 12K | 2 | **[blank; no load name printed]** |
| Q3 | U2 pin 6 | R4, 12K | 3 | **[blank; no load name printed]** |
| Q4 | U2 pin 8 | R5, 12K | 4 | **[blank; no load name printed]** |
| Q5 | U2 pin 10 | R6, 12K | 5 | **[blank; no load name printed]** |
| Q6 | U6 pin 2 | R7, 12K | 6 | **[blank; no load name printed]** |
| Q7 | U6 pin 4 | R8, 12K | 7 | **[blank; no load name printed]** |
| Q8 | U6 pin 6 | R9, 12K | 8 | **[blank; no load name printed]** |
| Q9 | U6 pin 8 | R10, 12K | 9 | **[blank; no load name printed]** |
| Q10 | U6 pin 10 | R11, 12K | 10 | **[blank; no load name printed]** |

U2 and U6 are each labelled SN7405N. The table above records the output-pin/channel traces drawn; it does not assign game lamp names.

### Other ICs and printed connector pins

- U1: 7400N, 2-input NAND; shown with outputs at pins 3, 6, 8 and 11.
- U3: SN7490N decade counter; shown with outputs/pins 12, 9, 8 and 11 routed toward U4.
- U4: SN7442N decoder; input pins shown 1, 2, 3 and 4; supply pin 16, ground pin 8.
- U2: SN7405N; supply pin 14, ground pin 7.
- U6: SN7405N; supply pin 14, ground pin 7.
- U5: LM555M timer; pins 1, 2, 3, 4, 6, 7 and 8 are shown in the timing circuit.
- P2: 10 POS. CONNECTOR; P1: 4 POS. CONNECTOR.

## Schematic notes

1. ALL TRANSISTORS ARE NSD-U45.
2. ALL RESISTORS ARE ±5%, 1/4W.
3. ALL STROBED LAMPS ARE #44.

The board title block reads `AUX. LAMP DRIVER BOARD (A11)`, drawing `E-21594`, date `10-15-81`.

## Auxiliary lamp driver board (A11) parts list

| Reference | Description | Part number |
|---|---|---|
| **[blank reference]** | AUXILIARY LAMP DRIVER ASSEMBLY | MA-789 |
| C1 | CAPACITOR, .1 MFD, 100V CERAMIC RADIAL LEAD | XO-626 |
| C2-C3 | CAPACITOR, .01 MFD, 100V RADIAL LEAD | XO-202 |
| C4 | CAPACITOR, 47 MFD, 10V ELECTROLYTIC RADIAL LEAD | XO-227 |
| Q1-Q10 | TRANSISTOR, NSD-U45 NPN DARLINGTON | XO-146 |
| R1, R12 | RESISTOR, 3K OHM, 5%, 1/4 W | XO-23 |
| R2-R11 | RESISTOR, 12K OHM, 5%, 1/4W | XO-9 |
| R13 | RESISTOR, 680K OHM, 5%, 1/4W | XO-669 |
| U1 | I.C. 2-INPUT NAND, 7400 | XO-420 |
| U2, U6 | I.C. INVERTER, 7405 | XO-403 |
| U3 | I.C. DECADE COUNTER, 7490 | XO-425 |
| U4 | I.C. DECODER, 7442 | XO-426 |
| U5 | I.C. TIMER, NE555 | XO-631 |
| P2 | 10 POS. CONNECTOR | XO-B79 |
| P1 | 4 POS. CONNECTOR | XO-B79 |

## Uncertainty markers

- The source contains ten channel outputs, not eight. This file retains Q1–Q10 and A11P2 pins 1–10 exactly as drawn; it does not decide whether some outputs are unused elsewhere.
- The sheet gives channel identifiers and connector pins but no load names for the ten A11P2 outputs.
- P1 pin 3 has no line or label drawn. It is recorded as blank/no connection drawn, not as “not used.”
- The text “NOT USED IN THIS GAME” is adjacent to P1 pin 1. No broader “board not used” claim is made.
