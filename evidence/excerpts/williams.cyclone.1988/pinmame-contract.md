# Pinned PinMAME source - the Cyclone driver contract

`reviewed: true`; copied by the curator from the pinned checkout on 2026-10-31
`source: https://github.com/vpinball/pinmame at 46e1a01a0f73dc5ce163d98db1ae435883ecc450`

Lines are quoted verbatim with their line numbers; `...` separates non-adjacent ranges.

## src/wpc/driver.c

```c
2767: DRIVER(cycln,l1)        //S11-564:  02/88 W Cyclone (L-1)
2768: DRIVER(cycln,l4)        //          02/88 W Cyclone (L-4)
2769: DRIVER(cycln,l5)        //          02/88 W Cyclone (L-5)
```

## src/wpc/s11games.c

```c
33: #define INITGAME(name, gen, disp, mux, flip, db, gs1) \
34: static core_tGameData name##GameData = { \
35:   gen, disp, {flip,0,0,0,0,db,gs1}, NULL, {{0}}, {mux} }; \
36: static void init_##name(void) { core_gameData = &name##GameData; }
...
500: /*--------------------
501: / Cyclone 2/88
502: /--------------------*/
503: INITGAME(cycln, GEN_S11B,s11_dispS11b1, 12, FLIP_SWNO(57,58), 0,0)
504: S11_ROMSTART48(cycln,l5,"cycl_u26.l5", CRC(9ab15e12) SHA1(406f3212269dc42de1f3fabcf179958adbd4b5e8),
505:                         "cycl_u27.l5", CRC(c4b6aac0) SHA1(9058e450dbf9d198b1746c258b0e437d7ee844e9))
506: S11XS_SOUNDROM88(       "cycl_u21.l1", CRC(d4f69a7c) SHA1(da0ce27d92b22583be54a41fc8083cee803c987a),
507:                         "cycl_u22.l1", CRC(28dc8f13) SHA1(bccce3a9b6b2f52da919c6df8db07e5e3de12657))
508: S11CS_SOUNDROM88(       "cycl_u4.l5",  CRC(d04b663b) SHA1(f54c6df08ec73b733cfeb2a989e44e5c04da3d9e),
509:                         "cycl_u19.l1", CRC(a20f6519) SHA1(63ded5f76133340fa31d4fe65420f4465866fb85))
510: S11_ROMEND
511: #define input_ports_cycln input_ports_s11
512: CORE_GAMEDEF(cycln, l5, "Cyclone (L-5)", 1988, "Williams", s11_mS11BS,0)
513:
514: S11_ROMSTART48(cycln,l4,"cycl_u26.l4", CRC(7da30995) SHA1(3774004df22ddce508fe0604c0349df3edd513b4),
515:                         "cycl_u27.l4", CRC(8874d65f) SHA1(600e2e8cd21faf8999ebef06fb08c43a1eb2ffd7))
516: S11XS_SOUNDROM88(       "cycl_u21.l1", CRC(d4f69a7c) SHA1(da0ce27d92b22583be54a41fc8083cee803c987a),
517:                         "cycl_u22.l1", CRC(28dc8f13) SHA1(bccce3a9b6b2f52da919c6df8db07e5e3de12657))
518: S11CS_SOUNDROM88(       "cycl_u4.l5",  CRC(d04b663b) SHA1(f54c6df08ec73b733cfeb2a989e44e5c04da3d9e),
519:                         "cycl_u19.l1", CRC(a20f6519) SHA1(63ded5f76133340fa31d4fe65420f4465866fb85))
520: S11_ROMEND
521: CORE_CLONEDEF(cycln, l4, l5, "Cyclone (L-4)", 1988, "Williams", s11_mS11BS,0)
522:
523: S11_ROMSTART48(cycln,l1,"cycl_u26.l1", CRC(b6b8354e) SHA1(ae07fb74ce340cf5c520ce7faea636c234c6e4db),
524:                         "cycl_u27.l1", CRC(81340fcd) SHA1(9ec6754b25f80919f8fe0a2ff9136b37ca8c1aa0))
525: S11XS_SOUNDROM88(       "cycl_u21.l1", CRC(d4f69a7c) SHA1(da0ce27d92b22583be54a41fc8083cee803c987a),
526:                         "cycl_u22.l1", CRC(28dc8f13) SHA1(bccce3a9b6b2f52da919c6df8db07e5e3de12657))
527: S11CS_SOUNDROM88(       "cycl_u4.l5",  CRC(d04b663b) SHA1(f54c6df08ec73b733cfeb2a989e44e5c04da3d9e),
528:                         "cycl_u19.l1", CRC(a20f6519) SHA1(63ded5f76133340fa31d4fe65420f4465866fb85))
529: S11_ROMEND
530: CORE_CLONEDEF(cycln, l1, l5, "Cyclone (L-1)", 1988, "Williams", s11_mS11BS,0)
```

