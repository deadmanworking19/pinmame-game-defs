# Literal transcription — System 9 Playfield-Solenoid & Special-Switch Wiring Diagram

`reviewed: true`; transcribed by the curator from a 300 dpi render and visually checked against it on 2026-10-30
`source: Instruction Manual PDF page 17, printed folio 17`

Retained render: `external:pinmame-manuals/by-machine/williams.space-shuttle.1984/rendered-300/p-17.png`
(pdftoppm 23.05.0 -r 300 -gray).

Literal title: `System 9 Playfield-Solenoid & Special-Switch Wiring Diagram`. The drawing is a wiring diagram, so
the transcription lists every labelled element in drawing order; wire labels are as printed.

## Controlled solenoids (CPU 1J11/1P11 and 1J12/1P12, playfield plug 8P3/8J3, +28V on 8J3-36)

| DRIVE TRANSISTOR | CPU pin | wire label | 8P3 pin | load box |
| --- | --- | --- | --- | --- |
| Q47 | 1J11-1 | GRY-BRN SOL. 1 | 1 | 8L1 OUTHOLE |
| Q48 | 1J11-3 | GRY-RED SOL. 2 | 2 | 8L2 BALL RAMP RELEASE |
| Q49 | 1J11-4 | GRY-ORG SOL. 3 | 3 | 8L3 LEFT EJECT HOLE |
| Q50 | 1J11-5 | GRY-YEL SOL. 4 | 4 | 8L4 RIGHT EJECT HOLE |
| Q39 | 1J11-6 | GRY-GRN SOL. 5 | 5 | 8L5 "T" DROP TARGET |
| Q40 | 1J11-7 | GRY-BLU SOL. 6 | 6 | 8L6 3-BANK DROP TARGET |
| Q41 | 1J11-8 | GRY-VIO SOL. 7 | 7 | 8L7 UP POST |
| Q42 | 1J11-9 | GRY-BLK SOL. 8 | 8 | 8L8 DOWN POST |
| Q54 | 1J12-1 | BRN-BLK SOL. 9 | 9 | 8L9 SPACE FLASH LAMPS |
| Q55 | 1J12-2 | BRN-RED SOL. 10 | 10 | 8L10 SHUTTLE FLASH LAMPS |
| Q56 | 1J12-4 | BRN-ORG SOL. 11 | 11 | 8L11 GENERAL ILLUM. RELAY |
| Q57 | 1J12-5 | BRN-YEL SOL. 12 | 12 | 8L12 NOT USED |
| Q58 | 1J12-6 | BRN-GRN SOL. 13 | 13 | 8L13 GATE |
| Q59 | 1J12-7 | BRN-BLU SOL. 14 | 14 | 8L14 INSERT FLASH LAMPS |
| Q60 | 1J12-8 | BRN-VIO SOL. 15 | 15 | 8L15 BELL |

No 1J11 pin 2 and no 1J12 pin 3 is drawn. 1J12-9 (SOL. 16, coin lockout) is not on this
sheet.

## Special solenoids (CPU 1J19/1P19) and special switches (CPU 1J18/1P18)

| DRIVE TRANSISTOR | CPU pin | wire label | 8P3 pin | load box |
| --- | --- | --- | --- | --- |
| Q75 | 1J19-7 | BLU-BRN SP. SOL. 1 | 17 | 8L17 LEFT KICKER |
| Q77 | 1J19-4 | BLU-RED SP. SOL. 2 | 18 | 8L18 RIGHT KICKER |
| Q79 | 1J19-3 | BLU-ORG SP. SOL. 3 | 19 | 8L19 LEFT JET BUMPER |
| Q81 | 1J19-6 | BLU-YEL SP. SOL. 4 | 20 | 8L20 BOTTOM JET BUMPER |
| Q85 | 1J19-9 | BLU-BLK SP. SOL. 6 | 22 | 8L22 NOT USED |
| Q83 | 1J19-8 | BLU-GRN SP. SOL. 5 | 21 | 8L21 RIGHT JET BUMPER |

1J19-2 carries ORG-GRY and 1J19-1 ORG-VIO to the flipper buttons through the dashed relay contact `Z1`
(flipper relay) drawn between the two pins.

| 1J18 pin | wire label | 8P3 pin | switch |
| --- | --- | --- | --- |
| 9 | ORG-BLU SP. SOL. -6 SW | 29 | 8SW70 NOT USED |
| 8 | ORG-GRN SP. SOL. -5 SW | 28 | 8SW69 RIGHT JET BUMPER |
| 4 | ORG-YEL SP. SOL. -4 SW | 27 | 8SW68 LOWER JET BUMPER |
| 2 | ORG-BLK SP. SOL. -3 SW | 26 | 8SW67 LEFT JET BUMPER |
| 3 | ORG-RED SP. SOL. -2 SW | 25 | 8SW66 RIGHT KICKER |
| 5 | ORG-BRN SP. SOL. -1 SW | 24 | 8SW65 LEFT KICKER |

Each special switch has a 100 Ω resistor (8R1-8R6) and a 22 µF capacitor (8C1-8C6) drawn with it.

## Flippers

RIGHT FLIPPER BUTTON on 7J1/7P1-7 (ORG-VIO) and 7J1/7P1-8 (BLU-VIO); LEFT FLIPPER BUTTON on 7P1-10 (BLU-GRY)
and 7P1-9 (ORG-GRY). BLU-GRY reaches 8P3/8J3-32 and the coil 8L23 LEFT FLIPPER; BLU-VIO reaches 8P3/8J3-34 and
the coil 8L24 RIGHT FLIPPER. Each flipper coil is drawn with an `E.O.S.` contact. Flipper B+ comes from the
flipper power supply on P/O 3J3 / P/O 3P3 pins 4 (BLU) and 5 (GRY) to 8P2/8J2 pins 23 and 24. Only these two
flipper coils are drawn.

## Side notes

`TYPICAL SOLENOID CONNECTIONS` (coil with diode to SOL. B+, RED). `* FLASH LAMP CONNECTIONS`: four bulbs in a
series-parallel bridge between SOL. B+ and SOL. DRIVE, with a `2.2 1W` series resistor and a `330 1W` resistor
to ground. The page-3 corrections sheet changes these to `5, 10W` and `330, 2W`.

Uncertainty: every load on this sheet carries an `8L` (playfield) designator, including 8L11 GENERAL ILLUM.
RELAY, which the solenoid table connects at 3P7-1 on the power supply, and 8L15 BELL, which the table connects
at 7P1-17 in the cabinet. The designator prefix therefore does not prove where a load is mounted. The flash-lamp
bridge note says four bulbs but does not say which of 9, 10 and 14 it applies to.
