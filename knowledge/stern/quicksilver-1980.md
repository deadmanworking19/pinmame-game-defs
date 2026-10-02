# Quicksilver (Stern, 1980)

Coverage: **partial - the physical inventory, controller bindings, wiring and mechanisms are validated; one lamp circuit's fitment and the playfield placements are not**

## Identity and evidence precedence

This is the one physical Stern Quicksilver (IPDB 1895, June 1980, model 117, Stern M-200 MPU, 1,201 units). PinMAME `quicksil` is the production root and `quicksfp` its stock free-play clone; both use the same game-data line (`GEN_STMPU200`, seven-digit
`dispst7` displays, `FLIP_SW(FLIP_L)`, ST300 sound), and the community rules revisions `quicksib` (07D, 2021) and `quicksic` (8.1, 2024) use the same line again, so all four are physically identical; only the rules ROMs differ. The ROM archives `quicksil.zip` and
`quicksfp.zip` were available; `quicksib` and `quicksic` were not, so nothing here was measured on them.

The evidence order is the runbook's. The known-working VPW 1.0 script and the earlier retained tables give runtime semantics, this game's own manual, Lamp Driver Schematic (12B-432-S-116) and Solenoid Driver Schematic (12B-432-S-117 sheet 3) give construction and wiring, pinned PinMAME gives
the controller topology, and three retained harness runs (a Self Test sweep, the stuck-switch test and a scripted game) give the public addresses. The Lamp Driver Schematic was drawn for a sister game, `CHEETAH`, and relabelled by hand for this one; its list is Quicksilver's own and its
SCR numbering is the board's.

## Address translations

**Switches.** The matrix is five strobes by eight returns, public 1-40, and the ROM's stuck-switch display shows the closed address's own number for every one of the forty (retained run). The printed Self Test numbers are therefore the public addresses.
All forty positions are fitted: coin chutes 1-3, spinners 4-5, credit 6, tilt 7, slam 8, bumpers 9-11, slingshots 12-13, stand-ups 14-16, 25-27 and 40, top lanes 17-20, center drop targets 21-24, special roll-over 28, kick-out hole 29, right drop targets 30-32, out-hole 33,
outlanes and return lanes 34-37, bounce rubbers 38 and roll-over button 39. Every matrix contact is drawn as a normally open contact with a series 1N4004 diode. The cabinet switches (1-3, 6-8) are wired on the cabinet sheet through the front-door jack to MPU connector A4J3, the others on the
playfield sheet to A4J2. Service inputs are -7 (Self Test), -6 (CPU diagnostic NMI) and -5 (sound diagnostic); -6 and -5 are PinMAME routes whose physical buttons the manual does not document. The cabinet flipper buttons are PinMAME's synthetic 84 (left) and 82 (right); 81 and 83 are the
unused upper positions. Each flipper's end-of-stroke contact is a hard-wired normally closed contact drawn across the first winding of its dual-winding coil and is not a PinMAME address.

**Solenoids.** The printed solenoid list numbers the SDU transistors 1-19 and the public addresses do not follow it. The ROM's own Self Test energizes them in physical order, and the public addresses fire as `2,1,6,7,3,4,5,8,11,12,14,13,9,10,19,15,17,20,18`, so physical 1..19 map to public
`1->2, 2->1, 3->6, 4->7, 5->3, 6->4, 7->5, 8->8, 9->11, 10->12, 11->14, 12->13, 13->9, 14->10, 15->19, 16->15, 17->17, 18->20, 19->18`. Nine of those positions were independently confirmed in play: the three thumpers and two slingshots fire on their own switches (public 1, 2, 3, 4, 5 for
switches 9, 10, 11, 12, 13), the two drop-bank resets fire when their last target closes (7 and 8), the kick-out hole fires on its switch (9), the out-hole kicker fires from game start (10) and the flipper-enable relay rises at game start and drops on a tilt (19). Public 16 is an unaddressable decoder slot. Physical 9-12, 16, 17 and 18 are
printed OPEN and are unused. The lower flippers are the synthetic held-coil outputs 46 (right) and 48 (left); PinMAME also asserts 45 and 47 for exactly the same interval as 46 and 48 (retained gameplay run; `core.c` asserts both bits of each pair while the button is closed), which the Stern MPU-200 controller profile does not declare and this definition does not bind.

