# Godzilla (Sega, 1998)

Coverage: **partial**. IPDB capture identifies machine 4443, model 40; the
manual and retained VPW table establish the production playfield and I/O.
PinMAME uses the same Whitestar initialization for all three drivers. Production
1.00 and 2.05 use the same physical definition; prototype 0.90 physical
compatibility is unknown. Fast-flip output 15 is configured for the root
`godzilla` driver but not the two clone names; this is emulator behavior.

The four-ball trough has three roller contacts, lower VUK opto 14 and upper
stacking opto 15. The manual's receiver circuit is open in a clear beam and
closed when blocked. VPW starts with 11–14 active and pulses 15 during the
serve. Output 1 kicks the ball to the shooter lane, and 2 launches it. Sensors
change through ball movement; a direct coil-to-sensor relationship is not
asserted.

The Godzilla ramp diverter is output 17. The manual routes a hard shot to the
left return with the diverter up and through the mouth with it down. The table
exchanges two collision walls, but their flag has not been equated with the
physical up state. Three captive balls occupy separate lanes; hits on the outer
balls move the top center ball. Four separate magnets use outputs 3, 4, 5 and
14, with no established feedback sensors. Output 6 drives a cabinet shaker.
VPW timing is table tuning, not a measured hardware parameter.

Three retained fresh-state gameplay runs exercise 2.05, 1.00 and 0.90 with the
pinned native library. Every run responds to Start with trough output 1 and to
Launch with output 2. Switches 49/50/51 fire bumper outputs 9/10/11, 59/62 fire
slings 12/13, and cabinet inputs 82/84 produce the corresponding 45/46 and
47/48 flipper pairs. Other simultaneous flash and shaker outputs are recorded
as incidental responses, without inventing direct electrical relationships.
All three runs publish optional coin-meter output 24 on a coin; this does not
prove a meter is fitted. Only 2.05 publishes synthetic fast-flip output 15,
consistent with the driver-name test in `se.c`. Compact per-driver evidence
under `evidence/runtime/whitestar/godzilla-*-gameplay.json` records exact ROM,
library, scenario and raw-trace hashes. The host supplies ball movements and
switch stimuli; input readback is not ROM evidence.

The factory flipper diagram labels each cabinet button normally open and each
physical EOS normally closed. It describes one 23-1100 coil per flipper, a
50 V supply, a 40 ms kick and 1 ms pulses every 12 ms for hold. An EOS closure
after foldback calls for another 40 ms kick. Those are factory descriptions;
PinMAME's public 81 and 83 are synthesized EOS inputs, and do not establish
physical contact construction on their own.

Coils 21–23 and lamp 40 are optional UK-only hardware; the European token
dispenser 8 and coin meter 24 are optional. The manual's printed wiring and
parts are preserved in the excerpts. Some small chart captions and part numbers
are undeciphered and the respective excerpts remain candidate evidence. Switch
contact construction is recorded where the trough circuit or a script active
level and the Whitestar read path establish it; the remaining contact
polarities need an individual source-backed pass.

G.I. 0 is one relay over four fused circuits. The manual's nominal counts total
38 bulbs, including two in the coin door; it warns that production quantities
may vary. No retained evidence maps every physical GI socket. The spatial
report records observed factory drawing measurements and unresolved placement.
UK post mechanisms, their geometry and causal behavior remain incomplete.

Sources are recorded in the machine definition. The retained manual, script,
VPX table, IPDB capture, and source revisions are external or hash-pinned; no
whole manual, community table, or ROM is redistributed here.
