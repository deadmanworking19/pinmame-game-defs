# Harley-Davidson (Sega, 1999)

Coverage: **partial - every I/O address, controller binding, polarity, wiring detail, mechanism, variant and
recreation note is source-reconciled except lamps 52-54, which the 3rd-edition manual and the 1.03 ROM's own Single
Lamp Test both name NOT USED but `harl_a13` drives during play, so `output_semantics` is missing; `spatial_placement` is
missing because the retained table does not model the trough, the motorcycle trough, the lift or the stop light,
several flashers are drawn only with overlay objects, and no placement has been checked against the factory location
drawings**

## Identity and edition

This is Sega Pinball's Harley-Davidson of September 1999 (IPDB 4453, model 67), which IPDB calls the last game Sega
produced. Stern Pinball continued the same production run as its own Harley-Davidson (1st Edition) of 1999 (IPDB 4455),
which `stern.harley-davidson.1999` curates with Stern's later 2nd and 3rd editions. The two records describe one
playfield, one wiring and one controller routing; they stay separate because the catalog keeps Sega's game ROM 1.03
sets apart from Stern's later code, and this record holds only Sega's.

`tools/curate_harley_davidson_sega.py` therefore derives this record from the Stern curator's build. Every
construction, wiring, mechanism and placement fact comes over unchanged with its excerpts under
`evidence/excerpts/stern.harley-davidson.1999/`; the identity, drivers and sources are this record's own, and every
runtime claim rests on this machine's firmware. The evidence that one wiring covers both:

- **The factory manual.** The only manual held here is Stern's 3rd-edition service manual (780-5087-00). Its firmware
  appendix opens with the "Original (1999-2001)" block, game ROM A1.03 ($3EFF) and display A1.04 ($FC7C), which is
  exactly the `harl_a13` pair. Its production appendix dates the original's start "AUG 99" with manual 780-5067-01,
  and its board-type appendix prints one row for the "1st-3rd Editions": the same I/O power driver, display, opto,
  relay, shaker-motor and diode boards. Its CPU/sound cell prints 520-5136-16 over 520-5300-00, which the firmware
  appendix's footnote 8 names the CPU/Sound Board II with an ATMEL processor and cites only for the 2nd- and
  3rd-edition firmware, so the original run presumably carries the 520-5136-16 board.
- **The ROM's own wiring tables.** The 1.03 ROM's Portals service tests print a name and the drive and return wire
  colours for every matrix switch 1-64, every lamp 1-80 and every driver Q1-Q32 (next section). Every one matches the
  3rd-edition manual's Switch Matrix Grid, Lamp Matrix Grid and Coils Detailed Chart, wire for wire, apart from
  spellings. The Dedicated Switch Test prints the same DS-5 wiring as Stern's 4.00 ROM.
- **The service bulletins.** Stern's Service Bulletins 113 (December 10, 1999), 114 (February 11, 2000) and 121
  (February 5, 2001) concern the machines of the original production run and change trim, not wiring (below).

Where Sega's machine may differ from the manual's 3rd edition is art, trim and the motorcycle models, which the manual
does not tie to an edition, and the early-production parts the bulletins replace. None of these changes an address.

## Firmware and drivers

The record holds the seven Sega sets of pinned PinMAME, all game ROM 1.03. `src/wpc/sims/se/prelim/harley.c` builds
them (lines 476-510) on `de_mSES1` with the same sound set and the same `init_harl` as every Stern set, which installs
`harlGameData`: GEN_WS, a 128x32 DMD, lower flippers only (`FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L)`), two extra lamp
columns (lamps 1-80), no custom solenoids and no auxiliary board. All seven are `identical`; they differ in the
display ROM's language and version, and `harl_u13` also in its game ROM, `harcpuk.103` instead of `harcpu.103`.

| Driver | Game ROM | Display ROM | Display language and version |
| --- | --- | --- | --- |
| `harl_a13` (root) | `harcpu.103` (CRC 2a812c75) | `hddispa.104` (CRC fc7c2924) | English 1.04 |
| `harl_u13` | `harcpuk.103` (CRC e39130a7) | `hddispa.104` | English 1.04 |
| `harl_a10` | `harcpu.103` | `hddispa.100` (CRC bdeac0fd) | English 1.00 |
| `harl_f13` | `harcpu.103` | `hddispf.104` (CRC 5f80436e) | French 1.04 |
| `harl_g13` | `harcpu.103` | `hddispg.104` (CRC c7f197a0) | German 1.04 |
| `harl_i13` | `harcpu.103` | `hddispi.104` (CRC 387a5aad) | Italian 1.04 |
| `harl_l13` | `harcpu.103` | `hddisps.104` (CRC 2d26514a) | Spanish 1.04 |