**Lamps.** The Lamp Driver module has sixty discrete SCR outputs, not a matrix. A public lamp is `16 * k + a + 1` for decoder chip `U(k+1)` output `S(a)`, and each of the sixty output lines carries a resistor `R<n>` that ends at SCR `Q<n>` (the schematic's resistor and SCR numbers match on every line). The mapping from public address to SCR therefore
comes from the decoder drawing, and the connector table gives each SCR its jack and pin. This definition gives all sixty. Public 16, 32, 48 and 64 are unaddressable decoder slots. Two of the schematic's readings are easy to transpose and were checked three ways: `U2` outputs S7 and S8 drive SCRs Q25 and Q24, so the right
stand-up lamp V (J1 pin 6, Q25) is public 24 and the unused SCR Q24 is public 25, and `U3` and `U4` output S9 drive Q41 and Q46, so top divider 2 (Q41) is public 42 and top divider 1 (Q46) is public 58. The retained tables bind public 24 to the V insert, and the five dividers (10, 26, 42, 57, 58) light together in the ROM's coin-in lamp show.

The playfield lamp wiring list prints fifty rows and the Lamp Driver Schematic's list prints fifty-four: it adds `GAME OVER` (public 45), `HIGH SCORE TO DATE` (13), `MATCH` (63) and `TILT` (61). The two lists disagree about one pin and one number only: `SHOOT AGAIN` is J1 pin 26 on the playfield list and J2 pin 21 on the schematic (one SCR, Q3, reaches both, and there is a
playfield insert and a backbox bulb), and the playfield list prints jack J2 pin 6 for both spinner lamps while the schematic strikes the left spinner's 6 out by hand and writes 7. Those are wiring-detail differences and are resolved as device notes.

## Lamps with no printed load

Five SCRs have no row in either list and are driven by the ROM only in the power-up lamp flash (which ends about 12.6 s after power-up) and the self-test sweep, never in the attract pattern or in play (retained gameplay run): public 25, 27, 29, 41 and 43. They are recorded `unused`. Public 29 is the lamp a sister machine labels Ball in Play; here the ball in play is a digit on the Match/Ball display module.
**Public 6 (SCR Q10, connector pin J1-15) is different.** No list prints a load for it, yet the ROM keeps toggling it in the attract-mode lamp pattern after the power-up flash, together with 38 lamps that are all listed (retained gameplay run). The evidence available cannot say whether a bulb is fitted behind it, so it is recorded with availability `unknown`
and `output_semantics` stays in `coverage.missing`. A bulb-level answer needs a photograph of an unrestored machine's A5J1 harness at pin 15, or the ROM's lamp-show data decoded to see which feature it accompanies.

General illumination is a 6 VAC lamp string (`A2J1-8` to `A2J1-1`) with no driver-board connection and no controller address.

## Ball lifecycle

Quicksilver is a single-ball game with no trough. The ball starts on the out-hole switch (public 33). When a game starts the ROM resets both drop banks (public 7 and 8), ejects the kick-out hole once (9) and kicks the out-hole (10) repeatedly for as long as 33 stays closed. A real ball leaves 33 after the first kick and rolls to the shooter lane,
where the player launches it with the plunger. After a drain the ball returns to 33, the bonus is counted, the ball-in-play digit advances and the kick repeats. The retained tables release the ball from a shooter-lane kicker at 90 degrees. Tilt disqualifies the ball only: the ROM drops the flipper-enable relay (19) when switch 7 closes, and normal play resumes at the next serve.

## Mechanisms

- **Center bank:** four drop targets on a slant (switches 21 highest to 24 lowest, `4 Bank Target D-580-4`), closed while down, one reset coil (public 7, B-27-2300). The ROM resets the bank when the fourth target closes.
- **Right bank:** three drop targets beside the right rail (30 highest to 32 lowest, `3 Bank Target D-580-3`), one reset coil (public 8). Reset when the third target closes. Downing it raises the bonus multiplier (instruction card).
- **Kick-out hole:** a hole at the left edge with its switch (29) and an eject coil (public 9, J-28-2300) the ROM fires when a ball sits in it.
- **Spinners:** two spin target assemblies, switch 4 on the right and 5 on the left, 200 points per rotation in the retained run. Their lamps are public 46 (right) and 62 (left).
- **Pop bumpers and slingshots:** the ROM fires each coil when its own switch closes (public 1, 2, 3 for switches 9, 10, 11; public 4 and 5 for switches 12 and 13). The printed solenoid numbers are 2, 1 and 5 for the thumpers and 6 and 7 for the slingshots.
- **Flippers:** two lower dual-winding flippers fed from the +43 VDC bus through the flipper-enable relay; the buttons are hard-wired on A3J2-2 (left) and A3J2-1 (right).

## Scoring checkpoints from the retained gameplay run

Pop bumpers score 1,000, slingshots 10, spinners 200, the stand-ups (14, 15, 16, 25, 26, 27, 40) and top lanes 500, the special roll-over 1,000, the outlanes 25,000, the return lanes 5,000, bounce rubbers and the roll-over button 10. Center-bank targets score 1,000 each when closed, and opening the completed bank pays a further 3,000 after its reset fires; right-bank targets 30 and 31 score 500 each, and closing the third target (32) scores 25,500 and fires the bank reset. The kick-out hole scores 5,000. These are first-ball ROM scores
and only checkpoints: the instruction card governs the rules.

## Rules summary (instruction card)

