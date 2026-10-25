# Pabst Can Crusher (2016)

## Current PinMAME adapter

The active adapter is PinMAME `46e1a01a0f73dc5ce163d98db1ae435883ecc450`. Virtual GAME ON is public solenoid 33; it represents an armed lower-flipper reflex, not a physical relay. Direct reads at 34-36 are aliases; the canonical plugin and aggregate address is 33. The current driver samples I/O at 1 kHz, retains short host switch edges, and keeps newly observed coil pulses for at least one frame. The modulated poll includes lower binary mirrors 45-48 because nSolenoids is at least 48. Plugin DIP group 6 now maps ordinals 1-8 to bank 0 bits 0-7 correctly. Lower EOS synthesis is unchanged. Historical runtime traces and ROM-table excerpts remain scoped to their original revision; this source audit adds no new gameplay observation or physical fitment evidence.

Source records: `pinmame.adapter.current` provides the pinned code and active-route excerpts; `pinmame.catalog.current` provides the current public driver descriptor. Both supplement the historical sources below.

## Identity

Machine `stern.pabst-can-crusher.2016`, driver `pabst_101`, OPDB `GRYX4-MRjVP`, IPDB `6335`. Coverage remains partial; no author-ready claim.

Every legal public switch0–95/101–132, DIP1–8, solenoid1–32/45–48/51–72 and lamp1–80 has exactly one disposition. Printed identities remain aliases; physical matching uses node/channel positions. CPU semantic mapping preserves original numbering anomalies.

Factory PDF `Stern_2016_The_Pabst_Can_Crusher_Service_and_Operation_Manual.pdf`, SHA-256 `9ee381bce70e70e7c42ad60ba13bd9a62cf65b7ce00611701a712670cea0769e`. Source-owned documents remain external; the full reviewed factual table regions and construction supplements are preserved in the source-linked portable excerpts below.

## Recreation evidence and limits

- Full scanned reference regions were visually transcribed: Driver35 rows on PDF/folio12; Switch71 rows on12,13,15; Light78 rows on15,17 including wholly blank77/78; Motor15 rows17–31 on18. All authoring columns, literal spaces/dashes and wrapped cells retained.
- Table of contents gives Driver11 but the driver table is PDF/printed folio12; page11 is the driver diagram. Switch diagram14 and light diagram16 were also visually inspected.
- Motor Reference17–31 repeats Driver Reference17–31 as internal Node11 LP15..1 reel enable/phase channels, not physical public coil slots. All Motor Node Ext. and Light Color cells are blank, not dashes.
- CPU manual numbering skips0-SW-1: C1=0-SW-0, C2..C8=0-SW-2..8, C9..C12=0-SW-9..12. This does not alter exact ROM/public CPU101..112.
- CPU service wiring conflict: Switch Reference p15 CN25 Select/Plus/Minus/Back pins4/3/2/1 and ground6 BLK with515-1963-XX; direct mapping p19 pins1/2/3/4 and ground11 BLK-WHT with individual180-5192 parts. The p20 schematic agrees with4/3/2/1 and ground6. Both printed mappings are preserved without choosing a canonical pinout.
- Source PN conflict: Switch17 lists515-0215-00 tx/515-0215-01 rx, while p36 long-range opto assembly lists500-0215-00 emitter/500-0215-01 receiver. Do not silently normalize printed PN prefixes.
- P39 Ball Shooter Assembly heading repeats500-7286-00, also the Trough Coil Assembly label. Its exploded shooter construction differs from the trough; label anomaly is retained.
- P26 lower LED extension heading says9-LAMP but its drawing labelsD1..D10; light reference provides tenNode11B channels. No emitter count inferred from the inconsistent heading.
- Only explicit multiplicities are retained: Light2/3 flipper x2,75 GI Reels x8 and76 Coin Door GI x2. Physical score/credit reels and the mini LCD with unknown mounting location are distinct from the PinMAME128x32 DMD transport.
- Pabst model500-55D9-01/manual780-50D9-00 is printed on cover. Its own Pabst white bonus lights, bumper PNs and Start Button180-5174-00 are preserved; Tilt Pendulum PN is blank.

Own-title flipper BOMs explicitly print180-5149-00 SWITCH - END OF STROKE N/C. Matched lower EOS records set normally_closed=true while remaining virtual public transport. All other construction polarity, pulse flags and unprinted quantities remain unset.


