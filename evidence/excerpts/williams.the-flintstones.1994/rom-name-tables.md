# The Flintstones — ROM switch, lamp, coil, flasher and G.I. name tables

Decoded by `tools/flintstones_rom_name_tables.py` from the user-authorized local ROM archive; no ROM bytes are
reproduced. Each table in the 512 KiB game ROM is a count byte and a `0x02` entry-width byte followed by that many
big-endian pointers into the same 16 KiB bank (seen by the CPU at `0x4000-0x7fff`), each addressing a NUL-terminated
string. The first pointer is a sentinel (`INVALID SW. NUMBER`, `INVALID FL. SW. NUM.` or `NULL`) and is not
listed. Offsets are file offsets of the first pointer after the sentinel. The ROM holds each table once per
language and more than one English copy; a copy is English when its anchor entries match, every English copy
must decode identically, and the offset of each copy is listed. Text is shown exactly as stored, in code spans so
that the ROM's `<` and `>` letter markers are not read as markup.

| Driver | ROM archive SHA-256 | Game ROM member | Member SHA-256 | Tables identical to fs_lx5 |
| --- | --- | --- | --- | --- |
| fs_lx5 | `a041f2d31ea60013339b7edd806396256cc15eb2b03af21492fe9408273320ff` | flin_lx5.rom | `7b01e6913878a9e657915ad6bc008b13ede80847afa0589946ce304f7f28b58e` | reference |
| fs_lx4 | `0705f7d647ec97ed173731c26f0b1bcd10e2e84a07d6fb709e165045c02a5e67` | flin_lx4.rom | `ff70ebea544b004135bb06cdfee7f817fa55329cf4045e02d1628bb44db4b877` | all six |
| fs_lx2 | `a31cf41b3bd110fee0ac99cdf9c863dfecacc3563e97179e80a134735aaefbb9` | flin_lx2.rom | `14cf4b6e806481a1f978106c21a11c269ea9f56ca1b6ff0943d9a0376a4bb4cd` | all six |
| fs_sp2 | `2208a79d060c18337be742f894e379a4551f4328d364e3cd048d109077e7c040` | flin_lx5.rom | `7b01e6913878a9e657915ad6bc008b13ede80847afa0589946ce304f7f28b58e` | all six |

English copies in the reference set:

| Table | Copies (first entry offset) | Entries |
| --- | --- | ---: |
| Switch table | 0x44cef, 0x6dd1b, 0x6e4db | 72 |
| Fliptronic switch table | 0x45030, 0x6e0c7 | 8 |
| Coil table | 0x44a8a, 0x6da8c, 0x6e477 | 19 |
| Flasher table | 0x44bae, 0x6dbb0, 0x6e4a2 | 11 |
| G.I. table | 0x44c49, 0x6dc75, 0x6e4bd | 6 |
| Lamp table | 0x450b3, 0x6e160, 0x6e5ce | 64 |

## Switch table (D1-D8, then matrix switches 11-88 in column order)

