# KISS (Limited Edition) (2015)

## Identity

Reviewed partial definition; unresolved authoring dimensions are recorded below. One canonical binding is emitted per public address; complete manufacturer facts remain in the reviewed full JSON/Markdown rather than being inferred from emulator flags or similarly numbered entries.

Identity: machine `stern.kiss-limited-edition.2015`, OPDB `G4qX5-Ml9jb`, IPDB 6267; exact retained ROM driver `kiss15_141h`.

Factory PDF: `KissLEweb.pdf`, SHA-256 `a091af04322e78e966867b18bbe8131887a8bc6f5157c842065f4b21603610b9`, 50 pages. This is the exact50-page KISS LE manual; no Premium manual facts were carried into it.

Reference pages/folios: 10, 12, 13, 15, 16, 18, 19. Supplemental assembly pages/folios: 34, 37, 44, 45, 47. Every claimed full table region was checked with view_image against the retained/derived render; PDF page and printed folio are equal.

Extraction/render workflow: Python3.13.5, pdfplumber0.11.10 grid extraction; repository tools/render_excerpt_image.py using PyMuPDF1.28.2 and Pillow12.3.0. Original reference/assembly render DPI derives from embedded raster/native width or smallest vector type. Render_manifest pins each actual WebP SHA and available derivation sidecar. The own CPU appendix audit renders were supplied by the peer curator and independently viewed; their derivation sidecars were not supplied. Full13-row CPU direct regions are reviewed on PDF/folios20. Review performed2026-10-10; no unobserved acquisition timestamp asserted. Copyrighted Stern/title manuals stay outside Git; only derived factual tables and scoped excerpts are proposed.

## Controller contract

Inputs enumerate128 legal switch slots0–95,101–132 plus8 DIP ordinals1–8. Outputs enumerate58 solenoid slots1–32,45–48,51–72 plus lamps1–176. Unmapped inputs remain explicit unknown placeholders; exact-ROM unmapped outputs are virtual unused. Public address capacity does not prove fitment.

DIP ordinals use LibPinMAME bank0 bits0–7 and mirror into switches101–108 each frame. Direct mirror writes are overwritten. The exact-head plugin’s DIP accessors use shifted bit indices, so the profile omits that transport. CPU service buttons109–112 and interlock116 use exact title routing; no startup constant is declared from emulator rest flags.

Lower flipper actual coil channels retain their factory connections. Public45/46 right and47/48 left are identical binary OR mirrors of the named power/hold channels; they are virtual copies, not extra windings. Lower EOS is synthesized after two VBLANKs and direct writes are overwritten. Physical N/C is independently proved only for part180-5149-00 by own-title flipper BOM item3 and exact switch-reference reconciliation. Other polarity, pulse, initial_active and constant_active declarations are omitted.

RGB labels identify individual public channels where factory text gives color. This draft declares no shared-emitter quantity, co-located address set, or coordinates from labels. Controller class bits are routing/filter facts only. Lamp levels use0–255; binary nonzero state and modulated traversal behavior must remain distinct.

## Display evidence

The complete speaker-panel BOM proves physical LED matrix part520-5052-15. PinMAME separately exposes DMD transport index0 at128×32; these dimensions come from source, not from a guessed LED count. Own manual backbox drawing identifies the speaker panel, so its cabinet/backbox spatial placement is not_applicable to playfield coordinates.

## Recreation mechanisms, topology and causality

### LE Gene head ball lock and trip drop target

LE lock has a ball-lock trough, head-ball-lock actuator545-9811-00, plunger/link511-7673-00 and26-1200 no-diode coil090-5044-ND with compression spring. Lock BOM explicitly lists three receiver assemblies515-0215-01 and three emitter assemblies515-0215-00, associated with Lock1/2/3 sensors in the reference table. The one-bank target has reset coil090-5034-ND, trip coil assembly515-9702-01-ND and drop-target opto PCB520-5252-01. Limit: BOM repeats IDs21/22; duplicates retained. Limit: No ball release pulse, target reset/trip timing or jam-recovery behavior is established. Locators: PDF/folio44 §5.32 assembly500-9961-00; PDF/folio44 §5.31 assembly500-9960-00; PDF/folio13 switch50–52 Lock1/2/3; PDF/folio12 driver26 Lock Release; PDF/folio10–12 drivers4/5 1-Bank Drop Reset/Trip.

