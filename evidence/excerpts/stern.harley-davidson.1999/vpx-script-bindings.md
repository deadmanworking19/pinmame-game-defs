# Harley-Davidson (Stern) — controller bindings in the retained table's embedded script

Every non-comment line of the embedded script of `Harley Davidson (Sega 1999) 1.2.vpx` (table description "VPX Conversion
by: Goldchicco & 32assassin", version 1.2; extracted `script.vbs`, SHA-256
`eb0960bc9670cd367f7f2ce838e2969d4546b98abe5c8fc4d4df3fd53d32bc50`, byte-identical to the sidecar `.vbs` retained beside the table) that names the controller, a
ball stack, drop-target bank, magnet or mech, a switch write, a solenoid callback, a lamp or flasher assignment, or a toy
it moves from a solenoid, quoted verbatim with its line number. Selected with a fixed pattern over the whole file;
whole-line comments are left out, trailing comments kept. Tabs are kept as in the file.

```text
    9: Const cGameName="harl_a30",UseSolenoids=2,UseLamps=0,UseSync=1,UseGI=0,sCoin="coin3"
   11: LoadVPM "01200000","SEGA.VBS",3.1
   18: SolCallback(1)="bsTrough.SolOut"
   19: SolCallback(2)="bsLaunch.SolOut"
   20: SolCallback(3)="bsSVUK.SolOut"
   21: SolCallback(4)="bsScoop.SolOut"
   22: SolCallback(5)="bsCycle.SolOut"
   23: SolCallback(6)="dtL.SolDropUp"
   24: SolCallback(7)="dtR.SolDropUp"
   29: SolCallback(13)="SolShake"
   35: SolCallback(20)="SetLamp 120," 'Flash Scoop x1
   36: SolCallback(23)="SolPost"
   37: SolCallBack(25)="SetLamp 101,"	'Left drop target X2
   38: SolCallBack(26)="SetLamp 102,"	'Ramp Left X2 Flashers
   39: SolCallBack(27)="SetLamp 103," 	'Turbo Bumper X4
   40: SolCallBack(28)="SetLamp 104," 	'Ramp Top X2 Flashers
   41: SolCallBack(29)="SetLamp 105,"  '"MotoFlash" 	'Motorcycle X4
   42: SolCallBack(30)="SetLamp 106," 	'Super VUK X2
   43: SolCallBack(31)="SetLamp 107," 	'Right Drop Target X2
   44: SolCallBack(32)="SetLamp 108," 	'Speedometer X2
   46: SolCallback(sLRFlipper) = "SolRFlipper"
   47: SolCallback(sLLFlipper) = "SolLFlipper"
   49: Sub SolLFlipper(Enabled)
   51:          PlaySound SoundFX("FlipperupLeft",DOFFlippers):LeftFlipper.RotateToEnd
   53:          PlaySound SoundFX("FlipperdownLeft",DOFFlippers):LeftFlipper.RotateToStart
   57: Sub SolRFlipper(Enabled)
   59:          PlaySound SoundFX("FlipperupRight",DOFFlippers):RightFlipper.RotateToEnd
   61:          PlaySound SoundFX("FlipperdownRight",DOFFlippers):RightFlipper.RotateToStart
   70: Sub SolTrough(Enabled)
   73: 			bsTrough.ExitSol_On
   74: 			vpmTimer.PulseSw 15
   80:  Sub SolShake(Enabled)
   95:  Sub SolPost(Enabled)
   97: 		Wall32.IsDropped=0
  100: 		Wall32.IsDropped=1
  107: Sub PFGI(Enabled)
  111: 		For each xx in GI:xx.State = 0: Next
  115: 		For each xx in GI:xx.State = 1: Next
  131: 		.GameName = cGameName
  132: 		If Err Then MsgBox "Can't start Game" & cGameName & vbNewLine & Err.Description : Exit Sub
  134: 		.HandleMechanics=0
  140:         .Games(cGameName).Settings.Value("sound")=1
  152:    	    vpmNudge.TiltSwitch=14
  153:     	vpmNudge.Sensitivity=1
  156: 		bsTrough.InitSw 0,14,13,12,11,0,0,0
  157: 		bsTrough.InitKick BallRelease,110,5
  159: 		bsTrough.Balls=4
  162: 		bsCycle.InitSw 0,44,43,42,41,0,0,0
  163: 		bsCycle.InitKick Kicker1,180,5
  167: 		bsScoop.InitSw 0,46,0,0,0,0,0,0
  168: 		bsScoop.InitKick sw46,175,20
  172: 	bsLaunch.InitSaucer Kicker2,16,0,44
  176: 		bsSVUK.InitSw 0,45,0,0,0,0,0,0
  177: 		bsSVUK.InitKick sw45a,105,7
  181: 		dtL.InitDrop Array(sw17,sw18,sw19,sw20),Array(17,18,19,20)
  185: 		dtR.InitDrop Array(sw21,sw22,sw23,sw24),Array(21,22,23,24)
  189: 		mMagnet.InitMagnet MagTrig,75
  190: 		mMagnet.Solenoid=14
  196: 		mCycle.Sol1=19
  197: 		mCycle.Length=100
  198: 		mCycle.Steps=25
  199: 		mCycle.mType=vpmMechOneSol+vpmMechReverse+vpmMechLinear
  200: 		mCycle.AddSw 35,24,24
  201: 		mCycle.AddSw 36,0,0
  202: 		mCycle.Callback=GetRef("UpdateCycle")
  205: 		Wall32.IsDropped=1
  215: 	If KeyCode=PlungerKey Then Controller.Switch(53)=1
  216: 	If KeyCode=LeftMagnaSave Then Controller.Switch(8)=1
  217: 	If KeyCode=RightMagnaSave Then Controller.Switch(8)=1
  218: 	If KeyCode=KeyUpperRight Then Controller.Switch(8)=1
  219: 	If KeyCode=KeyUpperLeft Then Controller.Switch(8)=1
  225: 	If KeyCode=PlungerKey Then Controller.Switch(53)=0
  226: 	If KeyCode=LeftMagnaSave Then Controller.Switch(8)=0
  227: 	If KeyCode=RightMagnaSave Then Controller.Switch(8)=0
  228: 	If KeyCode=KeyUpperRight Then Controller.Switch(8)=0
  229: 	If KeyCode=KeyUpperLeft Then Controller.Switch(8)=0
  237: Sub Drain_Hit:bsTrough.AddBall Me: playsound "drain" : End Sub
  238: Sub Kicker2_Hit:bsLaunch.AddBall 0:End Sub
  239: Sub Kicker1_Hit:bsCycle.AddBall Me:playsound "scoopenter":End Sub
  240: Sub sw46_Hit:bsScoop.AddBall Me:playsound "scoopenter":End Sub
  241: Sub Sw45_Hit:bsSVUK.AddBall Me:playsound "kicker_enter left":End Sub
  246: 		bsSVUK.ExitSol_On
  251:  Sub Sw17_Dropped:dtL.Hit 1 :End Sub
  252:  Sub Sw18_Dropped:dtL.Hit 2 :End Sub
  253:  Sub Sw19_Dropped:dtL.Hit 3 :End Sub
  254:  Sub Sw20_Dropped:dtL.Hit 4 :End Sub
  256:  Sub Sw21_Dropped:dtR.Hit 1 :End Sub
  257:  Sub Sw22_Dropped:dtR.Hit 2 :End Sub
  258:  Sub Sw23_Dropped:dtR.Hit 3 :End Sub
  259:  Sub Sw24_Dropped:dtR.Hit 4 :End Sub
  262: Sub sw25_hit:PlaySound "gate":Controller.Switch(25)=1:End Sub
  263: Sub sw25_unhit:Controller.Switch(25)=0:End Sub
  264: Sub trigger26_hit:PlaySound "gate":Controller.Switch(26)=1:End Sub
  265: Sub trigger26_unhit:Controller.Switch(26)=0:End Sub
  266: Sub trigger27_hit:PlaySound "gate":Controller.Switch(27)=1:End Sub
  267: Sub trigger27_unhit:Controller.Switch(27)=0:End Sub
  271: Sub sw33_hit:Controller.Switch(33)=1:Playsound "sensor":End Sub
  272: Sub sw33_unhit:Controller.Switch(33)=0:End Sub
  273: Sub sw34_hit:Controller.Switch(34)=1:Playsound "sensor":End Sub
  274: Sub sw34_unhit:Controller.Switch(34)=0:End Sub
  275: Sub sw48_hit:Controller.Switch(48)=1:End Sub
  276: Sub sw48_unhit:Controller.Switch(48)=0:End Sub
  277: Sub sw57_hit:Controller.Switch(57)=1:Playsound "sensor":End Sub
  278: Sub sw57_unhit:Controller.Switch(57)=0:End Sub
  279: Sub sw58_hit:Controller.Switch(58)=1:Playsound "sensor":End Sub
  280: Sub sw58_unhit:Controller.Switch(58)=0:End Sub
  281: Sub sw60_hit:Controller.Switch(60)=1:Playsound "sensor":End Sub
  282: Sub sw60_unhit:Controller.Switch(60)=0:End Sub
  283: Sub sw61_hit:Controller.Switch(61)=1:Playsound "sensor":End Sub
  284: Sub sw61_unhit:Controller.Switch(61)=0:End Sub
  287: Sub Spinner1_Spin:PlaySound "gate":vpmTimer.PulseSwitch(28),0,"" end sub
  290: Sub sw29_hit:vpmTimer.pulseSw 29 : End Sub
  291: Sub sw30_hit:vpmTimer.pulseSw 30 : End Sub
  292: Sub sw31_hit:vpmTimer.pulseSw 31 : End Sub
  293: Sub sw32_hit:vpmTimer.pulseSw 32 : End Sub
  296: Sub Bumper1b_Hit:vpmTimer.pulseSW 51 : PlayBumperSound : End Sub
  297: Sub Bumper2b_Hit:vpmTimer.pulseSW 49 : PlayBumperSound : End Sub
  298: Sub Bumper3b_Hit:vpmTimer.pulseSW 50 : PlayBumperSound : End Sub
  299: Sub Bumper4b_Hit:vpmTimer.pulseSW 52 : PlayBumperSound : End Sub
  316: Sub sw37_Hit
  317: 	If Status=0 Then vpmtimer.pulsesw 37
  320: Sub UpdateCycle(aNewPos,aSpeed,aLastPos)
  322: 	Wall40.IsDropped=0
  323: 	Else Wall40.IsDropped=1
  326: 	If anewPos <25 Then: P3.ObjRotX = anewpos/2
  327: 	If aNewPos <25 Then: Platform.ObjRotX = anewpos/2
  328: 	If aNewPos <25 Then: PlatPost.ObjRotX = anewpos/2
  331: Sub Wall40_Hit(): ShakeBike:playsound SoundFXDOF("fx_shaker",102,DOFPulse,DOFShaker):End Sub
  412: 	NFadeL 1, l1
  413: 	NFadeL 2, l2
  414: 	NFadeL 3, l3
  415: 	NFadeL 4, l4
  416: 	NFadeL 5, l5
  417: 	NFadeL 6, l6
  418: 	NFadeL 7, l7
  419: 	NFadeL 8, l8
  420: 	NFadeL 9, l9
  421: 	NFadeL 10, l10
  422: 	NFadeL 11, l11
  423: 	NFadeL 12, l12
  424: NFadeL 13, l13
  425: NFadeL 14, l14
  426: NFadeL 15, l15
  427: NFadeL 16, l16
  428: NFadeL 17, l17
  429: NFadeL 18, l18
  430: NFadeL 19, l19
  431: NFadeL 20, l20
  432: NFadeL 21, l21
  433: NFadeL 22, l22
  434: 	NFadeL 23, l23
  435: 	NFadeL 24, l24
  436:     NFadeL 25, l25
  437:     NFadeL 26, l26
  438:     NFadeL 27, l27
  439:     NFadeLm 28, l28   'Bumper
  440: 	Flash 28, F28
  441:     NFadeLm 29, l29   'Bumper
  442: 	Flash 29, F29
  443:     NFadeLm 30, l30   'Bumper
  444: 	Flash 30, F30
  445:     NFadeLm 31, l31   'Bumper
  446: 	Flash 31, F31
  447:     NFadeL 32, l32
  448:     NFadeL 33, l33
  449:     NFadeL 34, l34
  450:     NFadeL 35, l35
  451:     NFadeL 36, l36
  452:     NFadeL 37, l37
  453: 	NFadeL 38, l38
  454:     NFadeL 39, l39
  455:     NFadeL 40, l40
  456:     NFadeL 41, l41
  457:     NFadeL 42, l42
  458:     NFadeL 43, l43
  459:     NFadeL 44, l44
  460:     NFadeL 45, l45
  461:     NFadeL 46, l46
  463: 	NFadeL 48, l48
  464:     NFadeL 49, l49
  465:     NFadeL 50, l50
  466:     NFadeL 51, l51
  468: 	Flash 57, F57   'Traffic Light Green
  469: 	Flash 58, F58   'Traffic Light Yellow
  470: 	Flash 59, F59   'Traffic Light Red
  472:     NFadeL 65, l65
  473:     NFadeL 66, l66
  474: 	NFadeL 67, l67
  475:     NFadeL 68, l68
  476: 	NFadeL 69, l69
  477:     NFadeLm 70, l70
  478:     NFadeLm 70, l70a
  479:     NFadeL 71, l71
  480: 	Flashm 72, F72a 'Scoop LED
  481: 	Flash 72, F72
  488: 	Flashm 101, F101a
  489: 	Flash 101, F101
  491:     NFadeLm 102, L102
  492:     NFadeLm 102, L102a
  494: 	Flashm 102, F102b
  496: 	Flashm 103, F103a
  497: 	Flashm 103, F103b
  498: 	Flash 103, F103
  500:     NFadeLm 104, L104
  501:     NFadeLm 104, L104a
  502: 	Flashm 104, F104b
  504: 	Flashm 105, F105a
  505: 	Flashm 105, F105b
  506: 	Flashm 105, F105c
  507: 	Flash 105, F105
  509: 	Flashm 106, F106a
  510: 	Flash 106, F106
  511: 	Flashm 106, L106c
  512: 	Flashm 106, L106d
  513: 	Flashm 106, L106e
  514: 	Flashm 106, L106f
  515: 	Flashm 106, L106g
  516: 	Flashm 106, L106h
  517: 	Flashm 106, L106i
  519: 	Flashm 107, F107a
  520: 	Flash 107, F107
  522: 	Flashm 108, F108a
  523: 	Flash 108, F108
  558: Sub NFadeL(nr, object)
  565: Sub NFadeLm(nr, object) ' used for multiple lights
  640: 	vpmTimer.PulseSw 62
  659: 	vpmTimer.PulseSw 59
```

Commented-out bindings the selection leaves out, summarized: lines 25-28 comment out SolCallback(9) to (12)
(`vpmSolSound ""jet3""`, the bumpers), line 30 reads `'SolCallback(14)=magnet`, lines 32-33 comment out SolCallback(17)
and (18) (`vpmSolSound ""Sling""`), line 34 reads `'SolCallback(19)="SolCycle" 'Shake Bike`, line 462 `'NFadeL 47, l47`
and line 486 `'NFadeL 120, F120`.

Observations on these lines (not part of the script):

- `vpmNudge.TiltSwitch=14` (line 152) names the trough VUK opto's address; sega.vbs defines `swTilt = 56`.
- `SolTrough`, the only writer of 15, is never bound (SolCallback(1) is `bsTrough.SolOut`), so 15 is never written.
- `Status` (line 317) is declared and never assigned, so every `sw37_Hit` pulses 37.
- `PFGI` is defined but no callback binds it; the G.I. lights stay as the table set them.
- SolCallback(20) sets lamp 120, but its only fader, `NFadeL 120, F120`, is commented out, so flasher 20 draws nothing.
- Switch 47 is never written, and matrix lamp 47 (the cabinet launch-button lamp) is commented out.
