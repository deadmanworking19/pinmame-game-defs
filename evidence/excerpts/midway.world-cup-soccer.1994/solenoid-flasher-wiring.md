# World Cup Soccer — Solenoid/Flasher Table (wiring) and Flipper Circuits

Transcribed from `World_Cup_Soccer_OPS.pdf`, PDF page 114, printed page 2-48, the
`SOLENOID / FLASHER TABLE` and the `Flipper Circuits` table at the bottom of the same page. Every
row is transcribed, including address 36, the only public solenoid address 1-36 with no table row
at all (re-verified against a 600 dpi crop of rows 1-9: addresses 4 "Lock Release" and 7 "Knocker"
both carry full, populated rows — 7 is simply backbox-mounted, with its Voltage/Drive/Part-Number
entries printed under the Backbox column instead of Playfield). Footnote: `* +12VDC`;
`J1XX = Power Driver Board; J9XX - Fliptronic II Board; 24-6549 = #44 Bulb; 24-8704 = #89 Bulb;
24-8768 = #555 Bulb; 24-8802 = #906 Bulb`.

## Solenoid / Flasher Table

| Sol. No. | Function | Type | Voltage Conn. | Drive Xistor | Drive Conn. | Drive Wire | Part No. (Playfield) | Part No. (Backbox) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Goal Popper | High Power | J107-2 | Q82 | J130-1 | Vio-Brn | AE-23-800 | |
| 02 | TV Popper | High Power | J107-2 | Q80 | J130-2 | Vio-Red | AE-26-1500 | |
| 03 | Kickback | High Power | J107-2 | Q78 | J130-4 | Vio-Org | AE-23-800 | |
| 04 | Lock Release | High Power | J107-2 | Q76 | J130-5 | Vio-Yel | AE-26-1500 | |
| 05 | Upper Eject Hole | High Power | J107-2 | Q64 | J130-6 | Vio-Grn | AE-26-1200 | |
| 06 | Trough | High Power | J107-2 | Q66 | J130-7 | Vio-Blu | AE-26-1500 | |
| 07 | Knocker | High Power | (Backbox) J107-2 | Q68 | (Backbox) J130-8 | Vio-Blk | | AE-23-800 |
| 08 | Ramp Diverter | High Power | J107-2 | Q70 | J130-9 | Vio-Gry | FL-11753-1 | |
| 09 | Left Jet Bumper | Low Power | J107-3 | Q58 | J127-1 | Brn-Blk | AE-26-1200 | |
| 10 | Upper Jet Bumper | Low Power | J107-3 | Q56 | J127-3 | Brn-Red | AE-26-1200 | |
| 11 | Lower Jet Bumper | Low Power | J107-3 | Q54 | J127-4 | Brn-Org | AE-26-1200 | |
| 12 | Left Slingshot | Low Power | J107-3 | Q52 | J127-5 | Brn-Yel | AE-26-1200 | |
| 13 | Right Slingshot | Low Power | J107-3 | Q50 | J127-6 | Brn-Grn | AE-26-1200 | |
| 14 | Right Eject Hole | Low Power | J107-3 | Q48 | J127-7 | Brn-Blu | AE-26-1200 | |
| 15 | Left Eject Hole | Low Power | J107-3 | Q46 | J127-8 | Brn-Vio | AE-26-1200 | |
| 16 | Diverter Hold | Low Power | J107-2 | Q44 | J127-9 | Brn-Gry | FL-11753-1 | |
| 17 | Goal Cage Top | Flasher | J107-6 / J106-5 | Q42 | J126-1 / J125-1 | Blk-Brn | #906 | #906 |
| 18 | Goal | Flasher | J107-6 / J106-5 | Q40 | J126-2 / J125-2 | Blk-Red | #89, #906 | #906 |
| 19 | Skill Shot | Flasher | J107-6 / J106-5 | Q38 | J126-3 / J125-3 | Blk-Org | #906 | #906 |
| 20 | Jet Bumpers | Flasher | J107-6 / J106-5 | Q36 | J126-4 / J125-5 | Blk-Yel | #89 | #906 |
| 21 | Goalie Drive | Flasher | J116-2 | Q28 | J126-5 | Blu-Grn | 14-7997 * | |
| 22 | Spinning Ball | Flasher | J107-6 | Q30 | J126-6 | Blu-Blk | #89 (2) | |
| 23 | Ball Clockwise | Flasher | J116-2 | Q34 | J126-7 | Blu-Vio | 14-7996 * | |
| 24 | Ball Counter-Clockwise | Flasher | J116-2 | Q32 | J126-8 | Blu-Gry | 14-7996 * | |
| 25 | Left Ramp Entrance | Gen. Purpose | J107-6 / J106-5 | Q26 | J122-1 / J124-1 | Blu-Brn | #89 | #906 |
| 26 | Lock Area | Gen. Purpose | J107-6 / J106-5 | Q24 | J122-2 / J124-2 | Blu-Red | #906 | #906 |
| 27 | Flipper Lanes | Gen. Purpose | J107-6 / J106-5 | Q22 | J122-3 / J124-3 | Blu-Org | #89 (2) | #906 |
| 28 | Ramp Rear | Gen. Purpose | J107-6 / J106-5 | Q20 | J122-4 / J124-5 | Blu-Yel | #906 (2) | #906 |
| 33 | Magna Goalie | High Power | J907-6,7 | Q2 | J902-6 | Yel-Vio | 20-9247 | |
| 34 | Loop Gate | Low Power | J907-6,7 | Q7 | J902-4 | Org-Vio | A-14406 | |
| 35 | Lock Magnet | High Power | J907-8,9 | Q1 | J902-3 | Yel-Gry | 20-9247 | |
| 36 | *(no row — no coil printed at all)* | | | | | | | |

