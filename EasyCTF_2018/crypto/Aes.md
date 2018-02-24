# AES
(Crypto, 160 points)

A funny AES challenge, pointing out vulnerabilities when you use a fixed (known) IV.
Tells you the key. Asks you to input 256 plaintexts of length 256 bits (=2 AES blocks) s.t. the XOR of all of them is the same as the XOR of the ciphertexts.
(Actually, it's not exactly the ciphertext. It converts it via converting to integer - essentially, leading zeros are stripped out).

The ciphertext includes the IV (i.e. the key) at the start.
