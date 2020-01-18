# import multiprocessing
import threading
# import os

class JsonFileHandler():
    
    def __init__(self):
        self.lock = threading.Lock()
        # self.file_location = 'data.json'

        # if not os.path.exists(self.file_location):
        #     with open(self.file_location, 'w'):
        #         pass


    def write(self, key, value):
        pass

    def read(self, key):
        pass

    def delete (self, key):
        pass