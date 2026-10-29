# Retained VPinMAME library bindings

Source: retained VPinMAME 3.61 `sega.vbs`, SHA-256
`d6e508aac5163fc6d93155e630a1ef5e9c57c3ef3416ada8930dca046daf4924`, and
`core.vbs`, SHA-256
`a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`.
Method: direct read of retained files; transcribed and checked by the curator.

`sega.vbs` lines 31 and 36–37 set slam tilt 55, right flipper button 82 and
left flipper button 84. Its keydown and keyup handlers write those switch
addresses and flip the corresponding table flipper. `core.vbs` lines
2862–2863 set `sLRFlipper = 46` and `sLLFlipper = 48`. Its `vpmMapLights`
routine uses each mapped light's timer interval as the controller address.
