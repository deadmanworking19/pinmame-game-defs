# Torneo (Recel 1978)

Coverage: **partial - grouping only. Machine identity beyond the PinMAME catalog, and everything about playfield devices,
wiring, mechanisms and behaviour, is not evidenced yet.**

## Why one record holds two drivers

PinMAME declares both `r_torneo` and `r_torneoa` as direct clones of `recel`, the System III BIOS
(`machines/partial/recel/system-iii-1978.json`), so the catalog's clone-root rule gives each its own root. They are one
physical game: `recelgames.c` documents `r_torneo` as the circulating dump of the Torneo PROM with one wrong byte at
0x809, which makes the ball counter pass its limit on the first drain, and `r_torneoa` as the one-byte repair of that same
PROM (0xF6 0x74 -> 0x72), after which the counter walks three balls like every sibling game. Both hashes are marked
`BAD_DUMP`; the repair is a reconstruction, not a read of a physical PROM.

## Drivers this record holds

- `r_torneo` (1978, Recel, clone of `recel`).
- `r_torneoa` (1978, Recel, clone of `recel`).

## What a curator must establish next

IPDB/OPDB identity, the System III controller platform, full input, output and display enumeration with semantic names,
wiring and polarity, mechanisms, and spatial placement. No manual, table, ROM analysis or harness evidence is retained.

## Sources

- PinMAME `b7a60eb0dd9722f5397fc296987d94528ab111ff`, `src/wpc/recelgames.c:160-190`.
