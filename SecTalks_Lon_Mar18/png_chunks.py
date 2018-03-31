from pwn import *

f = open("now_what.png")
header = f.read(8)

while f:
    size = f.read(4)
    size = u32(size[::-1])
    print size
    print f.read(4)
    f.read(size)
    f.read(4)
