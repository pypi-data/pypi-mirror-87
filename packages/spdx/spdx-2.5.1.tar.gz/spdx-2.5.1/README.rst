spdx
====

A Python module incorporating an interface to the SPDX license database.

This library serves purely as a holder for the database that can be
found on `the SPDX website <https://spdx.org/licenses/>`__.

To more easily query this database or detect licenses, consider using
something like
`spdx-lookup <https://pypi.python.org/pypi/spdx-lookup>`__.

Usage
-----

See the ``spdx/__init__.py`` file for the very simple interface.

tl;dr: ``spdx.licenses()`` gets you the licenses, and ``spdx.License``
is a nice wrapper for interacting with them.
