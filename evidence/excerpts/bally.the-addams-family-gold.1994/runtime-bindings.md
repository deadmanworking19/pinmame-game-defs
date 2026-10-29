# Gold embedded script — literal runtime regions

Leading indentation is expanded to spaces and trailing horizontal whitespace is omitted. Statements, quoted contents, source line numbers and full region boundaries are preserved; original byte-for-byte scripts/source remain external.

Source sha2562c33d2b7bb40fab1f41747170e55a2f2638928f6b33179955f4d0bc6eeca254c, vpxtool git:v0.33.3; Windows1252 source decoded to UTF8 for transcription. Line numbers refer to the unmodified retained script, including comments. These literal regions expose host mechanism configuration, callbacks, buyin, mechanism animation, complete matrix-lamp update, GI helpers/mods, and sling defect. No omitted script region is claimed unused.

## script.vbs L40–210

```vb
Const UseSync = 0
Const SCoin="Coin3"

Set GICallback2 = GetRef("UpdateGI")

Dim bsTrough, bsThingSaucer, BookMech, ThingMech
Dim UpperMagnet, RightMagnet, LeftMagnet
Dim LeftFlipperButton
Dim PrimCase1, PrimCase2, PrimCase3, PrimCase4, PrimCase6, PrimCase7, PrimCase8
Dim DayNight

'table init
Const cGameName = "tafg_lx3"   ' Special Collectors Edition

Sub Table1_Init()
    vpmInit Me
    With Controller
        .GameName = cGameName
        If Err Then MsgBox "Can't start Game " & cGameName & vbNewLine & Err.Description:Exit Sub
        .SplashInfoLine="The Addams Family by Bally from 1992"
        .Games(cGameName).Settings.Value("rol") = 0
        .HandleKeyboard=0
        .ShowTitle=0
        .ShowDMDOnly=1
        .HandleMechanics=0
        .DIP(0)=&H00
        .ShowFrame=0
        On Error Resume Next
        .Run GetPlayerHWnd
        If Err Then MsgBox Err.Description
        On Error Goto 0
        If DesktopMode = True THEN
'			If cNewController = 1 Then
'				Controller.Hidden = 0
'			Else
'				Controller.Hidden = 0
'			End If
            L81.Visible = True
            L82.Visible = True
            L83.Visible = True
            L84.Visible = True
            L85.Visible = True
            L86.Visible = True
            L87.Visible = True
            Incline = Table1.Inclination
          Else
            Controller.Hidden = 0
            L81.Visible = False
            L82.Visible = False
            L83.Visible = False
            L84.Visible = False
            L85.Visible = False
            L86.Visible = False
            L87.Visible = False
            Incline = Table1.InclinationFS
            RailRight.Visible = False
            RailLeft.Visible = False
        end If
    End With

    Set bsTrough = New cvpmTrough
    With bsTrough
    .size = 3
    .entrySw = 18
    .initSwitches Array(17, 16, 15)
    .Initexit BallRelease, 90, 8
    .InitExitSounds SoundFX("BallRelease",DOFContactors), SoundFX("ballrelease",DOFContactors)
    .Balls = 3
    End With

      Set BookMech = New cvpmMech
      With BookMech
        .Sol1 = 27
        .Length = 100
        .Steps = 90
        .MType = vpmMechOneSol + vpmMechReverse + vpmMechNonLinear
        .AddSw 81, 89, 90 					' Bookcase Open
        .AddSw 82, 0, 1 					' Bookcase Close
        .Callback = GetRef("BookCaseMotor")
        .Start
      End With

      Set ThingMech = New cvpmMech
      With ThingMech
        .Sol1 = 25
        .Length = 175
        .Steps = 60
        .MType = vpmMechOneSol + vpmMechReverse + vpmMechNonLinear
        .AddSw 85, 59, 60 					' Thing Up Opto
        .AddSw 84, 0, 1 					' Thing Down Opto
        .Callback = GetRef("ThingMotor")
        .Start
      End With

    Set UpperMagnet = New cvpmMagnet
    With UpperMagnet
        .InitMagnet UMagnet, 8
        .GrabCenter = 0
        .solenoid = 23						'Upper Magnet
        .CreateEvents "UpperMagnet"
    '	.magnetOn
    End With

    Set RightMagnet = New cvpmMagnet
    With RightMagnet
        .InitMagnet RMagnet, 8
        .GrabCenter = 0
        .solenoid = 24						'Right Magnet
        .CreateEvents "RightMagnet"
    '	.MagnetOn
    End With

    Set LeftMagnet = New cvpmMagnet
    With LeftMagnet
        .InitMagnet LMagnet, 8
        .GrabCenter = 0
        .solenoid = 16						'Left Magnet
        .CreateEvents "LeftMagnet"
    '	.MagnetOn
    End With

    Dim iv
    For each iv in InsertVis:iv.Opacity = (int(dayNight)*.3):Next  'inserts as dark as day/night slider

    Wall69.isDropped = 1
    Wall70.isDropped = 1
End Sub

Sub TAF_Paused:Controller.Pause = 1:End Sub
Sub TAF_unPaused:Controller.Pause = 0:End Sub
Sub TAF_Exit:Controller.Stop:End Sub

'Nudging
    vpmNudge.TiltSwitch = 14
    vpmNudge.Sensitivity = 2

'Solonoids
SolCallback(1)="Chair" 														'Chair Kickout
SolCallback(2)="Knocker" 													'Thing Knocker
SolCallback(3)="vpmSolDiverter Diverter,""MetalHit_medium"","				'Ramp Diverter
SolCallback(4)="bsTrough.SolOut"  											'Ball Release
SolCallBack(5)="bsTrough.SolIn" 											'Outhole
SolCallback(6)="ThingMagnet" 												'Thing Magnet
SolCallback(7)="ThingKickout" 												'Thing Kickout
SolCallback(8)="LockupKickout"												'Lockup Kickout
'SolCallback(9)= 															'Upper Left Jet
'SolCallback(10)= 															'Upper Right Jet
'SolCallback(11)=															'Center Left Jet
'SolCallBack(12)=			  												'Center Right Jet
'SolCallback(13)= 															'Lower Jet
'SolCallback(14)= 															'Left Slingshot
'SolCallback(15)= 															'Right Slingshot
'SolCallback(16)=		 													'Left Magnet
SolModCallback(17)="TelephoneFlasher"								'Telephone/Upper Right Ramp - flasher
SolModCallback(18)="TrainFlasher" 									'Train/Upper Left Ramp - flasher
SolModCallback(19)="LowerRampFlasher" 								'Lower Ramp/Jet Bumpers (2) - flasher
SolModCallback(20)="LlightningBoltFlasher" 						'Left Lighting bolt/Mini Flipper - flasher
SolModCallback(21)="RlightningBoltFlasher"							'Right Lightning bolt/Swampt - flasher
SolModCallback(22)="ThePowerFlasher"											'The Power/Backbox Cloud(3) - flasher
'SolCallback(23)=															'Upper Magnet
'SolCallback(24)=															'Right Magnet
'SolCallback(25)=															'Thing Motor
SolCallback(26)="ThingEjectHole"											'Thing Eject Hole - flasher
'SolCallback(27)=															'Bookcase Motor
SolCallback(28)="SwampRelease"												'Swamp Release

'Flippers
SolCallback(sLRFlipper) = "SolRFlipper"
SolCallback(sLLFlipper) = "SolLFlipper"
SolCallback(sURFlipper) = "SolURFlipper"
SolCallback(sULFlipper) = "SolULFlipper"
```

