# Keyed Xor
(Crypto, 100 points)

The description is a little vague. Says it's keyed XOR, and the key was created "by taking two words from this wordlist". Not clear if it means concatenation to make the key, or something else.

75 characters long.

Crib dragging:
`easyctf{` would fit with the first bit being "indentures.
But this doesn't seem to match with it going anywhere else.
(I'm a little suspicious of this - does it make sense to have that be the first word? It's a pretty long piece of ciphertext.)

All of the characters of the ciphertext are at most `0x1f`, suggesting that both the key and the ciphertext just consist of lowercase letters (and other upper-end ASCII characters, pretty much just the braces and pipe).

More crib dragging:
I tried every word to see "how much" of `easyctf{` it got. `indentures` was the only one, couldn't get close with anything else.


