# Game of Thrones (Pro) (2015)

## Current PinMAME adapter

The active adapter is PinMAME `46e1a01a0f73dc5ce163d98db1ae435883ecc450`. Virtual GAME ON is public solenoid 33; it represents an armed lower-flipper reflex, not a physical relay. Direct reads at 34-36 are aliases; the canonical plugin and aggregate address is 33. The current driver samples I/O at 1 kHz, retains short host switch edges, and keeps newly observed coil pulses for at least one frame. The modulated poll includes lower binary mirrors 45-48 because nSolenoids is at least 48. Plugin DIP group 6 now maps ordinals 1-8 to bank 0 bits 0-7 correctly. Lower EOS synthesis is unchanged. Historical runtime traces and ROM-table excerpts remain scoped to their original revision; this source audit adds no new gameplay observation or physical fitment evidence.

Source records: `pinmame.adapter.current` provides the pinned code and active-route excerpts; `pinmame.catalog.current` provides the current public driver descriptor. Both supplement the historical sources below.

## Identity

Machine `stern.game-of-thrones-pro.2015`, driver `got_137`, OPDB `G41d5-MKNwX`, IPDB `6307`. Coverage remains partial; no author-ready claim.

Every legal public switch0–95/101–132, DIP1–8, solenoid1–32/45–48/51–72 and lamp1–272 has exactly one disposition. Printed identities remain aliases; physical matching uses node/channel positions. CPU semantic mapping preserves original numbering anomalies.

Factory PDF `GameOfThrones_Pro_web.pdf`, SHA-256 `87f012c844a217f1c3bde335b28af07bc9d36f683f48c6921896de801eb96a83`. Source-owned documents remain external; the full reviewed factual table regions and construction supplements are preserved in the source-linked portable excerpts below.

## Recreation evidence and limits

- All reference table regions reviewed: PDF/printed folios 12, 14, 15, 17, 18, 20, 21. Driver 32, Switch 89, Light 112 rows including every printed blank numbered row and CPU/DIP row. No switch row 73 is printed; row 72 prints only a Node Ext. dash.
- PDF page 12 driver grid splits Ret. Wire/Voltage; BLU + 48V and BLK + 12V corrected against visual while raw erroneous grid and correction log remain.
- CPU manual discrepancy: Switch Reference p17 DIP C1–C8 prints 0-SW-0 through 0-SW-7 and Service C9–C12 prints 0-SW-8 through 0-SW-11; repeated Direct Switch Mapping p22 skips 0-SW-1, prints DIP C2–C8 as 0-SW-2 through 0-SW-8 and Service C9–C12 as 0-SW-9 through 0-SW-12. Both literal regions preserved. Exact ROM public routing 101–112 is kept separately.
- CPU service wiring discrepancy: p17 CN25 service pins 4,3,2,1 with ground 6 and assembly PN 515-1963-XX; p22 pins 1,2,3,4 with ground 11 and individual 180-5192 parts. P23 schematic prints service Select4,Plus3,Minus2,Back1; ground6 routed through Cabinet Node CN10/CN12 to CPU CN25. Do not silently normalize p22.
- Physical source PN discrepancy: p12 trough receiver extension 520-5345-01, switch reference p15 receiver 520-5345-00 rx and assembly p36 520-5345-00. Keep the printed forms scoped to each source.
- Drop-reset physical source conflict: p14 driver14 specifies Coil 25-1240 / 090-5034-ND; p38 assembly500-7216-13 item17 specifies Coil24-940 / 090-5036-ND. Both are visually verified; variant/printing conflict requires resolution before assigning one canonical coil PN.
- Light107 Dragon Left x2 explicitly states two and prints White / Red with two part numbers. Other RGB reference channels do not establish physical emitter quantity. No RGB quantity or coordinates inferred.
- Factory manual scope is PRO model500-55G4-01 / manual780-50G4-00, visually printed on cover; Pro assemblies named explicitly on p45/p46/p47. Premium/LE features are not transferred.

Own-title flipper BOMs explicitly print180-5149-00 SWITCH - END OF STROKE N/C. Matched lower EOS records set normally_closed=true while remaining virtual public transport. All other construction polarity, pulse flags and unprinted quantities remain unset.

- Headings give left500-6543-83-ND/right500-6543-82-ND, while figure captions say left500-6543-02-ND/right500-6543-12-ND. Preserve both title/caption identities; assembly label discrepancy does not change explicitly printed EOS construction.

