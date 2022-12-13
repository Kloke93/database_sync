"""
Author: Tomas Dal Farra
Date:
Description:
"""


class DataBase:
    """
    Simple dictionary database
    """
    def __init__(self):
        self.db = {}

    def set_value(self, key, val):
        """
        Sets new key:value to database
        :param key: Key for the database
        :param val: Value of the key
        """
        self.db[key] = val

    def get_value(self, key):
        """
        Gets value according to the key of the database
        If key doesn't exist None is returned
        :param key: Key for the database element
        :return: Value from the database if found
        """
        return self.db.get(key)

    def delete_value(self, key):
        """
        Deletes value from database
        :param key: Key for a database value
        :return: Deleted value if existed
        """
        return self.db.pop(key, None)

    def __str__(self):
        """
        Prints dictionary database
        :return: string description of the database
        """
        return str(self.db)


if __name__ == "__main__":
    pass
