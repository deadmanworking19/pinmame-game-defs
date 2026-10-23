# Bram Stoker's Dracula (Williams, 1993)

Coverage: **partial** on one count, an unresolved conflict over flasher 19's playfield bulb
count (`conflict.flasher-19-playfield-bulb-count`, see Flashers). Every other dimension is
validated, and every placement the manual's factory location drawings can check is checked
against them (see Spatial checks for the exclusions and measurements). One
wiring disagreement about solenoids 33-36 is recorded as an ignored conflict
(`conflict.upper-flipper-circuit-side-naming`), because it cannot change a recreation. See
`reports/spatial/williams/bram-stoker-s-dracula-1993.md` for the full audit.

## Overview

Bram Stoker's Dracula is a Williams WPC-Fliptronic machine (`GEN_WPCFLIPTRON`,
`PINMAME_HARDWARE_GEN_WPCFLIPTRON = 0x8`), designed around the 1992 Francis Ford Coppola
film. The physical family is the five-driver `drac_*` clone tree: `drac_l1` (production
parent, and the driver the retained known-working script binds directly via
`Const cGameName = "drac_l1"`), `drac_d1` (D-1 LED Ghost Fix), `drac_l2c` (2016 community
Competition MOD), and two prototype revisions `drac_p11`/`drac_p12`. All five share one
static `dracGameData` struct, so all five are physically identical.

This is the fourth WPC-Fliptronic game curated in this project (after Bally Twilight
Zone, Bally The Addams Family, and — via the WPC-DCS variant — Williams Indiana Jones and
Williams Star Trek: The Next Generation), reusing `controllers/pinmame/wpc-fliptronic.json`
unchanged. Its switch-matrix opto sweep found **zero disagreement** with pinned PinMAME
across all three affected columns (5, 7, and 8) — the cleanest sweep result of any
Fliptronic-generation game curated so far, matching the clean-sweep precedent already set
by Bally Kiss, Bally The Addams Family, and Williams Star Trek: The Next Generation.

## Physical devices

Switch, lamp/GI, and controlled-device records are in the adjacent machine definition
(`machines/partial/williams/bram-stoker-s-dracula-1993.json`). The full manual
transcription is retained at `external:pinmame-review-artifacts/dracula/manual-
transcription.md`, and per-table excerpts are committed at
`evidence/excerpts/williams.bram-stoker-s-dracula.1993/`.

### Switch matrix opto identity

Unlike most other curated WPC manuals, this one marks opto construction by writing
"Opto ___" directly into the printed switch-matrix cell rather than shading. Column 5's
seven "Opto ___" cells (51-57) and column 7's three "Opto ___" cells (71-73) match
pinned PinMAME's inverted-switch mask exactly (`0x7f` and `0x07` respectively). Column
8's single opto (switch 82, "Ball On Magnet") cannot be determined from the matrix page
at all — none of 81/82/83 is labelled "Opto" there — and is only resolvable from the
Switch Locations parts list, where 82 alone carries genuine A-14315(LED)+A-14316(Trans)
construction while 81 and 83 use the ordinary leaf part 5647-12693-14. This again matches
PinMAME's mask (`0x02`, row 2 only) exactly. Zero disagreement anywhere in the matrix.

### No physical upper flippers

Three independent sources converge on "no upper flippers fitted": the Switch Locations
parts list has no row at all for Fliptronic positions F5-F8 (unlike F1-F4, which each
carry a real part number); the Solenoid/Flasher Table lists only two flipper-coil rows
("Lower Left Flipper", "Lower Right Flipper" — no "Upper" row at all); and the retained
known-working script never references public switches 115-118 anywhere. The generic
Fliptronic II circuit-diagram pages (3-17 through 3-21) still print all eight F1-F8
positions descriptively and pinned PinMAME's own `dracGameData` sets
`FLIP_SW(FLIP_L | FLIP_U)` (reading both lower and upper button state) despite
`FLIP_SOL(FLIP_L)` (declaring only lower-flipper coils) — the same "board reads upper
positions with no upper coil ever installed" pattern already established for Monster
Bash's `mbGameData`. This is a known WPC-Fliptronic driver characteristic, not evidence of
real upper-flipper hardware.

