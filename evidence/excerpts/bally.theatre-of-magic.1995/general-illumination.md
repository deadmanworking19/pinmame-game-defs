# Theatre of Magic — General Illumination rows of the Solenoid/Flasher Table

Transcribed from `Theatre_of_Magic_OPS.pdf`, PDF page 2 (the unnumbered front-matter copy of the
Solenoid/Flasher Table), General Illumination block directly below the solenoid rows. The same block
is printed identically on printed page 2-44 (PDF page 120) and printed page 3-5 (PDF page 127). The committed crop shows only the
five G.I. rows; the column headers are in the crop of `solenoid-flasher-wiring.md`. Verified against
a native-resolution render of the page, not the OCR text layer.

Column headers, as printed at the top of the table: `Voltage Connections` (sub-columns `Playfield`,
`Backbox`, `Cabinet`), `Drive Xister`, `Drive Connections` (sub-columns `Playfield`, `Backbox`,
`Cabinet`), `Drive Wire Color`, `Solenoid Part number / Flashlamp Type` (sub-columns `Playfield`,
`Backbox`). Blank cells are printed blank.

| No. | Function | Type | Volt. Playfield | Volt. Backbox | Volt. Cabinet | Xister | Drive Playfield | Drive Backbox | Drive Cabinet | Wire | Lamp Playfield | Lamp Backbox |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | STRING 1 | G.I. | (blank) | J120-1 | (blank) | Q18 | (blank) | J120-7 | (blank) | Wht-Brn | (blank) | #555 |
| 02 | STRING 2 | G.I. | (blank) | J120-2 | (blank) | Q10 | (blank) | J120-8 | (blank) | Wht-Org | (blank) | #555 |
| 03 | STRING 3 | G.I. | J121-3 | (blank) | (blank) | Q14 | J121-9 | (blank) | (blank) | Wht-Yel | #44 | (blank) |
| 04 | STRING 4 | G.I. | J121-5 | (blank) | (blank) | Q16 | J121-10 | (blank) | (blank) | Wht-Grn | #44 | (blank) |
| 05 | STRING 5 | G.I. | J121-6 | (blank) | (blank) | Q12 | J121-11 | (blank) | (blank) | Wht-Vio | #44 | (blank) |

Footnote on the page: `J1xx=Power Driver Board; J9xx=Fliptronic II Board; 24-6549=#44 bulb;
24-8704=#89 bulb; 24-8768=#555 bulb; 24-8802=#906 bulb`.

## Which location columns are right

The game's own Power Driver Board connector list (printed 3-27, PDF page 149; see
`power-driver-gi-connectors-j119-j120.md` and `power-driver-gi-connectors-j121.md`) prints the same
pins with the opposite destination words: J120-1/-2/-7/-8 "to playfield" and J121-3/-5/-6/-9/-10/-11
"to insert". One of the two pages is wrong, and the manual cannot say which. Owners of real machines
can. Four independent repair reports (`gi-backbox-field-reports.md`) trace a dark backbox to J120,
its Brown and Orange strings (01 and 02) or its fuses F109/F110. On one machine both strings were
dead and the playfield G.I. kept working. Four more threads (`gi-playfield-field-reports.md`) are
about the playfield strings, and two of them put string 04 on the left side of the playfield and
string 05 on the right. So this table's location columns are right and
the connector list's destination words are the misprint, for the G.I. pins only. Its pin numbers and
wire colours agree with this table, and its flashlamp rows agree with this table's columns (J122 "to
playfield flashlamps", J124 "to insert flashlamp").

The bulbs agree too. Owners name #44 as the playfield G.I. bulb ("GI 44s/89s", "SMD type #44 LEDs"
in a playfield holder), and this table prints #44 for strings 03-05 and #555 for 01-02. The printed
bulb column names one bulb per string. The jet bumpers are a known exception: their assembly fits a
#555 wedge (printed 2-20, `jet-bumper-assembly.md`) although they are playfield G.I.

The table also prints each string's return pin (J120-1 "Brown Return G.I." on the connector list)
under Voltage Connections and its 6.8VAC supply pin (J120-7 "White-Brown 6.8VAC") under Drive
Connections. The printed G.I. circuit (printed 3-10, PDF page 132) puts the triac on the return side.
The definition therefore records the return pin as each string's control connection and the 6.8VAC
pin as its power connection.

The retained known-working script's `UpdateGI` (lines 1658-1716) dims playfield Light collections
for cases 0-3. That is not this machine's split. Cases 0 and 1 are the backbox strings 01 and 02,
and they drive the playfield collections `GITop`/`GIBumpers` and `GILeft`. Cases 2 and 3 are
playfield strings 03 and 04, but they drive the right-hand collections `GIRight` and `GIMiddle`,
while owners put string 04 on the left side. There is no case 4 for string 05, the right side. This
is a defect in the table's lighting script, not a disagreement about the machine. The definition
records it on the G.I. devices and does not take bulb-to-string membership from it.
