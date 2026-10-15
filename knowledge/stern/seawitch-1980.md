# Seawitch (Stern, 1980)

Coverage: **partial - full address dispositions and recreation notes, with four unknown lamp fitments and incomplete physical placement.** No author-ready promotion is claimed. The canonical missing dimensions are output semantics and spatial placement; the spatial report names the affected records and the evidence needed.

## Physical identity and firmware

Seawitch is Stern model 123, manufactured in May 1980, IPDB 2089, OPDB GR6kB-MDz81. The retained IPDB identity agrees with the factory manual and parts/topology sheets: four players, four flippers, three thumpers, two slingshots, four stand-ups, two four-target banks, one three-target bank, two star rollovers and one spinner. The physical release year remains 1980.

The pinned PinMAME revision is 97aa922bf8e4b6970126192ec1ac1fb0305a4f62. Production seawitch, free-play seawitfp, and rules revisions seawitcha through seawitchf (rev. 5, 6, 7, 8, 9 and 9.3) each declare the same GEN_STMPU200 hardware, dispst7, FLIP_SW(FLIP_L), no additional lamp columns/custom solenoids, ST300 sound and input_ports_st. They stay firmware variants of this physical record. The community firmware dates 2021-2024 do not create later physical machines. Only the production ROM was exercised; modified-rule behavior and scoring are not claimed to have been measured.

The read-only ROM archive's four members were checked against the pinned production driver's SHA-1s and sizes before boot. Its SHA-256 is bbed2206f4b5bb00362f6dc4aa0d5b00b9635af6c1ade127f498f7a066dad88b. No ROM bytes or NVRAM enter this repository.

## Evidence and authority

The factory operations manual (22 PDF pages) and Seawitch schematics (10 PDF pages) control construction, fitment, wiring and normally-open/closed contacts. The source IDs are manual.seawitch.1980 and manual.seawitch.schematics. Their hashes, direct IPDB resource URLs, acquisition metadata and exact transcribed/cropped regions are pinned in the definition. The two printed lamp lists are different: schematic page 8 contains 52 rows; page 9 contains 57, adding the backbox Game Over, High Score to Date, Match, Tilt and Shoot Again (Insert) rows. They are copies within one document, not independent corroboration.

The retained archive table is Seawitch (Stern 1980)2.0.0.vpx, SHA-256 cb91d8d726d8a451ba6f158e49e459812e8dca888b896e72dca69168d616e434. Its embedded script is a3483e9c4e00c68add7135cd0f3a0dbe216a418d17b9c4f02177da27f1239031. Blank table metadata does not establish an author, release or working-test history. A same-named corpus script explicitly says it was not verified; no filename grants runtime authority. The primary curator reconciled the retained script's actual handlers with the factory sheets and production-ROM traces. Where it has a concrete defect, the supported machine contract is recorded and the defect is stated below.

Luna's extraction inventory and Terra's OCR/transcription research were candidates. The primary curator read every decisive chart/circuit from retained renders and checked the resulting facts. The original PDFs and source table remain external. Full printed factual tables are transcribed in evidence/excerpts/stern.seawitch.1980; drawing crops retain their derivation and hash. The schematic PDFs store tiled scan strips: the crop helper now derives native resolution from the union of coherent tiles, rather than misclassifying them as vector art. Width caps and resulting resolution are disclosed verbatim on each crop.

The retained IPDB page and physical images corroborate title, count, side and topology. They do not settle a connector or socket count. The Gary Donovan Version 7 redraw and Pinside gallery were research leads; no SCR mapping or bulb coordinate was copied from the redraw.

## Inputs, polarity and service

Every matrix position 1-40 is represented. The factory marks 11, 15, 16, 26, 27 and 28 unused (26 literally No Used); they remain unused even though the ROM diagnostic recognizes all forty numbers. Fitted contacts are coins 1-3, rear star 4, spinner 5, credit 6, aggregate tilt 7, aggregate slam 8, thumpers 9/10/14, slings 12/13, stand-ups 17-20, center drops 21-24, runway star 25, upper-right drops 29-32, out-hole 33, outlanes 34/35, return lanes 36/37 and left drops 38-40.

