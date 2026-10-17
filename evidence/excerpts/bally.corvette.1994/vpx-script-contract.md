# Corvette - retained known-working table script, runtime contract

Source: the script embedded in the retained table `Corvette (Bally 1994).vpx` (version 1.4.2 by Goldchicco, 32assassin and Mussinger; table SHA-256 `4b500c6b33b280b0076e49b2e817fad2d1131095efeb57fd58bd160b7d8a010c`), extracted with vpxtool 0.33.3 as `script.vbs` (3605 lines, SHA-256 `d30534b6664ed214a3c8b33597ab1021bcc66e979363611e218d4fccb35e5bb5`). The blocks below quote its lines verbatim with their 1-based line numbers (CRLF line ends and trailing whitespace dropped, leading tabs kept); lines between the blocks are sound, lighting-effect and option code the definition does not rely on. The script itself is not redistributed.

## Controller and library

Lines 10-11:

```
  10  Const BallMass=1
  11  Const cGameName="corv_21",UseSolenoids=2,UseLamps=0, SCoin="coin", UseVPMDMD=True
```

Line 30:

```
  30  LoadVPM "01560000", "WPC.VBS", 3.26
```

## Solenoid callback table

Lines 40-76:

```
  40
  41  '********************
  42  'Solenoids Call backs
  43  '********************
  44  SolCallback(1) = "solTrough"
  45  SolCallback(2) = "SolLGate"
  46  SolCallback(3) = "SolKickback"
  47  SolCallback(4) = "bsL.SolOut"
  48  SolCallback(5) = "SolGateU"
  49  '6 Not Used
  50  SolCallback(8) = "bsR.SolOut"
  51  'SolCallback(9)="vpmSolSound ""Sling"","
  52  'SolCallback(10)="vpmSolSound ""Sling"","
  53  'SolCallback(11)="vpmSolSound ""Jet3"","
  54  'SolCallback(12)="vpmSolSound ""Jet3"","
  55  'SolCallback(13)="vpmSolSound ""Jet3"","
  56  '14 Not Used
  57  SolCallback(15) ="bsLock.SolOut"
  58  SolCallback(16) ="SolTGate"
  59  SolCallback(17) ="SetLamp 117," 'motor controller and Flasher
  60  SolCallback(18) ="SetLamp 118," 'motor controller
  61  SolCallback(19) ="SetLamp 119," 'motor controller
  62  SolCallback(20) ="SetLamp 120," 'Backglass Only
  63  SolCallback(21) ="SetLamp 121,"
  64  SolCallback(22) ="SetLamp 122,"
  65  SolCallback(23) ="SetLamp 123,"
  66  SolCallback(24) ="SetLamp 124,"
  67  SolCallback(25) ="SetLamp 125,"
  68  SolCallback(26) ="SolEngine" 'motor controller and flasher
  69  SolCallback(27) ="SetLamp 127,"
  70  SolCallback(28) ="SetLamp 128,"
  71
  72  'SolCallback(33) =
  73  SolCallback(34) = "SolDiv"
  74
  75  SolCallback(sLRFlipper) = "SolRFlipper"
  76  SolCallback(sLLFlipper) = "SolLFlipper"
```

## Flipper, trough, gate, kickback, engine and diverter callbacks

Lines 90-225:

```
  90  Sub SolLFlipper(Enabled)
  91  			If Enabled Then
  92  				LF.Fire
  93  		If leftflipper.currentangle < leftflipper.endangle + ReflipAngle Then
  94  			RandomSoundReflipUpLeft LeftFlipper
  95  		Else
  96  			SoundFlipperUpAttackLeft LeftFlipper
  97  			RandomSoundFlipperUpLeft LeftFlipper
  98              LeftFlipper1.RotateToEnd
  99  		End If
 100  	Else
 101  		LeftFlipper.RotateToStart
 102          LeftFlipper1.RotateToStart
 103  		If LeftFlipper.currentangle < LeftFlipper.startAngle - 5 Then
 104  			RandomSoundFlipperDownLeft LeftFlipper
 105  		End If
 106  		FlipperLeftHitParm = FlipperUpSoundLevel
 107  	End If
 108  End Sub
 109
 110  Sub SolRFlipper(Enabled)
 111  			If Enabled Then
 112  				RF.Fire
 113  		If rightflipper.currentangle > rightflipper.endangle - ReflipAngle Then
 114  			RandomSoundReflipUpRight RightFlipper
 115  		Else
 116  			SoundFlipperUpAttackRight RightFlipper
 117  			RandomSoundFlipperUpRight RightFlipper
 118  		End If
 119  	Else
 120  		RightFlipper.RotateToStart
 121  		If RightFlipper.currentangle > RightFlipper.startAngle + 5 Then
 122  			RandomSoundFlipperDownRight RightFlipper
 123  		End If
 124  		FlipperRightHitParm = FlipperUpSoundLevel
 125  	End If
 126  End Sub
 127
 128  '**********************************************************************************************************
 129
 130  'Solenoid Controlled toys
 131  '**********************************************************************************************************
 132
 133  Sub solTrough(Enabled)
 134  	If Enabled Then
 135  		bsTrough.ExitSol_On
 136  		vpmTimer.PulseSw 37
 137  	End If
 138   End Sub
 139
 140  Sub SolLGate(Enabled) 'Lock Gate 1
 141  	If Enabled Then
 142  		Lgate.open = 0
 143  		Wall12.IsDropped=0
 144          PlaySound SoundFX("",DOFContactors)
 145  	Else
 146  		Lgate.Open = 1
 147  		Wall12.IsDropped=1
 148       End If
 149   End Sub
 150
 151  Sub SolKickBack(Enabled)
 152  	If Enabled Then
 153  		KickBack.Fire
 154  		PlaySound SoundFX("WareHouseKick",DOFContactors)
 155  	Else
 156  		KickBack.PullBack
 157  	End if
 158  End Sub
 159
 160  Sub SolGateU(Enabled) 'Lock Gate 2
 161  	If Enabled Then
 162  		GateU.Open = 1
 163  		PlaySound SoundFX("",DOFContactors)
 164
 165  	Else
 166  		GateU.Open = 0
 167  	End If
 168  End Sub
 169
 170  Sub SolTGate(Enabled)
 171  	If Enabled Then
 172  		TGate.Open = 1
 173  		PlaySound SoundFX("",DOFContactors)
 174  	Else
 175  		TGate.Open = 0
 176  	End if
 177  End Sub
 178
 179  Sub SolEngine(Enabled)
 180  		SetLamp 126, Enabled
 181
 182  If EngineTol<100 Then
 183  	Magnet1.Enabled=1
 184  	Magnet2.Enabled=1
 185  	Magnet3.Enabled=1
 186  	Magnet4.Enabled=1
 187  Else
 188  	Magnet1.Enabled=0
 189  	Magnet2.Enabled=0
 190  	Magnet3.Enabled=0
 191  	Magnet4.Enabled=0
 192  End If
 193
 194      If Enabled then
 195          EngineP.RotY = EngineP.RotY + 5
 196          EngineP001.RotY = EngineP001.RotY + 5
 197  ' Thalamus
 198  		PlaySoundAtVol "fx_rampbump1", EngineP, EngineVol
 199      Else
 200         EngineP.RotY = EngineP.RotY - 5
 201         EngineP001.RotY = EngineP001.RotY - 5
 202  ' Thalamus
 203  		PlaySoundAtVol "fx_rampbump1", EngineP, EngineVol
 204  	End If
 205  End Sub
 206
 207
 208  Sub SolDiv(Enabled)
 209      If Enabled Then
 210  		PlaySound SoundFX("Diverter",DOFContactors)
 211  		DiverterOFF.IsDropped = 1
 212  		DiverterON.IsDropped = 0
 213  		DivFlipper.RotateToEnd
 214      Else
 215  		PlaySound SoundFX("Diverter",DOFContactors)
 216  		DiverterOFF.IsDropped = 0
 217  		DiverterON.IsDropped = 1
 218  		DivFlipper.RotateToStart
 219      End If
 220  End Sub
 221
 222
 223  '*****************************************
 224  '      		General Illumination  for Bally/Williams String GI
 225  '*****************************************
```

