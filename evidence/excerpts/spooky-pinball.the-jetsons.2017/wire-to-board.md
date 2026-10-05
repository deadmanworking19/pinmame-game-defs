# Jetson’s wire-to-board chart (JETSONS-WIRE-TO-BOARD.pdf)

Transcribed from the chart's text layer (the RZ chart from its raster), every pin aligned by its tick; the coil banks, the cabinet header and the GI_1 header were spot-checked against the render at 300 dpi, not every pin. Uncertain readings are listed at the end.

Pins are listed in tick order as drawn on the chart (connector header lines run left to right as printed, vertical headers top to bottom). '(blank)' means no wire text is printed at that tick; '(unlabeled tick)' means a tick with no pin label.

## Connectors

### Board Power

| # | pin label | wire text |
|---|---|---|
| 1 | g | black |
| 2 | 12v | yellow |
| 3 | (unlabeled tick) | (blank) |
| 4 | 5v | red |

### Display Pwr

| # | pin label | wire text |
|---|---|---|
| 1 | g | black |
| 2 | 5v | red |
| 3 | 12v | yellow |
| 4 | . | key |

### Aux Pwr

| # | pin label | wire text |
|---|---|---|
| 1 | 3.3v | (blank) |
| 2 | 5v | (blank) |
| 3 | 12v | (blank) |
| 4 | g | (blank) |

### Switch Row

| # | pin label | wire text |
|---|---|---|
| 1 | (unlabeled tick) | (blank) |
| 2 | 7 | white/gray |
| 3 | 6 | (blank) |
| 4 | . | key |
| 5 | 5 | white/blue |
| 6 | 4 | white/green |
| 7 | 3 | white/yellow |
| 8 | 2 | white/black |
| 9 | 1 | white/red |
| 10 | 0 | white/brown |

### Light Column

| # | pin label | wire text |
|---|---|---|
| 1 | (unlabeled tick) | (blank) |
| 2 | . | key |
| 3 | 0 | yellow/brown |
| 4 | 1 | yellow/red |
| 5 | 2 | yellow/white |
| 6 | 3 | yellow/black |
| 7 | 4 | yellow/green |
| 8 | 5 | (blank) |
| 9 | 6 | (blank) |
| 10 | 7 | (blank) |

### Light Row

| # | pin label | wire text |
|---|---|---|
| 1 | (unlabeled tick) | (blank) |
| 2 | 0 | red/brown |
| 3 | . | key |
| 4 | 1 | red/black |
| 5 | 2 | red/white |
| 6 | 3 | red/yellow |
| 7 | 4 | red/green |
| 8 | 5 | red/blue |
| 9 | 6 | red/violet |
| 10 | 7 | red/gray |

### Switch Column

| # | pin label | wire text |
|---|---|---|
| 1 | (unlabeled tick) | (blank) |
| 2 | 7 | (blank) |
| 3 | 6 | (blank) |
| 4 | 5 | (blank) |
| 5 | . | key |
| 6 | 4 | green/violet |
| 7 | 3 | green/blue |
| 8 | 2 | green/black |
| 9 | 1 | green/yellow |
| 10 | 0 | green/white |

### Sol Pwr

| # | pin label | wire text |
|---|---|---|
| 1 | g | black |
| 2 | g | black |
| 3 | . | key |
| 4 | p | red |

## RGB

### RGB Com Out

| # | pin label | wire text |
|---|---|---|
| 1 | 5v | whtie/red |
| 2 | 12v | (blank) |
| 3 | RGB CLK | white/blue |
| 4 | RGB DAT | white/green |
| 5 | prop aux 0 | (blank) |
| 6 | prop aux 1 | (blank) |
| 7 | . | key |
| 8 | g | white/black |

### Cabinet RGB

| # | pin label | wire text |
|---|---|---|
| 1 | RR | white/red |
| 2 | GR | white/green |
| 3 | BR | white/blue |
| 4 | 12v | white/black |
| 5 | RL | white/red |
| 6 | GL | white/green |
| 7 | BL | white/blue |
| 8 | 12v | white/black |
| 9 | (unlabeled tick) #9 | key |
| 10 | (unlabeled tick) #10 | (blank) |
| 11 | (unlabeled tick) #11 | (blank) |

## Sol Banks (connector pins)

### Sol Bank 0 (Power - ORANGE)

| # | pin label | wire text |
|---|---|---|
| 1 | pwr | 50v Orange |
| 2 | 0 | (blank) |
| 3 | 1 | (blank) |
| 4 | 2 | orange/green |
| 5 | 3 | orange/violet |
| 6 | . | key |
| 7 | 4 | orange/black |
| 8 | 5 | orange/grey |
| 9 | 6 | orange/white |
| 10 | 7 | orange/blue |

### Sol Bank 1 (Power - BLUE)

| # | pin label | wire text |
|---|---|---|
| 1 | pwr | 50v Blue |
| 2 | 8 | blue/green |
| 3 | 9 | blue/red |
| 4 | 10 | blue/grey |
| 5 | 11 | (blank) |
| 6 | 12 | (blank) |
| 7 | . | key |
| 8 | 13 | (blank) |
| 9 | 14 | (blank) |
| 10 | 15 | (blank) |

