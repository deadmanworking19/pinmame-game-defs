# Game of Thrones (Limited Edition) (2015)

## Identity

Reviewed partial definition; unresolved authoring dimensions are recorded below. One canonical binding is emitted per public address; complete manufacturer facts remain in the reviewed full JSON/Markdown rather than being inferred from emulator flags or similarly numbered entries.

Identity: machine `stern.game-of-thrones-limited-edition.2015`, OPDB `G41d5-M9REd`, IPDB 6309; exact retained ROM driver `got_137h`.

Factory PDF: `GameOfThrones_LE_Prem_web.pdf`, SHA-256 `e559316b46e768099cd7165540c5cabf0d0f78a9eebd4e30051453ad6637c415`, 56 pages.

Reference pages/folios: 12, 14, 15, 17, 18, 20, 21, 22, 23. Supplemental assembly pages/folios: 38, 41, 43, 48, 51, 52, 53. Every claimed full table region was checked with view_image against the retained/derived render; PDF page and printed folio are equal.

Extraction/render workflow: Python3.13.5, pdfplumber0.11.10 grid extraction; repository tools/render_excerpt_image.py using PyMuPDF1.28.2 and Pillow12.3.0. Original reference/assembly render DPI derives from embedded raster/native width or smallest vector type. Render_manifest pins each actual WebP SHA and available derivation sidecar. The own CPU appendix audit renders were supplied by the peer curator and independently viewed; their derivation sidecars were not supplied. Full13-row CPU direct regions are reviewed on PDF/folios24. Review performed2026-10-10; no unobserved acquisition timestamp asserted. Copyrighted Stern/title manuals stay outside Git; only derived factual tables and scoped excerpts are proposed.

## Controller contract

Inputs enumerate128 legal switch slots0–95,101–132 plus8 DIP ordinals1–8. Outputs enumerate58 solenoid slots1–32,45–48,51–72 plus lamps1–272. Unmapped inputs remain explicit unknown placeholders; exact-ROM unmapped outputs are virtual unused. Public address capacity does not prove fitment.

DIP ordinals use LibPinMAME bank0 bits0–7 and mirror into switches101–108 each frame. Direct mirror writes are overwritten. The exact-head plugin’s DIP accessors use shifted bit indices, so the profile omits that transport. CPU service buttons109–112 and interlock116 use exact title routing; no startup constant is declared from emulator rest flags.

Lower flipper actual coil channels retain their factory connections. Public45/46 right and47/48 left are identical binary OR mirrors of the named power/hold channels; they are virtual copies, not extra windings. Lower EOS is synthesized after two VBLANKs and direct writes are overwritten. Physical N/C is independently proved only for part180-5149-00 by own-title flipper BOM item3 and exact switch-reference reconciliation. Other polarity, pulse, initial_active and constant_active declarations are omitted.

RGB labels identify individual public channels where factory text gives color. This draft declares no shared-emitter quantity, co-located address set, or coordinates from labels. Controller class bits are routing/filter facts only. Lamp levels use0–255; binary nonzero state and modulated traversal behavior must remain distinct.

## Display evidence

The complete speaker-panel BOM proves physical LED matrix part520-5052-15. PinMAME separately exposes DMD transport index0 at128×32; these dimensions come from source, not from a guessed LED count. Own manual backbox drawing identifies the speaker panel, so its cabinet/backbox spatial placement is not_applicable to playfield coordinates.

## Recreation mechanisms, topology and causality

### Dragon wing drive

The assembly drawing shows a shaft driving paired gear segments, left/right wing rivet assemblies, torsion spring, cam and collar/switch actuator. BOM item29 is one unipolar stepper motor041-5105-00; item17 is one micro-switch180-5119-02. The switch table names Dragon Home88 at11-SW-4; two printed motor channels share node10 CN16, pins11/12, addresses10-LP-10/11. Limit: The manual assembly title and BOM say RAPTOR although the game reference names Dragon. This is retained literally. Limit: No numeric wing angles, step count, gear ratio, homing algorithm, pulse timing or jam-recovery behavior is established. Locators: PDF/folio48 §5.28 assembly511-7569-00; PDF/folio17 switch88 Dragon Home; PDF/folio23 separate Motor Reference IDs1–2. PinMAME models node10 wing stepper with home88; optional node12 topper stepper with internal home121. GetMech0/1 returns model step0–199 where instantiated. These positions are emulator steps, not wing angles or measured travel. No public coil/lamp actuator exists for the reviewed printed wing motor channels; no binding is invented.

