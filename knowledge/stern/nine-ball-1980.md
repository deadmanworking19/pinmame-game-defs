# Nine Ball (Stern, 1980)

Coverage: **partial - the controller inventory, wiring, mechanisms and rules are documented and the public addresses proved by the ROM's own tests; no playfield lamp is placed, and one option switch's printed setting is contradictory**

## Identity and evidence precedence

This is the one physical Stern Nine Ball (IPDB 1678, December 1980, model 125, Stern M-200 MPU, 2,279 units; design Steve Kirk, art Robert Quinn and Jorge Obregon). PinMAME `nineball` is the production root
(ROMs U1, U2, U5 and U6, the parts list's 25A-125-E1E48 to E6E48) and `ninebafp` its free-play clone with free-play U2 and U6. `ninebala` and `ninebalc` are Idleman's ball-handling modifications (beta 18,
2020, and beta 19, 2021), `ninebald` his gameplay modification (beta 21, 2021), and `ninebalb` Oliver's modified rules revision 85 (2007) in one 32 KB image; its source comment says a two-ball multiball
flashes 2X and doubles all scores, a three-ball multiball flashes 4X and quadruples them, the self test is incomplete and it is free play only. All six share one game-data line (`GEN_STMPU200`, seven-digit
`dispst7` displays, `FLIP_SW(FLIP_L)`, no extra lamp columns, ST300 sound), so they are physically identical and only the ROM program differs. The authorized ROM library holds `nineball`, `ninebafp` and
`ninebalb`; it has no set for `ninebala`, `ninebalc` or `ninebald`, so those three were not run.

Evidence order is the runbook's. The two pinned corpus scripts give runtime bindings, this game's own manual and four-sheet schematic set give construction and wiring, pinned PinMAME gives the controller
topology, and ten retained harness runs (burn-in, solenoid test, switch test, a scripted game, game over and slam, a kick-out spot, the lock lane, an option-switch probe, and one run each of `ninebafp` and
`ninebalb`) pair the printed numbers with public addresses and show the ROM's responses. The manual is a 72 dpi scan; the schematic set is four large-format scans, three of them drawn or lettered for Nine Ball.

## Address translations

**Switches.** The matrix is five strobes by eight returns, public 1-40, and the ROM's switch test shows the closed address's own number for every one of the forty (retained run), so the Switch I.D.
numbers are the public addresses. All forty positions are fitted. The cabinet switches 1-3 (coin chutes), 6 (credit), 7 (tilt) and 8 (slam) are strobed on R-Y (J3-3) and return on MPU connector J3;
the playfield sheet draws them as unlabelled contacts. Every matrix contact is normally open; every one has a series 1N4004 diode except coin chutes 1-3, and 4, 17 and 35 also carry a .05 capacitor.
Service inputs are -7 (Self Test), -6 (CPU diagnostic NMI) and -5 (sound diagnostic); the last two are PinMAME routes with no documented button. The flipper
buttons are PinMAME's synthetic 84 (left) and 82 (right); 81 and 83 are unused. The flippers' end-of-stroke contacts and the door's remote S33 memory-clear button are hard-wired and have only profile-local
identities (physical direct inputs 1-3).

**Solenoids.** The printed solenoid numbers are SDU driver transistor positions, and the public addresses do not follow them. The ROM's solenoid test shows each driver number while it fires, pairing them as
`1->2, 2->1, 3->6, 4->7, 5->3, 6->4, 7->5, 8->8, 9->11, 10->12, 11->14, 12->13, 13->9, 14->10, 15->19, 16->15, 17->17, 18->20, 19->18` over four identical cycles. In public terms: 1 right slingshot,
2 left slingshot, 3 right three-bank reset, 4 center three-bank reset, 5 pop bumper, 6 knocker, 7 outhole kicker, 8 kick-out hole, 9-15 the knock-down coils of objects 7 down to 1 (object k on 16-k),
17 eight-bank reset, 18 coin lockout, 19 flipper enable relay, 20 loop drop target reset. Public 16 is the decoder's unaddressable slot. Every one of the nineteen drivers carries a load.

**Continuous outputs.** Public 17 (Q17, PB4), 18 (Q19, PB5), 19 (Q15, PB6) and 20 (Q18, PB7) are the SDU's continuous section. 18 and 19 are held: the coin lockout is energized from about 8.7 s after
power-up, as the manual's attract description says, and the flipper relay is on only during a game. 17 and 20 are used as pulsed coils. The power-up initialisation pulses all four once, and the kick-out hole
(8) as well. Besides its pulses after switch 21, the ROM pulsed 20 once in the gameplay run about 4.2 s after the left outlane collected the loop value; that may be the loop target's reset after a collect,
but the run does not prove it.

**Lamps.** The Lamp Driver module has sixty discrete SCR outputs. A public lamp is `16 * k + a + 1` for decoder `U(k+1)` output `S(a)`, and each output line's resistor `R<n>` ends at SCR `Q<n>`. This game's
lettered copy of sheet 12B-431S-128 was read for all sixty lines; it crosses `U2` S7/S8 to Q25/Q24 and `U3`/`U4` S9 to Q41/Q46, and the ROM confirms both: the bonus-object lamps it lights in order in the
lock-lane run are public 58, 42, 26, 10, 57, 41 and 25, the SCRs Q46, Q41, Q17, Q2, Q56, Q42 and Q24 that the light list prints for BONUS TARGET 1-7. The game's own lamp assignment is the sixty-row
`NINE BALL LDA LIGHT LOCATION` list on the playfield sheet, which names a load, wire, jack, pin and SCR for every output; the typed list on the lamp-driver sheet belongs to another game and is not used.
Four of the list's J2 pins differ from the lamp-driver sheet's connector block (SCRs Q3, Q5, Q7 and Q39); the definition follows the game's list. GAME OVER (45), HIGH SCORE TO DATE (13), MATCH (63) and TILT
(61) are backbox lamps. SHOOT AGAIN (27) is drawn on the playfield by the table. SUPER BONUS (14), R. BANK BOTTOM WOW (15) and R. BANK TOP WOW (31) changed state only in the service runs and
no play run lit them; they are printed loads and stay used. The spinner value lamps are 12, 28, 44 and 60, and the loop value lamps 55 (10K), 8 (20K), 24 (30K), 40 (40K) and 56 (top value).

**General illumination** is uncontrolled: a 6 VAC playfield string from A2J1-8, the cabinet bus and the backbox buses straight off the transformer, with no relay or driver in any line.

## Ball lifecycle

Three balls sit in the trough under the apron on switches 37, 36 and 33, left to right, the one on 33 in front of the outhole kicker. When a game starts the ROM resets the eight-bank (17) and both
three-banks (3, 4) and kicks the outhole (7), repeating all four about every 1.2 s while 33 stays closed; a real ball leaves 33 on the first kick and rolls to the shooter lane (switch 40). After a drain the
bonus times the multiplier is collected, the ball-in-play advances and the next ball is served; an extra ball is played without advancing. Tilt drops the flipper relay (19), lights TILT (61) and fires the
kick-out hole (8) to free a captured ball. A slam (8) ends the game, and the ROM repeats its power-up initialisation.

## Mechanisms

- **Left eight-target bank**: two four-target banks on one reset coil (17). Upper bank objects 2, 4, 6, 8 from the top (switches 10, 12, 14, 16), lower bank objects 7, 5, 3, 1 (switches 15, 13, 11, 9).
  Objects 1-7 have knock-down coils (public 16-k); object 8 has none. The objects are made in order: when the lit object is made the ROM resets the bank within about 35 ms and knocks down every object
  made so far, lowest first, firing each coil only after the previous target's switch has closed. If a target's switch never closes, the ROM retries that coil about every 0.8 s.
- **Kick-out hole and lock lane** at the left: switch 34 in the hole (coil 8), 38 and 39 above it. Before object 5 is lit the hole spots objects with the knock-down coils and ejects. Once object 5 is lit
  it captures: a ball on 34 is held and a new one served, a ball on 38 behind it the same, and a third ball on 39 releases all three, the ROM firing 8 once per ball.
- **Center (18, 19, 20) and right (22, 23, 24) three-target banks**, each with one reset coil (4 and 3) and no knock-downs. With option switch 14 OFF both reset only after all six targets are down.
- **Loop drop target** (21) at the exit of the top-left loop, raised by 20; the loop's entrance is the roll-under gate switch 4.
- **Spinner** (5) on the right, **pop bumper** (31 fires 5), **slingshots** (30 fires 2, 29 fires 1), the passive **top dead bumper** (17) and two passive gates.
- **Flippers**: one per side, J-25-475/34-4500 dual-winding coils, gated by the flipper enable relay; PinMAME publishes 46 (right) and 48 (left) with 45 and 47 alongside.

## Rules summary

From the manual's feature pages: each of the eight drop targets scores its object number x 1,000, and hitting the lit object advances the bonus and lights the next object (bonus maximum 45,000). The top
dead bumper and the return lanes spot the lit object when lit, and the kick-out hole and the lock-lane switches spot numbers too. Making all eight in order lights the flashing object 9 target and the
flashing WOW lite; making object 9 lights Super Bonus (77,000) for the next ball (option switch 29 moves the WOW lite and option switch 30 the Super Bonus to object 8). Making all the targets again lights Special and excludes target 1 from play,
and each further round excludes the next. Completing a three-bank advances the multiplier (7X maximum; after 6X or 7X it resets to 2X for the next ball), and once the multiplier reaches 6X or 7X a lit
outside three-bank target awards WOW. The spinner scores 100 or the highest lit value and any spin resets it; the targets option switch 17 selects advance the value, and the stand-up 35 scores 7,000 and
sends the value to the top. The loop roll-under and the left lane lower switch score 3,000 and advance the loop value; the loop target and a lit outlane collect it. Capturing all three balls, or making
object 9, releases the captured balls for three-ball play. Option switches 22-24 choose the WOW and Special awards from the chart on PDF page 11.

## Option switches

The thirty-two MPU option switches are S1-8, S9-16, S17-24 and S25-32 (Figure 1, page 12). Coin chutes 1, 2 and 3 take S1-4, S9-12 and S25-28; S5 add-a-ball, S6 high-score award, S7 balls per game, S8
background sound, S13 spot-number lite, S14 multiplier step-up, S15-16 high score to date, S17 spinner-advance targets, S18-19 maximum credits, S20 credit display, S21 match, S22-24 WOW and Special
awards, S29-30 which object lights the eight-bank WOW and Super Bonus, S31 the three-bank WOW multiplier and S32 the Special limit. PinMAME boots with all of them OFF, which gives the three-ball games of the
retained runs (S7 OFF = 3 balls). Two settings disagree between the manual's pages:

- **S17.** PDF page 11 prints ON = outside targets and OFF = center targets; PDF page 14 prints the reverse. The retained spinner-option run settles it: with S17 OFF the center targets 19 and 23 lit the
  spinner value lamps 12 and 28, and the outside targets 18, 20 and 22 lit none. Page 11 is right.
- **S8.** PDF page 11 prints ON = background sound on; PDF page 13 prints SOUND OFF = ON. Nothing retained settles it, and it stays an unresolved conflict. A harness run with S8 set ON and OFF,
  comparing the sound board commands over an idle stretch of play, would settle it, but `tools/run_pinmame_harness.py` cannot set option switches yet. An owner flipping S8 on a machine would also settle it.

The known-working scripts' option menu copies another game's text for several of these bits, so do not label a recreation's options from it.

## Displays and sound

Four seven-digit player displays (indices 0-3, segment starts 1, 9, 17 and 25), a two-digit credit display (index 4, start 35) and a two-digit match/ball-in-play display (index 5, start 38): PinMAME `dispst7`.
Sound is the Stern sound module (ST300; Figure 1 labels it B-605 and the parts list C-605); sound commands add no playfield devices.

## Disagreements between this game's own documents

- Option switches 8 and 17, as above.
- The lamp-driver sheet's connector block and the game's light list disagree on four J2 pins (SCRs Q3, Q5, Q7 and Q39); connector-pin readings only, and the light list is followed.
- The playfield sheet draws no coil for drop target 1, which the solenoid table prints as `16 Q16 J5-8 G-W DROP TARGET #1`; the ROM's solenoid test fires public 15 for driver 16, and the knock-down runs
  show it putting object 1 down.
- The installation page names three tilt switches including a `Panel tilt on bottom of playfield panel`, while the location page lists `7 ROLL-TILT`, `7 PENDULUM`, `8 TILT BOARD` and `8 DOOR`; whether the
  panel tilt is the tilt-board slam contact is not settled, so switch 7 counts the two contacts the location page lists.
- The parts list prints a `Stand-Up Target J-26-1200` coil that matches no driver in the solenoid table, and no coil for the single loop drop target; the loop target's reset coil has no part number.
- Figure 1 labels the sound board B-605; the parts list prints C-605.
- The credit table spells the coin-chute colours out (`BRN-WHITE`, `RED-WHITE`) where the Switch I.D. prints `BRN-W` and `R-W`.

## Recreation checklist

- Build the full inventory: 40 matrix switches, three service inputs, four flipper-button positions, 32 option switches, the solenoid addresses 1-15 and 17-20 with the two flipper callbacks, the sixty
  SCR lamp addresses and the six displays.
- Start with three balls in the trough (33, 36 and 37 closed), every drop target up, the lock lane empty and the flipper relay off until a game starts.
- Make each knock-down coil (public 16-k) put its object's target down so that its switch closes; the ROM waits for that switch before the next spot and retries the coil about every 0.8 s until it closes.
- Capture balls in the kick-out hole and the lane behind it once object 5 is lit, and release them one at a time on public 8.
- Treat the manual's feature pages and the ROM as the rules authority; the community ROMs change rules, not hardware.
- Placements: switches, coils and general illumination come from the retained table and are `observed`; lamps are unplaced until a table or drawing marks their sockets.

## What would complete the record

- **Spatial placement**: a Nine Ball table that models its insert bulbs (or a lamp-location drawing), a second independent table or a factory-drawing callout check for the switches and coils, and a
  trough model with objects at 33, 36 and 37.
- **Option switch 8**: the harness probe or owner check described above.

## Retained table and its defects

The geometry comes from `Nine Ball (Stern 1980).vpx` by bord (1.0, June 2017, with bracket primitives by randr), the only local Nine Ball table. Its script binds the same solenoids and switches as the two
pinned corpus scripts, which share its option menu and ball control and add a VR room, except where it is defective: trigger `sw38` writes switch 39 and nothing writes 38, trigger `sw1` at the top of the lock
lane has no handler, the pop bumper's SolCallback(5) is commented out (the bumper kicks on its own hit), and `sw27_Hit` is defined twice. None of these changes what the machine is; they are stated on the
affected devices. Its insert lights show no bulb mesh, so they place no lamp.

## Sources

- `manual.stern.nine-ball.1980`: the 23-page IPDB manual, with transcribed excerpts of its identification tables, location drawings, parts pages, option switches, flipper wiring and operating text.
- `schematic.stern.nine-ball.wiring-set`: the four-page IPDB schematic set, with excerpts of the playfield sheet (switch matrix, coil wiring, light list), the solenoid driver sheet, the lamp driver sheet
  and the general-illumination buses.
- `vpx-script.nine-ball-corpus` and `vpx-script.nine-ball-standalone`: the pinned known-working corpus scripts.
- `vpx-table.nine-ball-bord-1-0`, its embedded script and its retained extraction: the geometry of every placement.
- `runtime.nine-ball.*`: ten isolated harness runs on the pinned `pinmame64.dll`, eight of `nineball` (ROM archive SHA-256 `4311155374bd000db727c74747cfec8707755a899e5bfd25cc35c133851da971`) and one
  each of `ninebafp` and `ninebalb`; ROM bytes and raw NVRAM remain outside the repository.
- `pinmame.core.46e1a01a0f73`: driver declarations, MPU-200 implementation, public-address conversion and display layout.
