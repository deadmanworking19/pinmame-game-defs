# Scared Stiff - Midway's development notes on the skull pile's LED eyes

Midway Manufacturing Company's own Scared Stiff page "So just how did we get Scared Stiff anyway?"
(`games/stiff/dev.htm` on the Williams/Bally pinball web site `www.pinball.wms.com`), read on
2026-10-30 from the Internet Archive capture of 1997-01-29
(`https://web.archive.org/web/19970129085638id_/http://www.pinball.wms.com:80/games/stiff/dev.htm`).
The page's HTML header carries the comments `Date: 02/Oct/1996`, `Cameron Silver` and
`Thanks to: Louis Koziarz`, and its footer reads "All text and images (c) Copyright 1996 Midway
Manufacturing Company." The capture is retained outside the repository at
`external:pinmame-review-artifacts/scared-stiff-1996/aux-lamp-sources/pinball-wms-com-games-stiff-dev.wayback-19970129085638.htm`
(SHA-256 `29b617dd43df7139cabc9c01966d1fc44219d3cb705dc2f0d1ba4b1cd990d182`), with the page's
`leds.gif` illustration from the capture of 1997-03-09 beside it
(`pinball-wms-com-games-stiff-leds.wayback-19970309211623.gif`, SHA-256
`ae1370e465d4aac73d2e2bde0b0f96e61a94aadd586028829056a365a51e9547`). A later mirror of the same
page at `https://www.planetarypinball.com/mm5/Williams/games/stiff/dev.htm` carries the same text
(`planetarypinball-williams-games-stiff-dev.htm`, SHA-256
`261164d5573865db6efc3a837bc93fcb358ea599fd76956c80158309d9a6a326`). The directory is pinned by
its external evidence manifest, SHA-256
`292cedb949dc7898378f3573d6c8ce028592d5b02561a56fbe835908a0c6bde4`.

Quotations are verbatim, including the page's spelling ("animtions"); HTML markup is dropped and
line breaks are joined.

## "Pile-o-Skulls"

The section is illustrated by `leds.gif` (alt text "Skulls"), a photograph of the skull pile with
six skulls whose eyes are lit red, between two red candles, on a plaque lettered "DEAD HEADS".

> The skulls (which now sit in the back-right corner of the playfield) originally had red LEDs as
> eyes. Rolling through a skull roll-over lane would light one pair of eyes ("Wake the
> Deadheads!"). Lighting all six pairs of eyes would award the **Return Of The Deadheads** tale.
>
> The LEDs had to be removed because of cost issues, and two flashers were placed behind the
> skulls. The white and blue flashers give the skulls a nice eerie feel, and the Deadhead tale is
> now awarded after only three roll-over lanes instead of six.

## "Break the Deadheads" (first sentence)

> The Pile-o-Skulls looked quite cool with all eyes lit (yes, they would even blink occasionally),
> that we felt something different was needed on the skull roll-over lanes as an alternative to
> the Family Album.

## What this settles

The page is the manufacturer describing the shipped game: the skull pile "now" sits in the
back-right corner, the Deadhead tale "is now awarded after only three roll-over lanes", and two
flashers replace the LED eyes. Those two flashers are the production machine's Skull Flasher Left
and Skull Flasher Right (solenoids 21 and 25), whose placements sit at the playfield's back-right
corner. The page names no part number and no lamp address. Pinned PinMAME's `ss.c` names the
board that carried the LEDs, "a 16 LED Skull driver board assembly A-20781" of "Prototype 0.1",
which the manual still lists as item 7, `A-20781-1 16-LED Skull Driver PCB Assy.`
(`lower-playfield-parts.md`). Which of its sixteen outputs lit which eye, and what the other four
lit, is not stated anywhere retained.
