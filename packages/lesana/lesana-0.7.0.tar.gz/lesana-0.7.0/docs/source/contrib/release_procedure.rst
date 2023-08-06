*******************
 Release procedure
*******************

* Check that the version number in setup.py is correct.

* Check that the changelog is up to date.

* Generate the distribution files::

     $ python3 setup.py sdist bdist_wheel

* Upload ::

     $ twine upload -s dist/*

* Tag the uploaded version::

     $ git tag -s v$VERSION -m "Version $VERSION"
     $ git push
     $ git push --tags

