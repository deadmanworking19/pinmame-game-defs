# Harlem Globetrotters On Tour - A3 solenoid driver, continuous outputs and the flipper enable relay

Transcribed from `Bally_1979_Harlem_Globetrotters_On_Tour_Manual.pdf`, PDF page 42, the "REG & SOLENOID DRIVE ASSEMBLY A3" sheet W-1183-18c, read from a 206 dpi render of the scan. Only the continuous-solenoid section on the right of the sheet and the flipper circuit it switches are transcribed; the momentary-solenoid decoder and the regulator are not. Component values are the sheet's own; "IN4004" is printed with a letter I.

## Continuous solenoid drivers

| A3 J4 pin | sheet label | PIA line | driver | output |
| --- | --- | --- | --- | --- |
| 8 | FLIPPER DISABLE | PB6, CONT. 1 | R37 3.9K, U4 pin 3 (P/03081), R38 120Ω, CR15 IN4004, Q15 SE9302 (R39 330Ω, C11 .002) | the K1 relay coil, labelled "FLIPPER ENABLE RLY.", returned to "43 V.", with CR20 IN4004 drawn across the coil |
| 11 | *(no label beside the pin)* | PB4, CONT. 2 | R40 3.9K, U4 pins 9-10, R41 120Ω, CR17 IN4004, Q17 SE9302 (R42 330Ω, C12 .002) | J5 pin 7, "RIGHT GATE" |
| 10 | *(no label beside the pin)* | PB7, CONT. 3 | R43 3.9K, U4 pins 11-12, R44 120Ω, CR18 IN4004, Q13 SE9302 (R45 330Ω, C13 .002) | J2 pin 5, "N/U" |
| 9 | COIN LOCK OUT | PB5, CONT. 4 | R46 3.9K, U4 pins 13-14, R48 120Ω, CR19 IN4004, Q19 SE9302 (R47 330Ω, C14 .002) | J2 pin 8, "COIN LO." |

J4 pin 1 is "N/U", pin 2 "KEY" and pin 12 "N/U". J5 pin 3 and J3 pin 9 are "N/U" on the same vertical bus; J3 pins 24 and 23 are "GRD." with "+43V SOLENOID GRD."

## Flipper circuit

The K1 contacts sit between the flipper buttons and the flipper coils:

| connector | sheet label |
| --- | --- |
| J2 pin 2 | LEFT FLIPPER SW., "TO LEFT FLIPPER BUTTON" |
| J2 pin 1 | RIGHT FLIPPER SW., "TO RIGHT FLIPPER BUTTON" |
| J1 pin 8 | "TO LEFT FLIPPER COIL" |
| J1 pin 9 | "TO RIGHT FLIPPER COIL" |
| J3 pin 5 | "TO A2J3-9" (the K1 enable line) |

A K1 contact is drawn between each button line and its coil line (the contact numbers printed beside them are not reliably legible in the scan and are not transcribed); each button reaches its coil line only through K1, so the flippers work only while the ROM holds CONT. 1 energized.
