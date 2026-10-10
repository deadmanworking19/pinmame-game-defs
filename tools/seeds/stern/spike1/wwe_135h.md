# Legends of Wrestlemania (2015)

## Identity

Reviewed partial definition; unresolved authoring dimensions are recorded below. One canonical binding is emitted per public address; complete manufacturer facts remain in the reviewed full JSON/Markdown rather than being inferred from emulator flags or similarly numbered entries.

Identity: machine `stern.wwe-wrestlemania-limited-edition.2015`, OPDB `GR6Or-MKNYR`, IPDB 6216; exact retained ROM driver `wwe_135h`. The physical LE title is Legends of Wrestlemania; PinMAME’s driver description calls it WWE WrestleMania LE.

Factory PDF: `WWE-LE-Manual.pdf`, SHA-256 `74c482af5b0e3e1d9ba18532ce717ee1858a606adfc4a2ca2f2d6f69624cfbfb`, 56 pages.

Reference pages/folios: 9, 11, 13, 14, 15, 17, 18. Supplemental assembly pages/folios: 31, 35, 41, 43, 49, 50, 53. Every claimed full table region was checked with view_image against the retained/derived render; PDF page and printed folio are equal.

Extraction/render workflow: Python3.13.5, pdfplumber0.11.10 grid extraction; repository tools/render_excerpt_image.py using PyMuPDF1.28.2 and Pillow12.3.0. Original reference/assembly render DPI derives from embedded raster/native width or smallest vector type. Render_manifest pins each actual WebP SHA and available derivation sidecar. The own CPU appendix audit renders were supplied by the peer curator and independently viewed; their derivation sidecars were not supplied. Full13-row CPU direct regions are reviewed on PDF/folios19. Review performed2026-10-10; no unobserved acquisition timestamp asserted. Copyrighted Stern/title manuals stay outside Git; only derived factual tables and scoped excerpts are proposed.

## Controller contract

Inputs enumerate128 legal switch slots0–95,101–132 plus8 DIP ordinals1–8. Outputs enumerate58 solenoid slots1–32,45–48,51–72 plus lamps1–104. Unmapped inputs remain explicit unknown placeholders; exact-ROM unmapped outputs are virtual unused. Public address capacity does not prove fitment.

DIP ordinals use LibPinMAME bank0 bits0–7 and mirror into switches101–108 each frame. Direct mirror writes are overwritten. The exact-head plugin’s DIP accessors use shifted bit indices, so the profile omits that transport. CPU service buttons109–112 and interlock116 use exact title routing; no startup constant is declared from emulator rest flags.

Lower flipper actual coil channels retain their factory connections. Public45/46 right and47/48 left are identical binary OR mirrors of the named power/hold channels; they are virtual copies, not extra windings. Lower EOS is synthesized after two VBLANKs and direct writes are overwritten. Physical N/C is independently proved only for part180-5149-00 by own-title flipper BOM item3 and exact switch-reference reconciliation. Other polarity, pulse, initial_active and constant_active declarations are omitted.

RGB labels identify individual public channels where factory text gives color. This draft declares no shared-emitter quantity, co-located address set, or coordinates from labels. Controller class bits are routing/filter facts only. Lamp levels use0–255; binary nonzero state and modulated traversal behavior must remain distinct.

## Display evidence

The complete speaker-panel BOM proves physical LED matrix part520-5052-15. PinMAME separately exposes DMD transport index0 at128×32; these dimensions come from source, not from a guessed LED count. Speaker-panel physical location is not assigned from controller comments; exact manual placement remains to be retained.

Own manual PDF/folio53 §5.40 LCD assembly500-9949-00 proves one5.7 inch LCD/LVDS receiver511-7649-00 and60-inch LVDS cable037-1111-00. PinMAME calls it the LE playfield LCD and exposes CORE_VIDEO index1 at320×240 in spike1_dmd_lcd. The manual establishes construction; the controller comment is retained as a source-model description without being substituted for physical placement evidence. This is a separate physical display and transport from the speaker-panel DMD; the source layout’s UI offset is not a physical coordinate. LCD physical placement/coordinates remain unresolved.

