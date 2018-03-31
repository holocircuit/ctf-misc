# Nonsense
(Crypto, 200 points)

We're given a Python script, and a file containing some strings and signatures.
The Python script runs the DSA algorithm, with a linear generator for generating the "random" nonces.
Goal is to get the secret key.

Because the generator is linear, we can end up taking two signatures and writing a linear equation to get the seed.
Once we have the seed, we know what nonces were used - with DSA this lets us recover the secret key.

See `nonsense_sol.py` for details.
