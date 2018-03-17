# rsa_padding
(Crypto)

We're given a network port, protected by a proof of work check.
After doing that, we get some source code.

## Overview
The code RSA-encrypts a flag.
It asks us for some "padding". It SHA256's our input, and uses this as padding for the flag before it is encrypted.

Great. It looks like this exactly fits the Franklin-Reiter attack (see the page about Coppersmith). I just found some code off GitHub implementing this.

(Basically, if you have two ciphertexts which are related by a linear function - i.e. two different paddings - then you can quickly find one of them. The linear function here is adding the differnce between the paddings.)

The flag was **N1CTF{f7efbf4e5f5ef78ca1fb9c8f5eb02635}**.
