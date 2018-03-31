# CrackMe
(Reversing, 100 points)

.NET executable. Decompiles nicely in JetBrains.

## Reversing
The executable expects an input file, output file, a "user pass phrase" and a mode.
We also have a text file - presumably this has been encrypted with some pass phrase we don't know.

The cryptography itself is in the `CryptoOperation` object.
