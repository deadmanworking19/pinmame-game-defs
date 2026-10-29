# Pinned Gold emulator contract

Leading indentation is expanded to spaces and trailing horizontal whitespace is omitted. Statements, quoted contents, source line numbers and full region boundaries are preserved; original byte-for-byte scripts/source remain external.

Revision `46e1a01a0f73dc5ce163d98db1ae435883ecc450`. Literal complete declaration/function regions, with file hashes and original line numbers. The simulator shooter is a live virtual channel; it is not an automatic physical plunger. GPIO and winding address publication is distinct from physical load fitment.

## src/wpc/sims/wpc/full/taf.c

SHA-256 `7fc3551f27f4786f5dc3c83440fe7dd3b6e90377e786daeb616ff3480d187113`

```c
525: /*-- TAFG uses TAF input ports and init functions --*/
526: #define input_ports_tafg input_ports_taf
527: #define init_tafg        init_taf
```

```c
557: CORE_GAMEDEF(tafg,lx3,      "Addams Family Special Collectors Edition / Gold, The (LX-3)",1994,"Bally",wpc_mFliptronS,0)
558: CORE_CLONEDEF(tafg,dx3,lx3, "Addams Family Special Collectors Edition / Gold, The (DX-3 LED Ghost Fix)",1994,"Bally",wpc_mFliptronS,0)
559: CORE_CLONEDEF(tafg,h3,lx3,  "Addams Family Special Collectors Edition / Gold, The (H-3)",1994,"Bally",wpc_mFliptronS,0) // is it actually newer than LX-3/LA-3? (but only change apparently is 'Does not display "Free Play" when set to Free Play mode' -> needs verification), or is it just a MOD? The OS version definetly is the newest one, both for TAF and TAFG, so this should be really the most up-to-date overall
560: CORE_CLONEDEF(tafg,i3,lx3,  "Addams Family Special Collectors Edition / Gold, The (I-3 LED Ghost Fix)",1994,"Bally",wpc_mFliptronS,0)
561: CORE_CLONEDEF(tafg,i3bs,lx3,"Addams Family Special Collectors Edition / Gold, The (I-3 LED Ghost Fix + Ballsaver MOD)",2026,"Bally / RedBall",wpc_mFliptronS,0) // patch of TAFG H-3 to add a ball saver feature, which can be configured via Adjustment A.2 (setting 36). It also includes the "No Ghosting" patch
562: CORE_CLONEDEF(tafg,la2,lx3, "Addams Family Special Collectors Edition / Gold, The (LA-2)",1994,"Bally",wpc_mFliptronS,0)
563: CORE_CLONEDEF(tafg,da2,lx3, "Addams Family Special Collectors Edition / Gold, The (DA-2 LED Ghost Fix)",1994,"Bally",wpc_mFliptronS,0)
564: CORE_CLONEDEF(tafg,la3,lx3, "Addams Family Special Collectors Edition / Gold, The (LA-3)",1994,"Bally",wpc_mFliptronS,0)
565: CORE_CLONEDEF(tafg,da3,lx3, "Addams Family Special Collectors Edition / Gold, The (DA-3 LED Ghost Fix)",1994,"Bally",wpc_mFliptronS,0)
```

