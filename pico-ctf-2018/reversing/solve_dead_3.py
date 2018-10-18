# 0x004007a0
# 0x0040079b

l = []

for i in xrange(0, 5):
    l.append(i * i + 0x2345)

x = 0x18f4b

for i in xrange(5, x + 1):
    y = l[i-1] - l[i-2] + l[i-3] - l[i-4]
    y += (l[i-5] * 0x1234)
    y %= (2**32)
    l.append(y)


print "\n".join(hex(i) for i in l)
