# Terminator 3 — controller bindings in the retained table's embedded script

Every non-comment line of the embedded script of `Terminator 3 (Stern 2003) Hanibal v1.5.vpx` (extracted `script.vbs`,
SHA-256 `33aaf9c0d4b89d15b57a0295f568f8fcce3381035f0749a9a0cd05981802e8b6`, 1666 lines) that names the controller, a ball stack,
drop target or impulse plunger, a switch write, a solenoid callback, a lamp, flasher or G.I. assignment, or a toy it
moves from a solenoid, quoted verbatim with its line number. Selected with one fixed case-insensitive pattern over the
whole file; whole-line comments are left out, trailing comments are kept, and trailing blanks are trimmed. Tabs are
kept as in the file. The script is read as Latin-1.

The pattern, as a Python regular expression:

```text
cGameName|LoadVPM|Const Use(Solenoids|Lamps|GI)\b|HandleMechanics|cvpm|\.Init(Sw|Kick|ImpulseP)\b|\.Balls\b|initdrop|TiltSwitch|AutoFire|Solcallback\(|controller\.switch\(|PulseSw|pulseswitch|\.addball|\.solout|soldropup|solhit|dtdroptarget\.hit|^\s*Sub (Sol\w*|Flash\d+|Auto_Plunger|kickit|GIUpdate|Kombi\w+)\b|Kickback\.(fire|pullback)|(LeftPost|CenterPost|bwdiverter1a?)\.isdropped|sol20timer\.enabled|Then kickit|Set GICallback|For each x in GIGruppe|x\.State = ABS|Set Lights\(|^\s*Kombi(flasher2?|licht) \d+|^\s*(Flasher(26|30|31|32)[a-d]|RPGFLASH\w*)\.State = 1|^\s*Flasher3\dp\d\.Image = \"DomeOn\"|^\s*b\.state = Helfer
```