## General Illumination (top of the GI block on the same page — see `general-illumination.md` for
the continuation and circuit summary)

| No. | Function | Type | Voltage Conn. (Playfield/Backbox) | Drive Xistor | Drive Conn. (Playfield/Backbox) | Drive Wire | Bulb (Playfield/Backbox) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Playfield Left | G.I. | J121-1 | Q18 | J121-7 | Wht-Brn | #44, #555 |
| 02 | Playfield Right | G.I. | J121-2 | Q10 | J121-8 | Wht-Org | #44, #555 |
| 03 | Insert Background | G.I. | J120-3 (Backbox) | Q14 | J120-9 (Backbox) | Wht-Yel | #555 (Backbox only) |
| 04 | Insert Title | G.I. | J120-5 (Backbox) | Q16 | J120-10 (Backbox) | Wht-Grn | #555 (Backbox only) |
| 05 | Playfield Top | G.I. | J121-6 | Q12 | J121-11 | Wht-Vio | #555 (Playfield only) |

## Flipper Circuits

Each flipper prints two rows, power then hold. The Coil Part Number and Coil Color cells are merged
across each flipper's two rows; they are repeated on both rows below. Each row prints its transistor
in the Power or the Hold column only; the other is blank (`—`).

| Flipper | Winding | Voltage Connections (Playfield) | Drive Transistor (Power) | Drive Transistor (Hold) | Drive Connections (Playfield) | Drive Wire (Power) | Drive Wire (Hold) | Coil Part Number | Coil Color |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Lower Left Flipper | Lwr. Lt. Power | J907-4 (Red-Blu) | Q3 | — | J902-9 | Yel-Blu | — | FL-11629 | BLUE |
| Lower Left Flipper | Lwr. Lt. Hold | J907-4 (Red-Blu) | — | Q9 | J902-7 | — | Org-Blu | FL-11629 | BLUE |
| Lower Right Flipper | Lwr. Rt. Power | J907-1 (Red-Grn) | Q4 | — | J902-13 | Yel-Grn | — | FL-11629 | BLUE |
| Lower Right Flipper | Lwr. Rt. Hold | J907-1 (Red-Grn) | — | Q11 | J902-11 | — | Org-Grn | FL-11629 | BLUE |
| Upper Left Flipper | Up Lt. Power | J907-8 (Red-Gry) | Q1 | — | J902-3 | Yel-Gry | — | Not Used | |
| Upper Left Flipper | Up Lt. Hold | J907-8 (Red-Gry) | — | Q5 | J902-1 | — | Org-Gry | Not Used | |
| Upper Right Flipper | Up Rt. Power | J907-6 (Red-Vio) | Q2 | — | J902-6 | Yel-Vio | — | Not Used | |
| Upper Right Flipper | Up Rt. Hold | J907-6 (Red-Vio) | — | Q7 | J902-4 | — | Org-Vio | Not Used | |

`Not Used` is printed once across the Coil Part Number and Coil Color columns of each upper flipper's
two rows. An earlier transcription collapsed each flipper to one row, left the power windings' drive
connections blank (J902-9, J902-13 and J902-6 here) and gave the Up Lt. Power connection J902-3 as the
Up Lt. Hold one (J902-1 here); this table was re-read from the rendered page.

**Cross-reference (curator note, not part of the transcription):** solenoid 33 "Magna Goalie" shares
driver transistor Q2 and drive connection J902-6/wire Yel-Vio-family with "Up Rt. Power"; solenoid 34
"Loop Gate" shares Q7/J902-4/Org-Vio with "Up Rt. Hold"; solenoid 35 "Lock Magnet" shares Q1/J902-3/
Yel-Gry with "Up Lt. Power". The fourth upper-flipper circuit position, Up Lt. Hold (Q5, J902-1,
Org-Gry), has no solenoid-table row at all (matches solenoid 36 having no printed row). World Cup Soccer has no upper
flippers (`FLIP_SOL(FLIP_L)` only in `wcsGameData`), so these three genuinely-fitted solenoids
(33/34/35) are wired through what the generic Fliptronic template calls the upper-flipper
power/hold driver-transistor positions, and the fourth position (36) is unfitted.
