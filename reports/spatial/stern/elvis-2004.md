# Elvis (Stern, 2004) spatial blockers

Retained VPX SHA-256 `d53202dea8620d92b6598894e71b26de59db1a0932234ceb5938f0844d22afc6`; script `51594f64207eca7afec821dea1ecd607d7cc756187d8ff63d7a815bb4c6c17ad`; 1119-file extraction manifest `43fad35f4be49537c2ff14cba101defb2f6dfe0117d15f4889642f92743a2fea`; manual `83593eb6de4c468c3acfb842c38a81563bc0f4bfbfa6d3a9ff39123b86342125`.

Bounds: `left=0 top=0 right=952 bottom=2115`. Every canonical coordinate is x/952 and y/2115 rounded to at most six places.

## Placement status

- `validated`: 0 devices
- `observed`: 78 devices
- `candidate`: 0 devices
- controlled `not_applicable` records: 54
- used devices with no placement record: 83

  - `device.q20-back-panel-flashers-x2`
  - `device.q21-back-panel-tcb-flasher`
  - `device.q23-upper-right-flipper-flashers-x2`
  - `device.q31-elvis-spot-light-flasher`
  - `lamp.1-rock-again`
  - `lamp.10-blue-suede-shoes`
  - `lamp.11-heartbreak-hotel`
  - `lamp.12-jailhouse-rock`
  - `lamp.13-all-shook-up`
  - `lamp.14-hits-completed`
  - `lamp.15-elvis-collected`
  - `lamp.16-top-10-completed`
  - `lamp.17-top-10-ladder-10`
  - `lamp.18-top-10-ladder-9`
  - `lamp.19-top-10-ladder-8`
  - `lamp.2-left-outlane`
  - `lamp.20-top-10-ladder-7`
  - `lamp.21-top-10-ladder-6`
  - `lamp.22-left-ramp-arrow`
  - `lamp.23-shook`
  - `lamp.24-left-ramp-note`
  - `lamp.25-top-10-ladder-5`
  - `lamp.26-top-10-ladder-4`
  - `lamp.27-top-10-ladder-3`
  - `lamp.28-top-10-ladder-2`
  - `lamp.29-top-10-ladder-1`
  - `lamp.3-left-return-lane`
  - `lamp.30-right-ramp-arrow`
  - `lamp.31-up`
  - `lamp.32-right-ramp-note`
  - `lamp.33-elvis-e`
  - `lamp.34-elvis-l`
  - `lamp.35-elvis-v`
  - `lamp.36-elvis-i`
  - `lamp.37-elvis-s`
  - `lamp.38-right-orbit-arrow`
  - `lamp.39-gift-from-elvis`
  - `lamp.4-right-return-lane`
  - `lamp.40-right-orbit-note`
  - `lamp.41-left-orbit-arrow`
  - `lamp.42-left-orbit-blue-suede-shoes`
  - `lamp.43-all`
  - `lamp.44-left-orbit-note`
  - `lamp.45-king-k`
  - `lamp.46-king-i`
  - `lamp.47-king-n`
  - `lamp.48-king-g`
  - `lamp.49-hound`
  - `lamp.5-right-outlane`
  - `lamp.50-dog`
  - `lamp.51-center-loop-arrow`
  - `lamp.52-center-loop-blue-suede-shoes`
  - `lamp.53-center-loop-note`
  - `lamp.54-lock`
  - `lamp.55-jackpot`
  - `lamp.56-super-jackpot`
  - `lamp.57-left-top-lane`
  - `lamp.58-middle-top-lane`
  - `lamp.59-right-top-lane`
  - `lamp.6-spot-note`
  - `lamp.60-heart`
  - `lamp.61-break`
  - `lamp.62-hotel`
  - `lamp.63-tcb-c`
  - `lamp.64-tcb-b`
  - `lamp.65-video-mode`
  - `lamp.66-gold-record`
  - `lamp.67-king-of-rock-n-roll`
  - `lamp.68-lite-extra-ball`
  - `lamp.69-encore-letter`
  - `lamp.7-scarf`
  - `lamp.70-graceland`
  - `lamp.71-special`
  - `lamp.72-extra-ball`
  - `lamp.73-encore-e-first`
  - `lamp.74-encore-n`
  - `lamp.75-encore-c`
  - `lamp.76-encore-o`
  - `lamp.77-encore-r`
  - `lamp.78-encore-e-last`
  - `lamp.8-tcb-t`
  - `lamp.9-hound-dog`
  - `switch.10-shooter-lane-exit`

## Projection classes

- **switch:** The centre of the VPX object the embedded script binds to each switch (trigger, spinner, hit target, kicker, slingshot wall, bumper, primitive). The trough switches 11-14 and the stacking opto 15, which the table does not model, are projected onto the release kicker BallRelease; the home switch 33 onto the figure's stand primitive pStand, which the mech moves; each end-of-stroke contact onto its flipper.
- **lamp:** None: every lamp the table fades is an insert overlay Light with no bulb or a Flasher sprite, so no lamp is placed.
- **solenoid:** The kicker, slingshot wall, bumper, flipper, trigger, gate or wall the script fires; the drop-target reset on the mean of its bank's five targets; the stepper phases 25-28 and the legs and arms coils 29 and 30 on the stand primitive pStand; flashers 22 and 32 on the script-driven glow Lights centred on their modelled Flupper domes. Flasher 23 is not placed: its faded Lights f23 and f23a show no bulb mesh and sit on no modelled socket.
- **gi:** The 6 members of the table's aGiLights collection that draw their bulb mesh, after collapsing co-located Lights; observed only, without per-string assignment. Members that show no bulb mesh sit on no bulb and are not placed.

## Unresolved physical geometry

- Every lamp 1-78 is unplaced: the table draws 1-59, 63 and 64 with insert overlay Lights that have no bulb and 57-78 with Flasher sprites; placing them needs the lamp location drawing (DR. 5) fitted to the table by a callout check, or playfield photographs.
- The back-panel flashers 20 and 21, the back-panel lamps 60-62 and 73-78 and the back panel's ten G.I. bulbs stand on the back panel behind the playfield's rear edge; the table models the flashers as Flupper domes on that plane outside the playfield bounds, so they need the back-panel elevation rule and a drawing fit.
- The Elvis spot light 31 is drawn by the table only with Flasher sprites; DR. 7 draws it right of the stepper callouts.
- The upper right flipper flasher 23 (two #906 bulbs) is drawn by the table only with bulb-mode Lights that show no bulb mesh and sit on no modelled socket; DR. 7 draws it twice along the right edge.
- The shooter lane exit switch 10 has no table object.
- The trough switches 11-15, the home switch 33, the stepper phases 25-28, the legs and arms coils 29 and 30, the drop-bank reset 3 and the end-of-stroke switches 81 and 83 are projections onto mechanism objects.
- No placement has been checked against the factory location drawings (DR. 4, DR. 5, DR. 7) by a callout fit, so every placement stays observed.
- The table draws 6 G.I. bulbs against the 48 the G.I. page counts; 26 more aGiLights members show no bulb mesh and are not placed, and matching the placed ones to the drawing's circuit discs is not done.

## Promotion decision

partial: unplaced lamps and back-panel devices, projections, and placements the drawings do not yet confirm keep spatial_placement in coverage.missing.
