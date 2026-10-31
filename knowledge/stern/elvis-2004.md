# Elvis (Stern, 2004)

Coverage: **partial - every I/O address, controller binding, polarity, wiring detail, mechanism, variant and
recreation note is source-reconciled; `spatial_placement` is missing because every lamp the retained table binds is an
insert overlay without a bulb, the back-panel flashers and lamps and the Elvis spot light have no bulb object on the
playfield, the shooter-lane exit switch 10 has no table object, several mechanism parts are projections, and no
placement has been checked against the factory location drawings**

## Identity and evidence precedence

This is Stern Pinball's Elvis of 2004 (IPDB 4983, model I-0084), designed by Steve Ritchie, on Stern's Whitestar
platform with the CPU/Sound Board II (520-5300-00) and the 520-5137-01 I/O Power Driver Board. The manual's Appendix C
gives production start AUG 04 and manual part number 780-5084-00. IPDB points to a separate "Elvis Gold (Limited
Edition)" entry; no pinned driver distinguishes it and nothing held here documents its hardware, so this record does
not describe it.

The record holds all twenty-one Elvis drivers of pinned PinMAME: CPU 5.00 (`elvis`, the catalog root, and its
Spanish, German, French and Italian sets `elvisl`, `elvisg`, `elvisf`, `elvisi`), CPU 4.00 (`elv400` and its four
language sets), CPU 3.03 (`elv303` and four), CPU 3.02 (`elv302` and four) and CPU 1.00 (`elv100`).
`src/wpc/sims/se/prelim/elvis.c` builds every one on `de_mSES3` with one `init_elvis`, which installs `elvisGameData`
(GEN_WS, a 128x32 DMD, `FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L)`, two extra lamp columns, no custom solenoids, no auxiliary
board) and the `elvis_w` stepper model. A language set pairs that language's CPU, display and sound/voice ROMs; the
machine is the same. All twenty-one are `identical`. The manual's firmware appendix names game ROM A4.00 (check sum
$90FF, U210) and display ROM A4.01 ($0502, U5), the pair `elv400` loads (`elvscpua.400`, `elvsdspa.401`); no document
held here names a 5.00, 3.03, 3.02 or 1.00 release. Its boxed note maps file-name letters to languages: A USA, F
France, G Germany, I Italy, S or L Spain.

IPDB's Notable Features line says "Flippers (3)". The manual's 4-Flipper Circuit Wiring Diagram says "4-Flippers are
used (Lower & Upper Left, Lower & Upper Right)", its coil chart drives four flipper coils (Q13-Q16), the ROM's Single
Coil Test names all four, and the retained table models four; the record follows the manual.

Authority follows the runbook. The known-working table's embedded script decides controller callbacks; Stern's own
185-page service manual decides construction, wiring, parts and placement on the drawings; pinned PinMAME decides
routing. Nine LibPinMAME harness runs of `elvis` (5.00) read the ROM's own Switch, Dedicated Switch, Single Coil,
Single Lamp and ELVIS tests and exercised the switch-to-coil responses in a game. The retained table is jpsalas's VPX
1.0.2 (2017; the Elvis and Hound Dog objects by Steve Paradis). The pinned corpus script `Elvis (Stern 2004) WED SSF
Mod.vbs` is a sound modification of the same 1.0.2 script with identical controller bindings, so it corroborates them
without being independent.

## Controller platform and address topology

- Switches: `se.c`'s `switch_r` returns `~core_getSwCol` and the driver's `invSw` is zero, so public 1 is the CPU's
  closed-contact reading for matrix switches 1-64. `dedswitch_r` hands U206 the flipper column complemented and
  reordered: 84 is DS-1 (left button), 83 DS-2 (left EOS), 82 DS-3 (right button), 81 DS-4 (right EOS) and 88 DS-5
  (upper right button); 85-87 reach no input. The coin-door buttons are -2 (red, DS-6), -1 (green, DS-7) and 0 (black,
  DS-8), and -3 is the memory-protect switch, 1 while the coin door is closed.
- PinMAME's start/tilt/slam triple for this driver is 54/56/55. Address 55 is this machine's TOURNAMENT START (an
  optional tournament kit); Elvis has no slam tilt switch, so PinMAME's and `sega.vbs`'s slam-tilt label for 55 is a
  second name for the same input.
