# Ghostbusters (Limited Edition) (2016)

## Identity

This partial definition describes Stern's physical 2016 Ghostbusters Limited Edition and the exact catalog driver `gbust_117h`, “Ghostbusters (Limited Edition 1.17.0)”. The retained OPDB record `GR9Nr-MVKol` is “Ghostbusters (LE)”, manufacture date `2016-01-01`, physicalMachine1, Stern Pinball Inc., IPDB6334 and Limited edition. OPDB supports identity only; secondary database features do not establish wiring, physical component quantities or mechanism construction. The [exact source catalog initializer](https://github.com/vpinball/pinmame/blob/8e0f721e3df7a2b4e8a9d2f4454ac7a9aa1ced53/src/wpc/spike1.c#L717) and the source-matching LE ROM independently retain the firmware/title designation. The year is the physical title's year, not a software revision date.

The title's own manufacturer manual is `Ghostbusters_LE_web.pdf`, “GHOSTBUSTERS LE / PREMIUM MANUAL500-55H6-01”, 54 PDF pages, SHA256 `f793c2a029ff72ccb555f0d15dee90afd6fc82567be353792de92965d4b57025`. It is a combined LE/Premium manual; this record contains only the LE driver. Its explicitly different bottom-arch LE/Premium part entries are retained in the reviewed assembly evidence; no Pro or Premium driver compatibility or geometry is borrowed into this LE record. Complete recreation is blocked by unresolved physical labels/endpoints, missing placement, incomplete mechanism causal behavior/timing and unproved light/emitter quantities.

This note accompanies the primary candidate after a bounded source/manual/runtime audit by GPT-6.1 Sol. The audit checked the retained reviewed transcription and decisive page renders, not every physical component in a real machine. The definition remains `partial`; the audit is not overall author-ready signoff. Portable excerpt import and final source-digest reconciliation remain integration work.

## Recreation

### Public controller routing and startup

Use controller `pinmame.spike1` at revision `8e0f721e3df7a2b4e8a9d2f4454ac7a9aa1ced53`. The candidate enumerates all128 common switch positions `0–95,101–132`, eight DIP configuration ordinals `1–8`, all58 legal common solenoid positions `1–32,45–48,51–72`, and this title's168-channel padded lamp envelope. Holes33–44 and49–50 are not solenoid routes. This ROM contains85 switch rows,22 coil rows and140 LED rows, of which137 rows expose137 distinct public lamps. Highest configured LightReference165 rounds to168. The API's query capacities72/624/8 are not this title's physical inventory.

The [full routing facts](working-root:review-artifacts/spike1-2026-10-10/rom-maps/gbust_117h.json) have SHA256 `417bf954e4d3a1a3b3d76c2492c5f582af46ff7e08f7d61251e6c59110920ee3`. Its complete ELF rows match standalone printed counts and names, with exact original node positions/device indices. Absent vector entries are unused emulator address space, not proof of an unfitted factory hardware position. In this exact driver, custom coil count is0 and `nSolenoids=32`; no factory meter references30/31 are exported by the exact coil vector. Their manual circuit descriptions remain known physical reference data; public30/31 must not be treated as live meter actuators.

Initial logical closure is declared at trough inputs15–20 and DC SENSE116, matching the exact ROM device model. The other trough contact is jam21 and starts open. These initial states are firmware/emulator startup requirements; they do not prove the contact is normally closed or substitute for physical ball inventory. A public1 means logical closed. The subsystem translates that state to its wire level using ROM-table flags. The definition's `inversion_applied_by_emulator` is informational and must not be applied again. SLIMER HIT68 and DIP8's literal “active high” annotations are retained as emulator facts, not physical contact construction.

Lower button references9/10 and EOS11/12 are mapped through the core's flipper-column permutation. Use those exact public references; do not apply a WPC cabinet-switch recipe. Physical lower EOS part180-5149-00 is explicitly N/C in each own flipper BOM on folio38. Public11/12 are nevertheless virtual: the core synthesizes EOS after two VBLANKs of mirror activity and overwrites direct EOS writes. The physical construction, manual wiring and `normally_closed:true` are retained alongside that virtual controller binding. Remaining contact polarities are not filled from firmware flags or opto rest states.

### Mechanism references and physical topology

