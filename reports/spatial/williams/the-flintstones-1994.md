# The Flintstones (Williams, 1994) spatial review

Status: observed. Every switch, coil, motor and lamp that has a playfield location is placed from the retained table or carries a controlled `not_applicable` record, except the playfield flashers, the left up/down gate and the G.I. strings, which have no coordinate. No placement was checked against the manual's location drawings, so every placement stays `observed` and the record stays at `machines/partial/williams/the-flintstones-1994.json`.

The geometry source is the retained known-working `The Flintstones (Williams 1994) v1.25.7.vpx` (SHA-256 `88c7a36ade06cf2df8aa78e2ede85d040b11330e45dff69897cc3402f2105384`); its embedded script (SHA-256 `352efc7660b8257df9f3534c5b01262de8ce10934047907e1a5a8e64e124f94d`) is the runtime binding authority. Exact playfield bounds are `left=0 top=0 right=964 bottom=2162`; every table coordinate is x/964 and y/2162 rounded to six places.

## Evidence decisions

- The embedded script is the runtime authority; the July 1994 operations manual and its two bulletins are the physical inventory, construction and wiring authority; the game ROM's own name tables settle the semantic names where the printed tables disagree; pinned PinMAME owns controller topology; the retained table supplies geometry for named objects.
- The script's InitLamps binds each light of its Lamps collection by the two digits of its name (LTnn), so every lamp placement names its object. Each lamp sits on its bulb light (is_bulb_light, no image), not on the LTnn insert overlay beside it; the six two-bulb lamps are placed at both bulbs.
- The trough optos, the drop-target reset coils and the two right flippers' shared button are documented in the definition's device notes.
- Flashers 17-21 also light #906 backbox insert flashers, and 26/27 are backbox-only; G.I. strings 2-4 also feed #555 backbox bulbs. None of those is placed.

## Blockers

- Every placement comes from one community table's named objects and none was checked against the manual's switch, lamp or solenoid location drawings, so all of them stay observed. Promotion needs a callout check of those drawings. The lamp placements are the table's bulb lights, which sit at its insert centres and draw no bulb mesh; until that check, nothing but the table puts a socket there.
- Flashers 17-22, 24, 25 and 28 have no coordinate: the retained table drives light objects (Fl17-Fl28 and full-playfield FlPf overlays) that paint light rather than mark sockets, and no socket was measured on the location drawing.
- The Left Up/Down Gate (36) has no coordinate: the location drawing's callout 36 ends at the rear left beside the Boulder Machine, about 0.3 of the table width from the Gate4 the retained script binds it to.
- G.I. strings 1-5 have no coordinate: the manual prints no per-string socket list and the retained table places no G.I. bulb per string.
- The trough optos (31-35) are projected onto the trough exit and the drop-target reset coils (5, 6) onto the mean of their bank's targets; the table models none of them.

## Explicit projections

- pinmame.input.switch 31: Projected onto the trough exit kicker BallRelease: the retained table models no trough opto objects (its cvpmTrough holds the balls virtually and exits them at BallRelease), so the five trough optos share the exit position.
- pinmame.input.switch 32: Projected onto the trough exit kicker BallRelease: the retained table models no trough opto objects (its cvpmTrough holds the balls virtually and exits them at BallRelease), so the five trough optos share the exit position.
- pinmame.input.switch 33: Projected onto the trough exit kicker BallRelease: the retained table models no trough opto objects (its cvpmTrough holds the balls virtually and exits them at BallRelease), so the five trough optos share the exit position.
- pinmame.input.switch 34: Projected onto the trough exit kicker BallRelease: the retained table models no trough opto objects (its cvpmTrough holds the balls virtually and exits them at BallRelease), so the five trough optos share the exit position.
- pinmame.input.switch 35: Projected onto the trough exit kicker BallRelease: the retained table models no trough opto objects (its cvpmTrough holds the balls virtually and exits them at BallRelease), so the five trough optos share the exit position.
- pinmame.output.solenoid 5: Projected to the mean of the three 3-bank drop targets (HitTarget Sw45-Sw47): the reset coil sits under the bank and the retained table models no coil object.
- pinmame.output.solenoid 6: Projected to the mean of the four 4-bank drop targets (HitTarget Sw41-Sw44): the reset coil sits under the bank and the retained table models no coil object.

## Counts

- Placements: 140
- Validated input addresses: 0
- Observed-only input addresses: 46
- Validated output bindings: 0
- Observed-only output bindings: 85
- Output bindings with no coordinate: 15
- Inputs with a controlled `cabinet_or_service` record: 18
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 3
- Inputs with a controlled `unused` record: 12
- Outputs with a controlled `cabinet_or_service` record: 5
- Outputs with a controlled `virtual` record: 14

## Promotion decision

Refused. `coverage.missing` is `["spatial_placement"]`: every coordinate rests on one community table without a drawing check, and the playfield flashers, the left up/down gate and the five G.I. strings are not placed at all.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/the-flintstones-1994/extracted-vpxtool.manifest.json`, SHA-256 `c748c3b416a8cb8b8974c679fe8dcb064f267dd1fb9f650b0bce597bfc4b0d88`, 1144 files, 386155547 bytes.
- Operations manual SHA-256 `6c615147ac98e217585858ad17c2dfc56d86897ee6934ea03f2e58a1599d94bb`.