Bindings: actuators `solenoid.026`, `solenoid.004`, `solenoid.005`; sensors `switch.050`, `switch.051`, `switch.052`, `switch.037`.

### Paul dance plunger

Assembly uses mini27-950 coil090-5084-01, eject spring, Paul plunger and Paul wire linkage535-1187-00. Limit: Driver row19 type is printed blank; assembly establishes solenoid construction. No measured motion range or pulse timing is supplied. Locators: PDF/folio45 §5.33 assembly511-7672-00; PDF/folio47 §5.41 assembly515-9834-00; PDF/folio12 driver19PaulDance.

Bindings: actuators `solenoid.019`; sensors no supported public sensor binding.

### Spinning disk

Disk assembly has a motor solder assembly511-5190-00, disk/hub weldment515-7714-02 and adhesive pad545-9807-00. Driver29 cites motor041-5029-04 at node10 extension10a CN9 pin4/address10-LP-41; driver30 is pin5/address10-LP-42 with type/part cells blank. Limit: Blank type/part cells in driver30 are not repeated as separately printed motor facts. No speed, home position, angular limits or measured dynamics supplied. Locators: PDF/folio45 §5.35 assembly500-7144-03; PDF/folio12 driver29/30SpinDisc1/2. Exact LE motor outputs are public lamps171/172 at node10 LP41/42. Both channels retained; source comment mentions disc motion on lamp172, but the physical table does not establish a measured direction/control sequence.

Bindings: actuators `lamp.171`, `lamp.172`; sensors no supported public sensor binding.

### Ball movement motor and end sensors

Driver27 cites motor041-5129-00, node10 extension10a CN9 pin2/address10-LP-39; driver28 is pin3/address10-LP-40 with blank type/part cells. Two micro-switches180-5119-02 are named MotorHome53 and MotorAway54 at back-panel addresses11-SW-18/19. Limit: No assembly depiction for this motor was located in this reviewed supplement. The names alone do not establish travel axis, normal position, exact endpoints or which switch stops a particular direction. Limit: No travel distance, run timing, limit logic or jam recovery is established. Locators: PDF/folio12 driver27/28Motor-BallLeft/Right; PDF/folio13 switch53MotorHome /54MotorAway. PinMAME SPIKE1_LIMIT_MOTOR(169,170,53,54,1000) models forward169 away/backward170 home, synthetic home53/away54 and GetMech0 as percentage0 home/100 away. The1000ms travel and source-comment roughly5s timeout are emulator assumptions, not measured factory facts. Internal generated home/away state is copied to the public matrix only at initial mapping; later public readback does not prove internal travel.

Bindings: actuators `lamp.169`, `lamp.170`; sensors `switch.053`, `switch.054`.

### Main/hold diverter and one-way gate

Diverter assembly uses a primary/secondary no-diode coil090-5083-00-ND, rod, stop and compression spring. Driver reference separately prints hold31-4000 and main26-1200 windings for that same part number. One-way gate assembly has wire form gate535-1201-00 and micro-switch180-5010-04. Limit: No hold duty, pulse duration, ball routing sequence or measured gate angle is established. Locators: PDF/folio47 §5.40 assembly500-9959-00; PDF/folio47 §5.42 assembly511-7679-00; PDF/folio12 driver13DiverterHold /25DiverterMain.

Bindings: actuators `solenoid.013`, `solenoid.025`; sensors no supported public sensor binding.

### Trough positions and jam sensor

The exact manual reference rows name Trough1–6 and TroughJam; the driver table names Trough eject. Six position labels are retained individually. No eject pulse, jam recovery, installed-ball startup configuration or ball-transfer timing is declared from labels alone.

Bindings: actuators `solenoid.001`; sensors `switch.016`, `switch.017`, `switch.018`, `switch.019`, `switch.020`, `switch.021`, `switch.022`.

### Lower flippers and synthesized EOS contract

