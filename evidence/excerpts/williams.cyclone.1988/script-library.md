# VPinMAME script library - S11.VBS cabinet and flipper constants

`reviewed: true`; copied by the curator from the retained library on 2026-10-31
`source: external:pinmame-review-artifacts/vpm-script-libs/s11.vbs, SHA-256 5582155ffbdaeeeb3d86fcb54d7738d9ea5f9c24951b607e30a316f88dfd5f91`

Lines are quoted verbatim with their line numbers. The table loads `LoadVPM "00990300", "S11.VBS", 1.91`, a minimum
version; the retained machine-neutral copy is a later release (`'Last Updated in VBS v3.61`). The constants below are
the System 11 public addresses this table's key handlers write through `vpmKeyDown`/`vpmKeyUp`.

```vb
1: 'Last Updated in VBS v3.61
...
18: '-------------------------
19: ' S11 Data
20: '-------------------------
21: ' Flipper Solenoid
22: Const GameOnSolenoid = 23
23: ' Cabinet switches
24: Const swAdvance      = -7
25: Const swUpDown       = -6
26: Const swCPUDiag      = -5
27: Const swSoundDiag    = -4
28: Const swTilt         =  1
29: Const swBallRollTilt =  2
30: Const swStartButton  =  3
31: Const swCoin3        =  4
32: Const swCoin2        =  5
33: Const swCoin1        =  6
34: Const swSlamTilt     =  7
35: Const swHiScoreReset =  8
36:
37: Const swLRFlip       = 82
38: Const swLLFlip       = 84
39: Const swURFlip       = 81
40: Const swULFlip       = 83
```
