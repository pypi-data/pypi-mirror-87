===========
lesana-edit
===========

SYNOPSIS
========

lesana edit [--help] [--collection <collection>] [--no-git] <entry>

DESCRIPTION
===========

Lesana edit will open an existing entry (specified by id or partial id)
in an editor, so that it can be changed.

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
