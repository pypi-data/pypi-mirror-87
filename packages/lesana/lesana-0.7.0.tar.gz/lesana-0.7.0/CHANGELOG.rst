***********
 CHANGELOG
***********

Unreleased
==========

0.7.0
=====

* Improved round trip loading of data results in less spurious changes
  when editing entries.
* More documentation and examples.
* Added support for sorting search results.
* Added --reset option to lesana index.

0.6.2
=====

* Documentation improvements.
* The timestamp field is now always interpreted as UTC.
* Updated links to the published homepage and docs.

0.6.1
=====

* Tarball fixes

0.6.0
=====

* Validation of field contents have been made stricter: invalid contents
  that were accepted in the past may now cause an indexing error.
* The timestamp field type is now deprecated and expected to contain a
  unix timestamp (a yaml datetime is accepted, but may be converted to a
  unix timestamp) and the types datetime and date have been added.

0.5.1
=====

Library
-------

* This version changes the name of entry IDs from the nonsensical ``uid`` to
  ``eid`` (Entry ID) everywhere in the code, including the property
  ``Entry.uid`` and all method names.