## script.vbs L334–412

```vb
Sub Table1_KeyDown(ByVal keycode)

    If vpmKeyDown(keycode) Then Exit Sub

    If keycode = PlungerKey Then
        Plunger.PullBack
        PlaySound "plungerpull",0,1,1,0.25
    End If

    If keycode = LeftTiltKey Then
        Nudge 90, 2
    End If

    If keycode = RightTiltKey Then
        Nudge 270, 2
    End If

    If keycode = CenterTiltKey Then
        Nudge 0, 2
    End If

    If Keycode = LeftFlipperKey Then
        LeftFlipperButton = 1
    End if

    If keycode = PlungerKey Then
        Plunger.PullBack
        PlaySound "plungerpull",0,1,1,0.25
    End If

    If Keycode = KeyFront Then
        Controller.Switch(11) = 1
    End If

End Sub

Sub Table1_KeyUp(ByVal keycode)

     If vpmKeyUp(keycode) Then Exit Sub

    If keycode = PlungerKey Then
        Plunger.Fire
        PlaySound "plunger",0,1,1,0.25
    End If

    If Keycode = LeftFlipperKey Then
        LeftFlipperButton = 0
    End if

    If Keycode = KeyFront Then
        Controller.Switch(11) = 0
    End If


End Sub

Sub Chair (enabled)
    If Enabled Then
        ChairKicker.TimerEnabled = 1
    End If
End Sub

Sub ThingMagnet(Enabled)
    If Enabled = true and  Position> 25 Then
        ThingBall = true
        ThingSaucer.destroyball
        Controller.Switch(87) = 0
        Playsound "MetalHit_Medium"
    End If
    If enabled = false and position< -85 and ThingBall=true then
       ThingBall=false
       ThingKickOutKicker.CreateBall
       Controller.Switch(77) = 1   	'Thing KickOut
    End If
    If enabled = false and position> 25 then
       ThingBall=false
       ThingSaucer.createball
        Controller.switch(87) = 1
    End If
```