## Physical topology and behavior

### Three drop targets and shared reset

P38 assembly500-7216-13 has three545-6305-00 bodies, three266-5089-00 compression springs and three265-5003-02 target-reset springs. A single530-5757-00 plunger, single535-9996-03 lift bracket and one coil operate the bank;520-5252-13 opto PCB senses the three target states. Reference switches7/8/9 are 3-Bank Drop Target Top/Mid/Btm and driver14 is Drop Reset. Geometry shows a common reset actuator under three independently dropping bodies. Coil specification conflict is recorded above.

Unresolved: No calibrated travel, pulse duration, electrical rest/polarity, reset timing, startup state, target jam or retry behavior is specified by these pages.

### Dragon and coupled wing motion, Pro

P46 Dragon Pro516-6783-00 comprises Dragon500-9873-01 and one Dragon Solenoid511-7548-01. P44 shows23-800 coil090-5001-ND driving pull-down plunger515-9770-02 with compression spring266-5076-04; p46 shows the pivot connection into Dragon500-9873-01 / fulcrum511-7551-00. Wing511-7569-01 has driver gear segment550-7367-00, driven segment550-7368-00, two distinct wing rivet assemblies510-7541-00/-01, torsion spring265-5079-00-00, stop bracket535-1193-00 and rubber bumper545-5105-02. This documents one solenoid and a linked gear/fulcrum mechanism with spring and stops, rather than separate public wing motors. Driver18 Dragon is the reference actuator. No position/home sensor is listed in the wing/dragon BOMs. RaptorToy511-7696-00 has one red LED112-5049-02 (p44).

Unresolved: No angle calibration, active/rest wing angle, direction convention, timing, homing, servo feedback, jam or retry behavior is established. Absence of a BOM sensor is not a claim that all possible sensors are absent. Ball impact coupling to dragon motion is not specified.

### Sword and down-post lock topology

P42 DownPost500-9933-00 contains one bracket515-9805-01, two26-1200 coils090-5044-ND, distinct down-post plunger515-9806-00 and sword-actuator plunger511-7612-00, plus266-5081-00 and266-5076-02 compression springs. P44 rightwireform500-9927-00 includes wire ramp515-9801-00, Sword535-1081-00 and switch bracket511-7605-00; drawing shows three sequential switch levers on the wireform. Reference switches46/47/48 Lock1/2/3 are separate Rollover180-5119-02 circuits at Node9; drivers21 Sword and20 LockReleasePost are separate Node9 outputs. Reference also has driver16 UpPost at Node8; p39 ball-deflector500-7081-01 is another26-1200 plunger mechanism. These distinct outputs are not merged merely because all move posts.

Unresolved: Exact association of each generic post drawing with every driver requires explicit wiring/assembly evidence. No capacity/default post height, release ball destination, timing, jam/overflow or retry behavior is documented here. Three lock sensors do not on their own establish the ROM multiball capacity or which physical lock is occupied by default.

### Two shared control gates

P47 BackPanel500-2458-00 lists one511-7656-01 rightgate and one511-7656-00 leftgate, both labeled UP. P43 generic511-7656-XX BOM lists one32-1250 mini-coil/core090-5060-01-ND, electric gate/magnet535-9682-00, hinge/rebound pin535-5372-00 and clevis pin530-5702-01. Driver22 Left/RightControlGates is one shared output10-DR-0. Drawing supports two physical gates on one electrical reference and pivoting gates operated by their mini-coils; UP is an assembly label.

Unresolved: Unpowered gate position, allowed/pass/blocked ball direction, complete destination routes, pulse/hold requirements, timing and jam/retry handling are not specified. Assembly label UP is not treated as an electrical normal-state proof.

### Ram target and passive ram body

P43 Ram500-9963-00 has body535-1189-00, two530-7908-00 wheel axles, timber cover545-9812-00, guide pins530-7909-00, ramhead545-9817-00, rubber bumper545-5428-00 and glideplate535-1190-00. P39 S/U target500-9966-00 includes515-9836-00 target-switch assembly-RAM; reference switch40 BatteringRam lists that same part. No driven ram coil or motor appears in the ram BOM or driver reference. Drawing shows the body supported on axles/guide pins with a bumper/slide plate.