```text
   20:  LoadVPM "01560000", "SEGA.VBS", 3.26
   22:  Const UseSolenoids = 1
   23:  Const UseLamps = 1
   24:  Const UseGI = 0
   50:  Dim cGameName
   52:  cGameName = "term3"
   54:   .GameName = cGameName
   60:  .HandleMechanics = 0
   62:  .Games(cGameName).Settings.Value("rol")=0
   63:  .Games(cGameName).Settings.Value("ror")=0
   72:  Set bsTrough = New cvpmBallStack
   74:  .InitSw 0, 14, 13, 12, 11, 0, 0, 0
   75:  .InitKick BallRelease, 45, 9
   78:  .Balls = 4
   83:   Set bsvuk=new cvpmballstack
   85:  .InitSw 0,36,0,0,0,0,0,0
   86:  .InitKick vukout,180,8
   92:  Set bstxhole=new cvpmballstack
   94:  .InitSw 0,33,34,35,0,0,0,0
   95:  .InitKick tvukout,180,12
  101:  Set dtdroptarget=new cvpmdroptarget
  102:  dtdroptarget.initdrop sw25,25
  183:  vpmNudge.TiltSwitch = 56
  189:  CenterPost.isdropped = 1
  190:  LeftPost.isdropped = 1
  191:  Bwdiverter1a.isdropped = 1
  193:  kickback.pullback
  212:  If keycode=plungerkey then controller.switch(55)=true
  213:  If keycode=keyfront then controller.switch(53)=true:end if
  234:  If keycode=plungerkey then controller.switch(55)=false
  235:  If keycode=keyfront then controller.switch(53)=false:end if
  241:  SolCallback(sLLFlipper) = "SolLeftFlippers"
  242:  SolCallback(sLRFlipper) = "SolRightFlippers"
  244:  Sub SolLeftFlippers(Enabled)
  248:  Sub SolRightFlippers(Enabled)
  252:  Sub SolFlipL(Flip, Enabled)
  262:  Sub SolFlipR(Flip, Enabled)
  274:  Sub LeftSlingShot_Slingshot:LS.IsDropped = 0:PlaySound "slingshotleft":vpmTimer.PulseSw 59:Me.TimerEnabled = 1:End Sub
  277:  Sub RightSlingShot_Slingshot:RS.IsDropped = 0:PlaySound "slingshotright":vpmTimer.PulseSw 62:Me.TimerEnabled = 1:End Sub
  282:  Sub Drain_Hit:Playsound "drain":bsTrough.AddBall Me:End Sub
  283:  Sub Drain2_Hit:Playsound "drain":bsTrough.AddBall Me:End Sub
  284:  Sub Drain1_Hit:Playsound "drain":bsTrough.AddBall Me:End Sub
  285:  Sub Drain4_Hit:Playsound "drain":bsTrough.AddBall Me:End Sub
  286:  Sub Drain3_Hit:Playsound "drain":bsTrough.AddBall Me:End Sub
  290:  Sub shooterlane_Hit():Controller.Switch(16) = 1:End Sub:Sub shooterlane_Unhit():Controller.Switch(16) = 0:End Sub
  294:  Set plungerIM = New cvpmImpulseP
  296:  .InitImpulseP swplunger, IMPowerSetting, IMTime
  302:  Sub Auto_Plunger(Enabled)
  304:  PlungerIM.AutoFire
  310:  Solcallback(1)  = "bstrough.solout"
  311:  Solcallback(2)  = "Auto_plunger"
  312:  Solcallback(3)  = "dtdroptarget.soldropup"
  313:  Solcallback(4)  = "Flash4"
  314:  Solcallback(5)  = "sol5" '5 backbox kicker
  315:  Solcallback(8)  = "dtdroptarget.solhit 1,"
  316:  Solcallback(12) = "sol12"
  317:  Solcallback(13) = "bsvuk.solout"
  318:  Solcallback(14) = "bstxhole.solout"
  319:  Solcallback(20) = "Sol20"
  320:  Solcallback(21) = "sol21"
  321:  Solcallback(22) = "sol22"
  322:  Solcallback(23) = "sol23"
  323:  Solcallback(26) = "Flash26"
  324:  Solcallback(27) = "Flash27"
  325:  Solcallback(28) = "Flash28"
  328:  Solcallback(29) = ""'"SetLamp 129,"
  329:  Solcallback(30) = "Flash30"
  330:  Solcallback(31) = "Flash31"
  331:  Solcallback(32) = "Flash32"
  360:  Sub sol20timer_timer()
  423:  Sub kickit()
  617:  Sub sw41_Hit:vpmTimer.PulseSw 41:PlaySound "target":End Sub
  619:  Sub sw42_Hit:vpmTimer.PulseSw 42:PlaySound "target":End Sub
  621:  Sub sw43_Hit:vpmTimer.PulseSw 43:PlaySound "target":End Sub
  623:  Sub sw44_Hit:vpmTimer.PulseSw 44:PlaySound "target":End Sub
  625:  Sub sw45_Hit:vpmTimer.PulseSw 45:PlaySound "target":End Sub
  627:  Sub sw41a_Hit:vpmTimer.PulseSw 41:PlaySound "target":End Sub
  629:  Sub sw42a_Hit:vpmTimer.PulseSw 42:PlaySound "target":End Sub
  631:  Sub sw43a_Hit:vpmTimer.PulseSw 43:PlaySound "target":End Sub
  633:  Sub sw44a_Hit:vpmTimer.PulseSw 44:PlaySound "target":End Sub
  635:  Sub sw45a_Hit:vpmTimer.PulseSw 45:PlaySound "target":End Sub
  767:  Sub Sol12(enabled)
  770:  Kickback.fire
  773:  Kickback.pullback
  780:  Sub Tophole_hit():bsvuk.addball me:end sub
  784:  Sub txshot_hit():vpmtimer.pulseswitch 31,0,0:bstxhole.addball me:Playsound "VUKEnter":End Sub
  785:  Sub txshota_hit():bstxhole.addball me:Playsound "VUKEnter":End Sub
  786:  Sub txshotb_hit():bstxhole.addball me:Playsound "VUKEnter":End Sub
  787:  Sub txshotc_hit():bstxhole.addball me:Playsound "VUKEnter":End Sub
  788:  Sub txshotd_hit():bstxhole.addball me:Playsound "VUKEnter":End Sub
  805:  Sub sol22(enabled)
  807:  LeftPost.isdropped = 0
  811:  LeftPost.isdropped = 1
  819:  Sub sol23(enabled)
  821:  CenterPost.isdropped = 0
  825:  CenterPost.isdropped = 1
  833:  Sub sol20(enabled)
  836:  sol20timer.enabled=true
  847:  sol20timer.enabled=false
  870:  Sub sol21(enabled)
  872:  bwdiverter1.isdropped = 1
  873:  bwdiverter1a.isdropped = 0
  876:  bwdiverter1.isdropped = 0
  877:  bwdiverter1a.isdropped = 1
  884:  Sub sol5(enabled)
  887:   If ballinbbk=true Then kickit
  912:  Sub LBumper_Hit:vpmTimer.PulseSw 49:PlaySound "BumperMiddle":Bumperlicht1.state = 1:Me.TimerEnabled = 1:End Sub
  917:  Sub RBumper_Hit:vpmTimer.PulseSw 50:PlaySound "BumperMiddle":Bumperlicht2.state = 1:Me.TimerEnabled = 1:End Sub
  921:  Sub BBumper_Hit:vpmTimer.PulseSw 51:PlaySound "BumperMiddle":Bumperlicht3.state = 1:Me.TimerEnabled = 1:End Sub
  928:  Sub sw24_Hit:Controller.Switch(24) = 1:PlaySound "sensor":End Sub
  929:  Sub sw24_Unhit:Controller.Switch(24) = 0:End Sub
  931:  Sub sw28_Hit:Controller.Switch(28) = 1:PlaySound "sensor":End Sub
  932:  Sub sw28_Unhit:Controller.Switch(28) = 0:End Sub
  934:  Sub sw29_Hit:Controller.Switch(29) = 1:PlaySound "sensor":End Sub
  935:  Sub sw29_Unhit:Controller.Switch(29) = 0:End Sub
  937:  Sub sw30_Hit:Controller.Switch(30) = 1:PlaySound "sensor":End Sub
  938:  Sub sw30_Unhit:Controller.Switch(30) = 0:End Sub
  940:  Sub sw32_Hit:Controller.Switch(32) = 1:PlaySound "sensor":End Sub
  941:  Sub sw32_Unhit:Controller.Switch(32) = 0:End Sub
  943:  Sub sw37_Hit:Controller.Switch(37) = 1:PlaySound "sensor":End Sub
  944:  Sub sw37_Unhit:Controller.Switch(37) = 0:End Sub
  946:  Sub sw38_Hit:Controller.Switch(38) = 1:PlaySound "sensor":End Sub
  947:  Sub sw38_Unhit:Controller.Switch(38) = 0:End Sub
  949:  Sub sw39_Hit:Controller.Switch(39) = 1:PlaySound "sensor":End Sub
  950:  Sub sw39_Unhit:Controller.Switch(39) = 0:End Sub
  952:  Sub sw40_Hit:Controller.Switch(40) = 1:PlaySound "sensor":End Sub
  953:  Sub sw40_Unhit:Controller.Switch(40) = 0:End Sub
  955:  Sub sw46_Hit:Controller.Switch(46) = 1:PlaySound "sensor":End Sub
  956:  Sub sw46_Unhit:Controller.Switch(46) = 0:End Sub
  958:  Sub sw52_Hit:Controller.Switch(52) = 1:PlaySound "sensor":End Sub
  959:  Sub sw52_Unhit:Controller.Switch(52) = 0:End Sub
  961:  Sub sw57_Hit:Controller.Switch(57) = 1:PlaySound "sensor":End Sub
  962:  Sub sw57_Unhit:Controller.Switch(57) = 0:End Sub
  964:  Sub sw58_Hit:Controller.Switch(58) = 1:PlaySound "sensor":End Sub
  965:  Sub sw58_Unhit:Controller.Switch(58) = 0:End Sub
  967:  Sub sw60_Hit:Controller.Switch(60) = 1:PlaySound "sensor":End Sub
  968:  Sub sw60_Unhit:Controller.Switch(60) = 0:End Sub
  970:  Sub sw61_Hit:Controller.Switch(61) = 1:PlaySound "sensor":End Sub
  971:  Sub sw61_Unhit:Controller.Switch(61) = 0:End Sub
  975:  Sub sw10_Hit:vpmTimer.PulseSw 10:PlaySound "target":End Sub
  978:  Sub sw17_Hit:vpmTimer.PulseSw 17:PlaySound "target":Switchlicht6.state = 1 :Me.TimerEnabled = 1:End Sub
  981:  Sub sw18_Hit:vpmTimer.PulseSw 18:PlaySound "target":Switchlicht5.state = 1 :Me.TimerEnabled = 1:End Sub
  984:  Sub sw19_Hit:vpmTimer.PulseSw 19:PlaySound "target":Switchlicht4.state = 1 :Me.TimerEnabled = 1:End Sub
  988:  Sub sw20_Hit:vpmTimer.PulseSw 20:PlaySound "target":Switchlicht1.state = 1 :Me.TimerEnabled = 1:End Sub
  991:  Sub sw21_Hit:vpmTimer.PulseSw 21:PlaySound "target":Switchlicht2.state = 1 :Me.TimerEnabled = 1:End Sub
  994:  Sub sw22_Hit:vpmTimer.PulseSw 22:PlaySound "target":Switchlicht3.state = 1 :Me.TimerEnabled = 1:End Sub
  997:  Sub sw23_Hit:vpmTimer.PulseSw 23:PlaySound "target":End Sub
  999:  Sub sw25_hit():dtdroptarget.hit 1:PlaySound "target":End sub
 1091: Sub Flash4(enabled)
 1093: 		RPGFLASH4.State = 1
 1094: 		RPGFLASH4a1.State = 1
 1095: 		RPGFLASH4a2.State = 1
 1096: 		RPGFLASH4a3.State = 1
 1097: 		RPGFLASH4a.State = 1
 1098: 		RPGFLASHeye.State = 1
 1110: Sub Flash26(enabled)
 1112: 		Flasher26a.State = 1
 1113: 		Flasher26b.State = 1
 1114: 		Flasher26c.State = 1
 1125: Sub Flash27(enabled)
 1127: 		RPGFLASH27a.State = 1
 1128: 		RPGFLASH27a1.State = 1
 1129: RPGFLASH27a2.State = 1
 1130: RPGFLASH27a3.State = 1
 1131: RPGFLASH27a4.State = 1
 1132: RPGFLASH27a5.State = 1
 1133: RPGFLASH27a6.State = 1
 1145: Sub Flash28(enabled)
 1147: 		RPGFLASH28a.State = 1
 1148: 		RPGFLASH28a1.State = 1
 1159: Sub Flash30(enabled)
 1161: 		Flasher30a.State = 1
 1163: 		Flasher30b.State = 1
 1165: 		Flasher30c.State = 1
 1167: 		Flasher30d.State = 1
 1170: 		Flasher30p1.Image = "DomeOn"
 1171: 		Flasher30p2.Image = "DomeOn"
 1172: 		Flasher30p3.Image = "DomeOn"
 1173: 		Flasher30p4.Image = "DomeOn"
 1193: Sub Flash31(enabled)
 1195: 		Flasher31a.State = 1
 1197: 		Flasher31b.State = 1
 1199: 		Flasher31p1.Image = "DomeOn"
 1200: 		Flasher31p2.Image = "DomeOn"
 1213: Sub Flash32(enabled)
 1215: 		Flasher32a.State = 1
 1217: 		Flasher32b.State = 1
 1219: 		Flasher32p1.Image = "DomeOn"
 1220: 		Flasher32p2.Image = "DomeOn"
 1239: Execute "Set Lights(" & i & ")  = L" & i
 1250: Set GICallback = GetRef("GIUpdate")
 1252: Sub GIUpdate(no, Enabled)
 1254:     For each x in GIGruppe
 1255:         x.State = ABS(Enabled)
 1267: Sub Kombiflasher(nr, a, object)
 1294: Sub Kombiflasher2(nr, a, object,b)
 1301: 	b.state = Helfer
 1320: Sub Kombilicht(nr, a, b)
 1327: 	b.state = Helfer
 1330: Sub Kombilichtb(nr, a, b)
 1337: 	b.state = Helfer
 1346: Kombiflasher 119, Flasher30a, Flasherr30a
 1347: Kombiflasher 120, Flasher30b, Flasherr30b
 1348: Kombiflasher 121, Flasher30c, Flasherr30c
 1349: Kombiflasher 122, Flasher30d, Flasherr30d
 1350: Kombiflasher 123, Flasher31a, Flasherr31a
 1351: Kombiflasher 124, Flasher31b, Flasherr31b
 1352: Kombiflasher 125, Flasher32a, Flasherr32a
 1353: Kombiflasher 126, Flasher32b, Flasherr32b
 1354: Kombiflasher 127, Flasher26a, Flasherr26a
 1355: Kombiflasher 137, Flasher26b, Flasherr26b
 1358: Kombiflasher 128, GL5, FlasherGLLED1
 1359: Kombiflasher 129, GL4, FlasherGLLED2
 1360: Kombiflasher 130, GL3, FlasherGLLED3
 1361: Kombiflasher 131, GL2, FlasherGLLED4
 1362: Kombiflasher 132, GL1, FlasherGLLED5
 1363: Kombiflasher 133, GL60, FlasherGLLED6
 1365: Kombiflasher 134, l71, FlasherTLicht
 1366: Kombiflasher 135, l64, FlasherTx1
 1367: Kombiflasher2 136, l64, FlasherTx2,l64a
 1370: Kombilicht 1, l1,l1a
 1371: Kombilicht 2, l2,l2a
 1372: Kombilicht 3, l3,l3a
 1373: Kombilicht 4, l4,l4a
 1374: Kombilicht 5, l5,l5a
 1375: Kombilicht 6, l6,l6a
 1376: Kombilicht 7, l7,l7a
 1377: Kombilicht 8, l8,l8a
 1378: Kombilicht 9, l9,l9a
 1379: Kombilicht 10, l10,l10a
 1380: Kombilicht 11, l11,l11a
 1381: Kombilicht 12, l12,l12a
 1382: Kombilicht 13, l13,l13a
 1383: Kombilicht 14, l14,l14a
 1384: Kombilicht 15, l15,l15a
 1385: Kombilicht 16, l16,l16a
 1386: Kombilicht 17, l17,l17a
 1387: Kombilicht 18, l18,l18a
 1388: Kombilicht 19, l19,l19a
 1389: Kombilicht 20, l20,l20a
 1390: Kombilicht 21, l21,l21a
 1391: Kombilicht 22, l22,l22a
 1392: Kombilicht 23, l23,l23a
 1393: Kombilicht 24, l24,l24a
 1394: Kombilicht 25, l25,l25a
 1395: Kombilicht 26, l26,l26a
 1396: Kombilicht 27, l27,l27a
 1397: Kombilicht 28, l28,l28a
 1398: Kombilicht 29, l29,l29a
 1399: Kombilicht 30, l30,l30a
 1400: Kombilicht 31, l31,l31a
 1401: Kombilicht 32, l32,l32a
 1402: Kombilicht 33, l33,l33a
 1403: Kombilicht 34, l34,l34a
 1404: Kombilicht 35, l35,l35a
 1405: Kombilicht 36, l36,l36a
 1406: Kombilicht 37, l37,l37a
 1407: Kombilicht 38, l38,l38a
 1408: Kombilicht 39, l39,l39a
 1409: Kombilicht 40, l40,l40a
 1410: Kombilicht 41, l41,l41a
 1411: Kombilicht 42, l42,l42a
 1412: Kombilicht 43, l43,l43a
 1413: Kombilicht 44, l44,l44a
 1414: Kombilicht 45, l45,l45a
 1415: Kombilicht 46, l46,l46a
 1416: Kombilicht 47, l47,l47a
 1417: Kombilicht 48, l48,l48a
 1418: Kombilicht 49, l49,l49a
 1419: Kombilicht 50, l50,l50a
 1420: Kombilicht 51, l51,l51a
 1421: Kombilicht 52, l52,l52a
 1422: Kombilicht 55, l55,l55a
 1423: Kombilicht 56, l56,l56a
 1424: Kombilicht 57, l57,l57a
 1425: Kombilicht 58, l58,l58a
 1426: Kombilicht 59, l59,l59a
 1427: Kombilicht 60, l60,l60a
 1428: Kombilicht 61, l61,l61a
 1429: Kombilicht 62, l62,l62a
 1431: Kombilicht 65, l65,l65a
 1432: Kombilicht 66, l66,l66a
 1433: Kombilicht 67, l67,l67a
 1434: Kombilicht 68, l68,l68a
 1435: Kombilicht 69, l69,l69a
 1438: Kombilicht 72, l72,l72a
 1447: Kombilicht 38, l38,l38a
 1448: Kombilicht 39, l39,l39a
 1449: Kombilicht 40, l40,l40a
 1453: Kombilicht 80, l80,l80a
```

