# Firepower II (Williams, 1983)

Coverage remains **partial**. Public addresses, wiring identities, controller
read paths, displays and causal mechanisms are curated from the original
manual, pinned source, photographs and isolated L-2 ROM runs. Physical lamp
routing, socket inventory and exact spatial geometry remain incomplete.

## Identity

Williams model 521, IPDB 857, OPDB GRWYk-Mb5OV. The visually checked cover is
16-521-101, July 1983. IPDB says August 1983; Pinside says June 1983. These
month differences do not alter canonical year 1983. The old OPDB attachment's
1983-01-08 is retained as an identity link, not evidence of a January release.

Only fpwr2_l2 belongs to this original Williams record. wldtexas belongs to
unknown-manufacturer.wild-texas, a separate physical_conversion, IPDB 5500,
unknown manufacturer and null year. Tony Turner's IPDB hardware account and
Theonlylilo's successful Pinside repair describe changed coils/flippers and
a replacement single-EPROM MPU. The retained MPU photo shows the changed
CPU layout. Shared PinMAME init/routing and clone ancestry do not establish
physical identity. No OPDB identity has been invented for the conversion.

## Controller and complete address dispositions

System 7, GEN0x10000, s7_dispS7. Switches and lamps use column-major
(column-1)*8+row numbering. The complete transcriptions preserve all 64 cells,
wire colours, connector pins, drive transistors and Table 4 footnotes.

Services -7/-6 are Advance/Auto-Up; -5 CPU diagnostic; -4 sound diagnostic.
-3 is generic Master Command Enter scaffolding. The normal production
adjustment interface is the coin-door service pair. Matrix 1-49 is wired
except 21 Not Used. Matrix 50-64 is Not Used. 13 is a virtual lane-change
copy of right button 82: core_updateSw overwrites direct 13 writes every
frame. Button 84 is left. Generic flipper-column 81/83/85-88 is unused.
Transport holes -2..0 and 65..80 are not invented inputs.

DIP 1/2 are fitted sound-board switches entering s67s_cmd_w. DIP 3-8 is
undeclared. The emulator exposes F/D bank bits 9-24 through s7_dips_r:
Enter held selects inverted nibbles on PA4-7. They are optional virtual
configuration inputs, not sixteen fitted CPU switches. The CPU BOM item 24
lists DS1/DS2, 8 STD DIP switches, quantity 2; the assembly view of the same factory drawing has no such footprints. Logic
PDF 24-25 wires those PA pins to the IC34/IC35 diagnostic display. The
independent production photo 50056 shows that display and resistor packs
without visible DS1/DS2 banks, supporting the no-fitted-banks disposition.
DIP resistor packages IC28/29/37 are not switches. These transport bit
names are not factory software adjustment numbers.

Outputs 1-25 include coils 1/2/3, Type 83 flash load 4, power-board GI relay 11,
bell 15, two parallel coin-lockout loads 16, six specials 17-22, and game-on 25.
Table 4 marks 5-10/12-14 Not Used; Test 02 still pulses them. 23/24 are swept
PIA slots without fitted circuits on the six-special-driver board.
25 enables specials and driver-board Z1 flipper returns. K1 and Z1 differ.
45/46 follow right 82 and 47/48 follow left 84 while 25 is enabled. These are
used virtual power/hold callback states that assert together; they model
neither separate physical coils nor EOS timing. Custom 51-60 is unavailable
because this game has no custom callback; 26-44/49-50 are transport holes.
Lamps 61-64 are Not Used; 65-96 is absent auxiliary-column space (lampCol0).
System 7 publishes no separate GI channel. Output transitions do not fit loads.

Four seven-digit player displays map callback 2/3/0/1. Four single-digit
fragments at 4/5 and 6/7 form ball/match and credits. s7_dispS7 offsets are
1/9/21/29 and 0/8/20/28 respectively. Photographs verify physical segmented
displays. Synthetic DMD 8 is an emulator render, not fitted hardware.

## Ball movement and mechanisms

Two stored balls occupy 10/11. Drain 9 prompts outhole 1; thrower 2 feeds
shooter trough 12 and a manual plunger launches the ball. Hold occupancy
contacts while a ball rests there and release when it leaves. The source
script models 9, 11, 10 with two balls. The ROM run observes serve 2 on Start
and repeated outhole 1 while 9 is held. A host ball move is not ROM feedback.

Saucer 23 holds the first ball while 2 serves the second. Release 24 fires 3
before 23 is cleared, starting two-ball play. During multiball, saucer entries
score 5,000 and eject immediately (manual operation). A coil does not directly
close a ball-presence contact. The passive orbit uses spinner 18, entry 19
and exit 40; completion fires flash 4. Passive ramp 14/15 awards its lit value,
mystery or extra ball; there is no ramp actuator. The upper orbit's wire
ball preventer is passive (photo 60457), with no invented output.

