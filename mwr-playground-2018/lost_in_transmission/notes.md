# Lost In Transmission
A WAV file. The instructions are:

```
A shady underground group is sending digital radio messages to communicate between cells. We need to obtain some of their code words to help our agents infiltrate the cells.

We have provided you with a broad band audio recording of a section of the radio spectrum we believe they are using. This is an 8 kHz wide band starting at 14.013715MHz. They communicate by sending a series of short messages in different digital modes, usually including details of the next transmission and where to tune in for it. Fake transmissions are also used to slow down our analysis, and there may be other unrelated transmissions in the band too.

We believe there are 3 code words to be found in this recording. Follow the trail and provide us the code words and we will see that you are compensated for your time in points.   Our contact gave us this information to start you off: begin at offset 2000hz, BPSK-31.
```

## 35s - 40s
From the spectogram (in Audacity), this looks like DMTF tones.
Putting it through http://dialabc.com/sound/detect/index.html, decodes as *8444684891439*. Not sure what this means. 
Update: After googling, apparently it's the song "Auld Lang Syne" in dial tones...

## 51s - 1m11s
Another string of DMTF tones. Decodes as another string of numbers.
*33155344444211334332244343243433123543254423421515343315543445421334141552344214244343441124333115434*

## Part 2
Used flDigi to decode the radio tones. This gives a "path" through the audio, saying where the next frequency is. See *radio.txt* for details.
Got the code for the second part.

Continued following this through, and got to the message `SCOPE YOUR SURROUNDINGS`. Not sure what this means - presumably this is for the last part.
This ends just before the "last" section of the audio.

There are a few other transmissions in the audio that I found. They mostly seem unrelated.

## Part 3
Noticed the last section of the audio has left/right out of sync, unlike the rest.
Tried plotting a Lissajous curve thing (left against right). It produces an interesting pattern between samples 3400000 - 350000. There's a circle, as well as a sort of grid-pattern it produces.
Update: I realised I plotted this wrong. A goinometer actually plots them against each other but at an offset. 
Still produces interesting shapes, but I can't figure out what this is.