## General illumination

Lines 227-298:

```
 227  Set GiCallBack2 = GetRef("UpdateGi")
 228
 229  Sub UpdateGi(nr,step)
 230  	Dim xx
 231
 232  	If step > 0 Then
 233  		DOF 101, DOFOn
 234  	Else
 235  		DOF 101, DOFOff
 236  	End If
 237
 238  	Select Case nr
 239  	Case 0
 240  		If step=0 Then
 241  			'GI1 OFF
 242  			For each xx in GI1:xx.State = 0: Next
 243  			Sound_GI_Relay 0, sw36a 'selected this locatiom at randon because it's central
 244  '			PinCab_Backglass.image = "Corvette Dark"
 245  		Else
 246  			'GI1 ON
 247  			For each xx in GI1:xx.State = 1: Next
 248  			Sound_GI_Relay 1, sw36a 'selected this locatiom at randon because it's central
 249  '			PinCab_Backglass.image = "Corvette Illuminated"
 250  		End If
 251  	Case 1
 252  		If step=0 Then
 253  			'GI2 OFF
 254  			For each xx in GI2:xx.State = 0: Next
 255  			Sound_GI_Relay 0, sw36a 'selected this locatiom at randon because it's central
 256  '			PinCab_Backglass.image = "Corvette Dark"
 257  		Else
 258  			'GI2 ON
 259  			For each xx in GI2:xx.State = 1: Next
 260  			Sound_GI_Relay 1, sw36a 'selected this locatiom at randon because it's central
 261  '			PinCab_Backglass.image = "Corvette Illuminated"
 262  		End If
 263
 264  	Case 2
 265  		If step=0 Then
 266  			'GI3 OFF
 267  			For each xx in GI3:xx.State = 0: Next
 268  			Sound_GI_Relay 0, sw36a 'selected this locatiom at randon because it's central
 269  '			PinCab_Backglass.image = "Corvette Dark"
 270  		Else
 271  			'GI3 ON
 272  			For each xx in GI3:xx.State = 1: Next
 273  			Sound_GI_Relay 1, sw36a 'selected this locatiom at randon because it's central
 274  '			PinCab_Backglass.image = "Corvette Illuminated"
 275  		End If
 276
 277  	Case 3
 278  		If step=0 Then
 279  			'GI4 OFF
 280  			For each xx in GI4:xx.State = 0: Next
 281  			Sound_GI_Relay 0, sw36a 'selected this locatiom at randon because it's central
 282  '			PinCab_Backglass.image = "Corvette Dark"
 283  		Else
 284  			'GI4 ON
 285  			For each xx in GI4:xx.State = 1: Next
 286  			Sound_GI_Relay 1, sw36a 'selected this locatiom at randon because it's central
 287  '			PinCab_Backglass.image = "Corvette Illuminated"
 288  		End If
 289
 290  	'Case 4		'GI5  is Backglass Only
 291
 292  	End Select
 293
 294  End Sub
 295
 296
 297
 298
```

## Table init: controller settings, ball stacks and the engine magnets

Lines 302-396:

