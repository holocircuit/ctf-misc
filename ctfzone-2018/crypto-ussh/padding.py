import base64
import sys
import socket

BLOCK_LEN = 16

def crack_block(block, query_valid_padding):
    assert len(block) == BLOCK_LEN
    # Build up solution from the back
    soln = [0] * BLOCK_LEN

    for i in range(-1, -1 * (BLOCK_LEN + 1), -1):
        # This is the padding for this i
        value = i * -1
        pad = [0] * (BLOCK_LEN + i) + [value] * value

        send = [c ^ d for c,d in zip(soln, pad)]
        accepted = []
        for b in range(256):
            send[i] = b
            if query_valid_padding(bytes(send) + block):
                accepted.append(b)

        print(accepted)
        if len(accepted) == 1:
            soln[i] = accepted[b] ^ value
        elif len(accepted) > 1:
            print("There were multiple that worked! :O")

            # hack: I think the one that should be accepted is the "odd-one-out"
            accepted = set(accepted)
            l = [s for s in accepted if s & 0b11110000 not in accepted]
            print(l)
            soln[i] = l[0] ^ value
        else:
            print("Couldn't find any that worked :(")
            sys.exit(1)

        print(soln)
        sys.stdout.flush()
    return bytes(soln)

sock = socket.create_connection(("crypto-01.v7frkwrfyhsjtbpfcppnu.ctfz.one", 1337))
sock.send(b"test\n")
if b"crypto: $" not in sock.recv(4096):
    print("Connection failure?")
    sys.exit(1)

sock.send(b"session --get")
this_session = sock.recv(4096)
if b"crypto: $" not in this_session:
    this_session += sock.recv(4096)
print("This session:", repr(this_session))

split = this_session.split(b"\n")[0].strip().split(b":")
iv = split[0]
ciphertext = split[1]

print(iv, ciphertext)

iv = base64.b64decode(iv)
ciphertext = base64.b64decode(ciphertext)

def get_response(iv, ciphertext):
    s = base64.b64encode(iv) + b":" + base64.b64encode(ciphertext)
    msg = b"session --set %s\n" % s

    sock.send(msg)

    response = b""
    while b"crypto: $" not in response:
        response += sock.recv(1024)

    return response

# some testing...
empty_block = b"\x00" * 16

good_bytes = []
for i in range(256):
    iv = b"\x00" * 15 + bytes([i])

    response = get_response(iv, empty_block)

    if b"PKCS7" not in response:
        good_bytes.append(i)
print(good_bytes)

for byte in good_bytes:
    print("testing byte %d..." % byte)
    l = []
    for j in range(256):
        iv = b"\x00" * 14 + bytes([(byte ^ 1) ^ 2, j])

        response = get_response(iv, empty_block)

        if b"PKCS7" not in response:
            print(repr(response))
            l.append(j)
    print(byte, l)


assert False

def query_valid_padding(ciphertext):
    s = base64.b64encode(iv) + b":" + base64.b64encode(ciphertext)
    msg = b"session --set %s\n" % s

    done = False
    while not done:
        sock.send(msg)

        response = b""
        while b"crypto: $" not in response:
            response += sock.recv(1024)

        if b"Usage: session" in response:
            print("Saw usage message, weird. Continuing...")
            continue
        else:
            break

    if b"PKCS7 padding is incorrect" in response:
        return False
    else:
        print(repr(response))
        return True

blocks = [ciphertext[i:i+BLOCK_LEN] for i in range(0, len(ciphertext), BLOCK_LEN)]

soln = b""
for i, block in enumerate(blocks):
    s = crack_block(block, query_valid_padding)
    if i == 0:
        # XOR with IV
        soln += bytes([c ^ d for c, d in zip(s, iv)])
        print(soln)
    else:
        soln += bytes([c ^ d for c, d in zip(s, blocks[i-1])])
        print(soln)
    print(soln)
