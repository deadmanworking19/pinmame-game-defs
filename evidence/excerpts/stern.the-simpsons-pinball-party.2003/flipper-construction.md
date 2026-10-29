# The Simpsons Pinball Party — physical contact construction

Source: Stern operations manual, SHA256 `412023c67f699d68c10c6a70120712d34d71417b7dd16f1662e252a66561c898`.
Method: mixed; complete relevant contact-diagram transcription and factual technical-overview paraphrase. Transcribed and visually reviewed by pinmame-game-defs curation against the factory pages on 2026-10-29. Contact construction is independent of the emulator's public state.

## PDF124 / printed106 — 5-Flipper Circuit Wiring Diagram

The factory legend explicitly defines **N.C. = Normally Closed** and **N.O. = Normally Open**. Both EOS contacts are labelled N.C.; all three cabinet flipper-button contacts are labelled N.O. All five shown contacts return to the BLK ground common. The CPU connector heading reads “DEDICATED SWITCH INPUTS (SWITCH TO GROUND), CN6.”

| Dedicated switch | Literal contact label and physical function | Contact at rest | Wire | CPU CN6 pin |
|---|---|---|---|---|
| DS-1 | 2nd LEVEL PLAYFIED [sic] LEFT FLIPPER and LWR. LEFT FLIPPER; IN CABINET | N.O. | GRY-BRN |2|
| DS-2 | LEFT E.O.S.; ON ASSY. | N.C. | GRY-RED |3|
| DS-3 | 2nd LEVEL PLAYFIED [sic] RIGHT FLIPPER and LWR. RT. FLIPPER; IN CABINET | N.O. | GRY-ORG |4|
| DS-4 | RIGHT E.O.S.; ON ASSY. | N.C. | GRY-YEL |6|
| DS-5 | UPPER RIGHT FLIPPER; IN CABINET | N.O. | GRY-GRN |7|

The same manual's complete dedicated-switch table, PDF30/printed16, binds the parts and lists the remaining contacts. Its header gives BLK common ground on CN6-P1 and CN6-P11.

| Dedicated switch | Full factory function | Wire and CN6 pin | Factory part number | Rest-state authority |
|---|---|---|---|---|
|DS-1|LEFT FLIPPER BUTTON, on Cabinet Side|GRY-BRN/P2|180-5160-00|N.O., PDF124 and126|
|DS-2|LEFT FLIPPER E.O.S. (End-of-Stroke), Below Playfield|GRY-RED/P3|180-5149-00 on Flipper|N.C., PDF124|
|DS-3|RIGHT FLIPPER BUTTON, on Cabinet Side|GRY-ORG/P4|180-5164-00 Doubled|N.O., PDF124 and126|
|DS-4|RIGHT FLIPPER E.O.S. (End-of-Stroke), Below Playfield|GRY-YEL/P6|180-5149-00 on Flipper|N.C., PDF124|
|DS-5|UPPER RT. FLIPPER BUTTON, on Cabinet Side|GRY-GRN/P7|180-5164-00 Doubled|N.O., PDF124 and126|
|DS-6|VOLUME (RED BUTTON), In Test: LEFT, on Coin Door|GRY-BLU/P8|180-5192-02|N.O., PDF126|
|DS-7|SERV. CRED. (GREEN BUTTON), In Test: RIGHT, on Coin Door|GRY-VIO/P9|180-5192-04|N.O., PDF126|
|DS-8|BEGIN TEST (BLACK BUTTON), In Test: ENTER, on Coin Door|GRY-BLK/P10|180-5192-00|N.O., PDF126|

PDF96/printed78, Left Flipper Assembly500-6543-12, and PDF97/printed79, Right Flipper Assembly500-6543-02, both list item3, **Power (End of Stroke) Switch**, quantity1, part180-5149-00. The assembly drawings label them DEDICATED SW.02 and SW.04 respectively. These are the game's own lower-flipper assemblies.

### Technical Overview: complete factual paraphrase, PDF124

- One 50 VDC supply provides both the kick and hold phases. The lower left and lower right each have one **22-1080 winding**, specified in their own assembly tables as coil 090-5032-00T. The diagram draws one winding per coil, without separate power and hold windings.
- During a game, a cabinet flipper-button closure causes the CPU to drive the STP20N10L transistor with an initial **40 ms** pulse.
- While that button stays closed, the hold phase pulses the same drive transistor for **1 ms every 12 ms**. This is pulsed control of the same physical winding.
- The physical EOS contact is **normally closed**. At the energized end of the stroke it opens by approximately **1/16 inch**.
- Its purpose is to resist foldback while the player holds a flipper up to catch or retain a ball. A fast shot or rebound can push the bat back and reclose the EOS. The CPU detects that closure and supplies another **40 ms** pulse of 50 VDC to the same coil.

### Complete factual cabinet-button operation note, PDF124

The outside left button operates the lower left and second-level left flippers. The outside right button uses two stacked NO contacts: half travel closes DS-3 and operates the lower right; full travel closes DS-3 and DS-5 and operates all three right flippers together (lower right, upper right on the main playfield, and second-level right). The factory circuit wires DS-3 and DS-5 separately to CN6-P4 and CN6-P7. The logical phases do not imply an extra physical button or a separate hold winding.


## Drawing crop

`flipper-construction.webp`: The_Simpsons_Manual.pdf page 124, crop box 0.03,0.02,0.94,0.93, born-digital page rendered for legibility (smallest type in region 5.0pt, targeting 11px glyphs), rendered at 158 dpi, grayscale, 1226x1587 WebP quality 70.
