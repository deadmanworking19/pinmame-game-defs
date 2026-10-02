# Star Gazer — VPinMAME Stern library constants

The retained known-working table loads `stern.VBS` through `LoadVPM "01560000", "stern.VBS", 3.36`. The copy kept beside the table's extraction is the `stern.vbs` and `core.vbs` of the author's VPinMAME `Scripts` folder, header line `Last Updated in VBS v3.61`. The library, not the table, decides which public addresses the cabinet keys write; the table's own `Table1_KeyDown` forwards to it through `KeyDownHandler`.

`stern.vbs`, section "Stern MPUx00 Data", declares exactly these constants:

| constant | value |
| --- | ---: |
| `GameOnSolenoid` | 19 |
| `swSelfTest` | -7 |
| `swCPUDiag` | -6 |
| `swSoundDiag` | -5 |
| `swTilt` | 7 |
| `swSlamTilt` | 8 |
| `swCoin3` | 3 |
| `swCoin2` | 2 |
| `swCoin1` | 1 |
| `swStartButton` | 6 |
| `swLRFlip` | 82 |
| `swLLFlip` | 84 |
| `swURFlip` | 81 |
| `swULFlip` | 83 |

Its `vpmKeyDown` writes `swLLFlip` and `swLRFlip` when the left and right flipper keys go down, `swULFlip` and `swURFlip` only for the staged flipper keys when a second flipper solenoid is configured, and `swCoin1`, `swCoin2` and `swCoin3` (after a 750 ms timer) for the three coin keys. `core.vbs` declares `sLRFlipper = 46` and `sLLFlipper = 48`.
