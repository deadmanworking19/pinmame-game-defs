# Space Station (Williams, 1987) spatial review

Status: observed. The machine record stays `partial` at `machines/partial/williams/space-station-1987.json`; its spatial dimension stays open because of the 5 spatial blockers below.

The geometry source is VPW's retained `Space Station (Williams 1987) VPW v1.0.vpx`, SHA-256 `3d595e21bc52cf39ba2741902526a0bcbce45de101490d24e3127dcefa4d1d25`, whose embedded script (SHA-256 `075c55dd8ef256266c58cf6033433f84cef231823704af8136b9414d593cb6ff`) is the pinned known-working v1.0.1 script (SHA-256 `0d47d55e2f5cbf6208ace2b01a1beaf30ff0e6e94d51c6712adc17eb282ae9e9`) apart from whitespace and one trailing changelog comment, so every cited script line is the same in both. Bounds are `left=0 top=0 right=952.941 bottom=1976.471`; every coordinate is x/952.941 and y/1976.471, rounded to at most six places.

## Evidence decisions

- A placement is the centre of the table object the script binds to the address: a trigger, kicker, hit target, bumper or drop-target wall for a switch, the `lN` light vpmMapLights binds for each lamp, the script-driven `fN` lights for each flasher, the bulb lights of the GI and gi_green collections for the playfield G.I., and the slingshot walls, bumpers and kickback for their coils.
- Sensors and coils with no table object of their own (the Space Station optos and motor, the outhole, feeder, popper, drop-reset and dock coils) are documented projections onto their own mechanism's object.
- Backbox and cabinet devices take controlled `not_applicable` records: the insert-board lamps 37, 41, 46-49 and 57, the backbox flashers 30 and 31, the insert G.I. (11), the knocker, the A/C relay, the cabinet, lane-change and diagnostic switches, the Country jumper and the four displays.

## Explicit projections

- Switch 52: Projected onto the Space Station's rotation centre (the pivot of Primitive BM_SS_01, which the script turns about its own position): the C-11872 opto board sits on the station's shaft under the playfield, and the script writes 52 from its modelled angle rather than from an object.
- Switch 53: Projected onto the Space Station's rotation centre; see switch 52.
- Solenoid 1: Projected onto the drain kicker sw10 the script kicks from; the outhole kicker coil has no object of its own.
- Solenoid 2: Projected onto the trough kicker sw11 the script releases from; the C-9638-3 feeder has no object of its own.
- Solenoid 3: Projected onto the left popper's switch trigger sw41, whose ball the script lifts; the D-11335-1 popper coil has no object of its own.
- Solenoid 4: Projected onto the right popper's switch trigger sw42, whose ball the script lifts; the popper coil has no object of its own.
- Solenoid 6: Projected onto the bank's middle drop target sw58; the reset coil sits below the bank and has no object of its own.
- Solenoid 8: Projected onto the single drop target sw33; its reset coil sits below it and has no object of its own.
- Solenoid 16: Projected onto the Space Station's rotation centre (the pivot of Primitive BM_SS_01); the motor sits below the station on its shaft.
- Solenoid 17: Projected onto the right lock's switch trigger sw45, whose ball the script kicks; the dock kicker has no object of its own.
- Solenoid 32: Projected onto the left lock's switch trigger sw47, whose ball the script kicks; the kickbig has no object of its own.

## Clamped placements

- Solenoid 15, f15: raw y -12.5083 clamped to 0.0
- Solenoid 15, f15b: raw y -12.8071 clamped to 0.0
- Solenoid 15, f15c: raw y -12.8071 clamped to 0.0
- Solenoid 29, f29: raw y -12.7503 clamped to 0.0
- Solenoid 29, f29b: raw y -12.1875 clamped to 0.0

## Counts

- Placements: 209 (observed 198, validated 11)
- Located input addresses: 48
- Located output bindings: 80
- Inputs with an omitted spatial key: 1
- Outputs with an omitted spatial key: 0
- Inputs with a controlled `cabinet_or_service` record: 16
- Inputs with a controlled `dip_switch` record: 1
- Inputs with a controlled `unused` record: 11
- Outputs with a controlled `cabinet_or_service` record: 11
- Outputs with a controlled `internal_nonvisual` record: 1
- Outputs with a controlled `unused` record: 2
- Outputs with a controlled `virtual` record: 20

## Blockers

- Switch 34 (West German scoreboard switch): fitted only on West German machines, and no source gives its location, so it has no spatial key.
- No placement has been checked against the manual's numbered location drawings: every table object placement (switches, lamps, flashers, the slings, bumpers and kickback, and the G.I.) keeps the table's `observed` status. A callout check of the switch (printed page 50), lamp (53) and solenoid (54) drawings would validate the ones that land on their callouts.
- Solenoids 9 and 10 (playfield white and green G.I.): the placements are the bulb lights of the retained table's GI and gi_green collections. The manual prints no G.I. bulb count or layout and a table's grouping is not the machine's wiring, so they stay observed without a quantity.
- Solenoids 15 and 29 (top panel flashers): the five dome lights sit 12-13 units behind the rear edge and are clamped to it; the panel is upright, so the clamped point is the panel's foot, not the dome.
- Switches 50 and 54: the table binds them to the opposite rubbers from the manual and the ROM; the placements follow the machine, so they rest on the table's other object and stay observed.

## Promotion decision

Every controller address is enumerated with a semantic disposition, every printed wiring detail is recorded, the mechanisms and both production insert boards are covered, polarity is settled by the ROM's Switch Levels test, and every playfield device has a placement. Promotion to `author_ready` is refused because the table placements are not checked against the factory drawings and the G.I. placements come only from the table's grouping, so `coverage.missing` is `["spatial_placement"]`.