```
 302  Dim bsTrough, bsR, bsL, bsLock, Mag1, Mag2, Mag3, Mag4, ApronImg
 303
 304  ApronImg=1
 305  Wall12.IsDropped=1
 306
 307  Sub Table1_Init
 308  	vpmInit Me
 309  	On Error Resume Next
 310  		With Controller
 311  		.GameName = cGameName
 312  		If Err Then MsgBox "Can't start Game" & cGameName & vbNewLine & Err.Description : Exit Sub
 313  		.SplashInfoLine = "Corvette Bally 1994"&chr(13)&"You Suck"
 314  		.HandleMechanics=0
 315  		.HandleKeyboard=0
 316  		.ShowDMDOnly=1
 317  		.ShowFrame=0
 318  		.ShowTitle=0
 319  		.hidden = 0
 320          .HandleMechanics = 7
 321          .Games(cGameName).Settings.Value("sound")=1
 322  		'.PuPHide = 1
 323           On Error Resume Next
 324           .Run GetPlayerHWnd
 325           If Err Then MsgBox Err.Description
 326           On Error Goto 0
 327          .Switch(22) = 1
 328          .Switch(24) = 1
 329       End With
 330       On Error Goto 0
 331
 332  	PinMAMETimer.Interval = PinMAMEInterval
 333  	PinMAMETimer.Enabled = 1
 334
 335      	vpmNudge.TiltSwitch=14
 336      	vpmNudge.Sensitivity=1
 337      	vpmNudge.TiltObj=Array(Bumper1,Bumper2,Bumper3,LeftSlingshot,RightSlingshot)
 338
 339  '**Trough
 340      Set bsTrough = New cvpmBallStack
 341      bsTrough.InitSw 0,31,32,33,34,0,0,0
 342      bsTrough.InitKick BallRelease, 90, 4
 343      bsTrough.InitExitSnd SoundFX("Ballrelease1",DOFContactors), SoundFX("Solenoid",DOFContactors)
 344      bsTrough.Balls = 4
 345
 346  '**Route 66 Kicker
 347  	Set bsR = New cvpmBallStack
 348          bsR.InitSw 0, 57, 0, 0, 0, 0, 0, 0
 349          bsR.InitKick sw57, 270, 24
 350          bsR.InitExitSnd SoundFX("",DOFContactors), SoundFX("Solenoid",DOFContactors)
 351          bsR.KickForceVar = 3
 352
 353  '**Pit Stop
 354  	Set bsL = New cvpmBallStack
 355          bsL.InitSw 0, 36, 0, 0, 0, 0, 0, 0
 356          bsL.InitKick sw36, 235, 5
 357          bsL.InitExitSnd SoundFX("WareHouseKick",DOFContactors), SoundFX("Solenoid",DOFContactors)
 358          bsL.KickForceVar = 3
 359
 360  '**ZR1 Lock
 361  	Set bsLock=New cvpmBallStack
 362  		bsLock.InitSw 0,76,77,78,0,0,0,0
 363  		bsLock.InitKick Kicker3,235,1
 364  		bsLock.InitExitSnd SoundFX("WareHouseKick",DOFContactors), SoundFX("Solenoid",DOFContactors)
 365  		bsLock.Balls=0
 366
 367  	Set mag1= New cvpmMagnet
 368  		mag1.InitMagnet Magnet1, 60
 369  		mag1.GrabCenter = False
 370   		mag1.solenoid=26
 371  		mag1.CreateEvents "mag1"
 372
 373  	Set mag2= New cvpmMagnet
 374   	With mag2
 375  		.InitMagnet Magnet2, 60
 376  		.GrabCenter = False
 377   		.solenoid=26
 378  		.CreateEvents "mag2"
 379  	End With
 380
 381  	Set mag3= New cvpmMagnet
 382   	With mag3
 383  	.InitMagnet Magnet3, 60
 384  		.GrabCenter = False
 385   		.solenoid=26
 386  		.CreateEvents "mag3"
 387  	End With
 388
 389  	Set mag4= New cvpmMagnet
 390   	With mag4
 391  		.InitMagnet Magnet4, 60
 392  		.GrabCenter = False
 393   		.solenoid=26
 394  		.CreateEvents "mag4"
 395  	End With
 396
```

