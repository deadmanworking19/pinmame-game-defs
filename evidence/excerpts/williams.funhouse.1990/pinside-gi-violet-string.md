# FunHouse — owner trace of the violet G.I. string (Pinside)

Source: Pinside forum topic "Funhouse G.I. Problem (SOLVED)" (Tech: Alpha-numeric), https://pinside.com/pinball/forum/topic/funhouse-gi-problem, posts #1-#16, read 2026-10-23. Quoted passages are the posters' own words; only the parts about the G.I. string are transcribed.

| Post | Poster | Text |
| --- | --- | --- |
| #1 | provato (owner) | "Problem: front playfield G.I. Strings (white-violet) burn the 5v fuse (F106) every time I turn the machine on." |
| #1 | provato | "until Suddenly while playing the front playfield G.I. (Including coin door) turned off. I opened the backbox and found out that f106 tripped." |
| #1 | provato | "I disconnected J119 & J121 which contained the white-violet G.I. Strings and now I don't have any voltage across f106 edges! [...] maybe the triac Q12 shorted out??" |
| #12 | ChrisHibler | "you're going to need to track that violet/white-violet GI string. Where you look depends on whether you have the backbox or playfield GI connector attached to J121. Fat wires go to the PF. Skinny wires go to the head lamp insert panel." |
| #13 | Lermods | "There are gi bulbs under the apron, check that they aren't shorting." |
| #16 | provato | "A lamp socket was shorted (its two legs were touching each other...). After I bent the legs outwards, f106 stopped tripping and all lights in the white-violet string are now lit!" |

The owner's machine puts the front-playfield G.I. and the coin-door lamps on the violet string: white-violet return, J119 (cabinet) and J121, fuse F106, triac Q12. The L-9 ROM's T.6 test prints the same wires, fuse and driver for public G.I. 4, FRONT PLAYFIELD (`evidence/runtime/wpc-alpha/funhouse-fh_l9-gi-test.json`). Post #12 notes that the two G.I. headers carry identical pinouts, so which of J120 and J121 holds the playfield harness is a fact of the harness, not of the board. Post #13 places G.I. bulbs under the apron. The retained table drives two render lights there, `Bottom_GI_32` and `Bottom_GI_39`, in its front-playfield group, but neither it nor its 2.0c revision models a bulb at them, so the record does not place the apron bulbs.
