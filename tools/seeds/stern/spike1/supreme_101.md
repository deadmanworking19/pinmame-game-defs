# Supreme (Stern, 2018) — partial candidate

## Current PinMAME adapter

The active adapter is PinMAME `46e1a01a0f73dc5ce163d98db1ae435883ecc450`. Virtual GAME ON is public solenoid 33; it represents an armed lower-flipper reflex, not a physical relay. Direct reads at 34-36 are aliases; the canonical plugin and aggregate address is 33. The current driver samples I/O at 1 kHz, retains short host switch edges, and keeps newly observed coil pulses for at least one frame. The modulated poll includes lower binary mirrors 45-48 because nSolenoids is at least 48. Plugin DIP group 6 now maps ordinals 1-8 to bank 0 bits 0-7 correctly. Lower EOS synthesis is unchanged. Historical runtime traces and ROM-table excerpts remain scoped to their original revision; this source audit adds no new gameplay observation or physical fitment evidence.

Source records: `pinmame.adapter.current` provides the pinned code and active-route excerpts; `pinmame.catalog.current` provides the current public driver descriptor. Both supplement the historical sources below.

This partial definition for `stern.supreme-x-stern.2018`, driver `supreme_101`, uses pinned PinMAME source, exact-ROM routing analysis, a retained LibPinMAME run, the supplied `supreme_008.vpx`, factory-label/display photographs and a photographed factory rule card. The VPX supplies observed sensor/effect proxies; its generic Basic VPW Example Table header does not identify its author or establish working status. The model label, backbox display and card rules are independently documented. Contact polarity, wiring, cabinet peripheral fitment, complete lighting quantities/positions and some mechanism behavior remain unresolved, so the record stays partial.

## Identity and physical evidence limits

