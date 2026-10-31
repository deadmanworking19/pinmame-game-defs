# Terminator 3: Rise of the Machines (Stern, 2003)

Coverage: **partial - every I/O address, controller binding, polarity, wiring detail, mechanism, variant and
recreation note is source-reconciled except lamp 63, which the manual and the ROM's own lamp test print NOT USED but
the ROM drives in step with the T-X lamp 64, so `output_semantics` is missing; `spatial_placement` is missing because
the retained table does not model the trough or the T-X lockup, draws the T-X flashers and the Super Jackpot flasher
on no bulb Light, binds every lamp to a bulb-mode Light that shows no bulb mesh so no lamp is placed, the UK-only coils
are projections, and no placement has been checked against the factory location drawings**

## Identity and evidence precedence

This is Stern Pinball's Terminator 3: Rise of the Machines of June 2003 (IPDB 4787, OPDB `GR91N-MLOyE`), designed by
Steve Ritchie on the Sega/Stern Whitestar board set. The record holds all fourteen `term3*` drivers of pinned PinMAME:
CPU 4.00 (`term3`, the catalog root, with French, German, Italian and Spanish display sets), CPU 3.01 (the same five
languages) and CPU 2.05 (English, French, Italian and Spanish; pinned PinMAME has no German 2.05 set).
`src/wpc/segames.c` builds every one from `INITGAME(term3, GEN_WS, se_dmd128x32, SE_BOARDID_520_5068_01)` on
`de_mSES2` with the same `T3_SND` sound ROMs: a 128x32 DMD, lower flippers only (`FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L)`),
two extra lamp columns (lamps 1-80), no custom solenoids and the three-output auxiliary driver board 520-5068-01. All
fourteen are `identical`; they differ in game code and display language. IPDB notes that later production reportedly
used a modified Whitestar sound section; that changes no switch, lamp or driver address.

Authority follows the runbook. The known-working table's embedded script decides controller callbacks; the official
service manual (218 pages, the copy IPDB hosts, retrieved through the Wayback Machine) decides construction, wiring,
parts and placement on the drawings; pinned PinMAME decides routing. Seven LibPinMAME harness runs of `term3` walk the
ROM's own Portals Switch, Dedicated Switch, Single Lamp and Single Coil Tests, which print a name and wire colours for
every address, and exercise the stacking opto, a ball serve and a scripted game. The curator refuses to build unless
each service-test frame agrees with the manual's grids and coil chart. The retained table is Hanibal's 1.5 release; the
pinned standalone corpus holds the same script, and the pinned Siggi script belongs to jpsalas's later table, so it
corroborates the bindings from a different table.

## Controller platform and address topology

- **Switches.** Matrix 1-64 is sequential (column = (n - 1) / 8 + 1). 9, 26, 27, 47, 48, 63 and 64 are NOT USED. 3 is the
  "6th Coin Slot Future Use" position, which the ROM's Switch Test ignores (it prints NONE); 7, the 5th coin slot, is
  also Future Use but the ROM names it. 2 is the 4th coin slot (European use), 53 the optional tournament start button,
  and 1 and 8 the UK-only Post Save buttons. The dedicated inputs are -3 memory protect, -2/-1/0 the red/green/black
  service buttons (DS-6/7/8), 84 left button (DS-1), 83 left EOS (DS-2), 82 right button (DS-3), 81 right EOS (DS-4) and
  88, the NOT USED DS-5; 85-87 reach no input.
- **DIP switches.** SW300 positions 1-5 select the country; the manual's nineteen charts never turn 6-8 on. `sega.vbs`'s
  DIP form covers only positions 1-4, and three of its labels (0x05 UK, 0x09 Japan, 0x0d Brazil) name other countries
  than this game's chart (Finland, Denmark, Australia); follow the chart.
