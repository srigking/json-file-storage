import unittest
import random
import string
import time

import json_file_handler

class TestJsonFileHandler(unittest.TestCase):

    def setUp(self):
        self.jfh = json_file_handler.JsonFileHandler()

    def test_write(self):
        result = self.jfh.write('unittest', '{"Hello": "World"}')
        self.assertTrue(result)
        
        #case 2 Check the size of the value
        # letters = string.ascii_lowercase
        # value = ''.join(random.choice(letters) for i in range(10))


    def test_read(self):
        self.jfh.write('readtest', '{"Hello": "World"}')
        result = self.jfh.read('readtest')
        self.assertEqual(result, '{"Hello": "World"}')

        result = self.jfh.read('notfoundkey')
        self.assertEqual(result, 'Key not found')

        self.jfh.write('testexpire', '{"Hello": "World"}', 1)
        time.sleep(1)
        result = self.jfh.read('testexpire')
        self.assertEqual(result, 'Requested data expired')

    def test_delete(self):
        self.assertTrue(self.jfh.delete('test'))
        pass