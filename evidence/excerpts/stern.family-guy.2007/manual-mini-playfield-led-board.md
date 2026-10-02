# Stern Family Guy (2007) — mini-playfield LED board 520-5264-00 (schematic reading)

Status: **a curator's reading of two factory schematic pages, joined to PinMAME's board model; not independently reviewed.** This file is an assertion, not a literal transcription: the net tracing in the second table is the curator's.

## Source and transcription envelope

| Field | Value |
| --- | --- |
| Source | *Family Guy Pinball Service Game Manual*, Stern Pinball, Inc., January 2008, v12.0+ |
| PDF SHA-256 | `2bbcfa34ad70ab90c0fadabaf825850cecae58c8028af9aaabf8be1ad01979cd` |
| Locator | PDF page **166** (printed Section 5, Chapter 4, Page 142, "Mini-Playfield Lamp PCB (520-5264-00) Schematic") and PDF page **167** (printed Page 143, "Mini-Playfield Lamp PCB (511-5046-00) Component Layout & Parts"); cabling PDF page **169** (printed Page 145) |
| PinMAME source | `src/wpc/sam.c`, the `SAM_GAME_FG` block "Board 520-5264-00: Family Guy & Shrek mini playfield LEDs" (pinned revision `8371478a7640f1896dcdf565aed340dc5df989ba`) |
| Method | 300 dpi renders of PDF page 166 cropped around each resistor group; nets followed by eye from each LED anode line to its resistor and from the resistor's bus line to the 74AC574 pin. |

## What the printed pages say

Schematic (PDF page 166): connector J1 (12-way, key at 8/9) with inputs "[1] B7 Data [2] B6 Data [3] B5 Data [4] B4 Data [5] B3 Data [6] B2 Data [7] B1 Data [8] B0 Data [9] Key No Connection [10] Clock [11] +5V [12] Ground" and the wire-colour table "1 ORG-GRY, 2 ORG-VIO, 3 ORG-BLU, 4 ORG-GRN, 5 ORG-YEL, 6 ORG-BLK, 7 ORG-RED, 8 ORG-BRN, 9 Key N/C, 10 ORG-WHT, 11 RED, 12 BLACK". Four 74AC574D octal latches IC1–IC4 are clocked together by J1-10, so a byte written to IC1 moves to IC2, then IC3, then IC4 on later clocks; IC1–IC3 outputs drive LEDs through current-limiting resistors; IC4's outputs go to the ULN2003AD driver IC5 and to transistors T1/T2, which together switch the two LED column buses (their exact roles were not traced). Three LED groups (anodes on shared resistor lines, cathodes on one of two column buses):

- Group 1 — resistors R2, R4, R5, R6, R1 (62 Ω), fed from IC1 outputs.
- Group 2 — resistors R10, R11, R12, R13 (3.3 Ω), fed from IC2 outputs.
- Group 3 — resistors R17, R18, R19, R20 (62 Ω), fed from IC3 outputs.

Component layout (PDF page 167): letters printed beside each LED place the names on the mini-playfield as the words **BRIAN** (B LED5, R LED6, I LED7, A LED8 along one diagonal, N LED24 at its end), **CHRIS** (C LED44, H LED45, R LED46, I LED47, S LED48), **LOIS** (L LED29, O LED30, I LED31, S LED32), **MEG** (M LED23, E LED22, G LED21, read left to right) and **PETER** (P LED39, E LED16, T LED15, E LED14, R LED13, read left to right). Parts list: amber Omron LA E65B (LED5–8, 24, 44–48), white Omron LW 67C (LED13–16, 39), yellow Omron LY E65B (LED21–23, 29–32).

The cathode buses read from the schematic: the cathodes of LED21–24 (G E M N), LED13–16 (R E T E) and LED5–8 (B R I A) join one bus (**column A**); the cathodes of LED44–48 (C H R I S), LED39 (P) and LED29–32 (L O I S) join the other (**column B**).

## Net tracing: resistor, latch bit and PinMAME lamp address