## script.vbs L743–803

```vb
 Sub BookCaseMotor(aNewPos,aSpeed,aLastPos)
    DIM OBJ
    PlaySound SoundFX("Motor2",DOFGear)
    Bookcase.rotZ = aNewPos
    BCPlastic.rotZ = aNewPos
    BCScrews.rotZ = aNewPos
    BCRubbers.rotZ = aNewPos
    BCPegs.rotZ = aNewPos
    if aNewPos >60 then
        for each obj in BookcaseOpen
            obj.collidable = true
        next
        for each obj in BookcaseClosed
            obj.collidable = false
        next
    else
        for each obj in BookcaseOpen
            obj.collidable = false
        next
        for each obj in BookcaseClosed
            obj.collidable = true
        next
    end if
 End Sub

Sub TestTimer_Timer

End Sub


Dim Position, HandPosition, Thingball

  Sub ThingMotor(aNewPos,aSpeed,aLastPos)
    dim BoxPosition
    PlaySound SoundFX("Motor",DOFGear)
    position = aNewPos * 2 - 90
    if aNewPos < 3 then
        BoxPosition = aNewPos
    elseif aNewPos < 33 then
        BoxPosition = aNewPos * 1.25
    elseif aNewPos =< 34 then
        BoxPosition = aNewPos * 1.2
    elseif aNewPos =< 35 then
        BoxPosition = aNewPos * 1.14
    elseif aNewPos =< 36 then
        BoxPosition = aNewPos * 1.1
    elseif aNewPos =< 37 then
        BoxPosition = aNewPos * 1.055
    elseif aNewPos =< 38 then
        BoxPosition = aNewPos * 1
    elseif aNewPos =< 39 then
        BoxPosition = aNewPos * .965
    elseif aNewPos =< 40 then
        BoxPosition = aNewPos * .925
    elseif aNewPos < 50 then
        BoxPosition = 34
    elseif aNewPos =< 51 then
        BoxPosition = aNewPos * .685
    elseif aNewPos =< 52 then
        BoxPosition = aNewPos * .67
    elseif aNewPos =< 53 then
```

## script.vbs L1000–1108

