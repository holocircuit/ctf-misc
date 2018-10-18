# James Brahm Returns
(700 points, Crypto)

OK, so it's another James Brahm one, where we can affect part of a message and want to find out another chunk.

Encrypted messages look like
`IV || AES-CBC(Pad(M + MAC), IV)`
(where MAC is a SHA-1 based MAC, unkeyed)

Messages are of the form
`prefix || report || flag_prefix || flag || suffix || PS`

(where `prefix`, `flag_prefix`, `suffix` are known)


We're allowed to do two things:
(1) Encrypt messages, where
- The IV is randomly chosen
- We get to pick `report` and `PS`. 

(2) Check if a message can decrypt, under two restrictions:
- Can't reuse the IV
- Can't distinguish between bad padding or bad MAC

note: we don't get the decryption, just find out if it validated

## Ideas
- SHA1 length extension? Not obvious how this helps
- The hint is something to do with SSLv3. BEAST attack? POODLE attack?

OK, reading about the POODLE attack, looks like it's very applicable here. There's another vulnerability - it doesn't check the padding properly, only the last byte of it.

So: we can encrypt a message, and then replace the last chunk with another chunk of our message. 
Let's suppose we shift the block sizes s.t. the last block is all padding. Then it'll validate iff the last byte is 16. We can use this to brute-force the flag, one byte at a time.

