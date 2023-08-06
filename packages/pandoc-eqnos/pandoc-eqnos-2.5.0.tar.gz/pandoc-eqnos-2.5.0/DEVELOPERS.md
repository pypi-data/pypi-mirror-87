
Developer Notes
===============

Contributions
-------------

Contributions to pandoc-eqnos are welcome.  Before implementing a new feature, it is best to discuss it in an Issue so that any potential problems can be resolved.  Pull Requests should be linked into the Issue when ready.


Design Philosophy
-----------------

1. This should be easy.

2. Features should be supported for *ALL* output formats.

3. The native capabilities of each output format should be employed.


Branches
--------

The next release is developed in the `nextrelease` branch.  When ready, the changes are merged into the `master` branch.

A copy of the 1.x release series is maintained in the 1.x branch.

Demo outputs are stored in the `demos` branch.


Install Alternatives
--------------------

Installing from source may require upgrading `setuptools` by executing

    pip install --upgrade setuptools

as root (or under sudo).

There are a few different options for installing from source:
    
1) To install from the github `master` branch use:

       pip install git+https://github.com/tomduck/pandoc-eqnos.git --user

   (to upgrade append the `--upgrade` flag).

2) To install from the `nextrelease` branch on github, use

       pip install git+https://github.com/tomduck/pandoc-eqnos.git@nextrelease --user

   (to upgrade use the --upgrade flag).

3) To install from a local source distribution, `cd` into its root
   and use

       pip install -e . --user

   Note that any changes made to the source will be automatically
   reflected when the filter is run (which is useful for development).


Testing
-------

Regression tests for pandoc-eqnos are provided in `test/`.  Read the README.md in that directory for instructions.


Preparing a Release
-------------------

These are notes for release managers.


### Merging ####

Merge the `nextrelease` branch into `master` using

    git checkout master
    git merge nextrelease
    git push


### Updating Demos ###

Starting from the root of the `master` branch, update demos in the `demos` branch using

    cd demos
    make -B
    git checkout demos
    cp -rf out/* ..
    git commit --amend -am "Updated demos."
    git push --force

This procedure ensures that there will only be a single revision of each file (see https://stackoverflow.com/a/22827188).


### Tagging ###

See https://www.python.org/dev/peps/pep-0440/ for numbering conventions, including for pre-releases.

Check that you are in the `master` branch.

Tagging  (update the version number):

    git tag -a 2.5.0 -m "New release."
    git push origin 2.5.0


### Distributing ###

Create source and binary distributions using

    python3 setup.py sdist bdist_wheel

(see https://packaging.python.org/tutorials/packaging-projects/).
    
Upload to pypi (update the version number) using

    twine upload dist/pandoc-eqnos-2.5.0.tar.gz \
                 dist/pandoc_eqnos-2.5.0-py3-none-any.whl

(see https://pypi.python.org/pypi/twine).
