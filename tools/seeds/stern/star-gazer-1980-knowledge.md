# Star Gazer (Stern 1980)

Coverage: **partial - two requirements are open: `spatial_placement` (two lamp circuits have no retained location, and the two stand-up targets at the left of the upper-right arch are in an open conflict) and `unresolved_conflicts`. Every other dimension is validated.**

Every input and output address is enumerated and named from the machine's own manual and schematics and from the retained ROM's behaviour, wiring and polarity are recorded, and every playfield device that has a retained location carries a normalized placement. What is not recorded is stated plainly below, in the definition's `conflicts` and in the device notes it affects.

## Identity and variants

- PinMAME catalog: root driver `stargzr` (Star Gazer, Stern, 1980), its free-play clone `stargzfp`, and the 2006 modified-rules clone `stargzrb` ("Star Gazer (modified rules rev. 9)", Stern / Oliver).
- IPDB 2346 (Stern Electronics, Chicago, August 1980, model number 127, MPU Stern M-200, 869 units, design Brian Poklacki, art Gerry Simkus) and OPDB `GrZY2-ML0Rb`. The manual's parts list is headed "STAR GAZER #127", which matches the IPDB model number.
- All three drivers declare the same game data: `GEN_STMPU200`, the seven-digit `dispst7` display layout, `FLIP_SW(FLIP_L)` and the ST300 sound board. In the retained burn-in run each published the same sixty lamp and nineteen solenoid addresses in the same order, so all three are recorded as physically identical to the production machine; `stargzfp` swaps two program ROMs for a free-play build and `stargzrb` swaps three for modified rules.
- The ROM zips used for the runs match the pinned driver's SHA-1 for every member (checked for all twelve ROM files).

## Evidence precedence

The ROM's own behaviour in the pinned LibPinMAME harness decides every public address and every semantic that depends on what the game does: the service tests, the cabinet-switch constants in the retained Stern VPinMAME library and the known-working table's bindings agree with it wherever they overlap. The manual and the schematics decide physical construction: wiring, connector pins, wire colours, driver transistors, part numbers, and what is and is not fitted. The retained table (VPW v2.0.0, whose embedded script equals the pinned script apart from whitespace) decides coordinates. Where the printed documents and the ROM disagree the record says so on the device.

## Controller address translations

Stern prints three different numbers for a solenoid and PinMAME publishes a fourth:

