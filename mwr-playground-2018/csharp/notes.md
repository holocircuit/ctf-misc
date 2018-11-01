# C# Reversing

We have a Linux binary, and a bunch of .NET DLL files.
Running the Linux binary, guessing that it loads `RevEngChallenge.dll`, and loads and runs it? Not sure how to verify this.

## DLL file
Inspect it with ILSpy. Has some classes `A`, `B`, `Z`.

`B.A`: This takes base64 input, and XORs it with a fixed array.
Easy to recreate the code that generates the array in Python, which lets us decrypt strings in the file.

`A.Main`: I'm guessing (don't know how to check) that this is the function that ends up being called.

Decrypting the strings, we see it reads a line from the input into the `text` variable.
It then does some BCrypt verify thing, against a hardcoded hash.
If it verifies, it prints some output, along with something else which is derived from the text. This uses a function from `libplayground` (a Linux `*.so` which comes with the binary).

## Hash
We decrypt the hash, and stick it through John. No luck so far.
It's cracking really slowly - looks maybe quite resistant to brute-force attacks?

## libplayground.so
Exports a function `a`, which takes in a reference to the .NET class `Z`.
This checks something. It then either prints the string `TAMPER` lots of times, or sets a bit of memory to `c92d0512`. This is presumably the argument (i.e. the variable for `Z**).


Putting this together, this gives output as 
**f088d0be-56df-40a2-8233-59ffc92d0512**
which works as the flag!