The cabinet sheet routes coins, credit, tilt and slam through A4J3; playfield switches use A4J2. Five strobes and eight returns are transcribed with their literal connector pins and wire order. Contacts are normally open and have series 1N4004 diodes. The unmasked BY35 read path and the ROM's own diagnostic agree on public 1 for a closure. Consume public states as delivered; do not apply a second controller-wide inversion.

Tilt 7 combines roll and pendulum contacts. Slam 8 combines door/tilt-board contacts and the playfield contact described on manual page 5; the location drawing lists the first two outside the playfield but does not locate the playfield member. Operator additions are expressly allowed. No total slam quantity or fabricated playfield coordinate is asserted.

Service -7 is the normally-open door Self Test button. Service -6 reaches the CPU NMI and corresponds to the separately drawn on-board S33 pushbutton, which the assembly drawing calls Memory Clear. The remote door S33 Memory Clear contact on A4J3-5 is labelled EXT. BOOKKEEPING RESET on the MPU sheet; it is retained as physical.input.direct identity 3, with no controller transport and no assumed host-write substitute. Generic sound diagnostic -5 is a meaningful virtual ST300 route: sndbrdIntf installs st300_switch_w, which sets voiceSw for st300_ctrl_w. No fitted Seawitch sound-diagnostic button is inferred from that route.

The driver declares the lower generic button positions only: 84 left and 82 right. Each operates the two physical flippers on its side. Generic upper positions 83/81 have no independent fitted button and cannot reach the CPU's row-read path; the gameplay probe corroborates their lack of coil response. The physical upper flippers therefore do not imply upper public button addresses.

All 32 physical option switches are represented, with S5 and S13 unused by the game. The complete assignments and every printed setting table are retained in options.md. Coin chute 1 uses S9-12, chute 2 S1-4, chute 3 S25-28. S6 selects high-score extra ball/replay, S7 three/five balls, S8 the special/multiplier-reset threshold, S14 background sound, S15-16 high-game award, S17 special alternation, S18-19 maximum credits, S20 credit display, S21 match, S22 special limit, S23-24 extra-ball alternation, S29-30 extra-ball memory and S31-32 special award. S33 is not an option DIP.

## Solenoids and physical flippers

The printed solenoid numbers are SDU Q/transistor positions. Public 1-15 reach Q2,Q1,Q5,Q6,Q7,Q3,Q4,Q8,Q13,Q14,Q9,Q10,Q12,Q11,Q16 respectively. Continuous public 17,18,19,20 reach Q17,Q19,Q15,Q18. This map is read from Seawitch's own U2 decoder and PB4-PB7 circuit; the retained burn-in sequence corroborates all nineteen positions. Q5,Q10,Q11,Q12,Q16,Q17,Q18 are explicitly OPEN/N/U. Their diagnostic pulses are explained by the sweep. Public 17 and 20 additionally transition [1, 0] during the gameplay run's boot stabilization, before any scripted input: startup state on PB4/PB7 is exposed by the inverted continuous-port export in by35.c pia1b_w. This is not diagnostic-only activity; no particular ROM instruction is inferred. Neither startup nor diagnostic transitions establish a fitted load. These unfitted physical driver positions retain kind coil and availability unused; unused matrix/flipper positions likewise retain kind switch. Public 16 is an unaddressable decoder slot.

Used public outputs are top thumper 1, left thumper 2, left/right slings 4/5, knocker 6, center/left/upper-right bank reset 7/8/9, out-hole 10, right thumper 11, coin lockout 18 and flipper-enable relay 19. Isolated gameplay closures pair switches 9/10/12/13/14 with coils 1/2/4/5/11. The final target of each bank causes its corresponding reset. Tilt 7 drops relay 19; the next serve enables normal play again.

Two dual-winding flippers share each side's hard-wired circuit through Q15's relay. Lower coils are J-25-475/34-4500, upper coils J-25-600/34-4500. The four winding-bypass contacts are normally closed at rest and open at stroke to insert the hold winding; the two side inventories are profile-local physical identities 1/2, projected onto their two flipper pivots. The factory drawing's additional E.O.S.-labelled series marks remain literal in the circuit excerpt. No extra contact quantity, independent public channel or physical staging time is invented from those marks.

PinMAME synthesizes right 45/46 and left 47/48 together, for the full enabled button closure. 46 and 48 describe the two physical coils on each side; 45 and 47 are meaningful virtual states, not additional coils. These callbacks do not measure winding current or EOS motion. The retained script moves both flippers of a side on its lower callback; mechanical stroke/return timing remains table-owned.

