# Factory service tests used by the recreation notes

Factual paraphrase and complete indicator/control tables from the retained
Champion Pub operations manual. Visually checked against native page renders.

## Setup and switch tests — PDF 42, printed 1-16

Up/Down selects a test, Enter opens it, and Escape returns to the test menu.
Start requests wire, driver, connector and fuse information. The manual's setup
for tests using the +50 V or +20 V circuits pulls the top interlock button out;
the interlocks are on the bracket inside the coin-door opening.

T.1 displays the name and number of each switch pressed. T.2 cycles through
detected closed switches. T.3 isolates a selected switch: a mechanical contact
is made when the display reads closed, while a broken opto beam is made when
it reads open. These factory diagnostic words are retained separately from
PinMAME's normalized public input polarity.

## T.16 Jump Rope — PDF 45, printed 1-19

The test reports motor, popper, magnet, cam and ball opto states. The cam should
be open at home, with the rope at a downward 45-degree angle. The printed
horizontal-position phrase is literally "left is center"; its wording is
ambiguous and no additional coordinate is inferred. The ball opto reads open
while a ball rests on the magnet.

| Control | Factory test action |
| --- | --- |
| Enter | Toggle rope motor on/off |
| Up | Operate popper and magnet as during a game |
| Exit | Leave test |

A ball can be placed on the magnet, the motor started and Up used to test
whether the launched ball avoids the rope.

## T.17 Boxer — PDF 46, printed 1-20

The display reports four facing optos and three impact contacts.

| Indicator | Printed condition for CLOSED |
| --- | --- |
| LT | Boxer faces left |
| FT | Boxer faces front |
| RT | Boxer faces right |
| RR | Boxer faces rear |
| HD | Head contact activated |
| G1 | Gut 1 contact activated |
| G2 | Gut 2 contact activated |

| Mode/control | Factory test action |
| --- | --- |
| Enter | Change between Arms and Move modes |
| Exit | Leave test |
| Arms: Down | Swing left arm |
| Arms: Up | Swing right arm |
| Move: Down | Move to next clockwise position, then stop |
| Move: Up | Move to next counterclockwise position, then stop |

## T.18 LED bars — PDF 46, printed 1-20

The test runs patterns on the life bars. Enter toggles running/stopped, and
Exit leaves the test. Both bars should show the same count of illuminated
LEDs. This procedure does not supply serial-bit or connector-pin identities.
