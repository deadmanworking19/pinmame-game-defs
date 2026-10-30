# Harley-Davidson (Stern) — General Illumination Circuit Detailed Wiring Diagram

Read from `Stern_Harley_Davidson_3rd_Edition_Pinball_Game_Service_Manual.pdf`, PDF page 101, printed `Section 5, Chapter
2, Page 85` ("Playfield Wiring"). The crop `gi-wiring.webp` renders the whole diagram. Read from a 200 dpi render and
checked against the page's decoded text layer.

## Relay and supply

- Board: "I-O POWER DRIVER BOARD 520-5137-01".
- "U206 74HCT273 Data Latch", output D0 (pin 3 in, 1Q pin 2 out), through "R254 1K Ω" to "Q200 2N3904 Transistor"
  ("RELAY DRIVER"), switching the "G.I. RELAY" coil from "20v DC" with "D229 1N4004 Diode" across it. The relay's drawn
  contact block prints terminals 8, 5, 6, 7, 1, 3, 2, 4.
- "Transformer MIDWESTCO U396PB47 PRI-103.5-115-207-230V 50/60Hz 750VA CLASS 130 EPBO"; "Secondary 6.3v AC".
- J14: pins 1-3 YEL, pins 4-6 YEL-WHT; "G.I. 6.3v AC INPUT FROM XFRMR".
- "General Illumination (G.I.) Bulbs (6.3v AC)", "5A 250v SLO-BLO Fuses F27 F26 F25 F24", out on J15 pins 9 to 1.
- As drawn, J14 pins 1-3 (YEL) run to the relay's contact terminals and the relay's switched side runs down the right
  edge to one line feeding all four fuses F27-F24, which go out on J15 pins 4 to 1; J14 pins 4-6 (YEL-WHT) run
  straight to J15 pins 6-9. The one relay therefore switches all four circuits.

## Circuits

| Marker | Printed route | Fuse | Wires | Location as printed | Bulbs as printed |
| --- | --- | --- | --- | --- | --- |
| B | J15-P6 to J15-P1 | F24 | BRN-WHT to WHT-BRN | Upper Left Playfield | Circuit 1: #1, #2 ... #10*, "10 ea. #44 Bulb" |
| Y | J15-P7 to J15-P2 | F25 | YEL to WHT-YEL | Upr. Rt. & Lwr. Right P/F | Circuit 2: #1, #2 ... #10*, "10 ea. #44 Bulb" |
| G | J15-P8 to J15-P3 | F26 | GRN to WHT-GRN | Lower Left P/F + Coin Door | Circuit 3: #1 ... "8 ea. #44 Bulb", then through a "Coin Door Wiring Harness Connector" to "2 ea. #555 Bulb" #9 and #10* "On Coin Door", YEL-WHT and YEL |
| V | J15-P9 to J15-P4 | F27 | VIO to WHT-VIO | Upper Right Playfield | Circuit 4: #1, #2 ... #10*, "10 ea. #44 Bulb" |

The J15 column labels read, pin 9 to pin 1: VIOLET, GREEN, YELLOW, BRN-WHT, (pin 5 not wired), WHT-VIO, WHT-GRN,
WHT-YEL, WHT-BRN. Page note: "* G.I. Bulb quantities may change during production."

## Bottom-of-playfield drawing

Captioned "Bottom of Playfield Shown as if leaning up against the Backbox": the apron end is at the top of the drawing.
Circled markers, counted on the render:

- G: 8, at the top left of the drawing (the playfield's lower left);
- Y: 10, down the right of the drawing (the playfield's right side, front and rear);
- B: 10, at the bottom left of the drawing (the playfield's upper left);
- V: 10, at the bottom right of the drawing (the playfield's upper right).

38 playfield markers in all, matching the bulb counts above (8 + 10 + 10 + 10); circuit 3's two #555 bulbs are on the
coin door, not on the playfield, for 40 G.I. bulbs in all.
