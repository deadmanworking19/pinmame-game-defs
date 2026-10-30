# South Park (Sega, 1999)

Coverage: **partial - every I/O address, controller binding, polarity, wiring detail, mechanism, variant and
recreation note is source-reconciled; only `spatial_placement` is missing, because the retained table does not model
the trough, the under-trough or the UK equipment, the toy coils are placed on the figures they move, and no placement
has yet been checked against the factory location drawings**

## Identity and evidence precedence

This is Sega Pinball's Whitestar machine of February 1999, model 71, IPDB 4444, with about 2,200 built. It covers the
three `sprk_*` drivers of pinned PinMAME: `sprk_103` (CPU 1.03, the production code) and the two prototype sets
`sprk_096` and `sprk_090`, which IPDB lists as the "Swearing" prototype ROMs. `segames.c` builds all three from one
`init_sprk`, `INITGAME(sprk, GEN_WS, se_dmd128x32, 0)`: lower flippers only (`FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L)`), two
extra lamp columns (lamps 1-80), no custom solenoids, a 128x32 DMD and no auxiliary driver board. The ROMs differ in
rules, language, sound and in one emulator detail (below), not hardware, so all three are `identical`. A harness run
exercised `sprk_103` and `sprk_096`; `sprk_090` was never run, because the authorized ROM archive's `sprk_090` set
carries the 1.01 display ROM instead of `spdspa.090`.

The machine's adult-language setting (G, TV-14 and TV-MA, per IPDB) is an operator adjustment, not hardware.

Authority follows the runbook. The known-working table's embedded script decides controller callbacks and mechanism
causality; the official manual (a 72-spread scan without a text layer, the copy IPDB hosts) decides construction, wiring,
parts and placement on the drawings; pinned PinMAME decides routing. Three harness runs, two of `sprk_103` and one of
`sprk_096`, confirm the routing and the switch-to-coil responses. The retained table is Knorr's 1.3 recreation; the
pinned corpus script is the same 1.3 script with a flipper tweak, so it corroborates the bindings but is not
independent.

## Controller platform and address topology

- **Switches.** Matrix 1-64 is sequential (column = (n - 1) / 8 + 1). 9, 27-33, 39-41, 52, 53, 63 and 64 are NOT USED.
  1 and 8 are the UK-only Sav-A-Ball cabinet buttons, 3 and 7 coin-door positions marked Future Use. The dedicated
  inputs are -3 memory protect, -2/-1/0 the red/green/black service buttons (DS-6/7/8), 84 left button (DS-1), 83 left
  EOS (DS-2), 82 right button (DS-3), 81 right EOS (DS-4) and 88, the NOT USED DS-5. 85-87 reach no input. The country
  selector is DIP bits 1-5.