Read against the macro: generation `GEN_S11B`; display layout `s11_dispS11b1`; `sxx.muxSol` 12, the A/C select
relay; `hw.flippers = FLIP_SWNO(57,58)`, the left button copied into matrix switch 57 and the right into 58, with no
`FLIP_SOL`; `hw.display` 0; `gameSpecific1` 0 (no `S11_MUXSW2`, `S11_SNDOVERLAY`, `S11_PRINTERLINE` or `S11_RKMUX`). The
`INITGAME` macro fills no `sxx.ssSw`, so every special-solenoid switch slot is 0 and no switch drives 17-22 from
PinMAME's side: the ROM fires them through the PIA control lines (`setSSSol`). `hw.custSol` and `hw.lampCol` are 0.
The three drivers share this game data and the U21/U22 and U4/U19 sound ROMs; they differ only in the U26 and U27
game ROMs.

## src/wpc/s11.c

```c
66: core_tLCDLayout s11_dispS11a[] = {
67:   DISP_SEG_7(0,0,CORE_SEG16),DISP_SEG_7(0,1,CORE_SEG16),
68:   DISP_SEG_7(1,0,CORE_SEG8), DISP_SEG_7(1,1,CORE_SEG8) ,{0}
69: };
...
180:   if (locals.ssEn) { // set gameon and special solenoids
181:     locals.solenoids |= CORE_SOLBIT(S11_GAMEONSOL);
182:
183: #ifdef PROC_SUPPORT
184:     if (!coreGlobals.p_rocEn) {
185: #endif
186: #ifdef LISY_SUPPORT
187:     if (0) { //not with LISY support
188: #endif
189:
190:     /*-- special solenoids updated based on switches         -- */
191:     /*-- but only when no P-ROC, otherwise special solenoids -- */
192:     /*-- lock on when controlled by direct switches          -- */
193:     for (ii = 0; ii < 6; ii++) {
194:       if (core_gameData->sxx.ssSw[ii]) {
195:         int switchState = core_getSw(core_gameData->sxx.ssSw[ii]);
196:         if (switchState)
197:           locals.solenoids |= CORE_SOLBIT(CORE_FIRSTSSSOL+ii);
198:         core_write_pwm_output(CORE_MODOUT_SOL0 + CORE_FIRSTSSSOL + ii - 1, 1, switchState ? 1 : 0);
199:       }
200:     }
...
371: /*-- Jumper W7 --*/
372: static READ_HANDLER (pia2a_r) { return core_getDip(0)<<7; }
...
537: static void setSSSol(int data, int solNo) {
538:                                     /*    WMS          DE */
539:   static const int ssSolNo[2][6] = {{5,4,1,2,0,3},{3,4,5,1,0,2}};
540:   int bit = CORE_SOLBIT(CORE_FIRSTSSSOL + ssSolNo[locals.deGame][solNo]);
541:   if (~data & 1)
542:     locals.switchedSol |= bit;
543:   else
544:     locals.switchedSol &= ~bit;
545:   if (locals.ssEn & (~data & 1))
546:   {
547:     coreGlobals.pulsedSolState |= bit;
548:     locals.solenoids |= bit;
549:     core_write_pwm_output(CORE_MODOUT_SOL0 + CORE_FIRSTSSSOL + ssSolNo[locals.deGame][solNo] - 1, 1, 1);
550:   }
551:   else
552:   {
553:     coreGlobals.pulsedSolState &= ~bit;
554:     core_write_pwm_output(CORE_MODOUT_SOL0 + CORE_FIRSTSSSOL + ssSolNo[locals.deGame][solNo] - 1, 1, 0);
555:   }
556: }
557:
558: static void updsol(void) {
559:   /* set new solenoids, preserve SSSol */
560:   coreGlobals.pulsedSolState = (coreGlobals.pulsedSolState & 0x00ff0000)
561:                              | (locals.solBits2 << 8)
562:                              | (locals.solBits1     );
563:
564:   /* if game has a MUX and it's active... */
565:   if ((core_gameData->sxx.muxSol) &&
566:       (coreGlobals.pulsedSolState & CORE_SOLBIT(core_gameData->sxx.muxSol))) {
567:     if (core_gameData->hw.gameSpecific1 & S11_RKMUX) /* special case WMS Road Kings */
568:       coreGlobals.pulsedSolState = (coreGlobals.pulsedSolState & 0x00ff8fef)      |
569:                                   ((coreGlobals.pulsedSolState & 0x00000010)<<20) |
570:                                   ((coreGlobals.pulsedSolState & 0x00007000)<<13);
571:     else
572:       coreGlobals.pulsedSolState = (coreGlobals.pulsedSolState & 0x00ffff00) |
573:                                    (coreGlobals.pulsedSolState << 24);
574:   }
575:
576:   // Simple implementation of modulated solenoids by pushing the pulsed state taking in account muxing to the physics emulation
577:   core_write_pwm_output_8b(CORE_MODOUT_SOL0     ,  coreGlobals.pulsedSolState        & 0x0FF); // Standard 'A'-side
578:   core_write_pwm_output_8b(CORE_MODOUT_SOL0 +  8, (coreGlobals.pulsedSolState >> 8)  & 0x0FF); // Standard
579:   // 17..22 are 6 special sol, processed either in fake VBlank if switch driven, or in setSSSol if PIA driven
580:   // 23 is GameOn, processed in pia0cb2_w (also filters out switched solenoids)
581:   core_write_pwm_output_8b(CORE_MODOUT_SOL0 + 24, (coreGlobals.pulsedSolState >> 24) & 0x0FF); // Standard 'C'-side (Muxed solenoids)
582:
583:   locals.solenoids |= coreGlobals.pulsedSolState;
584: }
...
611: static WRITE_HANDLER(pia0cb2_w) {
612:   locals.ssEn = !data;
613:   coreGlobals.pulsedSolState = (coreGlobals.pulsedSolState & ~(1 << (S11_GAMEONSOL - 1))) | (data ? 0 : (1 << (S11_GAMEONSOL - 1)));
614:   core_write_pwm_output(CORE_MODOUT_SOL0 + S11_GAMEONSOL - 1, 1, locals.ssEn ? 1 : 0);
615:   core_write_pwm_output(CORE_MODOUT_SOL0 + CORE_FIRSTSSSOL - 1, 6, locals.ssEn ? locals.switchedSol : 0);
616: }
617:
618: static WRITE_HANDLER(pia1ca2_w) { setSSSol(data, 0); }
619: static WRITE_HANDLER(pia1cb2_w) { setSSSol(data, 1); }
620: static WRITE_HANDLER(pia3ca2_w) { setSSSol(data, 2); }
621: static WRITE_HANDLER(pia3cb2_w) { setSSSol(data, 3); }
622: static WRITE_HANDLER(pia4ca2_w) { setSSSol(data, 4); }
623: static WRITE_HANDLER(pia4cb2_w) { setSSSol(data, 5); }
...
644: static READ_HANDLER(pia4a_r)
645: {
646: #if defined(LISY_SUPPORT)
647:   //get the switches from LISY_mini
648:   lisy_w_switch_handler();
649: #endif
650:   return core_getSwCol(locals.swCol);
651: }
...
796:
797:   /*-- Generate interupts for diganostic keys --*/
798:   cpu_set_nmi_line(0, core_getSw(S11_SWCPUDIAG) ? ASSERT_LINE : CLEAR_LINE);
799:   sndbrd_0_diag(core_getSw(S11_SWSOUNDDIAG));
800:   if ((core_gameData->hw.gameSpecific1 & S11_MUXSW2) && core_gameData->sxx.muxSol)
801:     core_setSw(2, core_getSol(core_gameData->sxx.muxSol));
...
727:  /* PA7       (I) Jumper W7 */
...
875:
876:   // Initialize outputs
877:   coreGlobals.nLamps = 64 + core_gameData->hw.lampCol * 8;
878:   core_set_pwm_output_type(CORE_MODOUT_LAMP0, coreGlobals.nLamps, CORE_MODOUT_BULB_44_18V_DC_S11);
879:   coreGlobals.nSolenoids = CORE_FIRSTCUSTSOL - 1 + core_gameData->hw.custSol;
880:   core_set_pwm_output_type(CORE_MODOUT_SOL0, coreGlobals.nSolenoids, CORE_MODOUT_SOL_2_STATE);
881:   core_set_pwm_output_type(CORE_MODOUT_SOL0 + S11_GAMEONSOL - 1, 1, CORE_MODOUT_PULSE);
...
956:   else if (strncasecmp(gn, "cycln_", 6) == 0) { // Cyclone
957:      core_set_pwm_output_type(CORE_MODOUT_SOL0 +  9 - 1, 1, CORE_MODOUT_BULB_89_25V_DC_S11);
958:      core_set_pwm_output_type(CORE_MODOUT_SOL0 + 10 - 1, 1, CORE_MODOUT_BULB_44_6_3V_AC_REV); // Playfield GI output
959:      core_set_pwm_output_type(CORE_MODOUT_SOL0 + 11 - 1, 1, CORE_MODOUT_BULB_44_6_3V_AC_REV); // Backbox GI output
960:      core_set_pwm_output_type(CORE_MODOUT_SOL0 + 15 - 1, 1, CORE_MODOUT_BULB_89_25V_DC_S11);
961:      core_set_pwm_output_type(CORE_MODOUT_SOL0 + 25 - 1, 8, CORE_MODOUT_BULB_89_25V_DC_S11); // 8 muxed flasher outputs (Mux relay is solenoid #12)
962:   }
```

