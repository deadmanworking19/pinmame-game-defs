# Gladiators (Gottlieb, 1993) spatial review

Status: unknown. The machine record stays `partial` at `machines/partial/gottlieb/gladiators-1993.json`; its spatial dimension stays open because of the 3 spatial blockers below. No playfield device is placed.

## Evidence decisions

- A playfield device without a retained table object or factory drawing carries no `spatial` key; nothing is projected or estimated.
- Backbox and cabinet devices take controlled `not_applicable` records: the six lightbox lamps, the credit-button lamp, the lightbox and game-over relays, the shaker motor, the knocker, the coin meter, the cabinet and flipper-button switches, the test inputs and the DMD.

## Counts

- Placements: 0
- Inputs with an omitted spatial key: 30
- Outputs with an omitted spatial key: 112
- Inputs with a controlled `cabinet_or_service` record: 14
- Inputs with a controlled `unused` record: 63
- Inputs with a controlled `virtual` record: 1
- Outputs with a controlled `cabinet_or_service` record: 12
- Outputs with a controlled `unused` record: 4
- Outputs with a controlled `virtual` record: 4

## Blockers

- No VPX table of the machine is retained: the known-working script is held only as the pinned corpus copy, and the table it belongs to (Kiwi's Gladiators (Premier 1993) VPX v1.1.1) has not been acquired, so no playfield object coordinate is available for any switch, lamp, coil or flasher.
- No factory drawing is retained: IPDB lists the instruction manual pages and the coil, fuse and switch charts without hosting them, and no other attributable copy was found, so no placement could be taken or checked from the machine's own location drawings.
- The known-working script places solenoids 8, 9, 22 and 24 and lamps 112-117 in its backbox; the lamps' ROM name (LIGHTBOX) settles theirs, but the flashers' location rests on the script and their backglass-art names alone, so they are not classified.

## Promotion decision

Every controller address is enumerated with a semantic disposition taken from the ROM's own service tests, the mechanisms are covered, and polarity is settled for every switch by the read path, the ROM's Switch Matrix Test and the known-working script. Promotion to `author_ready` is refused because no playfield device has a position, so `coverage.missing` is `["spatial_placement"]`. The retained known-working table (Kiwi's VPX v1.1.1) would give every script-bound object a coordinate, and the instruction manual's location drawings would check them.
