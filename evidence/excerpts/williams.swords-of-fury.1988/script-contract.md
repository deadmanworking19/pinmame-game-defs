# Retained table script contract

Source: embedded script SHA-256 719ed65888f146764f9490baea54f55d2acd210fbe807943823f2df89bacc717. Extracted using vpxtool git:v0.33.3; table not launched in VPX. These are literal selected source lines, not a known-working certification. Line numbers refer to the complete retained script.

## Controller and object assignments

```vb
124: Const cGameName = "swrds_l2"
146: 		.GameName = cGameName
147: 		If Err Then MsgBox "Can't start Game" & cGameName & vbNewLine & Err.Description : Exit Sub
179: 	Controller.Switch(11) = 1
180: 	Controller.Switch(12) = 1
181: 	Controller.Switch(13) = 1
246: 		If controller.switch(14) Then
271: SolCallback(1) = "SolOuthole"							'1 - Outhole
272: SolCallback(2) = "ReleaseBall"							'2 - Ball Release
273: SolCallback(4) = "SolLock"								'4 - Lock Kicker
274: SolCallback(5)	= "dt2up"								'5 drop2
275: SolCallback(6) = "SolKick"								'6 - Left Kicker
276: solcallback(7) = "SolKnocker" 							'7 - Bell
277: SolCallback(8)	= "dt3up"								'8 drop3
278: SolCallback(9) = "Flash9"								'9 top center flashers
279: SolCallback(10) = "PFGI"								'10 - GI Relay
280: 'SolCallback(11) = "Flash11"							'11 backglass sword flasher
281: 'SolCallback(13) = "Diverter"							'13 - Outlane Gate
282: SolCallback(14)="SolKickback"							'14 - outlane kickback
283: SolCallback(15)	= "dt1up"								'15 drop1
284: SolCallback(16)="Flash16" 								'16 kickback flasher
285: SolCallback(17)="BottomDiverter"
286: SolCallback(19)="TopDiverter"
287: SolCallback(21)	= "dt4up"								'21 drop4
288: SolCallback(22)	= "dt5up"								'22 drop5
289: SolCallback(25)="Flash25" 								'Sword and Stars Upper Playfield 1C, and VR BG Left sword monkey
290: SolCallback(26)="Flash26" 								'left loop flashers 2C
291: SolCallback(27)="Flash27" 								'tunnel flasher 3C
292: SolCallback(28)="Flash28" 								'ramp flasher 4C
293: SolCallback(29)="Flash29"								'left lockup flasher 5C
294: SolCallback(30)="Flash30" 								'balrog flasher 6C, and VR BG Upper Mid lighting chain
295: SolCallback(31)="Flash31" 								'left spinner flasher 7C
296: SolCallback(32)="Flash32" 								'shooter lane flasher 8C, and VR BG Main Monkey top
297: SolCallback(46)="Flash46"								'VR BG Small Lighting Chain
298: SolCallback(47)="Flash47"								'VR BG Small Lighting Chain (2nd one)
301: SolCallback(sLRFlipper) = "SolRFlipper"
302: SolCallback(sLLFlipper) = "SolLFlipper"
308: Sub Slot3_Hit():Controller.Switch(13) = 1:UpdateTrough:End Sub
309: Sub Slot3_UnHit():Controller.Switch(13) = 0:UpdateTrough:End Sub
310: Sub Slot2_Hit():Controller.Switch(12) = 1:UpdateTrough:End Sub
311: Sub Slot2_UnHit():Controller.Switch(12) = 0:UpdateTrough:End Sub
312: Sub Slot1_Hit():Controller.Switch(11) = 1:UpdateTrough:End Sub
313: Sub Slot1_UnHit():Controller.Switch(11) = 0:UpdateTrough:End Sub
333: 	Controller.Switch(10) = 1
337: 	Controller.Switch(10) = 0
361: 		If Controller.Switch(54) Then
367: 		Controller.Switch(54) = 0
372: 	Controller.Switch(54) = 1
384: 		Controller.Switch(55) = 0
389: 	Controller.Switch(55) = 1
411: 	Controller.Switch(57) = 1
416: 	Controller.Switch(57) = 0
513: 	vpmTimer.PulseSw 64
532: 	vpmTimer.PulseSw 63
562: Sub Sw17_Hit:DTHit 17:End Sub
563: Sub Sw18_Hit:DTHit 18:End Sub
564: Sub Sw19_Hit:DTHit 19:End Sub
565: Sub Sw20_Hit:DTHit 20:End Sub
566: Sub Sw21_Hit:DTHit 21:End Sub
578: Sub sw14_Hit:Controller.Switch(14)=1:End Sub
579: Sub sw14_unHit:Controller.Switch(14)=0:End Sub
580: Sub sw25_Hit:Controller.Switch(25)=1:wire002.transz=-5:End Sub
581: Sub sw25_unHit:Controller.Switch(25)=0:wire002.transz=0:End Sub
582: Sub sw48_Hit:Controller.Switch(48)=1:wire003.transz=-5:End Sub
583: Sub sw48_unHit:Controller.Switch(48)=0:wire003.transz=0:End Sub
584: Sub sw56_Hit:Controller.Switch(56)=1:End Sub
585: Sub sw56_unHit:Controller.Switch(56)=0:End Sub
586: Sub sw59_Hit:Controller.Switch(59)=1:wire004.transz=-5:End Sub
587: Sub sw59_unHit:Controller.Switch(59)=0:wire004.transz=0:End Sub
590: Sub sw15_Hit:vpmTimer.PulseSw 15:End Sub
591: Sub sw16_Hit:vpmTimer.PulseSw 16:End Sub
592: Sub sw38_Hit:vpmTimer.PulseSw 38:End Sub
593: Sub sw46_Hit:vpmTimer.PulseSw 46:End Sub
594: Sub sw47_Hit:vpmTimer.PulseSw 47:End Sub
597: Sub sw61_Hit:vpmTimer.PulseSw 61:End Sub
598: Sub sw62_Hit:vpmTimer.PulseSw 62:End Sub
601: Sub sw23_Spin():VPMTimer.PulseSw 23:SoundSpinner sw23:End Sub
602: Sub sw24_Spin():VPMTimer.PulseSw 24:SoundSpinner sw24:End Sub
603: Sub sw39_Spin():VPMTimer.PulseSw 39:SoundSpinner sw39:End Sub
606: Sub sw37_Hit:vpmTimer.PulseSw 37:End Sub
607: Sub sw40_Hit:vpmTimer.PulseSw 40:End Sub
631: DT17 = Array(sw17, sw17y, psw17, 17, 0)
632: DT18 = Array(sw18, sw18y, psw18, 18, 0)
633: DT19 = Array(sw19, sw19y, psw19, 19, 0)
634: DT20 = Array(sw20, sw20y, psw20, 20, 0)
635: DT21 = Array(sw21, sw21y, psw21, 21, 0)
802: 			controller.Switch(Switchid) = 1
856: 		controller.Switch(Switchid) = 0
1031: 		vpmTimer.PulseSw switch
2528: 	Lampz.MassAssign(1)= l1
2529: 	Lampz.MassAssign(1)= l1B
2530: 	Lampz.Callback(1) = "DisableLighting p1, 12,"
2531: 	Lampz.Callback(1) = "DisableLighting p1o, 22,"
2532: 	Lampz.MassAssign(2)= l2
2533: 	Lampz.MassAssign(2)= l2B
2534: 	Lampz.Callback(2) = "DisableLighting p2, 12,"
2535: 	Lampz.Callback(2) = "DisableLighting p2o, 22,"
2536: 	Lampz.MassAssign(3)= l3
2537: 	Lampz.MassAssign(3)= l3B
2538: 	Lampz.Callback(3) = "DisableLighting p3, 12,"
2539: 	Lampz.Callback(3) = "DisableLighting p3o, 22,"
2540: 	Lampz.MassAssign(4)= l4
2541: 	Lampz.MassAssign(4)= l4B
2542: 	Lampz.Callback(4) = "DisableLighting p4, 12,"
2543: 	Lampz.Callback(4) = "DisableLighting p4o, 22,"
2544: 	Lampz.MassAssign(5)= l5
2545: 	Lampz.MassAssign(5)= l5B
2546: 	Lampz.Callback(5) = "DisableLighting p5, 12,"
2547: 	Lampz.Callback(5) = "DisableLighting p5o, 22,"
2548: 	Lampz.MassAssign(6)= l6
2549: 	Lampz.MassAssign(6)= l6B
2550: 	Lampz.Callback(6) = "DisableLighting p6, 12,"
2551: 	Lampz.Callback(6) = "DisableLighting p6o, 22,"
2552: 	Lampz.MassAssign(7)= l7
2553: 	Lampz.MassAssign(7)= l7B
2554: 	Lampz.Callback(7) = "DisableLighting p7, 12,"
2555: 	Lampz.Callback(7) = "DisableLighting p7o, 22,"
2556: 	Lampz.MassAssign(9)= l9
2557: 	Lampz.MassAssign(9)= l9B
2558: 	Lampz.Callback(9) = "DisableLighting p9, 12,"
2559: 	Lampz.Callback(9) = "DisableLighting p9o, 22,"
2560: 	Lampz.MassAssign(10)= l10
2561: 	Lampz.MassAssign(10)= l10B
2562: 	Lampz.Callback(10) = "DisableLighting p10, 12,"
2563: 	Lampz.Callback(10) = "DisableLighting p10o, 22,"
2564: 	Lampz.MassAssign(11)= l11
2565: 	Lampz.MassAssign(11)= l11B
2566: 	Lampz.Callback(11) = "DisableLighting p11, 12,"
2567: 	Lampz.Callback(11) = "DisableLighting p11o, 22,"
2568: 	Lampz.MassAssign(12)= l12
2569: 	Lampz.MassAssign(12)= l12B
2570: 	Lampz.Callback(12) = "DisableLighting p12, 12,"
2571: 	Lampz.Callback(12) = "DisableLighting p12o, 22,"
2572: 	Lampz.MassAssign(13)= l13
2573: 	Lampz.MassAssign(13)= l13B
2574: 	Lampz.Callback(13) = "DisableLighting p13, 12,"
2575: 	Lampz.Callback(13) = "DisableLighting p13o, 22,"
2576: 	Lampz.MassAssign(14)= l14
2577: 	Lampz.MassAssign(14)= l14B
2578: 	Lampz.Callback(14) = "DisableLighting p14, 12,"
2579: 	Lampz.Callback(14) = "DisableLighting p14o, 22,"
2580: 	Lampz.MassAssign(15)= l15
2581: 	Lampz.MassAssign(15)= l15B
2582: 	Lampz.Callback(15) = "DisableLighting p15, 12,"
2583: 	Lampz.Callback(15) = "DisableLighting p15o, 22,"
2584: 	Lampz.MassAssign(16)= l16
2585: 	Lampz.MassAssign(16)= l16B
2586: 	Lampz.Callback(16) = "DisableLighting p16, 12,"
2587: 	Lampz.Callback(16) = "DisableLighting p16o, 12,"
2588: 	Lampz.Callback(16) = "DisableLightingMinMax speciallamp, 1, 40,"
2589: 	Lampz.Callback(17) = "DisableLighting droplamp1, 6,"
2590: 	Lampz.Callback(18) = "DisableLighting droplamp2, 6,"
2591: 	Lampz.Callback(19) = "DisableLighting droplamp3, 6,"
2592: 	Lampz.Callback(20) = "DisableLighting droplamp4, 6,"
2593: 	Lampz.Callback(21) = "DisableLighting droplamp5, 6,"
2594: '	Lampz.MassAssign(17)= l17
2595: '	Lampz.MassAssign(17)= l17B
2596: '	Lampz.Callback(17) = "DisableLighting p17, 12,"
2597: '	Lampz.Callback(17) = "DisableLighting p17o, 22,"
2598: '	Lampz.MassAssign(18)= l18
2599: '	Lampz.MassAssign(18)= l18B
2600: '	Lampz.Callback(18) = "DisableLighting p18, 12,"
2601: '	Lampz.Callback(18) = "DisableLighting p18o, 22,"
2602: '	Lampz.MassAssign(19)= l19
2603: '	Lampz.MassAssign(19)= l19B
2604: '	Lampz.Callback(19) = "DisableLighting p19, 12,"
2605: '	Lampz.Callback(19) = "DisableLighting p19o, 22,"
2606: '	Lampz.MassAssign(20)= l20
2607: '	Lampz.MassAssign(20)= l20B
2608: '	Lampz.Callback(20) = "DisableLighting p20, 12,"
2609: '	Lampz.Callback(20) = "DisableLighting p20o, 22,"
2610: '	Lampz.MassAssign(21)= l21
2611: '	Lampz.MassAssign(21)= l21B
2612: '	Lampz.Callback(21) = "DisableLighting p21, 12,"
2613: '	Lampz.Callback(21) = "DisableLighting p21o, 22,"
2614: 	Lampz.MassAssign(22)= l22
2615: 	Lampz.MassAssign(22)= l22B
2616: 	Lampz.Callback(22) = "DisableLighting p22, 12,"
2617: 	Lampz.Callback(22) = "DisableLighting p22o, 22,"
2618: 	Lampz.MassAssign(23)= l23
2619: 	Lampz.MassAssign(23)= l23B
2620: 	Lampz.Callback(23) = "DisableLighting p23, 12,"
2621: 	Lampz.Callback(23) = "DisableLighting p23o, 22,"
2622: 	Lampz.MassAssign(24)= l24
2623: 	Lampz.MassAssign(24)= l24B
2624: 	Lampz.Callback(24) = "DisableLighting p24, 12,"
2625: 	Lampz.Callback(24) = "DisableLighting p24o, 12,"
2626: '	Lampz.MassAssign(25)= l25
2627: '	Lampz.MassAssign(25)= l25B
2628: '	Lampz.Callback(25) = "DisableLightingMinMax p25, 1, 1.8,"
2629: '	Lampz.Callback(27) = "DisableLightingMinMax p25off, 1, 2,"
2630: '	Lampz.Callback(25) = "DisableLightingMinMax bumperskirt001, 1, 1.01,"
2631: 	Lampz.MassAssign(26)= l26
2632: 	Lampz.MassAssign(26)= l26B
2633: 	Lampz.Callback(26) = "DisableLighting p26, 12,"
2634: 	Lampz.Callback(26) = "DisableLighting p26o, 12,"
2635: 	Lampz.MassAssign(27)= l27
2636: 	Lampz.MassAssign(27)= l27B
2637: 	Lampz.Callback(27) = "DisableLighting p27, 12,"
2638: 	Lampz.Callback(27) = "DisableLighting p27o, 12,"
2639: 	Lampz.MassAssign(28)= l28
2640: 	Lampz.MassAssign(28)= l28B
2641: 	Lampz.Callback(28) = "DisableLighting p28, 12,"
2642: 	Lampz.Callback(28) = "DisableLighting p28o, 12,"
2643: 	Lampz.MassAssign(29)= l29
2644: 	Lampz.MassAssign(29)= l29B
2645: 	Lampz.Callback(29) = "DisableLighting p29, 12,"
2646: 	Lampz.Callback(29) = "DisableLighting p29o, 22,"
2647: 	Lampz.MassAssign(30)= l30
2648: 	Lampz.MassAssign(30)= l30B
2649: 	Lampz.Callback(30) = "DisableLighting p30, 12,"
2650: 	Lampz.Callback(30) = "DisableLighting p30o, 22,"
2651: 	Lampz.MassAssign(31)= l31
2652: 	Lampz.MassAssign(31)= l31B
2653: 	Lampz.Callback(31) = "DisableLighting p31, 12,"
2654: 	Lampz.Callback(31) = "DisableLighting p31o, 22,"
2655: 	Lampz.MassAssign(32)= l32
2656: 	Lampz.MassAssign(32)= l32B
2657: 	Lampz.Callback(32) = "DisableLighting p32, 12,"
2658: 	Lampz.Callback(32) = "DisableLighting p32o, 22,"
2659: 	Lampz.MassAssign(33)= l33
2660: 	Lampz.MassAssign(33)= l33B
2661: 	Lampz.Callback(33) = "DisableLighting p33, 12,"
2662: 	Lampz.Callback(33) = "DisableLighting p33o, 12,"
2663: 	Lampz.MassAssign(34)= l34
2664: 	Lampz.MassAssign(34)= l34B
2665: 	Lampz.Callback(34) = "DisableLighting p34, 12,"
2666: 	Lampz.Callback(34) = "DisableLighting p34o, 12,"
2667: 	Lampz.MassAssign(35)= l35
2668: 	Lampz.MassAssign(35)= l35B
2669: 	Lampz.Callback(35) = "DisableLighting p35, 12,"
2670: 	Lampz.Callback(35) = "DisableLighting p35o, 12,"
2671: 	Lampz.MassAssign(36)= l36
2672: 	Lampz.MassAssign(36)= l36B
2673: 	Lampz.Callback(36) = "DisableLighting p36, 12,"
2674: 	Lampz.Callback(36) = "DisableLighting p36o, 12,"
2675: '	Lampz.MassAssign(37)= l37
2676: '	Lampz.MassAssign(37)= l37B
2677: '	Lampz.Callback(37) = "DisableLighting p37, 12,"
2678: '	Lampz.Callback(37) = "DisableLighting p37o, 22,"
2679: 	Lampz.MassAssign(38)= l38
2680: 	Lampz.MassAssign(38)= l38B
2681: 	Lampz.Callback(38) = "DisableLighting p38, 12,"
2682: 	Lampz.Callback(38) = "DisableLighting p38o, 12,"
2683: 	Lampz.MassAssign(39)= l39
2684: 	Lampz.MassAssign(39)= l39B
2685: 	Lampz.Callback(39) = "DisableLighting p39, 12,"
2686: 	Lampz.Callback(39) = "DisableLighting p39o, 12,"
2687: 	Lampz.MassAssign(40)= l40
2688: 	Lampz.MassAssign(40)= l40B
2689: 	Lampz.Callback(40) = "DisableLighting p40, 12,"
2690: 	Lampz.Callback(40) = "DisableLighting p40o, 22,"
2691: 	Lampz.MassAssign(41)= l41
2692: 	Lampz.MassAssign(41)= l41B
2693: 	Lampz.Callback(41) = "DisableLighting p41, 12,"
2694: 	Lampz.Callback(41) = "DisableLighting p41o, 22,"
2695: 	Lampz.MassAssign(42)= l42
2696: 	Lampz.MassAssign(42)= l42B
2697: 	Lampz.Callback(42) = "DisableLighting p42, 12,"
2698: 	Lampz.Callback(42) = "DisableLighting p42o, 22,"
2699: 	Lampz.MassAssign(43)= l43
2700: 	Lampz.MassAssign(43)= l43B
2701: 	Lampz.Callback(43) = "DisableLighting p43, 12,"
2702: 	Lampz.Callback(43) = "DisableLighting p43o, 22,"
2703: 	Lampz.MassAssign(44)= l44
2704: 	Lampz.MassAssign(44)= l44B
2705: 	Lampz.Callback(44) = "DisableLighting p44, 12,"
2706: 	Lampz.Callback(44) = "DisableLighting p44o, 22,"
2707: 	Lampz.MassAssign(45)= l45
2708: 	Lampz.MassAssign(45)= l45B
2709: 	Lampz.Callback(45) = "DisableLighting p45, 12,"
2710: 	Lampz.Callback(45) = "DisableLighting p45o, 22,"
2711: 	Lampz.Callback(46) = "DisableLightingMinMax ramplamp001, 1, 75,"
2712: 	Lampz.Callback(47) = "DisableLightingMinMax ramplamp002, 1, 75,"
2713: 	Lampz.Callback(48) = "DisableLightingMinMax ramplamp003, 1, 75,"
2714: '	Lampz.MassAssign(46)= l46
2715: '	Lampz.MassAssign(46)= l46B
2716: '	Lampz.MassAssign(47)= l47
2717: '	Lampz.MassAssign(47)= l47B
2718: '	Lampz.Callback(47) = "DisableLighting p47, 12,"
2719: '	Lampz.Callback(47) = "DisableLighting p47o, 22,"
2720: '	Lampz.MassAssign(48)= l48
2721: '	Lampz.MassAssign(48)= l48B
2722: '	Lampz.Callback(48) = "DisableLighting p48, 12,"
2723: '	Lampz.Callback(48) = "DisableLighting p48o, 22,"
2724: 	Lampz.MassAssign(49)= l49
2725: 	Lampz.MassAssign(49)= l49B
2726: 	Lampz.Callback(49) = "DisableLighting p49, 12,"
2727: 	Lampz.Callback(49) = "DisableLighting p49o, 12,"
2728: 	Lampz.MassAssign(50)= l50
2729: 	Lampz.MassAssign(50)= l50B
2730: 	Lampz.Callback(50) = "DisableLighting p50, 12,"
2731: 	Lampz.Callback(50) = "DisableLighting p50o, 12,"
2732: 	Lampz.MassAssign(51)= l51
2733: 	Lampz.MassAssign(51)= l51B
2734: 	Lampz.Callback(51) = "DisableLighting p51, 12,"
2735: 	Lampz.Callback(51) = "DisableLighting p51o, 22,"
2736: 	Lampz.MassAssign(52)= l52
2737: 	Lampz.MassAssign(52)= l52B
2738: 	Lampz.Callback(52) = "DisableLighting p52, 12,"
2739: 	Lampz.Callback(52) = "DisableLighting p52o, 22,"
2740: 	Lampz.MassAssign(53)= l53
2741: 	Lampz.MassAssign(53)= l53B
2742: 	Lampz.Callback(53) = "DisableLighting p53, 12,"
2743: 	Lampz.Callback(53) = "DisableLighting p53o, 22,"
2744: 	Lampz.MassAssign(54)= l54
2745: 	Lampz.MassAssign(54)= l54B
2746: 	Lampz.Callback(54) = "DisableLighting p54, 12,"
2747: 	Lampz.Callback(54) = "DisableLighting p54o, 22,"
2748: 	Lampz.MassAssign(55)= l55
2749: 	Lampz.MassAssign(55)= l55B
2750: 	Lampz.Callback(55) = "DisableLighting p55, 12,"
2751: 	Lampz.Callback(55) = "DisableLighting p55o, 22,"
2752: 	Lampz.MassAssign(56)= l56
2753: 	Lampz.MassAssign(56)= l56B
2754: 	Lampz.Callback(56) = "DisableLighting p56, 12,"
2755: 	Lampz.Callback(56) = "DisableLighting p56o, 22,"
2756: 	Lampz.MassAssign(109)= FL_9
2757: '	Lampz.MassAssign(125)= FL_25
2758: 	Lampz.Callback(125) = "DisableLighting p125, 42,"
2759: 	Lampz.Callback(125) = "DisableLighting p125o, 52,"
2760: 	Lampz.MassAssign(125)= FL_25
2761: 	Lampz.MassAssign(127)= FL_27
2762: 	Lampz.MassAssign(128)= FL_28
2763: 	Lampz.MassAssign(129)= FL_29
2764: 	Lampz.MassAssign(130)= FL_30
2765: 	Lampz.MassAssign(131)= FL_31
2766: 	Lampz.MassAssign(132)= FL_32
2771: 	For each x in GI:Lampz.MassAssign(111) = x:Next
2772: 	Lampz.Callback(111) = "GIUpdates"
2778: 	Lampz.MassAssign(57) = VR_05Mil
2779: 	Lampz.MassAssign(58) = VR_1Mil
2780: 	Lampz.MassAssign(59) = VR_15Mil
2781: 	Lampz.MassAssign(60) = VR_2Mil
2782: 	Lampz.MassAssign(61) = VR_25Mil
2783: 	Lampz.MassAssign(62) = VR_3Mil
2784: 	Lampz.MassAssign(63) = VR_35Mil
2785: 	Lampz.MassAssign(64) = VR_4Mil
2786: 	Lampz.MassAssign(41) = VR_20K
2787: 	Lampz.MassAssign(42) = VR_30K
2788: 	Lampz.MassAssign(51) = VR_40K
2789: 	Lampz.MassAssign(52) = VR_50K
2790: 	Lampz.MassAssign(6) = VR_100K
2791: 	Lampz.MassAssign(7) = VR_500K
2792: 	Lampz.MassAssign(125) = BGFL25
2793: 	Lampz.Callback(125) = "BGLamps"
2794: 	Lampz.MassAssign(130) = BGFL30
2795: 	Lampz.Callback(130) = "BGLamps"
2796: 	Lampz.MassAssign(132) = BGFL32
2797: 	Lampz.Callback(132) = "BGLamps"
2798: 	Lampz.MassAssign(138) = BGFL46
2799: 	Lampz.Callback(138) = "BGLamps"
2800: 	Lampz.MassAssign(139) = BGFL47
2801: 	Lampz.Callback(139) = "BGLamps"
```