### Repurposed upper-flipper circuits

Because there are no upper-flipper coils, solenoids 33-36 (the Fliptronic II board's
upper-flipper power/hold driver-transistor pairs) are repurposed for four unrelated devices:
33 Up/Down Post Diverter, 34 Right Gate, 35 Castle Release Post, 36 Left Gate Actuator — the
same pattern already established for Indiana Jones's printed circuits 33-36 (right-ramp
diverter and Top Lockup post) and Monster Bash's repurposed Fliptronic switch position.

Which circuit each address drives is settled by the board, not by this manual. Pinned
PinMAME's `src/wpc/core.h` (`sURFlipPow`/`sURFlip` = 33/34, `sULFlipPow`/`sULFlip` = 35/36)
and the controller profile put 33/34 on the upper-**right** circuit and 35/36 on the
upper-**left** one. Twilight Zone proves it at runtime on the same board generation: its
known-working script drives the upper-right flipper from `SolCallback(sURFlipper)` (core.vbs
constant 34) and its manual wires that flipper on Q2/Q7 (J902-6/J902-4). Twelve other
Fliptronic II and WPC-95 solenoid tables in this repository that number these rows (Star Trek:
The Next Generation, Demolition Man, The Shadow, Theatre of Magic, World Cup Soccer, Corvette,
Indianapolis 500, Johnny Mnemonic, Jack*Bot, Dirty Harry, Doctor Who, WHO dunnit) put 33/34 on
J902-6/J902-4 and 35/36 on J902-3/J902-1. Their transistor columns agree too, except The Shadow's
main table, which prints Q2 and Q7 beside J902-3 and J902-1 on its 35/36 rows while its own
flipper rows print Q1 and Q5 for those pins; `fliptronic-ii-upper-circuits.md` quotes every row.
This manual's 3-8 table is the outlier: it pairs 33/34
with "Up Lt. F." (Q1/Q5, J902-3/J902-1) and 35/36 with "Up Rt. F." (Q2/Q7, J902-6/J902-4),
while its own 3-18 Fliptronic II Flipper Circuits page draws those pins on the sides the table's
labels say. The function column, PinMAME's `drac.c` (`sTopDiverter` 33, `sRGate` 34,
`sCastleRelease` 35, `sLGate` 36) and the retained script's `SolCallback(33)`-`(36)` agree on
every device and address, so nothing a recreation consumes is in doubt. Under the runbook's
wiring-detail rule the structured wiring follows the board mapping, with this machine's own
pin, wire colour and voltage pin for that circuit: 33 Q2/J902-6/Blk-Yel, 34 Q7/J902-4/Org-Vio,
35 Q1/J902-3/Blk-Blu, 36 Q5/J902-1/Org-Gry. The printed rows stay verbatim in the excerpt, and
`conflict.upper-flipper-circuit-side-naming` stays recorded as ignored.

The lower flippers' 3-8 rows print one merged drive cell per flipper (`J902-7,9`,
`J902-11,13`) with a power and a hold wire colour; the 3-18 page gives each colour its pin, so
the power windings are on J902-9 (Blue-Gray, 47) and J902-13 (Blue-Violet, 45) and the holding
windings on J902-7 (Orange-Blue, 48) and J902-11 (Orange-Green, 46). All of 33-36 and 45-48 are
Fliptronic II board circuits.

## Custom mechanisms

### Mist Magnet ball-levitation carriage

The headline mechanism. A single electromagnet (solenoid 27, "Magnet") is mounted on a
motor-driven carriage (solenoid 28, "Magnet's Motor") that travels diagonally beneath
the playfield between a right-side entry near the Right Gate and a left-side exit near
the Left Gate. The manual's A-16266 Coil Magnet & Screw Assembly page (printed 2-27) shows
the carrier riding a reversing screw, with the 20-9831 coil magnet on its bracket and, beside
it, an A-16205 light socket and bulb, both reaching the machine through a coiled cable. The
retained script tracks the carriage's position purely in software: a 0-500 counter
(`MagnetPos`) increments or decrements by 0.4 per tick while solenoid 28 is energized,
reversing direction at each endpoint (`MagnetDir`), and `SetMagnetPosition` puts the carriage
at x = 850 - 739 * MagnetPos / 500 on y = -0.44 x + 1238, from raw (850, 864) to
(111, 1189.16). The carriage therefore has no single resting coordinate. Solenoids 27 and 28
are projected onto the area centroid of the table's `Trigger.Magnet` zone, a thin band along
the track (raw (464.13, 1035.17)); the zone's stored centre, raw (390, 1000), lies outside that
band and is not used.