- The manual's solenoid list, and the number the ROM's solenoid test shows on the player display, is a test order and a driver position (the schematic's note says the displayed number "is Drive Transistor (Q) Position on SDU"): 1 to 19, with 20 to 29 for the sound board.
- PinMAME publishes decoder outputs 1 to 15, continuous outputs 17 to 20, and no output at 16.
- The two orders differ, and the retained solenoid test pairs them exactly: displayed `1->2, 2->1, 3->6, 4->7, 5->3, 6->4, 7->5, 8->8, 9->11, 10->12, 11->14, 12->13, 13->9, 14->10, 15->19, 16->15, 17->17, 18->20, 19->18` (printed number, then public address). The pairing was read from the display 0.25 s after each pulse and repeated identically at the start of the test's second cycle.
- Gameplay confirms it for every used coil by closing one switch at a time (below), so the pairing is not a guess from order alone. The printed numbers are kept as `manual.self-test` aliases and the driver transistor `Q` numbers as wiring.

The sixty lamps are an LDA-100 board of discrete SCR circuits, not a matrix. PinMAME publishes 1 to 15, 17 to 31, 33 to 47 and 49 to 63; 16, 32, 48 and 64 do not exist. The chart prints each lamp's SCR (`Q1` to `Q60`), connector pin and wire; the retained runs connect the public address to the printed row for every lamp that has behaviour to observe, and the other lamps follow the board's decoder order:

- the eight spinner-and-bank value lamps (500 to 4000) flash in the sweep order `7, 23, 39, 55, 8, 24, 40, 56` and back;
- the twelve zodiac sign lamps each flash when their stand-up closes (public 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35 and 51);
- public 11, 13, 45, 61 and 63 are the shoot-again, high-score, game-over, tilt and match lamps (the table reads exactly these for its backglass reels, game over and match are lit at power-up and drop once a coin posts a credit, and high score flashes in attract mode).

**Public 24 and 25 are the one pair the printed chart and the ROM cross.** The chart gives the 3000 value lamp Q25 on connector pin J1-6, and the lane lamp "L. 3 FROM TOP STAR ROLL-OVER" connector pin J1-5. The ROM's sweep makes public 24 the 3000 lamp, and the lamp-driver schematic draws J1 pin 5 at Q24 and pin 6 at Q25 (the chart prints Q27 for the lane lamp, the transistor it also gives SCORPIO, a misprint of Q24). Public 24 therefore reaches Q25 and public 25 reaches Q24. The Ali record pairs public 24 with Q24 and 25 with Q25; both are unused lamps there, so nothing in that record tested the pairing.

## Switches

All forty matrix addresses (five strobes by eight returns) are used, and the ROM's switch test displays each public address `N` as `N` (checked for every address 1 to 40, with the display flashing 0 when everything is open), so the manual's printed numbers are the public addresses. Every matrix contact is normally open: the manual calls them gold-plated contact switches adjusted to a 1/16 inch gap, the ROM treats public 1 as closed, and and the retained switch test displays a switch's number while its public address is 1. The matrix drawing prints a capacitor symbol across the contacts of switches 7, 8, 10, 11, 15 to 21, 31, 32 and 36 to 40; no other switch has one.

- 1 to 3 coin chutes (left, centre, right), 6 credit, 7 tilt (ball roll and plumb bob in parallel, with a panel tilt), 8 slam, tilt board and vibration.
- 4 left spinner, 5 right spinner and 9 centre spinner. The manual calls 9 "SPIN TARGET (CENTER)" and puts it at the upper-left lane mouth; each closure scores 200 in the ROM.
- 10, 11, 17 to 21, 31, 32 and 38 to 40 are the twelve zodiac stand-ups; each scores 1,000 and lights its sign lamp (names and the open question about 19 and 20 below).
- 12, 13, 14 left, right and centre thumper bumper skirts; 15 right and 16 left slingshot. The ROM scores 1,000 per thumper hit and 10 per slingshot hit.
- Three drop-target banks: 22, 23, 24 (left bank, bottom to top), 25, 26, 27 (upper-left bank, left to right), 28, 29, 30 (right bank, top to bottom). Each target holds its switch closed while down.
- 33 outhole, 34 right and 35 left outlane (5,000 each in the ROM), 36 right and 37 left star roll-over buttons (the ROM scored 4,000 for the first closure of 36, 2,000 for 37).
- Cabinet flipper buttons are public 82 (lower right) and 84 (lower left), declared by the Stern VPinMAME library; 81 and 83 are the generic upper-flipper positions and do nothing on this game. Each lower flipper's end-of-stroke contact is hard-wired, closed at rest, and is not a PinMAME address (the controller profile lists them as the two direct contacts).

**Switches 19 and 20 are an open conflict.** The matrix prints 19 as SCORPIO and 20 as LIBRA, and the factory switch drawing puts 20 at the left end of the upper-right arch with 19 beside it. The ROM, though, lights the Libra lamp (public 2) when 19 closes and the Scorpio lamp (public 18) when 20 closes, the retained table puts 19 left of 20 beside the Libra constellation, and the playfield art puts each sign's lamp insert beside its target. The record follows the ROM for the sign association and keeps both targets' provenance `conflicted` and their placements `observed` (the callout check below does not cover them). A recreation should pair each target with the lamp the ROM lights for its switch; which of the two stands further left is the part nobody here can settle, since the ROM and table are consistent with each other and so are the two manual pages. A switch test on a production machine, or a playfield photograph that shows which sign is printed beside the apex target, would settle it.

## Flippers, relay, general illumination, coin lockout

- The lower flipper circuits are hard-wired, dual-winding J-25-475/34-4500 assemblies on the 43 V solenoid supply. The cabinet button, not a driver transistor, switches each flipper, and the **flipper enable relay (public 19)** gates both. The ROM raises it when a credit starts a game, holds it until game over, drops it on a tilt and raises it again when the next ball is served; in attract mode the buttons do nothing. PinMAME publishes the generic flipper callbacks 46 (right) and 48 (left); it also sets 45 and 47 (`sLRFlipPow` and `sLLFlipPow`) in the same press, fabricating both bits together for a cabinet-wired flipper. Only 46 and 48 are addressable outputs in the controller profile, and no source here says which physical winding 45 or 47 stands for.
- The manual's solenoid list prints the relay's position as ENABLE REPLAY; the schematic names the load wired there the flipper enable relay. The ROM behaviour is the relay's, so the label here is the schematic's.
- Public 18 is the **coin lockout** coil, energized from power-up through attract mode and game over, as the manual says. The knocker is public 6; the retained ROM never fired it in the gameplay probes, so its address rests on the burn-in test order, the manual and the table's callback.
- There is **no general-illumination output**. The schematics draw one general-illumination lamp supply (`GEN. ILLUM`, 6 VAC on A2J1-8 with return A2J1-1) and no relay or driver in it, and PinMAME publishes no GI string. The retained table switches its own GI on two seconds after start for display purposes only. Treat the playfield general illumination as always on.
- Five momentary positions (public 9, 10, 13, 14 and 15) and two continuous ones (17 and 20) are wired but fitted with nothing: the manual's solenoid list prints them OPEN, the parts list names no coil for them, and the burn-in test fires them as part of its sweep. The schematic labels the public-20 load `BALL KICKER`; the manual and the parts list disagree, so it stays unused.

## Lamps

Fifty-nine lamp circuits are fitted and one (public 15, `Q6`) is not. The playfield carries, among others: the twelve zodiac sign inserts; bonus inserts 1K to 12K in the star ring plus 12,000 and 24,000; the eight spinner-and-bank value inserts; the four zodiac target value lamps (1000 to 4000); the 1X to 4X multiplier column; left and right outlane lites; the left-bank (extra ball) and right-bank (special) lites; two spinner lites; and the star roll-over lane arrows, whose four lamps (public 9, 25, 41, 57) the table lights in both lower lanes (the chart gives no bulb counts, so no quantity is stated). Shoot Again (public 11) is one SCR reaching two connector pins, which the table treats as a playfield insert and a backglass reel it reads from the lamp; no bulb count is stated. High score, game over, tilt and match are backglass lamps.

**Two circuits have no retained location.** The chart lists "L. B 1" (public 31) and "L. B 3 STAR ROLL" (public 47), the retained table binds no light to them, and in play the ROM flashes 31 in lockstep with 9 and 47 with 41, which suggests they are the opposite-side bulbs of two lane arrows. Nothing retained shows where they sit, so they are enumerated, named and wired but carry no placement.

## Spatial evidence

Placements come from the retained VPW table's objects, normalized to its playfield bounds (see the geometry excerpt for the exact object behind each address and for the lamp lights). The 57 table lights all lie in dark insert holes of the table's embedded playfield scan, which shows each sits on an insert but cannot tell same-sized inserts apart. The art identifies the socket of 22 lamp numbers by itself (the twelve signs by their constellation drawings, the eight spinner-and-bank values by their printed 500 to 4000, and the two captioned lites, extra ball and special), and those placements are `validated`; every other lamp placement rests on the table's light-to-lamp-number binding alone and stays `observed`. The switch and coil placements were checked against the manual's two factory location drawings (switch drawing PDF 19, solenoid drawing PDF 21) with `tools/drawing_callouts.py`: every number on each drawing was read independently from gridded tiles of the retained render, the controls were the three bumper rings and the two flipper pivots, and a placement validates when its own callout lands within 0.07 normalized under both fits. Thirty-five of the forty-two checked placements validate. The seven that do not stay `observed`: the outhole switch and the outhole kicker (the drawing prints 33 and 10 in open space between the flippers, while the table's drain hole is right of centre, as the playfield art's outhole slot is), the two flipper coils (the drawing prints 15 beside, not on, each flipper), the left slingshot coil, and the left and right drop-bank reset coils, which sit on a hidden assembly behind each bank and are projected onto the bank's middle target. The left slingshot switch (16) is unchecked because the switch drawing prints no number there, and the end-of-stroke contacts are unchecked because no drawing numbers them.

## Mechanisms and ball path

- **One ball, no trough.** The ball drains into the outhole between the flipper bays (switch 33), the ROM scores the bonus, and the outhole kicker (public 12) kicks it to the shooter lane, where the player launches it with the plunger. A credit with the ball waiting kicks it at once and resets all three drop banks in the same moment.
- **Three drop banks**, each with a single shared reset coil (public 7 for the lower-left bank, public 3 for the upper-left bank, public 4 for the right bank, called LEFT DROP TARGET, TOP DROP BANK and RIGHT DROP BANK by the manual). Completing a bank fires its reset after a short pause; the retained ROM pulsed it several times. Hitting a target of the upper-left bank stops the flashing value lite and fixes the centre spinner's value; completing the lower-left or the right bank advances the bonus multiplier (to 10x); the lower-left bank's middle target scores the extra ball when lit; the right bank scores the special when lit.
- **Bumpers and slingshots.** The ROM fires each coil from its own switch: 12 fires public 5, 13 fires 11, 14 fires 8; 15 fires 1 and 16 fires 2 (the reversed-looking pairs are the ROM's own and confirmed one switch at a time).
- **Tilt.** Closing public 7 in play dropped public 19 in the retained run; flippers and the centre bumper then did nothing until the ball drained and the next ball was served.

## Displays and sound

Four seven-digit player displays (controller indices 0 to 3, segment starts 1, 9, 17 and 25), a two-digit credits display (index 4, start 35) and a two-digit ball-in-play and match display (index 5, start 38). The manual's self-test text describes six-digit counts, but its attract description counts digits `1` to `7` and its recommended high-score levels reach 9,990,000, and the ROM's player displays have seven positions; the definition follows the seven. Sound is the Stern ST300 board and adds no playfield devices.

## Recreation checklist

- Build every address in the definition, including the seven wired-but-unfitted solenoid positions and public lamp 15, and keep printed numbers as aliases of the public addresses.
- One ball, outhole at the bottom centre feeding a shooter lane; three drop banks with one reset coil each, raised at game start and after completion.
- Flippers are cabinet-wired and gated by the enable relay; do not model a separate flipper driver.
- No general-illumination control: playfield GI is always on.
- Zodiac targets light the sign lamp the ROM pairs with their switch; keep 19 and 20 paired by the ROM until the conflict is resolved.
- Keep lamps 31 and 47 enumerated; place them only once a source shows where they sit.

## Sources

- IPDB 2346 (retained Internet Archive capture of the machine page) and the IPDB-hosted Stern manual and schematic scans: the manual is image-only, so every excerpt is a transcription read from the rendered page, with the printed numbers, wire colours and connector pins as printed, and a crop of the drawing where the fact is a drawing.
- The retained known-working VPX table (VPW v2.0.0), its pinned script and the retained Stern and core VPinMAME libraries.
- Runtime evidence: ten isolated LibPinMAME harness runs (burn-in on all three drivers, the solenoid test, the switch test over all forty addresses, and gameplay probes of coils, zodiac lamps, flippers, idle lamps and tilt), summarized in `evidence/runtime/by35/star-gazer-1980-harness.json`; raw runs, scenarios and hashes are listed there and ROM bytes stay external.
- Pinned PinMAME source (`stgames.c`, `by35.c`, `by35.h`) for the driver declarations, the seven-digit layout, the lamp strobe and the cabinet-port rewrite.
