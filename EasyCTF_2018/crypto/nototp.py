import binascii

c1 = "38445d4e5311544249005351535f005d5d0c575b5e4f481155504e495740145f4c505c5c0e196044454817564d4e12515a5f4f12465c4a45431245430050154b4d4d415c560c4f54144440415f595845494c125953575513454e11525e484550424941595b5a4b"
c2 = "3343464b415550424b415551454b00405b4553135e5f00455f540c535750464954154a5852505a4b00455f5458004b5f430c575b58550c4e5444545e0056405d5f53101055404155145d5f0053565f59524c54574f46416c5854416e525e11506f485206554e51"

c1 = binascii.unhexlify(c1)
c2 = binascii.unhexlify(c2)
l = len(c1)

def xor_strings(s1, s2):
    return bytes([c1 ^ c2 for c1, c2 in zip(s1, s2)])

def xor_with_key(s1, key):
    return bytes([c ^ key[i%len(key)] for i, c in enumerate(s1)])

# Crib drag easyctf{
# for i in range(l - 9):
#    print(i, repr(xor_with_key(xor_with_key(b" easyctf{", c1[i:]), c2[i:])))

# from this, we get that one of the ciphertexts (call it c1) has "easyctf{" at position 76
# other one is "intext u"

pad = bytes(l)
def add_guess(current_pad, plaintext, position, ciphertext):
    pad = current_pad[:position] + xor_with_key(plaintext, ciphertext[position:]) + current_pad[position+len(plaintext):]
    return pad

pad = add_guess(pad, b" easyctf{", 75, c1)
pad = add_guess(pad, b"plaintext", 73, c2)
pad = add_guess(pad, b" flag is easyctf{", 67, c1)

e1 = xor_strings(pad, c1)
e2 = xor_strings(pad, c2)
print(repr(e1))
print(repr(e2))
print(repr(e1[67:]))
print(repr(e2[67:]))

# OK, we got some guesses down, but it's still a little hard to see what's there
# we can XOR them together, and try and guess where spaces are (assuming the flag is all alphanumeric)
xored_in_flag_section = [i for i, c in enumerate(xor_strings(c1, c2)) if c & 0x40 != 0]
print(xored_in_flag_section)

# from this, we can sort of squint and decide that the next word in c2 is 4 letters
pad = add_guess(pad, b" used ", 82, c2)
# yay! "otp" appears in the flag, so we're probably right
# can guess more from the other plaintext we have, confirming that the flag looks vaguely sane

pad = add_guess(pad, b"in ", 88, c2)

# how I guessed codebreaking...
# don't really know. Guessed "codetext" and noticed that the start looked right
# probably would have been easier to guess with more context on the start of the string
pad = add_guess(pad, b"codebreaking", 91, c2)

e1 = xor_strings(pad, c1)
e2 = xor_strings(pad, c2)
print(repr(e1))
print(repr(e2))
print(repr(e1[67:]))
print(repr(e2[67:]))

print([hex(c) for c in xor_strings(e1, e2)[91:]])

