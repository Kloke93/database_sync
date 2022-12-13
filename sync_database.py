"""
Author: Tomas Dal Farra
Date:
Description:
"""
from file_database import FileDataBase
import threading
import multiprocessing


class SyncDataBase(FileDataBase):
    """
    Simple database thread/process synchronized
    """
    READERS_BOUND = 10

    def __init__(self, mode, file_name="dbfile.bin"):
        if mode != 0 or mode != 1:
            raise TypeError("Not Corresponding type")
        super().__init__(file_name)
        self.counter_readers = 0                 # readers count
        if mode:
            self.not_reading = threading.Event()                    # Event to check if there are readers
            self.not_writing = threading.Event()                    # Event to check if there are writers
            self.count_lock = threading.Lock()                      # Lock to change readers count
            self.to_write_lock = threading.Lock()                   # Lock to writers
            self.readers_semaphore = threading.Semaphore(SyncDataBase.READERS_BOUND)    # Semaphore to limit readers
        else:                       # same attributes but in the multiprocessing module
            self.not_reading = multiprocessing.Event()
            self.not_writing = multiprocessing.Event()
            self.count_lock = multiprocessing.Lock()
            self.to_write_lock = multiprocessing.Lock()
            self.readers_semaphore = multiprocessing.Semaphore(10)

    def _update_counter(self, factor: int):
        """
        Updates reading counter according to if reader acquired or released
        :param factor: 1 if acquired and -1 if released
        """
        self.count_lock.acquire()
        try:
            self.counter_readers += factor
        finally:
            self.count_lock.release()
        if self.counter_readers:
            self.not_reading.clear()
        else:
            self.not_reading.set()

    def set_value(self, key, val) -> bool:
        """
        Sets new key:value to database in file synchronized
        :param key: Key for the database
        :param val: Value of the key
        :return: If the operation was successful
        """
        self.to_write_lock.acquire()                        # blocks for writers
        try:
            self.not_writing.clear()                        # event: someone wants to write
            self.not_reading.wait()                         # waits for readers to finish
            is_set = super().set_value(key, val)
            self.not_writing.set()                          # event: stopped writing
        finally:
            self.to_write_lock.release()                    # release for writers
        return is_set

    def get_value(self, key):
        """
        Gets value according to the key of the database in file synchronized
        If key doesn't exist None is returned
        :param key: Key for the database element
        :return: Value from the database if found
        """
        self.not_writing.wait()                             # wait for writer to finish
        self.readers_semaphore.acquire()                    # acquires semaphore to read
        self._update_counter(1)                             # increases reader counter
        try:
            val = super().get_value(key)
        finally:
            self.readers_semaphore.release()                # releases semaphore
            self._update_counter(-1)                        # decreases reader counter
        return val

    def delete_value(self, key):
        """
        Deletes value from database in file synchronized
        :param key: Key for a database value
        :return: Deleted value if existed
        """
        self.to_write_lock.acquire()                        # blocks for writers
        try:
            self.not_reading.wait()                         # event: someone wants to write
            self.not_writing.clear()                        # waits for readers to finish
            deleted = super().delete_value(key)
            self.not_writing.set()                          # event: stopped writing
        finally:
            self.to_write_lock.release()                    # release for writers
        return deleted


def main():
    # db = SyncDataBase(1)
    # db
    pass


if __name__ == "__main__":
    main()
