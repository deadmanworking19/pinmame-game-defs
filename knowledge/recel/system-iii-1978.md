# System III (Recel 1978)

Coverage: **partial system-software classification; not a physical game definition**

## Classification

PinMAME registers `recel` as `GAMEX(1978,recel,0,RECEL,recel,recel,ROT0,"Recel","System III",NOT_A_DRIVER)` in `recelgames.c`, and `driver.c` lists it as "System III (not a game)". Its romset holds only the two spider-chip dumps of the shared System III program (`a2361.b1`, `a2362.b2`); `recel.h` calls it the BIOS common to every machine, which ships no game PROM of its own. Every Recel, Interflip and Inder System III game (`r_*`) is a clone of it that adds its own game PROM.

It is therefore system software, not a playfield an author can recreate, and the catalog keeps every `r_*` game out of this record: since PinMAME `b7a60eb0` a reported `NOT_A_DRIVER` parent ends clone-root resolution (`resolve_root_driver` in `src/pinmame_game_defs/catalog.py`), the same rule PinMAME's own drivers apply when they look for a game's root (`while (rootDrv->clone_of && (rootDrv->clone_of->flags & NOT_A_DRIVER) == 0)`), so each game is its own physical record.

## Remaining documentation

The shared program's behaviour, the System III controller contract and the board hardware are not documented here. That keeps this record partial without affecting physical-game coverage.

## Sources

- PinMAME `b7a60eb0dd9722f5397fc296987d94528ab111ff`, `src/wpc/recelgames.c:67-73`, `src/wpc/recel.h:103-126` and `src/wpc/driver.c:1016`.