Unresolved: Exact ball-hit displacement/contact sequence, return force, timing, jam state and quantitative travel are unresolved; no motor is invented from the animated object name.

### Trough, manual shooter, auto launch and kickback

P36 trough500-9820-00 has one27-1500 coil090-5004-ND, plunger515-7309-01, conical spring266-5020-00, tx520-5344-00 and rx520-5345-00. References20–25 Trough6..1 and26TroughJam give seven opto signals, with driver1 Trough. Manual shooter500-6146-00-07 uses long orange spring266-5001-07, short spring266-5010-00 and rod515-6557-00. P38 auto-launch500-9818-00 has one23-800 coil090-5001-ND, kickerarm535-0728-00, pivot530-7835-00, plunger/link515-6304-03, conical spring266-5020-00 and short-arm shooter switch180-5157-01; driver2 AutoPlunger and switch27 ShooterLane identify its electrical roles. P39 kicker500-6697-02-ND uses23-800 coil090-5001-ND, plunger515-7318-00 and spring266-5020-00; p32 explicitly places one kicker and one left spinner. Reference17 Kickback and switch37 Kickback opto provide named electrical roles. P45 guides511-7592-02/-03 carry515-0215-00 emitter and515-0215-01 receiver on opposite guide assemblies.

Unresolved: No complete ball-routing graph, calibrated velocities, pulse intervals, full trough/lock capacity behavior, opto rest/polarity, startup/default state or jam/retry sequence is asserted from these drawings.

### Lower flippers

Own-title PDF/printed folio37 supplies both complete assemblies, NC EOS, coil, plunger/crank, stop and return spring. Actual ROM coil identities are retained in the structured mechanisms.45/46 right and47/48 left are virtual binary OR mirrors; they do not add independent windings. Public lower EOS is synthesized; physical NC construction does not authorize driving the synthesized state.

## Exact runtime observations

API run started `2026-10-10T19:15:06Z`, source revision `8e0f721e3df7a2b4e8a9d2f4454ac7a9aa1ced53`, library SHA-256 `1875e0961759cbd21b566d31a60c7f9e7c59c26c7f1e0d21f97b1b50118db005`, observation SHA-256 `a07db409be41a2f914587de65313c4b400e52c85860863bd18aacf34322b3541`. Fresh state; physical-all mask2=2;10ms polling. These are emulator observations, not physical polarity or fitment proofs.

Observed solenoid addresses: [1, 3, 5, 8]. DMD layout0:128x32,4-bit. Changed frames: {'0': {'changed_frames': 173, 'recorded_events': 173, 'suppressed_events': 0}}. No activity at an address is not evidence of absence; shorter pulses can be missed.

- Step7 start: START BUTTON: 1 [255, 0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0].
- Step8 post-start serve observation: 1 [255, 0, 255, 0, 255, 0, 255, 0].
- Step12 left flipper button: 3 [255, 30, 0].
- Step13 right flipper button: 8 [255, 30, 0].
- Step14 LEFT SLINGSHOT: 5 [204, 0].

Full raw events, observations, DLL/scenario/ROM hashes and run manifest remain under `runtime/got_137-api-r2`. A post-serve synthetic trough-to-shooter transfer is conditional gameplay evidence; host write/readback alone is not a ROM response.

## Manual devices without a proven public binding

| Table / PDF | Printed ID | Name | Circuit | Disposition |
| --- | --- | --- | --- | --- |
| driver_reference / 12 | 30 | Coin Meter | 1-DR-2 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |
| driver_reference / 14 | 31 | Ticket Meter | 1-DR-3 | No matching exported node/channel, internal/withheld channel, or explicit unresolved manual/ROM conflict; physical source retained without inventing a public binding. |

## Remaining gaps

Unresolved switch construction polarity other than positively printed EOS; spatial placement with x0left/x1right/y0rear/y1apron; full ball path/capacity/default occupancy; calibrated travel/velocity; step/digit calibration; exact startup/homing/return conditions; pulse/hold timing; jam/retry/reset behavior; optional fitment and unreviewed edition differences. No numeric geometry or RGB emitter quantity is invented.

- Own Driver Reference p14 specifies25-1240/090-5034-ND; exploded bank500-7216-13 p38 specifies24-940/090-5036-ND. Both literal sources retained; no canonical coil PN selected. Resolution path: inspect factory revision documentation or an actual500-7216-13 assembly/coil label; ROM routing or a motion trace cannot settle winding fitment.

