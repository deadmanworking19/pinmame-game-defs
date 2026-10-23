# Creature from the Black Lagoon (Bally, 1992) spatial blockers

Retained VPW v1.0 VPX SHA-256 `960ebdd19b1a0f6d88822add16bbaf8a05d11bd5f1b8b26dc387a6db21705def`; script `110d85325e33cbaf465f5a60f3aeeb2069329c55719435e7b76380748ba70ea6`; 3345-file extraction manifest `bd06526a5fd2c0327964545403eb276fc7be4e982c2b7f1f1e5b065be5752cf9`; manual `d84d28a807505339f57676e0222adc6cc6fe7bef7371d31f9a9076ec33021d97`.

Bounds: `left=0 top=0 right=964 bottom=2162`. Every canonical coordinate is x/964 and y/2162 rounded to at most six places (factory-drawing measurements to three).

## Placement status

- `validated`: 87 devices
- `observed`: 30 devices
- `candidate`: 3 devices
- controlled `not_applicable` records: 85
- used devices with no placement record: 10 (`gi.string-0`, `gi.string-3`, `lamp.chase-91`, `lamp.chase-92`, `lamp.chase-93`, `lamp.chase-94`, `lamp.chase-95`, `lamp.chase-96`, `lamp.chase-97`, `lamp.chase-98`)

## Projection classes

- **switch:** The VPX collision object the retained script binds to each matrix switch (trigger, kicker, target, bumper or slingshot wall), observed and validated where the switch drawing's own callout agrees within the limit. Switches 16 and 17, whose callouts the drawing transposes, keep the table object without a check. The trough switches 55-58, which the drawing labels with pointerless balloons one ball position away, keep the table's ball seats without a check and stay observed. The ramp switches 18, 35, 36, 61, 62 and 64, whose table triggers sit 0.08 or more from the drawn switches or are swapped (62/64), and the lift ramp switch 38, which has no table object, are measured on the switch drawing and stay observed.
- **lamp:** The Light each lamp's TimerInterval binds, observed and validated where the lamp drawing's callout agrees; 28, 37 and 44 place both bulbs. The sockets of the A-14305 and C-12709 boards (55-58, 63-68) and lamp 51, which the table models only as placeholders, are measured on the lamp drawing and stay observed; the Admit One lamp 18 on the back panel takes the drawing's x at the playfield's rear edge. The backbox letters 71-78 and the Start button lamp 88 are controlled not-applicable records.
- **solenoid:** The script-driven flasher Light, the popper kicker, the slingshot wall or the jet bumper for each solenoid, observed and validated where the solenoid drawing's own symbol agrees. The trough and outhole coils project onto the ball seats they kick and stay observed with them, and the flipper windings project onto the flipper pivots, without a check; the hologram push motor and the lift ramp coils are measured on the drawing.
- **gi:** The table's G.I. light collections for strings 1, 2 and 4, as candidates only: the lights are invisible light-map sources, not modelled sockets, and no drawing or bulb count locates G.I. bulbs.

## Drawing callout check

A placement is validated when its own callout on the factory location drawing (each callout paired with at most one placement of its label, nearest first) lands within 0.07 normalized of it under two least-squares fits of that page: one on independently read controls (jet-bumper caps and flipper pivots, or another crisp mechanism feature where balloons hide a pivot), and one, measured leave-one-out, on the page's other callout reads, from which any read beyond the limit is dropped. Placements without such a read keep their table status. Placements measured on a drawing are never checked against it. It validates 86 of the 88 table placements it checks ([seed](../../../tools/seeds/bally/creature-from-the-black-lagoon-1992-callouts.json)); the rest keep their observed status:

- `lamp.matrix-25.emitter`: callout 25 on 2-40, no callout of this label on the drawing.
- `lamp.matrix-26.emitter`: callout 26 on 2-40, no callout of this label on the drawing.

## Unresolved physical geometry

- The 32 #86 chase bulbs on the swirl ramp's three boards and the bowl's board: which bulbs belong to which of the eight strings (lamps 91-98) and which ramp boards G.I. 0 and G.I. 3 power are unresolved (conflict.chase-light-board-group-assignment), so lamps 91-98 and G.I. 0 and 3 have no placement.
- The general-illumination bulbs of strings 1, 2 and 4 rest on the retained table's light-map sources; no modelled socket, drawing or count locates them, so they are only candidates.
- The trough switches 55-58 and the trough and outhole coils rest on the table's ball seats, which the switch drawing does not mark, so they stay observed.
- Drawing measurements stay observed: no retained table object corroborates their positions.

## Promotion decision

partial: the factory drawings validate most table placements, but the chase-light strings and G.I. 0 and 3 cannot be placed until their wiring is settled, the G.I. strings are only candidates, and the trough and the drawing measurements stay observed.
