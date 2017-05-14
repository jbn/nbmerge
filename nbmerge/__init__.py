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
__version__ = "0.0.4"

# See Readme.rst for ancestry. My role is mostly packaging this up for
# PyPI. The author is truely Fernando Perez (@fperez).
__author__ = "John Bjorn Nelson"
__email__ = "jbn@abreka.com"


def annotate_source_path(notebook, base_dir, nb_path, boundary_key):
    """
    Add the notebook's relative path to the cell metadata.

    :param notebook: the parsed notebook object
    :param base_dir: the base directory for this merge
    :param nb_path: the file path to the notebook
    :param boundary_key: the target key in the meatadata dictionary
    """
    cells = notebook.cells
    if cells:
        cells[0].metadata[boundary_key] = os.path.relpath(nb_path, base_dir)


def merge_notebooks(base_dir, file_paths, verbose=False, boundary_key=None):
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

    :param base_dir: the base directory for recursion and relative path
        calculation
    :param file_paths: the ordered file paths to the notebooks for
        concatenation
    :param boundary_key: the key in the first cells metadata where the
        source file_path goes
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

        if boundary_key:
            annotate_source_path(nb, base_dir, path, boundary_key)

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


def recursive_find(base_dir, ignore_underscored, predicate_re):
    """
    Find notebooks relative to the base dir which match the filtering criteria.

    :param base_dir: the base directory for the search
    :param ignore_underscored: filter out all notebooks which begin with
        an underscore prefix, irrespective of the predicate regexp
    :param predicate_re: a filter for file name acceptance
    :return: lexicographically ordered list of notebook file paths
    """
    predicate_re = re.compile(predicate_re or ".*")

    file_paths = []

    for dir_path, dir_names, file_names in os.walk(base_dir):
        # I can't think of a scenario where you'd ever want checkpoints.
        if os.path.basename(dir_path) == ".ipynb_checkpoints":
            continue

        for file_name in file_names:
            if not file_name.endswith(".ipynb"):
                continue

            if ignore_underscored and file_name.startswith('_'):
                continue

            if not predicate_re.match(file_name):
                continue

            file_paths.append(os.path.join(dir_path, file_name))

    return sorted(file_paths)  # For lexicographic sorting


def parse_plan(args=None, base_dir=None):
    """
    Parse the command line arguments and produce an execution plan.
    """
    if base_dir is None:
        base_dir = os.getcwd()

    parser = argparse.ArgumentParser(prog="nbmerge",
                                     description=__description__)

    parser.add_argument("-o", "--output",
                        help="Write to the specified file")

    parser.add_argument("-b", "--boundary",
                        help="Add boundary metadata to header cells" +
                             "(optionally by given key)",
                        nargs="?",
                        const="src_nb")
    parser.add_argument("-i", "--ignore-underscored",
                        help="Ignore notebooks with underscore prefix",
                        action="store_true")
    parser.add_argument("-r", "--recursive",
                        help="Merge all notebooks in subdirectories",
                        action="store_true")
    parser.add_argument("-p", "--predicate-re",
                        help="Regexp for filename acceptance")
    parser.add_argument("-v", "--verbose",
                        help="Print progress as processing",
                        action="store_true")

    parser.add_argument("files",
                        help="Paths to files to merge",
                        nargs="*")

    args = parser.parse_args(args)

    file_paths = args.files[:]

    if not file_paths and not args.recursive:
        parser.print_help()
        sys.exit(1)

    for file_path in file_paths:
        if not os.path.exists(file_path):
            raise IOError("Notebook `{}` does not exist".format(file_path))

    if args.recursive:
        # If you specify any files, they are added first, in order.
        # This is useful for a header notebook of some sort.
        file_paths.extend(recursive_find(base_dir,
                                         args.ignore_underscored,
                                         args.predicate_re))
    return {'notebooks': file_paths,
            'base_dir': base_dir,
            'output_file': args.output,
            'boundary_key': args.boundary,
            'verbose': args.verbose}


def main(args=None):
    plan = parse_plan(args)

    nb = merge_notebooks(plan['base_dir'],
                         plan['notebooks'],
                         plan['verbose'],
                         plan['boundary_key'])

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
