import socket
import re

# stolen from wikibooks. 
def egcd(b, a):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return b, x0, y0

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def int_to_string(n):
    s = ""
    while n != 0:
        s += chr(n%256)
        n /= 256
    return s[::-1]

def root(n, power):
    # returns power root, using binary search
    (lower, upper) = (0, n)
    while lower < upper - 1:
        mid = (lower + upper) / 2
        if mid**power > n:
            upper = mid
        else:
            lower = mid
    if lower**power == n:
        return lower
    else:
        return None

def get_flag_encryption((ip, port), e):
    s = socket.create_connection((ip, port))
    s.recv(4096)

    # we need to first of all generate N, so we don't corrupt the file
    s.send("3\n")
    s.recv(4096)
    N = s.recv(4096)
    print repr(N)
    N = int(re.findall("N = 0x([0-9a-f]*)", N)[0], 16)
    print hex(N)
    s.send("%d\n" % e)
    s.recv(4096)
    s.send("someplaintext\n")
    s.recv(4096)
    s.send("n\n")
    s.recv(4096)

    s.send("2\n")
    s.recv(4096)
    s.send("flag\n")
    s.recv(4096)
    s.send("%d\n" % e)
    result = s.recv(4096)
    if "Invalid" in result:
        # This means that e wasn't compatible with phi(N). Discard, try again
        return None

    print repr(result)
    C = int(re.findall("C = 0x([0-9a-f]*)", result)[0], 16)
    print hex(C)
    return (N, C)

def halstad_attack(observed_ciphertexts, power):
    if len(observed_ciphertexts) < power:
        assert False

    total_N = 1
    for (N, _) in observed_ciphertexts:
        total_N *= N

    results = []
    for (N, C) in observed_ciphertexts:
        other_ns = total_N / N
        results.append(C * other_ns * modinv(other_ns, N))

    for (N, C) in observed_ciphertexts:
        print C, [result % N for result in results]
        print ""

    result = sum(results) % total_N
    for (i, (N, C)) in enumerate(observed_ciphertexts):
        if result % N != C:
            print "failed on %d" % i
            assert False

    print len(hex(result))
    print len(hex(total_N))
    decrypt = root(result, power)
    if decrypt != None:
        print int_to_string(decrypt)
    else:
        print "didn't get a root :("

# higher power means we have to get more ciphertexts
# lower power means we're more likely to be rejected for not being coprime with phi(N)
power = 5

values = []

while len(values) < power + 3:
    try:
        value = get_flag_encryption(("47.52.195.203", 2333), power)
    except IndexError:
        # lazy! I think this happens when packets get split up, should use pwntools
        print "failure?"
        value = None
    if value != None:
        print "Got a value"
        values.append(value)

halstad_attack(values, power)
