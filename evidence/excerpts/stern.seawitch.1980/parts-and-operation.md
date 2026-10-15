# Seawitch parts, service and physical operation

Sources: manual PDF pages 3-6, 8-10, 16-17. Tables below preserve complete factual regions. Dotted leaders and heading punctuation are normalized; wording/part numbers are literal.

## Complete parts list, PDF page 16

| MISCELLANEOUS | PART NUMBER |
| --- | --- |
| Transformer (Domestic or Export) | 16B-6 |
| Transformer & Rectifier Board | B-438-2 |
| Bulbs, #44 | 8A-101 |
| U1 | 25A-E-1 |
| U2 | 25A-E-2 |
| U5 | 25A-E-5 |
| U6 | 25A-E-6 |

| ASSEMBLY COILS | PART NUMBER |
| --- | --- |
| Coin Lockout | C-36-5300 |
| Flipper L & R (Bottom Two) | J-25-475/34-4500 |
| Flipper L & R (Top Two) | J-25-600/34-4500 |
| Knocker | N-26-1200 |
| Outhole Kicker (1) | JX-26-1100 |
| Thumper Bumper (3) | J-26-1200 |
| Slingshots (2) | J-27-1700 |
| Drop Target Reset (3) | B-27-2300 |

| MODULES | PART NUMBER |
| --- | --- |
| Lamp Driver | B-431 |
| Display Driver (4) | A-645 |
| Match/Ball in Play Display | A-434 |
| Solenoid Driver/Voltage Regulator | B-432-FJ |
| MPU (FOR ROMS SEE MISCELLANEOUS ABOVE) | C-602 |
| Rectifier Board | A-430 |
| Sound Module | C-605 |
| PLAYFIELD PARTS | SEE PLAYFIELD DIAGRAM |

Page 17 OTHER PARTS & ASSEMBLIES: 1A-4-BANK DR. TARGET D-580-4B (TARGETS ALONE 13A-20-2); 1B-3-BANK DR. TARGET D-580-3A (TARGETS ALONE 13A-20-2); 2-THUMPER CAP 13A-37; 3-ROLL-OVER BUTTON 4B-275; 4-SPIN. TARGET ASSEM. A-563-13, TARGET & WIRE ONLY 14A-7-12; 5-TARGET ASSEMBLY A-649-BL; 6-FLIPPER & SHAFT ASS'Y. A-449-Y; 7-BALL GUIDE POST 2A-200; 8-INSTRUCTION PLATE 14B-3-3; 9-SHOOTER GAUGE 14A-2-6.

## Complete self-test and bookkeeping table, PDF page 6

| TEST SWITCH PUSH NUMBER | BALL/MATCH DISPLAY | DESCRIPTION |
| --- | --- | --- |
| 1st | [blank] | Burn in test - all outputs tested |
| 2nd | [blank] | Lamp test - all feature lamps on and off |
| 3rd | [blank] | Display test - all digits display 0000000 thru 9999999 then an 8 shifts from left to right |
| 4th | [blank] | Solenoid test - continuous sequence of solenoids pulsed with solenoid driver transistor, "Q" number displayed |
| 5th | Flashing 0 if all switches open | Switch test - switch I.D. No. displays if closed |

| TEST SWITCH PUSH NUMBER | BALL/MATCH DISPLAY | DESCRIPTION | DISPLAYS |
| --- | --- | --- | --- |
| 6th | 01 | 1st Threshold (High Score) | [blank] |
| 7th | 02 | 2nd Threshold (High Score) | [blank] |
| 8th | 03 | 3rd Threshold (High Score) | [blank] |
| 9th | 04 | Current High Game Threshold | [blank] |
| 10th | 05 | Current Credits | 00 to 40 |
| 11th | 06 | Total Plays | 00 to 999999 |
| 12th | 07 | Total Replays | 00 to 999999 |
| 13th | 08 | Total times high score is passed | 00 to 999999 |
| 14th | 09 | Number of coins thru Chute No. 2 | 00 to 999999 |
| 15th | 10 | Number of coins thru Chute No. 1 | 00 to 999999 |
| 16th | 11 | Number of coins thru Chute No. 3 | 00 to 999999 |
| 17th | 12 | Total balls played | 00 to 999999 |
| 18th | 13 | Total Extra Balls Awarded | 00 to 999999 |
| 19th | 14 | Total Playfield Special Awards | 00 to 999999 |
| 20th | 15 | N/U | 00 to 999999 |
| 21st | 16 | Total level 1 passed | 00 to 999999 |
| 22nd | 17 | Total level 2 passed | 00 to 999999 |
| 23rd | 18 | Total level 3 passed | 00 to 999999 |

## Source-linked operation paraphrase

Page 3: solenoid-test display numbers equal SDU transistor numbers; holding both flipper buttons energizes the flippers. Stuck-switch test reports the lowest closed address and excludes flipper buttons. Normal contacts are gold plated; flipper-button and flipper-EOS contacts are exceptions.

Page 4 Figure 1: four player displays, credits and match/ball-in-play displays are in the back-rack glass. MPU, lamp driver, sound board and solenoid driver are in the backbox; knocker is cabinet mounted. It labels S33 MEMORY CLEAR at both the MPU and door, distinct from the door SELF TEST button.

Page 5: one ball enters through the out-hole. Starting resets the targets and feeds the ball from the out-hole to the shooter lane. Bonus is counted at drain; player/ball advances except for an earned immediate extra ball. Tilt loses the ball's bonus and disables flippers/thumpers until the next serve. Slam loses the game through a delay. The text describes slam switches on door, tilt board and playfield, and allows operator additions; this is stronger than assuming a quantity from two cabinet-list entries.

Pages 8-10: bonus starts at zero, advances 1,000 on drops/lit stand-ups and 3,000 on outlanes/runway; maximum is 39,000 times multiplier. Completing a bank while INCREASE X is lit advances multiplier up to 7X. Multiplier through 5X carries between balls; the selected 6X/7X threshold resets it to 3X. Each drop spots a loop light. Bank completion transfers its ADVANCE LOOP VALUE to LIGHTS EXTRA BALL; when repeated with one target remaining, the last target can collect the lit bonus plus 1,000. Top roll-over scores 10 or 1,000 per lit loop lamp; all ten loop lamps and all three banks enable double loop. Spinner scores 200 plus 200 per lit value up to 1,000. Thumpers score 1,000 on three-ball and 100 on five-ball; slingshots 10. Unlit stand-ups score 100, lit ones 1,000 and advance bonus. Runway/outlanes score 5,000 and 3,000 bonus, special when lit; return lanes 500 and extra ball when lit. Operator option tables control award behavior.