## Recreation mechanisms, topology and causality

### LE wrestling ring and spinning disc

Mini-playfield BOM includes two single-switch slings, two banks of three standup targets, ring exit switch assembly511-7617-00 and VUK500-6868-00 with angled left-hand plunger tip. A spinning disk500-7144-02 sits in the ring, driven by one DC gearhead motor041-5126-00, nominal24 VDC400 RPM; friction pad820-8371-00 is4 inch diameter. Driver refs26 Motor1 and27 Motor2 both cite part041-5126-00 at node12 CN16 pins6/7, addresses12-LP-5/6. The ring uses serial switch/LED board520-6951-00. Dual motor driver CN1 has PHA1 ORG-GRY and PHA0 ORG-VIO control phases, V+ RED and ground BLK-WHT; CN2 pin5 is +48 VDC IN GRY, pin1 GND BLK; CN3 DRIVEA-1/0 pins4/6 are BRN/GRY. This is distinct from the 24 VDC nominal motor specification and the 5V reference-table control columns. Limit: Driver-table 5V, motor BOM nominal24 VDC and dual-driver +48 VDC IN are separate printed circuit/specification facts. The pinout establishes phase/control and supply separation; no unsupported identification of 5V as motor terminal voltage is made. Limit: Heading and figure assembly part numbers differ onp49. Limit: No encoder, home switch or jam detector appears in the reviewed disk BOM. This is scoped to this BOM, not proof of universal absence. No measured speed, inertia, angular limits or control timing is established. Locators: PDF/folio49 §5.30 assembly500-9919-01 (figure captions500-9919-00); PDF/folio53 §5.41 assembly500-7144-02; PDF/folio11 Driver Reference motor26/27; PDF/folio17–18 ring switches; PDF/folio31 DUAL MOTOR DRIVER BOARD connector pinout. Motor1/2 share public lamps22/5 with factory lights22/5. These canonical control signals alias loads; they are not independently controlled motor channels. Upper flipper uses second-leaf buttons74/75 and coil22. No disc encoder/home binding or measured dynamics is established.

Bindings: actuators `solenoid.012`, `solenoid.013`, `solenoid.014`, `lamp.005`, `lamp.022`; sensors `switch.025`, `switch.026`, `switch.027`, `switch.028`, `switch.034`, `switch.047`, `switch.054`, `switch.055`, `switch.056`, `switch.058`, `switch.059`, `switch.060`.

### LE ladder and briefcase lane

Ladder assembly incorporates ladder light/switch bracket, four standard rollover switches180-5230-00, four single-LED boards520-5307-00, ladder exit switch assembly511-7609-00 and briefcase assembly510-7520-24. No powered actuator appears in these reviewed ladder BOMs. Limit: No coordinates, ball transit timing, lane order from an unlabeled view or recovery behavior is inferred. Locators: PDF/folio50 §§5.31–5.32 assemblies511-7624-01 /500-9929-01; PDF/folio17 switch46 Ladder exit and50–53 Ladder1–4.

Bindings: actuators no supported public actuator binding; sensors `switch.046`, `switch.050`, `switch.051`, `switch.052`, `switch.053`.

### LE LCD assembly

The LE-specific assembly contains one5.7 inch LCD and LVDS receiver511-7649-00, LCD mounting bracket535-1144-00 and60 inch LVDS cable037-1111-00. Limit: The assembly proves physical LCD construction; display transport and surface dimensions still need controller/display evidence. Locators: PDF/folio53 §5.40 assembly500-9949-00.

Bindings: actuators no supported public actuator binding; sensors no supported public sensor binding.

### Upper flipper and second-leaf controls

