# Pinned PinMAME source — the Space Shuttle driver contract

`reviewed: true`; copied by the curator from the pinned checkout on 2026-10-30
`source: https://github.com/vpinball/pinmame at 46e1a01a0f73dc5ce163d98db1ae435883ecc450`

Lines are quoted verbatim with their line numbers.

## src/wpc/driver.c

```c
2713: DRIVER(sshtl,l3)        //S9-535:   12/84 W Space Shuttle (L-3)
2714: DRIVER(sshtl,l7)        //          12/84 W Space Shuttle (L-7)
```

`sshtlzac`/`sshtlzacf` (driver.c 3570-3571) are the unrelated 1980 Zaccaria Space Shuttle.

## src/wpc/s11games.c

```c
38: #define INITGAMEFULL(name, gen, disp, mux, flip, db, gs1, gs2, sc, ss17,ss18,ss19,ss20,ss21,ss22) \
39: static core_tGameData name##GameData = { \
40:   gen, disp, {flip,0,0,0,0,db,gs1,gs2}, NULL, {{0}}, {mux,{ss17,ss18,ss19,ss20,ss21,ss22}}}; \
41: static void init_##name(void) { core_gameData = &name##GameData; hc55516_set_sample_clock(0, sc); }
...
64: static core_tLCDLayout dispSshtl[] = { \
65:   { 0, 0,21,7, CORE_SEG87},
66:   { 2, 0,29,7, CORE_SEG87},
67:   { 4, 0, 1,7, CORE_SEG87}, { 4,26, 9,7,CORE_SEG87},
68:   { 5,16, 0,1, CORE_SEG7},  { 5,18, 8,1,CORE_SEG7},
69:   { 5,21,20,1, CORE_SEG7},  { 5,23,28,1,CORE_SEG7},{0}
70: };
71: INITGAMEFULL(sshtl, GEN_S9, dispSshtl, 0, FLIP_SWNO(0,41),
72:              S11_BCDDIAG|S11_BCDDISP,0,0,18867, 39, 40, 27, 26, 25, 0)
73: S9_ROMSTARTx4(sshtl,l7,"cpu_u20.128", CRC(848ad54c) SHA1(4e4ce5fb970da37706472f94a27fd912e1ecb1a0))
74: S9S_SOUNDROM4111(      "cpu_u49.128", CRC(8050ae27) SHA1(e3f5e9398f61b075620ecd075617a8dac3c07d0e),
...
80: CORE_GAMEDEF(sshtl, l7, "Space Shuttle (L-7)", 1984, "Williams", s9_mS9S,0)
82: S9_ROMSTARTx4(sshtl,l3,"cpu_u20.l3", CRC(dc5f08e0) SHA1(67869c1db4e1f49f38588978d4ed32fe7d62e2d6))
...
88: CORE_CLONEDEF(sshtl, l3, l7, "Space Shuttle (L-3)", 1984, "Williams", s9_mS9S,0)
```

Read against the macro: generation `GEN_S9`; display layout `dispSshtl`; `mux` (`sxx.muxSol`) 0, so no A/C relay
and no C-side copies at 25-32; `hw.flippers = FLIP_SWNO(0,41)`, a right-button copy into matrix switch 41 and no
left-button copy, with no `FLIP_SOL`; `hw.display` `S11_BCDDIAG|S11_BCDDISP`; `gameSpecific1` and
`gameSpecific2` 0 (no `S11_MUXSW2`, `S11_SNDOVERLAY` or `S11_PRINTERLINE`); special-solenoid switches
`sxx.ssSw = {39, 40, 27, 26, 25, 0}` for public 17-22. Both drivers share this game data and the U49 sound and
U4-U6 speech ROMs; they differ only in the U20 game ROM.

The `ssSw` order pairs 19 with switch 27, 20 with 26 and 21 with 25. The game's own solenoid table, solenoid
and switch location lists and playfield wiring diagram pair 19 (Left Jet-Bumper) with switch 25 (Left Jet), 20
(Lower Jet-Bumper) with 27 (Lower Jet) and 21 (Right Jet-Bumper) with 26 (Right Jet). The emulator therefore
publishes the left jet's switch on the right-jet coil and so on; the harness shows it (switch 25 publishes 21,
26 publishes 20, 27 publishes 19).

The display layout publishes, in LibPinMAME index order, player 1 at segment start 21 (index 0), player 2 at 29
(1), player 3 at 1 (2), player 4 at 9 (3), the credit digits at 0 and 8 (4 and 5) and the ball-in-play/match
digits at 20 and 28 (6 and 7).

## src/wpc/s11.c

```c
194:      if (core_gameData->sxx.ssSw[ii]) {
195:        int switchState = core_getSw(core_gameData->sxx.ssSw[ii]);
...
372: static READ_HANDLER (pia2a_r) { return core_getDip(0)<<7; }
...
919:   else if (strncasecmp(gn, "sshtl_", 6) == 0) { // Space Shuttle
920:      core_set_pwm_output_type(CORE_MODOUT_SOL0 +  9 - 1, 2, CORE_MODOUT_BULB_89_25V_DC_S11);
921:      core_set_pwm_output_type(CORE_MODOUT_SOL0 + 11 - 1, 1, CORE_MODOUT_BULB_44_6_3V_AC_REV); // GI output
922:      core_set_pwm_output_type(CORE_MODOUT_SOL0 + 14 - 1, 1, CORE_MODOUT_BULB_89_25V_DC_S11);
923:   }
```

The PWM block types public 9, 10 and 14 as `#89` flash bulbs and 11 as a reversed 6.3 V AC GI output (relay
energized means GI off).

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

The harness ran the `sshtl_l7` ROM archive whose U20 game ROM matches the CRC above; its `cpu_u49.128` sound ROM
reads CRC 20e77990 rather than the listed 8050ae27. The sound ROM does not drive the switch matrix, solenoids or
lamps; the L-3 run used the matching archive.
