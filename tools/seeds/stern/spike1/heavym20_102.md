# Heavy Metal (2020)

## Identity

Machine `stern.heavy-metal.2020`, driver `heavym20_102`, OPDB `GoEej-Mo1q0`, IPDB `6733`. Coverage remains partial; no author-ready claim.

Every legal public switch0–95/101–132, DIP1–8, solenoid1–32/45–48/51–72 and lamp1–112 has exactly one disposition. Printed identities remain aliases; physical matching uses node/channel positions. CPU semantic mapping preserves original numbering anomalies.

Factory PDF `HeaveyMetal_web.pdf`, SHA-256 `9a548f91e671abd747512736ba55d4de8c5a7193e0789ae14d5131906935d87c`. Source-owned documents remain external; full reviewed factual regions are preserved in the portable source-linked excerpts below.

## Recreation evidence and limits

- Full regions visually reviewed on PDF/printed folios12,14,15,16,18,19,20:35 driver rows,103 switch rows(1-90 plus13 CPU C rows),110 light rows. All numbered empty rows retained.
- CPU reference page16 prints DIP0-SW-0..7 and service0-SW-8..11. The repeated CPU direct-mapping table on page22 instead prints DIP0-SW-0,2..8 and service0-SW-9..12, different connector pins and individual service part numbers. Both are transcribed literally. Exact-ROM C1..C12 mapping controls public101..112. This is a wiring-detail/manual reprint discrepancy, not permission to overwrite either excerpt.
- Shared output topology: Driver5 Left/Right Slingshot; Driver7 Left/Right Pop Bumper; Driver10 Left/Right Control Gates. Page34 independently lists one left sling,one right sling andthree bumper bottom assemblies; page33 lists one left andone right gate. Do not duplicate public bindings silently.
- Lamp85,86,87 labels print GI quantities10,12,17; lamp87 location is Playfield/Back Panel. Other RGB quantities are not inferred.
- Manual switch14 is a genuinely empty printed row. Separately,14 ROM QR status source rows have reference/public0 and are aggregated as one non-independently-bindable ROM-only input; they are not14 physical switches or public14.
- Supporting reviewed pages22,23 CPU/DIP/service wiring;33,34 assembly top/bottom inventory;37 manual andauto launch;38 trough/sling;41 dropbank. Rendered42/43 are retained as unused scratch and are not reviewed/cited.

Own-title flipper BOMs explicitly print180-5149-00 SWITCH - END OF STROKE N/C. Matched lower EOS records set normally_closed=true while remaining virtual public transport. All other construction polarity, pulse flags and unprinted quantities remain unset.

- Headings give left500-6543-12-ND/right500-6543-02-ND; no sibling assembly identity substituted.

## Physical topology and behavior

### Three-bank drop targets

PDF/folio41 assembly500-7216-13 has three target bodies545-6305-00, three compression springs266-5089-00, three reset springs266-5003-02, one lift bracket535-9996-03, one plunger530-5757-00, one25-1240 coil090-5034-ND and one three-target opto PCB520-5252-13. Driver9 names bank reset; switch43/44/45 are left/center/right drop optos. The common lift/reset actuator and three separately sensed target positions are explicit. The drawing shows independently falling targets above the common reset frame. Their physical default raised state is a reset result, not a boot-state assertion.

Unresolved: Initial/park state, exact travel, coil pulse timing, opto rest contact construction, when reset is commanded, jam/missed-reset retry and target return timing are unresolved.

### Six-position trough and launcher

Switch reference16-21 explicitly names Trough6 throughTrough1 and22 Trough Jam. Page38 trough500-9820-00 includes coil090-5004-ND27-1500, spring266-5020-00, plunger515-7309-01, transmitter520-5344-00 andreceiver520-8509-00. Reference rows instead print receiver520-8516-00, preserved as a part-number discrepancy. Page37 auto launch500-9818-S1 has24-940 coil090-5036-ND, pivoted kicker arm535-0728-00, plunger/link515-6304-03, spring266-5020-00 andshort-arm shooter switch180-5157-01. Driver1 trough,2 auto plunger andswitch1 shooter lane are documented. The assembly proves an electromagnetic trough eject plunger andspring-return auto-launch arm alongside manual spring shooter500-6146-00-04.

Unresolved: Exact ball capacity beyond the six named occupancy positions, initial ball arrangement, jam beam ordering/threshold, ejection-to-shooter causality, launch strength/timing and retry policy require source/runtime proof.

### Shared paired control gates

Driver10 names Left/Right Control Gates on node8 DR2 with32-1250 coil090-5060-01-ND. Page33 assembly table lists one left gate511-2781-00 andone right gate511-5096-01-L8 anddraws them across the rear left/right orbit entries. This is evidence of two physical gates sharing the named output route. The reviewed manual contains no exploded gate mechanism assembly or printed gate-position sensor.

Unresolved: Gate actuator linkage/quantity, energized direction, default open/closed state, precise ball routing, timing, startup/reset andjam behavior remain unresolved; do not claim a motor/home sensor from ROM metadata.