PinMAME (`sam.c`, SAM_GAME_FG block) shifts four bytes through `latch[0..3]` on each ASTB strobe, takes the column select from `latch[3] & 3` (IC4), and publishes `latch[2] & 0x0F` (IC3) at lamp base 80 (column A) and 104 (column B), `latch[1] & 0x0F` (IC2) at base 88 / 112, and `latch[0] & 0x1F` (IC1) at base 96 / 120. A published output index `base + bit` is public lamp number `base + bit + 1`. Bit *k* of a latch is the IC's output *k*+1 (1Q = bit 0). The "bus line to IC pin" column below is the resistor's bus line followed to the next latch's D input, which is the same net as this latch's Q output.

| LED | Letter / name | Resistor | Bus line → IC input | Latch bit | Column | Public lamp |
| --- | --- | --- | --- | ---: | --- | ---: |
| LED24 | N of BRIAN | R1 (62 Ω) | pin 2 (1D of IC2) | 0 | A | 97 |
| LED23 | M of MEG | R6 | pin 3 (2D) | 1 | A | 98 |
| LED22 | E of MEG | R5 | pin 4 (3D) | 2 | A | 99 |
| LED21 | G of MEG | R4 | pin 5 (4D) | 3 | A | 100 |
| LED48 | S of CHRIS | R1 | pin 2 (1D) | 0 | B | 121 |
| LED47 | I of CHRIS | R6 | pin 3 (2D) | 1 | B | 122 |
| LED46 | R of CHRIS | R5 | pin 4 (3D) | 2 | B | 123 |
| LED45 | H of CHRIS | R4 | pin 5 (4D) | 3 | B | 124 |
| LED44 | C of CHRIS | R2 | pin 6 (5D) | 4 | B | 125 |
| LED16 | E (first) of PETER | R13 (3.3 Ω) | 1Q of IC2 (pin 19) | 0 | A | 89 |
| LED15 | T of PETER | R12 | 2Q (pin 18) | 1 | A | 90 |
| LED14 | E (second) of PETER | R11 | 3Q (pin 17) | 2 | A | 91 |
| LED13 | R of PETER | R10 | 4Q (pin 16) | 3 | A | 92 |
| LED39 | P of PETER | R12 | 2Q (pin 18) | 1 | B | 114 |
| LED8 | A of BRIAN | R20 (62 Ω) | 1Q of IC3 (pin 19) | 0 | A | 81 |
| LED7 | I of BRIAN | R19 | 2Q (pin 18) | 1 | A | 82 |
| LED6 | R of BRIAN | R18 | 3Q (pin 17) | 2 | A | 83 |
| LED5 | B of BRIAN | R17 | 4Q (pin 16) | 3 | A | 84 |
| LED32 | S of LOIS | R20 | 1Q (pin 19) | 0 | B | 105 |
| LED31 | I of LOIS | R19 | 2Q (pin 18) | 1 | B | 106 |
| LED30 | O of LOIS | R18 | 3Q (pin 17) | 2 | B | 107 |
| LED29 | L of LOIS | R17 | 4Q (pin 16) | 3 | B | 108 |

Twenty-two LEDs, twenty-two addresses. Checks the reading satisfies: (a) the set of addresses is exactly the set the ROM drove in every retained harness run of `fg_1200ag` (81–84, 89–92, 97–100, 105–108, 114, 121–125); (b) the only column-B group-2 LED is P on R12, and the only lamp driven in 113–116 is 114 (bit 1); (c) group 1 has five loads on column B (bits 0–4) but only four on column A, and 101 (column A bit 4) is never driven while 121–125 all are; (d) the group sizes (5, 4, 4 bits) equal the PinMAME masks 0x1F, 0x0F, 0x0F for IC1, IC2, IC3. The pairing of BRIAN's letters to column A and LOIS's to column B (the two groups of equal size) rests on the cathode-bus tracing alone.

## PinMAME's lamp typing

PinMAME types lamp outputs 81–128 (`CORE_MODOUT_LAMP0 + 80` onward) as LED outputs with 8 ms pulses over a 16 ms period (`core_set_pwm_output_led_vfd(CORE_MODOUT_LAMP0 + 80, 3 * 2 * 8, 0, 16.f / 8.f)`), i.e. six groups of eight, of which the 22 addresses above are the populated ones.