| Mechanism/group | Exact public sensor references | Exact public actuator references | Recreation implications |
| --- | --- | --- | --- |
| Shooter/auto-launch | 22 SHOOTER LANE | 2 AUTO PLUNGER | Manual spring/rod shooter and powered kicker; runtime launch probe succeeded. |
| Lower left/right flippers | 9/10 buttons;11/12 virtual EOS | 3/4 actual coils;47/48 left mirrors;45/46 right mirrors | Physical EOS N/C proved by own BOM. Virtual mirrors are not additional windings. |
| Sling magnets | 7 LEFT SLINGSHOT;8 RIGHT SLINGSHOT | 5/6 sling magnets | Own bottom BOM has two magnet-bracket assemblies; use magnetic sling behavior. |
| Pop bumpers | 49 LEFT;50 RIGHT;51 BOTTOM | 14 LEFT;15 RIGHT;16 BOTTOM | Reference inputs49–51, not41–43. Skirt/ring timing remains unmeasured. |
| Left single drop | 65 LEFT1-BANK DROP OPTO | 24 UP;25 DOWN | Reset/trip topology; not left-return input3 or standup bank24–26. |
| Right single drop | 66 RIGHT1-BANK DROP OPTO | 26 UP;27 DOWN | Separate reset/trip topology; not right-outlane input6. |
| Left scoop | 34 LEFT SCOOP | 10 LEFT SCOOP | VUK with roller microswitch; not target input25. |
| ROM lock/staging group | 31/32/33 LOCK1/2/3;28/29/30 distinct LOCK STAGE1/2/3 | 11 LOCK POST | Physical assembly association withheld; stage and lock sensors are distinct. |
| Subway route | 60/61/62 SUBWAY LOCK1/2/3;63 SUBWAY EJECT | 20 DIVERTER;21 LOCK;22 EJECT | Names identify the route group; full ball-path sequencing remains unmeasured. |
| Up post | 36 UP POST OPTO | 12 UP POST (SPINNER) | Do not bind this sensor to lock or scoop mechanisms. |
| Controlled upper gate | No identified dedicated gate sensor | 18 ELECTRIC GATE | Gate motion/default state not measured. |
| Slimer | 68 HIT;69 HOME;71/72 ENCODER WHEEL1/2 | No independent legal public motor actuator | ManualEncoderWheel3 ref73 maps by8-SW-5 to ROM/public69; public73 is unused. |
| Ecto Goggles | 59 ECTO GOGGLES | Video display index1 | Own LCD/support/reflector/opto assembly; no invented coil binding. |
| Cabinet shaker | No identified dedicated feedback sensor | 7 SHAKER MOTOR | Distinct cabinet motor route, not Slimer's motor channels. |
| Ticket device | 88 TICKET NOTCH | 32 TICKET DISPENSER | Physical dispenser fitment/enablement unverified. |
| Factory meters | Coin input routes81–85; other controls unexercised | Factory30/31 have no live exact-ROM public route | Keep the physical reference entries separate from virtual unused public30/31. |

The six-position trough assembly500-9820-00 contains transmitter/receiver boards and a27-1500 spring-return feed plunger. The manual's index names TROUGH6..1 and JAM are preserved at15..21. Runtime proved a credited serve output before the harness simulated removal of one ball. Complete ball travel, queue advancement, jam sensing and recovery timing still require a causal scenario or a known-working exact recreation.

The shooter assembly combines the spring/manual rod mechanism with powered auto-launch500-9818-01, coil23-800 and a short-arm rollover switch at22. LOCKDOWN BUTTON76 is explicitly optional in the factory reference and RGB button light rows4/5/6; those bindings retain optional availability. Runtime activation of this input proves the firmware route works, not that every cabinet has the optional button. No auto-launch output is inferred from writing a shooter contact alone.

Separate lower flipper assemblies have coil090-5032-ND (22-1080), plunger/crank, return spring, coil stop and the N/C EOS leaf. The actual public coils3/4 produce an initial high duty followed by30/255 hold duty in the tested ROM. Mirrored power/hold addresses are virtual copies of named lower coil activity, not independently driven windings. Both mirrors of a side can be on when only that side's single named ROM coil is on. Table-owned stroke angles, torque, acceleration and physical timing are not manufactured from the byte levels.

Factory references5/6 and own bottom BOM folio33 identify two magnet-coil bracket assemblies511-7705-00. These are magnetic slings, not conventional kicker arms. Left sling input7/output5 was exercised; right sling8/output6 and resulting ball deflections were not. Pop bumpers have three named input/output pairs49→14,50→15,51→16 and26-1200 driver coils. The separate folio42 assembly drawing/BOM needs the pending retained transcription; no skirt displacement, impact timing or part count is invented.

Both single drop groups use the documented one-bank-with-trip assembly500-9960-H5, reset coil25-1240, separate trip coil515-9702-01-ND, target, compression/reset springs and optoPCB520-5252-01. Sensor65 belongs to the left group24/25 and sensor66 to the right26/27. Reset raises and trip releases the target mechanically; public up/down commands do not directly toggle a sensor without that motion. Start-time DROP DOWN25/27 activity was observed, but no complete target drop/reset sensor cycle was performed. The duplicated printed BOM rows21/22 remain literal transcription anomalies and are not summed into additional quantities.

The left scoop/VUK has27-1500 ejection, a roller microswitch and spring-return plunger; its sensor is34 and actuator10. The separate deep-eject drawing500-9976-00 has24-940 coil and roller switch, consistent in type with the named subway eject22/input63. A type match alone is not a verified physical instance assignment; destinations, empty-state behavior, bounce/recovery and every path still require location/ball-path evidence.

