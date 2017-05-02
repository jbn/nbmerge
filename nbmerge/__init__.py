from __future__ import print_function
import codecs
import io
import sys

from nbformat import read as read_notebook
from nbformat import write as write_notebook

# See:
# - stackoverflow.com/a/1169209
# - github.com/kynan/nbstripout/commit/8e26f4df317fde8b935df8e4930b32c74f834cf9
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

__title__ = "nbmerge"
__description__ = "A tool to merge / concatenate Jupyter (IPython) notebooks"
__uri__ = "https://github.com/jbn/nbmerge"
__doc__ = __description__ + " <" + __uri__ + ">"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2017 John Bjorn Nelson"
__version__ = "0.0.1"

# See Readme.rst for ancestry. My role is mostly packaging this up for
# PyPI. The author is truely Fernando Perez (@fperez).
__author__ = "John Bjorn Nelson"
__email__ = "jbn@abreka.com"


def merge_notebooks(file_paths):
    """
    Merge the given notebooks into one notebook.

    This function aggregates metadata in reverse order relative to the
    ``file_paths``. It does not do so recursively. Concretely, the first
    notebook will overwrite any keys in the metadata for notebooks 2 and
    on; the second notebook will overwrite any keys in the metadata for
    notebooks 3 and on; and so forth. If the second notebook has a key
    path of metadata.ns.x which does not exist in the first notebook,
    but the first notebook has a key path of metadata.ns.y, the second
    data's entry is overwritten. It does not recursively descend into
    the dictionaries.
    """
    merged, metadata = None, []

    for path in file_paths:
        with io.open(path, 'r', encoding='utf-8') as fp:
            nb = read_notebook(fp, as_version=4)

        metadata.append(nb.metadata)

        if merged is None:
            merged = nb
        else:
            merged.cells.extend(nb.cells)

    merged_metadata = {}
    for meta in reversed(metadata):
        merged_metadata.update(meta)
    merged.metadata = merged_metadata

    return merged


def main():
    notebooks = sys.argv[1:]
    if not notebooks:
        print("Usage: nbconvert a.ipynb b.ipynb > merged.ipynb",
              file=sys.stderr)
        sys.exit(1)

    nb = merge_notebooks(notebooks)
    write_notebook(nb, sys.stdout)
