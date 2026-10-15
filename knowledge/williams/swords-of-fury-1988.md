# Swords of Fury (Williams 1988)

Coverage: **partial - controller and physical-device curation, with explicit spatial gaps and unknown construction polarity for the optional German score-board input.**

## Physical identity and software

Williams model 559 is the June24,1988 physical machine, verified against IPDB2486 and the factory operations/parts manuals. The OPDB identity remains `GrPzV-MDxj7`. It has four flippers, a five-target M-A-G-I-C mini-playfield row with five individual reset coils, three spinners, seven Avenger standups, two slingshots, two powered diverters, an outlane kickback, eject/lock fixtures, and a three-ball trough. No pop bumper or motorized toy is fitted.

The five pinned drivers are `swrds_l1`, `swrds_l2`, `swrds_lg2`, `swrds_rr1`, and `swrds_rr1b`. They select one `swrdsGameData` (`GEN_S11B`, `s11_dispS11b1`, mux12, `FLIP_SWNO(58,60)`, no per-game flags or custom solenoids). L-1 and L-2 are production revisions. LG-2 is the German U27 L-2 upgrade with the L-1 U26, whose chip label G2 differs from its displayed L-2. The Richrom/Lionman revisions change firmware on the1988 physical hardware; one suppresses swords sounds. Firmware dates are not new machine dates. Available ROMs were checked member-by-member against the pinned source, including inherited sound ROMs in the parent archive; no German gameplay run is claimed without a matching archive.

## Controller contract

Switches and lamps use sequential column-major addresses 1-64. Preserve every matrix cell, including blank/unused rows. The four service switches are-7 Advance,-6 Auto-Up/Manual-Down,-5 CPU Diagnostic and-4 Sound Diagnostic. One country jumper is DIP0. The System 11 CPU reads the switch matrix directly and this game supplies a zero inversion mask. Physical construction and ROM-active level must be read together; no consumer-wide inversion should be added.

The cabinet flipper buttons are public 82(right) and 84(left), copied on every update to matrix 60/58. A host write to 60/58 is overwritten. The remaining six positions81-88 are enumerated as unreachable by the ROM's eight-bit column strobe. The driver's cabinet wiring does not synthesize EOS inputs. Synthetic outputs45/46 and 47/48 describe right/left flipper state while game-on 23 enables; the cabinet buttons operate two bats per side. These outputs do not create four extra independently controlled physical coils.

Solenoids1-8 are the A side of the relay-multiplexed driver bank;25-32 are its C side, selected by relay 12. Keep factory printed A/C names and public addresses distinct. Special drives17-22 are derived from the selected System 11 PIA permutation and checked against the game's own service order. General illumination is an ordinary solenoid-group output 10, not a separate GI callback. The same output energizes relay boards on the playfield and insert board; an energized relay blacks out GI. The address enumeration also disposes the driver-specific/custom/synthetic ranges through 64; a quiet trace alone is not used to call an address unused.

Four physical seven-digit score displays occupy controller indices 0-3 and segment starts 1,9,21,29. The upper pair is alphanumeric and the lower pair numeric; all four are in the backbox. `s11_dispS11b1` aliases `s11_dispS11a`.

## Physical evidence and source distinctions

The operations manual's parts lists, wiring matrices and schematics control physical fitment. Its switch 2 parts-list row says Not Used, while its own matrix positively identifies the German Score Board and the ROM uses that name. Input2 therefore remains optional German cabinet hardware. This game does not set `S11_MUXSW2`, so it must not be relabelled as A/C feedback. Center coin5 is explicitly Not Used(USA) and is optional rather than silently dropped.

Lamp8 and 25 cells are blank; the transcriptions preserve that instead of manufacturing the words Not Used. Seven bindings6,7,16,41,42,51,52 each have an explicit two-lamp mark: one on the playfield and one on the backglass. The backglass header is not a backbox-only classification for those seven. Jackpot lamps57-64 are backglass-only. Each physical emitter is counted once; a bloom light or VR proxy is not another bulb.

The retained bord table binds `swrds_l2`, credits rothbauerw, Uncle Paulie, Sixtoe and Apophis, and includes upper-playfield/VR changes through 005. It was supplied by the user and retained byte-for-byte, but was not launched in VPX during curation. Controller claims are cross-checked with the real ROM's service/gameplay probes. Its geometry is observed recreation evidence, not automatically a factory measurement. The older local1.5 script credits takut/HauntFreaks and expressly says the table was not verified; it is a lead, not independent validation.

