from PIL import Image
im = Image.open("now_what.png")
print im.size

l = []

"""
for y in xrange(100):
  g_bits = [i for i,x in enumerate([im.getpixel((x, y))[2] for x in xrange(0, 400)]) if x == 0]
  print g_bits

for y in xrange(400):
  g_bits = [im.getpixel((227, y))]
  print g_bits
"""

def process_pixel(pixel):
  return chr(pixel[0] + pixel[1] + pixel[2])

d = {}
for x in xrange(400):
  row = [process_pixel(im.getpixel((x, y))) for y in xrange(400)]
  print "".join(row)