The [retained OPDB snapshot](working-root:review-artifacts/spike1-2026-10-10/identity/latest-opdb.json), SHA256 `be658179b49b2bc02dce55d928c3d6a6afe6307e2b00a0ac7ffc1a745ac2d9f3`, has the exact `machines` record `G3EnZ-MePOV`: name “Supreme x Stern”, `physicalMachine=1`, manufacture date `2018-06-01`, manufacturer “Stern Pinball, Inc.” and IPDB `6609`. The source catalog independently identifies Supreme (1.01.0), Stern, 2018 in [spike1.c:970–991](https://github.com/vpinball/pinmame/blob/8e0f721e3df7a2b4e8a9d2f4454ac7a9aa1ced53/src/wpc/spike1.c#L970). These support this physical title identity. OPDB features, player count and image labels are secondary metadata and are not used to establish wiring or component quantities.

[IPDB machine 6609](https://www.ipdb.org/machine.cgi?id=6609) is retained in the 2026-10-26 research. Dean Grover's factory-label photograph establishes `PINBALL I-00PL * SUPREME 1`; his display photograph, corroborated by production photos, establishes the DMD's backbox location. PinMAME/runtime evidence supplies its 128x32 dimensions, controller index 0 and depth 4. Secondary IPDB feature prose and another title's manual are not used as Supreme wiring evidence.

## Exact artifacts and reproducibility

The historical routing/runtime evidence below is pinned to `8e0f721e3df7a2b4e8a9d2f4454ac7a9aa1ced53`. Supreme's extracted `game` is 4,599,307 bytes, SHA256 `bb435ed68a1492b339c2736e93d753caba2378ac09f33c2e70bdea5a80d9bf85`, CRC32 `681a3c00`, SHA1 `dc9cbf0a4204a3bbaecede3a5f5f9b1f9a2269c2`. The matching checked archive `supreme_101.zip` is 121,951,961 bytes, SHA256 `d0136f8997f02ef617014823b34e9e41140cfbe37af98cb3014ed878c7011c36`. The [full routing facts](working-root:review-artifacts/spike1-2026-10-10/rom-maps/supreme_101.json) have SHA256 `5e43fd949decd03843f9baa35d3e74fb17ae0095e76595f20940045796212f7c` and retain all row names, class bits, node positions, original device indices, source hashes and ELF table locators. The game program matches the source manifest and the archive's extracted `game` bytes; all source archive-entry names, sizes and CRC metadata match. Retained build/extraction logs report successful full archive checks; the table extractor does not claim a second independent payload CRC pass over every large image file.

The standalone [map log](working-root:review-artifacts/spike1-2026-10-10/supreme_101-map.log) has SHA256 `e05913b20ea9cae7ce63658237cc1ee49306b60590198342168498be47e07da1`. `spike1boot.exe` has SHA256 `f79c4f05ad9a293294651e674d8697e7637eae46d1a3bb6fa8c9f40233e42e24`; the retained extraction tool v1 has SHA256 `59e4d5940064443b1ad2c1d6aaf05b7a3a594e71b890ec3d4287989166b40446`. The full ROM-derived switch/coil/LED tables reconcile to printed counts `66/12/65`, with no duplicate switch/coil references, duplicate node positions or truncated names. The only repeated exported lamp references are 1, 2 and 3.

The [runtime run.json](working-root:review-artifacts/spike1-2026-10-10/runtime/supreme_101-api-r2/run.json) has SHA256 `de0bc286584d1e484217083db67e28da246b176809beaac454482c50d6b7f1a0`. The complete flushed [run.events.jsonl](working-root:review-artifacts/spike1-2026-10-10/runtime/supreme_101-api-r2/run.events.jsonl) has SHA256 `0a3e81a4f3f364bee1a2692c24fdc0e4f09e5c29182e951fe22bf1eecfbed190`; the [derived observations](working-root:review-artifacts/spike1-2026-10-10/runtime/supreme_101-api-r2/observations.json) have SHA256 `f5e1bc071c9fa78f3c4c722ae659aa3f563710381b99305be22bbab0c4916ee1`. The [manifest](working-root:review-artifacts/spike1-2026-10-10/runtime/supreme_101-api-r2/manifest.json) records every snapshot, fresh-state file, trace/log digest, command, timeout and exit status. The visually checked [DMD contact sheet](working-root:review-artifacts/spike1-2026-10-10/runtime/supreme_101-api-r2/dmd-contact.png) has SHA256 `1f89d39333a3e0d289bf9fcefdcb839da839d3e957c5e8fb1697e4adaddc86df`; raw PGM snapshots, rather than the composed sheet alone, preserve display pixels.

The native library `pinmame64.dll` has SHA256 `1875e0961759cbd21b566d31a60c7f9e7c59c26c7f1e0d21f97b1b50118db005`. Python 3.12.9 invoked the unchanged existing harness (SHA256 `49c5e733bf436a260c915d88e275189950d8ebcc55575f01ab2d153099e1dd44`) through the retained external recorder (SHA256 `41400f2bdf14a0bb50e14a2d3368e0058366c9c156bfb64bcc7e4ce60013c529`). The exact [scenario](working-root:review-artifacts/spike1-2026-10-10/runtime/scenarios-coins6/supreme_101.json) has SHA256 `98b11a14ddd1efdee203f021ae5f78eccc03d027cb14cbbe04221837f970f337`. The run began at `2026-10-10T19:15:58Z`, used its own fresh empty state, keyboard handling off, mechanics handling 1, a 70-second ready timeout, 25-second boot wait and 180-second process timeout. Physical-all output mask index/value was `2/2`, with approximately 10 ms polling. The process ran about 52 seconds and exited 0 without timeout or native crash.

## Controller inventory and emulator semantics

The definition enumerates every legal common switch converter position `0–95,101–132` (128), DIP configuration ordinals `1–8` (8), common solenoid route slots `1–32,45–48,51–72` (58), and Supreme's padded lamp envelope `1–136` (136). The exact title has 66 ROM switch rows, 12 ROM coil rows, 65 exported LED rows and 62 distinct exported lamp addresses. The API's returned capacities `72 solenoids / 624 lamps / 8 GI` are query capacities and are not physical inventory. Legal solenoid holes `33–44` and `49–50` are excluded. Lamp positions above this title's 136-channel envelope are not borrowed from another title.

Inputs 101–108 are virtual readback mirrors of DIP bank 0 bits 0–7 and are rewritten every frame. Use configuration ordinals 1–8 through LibPinMAME's bank API. The exact-head controller plugin's DIP accessor treats its ID as a zero-based bit index, so its ordinal mapping is shifted; no faithful plugin transport is declared for these configuration bindings. Service Select/Plus/Minus/Back use 109/110/111/112. DC SENSE 116 starts closed. Source conversion swaps Supreme's lower button/EOS references 8/10/9/11 with the core's internal flipper column, so recreation code must use Supreme's public references directly, not a WPC switch recipe.

A public state of 1 means logical closed in the subsystem. The subsystem then applies its ROM-table wire-level flags. `inversion_applied_by_emulator` is informational and must not be applied a second time. A “closed at rest” or “active high” annotation does not establish a normally-closed physical contact. No `normally_closed` field is asserted. Source startup logically closes 18, 19, 20, 21, 33, 49 and 116; these are the only declared `initial_active:true` inputs. They are firmware startup states, not a physical ball-count, opto or switch-polarity claim. The scenario retains these source-created startup states and then changes only the explicitly listed public inputs.

DIP mirrors and lower EOS 9/11 are virtual used inputs. The core synthesizes lower EOS after two VBLANKs from the flipper mirrors and overwrites direct EOS writes. The 62 legal switch positions absent from the exact ROM's switch vector are unused emulator slots, not proof of an unfitted physical part. All ROM-named switch routes retain physical switch type `unknown`.

Physical output routes remain `availability:unknown` because no physical source settles fitted loads. The four flipper mirrors are virtual used outputs. Forty-two solenoid slots and seventy-four lamp slots absent from the exact title's export maps are virtual unused output space: the source mapping/getter explains their zero state. Runtime silence alone was not used to classify any address unused. Known ROM labels and runtime activity do not establish physical load quantity or electrical wiring.

## Coil routes and custom traversal

| Public solenoid | ROM Driver Reference | Firmware node/position | Exact ROM name | Runtime scope |
| --- | --- | --- | --- | --- |
| 51 | 33 | 1/2 | COIN METER | Observed in bounded run |
| 52 | 34 | 1/3 | TICKET METER | Not exercised |
| 53 | 35 | 1/4 | TICKET DISPENSER | Not exercised |
| 4 | 4 | 8/0 | RT FLIPPER POWER | Observed in bounded run |
| 1 | 1 | 8/1 | TROUGH | Observed in bounded run |
| 10 | 10 | 8/2 | CONTROL GATE | Not exercised |
| 9 | 9 | 8/3 | DROP TARGET RESET | Not exercised |
| 2 | 2 | 8/4 | AUTO PLUNGER | Observed in bounded run |
| 3 | 3 | 8/5 | LEFT FLIPPER POWER | Observed in bounded run |
| 7 | 7 | 8/6 | LT/RT POP BUMPER | Not exercised |
| 5 | 5 | 8/7 | LT/RT SLINGSHOT | Observed in bounded run |
| 8 | 8 | 8/8 | BOTTOM POP BUMPER | Not exercised |

Custom public 51, 52 and 53 are allocated from Driver References 33, 34 and 35 in this exact ROM's device-table traversal order; the source does not sort them. Supreme's `nSolenoids` becomes 53. The word “number order” in source prose must not replace the actual traversal. There is no coil-table row at actual 6, 11–32 or custom 54–72. Outputs 45/46 mirror the right lower coil 4, and 47/48 mirror the left lower coil 3; either named power/hold coil would assert both mirror bits, but this exact table has only one POWER row per side. Neither the mirror pair nor the actual 255→30 duty sequence proves two windings.

Actual coil and LED levels are normalized to duty/255 in the core's modulated storage; LibPinMAME physical-all mode reports 0–255 byte levels. Binary consumers test nonzero. The virtual flipper mirrors remain binary copies even though this run's physical-all callback encodes their on state as 255. Direct binary `GetSolenoid` can return a noncanonical bit mask; consumers must test `!=0`, not equality with 1. The source's physical-all output count includes Supreme's mirrors because `nSolenoids=53`; this is title-specific and must not be extrapolated to titles with `nSolenoids=32`.

## LED routes, aliases and physical uncertainties

Every mapped LED is represented by an ordinary public lamp channel. No Supreme row has unavailable reference 0 or motor-drive class bit 0x08. The GI class rows use lamp 80/81/82/130; there is no separate public GI export (`nGI=0`). The label DROP TARGET FLASHER at 76 has ROM class 0x01; neither that label nor the class settles the physical light type. No RGB shared-emitter/channel-color/quantity metadata is inferred.

| Public lamp | Firmware node/position | Exact ROM row name(s) | ROM class bit(s) |
| --- | --- | --- | --- |
| 1 | 1/0; 8/3 | COIN ENABLE; LEFT OUTLANE | 0x10; 0x1 |
| 2 | 1/2; 8/4 | START BUTTON; LEFT INLANE | 0x1; 0x1 |
| 3 | 1/3; 8/5 | TOURNAMENT START; RIGHT INLANE | 0x1; 0x1 |
| 4 | 8/6 | RIGHT OUTLANE | 0x1 |
| 5 | 8/7 | SHOOT AGAIN | 0x1 |
| 10 | 8/18 | LEFT MODE | 0x1 |
| 11 | 8/19 | LEFT CENTER MODE | 0x1 |
| 12 | 8/20 | RIGHT CENTER MODE | 0x1 |
| 13 | 8/21 | RIGHT MODE | 0x1 |
| 14 | 8/8 | BONUS 1 | 0x1 |
| 15 | 8/9 | BONUS 2 | 0x1 |
| 16 | 8/10 | BONUS 3 | 0x1 |
| 17 | 8/11 | BONUS 4 | 0x1 |
| 18 | 8/12 | BONUS 5 | 0x1 |
| 19 | 8/13 | BONUS 10 | 0x1 |
| 20 | 8/14 | BONUS 20 | 0x1 |
| 21 | 8/15 | BONUS 30 | 0x1 |
| 22 | 8/16 | BONUS 40 | 0x1 |
| 23 | 8/17 | BONUS ? | 0x1 |
| 25 | 8/22 | 2X | 0x1 |
| 26 | 8/23 | 3X | 0x1 |
| 27 | 8/24 | 5X | 0x1 |
| 28 | 8/25 | DOUBLE SCORING | 0x1 |
| 30 | 8/26 | LEFT BOTTOM STANDUP | 0x1 |
| 31 | 8/27 | LEFT CENTER STANDUP | 0x1 |
| 32 | 8/28 | LEFT TOP STANDUP | 0x1 |
| 33 | 8/61 | RIGHT TOP STANDUP | 0x1 |
| 34 | 8/62 | RIGHT CENTER STANDUP | 0x1 |
| 35 | 8/63 | RIGHT BOTTOM STANDUP | 0x1 |
| 37 | 8/29 | LEFT ORBIT ARROW | 0x1 |
| 38 | 8/30 | LEFT ORBIT 25000 | 0x1 |
| 39 | 8/31 | LEFT ORBIT 10000 | 0x1 |
| 41 | 8/32 | LEFT RAMP ARROW | 0x1 |
| 42 | 8/33 | LEFT RAMP 25000 | 0x1 |
| 43 | 8/34 | LEFT RAMP 10000 | 0x1 |
| 45 | 8/44 | DROP TARGET LEFT | 0x1 |
| 46 | 8/43 | DROP TARGET CENTER | 0x1 |
| 47 | 8/42 | DROP TARGET RIGHT | 0x1 |
| 49 | 8/40 | LEFT SINGLE STANDUP | 0x1 |
| 50 | 8/41 | CAPTIVE BALL | 0x1 |
| 52 | 8/35 | TOP LEFT LANE | 0x1 |
| 53 | 8/36 | TOP CENTER LANE | 0x1 |
| 54 | 8/37 | TOP RIGHT LANE | 0x1 |
| 56 | 8/39 | CENTER ARROW | 0x1 |
| 57 | 8/38 | EXTRA BALL | 0x1 |
| 59 | 8/45 | SPINNER ARROW | 0x1 |
| 60 | 8/46 | SPINNER 10000 | 0x1 |
| 61 | 8/47 | SPINNER 5000 | 0x1 |
| 63 | 8/48 | RIGHT RAMP ARROW | 0x1 |
| 64 | 8/49 | RIGHT RAMP 25000 | 0x1 |
| 65 | 8/50 | RIGHT RAMP 10000 | 0x1 |
| 67 | 8/55 | RT INNER ORBIT ARROW | 0x1 |
| 68 | 8/56 | RT INNER ORBIT 10000 | 0x1 |
| 69 | 8/57 | RT INNER ORBIT 5000 | 0x1 |
| 71 | 8/58 | RIGHT ORBIT ARROW | 0x1 |
| 72 | 8/59 | RIGHT ORBIT 25000 | 0x1 |
| 73 | 8/60 | RIGHT ORBIT 10000 | 0x1 |
| 76 | 8/51 | DROP TARGET FLASHER | 0x1 |
| 80 | 8/0 | PLAYFIELD GI 1 | 0x2 |
| 81 | 8/1 | PLAYFIELD GI 2 | 0x2 |
| 82 | 8/2 | PLAYFIELD GI 3 | 0x2 |
| 130 | 1/1 | COIN DOOR GI | 0x2 |

Lamp 1 combines COIN ENABLE (node1/0, class0x10) and LEFT OUTLANE (node8/3, class0x01). Lamp 2 combines START BUTTON (1/2) and LEFT INLANE (8/4). Lamp 3 combines TOURNAMENT START (1/3) and RIGHT INLANE (8/5). Each address has one canonical definition binding with both row aliases retained. The binary lamp matrix ORs all rows whose level is nonzero; the modulated/physical level is overwritten by the later visited row, here the node8 playfield-labelled row. The public API does not expose row-specific identities, so observing address 1/2/3 does not prove which emitter is on or how many physical emitters share a load. Treat the alias behavior as an emulator projection requiring physical evidence before creating any physical fan-out.

All 62 mapped lamp addresses produced activity somewhere in the bounded run, including the GI-labelled addresses. This proves public runtime activity, not physical fitment or quantity. Lamps 6–9,24,29,36,40,44,48,51,55,58,62,66,70,74,75,77–79,83–129 and131–136 are absent from this exact title's exported LED map and carry unused virtual dispositions.

## Causal runtime steps reached

| Step | Exact public input action | ROM/API observation |
| --- | --- | --- |
| Boot | Retain source-created startup state; wait25s | DMD attract/high-score activity; index0 is128×32 depth4; no extra display announced. |
| Credits | LEFT COIN76, six300ms closures, each followed by1.5s settling | COIN METER51 emits255→0 per pulse. Saved frames show credits1,2,3,5,6,7 under fresh defaults. |
| Start/serve | START BUTTON13,120ms closure; wait4s+2s | Supreme title animation and repeated TROUGH1 output at210→0. COINDOOR START B.73 is a different unexercised input. |
| Simulated transfer | Open TROUGH418; wait0.4s; close SHOOTER LANE1; wait1s | Prior ROM serve is already present; trough output stops after sensor change. This is a harness transfer, not measured ball physics. |
| Launch | LAUNCH BUTTON15,150ms closure; settle1s | AUTO PLUNGER2 at191→0. |
| Ball departure | Open SHOOTER LANE1; wait1s | DMD BALL1, credits6, score00. |
| Left lower flipper | LEFT FLIPPER BUTTON8,500ms closure, settle0.8s | Actual3 at255→30→0; virtual47/48 at255→0. |
| Right lower flipper | RIGHT FLIPPER BUTTON10,500ms closure, settle0.8s | Actual4 at255→30→0; virtual45/46 at255→0. |
| Sling probe | LEFT/RIGHT SLINGSHOTS6,100ms closure, settle1s | LT/RT SLINGSHOT5 at194→0; saved score130 in BALL1. |
| Shutdown | API stop, no external forced termination | State2→1→3→0; stop returned with `PinmameIsRunning()==0`; process exit0. |

The run proves credited startup, a ROM-driven ball serve, simulated one-ball departure, lower flipper responses, a sling response and clean API shutdown. It does not prove a completed ball drain, a full game, multiplayer, service diagnostics, tilt/slam, all coin inputs, ticket behavior, drop reset, gate motion, bumpers, ramps, captive-ball behavior or scoring at every input. At approximately 10 ms polling, a short pulse may be missed. Host-written `GetSwitch` readback is harness/debug information and was never used as evidence of a ROM response or physical polarity.

## Mechanism inventory and recreation gaps

The structured mechanisms group verified runtime routes for trough/serve, shooter/launch, lower left/right flippers, the combined sling route and coin meter. They preserve candidate ROM groupings for combined left/right pop bumpers (input37/output7), bottom pop (38/8), LEFT/CENTER/RIGHT drop positions (40/41/42) with reset9, CONTROL GATE10, spinner46, captive-ball inputs45/50, ticket outputs52/53 with notch83, and ramp exits33/49. The grouping does not establish physical assemblies, quantities, series/parallel circuits or spatial placement.

Other exact firmware labels cover outlanes2/5, return lanes3/4, standups24–29/32/44, top lanes34–36, left orbit31, right inner orbit47 and right orbit48. Physical target construction and paths are unknown. Cabinet/service labels cover start13, coin-door start73, tournament74, tilt14, slam84, service109–112 and DC sense116; all except start13 remain unexercised. Eight-bit CPU DIP configuration remains public, but none of the eight individual DIP settings was exercised.

Supreme's source initializer uses no special home-switch linkage or limit-motor helper. `GetMech(0..3)` was zero at retained snapshots; the driver returns zero when no motor position is available. This does not prove absence of a fitted physical motor or mechanism. No mechanism-position simulation is asserted in this definition. There is no physical electrical relationship entry because connectors, power feeds, load fan-out and switch circuits remain unknown; causal runtime observations are described explicitly instead.

A Supreme primary manual, schematic/parts set or direct cabinet/playfield inspection is needed to establish fitted coin/ticket hardware, trough and ball counts, flipper assemblies/windings/EOS contacts, sling/pop shared circuits, gate/drop-bank assemblies, launcher geometry, physical lamp/GI/flasher types, emitter quantities, alias fan-out and normalized coordinates. An exact known-working recreation could add runtime behavior and mapping evidence, but source names, another title's manual and further lamp/coil API toggles cannot settle physical construction. A later complete gameplay/drain and mechanism exercise should retain its own fresh state, DLL/ROM/source hashes, explicit title references and raw trace.

## Provenance and import note

Public routing is sourced from the immutable [driver](https://github.com/vpinball/pinmame/blob/8e0f721e3df7a2b4e8a9d2f4454ac7a9aa1ced53/src/wpc/spike1.c) and [core](https://github.com/vpinball/pinmame/blob/8e0f721e3df7a2b4e8a9d2f4454ac7a9aa1ced53/src/wpc/core.c), whose full-file SHA256 values are respectively `756ecd840f234cf7a62f84ef331ccb8b61f0f1aeffc409bc7b776d6c037211c9` and `9ef4b590d31be77ffa21765faeec9df4e3a175c2597f9f7e8937091cea888d6a`. Exact locators and generation/inspection times are in the six source records. PinMAME source is BSD-3-Clause; ROM rights remain with their owners. The retained artifacts contain hashes, derived table facts, runtime metadata and display snapshots; ROM bytes must remain outside the repository. OPDB provides identity metadata and does not grant redistribution rights to its linked images.

The retained VPX source is now recorded through portable compact excerpts and an external reproducible extraction manifest. It supplements rather than replaces the full original hash chain. Schema and semantic validation can run without optional evidence roots; the evidence-enabled gate checks the exact retained VPX, script, and manifest. The `partial` coverage and unknown physical fields survive this enrichment. No independent review or author-ready promotion is claimed.

Source `spike1.libpinmame.8e0f721e3df7` pins the plugin DIP indexing implementation; the canonical physical DIP group uses LibPinMAME bank/bit routing in the controller profile.

## Retained source records

External locators prefixed `working-root:` resolve under the configured sibling `pinmame-game-defs-working-dir`. Portable factual excerpts carry their own fail-closed repository digests; source-owned PDFs, ROMs, frames and tables remain external.

- `supreme.vpx.table.008` and `supreme.vpx.script.008` identify the supplied
  `supreme_008.vpx`, its `vpxtool git:v0.33.3` extraction and compact I/O
  excerpts. The original VPX SHA-256 is
  `444c21186425f23c173dece87fe9f683e2ee5c101e76271bf1d2339d1920edd9`; its
  script SHA-256 is
  `f2bb8a48bd0aa49310d7e7e8bc165757d59d168110815ac1712dcc971e7a34ca`.
  The external complete extraction manifest has 565 files, 64,800,271 bytes,
  and digest `9f4af73ce3091bde3c61ff734feb92a3ec48f113d57327bc8142e2b6905b41bb`.
  It is user-supplied recreation evidence only: no physical construction,
  license, original table author, or known-working claim is inferred.

- `pinmame.catalog.8e0f721e3df7` (pinmame_catalog): `756ecd840f234cf7a62f84ef331ccb8b61f0f1aeffc409bc7b776d6c037211c9`. src/wpc/spike1.c:970-991; CORE_GAMEDEF(supreme,101) and exact ROM manifest; catalog metadata reproduced by PinmameGetGames. Inspected 2026-10-10T19:33:29Z.
- `spike1.driver.8e0f721e3df7` (pinmame_core): `756ecd840f234cf7a62f84ef331ccb8b61f0f1aeffc409bc7b776d6c037211c9`. src/wpc/spike1.c:191-225 (switch/lamp conversion),259-313 (DIP/switch/output synchronization),511-564 (coil allocation, LED export and initial switch state),685-707 (title limits/layout),970-991 (Supreme exact title). Full-file source SHA256; inspected 2026-10-10T19:33:29Z.
- `spike1.core.8e0f721e3df7` (pinmame_core): `9ef4b590d31be77ffa21765faeec9df4e3a175c2597f9f7e8937091cea888d6a`. src/wpc/core.c:1778-1858 (button/EOS synthesis),2197-2304 (direct/binary reads),2336-2445 (changed output paths),2619-2625 (flipper mask); full-file SHA256, inspected 2026-10-10T19:33:29Z.
- `supreme.rom.routes.101` (rom_static_analysis): `5e43fd949decd03843f9baa35d3e74fb17ae0095e76595f20940045796212f7c`. Exact full routing facts: switches/coils/leds columns+rows, controller, validation and provenance. ELF mixed table VA 0x2bf06c, stride 24; game SHA256 bb435ed68a1492b339c2736e93d753caba2378ac09f33c2e70bdea5a80d9bf85, CRC32 681a3c00, SHA1 dc9cbf0a4204a3bbaecede3a5f5f9b1f9a2269c2. Archive SHA256 d0136f8997f02ef617014823b34e9e41140cfbe37af98cb3014ed878c7011c36. Map log SHA256 e05913b20ea9cae7ce63658237cc1ee49306b60590198342168498be47e07da1. Extractor v1 SHA256 59e4d5940064443b1ad2c1d6aaf05b7a3a594e71b890ec3d4287989166b40446; spike1boot.exe SHA256 f79c4f05ad9a293294651e674d8697e7637eae46d1a3bb6fa8c9f40233e42e24. Facts artifact retained 2026-10-10T19:04:46Z; 66/12/65 ELF rows match logs and printed counts.
- `supreme.runtime.api-r2` (runtime_scenario): `de0bc286584d1e484217083db67e28da246b176809beaac454482c50d6b7f1a0`. Fresh-state public LibPinMAME scenario started 2026-10-10T19:15:58Z, process 26292, 52 s, exit 0. Physical-all mask index/value 2/2; approximately 10 ms polls; keyboard off; mechanics=1; ready timeout70s, bootwait25s, supervisor timeout180s. Scenario SHA256 98b11a14ddd1efdee203f021ae5f78eccc03d027cb14cbbe04221837f970f337. DLL SHA256 1875e0961759cbd21b566d31a60c7f9e7c59c26c7f1e0d21f97b1b50118db005. Python3.12.9; harness SHA256 49c5e733bf436a260c915d88e275189950d8ebcc55575f01ab2d153099e1dd44; external recorder SHA256 41400f2bdf14a0bb50e14a2d3368e0058366c9c156bfb64bcc7e4ce60013c529. Step events and snapshots, solenoid/display callbacks and shutdown. Complete JSONL SHA256 0a3e81a4f3f364bee1a2692c24fdc0e4f09e5c29182e951fe22bf1eecfbed190; derived observations SHA256 f5e1bc071c9fa78f3c4c722ae659aa3f563710381b99305be22bbab0c4916ee1. GetSwitch host readback is not ROM evidence.
- `supreme.identity.opdb` (human_review): `be658179b49b2bc02dce55d928c3d6a6afe6307e2b00a0ac7ffc1a745ac2d9f3`. machines[opdbId=G3EnZ-MePOV]: Supreme x Stern, physicalMachine=1, manufacturer Stern Pinball Inc., manufactureDate2018-06-01, ipdbId6609, display dmd, record updated2022-01-26. Selection read with PowerShell ConvertFrom-Json on 2026-10-10T19:33:29Z; snapshot retained2026-10-10T19:02:39Z. OPDB identity authority only; features/playerCount/images are not primary wiring or physical quantity evidence.
- `spike1.libpinmame.8e0f721e3df7` (pinmame_core): `96739dc787262e9d6379c8c7eb311209e061c389b5b63d0c9997116d910e0777`. Get/SetDIPSwitchState2074–2092 and Plugin StateMapping2419–2424; plugin bit indices use srcId directly while published IDs are one-based.


## Verified factory label, display and production rule card

`supreme.factory-model-photo` records Dean Grover's IPDB 6609 photo 75062 of
the prototype label: `PINBALL I-00PL * SUPREME 1`. Its serial and voltage
rating apply to that example. `supreme.backbox-photo` (photo 75054), the
retained production photographs and current PinMAME display topology settle
the single 128x32 display at controller index 0 in the backbox. Its spatial
record is therefore `not_applicable/cabinet_or_service`, with validated
provenance. The display-inventory requirement is complete; the machine remains
partial for the other declared requirements.

`supreme.factory-rule-card` is OCPinballs's production-machine photograph,
Pinside ad 124610/photo 2639645. A curator visually checked all ten bullets
on the original apron card. The portable excerpt
`evidence/excerpts/stern.supreme-x-stern.2018/physical-web-research.md`
paraphrases the complete region and records the original hash, dimensions and
crop. The rules cover lightning targets qualifying Supreme shots, Supreme
scoring progression, Meteor Shower spinner scoring, top-lane timed double
scoring, seven-star bonus multipliers, extra ball after two Supreme shots,
pop-driven value/shot changes, trapped-ball Galaxy multiball, add-a-ball from
the target above the trapped ball and sequential-shot combination awards.

`supreme.programmer-tutorial-lead` retains the browser's automatic transcript
of Colorado Pinball Collective's *Supreme pinball with Dean Grover*. Its
description identifies the game's programmer. The ASR lead explains passive
capture/replacement serve (2:53-3:16), drop-bank/sign multiball and an escape
path without electrical drop-down (3:25-3:49), the final timed multiball
(4:02-4:26), open-sided second-ball capture (12:31-12:46) and linked slings
(49:08-49:25). The audio and speaker attribution were not checked: these are
qualified reconstruction leads, not validated electrical assertions.

The retained research includes both Pinside club pages, all 15 launch-thread
pages, production ads 124610 and 192007, the IPDB page/prototype photographs,
Stern's manuals index and direct Pinside searches for Supreme manual,
schematic, wiring, gate and opto information. No title-specific factory
wiring/parts pages were located. None of the production photos show cabinet
internals or the playfield underside. Primary photos and the factory rule
card resolve the facts above; they cannot settle physical switch normal
states, fitted coin/ticket equipment, complete trough hardware, gate-coil
direction or every lighting emitter's quantity and position. Those concrete
gaps still prevent author-ready promotion. A manual or direct physical
inspection is needed to settle them.

A further primary photograph, Grailed listing 69068187/photo 4, clearly shows
the factory label `INSTALL 4 BALLS` below the apron. Source
`supreme.factory-ball-label` and its complete label excerpt independently
corroborate four installed balls for that photographed example. This settles
an installed-ball instruction; it does not prove the trough's number of
sensor positions, jam hardware, opto/contact construction or firmware variants.

## Shared-design comparison with Spider-Man The Pin

The official donor manual 780-50H8-00 is now a qualified reference, not excluded
merely because the artwork/title differs. `supreme.shared-design.manual` and
`supreme.shared-design.crosswalk` retain the complete switch/coil/light rows
and a deterministic exact node-position/public-address comparison. It finds
56 shared switch routes, all 12 coil routes and all 65 LED rows. All common
public addresses and LED class bits agree; 72 literal name changes remain
visible instead of silently replacing Supreme labels with Spider-Man labels.
The manual reconciles 51 switch rows (including 9 CPU C-namespace rows), 9
playfield coil rows and 61 playfield lighting rows. Donor component types and
parts are available in each affected device's explicitly qualified physical
notes, with full connector/wire cells preserved in the comparison excerpt.
They are candidate references, not confirmed Supreme harness or part fields.

The two games are not electrically identical in every respect. Tilt public 14
moves from donor node 8/27 to Supreme node 1/14; launch public 15 moves from 8/26
to 1/15. Eight additional Supreme node 1 switch routes concern ticket notch,
tournament start, five coin channels and slam tilt. Generic node 1 coin/ticket
coil routes remain unconfirmed physical fitment even though both firmwares
contain them. Public lamp 1/2/3 collisions still combine distinct node 1 cabinet
and node 8 playfield rows; the donor's playfield rows prove no cabinet load.
Supreme's photographed manual plunger/coin-door cabinet and 128x32 DMD differ
from the donor's cabinet controls and 64x32 RGB transport. Node firmware also
differs (donor 0.19.1, Supreme 0.22.0). No ROM interchangeability is asserted.

`donor-assemblies.md` transcribes the complete pages 21-22 assembly tables.
These identify candidate trough, auto-launcher, flipper, slingshot, bumper,
drop-bank, gate and spinner assemblies without assigning their part numbers
or quantities to Supreme. Existing Supreme geometry and the photographed
four-ball installation label remain independent evidence; they do not settle
all underside components or emitter positions. Physical wiring stays candidate,
contact polarity and cabinet fitment stay unresolved, and the record is partial.

## Completed exact driver mapping

`supreme.archive.identity.current` and `supreme.driver.identity.current`
record a fresh independent decompression
of every member of the authorized Supreme archive: all 10 payloads match the
pinned current source's size, CRC32 and SHA1, and have their own SHA256. The
retained archive matches the user's original archive byte-for-byte. The
complete current initializer/manifest/driver declaration is excerpted in
`current-driver-identity.md`; the catalog assigns the one supported Supreme
driver, `supreme_101`, exactly once to this physical record, with no missing
clone. Existing exact-ROM routes and retained runtime remain pinned to their
own revisions. This resolves `driver_mapping`, independently of the donor
hardware assumptions. It does not settle the separate physical-compatibility
or variant-differences requirements. Eight requirements remain, so the generated
completion score is 50%, still partial.
