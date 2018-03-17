# easy_fs
(Crypto)

## Overview
We have a 64-bit executable running on a remote server. 
We can list the files in the directory - there's a flag file, and a "small file".
We can read the files, but only after encryption. Parameter names suggest it's RSA. It picks N, we specify e.
We can also do "custom encryption", which encrypts some data we provide.

## More details
### Parsing data
Using the custom encryption, I confirmed that it treats the data as an integer in base 256. Doesn't have to be hex characters or anything like that.

### Reading a file
There's a... bug? Confusing trap? in the logic for reading in the file.
It reads it into the variable `temp_buf`.
However, it also uses this internally to generate N, so it seems to end up overwriting the data from the file and just "encrypting" some data for N.

Looking at the reverse in r2, if we've already generated a value for N - i.e. if we've encrypted our own data - we don't regenerate N at this stage. So this skips this step, and means we actually encrypt the data in the file.

## Broadcast attack
We can use Halstad's broadcast attack, as we can get encryptions of the same data with different Ns.

We need to make sure the code does the following things when requesting encryptions:
- encrypt some test data first, to make sure we've generated N and don't overwrite `temp_buf`
- only keep a ciphertext if our exponent was accepted (i.e. coprime to phi(N))

I did this with exponent 5.

The decrypted flag file gives
**Particular applications of the Coppersmith method for attacking RSA include cases when the public exponent e is small or when partial knowledge of the secret key is available. N1CTF{A_sm4ll_l34k_l3ad5_t0_l4rge_br34k}**.

Very interesting! This suggests that the broadcast attack was not what they intended, and instead something with Coppersmith's method.
Oh well, it worked.
