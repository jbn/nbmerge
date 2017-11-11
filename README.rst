.. image:: https://travis-ci.org/jbn/nbmerge.svg?branch=master
    :target: https://travis-ci.org/jbn/nbmerge
.. image:: https://ci.appveyor.com/api/projects/status/69kj3prrrieyp8q2/branch/master?svg=true
    :target: https://ci.appveyor.com/project/jbn/nbmerge/branch/master 
.. image:: https://coveralls.io/repos/github/jbn/nbmerge/badge.svg?branch=master
    :target: https://coveralls.io/github/jbn/nbmerge?branch=master 
.. image:: https://img.shields.io/pypi/v/nbmerge.svg
    :target: https://pypi.python.org/pypi/nbmerge
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/jbn/nbmerge/master/LICENSE
.. image:: https://img.shields.io/pypi/pyversions/nbmerge.svg
    :target: https://pypi.python.org/pypi/nbmerge


==================================================
``nbmerge``: merge / concatenate Jupyter notebooks
==================================================

Installation
============

.. code:: sh

    pip install nbmerge

Usage
=====

For the usage as originally specified by 
`@fperez <https://github.com/fperez>`__'s gist, 

.. code:: sh

    nbmerge file_1.ipynb file_2.ipynb file_3.ipynb > merged.ipynb

Alternatively, nbmerge can cursively collect all files in the current
directory and below, recursively. After collection, it sorts them
lexicographically. You can use a regular expression as a file name
predicate. All ``.ipynb_checkpoints`` are automatically ignored. And, you
can use the ``-i`` option to ignore any notebook prefixed with an underscore
(think pseudo-private in python). 

For example, the following command collects all notebooks in your project
that have the word ``intro`` in the file name and saves it to a merged file
named ``_merged.ipynb``,

.. code:: sh

    nbmerge --recursive -i -p ".*intro.*" -o _merged.ipynb

Finally, you can also instruct the script to demarcate the boundary
between each original file with the ``-b`` / ``-boundary [BOUNDARY]`` flag.
The ``src_nb`` value in the metadata for the first cell in each original
notebook will then contain the path of the original notebook, relative to
the cwd at the point of script execution.

More details
============

Read the docs: `here <http://nbmerge.falsifiable.com>`_.
