# Harley-Davidson (Stern, 1999)

Coverage: **partial - every I/O address, controller binding, polarity, wiring detail, mechanism, variant and
recreation note is source-reconciled except lamps 52-54, which the 3rd-edition manual prints NOT USED but both
exercised ROMs drive during play, so `output_semantics` is missing; `spatial_placement` is missing because the retained
table does not model the trough, the motorcycle trough, the lift or the stop light, several flashers are drawn only with
overlay objects, and no placement has been checked against the factory location drawings**

## Identity and evidence precedence

This is Stern Pinball's Harley-Davidson of 1999 (IPDB 4455, model PINBALL-HD), which IPDB calls the first game by
Stern Pinball and the continuation of the production run of Sega's 1999 Harley-Davidson (IPDB 4453, model 67). Stern
followed it with a 2nd edition in November 2002 (IPDB 4664, PINBALL-HD2, about 600 units) and a 3rd edition (IPDB 5277,
PINBALL I-0087). Sega's machine keeps its own record for its own 1.03 and 1.00 drivers (`harl_a13`, `harl_a10` and
their language sets). The Stern editions differ in art, trim and the motorcycle models, not in wiring: the 3rd-edition
manual's board table lists one row for the "1st-3rd Editions".

The record holds all fifteen `harl_*` drivers of pinned PinMAME: CPU 4.00 (`harl_a40`, the catalog root, with French,
German, Italian and Spanish display sets), CPU 3.00 (the 3rd-edition A3.00 of the firmware appendix) and CPU 1.08 (the
2nd-edition A1.08). `src/wpc/sims/se/prelim/harley.c` builds every one on `de_mSES1` with the same sound set and one
`init_harl`, which installs `harlGameData`: GEN_WS, a 128x32 DMD, lower flippers only (`FLIP_SW(FLIP_L) |
FLIP_SOL(FLIP_L)`), two extra lamp columns (lamps 1-80), no custom solenoids and no auxiliary board. All fifteen are
`identical`. No factory document held here names a 4.00 release; the firmware appendix ends at A3.00.

Authority follows the runbook. The known-working table's embedded script decides controller callbacks; the official
3rd-edition manual (160 pages, the copy IPDB hosts) decides construction, wiring, parts and placement on the drawings;
pinned PinMAME decides routing. Nine LibPinMAME harness runs of `harl_a40` and one of `harl_a30` confirm the routing and
the switch-to-coil responses. The retained table is the Goldchicco and 32assassin 1.2 conversion; the two pinned corpus
scripts are releases of a later table of the same machine, so they corroborate bindings without being independent.

## Controller platform and address topology

- **Switches.** Matrix 1-64 is sequential (column = (n - 1) / 8 + 1). 9, 10, 38-40, 47, 63 and 64 are NOT USED. 1 and 8
  are cabinet buttons: on a USA machine the extra right button (8) asks for the up/down post; on a UK machine the left
  (1) and right (8) Post Save buttons ask for the outlane deflectors, and both together for the post. 2, 3 and 7 are
  optional coin positions (3 and 7 Future Use). The dedicated inputs are -3 memory protect, -2/-1/0 the red/green/black
  service buttons (DS-6/7/8), 84 left button (DS-1), 83 left EOS (DS-2), 82 right button (DS-3), 81 right EOS (DS-4) and
  88, the NOT USED DS-5. The cabinet wiring diagram draws an upper right flipper button on DS-5 (CN6-7), but the switch
  table, the flipper circuit diagram and the ROM's Dedicated Switch Test ('#5 NOT USED / CN6-7 GRY-GRN CN6-1 BLK') all
  name it NOT USED, and holding 88 switched no coil on in attract mode or play while holding 8 raised the post; 85-87
  reach no input.
- **DIP switches.** SW300 positions 1-5 select the country; the manual's nineteen charts never turn 6-8 on. Three of
  `sega.vbs`'s country labels (0x05 UK, 0x09 Japan, 0x0d Brazil) name other countries than this game's chart (Finland,
  Denmark, Australia; the UK is 2, 3 and 4 on); follow the chart.
