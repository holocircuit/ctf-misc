# USSH
(Crypto, "easy")

We have a restricted shell.
One option is `session`, where we can get or set a session.
Format is <16 bytes b64'd>:<32 bytes b64'd>

Mentions PKCS7 padding if we try and change it. Aha. Padding oracle attack.

## Decrypting it