Acquisition times, source manifest reconciliation, portable excerpt imports and independent root review remain pending, so coverage retains provenance and other stated partial blockers. Schema/full address/ID/reference/EOS checks passed externally; canonical semantic and evidence gates must run after import.


## Final retained disagreements and validation

- Own Driver Reference p14 specifies25-1240/090-5034-ND; exploded bank500-7216-13 p38 specifies24-940/090-5036-ND. Both literal sources retained; no canonical coil PN selected. Resolution path: inspect factory revision documentation or an actual500-7216-13 assembly/coil label; ROM routing or a motion trace cannot settle winding fitment.
- Switch Reference p17 assigns service Select/Plus/Minus/Back CN25 input pins 4/3/2/1, ground pin 6 BLK; direct CPU mapping p22 assigns pins 1/2/3/4, ground pin 11 BLK-WHT. No canonical service contact pinout selected. Resolution path: compare factory harness/revision documentation or inspect actual CN25 and service-button assembly. Public CPU functions 109–112 are separately established by exact ROM routing.
- Node inventory p12 prints trough receiver extension 520-5345-01; Switch Reference p15 and trough BOM p36 print 520-5345-00. Both source forms remain explicit and no receiver revision is selected as canonical fitment. Resolution path: consult factory revision/parts documentation or inspect the actual trough receiver-board marking.

JSON schema, repository machine semantic validation (without repository-relative file checks), controller group validation, complete legal-address disposition, unique identifiers, mechanism references and own-title EOS N/C gates passed. Portable excerpt and knowledge-path existence/hash checks are deferred until the root imports exact files. Coverage remains partial.

C16/public116 wiring detail: own Switch Reference PDF/folio17 prints DC Sense, CN7 input4 GRY RED, ground1 BLK, Cabinet, Type -, Part Number -. Own direct CPU mapping PDF/folio22 prints Playfield Power Interlock, CN7 input4 GRY, ground5 GRY-RED, Cabinet, Interlock,180-5136-00. Canonical wiring keeps only common CN7 input4; disputed wires/ground are omitted. Cabinet is independently printed by the reference; no alternate CPU-only part or contact construction is selected. Both literal regions are cited by manual.switch and manual.cpu-connectors. This wiring-detail disagreement does not block recreation or alter the exact public116 binding.

Recorded, nonblocking distinctions under INSTRUCTIONS.md: conflict.cpu-service-pinout. Service connector details and settled CPU ordinal numbering do not change device functions, public bindings or fitted hardware. Literal readings remain retained; ignored records include the specific rationale. Genuine unresolved coil/part/fitment conflicts remain unresolved.

Recorded wiring/printed-number discrepancies ignored for author-readiness under the runbook: `conflict.cpu-service-pinout`. Functions and public routing agree; the literal disagreements remain visible in excerpts and device notes.

## Retained source records

External locators prefixed `working-root:` resolve under the configured sibling `pinmame-game-defs-working-dir`. Portable factual excerpts carry their own fail-closed repository digests; source-owned PDFs, ROMs, frames and tables remain external.