Output11's table callback is commented out even though the factory fits the backglass swords flashers. Decorative VR effects on 25/30/32 and synthetic46/47 do not establish extra backglass flashers. The bell-like sound at7 is a table substitution for the factory knocker/optional ticket circuit. These are consumed-table omissions/substitutions, not unresolved disagreements about the physical machine.

## Spatial evidence and remaining work

The optional German score-board input 2 has a proven public address/name, but its physical contact construction and rest level remain unproved. `normally_closed` is deliberately absent and `coverage.missing` includes `polarity`. A German cabinet/score-board wiring or assembly record is needed to settle this; the shared-ROM service response alone cannot do so.

Player-view coordinates use x0 left/x1 right and y0 rear/x1 apron. Exact retained bounds are 0,0 to 952.9412,1976.471 VPX units. Coordinates are produced by the repository extraction helper with six-decimal rounding. Retained source/extraction manifests and per-file hashes make them reproducible.

Sensor/actuator positions projected onto their own drop target, trough/kicker fixture or slingshot wall are disclosed as projections. They do not locate the hidden contact, opto PCB or coil winding. Under-insert lamp centres are candidate projections to the script-bound render light; physical socket locations are unproved; B-suffixed bloom helpers and primitive origins are excluded. The drop-bank lamps17-21 have material callbacks rather than usable physical bulb centres. FL_* light glows and f*_render flashers are not accepted as sockets. The 15 script-controlled GI lights and three further GI objects are retained candidates only: no physical GI socket or relay mounting centre is accepted from their effect geometry.

The open spatial work is concrete: independently measured drop-bank and flasher socket centres; all actual playfield GI bulbs and wiring; hidden trough/drop/opto/tilt contact positions rather than fixture projections; physical winding centres where only mechanism anchors exist; and factory-to-table reconciliation of nominal Left/Right top-loop61/62. Cabinet/backbox devices deliberately have no normalized playfield position. Each affected device and the generated spatial report retains its exact gap.

IPDB photos70430(Olivier Rannou, partly stripped playfield) and 31484(James Greenhalgh, upper playfield), and Pinside gallery photo4086267(backglass), were inspected privately. They corroborate the physical layout and paired backglass effects, but do not show the hidden under-insert sockets with a calibrated frame. Photographs and original manuals/tables remain outside Git; only factual excerpts, compact derived evidence and hashes are committed. The machine remains partial until those physical placement requirements are actually met.

## Mechanism recreation

The following mechanism descriptions are generated from the reviewed semantic seed; table velocity, travel speed, random variation and animation timings are recreation tuning unless a source explicitly measures them.

The factory wiring table explicitly gives top-center output 9 two flashers (one playfield, one insert board), output 11 three insert-board swords flashers, output 26 two playfield flashers and output 27 one insert-board plus one playfield flasher. The abbreviated location list omits the playfield branch at 9. Wiring-table AE-23-800 versus parts-list AF-23-800 at 1/2/4 and opto-board C-11844 versus operations C-11184 are retained as wiring/part details, with structured data following the game wiring table or dedicated assembly table.

## Portable evidence

The machine source records link reviewed factual transcriptions under `evidence/excerpts/williams.swords-of-fury.1988/`. The compact `evidence/runtime/system-11/swords-of-fury-service-and-gameplay.json` pins 17 complete traces and scenarios. It preserves source/ROM/native identity and diagnostic text without ROM bytes. Run `tools/verify_swords_of_fury_runtime.py` with the review-artifacts root to independently reconstruct the controller contracts. The literal curator seed and evidence binding register under `tools/seeds/williams/` reproduce the definition and pin all retained originals, complete extraction, manual renders and raw probes. Source roles remain distinct: factory physical construction, pinned emulator transport, ROM behavior, and observed/candidate table geometry.

### Outhole, Three-Ball Trough and Manual Shooter

Three installed balls. Outhole10 kicks via1 into the trough; trough11/12/13 are right/middle/left. Feeder2 serves the right-hand ball to shooter14; remaining balls gravity-feed. Assert occupied switches while a ball rests, update only on actual movement. Manual spring plunger launches the served ball; no ROM-controlled shooter coil. The retained table initializes11..13 closed. Ball search/retries are ROM behavior, not proof a coil directly closes a sensor.

