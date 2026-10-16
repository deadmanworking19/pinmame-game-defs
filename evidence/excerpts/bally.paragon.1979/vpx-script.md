# Paragon - known-working table script, controller bindings

Source: `Paragon (Bally 1979).vbs` in the pinned `sverrewl/vpxtable_scripts` corpus (revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, path `special_audiopan_and_audiofade_patched/bord_probably/`, SHA-256 `c61b0824933bea6f136dcd3b06da8304e175dbfe7b1e88725635dd5e7b053bcc`). Its header reads "Paragon (Bally 1978) v2.3 / by bord / base script by 32assassin" with a change log up to "2.37 - bord - fixes for stuff Wylte found, env lighting from Haunts". The retained table `Paragon (Bally 1979).vpx` embeds a script that differs from the pinned file only in whitespace, in two audio-pan and audio-fade exponents the corpus patched, and in one line: the retained table comments out `set Lights(13)=L13`. The lines below are quoted from the pinned file; the script itself is not redistributed.

## Controller and libraries

```
Const cGameName="paragon",UseSolenoids=2,UseLamps=1,UseGI=0,SSolenoidOn="SolOn",SSolenoidOff="SolOff", SCoin=""
LoadVPM "01130100", "Bally.VBS", 3.21
		.HandleMechanics=0
		.HandleKeyboard=0
```

## Solenoid callbacks

```
	SolCallback(2) = "SolLeftTargetReset"								' Single Drop Targets Reset
	SolCallback(6) = "vpmSolSound SoundFX(""Knocker"",DOFKnocker),"		' Knocker
	SolCallback(8) = "SolLeftOut"										' Treasure Chamber Saucer Release
	SolCallback(9) = "SolCenterOut"										' Golden Cliffs Saucer Release
	SolCallback(10) = "SolRightOut"										' Paragon Saucer Release
	SolCallback(17) = "SolRightTargetReset"								' Right 3-bank Target Bank Reset
	SolCallback(7) = "bsTrough.SolOut"									' Outhole Kicker (Ball Release)
	SolCallBack(19) = "vpmNudge.SolGameOn"								' K1 Relay (Flipper Enable)

	SolCallback(sLRFlipper) = "SolRFlipper"
	SolCallback(sLLFlipper) = "SolLFlipper"
```

`SolLeftTargetReset` raises drop targets 1, 2, 3 and 4 (`DTRaise 1` to `DTRaise 4`); `SolRightTargetReset` raises 17, 18 and 19. `SolLFlipper` rotates `LeftFlipper` and `LeftFlipper1`; `SolRFlipper` rotates `RightFlipper` and `RightFlipper1`. The saucer callbacks kick the ball held in trigger `sw31` at 45 degrees, `sw32` at 140 degrees and `sw24` at 215 degrees (VPX angles, 0 = towards the back). The thumper bumpers and slingshots have no solenoid callback; the table kicks them itself.

## Trough and tilt

```
	vpmNudge.TiltSwitch  = swtilt
	bsTrough.Initsw 0,8,0,0,0,0,0,0
	bsTrough.InitKick BallRelease, 80,16
	bsTrough.Balls = 1
Sub Drain_Hit:RandomSoundDrain Drain:bsTrough.addball me:End Sub
```

## Switch handlers

```
Sub sw24_Hit ... Controller.Switch(24) = 1      ' saucer trigger, released in sw24_unHit
Sub sw31_Hit ... Controller.Switch(31) = 1
Sub sw32_Hit ... Controller.Switch(32) = 1
Sub sw1_Hit:DTHit 1:End Sub   (likewise sw2, sw3, sw4, sw17, sw18, sw19; DTArray = Array(DT1, DT2, DT3, DT4, DT17, DT18, DT19))
Sub SW22_Hit:Controller.Switch(22)=1 : End Sub
Sub SW23_Hit:Controller.Switch(23)=1 : End Sub
Sub SW26_Hit:Controller.Switch(26)=1 : End Sub
Sub SW28_Hit:Controller.Switch(28)=1 : End Sub
Sub SW34_Hit:Controller.Switch(34)=1 : End Sub
Sub SW34a_Hit:Controller.Switch(34)=1 : End Sub
Sub sw29_Hit : vpmTimer.PulseSw(29) : TargetBouncer activeball, 0.9 : End Sub
Sub sw30_Hit : vpmTimer.PulseSw(30) : toptarget_prim.transy = -4: sw30.timerenabled=1: End Sub
Sub sw27a_Hit : vpmTimer.PulseSw(27) : End Sub
Sub sw27b_Hit : vpmTimer.PulseSw(27) : End Sub
Sub sw34b_Hit : vpmTimer.PulseSw(34) : End Sub
Sub sw33_Spin:vpmTimer.PulseSw 33 : PlaySoundAt "Spinner", sw33 : End Sub
Sub Bumper1_Hit : vpmTimer.PulseSw(37) : ...
Sub Bumper2_Hit : vpmTimer.PulseSw(38) : ...
Sub Bumper3_Hit : vpmTimer.PulseSw(39) : ...
Sub Bumper4_Hit : vpmTimer.PulseSw(40) : ...
Sub LeftSlingShot_Slingshot ... vpmtimer.pulsesw 36
Sub RightSlingShot_Slingshot ... vpmtimer.pulsesw 35
```

The table has no object named `sw27b`, so the `sw27b_Hit` handler never runs; both 500-point rebound rubbers are the one baked collidable primitive `sw27a`.

## Lamp bindings

`set Lights(n)=Ln` for n = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 30, 31, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 47, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 62 and 63 - every main-board address except 11, 27, 29, 45 and 61. The retained table comments out the `13` line. The table's lights named `L11`, `L16`, `L27` and `L29` are members of its `GI` collection, switched on once at start-up (`For each xx in GI:xx.State = 1: Next`), not lamp outputs.

## Backglass lamp reads (VR backglass only)

```
	If Controller.Lamp(13) = 0 Then: f_BIP.visible=0: else: f_BIP.visible=1 'Ball In Play
	If Controller.Lamp(45) = 0 Then: f_GO.visible=0: else: f_GO.visible=1 'Game Over
	If Controller.Lamp(29) = 0 Then: f_HS.visible=0: else: f_HS.visible=1 'High Score To Date
	If Controller.Lamp(45) = 0 Then: f_Match.visible=0: else: f_Match.visible=1 'Match
	If Controller.Lamp(61) = 0 Then: f_Tilt.visible=0: else: f_Tilt.visible=1 'Tilt
	If Controller.Lamp(43) = 0 Then: f_SA.visible=0: else: f_SA.visible=1 'Shoot Again
```

## Option switches form (vpmDips)

The `editDips` form labels: "Match feature" (dip 21), "Credits display" (dip 20), "Maximum credits" (dips 17-19), "Sound features" (dips 8 and 32), "High score to date" (dips 6-7), "High score feature" (dips 14-15), "Balls per game" (dip 16), "Hitting in line targets" (dip 22), "PARAGON saucer adjustment" (dip 23), "PARAGON saucer lites" (dip 24), "3 drop target special can be collected" (dip 31), "Waterfall lane 5,000 lite" (dip 29), "In line drop targets" (dip 30).

## European variant option

```
Const EuropeVariant = 0				' 1 = 3 Flipper Europe Variant, 0 = Default
	RightFlipper1.enabled = False
```

With the option on, the table hides and disables `RightFlipper1` and enables a guide (`Europeguide`), a rubber (`EuropeRubber`) and a post in the Beast's Lair (`Lairpost_prim`, `Lairrubber`).