- **Solenoids.** Public 1-32 are Q1-Q32 except the flippers: `se_solenoid_w` masks Q15 (left) and Q16 (right) off public
  15/16 and publishes them at 47 and 45, and `core.c` synthesizes 48 and 46 from those. Bind the left flipper coil at 48
  and the right at 46; 45 and 47 are their power-phase states. Public 15 is PinMAME's fast-flip / game-on state
  (`sega.vbs`'s `GameOnSolenoid = 15`), but `MACHINE_INIT(se)` gives only `harl_a30` the fast-flip byte: in the
  `harl_a30` run 15 rose when the served ball reached the shooter lane, fell during the video mode and at the drain; the
  `harl_a40` runs never raised it. 16, 33-44, 49 and 50 are unused. Q8 (European token dispenser), Q21-Q22 (UK outlane
  deflectors) and Q24 (coin meter) are optional equipment; the up/down post Q23 is standard.
- **Lamps** 1-80 run across each row (lamp = (row - 1) x 8 + column). 55, 56, 60-64 and 73-80 are NOT USED and no run saw
  them lit. 47 is the Launch button's lamp in the cabinet. **G.I.** is one relay at public 0.

## Lamps 52-54

The Lamp Matrix Grid prints 52, 53 and 54 NOT USED, black with no bulb line, and the lamp location drawing marks none of
them, so the 3rd-edition machine fits no bulb there. Both exercised ROMs switch them during play, from about a second
after the served ball reaches the shooter lane, usually all three at once and in step with lamp effects on 36, 37, 42
and 49, and never in attract mode, while 55 and 56 stay dark. No retained script binds them. What that state reaches is
unknown; they carry `availability = unknown`. The 1st- or 2nd-edition manual (780-5067-01 or 780-5067-10, neither
retained) or the ROM's Single Lamp test on a harness run would settle whether an earlier edition fitted bulbs there.

## Switch polarity and names

Whitestar's `switch_r` hands the CPU `~core_getSwCol` with no per-game inversion, so public 1 is the closed-contact
reading for every matrix switch, and `dedswitch_r` does the same for the dedicated inputs.

- **Optos.** The trough's two Dual OPTO board pairs (VUK opto 14 and stacking opto 15) read 1 while the beam is blocked;
  the trough opto theory states the construction: with light on the receiver the output transistor is off and acts as an
  open switch. The motorcycle-enter opto 37 is one Long-Hop combo board on the stop light's bracket. Its theory text says
  a lit receiver makes the switch, but the drawn circuit and the retained script both make 37 a blocked-beam 1; the
  record follows the read path, so every opto has `normally_closed = false`.
- **End-of-stroke.** 81 and 83 are N.C. E.O.S. switches on the flipper assemblies: at rest public 1, open (0) at the end
  of the stroke. The driver declares no `FLIP_EOS`, so PinMAME never writes them; the CPU re-pulses a held flipper when
  the switch closes again. A recreation that never writes them loses only that re-pulse.
- **Names.** The labels follow the Switch Matrix Grid (DR. 4), with the page-15 table's longer names in each note. The
  page-15 table prints "7 4" in the left-turbo-bumper row; the grid and the matrix arithmetic give 49. Its opto 37 board
  numbers carry a 180- prefix where every other page gives 520-5082-00 and 520-5083-01.
- **Initial state.** Four balls rest on 11-14 ("FOUR (4) PINBALLS MUST BE INSTALLED!"), the motorcycle is down (36 at 1),
  and -3 is 1 with the coin door shut.

## Ball handling

- **Trough.** Four balls rest on micro switches 11 (left), 12, 13 and the VUK opto 14 at the trough up-kicker. Q1
  (26-1200) kicks the ball on 14 up past the stacking opto 15 into the shooter lane. Pulse 15 once per kicked ball; the
  retained table never writes it.
- **Shooter.** The ball rests on 16 and the auto launch Q2 (24-940) fires it, 40 ms after the ball arrives in the harness
  runs. While the ball stays, the ROM fires Q2 again 2.3 s later and then eight more times about 0.5 s apart, and then
  reports the switch, the Operator Alert behaviour the manual's Diagnostic Aids page describes for every
  switch-activated coil that can trap a ball. The cabinet's LAUNCH (FIRE) button (53) made no difference in the runs:
  the ROM launched without it, and a press during or after the retries drew no coil of its own.
- **Motorcycle lift and kick-out trough.** The H-D motorcycle model sits on the Lift Plate & Cycle Assembly, which a
  cam-driven 24 V AC motor raises into a "wheelie". Q19 drives a relay board that runs the motor; micro switches 35 (UP)
  and 36 (DOWN) on the cam report the end positions, and the ROM stops the motor when the wanted one closes, so the
  direction comes from the cam. At power-up the ROM runs the motor until 36 closes (and never runs it with 36 closed at
  boot); when a served ball reaches the shooter lane it runs the motor until 35 closes; the ball search runs it through
  any position. The motorcycle returns down on a game reset. The kick-out trough under the motorcycle takes up to four
  balls on one 4-position membrane switch, 44 (bottom, first in) to 41 (top), and Q5 (24-940) at its low end ejects
  them. The opto 37 at the stop light sees a ball entering. PinMAME's simulator lets a ball in only when the lift is at
  least half up. No harness run had the ROM fire Q5; the Motorcycle Test ejects the trough with Q5 from the Launch button.
  Technical Brief 49 adds a 68 Ω adapter harness for motors that stutter on 50 Hz mains.
- **Super VUK.** The Ball Under-Trough Assembly carries the Behind Top VUK switch 48 and leads the ball to the super VUK,
  where it rests on 45 until Q3 (23-800) kicks it up. A ball held on 45 drew repeated Q3 kicks. One closure of 48 fired no
  coil and started the ROM's video mode with the G.I. off. PinMAME's simulator routes a ball the top-orbit magnet catches
  behind the traffic light to 48 and on to 45.
- **Scoop.** The Kick-Big (Power Scoop) Assembly below the bumpers: with no other switch closed, a ball on 46 drew three
  scoop-flasher (Q20) flashes, then a Q4 (23-800) kick about 1.1 s after arriving and one every 0.75 s, ten in all, while
  it stayed. Later in a game a 6 s hold drew no kick, so the ROM can keep the ball there; a recreation must not assume a
  fixed eject delay.
- **Magnet.** Q14 (22-650) under the top centre of the playfield, the fuse table's "Magnet (Top Orbit)". No switch of its
  own; no run held a ball where it acts.
- **Ramps and orbits.** The right ramp carries entry (25), mid (27) and exit (26) wire-gate switches; the orbits have 33
  (left) and 34 (right).

## Scoring parts

Two 4-bank drop targets, left L-I-V-E (17-20, reset Q6) and right R-I-D-E (21-24, reset Q7), each reset the moment its
fourth target went down; four turbo bumpers (Q9-Q12 / 49-52, red caps over lamps 28-31); two slingshots with two contacts
each (Q17/59, Q18/62); four stand-up targets, two at the motorcycle (29, 30) and two at the right ramp (31, 32); the
spinner (28); and the four lanes (57, 58, 60, 61). The up/down post Q23 (23-1100) stands between the flippers; holding
8 for 1.5 s raised it. Every other target and lane closed in a run drew flashers, the shaker or nothing.

## Stop light

The Stop Light Assembly is a traffic-light housing with three #44 bulbs (59 red at the top, 58 yellow, 57 green at the
bottom) and the bracket that carries opto 37, so it stands at the motorcycle entrance. It has no moving part.

