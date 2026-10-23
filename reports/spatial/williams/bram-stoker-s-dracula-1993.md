# Bram Stoker's Dracula (Williams, 1993) spatial review

Status: validated. Every playfield switch, coil, flasher, lamp and GI address is placed, and every placement is validated; every other address carries a controlled `not_applicable` record. The machine record stays `partial` at `machines/partial/williams/bram-stoker-s-dracula-1993.json` on one unresolved conflict, flasher 19's playfield bulb count.

The matching source is the retained known-working `Bram Stokers Dracula (Williams 1993) VPW 1.0.vpx` at SHA-256 `e291eb0ab61eb8940aba6f54d16efd512d4565cbb6af29fcae5530035de7575e`. The retained `vpxtool git:v0.33.3` extraction produced the embedded script at SHA-256 `32f4f0ed85702cc015563eb262ea6c5b7cb7c90f6d30fa6b73c36f3c37c42c5f`; that embedded stream is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=952.941 bottom=2117.647`, and every canonical coordinate is x/952.941 and y/2117.647 rounded to at most six fractional places.

## Evidence decisions

- The embedded VPW script is the runtime address and causality authority; the Williams operations manual is the physical inventory, quantity, polarity, wiring and location authority; pinned PinMAME owns controller topology; the retained table supplies geometry where the factory drawings confirm it.
- Every table placement the factory location drawings can check was checked against them: the lamp drawing (printed 2-44), the solenoid/flasher drawing (printed 2-45) and the switch drawing (printed 2-46), with every callout transcribed by an independent reader working only from the page. A placement is validated only when its own callout lands within 0.07 normalized of it under both the page's control fit and its callout fit (tools/drawing_callouts.py). The curator refuses to build while any checked placement disagrees.
- Each page's controls are the drawn playfield frame's top-left and top-right corners, which match the table bounds, and crisp mechanism features: the three jet bumper caps and both flipper pivots on 2-45 and 2-46, and on 2-44, which draws only two jet-bumper rings and no flippers, those two rings and the four drain and return lane rollover slots (switches the lamp page does not check).
- Lamp 53 (Magnet) is the bulb on the Mist Magnet carrier: the A-16266 Coil Magnet & Screw Assembly page (printed 2-27) fits a light socket and bulb beside the coil on the carrier, and the manual's game story says the light moves in unison with the magnet. It lights the row of thirteen small round inserts the carrier runs under, so it is projected onto ml7, the middle of the thirteen fixed lights the retained table places under those inserts. The retained table never reads lamp 53; it steps ml1-ml13 from the carriage position instead.
- Solenoids 27 (Magnet) and 28 (Magnet's Motor) are projected onto the carriage track: the area centroid of the retained table's Trigger.Magnet zone, a thin band along the track. That zone's stored centre lies outside the band and is not used.
- Switches 81, 82 and 83 are placed where they act on the Mist Magnet path, from the retained script's carriage track: 81 and 83 at the left and right ends of the carriage's travel, the ends the leaf switches detect, and 82 at the left end of the ball-on-magnet beam line, where the switch drawing ends its leader (0.002 normalized away). Earlier they shared one projected point between the two ends.
- Switch 34 (Launch Ball) is the cabinet launch button, part A-15896-1 like lamp 87, printed below the playfield outline on the switch drawing and listed by PinMAME's drac.c among the cabinet switches; it takes a controlled `cabinet_or_service` record instead of the plunger projection it had.
- Flasher 17 has three playfield bulbs on the 3-8 table and three callouts on the solenoid drawing: the top-right corner dome, which the retained table models as F17_Dome, and two domes on the coffin's head piece, which it does not model. Those two are drawing measurements: the drawing pixel is pinned in the callout seed and normalized through that page's control fit, rounded to three places; each lies inside the convex hull of the page's controls, and IPDB picture 12459 shows the two blue domes flanking a cross on the coffin. Each flasher's quantity counts its playfield and backbox bulbs, and only the playfield bulbs are placed. Flasher 19's playfield function is `3-Bank's` on the Flashlamp Wiring page (printed 3-9), the solenoid drawing prints two callouts 19, one at each 3-bank, and the retained script drives a light at each; the 3-8 table and the Williams tech chart count one #89 for that function. Both drawn sockets are placed and the quantity follows the drawing (two playfield bulbs and House in the backbox), but `conflict.flasher-19-playfield-bulb-count` holds the count unresolved.
- Switches 61-65 (jets and slingshots) and 77 (Right Ramp Up) have no dedicated playfield trigger object; the retained script pulses their public state directly from the Bumper/Wall objects' Hit events or from solenoid commands, so they are documented projections onto the real mechanism object, and the switch drawing confirms each.
- GI strings 0-2 use the retained table's GIBOT/GITOP/GIMID emitter collections, matching the retained script's GIUpdate2 dispatch exactly with zero script-vs-manual disagreement; the drawings print no GI callouts. GI strings 3 and 4 are backbox-only circuits and take a controlled `cabinet_or_service` record.
- Lamps 58 and 61-63 are on the playfield's back panel, the upright panel at the playfield's rear edge: the A-16399 Back Panel & Decal Assembly (printed 2-39) carries the 3-lamp PCB A-16337-1 (61-63) and the B-12224 single lamp assembly (58), and the lamp drawing draws all four only in that assembly's inset box above the playfield, which spans the drawn playfield's width. Each takes the retained table's script-bound light on the playfield's rear edge, the panel's plane; through the page's control fit the centre of each lamp's insert symbol in the inset lies within 0.023 in x of its light, in the same order. IPDB picture 12459 shows the panel's `SKILL S` lettering behind the ramps.
- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME core and manual provenance.