The cabinet drawing calls the knocker wire B-Y while the SDU annotation says G-B. Both readings are preserved and structured wiring follows the cabinet sheet. This disagreement concerns wiring detail, with identity, public address and fitment settled; it is a note rather than an unresolved machine conflict.

## Lamps and general illumination

All sixty discrete LDA-100 SCR outputs are represented. Public address is 16*k+s+1 for U(k+1), S(s), and the game's circuit maps each line through its own resistor to its SCR and connector branches. This is not a lamp matrix. Public 16,32,48,64 are decoder holes.

The easily crossed pairs were checked from Seawitch's own drawing: public 24 is Q25 (spinner second-bottom, J1-6), public 25 is Q24 (right return, J1-5); public 42 is Q41 (left special, J3-20), public 58 is Q46 (middle-bank last-target 10,000, J3-18). U3/U4 print S12-S14 above S0, which must not be read as part of the previous decoder. The full decoder/SCR/connector transcription is retained independently of the complete load list.

Shoot Again shares Q3/public 11 between the separately printed J1-26 PLAYFIELD and J2-21 INSERT loads. INSERT denotes the backbox insert panel, corroborated by the separate playfield row and backbox construction. Both locations are preserved; the two connector/location rows do not establish a total socket quantity, so quantity stays unset. Four backbox-only outputs have controlled not_applicable placement records.

Public 29/Q15/J2-23, 41/Q42/J3-21, 51/Q51/J3-15 and 57/Q56/J3-10 have no printed load in either game-specific list. All four stay availability unknown. Burn-in drives every SCR, including these. Public 51 also changes during the scripted game; the transition happens during the upper-button-83 action, alongside background lamp activity, and is not attributed to that button. A run cannot establish whether a bulb is physically fitted. Resolution requires tracing an unrestored harness/socket at the concrete connector pins. No #44 bulb part or quantity is asserted for unknown loads.

General illumination is physically fitted and transformer-fed. The game's playfield sheet labels A2J1-8 W to A2J1-1 R as 6 VAC, and its cabinet sheet supplies front-door lighting on A2J2-1 to A2J2-5. The retained physical photograph corroborates backbox lamps, but the generic transformer diagram does not settle this game's populated backbox harness pins. No controlled GI relay or PinMAME GI output is fitted in these sources. physical.output.gi identity 1 records that physical circuit and has no controller transport; it must not be treated as a native GI channel.

The retained table turns its GI collection on. It contains 54 member occurrences, 53 distinct names and duplicate Light35, including glow/render helpers. Membership does not establish real socket count or branch wiring. The separate cosmetic bumper states 180-182 and VPX Flasher objects are not physical flasher outputs.

## Ball lifecycle and mechanisms

This is a single-ball game without a storage trough. Initialize the ball on switch 33 and all banks up. Credit/start resets all three banks and energizes the out-hole feed while 33 remains closed. Move the ball off 33 after the physical eject, into the manual shooter lane. The table's ballrelease kicker is the virtual serve destination; it is not another physical coil or sensor. Leaving 33 occupied produces repeat out-hole and bank-reset pulses, as the retained game shows. On drain, allow the ROM to count bonus and advance player/ball; an earned extra ball is played immediately without that advance. Tilt suppresses bonus for that ball and disables flippers until the next serve; slam loses the game through a delay.

Center bank: targets 21-24, highest to lowest, four-bank assembly D-580-4B, common reset public 7. Upper-right bank: 29-32, four-bank D-580-4B, reset 9. Left bank: 38-40, three-bank D-580-3A, reset 8. Each target independently falls and latches its contact closed. Hold it closed until the common reset bar raises it, then release it. A jam or stuck target leaves feedback closed; do not clear it merely because a timer elapsed. The retained script lists left/right bank objects in reverse order but preserves each address's own physical target.

The right spinner A-563-13 closes 5 on each revolution and has no actuator or home sensor. Star buttons 4 and 25 are passive rollovers. Bumper skirts and sling rubbers close their switches; the ROM fires the paired coil and spring return opens the contact. The runway gate is passive ball routing: SLS/SLS2 animate it from ball passage/direction with no output callback. It is not a powered diverter. All mechanisms' sensor/actuator membership and causal notes are typed in the definition. Physical pulse shaping, travel speed, spring force and animation remain recreation parameters.