## UK equipment

A UK machine adds two outlane ball deflectors (Q21 left, Q22 right) on the main I/O board. The chart prints a 28-1050
coil and the UK Ball Deflector Assembly page a 26-1200; the record keeps the chart's number. The US table models
neither; their placements are projections onto the outlane rollovers.

## Lamps, flashers and general illumination

- **Lamps.** 62 matrix lamps are fitted: 1-51 and 65-72 on the playfield, the stop light 57-59 and the Launch button lamp
  47 in the cabinet. 7, 8, 9, 16, 57-59, 71 and 72 are #44 bulbs, the rest #555. 32 and 70 each light two sockets.
- **Flashers.** Q20 (one #89 at the scoop), Q25 (two at the left drop targets), Q26 (two on the left), Q27 (four at the
  turbo bumpers), Q28 (two on the rear discs), Q29 (four around the motorcycle), Q30 (two at the super VUK), Q31 (two down
  the right ramp) and Q32 (two at the speedometer). se.c models every one as a #89 20v DC bulb.
- **G.I.** One relay switches four fused 6.3v AC strings: 38 #44 playfield bulbs and two #555 coin-door bulbs. The G.I.
  page warns that bulb quantities may change during production. The ROM blinks the G.I. on some events (coins, the right
  ramp exit, the outlanes) and switches it off for the video mode. The retained table does not bind G.I. 0.
- **Shaker.** Q13 runs a cabinet shaker motor on most scoring switches, when a ball is served or held in the motorcycle
  trough, and at the drain.

## Retained-table defects

The retained 1.2 table is known to work, but a recreation built from its script inherits these defects:

