# Nosource
(Web, 250 points)

Sequel to the other web challenge, where the flag was just there in the source, XOR encrypted.

In this one, it seems to stop you looking at the source. (Actually, it directed me to some page until I disabled Ghostery.)

I disabled extensions, and looked at the traffic in Wireshark to see the source.

This gives a base64-encoded string, and a key.
The key appears to be wrong? But by guessing a crib we can decode it, and get the flag.

(Not sure how the code works that blocks viewing the source. It's doing some DOM stuff.)
