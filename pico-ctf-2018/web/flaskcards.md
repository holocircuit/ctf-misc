# Flaskcards
(350 points, Web)

A small website which does flashcards. There's an admin page, but we're not allowed to see it.
Name strongly suggests it's running Flask.

By experimentation, we can do template injection in the cards, to execute arbitrary Python. Some things that work:
```
{{ 1 + 1 }}
{{ "test" }}
```

Tried using this to run "ls", but didn't work.
Tried using this to print output of "dir()", didn't work.

If we input something that's "invalid", it looks like it gives up on executing the template (and just shows us the code).

Turns out that `config` is a special thing in Flask which contains the config of the server. We can view it with
`{{config}}`

-- and this contains the flag as one of the variables. :)

