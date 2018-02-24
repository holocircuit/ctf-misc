# EzReverse
(Reverse Engineering, 140 points)

Takes some input as an argument. Has a nice feature that if the input is wrong, it deletes the binary...

Reversing the assembly by hand: expecting the input to be 5 bytes.

Uses this to set some values in memory.
Let's call them `X_1, ..., X_5`, and the input `c1c2..c5`.
It sets `X_i = c_i + i`.

Then it does the following checks:
- `X_4 = 0x6f`
- `X_4 + 0xe = X_3`
- `X_5 - 0xa = X_1`
- `X_2 = 0x35`
- `X_4 + 0x3 = X_5`

solving this, we get
`X_1 = 0x68`
`X_2 = 0x35`
`X_3 = 0x7d`
`X_4 = 0x6f`
`X_5 = 0x72`

and reversing the initial XORing, this gives required input of **g3zkm**.


