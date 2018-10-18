# Flask one 
(900 points, Web)

SSTI! Followed the guide at https://nvisium.com/blog/2016/03/11/exploring-ssti-in-flask-jinja2-part-ii.html.
By exploring the object tree, can see all classes included with
`{{ ''.__class__.mro()[1].__subclasses__() }}`

Injection guide *seems* to suggest that we'd expect to see file at index 40, and can do sneaky stuff with that.
That wasn't there, but subprocess.Popen was somewhere else, which let us create a reverse shell.
