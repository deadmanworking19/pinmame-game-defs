# Fitted sound DIP bank

The curator visually checked the original manual PDF36 sound-board
assembly and PDF38 sound-board logic. Assembly DS1 beside SW1/10J3 contains
two sliding contacts labelled1/2, unlike the CPU assembly's absent F/D banks.
The logic drawing positively draws both DS1 contacts to ground, with ON at
the right, pull-ups via SR1 and RC paths R2/C2 and R4/C4. This establishes
one two-position physical DIP bank, not a software menu inferred from ports.
Pinned wmssnd.c s67s_cmd_w combines(data &0x1f) with(core_getDip(0)<<5),
placing bank0 bits0/1(public DIP1/2) at sound-command bits5/6.
Functional audio-option names are not printed on
this drawing and are not invented. The committed CPU excerpt's full BOM
concerns the CPU board only; no sound-board parts-table cells are quoted here.
