# Junk Yard (Williams, 1996)

## Identity and evidence precedence

Junk Yard is a Williams WPC-95 machine (manual 16-50052-101, JANUARY 1997
FINAL). Pinned PinMAME's own `libpinmame.h` names the `GEN_WPC95` constant
"Integrated boards, Congo 3/96 - Cactus Canyon 2/99", i.e. Junk Yard is part
of the same integrated-board WPC-95 hardware generation as the other machines
in that era. The retained known-working table (VPX v1.3, author mfuegemann;
primitives/textures by Fuzzel and Dark, lighting by Hauntfreaks) binds driver
`jy_12`, the production 1.2 ROM (DCS sound).

This curation follows the project's standard evidence-authority order: the
retained script is runtime/causality ground truth, the Williams manual is
physical-construction/wiring/quantity ground truth, pinned PinMAME source is
controller-topology ground truth, and the retained table supplies geometry.
The retained manual (146 pages) carries a usable OCR text layer, but every
printed table cited here was read from 200 dpi renders and transcribed into
`evidence/excerpts/williams.junkyard.1996/`, cross-checked across the repeated
copies (front matter, printed 2-38, and Section 3). **These transcriptions are
recorded with `reviewed: false` / `method: model`** — a curator
has not yet visually re-checked them against the rendered pages. The
polarity, spatial, controller-topology, and mechanism-causality conclusions
rest on pinned PinMAME source, the retained VPX geometry/script, and the
cross-copy comparison rather than on the unchecked transcription alone, and
the semantic device identities are corroborated by the retained VPX object
names and the pinned PinMAME source. The raw transcription wording (labels,
part-number spellings) remains subject to a curator re-check of the excerpt
transcriptions before author-ready promotion. A retained 16-page operator
handbook (born-digital, with a real text layer) reproduces the same tables
and can assist that re-check.

**Junk Yard has no pop bumpers.** Unlike most WPC-95 machines, neither the
switch matrix nor the solenoid table lists a jet/popper bumper; the playfield
features standup targets, slingshots, a crane with a wrecking ball, a
refrigerator popper, a fork-lift scoop, a dog-house mechanism, and a spinner.

## Controller platform and address topology

Reuses `controllers/pinmame/wpc-95.json` unchanged, confirmed directly from
`jyGameData`'s own `GEN_WPC95` field in `src/wpc/sims/wpc/prelim/jy.c`. The
switch matrix, Fliptronic column, LPDC duplication (37-40 mirrored at 41-44),
and five-string GI layout all follow the standard WPC-95 rules already
documented on that profile.

