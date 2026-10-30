# Congo (Williams, 1995) spatial review

Status: validated. Every input and output has a validated placement or a controlled `not_applicable` record, and the physical machine record is `author_ready` at `machines/author-ready/williams/congo-1995.json`; see the promotion decision below.

The matching source is the retained known-working `Congo (Williams 1995) 1.1.vpx` at SHA-256 `45a6448efb586475a6886962c5bace44789be1d7cd3dde2c507169fdf085432c`. The retained `vpxtool` extraction produced the embedded script at SHA-256 `19c19ea64bb120af66ef3ca309a2ec98c08b35ecf08e198bb26b3cd1611cd936`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=964 bottom=2162`, and every canonical coordinate is x/964 and y/2162 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPX script is the runtime address and causality authority; the Williams operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- The retained manual PDF has a usable but imperfect OCR text layer (Paper Capture scan); every printed table used here was still read from 300/600/1200 dpi renders and transcribed by hand into `evidence/excerpts/williams.congo.1995/`.
- Several switches have no dedicated playfield trigger object because the retained script's cvpmTrough helpers (bsTrough, bsVolcano) model multi-position ball sensing purely as an internal switch array. Those addresses are explicit documented projections onto the real kicker object that carries the mechanism's exit/entry point.
- GiTop member `GI10_Deactivated` is excluded as a table modeling anomaly (its own name marks it disabled); GI address 1's physical quantity is 13, not the collection's raw 14 members.
- Flasher `F8L3` (part of solenoid 27, Volcano Flasher) sits at normalized x=1.022303, outside the retained table's 0..1 playfield bounds, and is excluded as the modeled stand-in for the printed table's backbox bulb; the other three Volcano Flasher bulbs (2 playfield #89, 1 playfield #906) are placed normally.
- GI strings 0-2 use the retained table's GiGorilla/GiTop/GIBottom emitter collections, matching the retained script's `UpdateGi`/`UpdateGiOn` dispatch exactly. GI strings 3 and 4 are backbox insert-panel circuits and take a controlled `cabinet_or_service` record.
- Solenoids 41-44 are PinMAME's unused WPC-95 LPDC mirrors; Congo populates no LPDC output at all (37-40 are also unused), unlike WPC-95 games with a DC-motor mechanism.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.
- Switch 25 (Right Eject Rubber) is placed at the centre of the transformed-vertex span of the collidable Primitive `sw25`, the rubber its `sw25_Hit` handler binds. An earlier pass left it unplaced because a second Primitive, `sw1`, shares its position field; `sw1` is an overlapping duplicate of the same rubber with no handler, and the position field is the mesh's pivot at one end of the band. Callout 25 on the Switch Locations drawing (printed 2-41), fitted to the drawing frame and five other callouts (28, 37, 56, 64, 65), lies 0.0065 from the placement, inside the fit's largest leave-one-out miss (0.0109) and the project's 0.07 callout limit (`evidence/excerpts/williams.congo.1995/switch-25-callout.md`).
- Fliptronic inputs 112, 114, 116 and 118 are the two optos of each cabinet button's Flipper Opto Board and take a controlled `cabinet_or_service` record; 115 is unused, since Congo fits no upper right flipper.

## Explicit projections

- Switch 31: Projected onto the trough's own release kicker (Kicker BallRelease, table object center): the retained cvpmTrough helper (bsTrough) models switches 32-35 purely as an internal switch array with no separate playfield trigger object, and the trough-eject opto is pulsed in the same SolRelease handler that fires the BallRelease kicker.
- Switch 32: Projected onto the trough's own release kicker (Kicker BallRelease, table object center); see switch 31. The retained cvpmTrough helper has no separate visible object per ball position.
- Switch 33: Projected onto the trough's own release kicker (Kicker BallRelease, table object center); see switch 31.
- Switch 34: Projected onto the trough's own release kicker (Kicker BallRelease, table object center); see switch 31.
- Switch 35: Projected onto the trough's own release kicker (Kicker BallRelease, table object center); see switch 31.
- Switch 41: Projected onto the Volcano lock's own exit kicker (Kicker sw36a, table object center): the retained cvpmTrough helper (bsVolcano) models switches 41-43 purely as an internal switch array with no separate playfield trigger object, and the volcano ejects a locked ball through the same sw36a kicker (.Initexit sw36a).
- Switch 42: Projected onto the Volcano lock's own exit kicker (Kicker sw36a, table object center); see switch 41.
- Switch 43: Projected onto the Volcano lock's own exit kicker (Kicker sw36a, table object center); see switch 41.

## Counts

- Placements: 188
- Located input addresses: 52
- Located output bindings: 100
- Unresolved input addresses: []
- Inputs with a controlled `cabinet_or_service` record: 16
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `unused` record: 11
- Outputs with a controlled `cabinet_or_service` record: 4
- Outputs with a controlled `unused` record: 1
- Outputs with a controlled `virtual` record: 14

## Promotion decision

No authoring-critical semantic, wiring, mechanism or spatial question remains unresolved, and the deterministic curator reproduces the canonical artifact and its pinned seed byte-for-byte. Switch 25, the last open placement, is the script-bound `sw25` rubber, corroborated by the factory drawing, so the definition is promoted to `author_ready` with an empty `coverage.missing`.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/congo-1995/extracted-vpxtool.manifest.json`, SHA-256 `c9b02744cbb2e1b0659c7032b0ef42d4e7cadf5c36ed33ac171a037b8be82b62`, 925 files, 47770557 bytes.
- Human-readable manual transcriptions under `evidence/excerpts/williams.congo.1995/` (six tables, the DIP switch chart, the flipper opto wiring pages and the switch 25 callout fit), each hashed and cited from the definition's manual source record.
- `external:pinmame-review-artifacts/congo/sw25-mesh/`: the `sw25` and `sw1` objects copied from a `vpxtool export obj --units vpu` export of the retained table, with the export log and a manifest.
- `external:pinmame-runtime-evidence/congo-1995/congo_21-flipper-button-polarity/`: the Fliptronic input run, pinned by its own manifest.
