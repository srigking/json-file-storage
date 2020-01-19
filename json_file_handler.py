# import multiprocessing
import threading
import os
import json
import time
from file_lock import FileLock

file = FileLock()

class JsonFileHandler():
    """
    Create, read and delete JSON object from a file.

    Parameters
    ----------
    file_location : str
        Location of the file. A new file will be created if the given file not exist.
        Default location is current directory with the file name `data.txt`
    debug : boolean
        Enable or disable debug messages. Default is False
    """

    def __init__(self, file_location='data.txt', debug = False):
        # self.lock = threading.Lock()
        self.file_location = file_location
        self._debug = debug

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
            The minimum length is 1 and maximum length is 32
        value : str
            Body of the JSON object. The maximum allowed size of the JSON object is 16 KB
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

        if len(value.encode('utf-8')) > 16000: # more than 16 KB
            return "The max size of the value is 16 KB"

        
        if not isinstance(key, str):
            return "Data type of key should be string"

        if len(key) < 1 or len(key) > 32:
            return "The min and max length of the key parameter are 1 to 32"


        input = {
            'data': value,
            'info': {
                'timestamp': time.time(),
                'expire_at': expire_at # in secs
            }
        }
        data = "'{}':{}".format(key, json.dumps(input, separators=(',', ':')))

        if self._debug:
            print('Create: waiting lock name: {}'.format(threading.current_thread().name))

        with file.write_locked():
            if self._debug:
                print('Create: lock acquired name: {}'.format(threading.current_thread().name))

            if (os.path.getsize(self.file_location)/(1024*1024.0)) > 1023: # 1023 - this will prevent by not reaching 1 GB file
                return "Maximum 1 GB file size reached"

            if self.is_exist(key):
                return "Key already exist"

            with open(self.file_location, 'a') as fd:
                fd.write(f'{data}\n')

                if self._debug:
                    print('Create: lock released name: {}'.format(threading.current_thread().name))

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

        if self._debug:
            print('Read: waiting lock name: {}'.format(threading.current_thread().name))

        with file.read_locked():
            if self._debug:
                print('Read: lock acquired name: {}'.format(threading.current_thread().name))

            line = self.search(searchkey)
            if line:
                obj = json.loads(line.rsplit(searchkey)[1])
                if self.is_expired(obj['info']):
                    return "Requested key expired"
                
                if self._debug:
                    print('Read: lock released name: {}'.format(threading.current_thread().name))

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
        if self._debug:
            print('Delete: waiting lock name: {}'.format(threading.current_thread().name))
        with file.write_locked():
            if self._debug:
                print('Delete: lock acquired name: {}'.format(threading.current_thread().name))

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
                            if self._debug:
                                print('Delete: lock released name: {}'.format(threading.current_thread().name))

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