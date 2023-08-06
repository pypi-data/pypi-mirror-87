from unittest import TestCase
from pear.replace import Replace
from pear.loader import Line
import json


class TestReplace(TestCase):
    def test_replaces_lines_with_given_lines(self):
        lines = [
            Line('first', 1),
            Line('first', 2),
            Line('first', 3)
        ]

        replacement_text = ['//comment']
        replace = Replace(replacement_text, 1, 3)

        output = replace.apply(lines)

        self.assertEqual([Line('//comment')], output)

    def test_from_json_builds_replace(self):

        src = json.loads("""
                {
                    "type": "replace",
                    "start": 1,
                    "end": 2,
                    "replacement": [
                        "// constructor"
                    ]
                }
        """)

        expected = Replace(['// constructor'], 1, 2)

        self.assertEqual(expected, Replace.from_json(src))
