def int_to_bits(x, bits):
  l = []
  for b in xrange(bits):
    l.append(x % 2)
    x /= 2
  l = l[::-1]
  return l

def bits_to_int(l):
  x = 0
  for i in l:
    x *= 2
    x += i
  return x

def int_to_dwords(x):
  l = []
  for i in xrange(4):
    l.append(x % 256)
    x /= 256
  return l
  
def rotate_right(x, i, bits):
  l = int_to_bits(x, bits)
  return l[-i:] + l[:-i]

def rotate_left(x, i, bits):
  l = int_to_bits(x, bits)
  return l[i:] + l[:i]
  
def encrypt_chars(c0, c1, c2, c3):
  c0 ^= 0xde

  x = c1*256 + c0
  x = int_to_dwords(bits_to_int(rotate_right(x, 13, 16)))
   
  c0 = x[0]
  c1 = x[1]
  
  x = c3*(256**3) + c2*(256**2) + c1*(256) + c0
  x = int_to_dwords(bits_to_int(rotate_left(x, 15, 32)))

  c0 = x[0]
  c1 = x[1]
  c2 = x[2]
  c3 = x[3]

  return (c0, c1, c2, c3)

def decrypt_chars(c0, c1, c2, c3):
  x = c3*(256**3) + c2*(256**2) + c1*(256) + c0
  x = int_to_dwords(bits_to_int(rotate_left(x, 17, 32)))
  c0 = x[0]
  c1 = x[1]
  c2 = x[2]
  c3 = x[3]

  x = c1*256 + c0
  x = int_to_dwords(bits_to_int(rotate_right(x, 3, 16)))
   
  c0 = x[0]
  c1 = x[1]

  c0 ^= 0xde
  return (c0, c1, c2, c3)

known_text = list(map(ord, "picoCTF{"))
for i in xrange(8 - 3):
  l = encrypt_chars(known_text[i], known_text[i+1], known_text[i+2], known_text[i+3])
  decrypted = decrypt_chars(l[0], l[1], l[2], l[3])

  print decrypted

  for j in xrange(4):
    assert known_text[i+j] == decrypted[j]

  for j in xrange(4):
    print i, j
    known_text[i+j] = l[j]
  #print known_text

s = "b1 d3 32 4c fc e6 ef 5e ed e4 66 cd 57 f5 e1 7f cd 7f 55 f6 e9 64 e7 c9 7f 75 e9 54 e6 4d f7 79 fc fc 51 71 f9 3e 18 d9".split(" ")
s = [int(c, 16) for c in s]

print s

for i in xrange(len(s) - 4, -1, -1):
  l = decrypt_chars(s[i], s[i+1], s[i+2], s[i+3])
  for j in xrange(4):
    s[i+j] = l[j]

print "".join(map(chr, s))
