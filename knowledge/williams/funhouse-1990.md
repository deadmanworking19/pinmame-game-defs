# Williams FunHouse (1990)

Physical machine ID: `williams.funhouse.1990`. FunHouse is a Williams WPC-Alpha machine with two sixteen-character alphanumeric displays. It predates Fliptronics: the physical flipper coils are direct-wired through a dedicated flipper driver board, while PinMAME publishes synthetic button-driven states for digital flipper animation.

## Identity and driver family

Pinned PinMAME's `fh_l9` clone tree has seventeen drivers: production parent `fh_l9` plus sixteen firmware revisions, LED ghost-fix variants, translation/rules modifications, FreeWPC firmware, and prototype `fh_pa1`. All use the same physical playfield and authoring-relevant address inventory.

`fh_pa1` uses a distinct `GEN_WPCALPHA_1` `core_tGameData` because the prototype had the earlier System 11 sound subsystem; production drivers use `GEN_WPCALPHA_2`. The two structs copy the same flipper-switch declaration, mechanisms, lamp-position data, and inverted-switch mask, so this is a controller/sound-generation variant of the same machine rather than another playfield.

The prototype struct also retains `gameSpecific1=1`, a stale value copied before production FunHouse was corrected to zero. In pinned `wpc.c`, that flag selects the unrelated `WPC_CFTBL` chase-light integrator and writes internal PWM lamp slots 65-72 from solenoids 20/24 and G.I. bits 0/3. `wpc_init` still publishes only 64 lamps because `fh_pa1` has `lampCol=0`, so those internal slots are not an eight-lamp FunHouse extension. They are a pinned-source defect and must not be recreated as physical lamps.

The retained known-working table binds `fh_905h` at active script line 64. The adjacent `fh_905` assignment is commented out. `fh_905h` is physically identical to the `fh_l9` parent.

## Controller and public addresses

The record reuses `controllers/pinmame/wpc-alpha.json` unchanged. It enumerates eight dedicated cabinet inputs, the complete 8×8 switch matrix, all eight public generic-flipper input positions 111-118, eight CPU DIP positions, 50 public solenoid/state positions, the complete 8×8 lamp matrix, five G.I. strings, and both displays. Generic inputs 112 and 114 are live right/left cabinet-button states; the other six positions are explicit unused addresses.

Public outputs 1-28 are the printed coils, motors, and flasher circuits. Addresses 29 and 30 mirror live J111/WPC_GILAMPS state bits. Address 31 is the real pre-Fliptronic Game-On relay whose documented chain runs from CPU board U4/J121 through power-driver J113, the relay, J110, the cabinet switch, and J109 to the flippers. Address 32 is constant zero; 33-44 are unused on this machine/generation; 49 is the live virtual `sShooterRel` channel consumed by the built-in PinMAME simulator's left- and right-shooter transitions; and 50 is the reserved gap before the custom-output range, which FunHouse does not declare. Address 49 has no physical driver-board circuit.

## Physical flippers versus synthetic outputs

`fhGameData` declares `FLIP_SWNO(12,11)` and no `FLIP_SOL()` bits. The handbook lists three fitted assemblies: lower right FL-11630, lower left FL-11630, and upper left FL-11753. The printed flipper-circuit page shows them wired through the dedicated flipper driver board and cabinet buttons, outside the CPU-addressable solenoid matrix; its generic upper-right position is unfitted on FunHouse. Public inputs 112 and 114 are the generic right/left cabinet-button states. `core_updateSw` copies them to ordinary matrix inputs 11 and 12 for the ROM, so 11/12 are neither playfield coordinates nor EOS contacts.

When the Game-On relay is active, `core_updateSw` fabricates public states 45-48 from the live flipper buttons because the physical coils are not CPU controlled. Addresses 45/46 represent the same right-side state in power and combined public views, and 47/48 do the same for the left side. The retained script consumes callbacks `sLRFlipper` (46) and `sLLFlipper` (48); `SolLFlipper` rotates both `LeftFlipper` and `LeftFlipper1`. A recreation should use 46 for the lower-right bat and 48 for both lower-left and upper-left bats, but must not model 45-48 as four additional physical coils.

## Switch matrix and trough