- **Solenoids.** Public 1-32 are Q1-Q32 except the flippers: `se_solenoid_w` masks Q15 (left) and Q16 (right) off public
  15/16 and publishes them at 47 and 45, and `core.c` synthesizes 48 and 46 from those. Bind the left flipper coil at 48
  and the right at 46; 45 and 47 are their power-phase states. Public 15 is PinMAME's fast-flip / game-on state
  (sega.vbs's `GameOnSolenoid = 15`), but `MACHINE_INIT(se)` gives only `sprk_103` the fast-flip byte (CPU RAM 0x00):
  in the `sprk_103` run 15 rose when the served ball reached the shooter lane and fell at the drain, and in the
  `sprk_096` run it never rose. A recreation that needs a game-on signal on the prototypes must derive it elsewhere.
  16, 33-44 (no auxiliary board), 49 and 50 are unused. Q8 (European token dispenser), Q21-Q23 (UK) and Q24 (coin
  meter) are optional equipment.
- **Lamps** 1-80 run across each row (lamp = (row - 1) x 8 + column). 31, 32, 47, 49 and all of 65-80 are NOT USED. The
  ROM's attract sweep strobes the whole 64-lamp matrix, so the NOT USED cells inside it toggle in a trace with their
  neighbours; that proves the sweep, not a socket. There is no Start-button lamp. **G.I.** is one relay at public 0.

## Switch polarity and names

Whitestar's `switch_r` hands the CPU `~core_getSwCol` with no per-game inversion, so public 1 is the closed-contact
reading for every matrix switch, and `dedswitch_r` does the same for the dedicated inputs.

- **Optos.** The trough's two dual opto boards (VUK opto 14 and stacking opto 15) and the Kenny opto 42 read 1 while the
  beam is blocked. The trough opto theory (printed page 89) states the construction: with light on the receiver the output
  transistor is off and acts as an open switch, so `normally_closed` is false.
- **End-of-stroke.** 81 and 83 are N.C. E.O.S. switches on the flipper assemblies: at rest public 1, open (0) at the end
  of the stroke. The driver declares no `FLIP_EOS`, so PinMAME never writes them; the CPU re-pulses a held flipper when
  the switch closes again. A recreation that never writes them loses only that re-pulse.
- **Names.** The labels follow the Switch Matrix Grid (DR. 4), with the page-15 table's longer names in each note. The
  page-15 table prints "7 4" in the left-turbo-bumper row's number cell; the grid and the location drawing put the left
  turbo bumper at 49.
- **Initial state.** Five balls rest on 10-14, and -3 is 1 with the coin door shut.

## Ball handling

- **Trough.** Five balls rest on micro switches 10 (left), 11, 12, 13 and the VUK opto 14 at the trough up-kicker. Q1
  (26-1200) kicks the ball on 14 up past the stacking opto 15 into the shooter lane. The ROM fired Q1 repeatedly on Start
  until the served ball left the trough. The retained table's `bsTrough` omits 15 (its `PulseSw 15` is commented out);
  pulse 15 once per kicked ball.
- **Shooter.** The ball rests on 16. A manual ball shooter launches it, or Q2 fires the autoplunger arm.
- **Top VUK.** A ball up the left orbit (47) settles on 46 at the top of the playfield. `sprk_103` fired Q4 (26-1200) once,
  a few seconds later (`sprk_096` only during a later step), and the VUK lifts the ball onto the top wire ramp, which
  feeds the left ramp.
- **Under-trough and super VUK.** The Under-Trough Assembly collects balls from under the toilet (43), from under Kenny
  (44) and from the playfield hole above the super VUK (48), one micro switch each, and leads them to the super VUK,
  where the ball rests on 45 until Q3 (24-940) kicks it back to the playfield. In the runs, a ball held on 45 drew repeated
  Q3 kicks, and one closure of 44 or 48 with the super VUK empty drew one Q3 kick without waiting for 45; a closure of 43 alone
  drew none. The
  retained table moves the ball from a kicker to its super-VUK ball stack after 1.2-2.4 s, which is a fair stand-in for
  the travel time.
- **Ramps.** The right ramp has an entry (25) and an exit (26) switch. With the toilet seat down, a ball from the right
  ramp passes over the toilet into the left ramp (Left Ramp Assembly page).

## Toys

- **Toilet and Mr. Hankey.** Q5 (23-1100) lifts the toilet seat lid while energized; with it up, the ball can enter the
  toilet and drop to 43. Mr. Hankey and the tank lid ride a spring-loaded lift: Q13 (23-1100, "MR. HANKEY (DOWN)") pulls
  them down onto a latch and Q6 (29-1000, "MR. HANKEY LATCH") trips it so the spring throws Mr. Hankey up. There is no
  position switch, so the ROM drives the figure open-loop: Q13 pulsed twice at power-up and once at the drain. No run
  fired Q5 or Q6. The retained table models the seat, Mr. Hankey and the tank lid with helper flippers.
- **Kenny.** Kenny stands on a carriage that two 24-940 coils swing left (Q19) and right (Q20); the centre 22-1080
  coil (Q14) pivots him over ("dead"). Lamp 30 (#555) and flasher Q30's #906 bulb are inside the figure. The Kenny opto 42
  sees the ball arrive; one closure made the ROM fire Q14 once, alternate Q19 and Q20 (nine or ten pulses each) and flash Q30. A
  ball that reaches Kenny drops to 44.
- **Scoring parts.** Three turbo bumpers (Q9-Q11 / 49-51), two slingshots with two contacts each (Q12/59, Q17/62), the
  left 5-bank (17-21), the centre 3-bank (22-24), the right 3-bank (34-36), the two pop-bumper targets (37, 38), the
  left orbit (47) and the four lanes (57, 58, 60, 61). Every target and lane closed in a run drew either its flashers or
  nothing: these are scoring switches, not mechanism sensors.

## UK equipment

A UK machine adds two outlane ball deflectors (Q21 left, Q22 right, coil 28-1050) and an up/down post between the
flippers (Q23, coil 23-1100), all on the main I/O board, and two Sav-A-Ball cabinet buttons on 1 (left) and 8 (right).
The UK-only box of the cabinet wiring diagram prints the two buttons' CN7 pins crossed against the Switch Matrix Grid;
the wire colours agree with the grid, and the record follows it. The coil location drawing draws the three coils in grey
boxes at the two outlanes and between the flippers; the placements are projections from it onto the US table's objects.

## Lamps, flashers and general illumination

- **Lamps.** 60 #555 inserts, every one bound by the retained table's `InitLamps` and every one driven by the ROM.
- **Flashers.** Q7 (four #89 around the turbo bumpers), Q18 (top VUK dome), Q25-Q29 (two #89 each, under each character's
  face and arrow inserts: Stan, Chef, Kenny, Kyle, Cartman), Q30 (one #906 inside Kenny and two #89 on the back panel), Q31
  (two at the toilet) and Q32 (super VUK dome). The flash lamp location drawing draws the two back-panel Q30 bulbs; only
  the Kenny bulb is placed.
- **G.I.** One relay switches four fused 6.3v AC strings: 31 #44 playfield bulbs and two #555 coin-door bulbs. The G.I.
  page warns that bulb quantities may change during production. The ROM blinks the G.I. on some events (the outlanes,
  the right ramp exit). The retained table does not bind G.I. 0; its own subs switch the G.I. on table events.

## Spatial status and why the record stays partial

Placements come from the retained table's script-bound objects, normalized against its 952 x 2162 bounds. They stay
`observed` and `spatial_placement` stays missing because:

- **Projections onto mechanism objects.** The table does not model the trough (10-15), which is projected onto the
  release kicker, or the under-trough switches 43, 44 and 48, which sit on the kickers that pulse them. The EOS contacts
  sit on the flippers.
- **Toy coils on figures.** The toilet seat, Mr. Hankey and Kenny coils and the Kenny flasher bulb are placed on the
  primitives the script animates, not on the coil bodies under the playfield.
- **UK coils.** Q21-Q23 are projections from the coil location drawing.
- **No callout check.** No placement has been fitted against the switch, lamp, coil and flash location drawings (DR. 5
  and DR. 7), whose crops are in the excerpts.
- **G.I.** The table models 29 G.I. sockets, each a bulb-drawing light with its glow double merged, against the 31
  playfield bulbs the G.I. page prints; three more GI-collection lights sit in the turbo bumper caps on matrix lamps 38-40
  and are not G.I. sockets. The page's mirrored bottom-view drawing
  labels every socket with its circuit (B, Y, G, V); matching the 29 table bulbs to it, which would also locate the two the
  table lacks, is not done.

Nothing here is a disagreement about the machine; the blockers are missing geometry, so the record carries no conflicts.

## Author construction checklist

- **Ball path.** Build the 5-ball trough with stacking opto, the manual and auto shooter, the top VUK behind the upper
  loop, the under-trough with its three entry switches, the super VUK, the two ramps and the toilet entry under the seat.
- **Toys.** Build the toilet seat lid, the spring-thrown Mr. Hankey with tank lid and latch, and Kenny with his swinging
  carriage and pivot. Neither toy reports its position.
- **Scoring parts.** Three turbo bumpers, two slingshots, two flippers with N.C. EOS, the 5-, 3- and 3-banks, the bumper
  targets, the left orbit and the four lanes.
- **Initial state.** Initialize 10-14 and -3 at 1. Pulse 15 per kicked ball.
- **Bindings.** Bind Q15 at 48 and Q16 at 46; 45/47 are power phases and 15 is game-on (on `sprk_103` only). Bind Q21-Q23
  only for a UK build, Q8 only with a token dispenser and Q24 only with a coin meter.
- **Displays and lights.** One 128x32 DMD in the cabinet. Recreate the 31 playfield G.I. bulbs and the 2 coin-door bulbs,
  all lamps and flashers, including the two back-panel Q30 bulbs.

## Sources

- `manual.sega.south-park.1999`: SHA-256 `c25723bfc9bb8726c12b1fc3f9a6d74df60ebe8ce7da1937e06a38ace1b59f0a`, IPDB 4444's
  English manual; excerpts under `evidence/excerpts/sega.south-park.1999/`.
- `vpx-table.south-park-knorr-1-3` and its embedded script (`63881ced...`), with the retained extraction and its
  manifest.
- `vpx-script.51b7c24a7b284174`: the pinned corpus script (`51b7c24a...`).
- `vpm-script-library.sega-vbs`: `sega.vbs` (`d6e508aa...`).
- `runtime.south-park.sprk-103` and `runtime.south-park.sprk-096`: three LibPinMAME runs, summarized in
  `evidence/runtime/whitestar/south-park-sprk-103-stacking-opto-and-gameplay.json` and
  `evidence/runtime/whitestar/south-park-sprk-096-gameplay.json`.
