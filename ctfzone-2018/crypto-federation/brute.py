import socket
import random
import sys
import base64

host = 'crypto-04.v7frkwrfyhsjtbpfcppnu.ctfz.one'
port = 7331

def get_file_encryption(s):
    sock = socket.create_connection((host, port))
    sock.send(b"file %s</msg>\n" % s)
    return base64.b64decode(sock.recv(1024)[:-6].decode("ascii"))

def encrypt_block(b):
    assert len(b) == 16
    return get_file_encryption(b)[:16]

def decrypt_block(b, prefix):
    assert len(prefix) == 15

    for i in range(256):
        guess = prefix + bytes([i])
        #print(repr(guess))
        if encrypt_block(guess) == b:
            return guess

    return None

filename = sys.argv[1].encode("ascii")
print(len(get_file_encryption(filename)))

decryption = b"\x00" * 14 + b": "

while True:
    i = len(decryption) - 16

    # We want to get position i of the message, so we want this to be at the end of a block

    our_prefix_length = 15 - (i % 16)

    our_prefix = filename
    # pad so that the length is equal to [our_prefix_length-2] mod 16
    # (minus 2 because of the ": ")
    our_prefix += b"\x00" * 16
    padding = (len(our_prefix) - (our_prefix_length - 2)) % 16
    our_prefix += b"\x00" * (16 - padding)

    assert(len(our_prefix) + 2) % 16 == our_prefix_length

    encrypted = get_file_encryption(our_prefix)

    position = i + len(our_prefix) + 2
    assert position % 16 == 15

    blocks = [encrypted[i:i+16] for i in range(0, len(encrypted), 16)]

    block = encrypted[position-15:position+1]
    assert block in blocks
    decrypted_block = decrypt_block(block, decryption[-15:])

    decryption += bytes([decrypted_block[-1]])
    print(repr(decryption))


print(repr(get_file_encryption(filename)))
