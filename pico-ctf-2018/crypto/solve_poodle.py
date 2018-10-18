from pwn import *

p = remote("2018shell2.picoctf.com", 15608)

def encrypt_msg(body, ps):
  p.sendline("E")
  p.recvuntil("Please enter your")
  p.sendline(body)
  p.recvuntil("Anything else?")
  p.sendline(ps)
  p.recvuntil("encrypted: ")
  s = p.recv(1024)
  s = s.decode("hex")

  assert len(s) % 16 == 0
  
  return (s[:16], s[16:])

def check_decryption(msg):
  p.sendline("S")
  p.recvuntil("Please input the encrypted message: ")
  p.sendline(msg.encode("hex"))
  s = p.recv(1024)
  if "Ooops!" in s:
    return False
  if "Cannot reuse IVs" in s:
    assert False
  if "Successful decryption" in s:
    return True

  print "Didn't recognise response!"
  print repr(s)
  assert False

prefix = "Agent,\nGreetings. My situation report is as follows:\n"
flag_prefix = "\nMy agent identifying code is: "
suffix = ".\nDown with the Soviets,\n006\n"

MAC_LENGTH = 20
BLOCK_SIZE = 16

def get_flag_length():
  for i in xrange(16):
    this_len = len(encrypt_msg("", "A" * i)[1])
    next_len = len(encrypt_msg("", "A" * (i + 1))[1])
  
    if this_len != next_len:
      # For i + 1, there are 16 bytes of padding
      bytes_without_flag = len(prefix + flag_prefix + suffix) + (i+1) + 16 + MAC_LENGTH 
      return next_len - bytes_without_flag

def get_next_flag_byte(j, flag_length):
  # Set up body such that the next byte is the last one in the block

  desired_body_len = 16 - (len(prefix) + len(flag_prefix) + j + 1) % 16
  assert (len(prefix) + desired_body_len + len(flag_prefix) + j + 1) % 16 == 0

  desired_ps_len = 16 - (len(prefix) + len(flag_prefix) + len(suffix) + flag_length + desired_body_len + MAC_LENGTH) % 16
  assert (len(prefix) + desired_body_len + len(flag_prefix) + flag_length + len(suffix) + desired_ps_len + MAC_LENGTH) % 16 == 0

  block_with_flag_byte = (len(prefix) + desired_body_len + len(flag_prefix) + j+1) / 16 - 1
  
  possible_bytes = set(xrange(256))

  count = 0
  while len(possible_bytes) != 0:
    (iv, s) = encrypt_msg("A" * desired_body_len, "B" * desired_ps_len)  

    blocks = [s[i:i+16] for i in xrange(0, len(s), 16)]
    # replace last block with [block_with_flag_byte]
    blocks[-1] = blocks[block_with_flag_byte]

    s = "".join(blocks)
    if check_decryption(iv + s):
      # print "Yay, got a byte!"
  
      # print prefix + "A" * desired_body_len + flag_prefix + "F" * flag_length + suffix + "B" * desired_ps_len + "M" * 20 + "P" * 16
      # print repr(s)
      # print block_with_flag_byte

      # This means that the decryption of that chunk, XORed with the byte before was 16
      decrypted_byte = ord(blocks[-2][15]) ^ 16
      return decrypted_byte ^ ord(blocks[block_with_flag_byte - 1][15])

    count += 1 
    if count % 200 == 0: print "Still searchign for byte %d, %d" % (j, count)

flag_length = get_flag_length()
print "[+] Flag length is %d" % flag_length

flag = "picoCTF{g0_@g3nt006!_"
while len(flag) < flag_length:
  flag += chr(get_next_flag_byte(len(flag), flag_length))
  print "Flag so far: %s" % flag