- `manual.driver` (manual): `87f012c844a217f1c3bde335b28af07bc9d36f683f48c6921896de801eb96a83`. driver_reference full printed table regions, PDF pages/printed folios12,14; 32 printed rows including blanks; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.game-of-thrones-pro.2015/factory-reference.json.txt`: `9e597bfc38273246473b0f7335fd675cc2a8c03c2ee11daca3c6e76f45b3eb71`.
- `manual.switch` (manual): `87f012c844a217f1c3bde335b28af07bc9d36f683f48c6921896de801eb96a83`. switch_reference full printed table regions, PDF pages/printed folios14,15,17; 89 printed rows including blanks; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.game-of-thrones-pro.2015/factory-reference.json.txt`: `9e597bfc38273246473b0f7335fd675cc2a8c03c2ee11daca3c6e76f45b3eb71`.
- `manual.light` (manual): `87f012c844a217f1c3bde335b28af07bc9d36f683f48c6921896de801eb96a83`. light_reference full printed table regions, PDF pages/printed folios17,18,20,21; 112 printed rows including blanks; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.game-of-thrones-pro.2015/factory-reference.json.txt`: `9e597bfc38273246473b0f7335fd675cc2a8c03c2ee11daca3c6e76f45b3eb71`.
- `manual.assemblies` (manual): `87f012c844a217f1c3bde335b28af07bc9d36f683f48c6921896de801eb96a83`. Own-title supporting assemblies, PDF pages/printed folios22,23,32,33,36,38,39,42,43,44,45,46,47; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.game-of-thrones-pro.2015/factory-reference.json.txt`: `9e597bfc38273246473b0f7335fd675cc2a8c03c2ee11daca3c6e76f45b3eb71`.
- `manual.flipper` (manual): `87f012c844a217f1c3bde335b28af07bc9d36f683f48c6921896de801eb96a83`. Both complete flipper BOMs, PDF page/printed folio37, EOS item3, coil item4 and return spring item7; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.game-of-thrones-pro.2015/factory-reference.json.txt`: `9e597bfc38273246473b0f7335fd675cc2a8c03c2ee11daca3c6e76f45b3eb71`.
- `pinmame.catalog.8e0f721e3df7` (pinmame_catalog): `756ecd840f234cf7a62f84ef331ccb8b61f0f1aeffc409bc7b776d6c037211c9`. PinmameGetGames
- `rom.routing` (rom_static_analysis): `66881f5f57c0318b90178bc538add0013cbd4be4219e1f8fc71857787321c6df`. Complete exact ROM switch/coil/LED tables; public mapping by node/position; game SHA256637acf6d6ff171def2c6e75437534ece8ea4017959eccd616829ccd621f97828; extractor SHA25659e4d5940064443b1ad2c1d6aaf05b7a3a594e71b890ec3d4287989166b40446; source/core hashes and locators retained inside artifact. Physical construction excluded. Excerpt `evidence/excerpts/stern.game-of-thrones-pro.2015/rom-routing.json.txt`: `c1a9e7105ff60ba3b22e53fb6b6c6ee457385040be87e19f3d9c923f3a3a0647`.
- `runtime.api-r2` (runtime_scenario): `a07db409be41a2f914587de65313c4b400e52c85860863bd18aacf34322b3541`. Physical-all output mask2=2, 10ms polling, fresh empty state; recorder SHA25641400f2bdf14a0bb50e14a2d3368e0058366c9c156bfb64bcc7e4ce60013c529; harness SHA25649c5e733bf436a260c915d88e275189950d8ebcc55575f01ab2d153099e1dd44; DLL SHA2561875e0961759cbd21b566d31a60c7f9e7c59c26c7f1e0d21f97b1b50118db005; full raw trace and manifest retained. Excerpt `evidence/excerpts/stern.game-of-thrones-pro.2015/runtime-observations.json.txt`: `76e985c6ea8bf1e3f7752ac1bb2bb5176cb9b0c30939c76a70164412416c6a6b`.
- `identity.opdb` (human_review): `be658179b49b2bc02dce55d928c3d6a6afe6307e2b00a0ac7ffc1a745ac2d9f3`. Exact OPDB machine recordG41d5-MKNwX; IPDB6307, Stern, physical manufacture year2015; reviewed identity snapshot from2026-10-10. Excerpt `evidence/excerpts/stern.game-of-thrones-pro.2015/identity.json.txt`: `003bc3522713969484fc759a35357ac9178db7668f70cc8eaa7a2d3ff8ce5c3a`.
- `manual.cpu-connectors` (manual): `87f012c844a217f1c3bde335b28af07bc9d36f683f48c6921896de801eb96a83`. Full direct CPU switch mapping, PDF page and printed folio 22; supporting service wiring schematic on folio 23. Full literal cells retained in manual excerpt. Excerpt `evidence/excerpts/stern.game-of-thrones-pro.2015/factory-reference.json.txt`: `9e597bfc38273246473b0f7335fd675cc2a8c03c2ee11daca3c6e76f45b3eb71`.
- `manual.node-inventory` (manual): `87f012c844a217f1c3bde335b28af07bc9d36f683f48c6921896de801eb96a83`. SPIKE node-board inventory, PDF page and printed folio 12, trough receiver extension 8a; full literal grid retained in manual excerpt. Excerpt `evidence/excerpts/stern.game-of-thrones-pro.2015/factory-reference.json.txt`: `9e597bfc38273246473b0f7335fd675cc2a8c03c2ee11daca3c6e76f45b3eb71`.
