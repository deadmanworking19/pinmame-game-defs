# Space Station — ROM and Jumper Table and Solenoid Table (PDF page 2, no printed folio)

Source: `Williams_1987_Space_Station_Operations_Manual_and_Test_Procedures.pdf` (86 pages, SHA-256
`71e3212599e733ed432cdc533190ead6a925ff7a5d62862d7c09897566aaddbc`), PDF page 2. The page prints no
folio; it carries the "SPACE STATION ROM and Jumper Table" above the "SPACE STATION Solenoid Table".
Read from the page's embedded 150 dpi scan, rendered at 300 dpi and cropped in strips; the scan has no
text layer and the Windows OCR pass was used only to find pages. Every row and every column is
transcribed. Superscript note markers are written `^n`.

## SPACE STATION ROM and Jumper Table

| Game | System 11B CPU Rev. | P/N - U15 Game µP | P/N - U27 G. ROM 1 | P/N - U26 G. ROM 2 | P/N - U21 S. ROM 1 | P/N - U22 S. ROM 2 | P/N - U24 Sound µP | Jumpers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BIG GUNS | - | 5400-09150-00 | A-5343-557-2 | A-5343-557-1 | A-5343-557-4 | A-5343-557-3 | 5400-09150-00 | W1, 2, 4, 5, 7, 8, 11, 14, 16, 17, and 19 |
| SPACE STATION | - | (arrow down) | A-5343-552-2 | A-5343-552-1 | A-5343-552-4 | A-5343-552-3 | (arrow down) | W1, 2, 4, 5, 7, 8, 11, 14, 16, 17, and 19 |

Part numbers printed on two lines (`A-5343-` / `557-2`) are joined. The U15 and U24 cells of the SPACE
STATION row print a downward arrow under the BIG GUNS part number instead of repeating it.

## SPACE STATION Solenoid Table

Column headers as printed: `Sol. No.` | `Function` | `Solenoid Type` | `Wire Color` with superscript `1`
| `Connections` spanning `CPU Bd.` and `Playfield/ Cabinet` | `Driver Trans.` | `Solenoid Part Number /
Flashlamp Type` with the small line `b - Backbox    p - Playfield` under that heading.

In rows 01A to 08C the two wire colours of an A/C pair are printed between a pair of braces, the CPU Bd.
cell prints the A row's pin on the first line and the C row's bracketed wire colour on the second, and the
Playfield/Cabinet cell prints `8P3-n (to J1-m on` on the A row and `Aux Pwr Drvr Bd)` on the C row. Each
printed line is kept as its own row; the braces are noted here and not repeated.