Stern's ROM readme dates the initial 1.00 release to September 7, 1999 (with `hddispa.100`), 1.01 to September 20,
1.02 to September 30 and 1.03 to October 1, 1999. It lists the 1.04 display ROMs, `hddispa.104` $FC7C among them, in an
undated block before the 1.05 release of October 28, 2002, which "removed references to Sega Pinball, Inc." and added
the Stern logo. For 1.01, 1.02 and 1.03 it lists a `harcpuk` game ROM beside the `harcpu` ROM with the same checksum,
and does not say what the `k` variant changes; pinned PinMAME calls `harl_u13` "1.03 English". Thirteen harness runs booted
`harl_a13`; no other Sega set was run.

## Controller platform and address topology

- **Switches.** Matrix 1-64 is sequential (column = (n - 1) / 8 + 1). 9, 10, 38-40, 47, 63 and 64 are NOT USED, and
  the 1.03 Switch Test names them so. 1 and 8 are cabinet buttons: on a USA machine the extra right button (8) asks for
  the up/down post; on a UK machine the left (1) and right (8) Post Save buttons ask for the outlane deflectors, and
  both together for the post. 2, 3 and 7 are optional coin positions (3 and 7 Future Use). The dedicated inputs are -3
  memory protect, -2/-1/0 the red/green/black service buttons (DS-6/7/8), 84 left button (DS-1), 83 left EOS (DS-2), 82
  right button (DS-3), 81 right EOS (DS-4) and 88, the NOT USED DS-5. The cabinet wiring diagram draws an upper right
  flipper button on DS-5 (CN6-7), but the switch table, the flipper circuit diagram and the 1.03 ROM's Dedicated Switch
  Test ('#5 NOT USED / CN6-7 GRY-GRN CN6-1 BLK') all name it NOT USED, and holding 88 switched no coil on in attract mode
  or play while holding 8 raised the post; 85-87 reach no input.
- **DIP switches.** SW300 positions 1-5 select the country; the manual's nineteen charts never turn 6-8 on. Three of
  `sega.vbs`'s country labels (0x05 UK, 0x09 Japan, 0x0d Brazil) name other countries than this game's chart (Finland,
  Denmark, Australia; the UK is 2, 3 and 4 on); follow the chart.
