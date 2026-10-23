# Big Game (Stern, 1980)

Coverage: **partial - the controller inventory, wiring, mechanisms and rules are documented and the public addresses proved by the ROM's own tests; one continuous output's purpose is unexplained, the lamp placements rest on one table and general illumination is unplaced**

## Identity and evidence precedence

This is the one physical Stern Big Game (IPDB 249, March 1980, model 121, Stern M-200 MPU, 2,713 units, Stern's first widebody). PinMAME `biggame` is the production root and `biggamfp` its stock free-play clone;
`biggameb`, `biggamec`, `biggamed`, `biggamee` and `biggamef` are the community rules revisions 7, 8, 9, 12 and 13 (2019-2024). All seven use the same game-data line (`GEN_STMPU200`, seven-digit `dispst7`
displays, `FLIP_SW(FLIP_L)`, no extra lamp columns, ST300 sound), so they are physically identical and only the ROM rules differ. Only `biggame.zip` was used for the harness runs.

Evidence order is the runbook's. The two pinned corpus scripts give runtime bindings (the 1.5.1 VR build is the working one; the older 1.0.4 script says it was not verified), this game's own manual, March 1980
corrections sheet and schematic set give construction and wiring, pinned PinMAME gives the controller topology, and five retained harness runs of `biggame` (burn-in, solenoid test, switch test, a scripted game, and a
game-over and slam run) pair the printed numbers with public addresses. The manual is a 72 dpi scan without a lamp-location drawing; the schematic set is a 300 dpi scan whose Lamp Driver, Solenoid Driver and Playfield
Wiring sheets are drawn for this game.

## Address translations

**Switches.** The matrix is five strobes by eight returns, public 1-40, and the ROM's switch test shows the closed address's own number for every one of the forty (retained run), so the Switch Identification
numbers are the public addresses. All forty positions are fitted. Cabinet switches 1-3 (coin chutes), 6 (credit), 7 (tilt) and 8 (slam) are wired on the cabinet sheet to MPU connector A4J3, the others on the playfield
sheet to A4J2. Every matrix contact is normally open, and the sheets draw a series 1N4004 diode on each except coin chutes 2 and 3, which the cabinet sheet draws without one. PinMAME's BY35 read path takes them unmasked, so public 1 is a closed contact. Service inputs are -7 (Self Test), -6 (CPU diagnostic
NMI) and -5 (sound diagnostic); the last two are PinMAME routes with no documented button. The flipper buttons are PinMAME's synthetic 84 (left) and 82 (right); 81 and 83 are unused. The flippers' end-of-stroke
contacts and the door's remote S33 memory-clear button are hard-wired and have only profile-local identities (physical direct inputs 1-3).

**Solenoids.** The printed solenoid numbers are SDU driver transistor positions, and the public addresses do not follow them. The ROM's solenoid test shows each driver number while it fires, pairing them as
`1->2, 2->1, 3->6, 4->7, 5->3, 6->4, 7->5, 8->8, 9->11, 10->12, 11->14, 12->13, 13->9, 14->10, 15->19, 16->15, 17->17, 18->20, 19->18` over three identical cycles. In public terms: 1 top thumper, 2 lower left thumper,
3 lower right thumper, 4 left slingshot, 5 right slingshot, 6 knocker, 7 top-left bank reset, 8 top-right bank reset, 9 lower-right bank reset, 10 saucer eject, 11 out-hole kicker, 18 coin lockout, 19 flipper
enable relay. Public 12-15 (drivers 10, 12, 11, 16) are printed OPEN and unused; 16 is an unaddressable decoder slot. The gameplay run independently confirms 1-5 and 7-11 and 19.

