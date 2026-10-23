# Creature from the Black Lagoon — VPW v1.0 script bindings

Quoted from the retained VPW v1.0 table's embedded script (`script.vbs` extracted with vpxtool from
`Creature from the Black Lagoon (Williams 1992) VPW v1.0.vpx`, SHA-256
`110d85325e33cbaf465f5a60f3aeeb2069329c55719435e7b76380748ba70ea6`). Every non-comment line that names the ROM, binds a solenoid, lamp,
G.I. string or switch to the controller, or drives the chase-light, ramp-lift and kicker code, with its line
number. Lines are reproduced byte for byte apart from tabs, which are shown as four spaces.

```vbscript
   83  Const cGameName="cftbl_l4"
   85  Const UseSolenoids = 2
  661      vpmMapLights AllLamps ' Map all lamps to the corresponding ROM output suing the value of TimerInterval of each light object
  663          .GameName = cGameName
  664          If Err Then MsgBox "Can't start Game" & cGameName & vbNewLine & Err.Description : Exit Sub
  666          .HandleMechanics=0
  690      Controller.Switch(58) = 1
  691      Controller.Switch(57) = 1
  692      Controller.Switch(56) = 1
  693      Controller.Switch(15) = 1
  700  Set GiCallback2 = GetRef("UpdateGI")
  702  Dim ChaseLightRampState, ChaseLightBowlState: ChaseLightRampState=0: ChaseLightBowlState=0
  703  Dim ChaseLightBit1, ChaseLightBit2: ChaseLightBit1=0: ChaseLightBit2=0
  705  Sub UpdateChaseLight
  707      Dim chase1: chase1 = ChaseLight1.GetInPlayState
  708      Dim chase2: chase2 = ChaseLight2.GetInPlayState
  709      Dim chase3: chase3 = ChaseLight3.GetInPlayState
  710      Dim chase4: chase4 = ChaseLight4.GetInPlayState
  711      l143.state = chase1 * ChaseLightRampState
  712      l144.state = chase2 * ChaseLightRampState
  713      l145.state = chase3 * ChaseLightRampState
  714      l146.state = chase4 * ChaseLightRampState
  715      l133.state = chase1 * ChaseLightBowlState
  716      l134.state = chase2 * ChaseLightBowlState
  717      l135.state = chase3 * ChaseLightBowlState
  718      l136.state = chase4 * ChaseLightBowlState
  721  Sub UpdateGI(no, step) ' GI Strings with 9 intensity levels (0 to 8)
  731          Case 0 : ChaseLightRampState = v
  732          Case 1 : For Each gi_lamp in GI_Middle : gi_lamp.state = v : Next
  733          Case 2 : For Each gi_lamp in GI_Upper : gi_lamp.state = v : Next
  734          Case 3 : ChaseLightBowlState = v
  735          Case 4 : For Each gi_lamp in GI_Lower : gi_lamp.state = v : Next
  817  SolCallback(1) =    "RightUpperKicker"    'Top Right Popper
  818  SolCallback(3) =    "RightLowerKicker"    'Bottom Right Popper
  819  SolCallback(4) =     "SolRelease"        'Ball Release
  826  SolCallback(12) =    "SolOuthole"        'Drain Outhole
  833  SolCallback(23) = "SolRampUp"
  835  SolCallback(26) = "SolRampDown"
  836  SolCallBack(27) = "CreatureMotorMirror"
  837  SolCallBack(28) = "HoloLamp"            'Hologram Light
  839  SolModCallBack(2)  = "Flasher2"  'Flasher2  - Subway Enter Flasher x2 (1x Playfield / 1x Insert)
  840  SolModCallBack(8)  = "Flasher8"  'Flasher8  - Bottom Right Flasher x2 (1x Playfield / 1x Insert)
  841  SolModCallBack(9)  = "Flasher9"  'Flasher9  - Top Left & Right Flashers
  842  SolModCallBack(10) = "Flasher10" 'Flasher10 - Bowl Flasher x2 (1x Playfield / 1x Insert)
  843  SolModCallBack(11) = "Flasher11" 'Flasher11
  844  SolModCallBack(16) = "Flasher16" 'Flasher16 - Right Popper Side Flasher x2 (1x Playfield / 1x Insert)
  845  SolModCallBack(17) = "Flasher17" 'Flasher17 - Bottom Left Flasher x2 (1x Playfield / 1x Insert)
  846  SolModCallBack(18) = "Flasher18" 'Flasher18 - Right Ramp Flasher x2 (1x Playfield / 1x Insert)
  847  SolModCallBack(19) = "Flasher19" 'Flasher19 - Left Ramp Flasher x2 (1x Playfield / 1x Insert)
  848  SolModCallBack(22) = "Flasher22" 'Flasher22 - Centre Hole Flasher x2 (1x Playfield / 1x Insert)
  849  SolModCallBack(25) = "Flasher25 " 'MovieFlasher - Left and Right Start Movie Flashers (Inserts)
  850  SolModCallBack(33) = "Flasher33" 'Flasher33
  851  SolModCallBack(34) = "Flasher34" 'Flasher34
  852  SolModCallBack(35) = "Flasher35" 'Flasher35
  853  SolModCallBack(36) = "Flasher36" 'Flasher36
  855  SolCallBack(20) = "ChaseLightBit1="
  856  SolCallBack(24) = "ChaseLightBit2="
  859  Sub Flasher2(pwm)
  861      f2.state = pwm
  868  Sub Flasher8(pwm)
  870      f8.state = pwm
  877  Sub Flasher9(pwm)
  879      f9.state = pwm
  880      f9b.state = pwm
  887  Sub Flasher10(pwm)
  889      f10.state = pwm
  896  Sub Flasher11(pwm)
  898      f11.state = pwm
  902  Sub Flasher16(pwm)
  904      f16.state = pwm
  911  Sub Flasher17(pwm)
  913      f17.state = pwm
  920  Sub Flasher18(pwm)
  922      f18.state = pwm
  929  Sub Flasher19(pwm)
  931      f19.state = pwm
  938  Sub Flasher22(pwm)
  940      f22.state = pwm
  947  Sub Flasher25(pwm)
  949      f25.state = pwm
  950      f25b.state = pwm
  957  Sub Flasher33(pwm)
  959      f33.state = pwm
  963  Sub Flasher34(pwm)
  965      f34.state = pwm
  969  Sub Flasher35(pwm)
  971      f35.state = pwm
  975  Sub Flasher36(pwm)
  977      f36.state = pwm
  997  SolCallback(sLRFlipper) = "SolRFlipper"
  998  SolCallback(sLLFlipper) = "SolLFlipper"
 1099  Sub sw58_Hit():Controller.Switch(58) = 1:UpdateTrough:End Sub
 1100  Sub sw58_UnHit():Controller.Switch(58) = 0:UpdateTrough:End Sub
 1101  Sub sw57_Hit():Controller.Switch(57) = 1:UpdateTrough:End Sub
 1102  Sub sw57_UnHit():Controller.Switch(57) = 0:UpdateTrough:End Sub
 1103  Sub sw56_Hit():Controller.Switch(56) = 1:UpdateTrough:End Sub
 1104  Sub sw56_UnHit():Controller.Switch(56) = 0:UpdateTrough:End Sub
 1112      If sw56.BallCntOver = 0 Then sw57.kick 60, 9
 1113      If sw57.BallCntOver = 0 Then sw58.kick 60, 9
 1121  Sub sw55_Hit()        'Drain
 1124      Controller.Switch(55) = 1
 1127  Sub sw55_UnHit()    'Drain
 1128      Controller.Switch(55) = 0
 1131  Sub SolOuthole(enabled)
 1133          sw55.kick 60,20
 1137  Sub SolRelease(enabled)
 1139          sw56.kick 60, 12
 1162  Sub sw34_Hit
 1164      Controller.Switch(34) = 1
 1169  Sub RightUpperKicker(Enable)
 1171          If Controller.Switch(34) <> 0 Then
 1174              Controller.Switch(34) = 0
 1180  Sub sw37_Hit
 1182      Controller.Switch(37) = 1
 1187  Sub RightLowerKicker(Enable)
 1189          If Controller.Switch(37) <> 0 Then
 1192              Controller.Switch(37) = 0
 1197  Sub sw17_Hit()
 1199      vpmTimer.PulseSw 17
 1206  Sub sw16_Hit()
 1208      vpmTimer.PulseSw 16
 1219  Sub sw51_Hit():VPMTimer.PulseSw 51:End Sub
 1220  Sub sw52_Hit():VPMTimer.PulseSw 52:End Sub
 1221  Sub sw53_Hit():VPMTimer.PulseSw 53:End Sub
 1222  Sub sw54_Hit():VPMTimer.PulseSw 54:End Sub
 1224  Sub sw15_Hit():controller.switch(15) = 0:End Sub
 1225  Sub sw15_Unhit():controller.switch(15) = 1:End Sub
 1227  Sub sw18_Hit():VPMTimer.PulseSw 18:End Sub                  'Center Shot
 1229  Sub sw25_Hit():VPMTimer.PulseSw 25:End Sub
 1230  Sub sw26_Hit():VPMTimer.PulseSw 26:End Sub
 1231  Sub sw27_Hit():VPMTimer.PulseSw 27:End Sub
 1232  Sub sw28_Hit():VPMTimer.PulseSw 28:End Sub
 1237  Sub sw41_Hit:STHit 41:End Sub
 1238  Sub sw41o_Hit:TargetBouncer Activeball, 1:End Sub
 1239  Sub sw42_Hit:STHit 42:End Sub
 1240  Sub sw42o_Hit:TargetBouncer Activeball, 1:End Sub
 1241  Sub sw43_Hit:STHit 43:End Sub
 1242  Sub sw43o_Hit:TargetBouncer Activeball, 1:End Sub
 1243  Sub sw44_Hit:STHit 44:End Sub
 1244  Sub sw44o_Hit:TargetBouncer Activeball, 1:End Sub
 1247  Sub sw63_Hit():VPMTimer.PulseSw 63:End Sub
 1249  Sub sw35_Hit():VPMTimer.PulseSw 35:End Sub                    'Right Ramp Enter
 1250  Sub sw36_Hit():VPMTimer.PulseSw 36:End Sub                  'Left Ramp Enter
 1252  Sub sw61_Hit():VPMTimer.PulseSw 61:End Sub                  'Right Ramp Exit
 1253  Sub sw62_Hit():VPMTimer.PulseSw 62:End Sub                  'Left Ramp Exit
 1254  Sub sw64_Hit():VPMTimer.PulseSw 64:End Sub                  'Upper Ramp Enter
 1255  Sub sw65_Hit():VPMTimer.PulseSw 65:End Sub                  'Pool switch
 1256  Sub sw66_Hit():controller.switch(66) = 1 : End Sub            'Ball Shooter Lane
 1257  Sub sw66_UnHit():controller.switch(66) = 0 : End Sub
 1344  Sub Bumper1_Hit():vpmTimer.PulseSw 45:RandomSoundBumperTop Bumper1:End Sub
 1345  Sub Bumper2_Hit():vpmTimer.PulseSw 46:RandomSoundBumperMiddle Bumper2:End Sub
 1346  Sub Bumper3_Hit():vpmTimer.PulseSw 33:RandomSoundBumperBottom Bumper3:End Sub
 1368  Sub SolRampUp(Enabled)
 1370          LRampF.RotateToEnd
 1371          Controller.Switch(38) = False
 1372          collRamp.collidable = False
 1377  Sub SolRampDown(Enabled)
 1379          LRampF.RotateToStart
 1380          Controller.Switch(38) = True
 1381          collRamp.collidable = True
 1400  Sub LeftSlingShot_Slingshot
 1402      vpmTimer.pulsesw 47
 1423  Sub RightSlingShot_Slingshot
 1425      vpmTimer.pulsesw 48
 1453    Sub HoloLamp(enabled)
 1473   Sub CreatureMotorMirror(enabled)
 2806          vpmTimer.PulseSw switch mod 100
 3824          Case 1 : snd = "Ball_Collide_1"
 3825          Case 2 : snd = "Ball_Collide_2"
 3826          Case 3 : snd = "Ball_Collide_3"
 3827          Case 4 : snd = "Ball_Collide_4"
```

## Reading notes

- `vpmMapLights AllLamps` binds every light in the AllLamps collection to the lamp its `TimerInterval` names;
  the placements read each light's interval from the table, not its name. `ChaseLight1`-`ChaseLight4` carry
  intervals 91-94 and sit off the playfield: they only feed `UpdateChaseLight`.
- `UpdateChaseLight` lights the ramp phase `l143`-`l146` and the bowl phase `l133`-`l136` while chase lamp
  91-94 is 1, gated by G.I. 0 for the ramp and G.I. 3 for the bowl. The table therefore shows one bulb group
  lit and three dark, and drives the whole ramp from G.I. 0; the Chase Light II schematic lights the three
  strings the decoder does not select (see `chase-light-board.md`).
- Solenoids 20 and 24 only store the decoder bits (`ChaseLightBit1=`, `ChaseLightBit2=`); the chase itself
  comes from PinMAME's lamps 91-94.
