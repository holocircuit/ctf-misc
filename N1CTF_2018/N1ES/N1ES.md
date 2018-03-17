# N1ES
(Crypto)

Overview: We have two Python files.

N1ES.py defines a block cipher, with key length 24 bytes, block size 16 bytes. 

challenge.py gives us the key, and the encryption of a (hidden flag).

## Understanding the cipher
### Overview
- It's essentially a block cipher with block size 16 bytes, encrypting in ECB mode with no padding.
- On initialisation, it generates 32 round keys (8 bytes long).
- Encrypting a block consists of 32 rounds, one with each round key.

### Rounds
Let the first block be `x_0||x_1`, where we mean 8-byte chunks.

Then `x_{i+1} = round_add(x_{i-1}, k_{i-1})` where `k_i` are the round keys.
The output is then `x_33||x_32`.

`round_add` does the following:
combines character-wise, where the combination is the function `a + b - 2*(a&b)`.

## Breaking it
We have the key, so we just need to work out how to write a decryption function.
This is equivalent to having a way to "reverse" each round.

It's effectively block size 1 (because the rounds are character-wise), so maybe we can just brute-force each character.

This works! We can brute-force the result after each round back to the start, and get the flag.

The flag is **N1CTF{F3istel_n3tw0rk_c4n_b3_ea5i1y_s0lv3d_/--/}**.
