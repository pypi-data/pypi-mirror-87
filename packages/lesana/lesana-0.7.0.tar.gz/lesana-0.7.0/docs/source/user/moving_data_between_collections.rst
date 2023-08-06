*******************************
Moving Data between Collections
*******************************

Entries can be exported from a lesana collection to another using the
``lesana export`` command and a jinja2 template.

The template should generate a yaml file that is a valid lesana entry
for the destination collection and it can use the fields of the starting
collection as variables. The variable ``entry`` is also available and
gives complete access to the entry of the original collection, so fields
with names that aren't valid jinja templates can be accessed as
``entry.data[<field-name>]``.

E.g. to convert between a collection with fields ``name``,
``short-desc``, ``desc`` to a collection with fields ``name``,
``description`` one could use the following template::

   name: {{ name }}
   description: |
       {{ entry.data.[short-desc] }}

       {{ desc | indent(width=4, first=False) }}

From the origin collection you can then run the command::

   lesana export <path/to/destination/collection> <path/to/template>

to export all entries.

You can also export just a subset of entries by adding a xapian query
with the parameter ``--query``; you can test the search using::

   lesana search --all <some search terms>

and then actually run the export with::

   lesana search --query '<some search terms>' <destination> <template>

note that in this second command the spaces in the search query have to
be protected from the shell.
