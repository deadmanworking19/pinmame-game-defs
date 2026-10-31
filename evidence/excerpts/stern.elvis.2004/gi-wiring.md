# Elvis (Stern) — General Illumination Circuit Detailed Wiring Diagram

Read from `Elvis_Manual.pdf`, PDF page 120, printed `Section 5, Chapter 2, Page 103` ("Playfield Wiring"), from a
200 dpi render checked against the page's text layer. Italics are the page's own.

## Circuits

Each circuit's legend prints a lettered disc, the J15 pins and fuse, the wire pair and the location. The circuit
schematics beside it print the bulb count, sockets numbered `#1`, `#2` … and the last socket's number with an asterisk.

| Disc | Circuit | J15 pins (fuse) as printed | Wires as printed | Location as printed | Bulbs as printed | Last socket |
| --- | --- | --- | --- | --- | --- | --- |
| B | 1 | J15-P6 to J15-P1 (Fuse F24) | BRN-WHT to WHT-BRN | Back Panel X10; Pops X3 Upper Right Corner X1 | 11 / 3 ea. #44 / #555 | #14* |
| Y | 2 | J15-P7 to J15-P2 (Fuse F25) | YELLOW to WHT-YEL | Mid Left & Lower Playfield X15 | 15 / 1 ea. #44 / #555 | #16* |
| G | 3 | J15-P8 to J15-P3 (Fuse F26) | GREEN to WHT-GRN | Upper Playfield X10 + US Coin Door X2 (Euro X3) | 10 ea. #44 Bulb, then 2 ea. #555 Bulb | #12* |
| V | 4 | J15-P9 to J15-P4 (Fuse F27) | VIOLET to WHT-VIO | Mid Right Playfield X6 | 5 / 1 ea. #44 / #555 | #5* |

Circuit 3's schematic runs its ten #44 bulbs (`#1` …) to a "Coin Door Wiring Harness Connector", continues as
`YEL-WHT` / `YEL` to two #555 bulbs (`#3` … `#12*`) captioned "On Coin Door". Circuit 4 prints a last socket of `#5*`
beside a count of six bulbs; both are kept as printed. Footnote: "* G.I. Bulb quantities may change during production."

The J15 header's wire labels, pin by pin as drawn: 9 VIOLET, 8 GREEN, 7 YELLOW, 6 BRN-WHT, 5 (no wire), 4 WHT-VIO,
3 WHT-GRN, 2 WHT-YEL, 1 WHT-BRN.

The page's text layer carries two further notes that the rendered page does not show: "Note: GI above P/F is #555
Bulb." and "Note: Various Colors, see Page 62 for Part Numbers."

## Board circuit (Partial View, I/O POWER DRIVER BD. 520-5137-01)

- `U206 74HCT273 Data Latch`, output `1Q` (pin 2) from input `1D` (`D0`, pin 3), through `R254 1K Ω` to the base of
  `Q200 2N3904 Transistor` ("RELAY DRIVER"), which switches the `G.I. RELAY` coil; the coil is fed from "20v DC" with
  `D229 1N4004 Diode` across it.
- The relay (a dashed box with pins numbered 1-8 and two drawn poles) sits between J14 and four "5A 250v SLO-BLO Fuses"
  `F27 F26 F25 F24`, which feed J15 and the "General Illumination (G.I.) Bulbs (5.7v AC)". The exact pole-to-fuse
  routing is not transcribed.
- `J14` "G.I. 5.7v AC INPUT FROM XFRMR": pins 1-3 `YEL`, pins 4-6 `YEL-WHT`, from the transformer's "Secondary 5.7v AC"
  ("Transformer PRI-103.5-115-207-230V 50/60Hz 750VA CLASS 130 EPBO").

## Location drawings

- "*Below:* Bottom of Playfield shown as if leaning up against the Backbox." A playfield plan marks each G.I. socket with
  its circuit disc. Boxed captions: "Above Playfield: G.I. in Light Reflector on Shooter Lane Gate Brkt." (a V disc),
  "Above Playfield: G.I. in Light Reflector on Left Wire Ramp Plastic." (a Y disc) and "Above Playfield: GIs in Pop
  Bumpers (X3)" (B discs).
- "*Below:* Located at the top of the P/F, rear view of the Back Panel." The inset draws ten B discs in a row along the
  panel's top edge, captioned "GIs on rear Back Panel: (X10)", fed by a `BRN` / `WHT-BRN` pair.
