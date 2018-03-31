# Golden Antelope
(Crypto, 350 points)

We're given a server (shielded by a proof of work system), and a Python script.
The script runs a "casino", where we have to guess random numbers. If we get enough points, we get a flag.

## Understanding the script
### Generator
Have a generator class which holds some state.
The state is 32 bits long, stored as a list internally.

Supports a `next_state` operation. You give it a list of indices.
The next bit is the XOR of the bits at those indices. That's put in the first bit of the state, everything else is shifted up. The last bit drops off the end.

So basically, this is an LFSR, but the function is passed in on each step rather than being intrinsic to the type.

It's not defined here, but there's also a utility function for getting a number out of the LFSR.
It takes the last 8 bits of the state (in reverse order), treats them as a binary string, and converts to an int.

### Main function
`L` = just some permutation of the numbers [0, 255].
There are 3 "Generators" defined, with random initial states.

`RX`: "Normal". Is tapped once per round.
`RA`: If bit 29 of `RX` is 0, then tap with function `A0`, else with `A1`.
`RB`: If bit 26 of `RX` is 0, then tap once, else tap twice.

The actual number is then generated via a combination of the 3 states:
`H(RX) + L(H(RA)) + L(H(RB))`

Interesting observation: We can tap "for free". We only lose a point if we actually guess a number. (But we don't learn anything about the number in that case.)

## Cracking
See `soln.py` for the solution. 
I was too lazy to automate this. It expects you to feed it numbers one-by-one - when it's got enough, it prints out the next part of the stream.

`proof_of_work.py` does the proof-of-work step.
