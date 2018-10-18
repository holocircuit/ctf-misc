# Keygen1
(400 points, Reversing)

Expects 16 byte key. All characters must be in `0..9A..Z`.
`ord` function - treats it as base 36.

Looks like the `validate_key` function calculates the sum of
`(i + 1) * (ord(s[i] + 1)`,

excluding the last character.

After doing that, it does some computation on it. Then checks if it's equal to `ord` of the last character, and validates.

Just tried passing in *AAAA...*, and checked what it expected for the last byte in a debugger. **AAAAAAAAAAAAAAAO** then gave a valid key.
