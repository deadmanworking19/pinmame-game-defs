# Primus (2018)

## Current PinMAME adapter

The active adapter is PinMAME `46e1a01a0f73dc5ce163d98db1ae435883ecc450`. Virtual GAME ON is public solenoid 33; it represents an armed lower-flipper reflex, not a physical relay. Direct reads at 34-36 are aliases; the canonical plugin and aggregate address is 33. The current driver samples I/O at 1 kHz, retains short host switch edges, and keeps newly observed coil pulses for at least one frame. The modulated poll includes lower binary mirrors 45-48 because nSolenoids is at least 48. Plugin DIP group 6 now maps ordinals 1-8 to bank 0 bits 0-7 correctly. Lower EOS synthesis is unchanged. Historical runtime traces and ROM-table excerpts remain scoped to their original revision; this source audit adds no new gameplay observation or physical fitment evidence.

Source records: `pinmame.adapter.current` provides the pinned code and active-route excerpts; `pinmame.catalog.current` provides the current public driver descriptor. Both supplement the historical sources below.

## Identity

Machine `stern.primus.2018`, driver `primus_103`, OPDB `GRYX4-MvBpz`, IPDB `6610`. Coverage remains partial; no author-ready claim.

Every legal public switch0–95/101–132, DIP1–8, solenoid1–32/45–48/51–72 and lamp1–80 has exactly one disposition. Printed identities remain aliases; physical matching uses node/channel positions. CPU semantic mapping preserves original numbering anomalies.

Factory PDF `Primus_web.pdf`, SHA-256 `e625023cefa445d0f38989d7d8d06f717f79b3f24ab50edb8622dfae5d5f9655`. Source-owned documents remain external; the full reviewed factual table regions and construction supplements are preserved in the source-linked portable excerpts below.

## Recreation evidence and limits

- All Driver Reference rows (35), Switch Reference rows (71), and Light Reference rows (78, including empty 77 and 78) were visually checked on PDF/printed pages 12, 13, 15 and 17. Header/footer artifacts in the mechanical candidate are excluded.
- Driver 17-31 are backbox stepper enable/phase wires at node 11 LP positions, not public solenoid callbacks. Public reel position/home feedback must use GetMech and the pinned source mechanism registration; the manual phase wires remain internal channels.
- Literal manual DIP addresses are preserved, including C1 0-SW-0 and C2 0-SW-2; exact-ROM CPU routing is C1-C8 to 101-108. No physical polarity is inferred.
- Supporting pages visually checked: 20 (country DIP table and service switch wiring), 36 (four-score-reel bank, credit reel, individual reel and long-range opto assembly), 39 (shooter, trough coil, bullseye and knocker), 41 (non-powered bumper and 30-degree eject).
- The same score-reel part list prints DECAL: SCORE and DECAL: CREDITS REEL on consecutive rows with quantity 1 each; these identify alternatives/subassembly labeling and do not prove two reels per instance.

Own-title flipper BOMs explicitly print180-5149-00 SWITCH - END OF STROKE N/C. Matched lower EOS records set normally_closed=true while remaining virtual public transport. All other construction polarity, pulse flags and unprinted quantities remain unset.


## Physical topology and behavior

### Four score reels and credit reel

PDF/folio 36: score bank 511-7614-00 contains four score reel assemblies 511-7648-00 and eight white LED boards 520-5307-00. Credit assembly 511-7615-00 contains one credit reel 511-7648-01 and one white LED board. Individual reel 511-7648-00 uses unipolar stepper motor 041-5105-00, reel 515-9819-00, motor bracket 535-1131-00, and opto sensor PCB 520-6960-00. Driver Reference 17-31 supplies credit/1s/10s/100s/1000s enable plus phase 1 and phase 2 wires; Switch Reference 46-50 identifies one opto home input per reel. This proves the actuator/sensor topology and a home mark. The drawing shows direct shaft drive of each reel. Ball path is not applicable to these backbox devices.

Unresolved: No manual timing, step-to-digit calibration, direction sequence, startup homing order, mechanical zero phase, jam timeout, retry/reset behavior or homing switch rest construction is specified on the reviewed pages.

### Manual shooter, trough and top eject

PDF/folio 39: beehive shooter 511-0009-07-04 is a manual spring/plunger assembly. Trough coil assembly 500-7286-00 uses 090-5044-ND 26-1200 coil, conical compression spring and plunger; PDF/folio 41 30-degree eject 500-6511-03-ND likewise uses a 26-1200 coil and spring-return plunger. Reference tables name shooter-lane switch 5, center drain 16, trough opto 17, top eject switch 20, trough output 6 and top eject output 5. The spring/plunger construction supports spring return after a coil pulse; these pages do not establish a complete ball route between the named switches.

Unresolved: Exact trough ball capacity, movement timing, eject retry/jam detection, switch-to-ball state and complete ball routing need script/runtime or additional physical evidence.

### Lower flippers