`s11_dispS11a` publishes, in LibPinMAME index order, player 1 (16-segment, segment start 1), player 2 (16-segment, 9),
player 3 (8-segment numeric, 21) and player 4 (8-segment numeric, 29), seven digits each (`DISP_SEG_7`).
`setSSSol`'s `ssSolNo` WMS row maps PIA lines 0-5 to specials 17 + {5,4,1,2,0,3}. `updsol` copies the low byte to
25-32 while the mux solenoid (12) is set, and `nSolenoids` is `CORE_FIRSTCUSTSOL - 1 + 0` = 50; `nLamps` is 64.

## src/wpc/s11.h

```c
89: #define S11_GAMEONSOL 23
...
96: #define S11_SWADVANCE     -7
97: #define S11_SWUPDN        -6
98: #define S11_SWCPUDIAG     -5
99: #define S11_SWSOUNDDIAG   -4
...
108: extern core_tLCDLayout s11_dispS9[], s11_dispS11[], s11_dispS11a[], s11_dispS11b2[];
109: #define s11_dispS11b1 s11_dispS11a
```

## src/wpc/gen.h

```c
19: #define GEN_S11X        U64(0x0000000000100) /* S11C sound board */
20: #define GEN_S11A        GEN_S11X
21: #define GEN_S11B        GEN_S11X
```

