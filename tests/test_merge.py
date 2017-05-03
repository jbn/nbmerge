import os
import sys
import unittest

from nbformat import reads
from nbmerge import merge_notebooks, main, parse_plan


SELF_DIR = os.path.abspath(os.path.dirname(__file__))

FIXTURES_DIR = os.path.join(SELF_DIR, "fixtures")

TARGET_NBS = [os.path.join(FIXTURES_DIR, file_name + ".ipynb")
              for file_name in ("1_Intro", "2_Middle", "3_Conclusion")]


def file_names_from(file_paths):
        return [os.path.basename(f) for f in file_paths]


class TestMerge(unittest.TestCase):
    def _validate_merged_three(self, merged):
        self.assertEqual(len(merged.cells), 6)
        self.assertEqual(merged.metadata['test_meta']['title'], "Page 1")
        self.assertEqual(merged.metadata['final_answer'], 42)

    def test_merge(self):
        self._validate_merged_three(merge_notebooks(TARGET_NBS))

    def test_parse_plan(self):
        header_nb = os.path.join(FIXTURES_DIR, "Header.ipynb")
        plan = parse_plan(["-o", "myfile.ipynb",
                           "-f", "(_|1|2)_.*",
                           "-i", "-r", "-v",
                           header_nb])

        self.assertEqual(file_names_from(plan['notebooks']),
                         ["Header.ipynb", "1_Intro.ipynb",
                          "1_Intro_In_Sub.ipynb", "2_Middle.ipynb"])
        self.assertTrue(plan["verbose"])
        self.assertEqual(plan["output_file"], "myfile.ipynb")

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