```c
600: /-----------*/
601: static sim_tSimData tafSimData = {
602:   2,    /* 2 game specific input ports */
603:   taf_stateDef,
604:   taf_inportData,
605:   { stRTrough, stCTrough, stLTrough, stDrain, stDrain, stDrain, stDrain },
606:   NULL, /* no init */
607:   taf_handleBallState,
608:   taf_drawStatic,
609: #ifdef NEWSHOOT
610:   {{{10, "Swamp",      stULock,  10},
611:     {20, "Thing Hole", stThHole, 15},
612:     {25, "Loop",       stRLoopDn,20}
613:   }}
614: #else
615:   TRUE, /* simulate manual shooter */
616: #endif
617:   NULL  /* no custom key conditions */
618: };
619:
620: static core_tGameData tafGameData = {
621:   GEN_WPCFLIPTRON, wpc_dispDMD,/* generation */
622:   {
623:     FLIP_BUT(FLIP_L) | FLIP_SW(FLIP_L | FLIP_U) | FLIP_SOL(FLIP_L|FLIP_U),
624:     0,0,0,0,0,0,0,
625:     NULL, taf_handleMech, taf_getMech, taf_drawMech,
626:     &taf_lampPos
627: #ifdef ENABLE_MECHANICAL_SAMPLES
628:     , taf_SamSolMap
629: #endif
630:   },
631:   &tafSimData,
632:   {
633:     "",
634:     /*Coin    1     2     3     4     5     6     7     8     9    10   Cab.  Cust */
635:     { 0x00, 0x00, 0x00, 0x00, 0x00, 0x7c, 0x00, 0x00, 0x18, 0x00, 0x00, 0x00}, /* inverted switches */
636:     /*Start    Tilt    SlamTilt    CoinDoor    Shooter */
637:     { swStart, swTilt, swSlamTilt, swCoinDoor, 0},
638:   }
639: };
640:
641:
642: /*---------------
643: /  Game handling
644: /----------------*/
645: static void init_taf(void) {
646:   core_gameData = &tafGameData;
647:   hc55516_set_sample_clock(0, 22372);
648: }
```

## src/wpc/core.c

SHA-256 `38a4418adba7f2ef408e8f92bfcf3e5ab950c45164cb69461460af3747386c00`