- **Solenoids.** Public 1-32 are Q1-Q32 except the flippers: `se_solenoid_w` masks Q15 (left) and Q16 (right) off public
  15/16 and publishes them at 47 and 45, and `core.c` synthesizes 48 and 46 from those. Bind the left flipper coil at 48
  and the right at 46; 45 and 47 are their power-phase states. Public 15 is the fast-flip / game-on state
  (`sega.vbs`'s `GameOnSolenoid = 15`), which `MACHINE_INIT(se)` reads from CPU RAM 0x04 for every `term3` set; it rose
  about 5.4 s after Start in both game runs and fell at the drain. 33-35 are the UK-only auxiliary outputs AUX 1-3.
  16, 36-44, 49 and 50 are unused. Q6, Q7, Q19 and Q25 are NOT USED on the chart and fired only in the Single Coil Test.
- **Lamps** 1-80 run across each row (lamp = (row - 1) x 8 + column). 70 is NOT USED: the Single Lamp Test drives it
  at its step 70, which prints NOT USED, and no run outside that test saw it driven. 63 is unresolved (below). 53
  (start), 54 (tournament) and 79 (optional launch button) are cabinet lamps, 65-69 light the backbox targets. **G.I.**
  is one relay at public 0.
- **End-of-stroke inputs.** term3 declares `FLIP_SOL(FLIP_L)`, which `core.h` defines to include `FLIP_EOS`, so `core.c`
  rewrites 81 and 83 on every update from the flipper solenoids: 0 while a flipper is off and 1 once it has been on for
  two updates. A host write never reaches the ROM; the Dedicated Switch Test stayed at NONE while the host held either
  input, and writes to 83 during a held flipper changed nothing. The manual draws both as N.C. switches that open at the
  end of the stroke, the opposite level; the record keeps the construction in `normally_closed` and the emulator's
  behaviour in the device notes. A recreation need not write either input.

## Lamp 63

The Lamp Matrix Grid prints 63 NOT USED in a black cell, the lamp location drawing marks no 63, and the ROM's own
Single Lamp Test names it NOT USED. Yet in every harness run except the lamp test the ROM switched it at exactly the
same instants as the T-X lamp 64, from about 9.3 s after power-up through attract mode and play. No retained script
binds it. Whether that state reaches a second bulb wired with 64, a socket an earlier build fitted, or nothing is not
settled, so it carries `availability = unknown`. A look under the playfield or a continuity check at row 8, column 7
(RED-GRY J12-P9 / YEL-VIO J13-P3) on a production machine would settle it. Lamp 70 shows no such activity.

## Switch polarity and names

Whitestar's `switch_r` hands the CPU `~core_getSwCol` with no per-game inversion, so public 1 is the closed-contact
reading for every matrix switch, and `dedswitch_r` does the same for the dedicated inputs.

- **Optos.** The trough's Dual OPTO boards (VUK opto 14 and stacking opto 15) and the single opto of the T-X cannon
  trough (33) read 1 while the beam is blocked: with light on the receiver the output transistor is off and acts as an
  open switch (OPTO Troubleshooting: "CLOSED OPTO (Light Blocked) = SWITCH CLOSED"), so each has `normally_closed =
  false`. The single receiver repeats the dual receiver's circuit; its parts list swaps the two transistor part numbers.
- **Names.** The labels follow the Switch Matrix Grid (DR. 4). The ROM abbreviates LEFT/RIGHT to LT/RT on the UK buttons
  1 and 8; every other matrix name matches.
- **Initial state.** Four balls rest on 11-14 and -3 is 1 with the coin door shut.

## Ball handling

- **Trough.** Four balls rest on micro switches 11 (left), 12, 13 and the VUK opto 14 at the up-kicker. Q1 (26-1200)
  kicks the ball on 14 up past the stacking opto 15 into the shooter lane. Pulse 15 once per kicked ball; the retained
  table never writes it. With four balls home in attract mode, each rise of 15 made the ROM fire Q1 six times about
  0.8 s apart and then the auto launch Q2 once, 9.1 s after the rise.
- **Shooter and gun.** The served ball rests on 16 in front of the Ball Auto Launch Q2 (22-1080). The player launches it
  with the gun trigger 55 on the cabinet front; an operator may fit the optional Ball Launch Button with lamp 79 instead.
  In the ball-serve run the ROM held the ball on 16 for 10 s and fired Q2 81 ms after the trigger was pulled. In the
  gameplay run the scenario put a ball on 16 before the ROM had served one; the ROM never fired Q1 and fired Q2 0.76 s
  later without a trigger pull, then every 1.6-1.7 s while the ball stayed on 16 and once 43 ms after the trigger was
  pulled, seven times in all, the retry behaviour the Diagnostic Aids page describes for #16 and #2. The record does not
  claim which condition makes the ROM launch on its own. In both runs lamp 79 blinked from just after the game-on state
  rose until about 1.5 s after the trigger was pulled.
- **Skill shot and back panel.** The back panel carries a wire ramp into a back-channel trough. The Kicker (Ball Stop)
  Assembly there (Q21, which the coil chart calls BACK PANEL DIVERTER) holds the ball in that trough while energized, and
  the skill-shot switch 52 sits behind the back panel under the trough. A closure of 52 fired Q21.
- **VUK.** A ball on the heavy-duty micro switch 36 is kicked by Q13 (26-1200) up the VUK chute onto the wire ramp. In the
  Switch Test closing 36 fired Q13, and a ball resting there in a game drew Q13 with 3, 8 and 30.
- **T-X cannon lockup.** The TX Cannon Trough at the T-X figure holds up to three balls on the opto 33 (lockup 1, right)
  and micro switches 34 and 35; the above-playfield switch 31 (T-X MADE) is drawn beside them, and both scripts pulse 31
  as a ball enters. The TX Vertical Up-Kicker Q14 (26-1200) kicks a ball into the T-X cannon's wire ramp; IPDB says the
  cannon shoots the ball at the right flipper. Closing 33, 34 or 35 in the Switch Test fired Q14; a ball on 33 in a game
  drew Q14 with the switched backbox G.I. 4 and flashers 26 and 30 while the G.I. blinked.
- **Kickback.** The left outlane kickback Q12 (23-800) fired when 57 closed; lamp 37 is printed KICK BACK.
- **Up posts.** Two Ball Deflector Assemblies (Q22 left, Q23 center, 26-1200) deflect the ball into the top VUKs or top
  lanes. Each orbit switch (24, 28, 29, 46) made the ROM hold both on for about 2.1 s in the gameplay run. Neither has a
  switch.

## Scoring parts

A 1-bank drop target on 25, raised by Q3 (27-1500) and knocked down by the mini trip coil Q8 (32-1250); the ROM fires
both as game logic, Q3 at power-up, Start, the drain and on several switches, Q8 on the launch, the backbox target 43
and around the target's own motion. Three bumpers (Q9-Q11 / 49-51), two slingshots with two contacts each (Q17/59,
Q18/62), two 3-bank stand-up groups (17-19 left, 20-22 right), the standup 10, the captive ball target 23, three ramps
(30 left, 40 center, 32 right), the orbits (28/29 left, 24/46 right), three top lanes (37-39) and four lanes (57, 58,
60, 61).

