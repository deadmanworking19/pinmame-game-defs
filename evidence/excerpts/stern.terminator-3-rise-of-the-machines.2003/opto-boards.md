# Terminator 3 — opto board pages

Read from `Stern_2003_Terminator_3_Rise_of_the_Machines_Pinball_Game_Service_Manual.pdf`, Section 5, Chapter 4 "Printed
Circuit Boards (PCBs)": PDF page 127 (printed `Page 109`), PDF page 128, and PDF page 169 (printed `Page 140`). Read from
120-130 dpi renders and checked against the pages' decoded text layer.

## Trough Up-Kicker Dual OPTO Boards Theory of Operation & Schematic (PDF page 127)

Verbatim: "As light from the Transmitter LED1 falls on the Receiver LED1, it generates a Positive Bias Voltage (0.7v to
1.5v) which is applied to the Gate (G) of Q1 (Fet 2N5460) turning Q1 off. When Q1 is held off, no current flows through
Q2's (2N3906) Base (B). With no base current, Q2 is off and acts as an OPEN SWITCH. When the light is interrupted
(BLOCKED) R1 (Rec. Bd.) bleeds the gate voltage off of Q1 allowing it to conduct, switching Q2 on, which acts as a CLOSED
SWITCH. The LED2 (Trans/Rec) Circuit operates identical as the LED1 Circuit."

Schematic: "520-5173-00 Transmitter", CN1 pin 2 RED (+5v) through R1 180 Ω / LED 1 TLRH180P and R2 180 Ω / LED 2
TLRH180P, CN1 pin 1 BLK (GND); "520-5174-00 Receiver", LED 1 / LED 2 TLRH180P, R1 / R4 10M Ω, R3 / R6 10K Ω, Q1 / Q3
2N5460, R2 / R5 4.7K Ω, Q2 / Q4 2N3906; receiver CN1 pins 1 and 3 "WHT/XXX (Switch Row/ Return +)", pin 2 "GRN/XXX
(Switch Col/ Drive -)". Test points A and B are marked on each circuit.

Parts list: "A 1 515-0173-00 Dual-OPTO Trans. Bd. Assy. PCB Assy. (with all Items 1-5)"; "— 1 520-5173-00 Dual-OPTO
Trans. Board"; "B 1 515-0174-00 Dual-OPTO Rec. Bd. Assy."; "— 1 520-5174-00 Dual-OPTO Rec. Board"; LEDs 165-5052-00
"LED TLRH180P (Ultra Bright Red)"; Q1, Q3 110-5006-00 "2N5460, Transistor (P-FET SOT-23)" (from the text layer); Q2, Q4
110-0086-00 "2N3906, Transistor".

## OPTO Troubleshooting (PDF page 128)

Verbatim, item 1: "A. OPEN OPTO (Light Falling on LED) = SWITCH OPEN. Place meter leads across points A and B on the LED1
Circuit (Refer to Schematic Drawing on previous page, 520-5174-00 Receiver Side). It should read approximately 0.8 - 1.2v
DC. The LED2 Circuit operates the same. B. CLOSED OPTO (Light Blocked) = SWITCH CLOSED. Place meter leads across points A
and B on the LED1 Circuit (Refer to Schematic Drawing on previous page, 520-5174-00 Receiver Side). It should read
approximately 0.0 - 0.1v DC. The LED2 Circuit operates the same."

Verbatim, from the alignment test: "the transmitter should light (LED1 lower & LED2 upper) when the power is switched on."
and "With the game in Switch Test Mode, lifting the Trough Plunger with a fingertip should block the beam and cause the
Switch Position to trigger".

## Playfield Switch Single OPTO Transmitter & Receiver Boards Schematic (PDF page 169, printed page 140)

Schematic: "Single OPTO Transmitter 520-5230-00", J1-A pin 1 through L1 TLRH180P and R1 180 Ω to J1-B pin 2; "Single
OPTO Receiver 520-5231-00", L1 TLRH180P with R2 1M Ω and R3 10K Ω into the gate of Q2 2N5460, R1 5.6K Ω to the base of
Q1 2N3906, J1-A pin 1 and J1-B pin 2. The page prints no theory text for this board.

Parts list: "A 1 515-7307-00 Single OPTO Trans. Bd. Assy. PCB Assy. (with all Items 1-5)"; "— 1 520-5230-00 Single OPTO
Trans. Board"; "B 1 515-7308-00 Single OPTO Rec. Bd. Assy."; "— 1 520-5231-00 Single OPTO Rec. Board"; L1 165-5052-00
"LED TLRH180P (Ultra Bright Red)"; Q1 110-5006-00 "2N3906, Transistor (P-FET SOT-23)"; Q2 110-0086-00 "2N5460,
Transistor"; R1 "SMT 5.6K Ω 1/8W Chip Res. (CRCW)", R2 "SMT 1M Ω 1/8W Chip Res. (CRCW)" (part number cells blank for both),
R3 121-5011-00 "SMT 10K Ω 1/8W Chip Res. (CRCW)". Footnote: "If a part is required where a part number is not provided,
call Technical Support (see back of cover)."

## Curator's observations (not printed)

- DR. 4's part note names these boards per switch: 14 and 15 use the dual boards (Trans 515-0173-00, Rec 515-0174-00),
  33 the single boards (Trans 515-7307-00, Rec 515-7308-00). The TX Cannon Trough Assembly 500-6655-00 (PDF page 104)
  carries the single opto; the board table (PDF page 183) lists 515-7307-00 / 515-7308-00 for this game's "TX Cannon
  Trough".
- The single receiver repeats the dual receiver's circuit (the LED's photovoltage on a 2N5460 gate, a 2N3906 output), so
  a blocked beam closes switch 33 as it closes 14 and 15.
- The single-board parts list pairs 110-5006-00 with the 2N3906 and 110-0086-00 with the 2N5460, the reverse of the dual
  board's list, where 110-5006-00 is the 2N5460 and 110-0086-00 the 2N3906.