The ROM lock group uses31/32/33 LOCK1/2/3 and11 LOCK POST. Staging inputs28/29/30 are separate. The reference table calls the lock sensors Rollover and gives parts180-5180/79/78. Folio39's separate three-ball lock500-9977-00 explicitly contains three long-range receiver515-0215-01/emitter515-0215-00 pairs and a down-post500-9811-01. The reviewed sources do not yet establish which public lock group owns this opto assembly. The candidate therefore withholds that assembly number from the ROM31–33 group rather than assigning it from the word “lock”. SUBWAY LOCK60/61/62 are explicitly opto references and may be a relevant lead; a location/connector diagram must settle the association, not similar names or shared27-1500 coil type.

The subway group preserves diverter20 (32-1800), lock21 (27-1500), eject22 (24-940), sensors60–63, subway500-9970-00 and HAROLD SUBWAY RAMPLE545-9819-01. The actuator names distinguish three functions; they do not establish that one coil directly actuates an opto or where a ball goes in every default/selected state. Library and subway release/refill, sequencing, jams and power-loss defaults remain unknown. Up post12 and its opto36 are distinct from these groups. Electric gate18 is independently documented; one runtime gate output was observed around shooter departure, but stroke and normal state were not measured or assigned causally to an unrelated button.

Passive/reference mechanisms include the three left standup targets24/25/26 (printed “Leaf, Target”, part515-9783-06-00), left-ramp targets37/38, Ghost45, Captive Ball46, Gozer48 and Terror Dog64. The three left standups are not a three-drop reset bank. Spinner35 is printed Micro, part180-5010-04; top assembly has spinner511-7655-00. Left-ramp input40, disputed ramp input43, outlane/return contacts1–6, pop exit52, left/right orbits54/55 and(P)KE/P(K)E/PK(E) lanes56–58 are retained, with no invented geometry, contact polarity or path timing.

Cabinet shaker7 is the manual's motor041-5029-04 on48V, separate from Slimer. Ticket output32/input88 and factory Coin/Ticket Meter30/31 are device-table/reference leads; generic firmware labels and blank part cells do not prove a dispenser or all meters fitted. Public30/31 are unused virtual outputs here, while32's fitment stays unresolved. Service buttons, country DIP blockS2, interlock, tilt and coin inputs are retained separately. Most were not exercised.

### Slimer and Ecto Goggles

Own Slimer motor assembly500-9982-01, folio49, contains24VDC10RPM motor041-5132-01, timing belt/pulleys, translating cam511-7718-01, cam530-7925-00, shaft, clutch/Belleville springs, encoder wheel550-7377-00, limit wheel535-1361-00 and encoder opto board520-6999-03. The drawing supports combined shaft translation/rotation. Boom500-9983-00, LED/contact PCB520-6987-00 and separate pendulum515-9877-01 are documented on folio48. HIT68 is a physical pendulum/plumb-bob-type sensing lead; no normal-contact polarity is inferred from the ROM's active-high flag.

MotorReference1/2 are node8 LP3/LP4, connectorCN14 return6 RED GRY/return5 RED WHT and power8 YEL, part041-5132-01. Exact ROM class0x08 filters both out of public lamp export. Public lamp1 is COIN ENABLE at node1/position0 and public lamp2 is START BUTTON; binding them to Slimer motor movement would drive the wrong public routes. The firmware motor can be represented in source and `GetMech` even though there is no independent legal public motor actuator binding at this pin.

Feedback is HIT68, HOME69 and EncoderWheel1/2 at71/72. The physical manual labels node8/position5 as reference73 EncoderWheel3, while the ROM labels and remaps the same circuit to public69 SLIMER HOME. The candidate preserves both names/locators; public73 is unused, not a fourth encoder. The driver seeds public switch state during initial mapping, so public readback does not prove later subsystem-generated motor feedback.

Source motor pacing uses1.5s home duration and2ms per requested encoder count, with linear interpolation and stop-at-current-position in `spike1_devices.cpp:56–60,689–726,1012–1026`. These are emulator timing choices, not physical calibration. `GetMech` returns the subsystem motor position before stepper and limit-motor entries, in source order. All retained checkpoint reads0..3 were0, so no targeted Slimer sweep, encoder causality, physical limits/angles, full travel, interruption, stall or return-home behavior is validated. A table still needs a source/ROM-specific motor-command scenario and physical marks/ball-path evidence before completing this mechanism.

Ecto Goggles assembly500-9984-00, screen511-7731-00, reflector511-7732-00, support/shield and LCD1.8INNODE520-6988-00 are own folio50 facts. The opto assembly511-7733-00 has a long-range transmitter515-0215-00 and receiver515-0215-01. Input59 is the ROM's ECTO GOGGLES route. Controller display index1 is160×128 direct video, depth24; source draws it below the DMD at layout top68. This layout offset is emulator display composition, not a normalized physical playfield coordinate. Optical alignment, cabinet geometry, actual view angle and gameplay interaction remain unverified.

