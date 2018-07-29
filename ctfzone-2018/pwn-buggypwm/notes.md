# Buggy Pwn
(pwn, medium)

It's a Python script, that looks like it's an emulator for a little register machine.

On reading it, it's kind of insane:
The machine has memory on a 2D plane, rather than on a line.
Correspondingly, registers contain complex values rather than integers.

The main class is called `CARM`, which I guess is Complex Arithemetic Register Machine.

## Code structure
### CARM.MemRange
Represents a rectangle of memory, at a given offset.

It has the concept of being "restricted" or "unrestricted".
If "restricted", accessing outside of the range crashes.
if "unrestricted", it loops around.

### CARM.REG
Represents a complex value, and relevant functions for it

### CARM
The rest of this has the "meat" of the register machine. It is initialized with 3 distinct blocks of memory:
- 1D part starting at `(0x60000, 0x60000)` (EIP starts here)
- 1D part starting at `(0x60000, 0x60001)` (the stack?)
- 2D part starting at `(0x60040, 0x60040)`. Amongst other things, this includes some text

Registers:
These are mostly like normal. There are some special registers `ESPD, EIPD`, which represent the "direction" of the instruction pointer and stack respectively.

Commands:
There's a dictionary of commands, and different codes representing each one.

#### Commands
##### __command_nop
Jump EIP forward one (defined by EIPD)

##### __command_add
Bottom 4 bits of amplifier give in register
Top 4 bits give out register

In register has out register added to it

##### __command_xor
similar to add

##### __command_switch
Bottom 4 bits give which register.
Exchanges real and imaginary part.

##### __command_mov_reg
similar to add, but moves the value rather than adding

##### __command_mov_data
TL;DR: Move memory into a register.
has "direct" and "indirect" modes

Bottom 4 bits say which register to move into.
Next bit says whether to move from EIP or from a register.

If from EIP:
Reads a dword from EIP, and stores it in the register.

If not:
Reads a memory location, and a direction from EIP.
Then reads a dword from that memory location (and direction**, and stores it in the register.

**This might have a bug - I'm not sure.**
It only pushes EIP forward one more step after reading a direction, despite reading a dword.

##### __command_rotip
Rotates direction of EIP (either clockwise or anticlockwise depending on parity of amplifier)

##### __command_test
Reads registers from amplifier
Sets ZF if they're equal.

(ZF is never used - not sure if this matters.)

##### __command_mov_data_to_reg
TL;DR: Load from memory location

Bottom 4 bits say which register to move into.
Top 4 bits say which register to read from.

Loads a direction from EIP. Reads from reg2 in that direction, into reg1.

##### __command_mov_data_from_reg

##### __command_call
Reads dword from EIP. (call this `reg`)
Puts next EIP location onto the stack, then jumps to `reg`

(i.e. x86-style function call)

##### __command_ret
Analogous to call.

##### __command_jmpne
subtracts one from ECX.
if the real part isn't zero, read a dword from EIP and jump to it. otherwise continue.

##### __command_sub
This means ESP. Reads a value from EIP, and subtracts it from ESP.
(The amplifier gives a register, but I don't think this is actually used.)

##### __command_syscall
The big one!

If amplifier is 1: 
Print EAX

If amplifier is 2: 
Read some input. Saves EDX values into EDI. (written in real/imaginary pairs, in a flat fashion)
Update: This only accepts "printable" characters. Wowwwww

If amplifier is 3: 
Print EDX values from EDI.

If amplifier is 4:
Seems to create some random data (in a range between ECXs real and imaginary part).
Saves it in EDI. EDX says how many bytes to do this for.

If amplifier is 5:
Reads an integer. Sets ECX to this integer (with 0 imaginary part).

If amplifier is 0x40:
If EAX is ("f","l") and EBX is ("a","g"), prints the flag.

## Disassembly of program
The emulator doesn't ask for any input directly, that's all done inside the program.

Vague disassembly, using the notes above:
```
call (0x060006, 0x060000)

(at this location)
mov_data EDI (0x060040, 0x060040)  # "EasyPwn"
mov_data EDX (0x4, 0x0)
mov_data EDID (0x1, 0x0)
syscall print

mov_data EDI (0x060040, 0x060041) # "How many strings:"
mov_data EDX (0x9, 0x0)
syscall print
mov_data ESI (0x060040, 0x060045)
mov_data EBX (0x0, 0x1)
syscall read_int

mov_data EDI (0x060040, 0x060042) # "Input:"
mov_data EDX (0x9, 0x0)
syscall print

mov EDI, ESI
mov_data EDX (0x10, 0x0)
syscall read_string
ADD EBX, EDI  # (i.e. move up one row of memory)
JMPNE (0x06002c, 0x060000) # (so loop over ECX)

mov_data EDI (0x060040, 0x060043) # "How many letters"
mov_data EDX (0x9, 0x0)
syscall print

syscall read_int

mov_data EDI (0x060040, 0x600044) # "Your name please"
mov_data EDX (0x10, 0x0)
syscall print

SUB ESP 0x10 
MOV EDI, ESP
MOV EDX, ECX
syscall read_string
syscall print

ADD ESP 0x10
RET
```

Seems pretty clear now that this is just a standard buffer-overflow.
We can overflow the buffer to the data in the top part of memory that we control.
So it's just a case of writing some shellcode there which gets us into a good state
to print the flag.

## Writing ASCII shellcode
Woah. We have to write our shellcode only with printable characters (because the syscall insists on this). This might be difficult...

Stuff we can do:
- All the commands are printable
- Add: Probably fine (with some limitations)
- Syscall: Horribly limited (can only do the final one)

How I think we can do this:
`XOR ESI, EDI` <- now ESI will contain 1

then a mixture of ADDs, MOVs and XORs from ESI and EDX (which is `0x11`) should be able to get it.
