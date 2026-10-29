# Bord 1.0.2 retained runtime bindings

Source: retained user-supplied Stars-bord-1.0.2.vpx, SHA256
4a6362487f2628e5d1685e2f51a05fb21f003a12be4f7ff4a727c825bbb0f6a3.
Extracted script SHA256 82ea40733a60135c298d59b19548fb6086175af62923009fdaf5ae255ffcbc72.
The following full binding regions are literal apart from trailing whitespace
removal and one space-before-tab indentation normalization for the whitespace gate.
The table was not launched in this session.

## script.vbs:122-137

```vb
SolCallback(1) = "SolChime1"
SolCallback(2) = "SolChime2"
SolCallback(3) = "SolChime3"
SolCallback(4) = "SolChime4"
SolCallback(6) = "SolKnocker"
SolCallback(7) = "bsTrough.SolOut"
SolCallback(9)	=  "solDropUpL"
SolCallback(10)	=  "solDropUpR"
SolCallback(19)	=  "vpmNudge.SolGameOn"

'******************************************************
'					FLIPPERS
'******************************************************

SolCallback(sLRFlipper) = "SolRFlipper"
SolCallback(sLLFlipper) = "SolLFlipper"
```

## script.vbs:244-284

```vb
Sub Table1_Init
	vpmInit Me
'	On Error Resume Next
	With Controller
		.GameName = cGameName
		If Err Then MsgBox "Can't start Game" & cGameName & vbNewLine & Err.Description : Exit Sub
		.SplashInfoLine = "Stars (Stern 1977)"
		.HandleMechanics=0
		.HandleKeyboard=0
		.ShowDMDOnly=1
		.ShowFrame=0
		.ShowTitle=0
        .hidden = 1
		If Err Then MsgBox Err.Description
	End With
	On Error Goto 0
		Controller.SolMask(0)=0
      vpmTimer.AddTimer 2000,"Controller.SolMask(0)=&Hffffffff'" 'ignore all solenoids - then add the timer to renable all the solenoids after 2 seconds
		Controller.Run
	If Err Then MsgBox Err.Description
	On Error Goto 0

	PinMAMETimer.Interval=PinMAMEInterval
	PinMAMETimer.Enabled=1
	vpmNudge.TiltSwitch = 7
	vpmNudge.Sensitivity = 3
	vpmNudge.TiltObj = Array(Bumper1,LeftSlingshot,RightSlingshot)

	Set bsTrough = New cvpmBallStack
		bsTrough.Initsw 0,8,0,0,0,0,0,0
		bsTrough.Balls = 1
		bsTrough.InitKick BallRelease, 90,5
		randomsoundballrelease drain
		bsTrough.InitExitSnd "",""
		bsTrough.InitEntrySnd "",""

	If VR_Room = 1 Then
		setup_backglass
	End If

End Sub
```

## script.vbs:550-585

```vb
 Sub Drain_Hit:RandomSoundDrain drain:bsTrough.AddBall me:End Sub

'Drop Targets
Sub Sw32_Hit:DTHit 32:End Sub
Sub Sw28_Hit:DTHit 28:End Sub
Sub Sw31_Hit:DTHit 31:End Sub

Sub Sw30_Hit:DTHit 30:End Sub
Sub Sw27_Hit:DTHit 27:End Sub
Sub Sw29_Hit:DTHit 29:End Sub

'Stand Up Targets
 Sub Tsw24_Hit: PrimStandupTgtHit 12, Tsw24, PrimT24: vpmTimer.PulseSw 24 : End Sub
 Sub Tsw24_Timer: PrimStandupTgtMove 12, Tsw24, PrimT24: End Sub

 Sub Tsw21_Hit: PrimStandupTgtHit 12, Tsw21, PrimT21: vpmTimer.PulseSw 21 : End Sub
 Sub Tsw21_Timer: PrimStandupTgtMove 12, Tsw21, PrimT21: End Sub

 Sub Tsw23_Hit: PrimStandupTgtHit 12, Tsw23, PrimT23: vpmTimer.PulseSw 23 : End Sub
 Sub Tsw23_Timer: PrimStandupTgtMove 12, Tsw23, PrimT23: End Sub

 Sub Tsw20_Hit: PrimStandupTgtHit 12, Tsw20, PrimT20: vpmTimer.PulseSw 20 : End Sub
 Sub Tsw20_Timer: PrimStandupTgtMove 12, Tsw20, PrimT20: End Sub

 Sub Tsw22_Hit: PrimStandupTgtHit 12, Tsw22, PrimT22: vpmTimer.PulseSw 22 : End Sub
 Sub Tsw22_Timer: PrimStandupTgtMove 12, Tsw22, PrimT22: End Sub

'Bumpers
Sub Bumper1_Hit
	vpmTimer.PulseSw 38
	RandomSoundBumperMiddle Bumper1
	layer1skirt1.roty=skirtAY(me,Activeball)
	layer1skirt1.rotx=skirtAX(me,Activeball)
	me.timerinterval = 150
	me.timerenabled=1
End Sub
```

