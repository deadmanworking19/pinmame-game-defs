# Stars (Stern 1978)

Coverage is **partial**. The controller, complete public address disposition,
factory switch and named output inventory, six display windows, ordinary
mechanisms, and original-ROM causal checks are curated. Blank lamp loads,
complete physical emitter inventory and placement, and community-firmware
differences still prevent author readiness. The exact blockers are in
`reports/spatial/stern/stars-1978.json` and `coverage.missing`.

## Identity and variants

Stars is Stern Electronics model 103, March 1978, IPDB 2366, OPDB
`GrXEW-MDEwr`. The retained [IPDB record](https://www.ipdb.org/machine.cgi?id=2366)
and factory CAT. NO. 12G-5-103 agree. Its physical controller is MPU-100,
not MPU-200: pinned `stgames.c` declares `GEN_STMPU100`, `dispst6`,
`FLIP_SW(FLIP_L)`, no auxiliary lamps, and `SNDBRD_NONE` for every set.
It has four mechanical chime channels, not an electronic sound board.

The pinned family contains `stars`, `starsfp`, `starsb` (MOD rev.103), and
`starsb7` (rev.103 seven-digit conversion). The factory and Free Play sets
use six-digit player displays, starting in controller memory at 2,10,18,26.
Credits and ball/match use two digits each, at 35 and 38. The seven-digit
driver instead starts at 1,9,17,25, with seven characters of CORE_SEG87F;
its overrides do not silently turn factory six-digit displays into seven.
The extra 128x32 display callback in the retained harness is PinMAME's
synthetic segment-to-DMD rendering, not another physical display.

The original and Free Play ROM archive members were checked against the
pinned SHA-1s. Community MOD ROMs are absent from the authorized library;
shared init is evidence of emulator routing, not proof of every rules or
physical-installation difference. Keep those differences open. No later
firmware year changes the machine's 1978 release year. Factory Bulletin 7
requires paired P3/P4 or paired P3A/P4A ROMs, replacing both together. Its
file/discovery label says July 7; the rendered bulletin actually prints
JUNE 7, 1978. The A pair and tournament modification mentioned in source
are not separate supported drivers at this pin.

A retained vendor-hosted readme for related STARS#103 seven-digit alpha
firmware describes DIP25 becoming Free Play, four replacement score
displays and MPU A4 J1-7 distribution to display pin12 (pin11 for Stern),
leaving credits unchanged. It reports PinMAME-only testing and a v72
stack-top fix. Its STARS103_7X filenames differ from pinned STARS_72.U2/U6;
similar version names do not verify byte identity. These are attributed
leads, not silently applied clone behavior or a proven physical conversion.

S25 selects two/four player operation; IPDB describes a two-player
backglass and says the third/fourth displays likely were omitted. That
qualification is not proof of the display fitment of any particular unit.
Bulletin 8 requires S27 ON for multiplayer, superseding the manual's N/U.
These are option-bank ordinals, independent of playfield switch 25 or 27.

## Controller and physical input contract

Use public state as PinMAME delivers it. The MPU-100 matrix is unmasked,
uncomplemented and normally open: public 1 is closure. Its cabinet map is
coins 9-11, Start 6, Tilt 7, Slam 16. The two normally-open tilt contacts
(pendulum and roll cage) share 7; generic Bally ball-roll-tilt address 2 is
unfitted. Keyboard handling can overwrite these cabinet inputs. The
retained traces use direct writes, with keyboard/mechanics disabled.

All 1-40 appear by their own number in the ROM switch diagnostic, including
factory N/U positions. The sweep of 41-48 and 81-88 shows no numbered
response. Lower generic flipper buttons 82/84 still publish synthetic
right 45/46 and left 47/48 while public 19 is enabled. They do not reach
the ROM matrix. Both outputs of a pair rise together for the full closure;
they measure neither winding current nor physical EOS time. Only one
physical flipper exists per side; the duplicate callback adds no coil.
The real normally-closed EOS contacts are separate physical direct inputs.

Self-test -7 drives PIA CA1; CPU diagnostic -6 drives NMI. The factory
Figure3 MPU S33 button is represented by the -6 record, with an explicit
S33 alias and quantity one. The pinned hardware-backed CPU-diagnostic
branch explicitly reads lisy35_get_SW_S33 on that same NMI route. The
adjustment instructions use S33 to clear selected bookkeeping/high-game
values; that does not promise an unconditional bookkeeping-clear API.
Sound diagnostic -5 has no selected sound board on this chime game.

Seven ten-point rebound contacts share 25; two bonus rollovers share 15.
Three slam contacts share 16 (door, tilt board and underside of playfield).
Do not collapse a shared input to one switch or exempt the whole slam
aggregate from playfield placement merely because two contacts are cabinet.

## Outputs and recreation behavior

Printed coil-test order differs from the public selector. The retained ROM
test displays each factory number as it fires; the complete pairing is
preserved in the compact runtime evidence. Public coils 1-4 are chimes,
6 knocker, 7 outhole, 9 left bank reset, 10 upper/right bank reset,
13 bumper, 14 right sling and 15 left sling. Continuous 18 is coin lockout
and 19 the flipper-enable relay. Momentary 5,8,11,12 are unfitted; their
printed test numbers remain blank, while the decoder and collector paths
establish their public-to-transistor/connector assignments. Continuous
17/20 are also N/U. The service sweep pulses the unused momentary drives;
17/20 briefly rise in the power-up continuous-port initialization.

The native PDF25/26 U2 decoder, traced collector wires, numbered fitted
loads and ROM coil test agree. The complete routes and literal blank cells
are retained in the solenoid excerpt and coil-decoder seed. Engineering
Bulletin9's full CA3081 chart corroborates every momentary stage, including
base16/collector1 for Q1/U1 and Q8/U3. Outhole is Q4 to A3J1-5, not J5.
Additional N/U connector branches on Q2, Q1, Q3 and Q16 have no fitted
loads. Q18 reaches three N/U pins, A3J5-3/A3J2-15/A3J3-9. Q15's collector
drives the on-board relay's terminal8; A3J3-5 supplies terminal7 with +43V.
Source-pixel collector overlays and hashes are retained externally in
review-artifacts/stern.stars.1978/retrace-r2; the spatial report pins them.

The one ball rests on outhole switch 8. Start with credits fires coil 7;
the host moves the ball into the shooter lane and releases 8. Drain returns
the ball to 8, pays bonus, then serves the next player/ball. The plunger is
manual, with no launch coil or shooter switch in the factory matrix. The
retained script's BallRelease is the shooter proxy, not the physical outhole.
Never describe this single-ball stack as a multiball trough.

Each bank has three individually latched targets and one common reset.
Left order is targets 1,2,3 at switches 32,28,31; upper/right order is
targets 4,5,6 at 30,27,29. A down target holds its contact closed; reset
raises the bank and opens all three. Startup resets both banks. In the
retained gameplay sequence, completing either fires **both** reset coils.
Factory part D-393-3 names the three-bank assembly. Repeated completion
advances double/triple-bonus features, with S24 selecting whether the second
stage needs either bank or both. The third stage can award WOW/extra ball
(S26), the fourth and later special; either bank's center target alone
standing with both side targets down scores 7000. These are ROM rules,
not a direct electrical connection between the two physical reset coils.
No unverified speed, pulse duration, special jam sensor or home switch is
invented; a stuck-down contact can be seen in the ROM's stuck-switch test.

The isolated original-ROM probes pair switch 38 with coil 13, 37 with 15,
and 36 with 14; tilt 7 drops relay 19 and lights lamp 61. Both older local
tables swap the slingshot switch writes. This is a table defect, recorded
on those devices, not an unresolved disagreement about the physical game.
Coil 7 is assigned twice in their script; the last SolOut assignment wins.
The newly supplied bord 1.0.2 table corrects right 36 / left 37 and assigns
coil 7 once. Its optional VR backglass callback instead labels 45 as Match
and 60 as Game Over, conflicting with the traced factory Match 27 and Game
Over 45 circuits. The physical identities follow the factory wiring.

The lamp board has sixty discrete SCR outputs. Public address is
`16*(decoder-1)+selector+1`, selectors 0-14; addresses 16,32,48,64 are holes.
The complete decoder/resistor/SCR/connector transcription keeps all blank
labels and eight split connector branches. It must not be replaced by a
sibling game's SCR ordering. {{LAMP_INVENTORY}}
Every partially named split explicitly leaves its unnamed branch's load,
location and quantity unknown. Match27 has named MATCH at A5J2-8 and a
blank A5J1-4 branch; the aggregate has no cabinet-only spatial exemption.

General illumination is transformer-fed and has no ROM GI callback. Stars'
own harness separates the G.I. bus from the controlled feature-lamp bus.
The reusable power-transformer drawing is still labelled Stingray; only
board-internal facts may be reused from it, not another game's fitment.

Apply the manual's corrections: starting bonus is 1,000 (not 10,000), star
targets also advance bonus, bumper value depends on three/five-ball option,
S16 controls the hinge-side coin chute, and S15 disables high-game-to-date.
Full identification tables, option summary, corrections, ROM-pair table and
coil-array table are retained as excerpts with the exact source hashes.

## Spatial evidence and remaining work

Two 32assassin local table revisions, 0.9.0.4 and 0.9.0.2, were discovered,
retained and extracted with vpxtool git:v0.33.3. They use the same geometry
and script lineage; agreement is not independent corroboration. Their
952 by 1974 bounds give x=X/952, y=Y/1974 (left-to-right, rear-to-front).
Each extraction is pinned by a reproducible all-file manifest, including
file count and total bytes. Pinned newer script corpora are separately
hashed and use a different lamp-update idiom; their geometry was not
silently substituted for these older tables. The user then supplied bord
1.0.2 / Uncle_Paulie VR, retained separately with complete extraction
manifest. Its actual bounds are 952.9412 by 1976.4706; its metadata's 1977
title is a typo against the physical 1978 identity. None of the three
tables was launched in this session; no known-working claim is invented.

Switch/coil coordinates are observed, with explicit mechanism projections
for rubber contacts, hidden coils/EOS, bank resets and the Drain proxy.
Nineteen GI objects show bulb meshes; their nineteen neighboring broad
lights are helpers and are excluded. Complete GI string membership, hidden
sockets and cabinet/backbox quantity still need reconciliation. Controlled
lamp Light objects show no bulb mesh, and may be insert/glow proxies; their
42 bound centers are report candidates, not physical socket placements.
The bord script drives 44 objects at 34 addresses, including co-located
L8/L8b and L8a/L8c helper pairs. None of its Light objects shows a bulb
mesh; its 16-member GI group is also a render grouping. Its lightmap layers
do not turn insert glow centers into socket coordinates. Both candidate
sets are retained separately rather than mixing their object names.

Independent parent reads of factory PDF19/21 were visually corrected on
source-pixel grids before consulting table coordinates. Four controls
(bumper center, two inlane slots and left spinner axle) span over half the
playfield height. The shared affine checker reproduces control RMS about
0.006 and leave-one-out maximum about 0.034. PDF19 corroborates 29 of 30
switch anchors at the 0.07 limit. The upper bonus-rollover callout fails at
0.1063 control / 0.0938 callout offset; its coordinate stays observed and
unchanged. Coil projections mostly fail. Full reads, source/render hashes,
corrections, per-page fits and all outcomes are retained in the callout
seed and spatial report. Projections and multi-table geometry remain
observed; a fit is corroboration, not a license to move an anchor or claim
an exact hidden contact. The underside slam contact remains unlocated.

Original PDFs, native renders, Windows.Media.Ocr search output, photographs,
VPX tables, extractions, ROM indexes and raw traces stay under the fixed
external working root. Their bytes are not redistributed in Git. The exact
locations, hashes and model/command logs are in the game's review artifacts.
