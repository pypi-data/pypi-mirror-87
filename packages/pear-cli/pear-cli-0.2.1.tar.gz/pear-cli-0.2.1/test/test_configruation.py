from pathlib import Path
from unittest import TestCase
from pear.configuration import Configuration
from pear.replace import Replace
from pear.remove import Remove


class TestConfiguration(TestCase):
    def test_parses_file(self):
        config = Configuration(Path('test/files/config.json'))
        self.assertEqual('test/files/Test.java',
                         config.input['files'][0]['path'])
        self.assertEqual('out', config.input['out'])
        self.assertEqual('tag', config.input['files'][0]['tag'])

    def test_files_maps_remove_correctly(self):
        files = Configuration(Path('test/files/config_replace.json')).files()
        self.assertIsInstance(files[0].formatters[0], Replace)

    def test_files_maps_replace_correctly(self):
        files = Configuration(Path('test/files/config_remove.json')).files()
        self.assertIsInstance(files[0].formatters[0], Remove)
