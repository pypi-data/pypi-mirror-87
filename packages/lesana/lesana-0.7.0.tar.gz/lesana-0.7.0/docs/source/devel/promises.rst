********
Promises
********

Semantic versioning
===================

This project uses semver_.

.. _semver: http://semver.org/

Collection format stability
===========================

Future versions of lesana will be able to read collections written by
older versions.

Older versions in the same mayor release will also be able to work
concurrently on the same repository.

If in the future a change of formats will be required, conversions
scripts will be written in a way that will make them as stable as
possibile, and will have enought test data to keep them maintained for
the time being.

Disposable cache
================

Contrary to the yaml files, the xapian cache is considered disposable:
from time to time there may be a need to delete the cache and reindex
everything, either because of an upgrade or to perform repository
mainteinance.

Of course, effort will be made to reduce the need for this so that it
only happens sporadically, but it will probably never completely
disappear.