**Continuous outputs 17 and 20.** Public 17 is driver Q17 (PIA PB4). The manual prints it OPEN and the parts list names no relay, but the Solenoid Driver Schematic drawn for this game labels its J5 pin 7
`GEN. ILLUM. RELAY`. No other sheet has a relay in any general-illumination circuit, and the ROM drives 17 only in the power-up initialisation pulse it gives all four continuous lines and in its own tests.
It is recorded unused, with the label stated, as Star Gazer's record treats its own solenoid-sheet label on an OPEN position. Award events were not exercised, because PinMAME's default option switches
disable them. Public 20 is driver Q18 (PB7). The manual prints it OPEN and the schematic wires it only to N/U pins, yet the ROM holds it on for about 1.5 s whenever the displays flash `7777777` in
attract mode. Nothing documents a load or a reason, so it stays `unknown` and `output_semantics` stays in `coverage.missing`. Settling it needs the ROM's attract routine decoded, or an owner's check of whether
anything is connected to SDU J2 pin 15, J3 pin 9 or J5 pin 3. Static analysis found the ROM's generic set and clear routines for the four continuous bits at 0x1816 and 0x1829, but not yet their callers.

**Lamps.** The Lamp Driver module has sixty discrete SCR outputs. A public lamp is `16 * k + a + 1` for decoder `U(k+1)` output `S(a)`, and each output line's resistor `R<n>` ends at SCR `Q<n>`; this game's sheet
was read for all sixty lines and matches the LDA-100 order other Stern MPU-200 games use, including the transposable U2 S7/S8 (Q25/Q24) and U3/U4 S9 (Q41/Q46) pairs. The connector blocks give each SCR its pin.
The Lamp Driver Schematic's list has 56 rows, the playfield list the same rows without the four backbox lamps (GAME OVER 45, HIGH SCORE TO DATE 13, MATCH 63, TILT 61), and the 56 rows land on 56 different public
addresses. Every lamp the ROM lit for a switch in the gameplay run is the one its row names: B, I and G for the top lanes (42, 26, 10), the second G and A for the stand-ups (57, 41), E for the right return lane (9), the
card numbers each drop target spots, and the B-I-G awards (6 and 30). The four SCRs without a row, public 14, 15, 31 and 47, change only in the burn-in and lamp tests and are unused. Public 25, the letter M, sits on J1
pin 5, but the connector block's J1 row for its SCR (Q24) prints a flat-topped figure that reads as 3 or 5; the ROM flashes 25 with the other six letters when the saucer collects them.

The seven letter lamps (9, 10, 25, 26, 41, 42, 57) each light two inserts, the letter at its own lane or target and the letter in the B-I-G-G-A-M-E column beside the eject-pocket lane (instruction card, IPDB
photographs). General illumination is an uncontrolled 6 VAC playfield string, the front-door lamp and 5.9 VAC backbox lamps straight from the transformer.

## Ball lifecycle

Big Game is a single-ball game with no trough. The ball starts on the out-hole switch (33). When a game starts the ROM resets the three drop banks (7, 8, 9) and kicks the out-hole (11), repeating both for as long as 33
stays closed; a real ball leaves 33 on the first kick and rolls to the shooter lane, where the player launches it. After a drain the bonus and multiplier are added, the ball-in-play digit advances and the kick repeats;
an extra ball is played without advancing. Tilt drops the flipper enable relay (19) and disqualifies the ball only (instruction card); a slam (8) ends the game and the ROM restarts through its power-up test.

## Mechanisms

- **Three drop banks**, each three targets with one reset coil: top-left 1A (targets 3, 2, 1 top to bottom = switches 14, 15, 16; reset 7), top-right 1B (4, 5, 6 = switches 24, 23, 22; reset 8) and lower-right 1C
  (7, 8, 9 = switches 32, 31, 30; reset 9). The ROM resets a bank when its last target goes down and at every serve. Each target spots its number in the selected cards.