- **Solenoids.** Public 1-32 are Q1-Q32 except the flippers: `se_solenoid_w` masks Q15 (left) and Q16 (right) off public
  15/16 and publishes them at 47 and 45, and `core.c` synthesizes 48 and 46 from those. Bind the left flipper coil at 48
  and the right at 46; 45 and 47 are their power-phase states. Public 15 is PinMAME's fast-flip / game-on state
  (`sega.vbs`'s `GameOnSolenoid = 15`), but `MACHINE_INIT(se)` places the fast-flip byte only for the Stern CPU 3.00
  set and for none of the seven Sega sets, so 15 never rises for this machine: no run saw it, although the gameplay run
  enabled the flippers. A recreation that needs a game-on signal must derive it elsewhere. 15, 16, 33-44, 49 and 50 are
  unused. Q8 (European token dispenser), Q21-Q22 (UK outlane deflectors) and Q24 (coin meter) are optional equipment;
  the up/down post Q23 is standard.
- **Lamps** 1-80 run across each row (lamp = (row - 1) x 8 + column). 55, 56, 60-64 and 73-80 are NOT USED, and outside
  the Single Lamp Test no run saw them lit. 47 is the Launch button's lamp in the cabinet. **G.I.** is one relay at
  public 0.

## The 1.03 ROM's service tests

Five harness runs walk the Portals service menu with the service buttons and read every frame they cite;
`tools/seeds/sega/harley-davidson-1999-frame-readings.json` pins each reading to its frame's pixel SHA-256.

- **Switch Test.** For about a second after a matrix switch closes the display prints `NAME / DRIVE RETURN #NN`, for
  example `LT BUTTON (UK ONLY) / GRN-BRN WHT-BRN #01`. One run closes 1-64 in turn; the motorcycle-trough positions
  41-44 and the super VUK 45 print their names only about a second after they close, so a second run reads those five
  later.
- **Single Lamp Test.** Each press steps to the next lamp, lights it and prints `NAME / DRIVE RETURN #NN`; 52-56 and
  every other NOT USED cell print `NOT USED`. After lamp 80 the display prints `NONE`, then starts again at 1.
- **Single Coil Test.** Each selection prints `#N NAME / POWER CONTROL` for Q1-Q24 and `#F1`-`#F8` for the flash lamps
  Q25-Q32, with the power wire the coil chart prints and the drive wire. Firing each driver pulsed its own public
  address, Q15 raised 47 and 48 and Q16 raised 45 and 46.
- **Dedicated Switch Test.** As on Stern's 4.00 ROM: `#1 LEFT FLIPPER BUTTON / CN6-2 GRY-BRN CN6-1 BLK` (84), `#3 RIGHT
  FLIPPER BUTTON / CN6-4 GRY-ORG CN6-1 BLK` (82) and `#5 NOT USED / CN6-7 GRY-GRN CN6-1 BLK` (88).

Every name matches the manual once spacing and case are set aside, except these spellings, which the curator lists and
refuses to extend silently:

| Device | Manual | 1.03 ROM |
| --- | --- | --- |
| Switch 1 | LEFT BUTTON (UK ONLY) | LT BUTTON (UK ONLY) |
| Switch 8 | RIGHT BUTTON (SKILL) | RT BUTTON (SKILL) |
| Switch 41 | M-CYCLE TROUGH #4 (TOP) | M-CYCLE TROUGH #4 |
| Switch 44 | M-CYCLE TROUGH #1 (BOT) | M-CYCLE TROUGH #1 |
| Lamps 7, 8 | SUPER JACK-PO T (RED), (GRN) | SUPER JACKPOT (RED), (GRN) |
| Lamps 25, 26 | M-CYCLE GRN LIGHT, YEL LIGHT | M-CYCLE GREEN LIGHT, YELLOW LIGHT |
| Lamps 29, 30 | RT, BOT TURBO BUMPER | RIGHT, BOTTOM TURBO BUMPER |
| Lamp 32 | SPEEDO- METER X2 | SPEEDOMETER x2 |
| Lamps 33, 34 | SUPER VUK GRN, YEL LIGHT | SUPER VUK GREEN, YELLOW LIGHT |
| Lamps 41, 42 | RT RAMP GRN, YEL LIGHT | RT RAMP GREEN, YELLOW LIGHT |
| Lamp 48 | LITE MYST- ERY RIDER | LITE MYSTERY RIDER |
| Lamps 49, 50 | RT ORBIT GRN, YEL LIGHT | RT ORBIT GREEN, YELLOW LIGHT |
| Lamp 67 | LITE MYSTERY... RT RETURN | LITE MYSTERY RT RETURN |
| Lamp 70 | RIDE AGAIN X2 | RIDE AGAIN #2 |
| Q31 | FLASH: RT. DROP TARGET X2 | FLASH: RIGHT DROP TARGET x2 |

The record's labels keep the manual's names; each device note quotes what the ROM prints.

## Lamps 52-54

The 3rd-edition Lamp Matrix Grid prints 52, 53 and 54 NOT USED, black with no bulb line, the lamp location drawing
marks none of them, and the 1.03 ROM's own Single Lamp Test names all three NOT USED. Yet `harl_a13` switches them
during play, as Stern's later ROMs do: in the gameplay run from about a second after the served ball reached the
shooter lane, usually all three at once and in step with lamp effects on 36, 37, 42 and 49, never in attract mode,
while 55 and 56 stayed dark. No retained script binds them. What that state reaches is unknown, so they carry
`availability = unknown`. The 1st-edition manual (780-5067-01, not retained) or a look under an early production
playfield would settle whether anything was ever fitted there.

## Production changes

- **Service Bulletin 113** (December 10, 1999). Some early machines have 5/8" ball guides without stamped flange ends
  at the left and right of the motorcycle entrance, where they protect the entrance optos; the ball can hammer them
  into the playfield. Kit 500-6408-67 replaces them with flanged guides 535-5356-19 (serials 148598-149648) and adds a
  support plate 515-8636-67 under the -16 plastic over the right stand-up target in front of the motorcycle (serials
  148598-150600), which "current production games include".
- **Service Bulletin 114** (February 11, 2000). Operator Alert #19 (Motor Relay) usually means a mechanical fault in
  the lift: the spring off the link, a binding link, a loose cam set screw, the cam catching the motor mounting screws
  or a dead spot in the motor. The cam is set to stop on the Up switch 35 and the Down switch 36, and the motor test's
  RUN and PULSE icons drive the relay Q19 with the power interlock switch pulled out.
- **Service Bulletin 121** (February 5, 2001). Kit 502-5003-67 adds a metal support plate under the -15 plastic at the
  left of the motorcycle, which cracks at the front near the right bumper.

<!-- stern-section: Switch polarity and names -->

<!-- stern-section: Ball handling -->

<!-- stern-section: Scoring parts -->

<!-- stern-section: Stop light -->

<!-- stern-section: UK equipment -->

<!-- stern-section: Lamps, flashers and general illumination -->

<!-- stern-section: Retained-table defects -->

<!-- stern-section: Spatial status and why the record stays partial -->

## Author construction checklist

- **Ball path.** Build the 4-ball trough with stacking opto, the auto-launch shooter lane, the motorcycle lift with its
  kick-out trough and entry opto, the under-trough and super VUK, the power scoop, the right ramp, the two orbits and the
  top-orbit magnet.
- **Motorcycle.** Make the lift a motor that runs while Q19 is on and reverses at each end, closing 36 at the bottom and
  35 at the top; start it down with 36 at 1. Admit balls to the kick-out trough only when the motorcycle is up.
- **Scoring parts.** Two 4-bank drop targets, four turbo bumpers, two slingshots, two flippers with N.C. EOS, four
  stand-up targets, the spinner, the four lanes and the up/down post.
- **Initial state.** Initialize 11-14, 36 and -3 at 1. Pulse 15 per kicked ball.
- **Bindings.** Bind Q15 at 48 and Q16 at 46; 45/47 are power phases, and public 15 never rises on a Sega set. Bind
  Q21-Q22 only for a UK build, Q8 only with a token dispenser and Q24 only with a coin meter. Leave 52-54 unbound until
  their load is known.
- **Displays and lights.** One 128x32 DMD in the cabinet. Recreate the 38 playfield G.I. bulbs and the two coin-door bulbs,
  all lamps, the stop light and every flasher bulb.
- **Early production.** Some early machines had ball guides without flanged ends at the motorcycle entrance, machines up
  to serial 150600 had no support plate under the -16 plastic, and the -15 plastic's plate came as a 2001 kit; build
  the guides flanged and the plates fitted unless recreating an unmodified early machine.

## Sources

- `identity.sega.harley-davidson.1999`: IPDB pages 4453 and 4455, retained under the Stern record's manuals directory;
  excerpt under `evidence/excerpts/sega.harley-davidson.1999/`. `identity.stern.harley-davidson.1999`, the Stern
  record's IPDB source, carries the 2nd- and 3rd-edition pages that two device notes quote.
- `manual.stern.harley-davidson.1999`: SHA-256 `a10e91542f9c8ab965d18908626114d1d03cba499f36fa47751045e8adae4731`, IPDB
  5277's 3rd-edition manual; excerpts under `evidence/excerpts/stern.harley-davidson.1999/`.
- `service-bulletin.stern.harley-davidson.rom-readme`: Stern's ROM readme (`abff199c...`), from the Wayback Machine.
- `service-bulletin.stern.harley-davidson.113`, `.114` and `.121`: the three bulletins from the Internet Archive.
- `service-bulletin.stern.harley-davidson.tech-brief-49`: Technical Brief 49 (`7605f4c4...`).
- `vpx-table.harley-davidson-1-2` and its embedded script (`eb0960bc...`), with the retained extraction and its manifest.
  The table runs the Stern CPU 3.00 set; every Harley-Davidson set shares `harlGameData`, so its bindings apply here.
- `vpx-script.6c9fb236b2931fc9` and `vpx-script.e101da5130f14724`: the pinned corpus scripts of a later table.
- `vpm-script-library.sega-vbs`: `sega.vbs` (`d6e508aa...`).
- `pinmame.sim.harley.46e1a01a0f73`: PinMAME's simulator for this game, a lead for the ball routes.
- `rom.sega.harley-davidson.1-03` and `runtime.harley-davidson.harl-a13`: thirteen LibPinMAME runs of `harl_a13`,
  summarized in `evidence/runtime/whitestar/harley-davidson-harl-a13-service-tests-and-gameplay.json`. Nine of them
  repeat the Stern record's harl_a40 scenarios step for step.
