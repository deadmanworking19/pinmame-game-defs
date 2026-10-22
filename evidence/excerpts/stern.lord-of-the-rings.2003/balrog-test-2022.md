# Balrog Test

Transcribed from `Lord_of_the_Rings_Manual-2022.pdf`, PDF page 42, the LOTR TESTS "BROG" test (complete text of the test's block). The page's figures label `Sw. 31` and `Sw. 32` on the motor assembly and `Sw. 28` on the Balrog assembly, each drawn with `Top Edge of Playfield.` marked.

> Selecting the "BROG" Icon will bring up the BALROG TEST MENU with the "RUN" Mini-Icon flashing. Note: Upon selection of the "BROG" Icon, (and with the Power Interlock Switched pulled out), the motor will cycle, moving the Balrog, blocking the entrance of the Center Ramp (Fig. 1). This test is provided to allow a method of testing the Balrog Open (Sw. 31), Balrog Closed (Sw. 32) and Balrog (Bash) Hit (Sw. 28) and Balrog Motor (Q32) operation in conjunction with the Motor Relay Board (Q20). Switches 31, 32 & 28 are in a Normally Closed state (Switches 31 & 32 are under the playfield on the Motor Assembly; Switch 28 is located inside the Balrog Assembly). With the Balrog now blocking the Center Ramp (Fig. 1), with ball-in-hand, roll the ball at the front hit plate (knocking the Balrog Over), and note the Bash (Sw. 28, Balrog Hit) [box] box will turn [solid], thus indicating proper operation.
>
> Select and activate the "RUN" Mini-Icon to cycle the Motor. As the Balrog opens the Center Ramp (Fig. 2) and comes to a rest, the Balrog Closed (Sw. 32) will open, the solid [box] box will turn [empty] and Balrog Open (Sw. 31) will close, the [empty] box will turn solid [box].
>
> For more details of the Switches & Coils (Part Numbers & views) tested on this and the previous page, review Section 4, Chapter 2, Drawings for Major Assemblies & Ramps, Pages 93-97.

The bracketed words stand for the small box glyphs the text prints inline (a hollow and a solid square); they are not legible as text in the PDF's text layer.

Two things the text says that the definition does not adopt as written:

- It calls the motor `Q32`. The coil chart (DR. 6) and the coil location drawing (DR. 7) print the Balrog motor as `Q22` and the Balrog flasher as `Q32`, so `Q32` here is a misprint for the motor.
- "Normally Closed state" describes the switches at their end positions, not the contact the matrix sees at rest: the same paragraph says Sw. 32 reads closed with the Balrog closed and Sw. 31 closes once it comes to rest open, and every retained known-working script holds each of 28, 31 and 32 at public 0 except while the Balrog is hit or parked at that switch's end. On Whitestar public 1 is the CPU's closed-contact reading, so the matrix-facing contacts rest open.
