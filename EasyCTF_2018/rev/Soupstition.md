# Soupstition Cipher
(Reverse Engineering, 150 points)

We have a Python script, which has been obfuscated! Lots of variables have been replaced with "soup", with different capitalisation.

After manually doing some substitutions, and renaming some functions, we have something that looks saner:

```
#!/usr/bin/env python3

from binascii import unhexlify as unhexlify
from operator import attrgetter as attrgetter

ME_FLAGE = '<censored>'

input = input
hex = hex
print = print
ord = ord
open = open

def reverse_digits(y):
    x = 0
    while y != 0:
        x = (x * 10) + (y % 10)
        y //= 10
    return x

def digits_to_int(l):
    x = 0
    for y in l:
        x *= 10
        x += ord(y) - ord('0')
    return x

def main_func():
    your_input = input()[:7]
    print(your_input)
    if not attrgetter('isdigit')(your_input)():
        print("that's not a number lol")
        return

    reversed_digits = reverse_digits(digits_to_int(your_input))
    #result = attrgetter('zfill')(hex(reversed_digits)[2:])(8)[-8:]
    result = hex(reversed_digits)[2:].zfill(8)[-8:]
    if unhexlify(result) == attrgetter('encode')('s0up')():
        print("oh yay it's a flag!", ME_FLAGE)
    else:
        print('oh noes rip u')

if __name__ == '__main__':
    main_func()
```

So we want to input an integer, such that when we reverse the digits and hex it, we get hex that spells out the word *s0up*.
On first glance, this looks impossible. We're limited to 7 bytes of input, and the hex representation is *73307570*, or *1932555632* in decimal, which is too big.

I looked up the definition of isdigit in the Python source. Turns out (of course...) that there are many other larger Unicode characters that count as digits. E.g. `0x2460`.

We can generate all characters that count as digits by doing something like
`print([i for i in xrange(0x110000) if chr(i).isdigit()])`

Using this, we can then by inspection construct something that works:
We're aiming to input at most 7 "digits" s.t. the number it constructs is 2365552391.

I just build this up randomly: the list
`[2406, "9", "9", 6610, "3", "9", "1"]`
works.

We can pipe this in via
`python3 -c 'import sys; sys.stdout.write(chr(2406) + "99" + chr(6610) + "391")'`
- sending this to the socket gives us the flag.
