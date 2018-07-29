import socket
import base64
import struct
import binascii
import random
from hashlib import sha256

def recv_until(sock, s):
    t = b""
    while s not in t:
        t += sock.recv(1024)
    return t

sock = socket.create_connection(("crypto-02.v7frkwrfyhsjtbpfcppnu.ctfz.one", 1337))
print(repr(recv_until(sock, b"You can sign")))

def sign(msg):
    msg = b"sign:%s" % base64.b64encode(msg)

    sock.send(msg + b"\n")
    result = recv_until(sock, b"\n")
    checksummed_msg = result.split(b",")[0]
    signature       = result.split(b",")[1]

    msg = base64.b64decode(checksummed_msg)
    sig = base64.b64decode(signature)

    checksum = msg[-4:]
    return (msg, checksum, sig)

def execute(msg_with_checksum, sig):
    msg = base64.b64encode(msg_with_checksum)
    sig = base64.b64encode(sig)

    msg = b"execute_command:%s,%s" % (msg, sig)
    sock.send(msg + b"\n")
    result = recv_until(sock, b"\n")

    return result

def get_signing_dictionary():
    msg, checksum, sig = sign(b"\x00" * 32)
    d = {(0, i) : sig[32*i:32*i+32] for i in range(0, 32)}

    for b in range(1, 256):
        for i in range(32):
            d[(b, i)] = sha256(d[(b-1, i)]).digest()

    return d

def get_checksum(msg):
    # gets the appropriate checksum for a message
    sig = b""
    msg_padded = msg + b"\xff" * (32 - len(msg))

    for guess in range(2500, 5500):
      if guess % 100 == 0: print("Still calculating checksum, guessing %d" % guess)
      msg_with_checksum = msg_padded + struct.pack("<I", guess)
      output = execute(msg_with_checksum, sig)

      if b"signature" in output:
          return guess

admin_command=b"su admin" + 24*b"\x00"

print("[+] Building dictionary of secret key for non-checksum part")
signing_dict = get_signing_dictionary()

print("[+] Getting checksum for the admin command")
checksum = get_checksum(admin_command)

checksum_unpacked = struct.pack("<I", checksum)

print("[+] Trying lots of guesses until we have enough to sign the checksum")
while True:
    msg = bytes(random.randrange(256) for _ in range(32))
    msg, checksum, sig = sign(msg)

    for i, c in enumerate(checksum):
        signing_dict[(c, 32+i)] = sig[(32+i)*32:(32+i+1)*32]

        for b in range(c+1, 256):
            if (b, 32+i) not in signing_dict:
                signing_dict[(b, 32+i)] = sha256(signing_dict[(b-1, 32+i)]).digest()

    min_in_dict = [min(c for c in range(256) if (c, i) in signing_dict) for i in range(32, 36)]
    print(min_in_dict)
    print(checksum_unpacked)

    if all(min_in_dict[i] <= checksum_unpacked[i] for i in range(4)):
        break

print("[+] Signing admin message and sending...")
msg = admin_command + checksum_unpacked
sig = b"".join(signing_dict[c, i] for i, c in enumerate(msg))

result = execute(msg, sig)
print(repr(result))

print("[+] Getting flag...")
msg, checksum, sig = sign(b"show flag")

result = execute(msg, sig)
print(repr(result))
