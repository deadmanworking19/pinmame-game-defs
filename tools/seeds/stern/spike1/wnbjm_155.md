# Whoa Nellie! Big Juicy Melons (2015)

## Current PinMAME adapter

The active adapter is PinMAME `46e1a01a0f73dc5ce163d98db1ae435883ecc450`. Virtual GAME ON is public solenoid 33; it represents an armed lower-flipper reflex, not a physical relay. Direct reads at 34-36 are aliases; the canonical plugin and aggregate address is 33. The current driver samples I/O at 1 kHz, retains short host switch edges, and keeps newly observed coil pulses for at least one frame. The modulated poll includes lower binary mirrors 45-48 because nSolenoids is at least 48. Plugin DIP group 6 now maps ordinals 1-8 to bank 0 bits 0-7 correctly. Lower EOS synthesis is unchanged. Historical runtime traces and ROM-table excerpts remain scoped to their original revision; this source audit adds no new gameplay observation or physical fitment evidence.

Source records: `pinmame.adapter.current` provides the pinned code and active-route excerpts; `pinmame.catalog.current` provides the current public driver descriptor. Both supplement the historical sources below.

## Identity

Machine `stern.whoa-nellie-big-juicy-melons.2015`, driver `wnbjm_155`, OPDB `GRYX4-MLqqx`, IPDB `6252`. Coverage remains partial; no author-ready claim.

Every legal public switch0–95/101–132, DIP1–8, solenoid1–32/45–48/51–72 and lamp1–80 has exactly one disposition. Printed identities remain aliases; physical matching uses node/channel positions. CPU semantic mapping preserves original numbering anomalies.

Factory PDF `Whoa-Nelly-Manual.pdf`, SHA-256 `aaeedb049d621e5d6d66f680aa07fd19d07824dd277cf4ed9f0684f570be61c2`. Source-owned documents remain external; the full reviewed factual table regions and construction supplements are preserved in the source-linked portable excerpts below.

## Recreation evidence and limits

- Complete reference regions visually checked on PDF/printed folios 18,20,22,23: 35 driver,70 switch and78 light rows. Blank and printed dash cells preserved.
- Manual CPU C1 DIP address prints 0-SW-0; C2 starts 0-SW-2. These literals are retained separately from exact-ROM CPU addresses101-108.
- Light69 Match7 part number prints 520-6962-v; it is preserved literally rather than completed from neighboring rows.
- Switch54 Right Coin uses CN5 pin8 PNK-RED with printed address1-SW-18; switch55 Center Coin uses pin7 PNK-ORG with1-SW-17. Slam Tilt60 prints1-SW-21. Their routing is an independent ROM-source assertion.
- Driver17-31 are reel stepper enable/phase wires carried by node11 LP1-15. They are internal mechanism channels, not public coils.
- Supporting pages visually checked:24 CPU connectors/audio/country DIP codes,41 score/credit reel and long-range opto assemblies,44 shooter/trough/bullseye/knocker,46 non-powered bumper and30-degree eject.
- The shooter heading on page44 prints500-7286-00, also printed on the separate trough assembly. This literal repeated identifier is retained as a manual labeling anomaly; no corrected shooter part number is invented.

Own-title flipper BOMs explicitly print180-5149-00 SWITCH - END OF STROKE N/C. Matched lower EOS records set normally_closed=true while remaining virtual public transport. All other construction polarity, pulse flags and unprinted quantities remain unset.


## Physical topology and behavior

### Score and credit reels

PDF/folio41 shows four-score-reel bank511-7614-00 with four511-7648-00 score assemblies and eight white LED boards520-5307-00; credit assembly511-7615-00 contains one511-7648-01 credit reel and one white LED board. Individual reel uses unipolar stepper041-5105-00, reel515-9819-00, motor bracket535-1131-00 and reel opto PCB520-6960-00. Driver17-31 provides enable/phase1/phase2 for credit,1s,10s,100s,1000s; Switch46-50 names one home opto per reel. Drawing proves shaft drive and sensor placement on the reel bracket. Backbox ball path is not applicable.

Unresolved: No verified step/digit calibration, phase direction, initial zero/home angle, startup homing sequence, pulse timing, reset/retry or jam procedure; no contact-rest construction inferred from opto.

### Shooter, trough and top eject