Own-title PDF/printed folio38 supplies both complete assemblies, NC EOS, coil, plunger/crank, stop and return spring. Actual ROM coil identities are retained in the structured mechanisms.45/46 right and47/48 left are virtual binary OR mirrors; they do not add independent windings. Public lower EOS is synthesized; physical NC construction does not authorize driving the synthesized state.

### Physical reels, internal phase controls and apron LCD

Four physical score reels and one credit reel belong in the mechanism inventory. Manual Driver17–31 are Node11 LP15..1 enable/phase signals for internal stepper control, withheld from ordinary public output export. Public solenoids17..31 are zero slots; never bind reel phases there. Controller520-6961-00 supplies five two-phase motor connections and five opto-home circuits; current-limit/OCP pin labels remain literal. Small520-6964-00 LCD uses128x32 drawing label and14-pin ribbon036-8045-132. The128x32 PinMAME DMD callback is its transport. PinMAME describes the display as an apron LCD, but the cited own-manual pinout establishes no mounting location. This definition uses schema video and withholds physical location and coordinates until a title-correct assembly drawing or photo proves mounting.

GetMech ordering is subsystem motors, then steppers, then registered limit motors, and an absent entry also returns zero. The retained harness samples only indices0..3 and does not itself establish all five reel ordinals, digit calibration, phase direction, startup homing or jam recovery; those remain explicit gaps.

## Exact runtime observations

API run started `2026-10-10T19:21:29Z`, source revision `8e0f721e3df7a2b4e8a9d2f4454ac7a9aa1ced53`, library SHA-256 `1875e0961759cbd21b566d31a60c7f9e7c59c26c7f1e0d21f97b1b50118db005`, observation SHA-256 `6e00ff4a9709bb546f6df1b6a28e27e13665fff0aaaf3f8fa8b12c1914a0f3a4`. Fresh state; physical-all mask2=2;10ms polling. These are emulator observations, not physical polarity or fitment proofs.

Observed solenoid addresses: [1, 2, 3, 4, 6, 8, 45, 46, 47, 48]. DMD layout0:128x32,4-bit. Changed frames: {'0': {'changed_frames': 177, 'recorded_events': 177, 'suppressed_events': 0}}. No activity at an address is not evidence of absence; shorter pulses can be missed.

- Step7 start: START BUTTON: 6 [155, 0, 155, 0, 155, 0, 155, 0, 155, 0, 155, 0].
- Step8 post-start serve observation: 6 [155, 0, 155, 0, 155].
- Step9 remove one ball from TROUGH OPTO after attempted serve: 6 [0].
- Step12 left flipper button: 1 [255, 0], 3 [255, 0], 47 [255, 0], 48 [255, 0].
- Step13 right flipper button: 2 [255, 0], 4 [255, 0], 45 [255, 0], 46 [255, 0].
- Step14 LEFT SLINGSHOT: 8 [200, 0].

Full raw events, observations, DLL/scenario/ROM hashes and run manifest remain under `runtime/primus_103-api-r2`. A post-serve synthetic trough-to-shooter transfer is conditional gameplay evidence; host write/readback alone is not a ROM response.

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


Full own-title CPU direct mapping folio19 was additionally reviewed: service CN25 pins4/3/2/1 and ground6 BLK agree with this title’s reference. The skipped0-SW-1 printed numbering remains unresolved.

## Final retained disagreements and validation

- Switch Reference p13 Trough Opto prints 515-0215-00 tx / 515-0215-01 rx; the long-range opto assembly BOM p36 prints 500-0215-00 emitter / 500-0215-01 receiver. The common suffix and assembly class suggest a prefix discrepancy, but exact assembly-to-trough fitment is not independently proven. Both literal assertions are retained; no canonical sensor PN selected. Resolution path: consult factory revision/parts documentation or inspect the actual trough sensor and its assembly marking.
- The manual CPU DIP/service numbering omits 0-SW-1 and shifts the subsequent printed addresses; exact ROM Node 0 positions 0–7 mirror physical DIP ordinals 1–8 as public 101–108 and positions 8–11 are Select/Plus/Minus/Back public 109–112. Canonical public bindings follow verified ROM routing; source-literal addresses remain aliases. Resolution path: check factory CPU mapping documentation or exact machine wiring to resolve the printed numbering discrepancy; do not remap the API from printed IDs alone.

The CPU numbering record is ignored for author-readiness: physical ordinal/function and public API behavior are established, leaving only a printed address discrepancy. The unresolved trough part fitment remains a physical conflict.

JSON schema, repository machine semantic validation (without repository-relative file checks), controller group validation, complete legal-address disposition, unique identifiers, mechanism references and own-title EOS N/C gates passed. Portable excerpt and knowledge-path existence/hash checks are deferred until the root imports exact files. Coverage remains partial.

Peer review correction: exported solenoid51–53 are factory Digital Out meter/ticket control signals. Their public solenoid group/address and literal wiring remain; canonical IDs use control.* and kind=control_signal. No meter coil winding is inferred.

## Retained source records

