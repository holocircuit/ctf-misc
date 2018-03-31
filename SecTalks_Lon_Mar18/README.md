# README
SecTalks Lon, March 2018. 

The challenges were 6 image files containing flags.

1): Hidden in EXIF data
2): ZIP archive at end of PNG file
3): Pixels represent bits (by taking the sum of RGB values). Column in middle contains flag.
4): LSB stego
5): GIF image with colourmap all set to black. Fix colourmap to see flag.
6): GIF image with coloured squares. Each represents a bit.

Directory contains some scripts I wrote. 
`png_chunks.py` is a script which tries to print out the chunks in a PNG file.
