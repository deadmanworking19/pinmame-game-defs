# Harley-Davidson (Stern) — major assemblies, magnet and fuse notes

Read from `Stern_Harley_Davidson_3rd_Edition_Pinball_Game_Service_Manual.pdf`, Section 4 Chapter 2 "Drawings for Major
Assemblies & Ramps", PDF pages 82-98 (printed pages 64-80: the printed number is the PDF page less 18; the footers of
PDF pages 82, 90, 94 and 98 print pages 64, 72, 76 and 80), plus the fuse table on PDF page 62 and the diode note on PDF
page 103. Each assembly page is an exploded drawing with a parts list whose part numbers and quantities are set in a
re-encoded font; they were decoded from the text layer by a character shift and spot-checked against the renders, not
read cell by cell, so this excerpt is not marked reviewed. Only the items that bear on a controller device, its sensor
or its actuator are listed.

| PDF page (printed) | Assembly | Items listed here |
| --- | --- | --- |
| 82 (64) | Ball Auto Launch Assembly | coil 24-940 090-5036-00B; plunger assembly 515-5000-02 |
| 82 (64) | Slingshot Assembly (Qty. 2) | coil 23-800; two Slingshot Stack (Blade) Switches 180-5054-00 per slingshot; slingshot bracket assembly 515-5339-01 |
| 83 (65) | Ball Trough Assembly | coil 26-1200 090-5044-00T; Dual OPTO TRANS Board Assembly 515-0173-00 and REC Board Assembly 515-0174-00; AP-A Ball Trough Enter/Exit Scoop 535-7329-01; AP-B Steel Balls (1-1/16") Qty 4 260-5000-00 |
| 84 (66) | Flipper Assembly (Left) 500-6307-10 | coil 22-1080 (YEL-GRN) (Left) 090-5032-00T; Power (End of Stroke) Switch 180-5149-00 |
| 85 (67) | Flipper Assembly (Right) 500-6307-00 | coil 23-1100 (ORANGE) (Right) 090-5030-00T; Power (End of Stroke) Switch 180-5149-00 |
| 86 (68) | Turbo Bumper Assembly | coil 26-1200; stack switch assembly 180-5015-04 with spoon actuator 545-5610-02; #555 wedge bulb 165-5002-00; Bumper Cap (RED) Qty 4 550-5057-02 |
| 87 (69) | Super VUK Assembly 500-6184-05 | coil 23-800 090-5001-00T (the page notes the -04 assembly used 24-940); Micro-Switch 180-5052-00 |
| 88 (70) | Kick-Big (Power Scoop) Assembly 500-6398-00 | coil 23-800; Power Scoop Weldment Assembly 515-6022-00; Micro Switch (High Form) 180-5057-00 |
| 89 (71) | Kick-Out Trough Assembly 500-6397-00 | 4-Position Membrane Switch 181-5001-00; coil 24-940 090-5036-00B; Diode PC Board 520-5146-00 (the switch diodes are not on the assembly) |
| 90 (72) | Lift (Motor) Assembly 500-6396-00-67 | Motor & Connector Assembly 515-7025-00-67 (motor "Autotrol 20 RPM 24v AC CCW" 041-5072-02, capacitor 130-5000-00, neon bulb 165-5021-00); Lift Cam Assembly 515-7021-00; two Micro-Switches 180-5052-00 with switch diodes 1N4001 112-5001-00; Relay PC Board 520-5010-00 |
| 91 (73) | Lift Plate & Cycle Assembly 500-6362-01-67 | Lift Plate Weldment Sub-Assembly 515-7022-00; the H-D® FLSTF® Fat Boy 1:10 motorcycle model 880-5034-01; link and spring; mounts on the Lift (Motor) Assembly 500-6396-00-67 |
| 92 (74) | Drop target bank harness | 500-6372-00-67 (Left) and 500-6372-01-67 (Right) |
| 93 (75) | 4-Bank Drop Target Assembly 500-5799-04 | coil 23-700 090-5022-00T; four Drop Targets (White) 545-5048-01; four Leaf-Switches (Drop Target Style) 180-5104-00; reset springs 265-5003-00 |
| 93 (75) | Magnet Assembly 515-6142-01 | Threaded Bushing Weld Assy. 515-6141-01; AP-A Magnet Coil, 22-650 (12" leads) 090-5042-01, secured under the playfield |
| 94 (76) | Up/Down Post Assembly 500-6293-00 | coil 23-1100 (ORG) 090-5030-00T |
| 94 (76) | Ball Deflector Assemblies, 500-5788-02 (Qty. 2) (Items 1-8), under a "UK ONLY OPTIONAL" band | item 1 Ball Deflector Coil Mounting Bracket 535-6857-02; item 3 coil 26-1200 090-5044-00T |
| 95 (77) | Ball Under-Trough Assembly 500-6401-00 (add -67) | Micro-Switch (High Form) 180-5057-00; switch body protect plate 535-6539-00 |
| 97 (79) | Right ramp | two Micro-Switches (for Wire Gate) 180-5087-00; gate assemblies 515-6556-04 |
| 98 (80) | Stop Light Assembly 500-6400-00-67 | Stop Light Plastic Housing Assembly 515-7030-00; three #44 bulbs 165-5000-44 in 3-lug sockets with 1N4001 diodes; OPTO Mtng Bracket 515-7026-00 carrying OPTO TRANS 520-5082-00 and REC 520-5083-01 |

Fuse table (PDF page 62), under-playfield fuses "LOC: UNDER PLAYFIELD (near Flippers)": "3A 250v S.B. 50V DC Rt. Flipper
(BLU-YEL RED-YEL)", "3A 250v S.B. 50V DC Lt. Flipper (GRY-YEL RED-YEL)", "3A 250v S.B. 50V DC Magnet (Top Orbit) (VIO-YEL
BLK)"; the I/O board fuse list also carries "F20 4A 250v S.B. 50V DC Magnet(s)".

Diode note (PDF page 103): diodes sit on terminal strips ("DOTS") or the Diode Board ("DODB"); "There is 1 diode located
on a solder lug for the Magnet Fuse."; the terminal-strip decal lists "MAGNET", "FUSE", "Switch 46 Ball Eject (Scoop)".