## RPG backbox cannon

IPDB: "Backbox reciprocating cannon shoots Delrin Ball horizontally at 5 targets." In the backbox insert, Q20 drives a
relay board that runs a 24 V AC 21 RPM motor; its eccentric drive wheel moves the cannon's kicker bracket up and down.
The RPG Cannon Kicker Q5 (23-800) shoots the cannon's own ball at five stand-up targets 41 (top) to 45 (bottom), each
with an insert lamp 65-69. No switch reports the cannon's position. Q4 switches eight #44 lamps in the centre of the
arc (19 V AC), and Q27/Q28 flash four #89 lamps down each side. A shipping post under the cannon must be removed before
power-up. The RPG Backbox Test runs the motor one full cycle and fires the kicker from the gun trigger. In the gameplay
run closing each target fired neither Q5 nor Q20; only the Single Coil Test fired them, so the record does not describe
when the game moves or fires the cannon.

## UK equipment

A UK machine adds the auxiliary board 520-5068-01 with three outputs: AUX 1 (33) and AUX 3 (35), outlane Ball Deflector
Assemblies 500-5788-02, and AUX 2 (34), the center Up/Down Post 500-6293-00 between the flippers, plus two cabinet
buttons under the flipper buttons (1 left, 8 right). The coil chart and the ROM call all three UP/DOWN POST; the record
labels AUX 1 and AUX 3 by their assembly. On term3's default settings, holding either button fired none of 33-35. The
US table models none of them; their placements are projections.

