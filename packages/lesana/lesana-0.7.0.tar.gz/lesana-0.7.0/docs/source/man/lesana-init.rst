===========
lesana-init
===========

SYNOPSIS
========

lesana init [--help] [--collection <collection>] [--no-git]

DESCRIPTION
===========

lesana init initializes a new lesana collection.

It will create the directory (if it does not exist) and, unless
``--no-git`` is specified it will initialize it as a git repository and
create a ``.gitignore`` file with some relevant contents.

It will then create a skeleton ``settings.yaml`` file and open it in an
editor to start configuring the collection.

When leaving the editor, again unless ``--no-git`` is used, it will add
this file to the git staging area, but not commit it.

OPTIONS
=======

--help, -h
   Prints an help message and exits.
--collection COLLECTION, -c COLLECTION
   The directory where the collection will be initialized. Default is .
--no-git
   Do not use git in the current collection.
