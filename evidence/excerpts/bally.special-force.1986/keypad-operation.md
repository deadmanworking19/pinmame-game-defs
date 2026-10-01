# Bally Midway Special Force (game no. 0E47) — Tailoring and Testing: Operation

Source: `Bally_1986_Special_Force_Manual.pdf`, PDF page 8, printed page 1-2, section `III. TAILORING & TESTING THE
GAME`. Transcribed by hand from a render of that page at its native 299 ppi. The `OPERATION` subsection is transcribed
in full; the introduction above it and `STEPPING THROUGH` below it are not. The printed bold `Note:` is marked `**`,
and the printed line breaks are not kept.

## OPERATION

The keyboard is located on the right inside wall of the game near the front door. The cable is long enough, so that
once the keyboard is removed, it may be operated from outside the machine. **Note:** The keypad is mounted with a 1/4"
Hex screw for shipping purposes.

1. Press the Test button located on the front door. This tells the processor to do the following;
   A. It checks the switches wired in parallel with the keypad. If any switches are closed the game automatically
   jumps to Stuck Switch Test and displays a stuck switch message.
   B. If there were no stuck switches you will be welcomed with "Bally's Testing is Easy As ABC."
2. When appropriate heading appears on backglass display, press "Enter" on keypad once.
   Within each heading, there are categories which are operator selectable. When the appropriate category appears on
   the backglass display, press "Enter" once to access that category.
3. Set your registers with keypad.
4. Press "Enter" again to advance to next category setting. Press "CLR" to re-start Self-Test. Press "Game" to
   lock-in option settings.

The manual does not say which keypad key shares which matrix position. PinMAME's `by6803.c` `SWITCH_UPDATE(by6803)`
(with `BY6803_COMPORTS` in `by6803.h`) and the VPinMAME `6803.vbs` script library both put keypad 0 on public 2,
Enter on 1, Clear on 3, Game (PinMAME's port names it Cancel) on 4, A on 12, 1-3 on 11-9 (shared with the coin switches), 4-6 on 19-17, B on 20, 7-9 on
27-25 and C on 28.
