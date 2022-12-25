"""
Author: Tomas Dal Farra
Date: 25/12/2022
Description: Defines a class where to handle a dictionary database within a file
"""
from dict_database import DataBase
import pickle
import os
import logging


class FileDataBase(DataBase):
    """
    File handling dictionary database
    """
    def __init__(self, file_name="dbfile.bin"):
        self.file_name = file_name
        super().__init__()
        if not self._non_zero_file(self.file_name):      # creates file with empty dictionary if it doesn't exist
            with open(self.file_name, 'wb') as f:
                pickle.dump({}, f)
                logging.debug("New database initialized")
        else:
            with open(self.file_name, 'rb') as f:
                self.db = pickle.load(f)
                logging.debug("Previous database content loaded")

    @staticmethod
    def _non_zero_file(file_path) -> bool:
        """
        Checks if a file exists and if it has any content
        :param file_path: path for file to check
        :return: if file meets the condition
        """
        try:
            return os.path.getsize(file_path) > 0
        except OSError:
            return False

    def set_value(self, key, val) -> bool:
        """
        Sets new key:value to database in file
        :param key: Key for the database
        :param val: Value of the key
        :return: If the operation was successful
        """
        try:
            with open(self.file_name, 'rb') as f:
                self.db = pickle.load(f)
            is_set = super().set_value(key, val)
            with open(self.file_name, 'wb') as f:
                pickle.dump(self.db, f)
            return is_set
        except Exception as err:
            logging.error(f"There was a problem to set value: {err}")
            raise err

    def get_value(self, key):
        """
        Gets value according to the key of the database in file
        If key doesn't exist None is returned
        :param key: Key for the database element
        :return: Value from the database if found
        """
        try:
            with open(self.file_name, 'rb') as f:
                self.db = pickle.load(f)
            return super().get_value(key)
        except Exception as err:
            logging.error(f"There was a problem to get value: {err}")
            raise err

    def delete_value(self, key):
        """
        Deletes value from database in file
        :param key: Key for a database value
        :return: Deleted value if existed
        """
        try:
            with open(self.file_name, 'rb') as f:
                self.db = pickle.load(f)
            val = super().delete_value(key)
            with open(self.file_name, 'wb') as f:
                pickle.dump(self.db, f)
            return val
        except Exception as err:
            logging.error(f"There was a problem to delete value: {err}")
            raise err

    def get_name(self) -> str:
        """
        Gets file name
        :return: file name
        """
        return self.file_name

    def __repr__(self):
        """
        Prints file name and then file dictionary
        :return: string description of the database
        """
        try:
            with open(self.file_name, "rb") as f:
                self.db = pickle.load(f)
        except Exception as err:
            logging.error(f"There was a problem trying to print database: {err}")
            raise err
        return f"{self.file_name}: " + super().__repr__()


if __name__ == "__main__":
    database = FileDataBase('testfile.bin')
    try:
        assert database.set_value('1', '2')
        assert database.set_value(1, '3')
        assert database.get_value(1) == '3'
        assert database.delete_value('1') == '2'
        assert database.get_value('1') is None
        assert database.delete_value('1') is None
        assert repr(database) == database.get_name() + ": {1: '3'}"
    finally:
        os.remove(database.get_name())
    # logging configuration just when running
    log_file = "file_database.log"                                                   # file to save the log
    log_level = logging.DEBUG                                                        # set the minimum logger level
    log_format = "[%(filename)s] - %(asctime)s - %(levelname)s - %(message)s"        # logging format
    logging.basicConfig(filename=log_file, level=log_level, format=log_format)
