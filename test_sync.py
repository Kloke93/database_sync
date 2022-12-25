"""
Author: Tomas Dal Farra
Date: 25/12/2022
Description: Test file for threading and multiprocessing synchronized
"""
from sync_database import SyncDataBase
import multiprocessing
import threading
import unittest
import pickle
import os


class TestThreadDB(unittest.TestCase):
    """ Class to test synchronized database in threading mode """
    test_fname = "testfile.bin"
    reps = 100

    def set_value(self, key, val):
        """ Test set_value method """
        for _ in range(TestThreadDB.reps):
            self.assertTrue(self.sync_db.set_value(key, val))

    def get_value(self, key):
        """ Test get_value method """
        for _ in range(TestThreadDB.reps):
            self.assertEqual(self.sync_db.get_value(key), key * 100)

    def delete_value(self, key):
        """ Test delete_value method """
        self.assertEqual(self.sync_db.delete_value(key), key * 100)
        for _ in range(TestThreadDB.reps - 1):
            self.assertIsNone(self.sync_db.delete_value(key))

    @staticmethod
    def get_database_dict():
        """
        Gets the database dictionary
        :return: Dictionary from file
        """
        with open(TestThreadDB.test_fname, "rb") as f:
            db = pickle.load(f)
        return db

    def setUp(self):
        """
        sets up the testing file with a specific dictionary and creates an instance of the database
        """
        self.test_dict = {n: n * 100 for n in range(1, 51)}
        with open(TestThreadDB.test_fname, "wb") as f:
            pickle.dump(self.test_dict, f)
        self.sync_db = SyncDataBase(1, "testfile.bin")

    def test_write_simple(self):
        thread = threading.Thread(target=self.set_value, name="thread_ws", args=(40, 4002))
        thread.start()
        thread.join()
        self.test_dict[40] = 4002
        self.assertEqual(self.get_database_dict(), self.test_dict)

    def test_read_simple(self):
        thread = threading.Thread(target=self.get_value, name="thread_ws", args=(40,))
        thread.start()
        thread.join()
        self.assertEqual(self.get_database_dict(), self.test_dict)

    def test_write_waits(self):
        pass

    def test_read_waits(self):
        pass

    def tearDown(self):
        """
        Deletes the testing file
        """
        os.remove("testfile.bin")


class TestProcessDB(unittest.TestCase):
    """ Class to test synchronized database in multiprocessing mode """
    test_fname = "testfile.bin"

    @staticmethod
    def get_database_dict():
        """
        Gets the database dictionary
        :return: Dictionary from file
        """
        with open(TestProcessDB.test_fname, "rb") as f:
            db = pickle.load(f)
        return db

    def setUp(self):
        """
        sets up the testing file with a specific dictionary and creates an instance of the database
        """
        self.test_dict = {n: n * 100 for n in range(1, 51)}
        with open(TestProcessDB.test_fname, "wb") as f:
            pickle.dump(self.test_dict, f)
        self.sync_db = SyncDataBase(1, "testfile.bin")

    def test_a(self):
        pass

    def tearDown(self):
        """
        Deletes the testing file
        """
        os.remove("testfile.bin")


if __name__ == "__main__":
    unittest.main()