The physical backbox DMD uses source/controller index0,128×32, depth4. The CPU node manual's CN23 DMD and CN24 display-power connectors support the cabinet display context. Only two actual displays were announced in the run, even though the callback's total count was3 because the wrapper reserves an extra layout slot. An unannounced slot is not a third physical display.

### RGB channel construction and light export

The manufacturer explicitly names red/green/blue channel rows for ten groups. Each child has a unique ordinary public lamp binding, a literal color alias and a shared group alias. A parent mechanism group references those children. The shared construction is retained without counting three color channels as three physical LED packages.

| Documented RGB group | Public channel/color | Printed part number |
| --- | --- | --- |
| lockdown-button | 4 red; 5 green; 6 blue | 520-5333-00 |
| library-arrow | 26 blue; 27 green; 28 red | 520-6992-00 |
| left-scoop-arrow | 41 blue; 42 green; 43 red | 520-6992-00 |
| library-lock-arrow | 45 red; 46 green; 47 blue | 520-5333-00 |
| left-orbit-arrow | 50 blue; 51 green; 52 red | 520-6993-00 |
| left-ramp-arrow | 62 blue; 63 green; 64 red | 520-6993-00 |
| right-orbit-arrow | 80 blue; 81 green; 82 red | 520-6990-00 |
| right-ramp-arrow | 86 blue; 87 green; 88 red | 520-6991-00 |
| subway-arrow | 96 red; 97 green; 98 blue | 520-5333-00 |
| stay-puft | 107 red; 108 green; 109 blue | 520-5333-00 |

Library arrow26–28 and scoop arrow41–43 share own board8c CN3 LED7/LED1 designators, part520-6992-00. Left orbit50–52 and left ramp62–64 use board9a CN3 LED2/LED1, part520-6993-00; right orbit80–82 uses9b LED6 and right ramp86–88 uses9c LED4. Other RGB groups have explicitly separate color wire/pin rows. Color is taken from the manufacturer's named channel, not numeric order: lockdown, library lock, subway and Stay Puft are R/G/B in address order; the other listed groups are B/G/R.

The schema's `physical.emitter_channel`, `shared_emitter_group` and `co_located_addresses` are atomic with `quantity` and `shared_physical_quantity`. The reviewed reference confirms channel colors/designators and common RGB grouping but does not prove physical emitter quantity. Those atomic fields are therefore withheld. Color/group/reference aliases and parent-child actuator references retain the known construction; primary board-BOM/diagram or direct emitter counting is required to promote it to full shared-emitter metadata. No quantity1 is silently inserted, and no positions are manufactured from “Playfield” labels.

GI and flasher rows use ordinary public lamp channels; `nGI=0`. White/color/part labels and the factory's GI/Flasher classification are retained wherever present. BACKBOX GI's ROM LightReference0 is withheld; the two Slimer class0x08 motor rows are also withheld. Padding166–168 and absent title references are unused virtual slots. Runtime failure to notice a lamp was never used as absence proof. Reference1 CoinEnable and MotorReference1 belong to different namespaces despite their same printed number.

### CPU/DIP/manual anomalies and conflicts

The folio16 reference list has DIP1..8 at0-SW-0..7. Folio21's CPU direct table literally prints DIP1 at0-SW-0, then DIP2..8 at0-SW-2..8, skipping0-SW-1. The exact ROM node0 positions0..7 and driver DIP bank0 bits0..7 settle public101..108. Both printed lists remain aliases/excerpts; do not derive public numbers by adding100 to the folio21 cells. Public101..108 are virtual mirrors overwritten every frame. Separate DIP ordinals1..8 configure the physical S2 block through LibPinMAME bank0. The exact-head plugin DIP accessor is shifted by one bit, so a faithful ordinal plugin transport is not declared at this pin.

Folio21's service table gives Select/Plus/Minus/Back at CPU CN25 pins1/2/3/4, common11 BLK-WHT and addresses0-SW-9..12. The folio16 reference gives pins4/3/2/1, common6 BLK and addresses0-SW-8..11. The visually inspected folio22 schematic distinguishes connectors: service-switch-side common6 passes through cabinetNode1 CN10/CN12 and reaches CPU CN25 common11; Select/Plus/Minus/Back reach CPU CN25 pins4/3/2/1. The physical candidate follows that schematic and retains literal table cells. CPU CN25 pin6 must not be substituted for the service-switch-side common6. This also documents why the CPU and cabinet nodes are both required for service controls. Public Select/Plus/Minus/Back remain109/110/111/112, determined by exact source/ROM.

Three unresolved recreation-facing conflicts are retained in the definition:

- `conflict.cpu-interlock-endpoints`: folio16 C16 prints CN7 input4 GRY RED/common1 BLK, while folio21 prints input4 GRY/common5 GRY RED. Selected interlock endpoint wiring is withheld; public116, its startup closure and logical door-shut meaning remain fixed. A title-correct interlock schematic/assembly or direct wiring inspection must resolve the physical endpoints.
- `conflict.cabinet-slam-sixth-coin`: manual reference87 SIXTH COIN is1-SW-21 and reference89 SLAM TILT is1-SW-22; exact ROM maps node1/position21 to public89 SLAM TILT and position22 to public80 SIXTH COIN. Public references/names follow the exact ROM. Physical circuit-to-control associations/endpoints are withheld instead of silently choosing the same-numbered manual row. Public87 has no ROM route.
- `conflict.ramp43-physical-identity`: manual reference43 at8-SW-12 is LEFT RAMP EXIT; the exact ROM names that node8/position12/public43 RIGHT RAMP. The endpoint agrees, but a title-correct ball-path/location drawing or known-working exact recreation must resolve its physical path name. Both names remain visible.

Other literal anomalies remain notes rather than extra physical devices. Flipper folio38 heading labels left assembly500-6543-12-ND and right500-6543-02-ND, while figure captions interchange02/12; underlying left/right base and crank/BOM rows remain distinct. Single-drop BOM duplicated rows21/22 are not additive quantities. The Slimer manual73/public69 distinction is a resolved public-routing discrepancy with physical naming preserved. Table blank/dash cells never by themselves establish unused physical hardware. The three-ball opto assembly-to-ROM-lock association is an evidence gap, not invented geometry or a falsely resolved sensor topology.

Country codes are physical S2 configuration facts from own folio22; they are not physical N/C contact declarations. The full reviewed26-row table is retained below. USA allOFF is a printed setting, not a claim that every imported cabinet is configured for USA.

| Country | DIP1 | DIP2 | DIP3 | DIP4 | DIP5 | DIP6 | DIP7 | DIP8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| USA | OFF | OFF | OFF | OFF | OFF | OFF | OFF | OFF |
| Austria | ON | OFF | OFF | OFF | OFF | OFF | OFF | OFF |
| Australia | ON | OFF | ON | ON | OFF | OFF | OFF | OFF |
| Belgium | OFF | ON | OFF | OFF | OFF | OFF | OFF | OFF |
| Canada 1 | ON | ON | OFF | OFF | OFF | OFF | OFF | OFF |
| Canada 2 | OFF | ON | OFF | ON | ON | OFF | OFF | OFF |
| Croatia | OFF | ON | ON | OFF | ON | OFF | OFF | OFF |
| Denmark | ON | OFF | OFF | ON | OFF | OFF | OFF | OFF |
| Finland | ON | OFF | ON | OFF | OFF | OFF | OFF | OFF |
| France | OFF | ON | ON | OFF | OFF | OFF | OFF | OFF |
| Germany | ON | ON | ON | OFF | OFF | OFF | OFF | OFF |
| Greece | ON | ON | ON | ON | OFF | OFF | OFF | OFF |
| Italy | OFF | OFF | OFF | ON | OFF | OFF | OFF | OFF |
| Japan | ON | OFF | ON | OFF | ON | OFF | OFF | OFF |
| Middle East | ON | ON | ON | OFF | ON | OFF | OFF | OFF |
| Netherlands | OFF | OFF | ON | OFF | OFF | OFF | OFF | OFF |
| New Zealand | OFF | OFF | OFF | OFF | ON | OFF | OFF | OFF |
| Norway | OFF | ON | OFF | ON | OFF | OFF | OFF | OFF |
| Portugal | ON | OFF | OFF | OFF | OFF | ON | OFF | OFF |
| Russia | ON | OFF | OFF | ON | ON | OFF | OFF | OFF |
| S. Africa | OFF | OFF | ON | OFF | ON | OFF | OFF | OFF |
| Spain | OFF | ON | OFF | OFF | ON | OFF | OFF | OFF |
| Sweden | ON | ON | OFF | ON | OFF | OFF | OFF | OFF |
| Switzerland | OFF | OFF | ON | ON | OFF | OFF | OFF | OFF |
| Taiwan | OFF | OFF | OFF | ON | ON | OFF | OFF | OFF |
| United Kingdom | OFF | ON | ON | ON | OFF | OFF | OFF | OFF |

### Runtime behavior reached and remaining gaps

The [fresh-state exact public API run](working-root:review-artifacts/spike1-2026-10-10/runtime/gbust_117h-api-r2/run.json) started at`2026-10-10T19:17:48Z`, own process173496, with keyboard handling off, mechanics1, physical-all output mask2/2 and approximately10ms polling. The recorder used70s ready,25s boot and180s own-process timeout bounds. The process exited0 after about53.984s without timeout/crash. Source-created startup states were retained.