## script.vbs:623-646

```vb
 'Star Rollovers
 Sub sw15a_Hit   : Controller.Switch(15) = 1 : layer2star3.transz=-6:End Sub
 Sub sw15a_UnHit : Controller.Switch(15) = 0 : layer2star3.transz=0:End Sub
 Sub sw15b_Hit   : Controller.Switch(15) = 1 : layer2star2.transz=-6:End Sub
 Sub sw15b_UnHit : Controller.Switch(15) = 0 : layer2star2.transz=0:End Sub

 'Wire Triggers
 Sub sw4_Hit  : Controller.Switch(4) = 1 : wire1.transz=-6:End Sub
 Sub sw4_UnHit: Controller.Switch(4) = 0 : wire1.transz=0:End Sub
 Sub sw5_Hit  : Controller.Switch(5) = 1 : wire2.transz=-6:End Sub
 Sub sw5_UnHit: Controller.Switch(5) = 0 : wire2.transz=0:End Sub
 Sub sw13_Hit  : Controller.Switch(13) = 1 : wire3.transz=-6:End Sub
 Sub sw13_UnHit: Controller.Switch(13) = 0 : wire3.transz=0:End Sub
 Sub sw12_Hit  : Controller.Switch(12) = 1 : wire4.transz=-6:End Sub
 Sub sw12_UnHit: Controller.Switch(12) = 0 : wire4.transz=0:End Sub

'Leaf Switches
Sub sw25_hit : vpmTimer.PulseSw (25) : End Sub

'Spinner
Sub sw1_Spin : vpmTimer.PulseSw (1) :PlaySoundAtLevelStatic ("fx_spinner"), gatesoundlevel, spinnerrod001: End Sub

Sub sw17_Spin : vpmTimer.PulseSw (17) :PlaySoundAtLevelStatic ("fx_spinner"), gatesoundlevel, spinnerrod: End Sub

```

## script.vbs:696-750

```vb
Sub UpdateLamps
NFadeLm 1, L1
NFadeLm 2, L2
NFadeLm 3, L3
NFadeLm 4, L4
NFadeLm 5, L5
NFadeLm 6, L6
NFadeLm 6, L6a
NFadeLm 7, L7
NFadeLm 7, L7a
NFadeLm 8, L8
NFadeLm 8, L8a
NFadeLm 8, L8b
NFadeLm 8, L8c
	If l8.state=1 Then
		layer2star2.image="layer2"
		layer2star3.image="layer2"
	End If
	If l8.state=0 Then
		layer2star2.image="layer1"
		layer2star3.image="layer1"
	End If
NFadeLm 10, L10
NFadeLm 11, L11
NFadeLm 12, L12
NFadeLm 17, L17
NFadeLm 19, L19
NFadeLm 20, L20
NFadeLm 21, L21
NFadeLm 22, L22
NFadeLm 22, L22a
'NFadeLm 23, L23
NFadeLm 24, L24
NFadeLm 24, L24a
NFadeLm 25, L25
NFadeLm 25, L25a
NFadeLm 26, L26
NFadeLm 28, L28
NFadeLm 33, L33
NFadeLm 35, L35
NFadeLm 36, L36
NFadeLm 38, L38
NFadeLm 38, L38a
NFadeLm 42, L42
NFadeLm 43, L43
NFadeLm 44, L44
NFadeLm 49, L49
NFadeLm 51, L51
NFadeLm 52, L52
NFadeLm 54, L54
NFadeLm 54, L54a
NFadeLm 58, L58
NFadeLm 59, L59
NFadeLm 60, L60

```

## script.vbs:990-1024