## Consumed routines

```vb
2440: Sub PFGI(Enabled)
2441: 	If Enabled Then  ' GI state inverted, enabled = OFF
2442: 		dim xx
2443: '		For each xx in UV1col:xx.image="UV1off": Next
2444: '		sw37.image="spin1off"
2445: 		SetLamp 111, 0
2446:         GIIsOff=true
2447: 	Else
2448: '		For each xx in UV1col:xx.image="UV1": Next
2449: '		sw37.image="spin1"
2450: 		SetLamp 111, 5
2451:         GIIsOff=false
2452: 	End If
2453: 	' Update lamps that may swap textures when GI changes here
2454: '	SetLamp 110, Not Enabled
2455: '	SetLamp 111, Enabled
2456: '	UpdateLamp25
2457: '	UpdateLamp26
2458: '	UpdateLamp27
2459: 	Sound_GI_Relay enabled, Relay_11
2460: End Sub
```

```vb
1060: Sub SolLFlipper(Enabled)
1061: 	If Enabled Then
1062: 		LF.Fire
1063: 		LF1.Fire
1064: 		If leftflipper.currentangle < leftflipper.endangle + ReflipAngle Then
1065: 			RandomSoundReflipUpLeft LeftFlipper
1066: 		Else
1067: 			SoundFlipperUpAttackLeft LeftFlipper
1068: 			RandomSoundFlipperUpLeft LeftFlipper
1069: 		End If
1070: 	Else
1071: 		LeftFlipper.RotateToStart
1072: 		leftflipper001.rotatetostart
1073: 		If LeftFlipper.currentangle < LeftFlipper.startAngle - 5 Then
1074: 			RandomSoundFlipperDownLeft LeftFlipper
1075: 		End If
1076: 		FlipperLeftHitParm = FlipperUpSoundLevel
1077: 	End If
1078: End Sub
```

