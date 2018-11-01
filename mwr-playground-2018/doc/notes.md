# Dodgy Word Doc (OLE streams)

Easy one, has a guide to browsing the OLE streams.

## Find the username
`olemeta` prints out all the metadata, including the author.

## Find the "suspiciously large stream"
`oledir` prints out information about the different streams.
The one called *Package* jumps out as the large one.

Extracting this with `olebrowse` and inspecting it with `file`, it's a PowerPoint.

## Find dodgy DNS name
Can inspect the VBA macro with `olevba` on the PowerPoint.
Immediately reveals something which is downloading an EXE, and the domain.
