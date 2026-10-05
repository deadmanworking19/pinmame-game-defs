# AMH SWITCH MATRIX (AMH_Switch_Matrix_Production.pdf)

Transcribed from the chart's text layer, each word placed by the cell number it sits under, and every cell compared with the 110 dpi render on 2026-10-05. Blank cells are written (blank).

Column headers (wire colours, as printed): COLUMN 7: GREEN GRAY; COLUMN 6: GREEN VIOLET; COLUMN 5: GREEN BLUE; COLUMN 4: GREEN BLACK; COLUMN 3: GREEN YELLOW; COLUMN 2: GREEN WHITE; COLUMN 1: (blank); COLUMN 0: (blank)

Row headers (wire colours, as printed): ROW 0: WHITE BROWN; ROW 1: WHITE RED; ROW 2: WHITE BLACK; ROW 3: WHITE YELLOW; ROW 4: WHITE GREEN; ROW 5: WHITE BLUE; ROW 6: WHITE VIOLET; ROW 7: WHITE GREY

Grid (COLUMN 7 at left to COLUMN 0 at right; ROW 0 at top). Each cell is `n = column*8 + row`: label.

| | COL 7 | COL 6 | COL 5 | COL 4 | COL 3 | COL 2 | COL 1 | COL 0 |
|---|---|---|---|---|---|---|---|---|
| ROW 0 | 56: (blank) | 48: LEFT OUTLANE | 40: “O” | 32: BALCONY JUMP SUCCESS | 24: (blank) | 16: WIKI | 8: (blank) | 0: (blank) |
| ROW 1 | 57: SHOOTER LANE | 49: LEFT INLANE | 41: “R” | 33: BALCONY JUMP APPROACH | 25: (blank) | 17: TECH | 9: (blank) | 1: (blank) |
| ROW 2 | 58: (blank) | 50: LEFT SLING | 42: “B” | 34: POP PATH/ JUMP FAIL | 26: (blank) | 18: GHOST TARGET 1 (left) | 10: (blank) | 2: (blank) |
| ROW 3 | 59: TROUGH BALL 1 | 51: LEFT EOS | 43: BALL IN ELEVATOR CAR | 35: BASEMENT UPPER | 27: (blank) | 19: GHOST TARGET 2 (middle) | 11: (blank) | 3: (blank) |
| ROW 4 | 60: TROUGH BALL 2 | 52: RIGHT EOS | 44: (blank) | 36: BASEMENT LOWER | 28: HOTEL PATH | 20: GHOST TARGET 3 (right) | 12: (blank) | 4: (blank) |
| ROW 5 | 61: TROUGH BALL 3 | 53: RIGHT SLING | 45: POP BUMPER 2 | 37: Pop Bumper 0 | 29: ELEVATOR CALL BUTTON | 21: (blank) | 13: (blank) | 5: (blank) |
| ROW 6 | 62: TROUGH BALL 4 | 54: RIGHT INLANE | 46: POP BUMPER 1 | 38: UPPER LEFT ORBIT | 30: PSYCHIC | 22: BASEMENT RIGHT SCOOP | 14: (blank) | 6: (blank) |
| ROW 7 | 63: DRAIN | 55: RIGHT OUTLANE | 47: (blank) | 39: LOWER LEFT ORBIT | 31: (blank) | 23: VUK LEFT BEHIND DOOR | 15: (blank) | 7: (blank) |

## CABINET SWITCHES

| right column | left column |
|---|---|
| 0: (blank) | 8: TILT (yellow) |
| 1: COIN DOOR OPEN (gray) | 9: (blank) |
| 2: (blank) | 10: (blank) |
| 3: RIGHT FLIPPER (Purp / black) | 11: (blank) |
| 4: LEFT FLIPPER (green / red) | 12: START BUTTON (yellow / brown) |
| 5: RED SERVICE MENU (blue) | 13: GHOST LOOP OPTO (opto #1 on aux, yellow / red) |
| 6: GREEN SERVICE MENU (green) | 14: SPOOKY DOOR OPTO (opto #2 on aux, yellow / blue) |
| 7: COIN MECH (purple) | 15: (blank) |

## Other printed text

- title_printed: AMH_ SWITCH MATRIX
- diagram_labels: NC | NO | C | Column Line | Row Line
- axis_labels: switch[x] BYTE | switch[x], x BIT
- pcb_switch_column_connector_pins: GND | COL7 | COL6 | COL5 | KEY | COL4 | COL3 | COL2 | COL1 | COL0
- pcb_switch_row_connector_pins: GND | ROW7 | ROW6 | KEY | ROW5 | ROW4 | ROW3 | ROW2 | ROW1 | ROW0
- servos: SERVOS | SERVO 0 - Hellevator | SERVO 1 - Spooky Door | SERVO 2 - Ghost | SERVO 3 - Target
- TCBDTWN: {"pins_left_to_right": ["3V", "GROUND", "EMPTY", "EMPTY", "KEY", "EMPTY", "EMPTY", "OPTO 2", "OPTO 1"], "wire_colours": {"3V": "YELLOW / BROWN", "GROUND": "YELLOW / GRAY", "OPTO 2": "YELLOW / BLUE", "OPTO 1": "YELLOW / RED"}}
