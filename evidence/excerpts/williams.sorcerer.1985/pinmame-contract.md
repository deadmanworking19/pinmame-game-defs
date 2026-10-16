# Pinned PinMAME source — the Sorcerer driver contract

`reviewed: true`; copied by the curator from the pinned checkout on 2026-10-16
`source: https://github.com/vpinball/pinmame at 97aa922bf8e4b6970126192ec1ac1fb0305a4f62`

Lines are quoted verbatim with their line numbers.

## src/wpc/driver.c

```c
2686: DRIVER(sorcr,l1)        //S9-532:   03/85 W Sorcerer (L-1)
2687: DRIVER(sorcr,l2)        //          03/85 W Sorcerer (L-2)
```

## src/wpc/s11games.c

```c
38: #define INITGAMEFULL(name, gen, disp, mux, flip, db, gs1, gs2, sc, ss17,ss18,ss19,ss20,ss21,ss22) \
39: static core_tGameData name##GameData = { \
40:   gen, disp, {flip,0,0,0,0,db,gs1,gs2}, NULL, {{0}}, {mux,{ss17,ss18,ss19,ss20,ss21,ss22}}}; \
41: static void init_##name(void) { core_gameData = &name##GameData; hc55516_set_sample_clock(0, sc); }
...
93: INITGAMEFULL(sorcr, GEN_S9, s11_dispS9, 0, FLIP_SWNO(0,44),
94:              S11_BCDDIAG|S11_BCDDISP,0,0,18181, 32,33,21,22,23,0)
...
103: #define input_ports_sorcr input_ports_s11
104: CORE_CLONEDEF(sorcr,l1,l2, "Sorcerer (L-1)", 1985, "Williams", s9_mS9S,0)
...
114: CORE_GAMEDEF(sorcr, l2, "Sorcerer (L-2)", 1985, "Williams", s9_mS9S,0)
```

Read against the macro: generation `GEN_S9`; display layout `s11_dispS9`; `mux` (`sxx.muxSol`) 0, so no A/C relay
and no C-side copies at 25-32; `hw.flippers = FLIP_SWNO(0,44)`, a right-button copy into matrix switch 44 and no
left-button copy, with no `FLIP_SOL`; `hw.swCol`, `hw.lampCol` and `hw.custSol` 0; `hw.display` (`db`)
`S11_BCDDIAG|S11_BCDDISP`; `gameSpecific1` and `gameSpecific2` 0 (no `S11_MUXSW2`, `S11_SNDOVERLAY` or
`S11_PRINTERLINE`); special-solenoid switches `sxx.ssSw = {32, 33, 21, 22, 23, 0}` for public 17-22. Both drivers
share this game data and ROM layout; they differ only in the U19/U20 game ROMs (L-1 `cpu_u19.732`/`cpu_u20.764`,
L-2 `cpu_u19.l2`/`cpu_u20.l2`) and share the U49 sound ROM and the four speech ROMs.

## src/wpc/s11.c

```c
56: core_tLCDLayout s11_dispS9[] = {
57:   {4, 0, 1,7, CORE_SEG87}, {4,16, 9,7, CORE_SEG87},
58:   {0, 0,21,7, CORE_SEG87}, {0,16,29,7, CORE_SEG87},
59:   DISP_SEG_CREDIT(0,8,CORE_SEG7S),DISP_SEG_BALLS(20,28,CORE_SEG7S),{0}
60: };
...
372: static READ_HANDLER (pia2a_r) { return core_getDip(0)<<7; }
...
907:   else if (strncasecmp(gn, "sorcr_", 6) == 0) { // Sorcerer
908:      core_set_pwm_output_type(CORE_MODOUT_SOL0 +  5 - 1, 3, CORE_MODOUT_BULB_89_25V_DC_S11);
909:      // Wired to a relay in the schematics, Labeled as "Flash eyes (cabinet)" but also as "Flipper Enable Relay" in the manual => left as is for the time being
910:      //core_set_pwm_output_type(CORE_MODOUT_SOL0 + 8 - 1, 1, CORE_MODOUT_BULB_89_25V_DC_S11);
911:      core_set_pwm_output_type(CORE_MODOUT_SOL0 + 11 - 1, 1, CORE_MODOUT_BULB_44_6_3V_AC_REV); // GI output
912:   }
```

The PWM block types public 5-7 as `#89` flash bulbs and 11 as a reversed 6.3 V AC GI output (relay energized
means GI off); it leaves 8 untyped and its comment records the same manual disagreement this definition settles
from the game's own table and the ROM's behaviour.

## src/wpc/s11.h and src/wpc/core.h

```c
s11.h:89:  #define S11_GAMEONSOL 23
s11.h:96:  #define S11_SWADVANCE     -7
s11.h:97:  #define S11_SWUPDN        -6
s11.h:98:  #define S11_SWCPUDIAG     -5
s11.h:99:  #define S11_SWSOUNDDIAG   -4
core.h:300: #define CORE_FIRSTCUSTSOL  51
core.h:301: #define CORE_FIRSTLFLIPSOL 45
core.h:302: #define CORE_FIRSTSIMSOL   49
core.h:305: #define CORE_SSFLIPENSOL  23
```

The S9 display layout publishes, in LibPinMAME index order, the lower-row 7-digit displays at segment starts 1
and 9 (indices 0 and 1), the upper-row 7-digit displays at 21 and 29 (indices 2 and 3), the credit digits at 0
and 8 (indices 4 and 5) and the ball-in-play/match digits at 20 and 28 (indices 6 and 7). The runtime evidence
shows player 1's score on index 2.
