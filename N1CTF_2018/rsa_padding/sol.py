import re
import socket
import hashlib
from pwn import *

def proof_of_work(p):
    test = p.recv(timeout=1)
    results = re.findall("\"([a-zA-Z0-9]*)\"", test)
    prefix = results[0]
    target = results[1]

    n = 0
    while n < 2**64:
        if hashlib.sha256(prefix+str(n)).hexdigest().startswith(target):
            break
        n += 1
    return n

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

# https://github.com/sonickun/cryptools/tree/master/cryptools
def franklin_reiter_related_message_attack(e, n, c1, c2, a, b):
    assert e == 3 and b != 0
    frac = b * (c2 + 2*pow(a,3)*c1 - pow(b,3))
    denom = a * (c2 - pow(a,3)*c1 + 2*pow(b,3))
    m = (frac * modinv(denom, n)) % n
    return m

def get_message_with_padding(padding):
    p = remote("47.75.39.249", 23333)
    n = proof_of_work(p)
    p.sendline(str(n))
    p.sendline("2")
    p.recvuntil("give me a padding")
    p.sendline(padding)
    s = p.recvall(timeout=5)
    print repr(s)
    return re.findall("Your Ciphertext is: ([0-9]*)", s)[0]

c1 = int((get_message_with_padding("1")))
c2 = int((get_message_with_padding("2")))

a = 1
pad1 = int(hashlib.sha256("1").hexdigest(), 16)
pad2 = int(hashlib.sha256("2").hexdigest(), 16)
b = pad2 - pad1
n = 21727106551797231400330796721401157037131178503238742210927927256416073956351568958100038047053002307191569558524956627892618119799679572039939819410371609015002302388267502253326720505214690802942662248282638776986759094777991439524946955458393011802700815763494042802326575866088840712980094975335414387283865492939790773300256234946983831571957038601270911425008907130353723909371646714722730577923843205527739734035515152341673364211058969041089741946974118237091455770042750971424415176552479618605177552145594339271192853653120859740022742221562438237923294609436512995857399568803043924319953346241964071252941

print int_to_string(franklin_reiter_related_message_attack(3, n, c1, c2, a, b) - pad1)