## Rules, displays and sound

The factory rules govern the stock game. Drops and lit stand-ups advance bonus by 1,000; outlanes/runway by 3,000; maximum bonus is 39,000 times multiplier. A completed lit INCREASE X bank advances multiplier to a maximum 7X. The option-selected 6X/7X threshold resets multiplier to 3X, with lower multipliers carried between balls. Each drop spots a loop lamp; bank completion transfers its loop award to the corresponding LIGHTS EXTRA BALL. A repeated bank with one target left can award the lit bonus plus 1,000. All ten loop lamps and all three banks enable double loop value. The complete options excerpt retains adjustable special, extra-ball, pricing and memory behavior; modified firmware may change rules.

Four seven-digit player displays use layout indices 0-3, segment-memory starts 1,9,17,25; credits index 4 starts 35 and match/ball-in-play index 5 starts 38, both two digits. Physical displays are in the backbox. PinMAME's extra DMD-style callback 6 renders the segment presentation and is not another physical display. Sound is ST300, factory C-605; sound test numbers 20 THRU 29 in the manual are one printed sound range, not additional solenoid addresses.

## Runtime and deterministic validation

Three accepted fresh-state scenarios are retained: burn-in, switch-test-v2 and gameplay. Their exact scenarios, raw runs, mutable state and canonical directory manifest remain under review-artifacts/stern.seawitch.1980/harness. The compact repository evidence is recomputed by tools/summarize_seawitch_runtime.py. It checks the full SCR sweep, SDU cycle order, ROM-displayed switch numbers, scenario hashes and pinned DLL. Host switch readback is excluded from ROM observations.

The initial switch-test run has runner failure null but remained in the solenoid test because a service press was missed. It is retained for diagnosis and excluded from switch-recognition claims. A navigation probe established 300 ms holds and five-second settles; the accepted sweep displays each isolated address 01 through 40. The burn-in display multiplexes digit cycling, so no semantic name is inferred from its digits. Each game began in a newly created state directory, mechanics mask 0, keyboard handling off, default binary output mode.

The verified DLL SHA-256 is 2011243e8d2747cbeac5e42262c271bbdd6a467605acd5edf13dbeeefcbc3591. It was built from the clean exact pinned checkout, using an external path-absolutized copy of its official CMake project. An older ignored root CMake copy caused an initial link failure and was left untouched; no tracked source was patched. The complete build/ROM identity record and logs remain external. The usable verified DLL was restored to the original managed build output when it was absent.

The deterministic curator reproduces the canonical definition, byte-identical seed, knowledge note and spatial JSON/Markdown. Its checks reject missing/changed excerpts, stale products and an existing author-ready artifact. Evidence-enabled checks rehash every retained extraction file, all pinned PDFs/photos, every stored coordinate and the complete runtime manifest/summary. No-evidence gates still validate all portable provenance and canonical data.

## Spatial limits and concrete remaining work

Exact retained bounds are left 0, top 0, right 956, bottom 1979 VPX units. Normalize (x-left)/(right-left), (y-top)/(bottom-top), rounded by the repository helper to six decimals. x=0 is player-left, y=0 rear; y=1 apron. No photo pixel or another game's coordinate frame is substituted.

Switch/coil positions are observed table geometry, with explicit projections: sling wall vertex means, reset effects on their own bank, EOS contacts on flipper pivots, and the hidden out-hole on the Drain collection proxy. The shooter-lane ballrelease is excluded as a physical out-hole anchor. The location drawings were visually reconciled for side/order/topology but have no independent quantitative control fit; none of these observations are promoted to validated placement.

Every retained lN light is an insert overlay with is_bulb_light=false and show_bulb_mesh=false. The report preserves its exact candidate coordinate and exclusion reason; no overlay is presented as a physical socket. Locate controlled-lamp bulbs and GI emitters from a bulb-level drawing or a measured, independently reconciled underside photograph, retaining frame/control points, actual socket centers and transformation. Resolve the four named LDA fitments and locate the playfield slam contact/hidden out-hole hardware. Until those dimensions are settled, the machine stays partial.
