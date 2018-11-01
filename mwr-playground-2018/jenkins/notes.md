# Jenkins

## Part 1
Easy: guess admin password as `admin`.

## Part 2
We have access to a console under `/script`, which let's us run "GroovyScript".
https://highon.coffee/blog/jenkins-api-unauthenticated-rce-exploit/ has an example of using this to run commands - can use this to cat the flag.

## Part 3
By running `sudo -l`, we see that we have sudo access to vim! (without needing password)
So if we can get a proper root shell, can pretty easily get access...

Running `uname -a`, it's 64-bit Linux.
Create a Python reverse shell. Upload with `wget` and run.

Then get a PTY with Python (needed this to be able to run vim).
Then `sudo vim`, get a reverse shell. Then we get a passwd and shadow file. John easily cracks the root password as `qwerty`.
