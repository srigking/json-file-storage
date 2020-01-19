from contextlib import contextmanager
from threading import Lock

class FileLock():
    def __init__(self):
        self.write_lock = Lock()
        self.num_read_lock = Lock() # Multiple read allowed
        self.num_read = 0

    def read_acquire(self):
        self.num_read_lock.acquire()
        self.num_read += 1
        if self.num_read == 1:
            self.write_lock.acquire()
        self.num_read_lock.release()

    def read_release(self):
        assert self.num_read > 0
        self.num_read_lock.acquire()
        self.num_read -= 1
        if self.num_read == 0:
            self.write_lock.release()
        self.num_read_lock.release()
    
    def write_acquire(self):
        self.write_lock.acquire()

    def write_release(self):
        self.write_lock.release()

    @contextmanager
    def read_locked(self):
        try:
            self.read_acquire()
            yield
        finally:
            self.read_release()

    @contextmanager
    def write_locked(self):
        try:
            self.write_acquire()
            yield
        finally:
            self.write_release()