- Solenoids: `se_solenoid_w` masks the lower-flipper transistors off their own addresses and publishes Q15 (left) at
  47 and Q16 (right) at 45; `core.c` synthesizes the canonical 48 and 46 from them. Bind each lower flipper coil once,
  at 48 and 46. The upper flipper coils are ordinary outputs at 13 (upper left) and 14 (upper right).
- `MACHINE_INIT(se3)` gives every se3 game the fast-flip byte at CPU RAM 0x04, so public 15 is the game-on state for
  all twenty-one Elvis sets (`sega.vbs`: `GameOnSolenoid = 15`). It rose at Start in the gameplay run. Never wire it to
  a transistor: physical Q15 is the left flipper at 48.
- `elvis_w`, installed on the solenoid latches 0x2000-0x2003, passes every write to `se_solenoid_w` and, on the
  Q25-Q32 latch, models the figure: the low four bits are the stepper phases Q25-Q28, bit 4 the legs coil Q29 and
  bit 5 the arms coil Q30. The phase order 0x0c, 0x06, 0x03, 0x09 counts the position up and the reverse order counts
  it down to zero. On every non-zero phase write a non-VPinMAME build (LibPinMAME) writes switch 33 itself, 1 at
  position zero and 0 elsewhere; in VPinMAME that line is compiled out and the table's own mech writes 33.
- Lamps 1-80 (64 plus two extra columns) and one G.I. relay at G.I. 0. `MACHINE_INIT(se3)` gives the Elvis root's
  sets the #89 flasher bulb model on 20-23 and 31-32; only 20 and 21 carry #89 bulbs, the rest #906. That is an
  emulator rendering choice, not a wiring fact.
- `elvisGameData` declares no Whitestar auxiliary board, so the UK-only 3X Transistor Driver Board 520-5068-01 (AUX 1
  left, AUX 2 centre and AUX 3 right up/down posts) reaches no public address: the ROM's Single Coil Test steps through
  AUX 1-3 and PinMAME publishes nothing. 33-44 are compatibility holes, 49 PinMAME's simulated shooter and 50 the last
  address below the custom-solenoid boundary.
- The CPU DIP switch SW300 sets the country with positions 1-5; no chart turns 6-8 on.

## Switch polarity and names

Every matrix switch rests open except the hound dog 64. The Dual OPTO boards (515-0173-00 transmitter, 515-0174-00
receiver, "4-Ball Trough over Up-Kicker") act as an open switch while their beam is lit and a closed switch while it is
blocked: LED1 is the lower beam the waiting ball blocks (14, "4-BALL TROUGH VUK OPTO") and LED2 the upper beam a
double-stacked ball blocks (15, "4-BALL STACKING OPTO"). In the stacking-opto run, with four balls on 11-14, raising
15 to 1 in attract mode made the ROM fire the trough up-kicker Q1 six times about 0.8 s apart and then the auto launch
Q2 once, both times; it treats a blocked upper beam as a jam to clear.

- **33, Elvis Home.** A Micro Switch (Short Actuator, Bend) 180-5189-00 on the figure's switch bracket. The ELVIS test
  page: "If the BOX is solid, Switch 33 is "Closed" (Elvis should be in the Home Position or closest to the Upper
  Playfield)". The ROM's Switch Test names it ELVIS HOME on closure, and its ELVIS test draws the box filled with 33 at
  1. It rests open and is closed while the figure is home: set it to 1 before the controller starts.
- **64, Hound Dog.** A Micro Switch (Short Flat Actuator) 180-5190-28 on the Hound Dog Pop-Up Target. The ROM's Switch
  Test reports HOUND DOG 0.5 s after 64 falls from 1 to 0, and never while it is held at 1 (pinned frames after 1, 3
  and 0.5 s); the hotel door 63 is reported 0.5 s after it rises. The ROM therefore treats 64 as actuated at 0: the
  contact rests closed and a hit opens it. Start it at 1 and pulse it to 0 on a hit. In the hound-dog probe, during a
  game, with 64 held at 1 the ROM switched the hotel door coil Q19 off 2.0-2.5 s later, and each return of 64 to 0
  switched Q19 on again about 65 ms later.
