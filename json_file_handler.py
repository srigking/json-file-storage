# import multiprocessing
import threading
import os
import json
import time

class JsonFileHandler():
    """
    Create, read and delete JSON object from a file.

    Parameters
    ----------
    file_location : str
        Location of the file. A new file will be created if the given file not exist.
        Default location is current directory with the file name `data.txt`
    """

    def __init__(self, file_location='data.txt'):
        self.lock = threading.Lock()
        self.file_location = file_location

        # Check the file exist
        if not os.path.exists(self.file_location):
            try:
                # Create file if not exist
                fd = open(self.file_location, 'w')
                fd.close()
            except:
                print("This dir is not exist")
                exit()


    def create(self, key, value, expire_at=0):
        """
        This function store the JSON object with the given `key` `value` pair.

        Parameters
        ----------
        key : str
            Key value to store the JSON object
        value : str
            Body of the JSON object
        expire_at : int
            The key will no longer can be read or delete. 
            If the value is 0, the key will not expire
            Default value is 0

        Returns
        -------
        str
            On success, the function returns `Created successfully` message.

        """
        
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

        with self.lock:
            if self.is_exist(key):
                return "Key already exist"

            with open(self.file_location, 'a') as fd:
                fd.write(f'{data}\n')
                return "Created successfully"
            return "Failed to create"

    def read(self, key):
        """
        This function find and get the JSON object by using the given `key`.

        Parameters
        ----------
        key : str
            Key of JSON object

        Returns
        -------
        str
            On success, the function returns the JSON object.
            If the given key not in the file, the function returns `Key not found`
            If the given key time expired, the function returns `Requested key expired`

        """
        searchkey = self.generate_search_key(key) # To compare only the key
        with self.lock:
            line = self.search(searchkey)
            if line:
                obj = json.loads(line.rsplit(searchkey)[1])
                if self.is_expired(obj['info']):
                    return "Requested key expired"
                return obj['data']
            return "Key not found"

    def delete (self, key):
        """
        This function delete the JSON object by using the given `key`.
        If the given key is expired, the function will not allow to delete the key.

        Parameters
        ----------
        key : str
            Key of JSON object

        Returns
        -------
        str
            On success, the function returns `Deleted successfully` message.
            If the given key not in the file, the function returns `Key not exist`
            If the given key time expired, the function returns `Requested key expired`

        """
        with self.lock:
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
        return None

    def is_exist(self, key):
        searchkey = self.generate_search_key(key)
        line = self.search(searchkey)
        if line:
            return True
        else:
            return False

    def search(self, searchkey):
        with open(self.file_location, 'r') as fd:
            while True: # Read line by line
                line = fd.readline()
                if not line:
                    break
                if line.startswith(searchkey, 0):
                    return line
        return False

    def generate_search_key(self, key):
        return "'{}':".format(key)

    def is_expired(self, info):
        if info['expire_at'] is 0:
            return False
        return (time.time() - info['timestamp'] > info['expire_at'])