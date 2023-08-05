Changelog
=========

0.6.4 - 2020-11-30
------------------
- Correctly handles MemcachedError with no retcode attribute
- Adds black formatiing
- Supports Python 3.6 through 3.8

0.6.3 - 2020-10-21
------------------
- Makes retry on ConnectionError
- Drops support of old Python and Django version
- Supports Django 2.2 through 3.1
- Supports Python 3.5 through 3.8

0.6.2 - 2020-10-16
------------------
- Supports Django 1.7 through 3.1
- Supports Python 2.7 through 3.8

0.6.1 - 2015-12-28
------------------
- Supports Django 1.7 through 1.11
- Supports Python 2.7, 3.4, and 3.5

0.6.0 - 2015-04-01
------------------
- Requires pylibmc 1.4.1 or greater
- Supports Django 1.4 through 1.8.
- Supports Python 2.5 through 2.7, and Python 3.3 through 3.4
- In Django 1.6 and higher, when the timeout is omitted, the default
  timeout is used, rather than set to "never expire".

.. Omit older changes from package
