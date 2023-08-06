==========
lesana-new
==========

SYNOPSIS
========

lesana new [--help] [--collection <collection>] [--no-git]

DESCRIPTION
===========

Lesana new creates a new lesana entry.

It will create an empty entry and open an editor so that it can be
filled.

If the collection is configured to use git, after the editor has been
closed, it will add the file to the git staging area, unless
``--no-git`` is given.

OPTIONS
=======

-h, --help
   Prints an help message and exits.
--collection COLLECTION, -c COLLECTION
   The collection to work on. Default is ``.``
--no-git
   Don't add the new entry to git.
