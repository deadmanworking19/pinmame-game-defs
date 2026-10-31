# Frontier - switch construction and the parts list coils and modules

Transcribed from `Bally_1980_Frontier_Manual.pdf`, PDF pages 23 and 24 (printed pages 19 and 20), read from the native 300 dpi renders of the scan, with Windows OCR as a first pass checked against the rendered pages.

## PDF page 23 (printed 19), ASSEMBLY ADJUSTMENTS: GENERAL

> All switch assemblies consist of leaf springs, contacts, separators, plastic tubing and screws to hold them to the mounting surface.. Before attempting to adjust a switch assembly, make sure that these screws are tight. If not, tighten screw closest to the contact end of the leaf spring first. This will prevent the assembly from being secured in such a manner that the leaf springs tend to fan out. In general, all leaf springs are adjusted for a 1/16" gap in the open position and .010" overtravel or wipe in the closed position. All contacts should be in good condition. Unless otherwise instructed, they should be dry or non-lubricated. All contacts should be free of dust and dirt. Contacts, with the exception of the flipper button switch assemblies, are plated to resist corrosion.

## PDF page 24 (printed 20), XI. PARTS LIST #1217 FRONTIER

| section | item | PART NUMBER |
| --- | --- | --- |
| MISCELLANEOUS | Transformer (Domestic or Export) | E-122-125 |
| MISCELLANEOUS | Bulbs, #44 | E-125-22 |
| MISCELLANEOUS | Fuse, 1 Amp. 3 AG Slow Blow (Playfield Solenoid Protection) | E-133-44 |
| ASSEMBLY COILS | Coin Lockout | FO-36-7000 |
| ASSEMBLY COILS | Flipper (2) | AQ-25-500/ 34-4500 |
| ASSEMBLY COILS | Knocker | AR-26-1200 |
| ASSEMBLY COILS | Outhole Kicker | AN-26-1200 |
| ASSEMBLY COILS | Thumper-Bumper (3) | AN-26-1200 |
| ASSEMBLY COILS | Sling-Shot (2) | AO-26-1200 |
| ASSEMBLY COILS | Drop Target (2) | NO-26-1900 |
| ASSEMBLY COILS | Saucer | AO-27-1300 |
| ASSEMBLY COILS | Gate | GO-36-6900 |
| PLAYFIELD PARTS | (blank) | See Figure II |
| MODULES | Lamp Driver A5 | AS-2518-23 |
| MODULES | Display Driver A1 (1 Used) | AS-2518-21 |
| MODULES | Display Driver A1 (4 Used) | AS-2518-58 |
| MODULES | Solenoid Driver/Voltage Regulator A3 | AS-2518-22 |
| MODULES | MPU A4 | AS-2962-23 |
| MODULES | Transformer & Rectifier A2 | AS-2877-1 |
| MODULES | Rectifier Board (Part of A2) | AS-2518-18 |
| MODULES | Sound | AS-3022-12 |
| REPAIRS PROCEDURES/AIDS | Module & Component Replacement | F.O.560-1 |
| REPAIRS PROCEDURES/AIDS | AID (Assistance in Diagnostics) Kit, used with F.O.560-1 | KIT #485-1 |

The page continues with the module component starter kits (#490 rectifier board, #503 MPU board A4 less memory U1-U6, #492 solenoid driver A3, #493 display driver A1, #494 lamp driver A5, and a sound A8 kit), which carry no game wiring.

The coil list counts two flipper coils, three thumper bumpers, two slingshots and two drop-target reset assemblies (the in-line bank and the three-target side bank). The MPU line prints AS-2962-23; IPDB lists the game's MPU as AS-2518-35. The parts list names the sound module AS-3022-12; pinned PinMAME emulates the game with its -51 sound board (SNDBRD_BY51).