```vb
1080: Sub SolRFlipper(Enabled)
1081: 	If Enabled Then
1082: 		RF.Fire 'rightflipper.rotatetoend
1083: 		RightFlipper001.rotatetoend
1084: 		If rightflipper.currentangle > rightflipper.endangle - ReflipAngle Then
1085: 			RandomSoundReflipUpRight RightFlipper
1086: 		Else
1087: 			SoundFlipperUpAttackRight RightFlipper
1088: 			RandomSoundFlipperUpRight RightFlipper
1089: 		End If
1090: 	Else
1091: 		RightFlipper.RotateToStart
1092: 		RightFlipper001.rotatetostart
1093: 		If RightFlipper.currentangle > RightFlipper.startAngle + 5 Then
1094: 			RandomSoundFlipperDownRight RightFlipper
1095: 		End If
1096: 		FlipperRightHitParm = FlipperUpSoundLevel
1097: 	End If
1098: End Sub
```

```vb
340: Sub SolOuthole(enabled)
341: 	If enabled Then
342: 		Drain.kick 60,20
343: 		'SoundSaucerKick 0, Drain
344: 	End If
345: End Sub
```

```vb
347: Sub ReleaseBall(enabled)
348: 	If enabled Then
349: 		RandomSoundBallRelease Slot1
350: 		Slot1.kick 60, 7
351: 		UpdateTrough
352: 	End If
353: End Sub
```