- **Eject pocket (saucer)** at the top of the left loop: switch 34, eject coil 10.
- **Spinners**: two on one wire across the left loop, left (4) at the outer end and right (5) beside the top-left bank; no coil.
- **Thumper bumpers** 9 (top), 10 (lower left), 11 (lower right) fire public 1, 2 and 3; **slingshots** 12 and 13 fire 4 and 5.
- **Flippers**: four, two per side at the bottom of the playfield, each side's lower (J-25-475/34-4500) and upper (J-25-500/34-5050) coils in parallel on one drive wire and one cabinet button, gated by the flipper
  enable relay. PinMAME publishes one callback per side (46 right, 48 left, with 45 and 47 alongside).
- **Passive gates** at the top of the right lane and the top of the left loop.

## Rules summary

From the instruction card and the manual's feature pages: three bingo-style cards X, Y and Z of nine numbers each; drop targets spot their numbers in the selected card or cards, and the card selection changes on
the top bumper, the slingshots, the center roll-over button and the top lanes. Each lit number adds 1,000 bonus; a full set of cards moves the 27,000 bonus to the reserve. Lines on the cards light 2X and 3X, the 5,000
extra score per line, the right outlane extra ball and the left outlane special. Spotting B-I-G-G-A-M-E lights the letters in the eject-pocket lane; the pocket scores 5,000 per lit letter and 35,000 more when the word is
made, and the left center side lane awards the extra ball the first time and the special the second. The top lanes score 500 and 5,000 for the middle lane when BIG is lit; the right roll-over buttons score 2,000 when Z is
lit.

## Scoring checkpoints from the retained gameplay run

Thumpers 1,000; slingshots 10; top lanes, stand-ups and drop targets 500; the left spinner 2,000 with card X selected and the right spinner 100 before B-I-G; the center roll-over, the left center side lane and the return
lanes 5,000; the outlanes 10,000; the top 10-point switches 10; the right roll-over buttons 2,000 with card Z selected; the top-left roll-over 5,000 after B-I-G (the manual says 3,000, the playfield art and the ROM
5,000); the saucer 35,000 after B-I-G-G-A-M-E. These are first-ball ROM scores and only checkpoints.

## Option switches

The thirty-two MPU option switches are S1-8, S9-16, S17-24 and S25-32 (Figure 1, page 11). Coin chutes 2, 3 and 1 take S1-5, S9-13 and S27-30. S6 high-score award, S7 balls per game, S8 background sound, S15-16 high game to date,
S17 extra ball, S18-19 maximum credits, S20 credit display, S21 match, S22 special replay limit, S23 card selection order, S25-26 the ball on which the 5,000-per-line feature comes on, S31-32 special award; S14 and S24 are
not used. The March 1980 corrections sheet reverses the printed S8 (ON = sound off) and S22 (ON = one replay per ball) settings. S33 on the MPU is a memory-clear pushbutton, repeated on the coin door.

## Displays and sound

Four seven-digit player displays (indices 0-3, segment starts 1, 9, 17 and 25), a two-digit credit display (index 4, start 35) and a two-digit match/ball-in-play display (index 5, start 38): PinMAME `dispst7`.
Big Game was the first electronic game with seven-digit displays; in attract mode all four count `1234567` and flash `7777777`. Sound is the Stern B-605 sound board (ST300); sound commands add no playfield devices.

## Disagreements between this game's own documents

- The feature text names the top bumper `SWS-#11` once and `SW-#9` once; the switch table, the matrix sheet, the location drawing and the ROM put it on 9.
- The credit tables call coin switch 1 `BLUE` and switch 3 `RED-WHITE`; the cabinet sheet prints `R-W` on switch 1's return and `BLU` on switch 3's. A wire-colour difference only.
- The switch table calls switch 27 a roll-over button; the matrix sheet, the location drawing and the parts drawing make it a roll-over wire, which is what the definition records.
- The manual says the top-left roll-over scores 3,000 when BIG is made; the playfield art and the ROM give 5,000.

## Recreation checklist

- Build the full inventory: 40 matrix switches, three service inputs, four flipper-button positions, 32 option switches, the solenoid addresses 1-15 and 17-20 with the two flipper callbacks, the sixty SCR lamp addresses
  and the six displays.
