# Terminator 3 — General Illumination Circuit Detailed Wiring Diagram

Read from `Stern_2003_Terminator_3_Rise_of_the_Machines_Pinball_Game_Service_Manual.pdf`, PDF page 121, printed
`Section 5, Chapter 2, Page 103` ("Playfield Wiring — General Illumination Circuit Detailed Wiring Diagram"). Read from
150 and 250 dpi renders. The page's text layer was used only for the two notes under "Text layer only" below, which the
renders do not show.

## Board detail (blue frame, "Partial View I/O POWER DRIVER BD. 520-5137-01")

- `U206 74HCT273 Data Latch`, input `D0 3` → `1D`, output `1Q 2` → `R254 1K Ω` → `Q200 2N3904 Transistor`, labelled
  `RELAY DRIVER`, emitter to ground.
- `G.I. RELAY`: coil between pin 8 (`20v DC`, with `D229 1N4004 Diode` across the coil) and pin 7 (to Q200). Contacts are
  drawn as two blades from pins 5 and 6 over pins 1, 3, 2 and 4, with a dashed blue line between the blades.
- `J14` pins 1, 2 and 3 `YEL` and pins 4, 5 and 6 `YEL-WHT`, labelled `G.I. 5.7v AC INPUT FROM XFRMR`, from the
  `Transformer` (`Primary`, `Secondary 5.7v AC`, `PRI-103.5-115-207-230V 50/60Hz 750VA CLASS 130 EPBO`). J14-1 runs to the
  relay contacts; J14-6 runs to J15 pins 6, 7, 8 and 9.
- `General Illumination (G.I.) Bulbs (5.7v AC)`, `5A 250v SLO-BLO Fuses F27 F26 F25 F24`; the four fuses are joined on one
  side, drawn back to the relay contacts, and run on the other side to J15 pins 4, 3, 2 and 1.
- `J15` pins `9 8 7 6 5 4 3 2 1`; pin 5 has no wire.

## Circuits (right half of the page)

| Circuit | Marker | Connector run (fuse) | Wire pair as printed | Location as printed | Bulbs as printed |
| --- | --- | --- | --- | --- | --- |
| 1 | B | J15-P6 to J15-P1 (Fuse F24) | BRN-WHT to WHT-BRN | Back Panel X10, Insert X6, and above Playfield X2 | 16 ea. #44 Bulb; 2 ea. #555 Bulb; sockets drawn #1, #2 … #18* |
| 2 | Y | J15-P7 to J15-P2 (Fuse F25) | YEL to WHT-YEL | Left & Lower Playfield X18 | 18 ea. #44 Bulb; sockets #1, #2 … #18* |
| 3 | G | J15-P8 to J15-P3 (Fuse F26) | GRN to WHT-GRN | Backbox Insert X17 + US Coin Door X2 (Euro X1) | 17 ea. #44 Bulb; 2 ea. #555 Bulb (coin door, through a "Coin Door Wiring Harness Connector", YEL-WHT and YEL); sockets #1 … #19 and "On Coin Door" #19* |
| 4 | V | J15-P9 to J15-P4 (Fuse F27) | VIO to WHT-VIO | Right Playfield X20 | 20 ea. #44 Bulb; sockets #1, #2 … #20* |

The J15 wire column under the board reads, left to right: 9 `VIOLET`, 8 `GREEN`, 7 `YELLOW`, 6 `BRN-WHT`, 4 `WHT-VIO`, 3
`WHT-GRN`, 2 `WHT-YEL`, 1 `WHT-BRN`. Footnote: "* G.I. Bulb quantities may change during production."

## Location drawings (left half of the page)

- Upper inset, captioned "Above: In the Backbox, rear view of the Backbox Wood Insert.": B markers (six, upper left) and G
  markers (seventeen) around the cannon arc, wires labelled with the colour pairs above, a box `COIL Q4`, and a box
  `MOTOR via Q20 WHT YEL-BLK`.
- Lower drawing, captioned "Below: Bottom of Playfield shown as if leaning up against the B'box." and along its lower edge
  "This Edge is "Upper Playfield". Bottom Assemblies Not Shown for clarity.": Y markers down the left and across the lower
  playfield, V markers down the right, a yellow box of ten B markers labelled "GIs in Cabinet (Light Board X10)", a
  yellow box of two B markers labelled "Above Playfield: GIs in Light Reflectors pointing at TX & T-850 BRN X2", and the
  label "Above Playfield: GIs in Pop Bumpers (X3)" beside three V markers at the bumpers.
- The page draws one G.I. relay for all four circuits; no circuit bypasses it.

## Text layer only

The page's text layer carries two notes at the right edge that do not appear in 200 and 300 dpi renders of the same
area. They are quoted from Poppler `pdftotext -bbox` output, with their positions in PDF points:

- x 505-562, y 444-453, below circuit 1's sockets: "Note: Various Colors, see Page 62 for Part Numbers."
- x 505-578, y 713-718, on the line of the footnote: "Note: GI above P/F is #555 Bulb."

## Bumper bulb on the assembly page (PDF page 101, printed Page 83)

The bumper assembly page ("Bumper Top Assemblies, 515-6459-01 (Qty. 3)") lists item 1 as "#555 Wedge Base Bulb", Qty.
1, 165-5002-00, and labels it "Gen. Illum. (GI) X3"; the assembled view is labelled "General Illumination X3". The
wiring page above counts the three "GIs in Pop Bumpers (X3)" among circuit V's "20 ea. #44 Bulb".
