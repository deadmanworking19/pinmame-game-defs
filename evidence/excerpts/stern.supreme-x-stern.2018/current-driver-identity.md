# Current Supreme driver identity

PinMAME 46e1a01a0f73dc5ce163d98db1ae435883ecc450, `src/wpc/spike1.c`
lines 1876-1890. Complete Supreme initializer, archive manifest and game descriptor:

```c
SPIKE1_INIT(supreme, "supreme", spike1_dmd, 130, SPIKE1_SWITCHES(8, 10, 9, 11, 76, 77, 78, 79, 14, 84))
ROM_START(supreme_101)
  ROM_REGION(0x07454000, SPIKE1_REGION, ROMREGION_MAPPED)
    ROM_LOAD("game", 0x00000000, 0x00462e0b, CRC(681a3c00) SHA1(dc9cbf0a4204a3bbaecede3a5f5f9b1f9a2269c2))
    ROM_LOAD("image.bin", 0x00463000, 0x06fa11ec, CRC(3eb2c19d) SHA1(23cf9140f30c15367c214503025962619a5937f6))
    ROM_LOAD("coil4node-LPC1112_101-0_22_0.hex", 0x07405000, 0x000082cd, CRC(22c8518e) SHA1(3961762f04c7ac0d5dfa12eb8e5f2a5c75a05bef))
    ROM_LOAD("coil4node-LPC1112_201-0_22_0.hex", 0x0740e000, 0x000082cd, CRC(01d69520) SHA1(f1b2f65b19ff88fd9fa3874b8373a1fc30fd8f88))
    ROM_LOAD("coil4node-LPC1313-0_22_0.hex", 0x07417000, 0x0000bcec, CRC(290c5e17) SHA1(ace1e1a6e37f370f4f49aa61624a95215566843a))
    ROM_LOAD("lcdnode-LPC1113_302-0_22_0.hex", 0x07423000, 0x0000b484, CRC(0e222d2c) SHA1(ae62c5331e7393b80e1ff0f946c41652f7d20a25))
    ROM_LOAD("pinnode-LPC1112_101-0_22_0.hex", 0x0742f000, 0x000080fb, CRC(0be8403d) SHA1(ff3f421ad4fcd06cdbc22936f378e3df123977cc))
    ROM_LOAD("pinnode-LPC1112_201-0_22_0.hex", 0x07438000, 0x00008138, CRC(b3646ae2) SHA1(1f5bda3ebbe5b8e2699f30bf946ea19e6a2ac6c0))
    ROM_LOAD("pinnode-LPC1313-0_22_0.hex", 0x07441000, 0x0000c313, CRC(f6416a86) SHA1(17a26b7800fba83936314fde8cac2191de4042c7))
    ROM_LOAD("ws2812node-LPC1313-0_22_0.hex", 0x0744e000, 0x00005590, CRC(9a090388) SHA1(2f92d8c86bb2c86026cda36ff256b2fcd813cf0e))
ROM_END
CORE_GAMEDEF(supreme, 101, "Supreme (1.01.0)", 2018, "Stern", spike1, 0)
```

All ten authorized archive members were independently decompressed and their
size, CRC32 and SHA1 compared with every row above; SHA256 was also computed
for each payload. The complete portable identities are in
`driver-map-identity.json.txt`. The retained archive is byte-identical to the
user's ROM-library archive. Archive integrity is separate from physical
compatibility, cabinet fitment, switch construction and wiring.

The current catalog has only `supreme_101` for this physical record; there is
no unassigned Supreme clone to map. This completes driver-to-machine mapping,
not author readiness. Spider-Man's firmware remains a separate title and is
not declared interchangeable.

Source attribution: PinMAME contributors, BSD-3-Clause. No ROM bytes are included.
