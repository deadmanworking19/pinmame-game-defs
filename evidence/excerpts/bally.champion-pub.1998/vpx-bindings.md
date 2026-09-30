# Retained Champion Pub script bindings

Embedded script SHA-256: 0060c3892e5b35d154d2fb5325284658787121b81111e6ba3d267d6d8bc66a6c; cGameName=cp_16. Version 1.2 mfuegemann. Known-working table is runtime-causality evidence; the factory manual controls physical construction.

## Live script statements

| Locator | Statement |
| --- | --- |
| script.vbs:60 | SolCallback(1)  = "SolCatapult" |
| script.vbs:61 | SolCallback(2)  = "SolTrough" |
| script.vbs:62 | SolCallback(5)  = "SolCornerKickout" |
| script.vbs:63 | SolCallback(8)  = "SolPostDiverter" |
| script.vbs:64 | SolCallback(9)  = "SolLeftScoop" |
| script.vbs:65 | SolCallback(10) = "SolRightScoop" |
| script.vbs:66 | SolCallback(12) = "SolPost" |
| script.vbs:67 | SolCallback(14) = "SolPopper" |
| script.vbs:68 | SolModCallback(17) = "sol17" |
| script.vbs:69 | SolModCallback(18) = "sol18" |
| script.vbs:70 | SolModCallback(19) = "UpperWhiteFlasher" |
| script.vbs:71 | SolModCallback(20) = "UpperRedFlasher" |
| script.vbs:72 | SolModCallback(21) = "LowerRedFlasher" |
| script.vbs:73 | SolModCallback(22) = "sol22" |
| script.vbs:74 | SolModCallback(23) = "SolRopeSpot" |
| script.vbs:75 | SolModCallback(24) = "SolSpeedBagSpot" |
| script.vbs:76 | SolCallback(28) = "SolLockPin" |
| script.vbs:77 | SolCallback(33) = "SolMagnetPopper" |
| script.vbs:78 | SolCallback(34) = "SolRampDiverter" |
| script.vbs:79 | SolCallback(35) = "SolLeftSP" |
| script.vbs:80 | SolCallback(36) = "SolRightSP" |
| script.vbs:81 | SolCallback(sLLFlipper) = "SolLFlipper" |
| script.vbs:82 | SolCallback(sLRFlipper) = "SolRFlipper" |
| script.vbs:84 | Set GIcallback2 = GetRef("UpdateGI") |
| script.vbs:174 | Sub LockPin_Timer |
| script.vbs:206 | Sub CornerKickout_Timer |
| script.vbs:229 | Sub catapultLaunchKicker_Timer |
| script.vbs:469 | Sub Popper_Hit |
| script.vbs:488 | Sub VUKTimer_Timer |
| script.vbs:607 | vpmMapLights AllLights |
| script.vbs:740 | for each obj in GIString1 |
| script.vbs:750 | for each obj in GIString1 |
| script.vbs:759 | for each obj in GIString2 |
| script.vbs:765 | for each obj in GIString2 |
| script.vbs:797 | Sub UpdateLightsTimer_Timer |
| script.vbs:798 | If controller.Lamp(85) = LightstateOff Then |
| script.vbs:863 | Sub Trigger6_Hit |
| script.vbs:868 | Sub RopePopperKicker_Timer |
| script.vbs:887 | Sub MagVUKTimer_Timer |
| script.vbs:908 | SolCallback(11)="SolRightArm" |
| script.vbs:909 | SolCallback(13)="SolLeftArm" |
| script.vbs:910 | SolCallback(26)="SolMotorDirc" |
| script.vbs:911 | SolCallback(27)="SolMotor" |
| script.vbs:931 | Sub BoxerTurnTimer_Timer |
| script.vbs:960 | Sub BRTimer_Timer |
| script.vbs:979 | Sub BLTimer_Timer |
| script.vbs:1055 | Sub Boxer_Wall_Hit |
| script.vbs:1060 | Sub Bag_Wall_Hit |
| script.vbs:1065 | Sub Boxer_Boxer_Hit |
| script.vbs:1071 | Sub Boxer_BoxerHead_Hit |
| script.vbs:1077 | Sub Boxer_Bag_Hit |
| script.vbs:1150 | Sub BoxerHit_Timer |
| script.vbs:1169 | Sub SpeedBag_Hit |
| script.vbs:1175 | Sub SpeedBagHit_Timer |
| script.vbs:1204 | Sub FistL_Timer |
| script.vbs:1215 | Sub FistR_Timer |
| script.vbs:1230 | sub FlipperMoveTimer_Timer() |
| script.vbs:1256 | Sub DiverterClosed_Hit |
| script.vbs:1263 | Sub DiverterClosed_Timer |
| script.vbs:1272 | Sub CatapultKicker_Hit:bsCatapult.addball Me:End Sub |
| script.vbs:1273 | Sub SW15_Hit:Controller.Switch(15)=1:LockWall1.isdropped = False:End Sub |
| script.vbs:1274 | Sub SW15_Unhit:Controller.Switch(15)=0:LockWall1.isdropped = True:End Sub |
| script.vbs:1275 | Sub SW57_Hit:Controller.Switch(57)=1:LockWall2.isdropped = False:End Sub |
| script.vbs:1276 | Sub SW57_Unhit:Controller.Switch(57)=0:LockWall2.isdropped = True:End Sub |
| script.vbs:1277 | Sub SW58_Hit:Controller.Switch(58)=1:End Sub |
| script.vbs:1278 | Sub SW58_Unhit:Controller.Switch(58)=0:End Sub |
| script.vbs:1281 | Sub LeftSlingshot_Slingshot |
| script.vbs:1290 | Sub LeftSlingShot_Timer |
| script.vbs:1297 | Sub RightSlingshot_Slingshot |
| script.vbs:1306 | Sub RightSlingShot_Timer |
| script.vbs:1314 | Sub Towel_Hit:Controller.Switch(63)=1:End Sub |
| script.vbs:1315 | Sub Towel_Unhit:Controller.Switch(63)=0:End Sub |
| script.vbs:1316 | Sub LeftOutlane_Hit:Controller.Switch(16)=1:End Sub |
| script.vbs:1317 | Sub LeftOutlane_unHit:Controller.Switch(16)=0:End Sub |
| script.vbs:1318 | Sub RightReturn_Hit:Controller.Switch(17)=1:End Sub |
| script.vbs:1319 | Sub RightReturn_unHit:Controller.Switch(17)=0:End Sub |
| script.vbs:1320 | Sub LeftReturn_Hit:Controller.Switch(26)=1:End Sub |
| script.vbs:1321 | Sub LeftReturn_unHit:Controller.Switch(26)=0:End Sub |
| script.vbs:1322 | Sub RightOutlane_Hit:Controller.Switch(27)=1:End Sub |
| script.vbs:1323 | Sub RightOutlane_unHit:Controller.Switch(27)=0:End Sub |
| script.vbs:1325 | Sub BehindLeftScoop_Hit:Controller.Switch(42)=1:End Sub |
| script.vbs:1326 | Sub BehindLeftScoop_Unhit:Controller.Switch(42)=0:End Sub |
| script.vbs:1327 | Sub BehindRightScoop_Hit:Controller.Switch(43)=1:End Sub |
| script.vbs:1328 | Sub BehindRightScoop_Unhit:Controller.Switch(43)=0:End Sub |
| script.vbs:1329 | Sub EnterRamp_Hit:Controller.Switch(44)=1:End Sub |
| script.vbs:1330 | Sub EnterRamp_Unhit:Controller.Switch(44)=0:End Sub |
| script.vbs:1332 | Sub EnterRope_Hit:Controller.Switch(78)=1:End Sub |
| script.vbs:1333 | Sub EnterRope_unHit:Controller.Switch(78)=0:End Sub |
| script.vbs:1334 | Sub ExitRope_Hit:Controller.Switch(71)=1:P_ExitRopeSwitchArm.Rotx=0:End Sub |
| script.vbs:1335 | Sub ExitRope_Unhit:Controller.Switch(71)=0:ExitRope.Timerenabled = True:End Sub |
| script.vbs:1337 | Sub ExitRope_Timer |
| script.vbs:1342 | Sub EnterLockup_Hit:Controller.Switch(74)=1:End Sub |
| script.vbs:1343 | Sub EnterLockup_unHit:Controller.Switch(74)=0:End Sub |
| script.vbs:1345 | Sub Drain_Hit:bsTrough.AddBall Me:Playsound "Drain5":End Sub |
| script.vbs:1347 | Sub RopePopper_Hit:Controller.Switch(45) = 1:set VUKball = activeball:End Sub |
| script.vbs:1348 | Sub CornerKickout_Hit:bsCornerKickout.AddBall 0:End Sub |
| script.vbs:1350 | Sub ThreeBankMid_Hit:vpmTimer.PulseSw 25:End Sub |
| script.vbs:1351 | Sub ThreeBankBottom_Hit:vpmTimer.PulseSw 53:End Sub |
| script.vbs:1352 | Sub ThreeBankTop_Hit:vpmTimer.PulseSw 54:End Sub |
| script.vbs:1355 | Sub LeftHalfGuy_Hit:vpmTimer.PulseSw 55:End Sub |
| script.vbs:1356 | Sub RightHalfGuy_Hit:vpmTimer.PulseSw 56:End Sub |
| script.vbs:1358 | Sub TopOfRamp_Hit:Controller.Switch(76)=1:End Sub |
| script.vbs:1359 | Sub TopOfRamp_Unhit:Controller.Switch(76)=0:End Sub |
| script.vbs:1361 | Sub EnterSpeedBag_Hit:Controller.Switch(72)=1:End Sub |
| script.vbs:1362 | Sub EnterSpeedBag_Unhit:Controller.Switch(72)=0:End Sub |
| script.vbs:1364 | Sub MadeRamp_Hit:Controller.Switch(11)=1:P_MadeRampArm.rotx = 0:End Sub |
| script.vbs:1365 | Sub MadeRamp_Unhit:Controller.Switch(11)=0:MadeRamp.Timerenabled = True:End Sub |
| script.vbs:1367 | Sub MadeRamp_Timer |
| script.vbs:1373 | Sub EnterLeftScoop_Hit |
| script.vbs:1377 | Sub EnterRightScoop_Hit |
| script.vbs:1381 | Sub LeftScoopGrab_Hit |
| script.vbs:1393 | Sub RightScoopGrab_Hit |
| script.vbs:1406 | Sub LeftJabMade_Hit:Controller.Switch(36)=1:End Sub |
| script.vbs:1407 | Sub LeftJabMade_Unhit:Controller.Switch(36)=0:End Sub |
| script.vbs:1409 | Sub RightJabMade_Hit:Controller.Switch(38)=1:End Sub |
| script.vbs:1410 | Sub RightJabMade_Unhit:Controller.Switch(38)=0:End Sub |
| script.vbs:1413 | Sub DangerZoneGate_Hit:vpmTimer.PulseSw 73:End Sub |
| script.vbs:1460 | Sub RollingTimer_Timer() |
| script.vbs:1534 | Sub Pins_Hit (idx) |
| script.vbs:1538 | Sub Targets_Hit (idx) |
| script.vbs:1542 | Sub Metals_Thin_Hit (idx) |
| script.vbs:1546 | Sub Metals_Medium_Hit (idx) |
| script.vbs:1550 | Sub Metals2_Hit (idx) |
| script.vbs:1554 | Sub Gates_Hit (idx) |
| script.vbs:1562 | Sub Rubbers_Hit(idx) |
| script.vbs:1573 | Sub Posts_Hit(idx) |
| script.vbs:1609 | Sub LWireRampStart1_hit |
| script.vbs:1613 | Sub LWireRampStart2_hit |
| script.vbs:1617 | Sub RWireRampStart_hit |
| script.vbs:89 | vpmTimer.PulseSw 31 |
| script.vbs:112 | Controller.Switch(61)=1 |
| script.vbs:122 | Controller.Switch(61)=0 |
| script.vbs:136 | Controller.Switch(62)=1 |
| script.vbs:146 | Controller.Switch(62)=0 |
| script.vbs:155 | Controller.Switch(75)=1 |
| script.vbs:160 | Controller.Switch(75)=0 |
| script.vbs:199 | if Controller.Switch(37) then |
| script.vbs:215 | if Controller.Switch(18) then |
| script.vbs:470 | Controller.Switch(28) = 1 |
| script.vbs:475 | If Controller.Switch(28) = True Then |
| script.vbs:477 | Controller.Switch(28) = 0 |
| script.vbs:617 | bsCatapult.InitKicker CatapultLaunchKicker,18,0,42,0 |
| script.vbs:625 | Set mRope=New cvpmMech |
| script.vbs:626 | mRope.MType=vpmMechOneSol+vpmMechCircle+vpmMechLinear+vpmMechFast |
| script.vbs:628 | mRope.Length=300 |
| script.vbs:629 | mRope.Steps=720 |
| script.vbs:633 | Set magRopeMagnet=New cvpmMagnet |
| script.vbs:634 | magRopeMagnet.InitMagnet TrigMagnet,39 |
| script.vbs:635 | magRopeMagnet.Solenoid=7 |
| script.vbs:640 | Controller.Switch(61)=1 |
| script.vbs:641 | Controller.Switch(62)=1 |
| script.vbs:642 | Controller.Switch(22)=1 |
| script.vbs:643 | vpmTimer.PulseSw 45 |
| script.vbs:715 | If keycode=PlungerKey Then Controller.Switch(23)=1 |
| script.vbs:720 | If keycode=PlungerKey Then Controller.Switch(23)=0 |
| script.vbs:841 | controller.switch(64) = 1 |
| script.vbs:843 | controller.switch(64) = 0 |
| script.vbs:847 | if controller.Switch(45) Then |
| script.vbs:850 | Controller.Switch(45) = 0 |
| script.vbs:854 | if controller.Switch(45) and ABS(BoxerZrot)<160 Then |
| script.vbs:858 | Controller.Switch(45) = 0 |
| script.vbs:877 | If Controller.Switch(45) = True Then |
| script.vbs:879 | Controller.Switch(45) = 0 |
| script.vbs:999 | Controller.Switch(46) = 1 |
| script.vbs:1007 | Controller.Switch(46) = 0 |
| script.vbs:1017 | Controller.Switch(41)=1 |
| script.vbs:1019 | Controller.Switch(41)=0 |
| script.vbs:1023 | Controller.Switch(47)=1 |
| script.vbs:1025 | Controller.Switch(47)=0 |
| script.vbs:1029 | Controller.Switch(48)=1 |
| script.vbs:1031 | Controller.Switch(48)=0 |
| script.vbs:1089 | vpmtimer.PulseSw 68 |
| script.vbs:1093 | vpmtimer.PulseSw 66 |
| script.vbs:1095 | vpmtimer.PulseSw 67 |
| script.vbs:1101 | vpmtimer.PulseSw 12 |
| script.vbs:1170 | vpmTimer.PulseSw 65 |
| script.vbs:1282 | vpmTimer.PulseSw 51 |
| script.vbs:1298 | vpmTimer.PulseSw 52 |

