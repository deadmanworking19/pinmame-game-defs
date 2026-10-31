# Elvis (Stern) — controller bindings in the retained table's embedded script

Every non-comment line of the embedded script of `elvis_mod_1.0.vpx` (table version 1.0.2; extracted `script.vbs`,
SHA-256 `51594f64207eca7afec821dea1ecd607d7cc756187d8ff63d7a815bb4c6c17ad`) that names the controller, a ball stack, drop-target bank, magnet, impulse plunger or mech, a switch
write, a solenoid callback, a lamp or flasher assignment, the G.I. callback, or a toy it moves from a solenoid, quoted
verbatim with its line number. Selected with a fixed pattern over the whole file; whole-line comments are left out,
trailing comments kept. Tabs are kept as in the file. The table ships no sidecar script.

```text
   18: Const cGameName = "elvis" 'English
   32: LoadVPM "01560000", "SEGA.VBS", 3.26
   38: Const UseSolenoids = 1
   39: Const UseLamps = 0
   40: Const UseGI = 0
   42: Const HandleMech = 0
   58:         .GameName = cGameName
   59:         .Games(cGameName).Settings.Value("sound") = 1 'enable the rom sound
   64:         .HandleMechanics = 0
   67:         .Games(cGameName).Settings.Value("rol") = 0
   79:     vpmNudge.TiltSwitch = 56
   84:     Set bsTrough = New cvpmBallStack
   86:         .InitSw 0, 14, 13, 12, 11, 0, 0, 0
   87:         .InitKick BallRelease, 90, 4
   89:         .Balls = 4
   93:     Set mMag = New cvpmMagnet
   95:         .InitMagnet Magnet, 60
   96:         .Solenoid = 5
  102:     set dtBankL = new cvpmdroptarget
  104:         .initdrop array(sw17, sw18, sw19, sw20, sw21), array(17, 18, 19, 20, 21)
  109:     Set bsLock = New cvpmBallStack
  111:         .InitSw 0, 48, 0, 0, 0, 0, 0, 0
  112:         .InitKick HLock, 180, 8
  117:     Set bsJail = new cvpmBallStack
  119:         .InitSaucer sw34, 34, 186, 18
  126:     Set bsUpper = new cvpmBallStack
  128:         .InitSaucer sw32, 32, 90, 15
  137:     Set plungerIM = New cvpmImpulseP
  139:         .InitImpulseP swplunger, IMPowerSetting, IMTime
  141:         .switch 16
  147:     Set mElvis = New cvpmMech
  149:         .MType = vpmMechOneSol + vpmMechReverse + vpmMechLinear
  150:         .Sol1 = 25
  151:         .Length = 150
  152:         .Steps = 150
  153:         .AddSw 33, 0, 0
  154:         .Callback = GetRef("UpdateElvis")
  176:     If keyUpperLeft Then Controller.Switch(55) = 1
  183:     If keyUpperLeft Then Controller.Switch(55) = 0
  190: Sub UpdateElvis(aNewPos, aSpeed, aLastPos)
  191:     pStand.x = 518+aNewPos/3
  196:     pStand.y = 482+aNewPos
  207: SolCallback(sLRFlipper) = "SolRFlipper"
  208: SolCallback(sLLFlipper) = "SolLFlipper"
  210: Sub SolLFlipper(Enabled)
  213:         LeftFlipper.RotateToEnd
  214:         LeftFlipper1.RotateToEnd
  217:         LeftFlipper.RotateToStart
  218:         LeftFlipper1.RotateToStart
  222: Sub SolRFlipper(Enabled)
  225:         RightFlipper.RotateToEnd
  226:         RightFlipper1.RotateToEnd
  229:         RightFlipper.RotateToStart
  230:         RightFlipper1.RotateToStart
  303: SolCallBack(1) = "SolTrough"
  304: SolCallBack(2) = "Auto_Plunger"
  305: SolCallBack(3) = "dtBankL.SolDropUp"
  306: SolCallBack(6) = "bsJail.SolOut"
  307: SolCallBack(7) = "bsLock.SolOut"
  308: SolCallBack(8) = "CGate.Open ="
  309: SolCallBack(12) = "bsUpper.SolOut"
  310: SolCallBack(19) = "SolHotelDoor"
  311: SolCallBack(24) = "vpmsolsound SoundFX(""fx_knocker"",DOFKnocker),"
  313: Sub SolTrough(Enabled)
  315:         bsTrough.ExitSol_On
  316:         vpmTimer.PulseSw 15
  320: Sub Auto_Plunger(Enabled)
  322:         PlungerIM.AutoFire
  326: Sub SolHotelDoor(Enabled)
  328:         fDoor.RotatetoEnd
  329:         doorwall.IsDropped = 1
  331:         fDoor.RotatetoStart
  332:         doorwall.IsDropped = 0
  339: SolCallBack(20) = "SetLamp 100,"
  340: SolCallback(21) = "SetLamp 101,"
  341: SolCallBack(22) = "SetLamp 102,"
  342: SolCallBack(23) = "SetLamp 103,"
  343: SolCallBack(32) = "SetLamp 104,"
  344: SolCallBack(31) = "SetLamp 105,"
  350: SolCallBack(29) = "ElvisLegs"
  351: SolCallBack(30) = "ElvisArms"
  353: Sub ElvisLegs(Enabled)
  356:         fLegs.RotatetoStart
  358:         fLegs.RotatetoEnd
  362: Sub ElvisArms(Enabled)
  364:         fArms.RotatetoStart
  366:         fArms.RotatetoEnd
  374: Sub Drain_Hit:Playsound "fx_drain":bsTrough.AddBall Me:End Sub
  377: Sub sw9_Hit:vpmTimer.PulseSw 9:PlaySound SoundFX("fx_target", DOFTargets), 0, 1, pan(ActiveBall):End Sub
  379: Sub sw10_Hit:Controller.Switch(10) = 1:End Sub
  380: Sub sw10_unHit:Controller.Switch(10) = 0:End Sub
  381: Sub sw17_Hit:dtBankL.Hit 1:End Sub
  382: Sub sw18_Hit:dtBankL.Hit 2:End Sub
  383: Sub sw19_Hit:dtBankL.Hit 3:End Sub
  384: Sub sw20_Hit:dtBankL.Hit 4:End Sub
  385: Sub sw21_Hit:dtBankL.Hit 5:End Sub
  386: Sub sw22_Hit:vpmTimer.PulseSw 22:PlaySound SoundFX("fx_target", DOFTargets), 0, 1, pan(ActiveBall), 0, 0, AudioFade(ActiveBall):End Sub
  387: Sub sw23_Hit:vpmTimer.PulseSw 23:PlaySound SoundFX("fx_target", DOFTargets), 0, 1, pan(ActiveBall), 0, 0, AudioFade(ActiveBall):End Sub
  388: Sub sw24_Hit:vpmTimer.PulseSw 24:PlaySound SoundFX("fx_target", DOFTargets), 0, 1, pan(ActiveBall), 0, 0, AudioFade(ActiveBall):End Sub
  389: Sub sw25_Spin:PlaySound "fx_spinner", 0, 1, -0.01:vpmTimer.PulseSw 25:End Sub
  391: Sub sw26_Hit:Controller.Switch(26) = 1:End Sub
  392: Sub sw26_unHit:Controller.Switch(26) = 0:End Sub
  393: Sub sw27_Hit:Controller.Switch(27) = 1:End Sub
  394: Sub sw27_unHit:Controller.Switch(27) = 0:End Sub
  395: Sub sw28_Hit:Controller.Switch(28) = 1:PlaySound "fx_metalrolling",0, 1, 0.15, 0.35:End Sub
  396: Sub sw28_unHit:Controller.Switch(28) = 0:End Sub
  397: Sub sw30_Hit:Controller.Switch(30) = 1:End Sub
  398: Sub sw30_unHit:Controller.Switch(30) = 0:End Sub
  399: Sub sw31_Hit:Controller.Switch(31) = 1:PlaySound "fx_metalrolling",0, 1, 0.15, 0.35:End Sub
  400: Sub sw31_unHit:Controller.Switch(31) = 0:End Sub
  401: Sub sw32_Hit:playsound "Kicker_Hit":bsUpper.AddBall 0:End Sub
  402: Sub sw34_Hit:playsound "fx_kicker_enter":bsJail.AddBall 0:End Sub
  403: Sub sw36_Hit:vpmTimer.PulseSw 36:PlaySound SoundFX("fx_target", DOFTargets), 0, 1, pan(ActiveBall), 0, 0, AudioFade(ActiveBall):End Sub
  404: Sub sw37_Hit:vpmTimer.PulseSw 37:PlaySound SoundFX("fx_target", DOFTargets), 0, 1, pan(ActiveBall), 0, 0, AudioFade(ActiveBall):End Sub
  405: Sub sw38_Hit:vpmTimer.PulseSw 38:PlaySound SoundFX("fx_target", DOFTargets), 0, 1, pan(ActiveBall), 0, 0, AudioFade(ActiveBall):End Sub
  406: Sub sw39_Hit:vpmTimer.PulseSw 39:PlaySound SoundFX("fx_target", DOFTargets), 0, 1, pan(ActiveBall), 0, 0, AudioFade(ActiveBall):End Sub
  407: Sub sw40_Hit:vpmTimer.PulseSw 40:PlaySound SoundFX("fx_target", DOFTargets), 0, 1, pan(ActiveBall), 0, 0, AudioFade(ActiveBall):End Sub
  408: Sub sw41_Hit:Controller.Switch(41) = 1:PlaySound "fx_sensor", 0, 1, pan(ActiveBall), 0, 0, AudioFade(ActiveBall):End Sub
  409: Sub sw41_UnHit:Controller.Switch(41) = 0:End Sub
  410: Sub sw42_Hit:Controller.Switch(42) = 1:PlaySound "fx_sensor", 0, 1, pan(ActiveBall), 0, 0, AudioFade(ActiveBall):End Sub
  411: Sub sw42_UnHit:Controller.Switch(42) = 0:End Sub
  412: Sub sw43_Hit:Controller.Switch(43) = 1:PlaySound "fx_sensor", 0, 1, pan(ActiveBall), 0, 0, AudioFade(ActiveBall):End Sub
  413: Sub sw43_UnHit:Controller.Switch(43) = 0:End Sub
  414: Sub sw45_Hit:Controller.Switch(45) = 1:End Sub
  415: Sub sw45_unHit:Controller.Switch(45) = 0:End Sub
  416: Sub sw46_Hit:Controller.Switch(46) = 1:End Sub
  417: Sub sw46_unHit:Controller.Switch(46) = 0:End Sub
  418: Sub sw47_Hit:Controller.Switch(47) = 1:End Sub
  419: Sub sw47_unHit:Controller.Switch(47) = 0:End Sub
  421: Sub sw48_Hit:Controller.Switch(48) = 1:End Sub
  422: Sub sw48_unHit:Controller.Switch(48) = 0:End Sub
  425: Sub Bumper1_Hit:vpmTimer.PulseSw 49:PlaySound SoundFX("fx_bumper1", DOFContactors), 0, 1, 0, 0:End Sub
  426: Sub Bumper2_Hit:vpmTimer.PulseSw 50:PlaySound SoundFX("fx_bumper2", DOFContactors), 0, 1, 0, 0:End Sub
  427: Sub Bumper3_Hit:vpmTimer.PulseSw 51:PlaySound SoundFX("fx_bumper3", DOFContactors), 0, 1, 0, 0:End Sub
  429: Sub sw52_Hit:vpmTimer.PulseSw 52:PlaySound SoundFX("fx_target", DOFTargets), 0, 1, pan(ActiveBall), 0, 0, AudioFade(ActiveBall):End Sub
  430: Sub sw53_Hit:vpmTimer.PulseSw 53:PlaySound SoundFX("fx_target", DOFTargets), 0, 1, pan(ActiveBall), 0, 0, AudioFade(ActiveBall):End Sub
  431: Sub sw57_Hit::Controller.Switch(57) = 1:PlaySound "fx_sensor", 0, 1, pan(ActiveBall), 0, 0, AudioFade(ActiveBall):End Sub
  432: Sub sw57_UnHit:Controller.Switch(57) = 0:End Sub
  433: Sub sw58_Hit:Controller.Switch(58) = 1:PlaySound "fx_sensor", 0, 1, pan(ActiveBall), 0, 0, AudioFade(ActiveBall):End Sub
  434: Sub sw58_UnHit:Controller.Switch(58) = 0:End Sub
  435: Sub sw60_Hit:Controller.Switch(60) = 1:PlaySound "fx_sensor", 0, 1, pan(ActiveBall), 0, 0, AudioFade(ActiveBall):End Sub
  436: Sub sw60_UnHit:Controller.Switch(60) = 0:End Sub
  437: Sub sw61_Hit:Controller.Switch(61) = 1:PlaySound "fx_sensor", 0, 1, pan(ActiveBall), 0, 0, AudioFade(ActiveBall):End Sub
  438: Sub sw61_UnHit:Controller.Switch(61) = 0:End Sub
  469:     vpmTimer.PulseSw 59
  488:     vpmTimer.PulseSw 62
  502: Sub sw63_Hit:Controller.Switch(63) = 1:End Sub
  503: Sub sw63_UnHit:Controller.Switch(63) = 0:PlaySound"fx_balldrop1",0,1,0.1:End Sub
  505: Sub sw64_Hit
  506:     vpmTimer.PulseSw 64
  522:     HoundDog.TransZ = DogStep
  570:     NFadeL 1, l1
  571:     NFadeL 2, l2
  572:     NFadeL 3, l3
  573:     NFadeL 4, l4
  574:     NFadeL 5, l5
  575:     NFadeL 6, l6
  576:     NFadeL 7, l7
  577:     NFadeL 8, l8
  578:     NFadeL 9, l9
  579:     NFadeL 10, l10
  580:     NFadeL 11, l11
  581:     NFadeL 12, l12
  582:     NFadeL 13, l13
  583:     NFadeL 14, l14
  584:     NFadeL 15, l15
  585:     NFadeL 16, l16
  586:     NFadeL 17, l17
  587:     NFadeL 18, l18
  588:     NFadeL 19, l19
  589:     NFadeL 20, l20
  590:     NFadeL 21, l21
  591:     NFadeL 22, l22
  592:     NFadeL 23, l23
  593:     NFadeL 24, l24
  594:     NFadeL 25, l25
  595:     NFadeL 26, l26
  596:     NFadeL 27, l27
  597:     NFadeL 28, l28
  598:     NFadeL 29, l29
  599:     NFadeL 30, l30
  600:     NFadeL 31, l31
  601:     NFadeL 32, l32
  602:     NFadeL 33, l33
  603:     NFadeL 34, l34
  604:     NFadeL 35, l35
  605:     NFadeL 36, l36
  606:     NFadeL 37, l37
  607:     NFadeL 38, l38
  608:     NFadeL 39, l39
  609:     NFadeL 40, l40
  610:     NFadeL 41, l41
  611:     NFadeL 42, l42
  612:     NFadeL 43, l43
  613:     NFadeL 44, l44
  614:     NFadeL 45, l45
  615:     NFadeL 46, l46
  616:     NFadeL 47, l47
  617:     NFadeL 48, l48
  618:     NFadeL 49, l49
  619:     NFadeL 50, l50
  620:     NFadeL 51, l51
  621:     NFadeL 52, l52
  622:     NFadeL 53, l53
  623:     NFadeL 54, l54
  624:     NFadeL 55, l55
  625:     NFadeL 56, l56
  626:     NFadeLm 57, l57
  627:     Flash 57, l57a
  628:     NFadeLm 58, l58
  629:     Flash 58, l58a
  630:     NFadeLm 59, l59
  631:     Flash 59, l59a
  632:     Flash 60, l60
  633:     Flash 61, l61
  634:     Flash 62, l62
  635:     NFadeL 63, l63
  636:     NFadeL 64, l64
  637:     Flash 65, l65
  638:     Flash 66, l66
  639:     Flash 67, l67
  640:     Flash 68, l68
  641:     Flash 69, l69
  642:     Flashm 70, l70a
  643:     Flash 70, l70
  644:     Flashm 71, l71a
  645:     Flash 71, l71
  646:     Flashm 72, l72a
  647:     Flash 72, l72
  648:     Flash 73, l73
  649:     Flash 74, l74
  650:     Flash 75, l75
  651:     Flash 76, l76
  652:     Flash 77, l77
  653:     Flash 78, l78
  656:     Flashm 100, f20a
  657:     Flashm 100, f20b
  658:     Flashm 100, f20c
  659:     Flashm 100, f20
  660: 	FlupperFlashm 100, Flasherflash666, FlasherLit6, FlasherBase6, FlasherLight6
  661: 	FlupperFlash 100, Flasherflash444, FlasherLit4, FlasherBase4, FlasherLight4
  662: 	Flashm 101, f21
  663: 	FlupperFlash 101, FlasherFlash555, FlasherLit5, FlasherBase5, FlasherLight5
  664: 	FlupperFlash 102, FlasherFlash333, FlasherLit3, FlasherBase3, FlasherLight3
  665:     NFadeLm 103, f23a
  666:     NFadeL 103, f23
  667: 	FlupperFlashm 104, FlasherFlash111, FlasherLit1, FlasherBase1, FlasherLight1
  668: 	FlupperFlash 104, FlasherFlash222, FlasherLit2, FlasherBase2, FlasherLight2
  669:     Flashm 105, f31a
  670:     Flash 105, f31
  695:         FlashRepeat(x) = 20     ' how many times the flash repeats
  769: 	flashm nr, Object
  782: 	FlupperFlashm nr, FlashObject, LitObject, BaseObject, LightObject
 1038: Set GICallback = GetRef("GIUpdate")
 1040: Sub GIUpdate(no, Enabled)
 1041:     For each x in aGiLights
 1045:     For each x in aGiFlashers
```

Bindings the selection shows and the definition relies on:

- `sega.vbs` (loaded at line 32) supplies the flipper and cabinet constants; `sLRFlipper` and `sLLFlipper` are core.vbs's
  public 46 and 48. `SolLFlipper` and `SolRFlipper` rotate each lower flipper together with its upper flipper
  (`LeftFlipper1`, `RightFlipper1`); the script registers no callback for public 13 or 14, and no key writes 88.
- `mElvis` (lines 147-156) moves the figure while solenoid 25 alone is on (`vpmMechOneSol + vpmMechReverse +
  vpmMechLinear`, 150 steps) and closes switch 33 at step 0; solenoids 26-28 are not read.
- Switch 15 is written only as a `vpmTimer.PulseSw 15` inside `SolTrough`; switch 64 only as a `vpmTimer.PulseSw 64` from
  `sw64_Hit`. Switch 10 has handlers but the table has no `sw10` object.
- Solenoids 20-23, 31 and 32 are flashers routed through `SetLamp 100`-`105`; solenoid 24 plays a knocker sound.
