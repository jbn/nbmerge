import os
import sys
import unittest

from nbformat import reads
from nbmerge import merge_notebooks, main


SELF_DIR = os.path.abspath(os.path.dirname(__file__))

FIXTURES_DIR = os.path.join(SELF_DIR, "fixtures")

TARGET_NBS = [os.path.join(FIXTURES_DIR, file_name + ".ipynb")
              for file_name in ("1_Intro", "2_Middle", "3_Conclusion")]


class TestMerge(unittest.TestCase):
    def _validate_merged_three(self, merged):
        self.assertEqual(len(merged.cells), 6)
        self.assertEqual(merged.metadata['test_meta']['title'], "Page 1")
        self.assertEqual(merged.metadata['final_answer'], 42)

    def test_merge(self):
        self._validate_merged_three(merge_notebooks(TARGET_NBS))

    def test_main(self):
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")

        prior_args = sys.argv

        try:
            sys.argv = ['nbmerge'] + TARGET_NBS
            main()
        finally:
            sys.argv = prior_args

        self._validate_merged_three(reads(sys.stdout.getvalue(), as_version=4))
