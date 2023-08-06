===========
lesana-show
===========

SYNOPSIS
========

lesana show [--help] [--collection COLLECTION] [--template TEMPLATE] <entry>

DESCRIPTION
===========

``lesana show`` will print an entry (specified by id or partial id) to
stdout.

A template can be specified with ``--template <template>`` to pretty
print entries.

OPTIONS
=======

-h, --help
   Prints an help message and exits.
--collection COLLECTION, -c COLLECTION
   The collection to work on. Default is ``.``
--template TEMPLATE, -t TEMPLATE
   Use the specified template to display results.

TEMPLATES
=========

The templates used by ``lesana show`` are jinja2 templates.

The entry fields are available as variables, and the full entry is
available as the variable ``entry`` and can be used to give access to
fields with names that aren't valid jinja2 variables e.g. as
``entry.data[<field-name>]``.

