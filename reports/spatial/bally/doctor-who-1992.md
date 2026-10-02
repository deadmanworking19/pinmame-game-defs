# Doctor Who (Bally, 1992) spatial blockers

Retained VPX SHA-256 `99e92c977f98bfc129bfa3ab63fdfe803d37d0033198b475d518eb387f89a503`; script `6c31324ab557a70e4caa1920c6f4be3b96c4d97d7306bf96243584f80518e232`; 1888-file extraction manifest `ea94e6d690dc96a37a0a05091147eda8824189cc51ea0346072a9e7d03149550`; manual `2f430808b59050a5814f3c1671c6de1a993cabc6b0366810f73e3dc2995f9235`.

Bounds: `left=0 top=0 right=952.965 bottom=2162`. Every canonical coordinate is x/952.965 and y/2162.0 rounded to at most six places (factory-drawing measurements to three).

## Placement status

- `validated`: 116 devices
- `observed`: 26 devices
- `candidate`: 0 devices
- controlled `not_applicable` records: 65
- used devices with no placement record: 0

## Projection classes

- **switch:** Exact-name VPX collision object centre for the matrix switch, observed, and validated where the factory drawing's own callout agrees within the limit; switch 32 (the Home Opto, which the table models in software) is measured on the drawing instead.
- **lamp:** Exact VPX Light centre for each lamp's playfield bulb, observed, validated where the lamp drawing's callout agrees. Lamp 67 has no table Light and is measured on the drawing. Second bulbs on the speaker panel and back panel are not placed.
- **solenoid:** Named VPX mechanism anchor or visible effect projection, observed, validated where the solenoid/flasher drawing's own callout agrees; coils 27 and 28 have no table object and are measured on the drawing. Flipper windings print no callout and keep their table placements observed.
- **gi:** Per-string collections of table GI lights, collapsed where bulbs are stacked, observed only: the manual prints no per-string bulb count and no drawing locates GI bulbs, so none of these placements can be validated.

## Drawing callout check

A placement is validated when its own callout on the factory location drawing (each callout paired with at most one placement of its label, nearest first) lands within 0.07 normalized of it under two least-squares fits of that page: one on independently read controls (jet-bumper caps and flipper pivots, or another crisp mechanism feature where balloons hide a pivot), and one, measured leave-one-out, on the page's other callout reads, from which any read beyond the limit is dropped. Placements without such a read keep their table status. Placements measured on a drawing are never checked against it. It validates 119 of the 122 table placements it checks ([seed](../../../tools/seeds/bally/doctor-who-1992-callouts.json)); the rest keep their observed status:

- `switch.matrix-26.sensor`: callout 26 on pdf-119, 0.087 normalized away.
- `switch.matrix-27.sensor`: callout 27 on pdf-119, 0.123 normalized away.
- `switch.matrix-36.sensor`: callout 36 on pdf-119, 0.098 normalized away.

## Unresolved physical geometry

- The general-illumination bulb coordinates of strings 3-5 rest on the retained table's own grouping; no factory drawing or bulb count locates them, so their placements stay observed and spatial_placement stays in coverage.missing.
- The mini-playfield is modelled at a fixed playfield position; its lamps 56-58, the Doctor 7 flasher and the lock-hole switches 76-77 travel with it, so a playfield coordinate describes the lowest-level position only.
- Hidden mechanism contacts (trough, end-of-stroke, trap-door, reel-like cam optos) have whole-mechanism projections, not contact centres.

## Promotion decision

partial: every used device has a placement or a controlled not-applicable record, and the factory drawings validate most table placements, but the general-illumination bulbs cannot be validated from any retained drawing or count.
