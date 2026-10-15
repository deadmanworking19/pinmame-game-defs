# Retained Seawitch 2.0.0 script contract

Embedded script.vbs SHA-256 a3483e9c4e00c68add7135cd0f3a0dbe216a418d17b9c4f02177da27f1239031. Claimed regions follow; trailing horizontal whitespace is trimmed. The mixed space/tab indentation on the two bsTrough initialization lines is expanded to spaces at eight-column tab stops; all other source text and line boundaries are preserved. Original metadata lacks author,version,date. The corpus script called2.0.0 has a NOT VERIFIED header; filename does not grant runtime authority. Factory sheets and production-ROM runs settle the binding decisions.

## Embedded lines 1-51

```vb
Option Explicit
Randomize

On Error Resume Next
ExecuteGlobal GetTextFile("controller.vbs")
If Err Then MsgBox "You need the controller.vbs in order to run this table, available in the vp10 package"
On Error Goto 0

Const cGameName="seawitch",UseSolenoids=1,UseLamps=0,UseGI=0,SSolenoidOn="SolOn",SSolenoidOff="SolOff",SCoin="coin"

LoadVPM "01560000", "stern.vbs", 3.26
Dim DesktopMode: DesktopMode = Table1.ShowDT

If DesktopMode = True Then 'Show Desktop components
Ramp16.visible=1
Ramp15.visible=1
Primitive13.visible=1
Else
Ramp16.visible=0
Ramp15.visible=0
Primitive13.visible=0
End if

'**********************************************************************************************************
'Solenoid Call backs
'**********************************************************************************************************
SolCallback(6) =  "vpmSolSound SoundFX(""Knocker"",DOFKnocker),"
SolCallback(7) = "dtBank.SolDropUp" 'Drop Targets
SolCallback(8) = "dtLBank.SolDropUp" 'Drop Targets
SolCallback(9) = "dtRBank.SolDropUp" 'Drop Targets
SolCallback(10) = "bsTrough.SolOut"

SolCallback(sLRFlipper) = "SolRFlipper"
SolCallback(sLLFlipper) = "SolLFlipper"

Sub SolLFlipper(Enabled)
     If Enabled Then
         PlaySound SoundFX("fx_Flipperup",DOFContactors):LeftFlipper.RotateToEnd:LeftFlipper1.RotateToEnd
     Else
         PlaySound SoundFX("fx_Flipperdown",DOFContactors):LeftFlipper.RotateToStart:LeftFlipper1.RotateToStart
     End If
  End Sub

Sub SolRFlipper(Enabled)
     If Enabled Then
         PlaySound SoundFX("fx_Flipperup",DOFContactors):RightFlipper.RotateToEnd:RightFlipper1.RotateToEnd
     Else
         PlaySound SoundFX("fx_Flipperdown",DOFContactors):RightFlipper.RotateToStart:RightFlipper1.RotateToStart
     End If
End Sub
'**********************************************************************************************************
```

## Embedded lines 67-113

```vb
Dim bsTrough, dtBank, dtLBank, dtRBank

Sub Table1_Init
	vpmInit Me
	On Error Resume Next
		With Controller
		.GameName = cGameName
		If Err Then MsgBox "Can't start Game" & cGameName & vbNewLine & Err.Description : Exit Sub
		.SplashInfoLine = "SeaWitch"&chr(13)&"You Suck"
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

          PinMAMETimer.Interval = PinMAMEInterval
          PinMAMETimer.Enabled = 1
          vpmNudge.TiltSwitch = 7
          vpmNudge.Sensitivity = 2
          vpmNudge.TiltObj = Array(Bumper1, Bumper2, Bumper3,LeftSlingShot, RightSlingShot)

          Set bsTrough = New cvpmBallStack
                  bsTrough.InitNoTrough ballrelease, 33, 90, 4
                          bsTrough.InitExitSnd SoundFX("ballrelease",DOFContactors), SoundFX("Solenoid",DOFContactors)

          set dtLBank = new cvpmdroptarget
              dtLBank.InitDrop Array(sw40, sw39, sw38), Array(40, 39, 38)
              dtLBank.InitSnd SoundFX("DTDrop",DOFContactors),SoundFX("DTReset",DOFContactors)

          set dtRBank = new cvpmdroptarget
              dtRBank.InitDrop Array(sw32, sw31, sw30, sw29), Array(32, 31, 30, 29)
              dtRBank.InitSnd SoundFX("DTDrop",DOFContactors),SoundFX("DTReset",DOFContactors)

          set dtBank = new cvpmdroptarget
              dtBank.InitDrop Array(sw21, sw22, sw23, sw24), Array(21, 22, 23, 24)
              dtBank.InitSnd SoundFX("DTDrop",DOFContactors),SoundFX("DTReset",DOFContactors)
 End Sub

```

