# The Flintstones (Williams 1994)

Coverage: **partial**. Every address is enumerated and named, and construction, polarity, mechanism
and variant facts are validated from the factory operations manual, its two service bulletins, the game
ROM's own name tables, pinned PinMAME and the retained known-working table, and no conflict is open. It
stays partial on spatial placement alone: every coordinate comes from one community table and none was
checked against the manual's location drawings; the playfield flashers have no socket coordinate; the
left up/down gate's drawing callout and the table's gate disagree; and no G.I. string is placed.

## Identity and drivers

- Williams Electronics Games, model 50029, July 1994, 4,779 units (IPDB 888, OPDB `GRK95-MQ674`).
  WPC-Security (WPC-S) hardware, a 128x32 DMD, three flippers and an automatic plunger.
- PinMAME drivers, all declared in `src/wpc/sims/wpc/prelim/fs.c` with the `wpc_mSecurityS` machine
  driver and sharing one `fsGameData`, so every public address is the same:
  - `fs_lx5` (parent), `fs_lx4`, `fs_lx3` and `fs_lx2`: Williams production revisions, recorded
    identical. The LX-4 and LX-2 game ROMs decode to the same name tables as LX-5.
  - `fs_la5`: a Williams LA-5 game ROM. No retained source says what distinguishes it, so it is
    recorded compatible.
  - `fs_sp2`: the LX-5 game ROM with the SP-2 sound ROM `su2-sp2.rom`, which `fs.c` comments
    `// Prototype Sound ??`. Compatible.
  - `fs_dx5`, `fs_dx4`, `fs_dx2` and `fs_sp2d`: community "LED Ghost Fix" modifications of the LX game
    ROMs for machines converted to LEDs. They run on the physical machine but are not Williams
    releases, so they are recorded compatible.

## Evidence used

- The July 1994 operations manual 16-50029-101 (IPDB's "English Manual", 150 pages, image-only 300 dpi
  scan), retrieved from the Internet Archive's capture of the IPDB file because IPDB is
  Cloudflare-gated. A local Windows OCR text layer helped find pages; every cited cell was read from the
  render. Printed page 1-N is PDF page N + 23, 2-N is N + 65 and 3-N is N + 114.
- Ball Hang-up Correction Instructions 16-9872 (August 4, 1994): remove the washers on the posts at both
  sides of the bottom arch (03-9068) to stop balls hanging up there.
- Manual Amendment 16-9876 (August 10, 1994): the A-17932 diverter drawing calls the A-17986 bell
  armature item 9 instead of item 6. A third amendment on the same IPDB page, 16-9875 (August 9, 1994),
  only adds a trademark notice and carries nothing a recreation needs.
- The game ROM's English switch, Fliptronic switch, coil, flasher, G.I. and lamp name tables, decoded by
  `tools/flintstones_rom_name_tables.py` from the LX-5, LX-4, LX-2 and SP-2 sets, which decode
  identically. The decoded tables are in the excerpt `rom-name-tables.md`.
- Pinned PinMAME `fs.c`, `wpc.c` and `core.c`.
- The retained known-working table "The Flintstones (Williams 1994) v1.25.7" (g5k, 3rdAxis and DJRobX)
  and its script, and, as corroboration from the same lineage, the corpus script v1.25.8.

## Controller facts a recreation needs

- Switch matrix 11-78, sequential WPC column-times-ten addressing; 57, 58 and column 8 (81-88) are not
  used. Dedicated coin-door inputs D1-D8 are public 1-8.
- Optos: the trough (31-35), the popper (36), the 4-bank drop targets (41-44) and the 3-bank drop
  targets (45-47). `fsGameData`'s inverted-switch mask (`0x3f` for column 3, `0x7f` for column 4)
  normalizes exactly these thirteen, so every public switch is already normalized; do not invert again.
- Trough Jam is **31** and Trough 1-4 are **32-35**, as the ROM's switch table, `fs.c` and the script
  all agree. The printed matrix and switch list name 31-34 "Trough #1-#4" and 35 "Trough Jam".
- Each of 51, 52 and 53 is two standup targets, one in each side 3-bank, wired to one address. 51 is
  the upper pair and 53 the lower pair (the ROM pairs them with lamps 52, 63 and 64); the printed
  matrix and switch list reverse that.