## Drawing callout check

Seed `tools/seeds/williams/bram-stoker-s-dracula-1993-callouts.json` (SHA-256 `7161dc6ad16e105266bbf68c9e99e77b1859d8467c8129c630f09b70899bb9b6`); 120 placements checked, 120 validated.

- 2-44: 8 controls (RMS 0.0034, leave-one-out max 0.01), 47 callout pairs, 47 in the callout fit (leave-one-out max 0.0452).
- 2-45: 7 controls (RMS 0.0036, leave-one-out max 0.0083), 30 callout pairs, 30 in the callout fit (leave-one-out max 0.0603).
- 2-46: 7 controls (RMS 0.0042, leave-one-out max 0.0111), 43 callout pairs, 43 in the callout fit (leave-one-out max 0.0621).

Excluded from the check, with the seed's reasons:

- `device.lower-left-flipper-hold.effect`: the solenoid drawing prints no callout for the flipper coils (its Flippers list is marked '*Not Shown').
- `device.lower-left-flipper-power.effect`: the solenoid drawing prints no callout for the flipper coils (its Flippers list is marked '*Not Shown').
- `device.lower-right-flipper-hold.effect`: the solenoid drawing prints no callout for the flipper coils (its Flippers list is marked '*Not Shown').
- `device.lower-right-flipper-power.effect`: the solenoid drawing prints no callout for the flipper coils (its Flippers list is marked '*Not Shown').
- `device.magnet-s-motor.effect`: the motor drives the Mist Magnet carrier along its screw; the solenoid drawing prints balloon 28 mid-path on a double-headed arrow along the track, not at a part, and the placement is a projection onto the track.
- `device.magnet.effect`: the coil magnet rides on the Mist Magnet carrier; the solenoid drawing prints balloon 27 mid-path on a double-headed arrow along the track, not at a part, and the placement is a projection onto the track.
- `device.shooter-ramp-entry.effect`: the solenoid drawing prints balloon 8 with no leader on the shooter lane at about 0.666 normalized, over the upper end of the table's sramp2 incline (the shooter-lane ramp the script's SolShooterRamp makes collidable, spanning 0.650-0.825 of the playfield height along the lane); the drawing is consistent with that object, but a balloon centre is not a part and the placement, the incline's centre, is 0.077 from it.
- `lamp.matrix-16.emitter`: the lamp drawing prints no callout 16 and draws no insert for the right ramp lock lamp; the placement keeps the table's script-bound Light l16.
- `lamp.matrix-37.emitter`: the lamp drawing draws the left outlane insert as an unnumbered clear diamond and prints no callout 37 anywhere; the table's script-bound Light l37 lies on that drawn insert, so the placement keeps its table status.
- `lamp.matrix-38.emitter`: the lamp drawing draws the left inlane insert as an unnumbered clear diamond and prints no callout 38 anywhere; the table's script-bound Light l38 lies on that drawn insert, so the placement keeps its table status.
- `lamp.matrix-41.emitter`: the lamp drawing draws the right inlane insert as an unnumbered dashed oval under the right inlane wireform and prints no callout 41 anywhere; the table's script-bound Light l41 lies on that drawn insert, so the placement keeps its table status.
- `lamp.matrix-42.emitter`: the lamp drawing draws the right outlane insert as an unnumbered clear diamond and prints no callout 42 anywhere; the table's script-bound Light l42 lies on that drawn insert, so the placement keeps its table status.
- `lamp.matrix-53.emitter`: the bulb rides on the Mist Magnet carrier; the lamp drawing prints balloon 53 with no leader at the left end of the row of inserts the carrier runs under, beside a free-standing arrow along it, and the placement is a projection onto the middle of that row.
- `lamp.matrix-58.emitter`: the lamp drawing draws lamp 58 only in its inset box 'A-16399 Back Panel Assy.' above the playfield, an elevation of the upright back panel at the playfield's rear edge (printed 2-39), not on the playfield plan; the inset box spans the drawn playfield's width (its edges at 16.5 and 509.5 px against the frame's 15 and 515.5), and through the page's control fit the centre of its insert symbol (the read's recorded point, pixel [341, 68]) lies 0.006 in x from the table's script-bound light, the four inset lamps in the same order as the table's; the placement keeps that light on the panel's plane.
- `lamp.matrix-61.emitter`: the lamp drawing draws lamp 61 only in its inset box 'A-16399 Back Panel Assy.' above the playfield, an elevation of the upright back panel at the playfield's rear edge (printed 2-39), not on the playfield plan; the inset box spans the drawn playfield's width (its edges at 16.5 and 509.5 px against the frame's 15 and 515.5), and through the page's control fit the centre of its insert symbol (the read's recorded point, pixel [253, 152]) lies 0.014 in x from the table's script-bound light, the four inset lamps in the same order as the table's; the placement keeps that light on the panel's plane.
- `lamp.matrix-62.emitter`: the lamp drawing draws lamp 62 only in its inset box 'A-16399 Back Panel Assy.' above the playfield, an elevation of the upright back panel at the playfield's rear edge (printed 2-39), not on the playfield plan; the inset box spans the drawn playfield's width (its edges at 16.5 and 509.5 px against the frame's 15 and 515.5), and through the page's control fit the centre of its insert symbol (the read's recorded point, pixel [287, 162]) lies 0.021 in x from the table's script-bound light, the four inset lamps in the same order as the table's; the placement keeps that light on the panel's plane.
- `lamp.matrix-63.emitter`: the lamp drawing draws lamp 63 only in its inset box 'A-16399 Back Panel Assy.' above the playfield, an elevation of the upright back panel at the playfield's rear edge (printed 2-39), not on the playfield plan; the inset box spans the drawn playfield's width (its edges at 16.5 and 509.5 px against the frame's 15 and 515.5), and through the page's control fit the centre of its insert symbol (the read's recorded point, pixel [317, 153]) lies 0.023 in x from the table's script-bound light, the four inset lamps in the same order as the table's; the placement keeps that light on the panel's plane.
- `switch.matrix-81.sensor`: the switch drawing prints balloon 81, tagged (Under Playfield), with no leader at the playfield's left edge beside the left end of the mist path; its centre marks the end of the path, not a part, and lies 0.072 from the placement, the end of the carriage travel where the script asserts switch 81.
- `switch.matrix-85.sensor`: the switch drawing prints no callout 85 but two balloons 25: the left one's leader ends on the left top-lane rollover, 0.019 from the table's sw25; the right one's leader crosses the left ramp's wireform and ends at the top of the right top-lane slot, which callout 27 marks from below, 0.015 from the table's sw27 and 0.047 from its sw85. A printed label is not relabelled, and neither balloon can be taken for 85, so the placement keeps its script-bound table trigger sw85.

## Drawing measurements

- `device.t-r-corner-dracula-flasher.emitter.2`: callout 17 on 2-45, pixel [911.3, 386.3] (arrow_tip), normalized (0.639, 0.21); corroborated by the photos.
- `device.t-r-corner-dracula-flasher.emitter.3`: callout 17 on 2-45, pixel [951.9, 388.1] (arrow_tip), normalized (0.721, 0.212); corroborated by the photos.

## Explicit projections

- Switch 61: Projected onto the retained Bumper2 object, which the retained script's Bumper2_Hit handler pulses as switch 61 (Left Jet).
- Switch 62: Projected onto the retained Bumper3 object, which the retained script's Bumper3_Hit handler pulses as switch 62 (Right Jet).
- Switch 63: Projected onto the retained Bumper1 object, which the retained script's Bumper1_Hit handler pulses as switch 63 (Bottom Jet).
- Switch 64: Projected onto the retained LeftSlingShot wall, which the retained script's LeftSlingShot_Slingshot handler pulses as switch 64.
- Switch 65: Projected onto the retained RightSlingShot wall, which the retained script's RightSlingShot_Slingshot handler pulses as switch 65.
- Switch 77: Projected onto the Right Ramp mechanism (Ramp.RightRamp): the retained script sets public switch 77 directly from the SolRRampUp/SolRRampDown solenoid commands (Controller.Switch(77) = True/False) rather than from a discrete sensor object, even though the Switch Locations parts list prints a real part number (5647-12693-36) for it.
- Solenoid 27: Projected onto the Mist Magnet carriage track: the area centroid of the retained table's Trigger.Magnet zone along it (the coil rides on the carrier).
- Solenoid 28: Projected onto the Mist Magnet carriage track: the area centroid of the retained table's Trigger.Magnet zone along it (the motor drives the carrier along its screw).
- Lamp 53: Projected onto ml7, the middle of the thirteen fixed lights the retained table places under the row of inserts the carrier's bulb lights.

## Mist Magnet switches

- Switch 81: Placed at the left end of the Mist Magnet carriage's travel, raw (111, 1189.16): the retained script's SetMagnetPosition puts the carriage at x = 850 - 739 * MagnetPos / 500 on y = -0.44 x + 1238 and asserts switch 81 for MagnetPos > 490, the last 2 percent of travel towards that end. The 2-46 switch drawing prints balloon 81, tagged (Under Playfield), with no leader at the playfield's left edge beside that end of the path, so it marks the end without marking a part; the placement is the end of travel the leaf switch detects, not a drawn part.
- Switch 82: Placed at the left end of the ball-on-magnet beam, raw (126, 1220): the retained script's MistTimer_Timer reads switch 82 from a line test along the whole mist path, the line its comment gives as running from (126, 1220) to (870, 885), and the 2-46 switch drawing runs callout 82's leader the length of the path to a dot at its left end, within 0.005 normalized of that point. The opto watches the whole path; the placement is the end the drawing marks.
- Switch 83: Placed at the right end of the Mist Magnet carriage's travel, raw (850, 864): the retained script asserts switch 83 for MagnetPos < 10, the first 2 percent of travel from that end (see switch 81), and the 2-46 switch drawing ends callout 83's leader in a dot at the right end of the mist path.

## Counts

- Placements: 179
- Located input addresses: 45
- Located output bindings: 94
- Outputs with no spatial key at all: 0
- Inputs with a controlled `cabinet_or_service` record: 15
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 2
- Inputs with a controlled `unused` record: 17
- Outputs with a controlled `cabinet_or_service` record: 6
- Outputs with a controlled `unused` record: 5
- Outputs with a controlled `virtual` record: 14

## Promotion decision

Every placement is validated and the deterministic curator reproduces the canonical artifact and its pinned seed byte-for-byte. The former blocker, lamp 53, is settled by the manual's magnet assembly page and game story, which put the bulb on the moving Mist Magnet carrier, and it takes a documented projection onto the row of inserts it lights. `conflict.upper-flipper-circuit-side-naming` stays recorded as ignored: it is a wiring detail that cannot change a recreation. One authoring-relevant quantity is not settled: flasher 19's playfield bulb count, two on the solenoid drawing and in the known-working table, one on the 3-8 table and the tech chart. `conflict.flasher-19-playfield-bulb-count` records it with its resolution path, and the record stays `partial` until a production machine settles it.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/bram-stokers-dracula-1993/extracted-vpxtool.manifest.json`, SHA-256 `ea69203a05b34f6eeb7572e17d1185e2d42be87b8ebd5593bf9efe44baa28da0`, 2484 files, 597253321 bytes.
- Human transcription of every printed table read from the rendered manual pages, SHA-256 `46fae8a9e5b625634576dd280d0cf8ce78106ecd71aafdee0f921784f5105548`.
- Callout-check reads, controls, corrections, overlays and generators: `external:pinmame-review-artifacts/dracula/callout-check`, manifest SHA-256 `3da3b0cbc5aebe7b813c0e579a93517013cd739dd3050d3a29af03de7109df1f`.
- Physical photographs and an owner's page: `external:pinmame-review-artifacts/dracula/physical-photos`, manifest SHA-256 `7a262bfa8950e235574621c58d2cd725ee52a608644a31c5cd533aab60e6ed7a`.
