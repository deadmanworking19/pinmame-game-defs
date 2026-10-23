# Bram Stoker's Dracula — Fliptronic II Flipper Circuits

Transcribed from `Dracula_Bram_Stoker_OPS.pdf`, PDF page 130, printed page 3-18,
"Fliptronic II Flipper Circuits", read from the committed crop `fliptronic-flipper-circuits.webp`
(the page's native 150 dpi scan). The page draws two schematics side by side, each boxed as
"Fliptronic II Board" on the left of a dashed line with "Playfield" on the right. It is the
generic Fliptronic II drawing: it draws upper-flipper coils this machine does not fit, and it
prints no solenoid numbers.

## Left Flipper Circuit

- `J901` pins 1, 2, 3, 5 feed bridge rectifier `BR1`; filter capacitor `C2`.
- Fuse `F903` to `J907` pins 6 and 7 (joined), `Gray-Yellow`, to the **Lower Left Flipper** coil.
- Fuse `F901` to `J907` pins 1 and 2 (joined), `Gray-Yellow`, to the **Upper Left Flipper** coil.

| J902 pin | Wire | Printed | Coil drawn on that line |
| --- | --- | --- | --- |
| 9 | Blue-Gray | Power | Lower Left Flipper |
| 7 | Orange-Blue | Holding | Lower Left Flipper |
| 3 | Black-Blue | Power | Upper Left Flipper |
| 1 | Orange-Gray | Holding | Upper Left Flipper |

End-of-stroke switches on `J906`: pin 3 `Black-Blue` to the Lower Left End-of-Stroke Switch,
pin 5 `Black-Gray` to the Upper Left End-of-Stroke Switch, each returning on `Orange` to pin 6,
which is drawn to ground.

## Right Flipper Circuit

- `J901` pins 1, 2, 3, 5 feed bridge rectifier `BR1`; filter capacitor `C2`.
- Fuse `F904` to `J907` pins 8 and 9 (joined), `Blue-Yellow`, to the **Lower Right Flipper** coil.
- Fuse `F902` to `J907` pins 4 and 5 (joined), `Blue-Yellow`, to the **Upper Right Flipper** coil.

| J902 pin | Wire | Printed | Coil drawn on that line |
| --- | --- | --- | --- |
| 13 | Blue-Violet | Power | Lower Right Flipper |
| 11 | Orange-Green | Holding | Lower Right Flipper |
| 6 | Black-Yellow | Power | Upper Right Flipper |
| 4 | Orange-Violet | Holding | Upper Right Flipper |

End-of-stroke switches on `J906`: pin 1 `Black-Green` to the Lower Right End-of-Stroke Switch,
pin 4 `Black-Violet` to the Upper Right End-of-Stroke Switch, each returning on `Orange` to pin
6, which is drawn to ground.

Each coil is drawn as a power winding and a holding winding with two diodes.

## Facts established from this page

- **Per-winding drive pins of the lower flippers.** The 3-8 Solenoid/Flasher Table prints one
  merged drive cell per lower flipper (`J902-7,9` and `J902-11,13`) with separate power and hold
  wire colours. This page splits them by those colours: lower left power `J902-9` Blue-Gray, hold
  `J902-7` Orange-Blue; lower right power `J902-13` Blue-Violet, hold `J902-11` Orange-Green.
- **Upper-flipper pins by side.** `J902-3`/`J902-1` (Black-Blue/Orange-Gray) drive the
  upper-left position and `J902-6`/`J902-4` (Black-Yellow/Orange-Violet) the upper-right one,
  with `J907-1,2` (Gray-Yellow) and `J907-4,5` (Blue-Yellow) as their supplies. This agrees with
  the side labels the 3-8 table prints on those pins. The page names no solenoid number, so it
  does not say which public address drives which side; see
  `conflict.upper-flipper-circuit-side-naming`.
- All of `J901`, `J902`, `J906` and `J907` are drawn on the Fliptronic II board, not the power
  driver board.
