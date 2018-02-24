# Hidden Key
(Crypto, 250 points)

RSA challenge.
We're given the value of `2d + phi(n)`.

We can work out the relationship
`c^{2d + phi(n)} mod n = c^{2d} mod n = m^2 mod n`,
so we can work out the value of `m^2 mod n`.

This turned out to be small, so we can just square root it and get the message.