## Curator's notes (not part of the script)

- `Const UseLamps = 1` makes core.vbs copy each changed lamp onto `Lights(n)`, and line 1239 binds `Lights(n)` to the
  table Light `L<n>` for 0-127; the `Flasherupdate` timer then copies each insert `l<n>` onto its bulb `l<n>a` with
  `Kombilicht` (lamps 1-52, 55-62, 65-69, 72 and 80; 38-40 twice) and drives the sprites of 64 and 71 with
  `Kombiflasher`/`Kombiflasher2`, which also copies `l64` onto `l64a`. No line copies lamps 53, 54, 63, 70 or 73-79.
- `Const UseGI = 0` does not unbind G.I.: core.vbs calls `GICallback` for every changed G.I. string whenever one is set,
  and line 1250 sets it to `GIUpdate`, which switches every member of the `GIGruppe` collection with G.I. 0.
- `Solcallback(29) = ""'"SetLamp 129,"` leaves flasher 29 unbound. Solenoids 6, 7, 9-11, 15-19, 24, 25 and 33-35 have
  no callback; the table fires its bumpers and slingshots from their own hit events, and core.vbs routes the flipper
  callbacks `sLLFlipper`/`sLRFlipper`.
- Switches 1-3, 7-9, 15, 26, 27, 47, 48, 63, 64, 81 and 83 are never written. sega.vbs writes the coin switches 4-6, the
  start button 54, the flipper buttons 82 and 84 and the coin-door buttons -3 to 0 from its key handlers; the table's own
  key handlers write 55 and 53, and `vpmNudge.TiltSwitch = 56` writes the tilt.