## Engine magnet disarm

Lines 402-416:

```
 402
 403  Sub EngTol_Timer
 404  If EngineTol>100 Then
 405  mag1.solenoid=0
 406  mag2.solenoid=0
 407  mag3.solenoid=0
 408  mag4.solenoid=0
 409  else
 410  mag1.solenoid=26
 411  mag2.solenoid=26
 412  mag3.solenoid=26
 413  mag4.solenoid=26
 414  End If
 415
 416  'PinCab_Backglass.BlendDisableLighting = 1.3
```

## Kickers that add balls to the ball stacks

Lines 486-491:

```
 486  Sub sw57a_Hit::SoundSaucerLock:bsR.AddBall Me:End Sub
 487  Sub sw57_Hit()::SoundSaucerLock:bsL.AddBall Me:End Sub
 488  Sub sw36a_Hit: :RandomSoundDelayedBallDropOnPlayfield sw36a:bsL.AddBall Me:End Sub
 489  Sub Kicker3_Hit():::SoundSaucerLock:bsR.AddBall Me:End Sub
 490  Sub Kicker1_Hit::SoundSaucerLock:bsLock.AddBall Me:End Sub
 491  Sub ApronTimer_Timer
```

## Switch events

Lines 501-583:

```
 501  '**********************************
 502  'Switches
 503  '**********************************
 504  'Wire Triggers
 505    Sub sw11_Hit:Controller.Switch(11) = 1:RandomSoundRollover:End Sub
 506    Sub sw11_UnHit:Controller.Switch(11) = 0:End Sub
 507    Sub sw12_Hit:Controller.Switch(12) = 1:RandomSoundRollover:End Sub
 508    Sub sw12_UnHit:Controller.Switch(12) = 0:End Sub
 509    Sub sw15_Hit:Controller.Switch(15) = 1:RandomSoundRollover:End Sub
 510    Sub sw15_UnHit:Controller.Switch(15) = 0:End Sub
 511    Sub sw16_Hit:Controller.Switch(16) = 1:RandomSoundRollover:End Sub
 512    Sub sw16_UnHit:Controller.Switch(16) = 0:End Sub
 513    Sub sw17_Hit:Controller.Switch(17) = 1:RandomSoundRollover:End Sub
 514    Sub sw17_UnHit:Controller.Switch(17) = 0:End Sub
 515    Sub sw38_Hit:Controller.Switch(38) = 1:RandomSoundRollover:End Sub
 516    Sub sw38_UnHit:Controller.Switch(38) = 0:End Sub
 517    Sub sw66_Hit:Controller.Switch(66) = 1:RandomSoundRollover:End Sub
 518    Sub sw66_UnHit:Controller.Switch(66) = 0:End Sub
 519    Sub sw67_Hit:Controller.Switch(67) = 1:RandomSoundRollover:End Sub
 520    Sub sw67_UnHit:Controller.Switch(67) = 0:End Sub
 521    Sub sw68_Hit:Controller.Switch(68) = 1:RandomSoundRollover:End Sub
 522    Sub sw68_UnHit:Controller.Switch(68) = 0:End Sub
 523    Sub sw87_Hit:Controller.Switch(87) = 1:RandomSoundRollover:End Sub
 524    Sub sw87_UnHit:Controller.Switch(87) = 0:End Sub
 525    Sub sw88_Hit:Controller.Switch(88) = 1:RandomSoundRollover:End Sub
 526    Sub sw88_UnHit:Controller.Switch(88) = 0:End Sub
 527    Sub sw71_Hit:Controller.Switch(71) = 1:PlaySound "fx_rampbump1":EngineTol=EngineTol+1:End Sub
 528    Sub sw71_UnHit:Controller.Switch(71) = 0:End Sub
 529    Sub sw72_Hit:Controller.Switch(72) = 1:PlaySound "fx_rampbump1":EngineTol=EngineTol+1:End Sub
 530    Sub sw72_UnHit:Controller.Switch(72) = 0:End Sub
 531
 532  'Spinners
 533  Sub sw18_Spin:vpmTimer.PulseSw 18 : SoundSpinner sw18 : End Sub
 534
 535  '********* Stand Up Target ***********
 536  Sub sw46_Hit:vpmTimer.PulseSw 46: End Sub
 537  Sub sw47_Hit:vpmTimer.PulseSw 47: End Sub
 538  Sub sw48_Hit:vpmTimer.PulseSw 48: End Sub
 539  Sub sw83_Hit:vpmTimer.PulseSw 83: End Sub
 540  Sub sw81_Hit:vpmTimer.PulseSw 81: End Sub
 541  Sub sw82_Hit:vpmTimer.PulseSw 82 :End Sub
 542
 543  'RAMP SWITCHES *********************************
 544   Sub sw35_Hit:Controller.Switch(35) = 1:End Sub
 545   Sub sw35_unHit:Controller.Switch(35)=0:End Sub
 546   Sub sw43_Hit:Controller.Switch(43) = 1:End Sub
 547   Sub sw43_unHit:Controller.Switch(43)=0:End Sub
 548   Sub sw44_Hit:vpmTimer.PulseSw 44:End Sub
 549   Sub sw45_Hit:vpmTimer.PulseSw 45:End Sub
 550   'Sub sw58_Hit:vpmTimer.PulseSw 58:PlaySound "fx_metalrolling":End Sub
 551   Sub sw75_Hit:vpmTimer.PulseSw 75:End Sub
 552
 553  'Optical Triggers
 554   Sub sw41_Hit
 555      If ActiveBall.VelY < 0 Then   ' going up the table
 556          WireRampOn True           ' plastic
 557      Else
 558          WireRampOff               ' coming from above, treat as exit
 559      End If
 560  Controller.Switch(41) = 1
 561  	EngineTol=0
 562  	Magnet1.Enabled=1
 563  	Magnet2.Enabled=1
 564  	Magnet3.Enabled=1
 565  	Magnet4.Enabled=1
 566  	Magnet5.Enabled=1
 567  End Sub
 568
 569   Sub sw41_unHit:Controller.Switch(41)=0:End Sub
 570   Sub sw42_Hit:Controller.Switch(42) = 1:End Sub
 571   Sub sw42_unHit:Controller.Switch(42)=0:End Sub
 572   Sub sw58_Hit:Controller.Switch(58) = 1:End Sub
 573   Sub sw58_unHit:Controller.Switch(58)=0:End Sub
 574  '51
 575  '52
 576  '55
 577  '56
 578  '71
 579  '72
 580
 581  'Scoring rubber
 582  Sub sw84_Hit:vpmTimer.PulseSw 84:End Sub
 583  Sub sw86_Hit:vpmTimer.PulseSw 86:End Sub
```

