import unittest
import json_file_handler

class TestJsonFileHandler(unittest.TestCase):

    def setUp(self):
        self.jfh = json_file_handler.JsonFileHandler()

    def test_write(self):
        result = self.jfh.write('test', ['Hello world'])
        self.assertEqual(result, {'test': ['Hello world']})
        pass

    def test_read(self):
        result = self.jfh.read('test')
        self.assertEqual(result, {'test': ['Hello world']})
        pass

    def test_delete(self):
        self.assertTrue(self.jfh.delete('test'))
        pass