### M-A-G-I-C Individually Reset Drop Targets

Five upper mini-playfield targets ordered M,A,G,I,C from left to right. Each target latches down and asserts its opto until its OWN reset:17->15,18->5,19->8,20->21,21->22. Reset raises target and clears its opto after physical travel. Do not reset the whole row from one coil or pulse the switches. The lowered row lets a ball enter the rear payoff return; progressive ROM reset timing changes time on the mini-playfield. Initial reset, restart, incomplete resets and stuck-target search are handled by ROM; a coil callback alone is not proof of completed travel. Parts Information PDF 17 identifies C-11844 as the opto board, not the complete bank assembly; its OP1..OP5 use 5490-10159-00 opto interrupters. Operations PDF 42 prints C-11184, retained as the parts-list discrepancy.

### Top Left Eject Hole

Ball rests in top-left eject hole54 until coil 4 ejects it into the mini-playfield route. Hold54 while captured, release when ball leaves. Retained SolLock clears54 on kick; table random velocity is tuning, not factory data.

### Left Slot Lockup and Upper Entry

Upper-left entry56 leads to the left-slot lockup55. Hold55 while captured. Coil6 kicks the ball up the left route; the retained script clears55 on ejection. Entry56 is a separate passing sensor, not directly actuated by the coil. Ball routing, not switch naming, distinguishes this from top eject54.

### Left Outlane Kickback

Ball in left outlane57 can be returned up the lane by kickback14 when lit. Hold/contact follows ball location; a kick changes velocity and switch releases only when the ball leaves. Lamp49 indicates availability; output 16 is a separate local flasher. The table's velocity/lift parameters are recreation tuning.

### Bottom Diverter

Coil17 moves the bottom diverter finger; deenergizing returns it by spring. Script bottomgate.RotateToEnd on1 and RotateToStart on0. Tube switch 16 senses passing balls, not diverter end position. No separate end-stop feedback is declared; route balls from actual gate pose and geometry, not from a synthetic sensor.

### Top Diverter

Coil19 moves the top diverter finger; deenergizing returns it by spring. Script topgate.RotateToEnd on1 and RotateToStart on0. Tube switch 15 senses passing balls, not diverter end position. No separate end-stop feedback is declared; route balls from actual gate pose and geometry, not from a synthetic sensor.

### Left Slingshot

Left rubber impact closes scoring switch 63; the kick contact and coil 18 supply rebound. Scoring contact differs from the direct special-solenoid kick contact; retained table animates rubber locally and pulses the scoring switch. Do not infer a ROM-fired coil callback merely from that animation.

### Right Slingshot

Right rubber impact closes scoring switch 64; the kick contact and coil 20 supply rebound. Scoring contact differs from the direct special-solenoid kick contact; retained table animates rubber locally and pulses the scoring switch. Do not infer a ROM-fired coil callback merely from that animation.

### Right Cabinet Flipper Pair

One cabinet right button drives the lower-right and mini-playfield right bats. Lower pair coils are FL11630/50VDC; upper-left and mini-playfield right use FL11753/50VDC. Cabinet wiring and EOS contacts manage power/hold; PinMAME only publishes synthetic pair[45, 46] from button 82 when23 enables. Hold button for raised bats, release for spring return. EOS is not a separately host-driven public sensor on this driver. Script SolRFlipper moves both bats; geometry and speed remain table-owned.

### Left Cabinet Flipper Pair

One cabinet left button drives the lower-left and upper-left bats. Lower pair coils are FL11630/50VDC; upper-left and mini-playfield right use FL11753/50VDC. Cabinet wiring and EOS contacts manage power/hold; PinMAME only publishes synthetic pair[47, 48] from button 84 when23 enables. Hold button for raised bats, release for spring return. EOS is not a separately host-driven public sensor on this driver. Script SolLFlipper moves both bats; geometry and speed remain table-owned.

### Spinners, Avenger Targets and Ramp/Loop Paths

Three spinners are23/24 in left loop and39 at left entry; pulse per actual rotation. Seven Avenger standups26..32 spring back after impact. Upper/lower right10-point contacts37/40 are separate from spinner39. Ramp/tube/return-lane switches pulse as balls pass, while resting lock/trough contacts hold. Top loop61/62 must keep their proven script bindings; their spatial sides are not silently corrected. Passive gates, rubber, rails, the centre mini-post and manual plunger require table geometry but no additional controller actuators.