PDF/folio44 manual spring/plunger shooter uses shooter spring266-5001-04, short-plunger spring266-5010-00 and rod515-6557-00. Trough assembly500-7286-00 uses coil090-5044-ND26-1200, spring266-5020-00 and plunger515-7309-01. Page46 eject500-6511-03-ND uses26-1200 coil090-5044-ND, conical compression spring, and30-degree plunger515-7197-00. Reference switches5 shooter lane,16 center drain,17 trough opto,20 top eject and outputs6 trough/5 top eject identify relevant sensors and actuators. Mechanical spring-return construction is documented; this does not establish all ball travel causality.

Unresolved: Trough capacity, complete ball route, default ball arrangement, timing, retries and jam behavior not established by these pages.

### Lower flippers

Own-title PDF/printed folio43 supplies both complete assemblies, NC EOS, coil, plunger/crank, stop and return spring. Actual ROM coil identities are retained in the structured mechanisms.45/46 right and47/48 left are virtual binary OR mirrors; they do not add independent windings. Public lower EOS is synthesized; physical NC construction does not authorize driving the synthesized state.

### Physical reels, internal phase controls and mini LCD

Four physical score reels and one credit reel belong in the mechanism inventory. Manual Driver17–31 are Node11 LP15..1 enable/phase signals for internal stepper control, withheld from ordinary public output export. Public solenoids17..31 are zero slots; never bind reel phases there. Controller520-6961-00 supplies five two-phase motor connections and five opto-home circuits; current-limit/OCP pin labels remain literal. Small520-6964-00 LCD uses128x32 drawing label and14-pin ribbon036-8045-132. The128x32 PinMAME DMD callback is its transport, not evidence for a physical backbox DMD. This draft uses schema video for the physical LCD and leaves its physical mounting location and normalized coordinates unresolved.

GetMech ordering is subsystem motors, then steppers, then registered limit motors, and an absent entry also returns zero. The retained harness samples only indices0..3 and does not itself establish all five reel ordinals, digit calibration, phase direction, startup homing or jam recovery; those remain explicit gaps.

## Exact runtime observations

API run started `2026-10-10T19:14:14Z`, source revision `8e0f721e3df7a2b4e8a9d2f4454ac7a9aa1ced53`, library SHA-256 `1875e0961759cbd21b566d31a60c7f9e7c59c26c7f1e0d21f97b1b50118db005`, observation SHA-256 `e86ab4da24067ba4eabc592c8551bbeb3d4c68b59784a12f095a1d024c49062b`. Fresh state; physical-all mask2=2;10ms polling. These are emulator observations, not physical polarity or fitment proofs.

Observed solenoid addresses: [1, 2, 3, 4, 6, 8, 45, 46, 47, 48]. DMD layout0:128x32,4-bit. Changed frames: {'0': {'changed_frames': 178, 'recorded_events': 178, 'suppressed_events': 0}}. No activity at an address is not evidence of absence; shorter pulses can be missed.

- Step7 start: START BUTTON: 6 [155, 0, 155, 0, 155, 0, 155, 0, 155, 0, 155, 0].
- Step8 post-start serve observation: 6 [155, 0, 155, 0, 155, 0].
- Step12 left flipper button: 1 [255, 0], 3 [255, 0], 47 [255, 0], 48 [255, 0].
- Step13 right flipper button: 2 [255, 0], 4 [255, 0], 45 [255, 0], 46 [255, 0].
- Step14 LEFT SLINGSHOT: 8 [200, 0].

Full raw events, observations, DLL/scenario/ROM hashes and run manifest remain under `runtime/wnbjm_155-api-r2`. A post-serve synthetic trough-to-shooter transfer is conditional gameplay evidence; host write/readback alone is not a ROM response.

## Manual devices without a proven public binding

| Table / PDF | Printed ID | Name | Circuit | Disposition |
| --- | --- | --- | --- | --- |
| driver_reference / 18 | 17 | Credit Reel Enable | 11-LP-15 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 18 | 18 | Credit Reel Phase 1 | 11-LP-14 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 18 | 19 | Credit Reel Phase 2 | 11-LP-13 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 18 | 20 | 1s Reel Enable | 11-LP-12 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 18 | 21 | 1s Reel Phase 1 | 11-LP-11 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 18 | 22 | 1s Reel Phase 2 | 11-LP-10 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 18 | 23 | 10s Reel Enable | 11-LP-9 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 18 | 24 | 10s Reel Phase 1 | 11-LP-8 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 18 | 25 | 10s Reel Phase 2 | 11-LP-7 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 18 | 26 | 100s Reel Enable | 11-LP-6 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 18 | 27 | 100s Reel Phase 1 | 11-LP-5 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 18 | 28 | 100s Reel Phase 2 | 11-LP-4 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 18 | 29 | 1000s Reel Enable | 11-LP-3 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 18 | 30 | 1000s Reel Phase 1 | 11-LP-2 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 18 | 31 | 1000s Reel Phase 2 | 11-LP-1 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 18 | 33 | Shaker motor(opt) | 1-DR-0 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| switch_reference / 23 | 60 | Slam Tilt | 1-SW-21 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| light_reference / 22 | 77 | Cabinet Left | 1-LP-3 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| light_reference / 22 | 78 | Cabinet Right | 1-LP-6 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |

