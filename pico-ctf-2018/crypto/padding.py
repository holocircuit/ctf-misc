from pwn import *

def check_padding(iv, block):
  assert len(iv) == 16
  assert len(block) == 16

  while True:
    try:
      p = remote("2018shell2.picoctf.com", 4966)
      p.recvuntil("What is your cookie?")
 
      p.send(iv.encode("hex") + block.encode("hex") + "\n")

      s = p.recvall(timeout=1)
      #print repr(s)
      if "invalid padding" in s:
        return False
      return True
    except EOFError:
      print "Got EOF error, trying again..."
    except pwnlib.exception.PwnlibException:
      print "Got EOF error, trying again..."
  
def decrypt_block(block, known_suffix):
  target_byte = -1 - len(known_suffix)
 
  padding_byte = -1 * target_byte

  # We want to set up the IV such that the last (target_byte-1) bytes of the block are equal to the padding_byte
  iv = [0] * 16
 
  for i in xrange(-1, target_byte, -1):
    iv[i] = ord(known_suffix[i]) ^ padding_byte

  for b in xrange(256):
    iv[target_byte] = b
    if check_padding("".join(chr(c) for c in iv), block):
      # we got a match!
      actual_byte = b ^ padding_byte 
      return chr(actual_byte) + known_suffix

  return None

def decrypt_block_actual(block):
  known_suffix = ""
  while len(known_suffix) != 16:
    known_suffix = decrypt_block(block, known_suffix)
  return known_suffix

target = '{"username" : "holly", "is_admin" : "true", "expires" : "2018-12-12"}'
target += "\x0b" * 11

blocks = [target[i:i+16] for i in xrange(0, 80, 16)]
print blocks

cookie = "\x00" * 16
for target_block in blocks[::-1]:
  print "Finding for target block %s" % repr(target_block)
  # We want the *next* block to XOR with the decryption of *this* block, to give what we wanted
  last_cookie_block = cookie[:16]
  decrypted_block = decrypt_block_actual(last_cookie_block)

  xored = "".join(chr(ord(c) ^ ord(d)) for c, d in zip(decrypted_block, target_block))
  cookie = xored + cookie