```c
2456: int core_getSol(int solNo) {
2457:   // No solenoid 0, but VPM's Solenoids/SolenoidsState arrays start at index 0
2458:   if (solNo < 1)
2459:     return 0;
2460:   // Binary states are returned as 0/1, like the changed solenoid list. The integrated value is only returned with physical solenoid outputs
2461:   // or modulated solenoids: with CORE_MODOUT_FORCE_ON alone (SAM, Capcom, pinHeck), a blinking flasher would read on for the whole sequence
2462:   // 1-32: driver board outputs, like core_getAllSol / core_getAllPhysicSols
2463:   if (solNo <= 28 || (solNo <= 32 && !(core_gameData->gen & GEN_ALLWPC)))
2464:     return coreGlobals.nSolenoids && (options.usemodsol & (CORE_MODOUT_ENABLE_PHYSOUT_SOLENOIDS | CORE_MODOUT_ENABLE_MODSOL)) ? saturatedByte(coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + solNo - 1].value) : ((coreGlobals.solenoids & CORE_SOLBIT(solNo)) != 0);
2465:   else if (solNo <= 32) // 29-32 WPC: remap GameOn/J111 GPIO (hacky)
2466:     // Binary state even with physical outputs, while core_getAllPhysicSols reports slots 28-30 (CORE_MODOUT_PULSE, same states) as 0/255
2467:     return (coreGlobals.solenoids2 & (1<<(solNo-29+8))) != 0;
2468:   else if (solNo <= 36) { // 33-36 driver specific sols
2469:     if (coreGlobals.hasModulatedFlippers && (options.usemodsol & (CORE_MODOUT_ENABLE_PHYSOUT_SOLENOIDS | CORE_MODOUT_ENABLE_MODSOL)))
2470:       return saturatedByte(coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + solNo - 1].value); // Fliptronics are implemented through PWM (needed as these are used to drive flashers on some games)
2471:     if (coreGlobals.hasModulatedFlippers && (options.usemodsol & CORE_MODOUT_FORCE_ON)) // Binary state of the flipper outputs, like core_getFlipSolBits
2472:       return coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + solNo - 1].value > 0.f;
2473:     if (core_gameData->gen & GEN_ALLWPC) { // WPC only: Upper flipper (note that other systems also have upper flippers, they just don't implement the legacy PinMAME flipper output mapping)
2474:       int mask;
2475:       /*-- flipper coils --*/
2476:       if      ((solNo == sURFlip) && (core_gameData->hw.flippers & FLIP_SOL(FLIP_UR)))
2477:         mask = CORE_URFLIPSOLBITS;
2478:       else if ((solNo == sULFlip) && (core_gameData->hw.flippers & FLIP_SOL(FLIP_UL)))
2479:         mask = CORE_ULFLIPSOLBITS;
2480:       else
2481:         mask = 1<<(solNo - 33 + 4);
2482:       return (coreGlobals.solenoids2 & mask) != 0;
2483:     }
2484:     else if (core_gameData->gen & (GEN_SAM | GEN_SPIKE1)) // SAM, SPIKE 1: fake GameOn solenoid for fast flips
2485:        return (coreGlobals.solenoids2 & 0x10) != 0;
2486:     else if (core_gameData->gen & GEN_ALLWS) // Whitestar: aux board outputs (magnets, ...), like core_getAllSol
2487:        return coreGlobals.nSolenoids && (options.usemodsol & (CORE_MODOUT_ENABLE_PHYSOUT_SOLENOIDS | CORE_MODOUT_ENABLE_MODSOL)) ? saturatedByte(coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + solNo - 1].value) : ((coreGlobals.solenoids2 & (1<<(solNo - 33 + 4))) != 0);
2488:   }
2489:   else if (solNo <= 44) { // 37-44 WPC95 & S11 extra
2490:     if (core_gameData->gen & (GEN_WPC95|GEN_WPC95DCS)) { // Duplicated in 37..40 / 41..44, so always read from 41..44 (hence the |4 in the index/mask) for solenoids, and 37..40 for PWM outputs
2491:       if (coreGlobals.nSolenoids && (options.usemodsol & (CORE_MODOUT_ENABLE_PHYSOUT_SOLENOIDS | CORE_MODOUT_ENABLE_MODSOL)))
2492:         return saturatedByte(coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + (solNo <= 40 ? solNo : (solNo - 4))-1].value);
2493:       else
2494:         return (coreGlobals.solenoids & (1<<((solNo - 13)|4))) != 0;
2495:     }
2496:     if (core_gameData->gen & (GEN_ALLS11 | GEN_PINHECK)) // S11 outputs in slots 40-47; pinHeck's GI 8-15 in 36-43, its lower flippers using 44-47
2497:       return coreGlobals.nSolenoids && (options.usemodsol & (CORE_MODOUT_ENABLE_PHYSOUT_SOLENOIDS | CORE_MODOUT_ENABLE_MODSOL)) ? saturatedByte(coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + ((core_gameData->gen & GEN_PINHECK) ? solNo - 1 : 32 + solNo - 37 + 8)].value) : ((coreGlobals.solenoids2 & (1<<(solNo - 37 + 8))) != 0);
2498:   }
2499:   else if (solNo <= 48) { // 45-48 Lower flippers
2500:     if (coreGlobals.hasModulatedFlippers && (options.usemodsol & (CORE_MODOUT_ENABLE_PHYSOUT_SOLENOIDS | CORE_MODOUT_ENABLE_MODSOL)))
2501:       return saturatedByte(coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + solNo - 1].value); // Fliptronics are implemented through PWM
2502:     if (coreGlobals.hasModulatedFlippers && (options.usemodsol & CORE_MODOUT_FORCE_ON)) // Binary state of the flipper outputs, like core_getFlipSolBits
2503:       return coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + solNo - 1].value > 0.f;
2504:     int mask = 1<<(solNo - 45);
2505:     /*-- Game must have lower flippers but for symmetry we check anyway --*/
2506:     if      /*(*/(solNo == sLRFlip) //&& (core_gameData->hw.flippers & FLIP_SOL(FLIP_LR)))
2507:       mask = CORE_LRFLIPSOLBITS;
2508:     else if /*(*/(solNo == sLLFlip) //&& (core_gameData->hw.flippers & FLIP_SOL(FLIP_LL)))
2509:       mask = CORE_LLFLIPSOLBITS;
2510:     return (coreGlobals.solenoids2 & mask) != 0;
2511:   }
2512:   else if (solNo <= 50) // 49-50 simulated
2513:     return sim_getSol(solNo);
2514:   else if (core_gameData->hw.getSol)
2515:     return core_gameData->hw.getSol(solNo);
2516:   return 0;
2517: }
```

## src/wpc/wpc.c

SHA-256 `a3005e72121adebd81efb622bc3e59c380ae70a4148700b2329a9310f9761176`

