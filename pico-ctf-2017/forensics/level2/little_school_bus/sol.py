from PIL import Image

im = Image.open("littleschoolbus.bmp")

last_row = [im.getpixel((i, im.height-1)) for i in xrange(0, im.width)]
bits = [x%2 for l in last_row for x in l[::-1]]

def print_slide(n):
    for i in xrange(n):
        print i, bits[i::n]

def bits_to_byte(bits):
    result = 0
    for i in bits:
        result *= 2
        result += i
    return result

print_slide(24)
data = [bits_to_byte(bits[8*i:8*i+8]) for i in xrange(0, len(bits)/8)]
print "".join(chr(c) for c in data)
