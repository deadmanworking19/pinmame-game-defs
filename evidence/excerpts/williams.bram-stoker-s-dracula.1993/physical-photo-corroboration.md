# Bram Stoker's Dracula — 2026-10-23 physical photo corroboration

Physical photographs of production machines, one owner's description and a reproduction of the
Williams tech chart, used to corroborate the identity and count of devices whose coordinates this
definition measures on the factory location drawings, the playfield art at the Mist Magnet path, and the
playfield back panel, and to check flasher 19's bulb count. They supply no coordinate: every photograph
is a perspective view.

The files stay external, under the working root's `review-artifacts/dracula/physical-photos/`, pinned by
that folder's canonical manifest (`manifest.json`, SHA-256
`7a262bfa8950e235574621c58d2cd725ee52a608644a31c5cd533aab60e6ed7a`). Copyright in each photograph and in
the web page stays with its author, in the chart with Williams and its reproducer, and in the machine
artwork with WMS Industries; rights and license are `NOASSERTION`. This excerpt records only what the
files show, quotes two sentences of the page and one row of the chart; it does not copy any photograph.

## Files

| File | Source | SHA-256 |
| --- | --- | --- |
| `ipdb-3072/ipdb-3072-image-8.jpg` | IPDB machine 3072, picture 12459 "Upper Playfield" [Robert Winter], `https://www.ipdb.org/images/3072/image-8.jpg` | `16329e2b78218da2ef5be7d2d9a0b51541df06a2bd0198327938c5a9ad63912b` |
| `ipdb-3072/ipdb-3072-image-7.jpg` | IPDB machine 3072, picture 12458 "Middle Playfield" [Robert Winter], `https://www.ipdb.org/images/3072/image-7.jpg` | `8f986bf1dc3170cfdb0da68ecb5541ddc2fee431a295c8b25825e0f49d0c6c62` |
| `ipdb-3072/ipdb-3072-image-17.jpg` | IPDB machine 3072, picture 35879 "Playfield - Plastic Covers Removed" [Philippe Thibault], `https://www.ipdb.org/images/3072/image-17.jpg` | `fb423674ad460a5c13884fb68395856ed9105cc1b521b89191e1c25eeed6e550` |
| `web/davidhouchin-posts-bsd.html` | David Houchin, "Bram Stoker's Dracula Pinball", posted 2020-07-10, `https://davidhouchin.com/posts/bsd/`, fetched 2026-10-23 | `7a4a9b8b2cf4b9af9b6b70a598aa5ce08101a84d8b7a0796da01961d7d3fa27e` |
| `web/Williams_Bram_Stokers_Dracula_Tech_Chart.pdf` | Inkochnito's reproduction (Martin Reynolds, 2016, born-digital) of the Williams tech chart, `https://www.pinballrebel.com/pinball/cards/Tech_Charts/Williams_Bram_Stokers_Dracula_Tech_Chart.pdf`, fetched 2026-10-23 | `8f367fc95c09c80da90344244d72736b27616714ad2c4426f8cd9fa0e28a6b62` |

The three photographs were fetched as raw bytes from Wayback Machine captures of those IPDB URLs.

## What they show

- **The coffin flasher domes (flasher 17).** Picture 12459 shows the coffin in the upper right of the
  playfield, with the Dracula figure lying in it, and a raised head piece at its rear
  end carrying a cross between two blue flasher domes. Those are the two sockets where the two arrowed
  callouts 17 of the solenoid drawing (printed 2-45) end, on either side of the coffin; the third callout
  17 stands in the top right corner, where the retained table's F17_Dome is.
- **The playfield back panel (lamps 58 and 61-63).** Picture 12459 also shows, behind the top of the
  ramps, an upright panel at the rear edge of the playfield whose plastic carries red and purple art and
  the yellow letters `SKILL S`, the rest hidden by the ramp in front of it. That is the A-16399 back panel
  of printed page 2-39, whose 3-lamp PCB carries the L./M./R. Skill lamps 61-63. Its insert windows are
  not distinguishable in the photograph.
- **The mist art (lamp 53 and the Mist Magnet).** Pictures 12458 and 35879 show the green mist art running
  diagonally across the middle of the playfield, from the lower left through the BRAM STOKER'S DRACULA logo
  up towards the right side, the path the Mist Magnet carrier runs under. Neither shows an arrow-shaped
  insert at the left end of that path, so the small arrow beside balloon 53 on the lamp drawing (printed
  2-44) is a drawing mark, not an insert. The thirteen small round inserts of the drawn row are not
  distinguishable in these photographs.
- **The Mist Magnet carrier light (lamp 53).** The owner's page describes the mechanism from the machine
  in hand. Quoted as printed:

  > It should also be noted that there are actually a series of inserts below the green mist line, which
  > allows a light mounted on the magnet assembly to shine through, giving the appearance of a light
  > traveling across the mist.

  > The magnet is stopped at it’s limits by two switches, 81 and 83, (Magnet Left and Magnet Right) that
  > indicate the magnet has reached the end of it’s travel.

  This agrees with the magnet-carrier drawing (printed 2-27), whose assembly carries a light socket and
  bulb (item 7) beside the coil, and with the lamp drawing's row of inserts along the mist path. The page
  is an owner's account, a lead rather than an authority; it settles nothing the manual does not already
  show.
- **Flasher 19's playfield bulb count (not settled).** The tech chart's Solenoid/Flasher Table, whose
  Flashlamp Type columns are headed `Playfield` and `Insert`, prints the row as `pdftotext -layout`
  extracts it from the text layer, up to its last flashlamp cell (the rest of that text line belongs to
  the chart's switch matrix):

      19 3-BANK / HOUSE FLASHER            Flasher   J107-6 J106-5            Q38 J126-3 J125-3                     BLK-ORG       #89(1)       #906(1)

  It counts one #89 on the playfield, as the manual's 3-8 table does, and may be copied from it. Its
  other flasher rows match the callouts the 2-45 drawing prints (#906(3) for 17, #906(1) for 18,
  #89(1) #906(1) for 20 on the playfield, #89(2) for 21, one bulb each for 22, 23 and 24); only row 19
  counts fewer playfield bulbs than the drawing's two callouts 19. None of the photographs shows what
  drives the bulbs behind either 3-bank.