- `vpmNudge.TiltSwitch=14` writes the trough VUK opto on a nudge tilt instead of the plumb-bob tilt 56.
- The stacking opto 15 is never written: `SolTrough` is bound to no callback.
- `sw25` is a VPX gate, which raises Hit but no Unhit event, so 25 stays at 1 after the first pass.
- The 27 handlers name `trigger27`, which does not exist; the ramp's wire gate is `Trigger27q`, so 27 is never written.
- The scoop flasher Q20's only fader is commented out, so it draws nothing.
- G.I. 0 and the EOS inputs 81/83 are never written, the shaker callback shakes nothing, and the motorcycle trough ejects
  on Q5 whatever the lift's position.

## Spatial status and why the record stays partial

Placements come from the retained table's script-bound objects, normalized against its 1000 x 2000 bounds. They stay
`observed` and `spatial_placement` stays missing because:

- **Projections onto mechanism objects.** The table does not model the trough (11-15), projected onto the release
  kicker; the motorcycle trough (41-44) and the lift switches 35 and 36, projected onto the kicker Kicker1; or the lift
  relay 19, also on Kicker1. The drop-target resets sit on their banks' mean, the EOS contacts on the flippers.
- **Unplaced devices.** Switch 27 has no bound object. The stop light 57-59, the Next City lamp 72 and the flashers 20,
  25, 27 and 29-32 are drawn only with Flasher overlay objects or not at all.
- **UK coils.** Q21 and Q22 are projections onto US-table objects.
- **No callout check.** No placement has been fitted against the switch, lamp, coil and flash location drawings (DR. 5
  and DR. 7), whose crops are in the excerpts.
- **G.I.** The table models 20 G.I. sockets against the 38 playfield bulbs the G.I. page draws; matching them to the
  circuit-lettered sockets of its mirrored bottom-view drawing is not done.

Nothing here is a disagreement between sources about the machine, so the record carries no conflicts.

## Author construction checklist

- **Ball path.** Build the 4-ball trough with stacking opto, the auto-launch shooter lane, the motorcycle lift with its
  kick-out trough and entry opto, the under-trough and super VUK, the power scoop, the right ramp, the two orbits and the
  top-orbit magnet.
- **Motorcycle.** Make the lift a motor that runs while Q19 is on and reverses at each end, closing 36 at the bottom and
  35 at the top; start it down with 36 at 1. Admit balls to the kick-out trough only when the motorcycle is up.
- **Scoring parts.** Two 4-bank drop targets, four turbo bumpers, two slingshots, two flippers with N.C. EOS, four
  stand-up targets, the spinner, the four lanes and the up/down post.
- **Initial state.** Initialize 11-14, 36 and -3 at 1. Pulse 15 per kicked ball.
- **Bindings.** Bind Q15 at 48 and Q16 at 46; 45/47 are power phases and 15 is game-on (on `harl_a30` only). Bind Q21-Q22
  only for a UK build, Q8 only with a token dispenser and Q24 only with a coin meter. Leave 52-54 unbound until their
  load is known.
- **Displays and lights.** One 128x32 DMD in the cabinet. Recreate the 38 playfield G.I. bulbs and the two coin-door bulbs,
  all lamps, the stop light and every flasher bulb.

## Sources

- `manual.stern.harley-davidson.1999`: SHA-256 `a10e91542f9c8ab965d18908626114d1d03cba499f36fa47751045e8adae4731`, IPDB
  5277's 3rd-edition manual; excerpts under `evidence/excerpts/stern.harley-davidson.1999/`.
- `service-bulletin.stern.harley-davidson.tech-brief-49`: Technical Brief 49 (`7605f4c4...`).
- `vpx-table.harley-davidson-1-2` and its embedded script (`eb0960bc...`), with the retained extraction and its manifest.
- `vpx-script.6c9fb236b2931fc9` and `vpx-script.e101da5130f14724`: the pinned corpus scripts of the later table.
- `vpm-script-library.sega-vbs`: `sega.vbs` (`d6e508aa...`).
- `pinmame.sim.harley.46e1a01a0f73`: PinMAME's simulator for this game, a lead for the ball routes.
- `runtime.harley-davidson.harl-a40` and `runtime.harley-davidson.harl-a30`: ten LibPinMAME runs, summarized in
  `evidence/runtime/whitestar/harley-davidson-harl-a40-motorcycle-and-gameplay.json` and
  `evidence/runtime/whitestar/harley-davidson-harl-a30-gameplay.json`.
