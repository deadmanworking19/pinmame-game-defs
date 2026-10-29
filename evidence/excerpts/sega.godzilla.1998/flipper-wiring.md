# Flipper circuit and technical overview

Source: Godzilla manual PDF page 92, printed page 86, `2-Flipper Circuit Wiring
Diagram`; manual SHA-256
`fc71e6584b2a8ad715100f94b5d4d690b0cd3864cd9abd6746c2441ad4d6c1c5`.
Method: curator visually inspected the native-resolution
render. The diagram labels both cabinet flipper switches N.O. and both physical
end-of-stroke switches N.C. It shows one 23-1100 coil per flipper and 50 V DC
for both kick and hold. The technical overview describes a 40 ms kick followed
by 1 ms pulses every 12 ms during hold. The physical EOS opens about 1/16 inch
after energizing; foldback closes it and the CPU reapplies a 40 ms pulse.
These are the manual's physical-system descriptions, not measured VPW timing
and not the construction of the emulator's synthesized EOS bits.
