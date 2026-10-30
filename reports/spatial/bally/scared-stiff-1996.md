# Scared Stiff (Bally, 1996) spatial review

Status: validated. Every spatial dimension audited here is complete. The sixteen driver-declared auxiliary lamp addresses (91-98, 101-108) and their clock and data lines (37/38) take a controlled `unused` record: they belong to the prototype-only 16-LED Skull Driver PCB, which production machines do not carry (see the promotion decision below).

The matching source is the retained known-working `Scared Stiff (Bally 1996) VPW v1.0.vpx` at SHA-256 `bede6f6c5b7592c4610af444a196c42432949468f708e79b4b112a73692cdc1e`. The retained `vpxtool git:v0.33.3` extraction produced the embedded script at SHA-256 `4c9a63e77e10ea65d1146e33f81197bb41b719d70027d8fa0c2d258f823211b4`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=952.941 bottom=2164.706`, and every canonical coordinate is x/952.941 and y/2164.706 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPW script is the runtime address and causality authority; the Bally/Midway operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- The retained manual PDF has a real but badly garbled multi-column OCR text layer for its Section 2/3 tables (unlike Monster Bash's fully image-only scan); every printed table used here was still read from rendered 300-600 dpi pages and transcribed into `external:pinmame-review-artifacts/scared-stiff-1996/manual-transcription.md`, never trusted from `pdftotext` alone.
- The switch-matrix page's own opto legend (a small box, 'OPTO, TYPICALLY CLOSED') shades zero cells on this manual, unlike Monster Bash's. Opto identity instead comes from the Switch Locations parts list's own two-row `(LED)` + `(Trans.)` construction disclosure, swept exhaustively; it produced exactly the same 17-address set PinMAME's own inverted-switch mask normalizes, with zero disagreement.
- Switch 31 (Trough Eject) and solenoids 5/8/16/33/34 have no dedicated collision object because the retained script sets their public state, or animates their visible proxy, from another object's own event or rotation angle rather than from a Hit/Trigger event on a coordinate of their own. Those addresses are explicit documented projections onto the real table object that carries the underlying mechanism state.
- Sixteen 'Web Award' lamps (64-68, 71-78, 81-83) and general-illumination strings 3/4 are backbox devices: the manual's own `*Located in backbox` annotation and the retained table's strongly negative normalized-x Light-object coordinates agree independently, so they take a controlled `cabinet_or_service` record rather than a fabricated playfield position.
- Switch 12 (Wheel Index) and solenoids 39/40 (Spider Wheel motor) are part of a backbox mechanism -- the rotated `pSpider` primitive sits at a strongly negative normalized y, behind the playfield's own rear edge -- and take a controlled `cabinet_or_service` record for the same reason.
- Solenoids 41-44 are PinMAME's LPDC mirrors of physical drive lines 37-40 (aux lamp clock/data, Spider Wheel motor phases) and are declared virtual with a `virtual` spatial record so no duplicate device is ever placed on the playfield.
- Auxiliary lamp addresses 91-98 and 101-108 and their clock and data lines 37/38 take a controlled `unused` record. Midway's own 1996 development notes say the skull pile's LED eyes were removed for cost and two flashers (21 and 25) placed behind the skulls, pinned `ss.c` calls the matching 16-LED Skull Driver PCB A-20781 a 'Prototype 0.1' part 'not kept in production build', and the production ROMs never drive those addresses in the retained auxiliary lamp probe. The retained table implements no Light object at any of them, so no coordinate is invented.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.
- Flasher addresses 21, 22, 25, and 27 sit at normalized y between 0.0014 and 0.0015 -- within the y<0.005 band this project treats as a required manual check before recording a placement. Each is the sole, non-suffixed Light object at its address (not a duplicate/halo variant), the manual's printed table shows a single Playfield-only flashlamp part for each (no Backbox pairing, unlike addresses 17-19 which do print a Backbox part alongside Playfield), and neighboring Skull Lane switches/lamps independently cluster at a similarly low y -- consistent with real flasher domes mounted at the very top of the playfield, not a back-panel render proxy of the kind Monster Bash and Theatre of Magic both found at y=0.000. Kept as validated placements with this reasoning disclosed.

## Explicit projections

- Switch 31: Projected onto the trough Ball 1 kicker position (switch 32): the retained script's SolRelease handler (solenoid 9) kicks the ball resting on switch 32 (sw32.kick 60,9) and pulses switch 31 in the same event (vpmTimer.PulseSw 31); there is no separate Trough Eject collision object.
- Solenoid 5: Projected onto the coffin-door proxy primitive BM_cDoorClose: the retained script's CoffinFlipper_animate drives BP_cDoorClose/BP_cDoorOpen from an off-playfield helper Flipper object (CoffinFlipper, negative x), so the visible door primitive's own position is used instead of the invisible helper's coordinate.
- Solenoid 8: Projected onto switch 38 (Crate Entrance): the Crate Post assembly's own primitive (Crate_Pin) sits at local origin (0,0,0), a meaningless raw mesh coordinate, not a playfield position, so the post is projected onto the crate mechanism's own entrance opto instead.
- Solenoid 16: Projected onto switch 38 (Crate Entrance); see solenoid 8 -- both solenoids actuate the same Crate Post.
- Solenoid 33: Projected onto the diverter proxy primitive BM_CoffinDiverter: the retained script's LockFlipper_Animate drives BP_CoffinDiverter from an off-playfield helper Flipper object (LockFlipper, negative x), so the visible diverter primitive's own position is used instead of the invisible helper's coordinate.
- Solenoid 34: Projected onto the diverter proxy primitive BM_CoffinDiverter; see solenoid 33.

## Counts

- Placements: 163
- Located input addresses: 43
- Located output bindings: 84
- Inputs with a controlled `cabinet_or_service` record: 16
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 2
- Inputs with a controlled `unused` record: 18
- Outputs with a controlled `cabinet_or_service` record: 23
- Outputs with a controlled `unused` record: 18
- Outputs with a controlled `virtual` record: 10

## Promotion decision

Promoted to `author_ready`. No authoring-critical placement, quantity, or semantic question remains unresolved, and the deterministic curator reproduces the canonical artifact and its pinned seed byte-for-byte. The one question that held the record partial, whether a production machine carries the board behind auxiliary lamp addresses 91-98 and 101-108, is settled by Midway's own development notes: the skull LEDs were removed for cost before production, so those addresses and their clock and data lines 37/38 are recorded `unused`. The D.01R prototype ROMs (`ss_01`, `ss_01b`), which still drive that board, moved to `bally.scared-stiff-d01r-prototype.1996`.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/bally/scared-stiff-1996/extracted-vpxtool.manifest.json`, SHA-256 `8cf07f3cef5678fdac96b27b0974a2c8653a7070ed69ea364ca5ebffd386756d`, 2302 files, 937624764 bytes.
- Human transcription of every printed table read from the rendered manual pages, SHA-256 `493e070b4244cefd99acf907103a758d70bc9e55d5605fea412f9e7ed0696537`.
- Midway's development notes with their illustration and later mirror, and the owner reports, pinned by the external manifest `external:pinmame-review-artifacts/scared-stiff-1996/aux-lamp-sources/manifest.json`, SHA-256 `292cedb949dc7898378f3573d6c8ce028592d5b02561a56fbe835908a0c6bde4`.
- Auxiliary lamp probe and flipper-button polarity runs under `external:pinmame-runtime-evidence/scared-stiff-1996/`, each pinned by its own manifest.