## Embedded lines 134-205

```vb
Sub sw5_Spin():vpmTimer.PulseSw 5 : playsound"fx_spinner" : End Sub

'Bumpers
     Sub Bumper1_Hit:vpmTimer.PulseSw 9:playsound SoundFX("fx_bumper1",DOFContactors):SetLamp 181, 0:Me.TimerEnabled = 1::End Sub

      Sub Bumper1_Timer()
		SetLamp 181, 1
		Me.TimerEnabled = 0
      End Sub

       Sub Bumper2_Hit:vpmTimer.PulseSw 10:playsound SoundFX("fx_bumper1",DOFContactors):SetLamp 180, 0:Me.TimerEnabled = 1::End Sub

      Sub Bumper2_Timer()
		SetLamp 180, 1
		Me.TimerEnabled = 0
      End Sub

     Sub Bumper3_Hit:vpmTimer.PulseSw 14:playsound SoundFX("fx_bumper1",DOFContactors):SetLamp 182, 0:Me.TimerEnabled = 1::End Sub

      Sub Bumper3_Timer()
		SetLamp 182, 1
		Me.TimerEnabled = 0
      End Sub

'Star Trigger
Sub sw4_Hit:Controller.Switch(4) = 1:PlaySound "rollover":End Sub
Sub sw4_UnHit:Controller.Switch(4) = 0:End Sub
Sub sw25_Hit():DivDir = -1:closedSL.IsDropped=1:OpenSL.IsDropped=0:Controller.Switch(25) = 1:lrro.State=0:PlaySound "rollover":End Sub
Sub sw25_UnHit():Controller.Switch(25) = 0:lrro.State=1:End Sub

 'Rollovers
Sub sw34_Hit::Controller.Switch(34) = 1:PlaySound "rollover":End Sub
Sub sw34_UnHit::Controller.Switch(34) = 0:End Sub
Sub sw35_Hit::Controller.Switch(35) = 1:PlaySound "rollover":End Sub
Sub sw35_UnHit::Controller.Switch(35) = 0:End Sub
Sub sw36_Hit::Controller.Switch(36) = 1:PlaySound "rollover":End Sub
Sub sw36_UnHit::Controller.Switch(36) = 0:End Sub
Sub sw37_Hit::Controller.Switch(37) = 1:PlaySound "rollover":End Sub
Sub sw37_UnHit::Controller.Switch(37) = 0:End Sub

'Standup Targets
Sub sw17_Hit:vpmTimer.PulseSw 17:End Sub
Sub sw18_Hit:vpmTimer.PulseSw 18:End Sub
Sub sw19_Hit:vpmTimer.PulseSw 19:End Sub
Sub sw20_Hit:vpmTimer.PulseSw 20:End Sub

'Drop Targets
Sub Sw21_Dropped: DTBank.Hit 1:end sub
Sub Sw22_Dropped: DTBank.Hit 2:end sub
Sub Sw23_Dropped: DTBank.Hit 3:end sub
Sub Sw24_Dropped: DTBank.Hit 4:end sub

Sub Sw40_Dropped: DTLBank.Hit 1:end sub
Sub Sw39_Dropped: DTLBank.Hit 2:end sub
Sub Sw38_Dropped: DTLBank.Hit 3:end sub

Sub Sw32_Dropped: DTRBank.Hit 1:end sub
Sub Sw31_Dropped: DTRBank.Hit 2:end sub
Sub Sw30_Dropped: DTRBank.Hit 3:end sub
Sub Sw29_Dropped: DTRBank.Hit 4:end sub

'Diverter
 Sub SLS_Hit()
	If ActiveBall.VelY<0 Then
		DivDir = -1
		closedSL.IsDropped=1
		OpenSL.IsDropped=0
	End If
End Sub

 Sub SLS2_Hit()
		DivDir = 1
```

## Embedded lines 249-339