The manual marks exactly two switches `(opto)`: 51 Dummy Jaw and 55 Steps Superdog. Pinned `fhGameData`'s inverted-switch mask sets exactly those two positions (`0x11` in column 5), so PinMAME's public polarity is fully normalized with no disagreement.

Switch 63 is Right Trough. The November 1990 handbook places callout 63 at the rightmost trough position, while the retained script's `ballrelease_hit` asserts `Controller.Switch(63)` and `KickBallToLane` kicks the same `ballrelease` object before clearing it. That kicker supplies the validated position and makes the trough sequence explicit: drained ball at outhole 73, trough positions 72/74/63, then solenoid 15 releases the rightmost ball into a shooter lane.

## Rudy comprises separate mechanisms

Rudy's head assembly combines three independent systems:

1. The jaw uses solenoid 21, a continuously running A-13997 DC gearmotor, and solenoid 22, its direction relay. Pinned `fh_handleMech` closes the open jaw when 21 is active alone and opens the closed jaw when 21 and 22 are active together. Dummy Jaw opto 51 detects a ball in the mouth.
2. Solenoids 26 and 27 latch the eyelids open and closed.
3. Solenoids 25 and 28 move the eyes right and left; neither active means straight ahead.

The retained table models no separate object for the jaw motor or the four eye/eyelid drives, so they are projections onto the parts they move: 21 and 22 onto the Dummy Jaw opto at the mouth, and 25-28 onto the eyelid assembly, the centre of the `PrLids` primitive's world-space mesh bounds, which spans both eyes. The handbook's solenoid-locations drawing prints 25-28 inside Rudy's head outline and 21 at the top of the jaw's guide pair. It prints 22 in the row of back-panel labels along the top rail, so the C-13963 driver may sit on the back panel behind Rudy; the projection keeps it with the jaw it drives.

## Trap door, gates, locks, and kickouts

Solenoids 5 and 6 open and close the upper-right trap door. The retained script derives switch 76 directly from the door primitive's `RotX`, asserting it at the closed angle rather than reading a discrete contact object. Switch 75 senses the upper-right loop path next to the door.

Solenoid 2 controls the upper-ramp/Steps-track diverter and automatically returns after the window modeled by `fh_handleMech`. Solenoid 14 controls the left-outlane Steps gate, rerouting a ball to the left shooter lane as a save feature; it likewise has no separate position sensor.

The three lock sensors 25, 27, and 28 share one A-14138 three-switch assembly. Solenoid 8 releases the locked balls for multiball: the retained script's `MBRelease` drops the `WaSw28` lock wall and swings the lock-release gate (`Lock_Release_Prim`, with the hidden `Flipper1` gate), and the handbook's solenoid drawing prints 8 on the release box there. Rudy's Hideout uses switch 46 and solenoid 3, while the separate Dummy Eject Hole uses switch 65 and solenoid 16.

The Steps is a raised staircase ramp on the left side, its track ending above the upper-left flipper. Switches 15, 26 and 36 sense the ball on its bottom, middle and top step, whose awards lamps 54 (Frenzy), 55 (Extra Ball) and 56 (500,000) show. The handbook's switch drawing draws them as three wire slots across the Steps track, close together near its upper end, and its lamp drawing puts the three lamps on small sockets on the track's left rail. The retained table places its three invisible star triggers on the track's right rail, spaced twice as far apart and 0.06-0.07 normalized from the slots, and lights the awards from hotspots on a sign raised about 200 units beside the track, 0.05-0.08 from the drawn sockets. All six coordinates are therefore measured on the drawings.

The manual really uses `Kickbig` twice: solenoid 3 is `Kickbig` and solenoid 4 is `Tunnel Kickbig`. These are distinct devices, not OCR errors or misspellings to normalize without evidence.

## Lamps and flashers

The controlled lamp matrix is fully populated. Addresses 53, 61, and 82 are marked `(x 2)` and have two spatially distinct physical bulbs. Same-named co-located table objects for 51, 52, and 72 are brightness/render layers around one manual-documented bulb, so each remains quantity one.