Own Driver Reference11 lists Upper Flipper22. Switch Reference18 lists Upper Left/Right Flipper Button74/75 and Upper Left Flipper EOS78; these documented controls are recorded separately from ring disc/VUK motion. Exact upper-left EOS part180-5149-00 is physically N/C in the complete lower/upper-left flipper BOM41. No upper-right EOS, extra winding or independent upper-right actuator is invented. Complete button-to-coil game causality, pulse/hold control, rest angle, stroke threshold, startup/reset and jam handling remain unresolved.

Bindings: actuators `solenoid.022`; sensors `switch.074`, `switch.075`, `switch.078`.

### Trough positions and jam sensor

The exact manual reference rows name Trough1–6 and TroughJam; the driver table names Trough eject. Six position labels are retained individually. No eject pulse, jam recovery, installed-ball startup configuration or ball-transfer timing is declared from labels alone.

Bindings: actuators `solenoid.001`; sensors `switch.016`, `switch.017`, `switch.018`, `switch.019`, `switch.020`, `switch.021`, `switch.022`.

### Lower flippers and synthesized EOS contract

Exact manual flipper BOM item3 proves EOS part180-5149-00 normally closed. Actual coil references are distinct from virtual45–48 binary OR mirrors. PinMAME synthesizes lower EOS after two VBLANKs and overwrites direct EOS writes. Button leaves round-trip with keyboard handling disabled; keyboard handling rewrites leaves. No physical pulse/hold duty, rest angle, startup active state or EOS travel threshold is declared. Literal alternative coil/bat/BOM rows are retained in reviewed excerpts and do not prove variant fitment on their own.

Bindings: actuators `solenoid.015`, `solenoid.020`, `solenoid.016`, `solenoid.021`; sensors `switch.010`, `switch.011`, `switch.065`, `switch.066`.

The physical ring exit/VUK and slings/standups are established by the LE mini-playfield BOM. Driver motor26/27 control rows, dual-driver p31 +48VDC input/phase outputs, and nominal24VDC400RPM motor BOM are retained as separate circuit/specification facts. 400RPM is a nominal part specification, not measured game speed; printed5V is not assigned as motor-terminal voltage. No encoder/home switch binding, default orientation or jam recovery is known.

## Conflicts and unresolved facts

- Own Switch Reference18 and direct CPU mapping19 omit0-SW-1 and shift DIP2..8/service Select..Back to0-SW2..8/9..12; exact ROM uses1..7/8..11. Physical ordinal/function reconciliation preserves literal aliases and correct public101–112 meanings; circuit equality is unresolved. The two own manual regions agree on service CN25 pins4/3/2/1, ground6 BLK.
- Own Switch Reference PDF/folio18 C16 prints CN7 input4 GRY-RED (GOT spelling GRY RED), ground1 BLK; own direct CPU mapping PDF/folio19 C16 prints input4 GRY, ground5 GRY-RED. Both regions address0-SW-16/public116, but canonical disputed input wire/ground endpoint is withheld. Public running/closed-door state is an emulator fact and cannot resolve physical pinout, contact construction or normally-closed polarity. Resolve from exact factory harness/revision authority or inspected own machine.
- Exact ROM lamp5 and22 each publish two distinct mapped rows: motor2/200Thousand at5 and motor1/SpecialWhenRedRight at22. Binary OR and modulated last-traversal overwrite differ; one canonical binding per public address retains all load aliases without independent physical output state. `wwe.led-aliases` is ignored as a formal physical conflict: the factory motor and feature-light circuits are distinct, while the pinned adapter demonstrably collapses their public references. A hardware inspection cannot recover independent states from that adapter. Output and mechanism behavior remain incomplete, and the separate extension-address crosswalk remains candidate.
- Manual extension8a LED printed positions16..47 consistently match ROMnode8 positions8..39 by channel name/reference. Candidate translation subtracts8; source proving factory-to-ROM address translation is still required. This does not apply to extension switches or other titles.
- Manual PDF/folio49 §5.30 heading says500-9919-01 while Figure5.30.1–3 captions say500-9919-00. Both exact source literals retained; no replacement part assumption.

