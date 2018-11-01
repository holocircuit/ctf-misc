# Warehouse Controller
Name of the host suggests it's running Flask. Template injection?

Flags are: Get access to search, get a shell, get root access.

## Flag 1
We have access to register an account, and login.
There's not much we can do after logging in. We're blocked from searching. We can add information about ourselves, or change our name.

Our "name" is displayed in the top-right.

Write a quick script to log in, and pass in given values for name/description. 
Not much luck with template injection: Try some values, but nothing seems to display any differently in the name section.

Trying individual characters: `"&<>` are escaped (HTML-encoded), everything else seems to get through.
Try injections: No luck.
Try injections, and separately checking if we can log into the search page - nothing works.
Try setting name/description to some things like "admin", etc. - no luck.

**I think** something I did got the server into an error state, but I couldn't replicate that.


Update:
OH COME ON. If you just inject an extra parameter `admin=1` into the POST request on the update page, it let's you become the admin.

### Search page
Try POSTing directly - still get "admin privileges" message.

### Dirbuster
Try dirbuster with default settings, didn't find anything.
Ran wfuzz with `big.txt` and `words`. Nothing that we didn't already know about. (login/logout/register/search/update)

### SQLmap
Try SQLmapping the front page out of politeness. 
It suggests a few things, but I think they're spurious. (If I don't skip, it hangs on that test indefinitely.)

### User enumeration
We can enumerate existing users by trying to register them.


## Flag 2
OK, we have the search page, and there's immediately template injection.
Inspecting with `{{ ''.__class__.__mro__[2].__subclasses__() }}`, we have Popen. It's at index 208.

Can read the flag file with `{{ ''.__class__.__mro__[2].__subclasses__()[40]("flag.txt").read() }}`.

## Flag 3 (getting a shell and root)
Struggled to call a reverse shell directory with the template injection. But easy enough to download a reverse shell from our computer and run it.
We can run commands with
`{{ ''.__class__.__mro__[2].__subclasses__()[208]("some command", shell=True) }}`

Running Ubuntu Xenial, 4.4.0-135. Fairly recent...
Two "real" users: ubuntu and vagrant. **Ubuntu is in the sudo group.**
Both of them have `.ssh` directories - can't SSH into either of them with just a password.

OK. I also have sudo access as root, to run `flask`. What could I do with this...

Turns out it's pretty easy to go from that to a reverse shell:
Create a Python file, calling a reverse shell.
`export FLASK_APP=rev_shell.py`
`sudo flask run`
and we get our reverse shell as root!

### Getting the root password
Blah, not sure what to do here. We have the shadow file, nothing else.
Start cracking it...