```vb
               Case 6:ChairScoop.image = "ScoopMap":ChairPrim.Image = "TAFChairMappingOFF":FesterPrim.Image = "eChairNew":Me.Enabled = 0
           End Select
       End Sub

Set LampCallback = GetRef("Lamps")
    Sub Lamps
        L11.State = Controller.Lamp(11)
        L12.State = Controller.Lamp(12)
        L13.State = Controller.Lamp(13)
        L14.State = Controller.Lamp(14)
        L15.State = Controller.Lamp(15)
        L16.State = Controller.Lamp(16)
        L17.State = Controller.Lamp(17)
        L18.State = Controller.Lamp(18)
'		L19.State = Controller.Lamp(19)
'		L20.State = Controller.Lamp(20)
        L21.State = Controller.Lamp(21)
        L21b.State = Controller.Lamp(21)
        L21c.State = Controller.Lamp(21)
        L22.State = Controller.Lamp(22)
        L22b.State = Controller.Lamp(22)
        L22c.State = Controller.Lamp(22)
        L23.State = Controller.Lamp(23)
        L23b.State = Controller.Lamp(23)
        L23c.State = Controller.Lamp(23)
        L24.State = Controller.Lamp(24)
        L24b.State = Controller.Lamp(24)
        L24c.State = Controller.Lamp(24)
        L25.State = Controller.Lamp(25)
        L25b.State = Controller.Lamp(25)
        L25c.State = Controller.Lamp(25)
        L26.State = Controller.Lamp(26)
        L27.State = Controller.Lamp(27)
        L28.State = Controller.Lamp(28)
'		L29.State = Controller.Lamp(29)
'		L30.State = Controller.Lamp(30)
        L31.State = Controller.Lamp(31)
        L32.State = Controller.Lamp(32)
        L33.State = Controller.Lamp(33)
        L34.State = Controller.Lamp(34)
        L35.State = Controller.Lamp(35)
        L36.State = Controller.Lamp(36)
        L37.State = Controller.Lamp(37)
        L38.State = Controller.Lamp(38)
'		L39.State = Controller.Lamp(39)
'		L40.State = Controller.Lamp(40)
'		L41.State = Controller.Lamp(41)
        L42.State = Controller.Lamp(42)
        L43.State = Controller.Lamp(43)
        L44.State = Controller.Lamp(44)
        L45.State = Controller.Lamp(45)
        L46.State = Controller.Lamp(46)
        L47.State = Controller.Lamp(47)
        L47b.State = Controller.Lamp(47)
        L48.State = Controller.Lamp(48)
'		L49.State = Controller.Lamp(49)
'		L50.State = Controller.Lamp(50)
        L51.State = Controller.Lamp(51)
        L52.State = Controller.Lamp(52)
        L53.State = Controller.Lamp(53)
        L54.State = Controller.Lamp(54)
        L55.State = Controller.Lamp(55)
        L56.State = Controller.Lamp(56)
        L57.State = Controller.Lamp(57)
        L58.State = Controller.Lamp(58)
'		L59.State = Controller.Lamp(59)
'		L60.State = Controller.Lamp(60)
        L61.State = Controller.Lamp(61)
        L62.State = Controller.Lamp(62)
        L63.State = Controller.Lamp(63)
        L64.State = Controller.Lamp(64)
        L64b.State = Controller.Lamp(64)
        L65.State = Controller.Lamp(65)
        L66.State = Controller.Lamp(66)
        L67.State = Controller.Lamp(67)
        L68.State = Controller.Lamp(68)
'		L69.State = Controller.Lamp(69)
'		L70.State = Controller.Lamp(70)
        L71.State = Controller.Lamp(71)
        L72.State = Controller.Lamp(72)
        L73.State = Controller.Lamp(73)
        L74.State = Controller.Lamp(74)
        L74b.State = Controller.Lamp(74)
        L75.State = Controller.Lamp(75)
        L75b.State = Controller.Lamp(75)
    '	L76.State = Controller.Lamp(76)
        L77.State = Controller.Lamp(77)
        L77b.State = Controller.Lamp(77)
        L78.State = Controller.Lamp(78)
        L78b.State = Controller.Lamp(78)
'		L79.State = Controller.Lamp(79)
'		L80.State = Controller.Lamp(80)
        L81.State = Controller.Lamp(81)
        L82.State = Controller.Lamp(82)
        L83.State = Controller.Lamp(83)
        L84.State = Controller.Lamp(84)
        L85.State = Controller.Lamp(85)
        L86.State = Controller.Lamp(86)
        L87.State = Controller.Lamp(87)
        L81F.visible = L81.state
        L82F.visible = L82.state
        L83F.visible = L83.state
        L84F.visible = L84.state
        L85F.visible = L85.state
        L86F.visible = L86.state
        L87F.visible = L87.state

End Sub

```

## script.vbs L1111–1236

