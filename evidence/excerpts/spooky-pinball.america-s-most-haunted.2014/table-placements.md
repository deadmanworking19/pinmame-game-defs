# LW recreation placements: America's Most Haunted

Table `America's Most Haunted (Spooky Pinball 2014) LW.vpx` (SHA-256 c677c6b98bfd563f4ae83dc93bd5c6f807b9bce6b380063655b9e40e595d0500, 347865088 bytes), version 2.0 by freneticamnesic, Shoopity and LoadedWeapon; extracted with vpxtool 0.33.3 (manifest SHA-256 b717aa8414042919fc8fd55e9de9a469d078f819f9c61908163d04a9ceb470e2, 2185 files, 388534248 bytes); its script.vbs SHA-256 ffaeea988c8e27d2d7768c4cfcdfe280776e4b108921c1f728ec51bfff099a0d. Playfield bounds left=0 top=0 right=952 bottom=2185; normalized = (x/952, y/2185). The table runs its own port of the game code, not the ROM, so each object was chosen by what its script does, checked against the factory chart's label. The primitives' stated mesh centres come from `vpxtool export obj --units vpu` (OBJ SHA-256 6ed05f976f7b5d01ed85c31449ebe3e5334953eaa95df310f7c8228c730adfa1).

| Device | Table object | Raw VPX | Normalized | Script binding |
|---|---|---|---|---|
| switch 31 | WaSw16 (Wall, drag_point_centroid) | 77.34375, 1167.0 | 0.081243, 0.534096 | WaSw16_Hit (script.vbs line 10542) advances wiki(player): the WIKI target [16]. |
| switch 32 | WaSW17 (Wall, drag_point_centroid) | 134.90625, 841.21875 | 0.141708, 0.384997 | WaSw17_Hit (line 10571) advances tech(player): the TECH target [17]. |
| switch 33 | WaSw18 (Wall, drag_point_centroid) | 325.61646, 862.960562 | 0.342034, 0.394948 | WaSw18_Hit (line 10596), the left wall of the TargetBankWalls collection under PrBankTop: GHOST TARGET 1 (left) [18]. |
| switch 34 | WaSw19 (Wall, drag_point_centroid) | 379.63977, 840.585253 | 0.398781, 0.384707 | WaSw19_Hit (line 10704), the middle target-bank wall: GHOST TARGET 2 (middle) [19]. |
| switch 35 | WaSw20 (Wall, drag_point_centroid) | 432.5363, 818.871752 | 0.454345, 0.37477 | WaSw20_Hit (line 10812), the right target-bank wall: GHOST TARGET 3 (right) [20]. |
| switch 37 | KiVUK1 (Kicker, center) | 797.0, 1138.7925 | 0.837185, 0.521186 | KiVUK1_Hit (line 11827, commented 'basement exit/VUK') sets Sw22 and sends the ball to the basement trough; the scoop kick returns it here (line 1355): BASEMENT RIGHT SCOOP [22]. |
| switch 38 | KiDoor (Kicker, center) | 147.75, 519.9375 | 0.1552, 0.237958 | KiDoor_Hit (line 11877, commented 'Switch 23') sets Sw23 and runs leftVUKlogic: VUK LEFT BEHIND DOOR [23]. |
| switch 45 | TrSw28 (Trigger, center) | 902.3334, 405.125 | 0.947829, 0.185412 | TrSw28_Hit (line 11033) runs hotelPathLogic: HOTEL PATH [28]. |
| switch 46 | WaSw29 (Wall, drag_point_centroid) | 556.879068, 797.355525 | 0.584957, 0.364922 | WaSw29_Hit (line 11044) counts callHits towards the elevator: ELEVATOR CALL BUTTON [29]. |
| switch 47 | WaSw30 (Wall, drag_point_centroid) | 710.625, 841.1953 | 0.746455, 0.384986 | WaSw30_Hit (line 11065) advances psychic(player): PSYCHIC [30]. |
| switch 51 | TrSw32 (Trigger, center) | 86.5, 415.125 | 0.090861, 0.189989 | TrSw32_Hit (line 11106) calls balconyJump(): BALCONY JUMP SUCCESS [32]. |
| switch 52 | TrSw33 (Trigger, center) | 742.0, 549.75 | 0.779412, 0.251602 | TrSw33_Hit (line 11113) calls balconyApproach(): BALCONY JUMP APPROACH [33]. |
| switch 53 | TrSw34 (Trigger, center) | 457.0, 494.5 | 0.480042, 0.226316 | TrSw34_Hit (line 11126) scores the pop skill shot for a ball that slips through the pops: POP PATH/ JUMP FAIL [34]. |
| switch 56 | Bu1 (Bumper, center) | 212.5, 239.90741 | 0.223214, 0.109797 | Bumpers_Hit (line 11551) treats the three Bumpers members alike, so the pop is taken from the wire chart's position: Pop Bumper 0 is the upper left pop, the table's upper left bumper Bu1 [37]. |
| switch 57 | TrSw38 (Trigger, center) | 90.25, 214.75 | 0.0948, 0.098284 | TrSw38_Hit (line 11181, commented 'Left orbit UPPER switch'): UPPER LEFT ORBIT [38]. |
| switch 58 | TrSw39 (Trigger, center) | 52.75, 688.75 | 0.05541, 0.315217 | TrSw39_Hit (line 11194, commented 'Left orbit LOWER switch'): LOWER LEFT ORBIT [39]. |
| switch 61 | TrSw41 (Trigger, center) | 523.87537, 250.17401 | 0.550289, 0.114496 | The left top lane. TrSw41_Hit (line 11203) sets orb bits 36, which updateRollovers (line 9937) shows on lamp 32 "O", the leftmost lane lamp; the ROM lights O (public 51) when public 61 [40] closes (lanes run). The table names its lane triggers out of order (TrSw40 is B, TrSw41 is O). |
| switch 62 | TrSw42 (Trigger, center) | 599.8503, 250.67401 | 0.630095, 0.114725 | The middle top lane. TrSw42_Hit (line 11225, commented '"R"') sets orb bits 18, lamp 33 "R"; the ROM lights R (public 52) when public 62 [41] closes (lanes run). |
| switch 63 | TrSw40 (Trigger, center) | 676.2733, 251.212 | 0.710371, 0.114971 | The right top lane. TrSw40_Hit (line 11246, commented '"B"') sets orb bits 9, lamp 34 "B"; in the ROM public 63 [42] completes O-R-B after 61 and 62 (lanes run). |
| switch 64 | KiHellevator (Kicker, center) | 782.0, 322.25 | 0.821429, 0.147483 | KiHellEvator_Hit (line 11267, commented 'Switch 43') starts ballElevatorLogic: BALL IN ELEVATOR CAR [43]. |
| switch 66 | Bu3 (Bumper, center) | 306.5, 404.9074 | 0.321954, 0.185312 | Bumpers_Hit (line 11551); the wire chart's lower pop is POP BUMPER 2, the table's lower bumper Bu3 [45]. |
| switch 67 | Bu2 (Bumper, center) | 401.0, 240.15741 | 0.421218, 0.109912 | Bumpers_Hit (line 11551); the wire chart's upper right pop is POP BUMPER 1, the table's upper right bumper Bu2 [46]. |
| switch 71 | TrSw48 (Trigger, center) | 54.0, 1708.25 | 0.056723, 0.781808 | TrSw48_Hit (line 11273) adds rollover bits 136 (the G lamp, line 9952) with a 'bad' sound: LEFT OUTLANE [48]. |
| switch 72 | TrSw49 (Trigger, center) | 125.0, 1611.75 | 0.131303, 0.737643 | TrSw49_Hit (line 11282) adds rollover bits 68: LEFT INLANE [49]. |
| switch 73 | LeftSlingShot (Wall, drag_point_centroid) | 231.47443, 1604.8617 | 0.243145, 0.73449 | LeftSlingShot_Slingshot (line 11452): LEFT SLING [50]. |
| switch 74 | LeftFlipper (Flipper, center) | 277.0, 1848.0 | 0.290966, 0.845767 | LEFT EOS [51] has no table object; the end-of-stroke contact is on the flipper assembly, placed on the left flipper's pivot. |
| switch 75 | RightFlipper (Flipper, center) | 593.5, 1848.0 | 0.623424, 0.845767 | RIGHT EOS [52] has no table object; the end-of-stroke contact is on the flipper assembly, placed on the right flipper's pivot. |
| switch 76 | RightSlingShot (Wall, drag_point_centroid) | 640.461867, 1605.2336 | 0.672754, 0.734661 | RightSlingShot_Slingshot (line 11423): RIGHT SLING [53]. |
| switch 77 | TrSw54 (Trigger, center) | 746.25, 1611.75 | 0.783876, 0.737643 | TrSw54_Hit (line 11299) adds rollover bits 34: RIGHT INLANE [54]. |
| switch 78 | TrSw55 (Trigger, center) | 817.25, 1707.25 | 0.858456, 0.78135 | TrSw55_Hit (line 11313) adds rollover bits 17 (the R lamp) with a 'bad' sound: RIGHT OUTLANE [55]. |
| switch 82 | TrSw57 (Trigger, center) | 899.5, 1962.75 | 0.944853, 0.898284 | TrSw57_Hit (line 11323) sets Sw57 and holds the ball for the launch: SHOOTER LANE [57]. |
| switch 84 | KiMainTrough1 (Kicker, center) | 781.5, 1922.2925 | 0.820903, 0.879768 | KiMainTrough1_Hit (line 11790, 'the bottom most kicker') sets Sw59: TROUGH BALL 1 [59]. |
| switch 85 | KiMainTrough2 (Kicker, center) | 733.5, 1951.7925 | 0.770483, 0.893269 | KiMainTrough2_Hit (line 11796) sets Sw60: TROUGH BALL 2 [60]. |
| switch 86 | KiMainTrough3 (Kicker, center) | 685.0, 1980.7925 | 0.719538, 0.906541 | KiMainTrough3_Hit (line 11802) sets Sw61: TROUGH BALL 3 [61]. |
| switch 87 | KiMainTrough4 (Kicker, center) | 636.5, 2009.7925 | 0.668592, 0.919814 | KiMainTrough4_Hit (line 11808) sets Sw62: TROUGH BALL 4 [62]. |
| switch 88 | KiDrain (Kicker, center) | 514.875, 2084.605 | 0.540835, 0.954053 | KiDrain_Hit (line 11781, commented 'Switch 63'): DRAIN [63]. |
| switch 95 | TrSw24 (Trigger, center) | 371.12115, 731.53265 | 0.389833, 0.334798 | TrSw24_Hit (line 10928, 'GHOST HIT? (the loop)', 'not a matrix switch'): the GHOST LOOP OPTO, cabinet input 13. |
| switch 96 | TrSw31 (Trigger, center) | 198.0, 771.5 | 0.207983, 0.353089 | TrSw31_Hit (line 11100, 'not a matrix switch') calls doorDo(): the SPOOKY DOOR OPTO, cabinet input 14. |
| solenoid 1 | TrSw24m (Trigger, center) | 363.25, 706.375 | 0.381565, 0.323284 | mMagnaSave is a cvpmMagnet initialised on TrSw24m (lines 186-187) and switched by the loop logic (line 5482): LOOP MAGNET. |
| solenoid 9 | LeftSlingShot (Wall, drag_point_centroid) | 231.47443, 1604.8617 | 0.243145, 0.73449 | The left slingshot wall that LeftSlingShot_Slingshot (line 11452) kicks: LSLING. |
| solenoid 10 | RightSlingShot (Wall, drag_point_centroid) | 640.461867, 1605.2336 | 0.672754, 0.734661 | The right slingshot wall that RightSlingShot_Slingshot (line 11423) kicks: RSLING. |
| solenoid 11 | KiVUK1 (Kicker, center) | 797.0, 1138.7925 | 0.837185, 0.521186 | The basement scoop eject: the basement trough's ball is moved to KiVUK1 and kicked out at 218 degrees (line 1355): SCOOPKICK. |
| solenoid 12 | KiDoor (Kicker, center) | 147.75, 519.9375 | 0.1552, 0.237958 | The VUK behind the Spooky Door kicks the ball held on KiDoor (KiDoor_Hit, line 11877): VUK. |
| solenoid 14 | Bu1 (Bumper, center) | 212.5, 239.90741 | 0.223214, 0.109797 | Upper left pop (the ROM's upper left pop) on the upper left bumper Bu1. |
| solenoid 15 | Bu2 (Bumper, center) | 401.0, 240.15741 | 0.421218, 0.109912 | Upper right pop on the upper right bumper Bu2. |
| solenoid 16 | Bu3 (Bumper, center) | 306.5, 404.9074 | 0.321954, 0.185312 | Lower pop on the lower bumper Bu3. |
| solenoid 17 | RightFlipper (Flipper, center) | 593.5, 1848.0 | 0.623424, 0.845767 | Right flipper winding, placed on the right flipper's pivot. |
| solenoid 18 | RightFlipper (Flipper, center) | 593.5, 1848.0 | 0.623424, 0.845767 | Right flipper winding, placed on the right flipper's pivot. |
| solenoid 19 | LeftFlipper (Flipper, center) | 277.0, 1848.0 | 0.290966, 0.845767 | Left flipper winding, placed on the left flipper's pivot. |
| solenoid 20 | LeftFlipper (Flipper, center) | 277.0, 1848.0 | 0.290966, 0.845767 | Left flipper winding, placed on the left flipper's pivot. |
| solenoid 21 | KiMainTrough1 (Kicker, center) | 781.5, 1922.2925 | 0.820903, 0.879768 | ServeBall (line 12178) kicks the ball from KiMainTrough1, the trough's exit position, into the shooter lane: BALL LOAD. |
| solenoid 22 | KiDrain (Kicker, center) | 514.875, 2084.605 | 0.540835, 0.954053 | KiDrain_Hit (line 11781) moves the drained ball into the trough: DRAIN KICK. |
| solenoid 23 | TrAutoPlunge (Trigger, center) | 899.5, 1966.75 | 0.944853, 0.900114 | AutoPlunger is a cvpmImpulseP on TrAutoPlunge (lines 192-195), fired by AutoPlunge (line 1370): AUTOPLUNGER. |
| solenoid 57 | PrElevator (Primitive, position) | 781.6929, 322.0 | 0.821106, 0.147368 | TiElevator_Timer (line 11571) moves PrElevator up and down, carrying the ball kicked at KiHellevator: the Hellevator servo (0). Its position agrees with its exported mesh centre (781.69, 322.00). |
| solenoid 58 | PrDoor (Primitive, position) | 237.5, 656.75 | 0.249475, 0.300572 | The door turns about PrDoor's position (ObjRotZ, lines 2822-2881 and 11693), the servo's axis: the Spooky Door servo (1). The door panel's exported mesh centre is (195.20, 681.88). |
| solenoid 59 | PrGhost (Primitive, position) | 365.5, 575.5 | 0.383929, 0.263387 | The ghost turns about PrGhost's position (ObjRotZ, lines 11678-11688), the servo's axis: the Ghost servo (2). The figure's exported mesh centre is (380.14, 568.70). |
| solenoid 60 | PrBankTop (Primitive, position) | 372.25, 827.125 | 0.391019, 0.378547 | WaSw18_Hit compares PrBankTop.Z with TargetUp (line 10598): the bank the Target servo (3) raises and lowers. Its position agrees with its exported mesh centre (371.66, 825.54). |
| solenoid 62 | GILight1 (Light, center) | 365.0, 575.8125 | 0.383403, 0.26353 | The ghost's LED: the Ghost_RGB collection (GILight1, GILight2 at one point, and Li64) takes ghostRGB (line 3709); GILight1 sits on the ghost's axis. |
| solenoid 63 | GILight1 (Light, center) | 365.0, 575.8125 | 0.383403, 0.26353 | The ghost's LED: the Ghost_RGB collection (GILight1, GILight2 at one point, and Li64) takes ghostRGB (line 3709); GILight1 sits on the ghost's axis. |
| solenoid 64 | GILight1 (Light, center) | 365.0, 575.8125 | 0.383403, 0.26353 | The ghost's LED: the Ghost_RGB collection (GILight1, GILight2 at one point, and Li64) takes ghostRGB (line 3709); GILight1 sits on the ghost's axis. |
| lamp 11 | Li0 (Light, center) | 110.75, 1229.25 | 0.116334, 0.562586 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 0 is Li0. |
| lamp 12 | Li1 (Light, center) | 158.25, 907.25 | 0.166229, 0.415217 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 1 is Li1. |
| lamp 13 | Li2 (Light, center) | 518.0, 1712.75 | 0.544118, 0.783867 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 2 is Li2. |
| lamp 14 | Li3 (Light, center) | 146.0, 1098.375 | 0.153361, 0.502689 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 3 is Li3. |
| lamp 15 | Li4 (Light, center) | 131.375, 1059.625 | 0.137999, 0.484954 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 4 is Li4. |
| lamp 16 | Li5 (Light, center) | 117.625, 1020.75 | 0.123556, 0.467162 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 5 is Li5. |
| lamp 17 | Li6 (Light, center) | 104.0, 979.125 | 0.109244, 0.448112 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 6 is Li6. |
| lamp 18 | Li7 (Light, center) | 86.125, 933.75 | 0.090467, 0.427346 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 7 is Li7. |
| lamp 21 | Li8 (Light, center) | 274.0, 998.75 | 0.287815, 0.457094 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 8 is Li8. |
| lamp 22 | Li9 (Light, center) | 260.5, 958.5 | 0.273634, 0.438673 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 9 is Li9. |
| lamp 23 | Li10 (Light, center) | 248.5, 918.5 | 0.261029, 0.420366 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 10 is Li10. |
| lamp 24 | Li11 (Light, center) | 235.25, 876.5 | 0.247111, 0.401144 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 11 is Li11. |
| lamp 25 | Li12 (Light, center) | 219.75, 832.5 | 0.23083, 0.381007 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 12 is Li12. |
| lamp 26 | Li13 (Light, center) | 207.0, 787.0 | 0.217437, 0.360183 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 13 is Li13. |
| lamp 27 | Li14 (Light, center) | 192.375, 739.75 | 0.202075, 0.338558 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 14 is Li14. |
| lamp 28 | Li15 (Light, center) | 164.0, 673.25 | 0.172269, 0.308124 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 15 is Li15. |
| lamp 31 | Li16 (Light, center) | 426.4944, 954.8352 | 0.447998, 0.436996 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 16 is Li16. |
| lamp 32 | Li17 (Light, center) | 338.0, 897.5 | 0.355042, 0.410755 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 17 is Li17. |
| lamp 33 | Li18 (Light, center) | 390.625, 872.625 | 0.41032, 0.399371 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 18 is Li18. |
| lamp 34 | Li19 (Light, center) | 445.5, 851.25 | 0.467962, 0.389588 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 19 is Li19. |
| lamp 35 | Li20 (Light, center) | 513.5, 793.5 | 0.539391, 0.363158 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 20 is Li20. |
| lamp 36 | Li21 (Light, center) | 516.5, 745.5 | 0.542542, 0.34119 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 21 is Li21. |
| lamp 37 | Li22 (Light, center) | 515.5, 695.0 | 0.541492, 0.318078 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 22 is Li22. |
| lamp 38 | Li23 (Light, center) | 529.0, 649.5 | 0.555672, 0.297254 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 23 is Li23. |
| lamp 41 | Li24 (Light, center) | 545.25, 838.5 | 0.572742, 0.383753 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 24 is Li24. |
| lamp 42 | Li25 (Light, center) | 533.0, 878.0 | 0.559874, 0.401831 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 25 is Li25. |
| lamp 43 | Li26 (Light, center) | 550.5, 1090.0 | 0.578256, 0.498856 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 26 is Li26. |
| lamp 44 | Li27 (Light, center) | 562.5, 1047.5 | 0.590861, 0.479405 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 27 is Li27. |
| lamp 45 | Li28 (Light, center) | 574.125, 1009.5 | 0.603072, 0.462014 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 28 is Li28. |
| lamp 46 | Li29 (Light, center) | 591.0, 963.5 | 0.620798, 0.440961 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 29 is Li29. |
| lamp 47 | Li30 (Light, center) | 602.5, 918.5 | 0.632878, 0.420366 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 30 is Li30. |
| lamp 48 | Li31 (Light, center) | 617.0, 875.0 | 0.648109, 0.400458 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 31 is Li31. |
| lamp 51 | Li32 (Light, center) | 523.25, 157.5 | 0.549632, 0.072082 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 32 is Li32. |
| lamp 52 | Li33 (Light, center) | 598.75, 156.5 | 0.628939, 0.071625 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 33 is Li33. |
| lamp 53 | Li34 (Light, center) | 676.5, 158.25 | 0.710609, 0.072426 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 34 is Li34. |
| lamp 55 | Li36 (Light, center) | 707.0, 1107.0 | 0.742647, 0.506636 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 36 is Li36. |
| lamp 56 | Li37 (Light, center) | 721.5, 1067.125 | 0.757878, 0.488387 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 37 is Li37. |
| lamp 57 | Li38 (Light, center) | 736.625, 1029.125 | 0.773766, 0.470995 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 38 is Li38. |
| lamp 58 | Li39 (Light, center) | 752.5, 983.5 | 0.790441, 0.450114 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 39 is Li39. |
| lamp 61 | Li40a (Light, center) | 71.182106, 66.124214 | 0.074771, 0.030263 | light(40) drives Li40, which the table parks in a row by the apron; a timer copies it to Li40a (line 11633), the bulb beside the flasher dome base Primitive002. |
| lamp 62 | Li41a (Light, center) | 823.2173, 483.39807 | 0.864724, 0.221235 | light(41) drives Li41, which the table parks in a row by the apron; a timer copies it to Li41a (line 11634), the bulb beside the flasher dome base Primitive001. |
| lamp 63 | Li42a (Light, center) | 827.48486, 1044.6665 | 0.869207, 0.478108 | light(42) drives Li42, which the table parks in a row by the apron; a timer copies it to Li42a (line 11635), the bulb beside the flasher dome base Primitive005. |
| lamp 64 | Li43 (Light, center) | 672.75, 1381.625 | 0.70667, 0.632323 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 43 is Li43. |
| lamp 65 | Li44 (Light, center) | 691.75, 1338.25 | 0.726628, 0.612471 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 44 is Li44. |
| lamp 66 | Li45 (Light, center) | 711.375, 1294.875 | 0.747243, 0.59262 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 45 is Li45. |
| lamp 67 | Li46 (Light, center) | 733.625, 1252.5 | 0.770614, 0.573227 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 46 is Li46. |
| lamp 68 | Li47 (Light, center) | 754.0, 1209.75 | 0.792017, 0.553661 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 47 is Li47. |
| lamp 71 | Li48 (Light, center) | 353.0, 1711.75 | 0.370798, 0.78341 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 48 is Li48. |
| lamp 72 | Li49 (Light, center) | 406.75, 1741.75 | 0.427258, 0.79714 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 49 is Li49. |
| lamp 73 | Li50 (Light, center) | 466.0, 1741.75 | 0.489496, 0.79714 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 50 is Li50. |
| lamp 74 | Li51 (Light, center) | 687.25, 914.75 | 0.721901, 0.41865 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 51 is Li51. |
| lamp 75 | Li52 (Light, center) | 49.2606, 1453.5709 | 0.051744, 0.66525 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 52 is Li52. |
| lamp 76 | Li53 (Light, center) | 125.75, 1455.0 | 0.13209, 0.665904 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 53 is Li53. |
| lamp 77 | Li54 (Light, center) | 739.375, 1453.875 | 0.776654, 0.665389 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 54 is Li54. |
| lamp 78 | Li55 (Light, center) | 819.875, 1455.25 | 0.861213, 0.666018 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 55 is Li55. |
| lamp 81 | Li56 (Light, center) | 437.0, 1908.5 | 0.459034, 0.873455 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 56 is Li56. |
| lamp 82 | Li57 (Light, center) | 436.25, 1674.0 | 0.458246, 0.766133 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 57 is Li57. |
| lamp 83 | Li58 (Light, center) | 436.25, 1602.75 | 0.458246, 0.733524 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 58 is Li58. |
| lamp 84 | Li59 (Light, center) | 436.5, 1531.0 | 0.458508, 0.700686 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 59 is Li59. |
| lamp 85 | Li60 (Light, center) | 435.75, 1459.0 | 0.457721, 0.667735 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 60 is Li60. |
| lamp 86 | Li61 (Light, center) | 437.0, 1388.5 | 0.459034, 0.635469 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 61 is Li61. |
| lamp 87 | Li62 (Light, center) | 436.5, 1315.5 | 0.458508, 0.602059 | light(n) sets light_inserts(n).Intensity (script.vbs lines 9856-9877) and Light_Inserts lists Li0-Li62 in order, so lamp 62 is Li62. |
| lamp 88 | Light_Inserts__Light__64_ (Light, center) | 438.5, 1087.5 | 0.460609, 0.497712 | Lamp 63 is light_inserts(63), the 64th member of Light_Inserts, the light named 'Light_Inserts [Light](64)'. |

## Used devices without a placement

- switch 54: BASEMENT UPPER [35] is a switch in the basement subway under the playfield; the table models the subway off the playfield (TrSw35 at x=1026.5), so it has no playfield position.
- switch 55: BASEMENT LOWER [36] is a switch in the basement subway; the table's TrSw36 sits off the playfield at x=1027.
- solenoid 51: The on-board RGB LEDs light the cabinet's left and right playfield edges (the script's leftRGB and rightRGB, 'cabinet GI'); nothing retained says which LED feeds which side, and the table draws each side as a row of about 35 lights, not as the physical strip.
- solenoid 52: The on-board RGB LEDs light the cabinet's left and right playfield edges (the script's leftRGB and rightRGB, 'cabinet GI'); nothing retained says which LED feeds which side, and the table draws each side as a row of about 35 lights, not as the physical strip.
- solenoid 53: The on-board RGB LEDs light the cabinet's left and right playfield edges (the script's leftRGB and rightRGB, 'cabinet GI'); nothing retained says which LED feeds which side, and the table draws each side as a row of about 35 lights, not as the physical strip.
- solenoid 54: The on-board RGB LEDs light the cabinet's left and right playfield edges (the script's leftRGB and rightRGB, 'cabinet GI'); nothing retained says which LED feeds which side, and the table draws each side as a row of about 35 lights, not as the physical strip.
- solenoid 55: The on-board RGB LEDs light the cabinet's left and right playfield edges (the script's leftRGB and rightRGB, 'cabinet GI'); nothing retained says which LED feeds which side, and the table draws each side as a row of about 35 lights, not as the physical strip.
- solenoid 56: The on-board RGB LEDs light the cabinet's left and right playfield edges (the script's leftRGB and rightRGB, 'cabinet GI'); nothing retained says which LED feeds which side, and the table draws each side as a row of about 35 lights, not as the physical strip.