## src/wpc/core.h

```c
159: #define FLIP_SWNO(l,r) (((l)<<8)|(r)|FLIP_SW(FLIP_L))
...
300: #define CORE_FIRSTCUSTSOL  51
301: #define CORE_FIRSTLFLIPSOL 45
302: #define CORE_FIRSTSIMSOL   49
303: #define CORE_MAXSOL        64
304:
305: #define CORE_SSFLIPENSOL  23
306: #define CORE_FIRSTSSSOL   17
...
332: #define CORE_FLIPPERSWCOL                11 /* internal array number */
```

## src/wpc/core.c

```c
1832:     /*-- set switches in matrix for non-fliptronic games --*/
1833:     if (FLIP_SWL(flip)) core_setSw(FLIP_SWL(flip), swFlip & CORE_SWLLFLIPBUTBIT);
1834:     if (FLIP_SWR(flip)) core_setSw(FLIP_SWR(flip), swFlip & CORE_SWLRFLIPBUTBIT);
1835: #ifdef PROC_SUPPORT
1836:   }
1837: #endif
1838:
1839:   /*-- fake solenoids if not CPU controlled --*/
1840:   if ((flip & FLIP_SOL(FLIP_L)) == 0) {
1841:     coreGlobals.solenoids2 &= 0xffffff00;
1842:     if (flipEn) {
1843:       if (swFlip & CORE_SWLLFLIPBUTBIT) coreGlobals.solenoids2 |= CORE_LLFLIPSOLBITS;
1844:       if (swFlip & CORE_SWLRFLIPBUTBIT) coreGlobals.solenoids2 |= CORE_LRFLIPSOLBITS;
1845:     }
1846:   }
...
2664: int core_getDip(int dipBank) {
2665: #if defined(VPINMAME) || defined(LIBPINMAME)
2666:   return vp_getDIP(dipBank);
2667: #else /* VPINMAME */
2668:   return (readinputport(CORE_COREINPORT+1+dipBank/2)>>((dipBank & 0x01)*8))&0xff;
2669: #endif /* VPINMAME */
2670: }
```

## src/memory.h

```c
125: #define READ_HANDLER(name)		data8_t  name(UNUSEDARG offs_t offset)
```

`FLIP_SWNO(57,58)` sets `FLIP_SW(FLIP_L)` only, so `locals.flipMask` holds the two lower button bits: core_updateSw
copies public 84 (left button) into 57 and 82 (right button) into 58 on every update and, with no `FLIP_SOL`, fabricates
`CORE_LLFLIPSOLBITS` (47/48) and `CORE_LRFLIPSOLBITS` (45/46) from them while the flipper enable is on.

`pia2a_r` returns `core_getDip(0)<<7` through an 8-bit `data8_t` handler, and in LibPinMAME and VPinMAME builds
`core_getDip` returns the host's DIP value unchanged, so only bit 0 of DIP 0 reaches PIA2 PA7 (Jumper W7): a host
value of 1 reads PA7 = 1, while 0 and `&H80` (shifted to 0x4000 and truncated to 0x00) both read PA7 = 0.
