# Elvis (Stern) — Trough Up-Kicker Dual OPTO boards

Read from `Elvis_Manual.pdf`, PDF pages 126-128 (Section 5, Chapter 4, "Printed Circuit Boards (PCBs)"; PDF 126 prints
`Page 109`, PDF 127 prints `Page 110`). Read from 110 dpi renders and checked against the pages' text layer. Italics and
bold are the page's own and are dropped here.

## Theory of Operation & Schematic (PDF page 126)

Verbatim: "As light from the Transmitter LED1 falls on the Receiver LED1, it generates a Positive Bias Voltage (0.7v to
1.5v) which is applied to the Gate (G) of Q1 (Fet 2N5460) turning Q1 off. When Q1 is held off, no current flows through
Q2's (2N3906) Base (B). With no base current, Q2 is off and acts as an OPEN SWITCH. When the light is interrupted
(BLOCKED) R1 (Rec. Bd.) bleeds the gate voltage off of Q1 allowing it to conduct, switching Q2 on, which acts as a CLOSED
SWITCH. The LED2 (Trans/Rec) Circuit operates identical as the LED1 Circuit."

Schematic as drawn: "520-5173-00 Transmitter", CN1 pin 2 RED (+5v) through R1 180 Ω / LED 1 TLRH180P and R2 180 Ω /
LED 2 TLRH180P to CN1 pin 1 BLK (GND); "520-5174-00 Receiver", LED 1 and LED 2 TLRH180P, R1 / R4 10M Ω, R3 / R6 10K Ω,
Q1 / Q3 2N5460, R2 / R5 4.7K Ω, Q2 / Q4 2N3906; receiver CN1 pin 1 and pin 3 "WHT/XXX (Switch Row/ Return +)", pin 2
"GRN/XXX (Switch Col/ Drive -)". Test points A and B are marked on each receiver circuit. "= Emitting Light".

Parts list (as printed): "A 1 515-0173-00 Dual-OPTO Trans. Bd. Assy. PCB Assy. (with all Items 1-5)"; "— 1 520-5173-00
Dual-OPTO Trans. Board PCB Assy. (with Items 1-3 only)"; "01 1 045-5111-02 CN1 2X, .156" Rt. Angle (26-60-5020) Conn.";
"02 2 165-5052-00 LED1, LED2 LED TLRH180P (Ultra Bright Red)"; "03 2 121-5067-00 R1, R2 180 Ω 1/8W Chip Res. (CRCW)";
"04 3 530-5308-02 n/a OPTO PCB Brass Tube Spacer"; "05 3 545-5518-00 n/a OPTO PCB Rubber Grommet"; "B 1 515-0174-00
Dual-OPTO Rec. Bd. Assy. PCB Assy. (with all Items 1-9)"; "— 1 520-5174-00 Dual-OPTO Rec. Board PCB Assy. (with Items
1-7 only)"; "01 1 045-5111-03 CN1 3X, .156" Rt. Angle (26-60-5030) Conn."; "02 2 165-5052-00 LED 1, LED 2 LED TLRH180P
(Ultra Bright Red)"; "03 2 110-5006-00 Q1, Q3 2N5460, Transistor (P-FET SOT-23)"; "04 2 110-0086-00 Q2, Q4 2N3906,
Transistor"; "05 2 121-5082-00 R1, R4 10M Ω 1/8W Chip Res. (CRCW)"; "06 2 121-5083-00 R2, R5 4.7K Ω 1/8W Chip Res.
(CRCW)"; "07 2 121-5011-00 R3, R6 10K Ω 1/8W Chip Res. (CRCW)"; "08 3 530-5308-02 n/a OPTO PCB Brass Tube Spacer";
"09 3 545-5518-00 n/a OPTO PCB Rubber Grommet". Rows 02 are printed in red.

## OPTO Troubleshooting (PDF page 127)

Verbatim:

- "1. Volt Meter Test (indicates normal operating condition): A. OPEN OPTO (Light Falling on LED) = SWITCH OPEN. Place
  meter leads across points A and B on the LED1 Circuit (Refer to Schematic Drawing on previous page, 520-5174-00
  Receiver Side). It should read approximately 0.8 - 1.2v DC. The LED2 Circuit operates the same. B. CLOSED OPTO (Light
  Blocked) = SWITCH CLOSED. Place meter leads across points A and B on the LED1 Circuit (…). It should read
  approximately 0.0 - 0.1v DC. The LED2 Circuit operates the same."
- "2. Oscilloscope Test (…): A. OPEN OPTO (Light Falling on LED) = SWITCH OPEN. … The Scope should display a STEADY +5v
  as shown in Fig. A, Wave Form Diagram. B. CLOSED OPTO (Light Blocked) = SWITCH CLOSED. … The Scope should display a
  PULSE STREAM indicating Q2 has switched "On" as shown in Fig. B, Wave Form Diagram. This is your Switch Drive Pulse."
- "3. Bench Test (See Fig. C): … The output will be approx. +5v DC when the BEAM IS NOT BLOCKED and approx. 0v when the
  BEAM IS BLOCKED." (The text layer prints the last value as "?v"; the render shows "0v".)

"Trough Dual OPTO Boards Alignment / Test for LED1", verbatim: "When a working OPTO is installed and connected in a game,
the transmitter should light (LED1 lower & LED2 upper) when the power is switched on. With the playfield in Service
Position #1 (playfield lifted up and resting on Playfield Support Slide Brackets) and the game on, the LED lights should
show up as a BRIGHT RED RINGS through the back of the Receiver Board around the Receivers LED1 & LED2 (see Fig. 1).
Testing only LED1: With the game in Switch Test Mode, lifting the Trough Plunger with a fingertip should block the BEAM
and cause the Switch Position to trigger (see Fig. 2). View Fig. 2a & 2b (on the next page) for a sectional view of the
Light Path (note alignment) and what happens as a ball breaks the light beam." Fig. 2 is captioned "Plunger blocks BEAM"
and "Lift plunger to check switch as shown."

## Test for LED2 (PDF page 128)

Verbatim: "… Testing only LED2: TO PERFORM THIS TEST, A PINBALL MUST BE IN THE BALL TROUGH. With the game in Switch Test
Mode, lifting the Trough Plunger with a finger tip should block the BEAM on LED2 and cause the Switch Position to
trigger (see Fig. 3). View Fig. 3a & 3b for a sectional view of the Light Path (note alignment) and what happens as a
"double-stacked" ball scenario breaks the light beam."

## Curator's observations (not printed)

The pages do not say which LED circuit is switch 14 and which is switch 15. The switch grid names 14 "4-BALL TROUGH VUK
OPTO" and 15 "4-BALL STACKING OPTO", which matches LED1 (lower, blocked by the up-kicker's ball) and LED2 (upper,
blocked only by a double-stacked ball).