Bindings: actuators no supported public actuator binding; sensors `switch.088`.

### LE elevator and throne

Elevator assembly has a26-1200 no-diode coil090-5044-ND, plunger511-7625-00, compression spring, hinged deflector weldment and pivot shaft. Throne assembly has a mini27-950 coil090-5084-01, ball seat535-1232-01, ball catcher535-1287-00 and one micro-switch180-5119-02. Back-panel drawing places the elevator under the elevated playfield and labels electric gates on its left/right. The assembly heading distinguishes LE and Premium part numbers. Limit: Back-panel assembly heading/drawing reviewed; its BOM is outside this supplement’s claimed complete-table transcription. Limit: No measured travel, pulse/hold timing, ball transfer sequence, jam behavior or distinction between normal position and power-off position is established. Locators: PDF/folio52 §5.37 assembly500-9938-00; PDF/folio52 §5.38 assembly511-7675-01; PDF/folio53 §5.39 Back Panel Assembly LE500-9930-00 / Premium500-9930-01; driver/switch rows in reference tables.

Bindings: actuators `solenoid.026`, `solenoid.027`, `solenoid.029`, `solenoid.022`; sensors `switch.087`, `switch.089`.

### Diverter

Assembly has a26-1200 no-diode coil090-5044-ND, plunger, compression spring, diverter gate, shaft and link. Limit: No dedicated home sensor is listed in this complete BOM; this does not prove that no sensor exists elsewhere. No timing or travel limit is supplied. Locators: PDF/folio51 §5.36 assembly500-9945-00. Driver refs27 ElevatorDiverter and30 LoopDiverter share coil090-5044-ND with generic assembly500-9945-00. Part equality does not identify which specific installation the assembly drawing depicts; no unique assembly-to-circuit assignment is asserted.

Bindings: actuators `solenoid.030`; sensors no supported public sensor binding.

### Three drop targets and shared reset

Three target bodies545-6305-00 each have a compression spring266-5089-00 and target reset spring265-5003-02. One plunger530-5757-00, one shared lift bracket535-9996-03, one coil and conical compression spring266-5020-00 operate the bank. The drawing shows three individually dropping targets above the shared reset mechanism. One PCB520-5252-13 senses the three target states; own switch reference7/8/9 identifies their independent circuits. Driver14 specifies25-1240/090-5034-ND, but own assembly item17 specifies24-940/090-5036-ND. Exact winding/part fitment is unresolved; no canonical coil PN is selected. Limit: No measured travel, physical polarity, startup/default target states, coil pulse/hold duration, reset sequence, jam detection or retry timing is established. Factory revision documentation or actual installed coil label is required to resolve the coil conflict. Locators: PDF/folio43 §5.16 assembly500-7216-13, full22-row BOM; PDF/folio14 driver14 Drop Reset; PDF/folio15 switches7/8/9 and opto PCB520-5252-13.

Bindings: actuators `solenoid.014`; sensors `switch.007`, `switch.008`, `switch.009`.

### Upper right flipper

Own LE Driver Reference14 names upper right flipper coil16; Switch Reference15 names its second-leaf button12. These explicit upper-playfield control associations are scoped separately from the elevator/throne. No dedicated upper EOS circuit is listed in the reviewed switch reference; this does not prove universal sensor absence. Exact upper assembly identity, construction polarity, pulse/hold behavior, rest angle, stroke threshold, startup/reset and jam handling remain unresolved.

Bindings: actuators `solenoid.016`; sensors `switch.012`.

### Upper left flipper