| Switch | ROM text |
| --- | --- |
| D1 | `LEFT COIN SLOT` |
| D2 | `CENTER COIN SLOT` |
| D3 | `RIGHT COIN SLOT` |
| D4 | `4TH COIN OPTION` |
| D5 | `ESCAPE` |
| D6 | `DOWN` |
| D7 | `UP` |
| D8 | `ENTER` |
| 11 | `LAUNCH BALL` |
| 12 | `TICKET OPTO.` |
| 13 | `START BUTTON` |
| 14 | `PLUMB BOB TILT` |
| 15 | `RT. SHOOTER LANE` |
| 16 | `LFT. BOWLING TGT.` |
| 17 | `CNT. BOWLING TGT.` |
| 18 | `RGT. BOWLING TGT.` |
| 21 | `SLAM TILT` |
| 22 | `COIN DOOR CLOSED` |
| 23 | `BUY IN` |
| 24 | `ALWAYS CLOSED` |
| 25 | `MACHINE EXIT` |
| 26 | `UP. LFT. HALF TGT.` |
| 27 | `LEFT LANE EXIT` |
| 28 | `LFT. LOOP ENTER` |
| 31 | `TROUGH JAM` |
| 32 | `TROUGH 1` |
| 33 | `TROUGH 2` |
| 34 | `TROUGH 3` |
| 35 | `TROUGH 4` |
| 36 | `TOP POPPER` |
| 37 | `RGHT. RMP. ENTER` |
| 38 | `LFT. RMP. ENTER` |
| 41 | `BED<R>OCK` |
| 42 | `BEDR<O>CK` |
| 43 | `BEDRO<C>K` |
| 44 | `BEDROC<K>` |
| 45 | `BE<D>ROCK` |
| 46 | `B<E>DROCK` |
| 47 | `<B>EDROCK` |
| 48 | `CENTER LANE EXIT` |
| 51 | `LFT. RGHT. TGT. 3` |
| 52 | `LFT. RGHT. TGT. 2` |
| 53 | `LFT. RGHT. TGT. 1` |
| 54 | `LEFT HALF TGT.` |
| 55 | `RIGHT HALF TGT.` |
| 56 | `DICTABIRD TARGET` |
| 57 | `NOT USED` |
| 58 | `NOT USED` |
| 61 | `LEFT SLING` |
| 62 | `RIGHT SLING` |
| 63 | `LEFT BUMPER` |
| 64 | `RIGHT BUMPER` |
| 65 | `BOTM. BUMPER` |
| 66 | `<D>IG` |
| 67 | `D<I>G` |
| 68 | `DI<G>` |
| 71 | `LEFT OUTLANE` |
| 72 | `LFT. RET. LANE` |
| 73 | `RGT. RET. LANE` |
| 74 | `RIGHT OUTLANE` |
| 75 | `RIGHT LANE EXIT` |
| 76 | `MACHINE ENTER` |
| 77 | `RIGHT RAMP EXIT` |
| 78 | `LEFT RAMP EXIT` |
| 81 | `NOT USED` |
| 82 | `NOT USED` |
| 83 | `NOT USED` |
| 84 | `NOT USED` |
| 85 | `NOT USED` |
| 86 | `NOT USED` |
| 87 | `NOT USED` |
| 88 | `NOT USED` |

## Fliptronic switch table (F1-F8)

| Switch | ROM text |
| --- | --- |
| F1 | `R. FLIPPER E.O.S.` |
| F2 | `R. FLIPPER BUTTON` |
| F3 | `L. FLIPPER E.O.S.` |
| F4 | `L. FLIPPER BUTTON` |
| F5 | `U.R. FLIPPER E.O.S.` |
| F6 | `U.R. FLIPPER BUT.` |
| F7 | (empty string) |
| F8 | (empty string) |

## Coil table (ROM coil-test order; entry numbers are table positions, not addresses)

| Entry | ROM text |
| --- | --- |
| 1 | `TROUGH` |
| 2 | `RIGHT SHOOTER` |
| 3 | `TOP DIVERT. POST` |
| 4 | `TOP POPPER` |
| 5 | `3 BANK RESET` |
| 6 | `4 BANK RESET` |
| 7 | `KNOCKER` |
| 8 | `BACKPANEL DIVRTR` |
| 9 | `RIGHT SLING` |
| 10 | `LEFT SLING` |
| 11 | `TOP LEFT JET` |
| 12 | `BOTTOM JET` |
| 13 | `TOP RIGHT JET` |
| 14 | `DICTABIRD` |
| 15 | `L. RMP. DIVERTER` |
| 16 | `R. RMP. DIVERTER` |
| 17 | `MACHINE MOTOR` |
| 18 | `R. UP/DWN GATE` |
| 19 | `L. UP/DWN GATE` |

## Flasher table (ROM flasher-test order; entry numbers are table positions, not addresses)

