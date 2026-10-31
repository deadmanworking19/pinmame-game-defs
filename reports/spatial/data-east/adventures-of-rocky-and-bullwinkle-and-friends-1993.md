# The Adventures of Rocky and Bullwinkle and Friends (Data East, 1993) spatial review

Status: observed. Every playfield switch and every coil or flash-lamp group the retained table models with a script-bound object is placed from that table; cabinet, backbox, virtual and unused addresses carry a controlled `not_applicable` record. The playfield lamps, the G.I., the knocker and flash lamps 1R, 2R, 4R, 6R, 7R and 8R have no coordinate. No placement was checked against the manual's location drawings, so every placement stays `observed` (hat targets 22 and 24 `conflicted`) and the record stays at `machines/partial/data-east/adventures-of-rocky-and-bullwinkle-and-friends-1993.json`.

The geometry source is the retained known-working `The Adventures of Rocky and Bullwinkle and Fiends (Data East 1993) 1.0.vpx` (SHA-256 `eb8806c40a3b1102ef7ee4d706dfb322dcc39b5909ae23b0132a7888f7971fa2`); its embedded script (SHA-256 `09f43d857b0a97eb2c6c1384db91e5f2aee6ab55541fcdb64292a77f8b4eb464`) is the runtime binding authority. Exact playfield bounds are 952 x 2162; every table coordinate is x/952 and y/2162 rounded to six places.

## Evidence decisions

- The embedded script is the runtime authority; the 1993 manual is the physical inventory, construction and wiring authority; the 3.20 ROM's own service tests settle names and switch-to-coil pairs; pinned PinMAME owns controller topology; the retained table supplies geometry for script-bound objects only.
- A lamp or flash lamp is placed only on a script-bound bulb: a Light that is a bulb Light and draws its bulb mesh, or a modelled bulb primitive the script fades with the lamp. Every flash-lamp Light in the table draws no bulb, so only 3R and 5R, which the table models with three upright bulb primitives, are placed; no playfield lamp is placed.
- Primitives are placed at the centre of their world-space mesh bounds from the retained `vpxtool export obj --units vpu` export (SHA-256 `561cf123e5c23d1a45c03ba2613586ca9fd52b17f9b1d8979c04a236f7055466`), never at their stored positions; the diverters' stored positions are their pivots.
- The retained table pulses 45 from its upper right bumper and 46 from its lower one; the manual's drawing and the ROM's names put 46 on the upper right and 45 on the lower, center bumper, so 45 is placed on Bumper3 and 46 on Bumper2. That swap is a table defect, recorded on the devices.
- The backbox figure coils 3, 6 and 7 and the Left/Right relay 10 are cabinet or backbox devices; flash-lamp bulbs in the backbox insert are not placed.

## Blockers

- Every placement comes from one community table (cyberpez's 1.0) and none was checked against the manual's switch, lamp or coil location drawings, so all of them stay observed. Promotion needs a callout check of those drawings or a second, independent table lineage.
- Hat targets 22 and 24 are placed on the retained table's top and bottom targets but stay conflicted: the manual prints 22 at the bottom and 24 at the top, the ROM the other way round (conflict hat-target-switch-order).
- The 62 playfield lamps have no coordinate: the retained script binds only insert overlays, primitives and sprites to them, the raised bulbs it fades for 16 and 53 are bound crossed against the manual's chart and the ROM's names, and the lamp-location drawing was not used for placement.
- Flash lamps 1R (25), 4R (28), 6R (30) and 8R (32) have no coordinate: the script fades only bulb-mode Lights that draw no bulb (show_bulb_mesh false) and sit on no modelled bulb, plus insert overlays and sprites. 2R (26) and 7R (31) have none either: the script binds only insert-overlay Lights to them.
- Flash lamps 3R (27) and 5R (29) are placed on the three bulbs the table models as primitives, one and two of the four bulbs the schematic counts outside the backbox for each group; the rest of their bulbs have no coordinate.
- The G.I. relay 11 has no coordinate: its fade drives 84 bulb-mode Lights of which only gi5a and gi6a draw a bulb, and no retained page counts or locates the G.I. bulbs, so no G.I. emitter survey was made.
- The knocker 8 has no coordinate: page 28's coil location drawing carries no 8L balloon and no other retained page locates it.
- The drop-target reset coil 15 is a projection onto the middle drop target.

## Explicit projections

- pinmame.output.solenoid 15: The drop-target reset coil is projected onto the middle drop target t19, where the retained table plays its reset sound; the table models no coil.

## Counts

- Placements: 59
- Validated input addresses: 0
- Observed-only input addresses: 38
- Conflicted input addresses: 2
- Validated output bindings: 0
- Observed-only output bindings: 18
- Output bindings with no coordinate: 70
- Inputs with a controlled `cabinet_or_service` record: 14
- Inputs with a controlled `dip_switch` record: 1
- Inputs with a controlled `unused` record: 20
- Outputs with a controlled `cabinet_or_service` record: 6
- Outputs with a controlled `unused` record: 1
- Outputs with a controlled `virtual` record: 19

## Promotion decision

Refused. `coverage.missing` lists `spatial_placement` because every coordinate rests on one community table without a drawing check and the lamps, the G.I., the knocker, six of the eight flash-lamp groups and most bulbs of the other two are not placed; the hat-target conflict and the other open requirements keep the record partial as well.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/data-east/adventures-of-rocky-and-bullwinkle-and-friends-1993/extracted-vpxtool.manifest.json`, SHA-256 `d5df345d6ca4c736a12f0ac5a6c80845a842d16f7985e14a5c377bc525c831f7`, 1374 files, 131952476 bytes.
- World-space export `external:pinmame-review-artifacts/adventures-of-rocky-and-bullwinkle-and-friends-1993/world-obj/The Adventures of Rocky and Bullwinkle and Fiends (Data East 1993) 1.0.obj`, SHA-256 `561cf123e5c23d1a45c03ba2613586ca9fd52b17f9b1d8979c04a236f7055466`.
- Manual SHA-256 `1f50634e743bccf6276e170dcb5da05c92e5c4769a4650147338fab59b36a381`.
