# STUB - System 80A with speech board

Coverage: **stub**. This is an abstract system container, not a physical machine or a playable game. It is retained because the public API reports it; `system_software` excludes it from physical-game coverage.

PinMAME `46e1a01a0f73dc5ce163d98db1ae435883ecc450` reports `gts80a` with `NOT_A_DRIVER` (0x4000). `src/driver.h` defines this flag as a fake root/container. Physical children retain their own identities because clone-root resolution stops below this flag. No playfield, fitted devices, mechanisms or physical construction is asserted here.

Reported manufacturer: Gottlieb. Reported year: 1981. Container drivers: `gts80a`.

Source: `PinmameGetGames`, https://github.com/vpinball/pinmame/tree/46e1a01a0f73dc5ce163d98db1ae435883ecc450; flag contract: `src/driver.h`, `NOT_A_DRIVER`.