### Sol Bank 2 (Power - PURPLE)

| # | pin label | wire text |
|---|---|---|
| 1 | pwr | 50v Violet |
| 2 | 16 | violet/black |
| 3 | 17 | violet/green |
| 4 | 18 | violte/white |
| 5 | 19 | violet/red |
| 6 | 20 | violet/grey |
| 7 | 21 | (blank) |
| 8 | . | key |
| 9 | 22 | (blank) |
| 10 | 23 | (blank) |

## Coil lists as printed under the wiring

Sol Bank 0

Power - ORANGE

- 0 - Knocker (option)
- 1 - Shaker (option)
- 2 - Rt Flip Low
- 3 - Rt Flip High (center)
- 4 - Ball Load
- 5 - Ball Launch
- 6 - Left Flip High (center)
- 7 - Left Flip Low

Sol Bank 1

Power - BLUE

- 8 - Scoop
- 9 - Left Sling
- 10 - Right Sling
- 11 -
- 12 -
- 13 -
- 14 -
- 15 -

Sol Bank 2

Power - PURPLE

- 16 - Up Post
- 17 - Lower Pop
- 18 - Left Pop
- 19 - Saucer Kick Out
- 20 - Right Pop
- 21 -
- 22 -
- 23 -

## Cabinet header

Title: Cabinet

- L. flipper - gray/orange
- R. flipper - gray/black
- launch - yellow
- door - gray/white
- menu - gray/blue
- enter - gray/green
- coin mech - gray/violet
- tilt - gray/yellow
- start but - gray/brown
- start light - white
- 5V - gray/red
- ground - black

## GI / Flasher

### GI_0

| # | pin label | wire text |
|---|---|---|
| 1 | 5V | (blank) |
| 2 | (unlabeled tick) (text 'key' printed to its right) | key |
| 3 | 7 | (blank) |
| 4 | 6 | (blank) |
| 5 | 5 | (blank) |
| 6 | 4 | (blank) |
| 7 | 3 | (blank) |
| 8 | 2 | (blank) |
| 9 | 1 | (blank) |
| 10 | 0 | (blank) |

### Flasher

| # | pin label | wire text |
|---|---|---|
| 1 | 12V | (blank) |
| 2 | g | (blank) |

Printed text beside header: pink

### GI_1

| # | pin label | wire text |
|---|---|---|
| 1 | 8 | brown/yellow - ramp Flasher |
| 2 | 9 | brown/red - scoop Flasher |
| 3 | 10 | brown/black - Left GI |
| 4 | 11 | brown/white - Right GI |
| 5 | 12 | (blank) |
| 6 | 13 | (blank) |
| 7 | 14 | (blank) |
| 8 | . | (blank) |
| 9 | 5V | brown - POWER |
| 10 | (unlabeled tick) | key |

## Optos

### Opto1 (header, 4 ticks)

| # | pin label | wire text |
|---|---|---|
| 1 | (none) | (blank) |
| 2 | (none) | (blank) |
| 3 | (none) | (blank) |
| 4 | (none) | (blank) |

### Opto2 (header, 4 ticks)

| # | pin label | wire text |
|---|---|---|
| 1 | (none) | (blank) |
| 2 | (none) | (blank) |
| 3 | (none) | (blank) |
| 4 | (none) | (blank) |

### Opto3 (header, 4 ticks)

| # | pin label | wire text |
|---|---|---|
| 1 | (none) | grey/violet |
| 2 | (none) | white/violet |
| 3 | (none) | grey/yellow |
| 4 | (none) | yellow/grey |

### Opto4 (header, 4 ticks)

| # | pin label | wire text |
|---|---|---|
| 1 | (none) | (blank) |
| 2 | (none) | (blank) |
| 3 | (none) | (blank) |
| 4 | (none) | (blank) |

### Opto5 (header, 4 ticks)

| # | pin label | wire text |
|---|---|---|
| 1 | (none) | blue/violet |
| 2 | (none) | black/violet |
| 3 | (none) | blue/orange |
| 4 | (none) | black/orange |

### Opto6 (header, 4 ticks)

| # | pin label | wire text |
|---|---|---|
| 1 | (none) | blue/red |
| 2 | (none) | black/red |
| 3 | (none) | blue/black |
| 4 | (none) | black/blue |

### Opto7 (header, 4 ticks)

| # | pin label | wire text |
|---|---|---|
| 1 | (none) | (blank) |
| 2 | (none) | (blank) |
| 3 | (none) | (blank) |
| 4 | (none) | (blank) |

### OPTOS box

- Opto6: wires left to right: blue/red, black/red, blue/black, black/blue
  - Trough Emitter <- blue/red, black/red
  - Trough Receiver <- blue/black, black/blue
- Opto5: wires left to right: blue/violet, black/violet, blue/orange, black/orange
  - JAM Emitter <- blue/violet, black/violet
  - JAM Receiver <- blue/orange, black/orange