```vb
        NFadeL 1, l1
        NFadeLm 2, l2
        Flash 2, f2
        NFadeLm 3, l3
		Flash 3, f3
        NFadeLm 4, l4b
        NFadeL 4, l4
        NFadeL 5, l5
        NFadeL 6, l6
        NFadeL 7, l7
        NFadeL 8, l8
        NFadeL 9, l9
        NFadeL 10, l10
        NFadeL 11, l11
        NFadeL 12, l12
     '   FadeR 13, hs 'High Score
        NFadeL 14, l14
        NFadeL 15, l15
        NFadeLm 17, l17
		Flash 17, f17
        NFadeLm 18, l18
		Flash 18, f18
        NFadeLm 19, l19
		Flash 19, f19
        NFadeL 20, l20
        NFadeL 21, l21
        NFadeL 22, l22
        NFadeL 23, l23
        NFadeL 24, l24
        NFadeL 25, l25
        NFadeL 26, l26
        NFadeL 27, l27
        NFadeL 28, l28
        NFadeL 30, l30
        NFadeL 31, l31
        NFadeLm 33, l33
		Flash 33, f33
        NFadeLm 34, l34
		Flash 34, f34
        NFadeL 35, l35
        NFadeL 36, l36
        NFadeL 37, l37
        NFadeL 38, l38
        NFadeL 39, l39
        NFadeL 40, l40
        NFadeL 42, l42
        NFadeL 43, l43
        NFadeL 44, l44
     '   FadeR 45, go 'Game Over
        NFadeL 46, l46
        NFadeL 47, l47
        NFadeLm 49, l49
        Flash 49, F49
        NFadeLm 50, l50
		Flash 50, f50

        NFadeL 52, l52
        NFadeL 53, l53
        NFadeL 54, l54
        NFadeL 55, l55
        NFadeL 56, l56
        NFadeL 58, l58
        NFadeL 59, l59
        NFadeL 60, l60
  '      FadeR 61, tilt 'Tilt
        NFadeL 62, l62
   '     FadeR 63, match 'Match

		NFadeLm 180, fb3a1
		NFadeL 180, fb1
		NFadeLm 181, fb3a2
		NFadeL 181, fb2
		NFadeLm 182, fb3a
		NFadeL 182, fb3

 End Sub


' div lamp subs

Sub InitLamps()
    Dim x
    For x = 0 to 200
        LampState(x) = 0        ' current light state, independent of the fading level. 0 is off and 1 is on
        FadingLevel(x) = 4      ' used to track the fading state
        FlashSpeedUp(x) = 0.4   ' faster speed when turning on the flasher
        FlashSpeedDown(x) = 0.2 ' slower speed when turning off the flasher
        FlashMax(x) = 1         ' the maximum value when on, usually 1
        FlashMin(x) = 0         ' the minimum value when off, usually 0
        FlashLevel(x) = 0       ' the intensity of the flashers, usually from 0 to 1
    Next
```

## Embedded lines 586-619

```vb
Sub RightSlingShot_Slingshot
	vpmTimer.PulseSw 42
    PlaySound SoundFX("right_slingshot",DOFContactors), 0,1, 0.05,0.05 '0,1, AudioPan(RightSlingShot), 0.05,0,0,1,AudioFade(RightSlingShot)
    RSling.Visible = 0
    RSling1.Visible = 1
    sling1.TransZ = -20
    RStep = 0
    RightSlingShot.TimerEnabled = 1

End Sub

Sub RightSlingShot_Timer
    Select Case RStep
        Case 3:RSLing1.Visible = 0:RSLing2.Visible = 1:sling1.TransZ = -10
        Case 4:RSLing2.Visible = 0:RSLing.Visible = 1:sling1.TransZ = 0:RightSlingShot.TimerEnabled = 0:
    End Select
    RStep = RStep + 1
End Sub

Sub LeftSlingShot_Slingshot
	vpmTimer.PulseSw 12
    PlaySound SoundFX("left_slingshot",DOFContactors), 0,1, -0.05,0.05 '0,1, AudioPan(LeftSlingShot), 0.05,0,0,1,AudioFade(LeftSlingShot)
    LSling.Visible = 0
    LSling1.Visible = 1
    sling2.TransZ = -20
    LStep = 0
    LeftSlingShot.TimerEnabled = 1

End Sub

Sub LeftSlingShot_Timer
    Select Case LStep
        Case 3:LSLing1.Visible = 0:LSLing2.Visible = 1:sling2.TransZ = -10
        Case 4:LSLing2.Visible = 0:LSLing.Visible = 1:sling2.TransZ = 0:LeftSlingShot.TimerEnabled = 0:
```

RightSlingShot_Slingshot writes42; factory switch13 and runtime coil5 settle that artifact defect. Cosmetic helper states180-182 are not controller addresses. lN lights are insert overlays, not proven sockets. F2/F3/F17/F18/F19/F33/F34/F49/F50 are VPX Flasher render helpers on lamp callbacks, not nine fitted flashers.
