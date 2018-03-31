import hashlib
import sys

def all_possibilities(possibilities, n):
    if n == 0: yield ""
    else:
        for p in possibilities:
            for prefix in all_possibilities(possibilities, n-1):
                yield p + prefix

def ending_bits(n):
    i = 0
    while n % 2 == 1:
        i += 1 
        n /= 2
    return i

def ending_bits_s(s):
    total = 0
    i = -1
    k = ending_bits(ord(s[i]))

    total += k
    while k == 8:
        i -= 1
        k = ending_bits(ord(s[i]))
        total += k
    return total

def proof_of_work(prefix):
    for suffix in all_possibilities("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", 5):
        x = prefix + suffix
        hash_ = hashlib.sha1(x).digest() 
        # check last 26 bits

        n = ending_bits_s(hash_)
        if n >= 20: print x, n

        if n >= 26:
            print x, n, repr(hash_)
            return x

proof_of_work(sys.argv[1])