Own LE Driver Reference14 names upper left flipper coil18; Switch Reference15 names its second-leaf button13. These explicit upper-playfield control associations are scoped separately from the elevator/throne. No dedicated upper EOS circuit is listed in the reviewed switch reference; this does not prove universal sensor absence. Exact upper assembly identity, construction polarity, pulse/hold behavior, rest angle, stroke threshold, startup/reset and jam handling remain unresolved.

Bindings: actuators `solenoid.018`; sensors `switch.013`.

### Trough positions and jam sensor

The exact manual reference rows name Trough1–6 and TroughJam; the driver table names Trough eject. Six position labels are retained individually. No eject pulse, jam recovery, installed-ball startup configuration or ball-transfer timing is declared from labels alone.

Bindings: actuators `solenoid.001`; sensors `switch.020`, `switch.021`, `switch.022`, `switch.023`, `switch.024`, `switch.025`, `switch.026`.

### Lower flippers and synthesized EOS contract

Exact manual flipper BOM item3 proves EOS part180-5149-00 normally closed. Actual coil references are distinct from virtual45–48 binary OR mirrors. PinMAME synthesizes lower EOS after two VBLANKs and overwrites direct EOS writes. Button leaves round-trip with keyboard handling disabled; keyboard handling rewrites leaves. No physical pulse/hold duty, rest angle, startup active state or EOS travel threshold is declared. Literal alternative coil/bat/BOM rows are retained in reviewed excerpts and do not prove variant fitment on their own.

Bindings: actuators `solenoid.003`, `solenoid.008`; sensors `switch.010`, `switch.011`, `switch.016`, `switch.005`.

PinMAME source distinguishes LE/Premium upper flippers/wing stepper from Pro coil18 dragon motor. This draft contains only got_137h; it does not inherit got_137 Pro physical compatibility from the old stub grouping. Optional topper references121 and250–265 are ROM/accessory metadata; own manual does not establish topper fitment/construction. Internal home121 and GetMech step results are model facts, not an independently verified physical sensor or animation-angle calibration.

## Conflicts and unresolved facts

- ROM public75 SLAM TILT is node1-SW21, but manufacturer same circuit is printed72 SixthCoin. Manufacturer SlamTilt75 is1-SW22 and has no matching ROM switch row. Both source literals retained; no physical identity/polarity inference.
- Own Driver Reference PDF/folio14 specifies DropReset14 coil25-1240/090-5034-ND; own full22-row assembly500-7216-13 PDF/folio43 §5.16 item17 specifies24-940/090-5036-ND, COIL - 24-940, NO DIODE. Same bank and optoPCB520-5252-13 reconcile the assembly identity. Both literals are retained; no canonical winding/PN is selected. Resolve against exact factory revision documentation or installed coil label.
- Own Switch Reference PDF/folio17 assigns Select/Plus/Minus/Back CN25 inputs4/3/2/1 and ground6 BLK; own direct CPU mapping PDF/folio24 assigns inputs1/2/3/4 and ground11 BLK-WHT. Both literal regions are retained. No canonical disputed service pins/grounds are selected; exact ROM public109–112 functions remain unchanged. Resolve from exact factory harness/revision authority or inspected own machine.
- Own direct CPU mapping PDF/folio24 omits0-SW-1 and shifts DIP2..8/service Select..Back to0-SW2..8/9..12. Own Switch Reference17 and ROM positions agree DIP2..8/service at1..7/8..11. Direct appendix literal aliases are retained separately; no circuit equality is inferred from its shifted numbers.
- Own Switch Reference PDF/folio17 C16 prints CN7 input4 GRY-RED (GOT spelling GRY RED), ground1 BLK; own direct CPU mapping PDF/folio24 C16 prints input4 GRY, ground5 GRY-RED. Both regions address0-SW-16/public116, but canonical disputed input wire/ground endpoint is withheld. The reference labels DC Sense with blank location and no part; direct mapping labels Playfield Power Interlock, Cabinet, part180-5136-00. No canonical alternative part/location is added. Public running/closed-door state is an emulator fact and cannot resolve physical pinout, contact construction or normally-closed polarity. Resolve from exact factory harness/revision authority or inspected own machine.


