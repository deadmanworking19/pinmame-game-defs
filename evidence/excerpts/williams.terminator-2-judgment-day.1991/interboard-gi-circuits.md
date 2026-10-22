# Terminator 2: Judgment Day - Interboard Wiring, general illumination circuits

Source: `Terminator 2 Judgement Day Operations Manual.pdf` (ARC ARC retained source SHA-256 `8540d654b39c58ad3b19ece0f42eb1dfdb8460d249e9480f8906385c8ecdb16b`), PDF page 115, printed page 3-9, headed `Interboard Wiring`. The crop is the `General Illumination Circuits` table at the top of the page. Transcribed manually from the image-only scan and checked against a native-resolution render of the page.

Header `Connectors from Power Driver Board`, columns `Wire Color` | `Function` | `To Playfield` | `To Cabinet` | `To Insert` | `Transistor`. A blank cell is `(blank)`.

| Wire Color | Function | To Playfield | To Cabinet | To Insert | Transistor |
| --- | --- | --- | --- | --- | --- |
| Green | Feed 1 | J121-5 | (blank) | J120-2 | Q12 |
| Violet | Feed 2 | J121-6 | J119-3 | (blank) | Q10 |
| Brown | Feed 3 | (blank) | (blank) | J120-1 | Q18 |
| Yellow | Feed 4 | J121-3 | (blank) | (blank) | Q14 |
| Orange | Feed 5 | (blank) | (blank) | (blank) | Q16 |
| White/Green | Return 1 | J121-10 | (blank) | J120-8 | F7 |
| White/Violet | Return 2 | J121-11 | J119-1 | (blank) | F6 |
| White/Brown | Return 3 | (blank) | (blank) | J120-7 | F10 |
| White/Yellow | Return 4 | J121-9 | (blank) | (blank) | F8 |
| White/Orange | Return 5 | (blank) | (blank) | (blank) | F9 |

A blank line separates the five feeds from the five returns. The return rows print fuse designators (`F7`, `F6`, `F10`, `F8`, `F9`) in the `Transistor` column.

As printed, the Orange feed and the White/Orange return carry no connector at all, while the Green row carries both a playfield pin (J121-5, return J121-10) and an insert pin (J120-2, return J120-8). The 1-28 and 2-38 solenoid tables print J120-8 on the `Wht-Orn` row (`04 Not Used`). The L-8 ROM's T.6 test names the orange string BOTTOM INSERT and the green string CPU STRING (`evidence/runtime/wpc-alpha/terminator-2-t2_l8-gi-test.json`), which places the insert pins J120-2/J120-8 on the orange string and the playfield pins J121-5/J121-10 on the green one; this table's feed numbering and transistor column do not follow the string numbers that the ROM and the 2-39 list use.