```vb
Sub RightSlingShot_Slingshot
	vpmTimer.PulseSw 36
	RandomSoundSlingshotRight slingr
	RSling.Visible = 0
	RSling1.Visible = 1
	slingr.TransZ = -20
	RStep = 0
	RightSlingShot.TimerEnabled = 1
End Sub

Sub RightSlingShot_Timer
	Select Case RStep
		Case 3:RSLing1.Visible = 0:RSLing2.Visible = 1:slingr.TransZ = -10
		Case 4:RSLing2.Visible = 0:RSLing.Visible = 1:slingr.TransZ = 0:RightSlingShot.TimerEnabled = 0:
	End Select
	RStep = RStep + 1
End Sub

Sub LeftSlingShot_Slingshot
	vpmTimer.PulseSw 37
	RandomSoundSlingshotLeft slingl
	LSling.Visible = 0
	LSling1.Visible = 1
	slingl.TransZ = -20
	LStep = 0
	LeftSlingShot.TimerEnabled = 1
End Sub

Sub LeftSlingShot_Timer
	Select Case LStep
		Case 3:LSLing1.Visible = 0:LSLing2.Visible = 1:slingl.TransZ = -10
		Case 4:LSLing2.Visible = 0:LSLing.Visible = 1:slingl.TransZ = 0:LeftSlingShot.TimerEnabled = 0:
	End Select
	LStep = LStep + 1
End Sub
```

## script.vbs:3001-3030

```vb
' ******************************************************************************************
'      LAMP CALLBACK for the 6 backglass flasher lamps (not the solenoid conrolled ones)
' ******************************************************************************************

IF VR_Room = 1 Then
	Set LampCallback = GetRef("UpdateMultipleLamps")
End If

Sub UpdateMultipleLamps()
	If Controller.Lamp(13) = 0 Then: FlBGL13.visible=0: else: FlBGL13.visible=1 'Ball In Play
	If Controller.Lamp(45) = 0 Then: FlBGL45.visible=0: else: FlBGL45.visible=1 'Match
	If Controller.Lamp(29) = 0 Then: FlBGL29.visible=0: else: FlBGL29.visible=1 'High Score
	If Controller.Lamp(60) = 0 Then: FlBGL60.visible=0: else: FlBGL60.visible=1 'Game Over
	If Controller.Lamp(14) = 0 Then: FlBGL14.visible=0: else: FlBGL14.visible=1 '1 Player
	If Controller.Lamp(30) = 0 Then: FlBGL30.visible=0: else: FlBGL30.visible=1 '1 Player
	If Controller.Lamp(46) = 0 Then: FlBGL46.visible=0: else: FlBGL46.visible=1 '1 Player
	If Controller.Lamp(62) = 0 Then: FlBGL62.visible=0: else: FlBGL62.visible=1 '1 Player
	If Controller.Lamp(15) = 0 Then: FlBGL15.visible=0: else: FlBGL15.visible=1 'Player 1 Up
	If Controller.Lamp(31) = 0 Then: FlBGL31.visible=0: else: FlBGL31.visible=1 'Player 2 Up
	If Controller.Lamp(47) = 0 Then: FlBGL47.visible=0: else: FlBGL47.visible=1 'Player 3 Up
	If Controller.Lamp(63) = 0 Then: FlBGL63.visible=0: else: FlBGL63.visible=1 'Player 4 Up

	If Controller.Lamp(61) = 0 Then
		FlBGL61.visible=0
		VR_Backbox_Backglass.blenddisablelighting = 2.5
	else
		FlBGL61.visible=1 'Tilt
		VR_Backbox_Backglass.blenddisablelighting = 0.5
	End If
End Sub
```

## Curator interpretation

The new script binds physical right sling to36 and left to37, agreeing with
the factory and ROM, and corrects the older local table swap. The NFadeLm
objects are render targets, not proof of lamp sockets. L8/L8b and L8a/L8c
are two co-located pairs; they do not establish four physical lamps. The
VR backglass callback labels45 as Match and60 as Game Over. The traced
factory circuit instead identifies Match at27 (A5J2-8), Game Over at45
(A5J2-11), and Triple Bonus at60 (A5J3-14, with an additional blank A5J2-3
branch). The VR mapping is recorded as a table defect against that wiring;
it does not rename the physical loads or establish the blank branch's use.
