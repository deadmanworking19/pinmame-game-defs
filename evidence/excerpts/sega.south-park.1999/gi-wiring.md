# South Park — General Illumination circuit wiring

Read from `Sega_1999_South_Park_Manual_English.pdf`, PDF page 49 (right half), printed Section 5 page 83, "Playfield
Wiring / General Illumination Circuit Detailed Wiring Diagram". The page is a scan; the crop `gi-wiring.webp` renders it
at the scan's native resolution, capped to 1500 px wide.

Board side, I-O POWER DRIVER BOARD 520-5137-01:

- U206 74HCT273 Data Latch, D0 (pin 3) to 1Q (pin 2), through R254 1K Ω to Q200 2N3904 ("RELAY DRIVER"), which grounds
  the G.I. RELAY coil; the coil is fed from 20v DC with D229 1N4004 Diode across it.
- "G.I. 6.3v AC INPUT FROM XFRMR": J14 pins 1-3 YEL, pins 4-6 YEL-WHT.
- "5A 250v SLO-BLO Fuses" F27, F26, F25, F24 to J15.
- "General Illumination (G.I.) Bulbs (6.3v AC)".

Circuit legend:

| Circle | Pins | Fuse | Wires | Location as printed | Bulbs |
| --- | --- | --- | --- | --- | --- |
| B | J15-P6 to J15-P1 | F24 | BRN-WHT to WHT-BRN | Left Playfield & Rt. Outlane | 7 ea #44 |
| Y | J15-P7 to J15-P2 | F25 | YELLOW to WHT-YEL | Top Lt. & Rt. Playfield | 9 ea #44 |
| G | J15-P8 to J15-P3 | F26 | GREEN to WHT-GRN | Rt. P/F & Lt. Outlane + Coin Door | 6 ea #44, plus 2 ea #555 on the coin door through a harness connector (YEL-WHT/YEL) |
| V | J15-P9 to J15-P4 | F27 | VIOLET to WHT-VIO | Mid Lt. & Rt. Playfield | 9 ea #44 |

J15 pin 5 is unconnected. Note on the page: "✻ G.I. Bulb quantities may change during production." The rest of the page
draws the playfield as a mirrored "Bottom of Playfield" view with one lettered circle (B, Y, G or V) per socket, and an
"Above P/F Rt. Outlane" callout on one G socket.