Lamp 12 is `Gangway 100,000`. The original operations manual's lamp matrix, the supplied November 1990 handbook's lamp matrix, and the physical playfield photograph agree; the original manual's isolated `Gangway 10,000` lamp-location entry is therefore a resolved one-digit typo. The physical award ladder is 75,000 / 100,000 / 150,000 / 200,000 / 250,000 / Extra Ball.

The November handbook's lamp-location drawing shows Steps lamps 56, 55, and 54 as top, middle, and bottom sockets on the Steps track; their coordinates are measured there (see the Steps above). In the retained table, `Top_finger_1`, `Mid_finger_1`, and `Bot_finger_1` are the five-unit-radius hotspots the script lights; the `_2`, `_3`, and `_4` objects are larger rendering layers.

Six printed flasher circuits carry explicit bulb quantities: 17 has three blue bulbs, 18 one Dummy flasher bulb, 19 two Clock bulbs, 20 two Superdog bulbs, 23 three red bulbs, and 24 three clear bulbs. Each of 17, 23 and 24 has a dome on the back panel at the top right (the table's Flupper dome primitive), a diamond insert beside the Steps (24 top, 23 middle, 17 bottom) and a dome on the right side wall (17 top, 23, 24 bottom); the handbook's solenoid drawing prints each number on both playfield sockets and once in a leader-less row of back-panel labels along the top rail. Circuit 19's two bulbs light the clock from under its centre, where the drawing prints 19 once and the table models one Light, so they share one placement. Circuit 20 has distinct `F20` and `F20a` Light objects, and the pinned community script assigns both to output 20, so the Superdog bulbs retain separate positions.

## General illumination

The L-9 ROM's T.6 G.I. test names the five public strings and, on Start, prints each one's wires, playfield and backbox pins, fuse and triac (`evidence/runtime/wpc-alpha/funhouse-fh_l9-gi-test.json`, built by `tools/funhouse_runtime_evidence.py` from the retained harness run):

| Public | ROM name | Feed / return | Playfield pins | Fuse | Triac | Loads |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | BACKGLASS UPPER | brown / white-brown | J120-1 / J120-7 | F110 | Q18 | backbox |
| 1 | RUDY / BACKGLASS | orange / white-orange | J120-2 / J120-8 | F109 | Q10 | Rudy's spotlight, lower backbox |
| 2 | REAR PLAYFIELD | yellow / white-yellow | J120-3 / J120-9 | F108 | Q14 | rear playfield |
| 3 | BACKGLASS CENTER | green / white-green | J120-5 / J120-10 | F107 | Q16 | backbox |
| 4 | FRONT PLAYFIELD | violet / white-violet | J120-6 / J120-11, cabinet J119-3 / J119-1 | F106 | Q12 | front playfield, under the apron, coin door |

This is the WPC power driver board's fixed triac wiring, and two owners' repairs on Pinside confirm it: one traced the spotlight on Rudy and the lower third of the backbox to the orange string and fuse F109, another the front playfield and coin-door lamps to the white-violet string, fuse F106 and triac Q12. The retained script agrees: Case 1 drives Rudy's spotlight, Case 2 the rear playfield, Case 4 the front playfield, and nothing on the playfield comes from 0 or 3.

The printed tables disagree only in their naming. The November handbook numbers the strings 01-05 in order and prints the triacs in that order, but its rows 02, 04 and 05 carry their names, wires and pins one string out of place, as Terminator 2's tables do, and the 2-40 parts list, which prints only number, bulb and name, puts the same names in the same rows: "Front Playfield" (white-violet, J119-1) is public 4, "Center Backglass / Right Rear Playfield" (white-orange, J120-8) is public 1, Rudy's spotlight being the right-rear playfield load, and "Top Playfield" (white-green, J120-10) stands where the ROM names public 3 BACKGLASS CENTER. The 3-17 interboard table repeats the swapped triacs beside correct wires, pins and fuses. Earlier versions of this note followed the printed row order and took public 3 for a mixed backglass and right-rear-playfield string; the ROM test and the owners' traces settle it as a backbox string.

Placements: public 1 is the spotlight, the retained table's `RudyShade` Light under its `pShade1`/`pShade2` lamp shade at the front right of Rudy; `RudySign1` and `RudySign2`, which Case 1 also drives, are `f_refl` glow sprites painted on Rudy and make no socket. The retained 1.3 table draws a bulb at only some of the Lights its G.I. handler drives: three of public 2's 19 `GI_Upper` Lights sit on `BulbFil` filament primitives, and eleven sockets of public 4's 45 `GI_Lower` Lights have a filament primitive or their own bulb mesh. A later edit of the same table in the local library (table version 2.0c; the retained file's table info says 1.2d) models a bulb, with `pBulb` glass, `pFiliment` filament and `pFBase` base primitives, under each Light its script assigns to public 2 (`GI_UpperBulbs`, 14) and public 4 (`GI_LowerBulbs`, 11). Each socket is one of those bulbs with a driven 1.3 Light within 0.01 normalized, placed on the 1.3 Light that shows its bulb mesh, else the one on a filament primitive, else the one with the smallest falloff: 14 sockets for public 2 and 11 for public 4. The 2.0c table shares its authors with 1.3, so it confirms where they model a bulb rather than the positions independently; the manuals draw no G.I. socket. Three driven 1.3 render lights sit under no bulb in either table and are not placed: `Light22` beside the `Light23` socket at the upper right, and the two `Bottom_GI` lights below the flippers. The parts supplier in the second owner thread names G.I. bulbs under the apron, and the 1.3 table's two `Bottom_GI` lights sit under its apron instruction cards (`pIC_Left`, `pIC_Right`) with their halo at card height, as if those bulbs lit the cards from below; but no manual page, drawing or parts list draws them and neither table models a bulb there, so their number and positions are unknown. No source gives a per-string bulb count, so no quantity is asserted.

