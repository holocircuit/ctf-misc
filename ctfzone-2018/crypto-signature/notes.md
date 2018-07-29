# Signature Server
(crypto, medium)

## Server
It's a server. Accepts input in the form `cmd:arg`.
Initializes itself with random data for the key each time (i.e. each time we connect).

## Signing
We can sign whatever we want, other than the two special commands (to become admin and read the flag).

Signing works as follows:
- It expects base64-encoded data, which is less than `MESSAGE_LENGTH` bytes long
- Expands to `MESSAGE_LENGTH` by padding with the byte `0xff`
- Adds a checksum (Winternitz checksum)
- Creates a signature by singing each byte of the data.

### Signing a byte
Has an array in memory called `full_sign_key`.
It's flat, but think of it as a 2D array:

Side lengths `CHANGED_MESSAGE_LENGTH` and `256`, where each "element" of the array is a hash.
The first row is random data.
Each entry is then given by the SHA256 of the element directly above.

The signature of a word is the concatenation of the signature of each byte.
The signature of a byte is given by an entry in this array. 
Rows correspond to the byte value. Column is the position in the string.

## Flaws
There's a flaw in the padding: it's not injective.
If we submit `show flag` without the padding, we can sign it!
This then works, but we're not admin yet.