- Switch 12 is the optional ticket dispenser input, printed Not Used.
- Fliptronic column: 111, 113 and 115 are the end-of-stroke leaves of the lower right, lower left and
  upper right flippers, which PinMAME recomputes from the coils every update (do not drive them);
  112, 114 and 116 are the cabinet flipper optos. The right cabinet button's opto board breaks both
  F2 (112) and F6 (116), so one press fires both right flippers and a host must drive 112 and 116
  together. 117 and 118 are not fitted.
- Solenoids 1-16 are coils. 17-22 and 24-28 are flashers; 17-21 also light two #906 insert flashers
  in the backbox, and 26 and 27 are backbox-only. **23 is the Boulder Machine motor**, not a lamp.
- 33/34 are the upper right flipper, synthesized like the lower flippers because `FLIP_SOL` covers
  `FLIP_UR`. **35 and 36 are the right and left up/down gates**, on the power and hold transistors of
  the Fliptronic upper-left circuit and published raw. The lower flippers are 45-48 (odd power, even
  power-or-hold).
- 29-31 carry WPC state (31 is game-on, since `fs.c` sets no fast-flip address); 32, 37-44, 49 and 50
  are dead or reserved. The manual prints rows `37*` to `44*` as Not Used with transistors but no
  connections.
- 64 lamp positions, all fitted. 87 and 88 are the cabinet Buy-In and Start buttons. Six lamps (41, 52,
  63, 64, 72 and 86) light one insert on each side of the playfield and carry two bulbs each.
- Five G.I. strings, each switched by a triac on its return pin, with the White-colour pin as the
  6.8 Vac feed. Strings 2-4 feed #44 playfield bulbs on J121 and #555 backbox bulbs on J120.
  - String 1, Machine Lighting, is recorded as a playfield string (J121-7 / J121-1), as the power driver
    board connector list wires it; the retained script lights the Boulder Machine with it. The solenoid
    table prints it on the backbox connector instead.
  - String 5, Lower Playfield & Insert Panel, is recorded from the solenoid table: playfield J121-11 /
    J121-6 and cabinet J119-1 / J119-3. The connector list instead marks the playfield pins N/C and
    sends the pair to the backbox and the coin door board.
- The lamp matrix prints its rows on J134 and its columns on J137; the connector list puts them on J133
  and J138, with rows 6-8 and column 8 also reaching the cabinet on J135 and J136.

## Mechanisms

### Trough and launch

Four balls sit in the A-18753 outhole trough on optos 32 (Trough 1, at the eject end) to 35; Trough Jam
(31) is a fifth LED and phototransistor pair. All five pairs sit on the trough's LED and transistor
boards, wired through the A-15576 7-opto switch board, which also carries the popper opto. Solenoid 1
kicks ball 1 into the shooter lane (15). Solenoid 2, the autoplunger, launches it when the player
presses Launch (11) or automatically after adjustment A.2 05 Seconds Before Autofire. Adjustment A.2 17
Flipper Plunger lets the right flipper button launch when the launch button is broken. There is no
manual plunger. The retained script pulses 31 on every eject; treat that as a table stand-in, not a jam.

### Top popper and the Boulder Machine

The popper (A-15769-1, solenoid 4, opto 36) at the rear left pops the ball up. Per the shot
maps, the upper lanes feed it when MACHINE TIME, START MULTI-BALL or BRONTO CRANE is lit.

The Boulder Machine (A-17978, on the A-18823 back panel in the upper left corner) is a wheel (A-18135)
turned by a 14-7999 motor. Solenoid 23 switches it through the A-15542 Motor EMI board, fed +12V from
J118-2. A ball reaches it from the upper right lane past Machine Enter (76) and leaves past Machine Exit
(25), an A-19098 exit switch on the assembly. Flasher 24 lights it, and G.I. string 1 lights its
surroundings. The rules call it the Rock Slicer Machine: shooting the lit Dicta-Bird target starts its
MACHINE TIME scoring round. The T.14 Machine Test turns the motor on. Wheel speed and timing are not
printed and are table-owned; the retained script runs it as a clockwise turntable and briefly blocks
the exit at some wheel angles.

### Drop targets

- B-E-D: the A-16032-1 3-bank on the left, with B (47) at the rear and D (45) at the front, read by
  the optos of the A-13609 board and reset by solenoid 5.
