Source: `Stern_1980_Quicksilver_Manual.pdf` (IPDB machine 1895, "English Manual [Stern Electronics]", 35 pages, a 300 dpi bilevel scan with no text layer), PDF page 21, left edge: the right-hand part of the playfield wiring diagram (title block on this page: `STERN ELECTRONICS INC.`,
`WIRING DIAGRAM FOR QUICK SILVER`, `SHEET #2 OF 3`, drawing `12B-432-S-117`). The crop overlaps the right edge of sheet A.

Transcribed by hand from the 300 dpi render:

- `RIGHT FLIPPER`: two windings with diodes and an end-of-stroke contact like the left flipper, fed from the same supply bus.
- `OUT-HOLE`: one coil with a diode, supply through a 1-amp slow-blow fuse labelled `1-AMP. SLO-BLO (-Y-)`. The supply bus
  is labelled `(Y)` and continues down the right edge through a second `1-AMP SLO-BLO` fuse.
- `RIGHT THUMP.` and `LOW THUMP.`: two coils on the `(Y)` bus.
- `RIGHT SLING SHOT` and `KICK-OUT HOLE`: two coils on the `(Y)` bus.
- `RIGHT D.T.`: one coil on the `(Y)` bus.

Return wires of the right-hand coils are the same wires listed on sheet A; the printed pin of the out-hole return is
`A3J1-5 (B-G)`, of the kick-out hole `A3J5-12 (B-Y)` and of the right drop-target bank `A3J5-12 (D-O)`. The same page-20
wire list prints A3J1-5 and A3J5-12 more than once; the Solenoid Driver Schematic of the same game
(excerpts `solenoid-driver-j5-pins` and `solenoid-driver-j2-pins`) settles which connector pin each coil really uses.
