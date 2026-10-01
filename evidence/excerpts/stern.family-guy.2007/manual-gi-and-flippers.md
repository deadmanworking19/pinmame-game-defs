# Stern Family Guy (2007) — general illumination and flipper circuit (manual transcription)

Status: **transcribed from the rendered factory pages; not independently reviewed.** Literal transcription; no source-authority or spatial decision.

## Source and transcription envelope

| Field | Value |
| --- | --- |
| Source | *Family Guy Pinball Service Game Manual*, Stern Pinball, Inc., January 2008, v12.0+ |
| PDF SHA-256 | `2bbcfa34ad70ab90c0fadabaf825850cecae58c8028af9aaabf8be1ad01979cd` |
| Locator | PDF page **123** (printed Section 5, Chapter 2, Page 99, "General Illumination Circuit Detailed Wiring Diagram") and PDF page **127** (printed Section 5, Chapter 2, Page 103, "3- Flipper Circuit Wiring Diagram"); flipper assemblies PDF pages **92–94** (printed Section 4, Chapter 2) |
| Method | Visual transcription of 200 dpi renders of the cited pages. |

## General illumination (PDF page 123)

The page shows the I/O Power Driver PCB (520-5249-00) partial view: connector J14 "TRANSFORMER" (pins 1–6: YEL, YEL, YEL, YEL-WHT, YEL-WHT, YEL-WHT; transformer secondary "2ndary 5.7v AC"), four 5 A 250 V SLO-BLO fuses F1–F4, status LEDs L9–L12 (AP2012EC) with 680 Ω resistors R14–R17 and diodes D50–D53 (1N4148), and a "G.I. RELAY RLY1" (FRL264, coil diode D49 1N4004) driven by transistor Q44 (MMBT3904, base resistor R150 1K, "RELAY DRIVER") from the U21 74HCT273 data latch (CLK from U20). The relay's printed note is "G.I.s 5.7VAC INPUT FROM TRANSFORMER". Connector J15 "GENERAL ILLUMINATION" pins 9 8 7 6 [5 KEY] 4 3 2 1 carry the four circuits.

| Circuit | Printed fuse and path | Printed colour mark | Printed location | Printed bulbs |
| --- | --- | --- | --- | --- |
| 1 | J15-P6 to J15-P1 (Fuse **F1**) = BRN-WHT to WHT-BRN | B | "Location: Not Used" | "0 ea. #44 Bulb" |
| 2 | J15-P7 to J15-P2 (Fuse **F2**) = YELLOW to WHT-YEL | Y | "Location: Left Side"; "Spot Lights Above P/F" | "13 each #44 Bulb", "3 each #555 Bulb" |
| 3 | J15-P8 to J15-P3 (Fuse **F3**) = GREEN to WHT-GRN | G | "Location:" followed by "+ US Coin Door X2 (Euro X3)"; "Yellow Bulbs"; "On Coin Door" | "10 each #44 Bulb", "2 each #555 Bulb" |
| 4 | J15-P9 to J15-P4 (Fuse **F4**) = VIOLET to WHT-VIO | V | "Location:" (blank); "Spot Lights Above P/F" | "8 each #44 Bulb", "10 each #555 Bulb" |

Printed footnote: "* G.I. Bulb quantities may change during production." The drawing on the left of the page marks circuit 2 (Y) mostly on the left half of the playfield and circuit 4 (V) mostly on the right half; ten circuit-3 (G) marks sit in a row at "the top of the P/F, rear view of the Back Panel". Four boxed callouts read: "Above Playfield: G.I. in Light Reflector Meg Spotlight" (Y), "Above Playfield: G.I. in Light Reflector Left Ramp @ Peter Spot" (Y), "Above Playfield: G.I. in Light Reflector Brian Spotlight" (Y), and "Above Playfield: X2 G.I. in Light Reflector on Stewie Mini-Pinball Spots" (V).

## Flipper circuit (PDF page 127)

Title: "3- Flipper Circuit Wiring Diagram (Upper Mini-Playfield Flippers operate with lower button presses if programming allows.)" Partial view of the CPU/Sound PCB (520-5246-00) connector J3 "DEDICATED SWITCHES": pins 1, 2, 4, 5, 6, 7, 8, 9 are GRY-BRN, GRY-RED, GRY-ORG, GRY-YEL, GRY-GRN, GRY-BLU, GRY-VIO, GRY-BLK and pin 10 is BLACK ground (dedicated switch IC source number LVC245A).

