from pathlib import Path
from unittest import TestCase
from pear.collapse import CollapsePath


class TestCollapsPath(TestCase):

    def test_collapses_path_to_underscores(self):
        path = Path('test/files/Test.java')
        collapse = CollapsePath('_')

        result = collapse.apply(path)
        expected = Path('test_files_Test.java')

        self.assertEqual(result, expected)
