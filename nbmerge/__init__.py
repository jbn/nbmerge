import io
import sys

from nbformat import read as read_notebook
from nbformat import writes as nb_to_str

__title__ = "nbmerge"
__description__ = "A tool to merge / concatenate Jupyter (IPython) notebooks"
__uri__ = "https://github.com/jbn/nbmerge"
__doc__ = __description__ + " <" + __uri__ + ">"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2017 John Bjorn Nelson"
__version__ = "0.0.1.dev0"

# See Readme.rst for ancestry. My role is mostly packaging this up for
# PyPI. The author is truely Fernando Perez (@fperez).
__author__ = "John Bjorn Nelson"
__email__ = "jbn@abreka.com"


def merge_notebooks(file_paths):
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
    print(nb_to_str(nb))