FIREPOWER letter targets 25-33 are standups, not a resettable drop bank.
16/17 are separate scoring standups; 20/22 are upper rebound contacts.
The IPDB feature count uses different categories; it is not a reason to
delete documented contacts. A-B-C-D 34-37 advance 2x/3x/5x and right-flipper
lane change. Letter groups light jets and the timed bonus-holdover orbit
award; repeated completions light return lanes, ramp extra ball and specials.
Operation and construction excerpts retain the award progression.

Four jets and two slings have separate scoring and direct-power contacts.
PinMAME synthesizes specials 17-22 from 47/48/41/42/43/44; these are not
public power-switch inputs 65-70. Each relation was exercised in gameplay.
Two flippers use dual-wound SFL-19-400/30-750-DC coils and local EOS contacts,
cabinet-switched through Z1. Physical geometry, tuning and pulse duration
remain consumer/table parameters; they are not invented from callback width.

Ordinary matrix contacts are normally open in the factory schematic;
the uninverted read path and Test 03 closure display agree with that
construction. Ball occupancy is not a normally-closed contact. New controlled
runs show plumb 1 warns twice through GI 11 then tilts on the third closure;
playfield 49 tilts immediately. Slam 7 ends play on its first closure and
resumes the attract sequence. These are exact L-2 observations under the
retained initialized settings, not universal adjustment thresholds.

## Lighting and source contradictions

Backbox 1-5, playfield Shoot Again 6, and separate Bonus Holdover 8/23 are
preserved. PDF 51 BACKBOX labels for 45-48 conflict with the game-specific
location drawing and the independent lower-playfield photo; follow the
physical playfield positions. Reprints within the manual are one source.

Lamp 40 publishes meaningful Ball in Play state, but its physical availability
and routing remain unknown.
Figure 1/Figure 2 call 40 Ball in Play; PDF 51 marks 40 NOT USED; PDF 41 draws
9B6 BALL IN PLAY on COL1/ROW6 (public 6), while 6 is the photographed playfield
Shoot Again. Photo 50054 shows sockets without readable circuit identities;
50030's footer does not trace the wiring. The scripts omit 40. Start/tilt
transitions prove meaningful 40 state, not presence or absence of a bulb.
No virtual-only fitment conclusion is justified. Its cabinet applicability
is recorded; no playfield position or bulb quantity is invented.
Resolution path: an owner/technician must trace the original Ball in Play
socket through 9P1 to its matrix bit and check whether 6 shares a backbox load.

Flash 4 is a real plural Type 83 load. Figure 5 gives a grouped callout and
PDF 52-53 a grouped diode/load, not a socket count. The repeated 8L2
designation also labels thrower 2; connector pins preserve separate circuits.
K1 on the power board opens the common 6.3 VAC GI leg when energized; four
fused branches serve two playfield groups (one also cabinet) and two insert
groups. Each is 5 A slow-blow. Z1 on the driver board gates flipper returns.
The GI excerpt transcribes all four branches. PDF 35/41 swap insert fused
pins; PDF 35/48 versus 50 disagree on playfield colours/pins. These are wiring
details, retained literally without turning public device identity into a
conflict. Table 4 versus solenoid schematics also disagrees on 19/21/22 pins,
colours and an omitted 22 footnote; structured values follow the game table.

Actual GI sockets and orbit-flash sockets cannot be counted from continued
schematic symbols. The retained above-playfield/stripped photos and all 16
Pinside previews lack a complete underside/socket inventory; LED-modified
gallery machines do not establish original fitment. No callback quantity
or geometry estimate substitutes for that missing physical evidence.

## Recreation artifacts and evidence

Two exact pinned corpus scripts remain candidates; the supplied table has
not been confirmed to launch or play. Newer 1.1 has ChangedLamps 6-39/41-60, virtual render
doubles and callbacks 1/2/3/4/11/15. It writes unfitted 57/58 for flippers
and clears 57 on left release. S7 library writes 82/84 correctly first.
The older script says unverified and pulses 39 from both outlane handlers;
left outlane is 38. These are script defects, not physical source conflicts.

Newer 1.1 also sets vpmNudge.TiltSwitch=7. The inspected installed s7.vbs
routes the mechanical-tilt key to core.vbs DoMechTilt, which pulses that
configured switch. Controlled L-2 runs distinguish 7 slam from 1 plumb and 49
playfield tilt. Repair the recreation's nudge/plumb route to 1. The separately
retained installed libraries are hash-pinned; no exact table library version
or successful launch is claimed.

The PDF was retained 2026-10-29T23:57:07Z, SHA256
c601834cd57c8cf01423355304d487f3143d92ef1374187344d264eab7e6e6d8.
Complete table transcriptions and native drawing crops are in the excerpt
folder. Source-owned originals remain external. The retained-input manifest
pins 72 source files, native frames, photo/page metadata and 16 gallery
resources with original attribution/rights. Sources include exact URLs,
acquisition times and hashes; none grants redistribution of originals.