## Race car animation from GetMech(0) and GetMech(1)

Lines 603-676:

```
 603  Dim EP,NewEP,RedCarPos,BlueCarPos,NewRedCarPos,NewBlueCarPos,RedPercentDownTrack,BluePercentDownTrack,MechNoMovement
 604  Dim BlueCarXStart, BlueCarYStart, BlueCarZStart, RedCarXStart, RedCarYStart, RedCarZStart
 605  Const MechCarStart 		= 0
 606  Const MechCarFinish 	= 675
 607  Const MechTimerFast		= 15
 608  Const MechTimerSlow		= 100
 609
 610  Const BlueCarXFinish 	= 878
 611  Const BlueCarYFinish 	= 117
 612  Const BlueCarZFinish 	= 275
 613  Const RedCarXFinish 	= 936
 614  Const RedCarYFinish 	= 117
 615  Const RedCarZFinish 	= 275
 616
 617  Dim bluecarlast, redcarlast
 618
 619  BlueCarXStart = BlueCar.X
 620  BlueCarYStart = BlueCar.Y
 621  BlueCarZStart = BlueCar.Z
 622  RedCarXStart = RedCar.X
 623  RedCarYStart = RedCar.Y
 624  RedCarZStart = RedCar.Z
 625
 626
 627  Sub Mech_Timer
 628      NewBlueCarPos=Controller.GetMech(0)
 629      NewRedCarPos=Controller.GetMech(1)
 630
 631  	'If Cars not moving slow down timer
 632  	If (NewBlueCarPos = BlueCarPos) and (NewRedCarPos = RedCarPos) and (Mech.Interval <> MechTimerSlow) Then
 633  		If MechNoMovement > 10 Then
 634  			Mech.Interval = MechTimerSlow
 635  		Else
 636  			MechNoMovement = MechNoMovement + 1
 637  		End If
 638
 639  	Else
 640  		If NewBlueCarPos <> BlueCarPos Then
 641  			BlueCarPos = NewBlueCarPos
 642  			BluePercentDownTrack = NewBlueCarPos/(MechCarFinish - MechCarStart)
 643  			BlueCar.Z = BlueCarZStart - (BlueCarZStart - BlueCarZFinish) * BluePercentDownTrack
 644  			BlueCar.Y = BlueCarYStart - (BlueCarYStart - BlueCarYFinish) * BluePercentDownTrack
 645  			BlueCar.X = BlueCarXStart - (BlueCarXStart - BlueCarXFinish) * BluePercentDownTrack
 646
 647   ' Thalamus
 648   		If ( ( bluecar.y > 117 ) and ( bluecar.y < 1421 ) and ( bluecarlast <> bluecar.y ) ) Then
 649  			PlaySoundAtVol "electric_motor", BlueCar, CarVolume
 650  			bluecarlast = bluecar.y
 651  		End if
 652  		debug.print bluecar.y
 653
 654  			'Speed Up Timer when car in motion
 655  			If Mech.Interval <>  MechTimerFast Then Mech.Interval = MechTimerFast
 656  		End If
 657
 658  		If NewRedCarPos <> RedCarPos Then
 659  			RedCarPos = NewRedCarPos
 660  			RedPercentDownTrack = NewRedCarPos/(MechCarFinish - MechCarStart)
 661  			RedCar.Z = RedCarZStart - (RedCarZStart - RedCarZFinish) * RedPercentDownTrack
 662  			RedCar.Y = RedCarYStart - (RedCarYStart - RedCarYFinish) * RedPercentDownTrack
 663  			RedCar.X = RedCarXStart - (RedCarXStart - RedCarXFinish) * RedPercentDownTrack
 664
 665   ' Thalamus
 666    		if ( ( redcar.y > 117 ) and ( redcar.y < 1422 ) and ( redcarlast <> redcar.y ) ) Then
 667  			PlaySoundAtVol "electric_motor", RedCar, CarVolume
 668  			redcarlast = redcar.y
 669  		end if
 670
 671  			'Speed Up Timer when car in motion
 672  			If Mech.Interval <>  MechTimerFast Then Mech.Interval = MechTimerFast
 673  		End If
 674  		MechNoMovement = 0
 675  	End If
 676  End Sub
```

