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


    def write(self, key, value, expire_at=0):
        input = {
            'data': value,
            'info': {
                'timestamp': time.time(),
                'expire_at': expire_at
            }
        }
        data = "'{}':{}".format(key, json.dumps(input, separators=(',', ':')))
        with open(self.file_location, 'a') as fd:
            fd.write(f'{data}\n')
        return True

    def read(self, key):
        searchkey = "'{}':".format(key)
        
        with open(self.file_location, 'r') as rfd:
            while True:
                line = rfd.readline()
                if not line:
                    break
                if line.startswith(searchkey, 0):
                    obj = json.loads(line.rsplit(searchkey)[1])
                    if self.is_expired(obj['info']):
                        return "Requested data expired"
                    
                    return obj['data']
            return "Key not found"

    def delete (self, key):
        pass

    def is_expired(self, info):
        if info['expire_at'] is 0:
            return False
        return (time.time() - info['timestamp'] > info['expire_at'])