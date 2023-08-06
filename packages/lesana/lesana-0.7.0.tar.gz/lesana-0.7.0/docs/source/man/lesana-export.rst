=============
lesana-export
=============

SYNOPSIS
========

lesana export [-h] [--collection COLLECTION] [--query QUERY] destination template

DESCRIPTION
===========

Lesana export converts entries from one lesana collection to another,
using a jinja2 template.

OPTIONS
=======

-h, --help
   Prints an help message and exits.
--collection COLLECTION, -c COLLECTION
   The collection to work on. Default is ``.``
--query QUERY, -q QUERY
   Xapian query to search in the collection

