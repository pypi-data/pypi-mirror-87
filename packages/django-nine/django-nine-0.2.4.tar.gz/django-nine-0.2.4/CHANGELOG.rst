Release history and notes
=========================
`Sequence based identifiers
<http://en.wikipedia.org/wiki/Software_versioning#Sequence-based_identifiers>`_
are used for versioning (schema follows below):

.. code-block:: none

    major.minor[.revision]

- It's always safe to upgrade within the same minor version (for example, from
  0.3 to 0.3.2).
- Minor version changes might be backwards incompatible. Read the
  release notes carefully before upgrading (for example, when upgrading from
  0.3.2 to 0.4).
- All backwards incompatible changes are mentioned in this document.

0.2.4
-----
2020-12-03

- Added more Django versions.

0.2.3
-----
2020-01-11

- Added more Django versions.

0.2.2
-----
2019-05-18

- Bring back the `user` compatibility module. However, it's deprecated and
  will be removed in version 0.3.
- Show deprecation warnings.

0.2.1
-----
2019-05-18

- Fixes in backwards compatibility.

0.2
---
2019-05-17

.. note::

    This release is still backwards-compatible with previous versions (0.1.x),
    but next versions (0.3.x) would not be.

- Drop Python 2.6 support.
- Change namespace from `nine` to `django_nine`.
- Removed `user` compatibility module. Implement your own if you need.
- Add travis.

0.1.13
------
2017-05-16

- Added context processor using versions in templates.

0.1.12
------
2017-02-09

- Test against Python 3.6 and Django 1.11.

0.1.11
------
2016-11-30

- Clean-up.

0.1.10
------
2016-09-13

- Added Django 2.2 and 3.0 to the version comparision.

0.1.9
-----
2016-07-12

- Adding missing `DJANGO_LTE_*` versions to `__all__`.

0.1.8
-----
2016-07-11

- Unify comparison versions list generation.

0.1.7
-----
2015-12-18

- Added Django 1.10 version comparison.

0.1.6
-----
2015-10-25

- Fixes for Python 3.3.
- Moving `Django` dependency from `install_requires` to `tests_require`.

0.1.5
-----
2015-10-05

- Moving `mock` dependency from `install_requires` to `tests_require`.

0.1.4
-----
2015-10-02

- Minor Django 1.4 fixes in the `user` module.

0.1.3
-----
2015-08-25

- Recreated release under 0.1.3 on PyPI due to upload error.

0.1.2
-----
2015-08-25

- Python 2.6 fixes.

0.1.1
-----
2015-02-15

- Tests for ``versions`` sub-module added.

0.1
---
2015-02-14

- Initial release with `versions` and `user` modules.