```vb
359: Sub SolLock(enabled)
360: 	If enabled Then
361: 		If Controller.Switch(54) Then
362: 			SoundSaucerKick 1, sw54
363: 		Else
364: 			SoundSaucerKick 0, sw54
365: 		End If
366: 		sw54.kick 180 + Rnd*4, 6 + Rnd*4
367: 		Controller.Switch(54) = 0
368: 	End If
369: End Sub
```

```vb
380: Sub SolKick(enabled)
381: 	If enabled Then
382: 		SoundSaucerKick 1, sw55
383: 		sw55.kick 0 + Rnd*4, 46 + Rnd*4
384: 		Controller.Switch(55) = 0
385: 	End If
386: End Sub
```

```vb
474: Sub BottomDiverter(Enabled)
475:  	If Enabled then
476: 		Playsoundat "soloff", knockerposition
477: 		bottomgate.rotatetoend
478: 	Else
479: 		Playsoundat "soloff", knockerposition
480: 		bottomgate.rotatetostart
481:  	end if
482: End Sub
```

```vb
484: Sub TopDiverter(Enabled)
485:  	If Enabled then
486: 		Playsoundat "soloff", knockerposition
487: 		topgate.rotatetoend
488: 	Else
489: 		Playsoundat "soloff", knockerposition
490: 		topgate.rotatetostart
491:  	end if
492: End Sub
```