## Physical topology and behavior

### Four physical score reels and one credit reel

P36 score bank511-7614-00 has four511-7648-00 score reel assemblies and eight520-5307-00 white LED boards; credit bank511-7615-00 has one511-7648-01 credit reel and one white LED. Individual reel has direct shaft041-5105-00 unipolar stepper motor,515-9819-00 reel,535-1131-00 motor bracket and one520-6960-00 opto home sensor. Switch46..50 names Credit,1s,10s,100s,1000s homes. P28 controller520-6961-00 receives Node11 LP enable/phase channels and supplies two polarities for each physical motor phase. CN6 home inputs return to CN5 home outputs, while CN5pin7 exposes one aggregated M1 OCP/OCP signal. P26 sensor pinout explicitly supplies5V/signal/ground. This proves five separate actuators and five home inputs; the internal channels do not bind independently as public coils. Ball path is inapplicable to these backbox mechanisms.

Unresolved: No step/digit calibration, rotation direction, enable/phase sequence, default digit, startup homing order, home polarity, current-limit semantics, jam/retry/reset timing or calibrated motion rate is established.

### Mini diagnostics LCD, mounting unknown

P28 names Mini Diagnostics Display520-6964-00 and draws128x32. CN4pin1 provides+5V and pin4 ground; CN7 uses14-pin ribbon036-8045-132 (11ft). The small physical LCD supplements the mechanical reels. PinMAME reports128x32 DMD transport for this LCD; it does not prove a physical backbox DMD.

Unresolved: Full pixel-to-LCD software routing, physical mounting locator, boot display content and brightness behavior need additional evidence.

### Manual shooter, trough and top eject

P39 shooter drawing has515-6557-00 rod,266-5001-04 long compression spring,266-5010-00 short spring,545-0902-02 red beehive knob and545-5276-00 rubber tip. Trough500-7286-00 has26-1200 coil090-5044-ND,515-7309-01 plunger,266-5020-00 conical spring,515-1021-01 coil bracket,535-5203-03 retainer and545-5076-01 sleeve. P41 30-degree eject500-6511-03-ND also has26-1200 coil090-5044-ND,515-7197-00 plunger and266-5020-00 spring. Reference output6 Trough,5 TopEject, switches5 ShooterLane,16 CenterDrain,17 TroughOpto and20 TopEject identify separate electrical roles. Springs establish return components; no pulse duration is derived from them.

Unresolved: Complete ball path/capacity, default ball occupancy, exact switch-to-ball association, launch/eject velocities, timing and jam/retry/reset sequence remain unresolved.

### Paired leaf target assembly, bumper upper/body subassemblies and knocker

P39 bullseye511-7581-00 includes two180-5231-00 leaf switches per target body; switch22/23 names Right Target Outer/Inner and40/41 names Left Target Outer/Inner. P41 bumper516-0033-88 documents the upper/body subassembly: cap, body, skirt, spring266-5048-00 and white LED520-5307-03. This six-row BOM region does not include the lower actuator assembly; it does not prove a passive complete bumper. The own Driver Reference p12 separately documents four driven26-1200 pop-bumper circuits, outputs9–12, each with coil090-5044-ND. P39 knocker511-1027-00 has26-1200 coil090-5044-ND,515-7318-00 plunger and266-5020-00 spring, matching reference16 Knocker.

Unresolved: Contact ordering, physical normally-closed construction, impact travel, default skirt position, knocker timing and jam behavior are not specified.

### Lower flippers

Own-title PDF/printed folio38 supplies both complete assemblies, NC EOS, coil, plunger/crank, stop and return spring. Actual ROM coil identities are retained in the structured mechanisms.45/46 right and47/48 left are virtual binary OR mirrors; they do not add independent windings. Public lower EOS is synthesized; physical NC construction does not authorize driving the synthesized state.

### Physical reels, internal phase controls and mini LCD

Four physical score reels and one credit reel belong in the mechanism inventory. Manual Driver17–31 are Node11 LP15..1 enable/phase signals for internal stepper control, withheld from ordinary public output export. Public solenoids17..31 are zero slots; never bind reel phases there. Controller520-6961-00 supplies five two-phase motor connections and five opto-home circuits; current-limit/OCP pin labels remain literal. Small520-6964-00 LCD uses128x32 drawing label and14-pin ribbon036-8045-132. The128x32 PinMAME DMD callback is its transport, not evidence for a physical backbox DMD. This draft uses schema video for the physical LCD and leaves its physical mounting location and normalized coordinates unresolved.