## Engine angle from GetMech(2) and the lamp bindings

Lines 713-833:

```
 713  Dim engnew, difeng, enghold
 714
 715  Sub UpdateLamps()
 716      LFLogo.RotY = LeftFlipper.CurrentAngle-210
 717      LFLogo1.RotY = LeftFlipper1.CurrentAngle-210
 718      RFlogo.RotY = RightFlipper.CurrentAngle+30
 719
 720
 721
 722   	engnew=Controller.getmech(2)
 723  	difeng=abs(enghold-engnew)
 724  	if difeng < 30 then
 725  		EngineP.objRoty=(engnew-127)/7
 726  		EngineP001.objRoty=(engnew-127)/7
 727  		enghold=engnew
 728  	end If
 729
 730
 731      NFadeL 1, L1    'Bumper1
 732      NFadeL 2, L2    'Bumper2
 733      NFadeL 3, L3    'Bumper3
 734
 735      NFadeL 11, l11
 736      NFadeL 12, l12
 737      NFadeL 13, l13
 738      NFadeL 14, l14
 739      NFadeL 15, l15
 740      NFadeL 16, l16
 741      NFadeL 17, l17
 742      NFadeL 18, l18
 743
 744
 745      NFadeL 21, l21
 746      NFadeL 22, l22
 747      NFadeL 23, l23
 748      NFadeL 24, l24
 749      NFadeL 25, l25
 750      NFadeL 26, l26
 751      NFadeL 27, l27
 752      NFadeL 28, l28
 753
 754
 755      NFadeL 31, l31
 756      NFadeL 32, l32
 757      NFadeL 33, l33
 758      NFadeL 34, l34
 759      NFadeL 35, l35
 760      NFadeL 36, l36
 761      NFadeL 37, l37
 762      NFadeL 38, l38
 763
 764
 765      NFadeL 41, l41
 766      NFadeL 42, l42
 767      NFadeL 43, l43
 768      NFadeL 44, l44
 769      NFadeL 45, l45
 770      NFadeL 46, l46
 771      NFadeL 47, l47
 772      NFadeL 48, l48
 773
 774
 775      NFadeL 51, l51
 776      NFadeL 52, l52
 777      Flash 53, f53
 778      NFadeL 54, l54
 779      NFadeL 55, l55
 780      NFadeL 56, l56
 781      NFadeL 57, l57
 782      NFadeL 58, l58
 783
 784
 785      NFadeL 61, l61
 786      NFadeL 62, l62
 787      NFadeL 63, l63
 788      NFadeL 64, l64
 789      NFadeL 65, l65
 790      NFadeL 66, l66
 791      NFadeL 67, l67
 792      Flash 68, f68
 793
 794
 795      NFadeL 71, l71
 796      NFadeL 72, l72
 797      NFadeL 73, l73
 798      NFadeL 74, l74
 799      NFadeL 75, l75
 800      Flash 76, f76
 801      Flash 77, f77
 802      Flash 78, f78
 803
 804
 805      Flash 81, f81
 806      Flash 82, f82
 807      Flashm 83, f83a
 808      Flash 83, f83
 809      Flashm 84, f84a
 810      Flash 84, f84
 811      Flash 85, f85
 812      Flash 86, f86
 813
 814  'Solenid Controlled Lamps
 815  'NFadeL 117,  L117  'Not Shown in the Service Manual No clue where it goes
 816  Flashm 118, Flasher118
 817  Flash 118, Flasher118a
 818  Flashm 119, Flasher119
 819  Flash 119, Flasher119a
 820  NFadeL 120,  L120 'Backglass Only
 821
 822  NFadeL 121,  L121
 823  NFadeL 122,  L122
 824  NFadeL 123,  L123
 825  NFadeL 124,  L124
 826  NFadeL 125,  L125
 827  NFadeL 126,  L126
 828  Flash 126, Flasher126
 829  NFadeL 127,  L127
 830  NFadeLm 128,  L128
 831  NFadeL 128,  L128b
 832
 833  End Sub
```

## Slingshot events

Lines 950-952:

```
 950  Sub RightSlingShot_Slingshot
 951      RS.VelocityCorrect(Activeball)
 952  	vpmTimer.PulseSw 62
```

Lines 970-972:

```
 970  Sub LeftSlingShot_Slingshot
 971      LS.VelocityCorrect(Activeball)
 972  	vpmTimer.PulseSw 61
```
