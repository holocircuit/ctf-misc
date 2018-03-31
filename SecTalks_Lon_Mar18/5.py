from PIL import Image
im = Image.open("now_what.gif")
print im.size
print im.n_frames
print dir(im)

pixels = []
for i in xrange(0, 35, 7):
    l = []
    for j in xrange(0, 434, 7):
        l.append(im.getpixel((j, i)))
    pixels.append(l)

for row in pixels:
    print row

def to_byte(l):
    t = 0
    for x in l:
        t *= 2
        t += x
    return t

t = []
for l in xrange(434/7):
    t += [row[l] for row in pixels]

s = "".join(chr(to_byte(t[i:i+7])) for i in xrange(0, len(t), 7))
print s