Exact manual flipper BOM item3 proves EOS part180-5149-00 normally closed. Actual coil references are distinct from virtual45–48 binary OR mirrors. PinMAME synthesizes lower EOS after two VBLANKs and overwrites direct EOS writes. Button leaves round-trip with keyboard handling disabled; keyboard handling rewrites leaves. No physical pulse/hold duty, rest angle, startup active state or EOS travel threshold is declared. Literal alternative coil/bat/BOM rows are retained in reviewed excerpts and do not prove variant fitment on their own.

Bindings: actuators `solenoid.015`, `solenoid.020`, `solenoid.016`, `solenoid.021`; sensors `switch.010`, `switch.011`, `switch.065`, `switch.066`.

KISS LE light table ends168. Motor Driver refs27–30 reconcile by node10 LP39–42 to public lamp169–172, not by printed reference169/170; Premium light rows at those numbers are irrelevant. ROM cabinet_0x10 class on these motor rows does not establish cabinet location. Exact manual calls the drive Playfield and sensors Backpanel; these distinct literals are retained without deriving travel axis. CoinEnable physical light160 at1-LP0 is ROM reference0/publicnull and has no exported lamp160 binding.

## Conflicts and unresolved facts

- Own Switch Reference PDF/folio15 C16 prints CN7 input4 GRY-RED (GOT spelling GRY RED), ground1 BLK; own direct CPU mapping PDF/folio20 C16 prints input4 GRY, ground5 GRY-RED. Both regions address0-SW-16/public116, but canonical disputed input wire/ground endpoint is withheld. Public running/closed-door state is an emulator fact and cannot resolve physical pinout, contact construction or normally-closed polarity. Resolve from exact factory harness/revision authority or inspected own machine.
- Exact LE manual PDF/folio15 prints DIP2..8 at0-SW2..8 and ServiceSelect/Plus/Minus/Back at0-SW9..12; exact LE ROM uses DIP2..8 at positions1..7 and service positions8..11. Physical ordinal/function reconciliation is retained with conflict; circuit equality is not asserted.


- Spatial playfield placement is unresolved throughout. Global convention is x0left/x1right, y0rear/y1apron; no coordinates or dimensions were inferred from location prose.
- Mechanism coverage remains partial: measured travel/speed, pulse/hold duty, startup/reset states, ball transfer timing and jam recovery are absent unless explicitly identified above as source-model facts. Assembly absence of a sensor is scoped to the reviewed BOM; it does not prove global absence.
- Blank cells remain literal blanks, structurally merged cells remain null in the full reference grids. Motor continuation type/part blanks are not silently repeated. Latent CAD text and sliced table columns were corrected against visible rendering with individual disclosures.
- Manual row names establish documented circuits; coin/ticket accessories and ROM topper metadata do not establish fitted optional configuration.

## Documented physical rows without a supported public reconciliation

These factual rows stay in the reviewed excerpt. They are not new API bindings, and their omission from a public group does not establish absence of physical hardware.

| Table | Printed ID | Name | Manufacturer circuit | PDF/folio | Reason |
| --- | --- | --- | --- | --- | --- |
| light_reference | 160 | Coin Enable | 1-LP-0 | 19 | No supported exact circuit reconciliation in this draft; see full row facts for all columns. |

## Evidence retention

Whole-table factory transcriptions and exact ROM routing facts are committed under `evidence/excerpts/stern.kiss-limited-edition.2015/` as `factory-reference.json.txt` and `rom-routing.json.txt`. Unbound physical rows, identity facts and runtime observations have separate factual excerpts. Source records below pin the actual excerpt digests and the retained external originals. Source-owned manuals, ROMs and tables remain outside Git.

Retained manifest and log identities govern evidence time. Runtime scenarios are cited separately and do not establish measured physical motion or complete game behavior. The OPDB identity snapshot and exact ROM, source, program and log hashes are retained in sources. A source hash proves bytes, not physical truth or rendering correctness. Independent cross-provider review remains pending before PR submission.

Recorded wiring/printed-number discrepancies ignored for author-readiness under the runbook: `kiss15.cpu-interlock-pinout`, `kiss.cpu-address-shift`. Functions and public routing agree; the literal disagreements remain visible in excerpts and device notes.

Runtime source `runtime.public-api.kiss15_141h` records the retained public API scenarios; these tests do not establish physical contact polarity, fitment, measured ball motion or complete game/drain behavior.

