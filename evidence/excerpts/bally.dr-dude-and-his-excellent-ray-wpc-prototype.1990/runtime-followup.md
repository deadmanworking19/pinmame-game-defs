# WPC dedicated-input and flipper follow-up

Driver `dd_p7`; keyboard and built-in mechanics disabled. Every isolated run inherits only the hashed dd_p7 initialization NVRAM and models three balls with trough switches 23-25. Full traces, scenarios and summary are retained in `runtime-wpc-followup`. This evidence records displayed text and changed output callbacks, never host input readback as ROM evidence. Negative observations do not establish physical absence.

| Probe | Observed result |
| --- | --- |
| Matrix control 71 held | ROM displays I TEST TARGET |
| Flipper 112 held / released | ROM displays RIGHT FLIPPER; synthetic outputs 45/46 rise / fall |
| Flipper 114 held / released | ROM displays LEFT FLIPPER; synthetic outputs 47/48 rise / fall |
| 111, 113, 115, 116, 117, 118 each held / released | SWITCH LEVELS remained; no synthetic 45-48 transitions in those steps |
| Input 5 high, pulse 6 | Advances test: DISPLAY to SOUND TEST, then ALL LAMPS |
| Input 5 low at SOUND TEST, pulse 6 | Stays at test 02 and advances item 02 to 03 |
| Inputs 7 and 8, separately at MUSIC OFF | No displayed change or solenoid/lamp/GI transition during those steps |
| Matrix coin 14, two pulses | Displays CREDITS 1 then CREDITS 2 |
| Start 13 after matrix coin control | Displays BALL 1 and raises GAME ON output 31; credits decrease to 1 |
| No coin; dedicated coin inputs 1, 2, 3, 4 in separate two-pulse runs | No displayed credit or output 31/45-48 activity under these conditions |

The working matrix coin/start case is the positive control for the isolated coin cases. Dedicated inputs 1-4 and 7-8 and the six extra flipper bits retain unknown physical fitment and unproven ROM use. The test does not justify marking them unused. Source-level `WPC_FLIPPERS` reads the full complemented column, so nonresponse alone is not a reachability proof. Output 31 is observable pre-Fliptronic game-on state, included in `core_getAllSol`; the run does not prove game-specific relay wiring.

Summary SHA-256: `73b437403e0a7a821791550e1fa667849c1807ac02b423c197d78a955af7b824`. Full-bundle manifest SHA-256: `798b930956ef9a56a5676c633d5fbc12ad1da5142b4e2d7b04c1834a21a9a536`.

| Run | Trace SHA-256 | Scenario SHA-256 |
| --- | --- | --- |
| switch-levels | b1bc7a39b2787fec2c85bfc833ee64d9cafaa59593658f2cae068febcb7aa716 | 3d7342cf289002ef0e044935de110b507097605cfb3e6d930ad40c49bce992db |
| service-directions | aab6166427c9ba580f3ec309f02b734c076a3df87f76b215d2782a4be58c684c | da91e47270a281bb386fb44a13e6f6eb7a0630cbcd23fffb1244cb12fb4575b3 |
| service-music | 9b87d6af72540bfb2b3375a61873313dc9ede0a8eb6e7ee2dffd324ce973b71e | 287d55a4b9ba6a034821259f6d8a6975c3ab027f6ab865edf3a76eb009613f89 |
| coin-none | 62133e5290d7c5160e1f8368ef2243853447830f0084e46fc5517b791f53de2c | 35db3673abe3c9991af04f33b629b891b5d43b183c663555a01cff7353060792 |
| coin-1 | aec18c8bfb2fe3b2e8474f62e11a1b9c68e546030499b55c4bb9df993016ecce | 85cdab7f428adeee739c10065871edd6b4f2f54d3dd285b0421f1fa077d0740d |
| coin-2 | b6583b55f93190faa3c1e8924b0d6fefeaefd8c272edbaa925cfd7866c1ec13e | cbc6a8d3fb3231f026320fa106334eec59367d91bc8c631375cca1bcad81acb5 |
| coin-3 | 18d6468150508fbecd3e4d55ed32eb2b6fd2ae93c620174739bd575bf3fb322b | 730cb77de5ef7f212e1ec8072018483184e94e951c700c814f7d44f699e1a908 |
| coin-4 | 62b9f05a0838c2a42e3aa0bdbb8eaadc2315f4bb1e55a6075add3bf6023f4dd9 | 22f4b270058b3bff1e8c034536e9eb6e5ed8c8cc1cfb848a7d9d9bf5b97c010f |
| coin-14 | 8928b3cdb9d9321fe6e2b521914e40f60214a5154fdc501b921725b54e44f567 | ebf61ce2bda954c4ebfdfb5497e9faf2cb97afaf31613e8a87f4b37d23923838 |