| Entry | ROM text |
| --- | --- |
| 1 | `LFT. RAMP FLS.` |
| 2 | `RGHT. RAMP FLS.` |
| 3 | `BOTTOM ARCH FLS.` |
| 4 | `BTM. 3 BNK. FLS.` |
| 5 | `TOP POPPER FLS.` |
| 6 | `"BOWLORAMA"` |
| 7 | `MACHINE FLS.` |
| 8 | `"DIG MILLIONS"` |
| 9 | `FLINT IN BACKBOX` |
| 10 | `STONE IN BACKBOX` |
| 11 | `"FREDS CHOICE"` |

## G.I. table (ROM test order)

| Entry | ROM text |
| --- | --- |
| 1 | `ILLUM. STRING 1` |
| 2 | `ILLUM. STRING 2` |
| 3 | `ILLUM. STRING 3` |
| 4 | `ILLUM. STRING 4` |
| 5 | `ILLUM. STRING 5` |
| 6 | `ALL ILLUMINATION` |

## Lamp table (lamps 11-88 in column order)

| Lamp | ROM text |
| --- | --- |
| 11 | `<D>IG` |
| 12 | `D<I>G` |
| 13 | `DI<G>` |
| 14 | `"MYSTERY MODE"` |
| 15 | `"FREDS CHOICE"` |
| 16 | `"EAT AT JOES"` |
| 17 | `"WATERBUFFALOS"` |
| 18 | `"DINO FRENZY"` |
| 21 | `LEFT "/" TGT.` |
| 22 | `CNTR. "X" TGT.` |
| 23 | `RIGHT "/" TGT.` |
| 24 | `EXTRA BALL` |
| 25 | `CENTER SEARCH` |
| 26 | `CNTR. DRIVE THRU` |
| 27 | `"SUPER JACKPOT"` |
| 28 | `START 2X` |
| 31 | `<C>ONCRETE` |
| 32 | `C<O>NCRETE` |
| 33 | `CO<N>CRETE` |
| 34 | `CON<C>RETE` |
| 35 | `CONC<R>ETE` |
| 36 | `CONCR<E>TE` |
| 37 | `CONCRE<T>E` |
| 38 | `CONCRET<E>` |
| 41 | `"DRAIN SAVE"` |
| 42 | `<B>EDROCK` |
| 43 | `B<E>DROCK` |
| 44 | `BE<D>ROCK` |
| 45 | `BED<R>OCK` |
| 46 | `BEDR<O>CK` |
| 47 | `BEDRO<C>K` |
| 48 | `BEDROC<K>` |
| 51 | `LEFT BOWLING` |
| 52 | `BOTM. TGTS. 3` |
| 53 | `LEFT FRENZY` |
| 54 | `LEFT DINO` |
| 55 | `LEFT RAMP "3"` |
| 56 | `LEFT RAMP "2"` |
| 57 | `LEFT RAMP "1"` |
| 58 | `START MACHINE` |
| 61 | `START JOB` |
| 62 | `"HELP"` |
| 63 | `BOTM. TGTS. 2` |
| 64 | `BOTM. TGTS. 1` |
| 65 | `"JACKPOT"` |
| 66 | `"ROCK AGAIN"` |
| 67 | `LEFT "X"` |
| 68 | `RIGHT "X"` |
| 71 | `RIGHT DINO` |
| 72 | `"MACHINE TIME"` |
| 73 | `RIGHT RAMP "2"` |
| 74 | `RIGHT RAMP "3"` |
| 75 | `RIGHT RAMP "1"` |
| 76 | `RIGHT BOWLING` |
| 77 | `RIGHT FRENZY` |
| 78 | `RIGHT SEARCH` |
| 81 | `UP. LFT. FRENZY` |
| 82 | `UP. LFT. DINO` |
| 83 | `"BRONTO CRANE"` |
| 84 | `LEFT SEARCH` |
| 85 | `JOB CHANGE` |
| 86 | `START MULTIBALL` |
| 87 | `BUY IN` |
| 88 | `START BUTTON` |

The coil, flasher and G.I. tables carry no solenoid or string numbers, so they do not by themselves pair an entry
with a public address; the definition records how each pairing was settled.
