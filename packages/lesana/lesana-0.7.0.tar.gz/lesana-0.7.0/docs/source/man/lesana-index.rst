============
lesana-index
============

SYNOPSIS
========

lesana index [--help] [--collection COLLECTION] [files [files ...]]

DESCRIPTION
===========

Lesana index adds some entries to the xapian cache, listed by filename
(by default all of the files found in the items directory).

OPTIONS
=======

-h, --help
   Prints an help message and exits.
--collection COLLECTION, -c COLLECTION
   The collection to work on. Default is ``.``
--reset
   Delete the existing xapian cache before indexing.

