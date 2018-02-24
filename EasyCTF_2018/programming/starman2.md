# Starman 2
(Programming, 175 points)

We have a bunch of points. We want to find the smallest width W such that they all lie in a rectangular "strip" of width W.
If our strip is angled at angle `t`, then the width is the range of values given by the dot product of `(x, y)` and `(cos t, sin t)`, i.e.
`x cos t + y sin t`

We can view this as a function from `t` to this range, and we just want to find the minimum of this function.
We'll do this by just some sort of interval bisection thing.

The function has period `pi` - we'll take our domain to 

