******************************
Getting Started (Command Line)
******************************

lesana can be used from the command line through the ``lesana`` command;
for more details run ``lesana help``.

Many commands will try to open some file in an editor: they will attempt
to use, in this order, ``$EDITOR``, ``sensible-editor`` or as a fallback
``vi``, which should be installed on any POSIX-like system.

To start a new collection, create a directory and run ``lesana
init`` into it::

    mkdir $DIRECTORY
    cd $DIRECTORY
    lesana init

It will create the basic file structure of a lesana collection,
including a ``settings.yaml`` skeleton and it will initialize a git
repository (use ``--no-git`` to skip this part and ignore all further
git commands).

It will then open ``settings.yaml`` in an editor: fill in your list of
fields and all other data, save and exit.
You are now ready to commit the configuration for your new collection::

    git commit -m 'Collection settings'

An empty collection is not very interesting: let us start adding new
entries::

   lesana new

It will again open an editor on a skeleton of entry where you can fill
in the values. When you close the editor it will print the entry id,
that you can use e.g. to edit again the same entry::

   lesana edit $ENTRY_ID

After you've added a few entries, you can now search for some word that
you entered in one of the indexed fields::

   lesana search some words

this will also print the entry ids of matching items, so that you can
open them with ``lesana edit``.

If you're using git, entries will be autoadded to the staging area, but
you need to commit them, so that you can choose how often you do so.

Search results are limited by default to 12 matches; to get all results
for your query you can use the option ``--all``. This is especially
useful when passing the results to a template::

   lesana search --template templates/my_report.html --all \
       some search terms \
       > some_search_terms-report.html

will generate an html file based on the jinja2 template
``templates/my_report.html`` with all the entries found for those search
terms.
