# The Vault
(250 points, Web)

It's SQLi, but they're validating that the input doesn't contain `OR`.
There's a `debug` parameter we can send which prints out the query it's running.

Using this, pretty easy to construct a `UNION` SQL injection which bypasses the filter. See `the_vault.py`