GetMech ordering is subsystem motors, then steppers, then registered limit motors, and an absent entry also returns zero. The retained harness samples only indices0..3 and does not itself establish all five reel ordinals, digit calibration, phase direction, startup homing or jam recovery; those remain explicit gaps.

## Exact runtime observations

API run started `2026-10-10T19:22:21Z`, source revision `8e0f721e3df7a2b4e8a9d2f4454ac7a9aa1ced53`, library SHA-256 `1875e0961759cbd21b566d31a60c7f9e7c59c26c7f1e0d21f97b1b50118db005`, observation SHA-256 `73a9a5c93b8d277d57273d151b776ed3210806ee08b7a437235e7af79b3ee765`. Fresh state; physical-all mask2=2;10ms polling. These are emulator observations, not physical polarity or fitment proofs.

Observed solenoid addresses: [1, 2, 3, 4, 6, 8, 45, 46, 47, 48]. DMD layout0:128x32,4-bit. Changed frames: {'0': {'changed_frames': 177, 'recorded_events': 177, 'suppressed_events': 0}}. No activity at an address is not evidence of absence; shorter pulses can be missed.

- Step7 start: START BUTTON: 6 [155, 0, 155, 0, 155, 0, 155, 0, 155, 0, 155, 0].
- Step8 post-start serve observation: 6 [155, 0, 155, 0, 155].
- Step9 remove one ball from TROUGH OPTO after attempted serve: 6 [0].
- Step12 left flipper button: 1 [255, 0], 3 [255, 0], 47 [255, 0], 48 [255, 0].
- Step13 right flipper button: 2 [255, 0], 4 [255, 0], 45 [255, 0], 46 [255, 0].
- Step14 LEFT SLINGSHOT: 8 [200, 0].

Full raw events, observations, DLL/scenario/ROM hashes and run manifest remain under `runtime/pabst_101-api-r2`. A post-serve synthetic trough-to-shooter transfer is conditional gameplay evidence; host write/readback alone is not a ROM response.

## Manual devices without a proven public binding

| Table / PDF | Printed ID | Name | Circuit | Disposition |
| --- | --- | --- | --- | --- |
| driver_reference / 12 | 17 | Credit Reel Enable | 11-LP-15 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 12 | 18 | Credit Reel Phase 1 | 11-LP-14 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 12 | 19 | Credit Reel Phase 2 | 11-LP-13 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 12 | 20 | 1s Reel Enable | 11-LP-12 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 12 | 21 | 1s Reel Phase 1 | 11-LP-11 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 12 | 22 | 1s Reel Phase 2 | 11-LP-10 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 12 | 23 | 10s Reel Enable | 11-LP-9 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 12 | 24 | 10s Reel Phase 1 | 11-LP-8 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 12 | 25 | 10s Reel Phase 2 | 11-LP-7 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 12 | 26 | 100s Reel Enable | 11-LP-6 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 12 | 27 | 100s Reel Phase 1 | 11-LP-5 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 12 | 28 | 100s Reel Phase 2 | 11-LP-4 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 12 | 29 | 1000s Reel Enable | 11-LP-3 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 12 | 30 | 1000s Reel Phase 1 | 11-LP-2 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 12 | 31 | 1000s Reel Phase 2 | 11-LP-1 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 12 | 33 | Shaker motor(opt) | 1-DR-0 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |

## Remaining gaps

Unresolved switch construction polarity other than positively printed EOS; spatial placement with x0left/x1right/y0rear/y1apron; full ball path/capacity/default occupancy; calibrated travel/velocity; step/digit calibration; exact startup/homing/return conditions; pulse/hold timing; jam/retry/reset behavior; optional fitment and unreviewed edition differences. No numeric geometry or RGB emitter quantity is invented.


Acquisition times, source manifest reconciliation, portable excerpt imports and independent root review remain pending, so coverage retains provenance and other stated partial blockers. Schema/full address/ID/reference/EOS checks passed externally; canonical semantic and evidence gates must run after import.


## Final retained disagreements and validation

