import base64

l = [
    [109, 179, 244, 231],
    [190, 224, 157, 69],
    [42, 246, 228, 204],
    [64, 241, 4, 252],
    ]

xor_array = []
for i in xrange(3, -1, -1):
    for j in xrange(i, 4):
        xor_array.append(l[i][j])

for i in xrange(4):
    for j in xrange(i, -1, -1):
        xor_array.append(l[i][j])

def decrypt(s):
    s = base64.b64decode(s)
    return "".join(chr(ord(c) ^ xor_array[i % len(xor_array)]) for i, c in enumerate(s))

print decrypt("q5allPgJBN2R")
print decrypt("uYq4he9lHdKHlBqPzIDWXpMkhymZk/bA")
print decrypt("tYqvj+8gDsfUlwyTzZOZWJgl")
print decrypt("mtT02Pl1D9bZ0luE2MnCGp023HjO1//NqHwL1Q==")
print decrypt("2NatxKx0SYG6hViK2ZfEQqpWxQHJkYKQzTQZ1pGgCI/00MFosV6rAqiFltX1JCGKlaMC1Y2uwEmIcLR2")