- Public lamp5 aliases MOTOR 2 node12-LP-6, 200 THOUSAND node8-LP-37. Binary OR versus modulated traversal overwrite means driving both physical loads from a single scalar is not independently faithful. Both full wiring rows remain in physical.notes and reviewed excerpt.
- Public lamp22 aliases MOTOR 1 node12-LP-5, SPECIAL WHEN RED(RIGHT) node8-LP-30. Binary OR versus modulated traversal overwrite means driving both physical loads from a single scalar is not independently faithful. Both full wiring rows remain in physical.notes and reviewed excerpt.

- Spatial playfield placement is unresolved throughout. Global convention is x0left/x1right, y0rear/y1apron; no coordinates or dimensions were inferred from location prose.
- Mechanism coverage remains partial: measured travel/speed, pulse/hold duty, startup/reset states, ball transfer timing and jam recovery are absent unless explicitly identified above as source-model facts. Assembly absence of a sensor is scoped to the reviewed BOM; it does not prove global absence.
- Blank cells remain literal blanks, structurally merged cells remain null in the full reference grids. Motor continuation type/part blanks are not silently repeated. Latent CAD text and sliced table columns were corrected against visible rendering with individual disclosures.
- Manual row names establish documented circuits; coin/ticket accessories and ROM topper metadata do not establish fitted optional configuration.

## Documented physical rows without a supported public reconciliation

These factual rows stay in the reviewed excerpt. They are not new API bindings, and their omission from a public group does not establish absence of physical hardware.

| Table | Printed ID | Name | Manufacturer circuit | PDF/folio | Reason |
| --- | --- | --- | --- | --- | --- |
| driver_reference | 30 | Meter 1 | 1-DR-2 | 11 | No supported exact circuit reconciliation in this draft; see full row facts for all columns. |
| driver_reference | 31 | Meter 2 | 1-DR-3 | 11 | No supported exact circuit reconciliation in this draft; see full row facts for all columns. |

## Evidence import contract

Copy external reviewed `stern.wwe-wrestlemania-limited-edition.2015.json` and `stern.wwe-wrestlemania-limited-edition.2015.md` byte-for-byte to `evidence/excerpts/stern.wwe-wrestlemania-limited-edition.2015/factory-tables.json` and `factory-tables.md`; copy exact `rom-maps/wwe_135h.json` to `evidence/excerpts/stern.wwe-wrestlemania-limited-edition.2015/rom-routing.json`. Draft sources already pin their actual external bytes. These are proposed portable destinations, currently absent in the read-only repository; root must verify imported hashes and run repository validation before installation. Source/manual URIs retain actual external identities for traceability.

No acquisition time was invented; retained manifest/log identities govern evidence time. No runtime motion scenario is claimed by this draft. OPDB identity snapshot and exact ROM/source program/log hashes are retained in sources. A source hash proves bytes, not physical truth or rendering correctness. Root independent manual and draft review remains required.

Recorded wiring/printed-number discrepancies ignored for author-readiness under the runbook: `wwe.cpu-address-shift`, `wwe.cpu-interlock-pinout`. Functions and public routing agree; the literal disagreements remain visible in excerpts and device notes.

Runtime source `runtime.public-api.wwe_135h` records the retained public API scenarios; these tests do not establish physical contact polarity, fitment, measured ball motion or complete game/drain behavior.

## Retained source records

External locators prefixed `working-root:` resolve under the configured sibling `pinmame-game-defs-working-dir`. Portable factual excerpts carry their own fail-closed repository digests; source-owned PDFs, ROMs, frames and tables remain external.

