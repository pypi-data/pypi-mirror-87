======
lesana
======

SYNOPSIS
========

lesana [--help] <command>

DESCRIPTION
===========

lesana is a tool to organize collections of various kinds.  It is
designed to have a data storage / serialization format that is friendly
to git and other VCSs, but decent performances.

To reach this aim it uses yaml_ as its serialization format, which is
easy to store in a VCS, share between people and syncronize between
different computers, but it also keeps an index of this data in a local
xapian_ database in order to allow for fast searches.

.. _yaml: http://yaml.org/
.. _xapian: https://xapian.org/

lesana supports collections of any kind, as long as their entries can be
described with a mostly flat dictionary of fields of the types described
in the documentation file ``field_types``.

Some example collection schemas are provided, but one big strength of
lesana is the ability to customize your collection with custom fields
either by simply writing a personalized ``settings.yaml``.

OPTIONS
=======

-h, --help
   Prints an help message and exits.

COMMANDS
========

new(1)
   Creates a new entry.
edit(1)
   Edits an existing entry.
show(1)
   Shows an existing entry.
index(1)
   Index some entries in the xapian cache.
search(1)
   Searches for entries in the xapian cache.
export(1)
   Exports entries from one lesana collection to another
init(1)
   Initialize a new lesana collection
rm(1)
   Removes an entry.

TEXT EDITOR
===========

Many lesana subcommands will try to open files in a text editor chosen
as follows:

* first, the value of $EDITOR is tried
* then the command ``sensible-editor``, as available under e.g. Debian
  and its derivatives
* lastly, it will try to fallback to ``vi``, which should be available
  under any posix system.