- Spatial playfield placement is unresolved throughout. Global convention is x0left/x1right, y0rear/y1apron; no coordinates or dimensions were inferred from location prose.
- Mechanism coverage remains partial: measured travel/speed, pulse/hold duty, startup/reset states, ball transfer timing and jam recovery are absent unless explicitly identified above as source-model facts. Assembly absence of a sensor is scoped to the reviewed BOM; it does not prove global absence.
- Blank cells remain literal blanks, structurally merged cells remain null in the full reference grids. Motor continuation type/part blanks are not silently repeated. Latent CAD text and sliced table columns were corrected against visible rendering with individual disclosures.
- Manual row names establish documented circuits; coin/ticket accessories and ROM topper metadata do not establish fitted optional configuration.

## Documented physical rows without a supported public reconciliation

These factual rows stay in the reviewed excerpt. They are not new API bindings, and their omission from a public group does not establish absence of physical hardware.

| Table | Printed ID | Name | Manufacturer circuit | PDF/folio | Reason |
| --- | --- | --- | --- | --- | --- |
| driver_reference | 33 | Coin Meter | 1-DR-2 | 14 | No supported exact circuit reconciliation in this draft; see full row facts for all columns. |
| driver_reference | 34 | Ticket Meter | 1-DR-3 | 14 | No supported exact circuit reconciliation in this draft; see full row facts for all columns. |
| switch_reference | 72 | Sixth Coin | 1-SW-21 | 17 | No supported exact circuit reconciliation in this draft; see full row facts for all columns. |
| switch_reference | 75 | Slam Tilt | 1-SW-22 | 17 | No supported exact circuit reconciliation in this draft; see full row facts for all columns. |
| light_reference | 245 | Throne | 11-LP-4 | 23 | No supported exact circuit reconciliation in this draft; see full row facts for all columns. |
| motor_reference | 1 | Dragon Motor 1 | 10-LP-10 | 23 | No supported exact circuit reconciliation in this draft; see full row facts for all columns. |
| motor_reference | 2 | Dragon Motor 2 | 10-LP-11 | 23 | No supported exact circuit reconciliation in this draft; see full row facts for all columns. |

## Evidence import contract

Copy external reviewed `stern.game-of-thrones-limited-edition.2015.json` and `stern.game-of-thrones-limited-edition.2015.md` byte-for-byte to `evidence/excerpts/stern.game-of-thrones-limited-edition.2015/factory-tables.json` and `factory-tables.md`; copy exact `rom-maps/got_137h.json` to `evidence/excerpts/stern.game-of-thrones-limited-edition.2015/rom-routing.json`. Draft sources already pin their actual external bytes. These are proposed portable destinations, currently absent in the read-only repository; root must verify imported hashes and run repository validation before installation. Source/manual URIs retain actual external identities for traceability.

No acquisition time was invented; retained manifest/log identities govern evidence time. No runtime motion scenario is claimed by this draft. OPDB identity snapshot and exact ROM/source program/log hashes are retained in sources. A source hash proves bytes, not physical truth or rendering correctness. Root independent manual and draft review remains required.

Recorded wiring/printed-number discrepancies ignored for author-readiness under the runbook: `got.cpu-service-pinout`, `got.cpu-direct-address-shift`, `got.cpu-interlock-pinout`. Functions and public routing agree; the literal disagreements remain visible in excerpts and device notes.

Runtime source `runtime.public-api.got_137h` records the retained public API scenarios; these tests do not establish physical contact polarity, fitment, measured ball motion or complete game/drain behavior.

## Retained source records

External locators prefixed `working-root:` resolve under the configured sibling `pinmame-game-defs-working-dir`. Portable factual excerpts carry their own fail-closed repository digests; source-owned PDFs, ROMs, frames and tables remain external.

