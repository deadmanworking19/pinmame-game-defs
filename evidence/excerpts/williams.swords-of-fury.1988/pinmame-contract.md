# Pinned PinMAME source contract

Revision: 97aa922bf8e4b6970126192ec1ac1fb0305a4f62. Literal numbered source regions retained by the runtime researcher and checked by primary; header locators identify their original files. No ROM bytes.

The same pinned `src/wpc/s11.h`, line 109, defines the selected layout alias literally:

```c
#define s11_dispS11b1 s11_dispS11a
```

```c
src/wpc/s11games.c:33-47
33: #define INITGAME(name, gen, disp, mux, flip, db, gs1) \
34: static core_tGameData name##GameData = { \
35:   gen, disp, {flip,0,0,0,0,db,gs1}, NULL, {{0}}, {mux} }; \
36: static void init_##name(void) { core_gameData = &name##GameData; }
37:
38: #define INITGAMEFULL(name, gen, disp, mux, flip, db, gs1, gs2, sc, ss17,ss18,ss19,ss20,ss21,ss22) \
39: static core_tGameData name##GameData = { \
40:   gen, disp, {flip,0,0,0,0,db,gs1,gs2}, NULL, {{0}}, {mux,{ss17,ss18,ss19,ss20,ss21,ss22}}}; \
41: static void init_##name(void) { core_gameData = &name##GameData; hc55516_set_sample_clock(0, sc); }
42:
43: S11_INPUT_PORTS_START(s11, 1) S11_INPUT_PORTS_END
44:
45: static core_tLCDLayout disp16oneline[] = { \
46:   {0,0,0,16,CORE_SEG16},{0,33,20,16,CORE_SEG16}, {0}
47: };

src/wpc/s11games.c:590-640
590: /--------------------*/
591: // tournament MOD exists (allentownpinball)
592: INITGAME(swrds, GEN_S11B, s11_dispS11b1,12, FLIP_SWNO(58,60),0,0)
593: S11_ROMSTART48(swrds,l2,"swrd_u26.l2", CRC(c036f4ff) SHA1(a86840dbc117774aeca695ded1ab3ec76e134325),
594:                         "swrd_u27.l2", CRC(33b0fb5a) SHA1(a55bdfe20b1c869eae52d3be75df1c550d0b20f5))
595: S11XS_SOUNDROM88(       "swrd_u21.l1", CRC(ee8b0a64) SHA1(c2c52059a9a5f7c0abcfdd76cfc6d5b5451f7d1e),
596:                         "swrd_u22.l1", CRC(73dcdbb0) SHA1(66f5b3804442a1742b6fb3cccf539c4df956b3f2))
597: S11CS_SOUNDROM88(       "swrd_u4.l1",  CRC(272b509c) SHA1(756d3783f664ca1c41dd1d12032330b74c3f89ea),
598:                         "swrd_u19.l1", CRC(a22f84fa) SHA1(1731e86e85cca2d283512d5048c787df3970c9c5))
599: S11_ROMEND
600: #define input_ports_swrds input_ports_s11
601: CORE_GAMEDEF(swrds, l2, "Swords of Fury (L-2)", 1988, "Williams", s11_mS11BS, 0)
602:
603: // single u27 rom that upgrades L1 to German Language Text L2 (labeled as G2), u26 was same rom content as swrd_u26.l1 (was also labeled as REV1)
604:
605: S11_ROMSTART48(swrds,lg2,"swrd_u26.l1", CRC(e7a54874) SHA1(9f3486a0eed32ab0919805bed771ffd214a78967),
606:                          "swrd_u27g.l2",CRC(ef7194d4) SHA1(45b4fc316b603921fdafaf2638a46a94e6efc190))
607: S11XS_SOUNDROM88(        "swrd_u21.l1", CRC(ee8b0a64) SHA1(c2c52059a9a5f7c0abcfdd76cfc6d5b5451f7d1e),
608:                          "swrd_u22.l1", CRC(73dcdbb0) SHA1(66f5b3804442a1742b6fb3cccf539c4df956b3f2))
609: S11CS_SOUNDROM88(        "swrd_u4.l1",  CRC(272b509c) SHA1(756d3783f664ca1c41dd1d12032330b74c3f89ea),
610:                          "swrd_u19.l1", CRC(a22f84fa) SHA1(1731e86e85cca2d283512d5048c787df3970c9c5))
611: S11_ROMEND
612: CORE_CLONEDEF(swrds, lg2, l2, "Swords of Fury (LG-2 German)", 1988, "Williams", s11_mS11BS, 0) // actually reports as L-2, not LG-2 (on chiplabel said G2)
613:
614: S11_ROMSTART48(swrds,l1,"swrd_u26.l1", CRC(e7a54874) SHA1(9f3486a0eed32ab0919805bed771ffd214a78967),
615:                         "swrd_u27.l1", CRC(885dc3d6) SHA1(26463efb476c0bbfc3cb49b450167c4a985672bf))
616: S11XS_SOUNDROM88(       "swrd_u21.l1", CRC(ee8b0a64) SHA1(c2c52059a9a5f7c0abcfdd76cfc6d5b5451f7d1e),
617:                         "swrd_u22.l1", CRC(73dcdbb0) SHA1(66f5b3804442a1742b6fb3cccf539c4df956b3f2))
618: S11CS_SOUNDROM88(       "swrd_u4.l1",  CRC(272b509c) SHA1(756d3783f664ca1c41dd1d12032330b74c3f89ea),
619:                         "swrd_u19.l1", CRC(a22f84fa) SHA1(1731e86e85cca2d283512d5048c787df3970c9c5))
620: S11_ROMEND
621: CORE_CLONEDEF(swrds, l1, l2, "Swords of Fury (L-1)", 1988, "Williams", s11_mS11BS, 0)
622:
623: S11_ROMSTART48(swrds,rr1,"SWRD_U26wSound.RRV1",CRC(DE498207) SHA1(1ece64e6aedde44bca26beb163ac64d9948fcecf),
624:                         "SWRD_U27.RRV1",       CRC(3746F3DE) SHA1(07385b904a7fdf29292ed59185f4c1affe0000d8))
625: S11XS_SOUNDROM88(       "swrd_u21.l1", CRC(ee8b0a64) SHA1(c2c52059a9a5f7c0abcfdd76cfc6d5b5451f7d1e),
626:                         "swrd_u22.l1", CRC(73dcdbb0) SHA1(66f5b3804442a1742b6fb3cccf539c4df956b3f2))
627: S11CS_SOUNDROM88(       "swrd_u4.l1",  CRC(272b509c) SHA1(756d3783f664ca1c41dd1d12032330b74c3f89ea),
628:                         "swrd_u19.l1", CRC(a22f84fa) SHA1(1731e86e85cca2d283512d5048c787df3970c9c5))
629: S11_ROMEND
630: CORE_CLONEDEF(swrds, rr1, l2, "Swords of Fury (Richrom/Lionman MOD V1)", 2026, "Williams / Frisbez", s11_mS11BS, 0)
631:
632: S11_ROMSTART48(swrds,rr1b,"SWRD_U26.RRV1",CRC(B8EFED27) SHA1(77b448fbd6d4546c2088344d91c110c1e6df3e00),
633:                         "SWRD_U27.RRV1",  CRC(3746F3DE) SHA1(07385b904a7fdf29292ed59185f4c1affe0000d8))
634: S11XS_SOUNDROM88(       "swrd_u21.l1", CRC(ee8b0a64) SHA1(c2c52059a9a5f7c0abcfdd76cfc6d5b5451f7d1e),
635:                         "swrd_u22.l1", CRC(73dcdbb0) SHA1(66f5b3804442a1742b6fb3cccf539c4df956b3f2))
636: S11CS_SOUNDROM88(       "swrd_u4.l1",  CRC(272b509c) SHA1(756d3783f664ca1c41dd1d12032330b74c3f89ea),
637:                         "swrd_u19.l1", CRC(a22f84fa) SHA1(1731e86e85cca2d283512d5048c787df3970c9c5))
638: S11_ROMEND
639: CORE_CLONEDEF(swrds, rr1b, l2, "Swords of Fury (Richrom/Lionman MOD V1 / No Swords Sounds)", 2026, "Williams / Frisbez", s11_mS11BS, 0)
640:

src/wpc/s11.c:60-72
60: };
61: core_tLCDLayout s11_dispS11[] = {
62:   DISP_SEG_7(0,0,CORE_SEG16),DISP_SEG_7(0,1,CORE_SEG16),
63:   DISP_SEG_7(1,0,CORE_SEG8), DISP_SEG_7(1,1,CORE_SEG8),
64:   {2,8,0,1,CORE_SEG7S},{2,10,8,1,CORE_SEG7S}, {2,2,20,1,CORE_SEG7S},{2,4,28,1,CORE_SEG7S}, {0}
65: };
66: core_tLCDLayout s11_dispS11a[] = {
67:   DISP_SEG_7(0,0,CORE_SEG16),DISP_SEG_7(0,1,CORE_SEG16),
68:   DISP_SEG_7(1,0,CORE_SEG8), DISP_SEG_7(1,1,CORE_SEG8) ,{0}
69: };
70: core_tLCDLayout s11_dispS11b2[] = {
71:   DISP_SEG_16(0,CORE_SEG16),DISP_SEG_16(1,CORE_SEG16),{0}
72: };

src/wpc/s11.c:178-221
178:   }
179:   /*-- solenoids --*/
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
201: #if defined(PROC_SUPPORT) || defined(LISY_SUPPORT)
202:     }
203: #endif
204:   }
205:   locals.solsmooth[locals.vblankCount % S11_SOLSMOOTH] = locals.solenoids;
206: #if !defined(PROC_SUPPORT) && !defined(LISY_SUPPORT)
207:  #if S11_SOLSMOOTH != 2
208:  #  error "Need to update smooth formula"
209:  #endif
210: #endif
211:   coreGlobals.solenoids = locals.solsmooth[0];
212: #if S11_SOLSMOOTH > 1
213:   coreGlobals.solenoids |= locals.solsmooth[1];
214: #endif
215:   coreGlobals.solenoids2 = (coreGlobals.solenoids2 & 0xFFFF00FF) | (locals.extSol << 8);
216: #if defined(LISY_SUPPORT)
217:    lisy_w_solenoid_handler( ); //RTH: need to add solenoids2 ?
218: #endif
219:   locals.solenoids = coreGlobals.pulsedSolState;
220:   locals.extSol = locals.extSolPulse;
221:

src/wpc/s11.c:396-415
396:        data = 0x02, CN3-Pin 8 (GNR Magnet 2, -"-)
397:        data = 0x04, CN3-Pin 7 (GNR Magnet 1, -"-)
398:        ....
399:        data = 0x80, CN3-Pin 1 (Blinder on Tommy)*/
400:   if (core_gameData->gen & GEN_DEDMD16) {
401:     if (core_gameData->hw.gameSpecific1 & S11_PRINTERLINE) {
402:       locals.extSol |= locals.extSolPulse = (data ^ 0xff);
403:       core_write_pwm_output_8b(CORE_MODOUT_SOL0 + 40, locals.extSolPulse);
404:     }
405:   } else if (core_gameData->gen & (GEN_DEDMD32|GEN_DEDMD64)) {
406:     if (core_gameData->hw.gameSpecific1 & S11_PRINTERLINE) {
407:       locals.extSol |= locals.extSolPulse = data;
408:       core_write_pwm_output_8b(CORE_MODOUT_SOL0 + 40, locals.extSolPulse);
409:     }
410:   }
411:   else {
412:     if (core_gameData->hw.display & S11_DISPINV) data = ~data;
413:     if (core_gameData->hw.display & S11_BCDDISP) {
414:       locals.segments[locals.digSel].w |=
415:            locals.pseg[locals.digSel].w = core_bcd2seg7[data&0x0f];

src/wpc/s11.c:537-583
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

src/wpc/s11.c:604-673
604:   if (data != locals.solBits1) {
605:     //fprintf(stderr,"\nPIA Data %d",data);
606:     locals.solBits1 = data;
607:     updsol();
608:   }
609: }
610:
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
624:
625: /*---------------
626: / Switch reading
627: /----------------*/
628: static WRITE_HANDLER(pia4b_w)
629: {
630:   if (locals.deGame) {
631:     int x;
632:     for (x=0; x<8; x++)
633:       if (data & (1u << x))
634:         break;
635:     locals.swCol = data & (1u << x);
636:   }
637:   else
638:     locals.swCol = data;
639: #if defined(LISY_SUPPORT)
640:   lisy_w_throttle();
641: #endif
642: }
643:
644: static READ_HANDLER(pia4a_r)
645: {
646: #if defined(LISY_SUPPORT)
647:   //get the switches from LISY_mini
648:   lisy_w_switch_handler();
649: #endif
650:   return core_getSwCol(locals.swCol);
651: }
652:
653: /*-------
654: /  Sound
655: /--------*/
656: /*-- Sound board sound command--*/
657: static WRITE_HANDLER(pia5b_w) {
658:   locals.sndCmd = data; sndbrd_1_data_w(0,data);
659: }
660:
661: /*-- Sound board sound command available --*/
662: static WRITE_HANDLER(pia5cb2_w) {
663:   /* don't pass to sound board if a sound overlay board is available */
664:   if ((core_gameData->hw.gameSpecific1 & S11_SNDOVERLAY) &&
665:       ((locals.sndCmd & 0xe0) == 0)) {
666:     if (!data) {
667:        locals.extSol |= locals.extSolPulse = (~locals.sndCmd) & 0x1f;
668:        core_write_pwm_output_8b(CORE_MODOUT_SOL0 + 40, locals.extSolPulse);
669:     }
670:   }
671:   else sndbrd_1_ctrl_w(0,data);
672: }
673: /*-- reset sound board CPU --*/

src/wpc/s11.c:773-798
773:
774: static SWITCH_UPDATE(s11) {
775: #ifdef PROC_SUPPORT
776: 	// Go read the switches from the P-ROC
777: 	if (coreGlobals.p_rocEn)
778: 		procGetSwitchEvents();
779: #endif
780:
781: #ifndef LISY_SUPPORT
782: //if we have LISY, all switches come from LISY (Matrix[0] has e.g. ADVANCE Button!
783:   if (inports) {
784:     coreGlobals.swMatrix[0] = (inports[S11_COMINPORT] & 0x7f00)>>8;
785:     // All the matrix switches come from the P-ROC, so we only want to read
786:     // the first column from the keyboard if we are not using the P-ROC
787: #ifndef PROC_SUPPORT
788:     coreGlobals.swMatrix[1] = inports[S11_COMINPORT];
789: #endif
790:   }
791: #endif
792:
793:   /*-- Generate interupts for diganostic keys --*/
794:   cpu_set_nmi_line(0, core_getSw(S11_SWCPUDIAG) ? ASSERT_LINE : CLEAR_LINE);
795:   sndbrd_0_diag(core_getSw(S11_SWSOUNDDIAG));
796:   if ((core_gameData->hw.gameSpecific1 & S11_MUXSW2) && core_gameData->sxx.muxSol)
797:     core_setSw(2, core_getSol(core_gameData->sxx.muxSol));
798:   if (locals.deGame) {

src/wpc/s11.c:1094-1100
1094:   else if (strncasecmp(gn, "swrds_", 6) == 0) { // Swords of Fury
1095:      core_set_pwm_output_type(CORE_MODOUT_SOL0 +  9 - 1, 1, CORE_MODOUT_BULB_89_25V_DC_S11);
1096:      core_set_pwm_output_type(CORE_MODOUT_SOL0 + 10 - 1, 1, CORE_MODOUT_BULB_44_6_3V_AC_REV); // GI output
1097:      core_set_pwm_output_type(CORE_MODOUT_SOL0 + 11 - 1, 1, CORE_MODOUT_BULB_89_25V_DC_S11);
1098:      core_set_pwm_output_type(CORE_MODOUT_SOL0 + 25 - 1, 8, CORE_MODOUT_BULB_89_25V_DC_S11); // 8 muxed flasher outputs (Mux relay is solenoid #12)
1099:   }
1100:   else if (strncasecmp(gn, "taxi_", 5) == 0) { // Taxi

src/wpc/core.c:1778-1832
1778: void core_updateSw(int flipEn) {
1779:   /*-- handle flippers--*/
1780:   const int flip = core_gameData->hw.flippers;
1781:   const int flipSwCol = (core_gameData->gen & (GEN_GTS3 | GEN_SPA | GEN_ALVG | GEN_ALVG_DMD2 | GEN_WICO)) ? 15 : CORE_FLIPPERSWCOL;
1782:   int inports[CORE_MAXPORTS];
1783:   UINT8 swFlip;
1784:   int ii;
1785:
1786:   if (g_fHandleKeyboard) {
1787:     const int n = CORE_COREINPORT+(coreData->coreDips+31)/16;
1788:     for (ii = 0; ii < n; ii++)
1789:       inports[ii] = readinputport(ii);
1790:
1791:     /*-- buttons --*/
1792:     swFlip = 0;
1793:     if (inports[CORE_FLIPINPORT] & CORE_LLFLIPKEY) swFlip |= CORE_SWLLFLIPBUTBIT;
1794:     if (inports[CORE_FLIPINPORT] & CORE_LRFLIPKEY) swFlip |= CORE_SWLRFLIPBUTBIT;
1795:     if (locals.flipMask & CORE_SWULFLIPBUTBIT) {    /* have UL switch */
1796:       if (flip & FLIP_BUT(FLIP_UL))
1797:         { if (inports[CORE_FLIPINPORT] & CORE_ULFLIPKEY) swFlip |= CORE_SWULFLIPBUTBIT; }
1798:       else
1799:         { if (inports[CORE_FLIPINPORT] & CORE_LLFLIPKEY) swFlip |= CORE_SWULFLIPBUTBIT; }
1800:     }
1801:     if (locals.flipMask & CORE_SWURFLIPBUTBIT) {    /* have UR switch */
1802:       if (flip & FLIP_BUT(FLIP_UR))
1803:         { if (inports[CORE_FLIPINPORT] & CORE_URFLIPKEY) swFlip |= CORE_SWURFLIPBUTBIT; }
1804:       else
1805:         { if (inports[CORE_FLIPINPORT] & CORE_LRFLIPKEY) swFlip |= CORE_SWURFLIPBUTBIT; }
1806:     }
1807:   }
1808:   else
1809:     swFlip = (coreGlobals.swMatrix[flipSwCol] ^ coreGlobals.invSw[flipSwCol]) & (CORE_SWULFLIPBUTBIT|CORE_SWURFLIPBUTBIT|CORE_SWLLFLIPBUTBIT|CORE_SWLRFLIPBUTBIT);
1810:
1811: #ifdef PROC_SUPPORT
1812:   /*-- Only handle flipper switches if we're not in a real game, otherwise they --*/
1813:   /*-- will get physically activated anyway */
1814:   if (!coreGlobals.p_rocEn) {
1815: #endif
1816:
1817:     /*-- set switches in matrix for non-fliptronic games --*/
1818:     if (FLIP_SWL(flip)) core_setSw(FLIP_SWL(flip), swFlip & CORE_SWLLFLIPBUTBIT);
1819:     if (FLIP_SWR(flip)) core_setSw(FLIP_SWR(flip), swFlip & CORE_SWLRFLIPBUTBIT);
1820: #ifdef PROC_SUPPORT
1821:   }
1822: #endif
1823:
1824:   /*-- fake solenoids if not CPU controlled --*/
1825:   if ((flip & FLIP_SOL(FLIP_L)) == 0) {
1826:     coreGlobals.solenoids2 &= 0xffffff00;
1827:     if (flipEn) {
1828:       if (swFlip & CORE_SWLLFLIPBUTBIT) coreGlobals.solenoids2 |= CORE_LLFLIPSOLBITS;
1829:       if (swFlip & CORE_SWLRFLIPBUTBIT) coreGlobals.solenoids2 |= CORE_LRFLIPSOLBITS;
1830:     }
1831:   }
1832:

src/wpc/core.c:2184-2217
2184:
2185: /*-- "normal" switch/lamp numbering (1-64) --*/
2186: int core_swSeq2m(int no) { return no+7; }
2187: int core_m2swSeq(int col, int row) { return col*8+row-7; }
2188:
2189: /*------------------------------------------
2190: /  Read the current switch value
2191: /
2192: /  This function returns TRUE for active
2193: /  switches even if the switch is active low.
2194: /-------------------------------------------*/
2195: int core_getSw(int swNo) {
2196:   if (coreData->sw2m) swNo = coreData->sw2m(swNo); else swNo = (swNo/10)*8+(swNo%10-1);
2197:   return (coreGlobals.swMatrix[swNo/8] ^ coreGlobals.invSw[swNo/8]) & (1<<(swNo%8));
2198: }
2199:
2200: int core_getSwCol(int colEn) {
2201:   int ii = 1;
2202:   if (colEn) {
2203:     while ((colEn & 0x01) == 0) {
2204:       colEn >>= 1;
2205:       ii++;
2206:     }
2207:   }
2208:   return coreGlobals.swMatrix[ii];
2209: }
2210:
2211: /*----------------------
2212: /  Set/reset a switch
2213: /-----------------------*/
2214: void core_setSw(int swNo, int value) {
2215:   if (coreData->sw2m) swNo = coreData->sw2m(swNo); else swNo = (swNo/10)*8+(swNo%10-1);
2216:   //fprintf(stderr,"\nPinMAME switch %d",swNo);
2217:   coreGlobals.swMatrix[swNo/8] &= ~(1<<(swNo%8)); /* clear the bit first */

src/wpc/core.c:2251-2306
2251: int core_getSol(int solNo) {
2252:   if (solNo <= 28)
2253:     return coreGlobals.nSolenoids && (options.usemodsol & (CORE_MODOUT_ENABLE_PHYSOUT_SOLENOIDS | CORE_MODOUT_ENABLE_MODSOL | CORE_MODOUT_FORCE_ON)) ? saturatedByte(coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + solNo - 1].value) : coreGlobals.solenoids & CORE_SOLBIT(solNo);
2254:   else if (solNo <= 32) { // 29-32
2255:     if (core_gameData->gen & (GEN_ALLS11 | GEN_PINHECK))
2256:       return coreGlobals.nSolenoids && (options.usemodsol & (CORE_MODOUT_ENABLE_PHYSOUT_SOLENOIDS | CORE_MODOUT_ENABLE_MODSOL | CORE_MODOUT_FORCE_ON)) ? saturatedByte(coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + solNo - 1].value) : coreGlobals.solenoids & CORE_SOLBIT(solNo);
2257:     else if (core_gameData->gen & GEN_ALLWPC) // Remap WPC GameOn/J111 GPIO (hacky)
2258:       return coreGlobals.solenoids2 & (1<<(solNo-29+8));
2259:   }
2260:   else if (solNo <= 36) { // 33-36 driver specific sols
2261:     if (coreGlobals.hasModulatedFlippers && (options.usemodsol & (CORE_MODOUT_ENABLE_PHYSOUT_SOLENOIDS | CORE_MODOUT_ENABLE_MODSOL | CORE_MODOUT_FORCE_ON)))
2262:       return saturatedByte(coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + solNo - 1].value); // Fliptronics are implemented through PWM (needed as these are used to drive flashers on some games)
2263:     if (core_gameData->gen & GEN_ALLWPC) { // WPC only: Upper flipper (note that other systems also have upper flippers, they just don't implement the legacy PinMAME flipper output mapping)
2264:       int mask;
2265:       /*-- flipper coils --*/
2266:       if      ((solNo == sURFlip) && (core_gameData->hw.flippers & FLIP_SOL(FLIP_UR)))
2267:         mask = CORE_URFLIPSOLBITS;
2268:       else if ((solNo == sULFlip) && (core_gameData->hw.flippers & FLIP_SOL(FLIP_UL)))
2269:         mask = CORE_ULFLIPSOLBITS;
2270:       else
2271:         mask = 1<<(solNo - 33 + 4);
2272:       return coreGlobals.solenoids2 & mask;
2273:     }
2274:     else if (core_gameData->gen & GEN_SAM) // SAM only: fake GameOn solenoid for fast flips
2275:        return coreGlobals.solenoids2 & 0x10;
2276:   }
2277:   else if (solNo <= 44) { // 37-44 WPC95 & S11 extra
2278:     if (core_gameData->gen & (GEN_WPC95|GEN_WPC95DCS)) { // Duplicated in 37..40 / 41..44, so always read from 41..44 (hence the |4 in the index/mask) for solenoids, and 37..40 for PWM outputs
2279:       if (coreGlobals.nSolenoids && (options.usemodsol & (CORE_MODOUT_ENABLE_PHYSOUT_SOLENOIDS | CORE_MODOUT_ENABLE_MODSOL | CORE_MODOUT_FORCE_ON)))
2280:         return saturatedByte(coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + (solNo <= 40 ? solNo : (solNo - 4))-1].value);
2281:       else
2282:         return coreGlobals.solenoids & (1<<((solNo - 13)|4));
2283:     }
2284:     if (core_gameData->gen & (GEN_ALLS11 | GEN_PINHECK))
2285:       return coreGlobals.nSolenoids && (options.usemodsol & (CORE_MODOUT_ENABLE_PHYSOUT_SOLENOIDS | CORE_MODOUT_ENABLE_MODSOL | CORE_MODOUT_FORCE_ON)) ? saturatedByte(coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + 32 + solNo - 37 + 8].value) : coreGlobals.solenoids2 & (1<<(solNo - 37 + 8));
2286:   }
2287:   else if (solNo <= 48) { // 45-48 Lower flippers
2288:     if (coreGlobals.hasModulatedFlippers && (options.usemodsol & (CORE_MODOUT_ENABLE_PHYSOUT_SOLENOIDS | CORE_MODOUT_ENABLE_MODSOL | CORE_MODOUT_FORCE_ON)))
2289:       return saturatedByte(coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + solNo - 1].value); // Fliptronics are implemented through PWM
2290:     int mask = 1<<(solNo - 45);
2291:     /*-- Game must have lower flippers but for symmetry we check anyway --*/
2292:     if      /*(*/(solNo == sLRFlip) //&& (core_gameData->hw.flippers & FLIP_SOL(FLIP_LR)))
2293:       mask = CORE_LRFLIPSOLBITS;
2294:     else if /*(*/(solNo == sLLFlip) //&& (core_gameData->hw.flippers & FLIP_SOL(FLIP_LL)))
2295:       mask = CORE_LLFLIPSOLBITS;
2296:     return coreGlobals.solenoids2 & mask;
2297:   }
2298:   else if (solNo <= 50) // 49-50 simulated
2299:     return sim_getSol(solNo);
2300:   else if (core_gameData->hw.getSol)
2301:     return core_gameData->hw.getSol(solNo);
2302:   return 0;
2303: }
2304:
2305: /*-------------------------------------
2306: /  Read the instant status of a solenoid

src/wpc/core.h:291-343
291: /*  1-15 Standard Pulse                  */
292: /* 17-20 Standard Hold                   */
293: /*                                       */
294: /*       GTS80                           */
295: /*  1- 9 Standard                        */
296: /* 10    GameOn (fake)                   */
297: /* 11    Tilt (for GI) (fake)            */
298: #define CORE_FIRSTEXTSOL   37
299: #define CORE_FIRSTUFLIPSOL 33
300: #define CORE_FIRSTCUSTSOL  51
301: #define CORE_FIRSTLFLIPSOL 45
302: #define CORE_FIRSTSIMSOL   49
303: #define CORE_MAXSOL        64
304:
305: #define CORE_SSFLIPENSOL  23
306: #define CORE_FIRSTSSSOL   17
307:
308: #define CORE_SOLBIT(x) (1u<<((x)-1))
309:
310: /*  Flipper Solenoid numbers */
311: #define sLRFlip     (CORE_FIRSTLFLIPSOL+1)
312: #define sLRFlipPow  (CORE_FIRSTLFLIPSOL+0)
313: #define sLLFlip     (CORE_FIRSTLFLIPSOL+3)
314: #define sLLFlipPow  (CORE_FIRSTLFLIPSOL+2)
315: #define sURFlip     (CORE_FIRSTUFLIPSOL+1)
316: #define sURFlipPow  (CORE_FIRSTUFLIPSOL+0)
317: #define sULFlip     (CORE_FIRSTUFLIPSOL+3)
318: #define sULFlipPow  (CORE_FIRSTUFLIPSOL+2)
319:
320: /*-- Flipper solenoid bits --*/
321: #define CORE_LRFLIPSOLBITS 0x03
322: #define CORE_LLFLIPSOLBITS 0x0c
323: #define CORE_URFLIPSOLBITS 0x30
324: #define CORE_ULFLIPSOLBITS 0xc0
325:
326: /*-- create a custom solenoid number --*/
327: /* example: #define swCustom CORE_CUSTSOLNO(1)  // custom solenoid 1 */
328: #define CORE_CUSTSOLNO(n) (CORE_FIRSTCUSTSOL-1+(n))
329:
330: #define CORE_COINDOORSWCOL                0 /* internal array number */
331: #define CORE_MAXSWCOL                    16 /* switch columns (0-9=sw matrix, 10=coin door, 11=cabinet/flippers) */
332: #define CORE_FLIPPERSWCOL                11 /* internal array number */
333: #define CORE_STDSWCOLS                   12 /* Base number of switch matrix columns */
334: #define CORE_CUSTSWCOL       CORE_STDSWCOLS /* first custom (game specific) switch column */
335: #define CORE_MAXLAMPCOL                  78 /* lamp column (0-7=std lamp matrix 8- custom) */
336: #define CORE_STDLAMPCOLS                  8 /* Base number of lamp matrix columns */
337: #define CORE_CUSTLAMPCOL   CORE_STDLAMPCOLS /* first custom lamp column */
338: #define CORE_MAXPORTS                     8 /* Maximum input ports */
339: #define CORE_MAXGI                        5 /* Maximum GI strings */
340: #define CORE_MAXNVRAM                131118 /* Maximum number of NVRAM bytes, only used for get_ChangedNVRAM so far */
341: #define CORE_SEGCOUNT                   128 /* Maximum number of alpha numeric display (16 segments each) */
342:
343: /*-- create a custom switch number --*/

src/wpc/sim.c:24-39
24: /  Global variables
25: /---------------------*/
26: static sim_tSimData *simData = NULL;  /* data about the game simulator */
27: static struct {
28:   sim_tBallStatus balls[SIM_MAXBALLS]; /* ball status etc */
29:   int  currBall;      /* currently select ball */
30:   int  prevIn[CORE_MAXPORTS]; /* last frame's game inports (autoBall: a key moves a ball when pressed) */
31:   int  shooterRel;    /* plunger released */
32:   int  shooterSpeed;  /* */
33:   struct {
34:     int swNo;         /* spinner switch */
35:     int spinCount;    /* time until next spin */
36:     int nextSpin;     /* timer for next spin */
37:   } spinner[SIM_MAXSPIN];
38: } locals;
39:

src/wpc/sim.c:100-127
100:       else if ((iData->action > 0) && (iData->action < SIM_STATES)) {
101:         core_setSw(iData->action, FALSE); /* reset switch regardless of ball state */
102:       }
103:       iData += 1;
104:     }
105:   }
106:   for (ii = 0; ii < simData->inports && firstGameInport + ii < CORE_MAXPORTS; ii++)
107:     locals.prevIn[firstGameInport + ii] = inports[firstGameInport + ii];
108:   /*----------------------------------------------
109:   /  update swithes depending playfield mechanics
110:   /-----------------------------------------------*/
111:   if (simData->manShooter) {
112:     /*--  ball shooter --*/
113:     if (inports[CORE_SIMINPORT] & SIM_SHOOTERKEY) {
114:       locals.shooterSpeed += 1;
115:       if (locals.shooterSpeed > 50)
116:         locals.shooterSpeed = 50;
117:     }
118:     else if (locals.shooterSpeed > 0) {
119:       /*-- Shooters been released --*/
120:       if (locals.shooterRel == 1) locals.shooterSpeed = 0;
121:       if (locals.shooterRel > 0)  locals.shooterRel -= 1;
122:       else                        locals.shooterRel = SIM_SHOOTRELTIME;
123:     }
124:   }
125:
126:   /*------------------------
127:   /  update ball positions

src/wpc/sim.c:247-251
247: int sim_getSol(int solNo) {
248:   if (solNo == sShooterRel)
249:     return locals.shooterRel > 0;
250:   return 0;
251: }

src/wpc/s11.h:128-138
128:   ROM_START(name##_##ver) \
129:     NORMALREGION(0x10000, S11_CPUREGION) \
130:       ROM_LOAD(n1, 0x6000, 0x2000, chk1) \
131:       ROM_RELOAD(  0xe000, 0x2000)
132:
133: #define S11_ROMSTART48(name, ver, n1, chk1, n2, chk2) \
134:   ROM_START(name##_##ver) \
135:     NORMALREGION(0x10000, S11_CPUREGION) \
136:       ROM_LOAD(n1, 0x4000, 0x4000, chk1) \
137:       ROM_LOAD(n2, 0x8000, 0x8000, chk2)
138:

src/wpc/wmssnd.h:87-110
87:     ROM_RELOAD(start+0x40000, 0x10000)
88:
89: #define S11CS_SOUNDROM000(n1,chk1,n2,chk2,n3,chk3) \
90:   S11CS_STDREG \
91:   S11CS_ROMLOAD0(0x00000, n1, chk1) \
92:   S11CS_ROMLOAD0(0x10000, n2, chk2) \
93:   S11CS_ROMLOAD0(0x20000, n3, chk3)
94:
95: #define S11CS_SOUNDROM008(n1,chk1,n2,chk2,n3,chk3) \
96:   S11CS_STDREG \
97:   S11CS_ROMLOAD0(0x00000, n1, chk1) \
98:   S11CS_ROMLOAD0(0x10000, n2, chk2) \
99:   S11CS_ROMLOAD8(0x20000, n3, chk3)
100:
101: #define S11CS_SOUNDROM888(n1,chk1,n2,chk2,n3,chk3) \
102:   S11CS_STDREG \
103:   S11CS_ROMLOAD8(0x00000, n1, chk1) \
104:   S11CS_ROMLOAD8(0x10000, n2, chk2) \
105:   S11CS_ROMLOAD8(0x20000, n3, chk3)
106:
107: #define S11CS_SOUNDROM88(n1,chk1,n2,chk2) \
108:   S11CS_STDREG \
109:   S11CS_ROMLOAD8(0x00000, n1, chk1) \
110:   S11CS_ROMLOAD8(0x10000, n2, chk2)

src/wpc/wmssnd.h:144-148
144: #define S11XS_SOUNDROM88(n1, chk1, n2, chk2) \
145:   SOUNDREGION(0x10000, S11XS_CPUREGION) \
146:   SOUNDREGION(0x10000, S11XS_ROMREGION) \
147:     ROM_LOAD(n1, 0x0000, 0x8000, chk1) \
148:     ROM_LOAD(n2, 0x8000, 0x8000, chk2)

```