```c
500:       }
501:     }
502:     #endif
503:
504:     wpc_data[WPC_SOLENOID1] = wpc_data[WPC_SOLENOID2] = 0;
505:     wpc_data[WPC_SOLENOID3] = wpc_data[WPC_SOLENOID4] = 0;
506:
507:     // GameOn Solenoid (solenoid #31) and other state bits (solenoids #29 and #30):
508:     // - We always mirror the state of 2 out of the 3 GPIO on J111 to solenoids #29 and #30
509:     // - Before fliptronic: real game on solenoid, controlled by CPU through the high bit of WPC_GILAMPS
510:     //   CPU board: U4 - J121 / Power driver board: J113 - Relay - J110 - Cabinet switch - J109 / Flippers
511:     // - Starting with fliptronic, no GameOn solenoid as flippers are ROM controlled:
512:     //   We use state of FastFlip address as a fake GameOn (letting the client decide to use it or not)
513:     //   If Fastflip is missing, we default to mirroring the high bit of WPC_GILAMPS
514:     // Note that these states are stored in solenoids2 (sol 33..35) but are remapped to solenoid 29..31 in core.c
515:     if (wpc_fastflip_addr == 0)
516:     {
517:       coreGlobals.solenoids2 = (wpc_data[WPC_GILAMPS] & 0xe0) << 3;
518:       core_write_pwm_output(CORE_MODOUT_SOL0 + 29 - 1, 3, wpc_data[WPC_GILAMPS] >> 5);
519:     }
520:     else
521:     {
522:       assert(core_gameData->gen & GENWPC_HASFLIPTRON);
523:       coreGlobals.solenoids2 = (wpc_data[WPC_GILAMPS] & 0x60) << 3;
524:       core_write_pwm_output(CORE_MODOUT_SOL0 + 29 - 1, 2, wpc_data[WPC_GILAMPS] >> 5);
525:       if (wpc_ram[wpc_fastflip_addr] > 0)
526:         coreGlobals.solenoids2 |= 0x400;
527:       core_write_pwm_output(CORE_MODOUT_SOL0 + 31 - 1, 1, wpc_ram[wpc_fastflip_addr] > 0 ? 1 : 0);
528:     }
529:
530:     // ROM controlled flipper coils when using FlipTronics
531:     if (core_gameData->gen & GENWPC_HASFLIPTRON) {
532:       coreGlobals.solenoids2 |= wpclocals.solFlip;
533:       wpclocals.solFlip = wpclocals.solFlipPulse;
534:     }
535:   }
536:   else if (((wpclocals.interfaceUpdateCount % WPC_INTERFACE_UPD_PER_FRAME) == 0) && (core_gameData->gen & GENWPC_HASFLIPTRON)) {
537:     coreGlobals.solenoids2 = (coreGlobals.solenoids2 & (0xffffff00 | wpclocals.nonFlipBits)) | wpclocals.solFlip;
538:     wpclocals.solFlip = (wpclocals.solFlip & wpclocals.nonFlipBits) | wpclocals.solFlipPulse;
539:   }
```

## src/wpc/sim.c

SHA-256 `e85dd8b7ae6b1940e6b0f87899bf045256cb507d9c136e147b04b7957b1d3522`

```c
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
```

```c
244: /*--------------------
245: / Simulated solenoids
246: /---------------------*/
247: int sim_getSol(int solNo) {
248:   if (solNo == sShooterRel)
249:     return locals.shooterRel > 0;
250:   return 0;
251: }
```

## src/wpc/sim.h

SHA-256 `1b9511bf5c4cc05b64ae2177ea5575f02a51de4e58b35325859e71ee183c0a65`

```c
7: /* 111100  Updated solenoid numbering */
8: /* 161000  Updated input port to new BITIMP macro */
9: /* 070401  Added firstrow argument to sim_draw */
10: /*----------------------
11: / WPC driver constants
12: /-----------------------*/
13: #define sShooterRel       (CORE_FIRSTSIMSOL+0)  /* fake solenoid for ball shooter */
14:
15: /*-- Simulator inputport --*/
16: #define SIM_PORTS(balls) \
17:     /* 0x000f occupied */ \
18:     COREPORT_BIT(     0x8000, "Shoot Ball",       KEYCODE_SPACE) \
```