Runtime evidence pins the ROM archive/member identity, 46e1a01a native build,
explicit initialization trace/NVRAM and every scenario/raw run. Each run
uses a fresh directory seeded only with that initialization NVRAM.
Test 02 pairs selectors 1-25 with public outputs; slow Test 03 displays 1-49
and blank 50-64, including scanned but physically unused 21. The initial
450 ms sweep missed multiplexed numerals; its 2200 ms successor is distinct.
A repeated pulse masks lane-change overwrite; the one-shot control and
button 82 display establish the actual copy path. Keyboard/simulator are off.

## Concrete remaining coverage requirements

- output_enumeration: exact stock GI socket inventory per branch and Orbit
  Complete Type 83 quantity. All retained schematics/photos/gallery previews
  were inspected; continued/grouped symbols and top views cannot settle it.
  An original-machine underside/socket inspection is needed.
- output_semantics and unresolved_conflicts: Ball in Play 6/40 routing above.
  The ROM probes and available photographs were exhausted for this question;
  only physical tracing can settle which bulb is wired to which bit.
- spatial_placement: the exact supplied Goldchicco/Apophis 1.1 table is now
  retained and extracted. The spatial report enumerates normalized sensor,
  effect and emitter placements and each projection/extrapolation. Fifty
  lamp locations are measured from Figure 2 rather than its table's insert
  render lights; four bumper lamps use their own modeled bulb meshes.
  Ball-ramp contacts 10/11, playfield tilt 49, individual orbit-flash bulbs
  and stock GI sockets still lack defensible placement. Their absence keeps
  this dimension missing. Original-machine underside/branch/socket evidence
  is needed; table grouping is not a stock inventory.

## Retained spatial continuation

The read-only user-supplied FirePower II (Williams 1983) 1.1.vpx is pinned
at SHA256 225acbf289239139e069886ebc1c7ba9754905a348ca2aba9f1a3822b1564eeb.
The full extraction manifest and native manual control readings are in the
spatial report and its seed. Bounds are x0..1000/y0..2000, normalized in
player view with y increasing toward the apron. Six independent bumper and
flipper controls reconcile each of PDF14/15/17 with leave-one-out checks;
all drawings, projections, extrapolations and rejected candidates are named.
Fifty manual emitter projections retain three-decimal scan precision.
The four NFadeLm bumper doubles collapse onto L41a-L44a, each showing its
own bulb mesh. Assembly sensor/effect projections remain observed; they do
not claim the exact contact or winding axis. Sensors 10/11 cannot both be
put on the one abstract BallRelease kicker, and 49 has no located symbol.
The baked OrbitGate mesh supplies only an observed gate-assembly projection;
its stored origin and the broad Trigger1 routing helper are rejected as
physical contact centers. Sling effects use exported world-space mesh bounds.

The embedded Windows-1252 script has SHA256
7a177b7170ea7113eccd11ba0c8ba232b534dcd92162495dc44b77bfdcf17922.
Its dampener scales x/y once, whereas the corpus version scales x/y/z twice.
I/O bindings agree; byte differences are not dismissed as encoding alone.
The contributor confirms the exact table has not been tested in play. Earlier
controller and runtime facts, including the nudge7 and flipper57/58 defects,
are preserved. Light62 has no identified bulb mesh, so callback4 still has
no individual emitter placement. The GI collection and visible unbound bulb
primitives document table geometry only; no new GI callbacks or relay aliases
are created and no stock bulb quantity is inferred. Lamp6's photographed
playfield member is placed, while possible parallel backbox load and lamp40
remain conflicted. No coverage requirement is removed for this continuation.

Independent source and overlay inspection identified four flipper-pivot
control reads above their inner circles. Primary native-crop inspection corrected
PDF14 left/right to approximately (540,2550)/(980,2550) and PDF17 to
(645,2545)/(1085,2545), at five-pixel precision; PDF15 controls were retained.
Old/new readings, crop boxes, frame/crop hashes and reasons are in the spatial
seed. The PDF14 refit recomputes all fifty manual lamp-symbol projections at
three-decimal normalized precision. PDF15 leaderless sling labels17/18 and
PDF17 storage/shooter labels9/12 are retained as excluded raw observations and
cannot enter precise callout fits. Their observed table assembly/sensor
placements remain. The source reviewer then verified the corrected native overlays and
source controls. This source check is separate from the independent
contribution review and does not assert tested play.

Driver mapping, input semantics, mechanism inventory/behavior, polarity,
variant separation, recreation notes and provenance have source-backed
dispositions above. Their earlier broad missing flags are closed; the
remaining physical-count/geometry blockers do not erase that evidence.