Pop bumpers score 1,000. The bonus multiplier increases when the right three-bank is down. Q-U-I-C-K and S-I-L-V-E-R targets advance the bonus only when not already lit; the 75,000 bonus lights after the 20,000 step and a lit 75,000 does not collect the multiplier. Lighting all QUICK SILVER targets lights the top and outlane specials.
A spinner's value increases when the ball enters the opposite return lane and must be re-lit after the spinner is hit. The kick-out target scores 5,000 and advances the center target value. Each center-bank target scores 1,000 plus its lit value, and downing all four spots the next letter. Spotting Q-U-I-C-K and then hitting the flashing target awards an extra ball. Tilt disqualifies the ball in play only.

## Option switches

The thirty-two MPU option switches are S1-8, S9-16, S17-24 and S25-32. Coin chutes 1, 2 and 3 take S1-4, S9-12 and S25-28 (the credit catalog); S5 add-a-ball memory, S6 high-score award, S7 balls per game (ON = 5), S8 maximum add-a-balls, S13 flashing-lite retention, S14 background sound, S15-16 high game to date, S17 QUICK extra ball
per game, S18-19 maximum credits (10/15/25/40), S20 credit display, S21 match, S22 QUICK extra ball, S23-24 special lite alternation, S29 QUICK SILVER special carry-over, S30 special replay limit and S31-32 special award. S33 on the MPU is a memory-clear pushbutton.

## Displays and sound

Four seven-digit score displays at layout indices 0-3 and segment-memory starts 1, 9, 17 and 25, a two-digit credits display (index 4, start 35) and a two-digit match/ball-in-play display (index 5, start 38): PinMAME `dispst7`. Sound is the Stern ST300 board (sound module C-605); sound commands add no playfield devices.

## Defects in consumed artifacts

- The retained VPW 1.0 script pulses switches 20 and 21 from its slingshots; the correct addresses are 12 and 13 (the corpus 1.0 script and the older retained table pulse them, and the ROM fires the sling coils on them). It also drives the two right-side coil banks through custom animation code, which does not change the controller contract.
- The older retained table names its two upper bumper objects the other way round: `Bumper1` stands at the left and pulses the right bumper's switch 9.
- The playfield wiring sheet prints `A3J1-5 (B-G)` for the out-hole and `A3J5-12 (D-O)` for the right drop-target bank; the Solenoid Driver Schematic places them on J5 pins 11 and 10, which are the pins used.

## Recreation checklist

- Build the full inventory: 40 matrix switches, three service inputs, four flipper-button positions, 32 option switches, the 18 solenoid addresses and two flipper coils, the 60 SCR lamp addresses and the six displays.
- Start with the ball on the out-hole switch, both drop banks up, the kick-out hole empty and the flipper-enable relay off until a game starts.
- Reproduce the ROM-fired thumpers and slingshots, the two drop-bank resets, the kick-out eject, the out-hole serve loop and the tilt behaviour exactly as the harness runs show.
- The slam quantity is left unstated: the location sheet lists a door and a tilt-board contact, while the operating text (manual page 5) also names one on the playfield, and no retained source settles whether that third contact was fitted. All of them share public address 8.
- Treat the instruction card as the rules summary and the ROM as the rules authority; the community 07D and 8.1 ROMs change rules, not hardware.
- Switch and solenoid placements are validated against the manual's two location drawings where they agree (46 of 48 checked); lamp placements are observed from the retained table only, and the five top-divider lamps have no placement.

## Sources

- `manual.stern.quicksilver.1980`: the 35-page IPDB manual, SHA-256 `140216dc27e97084e0b523fe0d5ff5417961723fea069b1fad3dd594b9723728`, with transcribed excerpts of its identification tables, switch and solenoid drawings, playfield and cabinet wiring, option switches and parts list.
- `schematic.stern.quicksilver.lamp-driver` and `schematic.stern.quicksilver.solenoid-driver`: the IPDB Lamp Driver and Solenoid Driver schematics, SHA-256 `bea05d384e1f7ddf2dc98793cc1c9c82a38aece048b6750fe67371b2262870ee` and `f71e59b6d72e7d1315eeb3eaca940479bd882d9d3bcbfb008905180f92078a5d`.
- `manual.stern.quicksilver.instruction-card`: the rules card, SHA-256 `f85d0a60e1a03bf904623816fa5747d64020a0a81192964915cd717180be3f67`.
- `vpx-table.quicksilver-vpw-1-0`, `vpx-script.quicksilver-vpw-1-0`, the corpus 1.0 script and the earlier archive table: geometry and runtime semantics.
- `runtime.quicksilver.self-test`, `runtime.quicksilver.stuck-switch-test` and `runtime.quicksilver.gameplay`: three isolated harness runs of `quicksil` (ROM archive SHA-256 `691e06ac64f445cde8842934efdc3a7e223b408f442131bcb2903bde56b45ad3`) on the pinned `pinmame64.dll`; ROM bytes and raw NVRAM remain outside the repository.
- `pinmame.core.8371478a7640`: driver declarations, MPU-200 implementation, public-address conversion and display layouts.
