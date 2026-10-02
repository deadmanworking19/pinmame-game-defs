# Quicksilver (Stern, 1980) spatial review

Status: incomplete. Six lamp addresses carry no placement and every lamp placement is `observed`, so the machine record stays `partial` at `machines/partial/stern/quicksilver-1980.json`.

The geometry source is the retained known-working `Quicksilver (Stern 1980) VPW 1.0.vpx` at SHA-256 `a81901b68745a1132c7fdb6fb3609a665a45b89b7bedb32348517c1a514c2b64`. Its embedded script at SHA-256 `44338d1e352558783d78c33ea1d575d4792fb843a1248e5427ecbe9eb9d0648a` is the runtime address and causality authority. Exact playfield bounds are `left=0 top=0 right=952.941 bottom=1976.471`, and every canonical coordinate is x/952.941 and y/1976.471 rounded to at most six fractional places.

## Evidence decisions

- The embedded script owns runtime addresses and causality, this game's own manual and driver-board schematics own physical construction, wiring, quantity and device presence, pinned PinMAME owns controller topology, and the retained table supplies geometry.
- Lamp bindings come from the table's own `vpmMapLights InsertLamps` collection (a light's TimerInterval is its public lamp number) and from `UpdateMultipleLamps` for the backbox lamps, and each was checked against the function the Lamp Driver Schematic prints against the SCR that public address reaches. The names fall in the right places: the Q-U-I-C-K lamps run left to right along the top, the S-I-L and V-E-R stand-up lamps run top to bottom down the left and right arcs, and the two spinner lamps sit beside their own spinners once the schematic's hand correction of the left spinner's pin is applied.
- The retained VPW script pulses switches 20 and 21 from its slingshots, which is a defect of that script (the older retained table and the corpus 1.0 script pulse 12 and 13, and the ROM fires the sling coils on 12 and 13); the slingshots are placed on the table's own sling walls and the defect is stated on the devices.
- General illumination is not a device on this machine: the playfield sheet draws it as a 6 VAC lamp string with no driver-board connection and the Stern MPU-200 controller profile declares no general-illumination group.

## Explicit projections

- pinmame.output.solenoid 7: Projected onto the center four-target drop bank it resets (the mean of the retained table's own target walls sw21-sw24); the reset coil sits under the bank and has no object of its own.
- pinmame.output.solenoid 8: Projected onto the right three-target drop bank it resets (the mean of the retained table's own target walls sw30-sw32).
- physical.input.direct 1: Placed on the left flipper object (its centre) because the end-of-stroke contact is mounted on the flipper assembly and has no object of its own.
- physical.input.direct 2: Placed on the right flipper object (its centre) because the end-of-stroke contact is mounted on the flipper assembly and has no object of its own.
- pinmame.output.solenoid 46: The right flipper coil is placed on the flipper object it drives (its centre).
- pinmame.output.solenoid 48: The left flipper coil is placed on the flipper object it drives (its centre).

## Counts

- Placements: 95 (49 observed, 46 validated)
- Callout check: 46 of 48 checked placements validated against the manual's location drawings; not validated: device.right-flipper.effect, switch.kick-out-hole.sensor
- Located input addresses: 34 matrix switches and 2 direct end-of-stroke contacts
- Located output bindings: 56
- Inputs with a controlled `cabinet_or_service` record: 11
- Inputs with a controlled `dip_switch` record: 32
- Inputs with a controlled `unused` record: 2
- Outputs with a controlled `cabinet_or_service` record: 6
- Outputs with a controlled `internal_nonvisual` record: 1
- Outputs with a controlled `unused` record: 12
- Inputs with no spatial key at all: 0 (none)
- Outputs with no spatial key at all: 6 (6, 10, 26, 42, 57, 58)

## Blockers

- Five lamp addresses have no spatial key because the retained tables model no light for them: the top roll-over dividers, public 10, 26, 42, 57 and 58. They are fitted (the Lamp Driver Schematic's list names them `TOP R.O. DIVIDERS (L TO R)`, five rows), but no retained object lies on them and the manual's playfield drawings carry no lamp-location page.
- Public lamp 6 (SCR Q10) has no spatial key and is unresolved: no lamp list prints a load for it, yet the ROM drives it in the attract-mode lamp pattern. See the knowledge note.
- Every lamp placement is `observed`, not `validated`: it comes from one retained factory-layout table, the manual carries no lamp-location drawing, and the earlier retained table agrees on the lamps to within 0.026 normalized but shares their numbering and the ancestral light list, so it only supplements. The callout check validated the switch and solenoid placements that agree with the manual's two location drawings (see the counts); the placements it left observed are listed under `callout_check.not_validated`.

## Promotion decision

Promotion to `author_ready` is refused. Public lamp 6 is driven by the ROM but listed by no wiring sheet, so its fitment is unresolved and `output_semantics` stays missing; five fitted top-divider lamps have no retained object; and every lamp placement rests on one factory-layout table with no lamp-location drawing to check it against. The record stays `partial` with `coverage.missing = ["output_semantics", "spatial_placement"]`.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/stern/quicksilver-1980/vpw-1.0/Quicksilver (Stern 1980) VPW 1.0.manifest.json`, SHA-256 `87a93746e47a892290eea8ea03a4b68e70fa3dc73d838c0638392a61335b52bf`, 1988 files, 438666984 bytes.
- Object-centre dump of the extracted game items, raw and normalized, at `external:pinmame-review-artifacts/quicksilver-1980/vpw-geometry.tsv`.
- Manual `Stern_1980_Quicksilver_Manual.pdf`, SHA-256 `140216dc27e97084e0b523fe0d5ff5417961723fea069b1fad3dd594b9723728`, with transcribed excerpts under `evidence/excerpts/stern.quicksilver.1980/`.
