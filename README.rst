.. image:: https://travis-ci.org/jbn/nbmerge.svg?branch=master
    :target: https://travis-ci.org/jbn/nbmerge
.. image:: https://coveralls.io/repos/github/jbn/nbmerge/badge.svg?branch=master
    :target: https://coveralls.io/github/jbn/nbmerge?branch=master 
.. image:: https://img.shields.io/pypi/dm/nbmerge.svg
    :target: https://pypi.python.org/pypi/nbmerge
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


.. code:: sh

    nbmerge file_1.ipynb file_2.ipynb file_3.ipynb > merged.ipynb

Lineage
=======

`@fperez <https://github.com/fperez>`__ wrote an
`nbmerge.py <https://gist.github.com/fperez/e2bbc0a208e82e450f69>`__
script which "Merge[s]/concatenate[s] multiple IPython notebooks into
one." I use it a lot. Evidently, `other people do,
too <https://github.com/search?utf8=%E2%9C%93&q=nbmerge.py&type=Code>`__.
In early 2016, he opened an `issue to add the script as an nbconvert
tool <https://github.com/jupyter/nbconvert/issues/253>`__, but nothing
came of it. However, he and `@Carreau <https://github.com/carreau>`__ came up
with good (i.e. unsurprising) `semantics for metadata merging and
notebook
naming <https://github.com/jupyter/nbconvert/issues/253#issuecomment-187492911>`__:

.. code:: python

    metadata = {}
    for n in reversed(notebooks):
        metadata.update(n.metadata)


I don't think it's possible to implement the merger as a preprocessor.
Preprocessors are stateless, so you can't implement a reduce operation.
Instead, I wrote (er, packaged up) this library as an
`nbstripoutput <https://github.com/kynan/nbstripout>`__-like package . 
It fits in a ``Makefile`` script just fine. 

Right now, only the basic (originally fperez's) functionality is 
implemented. However, I'm going to follow 
`kynan's <https://github.com/kynan>`__ lead and slowly pull in functionality
similar to his ``nbstripout`` package.