- Switch Reference p15 assigns service Select/Plus/Minus/Back CN25 input pins 4/3/2/1, ground pin 6 BLK; direct CPU mapping p19 assigns pins 1/2/3/4, ground pin 11 BLK-WHT. No canonical service contact pinout selected. Resolution path: compare factory harness/revision documentation or inspect actual CN25 and service-button assembly. Public CPU functions 109–112 are separately established by exact ROM routing.
- Switch Reference p13 Trough Opto prints 515-0215-00 tx / 515-0215-01 rx; the long-range opto assembly BOM p36 prints 500-0215-00 emitter / 500-0215-01 receiver. The common suffix and assembly class suggest a prefix discrepancy, but exact assembly-to-trough fitment is not independently proven. Both literal assertions are retained; no canonical sensor PN selected. Resolution path: consult factory revision/parts documentation or inspect the actual trough sensor and its assembly marking.
- The manual CPU DIP/service numbering omits 0-SW-1 and shifts the subsequent printed addresses; exact ROM Node 0 positions 0–7 mirror physical DIP ordinals 1–8 as public 101–108 and positions 8–11 are Select/Plus/Minus/Back public 109–112. Canonical public bindings follow verified ROM routing; source-literal addresses remain aliases. Resolution path: check factory CPU mapping documentation or exact machine wiring to resolve the printed numbering discrepancy; do not remap the API from printed IDs alone.

JSON schema, repository machine semantic validation (without repository-relative file checks), controller group validation, complete legal-address disposition, unique identifiers, mechanism references and own-title EOS N/C gates passed. Portable excerpt and knowledge-path existence/hash checks are deferred until the root imports exact files. Coverage remains partial.

Peer review correction: exported solenoid51–53 are factory Digital Out meter/ticket control signals. Their public solenoid group/address and literal wiring remain; canonical IDs use control.* and kind=control_signal. No meter coil winding is inferred.

LCD mounting gap: own factory controller/display pinout establishes LCD520-6964-00,128x32, supply and ribbon, but does not identify its installed mounting position. Physical location and normalized coordinates are unknown; the optional physical_location field is omitted. Pinned PinMAME spike1.c describes an apron LCD as an emulator model description, not an own-title physical placement authority. Obtain an exact-title factory placement/assembly locator or verified own-machine placement evidence before assigning the display to playfield or cabinet/service space.

Recorded, nonblocking distinctions under INSTRUCTIONS.md: conflict.cpu-service-pinout, conflict.cpu-printed-address. Service connector details and settled CPU ordinal numbering do not change device functions, public bindings or fitted hardware. Literal readings remain retained; ignored records include the specific rationale. Genuine unresolved coil/part/fitment conflicts remain unresolved.

Recorded wiring/printed-number discrepancies ignored for author-readiness under the runbook: `conflict.cpu-service-pinout`, `conflict.cpu-printed-address`. Functions and public routing agree; the literal disagreements remain visible in excerpts and device notes.

## Retained source records

External locators prefixed `working-root:` resolve under the configured sibling `pinmame-game-defs-working-dir`. Portable factual excerpts carry their own fail-closed repository digests; source-owned PDFs, ROMs, frames and tables remain external.

