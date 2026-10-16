# Retained System 9/11 VPinMAME library constants

`reviewed: true`; copied by the curator from the retained library on 2026-10-16
`source: external:pinmame-review-artifacts/vpm-script-libs/s11.vbs, SHA-256 5582155ffbdaeeeb3d86fcb54d7738d9ea5f9c24951b607e30a316f88dfd5f91`

The retained Sorcerer script loads this library (`LoadVPM "01550000", "S11.VBS", 3.26`). Its key handlers write `swLRFlip` and `swLLFlip`, PinMAME's flipper-column buttons 82 and 84. The upper constants 81 and 83 do not follow the PinMAME column; Sorcerer's upper flipper is wired to the left button and has no switch of its own.

```vb
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
