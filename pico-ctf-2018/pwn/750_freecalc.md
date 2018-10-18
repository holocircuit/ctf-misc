# Freecalc
(750 points, Pwn)

It's a little calculator! We can define functions.

It evaluates using a stack, which is implemented as a linked list.
Functions we define are stored in a fixed array. They're stored as a pointer to an array of operations (and an operation count).

Running it, I can make it crash with a double-free error. It seems to do this anytime I run the second computation?

## Vulnerability
Aha. There's a UAF in `line`. We free it, but then re-read into the same buffer.
This feels kind of tricky to exploit. The second line of input we put, we'll loop back to here, and crash on a double-free.

Idea: Perhaps we can make a function get reallocated to this block? Struggled to get that to work by hand.