- **81 and 83, end-of-stroke.** The 4-Flipper Circuit Wiring Diagram draws both lower-flipper E.O.S. switches "ON
  ASSY." as N.C. and explains that each opens about 1/16" at full stroke, and that the CPU applies another 40 ms pulse
  when it sees one close during a hold; the record keeps that construction as `normally_closed`. PinMAME, not the host,
  writes both addresses: the driver declares `FLIP_SOL(FLIP_L)`, and `core.h` defines `FLIP_SOL(x)` to include
  `FLIP_EOS(x)`, so `core.c`'s `flipMask` holds both lower EOS bits and `core_updateSw` rewrites them on every update
  from the lower flipper solenoids (81 from 46, 83 from 48): 1 once the solenoid has been on for two VBLANKs, 0
  otherwise. A host write is overwritten, so a recreation leaves 81 and 83 alone. The dedicated-switch run watched
  both and read 0 in every snapshot, including while the host held them, as that rewrite predicts with the flipper
  solenoids off; no gameplay run timed an end-of-stroke against a flip. The upper flippers carry spacers instead of an
  E.O.S. switch.
- **88, upper right flipper button.** The right cabinet button is double-stacked: half-way operates the lower right
  flipper (DS-3, 82), full down both right flippers (DS-5, 88). The switch grid, the flipper diagram and the cabinet
  wiring diagram all name DS-5 the upper right flipper button. The ROM's Dedicated Switch Test prints its generic label
  "#5 NOT USED / CN6-7 GRY-GRN CN6-1 BLK" while 88 is held, but in a game holding 88 made the ROM drive the upper
  right flipper Q14. The left button (84) drives both left flippers: holding it drove Q15 (47/48) and Q13.
- **10, Shooter Lane Exit.** A micro switch above the playfield past the shooter lane; the ROM names it and the
  retained script has handlers for it but no object, so the table never writes it.
- **29, 35 and 44.** Printed NOT USED on the grid and named NOT USED by the ROM's Switch Test.
- **3, 6th coin slot.** The grid prints "Future Use" and the cabinet diagram draws its wire to the coin door; the 5.00
  ROM's Switch Test reports nothing for it, whether held, released or pulsed. It is recorded optional.
- **1 and 8.** The UK-only Post Save cabinet buttons (below the flipper buttons): the left one asks for the left outlane
  deflector, the right one the right, both together the centre post. A standard machine fits neither.

## Ball handling

- **Trough.** Four balls (the manual's front page: four pinballs must be installed) rest on micro switches 11-13
  (180-5119-02) and the up-kicker opto 14. Q1 (26-1200) kicks the ball on 14 up past the stacking opto 15 into the
  shooter lane, and the rest roll one place toward the up-kicker. Hold each occupied position at 1 and pass the kicked
  ball through 15 as a short 1 pulse. At Start the ROM fired Q1 about 1.1 s after the press and every 1.25 s after
  that until the served ball reached 16.
- **Shooter lane.** The served ball rests on 16 (180-5157-00) and leaves past the exit switch 10. The Ball Shooter
  (Plunger) Autoplunger Arm assembly carries the auto-launch coil Q2 (23-800). The retained table has both a manual
  Plunger and an impulse plunger that Q2 fires. In the gameplay run the ROM did not fire Q2 while the served ball rested
  on 16 for 6 s; it fired Q2 only in ball search, once while it was still trying to serve a ball that never reached 16,
  and in the stacking-opto run after its Q1 retries. The Diagnostic Aids page names "#16 Shooter Lane & #2 Auto Launch"
  as a pair the CPU retries about ten times before reporting the switch.
- **Center saucer (Ball Eject (Left), SW. 34).** A ball resting on micro switch 34 (180-5186-00) is kicked by Q6
  (24-940). In the gameplay run the ROM kicked about 4.3 s after the ball arrived and twice more about 0.7 s apart
  while it stayed.
- **Top saucer (Ball Eject (Right), SW. 32).** Micro switch 32 (180-5186-00) and Q12 (24-940, "TOP EJECT"); the ROM
  kicked once about 5.7 s after the ball arrived.
- **Hotel lock.** The hotel post switch 48 (180-5189-00) sees a ball held at the hotel; Q7 (23-800, HOTEL LOCK
  RELEASE, on the Magnet Coil, Bracket and Ball Lock page) releases it. A ball held on 48 for 6 s drew no Q7; Q7 fired
  only in the ball-search pass. The retained table holds the ball in the kicker HLock and kicks it on Q7.
- **Ball search.** A pass fired 3 and 12, then 6, 7, 3, 2, 19, the bumpers 9, 11 and 10, the magnet 5 and the
  slingshots 17 and 18, one after another.

## The Elvis figure

The Elvis assembly (500-6796-00, PDF pages 109-110) puts the molded figure on a platform over a welded carrier frame,
moved by a Haydon 12 V DC stepper motor (46868-12-002) turning a 7.25" threaded shaft. The ELVIS test page calls one
full cycle back-to-front or front-to-back. Two 29-1400 coil assemblies (500-6818-00 and -01) pull the actuator wires
for the legs (Q29) and the arms (Q30); IPDB describes shaking hips and gesturing hands that bring the microphone to his
lips. The four KING stand-up targets 36-39 (515-7381-00, side lugs) sit on the figure's base and travel with it. The
home switch 33 is closed with Elvis home, "closest to the Upper Playfield".

- The stepper's four phases are Q25-Q28 (TIP122 drivers, RED, GRN, BLK and BLU leads, both centre taps on +12 V DC from
  J16-P3). The coil chart and driver-board diagram print the motor as 041-5069-00 and the parts page as 041-5089-00;
  both readings are kept in the device notes.
