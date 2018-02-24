# Fanfic
(Binary Exploitation, 350 points)

It's a little program which writes a fanfic. We have the source.
It stores the fanfic on a heap, as a doubly linked list of "chapters".

Each chapter also contains a function pointer, to a function which prints the chapter.

## Vulnerability
The code uses `gets` when *editing* (not creating) the contents of the chapter, so we can overflow the function pointer and call whatever we like.
There are two helper functions in the code: `validate` and `give_flag`.

If we call `validate` with `0x40`, and then `give_flag`, we'll get the flag. Cool!

When we "print a chapter", the first argument is the chapter number (starting from 1). So our exploit needs to look like:
- Create 0x41 chapters
- Edit chapter 0x40, overflow the function pointer with the address of `validate`
- Edit chapter 0x41, overflow the function pointer with the address of `give_flag`
- print the chapters