Junk Yard declares no custom switch column, no auxiliary lamp column, and no
custom solenoid board (`jyGameData`'s trailing `hw` fields are all zero), so
this is a clean WPC-95 baseline with no address-remapping surprises beyond
the flipper circuits below. The switch matrix's eighth column (81-88) is
entirely unpopulated; switches 23, 25, 55, and 75 are also printed Not Used.

**Flipper circuits.** Printed circuits 29/30 (Lwr Rt Power/Hold) and 31/32
(Lwr Lt Power/Hold) map to public addresses 45-48 (`CORE_FIRSTLFLIPSOL=45`).
Printed circuits 33-36 (the "Upr. Rt."/"Upr. Lt." driver-board slot,
`CORE_FIRSTUFLIPSOL=33`) already equal their own public addresses. Junk Yard
fits **no upper flippers**: `jyGameData` declares `FLIP_SOL(FLIP_L)` only, so
no upper flipper solenoid is CPU-driven and no upper `FLIP_EOS` bit is set.
The Switch Locations page marks F6 (Upper Right Flipper Cabinet), F7
(Upper Left Flipper E.O.S.) and F8 (Upper Left Flipper Cabinet) Not Used.

The flipper-column switch treatment deserves precision because it depends on
PinMAME's `flipMask` construction (`core.c:2510-2517`), which is driven by
`jyGameData`'s `FLIP_SW(FLIP_L | FLIP_U) | FLIP_SOL(FLIP_L)`. That mask always
carries the lower-right/left button bits and the lower EOS bits (from
`FLIP_SOL(FLIP_L)`), and additionally the upper-right/left **button** bits
(from `FLIP_SW(FLIP_U)`); it carries no upper EOS bit. The two addresses that
PinMAME genuinely **forces every VBLANK** regardless of keyboard mode are the
lower end-of-stroke contacts 111 and 113: `core_updateSw` recomputes them from
`core_getSol` (the flipper hold-coil state) plus `CORE_FLIPSTROKETIME`
(`core.c:1756-1775`) and writes them back, so **a recreation must not drive
111 or 113**. The button addresses 112/114/116/118 are read from and written
back to the matrix unchanged when keyboard handling is off
(`core.c:1731`, the LibPinMAME default `g_fHandleKeyboard=0`), so the emulator
publishes no meaningful runtime state at them; 116/118 are additionally
unfitted (no physical upper-flipper button exists) and are recorded `unused`,
while 117 (upper-left EOS) is dead because no upper `FLIP_EOS` bit is set.
F5, however, is **not** a flipper contact at all: the manual prints it
"SPINNER" (part 5647-12693-24), and the retained script's `Switch115_Spin`
handler pulses it as the playfield spinner. This is the same "Fliptronic F5
repurposed for a non-flipper device" pattern Monster Bash established with its
Center Spinner.

## Opto polarity sweep

The manual's Switch Locations parts list (2-35) identifies eleven
opto-constructed switches by printing an LED/photo-transistor pair on two
lines rather than a single mechanical part: 31-35 (A-18617-1/A-18618-1, the
trough) and 36-37 (lock-up) and 41-44 (Past Spinner, In The Sewer, Lock Jam,
Past Crane) (all A-16908/A-16909).
The switch matrix (2-34) shades column 3 rows 1-7 as "OPTO, TYPICALLY CLOSED".

Pinned PinMAME's `jyGameData` inverted-switch mask
(`{0x00,0x00,0x00,0x7f,0x07,0x00,...}`) normalizes column 3 rows 1-7
(31-37) and column 4 rows 1-3 (41-43). That matches the manual on ten of the
eleven opto addresses. The exception is **switch 44 (Past Crane)**:
opto-constructed per the manual but **not** normalized by PinMAME (column 4
row 4 is outside the mask's `0x07`).

The ROM's own T.1 SWITCH EDGES test shows that the mask is right. Hash-pinned
LibPinMAME runs of `jy_12`, `jy_11` and the `jy_03` prototype, each from empty
NVRAM, set public 45 (Ramp Exit, an ordinary switch), 41 (Past Spinner, the
same A-16908/A-16909 opto pair, normalized) and 44 to 1 and then 0. Each level
was held for two seconds. In all three runs the top display line names
PAST CRANE after 44 goes to 1 and returns to SWITCH EDGES after it goes to 0,
just as it does for both controls
(`evidence/runtime/wpc-95/junkyard-jy_*-switch-edges.json`). The ROM therefore
reads public 44 = 1 as active. A recreation drives it as the known-working
table does (`switch44_Hit` calls `vpmTimer.PulseSw 44`) and never inverts it.

Outside the inversion mask the WPC-95 security PIC passes the public level
through unchanged, so 44's matrix contact rests open (`normally_closed:
false`), while the masked optos 31-37 and 41-43 rest closed. The shared part
number fixes opto construction, not the contact's rest state. No retained
source shows the circuit difference behind it. The earlier conflict record for
this address was withdrawn.

The same runs show one incidental difference between ROM revisions. The
production ROMs (`jy_11`, `jy_12`) print GRN-WHT as the column-4 wire colour
in the T.1 display, while the `jy_03` prototype prints GRN-YEL. The manual
prints both. The (not yet visually reviewed) switch-matrix transcription gives
column 4 as Green-Yellow, while the Wreck Ball Target Assembly drawing (2-29)
labels the column wire of car targets 46-48 GRN-WHT. The definition keeps the
switch-matrix page's colour.

## Mechanisms

- **Four-ball trough and release** (A-19963-1): the retained script's
  `cvpmBallStack` helper `bsTrough` reads switches 32-35 as a plain switch
  array and ejects the ball through solenoid 9, pulsing opto 31 in the same
  `SolTrough` event.
- **Shooter lane and auto plunger** (A-21022): the `Autoplunger` handler pulls
  back and fires `Auto_Plunger` only when switch 18 is active.
- **Crane arm and wrecking ball** (A-21523 with A-21247): the Moving Crane
  Assembly (2-20) is an arm on an axle at the crane mount, lifted through a
  plunger by one A-20099 coil assembly, the coil part the solenoid table prints
  for both solenoid 3 (Power Crane, high power) and solenoid 15 (Hold Crane, low
  power). The wrecking ball hangs from the arm on a cable assembly (A-21326).
  The retained script lifts the arm, and the ball with it, while solenoid 3 is
  on, holds it up while solenoid 15 is on, and drops it when both are off.
  Switch 28 (Crane Down) is the assembly's micro mini switch
  (5647-12693-31): closed with the arm down, open with it up.
  - The arm only lifts and drops. No switch reports a left or right position.
  - The wrecking ball swings freely when the game ball hits it. The swing is
    registered by the Wreck Ball Target Assembly (2-29), an arc of five target
    switches around the ball. Its wire labels are exactly car targets 46, 47,
    48, 53 and 54, the five switches the Switch Locations page footnotes ABOVE
    CRANE. The car toys sit on those targets.
  - The retained table models the arc with a hidden pendulum below the apron
    that strikes walls `SWCar1`-`SWCar5`. The script copies the pendulum's
    swing onto the visible ball.
  - Switches 15 (Top Left Crane) and 38 (Top Right Crane) are not crane
    sensors. Their part, A-18530-4, is the Red Standup Target of the Upper
    Playfield Parts list (2-30, item 24, called out twice on its drawing).
    The Switch Locations drawing puts them at the top of the target arc,
    either side of the centre channel.
  - Switch 44 (Past Crane) is not a crane sensor either. The Switch Locations
    drawing runs its leader to a switch on the top-left lane, and the
    retained table models it as a lane trigger before the `CraneHole`
    kickout.
  - The Power Crane coil is placed at the crane arm's mount (`PCraneArm`),
    where the solenoid-location drawing puts it.
- **Refrigerator popper** (A-21216): `bsFridgePopper` uses switch 37 as the
  entry and switches 36/43 as the internal ball-stack array; solenoid 2 ejects.
- **Bus ramp diverter** (A-21409-1): solenoid 6 rotates a diverter flap
  (`Sol6.IsDropped`) with no dedicated switch.
- **Spike the dog** (A-21383): solenoid 16 drives the dog-house spike arm;
  `SpikeBark`/`SpikeTimer` animate it while switch 74 reports a ball in the
  dog-house entry.
- **Fork-lift scoop** (A-21220): solenoid 5 (Scoop Down) and solenoid 21
  (Scoop Up) lower/raise the fork arms; switches 73 (Scoop Made) and 72 (state)
  report the scoop.
- **Car targets** (SW-1A-210): 46-48 and 53-54 are the wrecking-ball target
  arc described under the crane above. They are struck by the swinging
  wrecking ball, and there is no resettable drop mechanism.
- **Three-bank target clusters** (A-21349-1 / A-21351): four clusters of three
  **standup** targets (56-58, 61-63, 64-66, 76-78); no bank is solenoid-reset.
- **Slingshots** (B-9362-R-3): left (solenoid 10, switch 51) and right
  (solenoid 11, switch 52).
- **Spinner**: Fliptronic F5 (public 115).

## Service and setup

The front-matter DIP Switch Chart documents five country combinations
(America, European, French, German, Spain) across SW1-SW8. The machine uses
four balls. The crane mechanism and the wrecking ball are the headline
features, with the cars, refrigerator, dog-house, and fork-lift scoop forming
the themed toy complex.

## Unresolved

No switch-polarity question remains open. The lamp-86 (Gen. Crane) plane
conflict is unresolved. Several crane/trough/sewer mechanism-internal sensors are documented
projections onto the mechanism's real kicker rather than surveyed
coordinates.

## Sources

- Williams Junk Yard Operations Manual (16-50052-101, January 1997 FINAL),
  146 pages, SHA-256 `08819a08990c61070c4a3a99a4d5f00d9d082b6d00477ffaf9b0a58fddce3fe1`.
- Retained known-working table `Junk Yard (Williams 1996).vpx` v1.3 by
  mfuegemann, SHA-256 `8ff2c1c8ae3457a4b88ff2207bc506d07435b049343301ded4dbf8e855bef07f`.
- Pinned PinMAME `8371478a7640f1896dcdf565aed340dc5df989ba`,
  `src/wpc/sims/wpc/prelim/jy.c`.
- T.1 SWITCH EDGES runs of `jy_12`, `jy_11` and `jy_03` on the pinned-revision
  library (`pinmame64.dll`, SHA-256
  `deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c`) with
  scenario `tools/harness-scenarios/wpc-95/jy-switch-edges-44.json`, summarized
  in `evidence/runtime/wpc-95/junkyard-jy_12-switch-edges.json`,
  `junkyard-jy_11-switch-edges.json` and `junkyard-jy_03-switch-edges.json`.
