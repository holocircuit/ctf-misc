from PIL import Image
im = Image.open("now_what.png")
print im.size

l = []

def process_pixel(pixel):
  return chr(pixel[0] + pixel[1] + pixel[2])

d = {}
for x in xrange(400):
  row = [process_pixel(im.getpixel((x, y))) for y in xrange(400)]
  print "".join(row)