- The ELVIS test (Section 3, page 27): RUN runs the stepper one full cycle, back-to-front or front-to-back; PULSE steps
  it; LEGS and ARMS energize Q29 and Q30. "Upon Power-Up ... the mechanism will return to it's HOME Position." In the
  ELVIS-test run, RUN drove 25-28 and left 33 at 0, a second RUN drove them and returned 33 to 1, PULSE moved it off
  home, and LEGS and ARMS drove 29 and 30. At boot every run drove the drop-target reset Q3 and the stepper phases and
  left 33 at 1.
- In a game the ROM ran the stepper with the legs and arms from many scoring switches (the bumpers, the shooter-lane
  exit, the right ramp exit, the right orbit low, the KING targets): the figure dances while songs play.
- Recreate the figure as a carriage on a linear track: step its position by the phase sequence, close 33 at the home
  end, move the KING targets with it, and pose the legs and arms while Q29 and Q30 are on. The retained table moves the
  stand primitive with a one-solenoid cvpmMech on Q25 alone (150 steps, 33 at step 0); that ignores the phase order
  and the direction, so it is a stand-in, not the machine's behaviour.

## Heartbreak Hotel and the hound dog

- The Hotel Door assembly (PDF pages 111-112) holds a 27-1500 coil (Q19, HOTEL DOOR) and an actuator arm that moves
  the metal hotel door; the door's micro switch 63 (180-5119-02) and the two 1" stand-up targets 52 (top) and 53
  (bottom) on the mini-playfield behind it complete it. The ROM holds Q19 on for long stretches; in the gameplay run it
  switched Q19 on when 52 closed and when balls rested in either saucer or on the hotel post, and in the hound-dog probe
  when 63 rose. The retained table drops `doorwall` and swings the flipper-shaped door `fDoor` open while Q19 is on.
- The hound dog (Hound Dog Pop-Up Target, assembly reference 500-6781-00) is a dog figure (500-6820-00) on a base
  bracket with an actuator bracket, a deflector pad and the micro switch 64; its parts list carries no coil. A hit
  opens the switch (see 64 above).

## Drop targets, flippers and scoring parts

- **ELVIS 5-bank.** Five white drop targets (545-6102-01) on leaf switches 17-21 (180-5158-00, diodes on the terminal
  strip) and the 24-940 reset coil Q3. A down target holds its switch closed. In the gameplay run the ROM reset the
  bank 0.33 s after the fifth target went down and pulsed Q3 twice more 0.41 s apart; it also resets the bank at boot
  and at Start.
- **Flippers.** The lower flippers have 22-900 coils (yellow wrap) and E.O.S. switches; the upper flippers have 23-900
  coils (green wrap), red bat bushings and no E.O.S. switch. One 50 V supply serves kick and hold: a 40 ms pulse on a
  button closure, then 1 ms every 12 ms while held, each coil through its own 3 A slow-blow fuse under the playfield.
