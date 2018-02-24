# Format
(BinExp, 160 points)

Basic format string vulnerability.
Unlike previous stuff I've seen, it's on 64-bit Linux.
Rather than `%08x`, had to use `%16llx` to print out the whole pointer - otherwise we "skipped over" where the random number was.

Using this, we can print out the random number from memory, then input it back to get the flag.