### The Magnet lamp rides on the carrier

Lamp 53 (Magnet, #44) is the bulb on the carrier. The game story at the front of the manual
says: "When certain shots are made a ball is transported across the playfield by means of a
magnet under the board. A light also moves in unison with the magnet. The playfield art in
that area is a 'mist' and when the light and ball move it seems that the ball is floating in
the 'mist'." The Lamp Locations drawing (printed 2-44) prints balloon 53 with no leader at the
left end of a diagonal row of thirteen small round inserts, beside a free-standing arrow that
points along the row, the path the carrier runs under; production playfield photographs show
the green mist art along that path and no arrow insert. The Lamp Locations list prints lamp
assembly A-11905 for this lamp and the magnet assembly page A-16205 for the socket, two
socket-and-bulb part numbers for the one bulb.

The bulb lights the inserts from below as the carrier moves, so a recreation should move a
light along the row with the carriage and switch it from lamp 53. The retained VPW table does
something simpler: it never reads lamp 53, and `MotorTimer_Timer` steps thirteen fixed lights
(`ml1`-`ml13`, one under each insert) from `MagnetPos \ 33` whenever solenoid 28 runs. The
placement projects the lamp onto `ml7`, the middle of that row, raw (464.91, 1119.45); the
row runs about 0.04 normalized below the carriage line, beside the ball's path.

Three switches report the mechanism's state, and only one of them is a true opto:

- **Switch 82 (Ball On Magnet, opto)**: the retained script's `MistTimer_Timer` tests
  every ball in the trigger's collision region against a fixed diagonal line equation
  representing the physical light beam, independent of carriage position; its comment gives
  the line's ends as (126, 1220) and (870, 885). This is the only genuinely opto-constructed
  magnet-area switch (A-14315/A-14316), and it is the only one PinMAME's inverted-switch mask
  normalizes. The switch drawing (printed 2-46) runs callout 82's leader the length of the
  path to a dot at its left end, 0.002 normalized from the beam line's left end, where the
  switch is placed.
- **Switch 81 (Magnet Left, plain leaf, part 5647-12693-14)**: asserts when
  `MagnetPos > 490`, i.e. the carriage is near its left/exit end, which feeds the Left
  Gate. It is placed at that end of travel, raw (111, 1189.16); the switch drawing prints
  balloon 81, tagged (Under Playfield), beside the left end of the path with no leader.
- **Switch 83 (Magnet Right, plain leaf, same part)**: asserts when `MagnetPos < 10`,
  i.e. the carriage is near its right/entry end, which feeds the Right Gate. It is placed at
  that end of travel, raw (850, 864), where the switch drawing ends callout 83's leader.

The driver's own `stMagnet` ball-state case requires the magnet to be both energized
(`core_getSol(sMagnet)`) and at the matching endpoint switch/position before releasing
the ball toward the corresponding gate — an explicit causal link between the magnet coil,
the motor position, and the two endpoint limit switches, not merely proximity.

The thirteen "mist lights" (`ml1`-`ml13`) have no PinMAME public address of their own and
are not modeled as controller-facing lamp devices; they are the table's stand-in for lamp
53's moving bulb (see above).

### Castle Lock lane and release post

A three-position lock lane behind the Left Ramp diverter queues balls on three genuine
opto switches: 57 (Castle Lock 3, entry, nearest the diverter), 54 (Castle Lock 2), and
53 (Castle Lock 1, exit, nearest the release post). Solenoid 35 (Castle Release Post,
printed "Dis. Castle Release Pst", driven through the Fliptronic II board's upper-left
flipper power circuit) retracts the post (`clpost.isdropped = 0`) to release the ball queued
at position 53 toward the shooter lane; the retained script's `clpost_Timer` sub restores
the post 280 ms later. The driver's own ball-state chain (`L. Ramp Div.` → `Castle Lock 3`
→ `Castle Lock 2` → `Castle Lock 1`, exit output `sCastleRelease`) confirms balls queue in
that order and release one at a time from the position nearest the post.

