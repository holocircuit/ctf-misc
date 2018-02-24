import zipfile
import hashlib
import sys

start = b"begin.zip"
start_pass = b"coolkarni"

def all_char_combinations_for_code(c):
    if c == ord('A'):
        for c in range(ord("A"), ord("Z") + 1): yield c
    elif c == ord('a'):
        for c in range(ord("a"), ord("z") + 1): yield c
    elif c == ord('0'):
        for c in range(ord("0"), ord("9") + 1): yield c
    else:
        print("[+] Failing, unknown char %s" % repr(c))
        assert False

def all_char_combinations(codes):
    if len(codes) == 0:
        yield []
    else:
        start = codes[0]
        rest = codes[1:]
        for c in all_char_combinations_for_code(start):
            for l in all_char_combinations(rest):
                yield [c] + l

def crack_pass(pattern, hash_):
    def substitute(chars):
        l = list(pattern)
        pos = 0
        for i, c in enumerate(l):
            if c != ord("_"):
                l[i] = chars[pos]
                pos += 1
        return bytes(l)

    chars_to_guess = bytes(c for c in pattern if c != ord("_"))
    print("[+] Generating combinations for %s" % chars_to_guess)

    for chars in all_char_combinations(chars_to_guess):
        guess = substitute(chars)
        if hashlib.sha1(guess).hexdigest().encode() == hash_:
            return guess

def process_zip(name, password):
    z = zipfile.ZipFile(name.decode("ascii"))
    l = z.namelist()
    print("[+] Files present: %s" % l)

    if "filename.txt" in l:
        next_file = z.open("filename.txt", "r", password).read().strip()
        if next_file.startswith(b"zip_files/"):
            next_file = next_file[10:]
    else:
        next_file = None

    if "hash.txt" in l:
        next_hash = z.open("hash.txt", "r", password).read().strip()
    else:
        next_hash = None

    if "pattern.txt" in l:
        next_pattern = z.open("pattern.txt", "r", password).read().strip()
    else:
        next_pattern = None

    if "flag.txt" in l:
        flag = z.open("flag.txt", "r", password).read()
        print("[+] Got flag: %s" % flag)
        sys.exit(0)
        
    return (next_file, next_hash, next_pattern)

next_file = start
next_pass = start_pass

while next_file != None:
    (next_file, next_hash, next_pattern) = process_zip(next_file, next_pass)
    print("[+] Next target: Pattern %s, for file %s" % (next_pattern, next_file))
    p = crack_pass(next_pattern, next_hash)
    if p != None:
        print("[+] Got the password: %s" % p)
        next_pass = p
