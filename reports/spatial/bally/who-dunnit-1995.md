# WHO dunnit spatial blockers

Retained VPX SHA-256 `a0f18c07f98ec7dce96cc030eb11af11a0c28d0d1cffb5390744067b9221e2a9`; script `034fe6483660fbc9516aa15a4727d8dc6da0cfb3db0321b0c1357523967ccd44`; 631-file extraction manifest `0fd20d012d8219583a8222b51a0997ca4876247cc9ec19352e5a06d270d3643c`; manual `5fa08344d905c9730c86c6baee79b43e6a4a1c4e2230f67a08c2973b57bc714e`.

Bounds: `left=0 top=0 right=953 bottom=2128`. x=object_x/953; y=object_y/2128; player view, rear y=0, apron y=1; values rounded to six decimals.

32 devices keep candidate placements after the drawing callout check; 0 used devices lack even a candidate. The 45 newly projected mechanism/actuator devices remain physically unplaced: a shared assembly anchor is not a hidden contact, coil, or bulb centre. Backbox flasher branches and the complete G.I. socket census remain unmeasured.

## Retained registers and projection classes

The [VPX object register](../../../tools/seeds/bally/who-dunnit-1995-spatial.json) has SHA-256 `e6c9f386a0e7b420893cd4736b89236ef3e25c68b36067ca4b743508588bd885`; the [G.I. bulb-mesh register](../../../tools/seeds/bally/who-dunnit-1995-gi-candidates.json) has SHA-256 `feb5185273d8f36596e75ec7753a4ff1a1d962a001005593c8b14bc38ae999d1`. The [reviewed geometry register](../../../tools/seeds/bally/who-dunnit-1995-geometry.json) has SHA-256 `4ece3a02cc9b7b579c062a79a0b8d3c3fc73cfc71de691c77d1897bfccc18035` and 47 candidate records. The JSON form embeds their source hashes, world-VPU or polygon centre definitions, projection classes, and uncertainty.

- **switch (16 candidate devices):** Exact-name VPX collision object centre for matrix switch or F5 Spinner, candidate, and validated where drawing_callout_check agrees; cabinet, EOS and always-closed positions use controlled not_applicable.
- **lamp (3 candidate devices):** Exact LNN VPX Light centre, candidate, and validated where drawing_callout_check agrees. L16/L17/L18 glow helpers are excluded.
- **gi (3 candidate devices):** Script collection members GI_Left/GI_Right/GI_Top with bulb mesh; 11/10/28 retained. Other collection members are glow/reflection leads, not sockets. Factory GI socket quantity is unknown. All five strings' table wiring/bulb/location claims and backbox exclusions remain candidate: the board layout shows J120/J121, but PDF 158–159 omits J112–J127 pin destinations and supplies no branch/placement corroboration.
- **actuator (10 candidate devices):** Named VPX mechanism anchor or visible effect projection only. No projection is called a hidden winding, motor body or physical bulb centre.
- **flasher_and_coil (0 candidate devices):** 45 devices use 46 VPX mechanism projections, validated where their own PDF 129 callout reaches the anchor within 0.07 under drawing_callout_check and candidate otherwise; flasher 14 uses the factory drawing instead. World-transformed OBJ bounds locate collidable primitives. Cup, reel, target, ramp, post and flipper anchors are not hidden coil or sensor centres; flasher domes and named Light proxies are not proven bulb centres. Backbox branches have no invented playfield point.
- **manual_drawing (0 candidate devices):** PDF 127 and PDF 129 have separate least-squares affine fits from eight control features read by eye on the native renders (RMS about 6-7 VPU, leave-one-out at most about 20 VPU). Their overlay identity checks are superseded by drawing_callout_check, which reads every callout and decides validation; they supply two candidate coordinates: switch 37 and flasher 14, whose leaders end at a ramp bracket the table does not model there. No balloon centre is used as a device coordinate. The earlier terra fit.json (session-20260930) is rejected: its control pixels were computed from the VPX coordinates through its own frame formula and sit 10-17 px from the drawn symbols, so its sub-VPU residuals reconcile nothing.
- **factory_drawing_measurement (0 candidate devices):** Candidate coordinate measured on a factory location drawing at the device symbol where a leader ends, through that page's independently read fit; used only where no retained table object sits at the factory position.

## Factory drawing reconciliation

Control pixels were read by eye on gridded native crops of the retained 300 dpi renders: jet bumper ring centres, flipper pivot circles, two flasher domes and the left lock cup. They are paired with the exact retained VPX object centres and fitted per page with a least-squares affine. Measured device points are factory device symbols at leader ends, never callout balloons.

