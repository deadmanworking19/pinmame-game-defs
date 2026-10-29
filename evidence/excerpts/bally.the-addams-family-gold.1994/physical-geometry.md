# Gold physical socket and mechanism audit

This is a curator's interpretation of retained sources, not a factory table transcription. The geometry seed retains every raw point, object, mesh bounds and normalization. Source-owned images remain outside Git with complete manifests.

## Authorities and edition reconciliation

The exact Gold manual identifies the fitted assemblies and circuit wiring. The undated IPDB 50038 hierarchical parts listing corroborates their contents; its complete selected branches are in `parts-crosscheck.md`. The Gold 0995 Alamo restoration archive shows the physical machine, including underside photos 40–45 and 53–63, coin door 51 and backbox 68. The original Alamo page and its complete original-image URL/hash manifest are retained. Gold 0984 owner photograph 34 shows the trough contacts from above with the apron removed. IPDB photographs 20799 and 20801 are credited to Mark Clayton and show the upper playfield with ramps removed and the lower playfield with apron removed respectively.

The exact Gold Sliderpoint table supplies its own bindings and geometry. The g5k 2.3.2 table is supplementary shared-layout geometry. Its ancestry means it cannot independently confirm the position of a shared object. It supplies modeled glass centers or separately bound functional contacts after the Gold assemblies, order, side and physical fitment have been established. Its bounds are 0,0,952.965,2164.76; Gold bounds are 0,0,985,2220. Normalize each point with its own table's bounds.

## General illumination

The Gold listing has 21 A-11905 #44 assemblies in the main playfield branch, one A-12887 #555 on A-15369-3/H-15232 brown/white-brown, and one A-12887 #555 on A-15369-1/H-15231 violet/white-violet. This is a physical assembly census, not a count of render lights. The exact Gold script's left/right groupings agree with the manual's string names and actual 3-20 connector routing. The later g5k table merges GI runtime control; it does not establish a different machine-side circuit split.

One glass envelope is counted for each connected baked-mesh bulb assembly. Weld vertices at 0.1 VPU before splitting triangle-connected components. Bounds and the complete splitting script are retained, so component numbers are locators within that pinned derivation, not intrinsic OBJ identities. Each envelope is checked against its own socket/base and the exact Gold light region. Three Gold envelopes are modeled separately in Primitive13, Primitive14 and Primitive160 and take precedence over the supplementary counterparts.

The 21 #44 envelopes reconcile as 14 on the left string and seven on the right. The component crosswalk is recorded individually in the geometry seed. The lower-left #555 glass is gRGP2_plasticOff component 30: bounds [25.4427,1328.1246,-80.87439] through [52.030403,1370.917,-62.469193]. Component 33 is the separate black holder; components 32 and 34 are electrical contacts. The glass center, rather than the holder or a light pool, supplies that placement.

RGP9_GI1_2Off component 5 is an extra modeled lamp at [351.0944,811.6257], not a 22nd factory GI #44. In the supplementary script, AllLamps includes CousinIttLight with TimerInterval 26; lines 2307–2312 toggle it with the optional CousinITT_5 figure. Its center lies inside that figure's transformed footprint. Exact Gold GI31 has no callback. This lamp therefore belongs to the optional Cousin Itt decoration and is excluded from GI.

Gold 0995 backbox photo 68 shows 15 wedge sockets on the orange house branch, eight wedge sockets on the yellow people branch, and seven metal-base self-blink bulbs on the yellow bare-bus branch. These reconcile with the listing's 23 #555 plus seven #455 backbox bulbs. Gold 0995 coin-door photo 51 shows two physical holders; the 09-61000-1 two-slot door and Gold 3-20 violet J119 branch corroborate the two cabinet loads. They contribute quantity but no playfield coordinates. No claim is made that every upper playfield GI wire was individually photographed.

## Trough and paired matrix lamps

Gold 2-24 and 2-40 identify two B-8925 miniature microswitches/wireforms and a separate right contact A-11680. The supplementary script's RealishTrough binds Trough3 to switch 15, Trough2 to 16 and BallRelease to 17 on Ramp48. The first two functional contact centers are [731.89264,1924.5958] and [783.9435,1898.9707] in that table. These are disclosed functional-contact projections, not microswitch body meshes. The exact Gold BallRelease [870.125,1940.625] supplies switch 17's projection and agrees with the later table's own right contact within 0.011 normalized. Gold 0984 and the Alamo underside views corroborate the three separate physical contacts. Leaderless location numbers supply no coordinates.

Gold's lamp table explicitly fits two bulbs to Jackpot 13 on A-15114 and two to Cousin It 26 on A-15113. All four sockets on each PCB are drawn in the native underside figure. The individual centers are independently read there, with the board's other single-circuit sockets checking identity and orientation. The geometry seed retains both reads for each paired circuit and the underside fit; no pair is synthesized as an offset about a single VPX light.

## Flasher census

The literal 3-6 rows and 2-43 symbols give two bulbs each for circuits 17, 18, 20 and 21. Circuit 19 has one lower-ramp dome and two jet-bumper sockets. The main-playfield A-12336-1 quantity five is exactly the two 19a sockets plus 20a, 21a and 22a. Circuit 22 has one playfield socket and three backbox cloud bulbs. The backbox bulbs contribute physical quantity but no playfield placements. Separate domes use their own glass/lens centers; bloom and reflection sprites are excluded.
