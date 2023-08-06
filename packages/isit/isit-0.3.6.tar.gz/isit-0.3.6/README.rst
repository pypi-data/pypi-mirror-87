Isit
====

Description
-----------

Detect environment variables, such ``linux``, ``distribution``, ``python``, etc...

::

  >>> import isit
  >>> isit.linux
  True
  >>> isit.linux2
  True
  >>> isit.linux3
  False
  >>> isit.py2
  True
  >>> isit.py27
  False
  >>> isit.debian
  True
  >>> isit.debian_version
  '6.0.5'
  >>> isit.debian_release
  '5'
  >>> isit.bit32
  True
  >>> isit.pypy
  False
  >>> isit.cpython
  True
  >>> isit.friday
  True
  >>> isit.winter
  True
  >>> isit.heroku
  False
  >>> isit.newrelic
  False

You can do ``help(isit)`` for list.

Installation
------------

::

	pip install isit