| Action | Exact stimulus | Observed ROM/API consequence |
| --- | --- | --- |
| Credits | LEFT COIN81, six300ms pulses with1.5s settling | Credited DMD/start response; no exported CoinMeter30 callback claimed. |
| Start/serve | START BUTTON78,120ms pulse;4s settling+2s wait | Repeated TROUGH1 at255; DROP DOWN25/27 pulses also observed. The latter are start-period outputs, not a measured target-motion cycle. |
| Simulated ball transfer | Open TROUGH615;0.4s wait; close SHOOTER LANE22;1s wait | Prior ROM-driven serve already exists; host transfer represents departure of one ball. |
| Launch | Optional LOCKDOWN BUTTON76,200ms closure;1s settling | AUTO PLUNGER2 at240→0. |
| Departure | Open SHOOTER LANE22;1s wait | Gameplay continued; ELECTRIC GATE18 activity observed in this interval, with no measured physical gate motion. |
| Lower left flipper | Button9,500ms hold;0.8s settling | Actual3 at255→30→0; held direct mirror reads47=4 and48=12. |
| Lower right flipper | Button10,500ms hold;0.8s settling | Actual4 at255→30→0; held direct mirror reads45=1 and46=3. |
| Left sling | Input7,100ms pulse;1s settling | LEFT SLING MAGNET5 at255→0 and saved score170 in BALL1. |
| Stop | Public stop call | State2→1→3→0; stop returns with IsRunning0; child exits0. |

Ghostbusters' `nSolenoids=32` means the physical-all changed-solenoid poll does not enumerate45–48. Direct reads during the same run prove the nonzero mirror states; failure to see them in the changed list is not absence. The direct mirror values are bit masks, so binary consumers must test`!=0`, not equality with1. Actual coil byte levels are normalized by255 in core/plugin modulated storage.

The run announced DMD index0 and160×128 video index1. All changed-frame digests were retained:120 DMD and48 video events. Full pixels exist at snapshots, not for every changed frame. Display activity alone would not prove gameplay; the credited serve, launch, actual flipper/sling output and BALL1 score snapshots provide the bounded causal evidence here. Host-written GetSwitch readback was never used as ROM-response or physical-polarity proof.

This remains a one-ball-start/departure exercise, not a completed drain/full game. Drop targets, bumpers, scoop, full lock/subway transfers, gate/default state, Slimer travel, goggles opto interaction, shaker, ticket, tilt/slam, service diagnostics, DIP variants and every physical light/load were not causally exercised. Approximately10ms polling can miss short pulses. Tables still own geometry and tuned physical parameters, and exact source model timing is not a physical service specification. No physical/electrical relationship is declared merely because an input and output share a label or a ball path.

## Sources

All six source IDs carried by the candidate are listed here; every identifier below is literal and remains available for provenance references.

| Source ID | Kind | Exact region/use |
| --- | --- | --- |
| `pinmame.spike1.8e0f721e3df7` | pinmame_core | src/wpc/spike1.c:191–225,275–313,368–390,511–564,668–692,717–733; source public conversion, flipper mirrors, LED filtering and display layouts. Also src/wpc/core.c:1778-1858,2197-2304 for EOS synthesis/direct binary masks (full-file SHA2569ef4b590d31be77ffa21765faeec9df4e3a175c2597f9f7e8937091cea888d6a in full ROM-routing provenance); src/spike1/spike1_devices.cpp:689-726,1010-1028,1729-1752 for GetMech motor position. Audited2026-10-10T19:44:20Z using reviewed physical tables, renders and exact routing/runtime artifacts; source remains pinned. |
| `rom.ghostbusters-le.gbust-117h` | rom_static_analysis | Exact ELF node_board_device_sw_table, coil table and LED table; complete rows/public mapping retained. spike1boot and extractor hashes/versions in excerpt. |
| `manual.ghostbusters-le-premium.2016` | manual | Manual500-55H6-01 PDF/printed11–20; complete node/driver/switch/light/MotorReference tables and location drawings. pdfplumber grid extraction, visually checked against derived-resolution renders. |
| `manual.ghostbusters-le-premium.assemblies.2016` | manual | Own factory CPU21–22 and assembly32–33,36–40,42,48–50; exact N/C EOS and mechanism topology. Font-filtered printed BOMs plus visual corrections; rendered with tools/render_excerpt_image.py. |
| `identity.opdb.ghostbusters-le.2016` | human_review | Selected OPDB record GR9Nr-MVKol; identity cross-check only, not physical I/O authority. |
| `runtime.ghostbusters-le.gbust-117h` | runtime_scenario | Fresh-state credited start/serve, simulated shooter departure, launch76, lowerbuttons9/10, sling7 and clean stop. Recorder/scenario/DLL/program/traces/snapshot hashes in portable excerpt; not a full-game/drain test. |

