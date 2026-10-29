# Retained Stars table runtime regions

Literal source regions, extracted with vpxtool git:v0.33.3.
Trailing whitespace alone is removed to satisfy the repository whitespace gate. The primary curator
checked these regions against the retained files. Code establishes bindings,
not physical socket positions. This 0.9.0.4 table has a swapped slingshot
write: LeftSlingshot pulses 36 and RightSlingshot 37. Factory and ROM mapping
is left 37/right 36. The repeated coil-7 assignment overwrites the first.

script.vbs:9-11

```vb
Const cGameName="stars",UseSolenoids=1,UseLamps=1,UseGI=0, SCoin="coin"

LoadVPM "01110000","bally.vbs",2.0
```

script.vbs:29-59

```vb
SolCallback(1)= "vpmSolSound SoundFX(""Chime1"",DOFChimes),"
SolCallback(2)= "vpmSolSound SoundFX(""Chime2"",DOFChimes),"
SolCallback(3)= "vpmSolSound SoundFX(""Chime3"",DOFChimes),"
SolCallback(4)= "vpmSolSound SoundFX(""Chime4"",DOFChimes),"
SolCallback(6)= "vpmSolSound SoundFX(""Knocker"",DOFKnocker),"
SolCallback(7)="bstrough.solin"
SolCallback(7)="bsTrough.SolOut"
SolCallback(9)="dtLeft.SolDropUp"
SolCallback(10)="dtTop.SolDropUp"
SolCallback(19)="vpmNudge.solGameOn"

SolCallback(sLRFlipper) = "SolRFlipper"
SolCallback(sLLFlipper) = "SolLFlipper"

Sub SolLFlipper(Enabled)
     If Enabled Then
         PlaySound SoundFX("fx_Flipperup",DOFContactors):LeftFlipper.RotateToEnd
     Else
         PlaySound SoundFX("fx_Flipperdown",DOFContactors):LeftFlipper.RotateToStart
     End If
  End Sub

Sub SolRFlipper(Enabled)
     If Enabled Then
         PlaySound SoundFX("fx_Flipperup",DOFContactors):RightFlipper.RotateToEnd
     Else
         PlaySound SoundFX("fx_Flipperdown",DOFContactors):RightFlipper.RotateToStart
     End If
End Sub
'**********************************************************************************************************

```

script.vbs:95-112

```vb
	PinMAMETimer.Enabled=1

	vpmNudge.TiltSwitch=7
	vpmNudge.Sensitivity=2
	vpmNudge.TiltObj=Array(Bumper1,LeftSlingshot,RightSlingshot)

	Set bsTrough=New cvpmBallstack
		bsTrough.InitNoTrough ballrelease,8,90,3
		bsTrough.InitExitSnd SoundFX("ballrelease",DOFContactors), SoundFX("Solenoid",DOFContactors)

	Set dtTop=New cvpmDropTarget
		dtTop.InitDrop Array(SW30,SW27,SW29),Array(30,27,29)
		dtTop.initsnd SoundFX("DTDrop",DOFContactors),SoundFX("DTReset",DOFContactors)

	Set dtLeft=New cvpmDropTarget
		dtLeft.InitDrop Array(SW32,SW28,SW31),Array(32,28,31)
		dtLeft.initsnd SoundFX("DTDrop",DOFContactors),SoundFX("DTReset",DOFContactors)

```

script.vbs:135-182

```vb

'Drop Targets
Sub sw30_Dropped:dtTop.Hit 1:End Sub
Sub sw27_Dropped:dtTop.Hit 2:End Sub
Sub sw29_Dropped:dtTop.Hit 3:End Sub

Sub sw32_Dropped:dtLeft.Hit 1:End Sub
Sub sw28_Dropped:dtLeft.Hit 2:End Sub
Sub sw31_Dropped:dtLeft.Hit 3:End Sub

 'Stand Up Targets
Sub sw20_Hit:VpmTimer.PulseSw 20:End Sub
Sub sw21_Hit:VpmTimer.PulseSw 21:End Sub
Sub sw22_Hit:VpmTimer.PulseSw 22:End Sub
Sub sw23_Hit:VpmTimer.PulseSw 23:End Sub
Sub sw24_Hit:VpmTimer.PulseSw 24:End Sub

'Wire Triggers
Sub sw4_Hit:Controller.Switch(4)=1 : playsound"rollover" : End Sub
Sub sw4_unHit:Controller.Switch(4)=0:End Sub
Sub sw5_Hit:Controller.Switch(5)=1 : playsound"rollover" : End Sub
Sub sw5_unHit:Controller.Switch(5)=0:End Sub
Sub sw12_Hit:Controller.Switch(12)=1 : playsound"rollover" : End Sub
Sub sw12_unHit:Controller.Switch(12)=0:End Sub
Sub sw13_Hit:Controller.Switch(13)=1 : playsound"rollover" : End Sub
Sub sw13_unHit:Controller.Switch(13)=0:End Sub

'Button Triggers
Sub sw15a_Hit:Controller.Switch(15)=1 : playsound"rollover" : End Sub
Sub sw15a_UnHit:Controller.Switch(15)=False:End Sub
Sub sw15b_Hit:Controller.Switch(15)=1 : playsound"rollover" : End Sub
Sub sw15b_UnHit:Controller.Switch(15)=False:End Sub

'Spinner
Sub sw1_Spin:vpmTimer.PulseSw 1 : playsound"fx_spinner" : End Sub
Sub sw17_Spin:vpmTimer.PulseSw 17 : playsound"fx_spinner" : End Sub

'Bumpers
Sub Bumper1_Hit : vpmTimer.PulseSw(38) : playsound SoundFX("fx_bumper1",DOFContactors): End Sub

 'Scoring Rubber
Sub sw25a_hit:vpmTimer.pulseSw 25 : playsound"flip_hit_3" : End Sub
Sub sw25b_hit:vpmTimer.pulseSw 25 : playsound"flip_hit_3" : End Sub
Sub sw25c_hit:vpmTimer.pulseSw 25 : playsound"flip_hit_3" : End Sub
Sub sw25d_hit:vpmTimer.pulseSw 25 : playsound"flip_hit_3" : End Sub
Sub sw25e_hit:vpmTimer.pulseSw 25 : playsound"flip_hit_3" : End Sub
Sub sw25f_hit:vpmTimer.pulseSw 25 : playsound"flip_hit_3" : End Sub
Sub sw25g_hit:vpmTimer.pulseSw 25 : playsound"flip_hit_3" : End Sub
```

