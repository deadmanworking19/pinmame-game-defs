# Harley-Davidson (Stern) — opto board theory pages

Read from `Stern_Harley_Davidson_3rd_Edition_Pinball_Game_Service_Manual.pdf`, PDF pages 107 and 140 (Section 5,
Chapter 4, "Printed Circuit Boards (PCBs)"; page 140 prints `Page 124`). Read from 200 dpi renders and checked against
the pages' decoded text layer.

## Trough Up-Kicker Dual OPTO Boards Theory of Operation & Schematic (PDF page 107)

Verbatim: "As light from the Transmitter LED1 falls on the Receiver LED1, it generates a Positive Bias Voltage (0.7v to
1.5v) which is applied to the Gate (G) of Q1 (Fet 2N5460) turning Q1 off. When Q1 is held off, no current flows through
Q2's (2N3906) Base (B). With no base current, Q2 is off and acts as an OPEN SWITCH. When the light is interrupted
(BLOCKED) R1 (Rec. Bd.) bleeds the gate voltage off of Q1 allowing it to conduct, switching Q2 on, which acts as a CLOSED
SWITCH. The LED2 (Trans/Rec) Circuit operates identical as the LED1 Circuit."

Schematic: transmitter CN1 pin 2 RED (+5v) through R1 180 Ω / LED 1 TLRH180P and R2 180 Ω / LED 2 TLRH180P; receiver
LED 1 / LED 2 TLRH180P, R1 / R4 10M Ω, R3 10K Ω, Q1 2N5460, R2 / R5 4.7K Ω, Q2 / Q4 2N3906; receiver CN1 pins 1 and 3
"WHT/XXX (Switch Row/ Return +)", the column "GRN/XXX (Switch Col/ Drive -)". Test points A and B are marked.

Parts list: "A 1 515-0173-00 Dual-OPTO Trans. Bd. Assy. PCB Assy. (with all Items 1-5)"; "— 1 520-5173-00 Dual-OPTO
Trans. Board"; "B 1 515-0174-00 Dual-OPTO Rec. Bd. Assy."; "— 1 520-5174-00 Dual-OPTO Rec. Board"; LEDs 165-5052-00
"LED TLRH180P (Ultra Bright Red)".

## Playfield Switch OPTO "Long-Hop" Boards Theory of Operation & Schematic (PDF page 140, printed page 124)

Verbatim: "The light falling on LED (CR1) generates a voltage which is applied to the input (Pin-2) of the LM311
Comparator (U1). R1 bleeds off excess charge. At about a volt input from LED (CR1) the Comparator (U1) trips & drives
either Q1 (during switch line strobes) or the indicator LED (CR2) (in between strobes). If a switch line is being strobed,
the emitter of Q1 drops to the saturation voltage of the Switch Line Driver, about .3 volts. This plus the .7 volt drop
on the base give a 1v forward bias voltage to Q1, which is lower than the 1.7v drop on LED (CR2) so the current flows
through the Transistor during strobes. This drives Q1 on and makes the switch. If the strobe line is high, then the 1.7v
path through LED (CR2) is lower than Q1's bias voltage so current flows through LED (CR2) and the indicator lights. D1
prevents reverse bleed, R2 and R3 form the voltage divider for the trip point, R4 is a current limiter for both Q1 and
CR2, C1 and C2 are general noise-filter caps."

Schematic as drawn: "520-5082-00 Transmitter" (CN1 1 RED +5v, R1 180 Ω, CR1 LED TLRH180P, CN1 2 BLK GND) and
"520-5083-01 Receiver": CR1 LED TLRH180P with R1 1M Ω across it into U1 LM311 pin 2, drawn with the triangle's "−" mark
at pin 2 and "+" at pin 3; pin 3 from the divider R2 330K Ω / R3 6.8K Ω on +5v with C1 .1uf, 25v; pins 8 (+5v) and 4
(ground); the output transistor's collector to +5v through R4 220K Ω and its emitter to Q1 2N3904's base and to CR2 "RED
T1-3/4 DIFF. LED"; D1 1N914 into the return line. CN1: "1 RED (+5v DC) from I/O Bd. J16-P8", "2 WHT-BLU (Sw. Return to
CPU/Snd. Bd. CN7-P3)", "3 GRN-BLK (Sw. Drive from CPU/Snd Bd. CN5-P6)", "5 BLK (Ground) from I/O Power Driver Bd.
J16-P9-15".

Component layout: "520-5082-00 (TRANS)" ("LONG OPTO XMTR", Pin-1 RED (+5v), Pin-2 BLK (GROUND)); "520-5083-01 (REC)"
("OPTO RCVR.", Pin-1 RED (+5v), Pin-2 WHT-GRN (Sw. Return +), Pin-3 GRN-BLK (Sw. Drive −), Pin-4 BLK (GROUND)).

Boxed note, verbatim: "Note: In this game, this Combo OPTO Board is used as a P/F Detection Switch for the Motorcycle
Enter Trough. See the Switch Matrix Grid (Pgs. 16-17 or 86). PCBs are used for Switch 37, (GRN-BLK, WHT-GRN)."

Parts list (selected): "A 1 520-5083-01 OPTO Receiver Board Complete PCB Assembly"; CR1 165-5052-00 "LED TLRH180P (Ultra
Bright Red)"; CR2 165-5099-00 "LED T1-3/4 RED DIFFUSER"; D1 112-5014-00 "1N914, Diode"; R1 121-5013-00 "1M Ω"; R2
121-5037-00 "330K Ω"; R3 121-5077-00 "6.8K Ω"; R4 121-5014-00 "220 Ω 1/4W Res., 5%"; U1 100-5025-00 "LM311"; Q1
110-0069-00 "2N3904, Transistor"; "B 1 520-5082-00 OPTO Transmitter Board Complete PCB Assembly".

## Curator's observations (not printed)

- The schematic's CN1 pin 2 colour and connector (WHT-BLU, CN7-P3) are another switch's; the layout drawing and the boxed
  note give this game's WHT-GRN return, which matches switch 37's row 5 (WHT-GRN, CN7-P5) on DR. 4.
- R4 prints 220K Ω on the schematic and "220 Ω" in the parts list.
- The theory text and the drawing's "−"/"+" marks say a lit receiver drives Q1 and makes the switch. On the LM311's own
  pinout pin 2 is the non-inverting input and pin 3 the inverting input; read that way, the drawn circuit drives Q1 when
  the beam is blocked, as the Dual OPTO boards do. The machine definition settles the contact's rest state from the
  platform read path and the retained script and harness runs, and states the disagreement on switch 37.