## Remaining gaps

Unresolved switch construction polarity other than positively printed EOS; spatial placement with x0left/x1right/y0rear/y1apron; full ball path/capacity/default occupancy; calibrated travel/velocity; step/digit calibration; exact startup/homing/return conditions; pulse/hold timing; jam/retry/reset behavior; optional fitment and unreviewed edition differences. No numeric geometry or RGB emitter quantity is invented.

- Manual p20 SlamTilt60 prints1-SW-21; exactROM Node1pos21 isSixthCoin public61 andpos22 isSlamTilt public60. Manual has no61 row. Resolution path: inspect this title’s cabinet harness/schematic or actualCN5/CN9 circuit; an API setter readback and sibling manual cannot establish this machine’s wiring.

Acquisition times, source manifest reconciliation, portable excerpt imports and independent root review remain pending, so coverage retains provenance and other stated partial blockers. Schema/full address/ID/reference/EOS checks passed externally; canonical semantic and evidence gates must run after import.


## Final retained disagreements and validation

- Manual p20 SlamTilt60 prints1-SW-21; exactROM Node1pos21 isSixthCoin public61 andpos22 isSlamTilt public60. Manual has no61 row. Resolution path: inspect this title’s cabinet harness/schematic or actualCN5/CN9 circuit; an API setter readback and sibling manual cannot establish this machine’s wiring.
- Switch Reference p22 Trough Opto prints 515-0215-00 tx / 515-0215-01 rx; the long-range opto assembly BOM p41 prints 500-0215-00 emitter / 500-0215-01 receiver. The common suffix and assembly class suggest a prefix discrepancy, but exact assembly-to-trough fitment is not independently proven. Both literal assertions are retained; no canonical sensor PN selected. Resolution path: consult factory revision/parts documentation or inspect the actual trough sensor and its assembly marking.
- The manual CPU DIP/service numbering omits 0-SW-1 and shifts the subsequent printed addresses; exact ROM Node 0 positions 0–7 mirror physical DIP ordinals 1–8 as public 101–108 and positions 8–11 are Select/Plus/Minus/Back public 109–112. Canonical public bindings follow verified ROM routing; source-literal addresses remain aliases. Resolution path: check factory CPU mapping documentation or exact machine wiring to resolve the printed numbering discrepancy; do not remap the API from printed IDs alone.

JSON schema, repository machine semantic validation (without repository-relative file checks), controller group validation, complete legal-address disposition, unique identifiers, mechanism references and own-title EOS N/C gates passed. Portable excerpt and knowledge-path existence/hash checks are deferred until the root imports exact files. Coverage remains partial.

Peer review correction: exported solenoid51–53 are factory Digital Out meter/ticket control signals. Their public solenoid group/address and literal wiring remain; canonical IDs use control.* and kind=control_signal. No meter coil winding is inferred.

LCD mounting gap: own factory controller/display pinout establishes LCD520-6964-00,128x32, supply and ribbon, but does not identify its installed mounting position. Physical location and normalized coordinates are unknown; the optional physical_location field is omitted. Pinned PinMAME spike1.c describes an apron LCD as an emulator model description, not an own-title physical placement authority. Obtain an exact-title factory placement/assembly locator or verified own-machine placement evidence before assigning the display to playfield or cabinet/service space.

Recorded, nonblocking distinctions under INSTRUCTIONS.md: conflict.cpu-printed-address. Service connector details and settled CPU ordinal numbering do not change device functions, public bindings or fitted hardware. Literal readings remain retained; ignored records include the specific rationale. Genuine unresolved coil/part/fitment conflicts remain unresolved.

Recorded wiring/printed-number discrepancies ignored for author-readiness under the runbook: `conflict.cpu-printed-address`. Functions and public routing agree; the literal disagreements remain visible in excerpts and device notes.

## Retained source records

External locators prefixed `working-root:` resolve under the configured sibling `pinmame-game-defs-working-dir`. Portable factual excerpts carry their own fail-closed repository digests; source-owned PDFs, ROMs, frames and tables remain external.

