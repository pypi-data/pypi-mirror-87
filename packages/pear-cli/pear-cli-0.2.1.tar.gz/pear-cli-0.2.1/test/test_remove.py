from unittest import TestCase
from pear.remove import Remove
from pear.file_formatter import Line


class TestRemove(TestCase):

    def test_removes_lines_from_list(self):
        remove = Remove(0, 2)

        lines = [
            Line('first', 0),
            Line('first', 1),
            Line('first', 2)
        ]

        output = remove.apply(lines)

        self.assertEqual([], output)

    def test_doesnt_remove_from_given_list(self):
        remove = Remove(0, 2)

        lines = [
            Line('first', 0),
            Line('first', 1),
            Line('first', 2)
        ]

        remove.apply(lines)

        self.assertEqual(3, len(lines))
