# LED Test and Playfield 19-LED PC Board

Transcribed from `Lord_of_the_Rings_Manual-2022.pdf` (Stern's 211-page reissue of manual 780-5080-00, November 2003), PDF page 42 (the LOTR TESTS "LED" test) and PDF page 162 (printed Section 5, Chapter 4, page 144). Both pages carry a text layer; the text below was read from the rendered pages and checked against that layer.

## PDF 42: LED Test (complete text of the test's block)

> Selecting the "LED" Icon will bring up the LED TEST MENU with the "+" Mini-Icon flashing and the LED Test set to ALL OFF. This test is provided to allow a method of testing the 19-LED PCB located between the flippers. Note: These LEDs are not Controlled Lamps (i.e. not part of the Lamp Matrix.)
>
> Select and activate the "+" Mini-Icon to cycle between the twenty (20) LED Tests (ALL ON, LED #1 through LED #19). ALL ON = All 19 LEDs will blink ON and OFF until the test is exited. LED #1 = L1 will blink ON and OFF. LED #2 through LED #19 will follow suit.
>
> See Section 5, Chapter 4, PCBs, Page 144 for a close up view of the 19-LED PCB.

## PDF 162: Playfield 19-LED PC Board Component Layout

The page prints two photographs of board 520-5242-00 (captioned `Front`, the LED side, and `Back`, the component side) and a component layout drawing captioned `Front`, with `Top Edge` printed above the top of the board, the connector `J1` drawn as a column of pins down the board's right-hand side between `12` (top) and the `J1` label (bottom), and `Key Pin-10` printed beside the second pin from the top. Four grey circles mark the mounting holes at the corners. The accompanying image keeps the layout drawing.

LED positions, read from the PDF's own vector circles (the centre of the white circle each label is printed in, in PDF points, y increasing downwards; `Top Edge` is printed at y 279):

| LED | x | y | ring around the board centre |
| --- | --- | --- | --- |
| L1 | 243.611 | 468.848 | inner |
| L2 | 201.395 | 468.838 | inner |
| L3 | 220.879 | 429.869 | inner |
| L4 | 323.171 | 341.379 | outer |
| L5 | 376.753 | 431.480 | outer |
| L6 | 356.457 | 535.409 | outer |
| L7 | 276.085 | 601.616 | outer |
| L8 | 169.733 | 601.616 | outer |
| L9 | 92.608 | 535.376 | outer |
| L10 | 72.311 | 431.493 | outer |
| L11 | 125.894 | 341.379 | outer |
| L12 | 220.846 | 368.981 | middle |
| L13 | 154.308 | 400.643 | middle |
| L14 | 137.259 | 475.333 | middle |
| L15 | 185.970 | 535.376 | middle |
| L16 | 262.283 | 535.376 | middle |
| L17 | 310.182 | 475.328 | middle |
| L18 | 294.757 | 400.664 | middle |
| L19 | 220.846 | 304.846 | outer |

Three LEDs form a triangle at the centre (L3 at its top), seven form a middle ring (L12 at its top) and nine an outer ring (L19 alone at its top, L8 and L7 as a pair at its bottom), so the layout has one axis of symmetry, left to right, and none top to bottom.

Printed parts table (the only row the rendered page shows):

| ITEM | QTY | PART NUMBER | REF-DESIGNATOR | DESCRIPTION |
| --- | --- | --- | --- | --- |
| - | 1 | 520-5242-00 | Playfield 19-LED PC Board | Complete PCB Assembly |

The page's text layer also holds three further rows that the rendered page does not draw: `1 | 1 | CN1 | Connector, 4X .156"`, `2 | 1 | CN2 | Connector, 5X .156"` and `3 | 3 | 112-5014-00 | D1, D2, D3 | 1N914, Signal Diode`. Printed beside the drawing: `For Wiring, see Pages 146 or 147.`
