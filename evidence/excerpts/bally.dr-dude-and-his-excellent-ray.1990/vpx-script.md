# Retained VPX runtime contract

Embedded script SHA-256 44f0924de1c33320134185cff9fa7cd09515497221b9ba0b805a4713c318a1eb, extracted with vpxtool git:v0.33.3 from the retained 2.3a filename. The header says Version 2.3; info.json says table_version 2.2. Neither label replaces the byte hashes.

The script selects dd_l2 and LoadVPM S11.VBS. It initializes a three-ball cvpmBallStack with switches 11,12,13 and BallRelease, a four-drop bank 21-24, cvpmTurnTable on trMixMaster, and cvpmMagnet on RMagnet. Solenoid callbacks: 1 stack SolIn; 2 stack SolOut; 3 left popper; 4 right popper; 6 knocker; 7 ResetDrops; 10 SetGI; 13 magnet; 14 Big Shot; 15 SetLamp115; 16 SolMixer; 25-32 SetLamp125-132. Lower flippers use the S11 library's synthetic outputs. Bumpers 1/2/3 pulse switches 52/53/54; slings pulse 55/56.

Drain pulses 10 then transfers the ball to the trough. Sw9 holds shooter occupancy. Sw14-16,25-31,33-38,41-43,46-50 pulse their named controller addresses; Sw17-20 and Sw59 hold while occupied. Drop targets hold down until output7 resets them. Popper ball detection is supplied by the saucer handling code; the eject timers clear 51/32 at step7. Their visual lift stages run on the table's timers and are implementation tuning, not physical timings.

LampTimer reads ChangedLamps into Lampz.state. Explicit MassAssign and Obj arrays select objects; Callback strings update primitives. Callback and MassAssign setters append, so repeated calls are cumulative. There is no vpmMapLights or TimerInterval lamp-address assignment. SortLamps is a visual intensity inventory and is not an address mapper. Lights and Flasher helpers never establish factory bulb quantities.

SetGI(True) cuts playfield G.I.; False restores it. The callback inverts output10 for its lamp-state110 visual. This is a solenoid-channel GI relay, not a dedicated GI callback. Table virtual color/apron/cheater-post/ray-beam options do not alter factory hardware.

The retained objects Sw19 and Sw20 lie in the left and right return lanes respectively while their script writes 19 and 20. The factory matrix, parts list, simulator and ROM names assign 19 Right Return and 20 Left Return; the location drawing misnumbers left return17 and right return20. Their physical coordinates therefore use the opposite lane object's geometry and disclose the table defect. Matrix flipper writes57/58 in the key handlers are overwritten by PinMAME; S11.vbs supplies the effective82/84 button bits.
