***************
 Search syntax
***************

Searches in lesana use the human readable query string format defined by
xapian.

The simplest search is just a list of terms: e.g. searching for
``thing object`` will find entries where either ``thing`` or ``object``
is present in one of the fields with ``free`` indexing.

It is also possible to specify that a term must be in one specific
field: the syntax for this is the name of the field follwed by ``:`` and
the term, e.g. ``name:object`` will search for entries with the term
``object`` in the ``name`` field.

Search queries can of course include the usual logical operators
``AND``, ``OR`` and ``NOT``.

More modifiers are available; see the `Query Parser`_ documentation from
xapian for details.

.. _`Query Parser`: https://getting-started-with-xapian.readthedocs.io/en/latest/concepts/search/queryparser.html

