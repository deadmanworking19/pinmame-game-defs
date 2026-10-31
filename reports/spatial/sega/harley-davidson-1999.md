# Harley-Davidson (Sega, 1999) spatial blockers

Sega's model 67 is the production run Stern continued as its 1st edition (IPDB 4453 and 4455), one playfield and one wiring, so every placement comes over unchanged from the Stern record's placement seed tools/seeds/stern/harley-davidson-1999-spatial.json, built from the retained table, whose title calls it the Sega 1999 machine; tools/curate_harley_davidson_sega.py derives this record from tools/curate_harley_davidson.py.

Retained VPX SHA-256 `349bc4e4d68173138928baed0a0fbfdb0d04ef78ca07dfbcfdf8d2583255cf37`; script `eb0960bc9670cd367f7f2ce838e2969d4546b98abe5c8fc4d4df3fd53d32bc50`; 691-file extraction manifest `c92e6bba4c9c6b5400b5e2a24e8bbd7f8d7018b8ef4337404291f1bd96fb17fc`; manual `a10e91542f9c8ab965d18908626114d1d03cba499f36fa47751045e8adae4731`.

Bounds: `left=0 top=0 right=1000 bottom=2000`. Every canonical coordinate is x/1000 and y/2000 rounded to at most six places.

## Placement status

- `validated`: 0 devices
- `observed`: 125 devices
- `candidate`: 0 devices
- controlled `not_applicable` records: 75
- used devices with no placement record: 12

  - `device.q20-scoop-flasher`
  - `device.q25-left-drop-target-flashers-x2`
  - `device.q27-turbo-bumper-flashers-x4`
  - `device.q29-motorcycle-flashers-x4`
  - `device.q30-super-vuk-flashers-x2`
  - `device.q31-right-drop-target-flashers-x2`
  - `device.q32-speedometer-flashers-x2`
  - `lamp.57-stop-light-green`
  - `lamp.58-stop-light-yellow`
  - `lamp.59-stop-light-red`
  - `lamp.72-next-city`
  - `switch.27-right-ramp-mid`

## Projection classes

- **switch:** The centre of the VPX object the embedded script binds to each switch (trigger, gate, spinner, hit target, kicker, slingshot wall, bumper). The trough switches 11-14 and the stacking opto 15, which the table does not model, are projected onto the release kicker BallRelease; the motorcycle-trough switches 41-44 onto the kicker Kicker1 its ball stack uses; the lift switches 35 and 36, which a cvpmMech models without objects, onto Kicker1; each end-of-stroke contact onto its flipper.
- **lamp:** The centre of the Light the lamp fader drives for each lamp; lamp 70's two sockets on its two Lights.
- **solenoid:** The kicker, slingshot wall, bumper, flipper, trigger or wall the script fires; the drop-target resets on the mean of their bank's four targets; the motor relay on Kicker1 under the motorcycle; for flashers 26 and 28 the script-driven Lights centred on their modelled dome primitives. The UK-only deflectors 21 and 22, which the US table does not model, are projected onto the outlane rollovers the cabinet wiring diagram's UK note names.
- **gi:** The 20 Light members of the table's GI collection, each a single socket; observed only, without per-string assignment.

## Unresolved physical geometry

- The trough switches 11-15, the motorcycle-trough switches 41-44 and the lift switches 35 and 36 are not modelled by the table; their placements are projections onto mechanism objects.
- Switch 27 (right ramp mid) has no bound table object; the table's unbound wire gate Trigger27q on the ramp near the top centre is a candidate, not used.
- The stop light lamps 57-59, the Next City lamp 72 and the flashers 20, 25, 27 and 29-32 are drawn by the table only with Flasher overlay objects or not at all; they need the factory drawings (DR. 5 and DR. 7) or playfield photographs to place.
- The UK-only deflectors 21 and 22 are projections onto US-table objects.
- No placement has been checked against the factory location drawings by a callout fit, so every placement stays observed.
- The table models 20 G.I. sockets against the 38 playfield sockets the G.I. page draws; matching them to the circuit-lettered sockets of its mirrored bottom-view drawing is not done.

## Promotion decision

partial: devices without placements, projections, and placements the drawings do not yet confirm keep spatial_placement in coverage.missing.
