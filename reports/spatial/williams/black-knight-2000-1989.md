# Black Knight 2000 (Williams, 1989) spatial review

Status: partial.

Geometry comes from the retained known-working Flupper 1.1 table (SHA-256 `98ffb10a95b9a584bca9d11dd2da1bce7fca42108f1082d8ebf616efc0d2c7ba`), whose embedded script (SHA-256 `955bc5ba128b3be1cbab9e7d3afab87389195c76b63185c406477240a880b21d`) is the runtime authority. Exact bounds are `left=0 top=0 right=954 bottom=2052`; every coordinate is x/954 and y/2052. The retained table models the split-level playfield in one x/y frame. The Williams operations manual is the physical authority; its location drawings were used to check sides and order, not to measure positions, except where a measured reconciliation is named below.

## Evidence decisions

- Coin chutes follow the switches list, the ROM and the cabinet wiring drawing (4 right, 6 left) over the matrix table's reversed pair.
- Drawbridge targets follow the matrix and list (33 upper, 34 middle, 35 lower), which the retained table's DBTrgt1-3 walls agree with; the ROM numbers them UPPER TARGET 3, 2, 1 for 33, 34, 35.
- Jet bumpers: switches 17/19/21 and coils 17/19/21 are the left, right and lower bumpers; the retained table's Bumper1/2/3 are the same left-to-right order and the script pulses 17, 19 and 21 from them.
- Speaker-panel R-A-N-S-O-M lamps (1-4, 6, 7), the insert-board G.I. (9), the knocker (14) and the A/C relay (12) take controlled non-playfield records.
- G.I. strings 10 and 11 are placed at the retained lightsGIupf and lightsGIlpf collections' bulbs; the manual prints no G.I. bulb count.

## Blocking gaps

- Solenoid 25: 2 playfield bulbs printed, 1 placed; the table models the flash as one light (RedBoltFlash) on the big red bolt; the second printed playfield bulb has no drawn or modelled location.
- Solenoid 26: 2 playfield bulbs printed, 1 placed; the table models the flash as one light (BlueBoltFlash) on the big blue bolt; the second printed playfield bulb has no drawn or modelled location.
- Solenoid 27: 2 playfield bulbs printed, 1 placed; the table models the flash as one light (KnightHeadFlash) at the bolt circle's center; the second printed playfield bulb has no drawn or modelled location.
- Solenoid 30: 2 playfield bulbs printed, 1 placed; the table models the flash as one light (SkyWayFlash) at the skyway ramp's lower left; the second printed playfield bulb has no drawn or modelled location.
- pinmame.input.switch 10, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33, 34, 35, 36, 37, 38, 53, 55: Placement status is observed, not validated: each rests on a retained-table object whose side and order the manual's drawings agree with, with a projection or centroid where the sensor itself is not modelled.
- pinmame.output 1, 2, 3, 4, 5, 7, 8, 9, 10, 10, 11, 11, 12, 13, 14, 15, 15, 16, 16, 17, 18, 18, 19, 20, 20, 21, 22, 23, 24, 25, 25, 26, 26, 27, 27, 28, 28, 29, 29, 30, 30, 31, 31, 32, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64: Placement status is observed, not validated (flasher glow objects, centroids, G.I. collections, lamp light objects, coil projections).

## Explicit projections

- pinmame.input.switch 16: UP (Motor Targets) is the roller snap-action switch (5647-12073-06, item 6 of Motor Assembly B-12465) that the motor cam (item 4, A-12463) closes at one end of the drawbridge targets' travel; no retained object models it, so it is anchored at the middle drawbridge-target wall, which the table's own motor model (cvpmMech Mech3Bank) moves.
- pinmame.input.switch 18: The slingshot switch pair (A-4834-H; A-11538-1, "Paired Kicker Actuating Sw") is inside the kicker; anchored at the drag-point centroid of the retained LSling wall.
- pinmame.input.switch 20: Anchored at the drag-point centroid of the retained RSling wall.
- pinmame.input.switch 24: DOWN (Motor Targets) is the second roller snap-action switch (5647-12073-06, item 6 of Motor Assembly B-12465) that the same motor cam (item 4, A-12463) closes at the other end; anchored at the middle drawbridge-target wall for the same reason as 16.
- pinmame.input.switch 33: Anchored at the drag-point centroid of the retained DBTrgt1 wall, the table's upper drawbridge target.
- pinmame.input.switch 34: Anchored at the drag-point centroid of the retained DBTrgt2 wall, the middle drawbridge target.
- pinmame.input.switch 35: Anchored at the drag-point centroid of the retained DBTrgt3 wall, the lower drawbridge target.
- pinmame.input.switch 40: The Right Eject Hole switch (5647-12073-10) closes in the eject hole; anchored at the retained REject kicker, which the script closes 40 from.
- pinmame.input.switch 47: The Ball Popper switch (A-11658, a switch and diode assembly under the popper cap) closes in the popper; anchored at the retained BallPopper1 kicker, which the script closes 47 from.
- pinmame.output.solenoid 3: Left Drop Target Reset placed on the middle target (sw5) of the bank it resets.
- pinmame.output.solenoid 4: Right Drop Target Reset placed on the middle target (sw2) of the bank it resets.
- pinmame.output.solenoid 16: Motor Targets relay placed on the middle drawbridge-target wall (DBTrgt2) the table's motor model moves.

## Counts

- Placements: 156
- Located input addresses: 41
- Located output bindings: 83
- Unresolved records: 3
- Inputs with a controlled `cabinet_or_service` record: 17
- Inputs with a controlled `dip_switch` record: 1
- Inputs with a controlled `internal_nonvisual` record: 1
- Inputs with a controlled `unused` record: 14
- Outputs with a controlled `cabinet_or_service` record: 8
- Outputs with a controlled `internal_nonvisual` record: 1
- Outputs with a controlled `unused` record: 2
- Outputs with a controlled `virtual` record: 20

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/black-knight-2000-1989/extracted-vpxtool.manifest.json`, SHA-256 `2e49d7c77422ed9e19133163172aa28bd1e18df6b36c03be69fd68835303a764`, 842 files, 47134919 bytes.
- Manual SHA-256 `4d9225b61d86072eaaeb8a6a1b2dd2365f1d25442641b9908a1cd1f8deff00b3`; committed excerpts under `evidence/excerpts/williams.black-knight-2000.1989/`.
- Runtime evidence `evidence/runtime/system-11/black-knight-2000-l4-service-and-mechanisms.json`.
