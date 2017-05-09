import os
import sys
import unittest

from tempfile import mkstemp
from nbformat import reads
from nbmerge import merge_notebooks, main, parse_plan, annotate_source_path


SELF_DIR = os.path.abspath(os.path.dirname(__file__))

FIXTURES_DIR = os.path.join(SELF_DIR, "fixtures")

TARGET_NBS = [os.path.join(FIXTURES_DIR, file_name + ".ipynb")
              for file_name in ("1_Intro", "2_Middle", "3_Conclusion")]


def file_names_from(file_paths):
        return [os.path.basename(f) for f in file_paths]


class TestMerge(unittest.TestCase):
    def setUp(self):
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")

    def _validate_merged_three(self, merged):
        self.assertEqual(len(merged.cells), 6)
        self.assertEqual(merged.metadata['test_meta']['title'], "Page 1")
        self.assertEqual(merged.metadata['final_answer'], 42)

    def test_merge_defaults(self):
        self._validate_merged_three(merge_notebooks(FIXTURES_DIR, TARGET_NBS))

    def test_merge_verbose(self):
        nb = merge_notebooks(FIXTURES_DIR, TARGET_NBS, verbose=True)
        self._validate_merged_three(nb)
        lines = sys.stdout.getvalue().splitlines()
        self.assertEqual(lines[0].strip(), "Merging notebooks...")
        for target, line in zip(TARGET_NBS, lines[1:4]):
            self.assertEqual(line.strip(), "Reading `{}`".format(target))

    def test_merge_with_boundary_key(self):
        nb = merge_notebooks(FIXTURES_DIR, TARGET_NBS, boundary_key='xxx')
        self._validate_merged_three(nb)
        self.assertEqual(nb.cells[0].metadata['xxx'], '1_Intro.ipynb')
        self.assertEqual(nb.cells[2].metadata['xxx'], '2_Middle.ipynb')
        self.assertEqual(nb.cells[4].metadata['xxx'], '3_Conclusion.ipynb')

    def test_parse_plan(self):
        header_nb = os.path.join(FIXTURES_DIR, "Header.ipynb")
        plan = parse_plan(["-o", "myfile.ipynb",
                           "-p", "(_|1|2)_.*",
                           "-i", "-r", "-v",
                           header_nb])

        self.assertEqual(file_names_from(plan['notebooks']),
                         ["Header.ipynb", "1_Intro.ipynb",
                          "1_Intro_In_Sub.ipynb", "2_Middle.ipynb"])
        self.assertTrue(plan["verbose"])
        self.assertEqual(plan["output_file"], "myfile.ipynb")
        with self.assertRaises(IOError):
            parse_plan(["this-file-doesn't-exist"])

    def test_annotate_source_path(self):
        nb_path = os.path.join(FIXTURES_DIR, "1_Intro.ipynb")
        with open(nb_path, "r") as fp:
            nb = reads(fp.read(), as_version=4)
        annotate_source_path(nb, SELF_DIR, nb_path, "xylophone")
        self.assertEqual(nb.cells[0].metadata['xylophone'],
                         os.path.join('fixtures', '1_Intro.ipynb'))

    def test_main_to_stdout(self):
        main(TARGET_NBS)
        self._validate_merged_three(reads(sys.stdout.getvalue(), as_version=4))

    def test_main_to_file(self):
        _, path = mkstemp()

        try:
            main(TARGET_NBS + ["-o", path])
            with open(path) as fp:
                self._validate_merged_three(reads(fp.read(), as_version=4))
        except:
            os.unlink(path)
