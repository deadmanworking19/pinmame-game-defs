# Gold — Flipper Circuits and Opto Boards

Gold manual PDF page135, printed3-19, visually checked against page-135.png. Entire Flipper Circuits table region; layout flattened to one destination column with explicit blanks.

## Shared playfield power

| Wire | Function | Connector |
| --- | --- | --- |
| Gray/Yellow | Left Flipper Power | J109-5 |
| Blue/Yellow | Right Flipper Power | J109-7 |

## Flipper controller outputs to playfield

| Wire | Function | Connector |
| --- | --- | --- |
| Orange/Gray | Upper Left Flipper Holding | J802-1 |
| Black/Blue | Upper Left Flipper Power | J802-3 |
| Orange/Violet | Upper Right Flipper Holding | J802-4 |
| Black/Yellow | Upper Right Flipper Power | J802-6 |
| Orange/Blue | Lower Left Flipper Holding | J802-7 |
| Blue/Gray | Lower Left Flipper Power | J802-9 |
| Orange/Green | Lower Right Flipper Holding | J802-11 |
| Blue/Violet | Lower Right Flipper Power | J802-13 |


## Controller supplies and ribbon (same table)

| Wire | Function | To power driver | To CPU | To cabinet | To playfield |
| --- | --- | --- | --- | --- | --- |
| Black | Ground | J801-1,4 | --- | --- | --- |
| Gray | +5V | J804-1 | --- | --- | --- |
| Gray/Green | +12V | J804-2 | --- | --- | --- |
| Black | Ground | J804-5,6 | --- | --- | --- |
| Ribbon Cable | Data | --- | J803 | --- | --- |

## Controller inputs (same table)

| Wire | Function | To cabinet | To playfield |
| --- | --- | --- | --- |
| Blue/Violet | Right Flipper Button | J805-1 | --- |
| Blue/Gray | Left Flipper Button | J805-2 | --- |
| Black/Yellow | Right Flipper Button | J805-3 | --- |
| Black/Blue | Left Flipper Button | J805-5 | --- |
| Orange | Switch Ground | J805-6 | --- |
| Black/Green | Right Flipper Switch | --- | J806-1 |
| Black/Blue | Left Flipper Switch | --- | J806-3 |
| Black/Violet | Upper Right Flipper Switch | --- | J806-4 |
| Black/Gray | Upper Left Flipper Switch | --- | J806-5 |
| Orange | Switch Ground | --- | J806-6 |

## Gold opto board construction

Gold manual2-13 (PDF80) names A-17316 Flipper Opto PCB Assembly. Complete associated parts table, visually checked:

| Item | Part Number | Description |
| --- | --- | --- |
| 1 | 03-9001 | Interrupter Flip-Opto |
| 2 | A-16384 | Flipper Opto Switch Assembly |
| [blank, under item2] | 5010-08930-00 | Resistor, 470Ω, 1/2W, 5% |
| [blank, under item2] | 5490-12451-00 | Opto Interr Lg.10mA. |
| [blank, under item2] | 5791-14246-07 | Connector,7-pin Header |

The schematic on3-12 (PDF128) has two opto channels, SW1/SW2, common ground and+12V. Thus112/116 and114/118 are two optical channels of the two physical cabinet buttons. The flipper-register read is complemented in pinned wpc.c; no Fliptronic inversion mask applies here, so normally_closed is false under the platform contact convention. EOS construction is independent: Gold2-15 explicitly requires a .062±.015-inch gap at rest and closure on actuation.

The Gold flipper power schematic3-10 (PDF126) supplies the coils via a power-driver-board bridge and the J801-J806 controller. This primary circuitry, A-17316 button optos, and the separately retained owner board photo distinguish the button sensor revision from the Fliptronics I power/controller architecture.
