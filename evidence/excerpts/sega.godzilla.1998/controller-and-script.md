# PinMAME topology and VPW script excerpts

Sources: PinMAME revision `46e1a01a0f73dc5ce163d98db1ae435883ecc450`,
`src/wpc/segames.c` and `src/wpc/se.c`; retained VPW 1.0 extraction
`script.vbs`, SHA-256
`95d77a6678cc735792091e582abd66983a709b28e9bde307679d10029598949b`.
Method: direct source read; transcribed by the curator, reviewed against the files.

- `segames.c` declares all three Godzilla drivers using `INITGAME(..., GEN_WS,
  se_dmd128x32, 0)`; its macro sets the lamp-column count to 2 and the custom
  solenoid count to 0. `se.c` sets `nLamps` to `64 + lampCol * 8` and
  `nSolenoids` to `CORE_FIRSTCUSTSOL - 1 + custSol`, hence 80 and 50.
- `se.c` `switch_r` returns `~core_getSwCol(selocals.swCol)`;
  `dedswitch_r` reads the dedicated service bits and flipper column and returns
  their complement. `se_solenoid_w` masks Q15/Q16 and moves them to the
  flipper-output bits. Godzilla's own fast-flip configuration matches the root
  `godzilla` name but not the two clone names.
- VPW script lines 321 and 323–345 map lamps through `vpmMapLights AllLamps`,
  initialize switches 11–14 active and create three separate captive balls.
  Lines 353–384 bind magnets to 3, 4, 5 and 14. Lines 499–521 bind outputs 1,
  2, 6, 17, 7, 18–20 and 25–32 and the framework flipper callbacks. Lines
  720–727 hold trough switches while balls occupy the simulated trough, and
  line 762 pulses 15 during the release. Lines 774–785 exchange the two
  diverter walls; their flag is not itself proof of the physical UP position.
