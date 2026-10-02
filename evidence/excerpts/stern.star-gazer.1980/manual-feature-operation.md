# Star Gazer — feature operation and scoring

Transcribed from `Stern_1980_Star_Gazer_Manual.pdf`, PDF pages 8, 9 and 10 (printed pages 7, 8 and 9), section "VI. FEATURE OPERATION & SCORING", read from the rendered scans. Switch numbers are the manual's own "Pl. Sw." numbers, which are the PinMAME matrix addresses `1` to `40` (see the switch-identification excerpt). Spelling follows the page, including the printed `Lft.`, `Rt.`, `lite` and `lites`. The PDF has no text layer; every number below was read from the rendered page.

## Printed page 7

**To help explanation**, playfield switches involved "will be called out. See 'Switch Identification' (Pg. 18) for location of playfield switches."

**Bonus score feature.** "Game starts at O. Maximum bonus 48,000".

Bonus advancement:

| Pl. Sw. No. | Location | Advance Bonus |
| --- | --- | --- |
| 10, 11, 17, 18 | Top Lft. Stand-up Targets | Each Target 1,000 |
| 19, 20, 21, 31, 32, 38 | Top Rt. Stand-up Targets | Each Target 1,000 |
| 39, 40 | Lower Right Stand-up Targets | Each Target 1,000 |
| 36 | Right Rollover | Advances 1,000 by Spotting Zodiac Target. (See Note #1) |
| 37 | Left Rollover | Advances 1,000 by Spotting Zodiac Target. (See Note #1) |

"Spotting Zodiac target and bonus advancement can be made by hitting all three targets down on lower two drop banks. (See adjustment on MPU Sw. #29)"

Bonus multiplier:

| Pl. Sw. No. | Location | Advance Multiplier |
| --- | --- | --- |
| 22, 23, 24 | Lower Left Bank Drop Targets | Will Advance When All Three Targets Are Hit (to 10x Max.) |
| 28, 29, 30 | Right Bank Drop Targets | Will Advance When All Three Targets Are Hit (to 10x Max.) |

**Bonus collected.** "Outhole Switch - #33. When the ball enters the 'Outhole', the 'Bonus Score' (times the multiplier) is collected. The 'Bonus' and the 'Bonus Multiplier' are retained from ball to ball."

**Special.** "'Special' can be awarded by means of rt. three drop target bank or two outlanes"

| Pl. Sw. No. | Location | Award |
| --- | --- | --- |
| 28, 29, 30 | Right Three Drop Targets | To receive "Special" award all 12 Zodiac targets must be hit 2, 3, or 4x's (See Special Adjustments) |
| 34, 35 | 2 Outlanes | To receive "Special" award all 12 Zodiac targets must be hit 2, 3, or 4x's (See Special Adjustments) |

**Special alternation.**

1. "Three 'Special' positions alternate" — MPU SW. #23 ON
2. "Target bank 'Special' position stays on, outlanes alternate" — MPU SW. #23 OFF

## Printed page 8

**Special adjustment.** "Determines when 'Special' can be awarded for completing Zodiac ring."

| | MPU SW. 22 | MPU SW. 24 |
| --- | --- | --- |
| 2nd time | OFF | OFF |
| 2nd time | ON | OFF |
| 3rd time | OFF | ON |
| 4th time | ON | ON |

**Award** (what the Special gives):

| | MPU SW. 31 | MPU SW. 32 |
| --- | --- | --- |
| No award | OFF | OFF |
| Extra Ball | OFF | ON |
| 100,000 points | ON | OFF |
| Replay | ON | ON |

**Replay, high score.** "1) Replay" — MPU SW. #6 ON.

**Extra ball.** "Extra ball can be awarded by means of the center target in the lower left bank drop targets only (pl. Sw. 23)". Extra ball collected: Pl. Sw. No. 23, Lower Left Bank Drop Targets, Award (Lites Extra Ball): "When All 12 Zodiac Targets Have Been Lit".

Extra ball adjustments:

| | | |
| --- | --- | --- |
| 1) High SCORE | EXTRA BALL | MPU SW. #6 OFF |
| 2) SPECIAL AWARD | EXTRA BALL | MPU SW. #31 OFF SW. 32 ON |
| 3) EXTRA BALL, LITE LIMIT | Lite Alternates / Lite Stays On | MPU SW. #17 OFF / MPU SW. #17 ON |
| 4) EXTRA BALL LITE CONTROL | No Extra Ball | MPU SW. #30 OFF |

**Left spinner (Pl. Sw. #4).** "Scores 200 each spin or 2,000 when lit. (See Note #1)". **Right spinner (Pl. Sw. #5).** "Scores 200 each spin or 2,000 when lit. (See Note #1)". **Center spinner (Pl. Sw. #9).** "Scores 200 or lit value (See Left Upper Bank)".

**Left upper bank (Pl. Sw. No. 25, 26, 27).** "Each drop target scores 1,000. Hitting one target stops flashing lite determining value of points awarded and value of Center Spinner, hitting all three targets awards points."

## Printed page 9

**Flashing value lite speed.** "Control flashing lite speed as Zodiac targets are hit." Flashing lite speed: fast — MPU SWITCH #55 OFF; slow — MPU SWITCH #55 ON. The page prints `#55` in the switch column; the option-switch assignment chart on PDF page 11 and the prose on PDF page 13 give the flashing-lite-speed switch as 5, so `#55` is read as a misprint of 5 (there is no switch 55).

**NOTE 1.** "Alternates SPOT ZODIAC TARGET and LITE RIGHT/LEFT SPINNER lites at bottom of playfield".

| feature | printed text |
| --- | --- |
| Thumper bumper (Pl. Sw. No. #12, 13, 14) | "Scores 1,000 points" |
| Sling shots (Pl. Sw. No. #15) | "Scores 10 points." |
| Left rollover (Pl. Sw. No. #37) | "Scores 2,000 points and spots next zodiac target when white lite is lit or lites right spinner multiplier when yellow lite is lit." |
| Right rollover (Pl. Sw. No. #36) | "Scores 2,000 points and spots next zodiac target when white lite is lit or lites left spinner multiplier when yellow lite is lit." |
| Left outlane (Pl. Sw. No. #35) | "Scores 5,000 and awards 'Special' when special lite is lit." |
| Right outlane (Pl. Sw. No. #34) | "Scores 5,000 and awards 'Special' when special lite is lit." |
| Zodiac target value (Pl. Sw. No. #10, 11, 17-21, 31, 32, 38-40) | "Each target scores 1,000 when hit and advances bonus 1,000. Zodiac target value can be increased by hitting all twelve zodiacs targets. Each time all twelve targets have been hit the zodiac target value will increase by 1,000 (to a 4,000 max.)." |
| Right bank drop targets (Pl. Sw. No. 28, 29, 30) | "Each target scores 1,000. All three targets down increase bonus multiplier. All three targets down while red Special lite is lit awards Special." |
| Lower left bank drop targets (Pl. Sw. No. #22, 23, 24) | "Each target scores 1,000. All three targets down increase bonus multiplier. When center target is hit when 'Extra Ball' is on, an Extra Ball is awarded." |

The page's "lower left bank" uses the manual's own switch numbers 22 to 24, which the switch-identification table names bottom, middle and top left drop target, and the drawing groups as bank `1C`; the "left upper bank" is switches 25, 26 and 27, drawn as bank `1B`.
