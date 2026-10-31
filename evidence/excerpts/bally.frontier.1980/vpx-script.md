# Frontier - known-working table script, controller bindings

Source: `Frontier (Bally 1980).vbs` at the root of the pinned `sverrewl/vpxtable_scripts` corpus (revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `1016be1239e4fddb0791e77621f9988b4319afb49b3a06b057f939fd0b58484b`). Its header reads "Frontier (Bally 1980) v2.0 / by bord" followed by Thalamus's change notes of 2018 (positional sound, `UseSolenoids=1` changed to 2, Fast Flip v2, solenoids moved above `Table1_Init`). The retained table `Frontier (Bally 1980).vpx` (bord, "Update to 2.0 March 2017") embeds a script at SHA-256 `bb0e1773227f75632558b8c42431e1b87d92cf5c38255d8df3179a1aa959b769` whose controller-facing lines are the same apart from whitespace, sound calls, `Const UseSolenoids = True` against 2, the missing `vpminit me` and `NoUpperRightFlipper`/`NoUpperLeftFlipper` lines, and the position of the `GameName` block. The lines below are quoted from the pinned file; the script itself is not redistributed.

## Controller and libraries

```
Const cGameName = "frontier"
LoadVPM "01000100", "Bally.VBS", 3.02  'Frontier
NoUpperRightFlipper
NoUpperLeftFlipper
Const UseSolenoids = 2
Const UseLamps = True
         .HandleMechanics = False
```

## Solenoid callbacks

```
SolCallback(1) =  "vpmSolSound ""fx_slingshot"","   'sLSling
SolCallback(2) =  "vpmSolSound ""fx_slingshot"","   'sRSling
'SolCallback(3) =   ""
'SolCallback(4) =   ""
'SolCallback(5) =   ""
SolCallback(6) =  "SolKnocker "           'sKnocker
SolCallback(7) =  "bsTrough.SolOut"         'sBallRelease
SolCallback(8) =  "SolInlineTargetReset"        'sInlineTargets
SolCallback(9) =  "SolRightTargetReset"       'sRightTargets
SolCallback(10) =   "SolFrontierSaucer"         'sSaucer
'SolCallback(11) =  "vpmSolSound "            'sLJet
'SolCallback(12) =  "vpmSolSound "            'sRJet
'SolCallback(13) =  "vpmSolSound "            'sDJet
'SolCallback(14) =  ""
'SolCallback(15) =  ""
'SolCallback(16) =  ""
SolCallback(17) =   "vpmSolGate Gate2,true,"      'sGate
SolCallback(18) =   ""
SolCallback(19) =   "vpmNudge.SolGameOn"        'sEnable
'SolCallback(20) =  ""

SolCallback(sLRFlipper) = "SolRFlipper"
SolCallback(sLLFlipper) = "SolLFlipper"
```

`SolInlineTargetReset` raises the `dtLL` bank (`sw21`, `sw22`, `sw23`) and `SolRightTargetReset` the `dtRR` bank (`sw33`, `sw34`, `sw35`). `SolFrontierSaucer` clears switch 12 and kicks the ball held in kicker `sw12` (`sw12.Kick -10, 15 + 5 * Rnd`). `SolKnocker` only plays a sound. `vpmSolGate Gate2,true` opens the invisible one-way gate `Gate2` while 17 is on. The thumper bumpers and slingshots have no solenoid callback; the table kicks them itself. Callbacks 1 and 2 only play a slingshot sound; the ROM never drives either address (the slingshots are 14 and 15).

## Trough, tilt and drop targets

```
    Set bsTrough=New cvpmBallStack
  with bsTrough
    .InitSw 0,8,0,0,0,0,0,0
    .InitKick BallRelease,90,7
    .Balls=1
     vpmNudge.TiltSwitch = 7
     vpmNudge.TiltObj = Array(leftslingshot, rightslingshot, sw38, sw39, sw40)
  Set dtLL=New cvpmDropTarget
    dtLL.InitDrop Array(sw21,sw22,sw23),Array(21,22,23)
  Set dtRR=New cvpmDropTarget
    dtRR.InitDrop Array(sw33,sw34,sw35),Array(33,34,35)
Sub Drain_Hit()
  PlaySoundAtVol "fx2_drain2",Drain,1 : bstrough.addball me
```

## Switch handlers

