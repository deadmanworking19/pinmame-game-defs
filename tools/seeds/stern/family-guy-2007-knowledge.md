# Family Guy (Stern, 2007)

Coverage: **partial - the complete public I/O inventory, factory wiring and parts and firmware family are recorded from the Stern service manual, the ROM's own service tests and pinned PinMAME; the Evil Monkey latch gate's behavior and the spatial placements the retained table cannot supply are still open.**

## Identity and evidence precedence

This is the 2007 Stern S.A.M. machine (IPDB 5219, model I-0093, OPDB `G5LW9-MQ6N5`, designed by Pat Lawlor) with a 128x32 dot-matrix display, five flippers (two lower, one upper left, two on the mini-playfield), three pop bumpers and the Stewie mini-playfield. All nineteen pinned `fg_*` drivers are firmware and language versions of this one machine: the clone tree PinMAME declares under `fg_1200ag` initializes them identically (`INITGAME(fg, GEN_SAM, sam_dmd128x32, SAM_8COL, SAM_GAME_FG)`), the factory manual lists one parts set, and the ROMs that were run print the same switch and lamp names. Service Bulletin 170 (February 2007) records that starting with this game the factory firmware limits North American machines to 60 Hz line voltage; that is firmware, not hardware.

Authority used: the January 2008 Stern service manual (v12.0 and later; Internet Archive item `Stern_Pinball_Family_Guy_Manual`, 170 pages) for physical construction, parts and wiring; the ROM's own switch, coil and lamp tests, run in the pinned LibPinMAME harness, for names and public addresses; pinned PinMAME `sam.c` for the emulator contract; the retained VPX table's embedded script only for controller-facing pulse/hold behaviour, because it is a reconstruction with defects (below). Neither the manual nor any retained table is a verified-working recreation of this machine's rules.

## What the ROM tests settle

On a fresh NVRAM the S.A.M. service menu is reached with the Back key and three Select presses (diagnostics menu), after which the switch, coil and lamp tests name every address:

- **Switches.** Holding public 1-64 in turn, the switch test prints the ROM's name and the drive/return wire colours for exactly the cells the manual prints and the generic `SWITCH #n` for the NOT USED cells (11, 12, 14, 17, 34, 36-38, 56, 58-63). The public number is the manual's printed number, and a held public 1 is the ROM's active reading, so the public matrix is active-high and no consumer inverts it: pinned PinMAME's `samswitch_r` (`sam.c`) complements the matrix word on its way to the CPU's active-low port. `physical.normally_closed` is therefore false for every matrix switch, including the optos (21, 22, 9, 44-47, 52-55), whose receiver output closes when the beam is blocked.
- **Dedicated switches.** The switch test names public 65-69 (coin slots 1-5), -7 (tilt), -6 (slam tilt), -5 (ticket notch) and the EOS pairs 81-88. Pinned `samswitch_r` copies the flipper button bits D-9, D-11, D-13 and D-15 into their EOS bits D-10, D-12, D-14 and D-16 as the CPU reads the dedicated word, so holding 81 or 82 names the right EOS (D-12), 83 or 84 the left EOS (D-10), 85 or 86 an upper-right EOS (D-16) and 87 or 88 an upper-left EOS (D-14). D-14 and D-16 are generic S.A.M. names for an EOS the upper flippers do not carry (the manual's upper-left flipper parts list prints a spacer where the lower flippers have the EOS switch), and the ROM also names D-7 and D-8 "L./R. POST SAVE" although the manual prints NOT USED. The EOS contacts D-10 and D-12 are normally closed per the manual (they open about 1/16 in. as the coil is energized); the core also rewrites the lower pair's public bits (83 and 81) from the flipper coil timers, so they rest at 0 whatever the contact does.
- **Coils.** The Single Coil Test steps Q1-Q19, Q21-Q23 and Q25-Q32 (it skips Q20, the Stewie stepper, and Q24), printing the name, power and control wire colours. Pressing Select fires the public solenoid whose number equals the transistor number for every one of them. The ROM prints the control wire BRN-BLK for Q3 where the manual's chart prints BRN-ORG; the structured wiring follows the manual's chart (a wiring-detail difference, not a disagreement about the device). Every firmware that was run before V12.0 (V3.00, V4.00, V8.00 and V11.0) also lists two optional ticket-dispenser auxiliary coils, `AUX 1: TICKET ADVANCE #33` and `AUX 3: TICKET ENABLE #35`, after Q32; firing them changes no public solenoid. They are recorded as two optional physical ticket outputs (`physical.output.ticket` 33 and 35, outputs of the backbox auxiliary driver PCB 520-5068-01 on manual pages 169-170), not as public solenoids: PinMAME publishes nothing for them, public 33 is the synthetic game-on state and 51-66 are unused compatibility addresses. The board has a third transistor (AUX 2, #34) that no retained source names.
- **Lamps.** Stepping the Single Lamp Test lights public lamp *n* at selector position *n* for all 80 positions, with the manual's names for 3-70 and `NOT USED #n` for 59, 60 and 71-80. The firmware versions that were run draw identical lamp-test frames.
- **Power-up.** The ROM pulses the Stewie stepper (public solenoid 20) at power-up, GI 0 comes on, six coins and Start produce the synthetic game-on state on solenoid 33 and pulse the trough up-kicker (Q1), and each coin pulses public solenoid 24 (the optional coin meter/knocker output).

## Ball transport

Four balls are required; they rest on trough switches 18-21 (21 is a dual-OPTO "VUK" beam at the up-kicker end, 22 the stacking beam above it). Q1 lifts the right-most ball into the shooter lane (switch 23); the player plunges with the ball shooter or Q2 fires the autoplunger. The mini-pinball (5/8 in.) sits in the mini-playfield trough (OPTO 55) and must be installed for the game to run. Treat each trough position as sustained occupancy and the up-kicker transaction as the only way a ball leaves the stack.

## Playfield mechanisms

The mechanisms and their addresses are enumerated in the definition. Their behavior as the factory documents it:

- **Ball saver (Death) post.** An up/down post between the lower flippers (assembly 500-7022-00) that keeps the ball from draining when energized. Q12 raises it, Q4 (the 32-1800 mini-coil of the latch assembly) lowers it, and blade switches 1 and 2 report up and down. The Death 1-bank drop target (OPTO switch 9, reset by Q6) raises the post per the instruction card. Lamp 69 is the post, lamp 18 "Raise Death".
- **Drop targets.** F-A-R-T 4-bank (OPTO switches 44-47, reset by Q3) and the Death 1-bank (switch 9, reset by Q6). A target holds its OPTO beam interrupted while down.
- **Ejects.** TV scoop (switch 13, Q13) and Clam eject (switch 64, Q5), both vertical up-kickers that kick the held ball out; the diodes of switches 13 and 64 are on playfield terminal strips (DOTS).
- **Evil Monkey latch gate.** The left ramp's latch gate has a trip coil (Q19, 32-1250) and a roller microswitch (35); switch 33 is the ramp exit's roll-under gate switch. The instruction card says the Chris target (switch 3) lowers the Evil Monkey target and that collecting five Evil Monkey awards starts Crazy Chris. In the harness the ROM fires Q19 repeatedly from game start while public 35 reads open and stops once it reads closed (it never fires Q19 when 35 starts closed), so closed is the state the ROM drives it toward; a Chris-target hit on the first ball fired the back-panel flasher Q27 and not Q19, and opening switch 35 afterwards did not make the ROM fire Q19 again within four seconds. The physical action of Q19 on the target and the release path the instruction card describes are not documented or observed.
- **Figures.** Stewie turns on a stepper motor (Q20, controller PCB 511-5045-00, no position switch; homed against a raised stop by the ROM's Stewie Motor Test) to face his mini-pinball machine; Meg bobs on a mini-coil (Q22); Brian's beer can is a spring-returned target (switch 49). Peter, Chris and Lois are fixed figures.
- **Stewie mini-playfield.** Mini-shooter Q21 serves the ball from mini-trough 55; mini orbits 52 and 53 and mini ramp 54 are OPTO pairs, stand-ups 50 (Meg) and 51 (Peter) are mechanical switches (earlier machines had piezo sensors), and Q17/Q18 are the mini-flippers, operated with the lower flipper buttons. Per the instruction card, spelling P-I-N-B-A-L-L with the captive-ball (Newton) rollovers 6 and 7 and then shooting the TV scoop starts Stewie Pinball on this playfield.
- **Flippers.** Lower flippers Q15/Q16 with EOS D-10/D-12 and buttons D-9/D-11; upper-left flipper Q14 on D-13 (a full press of the double-stacked left button). No upper-right flipper is fitted. The manual specifies a 40 ms kick at 50 VDC and then 1 ms pulses every 12 ms while the button is held.
- **Bumpers and slings.** Pop bumper coil/switch pairs: Q9 bottom with 32, Q10 right with 31, Q11 top with 30. Slings: Q7 left with 26, Q8 right with 27.

## Lighting

Lamp matrix 1-80 as the manual prints it (lamps 1 and 2 are the cabinet start and tournament-start buttons; 59, 60 and 71-80 are NOT USED; 61, 68 and 70 are above the playfield; 61 is a white LED module). Eight flashers are #89 bulbs on Q23 and Q25-Q32; Q25-Q27 are the back-panel flashers behind blue, red and clear covers.

General illumination is one aggregate public GI 0 (the G.I. relay), over four fused 5.7 VAC circuits: circuit 1 unused, circuit 2 (left-side spot lights), circuit 3 (back panel and coin door) and circuit 4 (right-side spot lights); bulb counts are production-dependent.

The mini-playfield LED board 520-5264-00 is separate from the lamp matrix: 22 LEDs spell BRIAN, CHRIS, LOIS, MEG and PETER. PinMAME publishes them as lamp outputs 81-128, six groups of eight of which 22 are fitted. The mapping below was read from the board schematic and agrees with the 22 addresses every swept firmware drives (V3.00, V4.00, V8.00, V11.0 and V12.0 publish exactly this set and nothing else above lamp 80):

| Name | Letters to public lamps |
| --- | --- |
| BRIAN | B 84, R 83, I 82, A 81, N 97 |
| CHRIS | C 125, H 124, R 123, I 122, S 121 |
| LOIS | L 108, O 107, I 106, S 105 |
| MEG | M 98, E 99, G 100 |
| PETER | P 114, E 89, T 90, E 91, R 92 |

## Spatial placement

Placements are the stored centres of the retained table's objects, normalized by the table's 952×2115 bounds. Where the table's script binds an object to a device in the wrong place, the device takes the object the manual's location drawings put it at (the pop bumpers: switch 30 and coil Q11 are the rear bumper, 31 and Q10 the right one, 32 and Q9 the front one that carries the white lamp-61 LED module). {CALLOUT_CHECK} Mini-playfield switches 50-55 and lamp 68 are drawn on the DR.5 and DR.7 insets, which the page fits do not cover, so they keep their table status. The coil and flasher page (DR.9, PDF page 11) was transcribed too, but its only top-down view is an inset cut off at the page edge that shows the three bumpers and nothing else a fit could use, so no coil or flasher placement is checked against a drawing. Missing: the trough sensors 18-22 and the back-panel flashers Q25-Q28 (no table objects), GI and the coil bodies (anchors are the mechanisms the coils drive).

## Retained table defects (not machine facts)

The retained VPX table (`Family Guy (Stern 2007).vpx`) is a reconstruction. Its `info.json` still names "Shrek (Stern 2008)" (a stale header), and its script differs from the factory manual in ways a recreation must not copy: the rear pop-bumper object is bound to switch 32 (the manual's bottom/front bumper) and the front object to 30; the LED lamps are labelled with the wrong names (lamps 81-84 and 97 as CHRIS where the board has BRIAN, and 121-125 as BRIAN where it has CHRIS); switch 35 is asserted from the Q19 callback; the ball saver post runs a timer of its own; and some playfield switches (for example 33, the ramp exit gate) are bound only through gate and kicker objects rather than a switch object of their own. These are table defects, noted on the devices, not disagreements about the machine.

## Variants

Firmware versions V3.00, V4.00, V8.00 and V11.0 were run against the same switch, coil and lamp sweeps as V12.0; every name and public address matches, except for the two optional auxiliary ticket coils that all four list and V12.0 drops (see above). `fg_200a` has no retained ROM and `fg_1200af`'s retained zip holds a different dump from the pinned CRC, so neither was run. The 2008-and-later production run replaced the mini-playfield stand-up piezo sensor PCB on switches 50 and 51 with mechanical switches (manual note, PDF page 115); the public addresses are the same.

## What remains

- Spatial placement (`spatial_placement`) is incomplete: see the section below. No GI string, the trough sensors 18-22 or the back-panel flashers Q25-Q28 have a placement.
- The Evil Monkey latch gate: what Q19 does to the target physically and which game event releases it. A harness run that reaches the Evil Monkey award on a modelled ball, or a photograph or teardown of the assembly, would settle it (`mechanism_behavior`).

## Sources

- Service manual `FG_FIND_IT_IN_FRONT.pdf`, SHA-256 `2bbcfa34ad70ab90c0fadabaf825850cecae58c8028af9aaabf8be1ad01979cd`; transcribed excerpts under `evidence/excerpts/stern.family-guy.2007/`.
- Service Bulletin 170, SHA-256 `b26b97f9117513b44b78dbfc1c6e32aa7cb762313a7e6b836a512fbbf629ece0`.
- Retained table `Family Guy (Stern 2007).vpx`, SHA-256 `159558a39efd5a784bf0e587e9f07563e4fcd92765eeda02c9abc8bad015e2ff`, embedded script SHA-256 `c7b201acb74a329913b159db88315c422b8dcead0ba4bb30b61785ed1785f8db`.
- Runtime summaries `evidence/runtime/sam/family-guy-*.json`, each tied to its sealed raw run and the pinned native library.