## Spatial evidence

Coordinates use the retained table bounds `left=0 top=0 right=964 bottom=2162`, normalized as `x/964` and `y/2162`, with `x=0` left, `x=1` right, `y=0` rear/backglass, and `y=1` apron/player. Cabinet, DIP, constant, unused, and virtual positions carry explicit not-applicable records. Projections are limited to a mechanism's own known object and are enumerated in the spatial audit.

Every placement the factory drawings mark was checked against them with `tools/drawing_callouts.py` (`tools/seeds/williams/funhouse-1990-callouts.json`). The November 1990 handbook prints the solenoid, lamp and switch location drawings at 600 dpi, the same artwork as the operations manual's 2-40, 2-36 and 2-38 drawings. An independent reader transcribed every callout from the page alone; each page is fitted on its three jet-bumper caps, its three flipper pivots and its outer frame's top corners, which match the table bounds. 100 of the 102 checked placements agree within 0.07 normalized under both the control fit and the leave-one-out callout fit; the other two are the second bulbs of lamp 53 and flasher 20, under an insert the drawing marks once. A number printed with no leader where it names no single part checks nothing, and the audit lists the 36 placements whose only read is such a number. The check moved solenoid 8 from the clock, where an earlier version had copied lamp 28's coordinate, onto the lock release, and the Steps switches and lamps onto the drawing.

A placement names the bulb, never a glow sprite. The script flashes only `wf_on_blur` sprites for lamps 57 (Ramp Overhead Lamp) and 58 (Rt. Gangway Overhead Lamp) and `f_refl` sprites beside lamp 71; their bulbs are the overhead `BulbFil2` and `BulbFil1` filaments, 12 units from the sprites, and the `L71` lamp glass. The Magic Mirror's column of six lamps (71, 74-78) and the three back-panel flasher domes are primitives, placed at the centres of their world-space mesh bounds in the retained OBJ export rather than at their stored positions, which lie up to 0.009 normalized away. The drawing prints "81" on a round insert beside the S-T-E-P "P" target, where no 31 appears; the switch matrix marks 81 Not Used, so it is read literally and checks nothing.

Coverage is `partial`, missing only `spatial_placement`: catalog identity, address enumeration, semantic names, polarity/normalization, physical wiring, displays, mechanisms, variants, recreation notes and provenance are validated, every placement the record makes is validated, and no conflict remains. The blocker is the apron G.I. bulbs of public 4 above, whose number and positions no source gives. Resolution path: a recreation that models those bulbs, or a drawing that locates them, checked for number and sockets against a photograph of a FunHouse playfield with the apron removed, which any owner can take.
