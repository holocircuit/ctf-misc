# Sword
(800 points, pwn)

Heap pwn. We can create "swords" on the heap, which contain a pointer to a string and a function pointer.

Operations that we can do:
- Create a sword. Malloc's it. Does *not* properly zero out the memory - initialises `is_hardened` but not the name or the function pointer.

- Combine 2 swords. Takes two swords - checked they're marked as "used" in the table. Combines them by concatenating the names (reallocing if necessary).
Marked in the source as vulnerable. This causes a UAF - the first sword has its name freed, but not the sword itself.

- Show sword. Prints the sword's weight and name. Checks that it's "used" in the table.

- Free sword. Frees the sword's name, then the sword itself.

- Harden sword. This adds a name and a weight to the sword, and marks it as hardened. "Sleeps" for way too long unless `weight = -1`

- Equip sword. This runs the function pointer on the name. Does **not** check that the sword is used!


## Vulnerabilites
Two main vulnerabilities:
- Sword uses unalloated memory when created. We can abuse this by:
(1) Creating and hardening a sword, with name of the correct length
(2) Freeing
(3) Creating a sword (which collides with the "string" block)

This lets us control RIP.

- The UAF where the name of the sword is freed but not the sword.
This lets us go the other way:
We can create a sword which collides with the freed string block. We can then print the old sword.
This seems harder to use (the sword has null bytes in, so we can't easily use it to leak a heap pointer).

The first one feels useful, and in fact we can use this to call RIP with an arbitrary string. But we still need a pointer into libc to bypass ASLR.

### Bypassing ASLR
