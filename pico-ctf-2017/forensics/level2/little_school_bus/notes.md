# Little School Bus
(Forensics, Level 2, 70pts)

Obvious hint for LSB.
Using stegsolve, can see some data in the bottom row of the image.

Write a quick Python script to extract it. The only complication is that the bits went in order GBR rather than RGB.
I found this by looking at the bits modulo 24 (i.e. 3 and 8), and spotting which ones were all identical (assuming the key was ASCII).