The manufacturer PDF is [Ghostbusters_LE_web.pdf](https://sternpinball.com/wp-content/uploads/2018/10/Ghostbusters_LE_web.pdf), acquired in the retained provenance at`2026-10-10T18:43:13.500399Z`, full SHA256`f793c2a029ff72ccb555f0d15dee90afd6fc82567be353792de92965d4b57025`. Derived complete factory reference facts are [manual-reviewed-root/stern.ghostbusters-limited-edition.2016.json](working-root:review-artifacts/spike1-2026-10-10/manual-reviewed-root/stern.ghostbusters-limited-edition.2016.json), audit-time SHA256`4e2cfd52c339ff2b87a9a0824801d18046b8fb5c6fb74cdf7f0d43fe6e4255d8`; reviewed CPU/DIP/BOM supplements are [ghostbusters-supplements.json](working-root:review-artifacts/spike1-2026-10-10/manual-reviewed-root/ghostbusters-supplements.json), audit-time SHA256`7a6835ce001976d354ec610f39f4f0180e84581911a9c2768520f6469862f68a`. Raw cells preserve printed blank vs merged/absent cells; font-filtered BOM extraction excludes hidden CAD text. The decisive folio21/22/38/39/40 renders were inspected in this audit. The pending folio42/node-diagram transcription must keep its own derivation/hash and preserve the literal source rows.

The exact `game` is7,090,458 bytes, SHA256`164cea6e6fcbd7786007854c489cb0452eef34a5de7ebf30b341961f2d0c3725`, CRC32`0b6958ba`, SHA1`6f94dbcdaa85e95073534032d74a2dab390b7a4a`. The checked `gbust_117h.zip` is1,204,008,836 bytes, SHA256`b6dc795f91c21e15321abac5df7ba3ca470abba5af1ca7c14372a3d3b629884d`. Archive-entry name/size/CRC metadata and exact game bytes match the source manifest; retained build/extraction logs report completed CRC checks. The [standalone map log](working-root:review-artifacts/spike1-2026-10-10/gbust_117h-map.log) has SHA256`b2a3ace3602d11b0ab2085d7a07ba2d8ecea1168e629ddc2bbcf384ff14b4350`. ROM-routing provenance retains exact executable, extractor, original table-address/index and source-file hashes; no ROM bytes are proposed for repository import.

Runtime [run.json](working-root:review-artifacts/spike1-2026-10-10/runtime/gbust_117h-api-r2/run.json) SHA256 is`a594076e5e676c140547578fa1486e5669984a22f75f35e7665b455b1fd004bf`; complete [run.events.jsonl](working-root:review-artifacts/spike1-2026-10-10/runtime/gbust_117h-api-r2/run.events.jsonl) SHA256 is`5ef9e034d6905c78cbfec4154cb4e98f2de35caef6418b9fadc36bb39d4b0ed0`; [observations.json](working-root:review-artifacts/spike1-2026-10-10/runtime/gbust_117h-api-r2/observations.json) SHA256 is`8c22238f1366ca855d77051c0aa58b5f04ae7c88efca3c9b8e7f2084fd6ca707`. [manifest.json](working-root:review-artifacts/spike1-2026-10-10/runtime/gbust_117h-api-r2/manifest.json) hashes snapshots, logs, fresh-state files and raw traces. The exact scenario SHA256 is`78aa3a8df31975c14dd762f95737a5550fe92cb2db03ba75cbdaace12feabc5f`; DLL SHA256 is`1875e0961759cbd21b566d31a60c7f9e7c59c26c7f1e0d21f97b1b50118db005`. Python3.12.9, harness SHA256`49c5e733bf436a260c915d88e275189950d8ebcc55575f01ab2d153099e1dd44` and recorder SHA256`41400f2bdf14a0bb50e14a2d3368e0058366c9c156bfb64bcc7e4ce60013c529` are retained in probe metadata. The [DMD contact sheet](working-root:review-artifacts/spike1-2026-10-10/runtime/gbust_117h-api-r2/dmd-contact.png) has SHA256`c82278752d8d214c5f078e207d4fcc6f623caaeed8927e6ab88d994367985d76`; raw PGM/PPM snapshots remain the original pixel artifacts.

The [immutable driver source](https://github.com/vpinball/pinmame/blob/8e0f721e3df7a2b4e8a9d2f4454ac7a9aa1ced53/src/wpc/spike1.c) is SHA256`756ecd840f234cf7a62f84ef331ccb8b61f0f1aeffc409bc7b776d6c037211c9`. [core.c](https://github.com/vpinball/pinmame/blob/8e0f721e3df7a2b4e8a9d2f4454ac7a9aa1ced53/src/wpc/core.c) is SHA256`9ef4b590d31be77ffa21765faeec9df4e3a175c2597f9f7e8937091cea888d6a`; its1778–1858 region controls synthesized EOS. [spike1_devices.cpp](https://github.com/vpinball/pinmame/blob/8e0f721e3df7a2b4e8a9d2f4454ac7a9aa1ced53/src/spike1/spike1_devices.cpp) at689–726,1012–1026 and1729–1752 controls modeled motor motion/order; its full hash is in the routing facts. Source is BSD-3-Clause with PinMAME-contributor attribution. Public routing source is emulator authority, not proof of fitted physical hardware.

The [OPDB snapshot](working-root:review-artifacts/spike1-2026-10-10/identity/latest-opdb.json), acquired at`2026-10-10T19:02:39.614808Z`, has SHA256`be658179b49b2bc02dce55d928c3d6a6afe6307e2b00a0ac7ffc1a745ac2d9f3`; exact selected record`GR9Nr-MVKol` is identity authority only. Manufacturer/ROM/OPDB rights remain with their respective rightsholders. The repository's license does not grant redistribution rights to the manual, ROMs or linked photographs.

This candidate's six portable excerpt paths and placeholder digests are integration targets, not completed imports. They must be replaced with retained full routing/runtime/identity/manual excerpts and actual byte digests before repository validation. The knowledge path on import is`knowledge/stern/ghostbusters-limited-edition-2016.md`. The physical conflicts and partial status must not disappear during that translation.


Recorded wiring/printed-number discrepancies ignored for author-readiness under the runbook: `conflict.cpu-interlock-endpoints`. Functions and public routing agree; the literal disagreements remain visible in excerpts and device notes.

## Retained source records

External locators prefixed `working-root:` resolve under the configured sibling `pinmame-game-defs-working-dir`. Portable factual excerpts carry their own fail-closed repository digests; source-owned PDFs, ROMs, frames and tables remain external.

- `pinmame.spike1.8e0f721e3df7` (pinmame_core): `756ecd840f234cf7a62f84ef331ccb8b61f0f1aeffc409bc7b776d6c037211c9`. src/wpc/spike1.c:191–225,275–313,368–390,511–564,668–692,717–733; source public conversion, flipper mirrors, LED filtering and display layouts. Also src/wpc/core.c:1778-1858,2197-2304 for EOS synthesis/direct binary masks (full-file SHA2569ef4b590d31be77ffa21765faeec9df4e3a175c2597f9f7e8937091cea888d6a in full ROM-routing provenance); src/spike1/spike1_devices.cpp:689-726,1010-1028,1729-1752 for GetMech motor position. Audited2026-10-10T19:44:20Z using reviewed physical tables, renders and exact routing/runtime artifacts; source remains pinned.
- `rom.ghostbusters-le.gbust-117h` (rom_static_analysis): `164cea6e6fcbd7786007854c489cb0452eef34a5de7ebf30b341961f2d0c3725`. Exact ELF node_board_device_sw_table, coil table and LED table; complete rows/public mapping retained. spike1boot and extractor hashes/versions in excerpt. Excerpt `evidence/excerpts/stern.ghostbusters-limited-edition.2016/rom-routing.json.txt`: `7d49c868f68c91318117b9a0af739d25063d5fd45a5ef05d08b0b04c8b8b8f98`.
- `manual.ghostbusters-le-premium.2016` (manual): `f793c2a029ff72ccb555f0d15dee90afd6fc82567be353792de92965d4b57025`. Manual500-55H6-01 PDF/printed11–20; complete node/driver/switch/light/MotorReference tables and location drawings. pdfplumber grid extraction, visually checked against derived-resolution renders. Excerpt `evidence/excerpts/stern.ghostbusters-limited-edition.2016/factory-reference.json.txt`: `d394e5f091c1fe920ee728128d8c73cf035de58ccb707dec404012b4d2255692`.
- `manual.ghostbusters-le-premium.assemblies.2016` (manual): `f793c2a029ff72ccb555f0d15dee90afd6fc82567be353792de92965d4b57025`. Own factory CPU21–22 and assembly32–33,36–40,42,48–50; exact N/C EOS and mechanism topology. Font-filtered printed BOMs plus visual corrections; rendered with tools/render_excerpt_image.py. Excerpt `evidence/excerpts/stern.ghostbusters-limited-edition.2016/factory-assemblies.json.txt`: `3f60c4cc35f1733454b06586c19cada10dc39adcd5a4f6fa56c40a01d5be62ab`.
- `identity.opdb.ghostbusters-le.2016` (human_review): `be658179b49b2bc02dce55d928c3d6a6afe6307e2b00a0ac7ffc1a745ac2d9f3`. Selected OPDB record GR9Nr-MVKol; identity cross-check only, not physical I/O authority. Excerpt `evidence/excerpts/stern.ghostbusters-limited-edition.2016/identity.json.txt`: `30500e43436c7169886bdf8996c39484b003e5a42b0258762002f82f62f20bbc`.
- `runtime.ghostbusters-le.gbust-117h` (runtime_scenario): `a594076e5e676c140547578fa1486e5669984a22f75f35e7665b455b1fd004bf`. Fresh-state credited start/serve, simulated shooter departure, launch76, lowerbuttons9/10, sling7 and clean stop. Recorder/scenario/DLL/program/traces/snapshot hashes in portable excerpt; not a full-game/drain test. Excerpt `evidence/excerpts/stern.ghostbusters-limited-edition.2016/runtime-observations.json.txt`: `ab937846692351b6a36ede07b544184833df90bef856cf1a28d57f955f48f6fe`.
