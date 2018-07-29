# Federation Workflow System
(Crypto, "medium")

We have two Python scripts, one for the server and one for the client

## Server
Listening on port 7331.
Custom TCP protocol: End of message is indicated by `</msg>`.

Commands are just space-separated words. It accepts one command, then closes the connection.

### list
Lists files. There's a fixed list of them.

### login
Bit of a misleading name: I think this just sends the current time on the server.

### file
Sends a given file to the client, encrypted.
The encryption mode is AES, in ECB mode.

The key is read from the file `../top_secret/aes.key`.

### admin
This takes in a "PIN" argument.
If this passes `check_totp`, we get sent the "real" flag, in `real.flag`.

#### check_totp
Takes the HMAC of some secret, along with a counter which is related to the current time. Then does... something with it.

## Client
This is just a basic wrapper around some commands to the server.

## Cracking
### Decrypting files
We can do the ECB cut-and-paste thing:

It sends us back the filename as the first part of the message, so we can control the first part of the encrypted message.
Also, we can freely add null bytes to the end of the filename (as it "sanitizes" it), so we can get the offset working.

So with the cut-and-paste thing, we can decrypt files.

All of the files that it suggests are troll files.

### Decrypting TOTP key
It adds `files/` to the filename we give (so all the files live there).
It then does `os.path.realpath` on the result, and confirms that the resulting path starts with the current directory.

So we can't read files from arbitrary directories, but we can read from the current directory.

Most of the working files are in the directory above, but `totp.secret` is in the current. So we can read it by passing in `../totp.secret`.

Decrypting it gives a hexstring, and then we can use this to generate our PIN to get the real flag.