## Lamps, flashers and general illumination

- **Lamps.** 78 matrix lamps are fitted: 1-52, 55-62, 64, 71-78 and 80 on the playfield, 65-69 in the backbox insert,
  and 53, 54 (tournament kit) and 79 (optional launch button) in the cabinet. 57 and 64 are #44 bulbs, 71 is the T-850
  head's red LED (TERMINATOR EYE), the rest #555.
- **Flashers.** Q26 (two blue at the T-X figure), Q27 and Q28 (four each in the backbox insert), Q29 (one at the centre,
  below the playfield), Q30 (four red across the back panel), Q31 (two red at mid-field) and Q32 (two red at the
  slingshots). Q31 and Q32 are #906 bulbs; se.c models all seven as #89. Q26 stayed lit for 15.8 s after a launch and
  14.5 s with a ball in the lockup, so treat it as a lamp-like output, not only a flash.
- **G.I.** One relay switches four fused 5.7 V AC circuits, 75 printed bulbs: 40 on the playfield (two of them reflector
  bulbs aimed at the T-X and T-850 heads, three in the pop bumpers), ten on the back panel's light board, 23 in the
  backbox insert and two on the coin door. The page warns that quantities may change during production. It counts the
  three pop-bumper G.I. bulbs among circuit V's #44 bulbs, while the bumper assembly page names a #555 wedge-base bulb
  (165-5002-00) in each bumper, and the wiring page's text layer carries an unrendered note that G.I. above the
  playfield is #555. The assembly page is the more specific source for the bumper bulb. The ROM blinks the G.I. on
  Start, several shots and the lockup, and switches it off at the drain.

## Retained-table defects

The retained 1.5 table is known to work, but a recreation built from its script inherits these defects:

- The stacking opto 15, the UK buttons 1 and 8 and the EOS inputs 81/83 are never written (the EOS inputs need not be).
- `Solcallback(29)` is commented out, so the Super Jackpot flasher draws nothing; Q26 lights non-bulb objects only.
- No line copies lamps 73-79 onto a Light, so the six insert lamps 73-78 between the flippers and in the arcs are dark.
- The backbox kicker Q5 fires only while the table's own ball is in its backbox; the cannon motor is a timer.
- The skill-shot switch 52 is a trigger on the playfield's rear edge and the back-panel ball stop two walls there.
- `sega.vbs` names 55 `swSlamTilt`, so the VPinMAME slam-tilt key pulls the gun trigger.

## Spatial status and why the record stays partial

Placements come from the retained table's script-bound objects, normalized against its 1025 x 2325 bounds. They stay
`observed` and `spatial_placement` stays missing because:

- **Projections onto mechanism objects.** The table does not model the trough (11-15), projected onto the release
  kicker; the lockup (33-35) and the T-X VUK, projected onto the lockup entry kicker; the EOS contacts sit on the
  flippers and the auto launch on the shooter-lane trigger.
- **Unplaced flashers.** The T-X flashers 26 and the Super Jackpot flasher 29 have no bulb Light in the table. Q31
  and Q32 sit on bulb Lights that coincide with their Flupper dome primitives.
