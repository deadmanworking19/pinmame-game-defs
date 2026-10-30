# South Park — controller bindings in the retained table's embedded script

Every non-comment line of the embedded script of `South Park (Sega 1999) 1.3.vpx` (Knorr; extracted `script.vbs`, SHA-256
`63881ced8ea42097d1dee146ee2df7b752160dbd9f04bbfd826b90b513e408bf`) that names the controller, a ball stack or saucer, a switch write, a solenoid
callback, a lamp assignment, a flasher light it switches or a toy it animates from a solenoid, quoted verbatim with its
line number. Selected with a fixed pattern over the whole file; whole-line comments are left out, trailing comments kept.
Tabs are kept as in the file.

```text
   44: LoadVPM "01560000", "sega.VBS", 3.36
   50: Const cGameName = "sprk_103"
   51: Const UseSolenoids = 1
   52: Const UseLamps = 1
   89:         .GameName = cGameName
   90:         If Err Then MsgBox "Can't start Game " & cGameName & vbNewLine & Err.Description:Exit Sub
   91:         .Games(cGameName).Settings.Value("rol") = 0
   92:         .HandleKeyboard = 0
   96:         .HandleMechanics = 0
  107:         vpmNudge.TiltSwitch = swTilt
  108:         vpmNudge.Sensitivity = 2
  113:         .InitSw 0, 14, 13, 12, 11, 10, 0, 0
  114:         .InitKick BallRelease, 80, 5
  116:         .Balls = 5
  117:         .IsTrough = 1
  123: 		.InitSaucer sw46, 46, -90, 100
  132:         .InitSw 0, 45, 0, 0, 0, 0, 0, 0
  133:         .InitKick sw45, -80, 70
  157:         If bsTrough.Balls > 0 Then bsTrough.ExitSol_On
  168:     bsTrough.AddBall Me
  169:     If BallCount <1 then GiOff:GiOffState = True
  176: 		Plunger.Autoplunger = True
  177: 		Plunger.Fire
  178: 		PlaySound SoundFX("AutoPlunger", DOFContactors)
  180: 		Plunger.Autoplunger = False
  190: 	TopVuk.AddBall Me
  194: 	GiOn
  206:     vpmTimer.PulseSw 48
  207:     vpmTimer.AddTimer 1200, "SuperVukAddBall'"
  214:     vpmTimer.PulseSw 48
  215:     vpmTimer.AddTimer 1200, "SuperVukAddBall'"
  222:     vpmTimer.PulseSw 48
  223:     vpmTimer.AddTimer 1200, "SuperVukAddBall'"
  230:     vpmTimer.PulseSw 48
  231:     vpmTimer.AddTimer 1200, "SuperVukAddBall'"
  238:     vpmTimer.PulseSw 48
  239:     vpmTimer.AddTimer 1200, "SuperVukAddBall'"
  246:     vpmTimer.PulseSw 48
  247:     vpmTimer.AddTimer 1200, "SuperVukAddBall'"
  254:     vpmTimer.PulseSw 48
  255:     vpmTimer.AddTimer 1200, "SuperVukAddBall'"
  262:     vpmTimer.PulseSw 48
  263:     vpmTimer.AddTimer 1200, "SuperVukAddBall'"
  268: Sub SuperVukAddBall()
  269: 	SuperVuk.AddBall 1
  373: 		Kenny.RotZ = 0
  374: 		KennyL.RotZ = 0
  385: 		Kenny.RotZ = 0
  386: 		KennyL.RotZ = 0
  392: 		KennyFlipper.RotatetoEnd
  395: 		KennyFlipper.RotatetoStart
  401: 	    Kenny.RotX = KennyFlipper.CurrentAngle
  412: 	If KennySolLeft = True And Kenny.RotZ < 8 then Kenny.RotZ = Kenny.RotZ +1
  413: 	If KennysolLeft = False And Kenny.RotZ > 0 then Kenny.RotZ = Kenny.RotZ -1
  414: 	If Kenny.RotZ >= 8 Then KennySolLeft = False
  416: 	If KennySolLeft = True And KennyL.RotZ < 8 then KennyL.RotZ = KennyL.RotZ +1
  417: 	If KennysolLeft = False And KennyL.RotZ > 0 then KennyL.RotZ = KennyL.RotZ -1
  418: 	If KennyL.RotZ >= 8 Then KennySolLeft = False
  422: 	If KennySolRight = True And Kenny.RotZ > -8 then Kenny.RotZ = Kenny.RotZ -1
  423: 	If KennySolRight = False And Kenny.RotZ < 0 then Kenny.RotZ = Kenny.RotZ +1
  424: 	If Kenny.RotZ <= -8 Then KennySolRight = False
  426: 	If KennySolRight = True And KennyL.RotZ > -8 then KennyL.RotZ = KennyL.RotZ -1
  427: 	If KennySolRight = False And KennyL.RotZ < 0 then KennyL.RotZ = KennyL.RotZ +1
  428: 	If KennyL.RotZ <= -8 Then KennySolRight = False
  437:     vpmTimer.PulseSw 44
  438:     vpmTimer.AddTimer 2000, "SuperVukAddBall'"
  455: 	vpmTimer.PulseSw 44
  456:     vpmTimer.AddTimer 2000, "SuperVukAddBall'"
  474:     vpmTimer.PulseSw 44
  475:     vpmTimer.AddTimer 2000, "SuperVukAddBall'"
  492:     vpmTimer.PulseSw 44
  493:     vpmTimer.AddTimer 2000, "SuperVukAddBall'"
  511:     vpmTimer.PulseSw 44
  512:     vpmTimer.AddTimer 2000, "SuperVukAddBall'"
  530:     vpmTimer.PulseSw 44
  531:     vpmTimer.AddTimer 2000, "SuperVukAddBall'"
  560: 		ToiletFlipper.RotatetoEnd
  561: 		ToiletKicker.Enabled = True
  564: 		ToiletFlipper.RotatetoStart
  565: 		ToiletKicker.Enabled = False
  574: 	MrHankeyFlipper.RotatetoEnd
  575: 	CisternFlipper.RotatetoEnd
  584: 	MrHankeyFlipper.RotatetoStart
  585: 	CisternFlipper.RotatetoStart
  597:     vpmTimer.PulseSw 43
  598:     vpmTimer.AddTimer 2400, "SuperVukAddBall'"
  601: 		vpmTimer.AddTimer 2400, "GiOff'"
  603: 		vpmTimer.AddTimer 2400, "GiOn'"
  741: SolCallback(1) = "SolRelease"
  742: SolCallback(2) = "AutoLaunch"
  743: SolCallback(3) = "SuperVuk.SolOut"
  744: SolCallback(4) = "TopVuk.SolOut"
  745: SolCallback(5) = "ToiletSeatLid"
  746: SolCallback(6) = "MrHankeyUp"
  747: SolCallback(13) = "MrHankeyDown"
  748: SolCallBack(14) = "KennyDead"
  749: SolCallBack(19) = "KennyLeft"
  750: SolCallback(20) = "KennyRight"
  761:         vpmTimer.PulseSw vpmNudge.TiltSwitch
  769:     If keycode = PlungerKey Then Plunger.Fire: PlaySound "Plunger"
  778: SolCallback(sLRFlipper) = "SolRFlipper"
  779: SolCallback(sLLFlipper) = "SolLFlipper"
  783:         PlaySound SoundFX("FlipperUpLeft", DOFFlippers):FlipperLeft.RotateToEnd
  785:         PlaySound SoundFX("FlipperDown", DOFFlippers):FlipperLeft.RotateToStart
  791:         PlaySound SoundFX("FlipperUpRightBoth", DOFFlippers):FlipperRight.RotateToEnd
  793:         PlaySound SoundFX("FlipperDown", DOFFlippers):FlipperRight.RotateToStart
  802: Sub sw16_Hit:Controller.Switch(16) = 1:sw16wire.RotX = 15:PlaySound "metalhit_thin":End Sub 'shooterlane'
  803: Sub sw16_UnHit:Controller.Switch(16) = 0:sw16wire.RotX = 0:GiOn:End Sub
  805: Sub sw25_Hit:Controller.Switch(25) = 1:End Sub
  806: Sub sw25_UnHit:Controller.Switch(25) = 0: End Sub
  808: Sub sw26_Hit:Controller.Switch(26) = 1: sw26spinner.timerenabled = True:End Sub
  809: Sub sw26_UnHit:Controller.Switch(26) = 0: End Sub
  815: 	if Ballcount > 0 then GiOn
  820: Sub sw42_Hit: Controller.Switch(42) = 1:ActiveBall.VelZ = 0: End Sub
  821: Sub sw42_UnHit: Controller.Switch(42) = 0: End Sub
  824: Sub sw47_Hit:Controller.Switch(47) = 1:sw47wire.RotX = 15:PlaySound "metalhit_thin":End Sub 'left orbit'
  825: Sub sw47_UnHit:Controller.Switch(47) = 0:sw47wire.RotX = 0:End Sub
  827: Sub sw57_Hit:Controller.Switch(57) = 1:GiOff:sw57wire.RotX = 15:PlaySound "metalhit_thin":End Sub 'left outlane'
  828: Sub sw57_UnHit:Controller.Switch(57) = 0:GiOn::sw57wire.RotX = 0:End Sub
  830: Sub sw58_Hit:Controller.Switch(58) = 1:sw58wire.RotX = 15:sw26spinner.timerenabled = False:PlaySound "metalhit_thin":End Sub 'left inlane'
  831: Sub sw58_UnHit:Controller.Switch(58) = 0:sw58wire.RotX = 0:End Sub
  833: Sub sw60_Hit:Controller.Switch(60) = 1:GiOff:sw60wire.RotX = 15:PlaySound "metalhit_thin":End Sub 'right outlane'
  834: Sub sw60_UnHit:Controller.Switch(60) = 0:GiOn:sw60wire.RotX = 0:End Sub
  836: Sub sw61_Hit:Controller.Switch(61) = 1:sw61wire.RotX = 15:PlaySound "metalhit_thin":End Sub 'right inlane'
  837: Sub sw61_UnHit:Controller.Switch(61) = 0:sw61wire.RotX = 0:End Sub
  844: Sub T17_Hit:vpmTimer.PulseSw 17: DTGrandpa.RotX = DTGrandpa.RotX +5:Playsound SoundFX("target", DOFTargets):Me.TimerEnabled = 1:End Sub
  846: Sub T18_Hit:vpmTimer.PulseSw 18: DTMsCartman.RotX = DTMsCartman.RotX +5:Playsound SoundFX("target", DOFTargets):Me.TimerEnabled = 1:End Sub
  848: Sub T19_Hit:vpmTimer.PulseSw 19: DTMayor.RotX = DTMayor.RotX +5:Playsound SoundFX("target", DOFTargets):Me.TimerEnabled = 1:End Sub
  850: Sub T20_Hit:vpmTimer.PulseSw 20: DTBarbrady.RotX = DTBarbrady.RotX +5:Playsound SoundFX("target", DOFTargets):Me.TimerEnabled = 1:End Sub
  852: Sub T21_Hit:vpmTimer.PulseSw 21: DTHugo.RotX = DTHugo.RotX +5:Playsound SoundFX("target", DOFTargets):Me.TimerEnabled = 1:End Sub
  856: Sub T22_Hit:vpmTimer.PulseSw 22: DTJ.RotX = DTJ.RotX +5:Playsound SoundFX("target", DOFTargets):Me.TimerEnabled = 1:End Sub
  858: Sub T23_Hit:vpmTimer.PulseSw 23: DTSirJohn.RotX = DTSirJohn.RotX +5:Playsound SoundFX("target", DOFTargets):Me.TimerEnabled = 1:End Sub
  860: Sub T24_Hit:vpmTimer.PulseSw 24: DTH.RotX = DTH.RotX +5:Playsound SoundFX("target", DOFTargets):Me.TimerEnabled = 1:End Sub
  864: Sub T34_Hit:vpmTimer.PulseSw 34: DTWendy.RotX = DTWendy.RotX +5:Playsound SoundFX("target", DOFTargets):Me.TimerEnabled = 1:End Sub
  866: Sub T35_Hit:vpmTimer.PulseSw 35: DTMrGarrison.RotX = DTMrGarrison.RotX +5:Playsound SoundFX("target", DOFTargets):Me.TimerEnabled = 1:End Sub
  868: Sub T36_Hit:vpmTimer.PulseSw 36: DTMrMackey.RotX = DTMrMackey.RotX +5:Playsound SoundFX("target", DOFTargets):Me.TimerEnabled = 1:End Sub
  872: Sub T37_Hit:vpmTimer.PulseSw 37: DTNed.RotX = DTNed.RotX +5:Playsound SoundFX("target", DOFTargets):Me.TimerEnabled = 1:End Sub
  874: Sub T38_Hit:vpmTimer.PulseSw 38: DTMephisto.RotX = DTMephisto.RotX +5:Playsound SoundFX("target", DOFTargets):Me.TimerEnabled = 1:End Sub
  894: Sub LeftBumper_hit:vpmTimer.pulseSw 49:Playsound SoundFX("BumperLeft", DOFContactors):Me.TimerEnabled = 1:End Sub
  897: Sub RightBumper_hit:vpmTimer.pulseSw 50:Playsound SoundFX("BumperMiddle", DOFContactors):Me.TimerEnabled = 1:End Sub
  900: Sub BottomBumper_hit:vpmTimer.pulseSw 51:Playsound SoundFX("BumperRight", DOFContactors):Me.TimerEnabled = 1:End Sub
  919:     vpmTimer.PulseSw 62
  937:     vpmTimer.PulseSw 59
  960:     Set Lights(1) = l1
  961:     Set Lights(2) = l2
  962:     Set Lights(3) = l3
  963:     Set Lights(4) = l4
  964:     Set Lights(5) = l5
  965:     Set Lights(6) = l6
  966:     Set Lights(7) = l7
  967:     Set Lights(8) = l8
  968:     Set Lights(9) = l9
  969:     Set Lights(10) = l10
  970:     Set Lights(11) = l11
  971:     Set Lights(12) = l12
  972:     Set Lights(13) = l13
  973:     Set Lights(14) = l14
  974:     Set Lights(15) = l15
  975:     Set Lights(16) = l16
  976:     Set Lights(17) = l17
  977:     Set Lights(18) = l18
  978:     Set Lights(19) = l19
  979:     Set Lights(20) = l20
  980:     Set Lights(21) = l21
  981:     Set Lights(22) = l22
  982:     Set Lights(23) = l23
  983:     Set Lights(24) = l24
  984:     Set Lights(25) = l25
  985:     Set Lights(26) = l26
  986:     Set Lights(27) = l27
  987:     Set Lights(28) = l28
  988:     Set Lights(29) = l29
  989:     Set Lights(30) = l30
  990:     Set Lights(33) = l33
  991:     Set Lights(34) = l34
  992:     Set Lights(35) = l35
  993:     Set Lights(36) = l36
  994:     Set Lights(37) = l37
  995:     Set Lights(38) = l38
  996:     Set Lights(39) = l39
  997:     Set Lights(40) = l40
  998:     Set Lights(41) = l41
  999:     Set Lights(42) = l42
 1000:     Set Lights(43) = l43
 1001:     Set Lights(44) = l44
 1002:     Set Lights(45) = l45
 1003:     Set Lights(46) = l46
 1004:     Set Lights(48) = l48
 1005:     Set Lights(50) = l50
 1006:     Set Lights(51) = l51
 1007:     Set Lights(52) = l52
 1008:     Set Lights(53) = l53
 1009:     Set Lights(54) = l54
 1010:     Set Lights(55) = l55
 1011:     Set Lights(56) = l56
 1012:     Set Lights(57) = l57
 1013:     Set Lights(58) = l58
 1014:     Set Lights(59) = l59
 1015:     Set Lights(60) = l60
 1016:     Set Lights(61) = l61
 1017:     Set Lights(62) = l62
 1018:     Set Lights(63) = l63
 1019:     Set Lights(64) = l64
 1098: Sub GIOff()
 1109: Sub GIOn()
 1200: SolCallback(7) = "FlashPops"
 1201: SolCallback(18) = "FlashTopVuk"
 1202: SolCallback(25) = "FlashStan"
 1203: SolCallback(26) = "FlashChef"
 1204: SolCallback(27) = "FlashKenny"
 1205: SolCallback(28) = "FlashKyle"
 1206: SolCallback(29) = "FlashCartman"
 1207: SolCallback(30) = "FlashKennyAndBack"
 1208: SolCallback(31) = "FlashMrHankeyToilet"
 1209: SolCallback(32) = "FlashSuperVuk"
 1218: 	F7l.State = 1
 1219: 	F7r.State = 1
 1227: 	F7l.State = 0
 1228: 	F7r.State = 0
 1236: 	F1.State = 1
 1237: 	F1a.State = 1
 1239: 	F1.State = 0
 1240: 	F1a.State = 0
 1246: 	F2.State = 1
 1247: 	F2a.State = 1
 1249: 	F2.State = 0
 1250: 	F2a.State = 0
 1256: 	F3.State = 1
 1257: 	F3a.State = 1
 1259: 	F3.State = 0
 1260: 	F3a.State = 0
 1266: 	F4.State = 1
 1267: 	F4a.State = 1
 1269: 	F4.State = 0
 1270: 	F4a.State = 0
 1276: 	F5.State = 1
 1277: 	F5a.State = 1
 1279: 	F5.State = 0
 1280: 	F5a.State = 0
 1286: 	F8.State = 1
 1291: 	F8.State = 0
 1294: 	If Ballcount > 0 And BallinToilet = 0 then GiOn
 1300: 	FPa.State = 1
 1301: 	FPb.State = 1
 1302: 	FPc.State = 1
 1303: 	FPd.State = 1
 1307: 	FPa.State = 0
 1308: 	FPb.State = 0
 1309: 	FPc.State = 0
 1310: 	FPd.State = 0
 1318: 	F6b.State = 1
 1326: 	F6b.State = 0
 1338: 	F18.State = 1
 1344: 	F18.State = 0
 1348: 	If BallCount > 0 And BallinToilet = 0 then GiOn
 1444: 	GiOn
```
