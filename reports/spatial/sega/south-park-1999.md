# South Park (Sega, 1999) spatial blockers

Retained VPX SHA-256 `39075dcb6ca5fb8f164a9d48b6e4b393fef85eae3607892f19f28318a4f8d1a8`; script `63881ced8ea42097d1dee146ee2df7b752160dbd9f04bbfd826b90b513e408bf`; 884-file extraction manifest `aae0b1258026105af3e02909e77dbf9d258be8138705ea40968e68acbb2e512c`; manual `c25723bfc9bb8726c12b1fc3f9a6d74df60ebe8ce7da1937e06a38ace1b59f0a`.

Bounds: `left=0 top=0 right=952 bottom=2162`. Every canonical coordinate is x/952 and y/2162 rounded to at most six places.

## Placement status

- `validated`: 0 devices
- `observed`: 131 devices
- `candidate`: 0 devices
- controlled `not_applicable` records: 84
- used devices with no placement record: 0


## Projection classes

- **switch:** The centre of the VPX object the embedded script binds to each switch (trigger, target wall, kicker, slingshot wall, bumper). The trough switches and the stacking opto, which the table does not model, are projected onto the release kicker BallRelease; the three under-trough switches onto the kickers that pulse them; each end-of-stroke contact onto its flipper.
- **lamp:** The centre of the Light InitLamps assigns to each lamp.
- **solenoid:** The kicker, slingshot wall, bumper or flipper the script fires, and for flashers the script-driven Lights. The auto launch is placed on the table's Plunger; the toilet seat on the ToiletSeat primitive; the Mr. Hankey coils on the MrHankey primitive; the Kenny coils and the Kenny bulb of flasher 30 on the Kenny primitive. The UK-only coils 21-23, which the US table does not model, are projected where the coil location drawing draws them: the two outlane rollovers and the flippers' midpoint.
- **gi:** The Light members of the table's GI collection, each render-double cluster placed on its member that draws the bulb (show_bulb_mesh); the three turbo-bumper-cap lights on matrix lamps 38-40 are excluded; observed only, without per-string assignment.

## Unresolved physical geometry

- The trough switches 10-15 and the under-trough switches 43, 44 and 48 are not modelled by the table; their placements are projections onto mechanism objects.
- The UK-only coils 21-23 are projections from the coil location drawing onto US-table objects.
- The toy coils (5, 6, 13, 14, 19, 20) and the Kenny flasher bulb are placed on the primitives the script animates, not on the coil bodies under the playfield.
- No placement has been checked against the factory location drawings by a callout fit, so every placement stays observed.
- The table models 29 G.I. sockets against the 31 playfield bulbs the G.I. page prints (its three GI lights in the turbo bumper caps sit on matrix lamps 38-40 and are excluded); matching the 29 table bulbs to the circuit-labelled sockets of the page's mirrored bottom-view drawing, which would locate the two the table lacks, is not done.

## Promotion decision

partial: every used device has a placement or a controlled not-applicable record, but projections and placements the drawings do not yet confirm keep spatial_placement in coverage.missing.