```vb
Sub UpdateGI(giNo, status)
Dim ii
   Select Case giNo
      Case 0  'Left String
        GI1.State = Abs(status)
        Intensity GI1.State, GI1
        GI2.State = Abs(status)
        Intensity GI2.State, GI2
        GI3.State = Abs(status)
        Intensity GI3.State, GI3
        GI4.State = Abs(status)
        Intensity GI4.State, GI4
'		GI10.State = Abs(status)
'		Intensity GI10.State, GI10
        GI11.State = Abs(status)
        Intensity GI11.State, GI11
        GI12.State = Abs(status)
        Intensity GI12.State, GI12
'		GI13.State = Abs(status)
'		Intensity GI13.State, GI13
        GI14.State = Abs(status)
        Intensity GI14.State, GI14
        GI15.State = Abs(status)
        Intensity GI15.State, GI15
        GI28.State = Abs(status)
        Intensity GI28.State, GI28
        GI17.State = Abs(status)
        Intensity GI17.State, GI17
        GI18.State = Abs(status)
        Intensity GI18.State, GI18
        GI19.State = Abs(status)
        Intensity GI19.State, GI19
        GI20.State = Abs(status)
        Intensity GI20.State, GI20
        GI21.State = Abs(status)
        Intensity GI21.State, GI21
        GI22.State = Abs(status)
        Intensity GI22.State, GI22
        GI24.State = Abs(status)
        Intensity GI24.State, GI24
        GI25.State = Abs(status)
        Intensity GI25.State, GI25
        GI27.State = Abs(status)
        Intensity GI27.State, GI27
        GI26.State = Abs(status)
        Intensity GI26.State, GI26
        GI30.State = Abs(status)
        Intensity GI30.State, GI30
        GI35.State = Abs(status)
        Intensity GI35.State, GI35
        GI10.State = Abs(status)		'Brighter
        Intensity2 GI10.State, GI10
        GI13.State = Abs(status)		'Brighter
        Intensity2 GI13.State, GI13
        GI38.State = Abs(status)		'Brighter
        Intensity2 GI38.State, GI38
        GI_Light1.State = Abs(status)
        Intensity GI_Light1.State, GI_Light1
        GI_Light.State = Abs(status)
        Intensity GI_Light.State, GI_Light
        LLightning1.State = Abs(status)
        Intensity LLightning1.State, LLightning1     'Chair Light Mod
 '     Case 1   'Insert House String
 '     Case 2   'Insert People String
      Case 4    'Right String
        GI5.State = Abs(status)
        Intensity GI5.State, GI5
        GI6.State = Abs(status)
        Intensity GI6.State, GI6
        GI7.State = Abs(status)
        Intensity GI7.State, GI7
        GI8.State = Abs(status)
        Intensity GI8.State, GI8
        GI9.State = Abs(status)
        Intensity GI9.State, GI9
        GI16.State = Abs(status)
        Intensity GI16.State, GI16
        GI23.State = Abs(status)
        Intensity GI23.State, GI23
        GI32.State = Abs(status)
        Intensity GI32.State, GI32
        GI29.State = Abs(status)
        Intensity GI29.State, GI29
        GI33.State = Abs(status)
        Intensity GI33.State, GI33
        GI34.State = Abs(status)
        Intensity GI34.State, GI34
        GI36.State = Abs(status)
        Intensity GI36.State, GI36
        GI37.State = Abs(status)		'Brighter
        Intensity2 GI37.State, GI37
        GI39.State = Abs(status)		'Brighter
        Intensity2 GI39.State, GI39
        GI40.State = Abs(status)		'Brighter
        Intensity2 GI40.State, GI40
        GI41.State = Abs(status)		'Brighter
        Intensity2 GI41.State, GI41
        GI42.State = Abs(status)		'Brighter
        Intensity2 GI42.State, GI42
        GI_Light2.State = Abs(status)
        Intensity GI_Light2.State, GI_Light2
        GI_Light3.State = Abs(status)
        Intensity GI_Light3.State, GI_Light3
        SwampLight.State = Abs(status)
        Intensity SwampLight.State, SwampLight			'Swamp Light Mod
        VaultLight.State = Abs(Status)
        Intensity VaultLight.State, VaultLight			'Vault Light Mod
    End Select

End Sub

Dim GILevel

    If DayNight <= 20 Then
            GILevel = .5
    ElseIf DayNight <= 40 Then
            GILevel = .4125
    ElseIf DayNight <= 60 Then
            GILevel = .325
    ElseIf DayNight <= 80 Then
            GILevel = .2375
    Elseif DayNight <= 100  Then
            GILevel = .15
    End If

Sub Intensity(nr, Object)
```

## script.vbs L1270–1315

```vb
    RStep = 0
    RightSlingShot.TimerEnabled = 1
    vpmTimer.pulsesw 36					'RightSlingShot
End Sub

Sub RightSlingShot_Timer
    Select Case RStep
        Case 3:RSLing1.Visible = 0:RSLing2.Visible = 1:sling1.TransZ = -15
        Case 4:RSLing2.Visible = 0:RSLing.Visible = 1:sling1.TransZ = 0:RightSlingShot.TimerEnabled = 0
    End Select
    RStep = RStep + 1
End Sub

Sub LeftSlingShot_Slingshot
    PlaySound SoundFX("Slingshot",DOFContactors),0,1,-0.05,0
    LSling.Visible = 0
    LSling1.Visible = 1
    sling2.TransZ = -30
    LStep = 0
    LeftSlingShot.TimerEnabled = 1
    vpmTimer.pulsesw 37					'LeftSlingShot
End Sub

Sub LeftSlingShot_Timer
    Select Case LStep
        Case 3:LSLing1.Visible = 0:LSLing2.Visible = 1:sling2.TransZ = -15
        Case 4:LSLing2.Visible = 0:LSLing.Visible = 1:sling2.TransZ = 0:LeftSlingShot.TimerEnabled = 0
    End Select
    LStep = LStep + 1
End Sub


'***********Extra triggers
Sub Trigger2_hit
    drop1.enabled = 1
End Sub

Sub Trigger3_hit
    drop2.enabled = 1
End Sub

Sub Drop_Hit
    Playsound "BallHit", 0, 1, Pan(ActiveBall), 0, Pitch(ActiveBall), 1, 0
    Drop.TimerEnabled = 1
End Sub

```
