# import multiprocessing
import threading
import os
import json
import time

class JsonFileHandler():

    def __init__(self, file_location='data.txt'):
        self.lock = threading.Lock()
        self.file_location = file_location

        if not os.path.exists(self.file_location):
            with open(self.file_location, 'w'):
                pass


    def create(self, key, value, expire_at=0):
        """
        TODO
        key: Key value to store the JSON object
        value: JSON object
        expire_at: 0 in sec
        """

        if self.is_exist(key):
            return "Key already exist"
        
        if not isinstance(value, str) or len(value) < 1:
            return "Parameter of value should be string and can not be empty"
        
        if not isinstance(key, str) or len(key) < 1:
            return "Parameter of key should be string and can not be empty"

        input = {
            'data': value,
            'info': {
                'timestamp': time.time(),
                'expire_at': expire_at # in secs
            }
        }
        data = "'{}':{}".format(key, json.dumps(input, separators=(',', ':')))

        with open(self.file_location, 'a') as fd:
            fd.write(f'{data}\n')
        return True

    def read(self, key):
        searchkey = self.generate_search_key(key) # To compare only the key
        
        with open(self.file_location, 'r') as fd:
            while True: # Read line by line
                line = fd.readline()
                if not line:
                    break
                if line.startswith(searchkey, 0):
                    obj = json.loads(line.rsplit(searchkey)[1])
                    if self.is_expired(obj['info']):
                        return "Requested key expired"
                    
                    return obj['data']
            return "Key not found"

    def delete (self, key):
        file_data = self.read_file()
        key_status = "Key not exist"

        with open(self.file_location, 'w') as fd:
            searchkey = self.generate_search_key(key) # To compare only the key
            for line in file_data:
                if line.startswith(searchkey, 0):
                    obj = json.loads(line.rsplit(searchkey)[1])
                    if self.is_expired(obj['info']):
                        # Once the TTL for a key has expired, the key will no longer be available for Read or Delete operations.
                        fd.write(line) 
                        key_status = "Requested key expired"
                    else:
                        key_status = "Deleted successfully"
                else:
                    fd.write(line)
        return key_status


    def read_file(self):
        with open(self.file_location, 'r') as fd:
            return fd.readlines()

    def is_exist(self, key):
        searchkey = self.generate_search_key(key)
        with open(self.file_location, 'r') as fd:
            while True: # Read line by line
                line = fd.readline()
                if not line:
                    break
                if line.startswith(searchkey, 0):
                    return True
        
        return False
    
    def generate_search_key(self, key):
        return "'{}':".format(key)


    def is_expired(self, info):
        if info['expire_at'] is 0:
            return False
        return (time.time() - info['timestamp'] > info['expire_at'])