External locators prefixed `working-root:` resolve under the configured sibling `pinmame-game-defs-working-dir`. Portable factual excerpts carry their own fail-closed repository digests; source-owned PDFs, ROMs, frames and tables remain external.

- `manual.driver` (manual): `e625023cefa445d0f38989d7d8d06f717f79b3f24ab50edb8622dfae5d5f9655`. driver_reference full printed table regions, PDF pages/printed folios12; 35 printed rows including blanks; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.primus.2018/factory-reference.json.txt`: `f9825d3a017330898ea54c2c326d49166e7f8e14973b450b1264aace2e009a35`.
- `manual.switch` (manual): `e625023cefa445d0f38989d7d8d06f717f79b3f24ab50edb8622dfae5d5f9655`. switch_reference full printed table regions, PDF pages/printed folios12,13,15; 71 printed rows including blanks; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.primus.2018/factory-reference.json.txt`: `f9825d3a017330898ea54c2c326d49166e7f8e14973b450b1264aace2e009a35`.
- `manual.light` (manual): `e625023cefa445d0f38989d7d8d06f717f79b3f24ab50edb8622dfae5d5f9655`. light_reference full printed table regions, PDF pages/printed folios15,17; 78 printed rows including blanks; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.primus.2018/factory-reference.json.txt`: `f9825d3a017330898ea54c2c326d49166e7f8e14973b450b1264aace2e009a35`.
- `manual.assemblies` (manual): `e625023cefa445d0f38989d7d8d06f717f79b3f24ab50edb8622dfae5d5f9655`. Own-title supporting CPU direct mapping and assemblies, PDF pages/printed folios 19,20,36,39,41; full printed supporting regions retained. Excerpt `evidence/excerpts/stern.primus.2018/factory-reference.json.txt`: `f9825d3a017330898ea54c2c326d49166e7f8e14973b450b1264aace2e009a35`.
- `manual.flipper` (manual): `e625023cefa445d0f38989d7d8d06f717f79b3f24ab50edb8622dfae5d5f9655`. Both complete flipper BOMs, PDF page/printed folio38, EOS item3, coil item4 and return spring item7; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.primus.2018/factory-reference.json.txt`: `f9825d3a017330898ea54c2c326d49166e7f8e14973b450b1264aace2e009a35`.
- `manual.reel-controller` (manual): `e625023cefa445d0f38989d7d8d06f717f79b3f24ab50edb8622dfae5d5f9655`. Full520-6961-00 controller and520-6964-00 LCD pinouts PDF/printed folio28; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.primus.2018/factory-reference.json.txt`: `f9825d3a017330898ea54c2c326d49166e7f8e14973b450b1264aace2e009a35`.
- `pinmame.catalog.8e0f721e3df7` (pinmame_catalog): `756ecd840f234cf7a62f84ef331ccb8b61f0f1aeffc409bc7b776d6c037211c9`. PinmameGetGames
- `rom.routing` (rom_static_analysis): `bcc66ffeb57fef1653c72a28e9eac61c80d498242f0395f47234e6e6e464950b`. Complete exact ROM switch/coil/LED tables; public mapping by node/position; game SHA256e72fcdfc911ce672e3b691c6720fcea4f0caa8fcdff20a6613fc3a358b28609a; extractor SHA25659e4d5940064443b1ad2c1d6aaf05b7a3a594e71b890ec3d4287989166b40446; source/core hashes and locators retained inside artifact. Physical construction excluded. Excerpt `evidence/excerpts/stern.primus.2018/rom-routing.json.txt`: `3615e6ddc0a6af7e02523322459d23b6b6a23c4bd85ff1bf9ba3317741d86980`.
- `runtime.api-r2` (runtime_scenario): `6e00ff4a9709bb546f6df1b6a28e27e13665fff0aaaf3f8fa8b12c1914a0f3a4`. Physical-all output mask2=2, 10ms polling, fresh empty state; recorder SHA2567d924857bb8c76d4039c900ecaa329023905a21a654a6fdfa85180446013d84c; harness SHA25649c5e733bf436a260c915d88e275189950d8ebcc55575f01ab2d153099e1dd44; DLL SHA2561875e0961759cbd21b566d31a60c7f9e7c59c26c7f1e0d21f97b1b50118db005; full raw trace and manifest retained. Excerpt `evidence/excerpts/stern.primus.2018/runtime-observations.json.txt`: `961430b18fefd098b32d5cba2004a8b55da62fabf9377824365aa928a62a75ca`.
- `identity.opdb` (human_review): `be658179b49b2bc02dce55d928c3d6a6afe6307e2b00a0ac7ffc1a745ac2d9f3`. Exact OPDB machine recordGRYX4-MvBpz; IPDB6610, Stern, physical manufacture year2018; reviewed identity snapshot from2026-10-10. Excerpt `evidence/excerpts/stern.primus.2018/identity.json.txt`: `9e528d125326d795de95263cccd52d328af9fe1dee8fb6215d159b2d1e5df23a`.
