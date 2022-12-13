"""
Author: Tomas Dal Farra
Date:
Description:
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
        if not self.non_zero_file(self.file_name):      # creates file with empty dictionary if it doesn't exist
            with open(self.file_name, 'wb') as f:
                pickle.dump({}, f)
                logging.debug("New database initialized")
        else:
            with open(self.file_name, 'rb') as f:
                self.db = pickle.load(f)
                logging.debug("Previous database content loaded")

    @staticmethod
    def non_zero_file(file_path) -> bool:
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
            super().set_value(key, val)
            with open(self.file_name, 'wb') as f:
                pickle.dump(self.db, f)
            return True
        except Exception as err:
            logging.error(f"There was a problem to set value: {err}")
            # return False
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
            # return None
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

    def __str__(self):
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
        return f"{self.file_name}: " + super().__str__()


def main():
    database = DataBase()
    database.set_value('1', '2')
    database.set_value(1, '3')
    database.delete_value('1')


if __name__ == "__main__":
    main()