- **Pop bumpers.** Left (Q9/49), right (Q10/50) and bottom (Q11/51), 26-1200 coils, stack switches 180-5015-05 ("-05
  because it is mounted in reverse"), #555 bulbs under the caps; each switch fired its own coil.
- **Slingshots.** Left (Q17/59) and right (Q18/62), 23-800 coils, two blade contacts per side, only one with a diode.
- **Magnet.** A 22-650 magnet coil (500-6808-00, diode in its connector) on Q5 under the playfield; it has no switch.
  It fired only in ball search. The retained table grabs balls with a cvpmMagnet around the trigger `Magnet`.
- **Control gate.** A mini-coil (32-1800, assembly 515-6543-00) on Q8; only the ROM's coil test fired it.

## UK and optional equipment

- **UK Post Save.** The coil chart's auxiliary group, printed for UK machines only: AUX 1 left up/down post (26-1200),
  AUX 2 centre up/down post (23-1100) and AUX 3 right up/down post (26-1200) on the UK 3X Transistor Driver Board; the
  cabinet diagram calls the outer two outlane ball deflectors. Standard adjustment 39 enables the feature (default NO,
  UK default YES). PinMAME publishes none of them, so a recreation of a UK machine has no address to drive them from.
- **Shaker motor (Q4).** Optional kit 502-5027-00-84 with the Shaker Motor Board 520-5065-00 in the cabinet. The ROM
  drives Q4 constantly in play whether or not the kit is fitted.
- **Q24.** "OPTIONAL COIL", left open at the factory: adjustment 46 chooses COIN METER (default), TOKEN DISPENSER or
  KNOCKER. Each coin pulsed Q24 four times in the harness runs. The coil chart and cabinet diagram feed it from J16-P7
  (+5 V DC); the driver-board diagram prints J16-P8.
- **Tournament kit.** Switch 55 (TOURNAMENT START) and lamp 79 (TOURNAMENT BUTTON) need the optional tournament kit.

## Lamps, flashers and general illumination

- Lamps 1-59, 63 and 64 are playfield inserts on #555 bulbs, except the ELVIS letters 33-37, the right orbit arrow 38
  and the KING letters 45-48, which are #44.
  65-72 are above the playfield (coloured #44 bulbs: yellow 65-69, blue 70, red 71, orange 72). 60-62 (HEART, BREAK,
  HOTEL) and 73-78 (ENCORE) are on the rear of the back panel. 79 and 80 are the tournament and start button lamps. The
  ROM's Single Lamp Test names all eighty; it prints 15 as ELVIS COMPLETED where the grid prints ELVIS COLLECTED.
- Flashers: Q20 two #89 bulbs (yellow mini-mars) on the back panel's lower left and upper right corners; Q21 one #89
  (clear) on the back panel left of the HEART BREAK HOTEL strip; Q22 the spinner flasher (#906, red) at the left edge;
  Q23 two #906 along the right edge by the upper right flipper; Q31 the Elvis spot light (#906; the driver board's load
  name says two, its bulb glyph one); Q32 one #906 (red) above each slingshot. The back panel's parts list carries three #89 sockets,
  Q20's two and Q21's one.
- G.I.: one relay on the I/O Power Driver Board switches the 5.7 V AC supply from J14 to four fused circuits on J15: B
  (F24, back panel 10, pop bumpers 3 and the upper right corner 1, 14 bulbs), Y (F25, mid left and lower playfield, 16),
  G (F26, upper playfield 10 and the coin door 2) and V (F27, mid right playfield, 6): 48 bulbs, #44 with a few #555.
  The ROM switched G.I. off at Start and back on when the served ball reached 16, and blinked it with several scoring
  switches.

## Retained-table defects

- 64 is pulsed to 1 on a hit (`vpmTimer.PulseSw 64`) and rests at 0, the ROM's actuated level.
- 55 is written from `If keyUpperLeft Then Controller.Switch(55) = 1` (lines 176 and 183), which tests a variable
  neither the script nor the retained core.vbs and sega.vbs define, not the keycode.
- Switch 10 has handlers but no object, so it is never written.
- The upper flippers are rotated by the lower-flipper callbacks (`SolLFlipper`, `SolRFlipper`); no callback reads 13
  or 14 and no key writes 88, so the upper right flipper follows the half-press instead of the full press.
- The script never writes the EOS inputs 81 and 83, which is right: PinMAME writes them itself.
- The Elvis mech moves on Q25 alone and ignores Q26-Q28 and the phase order (see the figure above).
- Q24 is bound to a knocker sound; the factory default for Q24 is a coin meter.
- The table declares `UseGI = 0` (line 40) and sets `GICallback = GetRef("GIUpdate")` (line 1038).

## Spatial status and why the record stays partial

Placements come from the retained table's object centres, normalized over its exact bounds 952 x 2115, and stay
`observed`. Projections: the trough switches 11-15 onto the release kicker `BallRelease`; the home switch 33, the
stepper phases 25-28 and the legs and arms coils 29 and 30 onto the figure's stand primitive `pStand`; the 5-bank
reset Q3 onto the mean of its five targets; each E.O.S. switch onto its flipper. Flashers 22 and 32 sit on the glow
Lights centred on their modelled Flupper domes. The G.I. relay carries the six members of the table's G.I. collection
that draw their bulb mesh (`gi9`, `gi10`, `gi11`, `gi13`, `gi14`, `gi27`), with no circuit assignment.

Not placed: every lamp (the table fades insert Lights without a bulb, or draws 57-78 with Flasher overlays), the back
panel flashers 20 and 21 (the table's Flupper domes `Flasherbase4`, `Flasherbase5` and `Flasherbase6` stand on the
back panel's plane behind the playfield's rear edge), the upper right flipper flasher 23 and the other 26 G.I.
collection members (bulb-mode Lights that show no bulb mesh and sit on no modelled socket), the Elvis spot light 31 (two
Flasher overlays) and the shooter-lane exit switch 10 (no object). Completing the record needs the factory lamp, switch and coil location drawings (DR. 5,
DR. 4 and DR. 7) fitted to the table by a callout check, the back panel placed by the elevation rule, and the G.I.
sockets matched to the drawing's circuit discs.

## Author construction checklist

1. Start with four balls on 11-14, 15 at 0, 33 at 1 (Elvis home), 64 at 1 (hound dog at rest, kept at 1 except for
   the length of a hit) and -3 at 1 (coin door closed).
2. Bind the lower flipper coils at 48 and 46, the upper flipper coils at 13 and 14; drive 84 from the left button,
   82 from a half press of the right button and 82 with 88 from a full press; leave 81 and 83 to PinMAME.
3. Model the trough, the up-kicker opto 14 and the stacking opto 15 as a short pulse when Q1 kicks a ball past it.
4. Model the figure as a stepper-driven carriage: count the Q25-Q28 phase sequence, close 33 at the home end, carry
   the KING targets 36-39, and pose the legs and arms from Q29 and Q30. LibPinMAME already writes 33 from its own
   phase count; VPinMAME needs the table to write it.
5. Hold Q19 as the hotel door's open state; open 64 on a hound-dog hit.
6. Treat Q4, Q24, 1, 2, 3, 7, 8, 55 and 79 as optional equipment, and AUX 1-3 as unreachable through PinMAME.
7. Drive the G.I. relay 0 for all 48 G.I. bulbs, including the ten on the back panel and the two on the coin door.

## Sources

- Stern, Elvis service manual (`Elvis_Manual.pdf`, 185 pages, manual part number 780-5084-00), from Stern's own manuals
  page; excerpts under `evidence/excerpts/stern.elvis.2004/`.
- IPDB machine 4983, from an Internet Archive capture.
- Retained table: jpsalas, Elvis VPX 1.0.2 (`elvis_mod_1.0.vpx`), its embedded script and a full-file extraction
  manifest; the pinned corpus script `Elvis (Stern 2004) WED SSF Mod.vbs`; VPinMAME's `sega.vbs` and `core.vbs`.
- Pinned PinMAME `46e1a01a`: `src/wpc/sims/se/prelim/elvis.c`, `src/wpc/se.c`, `src/wpc/core.c`.
- Nine LibPinMAME harness runs of `elvis` 5.00 from empty NVRAM, compacted in
  `evidence/runtime/whitestar/elvis-service-tests-and-gameplay.json`.