```
Sub sw12_Hit   : Controller.Switch(12) = True : PlaySoundAtVol "fx_hole-enter",sw12,1:End Sub
 Sub Sw21_Dropped:dtLL.Hit 1 : GI_12a.state=1 : End Sub
 Sub Sw22_Dropped:dtLL.Hit 2 : GI_12b.state=1 : End Sub
 Sub Sw23_Dropped:dtLL.Hit 3 : GI_12c.state=1 : End Sub
 Sub Sw33_Dropped:dtRR.Hit 1 : GI_14c.state=1 : GI_13c.state=1 : End Sub
 Sub Sw34_Dropped:dtRR.Hit 2 : GI_14b.state=1 : GI_13b.state=1 : End Sub
 Sub Sw35_Dropped:dtRR.Hit 3 : GI_14a.state=1 : GI_13a.state=1 : End Sub
Sub sw38_Hit : vpmTimer.PulseSw 38 : PlaySoundAtVol SoundFX("fx2_bumper_1",DOFContactors),sw38,VolSpin: End Sub
Sub sw39_Hit : vpmTimer.PulseSw 39 : PlaySoundAtVol SoundFX("fx2_bumper_2",DOFContactors),sw39,VolSpin: End Sub
Sub sw40_Hit : vpmTimer.PulseSw 40 : PlaySoundAtVol SoundFX("fx2_bumper_3",DOFContactors),sw40,VolSpin: End Sub
Sub sw1a1_hit
  vpmTimer.PulseSw(1)
Sub sw1a2_hit
  vpmTimer.PulseSw(1)
Sub sw1a3_hit
  vpmTimer.PulseSw(1)
Sub sw1a4_hit
  vpmTimer.PulseSw(1)
Sub SW2_Hit:Controller.Switch(2)=1 : End Sub  'Right Outlane
Sub SW3_Hit:Controller.Switch(3)=1 : End Sub  'Right Inlane
Sub SW4_Hit:Controller.Switch(4)=1 : End Sub  'Left Inlane
Sub SW5_Hit:Controller.Switch(5)=1 : End Sub  'Left Outlane
Sub SW13_Hit:Controller.Switch(13)=1 : End Sub  'A
Sub SW14_Hit:Controller.Switch(14)=1 : End Sub  'B
Sub SW15_Hit:Controller.Switch(15)=1 : End Sub  'C
Sub SW25_Hit:Controller.Switch(25)=1 : End Sub  'Falls
Sub sw27_Spin : vpmTimer.PulseSw (27) :PlaySoundAtVol "fx_spinner",sw27,VolSpin: End Sub
Sub sw24_Hit:vpmTimer.PulseSw (24):End Sub
Sub sw29_Hit:vpmTimer.PulseSw (29):End Sub
Sub sw30_Hit:vpmTimer.PulseSw (30):End Sub
Sub sw31_Hit:vpmTimer.PulseSw (31):End Sub
Sub RightSlingShot_Slingshot
  vpmtimer.PulseSw(36)
Sub LeftSlingShot_Slingshot
    vpmtimer.pulsesw(37)
```

Each `_unHit` handler of 2-5, 13-15 and 25 writes 0 to the same address. The `GI_12a`-`GI_14c` lights each drop-target handler turns on, and the `DTLeftLights`/`DTRightLights` collections the reset subs turn off, are table-side lights, not lamp outputs.

## Lamp bindings

```
Set Lights(1)  = l1 'LightSnake1
Set Lights(2)  = l2 'LightHawk1
Set Lights(3)  = l3 'LightCougar1
Set Lights(4)  = l4 'LightWolf1
Set Lights(5)  = l5 'LightBear1
Set Lights(6)  = l6 'LightA
Set Lights(7)  = l7 'LightBonus10K
Set Lights(8)  = l8 'LightBonus50K
Set Lights(9)  = l9 'LightLeftTarget
Set Lights(10) = BumperLeft 'BumperLeft (L10 and BumperLight2)
Set Lights(11) = l11 'LightExtraBall
Set Lights(12) = l12 'LightLeftReturnLane
'Set Lights(13) = LightBallInPlay
Set Lights(14) = l14 'LightDenTarget2X
Set Lights(15) = l15 'LightGateOpen
'Set Lights(16) = unused
Set Lights(17) = l17 'LightSnake2
Set Lights(18) = l18 'LightHawk2
Set Lights(19) = l19 'LightCougar2
Set Lights(20) = l20 'LightWolf2
Set Lights(21) = l21 'LightBear2
Set Lights(22) = l22 'LightB
Set Lights(23) = l23 'LightBonus20K
Set Lights(24) = l24 'LightBonus60K
Set Lights(25) = l25 'LightCenterTarget
Set Lights(26) = BumperCenter 'BumperCenter (L26 and BumperLight3)
'Set Lights(27) = LightMatch
Set Lights(28) = l28 'LightRightReturnLane
'Set Lights(29) = LightHighScore
Set Lights(30) = l30 'LightDenTarget3X
Set Lights(31) = l31 'LightDen2X
'Set Lights(32) = unused
Set Lights(33) = l33 'LightSnake3
Set Lights(34) = l34 'LightHawk3
Set Lights(35) = l35 'LightCougar3
Set Lights(36) = l36 'LightWolf3
Set Lights(37) = l37 'LightBear3
Set Lights(38) = l38 'LightC
Set Lights(39) = l39 'LightBonus30K
Set Lights(40) = l40 'LightSpinner
Set Lights(41) = l41 'LightRightTarget
Set Lights(42) = BumperRight 'BumperRight L42 and BumperLight1)
'Set Lights(43) = LightShootAgain
Set Lights(44) = l44 'LightLeftLaneSpecial
'Set Lights(45) = LightGameOver
Set Lights(46) = l46 'LightDenTarget4X
Set Lights(47) = l47 'LightDen3X
'Set Lights(48) = unused
Set Lights(49) = l49 'LightABCExtraBall
Set Lights(50) = l50 'LightABCSpecial
Set Lights(51) = l51 'LightDen45K
Set Lights(52) = l52 'LightBonus4X
Set Lights(53) = l53 'LightBonusSpecial
Set Lights(54) = l54 'LightGrizzly4X
Set Lights(55) = l55 'LightBonus40K
Set Lights(56) = l56 'LightGrizzlyPoints
Set Lights(57) = l57 'LightBonus2X
Set Lights(58) = l58 'LightBonus3X
Set Lights(59) = l59 'LightCredit
Set Lights(60) = l60 'LightRightLaneSpecial
'Set Lights(61) = LightTilt
Set Lights(62) = l62 'LightDenTargetSpecial
Set Lights(63) = l63'LightDen4X

'Set Lights(10) = GILeft    'PF_Left
'Set Lights(42) = GIRight 'PF_Right
'Set Lights(26) = GICenter  'PF_Center
```

