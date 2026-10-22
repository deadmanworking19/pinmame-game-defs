# World Cup Soccer (Bally/Midway, 1994) spatial review

Status: validated. Every playfield switch, coil, flasher, lamp and GI address is placed, and every placement is validated; every other address carries a controlled `not_applicable` record. The machine record is `author_ready` at `machines/author-ready/midway/world-cup-soccer-1994.json`.

The matching source is the retained known-working `World Cup Soccer (Bally 1994) VPW v1.5.vpx` at SHA-256 `ab7e07fce7b589f9732f458a7a09ad08b87237852d97d7b5bf9a74f6b0f6d23d`. The retained `vpxtool` extraction produced the embedded script at SHA-256 `c18cfbaa4e8c3b67259ac5d6c7b6842dfdaaf308b0fd71a64071118b57ac73c5`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=952.941 bottom=2152.941`, and every canonical coordinate is x/952.941 and y/2152.941 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPW script is the runtime address and causality authority; the Midway operations manual is the physical inventory, quantity, polarity, wiring and location authority; pinned PinMAME owns controller topology; the retained table supplies geometry where the factory drawings confirm it.
- Every table placement the factory location drawings can check was checked against them: the lamp drawing (printed 2-45), the switch drawing (printed 2-47) and the solenoid/flasher drawing (printed 2-49), with every callout transcribed by an independent reader working only from the page. A placement is validated only when its own callout lands within 0.07 normalized of it under both the page's control fit and its callout fit (tools/drawing_callouts.py). The curator refuses to build while any checked placement disagrees.
- The jet bumpers follow the manual's absolute names: both drawings put switch 81 and coil 9 on the left bumper, 82 and 10 on the upper one, and 83 and 11 on the lower one, and the jet-bumper harness run shows the ROM firing 9, 10 and 11 for 81, 82 and 83. The retained table's switch bindings are rotated one step against that, a defect of that table.
- Where the table models no object at the socket the drawing marks (the second Goal and Skill Shot flasher bulbs) or models it with a baked-light-map source away from the socket (the ramp-sign bulbs, the lock-area and right top-corner flasher domes) or with a trigger away from the switch (ramp switches 74 and 75), the coordinate is a reproducible drawing measurement: the drawing pixel is pinned in the callout seed and normalized through that page's control fit, rounded to three places. Every page's controls include the drawn playfield frame's top-left, top-right and bottom-left corners, which match the table bounds within 0.013 leave-one-out, and, because the bottom-right corner is not drawn, the ball shooter switch 38 slot at the foot of the shooter lane, within 0.005 of the table trigger. Each measured socket lies inside the convex hull of its page's controls, so none is extrapolated; the curator refuses one that is not. Each measured socket is corroborated by physical photographs of production machines (IPDB machine 2811 and the Pinside gallery) or by the table object nearby; neither supplies a coordinate.
- Solenoid 34 (Loop Gate) sits on the retained table's one-way Gate Gate003 at the top of the right orbit, where callout 34 ends on the solenoid drawing and the Upper Playfield Parts drawing (printed 2-41) puts the Ball Gate Actuator Coil Assy. and the Ball Gate Special Assy., Left. The table never drives it.
- Solenoids 8 and 16 sit on the diverter flap the script swings (Primitive BM_diverterside01), where their shared callout ends; an earlier pass had put them on switch 71 at the left rail.
- Switch 65 (Tackle) cannot be checked: the switch drawing prints no callout 65. It keeps the script-bound trigger sw65, which lies on the rubber the drawing draws at the right side of the left ramp entrance, 0.034 from the Tackle lamp (38) on the lamp drawing.
- Each flasher's quantity counts its printed playfield and backbox bulbs, and only the playfield bulbs are placed: two for 18, 19, 22, 27 and 28, where the drawing draws two callouts, and one for the others. Lamp 53 (Goal) is drawn once and its two bulbs share one placement. Lamps 46 and 47 keep both of the table's Lights; lamps 71 and 78 have one bulb on each ramp sign.
- GI strings 0, 1, and 4 use the retained table's GILeft/GIRight/GITop emitter collections, matching the retained script's GIUpdate2 dispatch exactly; the drawings print no GI callouts. GI strings 2 and 3 are backbox insert-panel circuits and take a controlled `cabinet_or_service` record.
- The synthetic solenoid mirror at public address 51 (wcs_getSol's OR of solenoids 8 and 16) is declared virtual with a `virtual` spatial record so no duplicate diverter mechanism is ever placed on the playfield.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.

## Drawing callout check

Seed `tools/seeds/midway/world-cup-soccer-1994-callouts.json` (SHA-256 `d96ddad8db742f0019d09016ebec67e3363ddb16757e89f8a2d478ecf861eff6`); 135 placements checked, 135 validated.

- 2-45: 10 controls (RMS 0.0031, leave-one-out max 0.01), 60 callout pairs, 60 in the callout fit (leave-one-out max 0.035).
- 2-47: 9 controls (RMS 0.0022, leave-one-out max 0.006), 44 callout pairs, 44 in the callout fit (leave-one-out max 0.0565).
- 2-49: 9 controls (RMS 0.0026, leave-one-out max 0.0084), 31 callout pairs, 31 in the callout fit (leave-one-out max 0.0481).

Excluded from the check, with the seed's reasons: projections onto the mechanism they belong to (switches 36, 43, 44 and 48), the four flipper coils the solenoid drawing marks Not Shown, and switch 65.

## Drawing measurements

- `device.goal.emitter.2`: callout 18 on 2-49, pixel [1594.0, 755.0] (line_end), normalized (0.385, 0.176); corroborated by the table.
- `device.lock-area.emitter`: callout 26 on 2-49, pixel [1250.0, 1149.0] (symbol_centre), normalized (0.038, 0.352); corroborated by the photos.
- `device.ramp-rear.emitter.2`: callout 28 on 2-49, pixel [2095.0, 494.0] (symbol_centre), normalized (0.891, 0.059); corroborated by the photos.
- `device.skill-shot.emitter.2`: callout 19 on 2-49, pixel [2146.0, 1464.0] (symbol_centre), normalized (0.942, 0.491); corroborated by the photos.
- `lamp.matrix-71.emitter.1`: callout 71 on 2-45, pixel [2086.0, 1152.0] (symbol_centre), normalized (0.879, 0.374); corroborated by the photos.
- `lamp.matrix-71.emitter.2`: callout 71 on 2-45, pixel [1438.0, 906.0] (symbol_centre), normalized (0.226, 0.264); corroborated by the photos.
- `lamp.matrix-76.emitter`: callout 76 on 2-45, pixel [1461.0, 988.0] (symbol_centre), normalized (0.249, 0.3); corroborated by the photos.
- `lamp.matrix-77.emitter`: callout 77 on 2-45, pixel [2047.0, 1227.0] (symbol_centre), normalized (0.84, 0.407); corroborated by the photos.
- `lamp.matrix-78.emitter.1`: callout 78 on 2-45, pixel [2066.0, 1189.0] (symbol_centre), normalized (0.859, 0.39); corroborated by the photos.
- `lamp.matrix-78.emitter.2`: callout 78 on 2-45, pixel [1449.0, 947.0] (symbol_centre), normalized (0.237, 0.282); corroborated by the photos.
- `switch.matrix-74.sensor`: callout 74 on 2-47, pixel [2133.0, 948.0] (arrow_tip), normalized (0.918, 0.289); corroborated by the table.
- `switch.matrix-75.sensor`: callout 75 on 2-47, pixel [2131.0, 1244.0] (arrow_tip), normalized (0.916, 0.421); corroborated by the table.

## Explicit projections

- Switch 36: Projected onto the trough eject Kicker (Trigger/Kicker sw31, table object center): the retained script's SolTrough handler fires sw31.kick and vpmTimer.PulseSw 36 in the same event (no separate playfield object represents Trough Stack), and pinned PinMAME's own sim ball-routing table (wcs_stateDef) places the 'Trough stack' state immediately after the 'Trough 1' eject state in the ball's path toward the shooter lane.
- Switch 43: Projected onto the rotating goalie figure (Primitive BM_goalkeeper, table object center): the retained script's InitGoalie sets BP_goalkeeper.x=376/.y=280, matching this primitive's own position (374.4,281.5) almost exactly, and wcs_handleMech sets public switches 43/44 directly from the DC-motor position counter (mech_getPos(0)) rather than from a fixed playfield sensor object.
- Switch 44: Projected onto the rotating goalie figure (Primitive BM_goalkeeper, table object center); see switch 43.
- Switch 48: Projected onto the goalie figure (Primitive BM_goalkeeper, table object center), the target this switch senses: the Goalie Target (A-17779) is the goalie figure itself, the switch drawing (printed 2-47) ends callout 48's leader on the goalie unit, and the retained script's GWalls_Hit handler pulses public 48 whenever a ball strikes whichever segment of the goalie's 35-segment hit ring (HitTarget GT006-GT040) is currently collidable. That ring moves with the figure and has no fixed playfield sensor object of its own. An earlier pass projected this switch onto the shooter-lane plunger trigger, which is unrelated to the goalie.

## Counts

- Placements: 200
- Located input addresses: 51
- Located output bindings: 99
- Outputs with no spatial key at all: 0
- Inputs with a controlled `cabinet_or_service` record: 16
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 2
- Inputs with a controlled `unused` record: 10
- Outputs with a controlled `cabinet_or_service` record: 5
- Outputs with a controlled `unused` record: 1
- Outputs with a controlled `virtual` record: 15

## Promotion decision

No authoring-critical placement, quantity, or semantic question remains unresolved, every placement is validated, and the deterministic curator reproduces the canonical artifact and its pinned seed byte-for-byte. The former blockers are settled: solenoid 34 is placed on the loop gate the factory drawings locate and the table models, and the jet-bumper identity is settled by both location drawings and the jet-bumper harness run, so `conflict.jet-bumper-script-binding-vs-physical-position` is withdrawn. The record is promoted to `author_ready`.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/midway/world-cup-soccer-1994/extracted-vpxtool.manifest.json`, SHA-256 `eab6beeaca073c66c01cacaee71d605f3629832062e56f67d92a31405d438032`, 2588 files, 773038506 bytes.
- Human transcription index of every printed table read from the rendered manual pages, SHA-256 `7055d31403f69bedd4dffa94aad45952c18e75065941e204338eb9a818690f75`.
- Callout-check reads, controls, corrections, overlays and generators: `external:pinmame-review-artifacts/world-cup-soccer/callout-check`, manifest SHA-256 `30235bf689623e70ca36775fd31ae691c2e4eaf4bfb49e1c9177aff47125357b`.
- Physical photographs: `external:pinmame-review-artifacts/world-cup-soccer/physical-photos`, manifest SHA-256 `5e9ba4932ae54593f7eb69c8689660d94ddd99a2b5a7ca7505a463ba7ef3e7a1`.