### Lower flippers

Own-title PDF/printed folio39 supplies both complete assemblies, NC EOS, coil, plunger/crank, stop and return spring. Actual ROM coil identities are retained in the structured mechanisms.45/46 right and47/48 left are virtual binary OR mirrors; they do not add independent windings. Public lower EOS is synthesized; physical NC construction does not authorize driving the synthesized state.

## Exact runtime observations

API run started `2026-10-10T19:16:51Z`, source revision `8e0f721e3df7a2b4e8a9d2f4454ac7a9aa1ced53`, library SHA-256 `1875e0961759cbd21b566d31a60c7f9e7c59c26c7f1e0d21f97b1b50118db005`, observation SHA-256 `8f1daae40cffeec4b20745b30e2a265bad86b0bae518e160bfa85d22188127b1`. Fresh state; physical-all mask2=2;10ms polling. These are emulator observations, not physical polarity or fitment proofs.

Observed solenoid addresses: [1, 3, 4, 5, 45, 46, 47, 48, 51]. DMD layout0:128x32,4-bit. Changed frames: {'0': {'changed_frames': 504, 'recorded_events': 256, 'suppressed_events': 248}}. No activity at an address is not evidence of absence; shorter pulses can be missed.

- Step1 coin 1: LEFT COIN: 51 [255, 0].
- Step2 coin 2: LEFT COIN: 51 [255, 0].
- Step3 coin 3: LEFT COIN: 51 [255, 0].
- Step4 coin 4: LEFT COIN: 51 [255, 0].
- Step5 coin 5: LEFT COIN: 51 [255, 0].
- Step6 coin 6: LEFT COIN: 51 [255, 0].
- Step7 start: START BUTTON: 1 [210, 0, 210, 0, 210, 0, 210, 0, 210, 0, 210, 0].
- Step8 post-start serve observation: 1 [210, 0, 210, 0, 210].
- Step9 remove one ball from TROUGH 4 after attempted serve: 1 [0].
- Step13 left flipper button: 3 [255, 30, 0], 47 [255, 0], 48 [255, 0].
- Step14 right flipper button: 4 [255, 30, 0], 45 [255, 0], 46 [255, 0].
- Step15 LEFT SLINGSHOT: 5 [194, 0].

Full raw events, observations, DLL/scenario/ROM hashes and run manifest remain under `runtime/heavym20_102-api-r2`. A post-serve synthetic trough-to-shooter transfer is conditional gameplay evidence; host write/readback alone is not a ROM response.

## Manual devices without a proven public binding

| Table / PDF | Printed ID | Name | Circuit | Disposition |
| --- | --- | --- | --- | --- |

## Remaining gaps

Unresolved switch construction polarity other than positively printed EOS; spatial placement with x0left/x1right/y0rear/y1apron; full ball path/capacity/default occupancy; calibrated travel/velocity; step/digit calibration; exact startup/homing/return conditions; pulse/hold timing; jam/retry/reset behavior; optional fitment and unreviewed edition differences. No numeric geometry or RGB emitter quantity is invented.


Acquisition times, source manifest reconciliation, portable excerpt imports and independent root review remain pending, so coverage retains provenance and other stated partial blockers. Schema/full address/ID/reference/EOS checks passed externally; canonical semantic and evidence gates must run after import.


## Final retained disagreements and validation

- Switch Reference p16 assigns service Select/Plus/Minus/Back CN25 input pins 4/3/2/1, ground pin 6 BLK; direct CPU mapping p22 assigns pins 1/2/3/4, ground pin 11 BLK-WHT. No canonical service contact pinout selected. Resolution path: compare factory harness/revision documentation or inspect actual CN25 and service-button assembly. Public CPU functions 109–112 are separately established by exact ROM routing.

The service pinout record is ignored for author-readiness because both readings establish the same functions, public addresses and fitment. For the power interlock, own Switch Reference p16 prints CN7 pin4 GRY RED input/pin1 BLK ground while CPU mapping p22 prints pin4 GRY input/pin5 GRY RED ground. Both literal readings remain in `manual.switch` and `manual.cpu-connectors`; only the agreeing CN7 pin4 endpoint is canonical. These wiring-detail discrepancies do not establish physical contact polarity.
- Switch Reference p15 trough sensor rows 16–22 print receiver 520-8516-00 with transmitter 520-5344-00; own trough 500-9820-00 BOM p38 prints receiver 520-8509-00 and the same transmitter. No canonical receiver PN selected. Resolution path: inspect factory trough revision/parts documentation or the actual receiver-board marking. Exact ROM routing cannot resolve physical part fitment.

JSON schema, repository machine semantic validation (without repository-relative file checks), controller group validation, complete legal-address disposition, unique identifiers, mechanism references and own-title EOS N/C gates passed. Portable excerpt and knowledge-path existence/hash checks are deferred until the root imports exact files. Coverage remains partial.

## Retained source records

External `working-root:` locators resolve under the configured sibling working directory. Portable full factual transcripts are UTF-8 JSON text with the explicit `.json.txt` suffix; the canonical machine-evidence format remains separate.

