# FunHouse — owner trace of the orange G.I. string (Pinside)

Source: Pinside forum topic "Funhouse: GI wiring / electrical help please *SOLVED*" (Tech: Alpha-numeric), https://pinside.com/pinball/forum/topic/funhouse-gi-wiring-electrical-help-please, posts #1-#9, read 2026-10-23. Quoted passages are the posters' own words; only the parts about the G.I. string are transcribed.

| Post | Poster | Text |
| --- | --- | --- |
| #1 | pezpunk (owner) | "just picked up a Funhouse and I noticed that the GI spotlight that shines on Rudy as well as the lower third of the backbox GI are out. [...] they all seem to be on the same string -- the first wire is orange and the other is white with orange stripe." |
| #1 | pezpunk | "also checked and reseated J120 (where those wires seem to enter the board)" |
| #6 | pezpunk | "i still have the original problem with half the backbox plus the rudy spotlight being out though." |
| #7 | Schwaggs | "I suspect the pin you think is #4 is actually #8 which is the one that should have the Orange with White wire. Pin #2 should be the Orange wire. [...] The orange GI circuit uses F109." |
| #9 | pezpunk | "it was indeed the F109 fuse. [...] i replaced it and everything lit up." |

The owner's machine puts the spotlight that lights Rudy's face and the lower part of the backbox G.I. on one string: orange feed, white-orange return, J120-2/J120-8, fuse F109. The L-9 ROM's T.6 test prints exactly those wires, pins and fuse for public G.I. 1, RUDY / BACKGLASS, with triac Q10 (`evidence/runtime/wpc-alpha/funhouse-fh_l9-gi-test.json`).
