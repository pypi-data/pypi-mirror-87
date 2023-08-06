from unittest import TestCase
from pear.file_formatter import FileFormatter, MissingLineError
from pear.loader import Line


class TestFileFormatter(TestCase):

    def test_remove_line_removes_line_from_position_in_list(self):
        expected = Line('second', 1)
        lines = [
            Line('first', 0),
            expected
        ]
        formatter = FileFormatter()
        output = formatter.remove(0, lines)

        self.assertEqual([expected], output)

    def test_remove_throws_exception_when_line_doesnt_exist(self):
        lines = [Line('first', 0)]
        formatter = FileFormatter()
        try:
            formatter.remove(1, lines)
            self.fail('Should throw exception')
        except MissingLineError:
            pass

    def test_insert_adds_given_line_to_lines(self):
        lines = [
            Line('first', 0),
            Line('third', 2),
        ]
        formatter = FileFormatter()

        output = formatter.insert(2, 'second', lines)
        expected = [
            Line('first', 0),
            Line('second'),
            Line('third', 2)
        ]

        self.assertEqual(expected, output)

    def test_insert_ignores_lines_with_no_line_number(self):
        lines = [
            Line('first', 1),
            Line('second'),
            Line('third', 3),
            Line('fifth', 5)
        ]
        formatter = FileFormatter()

        output = formatter.insert(4, 'fourth', lines)
        expected = [
            Line('first', 1),
            Line('second'),
            Line('third', 3),
            Line('fourth'),
            Line('fifth', 5)
        ]

        self.assertEqual(expected, output)