- `manual.driver` (manual): `9a548f91e671abd747512736ba55d4de8c5a7193e0789ae14d5131906935d87c`. driver_reference full printed table regions, PDF pages/printed folios12; 35 printed rows including blanks; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.heavy-metal.2020/factory-reference.json.txt`: `2f224e103133fc62f9823d3233f91ee41c8897167475862a387592bcbb56f6dc`.
- `manual.switch` (manual): `9a548f91e671abd747512736ba55d4de8c5a7193e0789ae14d5131906935d87c`. switch_reference full printed table regions, PDF pages/printed folios14,15,16; 103 printed rows including blanks; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.heavy-metal.2020/factory-reference.json.txt`: `2f224e103133fc62f9823d3233f91ee41c8897167475862a387592bcbb56f6dc`.
- `manual.light` (manual): `9a548f91e671abd747512736ba55d4de8c5a7193e0789ae14d5131906935d87c`. light_reference full printed table regions, PDF pages/printed folios18,19,20; 110 printed rows including blanks; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.heavy-metal.2020/factory-reference.json.txt`: `2f224e103133fc62f9823d3233f91ee41c8897167475862a387592bcbb56f6dc`.
- `manual.assemblies` (manual): `9a548f91e671abd747512736ba55d4de8c5a7193e0789ae14d5131906935d87c`. Own-title supporting assemblies, PDF pages/printed folios22,23,33,34,37,38,41; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.heavy-metal.2020/factory-reference.json.txt`: `2f224e103133fc62f9823d3233f91ee41c8897167475862a387592bcbb56f6dc`.
- `manual.flipper` (manual): `9a548f91e671abd747512736ba55d4de8c5a7193e0789ae14d5131906935d87c`. Both complete flipper BOMs, PDF page/printed folio39, EOS item3, coil item4 and return spring item7; reviewed from derived-resolution renders on2026-10-10; transcriberGPT-6 Codex; pdfplumber0.11.10 / PyMuPDF1.28.2 Excerpt `evidence/excerpts/stern.heavy-metal.2020/factory-reference.json.txt`: `2f224e103133fc62f9823d3233f91ee41c8897167475862a387592bcbb56f6dc`.
- `pinmame.catalog.8e0f721e3df7` (pinmame_catalog): `756ecd840f234cf7a62f84ef331ccb8b61f0f1aeffc409bc7b776d6c037211c9`. PinmameGetGames
- `rom.routing` (rom_static_analysis): `bdda0f46af8528cabb1b9baa8f447b9f01dd71812741b007e7ce54aac3ecdf3c`. Complete exact ROM switch/coil/LED tables; public mapping by node/position; game SHA25605c893e751c9b0975b2de0cb7bf8f23c7f009e34b53ae645d74e3a46cfbc017a; extractor SHA25659e4d5940064443b1ad2c1d6aaf05b7a3a594e71b890ec3d4287989166b40446; source/core hashes and locators retained inside artifact. Physical construction excluded. Excerpt `evidence/excerpts/stern.heavy-metal.2020/rom-routing.json.txt`: `a064b29c96cadf74a9123fbd0cd6c23afd45b590d47aa98e4529727064e3f1bb`.
- `runtime.api-r2` (runtime_scenario): `8f1daae40cffeec4b20745b30e2a265bad86b0bae518e160bfa85d22188127b1`. Physical-all output mask2=2, 10ms polling, fresh empty state; recorder SHA25641400f2bdf14a0bb50e14a2d3368e0058366c9c156bfb64bcc7e4ce60013c529; harness SHA25649c5e733bf436a260c915d88e275189950d8ebcc55575f01ab2d153099e1dd44; DLL SHA2561875e0961759cbd21b566d31a60c7f9e7c59c26c7f1e0d21f97b1b50118db005; full raw trace and manifest retained. Excerpt `evidence/excerpts/stern.heavy-metal.2020/runtime-observations.json.txt`: `c9a9375442209f8253b67c0e258533f21b075f525a71729ee8047fae1b8073b1`.
- `identity.opdb` (human_review): `be658179b49b2bc02dce55d928c3d6a6afe6307e2b00a0ac7ffc1a745ac2d9f3`. Exact OPDB machine recordGoEej-Mo1q0; IPDB6733, Stern, physical manufacture year2020; reviewed identity snapshot from2026-10-10. Excerpt `evidence/excerpts/stern.heavy-metal.2020/identity.json.txt`: `e9d5f7c72adf623f2f51f12b57b537b3ca1bb69adf2ee77096797d9df5ccaf81`.
- `manual.cpu-connectors` (manual): `9a548f91e671abd747512736ba55d4de8c5a7193e0789ae14d5131906935d87c`. Full direct CPU switch mapping, PDF page and printed folio 22; supporting service wiring schematic on folio 23. Full literal cells retained in manual excerpt. Excerpt `evidence/excerpts/stern.heavy-metal.2020/factory-reference.json.txt`: `2f224e103133fc62f9823d3233f91ee41c8897167475862a387592bcbb56f6dc`.