| Sol. No. | Function | Solenoid Type | Wire Color | CPU Bd. | Playfield/Cabinet | Driver Trans. | Solenoid Part Number / Flashlamp Type |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01A^3 | Outhole Kicker | Switched | Vio-Brn | 1P11-1 | 8P3-1 (to J1-9 on | Q33 | AE-23-800 |
| 01C^3 | Relaunch + "ON" Flashers | Switched | Blk-Brn | (Gry-Brn) | Aux Pwr Drvr Bd) | Q33 | #89 flashlamps 2b,2p |
| 02A^3 | Ball Shooter Lane Feeder | Switched | Vio-Red | 1P11-3 | 8P3-2 (to J1-7 on | Q25 | AE-23-800 |
| 02C^3 | Left Side + "SP" Flashers | Switched | Blk-Red | (Gry-Red) | Aux Pwr Drvr Bd) | Q25 | #89 flashlamps 2b,2p |
| 03A^3 | Left Ball Popper | Switched | Vio-Orn | 1P11-4 | 8P3-3 (to J1-6 on | Q32 | AE-24-900 |
| 03C^3 | Right Side + "AC" Flashers | Switched | Blk-Orn | (Gry-Orn) | Aux Pwr Drvr Bd) | Q32 | #89 flashlamps 2b,2p |
| 04A^3 | Right Ball Popper | Switched | Vio- Yel | 1P11-5 | 8P3-4 (to J1-5 on | Q24 | AE-23-800 |
| 04C^3 | Top (upr p/f) + "ES" Flashers | Switched | Blk-Yel | (Gry-Yel) | Aux Pwr Drvr Bd) | Q24 | #89 flashlamps 2b,2p |
| 05A^3 | Not Used | Switched | Vio-Grn | 1P11-6 | 8P3-5 (to J1-4 on | Q31 | (blank) |
| 05C^3 | P'fld Top Panel + "TA" Flashers | Switched | Blk-Grn | (Gry-Grn) | Aux Pwr Drvr Bd) | Q31 | #89 flashlamps 2b,2p |
| 06A^3 | 3-bank Drop Target | Switched | Vio-Blu | 1P11-7 | 8P3-6 (to J1-3 on | Q23 | AE-26-1200 |
| 06C^3 | Flame + "TI" Flashers | Switched | Blk-Blu | (Gry-Blu) | Aux Pwr Drvr Bd) | Q23 | #89 flashlamps 4b |
| 07A^3 | Knocker (or Ticket Dispenser) | Switched | Vio-Blk | 1P11-8 | 8P3-7 (to J1-2 on | Q30 | AE-26-1200 |
| 07C^3 | Station Flasher | Switched | Blk-Vio | (Gry-Vio) | Aux Pwr Drvr Bd) | Q30 | #89 flashlamps 2b |
| 08A^3 | R Sngl Drop Target - Raise | Switched | Vio-Gry | 1P11-9 | 8P3-8 (to J1-1 on | Q22 | AE-23-800 |
| 08C^3 | Left Dock Kickbig | Switched | Blk-Gry | (Gry-Blk) | Aux Pwr Drvr Bd) | Q22 | AE-23-800 |
| 09 | General Illum Relay (Playfield) | Controlled | Brn-Blk | 1P12-1 | 8P3-9 | Q17 | 5580-09555-01^4 |
| 10 | General Illum Relay (Green) | Controlled | Brn-Red | 1P12-2 | 8P3-10 | Q9 | 5580-09555-01^4 |
| 11 | General Illum Relay (Insert Bd) | Controlled | Brn-Orn | 1P12-4 | 6P3-5 | Q16 | 5580-09555-01^4 |
| 12 | A/C Select Relay | Controlled | Brn-Yel | 1P12-5 | 8P3-12 | Q8 | 5580-09555-01^5 |
| 13 | Left Re-Entry Kickback (drain) | Controlled | Brn-Grn | 1P12-6 | 8P3-13 | Q15 | AE-24-900 |
| 14 | Not Used | Controlled | Brn-Blu | 1P12-7 | 8P3-14 | Q7 | (blank) |
| 15 | P'fld Top Panel Flashers (3) | Controlled | Brn-Vio | 1P12-8 | 8P3-15 | Q14 | #1251 flashlamps 3b ^6 |
| 16 | Space Station Motor/Relay | Controlled | Brn-Gry | 1P12-9 | 8P3-16 | Q6 | 14-7941-2/5580-12145-01 |
| 17 | Right Dock Kickback | Special #1 | Blu-Brn | 1P19-7 | 8P3-17 | Q75 | AE-23-800 |
| 18 | Lower Left Kicker ("sling") | Special #2 | Blu-Red | 1P19-4 | 8P3-18 | Q71 | AE-26-1200 |
| 19 | Rt Jet Bumper | Special #3 | Blu-Orn | 1P19-3 | 8P3-19 | Q73 | AE-23-800 |
| 20 | Lower Right Kicker ("sling") | Special #4 | Blu-Yel | 1P19-6 | 8P3-20 | Q69 | AE-26-1200 |
| 21 | Left Jet Bumper | Special #5 | Blu-Grn | 1P19-8 | 8P3-21 | Q77 | AE-23-800 |
| 22 | Lower Jet Bumper | Special #6 | Blu-Blk | 1P19-9 | 8P3-22 | Q79 | AE-23-800 |
| - | Right Flipper | - | Orn-Vio [Blu-Vio] | 1P19-1 | 7P1-15 [7P1-16,8P3-34]^2 | - | FL11630-50VDC |
| - | Left Flipper | - | Orn-Gry [Blu-Gry] | 1P19-2 | 7P1-18 [7P1-19,8P3-32]^2 | - | FL11630-50VDC |

Notes printed under the table, verbatim:

> Notes: 1. Wire colors, except flipper Orn-Vio and Orn-Gry, are ground connections (to coil terminal
> with unbanded end of diode). Flipper Orn-Vio and Orn-Gry wires connect from CPU Board to flipper
> switch. 2. Flipper connections shown in braces are from flipper switch to flipper coil. 3. "A" circuits
> are pulsed, when Sol. 12 is de-energized; "C" circuits are pulsed, with Sol. 12 energized. Wire colors in
> brackets are those from respective A and C terminals corresponding to the J1-terminal connection listed
> for the Aux Power Driver Bd, which controls the device pulsing by Sol. 12. 4. Relay is mounted on Relay
> Bd, p/n C-11998-1. 5. Relay is mounted on Aux Power Driver Bd, D-11813 in the backbox. 6. Relay is
> mounted on Relay Bd, C-11902-1.

## Comparison with the copy on PDF page 32 (printed "SPACE STATION 28")

PDF page 32 ("TEST/DIAGNOSTIC PROCEDURES (Continued)", "SOLENOID TEST.") prints the same "SPACE STATION
Solenoid Table" under the Solenoid Test text, which reads: "Next, the player 3 display shows a series of
test steps from 01 through 22, while the player 1 and 2 displays show the solenoid/circuit name." Read
row by row from the same kind of crops: every Sol. No., Function, Solenoid Type, Wire Color, CPU Bd.,
Playfield/Cabinet, Driver Trans. and part-number cell, and the six notes, carry the same words and digits
as page 2. Print differences only: on page 32 the Driver Trans. and part-number columns of rows 01C-08A are
set about one text line lower than the left-hand columns, so for example the `Q23  #89 flashlamps 4b` of
06C prints level with the 07A function; read in order they give the same sequence as page 2. The 02A CPU
Bd. cell prints `P11-3` with its leading `1` hidden under the brace. Copies of one table are one source.

Normalization: none beyond joining lines printed one under another with a single space and writing
superscripts as `^n`.

Uncertain cells:
- 06A (page 2): the superscript after `06A` prints as a blotted mark that resembles `8`; every other A/C
  row and the page 32 copy print `3` there, and the table has no note 8. Written `^3`.
- 04A Wire Color prints `Vio- Yel` with a space after the hyphen on both copies; kept as printed.
- 15: the flashlamp cell prints `3b` followed by a superscript `6` at the cell edge.
