import unittest
import random
import string
import time

import json_file_handler

class TestJsonFileHandler(unittest.TestCase):

    def setUp(self):
        self.jfh = json_file_handler.JsonFileHandler('unittest')

    def test_create(self):
        result = self.jfh.create('unittest', '{"Hello": "World"}')
        self.assertEqual(result, 'Created successfully')

        result = self.jfh.create('unittest', '{"Hello": "World"}')
        self.assertEqual(result, 'Key already exist')

        result = self.jfh.create('', '{"Hello": "World"}')
        self.assertEqual(result, 'The min and max length of the key parameter are 1 to 32')
        
        result = self.jfh.create(self.randomString(33), '{"Hello": "World"}')
        self.assertEqual(result, 'The min and max length of the key parameter are 1 to 32')

        result = self.jfh.create(None, '{"Hello": "World"}')
        self.assertEqual(result, 'Data type of key should be string')

        result = self.jfh.create('unittest1', '')
        self.assertEqual(result, 'Parameter of value should be string and can not be empty')

        result = self.jfh.create('unittest1', self.randomString(16001))
        self.assertEqual(result, 'The max size of the value is 16 KB')

        result = self.jfh.create('unittest1', None)
        self.assertEqual(result, 'Parameter of value should be string and can not be empty')

    def test_read(self):
        self.jfh.create('readtest', '{"Hello": "World"}')
        result = self.jfh.read('readtest')
        self.assertEqual(result, '{"Hello": "World"}')

        result = self.jfh.read('notfoundkey')
        self.assertEqual(result, 'Key not found')

        self.jfh.create('testexpire', '{"Hello": "World"}', 1)
        time.sleep(1)
        result = self.jfh.read('testexpire')
        self.assertEqual(result, 'Requested key expired')

    def test_delete(self):
        self.jfh.create('deletetest', '{"Hello": "World"}')
        self.assertEqual(self.jfh.delete('deletetest'), "Deleted successfully")

        self.assertEqual(self.jfh.delete('keynotexist'), "Key not exist")
        
        self.jfh.create('keyexpired', '{"Hello": "World"}', 1)
        time.sleep(1)
        self.assertEqual(self.jfh.delete('keyexpired'), "Requested key expired")

    def tearDown(self):
        open('unittest', 'w').close()
        # pass
    
    def randomString(self, stringLength):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))