- **Unplaced lamps.** No lamp is placed. The script drives a bulb-mode Light for every lamp it binds (the
  Flasherupdate timer's copy `l<n>a` of each insert `l<n>`, `l64` with its copy `l64a`, and `l71`), and none of them
  shows a bulb mesh; the table models no bulb primitive or baked bulb mesh under the inserts, so these Lights mark no
  socket (docs/SPATIAL.md, picking the bulb). Lamps 73-78 are on no Light at all. In the heads the toy primitives LED8
  and LED9 (blue, image `bulb`) sit beside `l64` and `l64a` and LED7 (red) beside `l71`; the record does not take them
  as sockets without a check against the lamp location drawing. Placing lamps 1-80 needs a table that models the
  insert bulbs or a reproducible measurement on the lamp location drawing (DR. 5).
- **UK coils.** AUX 1-3 are projections onto US-table objects.
- **No callout check.** No placement has been fitted against the switch, lamp, coil and flash location drawings
  (DR. 4, DR. 5 and DR. 7).
- **G.I.** The table models 43 G.I. sockets that draw a bulb against 40 playfield bulbs on the G.I. page; five lie at
  the rear edge where the back panel's light board stands, and none is matched to a circuit.

Nothing here is a disagreement between sources about the machine, so the record carries no conflicts. Wiring-detail
differences (Q30's power wire, the start/tournament lamp pins, the backbox target part number, the Q4 bulb part) and
naming differences (the AUX outputs, the ROM's abbreviations) are stated in the device notes.

## Author construction checklist

- **Ball path.** Build the 4-ball trough with stacking opto, the gun-fired auto-launch shooter lane and its steel ramp,
  the back panel's ramp, trough and ball stop with the skill-shot switch, the VUK, the T-X cannon lockup with its
  up-kicker and wire ramp, three ramps, two orbits, the top lanes and the left outlane kickback.
- **Backbox.** Model the RPG cannon: a motor that moves while Q20 is on, a kicker Q5 that shoots its own ball at targets
  41-45, the insert lamps 65-69, the switched G.I. Q4 and the flashers Q27/Q28.
- **Scoring parts.** The drop target with both coils, three bumpers, two slingshots, two flippers, the 3-banks, the
  standup, the captive ball and the up posts Q22/Q23.
- **Initial state.** Initialize 11-14 and -3 at 1. Pulse 15 per kicked ball.
- **Bindings.** Bind Q15 at 48 and Q16 at 46; 45/47 are power phases and 15 is game-on. Bind 33-35 and buttons 1 and 8
  only for a UK build, 24 only with a coin meter, 53/54 only with the tournament kit and 79 only with the launch button.
  Leave 63 unbound until its load is known.
- **Displays and lights.** One 128x32 DMD in the cabinet. Recreate the 40 playfield G.I. bulbs, the back panel, insert
  and coin-door G.I., all lamps and every flasher bulb.

## Sources

- `manual.stern.terminator-3-rise-of-the-machines.2003`: SHA-256
  `fc11f0a19bd78b83857de36338339fb598386b962f934fe47dfbe1696d5e1a9b`, IPDB 4787's service manual; excerpts under
  `evidence/excerpts/stern.terminator-3-rise-of-the-machines.2003/`.
- `identity.stern.terminator-3-rise-of-the-machines.2003`: the IPDB 4787 page through the Wayback Machine
  (`e91a2eb6...`).
- `vpx-table.terminator-3-hanibal-1-5` and its embedded script (`33aaf9c0...`), with the retained extraction and its
  manifest.
- `vpx-script.33aaf9c0d4b89d15` (the same script in the pinned standalone corpus) and `vpx-script.1c88e99f0fa1319d`
  (the pinned Siggi script of jpsalas's later table).
- `vpm-script-library.sega-vbs`: `sega.vbs` (`d6e508aa...`).
- `runtime.terminator-3.term3`: seven LibPinMAME runs, summarized in
  `evidence/runtime/whitestar/terminator-3-term3-service-tests-and-gameplay.json`.
