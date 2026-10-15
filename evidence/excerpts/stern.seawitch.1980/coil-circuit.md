# Seawitch SDU decoder and continuous drivers

Source: schematics PDF page 10, 12B-432-S-123 sheet 3 of 3, SOLENOID DRIVER VOLTAGE REGULATOR SCHEMATIC for SEA WITCH. Drawing crop and complete output transcription. Public addresses are derived from the pinned emulator, not printed test numbers.

| U2 74154 pin | SDU transistor | Derived public |
| ---: | --- | ---: |
| 1 | Q2 | 1 |
| 2 | Q1 | 2 |
| 3 | Q5 | 3 |
| 4 | Q6 | 4 |
| 5 | Q7 | 5 |
| 6 | Q3 | 6 |
| 7 | Q4 | 7 |
| 8 | Q8 | 8 |
| 9 | Q13 | 9 |
| 10 | Q14 | 10 |
| 11 | Q9 | 11 |
| 13 | Q10 | 12 |
| 14 | Q12 | 13 |
| 15 | Q11 | 14 |
| 16 | Q16 | 15 |
| 17 | [blank: no transistor/load] | [unaddressable slot 16] |

| PIA line | Transistor | Printed destination | Derived public |
| --- | --- | --- | ---: |
| PB4 | Q17 | J5-7 N/U; J5-3 N/U | 17 |
| PB5 | Q19 | J2-8 COIN LOCK-OUT (Y-W) | 18 |
| PB6 | Q15 | FLIPPER ENABLE RELAY | 19 |
| PB7 | Q18 | J2-15 N/U; J3-9 N/U | 20 |

Complete solenoid connector annotations:

| Connector | Pin | Printed annotation |
| --- | ---: | --- |
| J2 | 9 | LEFT THUMPER (G-O) |
| J2 | 4 | TOP THUMPER (G-BLU) |
| J2 | 10 | OPEN |
| J2 | 11 | L. SLING-SHOT (G-R) |
| J2 | 5 | KNOCKER (G-B) |
| J2 | 12 | R. SLING-SHOT (R-Y) |
| J1 | 5 | MID. BANK TARG. (B-BLU) |
| J1 | 2 | [blank] |
| J1 | 3 | [blank] |
| J5 | 10 | L. BANK TARG. (B-O) |
| J5 | 12 | TOP BANK TARG. (B-Y) |
| J5 | 11 | OUT-HOLE (B-G) |
| J5 | 9 | R. THUMPER (R-BLU) |
| J5 | 15 | OPEN |
| J5 | 13 | OPEN |
| J5 | 14 | OPEN |
| J5 | 8 | OPEN |

Q15's relay contacts connect J1-8 to J2-2 (left button) and J1-9 to J2-1 (right button), with relay supply +43 VDC on J3-5 from A2J3-8 (Y-W). The two relay contacts are not four separately numbered CPU coil outputs. The printed note states that Solenoid Test Display No. is Drive Transistor (Q) Position on SDU.

Cabinet page 7 prints knocker wire B-Y; this sheet prints G-B. Both readings are retained. Structured wiring follows the game's cabinet sheet. Spare connector branches are not additional fitted loads.