- `manual.driver` (manual): `aaeedb049d621e5d6d66f680aa07fd19d07824dd277cf4ed9f0684f570be61c2`. driver_reference full printed table regions, PDF pages/printed folios18; 35 printed rows including blanks; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.whoa-nellie-big-juicy-melons.2015/factory-reference.json.txt`: `1e9064014d94c588ae141942e29842d3d33273f60db2875d8cb5ead853e7fc8b`.
- `manual.switch` (manual): `aaeedb049d621e5d6d66f680aa07fd19d07824dd277cf4ed9f0684f570be61c2`. switch_reference full printed table regions, PDF pages/printed folios22,23; 70 printed rows including blanks; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.whoa-nellie-big-juicy-melons.2015/factory-reference.json.txt`: `1e9064014d94c588ae141942e29842d3d33273f60db2875d8cb5ead853e7fc8b`.
- `manual.light` (manual): `aaeedb049d621e5d6d66f680aa07fd19d07824dd277cf4ed9f0684f570be61c2`. light_reference full printed table regions, PDF pages/printed folios18,20,22; 78 printed rows including blanks; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.whoa-nellie-big-juicy-melons.2015/factory-reference.json.txt`: `1e9064014d94c588ae141942e29842d3d33273f60db2875d8cb5ead853e7fc8b`.
- `manual.assemblies` (manual): `aaeedb049d621e5d6d66f680aa07fd19d07824dd277cf4ed9f0684f570be61c2`. Own-title supporting assemblies, PDF pages/printed folios24,41,44,46; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.whoa-nellie-big-juicy-melons.2015/factory-reference.json.txt`: `1e9064014d94c588ae141942e29842d3d33273f60db2875d8cb5ead853e7fc8b`.
- `manual.flipper` (manual): `aaeedb049d621e5d6d66f680aa07fd19d07824dd277cf4ed9f0684f570be61c2`. Both complete flipper BOMs, PDF page/printed folio43, EOS item3, coil item4 and return spring item7; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.whoa-nellie-big-juicy-melons.2015/factory-reference.json.txt`: `1e9064014d94c588ae141942e29842d3d33273f60db2875d8cb5ead853e7fc8b`.
- `manual.reel-controller` (manual): `aaeedb049d621e5d6d66f680aa07fd19d07824dd277cf4ed9f0684f570be61c2`. Full520-6961-00 controller and520-6964-00 LCD pinouts PDF/printed folio33; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.whoa-nellie-big-juicy-melons.2015/factory-reference.json.txt`: `1e9064014d94c588ae141942e29842d3d33273f60db2875d8cb5ead853e7fc8b`.
- `pinmame.catalog.8e0f721e3df7` (pinmame_catalog): `756ecd840f234cf7a62f84ef331ccb8b61f0f1aeffc409bc7b776d6c037211c9`. PinmameGetGames
- `rom.routing` (rom_static_analysis): `e6e96994d56fa5ba140175a7540ca96d3dd7182d9a1ccad87b071e6e94e978e9`. Complete exact ROM switch/coil/LED tables; public mapping by node/position; game SHA25692b7d8c494c4aceefd3fb4f6acec3c47d8968b1cba5b6a550349a6482336c458; extractor SHA25659e4d5940064443b1ad2c1d6aaf05b7a3a594e71b890ec3d4287989166b40446; source/core hashes and locators retained inside artifact. Physical construction excluded. Excerpt `evidence/excerpts/stern.whoa-nellie-big-juicy-melons.2015/rom-routing.json.txt`: `695ff5f6ee4e048d54da31adcd500758cb9c11289f99dadf05cbb2e4467512c2`.
- `runtime.api-r2` (runtime_scenario): `e86ab4da24067ba4eabc592c8551bbeb3d4c68b59784a12f095a1d024c49062b`. Physical-all output mask2=2, 10ms polling, fresh empty state; recorder SHA25641400f2bdf14a0bb50e14a2d3368e0058366c9c156bfb64bcc7e4ce60013c529; harness SHA25649c5e733bf436a260c915d88e275189950d8ebcc55575f01ab2d153099e1dd44; DLL SHA2561875e0961759cbd21b566d31a60c7f9e7c59c26c7f1e0d21f97b1b50118db005; full raw trace and manifest retained. Excerpt `evidence/excerpts/stern.whoa-nellie-big-juicy-melons.2015/runtime-observations.json.txt`: `2f4ebc7f656c04af9ebba74f2af42625215e57c175b24cbcb7038ec03f0fc5f2`.
- `identity.opdb` (human_review): `be658179b49b2bc02dce55d928c3d6a6afe6307e2b00a0ac7ffc1a745ac2d9f3`. Exact OPDB machine recordGRYX4-MLqqx; IPDB6252, Stern, physical manufacture year2015; reviewed identity snapshot from2026-10-10. Excerpt `evidence/excerpts/stern.whoa-nellie-big-juicy-melons.2015/identity.json.txt`: `bdd6b7922a3522d3e86a70854bfe51762defbee8466a7db88826634d11fe9ac5`.