- R-O-C-K: the A-18188 4-bank in the centre, angled from R (41) at the rear left to K (44) at the front
  right, read by the optos of the A-19103 board and reset by solenoid 6.
- Completing either bank adds a CONCRETE letter (lamps 31-38); completing CONCRETE lights START
  MULTI-BALL. The BEDROCK mystery mode awards 100 million for completing both banks.

### Diverters and gates

None of these has a position switch.

- Top Diverter Post (3, A-17932): a post on a bell armature at the rear beside the popper. The script
  makes it collidable while the coil is on.
- Top Diverter (8, A-18369): the back diverter 01-12803 on the A-18823 back panel, beside the 03-9131
  back panel diverter guide; the ROM calls it BACKPANEL DIVRTR. The script swings it as a flipper
  object.
- Lower Left and Lower Right Diverters (15, 16, A-19097-2 and -1): at the top of the outlane and return
  lane dividers, just below the Drain Save lamps (41). Completing either side 3-bank lights DRAIN SAVE
  for a timed period (adjustment A.2 10, factory 5 seconds). The ROM's coil test calls them ramp
  diverters.
- Right and Left Up/Down Gates (35, 36, A-17796): ball gates at the rear. The script lets the ball pass
  while the coil is on.

### Dicta-Bird

The A-18078 assembly on the left side drives the Dicta-Bird figure (solenoid 14) on the A-18079 perch
bracket, beside the Dicta-Bird target (56). The lit target starts MACHINE TIME, lights BARNEY'S JOB
CHANGE or starts SEARCH AND RESCUE. The figure's travel is table-owned.

### Bowl-O-Rama targets, jets, slingshots and flippers

- The upper 3-bank of bowling targets (16-18) at the upper left: after a lit GO BOWLING ramp, the
  centre target scores a strike and either end target a spare. Three strikes in a row start Bowl-O-Rama
  multiball.
- Three jets below the D-I-G rollovers (66-68): top left (coil 11, switch 63), bottom (12, 65) and top
  right (13, 64). The printed table calls 11-13 Left, Middle and Right.
- The slingshots each carry a kick and a score switch on one address.
- Three Fliptronic flippers with blue FL-11629 coils.

## Manual discrepancies worth knowing

- Rows 4 and 5 of the switch matrix both print `J209-4`; the trough and drop-target board pages put row
  5 on J209-5.
- All three copies of the lamp matrix print column 4 on `J137-5`, the same pin as column 5.
- The switch list prints item 18 twice and no item 17, for the upper 3-bank.
- The solenoid/flasher location list prints A-18825 and A-18812 for the drop-target reset coils; the
  assembly pages are A-16032-1 and A-18188.
- The note under the 3-5 solenoid table says the upper **right** flipper circuit drives the up/down
  gates; the table and the flipper circuit page put them on the upper left circuit.
- The flipper circuit pages print the F2 and F6 wire colours the reverse of the switch matrix, and the
  2-42 matrix copy prints F4 on `J906-2` instead of `J905-2`.
- The flashlamp wiring page draws solenoid 28 on J122-2; the table prints J122-4.
- The flipper coil circuit schematic (3-12) draws the right flipper with the left circuit's J902 pins
  9, 7, 3 and 1; the table and the 3-11 page give 13/11 for the lower right and 6/4 for the upper right.
- The power driver board connector list labels J124-2, solenoid 26's Blue-Red drive, "sol. 25".
- The solenoid table types flasher 17 "Low Power".
- The A-15542 Motor EMI board's connector list names the J2-1 motor wire White; the circuit diagram on
  the same page labels it BLK.
- The popper assembly list prints its part numbers beside the wrong descriptions (A-16909 beside the
  bracket, A-16908 beside a screw).
- Pinned `wpc.c` types every flasher as a #89 bulb for its brightness model; the manual prints #906 for
  19, 26, 27 and 28, for one bulb of 22 and for the backbox inserts of 17-21.

## What would complete the record

A callout check of the manual's switch, lamp and solenoid location drawings against the table's
coordinates, which would promote the placements from observed to validated; socket positions for
flashers 17-22, 24, 25 and 28; a settled position for the left up/down gate (36), whose drawing callout
ends near the Boulder Machine while the retained table's gate sits about a third of the playfield to the
right; and per-string G.I. bulb positions.