- `manual.switch` (manual): `e559316b46e768099cd7165540c5cabf0d0f78a9eebd4e30051453ad6637c415`. Complete switch_reference regions: PDF pages/printed folios 14,15,17. Raw grids preserve blanks/null merged cells; reviewed literal rows in full JSON/Markdown. Curator visual review2026-10-10; Python3.13.5/pdfplumber0.11.10, derived-DPI renderer using PyMuPDF1.28.2/Pillow12.3.0; actual render hashes/derivations in render_manifest. Excerpt `evidence/excerpts/stern.game-of-thrones-limited-edition.2015/factory-reference.json.txt`: `adbace170d99b2fae8fd76ec70aa6c6a4b88889a87243f2117b1adefefae134c`. Excerpt `evidence/excerpts/stern.game-of-thrones-limited-edition.2015/unbound-physical.json.txt`: `ad6d6db7a40fb5305485ea6c435e62edf57e07c1e229f9a768548bc6a93458c7`.
- `manual.driver` (manual): `e559316b46e768099cd7165540c5cabf0d0f78a9eebd4e30051453ad6637c415`. Complete driver_reference regions: PDF pages/printed folios 12,14. Raw grids preserve blanks/null merged cells; reviewed literal rows in full JSON/Markdown. Curator visual review2026-10-10; Python3.13.5/pdfplumber0.11.10, derived-DPI renderer using PyMuPDF1.28.2/Pillow12.3.0; actual render hashes/derivations in render_manifest. Excerpt `evidence/excerpts/stern.game-of-thrones-limited-edition.2015/factory-reference.json.txt`: `adbace170d99b2fae8fd76ec70aa6c6a4b88889a87243f2117b1adefefae134c`.
- `manual.light` (manual): `e559316b46e768099cd7165540c5cabf0d0f78a9eebd4e30051453ad6637c415`. Complete light_reference regions: PDF pages/printed folios 18,20,21,22,23. Raw grids preserve blanks/null merged cells; reviewed literal rows in full JSON/Markdown. Curator visual review2026-10-10; Python3.13.5/pdfplumber0.11.10, derived-DPI renderer using PyMuPDF1.28.2/Pillow12.3.0; actual render hashes/derivations in render_manifest. Excerpt `evidence/excerpts/stern.game-of-thrones-limited-edition.2015/factory-reference.json.txt`: `adbace170d99b2fae8fd76ec70aa6c6a4b88889a87243f2117b1adefefae134c`.
- `manual.assembly` (manual): `e559316b46e768099cd7165540c5cabf0d0f78a9eebd4e30051453ad6637c415`. Complete supplemental assembly BOMs and scoped drawings; PDF pages/printed folios 38,41,43,48,51,52,53. Specific section/assembly/item locators are in factory-tables.json assembly_tables. Excerpt `evidence/excerpts/stern.game-of-thrones-limited-edition.2015/factory-reference.json.txt`: `adbace170d99b2fae8fd76ec70aa6c6a4b88889a87243f2117b1adefefae134c`.
- `manual.flipper` (manual): `e559316b46e768099cd7165540c5cabf0d0f78a9eebd4e30051453ad6637c415`. Explicit N/C EOS part180-5149-00 in left/right flipper BOMs; PDF pages/printed folios 41. Specific section/assembly/item locators are in factory-tables.json assembly_tables. Excerpt `evidence/excerpts/stern.game-of-thrones-limited-edition.2015/factory-reference.json.txt`: `adbace170d99b2fae8fd76ec70aa6c6a4b88889a87243f2117b1adefefae134c`.
- `manual.display` (manual): `e559316b46e768099cd7165540c5cabf0d0f78a9eebd4e30051453ad6637c415`. Complete speaker-panel BOM and LE LCD BOM where present; PDF pages/printed folios 38. Specific section/assembly/item locators are in factory-tables.json assembly_tables. Excerpt `evidence/excerpts/stern.game-of-thrones-limited-edition.2015/factory-reference.json.txt`: `adbace170d99b2fae8fd76ec70aa6c6a4b88889a87243f2117b1adefefae134c`.
- `manual.cpu` (manual): `e559316b46e768099cd7165540c5cabf0d0f78a9eebd4e30051453ad6637c415`. Complete13-row own-title DIRECT SWITCH MAPPING (CN25) region, section4.1; PDF pages/printed folios 24. Full13 rows are in factory-tables.json tables.cpu_direct_reference and raw grid_tables. Excerpt `evidence/excerpts/stern.game-of-thrones-limited-edition.2015/factory-reference.json.txt`: `adbace170d99b2fae8fd76ec70aa6c6a4b88889a87243f2117b1adefefae134c`.
- `rom.routing` (rom_static_analysis): `f9e868568d7bc130a61e5f7e35f368f1ee61a34d89f26ca38a1ec97d97315889`. Exact got_137h ROM device/coil/LED/switch tables and public mapping/filter dispositions; spike1-rom-routing-facts v1. Program game SHA-256 240db7bed730b8958c8d1d34e160e296d2306fda22533e5f1461df389e65d410; extractor SHA-256 59e4d5940064443b1ad2c1d6aaf05b7a3a594e71b890ec3d4287989166b40446; spike1boot executable SHA-256 f79c4f05ad9a293294651e674d8697e7637eae46d1a3bb6fa8c9f40233e42e24. Retained map log SHA-256 5699d36187475ac4a94b90a80e7ae5881bb86b116d6dd94582aa5236bcf0322f. The file contains full program/archive/log/source identities. No dynamic scenario claimed. Excerpt `evidence/excerpts/stern.game-of-thrones-limited-edition.2015/rom-routing.json.txt`: `b076977c766ba6b55da1f8b6b818c1914da515a913bac910d03f64bb13d4d794`.
- `pinmame.core` (pinmame_core): `756ecd840f234cf7a62f84ef331ccb8b61f0f1aeffc409bc7b776d6c037211c9`. Input conversion191–225, displays426–443, public mapping/filter511–564, GetMech361–365; title initialization and comments798–804 GOT,850–857 KISS,873–879 WWE
- `pinmame.devices` (pinmame_core): `4435f0bd0576a14fa42bf5a32b85bbc2162f59e5c31e263831219f8811496a91`. load_device_table848–956; wire_bytes981–987; motor/home/limits1036–1101; apply_manual_numbers1632–1726; motor_at1729–1752
- `controller.profile` (human_review): `5d5e20b821aa2a01df271a8ec460f9d66915a255940432d40e540833f9843e63`. pinmame.spike1 complete public address rules and documented transport restrictions; current working-tree profile, proposed integration dependency
- `identity.opdb` (human_review): `be658179b49b2bc02dce55d928c3d6a6afe6307e2b00a0ac7ffc1a745ac2d9f3`. machines record opdb_id=G41d5-M9REd, ipdb_id=6309; retained exact edition identity snapshot Excerpt `evidence/excerpts/stern.game-of-thrones-limited-edition.2015/identity.json.txt`: `359d0071843851d282ad581b0ac6810d8cc90c57fb3910aa19e3d984ddae5b81`.
- `catalog.driver` (pinmame_catalog): `d0fd2e4fb48b00da9f89f3595dde8579fbae258c301676af828a51781a0359c9`. drivers entry id=got_137h; PinmameGetGames catalog metadata; no compatibility inherited from other drivers Excerpt `evidence/excerpts/stern.game-of-thrones-limited-edition.2015/baseline-catalog-record.json.txt`: `d0fd2e4fb48b00da9f89f3595dde8579fbae258c301676af828a51781a0359c9`.
- `runtime.public-api.got_137h` (runtime_scenario): `20acb59699ce13064aecee9b34c9362885148df7161afb91b1dd939b9a12f553`. Fresh-state exact-ROM credited-start/serve, manually injected departure, lower flipper and scoring stimuli; full retained runs/exceptions are disclosed in the excerpt. No completed-game claim. Excerpt `evidence/excerpts/stern.game-of-thrones-limited-edition.2015/runtime-observations.json.txt`: `e06049e05a6d68771baf051bc3472200f4f5f8a182df5a61766c0286982edfa1`.