- Start with the ball on the out-hole switch, all nine drop targets up, the saucer empty and the flipper enable relay off until a game starts.
- Reproduce the ROM-fired thumpers and slingshots, the three bank resets, the saucer eject, the out-hole serve loop and the tilt behaviour as the harness runs show.
- Drive both flippers of a side from one callback; drive both inserts of a letter from one lamp.
- Treat the instruction card and the ROM as the rules authority; the community MOD ROMs change rules, not hardware.
- Wire lamps 5, 6, 30 and 37 to the inserts this game's lamp sheet names, not the ones the retained table drives (next section).
- Placements: switches and coils come from the retained table and are checked against the factory drawings (the spatial report lists the outcome); lamps are observed from the table only; general illumination is unplaced.

## Retained table and its lamp-binding defects

The geometry comes from `Big Game (Stern 1980) - redbone(MOD) v1.2.0`, jpsalas' table 4.1.1 with redbone's graphics. Its script binds exactly the same lamps, switches and coils as the pinned 1.5.1 and 1.0.4 corpus scripts.
It models four flippers, two per side, and the drop banks, saucer and spinner wire where the factory drawings put them. Its lamp map comes from an older script (its header says so, because of "missing pages and errors on the manual").
It matches this game's Lamp Driver Schematic everywhere except four lamps:

- Lamp 6 (`TOP R.O.W. "I" 5,000`) is bound to the two spinner value inserts; the table lights the `5.000 WHEN LIT` insert above the middle lane itself whenever B, I and G are lit, the same condition the ROM uses for lamp 6.
- Lamp 30 (`RIGHT SPIN. TARG. 1,000`) is bound to a glow under the top-left roll-over button; the right spinner's `100 OR 1000 WHEN LIT` insert is on lamp 6 in the table.
- Lamp 37 (`"X" & LEFT SPIN. TARG.`): the table drives the left spinner's `200 OR 2000 WHEN LIT` insert from lamp 6. The ROM scored the left spinner at 2,000 with card X (37) on and lamp 6 off, so the table is wrong.
- Lamp 5 (`"Z" & R. 1,000 WHEN LIT`): the table drives the right roll-over buttons' `2.000 WHEN LIT` insert from lamp 34 (the reserve bonus). The ROM scored those buttons at 2,000 with card Z (5) on and lamp 34 off, so the table is wrong.

The definition places each of these lamps on the insert its printed row names. The eject pocket's `15.000 WHEN LIT` insert is named by no printed row; it is placed under lamp 53, as the script binds it, with the bulb count left unstated. The top-left roll-over button's `500 OR 5000 WHEN LIT` has no lamp in any printed row and is not placed.

## Sources

- `manual.stern.big-game.1980`: the 22-page IPDB manual, with transcribed excerpts of its identification tables, location drawings, parts pages, option switches and operating text.
- `manual.stern.big-game.corrections-1980-03`: the March 1980 corrections sheet.
- `schematic.stern.big-game.wiring-set`: the nine-page IPDB schematic set, with excerpts of the lamp driver, solenoid driver, playfield and cabinet sheets.
- `photo.ipdb-249.instruction-card` and `photo.ipdb-249.playfield`: IPDB photographs of the instruction card and the playfield.
- `vpx-script.big-game-vr-1-5-1` and `vpx-script.big-game-1-0-4`: the pinned corpus scripts.
- `vpx-table.big-game-redbone-1-2-0`, its embedded script and its retained extraction: the geometry of every placement.
- `review.big-game.drawing-callouts`: the factory location-drawing callout check.
- `runtime.big-game.*`: five isolated harness runs of `biggame` (ROM archive SHA-256 `e5cedcdb33f648a2a735fa4c250b9a379a935c06370c7c67500fe2cf70bc8043`) on the pinned `pinmame64.dll`; ROM bytes and raw NVRAM
  remain outside the repository.
- `pinmame.core.97aa922bf8e4`: driver declarations, MPU-200 implementation, public-address conversion and display layout.