- `manual.switch` (manual): `74c482af5b0e3e1d9ba18532ce717ee1858a606adfc4a2ca2f2d6f69624cfbfb`. Complete switch_reference regions: PDF pages/printed folios 15,17,18. Raw grids preserve blanks/null merged cells; reviewed literal rows in full JSON/Markdown. Curator visual review2026-10-10; Python3.13.5/pdfplumber0.11.10, derived-DPI renderer using PyMuPDF1.28.2/Pillow12.3.0; actual render hashes/derivations in render_manifest. Excerpt `evidence/excerpts/stern.wwe-wrestlemania-limited-edition.2015/factory-reference.json.txt`: `79df17026f5182de29a9e2db31cff740cac7a6d9da2199ce0e60a13f89c6f038`. Excerpt `evidence/excerpts/stern.wwe-wrestlemania-limited-edition.2015/unbound-physical.json.txt`: `5490aeb765bd337cdc38147797999a425405b04a152dd982981d05b3b9462b57`.
- `manual.driver` (manual): `74c482af5b0e3e1d9ba18532ce717ee1858a606adfc4a2ca2f2d6f69624cfbfb`. Complete driver_reference regions: PDF pages/printed folios 11. Raw grids preserve blanks/null merged cells; reviewed literal rows in full JSON/Markdown. Curator visual review2026-10-10; Python3.13.5/pdfplumber0.11.10, derived-DPI renderer using PyMuPDF1.28.2/Pillow12.3.0; actual render hashes/derivations in render_manifest. Excerpt `evidence/excerpts/stern.wwe-wrestlemania-limited-edition.2015/factory-reference.json.txt`: `79df17026f5182de29a9e2db31cff740cac7a6d9da2199ce0e60a13f89c6f038`.
- `manual.light` (manual): `74c482af5b0e3e1d9ba18532ce717ee1858a606adfc4a2ca2f2d6f69624cfbfb`. Complete light_reference regions: PDF pages/printed folios 11,13,14,15. Raw grids preserve blanks/null merged cells; reviewed literal rows in full JSON/Markdown. Curator visual review2026-10-10; Python3.13.5/pdfplumber0.11.10, derived-DPI renderer using PyMuPDF1.28.2/Pillow12.3.0; actual render hashes/derivations in render_manifest. Excerpt `evidence/excerpts/stern.wwe-wrestlemania-limited-edition.2015/factory-reference.json.txt`: `79df17026f5182de29a9e2db31cff740cac7a6d9da2199ce0e60a13f89c6f038`.
- `manual.assembly` (manual): `74c482af5b0e3e1d9ba18532ce717ee1858a606adfc4a2ca2f2d6f69624cfbfb`. Complete supplemental assembly BOMs and scoped drawings; PDF pages/printed folios 31,35,41,43,49,50,53. Specific section/assembly/item locators are in factory-tables.json assembly_tables. Excerpt `evidence/excerpts/stern.wwe-wrestlemania-limited-edition.2015/factory-reference.json.txt`: `79df17026f5182de29a9e2db31cff740cac7a6d9da2199ce0e60a13f89c6f038`.
- `manual.flipper` (manual): `74c482af5b0e3e1d9ba18532ce717ee1858a606adfc4a2ca2f2d6f69624cfbfb`. Explicit N/C EOS part180-5149-00 in left/right flipper BOMs; PDF pages/printed folios 41. Specific section/assembly/item locators are in factory-tables.json assembly_tables. Excerpt `evidence/excerpts/stern.wwe-wrestlemania-limited-edition.2015/factory-reference.json.txt`: `79df17026f5182de29a9e2db31cff740cac7a6d9da2199ce0e60a13f89c6f038`.
- `manual.display` (manual): `74c482af5b0e3e1d9ba18532ce717ee1858a606adfc4a2ca2f2d6f69624cfbfb`. Complete speaker-panel BOM and LE LCD BOM where present; PDF pages/printed folios 35,53. Specific section/assembly/item locators are in factory-tables.json assembly_tables. Excerpt `evidence/excerpts/stern.wwe-wrestlemania-limited-edition.2015/factory-reference.json.txt`: `79df17026f5182de29a9e2db31cff740cac7a6d9da2199ce0e60a13f89c6f038`.
- `manual.cpu` (manual): `74c482af5b0e3e1d9ba18532ce717ee1858a606adfc4a2ca2f2d6f69624cfbfb`. Complete13-row own-title DIRECT SWITCH MAPPING (CN25) region, section4.1; PDF pages/printed folios 19. Full13 rows are in factory-tables.json tables.cpu_direct_reference and raw grid_tables. Excerpt `evidence/excerpts/stern.wwe-wrestlemania-limited-edition.2015/factory-reference.json.txt`: `79df17026f5182de29a9e2db31cff740cac7a6d9da2199ce0e60a13f89c6f038`.
- `rom.routing` (rom_static_analysis): `1d3766394a4dbbc71cd447513246e4649e6814668b8faf69cb56cf6cde6aa9c1`. Exact wwe_135h ROM device/coil/LED/switch tables and public mapping/filter dispositions; spike1-rom-routing-facts v1. Program game SHA-256 1d3610b8dc90fd8c5fc7d5700dbe2d5cd03673ab3c1192273cd6b5dd547cbcf3; extractor SHA-256 59e4d5940064443b1ad2c1d6aaf05b7a3a594e71b890ec3d4287989166b40446; spike1boot executable SHA-256 f79c4f05ad9a293294651e674d8697e7637eae46d1a3bb6fa8c9f40233e42e24. Retained map log SHA-256 18236fc6231f6f1619f59188c38c8216b29257eac1cb0dd32881d893813f6301. The file contains full program/archive/log/source identities. No dynamic scenario claimed. Excerpt `evidence/excerpts/stern.wwe-wrestlemania-limited-edition.2015/rom-routing.json.txt`: `d934fa456ba73e04dd96736474e65967f35e42fde783063e4493e899ec0bc375`.
- `pinmame.core` (pinmame_core): `756ecd840f234cf7a62f84ef331ccb8b61f0f1aeffc409bc7b776d6c037211c9`. Input conversion191–225, displays426–443, public mapping/filter511–564, GetMech361–365; title initialization and comments798–804 GOT,850–857 KISS,873–879 WWE
- `pinmame.devices` (pinmame_core): `4435f0bd0576a14fa42bf5a32b85bbc2162f59e5c31e263831219f8811496a91`. load_device_table848–956; wire_bytes981–987; motor/home/limits1036–1101; apply_manual_numbers1632–1726; motor_at1729–1752
- `controller.profile` (human_review): `5d5e20b821aa2a01df271a8ec460f9d66915a255940432d40e540833f9843e63`. pinmame.spike1 complete public address rules and documented transport restrictions; current working-tree profile, proposed integration dependency
- `identity.opdb` (human_review): `be658179b49b2bc02dce55d928c3d6a6afe6307e2b00a0ac7ffc1a745ac2d9f3`. machines record opdb_id=GR6Or-MKNYR, ipdb_id=6216; retained exact edition identity snapshot Excerpt `evidence/excerpts/stern.wwe-wrestlemania-limited-edition.2015/identity.json.txt`: `9579d744db06d1ef8a6f3a5aea3081c87fdd8c446becb280f34b4cd31f7a5415`.
- `catalog.driver` (pinmame_catalog): `4a5a79f19498b2ef9fd837a07a5e22fbc5cbe3ad58be0fcd6aa243a580564b27`. drivers entry id=wwe_135h; PinmameGetGames catalog metadata; no compatibility inherited from other drivers Excerpt `evidence/excerpts/stern.wwe-wrestlemania-limited-edition.2015/baseline-catalog-record.json.txt`: `4a5a79f19498b2ef9fd837a07a5e22fbc5cbe3ad58be0fcd6aa243a580564b27`.
- `runtime.public-api.wwe_135h` (runtime_scenario): `3a76e163310759b5377308b0e8e55ea21dcce3ebb2311e9906ca24391a7c97ed`. Fresh-state exact-ROM credited-start/serve, manually injected departure, lower flipper and scoring stimuli; full retained runs/exceptions are disclosed in the excerpt. No completed-game claim. Excerpt `evidence/excerpts/stern.wwe-wrestlemania-limited-edition.2015/runtime-observations.json.txt`: `0ff3ab3b3d9e19ab033c5bbf76416dc65a1b01460746651aa877e6575e3f8303`.
