# STUB - PinHeck System

Coverage: **stub**. This is an abstract system container, not a physical machine or a playable game. It is retained because the public API reports it; `system_software` excludes it from physical-game coverage.

PinMAME `8e0f721e3df7a2b4e8a9d2f4454ac7a9aa1ced53` reports `pinheck` with `NOT_A_DRIVER` (0x4000). `src/driver.h` defines this flag as a fake root/container. Physical children retain their own identities because clone-root resolution stops below this flag. No playfield, fitted devices, mechanisms or physical construction is asserted here.

Reported manufacturer: Spooky Pinball. Reported year: 2014. Container drivers: `pinheck`.

Source: `PinmameGetGames`, https://github.com/vpinball/pinmame/tree/8e0f721e3df7a2b4e8a9d2f4454ac7a9aa1ced53; flag contract: `src/driver.h`, `NOT_A_DRIVER`.