script.vbs:185-234

```vb
set lights(1)=L1
set lights(2)=L2
set lights(3)=L3
set lights(4)=L4
set lights(5)=L5
lights(6)=array(L6,L6B)
lights(7)=array(L7,L7B)
lights(8)=array(L8A,L8B)
'set lights(9)=L9
set lights(10)=L10
set lights(11)=L11
set lights(12)=L12
'set lights(13)=L13
'set lights(14)=L14
'set lights(15)=L15
'set lights(16)=L16
set lights(17)=L17
'set lights(18)=L18
set lights(19)=L19
set lights(20)=L20
set lights(21)=L21
lights(22)=array(L22A,L22B)
'set lights(23)=L23
lights(24)=array(L24A,L24B)
lights(25)=array(L25A,L25B)
set lights(26)=L26
'set lights(27)=L27
set lights(28)=L28

set lights(33)=L33

set lights(35)=L35
set lights(36)=L36

lights(38)=array(L38,L38B)

set lights(42)=L42
set lights(43)=L43
set lights(44)=L44

set lights(49)=L49

set lights(51)=L51
set lights(52)=L52

lights(54)=array(L54,L54B)

set lights(58)=L58
set lights(59)=L59
set lights(60)=L60
```

script.vbs:326-358

```vb
End Sub
Set vpmShowDips = GetRef("editDips")


'**********Sling Shot Animations
' Rstep and Lstep  are the variables that increment the animation
'****************
Dim RStep, Lstep

Sub RightSlingShot_Slingshot
	vpmTimer.PulseSw 37
    PlaySound SoundFX("right_slingshot",DOFContactors), 0,1, 0.05,0.05 '0,1, AudioPan(RightSlingShot), 0.05,0,0,1,AudioFade(RightSlingShot)
    RSling.Visible = 0
    RSling1.Visible = 1
    sling1.rotx = 20
    RStep = 0
    RightSlingShot.TimerEnabled = 1
End Sub

Sub RightSlingShot_Timer
    Select Case RStep
        Case 3:RSLing1.Visible = 0:RSLing2.Visible = 1:sling1.rotx = 10
        Case 4:RSLing2.Visible = 0:RSLing.Visible = 1:sling1.rotx = 0:RightSlingShot.TimerEnabled = 0
    End Select
    RStep = RStep + 1
End Sub

Sub LeftSlingShot_Slingshot
	vpmTimer.PulseSw 36
    PlaySound SoundFX("left_slingshot",DOFContactors), 0,1, -0.05,0.05 '0,1, AudioPan(LeftSlingShot), 0.05,0,0,1,AudioFade(LeftSlingShot)
    LSling.Visible = 0
    LSling1.Visible = 1
    sling2.rotx = 20
```

Retained Bally.vbs v3.61; constants below are library identities. The generic
ball-roll-tilt at 2 is NOT fitted on Stars.

Bally.vbs:20-39

```vb
' Flipper Solenoid
Const GameOnSolenoid   = 19
' Cabinet switches
Const swSelfTest       = -7
Const swCPUDiag        = -6
Const swSoundDiag      = -5
Const swTilt           =  7
Const swBallRollTilt   =  2
Const swSlamTilt       = 16
Const swCoin3          =  9
Const swCoin2          = 10
Const swCoin1          = 11
Const swStartButton    =  6

Const swLRFlip         = 82
Const swLLFlip         = 84
Const swURFlip         = 81
Const swULFlip         = 83

' Help Window
```

Pinned `src/wpc/by35.c:475-490`, complete diagnostic/service routing block:

```c
  /*-- Diagnostic buttons on CPU board --*/
#ifndef LISY_SUPPORT
  cpu_set_nmi_line(0, core_getSw(BY35_SWCPUDIAG) ? ASSERT_LINE : CLEAR_LINE);
#else
  cpu_set_nmi_line(0, lisy35_get_SW_S33() ? ASSERT_LINE : CLEAR_LINE);
#endif
  sndbrd_0_diag(core_getSw(BY35_SWSOUNDDIAG));
  /*-- coin door switches --*/
#ifndef LISY_SUPPORT
  pia_set_input_ca1(BY35_PIA0, !core_getSw(BY35_SWSELFTEST));
#else
  pia_set_input_ca1(BY35_PIA0, !lisy35_get_SW_Selftest());
#endif
}
```

The hardware-backed branch names S33 explicitly on the same NMI route as
CPU diagnostic. Factory Figure 3 (PDF22 printed17) places that one button
on the MPU, separate from S1-S32 and the coin-door Self Test button. The
manual's memory-clear adjustment use is retained in `coils-and-options.md`.