| Drawn switch | Printed state | Printed location |
| --- | --- | --- |
| LEFT FLIPPER BUTTON SW. D-9 | N.O. | ON CABINET INSIDE LEFT DOUBLE-STACK, DEDICATED SWITCH |
| RIGHT FLIPPER BUTTON SW. D-11 | N.O. | ON CABINET INSIDE RIGHT DOUBLE-STACK, DEDICATED SWITCH |
| UPPER LEFT FLIPPER BUTTON SW. D-13 | N.O. | ON CABINET INSIDE UPR. LEFT DOUBLE-STACK, DEDICATED SWITCH |
| UPPER RIGHT FLIPPER BUTTON SW. D-15 | N.O. | ON CABINET INSIDE UPR. RIGHT DOUBLE-STACK, DEDICATED SWITCH |
| LEFT FLIPPER E.O.S. SW. D-10 | N.C. | ON LEFT FLIPPER ASSEMBLY, DEDICATED SWITCH |
| RIGHT FLIPPER E.O.S. SW. D-12 | N.C. | ON RIGHT FLIPPER ASSEMBLY, DEDICATED SWITCH |
| two further N.C. switches (no SW. number legible) | N.C. | drawn greyed out |

Printed text (verbatim): "The Outside LEFT FLIPPER BUTTON located on the Cabinet operates both the Left Flipper & Upper Left Flipper, if used. The Outside RIGHT FLIPPER BUTTON located on the Cabinet operates both the Right Flipper & Upper Right Flipper, if used. RIGHT & LEFT BUTTONS: These switches are Double-stacked. Pressing half-way down operates the Lower Flippers (respectively); pressing full down operates both the Lower Flipper & Upper Flippers (respectively) simultaneously."

Technical overview (verbatim extracts): "Our Flipper System uses one supply voltage (+50VDC) for both kick & hold. Once the Game CPU detects a Flipper Cabinet Switch closure (during game play) it applies a 40msec pulse to the gate of the Flipper Drive Transistor (STP22NE10L). If it continues to detect a Flipper Cabinet Switch closure (the player holding the button in) it will continue to pulse the flipper drive transistor 1msec every 12msecs for the duration of the hold cycle." "The E.O.S. (End-Of-Stroke) Switch serves the same function as before as it prevents foldback when the player has the flipper energized to capture balls. The E.O.S. Dedicated Switch is a normally closed switch which opens approximately 1/16" when the flipper is energized. The Game CPU will detect a switch closure if the flipper bat is forced back by a high velocity shot or rebound on the playfield and will apply another 40msec pulse of 50VDC to the coil."

I/O Power Driver PCB partial view (connector J9 "HIGH CURRENT SOLENOIDS", J10 "VOLTAGE OUTPUTS"): Q14 BLU-BLK pin 7 coil 23-1500 "#14 Upper Left Flipper" fed BLU-YEL through a 3A SLO-BLO fuse; Q15 ORG-GRY pin 8 coil 23-1100 "#15 (Lower) Left Flipper" fed GRY-YEL through a 3A SLO-BLO fuse; Q16 ORG-VIO pin 9 coil 23-1100 "#16 (Lower) Right Flipper" fed BLU-YEL through a 3A SLO-BLO fuse; "#13" (00-0000, BLU-GRN pin 6, GRY-YEL 3A SLO-BLO) and Q13 are drawn greyed out. "Q14-Q16: These Coil Fuses are located under the playfield NEAR the assembly, see Section 5, Chapter 2, Playfield Wiring" (the page number after "Playfield Wiring" is not legible in the render). "Coil Diodes (1N4004) are integrated on the I/O Power Driver PC Board." The flipper supply is "+50VDC RED-YEL HIGH POWER" through J10 pins 6/7.

## Flipper assemblies (PDF pages 92–94)

Parts tables, verbatim part rows: **Lower Left** assembly 500-6543-14-ND item 3 "Power (EOS / End-of-stroke) Switch" 180-5149-00, coil 23-1100 [NO DIODE] 090-5030-ND. **Lower Right** assembly 500-6543-04-ND item 3 "Power (EOS / End-of-stroke) Switch" 180-5149-00, coil 23-1100 [NO DIODE] 090-5030-ND. **Upper Left** assembly 500-6543-35-NDM, "Yellow Mini-Flipper Bat & Shaft Assy., 515-6275-06"; its item 3 reads "1/4" x 3/8" Plastic Spacer Gray" (quantity 2, 254-5000-02) where the lower assemblies carry the EOS switch; coil 23-1500 [NO DIODE] 090-5062-ND. The upper-left assembly's base plate is "(LEFT) Modified".
