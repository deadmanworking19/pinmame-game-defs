# Known-working script - the Cyclone controller bindings

`reviewed: true`; copied by the curator from the pinned corpus on 2026-10-31
`source: https://github.com/sverrewl/vpxtable_scripts at 0c036bb61b4b4e8c778c37559f6795df8cd1521e, file`
`Cyclone (Williams 1988) v1.5.vbs`, SHA-256 `3b917d098d2756b7889d63de1e69f54f5f185d9ad6c343dcc3cf2bcbbc00086d`

Lines are quoted verbatim with their line numbers; `...` separates non-adjacent ranges. Sound, animation and
ball-physics code between them is omitted. The file is the embedded script of the retained table
`Cyclone (Williams 1988) v1.5.vpx` apart from indentation (spaces here, tabs there), text encoding (UTF-8 here,
Latin-1 there), the Thalamus comment block (lines 7-11, four comment lines and a blank line, which the embedded
script lacks) and line 20, `Const UseSolenoids = 1`, which the embedded script writes as `Const UseSolenoids = True`.
From line 12 on, the embedded script's line numbers are therefore five lower than the numbers quoted here.

```vb
1: ' Cyclone VP9 by melon. December 2009.
2: ' Build For VPX by Sliderpoint 2017...
...
7: ' Thalamus 2018-07-24
8: ' Table has already its own  "Positional Sound Playback Functions" and "Supporting Ball & Sound Functions"
9: ' Changed UseSolenoids=1 to 2 - reverted as table already has its on built-in fastflip
10: ' No special SSF tweaks yet.
...
42: Const cGameName = "cycln_l5" ' Nombre corto de la ROM para el pinmame. Usamos la última versión oficial.
43:
44: LoadVPM "00990300", "S11.VBS", 1.91
...
49:     With Controller
50:         .GameName = cGameName
51:         If Err Then MsgBox "Can't start Game " & cGameName & vbNewLine & Err.Description:Exit Sub
52:         .SplashInfoLine = "Cyclone. Based on the Williams Table 1988" & vbNewLine & "For VPX by Sliderpoint"
53:         .HandleKeyboard = 0
54:         .ShowTitle = 0
55:         .ShowDMDOnly = 1
56:         .ShowFrame = 0
57:         .HandleMechanics = 0
58:         .Hidden = 0
59:         On Error Resume Next
60:         .Run GetPlayerHWnd
61:         .DIP(0) = &H80
62:         If Err Then MsgBox Err.Description
63:         On Error Goto 0
64:     End With
65:
66:     ' Nudging
67:     vpmNudge.TiltSwitch = swTilt
68:     vpmNudge.Sensitivity = 1
69:     vpmNudge.TiltObj = Array(BumperIzquierda, BumperDerecha, BumperAbajo, LeftSlingshot, RightSlingshot)
...
71:     'Mystery Wheel
72:     Dim mWheelMech
73:     Set mWheelMech = New cvpmMech
74:     With mWheelMech
75:         .MType = vpmMechStepSol + vpmMechCircle + vpmMechLinear + vpmMechFast
76:         .Sol1 = 14
77:         .Sol2 = 13
78:         .Length = 200
79:         .Steps = 360
80:         .AddSw 41, 0, 180
81:         .Callback = GetRef("SpinWheel")
82:         .Start
83:     End With
84:
85:   Intensity 'sets GI brightness depending on day/night slider settings
86:
87:   vpmMapLights AllLamps
...
89:   Outhole.CreateSizedBallWithMass 25, 1.55
90:   Outhole.kick 0,0
...
92:   'fastFlips enabled
93:   Set FastFlips = new cFastFlips
94:     with FastFlips
95:       .CallBackL = "SolLFlipper"  'Point these to flipper subs
96:       .CallBackR = "SolRFlipper"  '...
97:       .TiltObjects = True 'Optional, if True calls vpmnudge.solgameon automatically. IF YOU GET A LINE 1 ERROR, DISABLE THIS! (or setup vpmNudge.TiltObj!)
98:       .InitDelay "FastFlips", 100     'Optional, if > 0 adds some compensation for solenoid jitter (occasional problem on Bram Stoker's Dracula)
99:       .DebugOn = False
100:     end with
...
103: Sub Table1_KeyDown(keycode)
104:   If keycode = LeftFlipperKey Then FastFlips.FlipL True :  FastFlips.FlipUL True
105:   If keycode = RightFlipperKey Then FastFlips.FlipR True :  FastFlips.FlipUR True
106:     If keycode = PlungerKey Then Plunger.Pullback
107:     If keycode = LeftTiltKey Then PlaySound "nudge_left"
108:     If keycode = RightTiltKey Then PlaySound "nudge_right"
109:     If keycode = CenterTiltKey Then PlaySound "nudge_forward"
110:     If vpmKeyDown(keycode) Then Exit Sub
111: End Sub
112:
113: Sub Table1_KeyUp(ByVal keycode)
114:   If keycode = LeftFlipperKey Then FastFlips.FlipL False :  FastFlips.FlipUL False
115:     If keycode = RightFlipperKey Then FastFlips.FlipR False :  FastFlips.FlipUR False
116:     If keycode = PlungerKey Then Plunger.Fire:PlaySound "plunger",0,1,AudioPan(Plunger),0.25,0,0,1,AudioFade(Plunger)
117:     If vpmKeyUp(keycode) Then Exit Sub
118: End Sub
...
127: SolCallback(1) = "OutholeKick"
128: SolCallback(3) = "EMKicker"
129: SolCallback(4) = "solBoomerangKickout"
130: SolCallback(5) = "SpookHouseDropUp"
131: SolCallback(7) = "vpmSolSound ""Knocker"","
132: SolCallback(10) = "SolGI" 'PF GI
133: SolCallback(11) = "SolBackGenIllumin" 'BG GI
134: SolCallback(15) = "Flash15" 'boomerang flashers
135: SolCallback(16) = "SolWheelDrive"
136: SolCallBack(23) = "FastFlips.TiltSol"
137: SolCallback(25) = "Flash25" 'pops left
138: SolCallback(26) = "Flash26" 'pops right
139: SolCallback(27) = "Flash27" 'backmiddle
140: SolCallback(28) = "Flash28" 'cats
141: SolCallback(29) = "Flash29" 'ducks
142: SolCallback(30) = "Flash30" 'backleft/Ferris
143: SolCallback(31) = "Flash31" 'Cyclone Flasher
144: SolCallback(32) = "Flash32" 'SpookHouse
145:
146: Sub OutholeKick(enabled)
147:   If enabled Then
148:   Outhole.kick 65, 15
149:   Playsound SoundFX("BallRel",DOFContactors), 0, 1, AudioPan(Outhole), 0,0,0, 1, AudioFade(Outhole)
150:   End If
151: end Sub
152: Sub Outhole_Hit:PlaySound "drain", 0, 1, AudioPan(Outhole), 0,0,0, 1, AudioFade(Outhole):controller.switch(10) = 1:End Sub
153: Sub Outhole_unHit:Controller.Switch(10) = 0: End Sub
...
155: Dim empos, kForce
156: Sub EMKicker(Enabled)
157:     If Enabled Then
158:   kForce = 46.5 + (Rnd*(rnd*9.3))
159:     KSalida.Kick 0,kForce
160:     Playsound SoundFX("solenoid",DOFContactors), 0, 1, AudioPan(KSalida), 0,0,0, 1, AudioFade(KSalida)
161:         empos = 0
162:         emkickertimer.Enabled = 1
163:     End If
164: End Sub
...
185: Sub SolBackGenIllumin(Enabled)
186: If Enabled Then
187:   PlaySound"tickon" 'plays in BG sounds
188: Else
189:   PlaySound"tickoff" 'Plays in BG sounds
190: End If
191: End Sub
192:
193: Sub Flash15(Enabled)
194:   If Enabled Then
195:     Flash15a.State = 1
196:     Flash15b.State = 1
197:     Flash15c.State = 1
198:   Else
199:     Flash15a.State = 0
200:     Flash15b.State = 0
201:     Flash15c.State = 0
202:   End If
203: End Sub
...
205: Sub Flash25(enabled)
206:   If Enabled Then
207:     F25.State = 1
208:     F25b.State =1
209:   Else
210:     F25.State = 0
211:     F25b.State = 0
212:   End If
213: End Sub
...
225: Sub Flash27(enabled)
226:   If Enabled Then
227:     Flasher27p.image = "DomeOn"
228:     Flasher27p.material = "Orange FlashersOn"
229:     F27.State = 1
230:     F27b.State = 1
231:   Else
232:     Flasher27p.image = "DomeOff"
233:     Flasher27p.material = "Orange Flashers"
234:     F27.state = 0
235:     F27b.State = 0
236:   End If
237: End Sub
...
249: Sub Flash29(Enabled)
250:   If Enabled Then
251:     Flasher29p.image = "DomeOn"
252:     F29.State = 1
253:     F29b.State = 1
254:     F29c.State = 1
255:     F29d.State = 1
256:     Flasher29p.material = "Orange FlashersOn"
257:   Else
258:     Flasher29p.image = "DomeOff"
259:     F29.State = 0
260:     F29b.State = 0
261:     F29c.State = 0
262:     F29d.State = 0
263:     Flasher29p.material = "Orange Flashers"
264:   End If
265: End Sub
...
267: Sub Flash30(enabled)
268:   If Enabled Then
269:     Flasher30p.image = "DomeOn"
270:     Flasher30pb.image = "DomeOn"
271:     Flasher30p.material = "Orange FlashersOn"
272:     Flasher30pb.material = "Orange FlashersOn"
273:     F30.State = 1
274:     F30b.State =1
275:     F30c.State =1
276:     F30d.State =1
277:   Else
278:     Flasher30p.image = "DomeOff"
279:     Flasher30pb.image = "DomeOff"
280:     Flasher30p.material = "Orange Flashers"
281:     Flasher30pb.material = "Orange Flashers"
282:     F30.State = 0
283:     F30b.State = 0
284:     F30c.State = 0
285:     F30d.State = 0
286:   End If
287: End Sub
288:
289: Sub Flash31(enabled)
290:   If Enabled Then
291:     Flasher31p.image = "DomeOn"
292:     Flasher31p.material = "Blue Flasherson"
293:     F31.State = 1
294:     F31b.State = 1
295:   Else
296:     Flasher31p.image = "DomeOff"
297:     Flasher31p.material = "Blue Flashers"
298:     F31.State = 0
299:     F31b.State = 0
300:   End If
301: End Sub
...
305: Sub Flash32(enabled)
306:   If Enabled Then
307:   F32.State = 1
308:   F32b.State = 1
309:   F32c.State = 1
310:   Else
311:   F32.State = 0
312:   F32b.State = 0
313:   F32c.State = 0
314:   End If
315: End Sub
...
323: Sub SolGI(Enabled)
324:     If Enabled Then
325:       PlaySound"tickon" 'plays in BG sounds
326:       For each xx in GI:xx.State = 0:Next
327:       For each xx in GI2:xx.State = 0:Next
328:     Else
329:       For each xx in GI:xx.State = 1:Next
330:       For each xx in GI2:xx.State = 1:Next
331:       PlaySound"tickoff" 'plays in BG sounds
332:     End If
333: End Sub
...
380: SolCallback(sLRFlipper) = "SolRFlipper"
381: SolCallback(sLLFlipper) = "SolLFlipper"
382:
383: Sub SolLFlipper(Enabled)
384:     If Enabled Then
385:     PlaySound SoundFX("fx_flipperup",DOFFlippers), 0, 1, AudioPan(LeftFlipper), 0,0,0,1,AudioFade(LeftFlipper)
386:     LeftFlipper.RotateToEnd
387:     Else
388:     PlaySound SoundFX("fx_flipperDown",DOFFlippers), 0, 1, AudioPan(LeftFlipper), 0,0,0,1,AudioFade(LeftFlipper)
389:     LeftFlipper.RotateToStart
390:     End If
391: End Sub
392:
393: Sub SolRFlipper(Enabled)
394:     If Enabled Then
395:     PlaySound SoundFX("fx_flipperup",DOFFlippers), 0, 1, AudioPan(RightFlipper), 0,0,0,1,AudioFade(RightFlipper)
396:     RightFlipper.RotateToEnd
397:     Else
398:     PlaySound SoundFX("fx_flipperDown",DOFFlippers), 0, 1, AudioPan(RightFlipper), 0,0,0,1,AudioFade(RightFlipper)
399:     RightFlipper.RotateToStart
400:     End If
401: End Sub
...
538: Sub BumperIzquierda_Hit:vpmTimer.pulsesw 60:PlaySound SoundFX("bumper",DOFContactors), 0,1,AudioPan(BumperIzquierda),0,0,0,1,AudioFade(BumperIzquierda):End Sub
539: Sub BumperDerecha_Hit:vpmTimer.pulsesw 61:PlaySound SoundFX("bumper",DOFContactors), 0,1,AudioPan(BumperDerecha),0,0,0,1,AudioFade(BumperDerecha):End Sub
540: Sub BumperAbajo_Hit:vpmTimer.pulsesw 62:PlaySound SoundFX("bumper",DOFContactors), 0,1,AudioPan(BumperAbajo),0,0,0,1,AudioFade(BumperAbajo):End Sub
...
545: Sub LeftSlingShot_Slingshot
546:     vpmTimer.pulsesw 63
...
562: Sub RightSlingShot_Slingshot
563:     vpmTimer.pulsesw 64
...
583: Sub sw19_Hit():vpmTimer.pulsesw 19:Playsound "target", 0, 1, AudioPan(sw19), 0, Pitch(ActiveBall), 1, 0, AudioFade(sw19):End sub
584: Sub sw20_Hit():vpmTimer.pulsesw 20:Playsound "target", 0, 1, AudioPan(sw20), 0, Pitch(ActiveBall), 1, 0, AudioFade(sw20):End sub
585: Sub sw21_Hit():vpmTimer.pulsesw 21:Playsound "target", 0, 1, AudioPan(sw21), 0, Pitch(ActiveBall), 1, 0, AudioFade(sw21):End sub
586: 'Cats
587: Sub sw22_Hit():vpmTimer.pulsesw 22:Playsound "target", 0, 1, AudioPan(sw22), 0, Pitch(ActiveBall), 1, 0, AudioFade(sw22):End sub
588: Sub sw23_Hit():vpmTimer.pulsesw 23:Playsound "target", 0, 1, AudioPan(sw23), 0, Pitch(ActiveBall), 1, 0, AudioFade(sw23):End sub
589: Sub sw24_Hit():vpmTimer.pulsesw 24:Playsound "target", 0, 1, AudioPan(sw24), 0, Pitch(ActiveBall), 1, 0, AudioFade(sw24):End sub
590: Sub sw59_Hit():vpmTimer.pulsesw 25:Playsound "target", 0, 1, AudioPan(sw59), 0, Pitch(ActiveBall), 1, 0, AudioFade(sw59):End sub
...
595: Sub sw13_Hit:Controller.Switch(13) = 1:End Sub
596: Sub sw13_unHit: Controller.Switch(13) = 0:end Sub
597: Sub sw11_Hit:vpmtimer.pulsesw 11:End Sub
...
601: Sub Sw18_Hit:Sw18.Isdropped = True:PlaySound "DropTarget", 0, 1, AudioPan(sw18), 0, Pitch(ActiveBall), 1, 0, AudioFade(sw18):Controller.Switch(18) = 1:End Sub
602:
603: Sub SpookHouseDropUp(Enabled)
604:   If Enabled Then
605:   sw18.isDropped = 0
606:   Controller.Switch(18) = 0
607:   Playsound SoundFX("solenoid",DOFContactors), 0, 1, AudioPan(sw18), 0, 0, 1, 0, AudioFade(sw18)
608:   End If
609: End Sub
610:
611: Sub SolBoomerangKickOut(enabled)
612:   Kicker2.enabled = 0
613:   Sw13.kick 325, 32
614:   Kicker2.timerenabled = 1
615:   Playsound SoundFX("boomerang_kick",DOFContactors), 0, 1, AudioPan(Sw13), 0, 0, 1, 0, AudioFade(Sw13)
616: End Sub
...
618: Sub Kicker2_Hit:Playsound "Scoop_Enter", 0, 1, AudioPan(Kicker2), 0, 0, 1, 0, AudioFade(Kicker2):End Sub
619: Sub Kicker1_Hit:Playsound "Kicker2", 0, 1, AudioPan(Kicker1), 0, 0, 1, 0, AudioFade(Kicker1):End Sub
...
629: Sub ShooterLane_Hit:Controller.Switch(25) = 1:End Sub
630: Sub ShooterLane_Unhit:Controller.Switch(25) = 0:PlaySound "ballroll":End Sub
631:
632: 'Pasillos
633: Sub sw53_Hit:Controller.Switch(53) = 1:PlaySound "Sensor", 0, 1, AudioPan(sw53), 0, 0, 1, 0, AudioFade(sw53): End Sub
634: Sub sw53_Unhit:Controller.Switch(53) = 0:End Sub
635: Sub sw54_Hit:Controller.Switch(54) = 1:PlaySound "Sensor", 0, 1, AudioPan(sw54), 0, 0, 1, 0, AudioFade(sw54): End Sub
636: Sub sw54_Unhit:Controller.Switch(54) = 0:End Sub
637: Sub sw55_Hit:Controller.Switch(55) = 1:PlaySound "Sensor", 0, 1, AudioPan(sw55), 0, 0, 1, 0, AudioFade(sw55): End Sub
638: Sub sw55_Unhit:Controller.Switch(55) = 0:End Sub
639: Sub sw56_Hit:Controller.Switch(56) = 1:PlaySound "Sensor", 0, 1, AudioPan(sw56), 0, 0, 1, 0, AudioFade(sw56): End Sub
640: Sub sw56_Unhit:Controller.Switch(56) = 0:End Sub
641: Sub sw14_Hit:Controller.Switch(14) = 1:PlaySound "Sensor", 0, 1, AudioPan(sw14), 0, 0, 1, 0, AudioFade(sw14): End Sub
642: Sub sw14_Unhit:Controller.Switch(14) = 0:End Sub
643: Sub sw15_Hit:Controller.Switch(15) = 1:PlaySound "Sensor", 0, 1, AudioPan(sw15), 0, 0, 1, 0, AudioFade(sw15): End Sub
644: Sub sw15_Unhit:Controller.Switch(15) = 0:End Sub
645: Sub sw16_Hit:Controller.Switch(16) = 1:PlaySound "Sensor", 0, 1, AudioPan(sw16), 0, 0, 1, 0, AudioFade(sw16): End Sub
646: Sub sw16_Unhit:Controller.Switch(16) = 0:End Sub
647: Sub Sw17_Hit:Controller.Switch(17) = 1:PlaySound "Sensor", 0, 1, AudioPan(sw17), 0, 0, 1, 0, AudioFade(sw17): End Sub 'Entrada ferris wheel
648: Sub Sw17_UnHit:Controller.Switch(17) = 0:End Sub
649: Sub Sw31_Hit:Controller.Switch(31) = 1:PlaySound"comet_spinner", 0, 1, AudioPan(sw31), 0, 0, 1, 0, AudioFade(sw31):End Sub'Entrada rampa comet
650: Sub Sw31_UnHit
651:   Controller.Switch(31) = 0
652:   If ActiveBall.VelY < 0 Then
653:     PlaySound"comet_ramp", 0, 1, AudioPan(sw31), 0, 0, 1, 0, AudioFade(sw31)
654:   Else
655:     StopSound"comet_ramp"
656:   End If
657: End Sub
658: Sub Sw32_Hit:Controller.Switch(32) =1:SwitchWire2.objRotZ = -15:End Sub                          'Score rampa comet
659: Sub Sw32_UnHit:Controller.Switch(32) =0:SwitchWire2.objRotZ = 0:End Sub
660: Sub Sw34_Hit:Controller.Switch(34) =1:SwitchWire1.objRotZ = -15:End Sub                          'Score rampa cyclone
661: Sub Sw34_UnHit:Controller.Switch(34) =0:SwitchWire1.objRotZ = 0:End Sub
662: Sub Sw35_Hit:VPMTimer.PulseSw 35:PlaySound "Rubber_hit_3", 0, 1, AudioPan(ActiveBall), 0, Pitch(ActiveBall), 1, 0, AudioFade(ActiveBall): End Sub 'Sensores en varias gomas
663: Sub Sw36_Hit:VPMTimer.PulseSw 36:PlaySound "Rubber_hit_2", 0, 1, AudioPan(ActiveBall), 0, Pitch(ActiveBall), 1, 0, AudioFade(ActiveBall): End Sub
664: Sub Sw37_Hit:VPMTimer.PulseSw 37:PlaySound "Rubber_hit_1", 0, 1, AudioPan(ActiveBall), 0, Pitch(ActiveBall), 1, 0, AudioFade(ActiveBall): End Sub
665:
666: 'SkillShot
667: Sub sw26_Hit():VPMTimer.PulseSw 26:PlaySound "Sensor", 0, 1, AudioPan(sw26), 0, Pitch(ActiveBall), 1, 0, AudioFade(sw26): End Sub
668: Sub sw27_Hit():VPMTimer.PulseSw 27:PlaySound "Sensor", 0, 1, AudioPan(sw27), 0, Pitch(ActiveBall), 1, 0, AudioFade(sw27): End Sub
669: Sub sw28_Hit():VPMTimer.PulseSw 28:PlaySound "Sensor", 0, 1, AudioPan(sw28), 0, Pitch(ActiveBall), 1, 0, AudioFade(sw28): End Sub
670: Sub sw29_Hit():VPMTimer.PulseSw 29:PlaySound "Sensor", 0, 1, AudioPan(sw29), 0, Pitch(ActiveBall), 1, 0, AudioFade(sw29): End Sub
671: Sub sw30_Hit():VPMTimer.PulseSw 30:PlaySound "Sensor", 0, 1, AudioPan(sw30), 0, Pitch(ActiveBall), 1, 0, AudioFade(sw30): End Sub
...
678: Sub SpinWheel(aNewPos, aSpeed, aLastPos)
679:      If aNewPos <> aLastPos then
680:     MysteryWheel.Rotz = aNewPos
681:      End If
682: End Sub
...
711: Sub Trigger2_Hit
712: ' PlaySound "knocker" 'for testing
713:   PlaySound"ferris_hit1", 0, 1, AudioPan(Trigger2), 0, 0, 1, 0, AudioFade(Trigger2)
714:   activeball.vely=0
715:   activeball.velz=0
716:   activeball.x=xphstart
717:   activeball.y=yphstart
718:   activeball.z=zphstart
719:   Set Tball = Activeball
720:   tcount = 0
721:   WheelHit.enabled = 1
722:   Trigger2.enabled = 0
723: End Sub
...
755: Sub SolWheelDrive(enabled)
756:     if enabled then
757:         FWTimer.Enabled = 1
758:     PlaySound"motor", -1, 1, AudioPan(Trigger2), 0, 0, 1, 0, AudioFade(Trigger2)
759:     else
760:         FWTimer.Enabled = 0
761:     StopSound"motor"
762:     end if
763: End Sub
764:
765: Sub FWTimer_Timer
766:     RedWheel.RotX = (RedWheel.RotX + 1) MOD 360
767:
768:   If  RedWheel.RotX >15 and RedWheel.RotX <65 Then
769:     FerrisBlockedWall.isdropped = 1
770:   elseif RedWheel.RotX >105 and RedWheel.RotX <150 Then
771:     FerrisBlockedWall.isdropped = 1
772:   elseif RedWheel.RotX >200 and RedWheel.RotX <240 Then
773:     FerrisBlockedWall.isdropped = 1
774:   elseif RedWheel.RotX >285 and RedWheel.RotX <330 Then
775:     FerrisBlockedWall.isdropped = 1
776:   else
777:     FerrisBlockedWall.isdropped = 0
778:   End If
779: End Sub
```

Reading: the table runs `cycln_l5` through S11.VBS with `HandleMechanics = 0` and sets the Country jumper DIP 0 to
`&H80`. Its solenoid callbacks bind 1, 3, 4, 5, 7, 10, 11, 15, 16, 23 and 25-32; none binds 2, 6, 8, 9, 12, 17-22.
The Mystery Wheel stepper coils 13 and 14 drive the `cvpmMech` (`.Sol1 = 14`, `.Sol2 = 13`), which writes switch 41
closed over steps 0-180 of its 360. Bumpers pulse 60, 61 and 62, slingshots 63 and 64. `sw59_Hit` pulses 25, the
shooter-lane switch, instead of 59; no line of the script writes switch 59.