`BumperLeft`, `BumperCenter` and `BumperRight` are table collections holding `BumperLight2` and `L10`, `BumperLight3` and `L26`, and `BumperLight1` and `L42`. Four of the comments contradict the factory sheets and the ROM: the sheets put the right flipper feed lane on lamp 12 and the left on 28, and the right out special on 44 and the left on 60, and in the retained gameplay run the right feed lane (switch 3) scored 15,000 and the left outlane (switch 5) awarded the special with lamps 12 and 60 lit. The binding for 11, commented "LightExtraBall", puts the backbox SHOOT AGAIN on the playfield light `L11` at the centre just above the apron, and the binding for 43 (the playfield SAME PLAYER S.A.) is commented out; the ROM lit 11 and 43 together.

## Option switches

```
    .AddFrame 2, 10, 140, "Balls per game", &HC0000000, _
        Array("2", &HC0000000, "3", 0, "4", &H80000000, "5", &H40000000)
    .AddFrame 160, 10, 140, "Max Credits", &H03000000, _
        Array("10", 0, "15", &H01000000, "25", &H02000000, "40", &H03000000)
    .AddFrame 2, 90, 140, "A && C Lanes are", &H00000020, _
        Array("Separate", 0, "Linked", &H00000020)
    .AddFrame 160, 90, 140, "Frontier Bonus Max", &H00400000, _
        Array("60,000", 0, "110,000", &H00400000)
    .AddFrame 2, 140, 140, "Outlane Special lights", &H00000080, _
        Array("Alternate", 0, "Both light", &H00000080)
    .AddFrame 160, 140, 140, "Outlane Special lights when", &H00002000, _
        Array("3X lights", 0, "4X lights", &H00002000)
    .AddFrame 2, 190, 140, "Feeder Lane Special lights", &H20000000, _
        Array("Alternate", 0, "Both light", &H20000000)
    .AddChk 160, 200, 148, Array("Credit display", &H04000000)
    .AddChk 160, 220, 148, Array("Match", &H08000000)
    .AddChk 7, 250, 300, Array("A-B-C Extra Ball light on at start of game", &H00000040)
    .AddChk 7, 270, 300, Array("A-B-C lane memory", &H00004000)
    'Have to use 32768 because vbscript treats &H00008000 as -32768
    .AddChk 7, 290, 300, Array("Outhole collects Frontier Bonus", 32768)
    .AddChk 7, 310, 300, Array("Gate memory", &H00800000)
```

Bit n of the mask is option switch S(n+1): the form's switches are S6, S7, S8, S14, S15, S16, S23, S24, S25-S28, S30, S31 and S32. It offers nothing for S21, S22 or S29.

Checked setting by setting against the manual's game-adjustment tables (excerpt `manual-game-adjustments.md`), the form agrees everywhere except two frames:

- `&H00002000` is S14. The form reads "3X lights" with the bit off and "4X lights" with it on. The manual reads SW. 14 ON "Special lites come on when side drop target 4X is on." and SW. 14 OFF "Special lites come on when side drop target special is on." The ON readings agree; the OFF readings do not. The retained ROM runs had S14 off and lit the outlane special with the drop-target special on the right bank's third completion, as the manual says, so the form's OFF label is a defect in the table.
- `&H20000000` is S30. The form names it "Feeder Lane Special lights"; the manual's row is "Flipper feed lane 15,000 lite adjustment", and the lit feed lane scored 15,000 in the runs. Its "Alternate" and "Both light" settings match the manual's "1 lite comes on then alternates." and "Both lites come on."

The balls-per-game frame (`&HC0000000`: 2 both on, 3 both off, 4 S32 only, 5 S31 only) and the maximum-credits frame (`&H03000000`: 10 both off, 15 S25 only, 25 S26 only, 40 both on) match the manual's tables row for row.
