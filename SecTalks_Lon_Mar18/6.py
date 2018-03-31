from pwn import *

f = open("now_what.gif")
header = f.read(6)
print "Header:", header
print "Width:", repr(u16(f.read(2)))
print "Height:", repr(u16(f.read(2)))

packed_fields = f.read(1)
print "Packed fields:", repr(packed_fields)

background_colour_index = ord(f.read(1))
pixel_aspect_ratio = ord(f.read(1))
print "Background Colour Index", background_colour_index
print "Pixel Aspect Ratio", pixel_aspect_ratio

print repr(f.read(6))
print repr(f.read(6))

f.seek(0)
s = f.read(16)
s += "\xff\xff\xff"
f.read(3)
s += f.read()
open("out.gif","wb").write(s)