- Opto - 3: wires left to right: grey/violet, white/violet, grey/yellow, yellow/grey
  - Scoop Emitter <- grey/violet, white/violet
  - Scoop Receiver <- grey/yellow, yellow/grey

## Servos

- Servo0: 3 ticks, no labels, no wire colours
- Servo1: 3 ticks, no labels, no wire colours
- Servo2: 3 ticks, no labels, no wire colours
- Servo3: 3 ticks, no labels, no wire colours
- Servo4: 3 ticks, no labels, no wire colours
- Servo Fuse 3A Fast-Blo
- SERVOS box: SERVOS / Topper - 0 / Open - 1 / Black or Brown on far right pin

## Fuses

- F1 3A Slow-BLO
- F2 3A Slow-BLO
- F3 3A Slow-BLO
- GI 1 1A - Fast Blo
- GI 0 1A - Fast Blo
- FLASHER FUSE 1A - Fast Blo
- Servo Fuse 3A Fast-Blo

## Other text

- page: 792 x 612 pt, one page
- titles_printed: Board Power; Opto2; Opto1; Servo0; Servo1; Servo2; Servo3; Servo4; RGB Com Out; Cabinet RGB; DMD_CON; Display Pwr; SD CARD; AUDIO; Aux Pwr; Cabinet; Light Column; Light Row; Opto4; Opto3; Opto6; Opto5; Opto7; SERVOS; OPTOS; MOSFETS - IRL540; Switch Row; Switch Column; Sol Bank 0; Sol Bank 1; Sol Bank 2; Sol Pwr; GI_0; GI_1; Flasher
- mosfets: MOSFETS - IRL540; two staggered rows of boxed numbers: top row 0 2 4 ... 22, bottom row 1 3 5 ... 23
- fuse_leader_lines: Leader lines drawn from fuse F1 to the Sol Bank 0 title, from F2 to the Sol Bank 1 title, and from F3 to the Sol Bank 2 title
- diode_note: Power goes to the BANDED side of the diode! (followed by a diode symbol)
- sol_bank_list_titles: {"0": ["Sol Bank 0", "Power - ORANGE"], "1": ["Sol Bank 1", "Power - BLUE"], "2": ["Sol Bank 2", "Power - PURPLE"]}

## Uncertain readings

- Sol Bank 2: the list header says 'Power - PURPLE' but the connector pwr wire is printed '50v Violet' and every coil wire is 'violet/...'; transcribed as printed (purple and violet are likely the same colour).
- Typos kept verbatim: 'whtie/red' (RGB Com Out 5v), 'violte/white' (Sol Bank 2 pin 18).
- GI_1 colour alignment: wire texts sit under ticks 8, 9, 10, 11, 5V and the unlabeled 10th tick ('key'); ticks 12, 13, 14 and '.' carry nothing. Read from tick x positions at 220 dpi.
- Switch Row pin 6 has no wire colour printed (white/purple is printed on the other three boards); Switch Column pins 7, 6, 5 and Light Column pins 5, 6, 7 have no wire colour printed; transcribed as blank.
- 'grey' and 'gray' are both used on this chart (orange/grey, blue/grey, violet/grey, grey/violet, grey/yellow, yellow/grey vs white/gray, red/gray, gray/orange...); transcribed as printed.
- Opto headers: header Opto3 colours (grey/violet, white/violet, grey/yellow, yellow/grey), Opto5 (blue/violet, black/violet, blue/orange, black/orange) and Opto6 (blue/red, black/red, blue/black, black/blue) agree with the OPTOS box groups (Scoop / JAM / Trough). In the box the Trough group is captioned 'Opto6', the JAM group 'Opto5' and the scoop group 'Opto - 3' (spacing differs).
- Leading unlabeled tick on Switch Row, Switch Column, Light Row and Light Column, an extra unlabeled tick after 5V on GI_1, and two unlabeled ticks after the 'key' tick on Cabinet RGB: counted from the artwork.
- Sol Bank 0 coils 0 and 1 ('(option)'), Bank 1 coils 11-15 and Bank 2 coils 21-23 have no wire colour and no name; transcribed as blank.
- Fuse leader lines (F1->Sol Bank 0, F2->Sol Bank 1, F3->Sol Bank 2) read from the drawn lines; not stated in text.
- Switch matrix: COLUMN 7 and COLUMN 6 carry no wire colour; cabinet cell 10 'TROUGH OPTO 1' (printed over three lines TROUGH / OPTO / 1), cell 11 'TROUGH JAM OPTO', cell 14 'SCOOP OPTO'.
- Switch cells 6 'KICKOUT HOLE' and 5 'ELROY LOOP' (column 0). Rows 6-7 of columns 7..1 are blank. Lamp cell 4 'LEFT SCOOP S' (printed S as a third line); lamp 36 'ORBITY J', 28 'ELROY J', 24 'ASTRO J', 26 'JUDY J', 34 'KICKOUT C'.
- Servos list on the switch matrix page: 'SERVO 0 - ORBITTY TOPPER' (spelling 'ORBITTY' kept), servos 1-3 have no names. The wire-to-board chart's SERVOS box says 'Topper - 0', 'Open - 1'.