### Left and Right Mist Magnet entry gates

One-way gates admit a ball onto the Mist Magnet carriage from either side. Solenoid 34
(Right Gate, driven through the Fliptronic II board's upper-right flipper hold circuit)
opens a gate near the top-right loop (`RGate.open = 1`, plus dropping
`RGateWall`) so a ball can fall onto the carriage from the right; solenoid 36 (Left Gate
Actuator) opens a gate near the Magnet Left Pocket opto (switch 52) admitting a ball from
the left (`LGate.open = 1`, plus dropping `Wall_LO`). The driver's own ball-state chain
independently confirms both paths lead to `stMagnet`.

### Moving Right Ramp / Coffin Ramp section

A section of the Right Ramp raises and lowers to route the ball either up the ramp toward
the Coffin Popper or over a hump back into general play. Solenoid 14 (Right Ramp Up)
raises it, disables the ramp's own collision (letting the ball pass up and over), and sets
the retained script's `Controller.Switch(77) = True`; solenoid 4 (Right Ramp Down) does
the reverse. The Switch Locations parts list prints a real part number for switch 77
(5647-12693-36), but the retained script sets its public state directly from the solenoid
commands rather than reading a discrete position sensor — an implementation
simplification worth noting, not a source disagreement (all three sources agree the
switch and the solenoid-driven mechanism both genuinely exist).

### Shooter Ramp entry diverter

A small flap near the auto-plunger lane (solenoid 8, Shooter Ramp Entry) diverts the
auto-launched ball either up a habitrail loop toward the right side of the playfield
(solenoid energized, `sramp2.Collidable = 0`, `FLRamp.rotatetoend`) or lets it fall
through toward the Left Loop (solenoid off), per the driver's own `stBallLane` ball-state
case. No discrete switch reports this flap's position; the driver infers the routing
purely from the current solenoid state.

### Up/Down Post Diverter

A spring-loaded post near the top of the playfield (solenoid 33, printed "Up/Dn Post
Diverter", driven through the Fliptronic II board's upper-right flipper power circuit)
toggles the ball between two orbit/ramp paths (`wDivert.isdropped`, `FDivert.rotate`).
Left Ramp Entry (opto switch 73) senses a ball entering the diverted path.

### Single Left Drop Target

A single drop target — **not a bank** — sits near the top-left rollover lanes. Hitting it
drops the target (switch 15, L. Drop Target) and reveals a rollover behind it (switch 16,
L. Drop Score) that scores the ball's passage; solenoid 25 (L. Drop Target Reset) raises
it again after a delay via the retained script's `SolDTUp` callback. This corrects an
earlier candidate description of a "3-bank drop target" at this address: the retained
script instantiates exactly one `DropTarget` class object (`DT15`, `Set DT15 = (new
DropTarget)(sw15, sw15a, BM_sw15, 15, 0, false)`) for switch 15. The genuine 3-bank
standup-target arrays on this machine are the unrelated Left 3-bank (switches 66/67/68)
and Middle 3-bank (switches 86/87/88) banks, both plain standup targets with no drop
mechanism at all.

## Lamp chases

Seven lamps spell the machine's own name letter by letter: 48(D), 36(R), 23(A), 71(C),
67(U), 72(L), 82(A), in address order 48→36→23→71→67→72→82. Five more
(31-35) spell VIDEO in already-ascending address order, illuminating the "R. Lane" video
mode qualifier lamps in sequence.

## Flashers

Each flasher drives a playfield function and a backbox function, which the Flashlamp Wiring page
(printed 3-9) names separately: the first name in each 3-8 Solenoid/Flasher Table row (T.R. Corner,
Jackpot, 3-Bank's, T.L. Corner, Castle, L. Ramp, R. Ramp, Asylum) is the playfield flashlamp, on
J126 from supply J107-6, and the second (Dracula, Stoker, House, Mina, Helsing, L. Logo, R. Logo,
Renfield) is the backbox flashlamp, on J125 from supply J106-5. Flasher 26 (Speaker Panel) is
backbox only. Each quantity counts the playfield and backbox bulbs, and only the playfield bulbs
are placed.

Flasher 17 (T.R. Corner / Dracula) has three playfield bulbs and the solenoid drawing (printed
2-45) prints three callouts 17: one in the top right corner, at the retained table's `F17_Dome`,
and two arrows ending on either side of the coffin, where IPDB picture 12459 shows two blue domes
flanking a cross on the coffin's head piece. The table models only `F17_Dome` and drives it for
every bulb, so the two coffin domes are measured on the drawing.

Flasher 19 (3-Bank's / House) is the record's one open question. Its House bulb is in the
backbox. The solenoid drawing prints two callouts 19 on the playfield, one beside the middle
3-bank and one at the left edge behind the left 3-bank, and the retained known-working script
drives a light at each (`F19a`, `F19`); every other flasher's callouts match its 3-8 count. But
the 3-8 table prints `(1) #89` for the playfield function, and the Williams tech chart repeats it
(`#89(1)`). The record places both drawn sockets and counts three bulbs, and
`conflict.flasher-19-playfield-bulb-count` keeps the count unresolved. A table author should treat
the left 3-bank flash as possibly absent on a production machine. Settling it needs a production
machine: in the flasher test (T.5), watch whether the bulb behind the left 3-bank fires with the
one at the middle 3-bank when solenoid 19 is selected.

## Backbox and cabinet devices

Switch 34 (Launch Ball) is the cabinet launch button, not a plunger switch: its part
A-15896-1 is the Launch Ball button assembly that also carries lamp 87, the switch drawing
prints it below the playfield outline at the cabinet's right front corner, and PinMAME's
`drac.c` lists `swLaunch` among its cabinet switches. The retained script asserts it from the
plunger key.

## Playfield back panel

Four lamps (58 L. Ramp Diverted, 61 L. Skill 100K, 62 M. Skill 1 Million, 63 R. Skill) are on
the playfield's back panel, the upright panel standing at the rear edge of the playfield behind
the top lanes and ramps. The A-16399 Back Panel & Decal Assembly (printed 2-39) carries a
playfield plastic, the 3-lamp PCB A-16337-1 that holds the three skill-shot lamps 61-63, the
B-12224 single lamp assembly that holds lamp 58, and a single flashlamp assembly near each end.
The Lamp Locations drawing (printed 2-44) draws the four lamps only in an inset box of that
assembly above the playfield, spanning the drawn playfield's width: 61, 62 and 63 on three inserts
in a row, 58 on a round insert above and to their right. IPDB picture 12459 shows the panel's
plastic, lettered `SKILL S…`, behind the ramps. Each lamp takes the retained table's script-bound
light (`L61`, `L62`, `L63`, `l58`) on the playfield's rear edge, the panel's plane; through the
lamp drawing's control fit the centre of each lamp's insert symbol in the inset lies within 0.023
in x of its light, in the same
order.

Lamp 63 carries an internal manual disagreement: the Lamp Matrix wiring page prints "R. Skill
100K" while the Lamp Locations parts list prints "R Skill 500K" for the same address, a
scoring-legend discrepancy with no bearing on wiring, polarity, or placement, transcribed
verbatim from both pages.

## General illumination

GI strings 3 and 4 are backbox-only circuits (string 4 additionally reaches a cabinet
bulb through J119) with no playfield voltage or drive connection printed anywhere,
matching the retained script's `GIUpdate2`, which drives a single non-playfield bulb
(`gibg4`/`gibg5`) for each rather than a playfield light collection. GI strings 0-2 (Lower/
Upper/Center Playfield) drive the retained table's `GIBOT`/`GITOP`/`GIMID` collections
exactly, with zero script-vs-manual disagreement — unlike Williams Tales of the Arabian
Nights or Bally Theatre of Magic, both of which found a genuine GI script-vs-manual
conflict.

## Spatial checks

Every table placement the factory location drawings can check was checked against them with
`tools/drawing_callouts.py` (seed `tools/seeds/williams/bram-stoker-s-dracula-1993-callouts.json`):
120 placements, all within 0.07 normalized of their own callout under both fits. The drawings
leave a few placements unchecked, each with its reason in the seed: lamps 16, 37, 38, 41 and 42
have no callout (the lane inserts are drawn unnumbered), switch 85 has none (the drawing prints
a second 25 instead), switch 81 and solenoid 8 have only a leaderless balloon beside the part,
the four flipper coils are marked Not Shown, solenoids 27/28 and lamp 53 are projections of
the moving carrier, and the back-panel lamps 58 and 61-63 are drawn only in the back panel's
inset elevation, not on the playfield plan. Two placements are drawing measurements: flasher 17's
coffin domes.

## Unresolved questions

- Flasher 19's playfield bulb count, one or two (`conflict.flasher-19-playfield-bulb-count`, see
  Flashers). It keeps the record partial. The flasher test on a production machine, or a
  photograph of the wiring from J126-3, settles it.
- `conflict.upper-flipper-circuit-side-naming` stays recorded as ignored (see Repurposed
  upper-flipper circuits): the cross-machine evidence settles which circuit each address drives,
  and a photograph or continuity check of a production Dracula harness at J902 would confirm the
  pin each device's wire lands on. It does not block a recreation.

## Sources

- `manual.williams.bram-stoker-s-dracula.1993`: `Dracula_Bram_Stoker_OPS.pdf`, the
  Williams operations manual, SHA-256
  `de6840bb83a98333ef96a2781e3170103e5856380e9c46aad237974fc028498a`.
- `manual-support.williams.bram-stoker-s-dracula.1993`: retained human transcription,
  `external:pinmame-review-artifacts/dracula/manual-transcription.md`.
- `vpx-table.drac-vpw-1-0` / `vpx-script.drac-vpw-1-0`: the retained known-working VPW
  1.0 table and its embedded script, SHA-256
  `e291eb0ab61eb8940aba6f54d16efd512d4565cbb6af29fcae5530035de7575e` and
  `32f4f0ed85702cc015563eb262ea6c5b7cb7c90f6d30fa6b73c36f3c37c42c5f`.
- `pinmame.core.4ec52ff0ac13`: `src/wpc/sims/wpc/full/drac.c` at the pinned PinMAME
  revision `4ec52ff0ac133ac251681518aed2249e19fe26eb`.
- `ipdb.williams.bram-stoker-s-dracula.1993`: IPDB machine number 3072.
- `drawing-callouts.dracula.2026-10-23`: the factory location-drawing callout check, with its
  reads, controls, corrections, overlays and generators retained under the working root's
  `review-artifacts/dracula/callout-check/`.
- `human-review.dracula-physical-corroboration-2026-10-23`: IPDB pictures 12458, 12459 and
  35879, David Houchin's owner's page on the machine (2020) and Inkochnito's reproduction of
  the Williams tech chart, retained under
  `review-artifacts/dracula/physical-photos/`; what they show is in
  `evidence/excerpts/williams.bram-stoker-s-dracula.1993/physical-photo-corroboration.md`.
- `human-review.fliptronic-ii-upper-circuits`: the cross-machine reading of which Fliptronic II
  circuit drives each of solenoids 33-36, quoting each other machine's rows verbatim with the
  SHA-256 of the excerpt they come from in
  `evidence/excerpts/williams.bram-stoker-s-dracula.1993/fliptronic-ii-upper-circuits.md`.
- Manual excerpts added on 2026-10-23: the Lamp Locations drawing (2-44), the A-16266
  Coil Magnet & Screw Assembly page (2-27) with the game story, the A-16399 Back Panel & Decal
  Assembly (2-39), the Flashlamp Wiring page (3-9) and the Fliptronic II Flipper Circuits page
  (3-18).