## AllLights

vpmMapLights AllLights is live at script.vbs:607. Retained installed companion core.vbs SHA-256 a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69, lines 2607–2621, sets idx=obj.TimerInterval unconditionally; object name is not the address. TimerEnabled=false does not disable the mapping. The full function is retained in companion-light-mapping.md.

| Public lamp | VPX Light | Same-address helpers |
| --- | --- | --- |
| 11 | Light11 | 1 |
| 12 | Light12 | 1 |
| 13 | Light13 | 1 |
| 14 | Light14 | 1 |
| 15 | Light15 | 1 |
| 16 | Light16 | 1 |
| 17 | Light17 | 1 |
| 18 | Light18 | 1 |
| 21 | Light21 | 1 |
| 22 | Light22 | 1 |
| 23 | Light23 | 1 |
| 24 | Light24 | 1 |
| 25 | Light25 | 1 |
| 26 | Light26 | 1 |
| 27 | Light27 | 1 |
| 28 | Light28 | 1 |
| 31 | Light31 | 1 |
| 33 | Light33 | 1 |
| 34 | Light34 | 1 |
| 35 | Light35 | 1 |
| 36 | Light36 | 1 |
| 37 | Light37 | 1 |
| 41 | Light41 | 1 |
| 42 | Light42 | 1 |
| 43 | Light43 | 1 |
| 44 | Light44 | 1 |
| 45 | Light45 | 1 |
| 46 | Light46 | 1 |
| 47 | Light47 | 1 |
| 48 | Light48 | 1 |
| 51 | Light51 | 4 |
| 51 | Light51_1 | 4 |
| 51 | Light51_2 | 4 |
| 51 | Light51_3 | 4 |
| 52 | Light52 | 1 |
| 53 | Light53 | 3 |
| 53 | Light53_1 | 3 |
| 53 | Light53_2 | 3 |
| 54 | Light54 | 2 |
| 54 | Light54_1 | 2 |
| 55 | Light55 | 3 |
| 55 | Light55_1 | 3 |
| 55 | Light55_2 | 3 |
| 56 | Light56 | 1 |
| 57 | Light57 | 1 |
| 58 | Light58 | 1 |
| 61 | Light61 | 1 |
| 62 | Light62 | 1 |
| 63 | Light63 | 1 |
| 64 | Light64 | 1 |
| 65 | Light65 | 1 |
| 66 | Light66 | 1 |
| 67 | Light67 | 1 |
| 68 | Light68 | 1 |
| 71 | Light71 | 1 |
| 72 | Light72 | 1 |
| 73 | Light73 | 1 |
| 74 | Light74 | 1 |
| 75 | Light75 | 1 |
| 76 | Light76 | 1 |
| 77 | Light77 | 1 |
| 78 | Light78 | 1 |
| 81 | Light81 | 1 |
| 82 | Light82 | 1 |
| 83 | Light83 | 1 |
| 84 | Light84 | 1 |
| 86 | Light86 | 1 |
| 91 | LED1 | 1 |
| 92 | LED2 | 1 |
| 93 | LED3 | 1 |
| 94 | LED4 | 1 |
| 95 | LED91 | 1 |
| 96 | LED92 | 1 |
| 97 | LED93 | 1 |
| 98 | LED94 | 1 |
| 100 | Bolt1 | 5 |
| 100 | Bolt2 | 5 |
| 100 | Flash17 | 5 |
| 100 | Flasher18 | 5 |
| 100 | Flasher18B | 5 |
| 101 | LED95 | 1 |
| 102 | LED96 | 1 |
| 103 | LED97 | 1 |
| 104 | LED98 | 1 |
| 111 | LED5 | 1 |
| 112 | LED6 | 1 |
| 113 | LED7 | 1 |
| 114 | LED8 | 1 |
| 115 | LED101 | 1 |
| 116 | LED102 | 1 |
| 117 | LED103 | 1 |
| 118 | LED104 | 1 |
| 121 | LED105 | 1 |
| 122 | LED106 | 1 |
| 123 | LED107 | 1 |
| 124 | LED108 | 1 |

Address 100 is a bound helper timer, outside the public lamp matrix; it is not an additional ROM lamp. Several insert addresses have multiple lightmap helpers, which are not extra physical bulbs. LED names LED91 etc are not their TimerInterval bindings.