## Retained source records

External locators prefixed `working-root:` resolve under the configured sibling `pinmame-game-defs-working-dir`. Portable factual excerpts carry their own fail-closed repository digests; source-owned PDFs, ROMs, frames and tables remain external.

- `manual.switch` (manual): `a091af04322e78e966867b18bbe8131887a8bc6f5157c842065f4b21603610b9`. Complete switch_reference regions: PDF pages/printed folios 12,13,15. Raw grids preserve blanks/null merged cells; reviewed literal rows in full JSON/Markdown. Curator visual review2026-10-10; Python3.13.5/pdfplumber0.11.10, derived-DPI renderer using PyMuPDF1.28.2/Pillow12.3.0; actual render hashes/derivations in render_manifest. Excerpt `evidence/excerpts/stern.kiss-limited-edition.2015/factory-reference.json.txt`: `0b040a6a8b7ea01952943e21caa25b7500292390a2c385f643b4b99787a8668a`. Excerpt `evidence/excerpts/stern.kiss-limited-edition.2015/unbound-physical.json.txt`: `da81bbc305bd728ab566d7200fb51a2c41a8e3c4a92cdd54c514a86546862c1d`.
- `manual.driver` (manual): `a091af04322e78e966867b18bbe8131887a8bc6f5157c842065f4b21603610b9`. Complete driver_reference regions: PDF pages/printed folios 10,12. Raw grids preserve blanks/null merged cells; reviewed literal rows in full JSON/Markdown. Curator visual review2026-10-10; Python3.13.5/pdfplumber0.11.10, derived-DPI renderer using PyMuPDF1.28.2/Pillow12.3.0; actual render hashes/derivations in render_manifest. Excerpt `evidence/excerpts/stern.kiss-limited-edition.2015/factory-reference.json.txt`: `0b040a6a8b7ea01952943e21caa25b7500292390a2c385f643b4b99787a8668a`.
- `manual.light` (manual): `a091af04322e78e966867b18bbe8131887a8bc6f5157c842065f4b21603610b9`. Complete light_reference regions: PDF pages/printed folios 15,16,18,19. Raw grids preserve blanks/null merged cells; reviewed literal rows in full JSON/Markdown. Curator visual review2026-10-10; Python3.13.5/pdfplumber0.11.10, derived-DPI renderer using PyMuPDF1.28.2/Pillow12.3.0; actual render hashes/derivations in render_manifest. Excerpt `evidence/excerpts/stern.kiss-limited-edition.2015/factory-reference.json.txt`: `0b040a6a8b7ea01952943e21caa25b7500292390a2c385f643b4b99787a8668a`.
- `manual.assembly` (manual): `a091af04322e78e966867b18bbe8131887a8bc6f5157c842065f4b21603610b9`. Complete supplemental assembly BOMs and scoped drawings; PDF pages/printed folios 34,37,44,45,47. Specific section/assembly/item locators are in factory-tables.json assembly_tables. Excerpt `evidence/excerpts/stern.kiss-limited-edition.2015/factory-reference.json.txt`: `0b040a6a8b7ea01952943e21caa25b7500292390a2c385f643b4b99787a8668a`.
- `manual.flipper` (manual): `a091af04322e78e966867b18bbe8131887a8bc6f5157c842065f4b21603610b9`. Explicit N/C EOS part180-5149-00 in left/right flipper BOMs; PDF pages/printed folios 37. Specific section/assembly/item locators are in factory-tables.json assembly_tables. Excerpt `evidence/excerpts/stern.kiss-limited-edition.2015/factory-reference.json.txt`: `0b040a6a8b7ea01952943e21caa25b7500292390a2c385f643b4b99787a8668a`.
- `manual.display` (manual): `a091af04322e78e966867b18bbe8131887a8bc6f5157c842065f4b21603610b9`. Complete speaker-panel BOM and LE LCD BOM where present; PDF pages/printed folios 34. Specific section/assembly/item locators are in factory-tables.json assembly_tables. Excerpt `evidence/excerpts/stern.kiss-limited-edition.2015/factory-reference.json.txt`: `0b040a6a8b7ea01952943e21caa25b7500292390a2c385f643b4b99787a8668a`.
- `manual.cpu` (manual): `a091af04322e78e966867b18bbe8131887a8bc6f5157c842065f4b21603610b9`. Complete13-row own-title DIRECT SWITCH MAPPING (CN25) region, section4.1; PDF pages/printed folios 20. Full13 rows are in factory-tables.json tables.cpu_direct_reference and raw grid_tables. Excerpt `evidence/excerpts/stern.kiss-limited-edition.2015/factory-reference.json.txt`: `0b040a6a8b7ea01952943e21caa25b7500292390a2c385f643b4b99787a8668a`.
- `rom.routing` (rom_static_analysis): `3e0bc27ef1cf3171f7d4dda84fd0f1e7ab5bce6423042bf61a239c3af7a547eb`. Exact kiss15_141h ROM device/coil/LED/switch tables and public mapping/filter dispositions; spike1-rom-routing-facts v1. Program game SHA-256 cf5124483f438cfb09ab30babe800bef6b6f83522e0a001ba52dfd46297efef0; extractor SHA-256 59e4d5940064443b1ad2c1d6aaf05b7a3a594e71b890ec3d4287989166b40446; spike1boot executable SHA-256 f79c4f05ad9a293294651e674d8697e7637eae46d1a3bb6fa8c9f40233e42e24. Retained map log SHA-256 233c83a311f2ed9d9b5f382cfd55ed5ddf952637ad6f7cf208a4416aa0a716ce. The file contains full program/archive/log/source identities. No dynamic scenario claimed. Excerpt `evidence/excerpts/stern.kiss-limited-edition.2015/rom-routing.json.txt`: `cd58b4e78d2ce168c2b2da47bbd8213a0f6b52bd08db3e2326fb204998d7da0a`.
- `pinmame.core` (pinmame_core): `756ecd840f234cf7a62f84ef331ccb8b61f0f1aeffc409bc7b776d6c037211c9`. Input conversion191–225, displays426–443, public mapping/filter511–564, GetMech361–365; title initialization and comments798–804 GOT,850–857 KISS,873–879 WWE
- `pinmame.devices` (pinmame_core): `4435f0bd0576a14fa42bf5a32b85bbc2162f59e5c31e263831219f8811496a91`. load_device_table848–956; wire_bytes981–987; motor/home/limits1036–1101; apply_manual_numbers1632–1726; motor_at1729–1752
- `controller.profile` (human_review): `5d5e20b821aa2a01df271a8ec460f9d66915a255940432d40e540833f9843e63`. pinmame.spike1 complete public address rules and documented transport restrictions; current working-tree profile, proposed integration dependency
- `identity.opdb` (human_review): `be658179b49b2bc02dce55d928c3d6a6afe6307e2b00a0ac7ffc1a745ac2d9f3`. machines record opdb_id=G4qX5-Ml9jb, ipdb_id=6267; retained exact edition identity snapshot Excerpt `evidence/excerpts/stern.kiss-limited-edition.2015/identity.json.txt`: `9968b130cfae613ed49b8fe5eabfdff020c697f59696a162d448e220299c0b69`.
- `catalog.driver` (pinmame_catalog): `fa7d45f1f3d6798ff620f64e4155bfd53b3d3cfc8fec9937304afb987f397bfb`. drivers entry id=kiss15_141h; PinmameGetGames catalog metadata; no compatibility inherited from other drivers Excerpt `evidence/excerpts/stern.kiss-limited-edition.2015/baseline-catalog-record.json.txt`: `fa7d45f1f3d6798ff620f64e4155bfd53b3d3cfc8fec9937304afb987f397bfb`.
- `runtime.public-api.kiss15_141h` (runtime_scenario): `49868d5bcd3efac17e4e397c85af07a8167553f4c6e34f2a6c24d2729ee437e9`. Fresh-state exact-ROM credited-start/serve, manually injected departure, lower flipper and scoring stimuli; full retained runs/exceptions are disclosed in the excerpt. No completed-game claim. Excerpt `evidence/excerpts/stern.kiss-limited-edition.2015/runtime-observations.json.txt`: `749fc89e5346634923b434ca563fe503bc5ca3f4f192b9d16e8b76bfee23e4ca`.
