# Theatre of Magic — owner reports that G.I. strings 01 and 02 light the backbox

Four independent repair reports by owners of physical Theatre of Magic machines, read on 2026-10-23.
The pages are retained outside the repository at
`external:pinmame-review-artifacts/theatre-of-magic-1995/field-reports/` (external evidence manifest
SHA-256 `6635a6eb0fdbbaaa157ea486e7f5d98ba1044be84f36cbeebdadf28174686ed5`) and are not redistributed
here. Quotations are verbatim, including the posters' spelling.

The manual prints the G.I. location twice and the two pages disagree (see `general-illumination.md`
and `power-driver-gi-connectors-j119-j120.md`). These reports are what the strings on J120 actually
light on real machines. Each one names the connector, the pin, the wire colour or the string number,
so none rests on a guess about which string is which.

## rec.games.pinball, "TQ: TOM J120 problem-Backbox lights", December 2004

`https://rec.games.pinball.narkive.com/sukqOnGw/tq-tom-j120-problem-backbox-lights`, retained as
`narkive-tq-tom-j120-problem-backbox-lights.html` (SHA-256
`3de39dc02aadd73994f3b41c3384f30c268f0101b9c9bbb58ee6eac1d84c0b87`).

- Jeff, 2004-12-27 05:26:55 UTC: "However, there are 2 strings of lights in my backbox. One row works
  the other doesn't. I traced them to J120. The working side,brown/Brown-white has voltage the
  orange&orange-white wires don't."
- Jeff, 2004-12-29 06:08:24 UTC: "I also put a molex connector in because the 4 wires going to the
  backbox were spliced." In the same post he measured ".1 volts" on "pin 8 which is the white/orange
  wire" of J120, found "CONTINUITY ON FRONT OF BOARD!!! BROKEN TRACER!!! I AM REPAIRING IT NOW." and
  called fuse "110 on the other string Brown and white/brown.Side that works."

Brown/White-Brown and Orange/White-Orange are the wire colours of strings 01 and 02 on J120-1/-7 and
J120-2/-8 (`power-driver-gi-connectors-j119-j120.md`), and F109/F110 are their fuses on the manual's
fuse list (F110 "G.I. #1 Wht-Brn", F109 "G.I. #2 Wht-Org").

## Pinside, "Theatre Of Magic J120 and J121 issue", August 2011

`https://pinside.com/pinball/forum/topic/theatre-of-magic-j120-and-j121-issue`, retained from the
Wayback Machine capture of 2011-09-01 as
`pinside-theatre-of-magic-j120-and-j121-issue.wayback-20110901063215.html` (SHA-256
`a34e5ed2e2c122f27cba20f4aba1ff2a4227e538c1429d94dd75540ed618d640`). All quotations are by the
original poster, Rick471.

- Post 1: "My backbox doesnt light up all the way and my flashers are not working at all." He found a
  four-wire plug on J121 and a six-wire plug on J120, concluded "J120 and J121 were switched by
  someone incorrectly. (Maybe I am wrong,,,)", and swapped them so that J121 carries the six wires the
  manual lists for it.
- After swapping: "Looks like J121 is working fine then. I have strings 3-4-5 working perfectly. J120
  is the one thats toast then. Strings 1-2 are not working. That would be the burned #8 pin location."
- After replacing the plug: "The string that is out definitely powers the upper half of the backbox
  and who knows what else."
- After jumpering the burnt trace from J120-8 to its fuse: "everything is working perfectly!"

## Pinside, "No backbox GI on Theater of Magic" (topic 196358), August 2017

`https://pinside.com/pinball/forum/topic/no-backbox-gi-on-theater-of-magic`, retained as
`pinside-no-backbox-gi-on-theater-of-magic.html` (SHA-256
`4a2c9cdab91f1208d0d8df940644b4625e364fc1b77783b5a08c343a1404cfb7`). This is the most direct of the
four: the playfield G.I. kept working while both strings on J120 were dead.

- mfishell, 2017-08-23 14:04:31 UTC: "Everything works and plays great except the backbox GI doesn't
  light." "I opened it up and found J120 had the usual burned pins." "F109 & F110 fuses are both
  good." "When I powered up the machine, everything works but still, no back box GI. Ran through the
  tests for GI and Orange/White and Brown/White are the only two that don't work."
- schudel5, 2017-08-23 15:10:32 UTC, lists "the wiring for J120 and J121" on ToM: J120-1 brown,
  J120-2 orange, J120-7 white/brown, J120-8 white/orange; J121-3 yellow, J121-5 green, J121-6 violet,
  J121-9 white/yellow, J121-10 white/green, J121-11 white/violet; every other pin n/a, pin 4 the key
  on both. This is the manual's connector list pin for pin.

## Restoration blog, theatreofmagic.blogspot.com, "Day 1", October 2012

`http://theatreofmagic.blogspot.com/2012/10/day-1.html`, published 2012-10-28, retained as the blog's
JSON feed `theatreofmagic-blogspot-feed.json` (SHA-256
`6e73aecd246f2241c9df9945f297c463885647297df33fc653073e6d86721b8b`), since the post page itself
renders its text in the browser.

- "I noticed that half of the general illumination (GI) was off in the backbox and when you look at
  the picture of the connector J120 you will see why."
- Later in the same post the restorer replaced the burnt J120 header and plug, and "it all worked
  perfectly first time".
- On the playfield G.I.: "Because the SMD type #44 LEDs have no glass dome over them, it makes them
  quite hard to get in the holder"; the holder in question was "on the back upright of the
  playfield".

## Reading

Strings 01 and 02, the Brown and Orange strings on J120, are the backbox insert-board strings: two
rows of backbox lamps, one of them "the upper half of the backbox". On one machine both were dead
and only the backbox was dark. Strings 03-05 on J121 kept the playfield lit in each case. The
playfield G.I. sockets take #44 bulbs. All of this matches the Solenoid/Flasher Table's G.I. rows,
which print J120 and #555 under Backbox and J121 and #44 under Playfield. The Power Driver Board
connector list's destination words ("to playfield" on J120, "to insert" on J121) do not match these
machines.
