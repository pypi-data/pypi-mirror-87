=============
lesana-search
=============

SYNOPSIS
========

lesana search [--help] [--collection COLLECTION] [--template TEMPLATE] \
  [--offset OFFSET] [--pagesize PAGESIZE] [--all] \
  [--sort FIELD1 [--sort FIELD2 ...]] query [query ...]

DESCRIPTION
===========

Lesana search allows to make searches in the collection and render the
results.

The section :doc:`/user/search` in the full documentation describes
the query syntax in more detail; it is available online at
https://lesana.trueelena.org/user/search.html or it may be installed on
your system (e.g. in Debian and derivatives it will be at
``/usr/share/doc/lesana/html/user/search.html``).

By default entries are printed according to the ``entry_label`` from the
``settings.yaml`` file, but they can be rendered according to a jinja2
template.

OPTIONS
=======

-h, --help
   Prints an help message and exits.
--collection COLLECTION, -c COLLECTION
   The collection to work on. Default is ``.``
--template TEMPLATE, -t TEMPLATE
   Template to use when displaying results
--offset OFFSET
   .
--pagesize PAGESIZE
   .
--all
   Return all available results
--sort
   Sort the results by a sortable field.

   This option can be added multiple times; prefix the name of the field
   with ``-`` to reverse the results (e.g. ``--sort='-date'``).

