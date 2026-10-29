# A3 driver board output region

Source: game 712 manual PDF pages 33-34, printed 27-28, driver board E-20915 (shared board drawing). Curator visual transcription. These are board-internal identities, not a claim that every output has a fitted game harness. Q-bar branches are distinguished from the non-inverted latch outputs.

| Lamp | Transistor | Connector-pin | Literal annotation when present |
| ---: | --- | --- | --- |
| 0 | Q1 MPS-U45 | A3J3-A | GAME OVER RELAY (PLAYFIELD) |
| 1 | Q2 MPS-U45 | A3J3-B | TILT RELAY (PLAYFIELD) |
| 2 | Q3 MPS-U45 | A3J5-2 | [blank function] |
| 3 | Q4 MPS-U45 | A3J3-C; parallel A3J2-1 | SHOOT AGAIN (PLAYFIELD) |
| 4 | Q5 MPS-A13 | A3J2-2 | SOUND 16 |
| 5 | Q6 MPS-A13 | A3J2-3 | [blank function] |
| 6 | Q7 MPS-A13 | A3J2-5 | [blank function] |
| 7 | Q8 MPS-A13 | A3J2-4 | [blank function] |
| 8 | Q9 MPS-A13 | A3J2-10 | [blank function] |
| 9 | Q10 MPS-A13 | A3J2-9 | [blank function] |
| 10 | Q11 MPS-A13 | A3J2-7 | [blank function] |
| 11 | Q12 MPS-A13 | A3J2-8 | [blank function] |
| 12 | Q13 MPS-U45 | A3J3-25 | [blank function] |
| 13 | Q14 MPS-U45 | A3J3-24 | [blank function] |
| 14 | Q15 MPS-U45 | A3J3-22 | [blank function] |
| 15 | Q16 MPS-U45 | A3J3-23 | [blank function] |
| 16 | Q17 MPS-U45 | A3J3-13 | [blank function] |
| 17 | Q18 MPS-U45 | A3J3-14 | [blank function] |
| 18 | Q19 MPS-U45 | A3J3-16 | [blank function] |
| 19 | Q20 MPS-U45 | A3J3-15 | [blank function] |
| 20 | Q21 MPS-U45 | A3J3-21 | [blank function] |
| 21 | Q22 MPS-U45 | A3J3-20 | [blank function] |
| 22 | Q23 MPS-U45 | A3J3-18 | [blank function] |
| 23 | Q24 MPS-U45 | A3J3-19 | [blank function] |
| 24 | Q25 MPS-U45 | A3J3-9 | [blank function] |
| 25 | Q26 MPS-U45 | A3J3-10 | [blank function] |
| 26 | Q27 MPS-U45 | A3J3-12 | [blank function] |
| 27 | Q28 MPS-U45 | A3J3-11 | [blank function] |
| 28 | Q29 MPS-U45 | A3J3-Y | [blank function] |
| 29 | Q30 MPS-U45 | A3J3-X | [blank function] |
| 30 | Q31 MPS-U45 | A3J3-V | [blank function] |
| 31 | Q32 MPS-U45 | A3J3-W | [blank function] |
| 32 | Q33 MPS-A13 | A3J3-5 | [blank function] |
| 33 | Q34 MPS-A13 | A3J3-6 | [blank function] |
| 34 | Q35 MPS-A13 | A3J3-K | [blank function] |
| 35 | Q36 MPS-A13 | A3J3-7 | [blank function] |
| 36 | Q37 MPS-A13 | A3J4-1 | [blank function] |
| 37 | Q38 MPS-A13 | A3J4-2 | [blank function] |
| 38 | Q39 MPS-A13 | A3J4-4 | [blank function] |
| 39 | Q40 MPS-A13 | A3J4-3 | [blank function] |
| 40 | Q41 MPS-A13 | A3J3-4 | [blank function] |
| 41 | Q42 MPS-A13 | A3J3-3 | [blank function] |
| 42 | Q43 MPS-A13 | A3J3-T | [blank function] |
| 43 | Q44 MPS-A13 | A3J3-2 | [blank function] |
| 44 | Q45 MPS-U45 | A3J3-D | Z12 Q1 |
| 45 | Q46 MPS-U45 | A3J3-F | Z12 Q2 |
| 46 | Q47 MPS-U45 | A3J3-P | Z12 Q3 |
| 47 | Q48 MPS-U45 | A3J3-M | Z12 Q4 |
| 48 | Q49 MPS-U45 | A3J3-E | Z12 Q1-bar |
| 49 | Q50 MPS-U45 | A3J3-H | Z12 Q2-bar |
| 50 | Q51 MPS-U45 | A3J3-R | Z12 Q3-bar |
| 51 | Q52 MPS-U45 | A3J3-N | Z12 Q4-bar |

Connector labels are transcribed locally beside each output. This shared schematic repeats some connector/pin labels across separately drawn blocks; no ground or supply pinout is inferred from those repetitions. Consult the game-specific harness before connecting hardware.

| Solenoid | A3 transistor path | Connector-pin | Printed branch |
| ---: | --- | --- | --- |
| 1 | Q60 2N6043 | A3J4-7 | CR6 1N4148; ground A3J4-9 |
| 2 | Q57 MPS-U45; Q58 2N3055 | A3J4-13 | R53/R54/R55; ground A3J4-10 |
| 3 | Q54 MPS-U45 | A3J6-3 | see note4 |
| 4 | Q55 MPS-U45 | A3J6-2 | see note4 |
| 5 | Q61 MPS-U45; Q62 2N3055 | A3J4-6 | R56/R57/R58; ground A3J4-14 |
| 6 | Q63 MPS-U45; Q64 2N3055 | A3J4-12 | R59/R60/R61; ground A3J4-11 |
| 7 | Q56 MPS-U45 | A3J6-1 | see note4; common ground A3J6-4 |
| 8 | Q53 2N6043 | A3J5-8 | CR1 1N4148; ground A3J5-3 |
| 9 | Q59 2N6043 | A3J4-8 | CR5 1N4148; ground A3J4-9 |

Notes on page 28: unless specified, resistors are 1000 ohms ±5%, 1/4 W; capacitors are .01 uF ±20%, 50 V; integrated circuits are SN74175N. Jumper wires replace diodes CR2, CR3 and CR4 for System 80A/80B. Transistor types MPS-U45 and NDS-U45 are interchangeable.

Game-specific wiring readings remain literal. PDF 47/54 prints Q as L3 where this board explicitly prints L0. PDF 48 / printed 42 clearly prints L21 at A3J3-22, wire 322; the board instead provides Q22/public 21 at A3J3-20 and Q15/public 14 at A3J3-22. Its narrow L43 pin glyph, wire 744, is E or 2 and remains ambiguous; this board provides Q44/public 43 at A3J3-2 and Q49/public 48 at A3J3-E. The lamp-table transcription marks that uncertainty explicitly rather than presenting E as settled. Some L24/L25 pin glyphs are also narrow; no source-backed public-address disagreement is inferred from them.

Structured wiring on provisions 14/48/49 follows only these board-internal Q/pin paths, not a resolved game harness or fitted load. The L21 pin-22 reading and possible L43 pin-E reading are positive game-table observations that must be disclosed on provisions 14/48 and lamps 21/43. Their actual harness interpretation remains unverified; lamp 21/43 harness pins stay unset. Runtime bindings 21/43 do not independently measure a physical connector, and neither diagnostic sweeps nor omitted assignment rows settle fitment. These are wiring-detail notes, not blocking physical conflicts.