- `manual.driver` (manual): `9ee381bce70e70e7c42ad60ba13bd9a62cf65b7ce00611701a712670cea0769e`. driver_reference full printed table regions, PDF pages/printed folios12; 35 printed rows including blanks; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.pabst-can-crusher.2016/factory-reference.json.txt`: `e472ebc2e7ffd8eda9f6028ae69da9703cbb1544dea665bb265b1917873bf966`.
- `manual.switch` (manual): `9ee381bce70e70e7c42ad60ba13bd9a62cf65b7ce00611701a712670cea0769e`. switch_reference full printed table regions, PDF pages/printed folios12,13,15; 71 printed rows including blanks; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.pabst-can-crusher.2016/factory-reference.json.txt`: `e472ebc2e7ffd8eda9f6028ae69da9703cbb1544dea665bb265b1917873bf966`.
- `manual.light` (manual): `9ee381bce70e70e7c42ad60ba13bd9a62cf65b7ce00611701a712670cea0769e`. light_reference full printed table regions, PDF pages/printed folios15,17; 78 printed rows including blanks; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.pabst-can-crusher.2016/factory-reference.json.txt`: `e472ebc2e7ffd8eda9f6028ae69da9703cbb1544dea665bb265b1917873bf966`.
- `manual.assemblies` (manual): `9ee381bce70e70e7c42ad60ba13bd9a62cf65b7ce00611701a712670cea0769e`. Own-title supporting assemblies, PDF pages/printed folios1,2,14,16,19,20,26,28,36,39,41; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.pabst-can-crusher.2016/factory-reference.json.txt`: `e472ebc2e7ffd8eda9f6028ae69da9703cbb1544dea665bb265b1917873bf966`.
- `manual.flipper` (manual): `9ee381bce70e70e7c42ad60ba13bd9a62cf65b7ce00611701a712670cea0769e`. Both complete flipper BOMs, PDF page/printed folio38, EOS item3, coil item4 and return spring item7; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.pabst-can-crusher.2016/factory-reference.json.txt`: `e472ebc2e7ffd8eda9f6028ae69da9703cbb1544dea665bb265b1917873bf966`.
- `manual.reel-controller` (manual): `9ee381bce70e70e7c42ad60ba13bd9a62cf65b7ce00611701a712670cea0769e`. Full520-6961-00 controller and520-6964-00 LCD pinouts PDF/printed folio28; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.pabst-can-crusher.2016/factory-reference.json.txt`: `e472ebc2e7ffd8eda9f6028ae69da9703cbb1544dea665bb265b1917873bf966`.
- `pinmame.catalog.8e0f721e3df7` (pinmame_catalog): `756ecd840f234cf7a62f84ef331ccb8b61f0f1aeffc409bc7b776d6c037211c9`. PinmameGetGames
- `rom.routing` (rom_static_analysis): `21dc4b02336433bdb60b1b071f4fc7fa972baa31d4a140102a20881bd2f9d0b8`. Complete exact ROM switch/coil/LED tables; public mapping by node/position; game SHA2565af3006928ddbbe936b54a37938fc2d8252b81af0bdf7150d79431793bc2dc49; extractor SHA25659e4d5940064443b1ad2c1d6aaf05b7a3a594e71b890ec3d4287989166b40446; source/core hashes and locators retained inside artifact. Physical construction excluded. Excerpt `evidence/excerpts/stern.pabst-can-crusher.2016/rom-routing.json.txt`: `1f1490b1a82b6586f27941edd8fbcc4f642a8d10ae4e9f0518ac756bb1542e58`.
- `runtime.api-r2` (runtime_scenario): `73a9a5c93b8d277d57273d151b776ed3210806ee08b7a437235e7af79b3ee765`. Physical-all output mask2=2, 10ms polling, fresh empty state; recorder SHA2567d924857bb8c76d4039c900ecaa329023905a21a654a6fdfa85180446013d84c; harness SHA25649c5e733bf436a260c915d88e275189950d8ebcc55575f01ab2d153099e1dd44; DLL SHA2561875e0961759cbd21b566d31a60c7f9e7c59c26c7f1e0d21f97b1b50118db005; full raw trace and manifest retained. Excerpt `evidence/excerpts/stern.pabst-can-crusher.2016/runtime-observations.json.txt`: `52d13ede191f6f43a87d46ea2cdb6de811ba2c9e01170d1510e6c38254462fd6`.
- `identity.opdb` (human_review): `be658179b49b2bc02dce55d928c3d6a6afe6307e2b00a0ac7ffc1a745ac2d9f3`. Exact OPDB machine recordGRYX4-MRjVP; IPDB6335, Stern, physical manufacture year2016; reviewed identity snapshot from2026-10-10. Excerpt `evidence/excerpts/stern.pabst-can-crusher.2016/identity.json.txt`: `0b9f747bc7b34a77ca4332f5a4673327b195d4f08bf535444cc2cc2bc2761669`.
- `manual.cpu-connectors` (manual): `9ee381bce70e70e7c42ad60ba13bd9a62cf65b7ce00611701a712670cea0769e`. Full direct CPU switch mapping, PDF page and printed folio 19; supporting service wiring schematic on folio 20. Full literal cells retained in manual excerpt. Excerpt `evidence/excerpts/stern.pabst-can-crusher.2016/factory-reference.json.txt`: `e472ebc2e7ffd8eda9f6028ae69da9703cbb1544dea665bb265b1917873bf966`.