- **pdf-127** (PDF 127, printed 2-45, Switch Locations (continued)): 8 controls, RMS 5.7 VPU, largest leave-one-out 13.4 VPU.
- **pdf-129** (PDF 129, printed 2-47, Solenoid/Flasher Locations (continued)): 8 controls, RMS 7.0 VPU, largest leave-one-out 19.9 VPU.
- `switch.matrix-37` measured at (49.1, 323.2) VPU, ±20 VPU, replacing `sw37` (121 VPU away).
- `solenoid.14` measured at (42.2, 343.2) VPU, ±60 VPU, replacing `Flasherlight6` (204 VPU away).
- pdf-125: All 60 placed playfield lamps land on their own printed lamp symbol or leader end (overlay through the page frame x=(u-902)/729, y=(v-460)/1680; leader-only clusters 25-28, 37-38, 46, 61-68, 71-72, 78, 83-84 inspected zoomed). Identity check only; the frame overlay carries about 15 VPU of systematic offset. Superseded by the 2026-10-01 drawing callout check (tools/seeds/bally/who-dunnit-1995-callouts.json), which follows each leader to its end: the leaders of lamps 62 and 64 end at other inserts and 72's cannot be followed through the ramps.
- pdf-127: Placed switches land on their own leader ends except 37 (re-placed from this drawing) and 41, whose invisible subway trigger sits about 40 VPU from its leader end; trough 31-35 remain whole-mechanism projections. The drawing callout check also leaves switches 43, 71 and 74 unconfirmed.
- pdf-129: Coil and flasher anchors land on their own items except 14 (re-placed from this drawing) and 20, whose Flasherbase5 dome sits about 60 VPU from the bracket its leader marks; 1/2 are effect anchors, not coil mounts. The drawing callout check also leaves the trough and auto-plunger anchors 1/2 unconfirmed.
- Rejected: Its 'hand-read' control pixels equal its own frame formula applied to the VPX coordinates (switch 63: 914 + 349.2/953*700 = 1170.5) and sit 10-17 px from the drawn bumper and lamp symbols, so its sub-VPU residuals are not a drawing measurement and reconcile nothing.

## Drawing callout check

A placement is validated when its own callout on the factory location drawing (each callout paired with at most one placement of its label, nearest first) lands within 0.07 normalized of it under two least-squares fits of that page: one on independently read controls (jet-bumper caps and flipper pivots, or another crisp mechanism feature where balloons hide a pivot), and one, measured leave-one-out, on the page's other callout reads, from which any read beyond the limit is dropped. Placements without such a read keep their table status. Placements measured on a drawing are never checked against it. It validates 110 of the 137 table placements it checks ([seed](../../../tools/seeds/bally/who-dunnit-1995-callouts.json)); the rest keep their candidate status:

- `lamp.62.candidate-1`: callout 62 on pdf-125, 0.173 normalized away.
- `lamp.64.candidate-1`: callout 64 on pdf-125, 0.187 normalized away.
- `lamp.72.candidate-1`: callout 72 on pdf-125, 0.209 normalized away.
- `output.01.trough`: callout 1 on pdf-129, 0.094 normalized away.
- `output.02.auto-plunger`: callout 2 on pdf-129, 0.149 normalized away.
- `output.08.right-front-popper`: callout 8 on pdf-129, no callout of this label on the drawing.
- `output.23.reel1`: callout 23 on pdf-129, no callout of this label on the drawing.
- `output.24.reel1`: callout 24 on pdf-129, no callout of this label on the drawing.
- `output.25.reel2`: callout 25 on pdf-129, no callout of this label on the drawing.
- `output.26.reel2`: callout 26 on pdf-129, no callout of this label on the drawing.
- `output.27.reel3`: callout 27 on pdf-129, no callout of this label on the drawing.
- `output.28.reel3`: callout 28 on pdf-129, no callout of this label on the drawing.
- `switch.12.left-reel-index`: callout 12 on pdf-127, no callout of this label on the drawing.
- `switch.25.center-reel-index`: callout 25 on pdf-127, no callout of this label on the drawing.
- `switch.31.trough`: callout 31 on pdf-127, 0.299 normalized away.
- `switch.32.trough`: callout 32 on pdf-127, 0.248 normalized away.
- `switch.33.trough`: callout 33 on pdf-127, 0.198 normalized away.
- `switch.34.trough`: callout 34 on pdf-127, 0.150 normalized away.
- `switch.35.trough`: callout 35 on pdf-127, 0.115 normalized away.
- `switch.41.candidate-1`: callout 41 on pdf-127, 0.119 normalized away.
- `switch.43.candidate-1`: callout 43 on pdf-127, 0.092 normalized away.
- `switch.48.right-reel-index`: callout 48 on pdf-127, no callout of this label on the drawing.
- `switch.66.three-bank`: callout 66 on pdf-127, no callout of this label on the drawing.
- `switch.67.three-bank`: callout 67 on pdf-127, no callout of this label on the drawing.
- `switch.68.three-bank`: callout 68 on pdf-127, no callout of this label on the drawing.
- `switch.71.candidate-1`: callout 71 on pdf-127, 0.134 normalized away.
- `switch.74.up-down-ramp`: callout 74 on pdf-127, 0.153 normalized away.

## Unresolved physical geometry

- No complete factory G.I. socket census or backbox/cabinet bulb coordinates. G.I. table locations remain candidate without J120/J121 destination corroboration; PDF 158–159 omits J112–J127 connector-list entries.
- Hidden trough optos, reel indexes, bank/ramp limit contacts, coil bodies and flipper E.O.S. contacts have only whole-mechanism or output-effect projections.
- Switch 41's invisible subway trigger sits about 40 VPU and flasher 20's Flasherbase5 dome about 60 VPU from the parts their PDF 127/129 leaders mark; neither is re-placed from a single leader reading.
- One derivative VPX lineage and manual diagrams do not establish all physical centres or prototype geometry.

## Missing placements

None. Every used device has a candidate or controlled non-playfield status.
