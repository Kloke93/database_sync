"""
Author: Tomas Dal Farra
Date: 25/12/2022
Description: Synchronized database class for threads and processes
"""
from file_database import FileDataBase
import threading
import multiprocessing
import logging


class SyncDataBase(FileDataBase):
    """
    Simple database thread/process synchronized
    """
    # All the not_reading event part was commented out because it didn't work.
    READERS_BOUND = 10
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)              # set the minimum logger level

    def __init__(self, mode, file_name="dbfile.bin"):
        """
        Initializer for synchronized database class
        :param mode: Takes a flag 1 or 0 where this means threading or multiprocessing correspondingly
        :param file_name: Name of file for the database
        """
        if mode != 0 and mode != 1:
            raise TypeError("Not Corresponding type")
        super().__init__(file_name)
        # self.counter_readers = 0                                      # readers count
        if mode:
            self.not_writing = threading.Event()                        # Event to check if there are writers
            self.to_write_lock = threading.Lock()                       # Lock to writers
            self.semaphore = threading.Semaphore(SyncDataBase.READERS_BOUND)    # Semaphore to limit readers
            # self.count_lock = threading.Lock()                        # Lock to change readers count
            # self.not_reading = threading.Event()                      # Event to check if there are readers
            # logging format
            formatter = logging.Formatter("[%(filename)s][%(threadName)s][%(asctime)s] %(message)s")
        else:                       # same attributes but in the multiprocessing module
            self.not_writing = multiprocessing.Event()
            self.to_write_lock = multiprocessing.Lock()
            self.semaphore = multiprocessing.Semaphore(10)
            # self.count_lock = multiprocessing.Lock()
            # self.not_reading = multiprocessing.Event()
            # logging format
            formatter = logging.Formatter("[%(filename)s][%(processName)s][%(asctime)s] %(message)s")
        # logger configuration
        file_handler = logging.FileHandler("file_database.log")         # file to save the log
        file_handler.setFormatter(formatter)
        SyncDataBase.logger.addHandler(file_handler)
        SyncDataBase.logger.info(f"Start in mode {mode}")
        # setting not-events
        self.not_writing.set()
        # self.not_reading.set()

    def set_value(self, key, val) -> bool:
        """
        Sets new key:value to database in file synchronized
        :param key: Key for the database
        :param val: Value of the key
        :return: If the operation was successful
        """
        self.to_write_lock.acquire()                        # blocks for writers
        self.not_writing.clear()                            # event: someone wants to write
        for i in range(10):                                 # fills all the semaphore buffer to write
            self.semaphore.acquire()
        try:
            # self.not_reading.wait()                         # waits for readers to finish
            is_set = super().set_value(key, val)
        except Exception as err:
            SyncDataBase.logger.error(f"Error setting key<{key}> to value<{val}>: {err}")
            raise err
        finally:
            for i in range(10):                             # releases all the semaphore buffer
                self.semaphore.release()
            self.not_writing.set()                          # event: stopped writing
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
        # self._update_counter(1)                           # increases reader counter
        self.semaphore.acquire()                            # acquires semaphore to read
        try:
            val = super().get_value(key)
        except Exception as err:
            SyncDataBase.logger.error(f"Error getting key<{key}>: {err}")
            raise err
        finally:
            self.semaphore.release()                        # releases semaphore
            # self._update_counter(-1)                      # decreases reader counter
        return val

    def delete_value(self, key):
        """
        Deletes value from database in file synchronized
        :param key: Key for a database value
        :return: Deleted value if existed
        """
        self.to_write_lock.acquire()                        # blocks for writers
        for i in range(10):                                 # fills all the semaphore buffer to write
            self.semaphore.acquire()
        try:
            # self.not_reading.wait()                       # event: someone wants to write
            self.not_writing.clear()                        # waits for readers to finish
            deleted = super().delete_value(key)
        except Exception as err:
            SyncDataBase.logger.error(f"Error deleting key<{key}>: {err}")
            raise err
        finally:
            for i in range(10):                             # releases all the semaphore buffer
                self.semaphore.release()
            self.not_writing.set()                          # event: stopped writing
            self.to_write_lock.release()                    # release for writers
        return deleted

    def _set_value_testing(self, key) -> bool:
        """ Special set_value modification to change previous value of key in dictionary by one"""
        self.to_write_lock.acquire()                        # blocks for writers
        self.not_writing.clear()                            # event: someone wants to write
        for i in range(10):                                 # fills all the semaphore buffer to write
            self.semaphore.acquire()
        try:
            # self.not_reading.wait()                       # waits for readers to finish
            val = super().get_value(key)
            is_set = super().set_value(key, val + 1)
        except Exception as err:
            SyncDataBase.logger.error(f"Error setting (test) key<{key}>: {err}")
            raise err
        finally:
            for i in range(10):                             # releases all the semaphore buffer
                self.semaphore.release()
            self.not_writing.set()                          # event: stopped writing
            self.to_write_lock.release()                    # release for writers
        return is_set

    # Didn't work. Ignore it
    # def _update_counter(self, factor: int):
    #     """
    #     Updates reading counter according to if reader will acquire or release
    #     :param factor: 1 if acquired and -1 if released
    #     """
    #     self.count_lock.acquire()
    #     try:
    #         self.counter_readers += factor
    #     finally:
    #         self.count_lock.release()
    #     if self.counter_readers:
    #         self.not_reading.clear()
    #     else:
    #         self.not_reading.set()