## Exact supplied PinMAME table successor evidence

The contributor supplied `Whoa Nellie! Big Juicy Melons (Stern 2015) v2.1.4 PinMAME.vpx` for this refresh. Its exact VPX SHA-256 is `277fff2d00c349ef1c15b4ff4a97df05d38b7b0bc892949ea180305cd8ccc753`; embedded `cGameName` is `wnbjm_155`. The original and complete extraction are retained under `working-root:vpx-sources/stern/whoa-nellie-big-juicy-melons-2015/supplied-pinmame-2026-10-25/`; canonical full-file manifest SHA-256 `28b2f50b9353a2a1b790a7003cb796514ba21e70fbfe4d69c306da471fc311e5` covers 1219 files and 159869683 bytes. The older pinned manual, ROM, runtime and table evidence is preserved. `vpx.supplied-pinmame-script.2026-10-25` and `vpx.supplied-pinmame-table.2026-10-25` supply exact script and geometry identities. This source was inspected statically, not independently launched in this pass; `known_working:false` makes that limit explicit.

The detailed [supplied-table spatial supplement](../../evidence/spatial/stern/whoa-nellie-big-juicy-melons-2015-supplied-vpx.json) and [portable factual excerpt](../../evidence/excerpts/stern.whoa-nellie-big-juicy-melons.2015/supplied-pinmame-vpx.json.txt) retain raw object identities/hashes, source-line locators, bounds, normalization and every projection class. 27 input and 7 output placements are `observed`, using exact script bindings plus the machine’s own factory physical descriptions. No coordinate is validated by an independent factory drawing in this pass. Broad collision polygons are explicitly mechanism projections; coils projected to their own driven assembly are not located windings.

The script creates one ball in Drain, sets trough opto 17 active and tracks it in TroughHasBall. Output 6 clears that flag/contact, destroys the drain ball and creates/kicks a ball from Ballrelease. This is a simplified trough representation, not evidence for opto geometry or physical trough capacity.

Output 5 kicks a captured Kicker1 ball and clears top eject contact 20; the switch is driven by Kicker1 Hit/UnHit. Coil kick velocity and rod animation timer are table tuning, not measured physical behavior.

GetMech indices 0,1,2,3 supply the thousands, hundreds, tens and units score reels; index 4 supplies credits. ReelDigit rounds the position using 20 steps per score digit and 10 per credit, modulo 10. This is the exact script conversion; physical phase direction, service calibration, homing, stalls and jam recovery remain unverified.

Lower EOS writes at 1/2 are derived from virtual flipper angle within three degrees of EndAngle. The public core synthesizes EOS, so these host writes are not independent physical contact feedback and do not establish contact construction.

Dual target edge/center handlers pulse 22/23 on the right and 40/41 on the left. Rubber-backed one-point contacts use their own handlers; shared rubber regions are not treated as distinct measured leaf positions.

The retained table metadata still says “Whoa-Nellie (wizbang 2011)” and version 2.1.2 while the supplied filename says Stern 2015 v2.1.4. These source-literal metadata discrepancies are retained in the excerpt. They do not replace the own-title manufacturer manual, verified physical identity or the embedded `wnbjm_155` ROM binding.

Remaining placement limits: Trough opto 17 uses a shared Drain surrogate rather than independent opto geometry and remains unplaced; output 6 is not placed from Ballrelease, a ball-spawn proxy. Dual-target inner/outer contacts and rubber-backed one-point leaves are not placed at render or broad rubber proxies. Backbox score/credit reel geometry does not establish a playfield coordinate; the physical LCD mount remains unresolved because the table only displays its emulator window. No Light array member is treated as a physical bulb merely because the script drives it. GI arrays include duplicate glows/insert overlays; emitter identity, quantity and factory string membership remain unresolved.

The definition remains `partial` with its existing missing dimensions and physical/manual conflicts. This successor adds table evidence and observed placements, while physical emitter quantities, unresolved fitment, polarity, independent drawing reconciliation and complete mechanism causality remain gated.
