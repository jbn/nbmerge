from __future__ import print_function
import argparse
import io
import re
import os
import sys

from nbformat import read as read_notebook
from nbformat import write as write_notebook


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


def merge_notebooks(file_paths, verbose=False):
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

    :param file_paths: the ordered file paths to the notebooks for
        concatenation
    :param verbose: if True, print message for each notebook when processing
    :return: the merged notebook
    """
    merged, metadata = None, []

    if verbose:
        print("Merging notebooks...")

    for path in file_paths:
        with io.open(path, 'r', encoding='utf-8') as fp:
            if verbose:
                print("\tReading `{}`".format(path))
            nb = read_notebook(fp, as_version=4)

        metadata.append(nb.metadata)

        if merged is None:
            merged = nb
        else:
            merged.cells.extend(nb.cells)

    if verbose:
        print("Merging metadata in reverse order...")

    merged_metadata = {}
    for meta in reversed(metadata):
        merged_metadata.update(meta)
    merged.metadata = merged_metadata

    return merged


def recursive_find(ignore_underscored, filter_re):
    """
    Find all notebooks relative to the cwd which match the filtering criteria.

    :param ignore_underscored: filter out all notebooks which begin with
        an underscore prefix, irrespective of the filter regexp
    :param filter_re: a filter for file name acceptance
    :return: lexicographically ordered list of notebook file paths
    """
    filter_re = re.compile(filter_re or ".*")

    file_paths = []

    for dir_path, dir_names, file_names in os.walk(os.getcwd()):
        # I can't think of a scenario where you'd ever want checkpoints.
        if os.path.basename(dir_path) == ".ipynb_checkpoints":
            continue

        for file_name in file_names:
            if not file_name.endswith(".ipynb"):
                continue

            if ignore_underscored and file_name.startswith('_'):
                continue

            if not filter_re.match(file_name):
                continue

            file_paths.append(os.path.join(dir_path, file_name))

    return sorted(file_paths)  # For lexicographic sorting


def parse_plan(args=None):
    """
    Parse the command line arguments and produce an execution plan.
    """
    parser = argparse.ArgumentParser("Merge a set of notebooks into one.")

    parser.add_argument("files",
                        help="Paths to files to merge",
                        nargs="*")

    parser.add_argument("-o", "--output",
                        help="Write to the specified file")

    parser.add_argument("-f", "--filter-re",
                        help="Regexp for filename acceptance")
    parser.add_argument("-i", "--ignore-underscored",
                        help="Ignore notebooks with underscore prefix",
                        action="store_true")
    parser.add_argument("-r", "--recursive",
                        help="Merge all notebooks in subdirectories",
                        action="store_true")
    parser.add_argument("-v", "--verbose",
                        help="Print progress as processing",
                        action="store_true")

    args = parser.parse_args(args)

    file_paths = args.files[:]
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print("Notebook `{}` does not exist".format(file_path))
            sys.exit(1)

    if args.recursive:
        # If you specify any files, they are added first, in order.
        # This is useful for a header notebook of some sort.
        file_paths.extend(recursive_find(args.ignore_underscored,
                                         args.filter_re))
    return {'notebooks': file_paths,
            'output_file': args.output,
            'verbose': args.verbose}


def main():
    plan = parse_plan()

    nb = merge_notebooks(plan['notebooks'])

    if plan['output_file'] is None:
        # See:
        # - http://stackoverflow.com/a/1169209
        # - http://github.com/kynan/nbstripout/commit/8e26f4df
        # import codecs
        # write_notebook(nb, codecs.getwriter('utf8')(sys.stdout))
        write_notebook(nb, sys.stdout)
    else:
        with io.open(plan['output_file'], 'w', encoding='utf8') as fp:
            write_notebook(nb, fp)
